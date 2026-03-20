# Claude Bench

Score your Claude Code setup on a 100-point rubric across 9 dimensions.

```
╔════════════════════════════════════╗
║         CLAUDE BENCH  v1.0         ║
╠════════════════════════════════════╣
║  Overall Score:  87 / 100          ║
╠════════════════════════════════════╣
║  Agents    ████████████░░░  12/15  ║
║  Quality   █████████████░░  13/15  ║
║  Autonomy  ████████████░░░  12/15  ║
║  Safety    █████████████░░  13/15  ║
║  Memory    ████████░░░░░░░   8/10  ║
║  Skills    ████████░░░░░░░   8/10  ║
║  Infra     ████████░░░░░░░   8/10  ║
║  Security  ████░░░░░░░░░░░   4/5   ║
║  Domain    ███████████████   5/5   ║
╠════════════════════════════════════╣
║  Submit: claude-bench --submit     ║
╚════════════════════════════════════╝
```

## Install

```bash
# macOS (recommended)
brew install pipx && pipx install claude-bench

# Linux / venv
pip install claude-bench
```

Or run from source:

```bash
git clone https://github.com/Evilent4/claude-bench.git
cd claude-bench/scanner
pip install -e .
```

## Usage

```bash
# Scan current directory
claude-bench

# Scan a specific path
claude-bench --path ~/Projects/my-setup

# Detailed breakdown
claude-bench --verbose

# JSON output
claude-bench --json > score.json

# Submit to leaderboard
claude-bench --submit --name "myhandle"
```

## What It Scores

| Dimension | Max | What Earns Points |
|-----------|-----|-------------------|
| **Agents** | 15 | Agent count, model tiering (haiku/sonnet/opus), tool scoping, per-agent memory |
| **Quality** | 15 | Review pipeline, veto authority, acceptance criteria, TDD, deviation protocol |
| **Autonomy** | 15 | Crash recovery, stall detection, parallel orchestration, self-improvement, session chaining |
| **Safety** | 15 | Hook count, destructive command blocking, scope enforcement, memory protection, secrets scanning |
| **Memory** | 10 | Session persistence, structured handoffs, learning extraction, pre-compact save, lessons system |
| **Skills** | 10 | Skill count, structured frontmatter, trigger definitions |
| **Infra** | 10 | MCP server count, scripts, templates, deploy automation |
| **Security** | 5 | Pentest tooling, attack playbooks, scheduled scans, delta reporting |
| **Domain** | 5 | Specialised agents/tools for a vertical, custom data pipelines |

## Privacy

The scanner reads **file names and headings only**. It never reads full file contents and never transmits anything. The JSON output contains only counts and boolean flags.

## Badge

Add a badge to your README:

```markdown
![Claude Bench](https://claudebench.dev/api/badge/YOUR_HANDLE)
```

## Leaderboard

Visit [claudebench.dev](https://claudebench.dev) to see the leaderboard, submit your score, and compare setups.

## Development

```bash
# Scanner
cd scanner
pip install -e ".[dev]"
python -m pytest tests/

# Website
cd web
pnpm install
pnpm dev
```

## Licence

MIT
