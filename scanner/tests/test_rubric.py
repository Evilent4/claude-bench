"""Tests for the scoring rubric."""

from claude_bench.rubric import (
    MAX_SCORES,
    score_agents,
    score_all,
    score_autonomy,
    score_domain,
    score_infra,
    score_memory,
    score_quality,
    score_safety,
    score_security,
    score_skills,
)
from claude_bench.scanner import ScanResult


def _empty() -> ScanResult:
    return ScanResult()


def _full() -> ScanResult:
    """A maximally-scoring ScanResult."""
    return ScanResult(
        agent_count=60,
        has_tool_scoping=True,
        model_tiers={"haiku", "sonnet", "opus"},
        has_per_agent_memory=True,
        has_review_pipeline=True,
        review_stages=3,
        has_acceptance_criteria=True,
        has_tdd=True,
        has_deviation_protocol=True,
        has_ci_config=True,
        has_test_suite=True,
        has_crash_recovery=True,
        has_stall_detection=True,
        has_parallel_orchestration=True,
        has_self_improvement=True,
        has_session_chaining=True,
        has_cost_tracking=True,
        hook_count=12,
        has_destructive_blocking=True,
        has_scope_enforcement=True,
        has_memory_protection=True,
        has_secrets_scanning=True,
        has_rate_limiting=True,
        has_session_persistence=True,
        has_structured_handoffs=True,
        has_learning_extraction=True,
        has_pre_compact_save=True,
        has_lessons_system=True,
        has_semantic_search=True,
        skill_count=28,
        has_skill_frontmatter=True,
        has_trigger_definitions=True,
        mcp_count=16,
        script_count=10,
        has_templates=True,
        has_deploy_automation=True,
        has_pentest_tooling=True,
        has_attack_playbooks=True,
        has_scheduled_scans=True,
        has_delta_reporting=True,
        has_domain_specialisation=True,
        domain_detected="ML/Quant",
        has_custom_pipelines=True,
    )


class TestScoreAgents:
    def test_zero_agents(self):
        assert score_agents(_empty()) == 0

    def test_agent_count_capped(self):
        r = ScanResult(agent_count=100)
        assert score_agents(r) == 6  # max 6 from count (1pt per 10)

    def test_model_tiers(self):
        r = ScanResult(model_tiers={"haiku", "sonnet", "opus"})
        assert score_agents(r) == 2  # 3 tiers = 2pt

    def test_two_tiers(self):
        r = ScanResult(model_tiers={"haiku", "sonnet"})
        assert score_agents(r) == 1

    def test_full_agents(self):
        assert score_agents(_full()) == 15  # 6+2+4+3

    def test_tool_scoping(self):
        r = ScanResult(has_tool_scoping=True)
        assert score_agents(r) == 4


class TestScoreQuality:
    def test_empty(self):
        assert score_quality(_empty()) == 0

    def test_review_pipeline_only(self):
        r = ScanResult(has_review_pipeline=True, review_stages=1)
        assert score_quality(r) == 3

    def test_multi_stage_review(self):
        r = ScanResult(has_review_pipeline=True, review_stages=3)
        assert score_quality(r) == 6  # 4 + 2

    def test_full_quality(self):
        assert score_quality(_full()) == 15


class TestScoreAutonomy:
    def test_empty(self):
        assert score_autonomy(_empty()) == 0

    def test_full(self):
        assert score_autonomy(_full()) == 15

    def test_partial(self):
        r = ScanResult(has_crash_recovery=True, has_stall_detection=True)
        assert score_autonomy(r) == 5  # 3 + 2


class TestScoreSafety:
    def test_empty(self):
        assert score_safety(_empty()) == 0

    def test_hooks_only(self):
        r = ScanResult(hook_count=9)
        assert score_safety(r) == 3  # 9//3 = 3, capped at 3

    def test_full(self):
        assert score_safety(_full()) == 15


class TestScoreMemory:
    def test_empty(self):
        assert score_memory(_empty()) == 0

    def test_full(self):
        assert score_memory(_full()) == 10


class TestScoreSkills:
    def test_empty(self):
        assert score_skills(_empty()) == 0

    def test_skill_count_capped(self):
        r = ScanResult(skill_count=100)
        assert score_skills(r) == 4  # max 4 from count (1pt per 7)

    def test_full(self):
        assert score_skills(_full()) == 10  # 4+3+3


class TestScoreInfra:
    def test_empty(self):
        assert score_infra(_empty()) == 0

    def test_scripts_threshold(self):
        r = ScanResult(script_count=3)
        assert score_infra(r) == 1
        r2 = ScanResult(script_count=5)
        assert score_infra(r2) == 2

    def test_full(self):
        assert score_infra(_full()) == 10  # 4+2+2+2


class TestScoreSecurity:
    def test_empty(self):
        assert score_security(_empty()) == 0

    def test_full(self):
        assert score_security(_full()) == 5


class TestScoreDomain:
    def test_empty(self):
        assert score_domain(_empty()) == 0

    def test_full(self):
        assert score_domain(_full()) == 5


class TestScoreAll:
    def test_empty_overall_zero(self):
        scores = score_all(_empty())
        assert scores["overall"] == 0

    def test_full_overall_100(self):
        scores = score_all(_full())
        assert scores["overall"] == 100

    def test_overall_never_exceeds_100(self):
        r = _full()
        r.agent_count = 200
        r.hook_count = 100
        r.skill_count = 200
        r.mcp_count = 100
        r.script_count = 100
        scores = score_all(r)
        assert scores["overall"] <= 100

    def test_all_dimensions_present(self):
        scores = score_all(_empty())
        for key in MAX_SCORES:
            assert key in scores
        assert "overall" in scores
