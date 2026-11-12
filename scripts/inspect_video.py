#!/usr/bin/env python3
"""Inspect a video with FFprobe and write normalized video_metadata.json.

Usage:
  python inspect_video.py <video> [-o video_metadata.json]
Exit codes: 0 ok, 1 input missing/not a file, 2 ffprobe failed.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def ffprobe_json(path: Path):
    p = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json",
         "-show_format", "-show_streams", str(path)],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "ffprobe failed")
    return json.loads(p.stdout or "{}")


def _rate(r: str):
    if not r or r == "0/0":
        return None
    try:
        num, den = r.split("/")
        d = float(den)
        return round(float(num) / d, 6) if d else None
    except (ValueError, ZeroDivisionError):
        return None


def build_metadata(path: Path, probe: dict):
    fmt = probe.get("format", {})
    streams = probe.get("streams", [])
    v = next((s for s in streams if s.get("codec_type") == "video"), None)
    a = next((s for s in streams if s.get("codec_type") == "audio"), None)
    vstreams = [s for s in streams if s.get("codec_type") == "video"]
    astreams = [s for s in streams if s.get("codec_type") == "audio"]
    md = {
        "file": str(path),
        "inspected_at": datetime.now(timezone.utc).isoformat(),
        "container": fmt.get("format_name"),
        "duration_sec": float(fmt["duration"]) if fmt.get("duration") else None,
        "size_bytes": int(fmt["size"]) if fmt.get("size", "").isdigit() else fmt.get("size"),
        "bitrate_bps": int(fmt["bit_rate"]) if fmt.get("bit_rate", "").isdigit() else None,
        "video": None, "audio": None,
        "video_stream_count": len(vstreams),
        "audio_stream_count": len(astreams),
        "measurement": "ffprobe -show_format -show_streams (numerical only)",
    }
    if v:
        w, h = v.get("width"), v.get("height")
        md["video"] = {
            "codec": v.get("codec_name"), "profile": v.get("profile"),
            "width": w, "height": h,
            "aspect_ratio": v.get("display_aspect_ratio"),
            "fps": _rate(v.get("avg_frame_rate")) or _rate(v.get("r_frame_rate")),
            "pix_fmt": v.get("pix_fmt"),
            "bitrate_bps": int(v["bit_rate"]) if v.get("bit_rate", "").isdigit() else None,
        }
    if a:
        md["audio"] = {
            "codec": a.get("codec_name"), "sample_rate": a.get("sample_rate"),
            "channels": a.get("channels"),
            "channel_layout": a.get("channel_layout"),
            "bitrate_bps": int(a["bit_rate"]) if a.get("bit_rate", "").isdigit() else None,
        }
    return md


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("video")
    ap.add_argument("-o", "--out", default="video_metadata.json")
    a = ap.parse_args()
    src = Path(a.video)
    if not src.is_file():
        print(f"error: not a file: {src}", file=sys.stderr)
        return 1
    try:
        probe = ffprobe_json(src)
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    md = build_metadata(src, probe)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(md, indent=2), encoding="utf-8")
    print(json.dumps(md, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
