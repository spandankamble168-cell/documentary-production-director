#!/usr/bin/env python3
"""Extract sample frames from a video, preserving timestamps in filenames.

Usage:
  python extract_frames.py <video> -o frames/ [--every 3] [--limit 200]
      [--timestamps 12.5 44.1 ...] [--around 88.0:6]
Frames: one JPEG per timestamp, named frame_<HH-MM-SS.mmm>.jpg.
Opening (0s) and closing frame are always included.
Exit codes: 0 ok, 1 input missing, 2 ffmpeg failure (some frames may exist).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def probe_duration(path: Path):
    p = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", str(path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "ffprobe failed")
    d = json.loads(p.stdout or "{}").get("format", {}).get("duration")
    return float(d) if d else None


def grab(src: Path, ts: float, out: Path):
    p = subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-ss", f"{ts:.3f}", "-i", str(src),
         "-frames:v", "1", "-q:v", "2", str(out)],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode == 0 and out.is_file() and out.stat().st_size > 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("video")
    ap.add_argument("-o", "--outdir", default="frames")
    ap.add_argument("--every", type=float, default=3.0,
                    help="seconds between samples (default 3)")
    ap.add_argument("--limit", type=int, default=200, help="max frames total")
    ap.add_argument("--timestamps", type=float, nargs="*", default=[],
                    help="exact extra timestamps (e.g. suspicious cuts)")
    ap.add_argument("--around", action="append", default=[],
                    help="T:N — N frames spread around second T")
    a = ap.parse_args()
    src = Path(a.video)
    if not src.is_file():
        print(f"error: not a file: {src}", file=sys.stderr)
        return 1
    try:
        dur = probe_duration(src)
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    outdir = Path(a.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    ts: list[float] = [0.0]
    if dur:
        t = a.every
        while t < dur - 0.25:
            ts.append(round(t, 3))
            t += a.every
        ts.append(max(dur - 0.1, 0.0))  # closing frame
    ts += [round(x, 3) for x in a.timestamps]
    for spec in a.around:
        try:
            center, n = spec.split(":")
            center, n = float(center), max(int(n), 1)
        except ValueError:
            print(f"error: --around expects T:N, got '{spec}'", file=sys.stderr)
            return 2
        step = 1.0 if n <= 7 else 0.5
        for i in range(n):
            ts.append(round(center - (n - 1) * step / 2 + i * step, 3))
    # dedupe, sort, clamp
    seen, ordered = set(), []
    for t in sorted(ts):
        if t < 0 or (dur is not None and t > dur):
            continue
        k = round(t, 3)
        if k not in seen:
            seen.add(k)
            ordered.append(k)
    ordered = ordered[: a.limit]

    ok, failed = 0, 0
    for t in ordered:
        mm = int(t // 60)
        name = f"frame_{mm // 60:02d}-{mm % 60:02d}-{t % 60:06.3f}.jpg"
        if grab(src, t, outdir / name):
            ok += 1
        else:
            failed += 1
            print(f"warn: frame at {t:.3f}s failed", file=sys.stderr)
    print(f"extracted {ok} frames to {outdir}" + (f", {failed} failed" if failed else ""))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
