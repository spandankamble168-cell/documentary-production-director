#!/usr/bin/env python3
"""Compare two renders: metadata diff plus SSIM/PSNR on the aligned picture.

Usage:
  python compare_renders.py <old.mp4> <new.mp4> [-o comparison.json]
SSIM/PSNR are only computed when both files share resolution and pixel format;
otherwise the report records the mismatch. Numerical comparison only.
Exit codes: 0 ok, 1 input missing, 2 ffmpeg failure.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def probe(path: Path):
    p = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format",
         "-show_streams", str(path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "ffprobe failed")
    d = json.loads(p.stdout or "{}")
    fmt = d.get("format", {})
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    a = next((s for s in d.get("streams", []) if s.get("codec_type") == "audio"), {})
    return {
        "duration_sec": float(fmt["duration"]) if fmt.get("duration") else None,
        "size_bytes": int(fmt["size"]) if fmt.get("size", "").isdigit() else None,
        "resolution": f'{v.get("width")}x{v.get("height")}',
        "fps": v.get("avg_frame_rate"),
        "pix_fmt": v.get("pix_fmt"),
        "video_codec": v.get("codec_name"),
        "audio": {k: a.get(k) for k in ("codec_name", "sample_rate", "channels")},
    }


def quality_metrics(a: Path, b: Path):
    fc = "[0:v][1:v]ssim=shortest=1[l];[l][1:v]psnr=shortest=1"
    p = subprocess.run(
        ["ffmpeg", "-i", str(a), "-i", str(b), "-filter_complex", fc,
         "-an", "-f", "null", "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError("SSIM/PSNR pass failed: " + p.stderr.strip()[-400:])
    err = p.stderr
    ssim = psnr = None
    m = re.search(r"SSIM.*All:([0-9.]+)", err)
    if m:
        ssim = float(m.group(1))
    m = re.search(r"PSNR.*average:([0-9.]+|inf)", err)
    if m:
        psnr = float(m.group(1)) if m.group(1) != "inf" else 999.0
    return {"ssim_mean": ssim, "psnr_avg_db": psnr,
            "interpretation": "1.0 SSIM = identical picture; SSIM > 0.99 = "
                              "effectively unchanged; < 0.95 = visibly different"}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("old")
    ap.add_argument("new")
    ap.add_argument("-o", "--out", default="comparison.json")
    a = ap.parse_args()
    old, new = Path(a.old), Path(a.new)
    for f in (old, new):
        if not f.is_file():
            print(f"error: not a file: {f}", file=sys.stderr)
            return 1
    try:
        mo, mn = probe(old), probe(new)
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    comparable = (mo["resolution"] == mn["resolution"]
                  and mo["pix_fmt"] == mn["pix_fmt"] and mo["fps"] == mn["fps"])
    result = {"old": str(old), "new": str(new),
              "metadata": {"old": mo, "new": mn},
              "picture_comparable": comparable,
              "notes": []}
    if comparable:
        try:
            result["quality"] = quality_metrics(old, new)
        except RuntimeError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
    else:
        result["notes"].append(
            "SSIM/PSNR skipped: resolution, pixel format or fps differ between renders")
    d1, d2 = mo["duration_sec"], mn["duration_sec"]
    if d1 is not None and d2 is not None and abs(d1 - d2) > 0.5:
        result["notes"].append(f"duration differs by {abs(d1 - d2):.2f} s")
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
