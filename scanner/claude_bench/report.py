"""Output formatting — terminal, verbose, and JSON modes."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from claude_bench import __version__
from claude_bench.rubric import MAX_SCORES
from claude_bench.scanner import ScanResult

# Bar width inside the box (number of block characters)
BAR_WIDTH = 15
BOX_INNER = 36


def _bar(score: int, max_score: int) -> str:
    """Render a proportional progress bar."""
    filled = round(BAR_WIDTH * score / max_score) if max_score > 0 else 0
    empty = BAR_WIDTH - filled
    return "\u2588" * filled + "\u2591" * empty


def _pad_right(text: str, width: int) -> str:
    """Pad text to width, accounting for Unicode characters."""
    visible_len = len(text)
    return text + " " * max(0, width - visible_len)


def print_terminal(scores: dict[str, int]) -> None:
    """Print the score box to the terminal."""
    overall = scores["overall"]

    dimensions = [
        ("Agents", "agents"),
        ("Quality", "quality"),
        ("Autonomy", "autonomy"),
        ("Safety", "safety"),
        ("Memory", "memory"),
        ("Skills", "skills"),
        ("Infra", "infra"),
        ("Security", "security"),
        ("Domain", "domain"),
    ]

    print(f"\u2554{'\u2550' * BOX_INNER}\u2557")
    print(f"\u2551{_pad_right('         CLAUDE BENCH  v1.0', BOX_INNER)}\u2551")
    print(f"\u2560{'\u2550' * BOX_INNER}\u2563")
    print(f"\u2551{_pad_right(f'  Overall Score:  {overall} / 100', BOX_INNER)}\u2551")
    print(f"\u2560{'\u2550' * BOX_INNER}\u2563")

    for label, key in dimensions:
        score = scores[key]
        max_s = MAX_SCORES[key]
        bar = _bar(score, max_s)
        score_str = f"{score}/{max_s}"
        line = f"  {label:<10}{bar}  {score_str:>5}"
        print(f"\u2551{_pad_right(line, BOX_INNER)}\u2551")

    print(f"\u2560{'\u2550' * BOX_INNER}\u2563")
    print(f"\u2551{_pad_right('  Submit: claude-bench --submit', BOX_INNER)}\u2551")
    print(f"\u255a{'\u2550' * BOX_INNER}\u255d")


def print_verbose(scores: dict[str, int], result: ScanResult) -> None:
    """Print detailed breakdown per dimension."""
    print("\n--- Detailed Breakdown ---\n")

    # Agents
    print(f"AGENTS ({scores['agents']}/{MAX_SCORES['agents']})")
    print(f"  Agent count: {result.agent_count} ({min(result.agent_count // 5, 5)}pt)")
    print(f"  Model tiers: {sorted(result.model_tiers) if result.model_tiers else 'none'} ({min(len(result.model_tiers), 3)}pt)")
    print(f"  Tool scoping: {'yes' if result.has_tool_scoping else 'MISSING'} (4pt)")
    print(f"  Per-agent memory: {'yes' if result.has_per_agent_memory else 'MISSING'} (3pt)")

    # Quality
    print(f"\nQUALITY ({scores['quality']}/{MAX_SCORES['quality']})")
    print(f"  Review pipeline: {'yes' if result.has_review_pipeline else 'MISSING'}")
    print(f"  Review stages: {result.review_stages}")
    print(f"  Acceptance criteria: {'yes' if result.has_acceptance_criteria else 'MISSING'} (3pt)")
    print(f"  TDD: {'yes' if result.has_tdd else 'MISSING'} (2pt)")
    print(f"  Deviation protocol: {'yes' if result.has_deviation_protocol else 'MISSING'} (2pt)")

    # Autonomy
    print(f"\nAUTONOMY ({scores['autonomy']}/{MAX_SCORES['autonomy']})")
    print(f"  Crash recovery: {'yes' if result.has_crash_recovery else 'MISSING'} (4pt)")
    print(f"  Stall detection: {'yes' if result.has_stall_detection else 'MISSING'} (3pt)")
    print(f"  Parallel orchestration: {'yes' if result.has_parallel_orchestration else 'MISSING'} (3pt)")
    print(f"  Self-improvement: {'yes' if result.has_self_improvement else 'MISSING'} (3pt)")
    print(f"  Session chaining: {'yes' if result.has_session_chaining else 'MISSING'} (2pt)")

    # Safety
    print(f"\nSAFETY ({scores['safety']}/{MAX_SCORES['safety']})")
    print(f"  Hook count: {result.hook_count} ({min(result.hook_count // 2, 5)}pt)")
    print(f"  Destructive blocking: {'yes' if result.has_destructive_blocking else 'MISSING'} (3pt)")
    print(f"  Scope enforcement: {'yes' if result.has_scope_enforcement else 'MISSING'} (3pt)")
    print(f"  Memory protection: {'yes' if result.has_memory_protection else 'MISSING'} (2pt)")
    print(f"  Secrets scanning: {'yes' if result.has_secrets_scanning else 'MISSING'} (2pt)")

    # Memory
    print(f"\nMEMORY ({scores['memory']}/{MAX_SCORES['memory']})")
    print(f"  Session persistence: {'yes' if result.has_session_persistence else 'MISSING'} (3pt)")
    print(f"  Structured handoffs: {'yes' if result.has_structured_handoffs else 'MISSING'} (2pt)")
    print(f"  Learning extraction: {'yes' if result.has_learning_extraction else 'MISSING'} (2pt)")
    print(f"  Pre-compact save: {'yes' if result.has_pre_compact_save else 'MISSING'} (2pt)")
    print(f"  Lessons system: {'yes' if result.has_lessons_system else 'MISSING'} (1pt)")

    # Skills
    print(f"\nSKILLS ({scores['skills']}/{MAX_SCORES['skills']})")
    print(f"  Skill count: {result.skill_count} ({min(result.skill_count // 3, 4)}pt)")
    print(f"  Frontmatter: {'yes' if result.has_skill_frontmatter else 'MISSING'} (3pt)")
    print(f"  Trigger definitions: {'yes' if result.has_trigger_definitions else 'MISSING'} (3pt)")

    # Infra
    print(f"\nINFRA ({scores['infra']}/{MAX_SCORES['infra']})")
    print(f"  MCP servers: {result.mcp_count} ({min(result.mcp_count // 3, 4)}pt)")
    print(f"  Scripts: {result.script_count} ({'2pt' if result.script_count >= 5 else '1pt' if result.script_count > 0 else '0pt'})")
    print(f"  Templates: {'yes' if result.has_templates else 'MISSING'} (2pt)")
    print(f"  Deploy automation: {'yes' if result.has_deploy_automation else 'MISSING'} (2pt)")

    # Security
    print(f"\nSECURITY ({scores['security']}/{MAX_SCORES['security']})")
    print(f"  Pentest tooling: {'yes' if result.has_pentest_tooling else 'MISSING'} (2pt)")
    print(f"  Attack playbooks: {'yes' if result.has_attack_playbooks else 'MISSING'} (1pt)")
    print(f"  Scheduled scans: {'yes' if result.has_scheduled_scans else 'MISSING'} (1pt)")
    print(f"  Delta reporting: {'yes' if result.has_delta_reporting else 'MISSING'} (1pt)")

    # Domain
    print(f"\nDOMAIN ({scores['domain']}/{MAX_SCORES['domain']})")
    print(f"  Specialisation: {'yes — ' + result.domain_detected if result.has_domain_specialisation else 'MISSING'} (3pt)")
    print(f"  Custom pipelines: {'yes' if result.has_custom_pipelines else 'MISSING'} (2pt)")


def build_json(scores: dict[str, int], result: ScanResult, scanned_path: str) -> dict:
    """Build the JSON output dict."""
    dimensions = {k: v for k, v in scores.items() if k != "overall"}
    return {
        "version": __version__,
        "scanner_version": __version__,
        "overall": scores["overall"],
        "dimensions": dimensions,
        "max_scores": MAX_SCORES,
        "metadata": {
            "agent_count": result.agent_count,
            "skill_count": result.skill_count,
            "hook_count": result.hook_count,
            "mcp_count": result.mcp_count,
            "model_tiers": sorted(result.model_tiers),
            "domain_detected": result.domain_detected or "none",
            "scanned_path": scanned_path,
        },
    }


def print_json(scores: dict[str, int], result: ScanResult, scanned_path: str) -> None:
    """Print JSON output."""
    data = build_json(scores, result, scanned_path)
    print(json.dumps(data, indent=2))
