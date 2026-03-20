"""CLI entry point for claude-bench."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from claude_bench.report import build_json, print_json, print_terminal, print_verbose
from claude_bench.rubric import score_all
from claude_bench.scanner import scan_directory
from claude_bench.submit import submit_score


def main() -> None:
    parser = argparse.ArgumentParser(description="Score your Claude Code setup on a 100-point rubric")
    parser.add_argument("--path", default=".", help="Path to scan (default: current directory)")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Output JSON instead of terminal box")
    parser.add_argument("--verbose", action="store_true", help="Show detailed breakdown per dimension")
    parser.add_argument("--submit", action="store_true", help="Submit score to the leaderboard")
    parser.add_argument("--name", help="Handle for leaderboard submission (required with --submit)")
    args = parser.parse_args()

    target = Path(args.path).resolve()
    if not target.is_dir():
        print(f"Error: '{target}' is not a directory", file=sys.stderr)
        sys.exit(1)

    # 1. Scan
    result = scan_directory(target)

    # 2. Score
    scores = score_all(result)

    # 3. Output
    if args.json_output:
        print_json(scores, result, str(target))
    else:
        print_terminal(scores)
        if args.verbose:
            print_verbose(scores, result)

    # 4. Submit
    if args.submit:
        if not args.name:
            print("Error: --name required for submission", file=sys.stderr)
            sys.exit(1)
        json_data = build_json(scores, result, str(target))
        submit_score(json_data, args.name)
