#!/usr/bin/env python3
"""Print the production status of a documentary project.

Usage:
  python project_status.py <project-dir> [--json]
Reads project.json and reports stage progress, render/correction round,
score, open defects and approval status. Does not modify anything.
Exit codes: 0 ok, 1 project.json missing/invalid.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

STAGES = ["brief", "research", "script", "storyboard", "assets", "audio",
          "production", "assembly", "qc", "delivery"]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("project")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    pj = Path(a.project) / "project.json"
    if not pj.is_file():
        print(f"error: {pj} not found (is this a project directory?)", file=sys.stderr)
        return 1
    try:
        s = json.loads(pj.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"error: invalid project.json: {e}", file=sys.stderr)
        return 1
    if a.json:
        print(json.dumps(s, indent=2))
        return 0
    done, pend = s.get("stages_completed", []), s.get("stages_pending", [])
    print(f"Project      {s.get('name', Path(a.project).name)}")
    print(f"Stage        {s.get('stage')}")
    print()
    print("Stages:")
    for st in STAGES:
        mark = "done " if st in done else ("next" if st == s.get("stage") else "----")
        extra = "" if st in done or st in pend or st == s.get("stage") else " (unknown)"
        print(f"  [{mark}] {st}{extra}")
    print()
    print(f"Render round    {s.get('render_round', 0)}   "
          f"Current render: {s.get('current_render') or 'none'}")
    print(f"Corrections     {s.get('correction_round', 0)} of max 5")
    score = s.get("score")
    print(f"Score           {score if score is not None else 'not scored yet'}")
    defects = s.get("open_defects", [])
    print(f"Open defects    {len(defects)}"
          + (f" -> {', '.join(defects)}" if defects else ""))
    print(f"Approval        {s.get('approval_status', 'PENDING')}")
    history = s.get("history", [])
    if history:
        last = history[-1]
        print(f"Last event      {last.get('ts', '?')} — {last.get('event', '?')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
