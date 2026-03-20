# Tech Decisions — Claude Bench

## ADR-001: Python for Scanner
**Decision:** Python 3.10+ with pip install
**Alternatives:** Node.js (npx), Rust CLI
**Rationale:** Most Claude Code users have Python. pip/pipx install is universal. Type hints for maintainability.

## ADR-002: Privacy-First Scanning
**Decision:** Scanner reads file names and headings only. Never reads full file content. Never transmits file contents.
**Rationale:** Users must trust the tool with their setup. Reading structure is sufficient for scoring.

## ADR-003: Next.js 15 for Website
**Decision:** Next.js 15 App Router + Supabase + Vercel
**Alternatives:** Static site (Hugo), SvelteKit
**Rationale:** Matches primary stack. Server components for leaderboard. Supabase for storage.

## ADR-004: 100-Point Rubric with 9 Dimensions
**Decision:** Fixed rubric with weighted dimensions totalling 100
**Rationale:** Simple to understand, compare, and communicate. Dimensions cover all aspects of a Claude Code setup.
