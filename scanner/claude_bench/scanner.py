"""Core detection logic — walks a target directory and detects Claude Code setup features."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ScanResult:
    # Agents
    agent_count: int = 0
    has_tool_scoping: bool = False
    model_tiers: set[str] = field(default_factory=set)
    has_per_agent_memory: bool = False

    # Quality
    has_review_pipeline: bool = False
    review_stages: int = 0
    has_acceptance_criteria: bool = False
    has_tdd: bool = False
    has_deviation_protocol: bool = False

    # Autonomy
    has_crash_recovery: bool = False
    has_stall_detection: bool = False
    has_parallel_orchestration: bool = False
    has_self_improvement: bool = False
    has_session_chaining: bool = False

    # Safety
    hook_count: int = 0
    has_destructive_blocking: bool = False
    has_scope_enforcement: bool = False
    has_memory_protection: bool = False
    has_secrets_scanning: bool = False

    # Memory
    has_session_persistence: bool = False
    has_structured_handoffs: bool = False
    has_learning_extraction: bool = False
    has_pre_compact_save: bool = False
    has_lessons_system: bool = False

    # Skills
    skill_count: int = 0
    has_skill_frontmatter: bool = False
    has_trigger_definitions: bool = False

    # Infra
    mcp_count: int = 0
    script_count: int = 0
    has_templates: bool = False
    has_deploy_automation: bool = False

    # Security
    has_pentest_tooling: bool = False
    has_attack_playbooks: bool = False
    has_scheduled_scans: bool = False
    has_delta_reporting: bool = False

    # Domain
    has_domain_specialisation: bool = False
    domain_detected: str = ""
    has_custom_pipelines: bool = False


def _file_contains_keywords(path: Path, keywords: list[str], max_lines: int = 50) -> bool:
    """Check if file contains any of the keywords in the first N lines."""
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            text = ""
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                text += line
        text_lower = text.lower()
        return any(kw.lower() in text_lower for kw in keywords)
    except (OSError, UnicodeDecodeError):
        return False


def _file_heading_matches(path: Path, keywords: list[str], max_lines: int = 50) -> bool:
    """Check if file contains a markdown heading matching any keyword."""
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                stripped = line.strip().lower()
                if stripped.startswith("#"):
                    if any(kw.lower() in stripped for kw in keywords):
                        return True
        return False
    except (OSError, UnicodeDecodeError):
        return False


def _count_hooks(path: Path) -> tuple[int, bool, bool, bool]:
    """Parse hooks.json and return (hook_count, has_destructive_blocking, has_scope_enforcement, has_memory_protection).

    Supports multiple formats:
    - {"hooks": {"EventName": [...]}}  (Claude Code native format)
    - {"EventName": [...]}             (flat format)
    - [...]                            (list format)

    Each event array contains matcher entries, each with a nested "hooks" list of
    individual hook definitions. We count the individual hooks and scan their content.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return 0, False, False, False

    hook_count = 0
    has_destructive = False
    has_scope = False
    has_memory = False

    DESTRUCTIVE_KW = ["destructive", "block", "danger", "rm ", "rm -", "force", "blocked"]
    SCOPE_KW = ["scope", "permission", "enforce"]
    MEMORY_KW = ["inject", "saniti", "quarantine", "memory"]

    def _check_hook_str(hook_str: str) -> None:
        nonlocal has_destructive, has_scope, has_memory
        if any(kw in hook_str for kw in DESTRUCTIVE_KW):
            has_destructive = True
        if any(kw in hook_str for kw in SCOPE_KW):
            has_scope = True
        if any(kw in hook_str for kw in MEMORY_KW):
            has_memory = True

    def _process_event_entries(entries: list) -> None:
        """Process an array of matcher entries for one event type."""
        nonlocal hook_count
        for entry in entries:
            if isinstance(entry, dict):
                # Each entry may have a nested "hooks" list of individual hooks
                inner_hooks = entry.get("hooks", [])
                if isinstance(inner_hooks, list) and inner_hooks:
                    hook_count += len(inner_hooks)
                    for ih in inner_hooks:
                        s = json.dumps(ih).lower() if isinstance(ih, dict) else str(ih).lower()
                        _check_hook_str(s)
                else:
                    # Entry itself is a hook definition
                    hook_count += 1
                    s = json.dumps(entry).lower()
                    _check_hook_str(s)
            else:
                hook_count += 1

    if not isinstance(data, dict):
        if isinstance(data, list):
            _process_event_entries(data)
        return hook_count, has_destructive, has_scope, has_memory

    # Unwrap {"hooks": {...}} wrapper if present
    events = data.get("hooks", data) if "hooks" in data and isinstance(data["hooks"], dict) else data

    for _event, entries in events.items():
        if isinstance(entries, list):
            _process_event_entries(entries)
        elif isinstance(entries, dict):
            _process_event_entries([entries])

    return hook_count, has_destructive, has_scope, has_memory


