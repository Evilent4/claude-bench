# Claude Bench

> Open-source CLI scanner + leaderboard that scores any Claude Code setup on a 100-point rubric across 9 dimensions.

## Tech Stack
- **Scanner:** Python 3.10+ (pip-installable CLI)
- **Website:** Next.js 15 (App Router), Tailwind CSS, shadcn/ui, Supabase
- **Deploy:** Vercel (web), PyPI (scanner)

## Folder Structure
```
claude-bench/
├── scanner/                    # Python CLI (pip-installable)
│   ├── claude_bench/
│   │   ├── __init__.py
│   │   ├── __main__.py         # Entry point: python -m claude_bench
│   │   ├── cli.py              # argparse CLI
│   │   ├── scanner.py          # Core scanning logic
│   │   ├── rubric.py           # Scoring rules per dimension
│   │   ├── report.py           # Terminal output + JSON export
│   │   └── submit.py           # Submit score to leaderboard API
│   ├── pyproject.toml
│   └── tests/
├── web/                        # Next.js 15 leaderboard site
│   ├── src/app/
│   ├── package.json
│   └── tailwind.config.ts
├── CLAUDE.md
├── docs/
│   ├── product-requirements.md
│   ├── plan.md
│   ├── tech-decisions.md
│   └── error-log.md
└── README.md
```

## Commands
```sh
# Scanner
cd scanner && pip install -e . && claude-bench --path ~/Projects/task-orchestrator

# Web
cd web && pnpm install && pnpm dev

# Test
cd scanner && python -m pytest tests/
```

## Conventions
- Python: snake_case, type hints, ruff
- TypeScript: strict mode, server components by default
- Commits: feat:/fix:/docs: prefixes

## Key Files
- `scanner/claude_bench/scanner.py` — core detection logic
- `scanner/claude_bench/rubric.py` — scoring rules (100 points across 9 dimensions)
- `scanner/claude_bench/report.py` — terminal + JSON output
- `web/src/app/page.tsx` — leaderboard landing
- `web/src/app/api/scores/route.ts` — scores API

## Current State
- **Branch:** main
- **Status:** Initial scaffold
