#!/usr/bin/env python3
"""Build a contact sheet (JPEG mosaic) from extracted frames using FFmpeg tile.

Usage:
  python generate_contact_sheet.py <frames_dir> -o contact_sheet.jpg [--cols 6]
      [--width 320] [--max-frames 48]
Frames are used in filename order. If the count is not a multiple of --cols,
the last frame is repeated to fill the grid.
Exit codes: 0 ok, 1 no frames found, 2 ffmpeg failure.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("frames_dir")
    ap.add_argument("-o", "--out", default="contact_sheet.jpg")
    ap.add_argument("--cols", type=int, default=6)
    ap.add_argument("--width", type=int, default=320, help="cell width in px")
    ap.add_argument("--max-frames", type=int, default=48)
    a = ap.parse_args()
    d = Path(a.frames_dir)
    frames = sorted(p for p in d.glob("*.jpg")) + sorted(p for p in d.glob("*.png"))
    if not frames:
        print(f"error: no frames found in {d}", file=sys.stderr)
        return 1
    frames = frames[: a.max_frames]
    cols = max(a.cols, 1)
    rows = (len(frames) + cols - 1) // cols
    while len(frames) < cols * rows:
        frames.append(frames[-1])  # tile needs a full grid
    h = round(a.width * 9 / 16)  # assume 16:9 cells; tile scales to cell size
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for f in frames:
        cmd += ["-i", str(f)]
    n = len(frames)
    scale = "".join(f"[{i}:v]scale={a.width}:{h}[s{i}];" for i in range(n))
    chain = (scale + "".join(f"[s{i}]" for i in range(n))
             + f"concat=n={n}:v=1:a=0[vc];[vc]tile={cols}x{rows}[v]")
    cmd += ["-filter_complex", chain, "-map", "[v]", "-q:v", "3",
            "-frames:v", "1", str(a.out)]
    p = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if p.returncode != 0 or not Path(a.out).is_file():
        print(f"error: ffmpeg failed: {p.stderr.strip()[-400:]}", file=sys.stderr)
        return 2
    print(f"wrote {a.out} ({len(frames)} source frames, {cols}x{rows} grid)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
