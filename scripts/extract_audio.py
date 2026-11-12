#!/usr/bin/env python3
"""Extract the audio track of a video to WAV with FFmpeg (for analysis/mixing).

Usage:
  python extract_audio.py <video> [-o audio.wav] [--sample-rate 48000] [--mono]
Exit codes: 0 ok, 1 input missing, 2 ffmpeg failed / no audio stream.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("video")
    ap.add_argument("-o", "--out", default="audio.wav")
    ap.add_argument("--sample-rate", type=int, default=48000)
    ap.add_argument("--mono", action="store_true")
    a = ap.parse_args()
    src, out = Path(a.video), Path(a.out)
    if not src.is_file():
        print(f"error: not a file: {src}", file=sys.stderr)
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    layout = ["-ac", "1"] if a.mono else []
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vn",
           "-ar", str(a.sample_rate), *layout, "-c:a", "pcm_s16le", str(out)]
    p = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if p.returncode != 0:
        print(f"error: ffmpeg failed: {p.stderr.strip()[-400:]}", file=sys.stderr)
        return 2
    if not out.is_file() or out.stat().st_size == 0:
        print("error: no audio output produced (source may have no audio stream)",
              file=sys.stderr)
        return 2
    print(f"wrote {out} ({out.stat().st_size} bytes, {a.sample_rate} Hz, "
          f"{'mono' if a.mono else 'stereo-capable'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
