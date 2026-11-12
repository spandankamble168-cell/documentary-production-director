#!/usr/bin/env python3
"""Environment capability registry for the documentary-production-director skill.

Detects installed tools and reports their status WITHOUT installing anything.
Statuses: READY, INSTALLED_NOT_VERIFIED, OPTIONAL, MISSING, UNAVAILABLE.

Usage:
  python environment_check.py [--json] [--lib PATH] [--probe-hyperframes]
Output: capability_report.json (next to this script's invocation dir or --out).
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_LIB = Path(os.environ.get("LEMO_OPUSCAR_HOME", Path.home() / "lemo-opuscar"))
HF_SKILLS = SKILL_DIR.parent.parent.parent / ".opencode" / "skills"

READY, INSTALLED_NOT_VERIFIED, OPTIONAL, MISSING, UNAVAILABLE = (
    "READY", "INSTALLED_NOT_VERIFIED", "OPTIONAL", "MISSING", "UNAVAILABLE")


def _run(cmd, timeout=60):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, str(e)


def _version_line(cmd):
    rc, out = _run(cmd)
    if rc is None:
        return None, "could not run"
    first = out.strip().splitlines()[0] if out.strip() else ""
    return (rc == 0), first


def _check_binary(name, cmd):
    argv = list(cmd)
    if sys.platform == "win32" and argv[0] in ("npm", "npx"):
        argv = ["cmd", "/c"] + argv  # npm/npx are .cmd shims on Windows
    path = shutil.which(argv[0] if argv[0] != "cmd" else cmd[0])
    if not path:
        return {"capability": name, "status": MISSING, "location": None,
                "version": None, "limitations": "not on PATH"}
    ok, line = _version_line(argv)
    if ok:
        return {"capability": name, "status": READY, "location": path,
                "version": line, "limitations": None}
    return {"capability": name, "status": UNAVAILABLE, "location": path,
            "version": line[:120], "limitations": "ran but reported an error"}


def _check_lemo(lib: Path):
    rows = []
    base = {"capability": "Lemo-Opuscar library", "location": str(lib)}
    is_lib = (lib / "AGENTS.md").is_file() and (lib / "core" / "render").is_dir()
    rows.append({**base, "status": READY if is_lib else MISSING,
                 "version": None,
                 "limitations": None if is_lib else "AGENTS.md or core/ missing"})
    if not is_lib:
        for cap in ("Lemo core render", "Kokoro TTS", "edge-tts",
                    "Whisper (faster-whisper)", "music synthesis (numba/sampler)"):
            rows.append({"capability": cap, "status": MISSING, "location": str(lib),
                         "version": None, "limitations": "library not found"})
        return rows
    # core render tools
    tools = ["still.mjs", "video.mjs", "events.mjs", "readcheck.mjs"]
    have = all((lib / "core" / "render" / t).is_file() for t in tools)
    rows.append({"capability": "Lemo core render (still/video/events/readcheck)",
                 "status": READY if have else MISSING,
                 "location": str(lib / "core" / "render"), "version": None,
                 "limitations": None if have else "some render tools missing"})
    pw = (lib / "node_modules" / "playwright-core").is_dir()
    rows.append({"capability": "Playwright + headless Chromium",
                 "status": READY if pw else INSTALLED_NOT_VERIFIED,
                 "location": str(lib / "node_modules" / "playwright-core"),
                 "version": None,
                 "limitations": None if pw else
                 "playwright-core missing in library node_modules"})
    # python venv
    vpy = lib / ".venv" / "Scripts" / "python.exe"
    if not vpy.is_file():
        vpy = lib / ".venv" / "bin" / "python"
    venv_ok = vpy.is_file()
    rows.append({"capability": "Lemo .venv Python",
                 "status": READY if venv_ok else MISSING,
                 "location": str(vpy), "version": None,
                 "limitations": None if venv_ok else ".venv not found"})
    # voice tier
    model = lib / "core" / "tts" / "kokoro-v1.0.onnx"
    voices = lib / "core" / "tts" / "voices-v1.0.bin"
    tts = lib / "core" / "tts" / "tts.py"
    voice_ok = venv_ok and tts.is_file() and model.is_file() and voices.is_file()
    rows.append({"capability": "Kokoro TTS (offline English)",
                 "status": READY if voice_ok else MISSING,
                 "location": str(lib / "core" / "tts"),
                 "version": "kokoro-v1.0" if model.is_file() else None,
                 "limitations": "24 kHz output; espeak-ng path < 160 bytes" if voice_ok
                 else "model/voice files or tts.py missing"})
    for mod, cap in (("edge_tts", "edge-tts (online, free)"),
                     ("faster_whisper", "Whisper (faster-whisper)")):
        if venv_ok:
            rc, out = _run([str(vpy), "-c", f"import {mod}; print('ok')"], timeout=120)
            status = READY if rc == 0 else INSTALLED_NOT_VERIFIED
            lim = None if rc == 0 else (out.strip().splitlines()[-1][:160] if out.strip()
                                        else "import failed")
        else:
            status, lim = MISSING, "no venv"
        rows.append({"capability": cap, "status": status,
                     "location": str(lib / "core" / "tts"), "version": None,
                     "limitations": lim})
    # music tier
    mus = ["sfx.py", "sampler.py", "pluck.py"]
    have = all((lib / "core" / "audio" / f).is_file() for f in mus)
    numba = MISSING
    if venv_ok:
        rc, _ = _run([str(vpy), "-c", "import numba; print('ok')"], timeout=180)
        numba = READY if rc == 0 else INSTALLED_NOT_VERIFIED
    rows.append({"capability": "Procedural SFX (sfx.py)",
                 "status": READY if have else MISSING,
                 "location": str(lib / "core" / "audio"), "version": None, "limitations": None})
    rows.append({"capability": "Music synthesis (sampler.py / pluck.py)",
                 "status": READY if have and numba == READY else INSTALLED_NOT_VERIFIED,
                 "location": str(lib / "core" / "audio"), "version": None,
                 "limitations": "sample libraries may still be absent (fetched on demand)"
                 if have and numba == READY else "files or numba missing"})
    inst = lib / "core" / "audio" / "instruments"
    have_inst = inst.is_dir() and any(inst.iterdir()) if inst.is_dir() else False
    rows.append({"capability": "Instrument sample libraries",
                 "status": READY if have_inst else OPTIONAL,
                 "location": str(inst), "version": None,
                 "limitations": None if have_inst else
                 "not downloaded; fetch per library via tools/fetch.sh instruments <lib> (ask user)"})
    hdri = lib / "core" / "assets" / "polyhaven"
    have_hdri = hdri.is_dir() and any(hdri.iterdir()) if hdri.is_dir() else False
    rows.append({"capability": "CC0 HDRIs (Poly Haven)",
                 "status": READY if have_hdri else OPTIONAL,
                 "location": str(hdri), "version": None,
                 "limitations": None if have_hdri else "not downloaded; tools/fetch.sh hdri (ask user)"})
    return rows


def _check_hyperframes(probe: bool):
    rows = []
    for cap, dirname in (("HyperFrames skill docs", "hyperframes"),
                         ("HyperFrames CLI docs", "hyperframes-cli"),
                         ("HyperFrames Registry", "hyperframes-registry")):
        d = HF_SKILLS / dirname
        present = (d / "SKILL.md").is_file()
        rows.append({"capability": cap,
                     "status": READY if present else MISSING,
                     "location": str(d), "version": None,
                     "limitations": None if present else "SKILL.md not found"})
    cli = {"capability": "HyperFrames CLI (npx hyperframes)",
           "status": INSTALLED_NOT_VERIFIED, "location": "npx",
           "version": None,
           "limitations": "requires Node 22+ and FFmpeg; version not probed"}
    if probe:
        rc, out = _run(["npx", "--no-install", "hyperframes", "--version"], timeout=90)
        if rc == 0:
            cli.update(status=READY, version=out.strip()[:40], limitations=None)
        else:
            cli.update(status=MISSING, limitations=f"probe failed: {out.strip()[:160]}")
    rows.append(cli)
    return rows


def _check_agent_capabilities():
    return [
        {"capability": "Vision inspection (agent reads extracted frames as images)",
         "status": INSTALLED_NOT_VERIFIED, "location": "agent model", "version": None,
         "limitations": "depends on the running agent model being able to read "
                        "images; verify by reading one frame before scoring visual "
                        "categories, else write VISUAL INSPECTION NOT AVAILABLE"},
        {"capability": "Audio listening (subjective judgement of sound)",
         "status": UNAVAILABLE, "location": None, "version": None,
         "limitations": "no listening capability; audio review is numerical "
                        "measurement only (analyze_audio.py)"},
        {"capability": "Web research (agent web-search tools)",
         "status": INSTALLED_NOT_VERIFIED, "location": "agent harness", "version": None,
         "limitations": "depends on harness search integration; never fabricate "
                        "sources when unavailable"},
    ]


def build_report(lib: Path, probe: bool):
    rows = []
    rows.append({"capability": "Python", "status": READY,
                 "location": sys.executable,
                 "version": f"{sys.version_info.major}.{sys.version_info.minor}."
                            f"{sys.version_info.micro}", "limitations": None})
    for name, cmd in (("Node.js", ["node", "--version"]),
                      ("npm", ["npm", "--version"]),
                      ("FFmpeg", ["ffmpeg", "-version"]),
                      ("FFprobe", ["ffprobe", "-version"]),
                      ("Git", ["git", "--version"])):
        rows.append(_check_binary(name, cmd))
    rows += _check_lemo(lib)
    rows += _check_hyperframes(probe)
    rows += _check_agent_capabilities()
    counts = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    return {"generated_at": datetime.now(timezone.utc).isoformat(),
            "machine": {"platform": sys.platform,
                        "python": sys.version.split()[0]},
            "library": str(lib), "capabilities": rows, "summary": counts}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true", help="print full JSON report")
    ap.add_argument("--lib", default=str(DEFAULT_LIB), help="Lemo-Opuscar library path")
    ap.add_argument("--out", default=None, help="output JSON path (default: capability_report.json)")
    ap.add_argument("--probe-hyperframes", action="store_true",
                    help="also run 'npx --no-install hyperframes --version' (slower)")
    a = ap.parse_args()
    report = build_report(Path(a.lib), a.probe_hyperframes)
    out = Path(a.out) if a.out else Path("capability_report.json")
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    if a.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Capability report written to {out}\n")
        print(f"{'STATUS':<22} CAPABILITY")
        for r in report["capabilities"]:
            print(f"{r['status']:<22} {r['capability']}")
        print(f"\nSummary: {report['summary']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
