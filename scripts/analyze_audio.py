#!/usr/bin/env python3
"""Analyze the audio of a video or audio file with FFmpeg (numerical measurement).

Usage:
  python analyze_audio.py <video-or-audio> -o audio_analysis.json
Measures (numerical only — this is NOT listening):
  - integrated loudness (LUFS), LRA, true peak, threshold   [EBU R128 loudnorm]
  - RMS level, peak level, clipped-sample counts            [astats]
  - silence segments >= 2 s below -50 dB                    [silencedetect]
  - duration, channels, sample rate                         [ffprobe]
Exit codes: 0 ok, 1 input missing, 2 ffmpeg failure.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def _run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, p.stdout or "", p.stderr or ""


def probe(path: Path):
    rc, out, err = _run(["ffprobe", "-v", "error", "-print_format", "json",
                         "-show_format", "-show_streams", str(path)])
    if rc != 0:
        raise RuntimeError(err.strip() or "ffprobe failed")
    d = json.loads(out or "{}")
    fmt = d.get("format", {})
    a = next((s for s in d.get("streams", []) if s.get("codec_type") == "audio"), None)
    return {"duration_sec": float(fmt["duration"]) if fmt.get("duration") else None,
            "sample_rate": a.get("sample_rate") if a else None,
            "channels": a.get("channels") if a else None,
            "codec": a.get("codec_name") if a else None}


def loudnorm(path: Path):
    rc, _, err = _run(["ffmpeg", "-i", str(path), "-vn",
                       "-af", "loudnorm=print_format=json", "-f", "null", "-"])
    if rc != 0:
        raise RuntimeError("loudnorm pass failed: " + err.strip()[-300:])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", err, re.S)
    if not m:
        return None
    d = json.loads(m.group(0))
    def num(k):
        try:
            return float(d[k])
        except (KeyError, TypeError, ValueError):
            return None
    return {"integrated_loudness_lufs": num("input_i"),
            "true_peak_dbtp": num("input_tp"),
            "lra_lu": num("input_lra"),
            "threshold_lufs": num("input_thresh")}


def astats(path: Path):
    rc, _, err = _run(["ffmpeg", "-i", str(path), "-vn",
                       "-af", "astats=metadata=1:reset=0", "-f", "null", "-"])
    if rc != 0:
        raise RuntimeError("astats pass failed: " + err.strip()[-300:])
    peak = rms = None
    clipped = None
    for line in err.splitlines():
        if "Peak level dB:" in line and peak is None:
            peak = float(line.split(":")[1].strip())
        elif "RMS level dB:" in line and rms is None:
            rms = float(line.split(":")[1].strip())
        elif "Peak count:" in line and clipped is None:
            m = re.search(r"Peak count:\s*([0-9.e+]+)", line)
            clipped = float(m.group(1)) if m else None
    return {"sample_peak_dbfs": peak, "rms_level_dbfs": rms,
            "clipped_samples": clipped}


def silences(path: Path):
    rc, _, err = _run(["ffmpeg", "-i", str(path), "-vn",
                       "-af", "silencedetect=noise=-50dB:d=2", "-f", "null", "-"])
    if rc != 0:
        raise RuntimeError("silencedetect pass failed: " + err.strip()[-300:])
    segs, start = [], None
    for line in err.splitlines():
        if "silence_start:" in line:
            start = float(line.split("silence_start:")[1].strip())
        elif "silence_end:" in line and start is not None:
            end = float(line.split("silence_end:")[1].split("|")[0].strip())
            segs.append({"start_sec": round(start, 3), "end_sec": round(end, 3),
                         "duration_sec": round(end - start, 3)})
            start = None
    if start is not None:  # silence ran to the end of input
        segs.append({"start_sec": round(start, 3), "end_sec": None, "duration_sec": None})
    return segs


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("input")
    ap.add_argument("-o", "--out", default="audio_analysis.json")
    a = ap.parse_args()
    src = Path(a.input)
    if not src.is_file():
        print(f"error: not a file: {src}", file=sys.stderr)
        return 1
    try:
        meta = probe(src)
        ln = loudnorm(src)
        st = astats(src)
        sil = silences(src)
    except RuntimeError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    tp = (ln or {}).get("true_peak_dbtp")
    sp = st.get("sample_peak_dbfs")
    result = {
        "file": str(src),
        **meta,
        "loudness": ln,
        "levels": st,
        "silence_segments_below_-50dB_ge_2s": sil,
        "possible_clipping": bool(
            (tp is not None and tp > -0.1) or (sp is not None and sp >= -0.5)),
        "method": "ffmpeg loudnorm/astats/silencedetect — numerical measurement only; "
                  "no listening was performed",
    }
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
