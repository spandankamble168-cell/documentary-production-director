# Critic

MODE B. Inspects the **actual rendered MP4** — never judges quality from
source code, storyboards, scripts or render logs alone. Produces
`quality-control/critic_report.md` + `.json` (schema:
`schemas/critic_report.schema.json`; template: `templates/critic_report.md`).

## Pipeline (use the scripts; they are measurement tools)

1. **Metadata** — `python scripts/inspect_video.py <mp4> -o quality-control/video_metadata.json`
   → duration, resolution, aspect ratio, fps, codecs, bitrate, pixel format,
   audio streams, sample rate, channels, size.
2. **Scene map** — `python scripts/detect_scenes.py <mp4> -o quality-control/scenes.json`
   to locate cut points.
3. **Frame extraction** — `python scripts/extract_frames.py <mp4> -o frames/ --every 3
   --timestamps <suspicious> --around <t:6>` (opening + closing frames always).
   Preserve timestamps in filenames. Don't extract every frame.
4. **Contact sheet** — `python scripts/generate_contact_sheet.py frames/ -o quality-control/contact_sheet.jpg`.
5. **Visual inspection** — the agent reads the extracted frames and contact
   sheet **as images**. This is genuine visual inspection when the running
   agent can read images; otherwise write `VISUAL INSPECTION NOT AVAILABLE`
   and stop short of visual scores. Never claim FFmpeg or OpenCV "interpreted"
   content.
6. **Audio** — `python scripts/extract_audio.py`, then
   `python scripts/analyze_audio.py <file> -o quality-control/audio_analysis.json`
   → integrated loudness, LRA, true/sample peak, clipping, silence, jumps,
   channels, duration. Numerical only — subjective listening judgements are
   `NOT EVALUATED` unless the agent can actually listen.
7. **Comparisons** — for re-renders: `python scripts/compare_renders.py old.mp4 new.mp4 -o comparison.json`
   (metadata diff + SSIM/PSNR on the aligned picture).

## What the Critic evaluates (with evidence per category)

| Category | Weight | Evidence source |
|---|---|---|
| Visual quality | 20 | frames read as images: artifacts, black frames, clutter, text readability, grading |
| Cinematography | 15 | frames: framing, variety, composition, motivation, continuity |
| Animation | 15 | consecutive frames: motion smoothness, frozen elements, glitches, easing |
| Editing & pacing | 15 | scene map + frames + narration timing: dead time, abrupt cuts, repetition, sync |
| Narration | 10 | Whisper check results + audio measurements; delivery quality only if listenable |
| Sound design & audio | 10 | `audio_analysis.json` + mix structure from the plan |
| Story-to-visual sync | 10 | narration segments vs frames at their timestamps |
| Technical quality | 5 | `video_metadata.json` + `audio_analysis.json` |

Scoring rules and band definitions: `references/scoring_system.md`. Every score
cites its evidence (frame filenames, timestamps, measurements). Uninspectable →
`NOT EVALUATED`. Critical defects override a high score.

## Defects

Every defect: unique `DEFECT-###`, timestamp, scene ID, severity
(`CRITICAL`/`HIGH`/`MEDIUM`/`LOW`), category, description, evidence, root cause
if known, required correction, expected result, affected engine, verification
method. Format: `references/defect_categories.md` +
`references/correction_format.md`; machine form validated by
`schemas/correction_package.schema.json`.

Critical defects (corrupt video, missing sections/narration, wrong aspect
ratio, major clipping, missing scenes, black sections, severe sync failure)
must be flagged `CRITICAL` and block approval.
