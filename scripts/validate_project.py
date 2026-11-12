#!/usr/bin/env python3
"""Validate (or scaffold with --init) a documentary project directory.

Usage:
  python validate_project.py --init D:\\documentary\\projects\\my-film
  python validate_project.py <project-dir> [--json]
Checks: expected directories exist, JSON files parse, project.json is present
and well-formed. Exit codes: 0 valid, 1 invalid, 2 bad arguments.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DIRS = ["research", "script", "storyboard", "assets", "production",
        "audio/narration", "audio/music", "audio/sfx",
        "renders", "quality-control", "delivery"]

JSON_FILES = ["project.json",
              "research/claims.json", "research/sources.json",
              "script/narration.json", "storyboard/scenes.json",
              "assets/asset_manifest.json", "production/engine_manifest.json"]

STAGES = ["brief", "research", "script", "storyboard", "assets", "audio",
          "production", "assembly", "qc", "delivery"]


def scaffold(root: Path) -> int:
    if root.exists() and any(root.iterdir()):
        print(f"refusing to init non-empty directory: {root}", file=sys.stderr)
        return 2
    for d in DIRS + ["production/hyperframes", "production/lemo-opuscar",
                     "renders/round-01"]:
        (root / d).mkdir(parents=True, exist_ok=True)
    project = {
        "name": root.name, "created": datetime.now(timezone.utc).isoformat(),
        "updated": datetime.now(timezone.utc).isoformat(),
        "target": {"duration_sec": None, "resolution": "1920x1080", "fps": 24,
                   "language": "en"},
        "stage": "brief", "stages_completed": [],
        "stages_pending": STAGES[1:], "current_render": None,
        "render_round": 0, "correction_round": 0, "score": None,
        "open_defects": [], "approval_status": "PENDING", "history": [],
    }
    (root / "project.json").write_text(json.dumps(project, indent=2),
                                       encoding="utf-8")
    for d in ["research", "script", "storyboard", "quality-control"]:
        (root / d / ".gitkeep").touch()
    print(f"scaffolded project at {root}")
    return 0


def validate(root: Path, as_json: bool) -> int:
    errors, warnings = [], []
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 1
    for d in DIRS:
        if not (root / d).is_dir():
            warnings.append(f"missing directory: {d}")
    for f in JSON_FILES:
        p = root / f
        if not p.is_file():
            warnings.append(f"JSON file not created yet: {f}")
            continue
        try:
            json.loads(p.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as e:
            errors.append(f"invalid JSON {f}: {e}")
    pj = root / "project.json"
    state = None
    if pj.is_file():
        try:
            state = json.loads(pj.read_text(encoding="utf-8-sig"))
            for k in ("name", "stage", "stages_completed", "stages_pending",
                      "render_round", "correction_round", "approval_status"):
                if k not in state:
                    errors.append(f"project.json missing key: {k}")
            if state.get("stage") not in STAGES:
                errors.append(f"project.json stage '{state.get('stage')}' "
                              f"not one of {STAGES}")
        except (OSError, json.JSONDecodeError) as e:
            errors.append(f"invalid project.json: {e}")
    result = {"project": str(root), "valid": not errors,
              "errors": errors, "warnings": warnings, "state": state}
    if as_json:
        print(json.dumps(result, indent=2))
    else:
        for w in warnings:
            print(f"WARN  {w}")
        for e in errors:
            print(f"ERROR {e}")
        print(f"{'VALID' if not errors else 'INVALID'}: {root}")
    return 0 if not errors else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("project", nargs="?", default=None)
    ap.add_argument("--init", dest="init", default=None,
                    help="scaffold a new project directory and exit")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.init:
        return scaffold(Path(a.init))
    if not a.project:
        print("error: provide a project directory (or --init PATH)", file=sys.stderr)
        return 2
    return validate(Path(a.project), a.json)


if __name__ == "__main__":
    sys.exit(main())
