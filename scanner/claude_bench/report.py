"""Output formatting — terminal, verbose, and JSON modes."""

from __future__ import annotations

import json
from claude_bench import __version__
from claude_bench.rubric import MAX_SCORES
from claude_bench.scanner import ScanResult

BAR_WIDTH = 15
BOX_INNER = 36


def _bar(score: int, max_score: int) -> str:
    filled = round(BAR_WIDTH * score / max_score) if max_score > 0 else 0
    empty = BAR_WIDTH - filled
    return "\u2588" * filled + "\u2591" * empty


def _pad_right(text: str, width: int) -> str:
    return text + " " * max(0, width - len(text))


def print_terminal(scores: dict[str, int]) -> None:
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
    print("\n--- Detailed Breakdown ---\n")

    def _yn(val: bool, pts: str) -> str:
        return f"{'yes' if val else 'MISSING'} ({pts})"

    print(f"AGENTS ({scores['agents']}/{MAX_SCORES['agents']})")
    print(f"  Agent count: {result.agent_count} ({min(result.agent_count // 10, 6)}pt)")
    tiers = len(result.model_tiers)
    tier_pts = 2 if tiers >= 3 else 1 if tiers >= 2 else 0
    print(f"  Model tiers: {sorted(result.model_tiers) if result.model_tiers else 'none'} ({tier_pts}pt)")
    print(f"  Tool scoping: {_yn(result.has_tool_scoping, '4pt')}")
    print(f"  Per-agent memory: {_yn(result.has_per_agent_memory, '3pt')}")

    print(f"\nQUALITY ({scores['quality']}/{MAX_SCORES['quality']})")
    print(f"  Review pipeline: {'yes' if result.has_review_pipeline else 'MISSING'}")
    print(f"  Review stages: {result.review_stages}")
    print(f"  Acceptance criteria: {_yn(result.has_acceptance_criteria, '2pt')}")
    print(f"  TDD: {_yn(result.has_tdd, '2pt')}")
    print(f"  Deviation protocol: {_yn(result.has_deviation_protocol, '1pt')}")
    print(f"  CI/CD config: {_yn(result.has_ci_config, '2pt')}")
    print(f"  Test suite: {_yn(result.has_test_suite, '2pt')}")

    print(f"\nAUTONOMY ({scores['autonomy']}/{MAX_SCORES['autonomy']})")
    print(f"  Crash recovery: {_yn(result.has_crash_recovery, '3pt')}")
    print(f"  Stall detection: {_yn(result.has_stall_detection, '2pt')}")
    print(f"  Parallel orchestration: {_yn(result.has_parallel_orchestration, '3pt')}")
    print(f"  Self-improvement: {_yn(result.has_self_improvement, '2pt')}")
    print(f"  Session chaining: {_yn(result.has_session_chaining, '2pt')}")
    print(f"  Cost tracking: {_yn(result.has_cost_tracking, '3pt')}")

    print(f"\nSAFETY ({scores['safety']}/{MAX_SCORES['safety']})")
    print(f"  Hook count: {result.hook_count} ({min(result.hook_count // 3, 3)}pt)")
    print(f"  Destructive blocking: {_yn(result.has_destructive_blocking, '3pt')}")
    print(f"  Scope enforcement: {_yn(result.has_scope_enforcement, '3pt')}")
    print(f"  Memory protection: {_yn(result.has_memory_protection, '2pt')}")
    print(f"  Secrets scanning: {_yn(result.has_secrets_scanning, '2pt')}")
    print(f"  Rate limiting: {_yn(result.has_rate_limiting, '2pt')}")

    print(f"\nMEMORY ({scores['memory']}/{MAX_SCORES['memory']})")
    print(f"  Session persistence: {_yn(result.has_session_persistence, '2pt')}")
    print(f"  Structured handoffs: {_yn(result.has_structured_handoffs, '2pt')}")
    print(f"  Learning extraction: {_yn(result.has_learning_extraction, '2pt')}")
    print(f"  Pre-compact save: {_yn(result.has_pre_compact_save, '2pt')}")
    print(f"  Lessons system: {_yn(result.has_lessons_system, '1pt')}")
    print(f"  Semantic search: {_yn(result.has_semantic_search, '1pt')}")

    print(f"\nSKILLS ({scores['skills']}/{MAX_SCORES['skills']})")
    print(f"  Skill count: {result.skill_count} ({min(result.skill_count // 7, 4)}pt)")
    print(f"  Frontmatter: {_yn(result.has_skill_frontmatter, '3pt')}")
    print(f"  Trigger definitions: {_yn(result.has_trigger_definitions, '3pt')}")

    print(f"\nINFRA ({scores['infra']}/{MAX_SCORES['infra']})")
    print(f"  MCP servers: {result.mcp_count} ({min(result.mcp_count // 4, 4)}pt)")
    print(f"  Scripts: {result.script_count} ({'2pt' if result.script_count >= 5 else '1pt' if result.script_count > 0 else '0pt'})")
    print(f"  Templates: {_yn(result.has_templates, '2pt')}")
    print(f"  Deploy automation: {_yn(result.has_deploy_automation, '2pt')}")

    print(f"\nSECURITY ({scores['security']}/{MAX_SCORES['security']})")
    print(f"  Pentest tooling: {_yn(result.has_pentest_tooling, '2pt')}")
    print(f"  Attack playbooks: {_yn(result.has_attack_playbooks, '1pt')}")
    print(f"  Scheduled scans: {_yn(result.has_scheduled_scans, '1pt')}")
    print(f"  Delta reporting: {_yn(result.has_delta_reporting, '1pt')}")

    print(f"\nDOMAIN ({scores['domain']}/{MAX_SCORES['domain']})")
    print(f"  Specialisation: {'yes \u2014 ' + result.domain_detected if result.has_domain_specialisation else 'MISSING'} (3pt)")
    print(f"  Custom pipelines: {_yn(result.has_custom_pipelines, '2pt')}")


def build_json(scores: dict[str, int], result: ScanResult, scanned_path: str) -> dict:
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
    data = build_json(scores, result, scanned_path)
    print(json.dumps(data, indent=2))
