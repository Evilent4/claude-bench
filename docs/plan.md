# Implementation Plan — Claude Bench

## Plan Style: Vertical Slices
Chosen over horizontal layers (all backend then all frontend) because each slice is independently testable and demoable.

## Phase 1: Scanner CLI
- [ ] Scaffold Python package with pyproject.toml
- [ ] Implement scanner.py — directory walking + detection logic
- [ ] Implement rubric.py — scoring functions per dimension
- [ ] Implement report.py — terminal ASCII output + JSON serialisation
- [ ] Implement cli.py — argparse with --path, --json, --verbose, --submit, --name
- [ ] Implement submit.py — POST to leaderboard API
- [ ] Implement __main__.py — entry point
- [ ] Write tests — test against known directory structures
- [ ] Verify against task-orchestrator (target: ~87-90)

## Phase 2: Website
- [ ] Scaffold Next.js 15 app with Tailwind + shadcn/ui
- [ ] Create Supabase project + scores table
- [ ] Build leaderboard page (server component)
- [ ] Build submit page (form + API route)
- [ ] Build profile page with radar chart
- [ ] Build badge SVG endpoint
- [ ] Deploy to Vercel

## Phase 3: Launch
- [ ] Score task-orchestrator as first entry
- [ ] Write README with badges, examples, installation
- [ ] Push to GitHub (public repo)
