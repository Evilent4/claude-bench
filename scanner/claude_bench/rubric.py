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
    # 1pt per 10 agents, max 6
    score += min(result.agent_count // 10, 6)
    # Model tiering: 3 tiers=2, 2=1, 1=0
    tiers = len(result.model_tiers)
    if tiers >= 3:
        score += 2
    elif tiers >= 2:
        score += 1
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
    # Review pipeline: multi-stage(3+)=4, single=3, none=0
    if result.review_stages >= 3:
        score += 4
    elif result.has_review_pipeline:
        score += 3
    # Veto authority +2
    if result.has_review_pipeline and result.review_stages >= 2:
        score += 2
    # Acceptance criteria +2
    if result.has_acceptance_criteria:
        score += 2
    # TDD +2
    if result.has_tdd:
        score += 2
    # Deviation protocol +1
    if result.has_deviation_protocol:
        score += 1
    # CI/CD pipeline +2
    if result.has_ci_config:
        score += 2
    # Test suite at root +2
    if result.has_test_suite:
        score += 2
    return min(score, MAX_SCORES["quality"])


def score_autonomy(result: ScanResult) -> int:
    """Autonomy dimension: max 15."""
    score = 0
    # Crash recovery +3
    if result.has_crash_recovery:
        score += 3
    # Stall detection +2
    if result.has_stall_detection:
        score += 2
    # Parallel orchestration +3
    if result.has_parallel_orchestration:
        score += 3
    # Self-improvement +2
    if result.has_self_improvement:
        score += 2
    # Session chaining +2
    if result.has_session_chaining:
        score += 2
    # Cost/budget tracking +3
    if result.has_cost_tracking:
        score += 3
    return min(score, MAX_SCORES["autonomy"])


def score_safety(result: ScanResult) -> int:
    """Safety dimension: max 15."""
    score = 0
    # 1pt per 3 hooks, max 3
    score += min(result.hook_count // 3, 3)
    # Destructive blocking +3
    if result.has_destructive_blocking:
        score += 3
    # Scope enforcement +3
    if result.has_scope_enforcement:
        score += 3
    # Memory/injection protection +2
    if result.has_memory_protection:
        score += 2
    # Secrets scanning +2
    if result.has_secrets_scanning:
        score += 2
    # Rate limiting / abuse prevention +2
    if result.has_rate_limiting:
        score += 2
    return min(score, MAX_SCORES["safety"])


def score_memory(result: ScanResult) -> int:
    """Memory dimension: max 10."""
    score = 0
    # Session persistence +2
    if result.has_session_persistence:
        score += 2
    # Structured handoffs +2
    if result.has_structured_handoffs:
        score += 2
    # Learning extraction +2
    if result.has_learning_extraction:
        score += 2
    # Pre-compact save +2
    if result.has_pre_compact_save:
        score += 2
    # Lessons system +1
    if result.has_lessons_system:
        score += 1
    # Semantic search +1
    if result.has_semantic_search:
        score += 1
    return min(score, MAX_SCORES["memory"])


def score_skills(result: ScanResult) -> int:
    """Skills dimension: max 10."""
    score = 0
    # 1pt per 7 skills, max 4
    score += min(result.skill_count // 7, 4)
    # Structured frontmatter +3
    if result.has_skill_frontmatter:
        score += 3
    # Trigger definitions +3
    if result.has_trigger_definitions:
        score += 3
    return min(score, MAX_SCORES["skills"])


def score_infra(result: ScanResult) -> int:
    """Infra dimension: max 10."""
    score = 0
    # 1pt per 4 MCPs, max 4
    score += min(result.mcp_count // 4, 4)
    # Scripts: 5+ = 2, any = 1
    if result.script_count >= 5:
        score += 2
    elif result.script_count > 0:
        score += 1
    # Templates +2
    if result.has_templates:
        score += 2
    # Deploy automation +2
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
