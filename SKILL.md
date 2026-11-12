---
name: documentary-production-director
description: >
  Unified documentary production system: DIRECTOR mode (research, fact-checking,
  scripting, storyboarding, cinematography, narration, music/sound, scene
  rendering with HyperFrames and Lemo-Opuscar, final assembly with FFmpeg) and
  CRITIC mode (actual MP4 inspection, frame sampling, contact sheets, audio
  analysis, 100-point scoring, timestamped defects, correction packages, QC
  loop, final approval). Use when the user asks to create, produce, continue,
  research or script a documentary, or to review, critique, inspect, score,
  compare or fix a rendered documentary video.
---

# Documentary Production Director

Two roles, one skill, one shared project state. The agent running this skill is
the director **and** the critic; the project directory on disk is the shared
brain. Never keep production state only in the conversation.

## Non-negotiable rules

1. **Honesty about evidence.** Never fabricate research sources, visual
   observations, audio observations, or scores. Every score has supporting
   evidence from actual inspection. If a category cannot be inspected, write
   `NOT EVALUATED` — never a guessed number.
2. **Vision truth.** The agent may read extracted frame images and contact
   sheets directly (that is genuine visual inspection). Numerical FFmpeg output
   is measurement, not interpretation — keep them separate in every report. If
   the running agent cannot read images, write `VISUAL INSPECTION NOT
   AVAILABLE`.
3. **Free pipeline.** No mandatory paid APIs, subscriptions, API keys or cloud
   render services. The agent model itself may be cloud-hosted; do not claim
   the pipeline is fully offline or unlimited.
4. **Do not reinstall.** HyperFrames and Lemo-Opuscar are already installed.
   Detect them, read their docs, use them. Ask before any substantial optional
   download (models, sample libraries, HDRIs).
5. **Resource limits.** Target machine: RTX 2050 4 GB VRAM, 16 GB RAM. No large
   model in RAM/VRAM unnecessarily, no whole-video loading, frame sampling for
   inspection, chunked processing for long renders.
6. **Do not invent commands.** Only use commands verified in this skill, in the
   HyperFrames skills, or in `$LEMO_OPUSCAR_HOME/core/README.md`.
   Claim nothing as tested that was not tested.

## Modes

- **MODE A — DIRECTOR.** Activated by: new documentary, research,
  fact-checking, concepts, script, storyboard, scene direction, narration,
  music/sound, rendering, project continuation. Load the needed module under
  `modules/` before doing its work.
- **MODE B — CRITIC.** Activated by: video review, MP4 inspection, quality
  assessment, audio analysis, narration review, editing/pacing critique, render
  comparison, corrections, approval. Load `modules/critic.md` and
  `modules/quality-controller.md`.

Transition is automatic: production ends by handing its render to the critic;
corrections return it to the director. The loop is:

```
DIRECTOR → RESEARCH → SCRIPT → STORYBOARD → PRODUCTION → CRITIC
   → CORRECTIONS → RERENDER → CRITIC → ... → FINAL APPROVAL
```

Maximum **five** correction rounds. Final approval requires zero unresolved
critical defects.

## First move in any session

Run the environment check once per machine, cache the result in the project:

```
python scripts/environment_check.py [--json] [--lib $LEMO_OPUSCAR_HOME]
```

Statuses: `READY`, `INSTALLED_NOT_VERIFIED`, `OPTIONAL`, `MISSING`,
`UNAVAILABLE`. Report missing required components and ask before installing.

## Project layout

Every documentary lives in `<workspace>/projects/<documentary-name>/`:

```
project.json            state: stage, rounds, score, open defects, approval
production_plan.md
research/   research_report.md  claims.json  sources.json
script/     documentary_script.md  narration.json  pronunciation_guide.md
storyboard/ storyboard.md  scenes.json
assets/     asset_manifest.json  (+ files)
production/ engine_manifest.json  hyperframes/  lemo-opuscar/
audio/      narration/  music/  sfx/
renders/    round-01/ round-02/ ... final/
quality-control/  critic_report.md/.json  correction_package.json
                  video_metadata.json  audio_analysis.json
                  contact_sheet.jpg  correction_history.json
delivery/
```

Create it with `scripts/validate_project.py --init <dir>` (scaffolds and
validates). Check state any time with `scripts/project_status.py <dir>`.
Interrupted work resumes from `project.json` — never redo completed stages.

## Tool integration (verified commands)

| Job | Engine | Command |
|---|---|---|
| Titles, timelines, maps, charts, infographics, motion graphics | HyperFrames | `npx hyperframes init <dir> --skip-skills --skill=hyperframes`; `check --json`; `snapshot`; `render --quality looks -o out.mp4` (see `.opencode\skills\hyperframes*`) |
| Cinematic 3D scenes, artistic environments, stylized reenactment | Lemo-Opuscar | from `$LEMO_OPUSCAR_HOME`: `node core/render/still.mjs <scene> <t>…`; `node core/render/video.mjs <scene> --fps 24 --out out.mp4`; `readcheck.mjs` for text timing (page contract: `window.READY`, `render(t)`, `DUR`, `EV`, `TEXTS(t)`) |
| English narration (offline) | Lemo voice tier | `.venv/bin/python core/tts/tts.py narration.json out_dir` — `[{id, text, voice?, speed?, lang?}]`, defaults `af_bella`/`0.92`/`en-us`; unknown voice name prints the voice list |
| Chinese narration (online, free) | edge-tts | `.venv/bin/python core/tts/tts_zh.py lines.json out_dir --voice zh-CN-XiaoxiaoNeural` |
| Narration verification | Whisper | `.venv/bin/python core/tts/asr_check.py lines.json voices_dir [--lang en] [--model base]` |
| Music / SFX | Lemo music tier | `core/audio/sfx.py` (procedural), `core/audio/sampler.py`, `core/audio/pluck.py` (numba); missing sample library names its `tools/fetch.sh instruments <lib>` command |
| Mix + master | FFmpeg / Lemo mux | `sh core/render/mux.sh video.mp4 mix.wav out.mp4 [fps=24] [grain=2]` → −14 LUFS, true peak ≤ −1 dBTP |
| Scene clips inspection | this skill | `python scripts/inspect_video.py`, `extract_frames.py`, `generate_contact_sheet.py`, `analyze_audio.py`, `detect_scenes.py`, `compare_renders.py` |
| Subtitles | Lemo srt.py | `.venv/bin/python core/render/srt.py cues.json out.srt` |

Per-scene engine choice is recorded in `production/engine_manifest.json`
(schema: `schemas/engine_manifest.schema.json`; guidance:
`modules/visual-director.md`). Licences for any external asset are recorded in
`assets/asset_manifest.json` — never assume a free download is commercial-use.

## Module map

| Module | Load when |
|---|---|
| `modules/director.md` | always in MODE A |
| `modules/researcher.md`, `modules/fact-checker.md` | research stage |
| `modules/scriptwriter.md`, `modules/story-editor.md` | script stage |
| `modules/storyboard-artist.md`, `modules/cinematographer.md` | storyboard stage |
| `modules/visual-director.md`, `modules/animation-director.md` | production stage |
| `modules/voice-director.md`, `modules/sound-designer.md` | audio stages |
| `modules/production-manager.md` | project state, rendering rounds |
| `modules/critic.md`, `modules/quality-controller.md` | MODE B and every QC round |

Standards live in `references/`, output skeletons in `templates/`, machine
contracts in `schemas/`. Implementation history: `CHANGELOG.md`; usage guide:
`README.md`.
