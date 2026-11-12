#!/usr/bin/env python3
"""Detect scene cuts in a video using FFmpeg scene-change detection.

Usage:
  python detect_scenes.py <video> [-o scenes.json] [--threshold 0.3]
Outputs cut timestamps (seconds) found by the `select=gt(scene,T)` filter.
Exit codes: 0 ok, 1 input missing, 2 ffmpeg failure.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("video")
    ap.add_argument("-o", "--out", default="scenes.json")
    ap.add_argument("--threshold", type=float, default=0.3,
                    help="scene score threshold 0..1 (default 0.3)")
    a = ap.parse_args()
    src = Path(a.video)
    if not src.is_file():
        print(f"error: not a file: {src}", file=sys.stderr)
        return 1
    vf = f"select='gt(scene,{a.threshold})',showinfo"
    p = subprocess.run(
        ["ffmpeg", "-i", str(src), "-vf", vf, "-an", "-f", "null", "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        print(f"error: ffmpeg failed: {p.stderr.strip()[-400:]}", file=sys.stderr)
        return 2
    cuts = []
    for m in re.finditer(r"showinfo.*?pts_time:([0-9.]+)", p.stderr):
        t = float(m.group(1))
        if t > 0.05 and (not cuts or t - cuts[-1] > 0.05):
            cuts.append(round(t, 3))
    result = {"file": str(src), "threshold": a.threshold,
              "cuts_sec": cuts, "cut_count": len(cuts),
              "method": "ffmpeg scene-change select filter (numerical)"}
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
