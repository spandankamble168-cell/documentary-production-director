# Documentary Production Director

An OpenCode skill that produces documentaries end to end — and then inspects,
scores, corrects and approves the rendered video like an outside QC studio.

Built on two already-installed engines on this machine:

- **HyperFrames** (`D:\documentary\.opencode\skills\`) — HTML-to-video motion
  graphics: titles, timelines, maps, charts, infographics.
- **Lemo-Opuscar** (`C:\Users\ASUS\lemo-opuscar`) — code-rendered cinematic 3D
  scenes, plus the voice tier (Kokoro offline English TTS, edge-tts for Chinese,
  Whisper speech-check) and the music tier (numba sample synthesis).
- **FFmpeg / FFmpeg 9.0.2** — assembly, mastering, all technical inspection.

No paid APIs, no subscriptions, no API keys required anywhere in the pipeline.

## Quick start

Say any of these to the OpenCode agent:

| Request | What happens |
|---|---|
| "Create a 10-minute documentary about X" | DIRECTOR mode: project scaffold → research → script → storyboard → narration → music/SFX → per-scene rendering → assembly |
| "Critic this documentary" / "Review D:\...\out.mp4" | CRITIC mode: metadata → frame sampling → contact sheet → audio analysis → scoring → defects → correction package |
| "Fix all high-priority problems" | Load latest critic report → map defects to scenes → re-render → re-inspect → verify |
| "Continue the documentary" | Read `project.json`, resume at the current stage, no repeated work |

## Scripts (system Python 3.12, FFmpeg required — no extra packages)

```
python scripts/environment_check.py            # capability registry (JSON + summary)
python scripts/validate_project.py --init D:\documentary\projects\my-film
python scripts/validate_project.py <project>   # validate layout + JSON files
python scripts/project_status.py <project>     # stage, score, open defects
python scripts/inspect_video.py <video> -o <project>\quality-control\video_metadata.json
python scripts/extract_audio.py <video> -o audio\analysis.wav
python scripts/extract_frames.py <video> -o frames\ --every 3 [--timestamps 12.5 44.1] [--around 88.0:6]
python scripts/generate_contact_sheet.py frames\ -o contact_sheet.jpg --cols 6
python scripts/detect_scenes.py <video> -o scenes.json [--threshold 0.3]
python scripts/analyze_audio.py <video-or-wav> -o audio_analysis.json
python scripts/compare_renders.py old.mp4 new.mp4 -o comparison.json
python scripts/validate_report.py --schema schemas/critic_report.schema.json --data report.json
```

All scripts print help with `--help`. Run them from anywhere; they accept
Windows and POSIX paths.

## Honesty model

The skill distinguishes three kinds of evidence and never mixes them:

1. **Measured** — FFprobe/FFmpeg numbers (duration, loudness, peaks, SSIM).
2. **Observed** — the agent actually reading extracted frames / contact sheets
   with vision. If that is impossible, reports say `VISUAL INSPECTION NOT
   AVAILABLE`.
3. **NOT EVALUATED** — anything else. Uninspectable categories get no score.

## Limitations (by design, on this hardware)

- 4 GB VRAM / 16 GB RAM: no local generative video or large AI models; visual
  quality comes from deterministic code-rendered scenes (HyperFrames,
  Lemo-Opuscar), which suits documentary motion graphics well.
- English narration is offline (Kokoro); Chinese narration uses free online
  edge-tts. Whisper runs locally on CPU.
- Large optional assets (instrument sample packs, HDRIs, Whisper models beyond
  `base`) are only downloaded after asking the user.