def _count_mcp_servers(path: Path) -> int:
    """Count MCP server entries in .mcp.json or .mcp.json.template."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return 0

    if isinstance(data, dict):
        servers = data.get("mcpServers", data.get("servers", {}))
        if isinstance(servers, dict):
            return len(servers)
    return 0


def _detect_model_tiers(path: Path, max_lines: int = 50) -> set[str]:
    """Detect model tier mentions in first N lines of a file."""
    tiers: set[str] = set()
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            text = ""
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                text += line
        text_lower = text.lower()
        if "haiku" in text_lower:
            tiers.add("haiku")
        if "sonnet" in text_lower:
            tiers.add("sonnet")
        if "opus" in text_lower:
            tiers.add("opus")
    except (OSError, UnicodeDecodeError):
        pass
    return tiers


def _detect_domain(names: list[str]) -> tuple[bool, str]:
    """Detect domain specialisation from file/directory names."""
    names_lower = " ".join(n.lower() for n in names)

    domains: list[tuple[str, list[str]]] = [
        ("ML/Quant", ["trading", "quant", "backtest", "portfolio", "risk_engine", "macro", "deribit"]),
        ("ML", ["ml", "model-train", "training", "inference"]),
        ("DevOps", ["deploy", "infra", "ci-cd", "monitoring"]),
        ("Security", ["pentest", "attack", "vulnerability", "exploit"]),
    ]

    for domain_name, keywords in domains:
        if any(kw in names_lower for kw in keywords):
            return True, domain_name
    return False, ""


def _has_yaml_frontmatter(path: Path) -> bool:
    """Check if a file starts with YAML frontmatter (---)."""
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            first_line = f.readline().strip()
            return first_line == "---"
    except (OSError, UnicodeDecodeError):
        return False


def _has_trigger_in_frontmatter(path: Path) -> bool:
    """Check if YAML frontmatter contains trigger or description fields."""
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            lines = []
            first = f.readline().strip()
            if first != "---":
                return False
            for line in f:
                if line.strip() == "---":
                    break
                lines.append(line.lower())
            text = "".join(lines)
            return "trigger" in text or "description" in text
    except (OSError, UnicodeDecodeError):
        return False


def scan_directory(target: Path) -> ScanResult:
    """Scan a directory and detect Claude Code setup features."""
    result = ScanResult()

    if not target.is_dir():
        return result

    # --- Agents ---
    agent_dir = target / ".claude" / "agents"
    agent_files: list[Path] = []
    if agent_dir.is_dir():
        agent_files = sorted(agent_dir.glob("*.md"))
        result.agent_count = len(agent_files)
        for af in agent_files:
            if _file_heading_matches(af, ["Allowed Tools"]):
                result.has_tool_scoping = True
            result.model_tiers |= _detect_model_tiers(af)

    result.has_per_agent_memory = (target / "memory" / "agents").is_dir()

    # Also check rules for model tier mentions
    rules_dir = target / ".claude" / "rules"
    if rules_dir.is_dir():
        for rf in rules_dir.glob("*.md"):
            result.model_tiers |= _detect_model_tiers(rf)

    # --- Quality ---
    all_md_files: list[Path] = []
    skills_dir = target / "skills"
    if skills_dir.is_dir():
        all_md_files.extend(skills_dir.rglob("*.md"))
    if agent_dir.is_dir():
        all_md_files.extend(agent_files)
    if rules_dir.is_dir():
        all_md_files.extend(rules_dir.glob("*.md"))
    claude_md = target / "CLAUDE.md"
    if claude_md.is_file():
        all_md_files.append(claude_md)

    review_keywords = ["review", "veto", "qa-reviewer", "quality"]
    review_stage_keywords = ["spec compliance", "code quality", "output intent", "l1a", "l1b", "l2"]
    stages_found: set[str] = set()

    for md in all_md_files:
        if _file_contains_keywords(md, review_keywords):
            result.has_review_pipeline = True
        for sk in review_stage_keywords:
            if _file_contains_keywords(md, [sk]):
                stages_found.add(sk)
        if _file_contains_keywords(md, ["acceptance"]):
            result.has_acceptance_criteria = True
        if _file_contains_keywords(md, ["tdd", "test-driven"]):
            result.has_tdd = True
        if _file_contains_keywords(md, ["deviation"]):
            result.has_deviation_protocol = True

    result.review_stages = len(stages_found)

    # --- Autonomy ---
    scripts_dir = target / "scripts"
    script_files: list[Path] = []
    if scripts_dir.is_dir():
        script_files = [
            f for f in scripts_dir.iterdir()
            if f.is_file() and f.suffix in (".sh", ".py", ".js", ".ts")
        ]

    autonomy_files = list(all_md_files) + script_files
    for af in autonomy_files:
        if _file_contains_keywords(af, ["recovery", "crash", "flow protocol", "re-launch"]):
            result.has_crash_recovery = True
        if _file_contains_keywords(af, ["stall"]):
            result.has_stall_detection = True
        if _file_contains_keywords(af, ["parallel"]):
            result.has_parallel_orchestration = True
        if _file_contains_keywords(af, ["self-improvement", "self_improvement", "hone", "learn"]):
            result.has_self_improvement = True
        if _file_contains_keywords(af, ["flow", "chain", "session"]):
            result.has_session_chaining = True

    # Also check hooks scripts
    hooks_scripts_dir = target / "hooks" / "scripts"
    if hooks_scripts_dir.is_dir():
        for hs in hooks_scripts_dir.iterdir():
            if hs.is_file():
                if _file_contains_keywords(hs, ["stall"]):
                    result.has_stall_detection = True

    # --- Safety ---
    hooks_json = target / "hooks" / "hooks.json"
    settings_hooks = target / ".claude" / "settings.json"

    if hooks_json.is_file():
        hcount, h_destr, h_scope, h_mem = _count_hooks(hooks_json)
        result.hook_count += hcount
        result.has_destructive_blocking = result.has_destructive_blocking or h_destr
        result.has_scope_enforcement = result.has_scope_enforcement or h_scope
        result.has_memory_protection = result.has_memory_protection or h_mem

    if settings_hooks.is_file():
        hcount, h_destr, h_scope, h_mem = _count_hooks(settings_hooks)
        result.hook_count += hcount
        result.has_destructive_blocking = result.has_destructive_blocking or h_destr
        result.has_scope_enforcement = result.has_scope_enforcement or h_scope
        result.has_memory_protection = result.has_memory_protection or h_mem

    # Check rules for safety keywords
    for md in all_md_files:
        if _file_contains_keywords(md, ["scope", "permission", "enforce", "tool scoping"]):
            result.has_scope_enforcement = True
        if _file_contains_keywords(md, ["injection", "saniti", "quarantine"]):
            result.has_memory_protection = True
        if _file_contains_keywords(md, ["secret", "scan", "hardcoded"]):
            result.has_secrets_scanning = True

    # --- Memory ---
    result.has_session_persistence = (target / "memory" / "sessions").is_dir()
    sessions_dir = target / "memory" / "sessions"
    if sessions_dir.is_dir():
        has_latest = (sessions_dir / "latest.md").is_file()
        has_precompact = (sessions_dir / "pre-compact-snapshot.md").is_file()
        result.has_structured_handoffs = has_latest or has_precompact

    result.has_learning_extraction = (target / "memory" / "learn").is_dir()
    result.has_lessons_system = (target / "memory" / "lessons.md").is_file()

    # Pre-compact save detection
    for md in all_md_files:
        if _file_contains_keywords(md, ["pre-compact", "compaction"]):
            result.has_pre_compact_save = True
            break
    if hooks_scripts_dir.is_dir():
        for hs in hooks_scripts_dir.iterdir():
            if hs.is_file() and _file_contains_keywords(hs, ["pre-compact", "compaction", "pre_compact"]):
                result.has_pre_compact_save = True

    # --- Skills ---
    if skills_dir.is_dir():
        skill_files = sorted(skills_dir.glob("*/SKILL.md"))
        result.skill_count = len(skill_files)
        for sf in skill_files:
            if _has_yaml_frontmatter(sf):
                result.has_skill_frontmatter = True
            if _has_trigger_in_frontmatter(sf):
                result.has_trigger_definitions = True

    # --- Infra ---
    mcp_json = target / ".mcp.json"
    mcp_template = target / ".mcp.json.template"
    if mcp_json.is_file():
        result.mcp_count = _count_mcp_servers(mcp_json)
    elif mcp_template.is_file():
        result.mcp_count = _count_mcp_servers(mcp_template)

    result.script_count = len(script_files)
    result.has_templates = (target / "templates").is_dir()

    deploy_files = list(all_md_files) + script_files
    for df in deploy_files:
        if _file_contains_keywords(df, ["deploy"]):
            result.has_deploy_automation = True
            break

    # --- Security ---
    result.has_pentest_tooling = (target / "pentest").is_dir() or (target / "tools" / "pentest").is_dir()
    attack_skill = target / "skills" / "attack"
    result.has_attack_playbooks = attack_skill.is_dir() or (target / "attack").is_dir()

    # Scheduled scans
    for md in all_md_files:
        if _file_contains_keywords(md, ["scheduled scan", "cron", "audit"]):
            result.has_scheduled_scans = True
            break

    # Delta reporting
    for f in script_files + list(all_md_files):
        if _file_contains_keywords(f, ["delta", "diff report"]):
            result.has_delta_reporting = True
            break

    # --- Domain ---
    all_names: list[str] = []
    if agent_dir.is_dir():
        all_names.extend(f.stem for f in agent_files)
    if scripts_dir.is_dir():
        all_names.extend(f.stem for f in script_files)
    tools_dir = target / "tools"
    if tools_dir.is_dir():
        all_names.extend(f.stem for f in tools_dir.iterdir() if f.is_file())
    if skills_dir.is_dir():
        all_names.extend(d.name for d in skills_dir.iterdir() if d.is_dir())

    result.has_domain_specialisation, result.domain_detected = _detect_domain(all_names)

    # Custom pipelines
    if tools_dir.is_dir() and any(
        _file_contains_keywords(f, ["pipeline", "ingest", "extract", "transform"])
        for f in tools_dir.iterdir() if f.is_file() and f.suffix in (".py", ".sh")
    ):
        result.has_custom_pipelines = True

    return result
