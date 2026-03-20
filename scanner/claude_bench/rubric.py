"""Scoring logic — pure functions that take a ScanResult and return dimension scores."""

from __future__ import annotations

from claude_bench.scanner import ScanResult

MAX_SCORES: dict[str, int] = {
    "agents": 15,
    "quality": 15,
    "autonomy": 15,
    "safety": 15,
    "memory": 10,
    "skills": 10,
    "infra": 10,
    "security": 5,
    "domain": 5,
}


def score_agents(result: ScanResult) -> int:
    """Agents dimension: max 15."""
    score = 0
    # 1pt per 5 agents, max 5
    score += min(result.agent_count // 5, 5)
    # Model tiering: 3 tiers=3, 2=2, 1=1, 0=0
    score += min(len(result.model_tiers), 3)
    # Tool scoping +4
    if result.has_tool_scoping:
        score += 4
    # Per-agent memory +3
    if result.has_per_agent_memory:
        score += 3
    return min(score, MAX_SCORES["agents"])


def score_quality(result: ScanResult) -> int:
    """Quality dimension: max 15."""
    score = 0
    # Review pipeline: multi-stage(3+)=5, single=3, none=0
    if result.review_stages >= 3:
        score += 5
    elif result.has_review_pipeline:
        score += 3
    # Veto +3 (indicated by review pipeline with stages)
    if result.has_review_pipeline and result.review_stages >= 2:
        score += 3
    # Acceptance criteria +3
    if result.has_acceptance_criteria:
        score += 3
    # TDD +2
    if result.has_tdd:
        score += 2
    # Deviation protocol +2
    if result.has_deviation_protocol:
        score += 2
    return min(score, MAX_SCORES["quality"])


def score_autonomy(result: ScanResult) -> int:
    """Autonomy dimension: max 15."""
    score = 0
    if result.has_crash_recovery:
        score += 4
    if result.has_stall_detection:
        score += 3
    if result.has_parallel_orchestration:
        score += 3
    if result.has_self_improvement:
        score += 3
    if result.has_session_chaining:
        score += 2
    return min(score, MAX_SCORES["autonomy"])


def score_safety(result: ScanResult) -> int:
    """Safety dimension: max 15."""
    score = 0
    # 1pt per 2 hooks, max 5
    score += min(result.hook_count // 2, 5)
    if result.has_destructive_blocking:
        score += 3
    if result.has_scope_enforcement:
        score += 3
    if result.has_memory_protection:
        score += 2
    if result.has_secrets_scanning:
        score += 2
    return min(score, MAX_SCORES["safety"])


def score_memory(result: ScanResult) -> int:
    """Memory dimension: max 10."""
    score = 0
    if result.has_session_persistence:
        score += 3
    if result.has_structured_handoffs:
        score += 2
    if result.has_learning_extraction:
        score += 2
    if result.has_pre_compact_save:
        score += 2
    if result.has_lessons_system:
        score += 1
    return min(score, MAX_SCORES["memory"])


def score_skills(result: ScanResult) -> int:
    """Skills dimension: max 10."""
    score = 0
    # 1pt per 3 skills, max 4
    score += min(result.skill_count // 3, 4)
    if result.has_skill_frontmatter:
        score += 3
    if result.has_trigger_definitions:
        score += 3
    return min(score, MAX_SCORES["skills"])


def score_infra(result: ScanResult) -> int:
    """Infra dimension: max 10."""
    score = 0
    # 1pt per 3 MCPs, max 4
    score += min(result.mcp_count // 3, 4)
    # Scripts: 5+ = 2, any = 1
    if result.script_count >= 5:
        score += 2
    elif result.script_count > 0:
        score += 1
    if result.has_templates:
        score += 2
    if result.has_deploy_automation:
        score += 2
    return min(score, MAX_SCORES["infra"])


def score_security(result: ScanResult) -> int:
    """Security dimension: max 5."""
    score = 0
    if result.has_pentest_tooling:
        score += 2
    if result.has_attack_playbooks:
        score += 1
    if result.has_scheduled_scans:
        score += 1
    if result.has_delta_reporting:
        score += 1
    return min(score, MAX_SCORES["security"])


def score_domain(result: ScanResult) -> int:
    """Domain dimension: max 5."""
    score = 0
    if result.has_domain_specialisation:
        score += 3
    if result.has_custom_pipelines:
        score += 2
    return min(score, MAX_SCORES["domain"])


SCORERS: dict[str, callable] = {
    "agents": score_agents,
    "quality": score_quality,
    "autonomy": score_autonomy,
    "safety": score_safety,
    "memory": score_memory,
    "skills": score_skills,
    "infra": score_infra,
    "security": score_security,
    "domain": score_domain,
}


def score_all(result: ScanResult) -> dict[str, int]:
    """Return all dimension scores plus overall total."""
    scores = {name: fn(result) for name, fn in SCORERS.items()}
    scores["overall"] = sum(scores.values())
    return scores
