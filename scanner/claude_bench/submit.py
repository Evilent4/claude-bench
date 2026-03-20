"""Submit scores to the Claude Bench leaderboard API."""

from __future__ import annotations

import sys

import httpx

DEFAULT_API_URL = "https://claudebench.dev/api/scores"


def submit_score(
    score_json: dict,
    name: str,
    api_url: str = DEFAULT_API_URL,
) -> bool:
    """POST the score JSON to the leaderboard API. Returns True on success."""
    payload = {**score_json, "name": name}
    try:
        resp = httpx.post(api_url, json=payload, timeout=30)
        if resp.status_code in (200, 201):
            print(f"Submitted successfully as '{name}'. Check the leaderboard at https://claudebench.dev")
            return True
        print(f"Submission failed: HTTP {resp.status_code} — {resp.text}", file=sys.stderr)
        return False
    except httpx.HTTPError as e:
        print(f"Submission failed: {e}", file=sys.stderr)
        return False
