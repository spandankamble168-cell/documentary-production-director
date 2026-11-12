# Changelog

## 0.1.0 — 2026-11-12

Initial release.

### Added
- SKILL.md: unified Director + Critic skill definition, shared project state,
  verified integration table for HyperFrames, Lemo-Opuscar (core/voice/music
  tiers) and FFmpeg.
- 14 specialist modules under `modules/` (director, researcher, fact-checker,
  scriptwriter, story-editor, storyboard-artist, cinematographer,
  visual-director, animation-director, sound-designer, voice-director,
  production-manager, critic, quality-controller).
- 11 Python utility scripts under `scripts/` (stdlib + FFmpeg only):
  environment_check, inspect_video, extract_audio, extract_frames,
  generate_contact_sheet, detect_scenes, analyze_audio, compare_renders,
  validate_project, validate_report, project_status.
- 8 JSON schemas under `schemas/` (production plan, research report, script,
  storyboard, scene spec, engine manifest, critic report, correction package).
- 13 reference standards under `references/`, 6 templates under `templates/`.
- Project-state layout with resumable stages and a 5-round QC loop.

### Verified on this machine at build time
- FFmpeg/FFprobe 9.0.2, Node 26.13.0, npm 11.20.0, Python 3.12.10, Git 2.55.0.
- Lemo-Opuscar library present with Kokoro model (`core/tts/kokoro-v1.0.onnx`,
  `voices-v1.0.bin`), core/voice/music tiers installed; `edge_tts`,
  `faster_whisper`, `numba` import successfully in the library venv.
- HyperFrames skills present under `the local .opencode skills directory`.
- All 11 scripts compile and pass `--help`; all 8 schemas parse.
- `environment_check.py` run for real (capability registry correct after two
  bug fixes: Windows npm `.cmd` shim, HyperFrames skill path).
- `validate_project.py --init`, `validate_project.py`, `project_status.py`
  tested on a scaffolded empty project (temp dir).
- `validate_report.py` tested with a valid and an invalid correction-package
  fixture: valid passes, invalid rejected with 13 precise errors (after two
  bug fixes: BOM tolerance, JSON-Schema type arrays).
- Media scripts tested against a synthetic FFmpeg `testsrc2` clip (fixture for
  tooling only, not presented as documentary content): `inspect_video.py`,
  `detect_scenes.py`, `extract_frames.py`, `generate_contact_sheet.py`,
  `analyze_audio.py`, `compare_renders.py` (SSIM 1.0 on identical input)
  (after three bug fixes: tile filter graph, ssim/psnr label graph, clipping
  heuristic).
- Agent-vision loop verified: contact sheet read as an image by the agent.
- Kokoro TTS verified end-to-end: one line generated offline, `dur.json` and
  WAV duration confirmed with ffprobe (3.499 s).

### Known limits
- No local generative video model (4 GB VRAM); stylized visuals are
  code-rendered only.
- Whisper `asr_check.py` not exercised (would download the `base` model,
  ~150 MB — left for first real use, with user awareness).
- HyperFrames CLI probe deferred (`--probe-hyperframes`); skills' docs verified
  present. Full render of a HyperFrames project not exercised at build time.
- Lemo-Opuscar scene render (still.mjs/video.mjs) not exercised at build time;
  verified via library documentation and file presence.
- `extract_audio.py` tested indirectly via analyze_audio on the test clip.
