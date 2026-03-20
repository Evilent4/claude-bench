"""Tests for the scanner detection logic."""

import json
import tempfile
from pathlib import Path

from claude_bench.scanner import ScanResult, scan_directory


def _make_dir(base: Path, *parts: str) -> Path:
    d = base.joinpath(*parts)
    d.mkdir(parents=True, exist_ok=True)
    return d


def _write(base: Path, rel_path: str, content: str = "") -> Path:
    p = base / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p


class TestEmptyDirectory:
    def test_returns_all_defaults(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = scan_directory(Path(tmp))
            assert result.agent_count == 0
            assert result.has_tool_scoping is False
            assert result.model_tiers == set()
            assert result.hook_count == 0
            assert result.skill_count == 0
            assert result.mcp_count == 0
            assert result.script_count == 0
            assert result.domain_detected == ""

    def test_nonexistent_path(self):
        result = scan_directory(Path("/nonexistent/path/12345"))
        assert result.agent_count == 0


class TestAgentDetection:
    def test_counts_agent_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            agent_dir = _make_dir(base, ".claude", "agents")
            for i in range(5):
                (agent_dir / f"agent-{i}.md").write_text(f"# Agent {i}\n")
            result = scan_directory(base)
            assert result.agent_count == 5

    def test_detects_tool_scoping(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            agent_dir = _make_dir(base, ".claude", "agents")
            (agent_dir / "builder.md").write_text("# Builder\n\n## Allowed Tools\n- Read\n- Write\n")
            result = scan_directory(base)
            assert result.has_tool_scoping is True

    def test_detects_model_tiers(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            agent_dir = _make_dir(base, ".claude", "agents")
            (agent_dir / "fast.md").write_text("# Fast Agent\nModel: haiku\n")
            (agent_dir / "mid.md").write_text("# Mid Agent\nModel: sonnet\n")
            result = scan_directory(base)
            assert result.model_tiers == {"haiku", "sonnet"}


class TestHooksDetection:
    def test_counts_hooks(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            hooks_dir = _make_dir(base, "hooks")
            hooks_data = {
                "PreToolCall": [
                    {"name": "destructive-block", "command": "check-block.sh"},
                    {"name": "scope-check", "command": "scope.sh"},
                ],
                "PostToolCall": [
                    {"name": "memory-sanitiser", "command": "sanitise.sh"},
                ],
            }
            (hooks_dir / "hooks.json").write_text(json.dumps(hooks_data))
            result = scan_directory(base)
            assert result.hook_count == 3

    def test_detects_destructive_blocking(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            hooks_dir = _make_dir(base, "hooks")
            hooks_data = {
                "PreToolCall": [
                    {"name": "block-destructive", "command": "block.sh"},
                ],
            }
            (hooks_dir / "hooks.json").write_text(json.dumps(hooks_data))
            result = scan_directory(base)
            assert result.has_destructive_blocking is True


class TestMCPDetection:
    def test_counts_mcp_servers(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            mcp_data = {
                "mcpServers": {
                    "notion": {"type": "oauth"},
                    "linear": {"type": "oauth"},
                    "figma": {"type": "oauth"},
                }
            }
            (base / ".mcp.json").write_text(json.dumps(mcp_data))
            result = scan_directory(base)
            assert result.mcp_count == 3

    def test_falls_back_to_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            mcp_data = {"mcpServers": {"a": {}, "b": {}}}
            (base / ".mcp.json.template").write_text(json.dumps(mcp_data))
            result = scan_directory(base)
            assert result.mcp_count == 2


class TestSkillDetection:
    def test_counts_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            for name in ("deploy", "flow", "queue"):
                skill_dir = _make_dir(base, "skills", name)
                (skill_dir / "SKILL.md").write_text(f"# {name}\n")
            result = scan_directory(base)
            assert result.skill_count == 3

    def test_detects_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            skill_dir = _make_dir(base, "skills", "deploy")
            (skill_dir / "SKILL.md").write_text("---\nname: deploy\n---\n# Deploy\n")
            result = scan_directory(base)
            assert result.has_skill_frontmatter is True

    def test_detects_trigger_definitions(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            skill_dir = _make_dir(base, "skills", "deploy")
            (skill_dir / "SKILL.md").write_text("---\nname: deploy\ndescription: Deploy to prod\ntrigger: /deploy\n---\n")
            result = scan_directory(base)
            assert result.has_trigger_definitions is True


class TestMemoryDetection:
    def test_session_persistence(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            _make_dir(base, "memory", "sessions")
            result = scan_directory(base)
            assert result.has_session_persistence is True

    def test_structured_handoffs(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            sessions = _make_dir(base, "memory", "sessions")
            (sessions / "latest.md").write_text("# Latest\n")
            (sessions / "pre-compact-snapshot.md").write_text("# Snapshot\n")
            result = scan_directory(base)
            assert result.has_structured_handoffs is True

    def test_learning_extraction(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            _make_dir(base, "memory", "learn")
            result = scan_directory(base)
            assert result.has_learning_extraction is True

    def test_lessons_system(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            _make_dir(base, "memory")
            (base / "memory" / "lessons.md").write_text("# Lessons\n")
            result = scan_directory(base)
            assert result.has_lessons_system is True


class TestDomainDetection:
    def test_detects_quant_domain(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            agent_dir = _make_dir(base, ".claude", "agents")
            (agent_dir / "trading-bot.md").write_text("# Trading Bot\n")
            tools_dir = _make_dir(base, "tools")
            (tools_dir / "risk_engine.py").write_text("# Risk engine\n")
            result = scan_directory(base)
            assert result.has_domain_specialisation is True
            assert result.domain_detected == "ML/Quant"

    def test_no_domain_for_generic(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            agent_dir = _make_dir(base, ".claude", "agents")
            (agent_dir / "helper.md").write_text("# Helper\n")
            result = scan_directory(base)
            assert result.has_domain_specialisation is False


class TestSecurityDetection:
    def test_pentest_tooling(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            _make_dir(base, "tools", "pentest")
            result = scan_directory(base)
            assert result.has_pentest_tooling is True

    def test_attack_playbooks(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            _make_dir(base, "skills", "attack")
            (base / "skills" / "attack" / "SKILL.md").write_text("# Attack\n")
            result = scan_directory(base)
            assert result.has_attack_playbooks is True


class TestFullSetup:
    """Integration test: build a complete setup and verify all detections."""

    def test_full_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)

            # Agents
            agent_dir = _make_dir(base, ".claude", "agents")
            for i in range(10):
                content = f"# Agent {i}\nModel: {'haiku' if i < 3 else 'sonnet' if i < 7 else 'opus'}\n"
                if i == 0:
                    content += "\n## Allowed Tools\n- Read\n"
                (agent_dir / f"agent-{i}.md").write_text(content)

            # Rules
            rules_dir = _make_dir(base, ".claude", "rules")
            _write(base, ".claude/rules/security.md", "# Security\nScope enforcement\nInjection prevention\nScan for hardcoded secrets\n")
            _write(base, ".claude/rules/workflow.md", "# Workflow\nDeviation protocol\nAcceptance criteria\n")

            # Memory
            _make_dir(base, "memory", "agents")
            sessions = _make_dir(base, "memory", "sessions")
            (sessions / "latest.md").write_text("# Latest\n")
            (sessions / "pre-compact-snapshot.md").write_text("# Snapshot\n")
            _make_dir(base, "memory", "learn")
            _write(base, "memory/lessons.md", "# Lessons\n")

            # Hooks
            hooks_dir = _make_dir(base, "hooks")
            hooks_data = {
                "PreToolCall": [
                    {"name": "block-destructive", "command": "block.sh"},
                    {"name": "memory-sanitiser", "command": "sanitise.sh"},
                ],
                "PostResponse": [
                    {"name": "stall-detect", "command": "stall.sh"},
                    {"name": "learn", "command": "learn.sh"},
                ],
                "PreCompact": [
                    {"name": "pre-compact-save", "command": "save.sh"},
                ],
            }
            (hooks_dir / "hooks.json").write_text(json.dumps(hooks_data))
            scripts_dir = _make_dir(base, "hooks", "scripts")
            _write(base, "hooks/scripts/stall-detect.sh", "#!/bin/bash\n# stall detection\n")

            # Skills
            for name in ("deploy", "flow", "queue", "tdd-loop", "attack", "archivist"):
                sd = _make_dir(base, "skills", name)
                fm = "---\nname: {}\ndescription: Do {}\ntrigger: /{}\n---\n".format(name, name, name)
                if name == "tdd-loop":
                    fm += "# TDD Loop\nTest-driven development\n"
                elif name == "flow":
                    fm += "# Flow\nCrash recovery and session chaining\n"
                elif name == "deploy":
                    fm += "# Deploy\nDeploy to production\n"
                (sd / "SKILL.md").write_text(fm)

            # Scripts
            scripts = _make_dir(base, "scripts")
            _write(base, "scripts/flow.sh", "#!/bin/bash\n# flow protocol with crash recovery\n")
            _write(base, "scripts/parallel_runner.py", "# parallel orchestration\n")
            _write(base, "scripts/queue.sh", "# queue runner\n")
            _write(base, "scripts/deploy.sh", "# deploy script\n")
            _write(base, "scripts/scanner.py", "# scanner\n")

            # MCP
            mcp_data = {"mcpServers": {f"server-{i}": {} for i in range(6)}}
            (base / ".mcp.json").write_text(json.dumps(mcp_data))

            # Infra
            _make_dir(base, "templates")

            # Security
            _make_dir(base, "tools", "pentest")

            # Domain
            _write(base, "tools/risk_engine.py", "# Risk engine pipeline\ndef ingest(): pass\n")

            # CLAUDE.md
            _write(base, "CLAUDE.md", "# Project\nReview pipeline\nVeto authority\nPre-compact save\nSelf-improvement loop\n")

            result = scan_directory(base)

            assert result.agent_count == 10
            assert result.has_tool_scoping is True
            assert len(result.model_tiers) == 3
            assert result.has_per_agent_memory is True
            assert result.has_review_pipeline is True
            assert result.has_acceptance_criteria is True
            assert result.has_tdd is True
            assert result.has_deviation_protocol is True
            assert result.has_crash_recovery is True
            assert result.has_stall_detection is True
            assert result.has_parallel_orchestration is True
            assert result.has_self_improvement is True
            assert result.has_session_chaining is True
            assert result.hook_count == 5
            assert result.has_destructive_blocking is True
            assert result.has_memory_protection is True
            assert result.has_session_persistence is True
            assert result.has_structured_handoffs is True
            assert result.has_learning_extraction is True
            assert result.has_pre_compact_save is True
            assert result.has_lessons_system is True
            assert result.skill_count == 6
            assert result.has_skill_frontmatter is True
            assert result.has_trigger_definitions is True
            assert result.mcp_count == 6
            assert result.script_count == 5
            assert result.has_templates is True
            assert result.has_deploy_automation is True
            assert result.has_pentest_tooling is True
            assert result.has_attack_playbooks is True
            assert result.has_domain_specialisation is True
            assert result.domain_detected == "ML/Quant"
            assert result.has_custom_pipelines is True
