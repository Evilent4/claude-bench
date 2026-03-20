# Product Requirements — Claude Bench

## What
An open-source CLI tool that scans any Claude Code setup and produces a score out of 100 across 9 dimensions. A companion leaderboard website lets users submit and compare scores.

## Target User
Claude Code power users who customise their setup with agents, hooks, skills, memory, and MCP servers.

## Core Features
1. **CLI Scanner** — `claude-bench` command that scans a directory and outputs a score
2. **9-Dimension Rubric** — Agents, Quality, Autonomy, Safety, Memory, Skills, Infra, Security, Domain
3. **Terminal Report** — ASCII progress bars, dimension breakdown
4. **JSON Export** — Machine-readable output for CI/submission
5. **Leaderboard Website** — Ranked table, radar charts, shareable badges
6. **Badge API** — SVG badges for README embeds

## Non-Goals
- Reading file content (privacy-first: structure only)
- Prescribing a "correct" setup
- Paid tiers or authentication

## PRD Approach Evaluation
1. **CLI-only (no website):** Simpler but no community aspect. Rejected.
2. **Website-only (manual input):** Lower barrier but no automation. Rejected.
3. **CLI + Website (chosen):** Scanner provides automation and accuracy, website provides community and shareability. Best of both.
