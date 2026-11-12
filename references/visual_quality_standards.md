# Visual Quality Standards

## What counts as visual evidence
- **Observed**: the agent reads extracted frame images / contact sheets. This
  is genuine visual inspection and the basis of visual scores. The frame
  filename is the citation.
- **Measured**: FFprobe/FFmpeg numbers (resolution, fps, black-frame timing,
  SSIM). Real, but not interpretation.
- Neither may be invented. No observation without a frame; no score without
  observations or measurements.

## Checks (on sampled frames, every 2–3 s + suspicious timestamps)
| Check | Method |
|---|---|
| Rendering artifacts | read frames: banding, z-fighting, broken geometry, missing textures |
| Black/unintended frames | read frames + scene map gaps |
| Text readability | read frames: contrast, size, duration (readcheck for Lemo scenes) |
| Visual clutter | read frames: more than ~3 competing elements is clutter |
| Colour grading consistency | read frames across an act: one palette |
| Character consistency | read frames across scenes: same design/wardrobe/scale |
| Environment continuity | read frames: layout, light direction, props persist |
| Repetition | compare frames: same composition reused as filler |
| Composition safety | read frames: key content in title-safe box |

## Grading
- One palette per act; no per-scene random grading.
- Contrast ratio for text ≥ 4.5:1 against its immediate background
  (HyperFrames contrast audit; visually re-verified on frames).

## Common Lemo-Opuscar failure modes to check
- lost WebGL context → blank/black frames (render exits 1; check regardless).
- `window.READY` fired before textures loaded → first frames untextured.
- Bloom/DOF overdriven → white clipping (read bright-scene frames).
- 3D text/labels unreadable at camera extremes.

## Common HyperFrames failure modes to check
- unmounted scene (tiny unstyled content) at composition midpoint.
- clip overlapping neighbours (z-index surprises).
- assets with leading `/` path → silently missing images.
- end-state not landed before clip end → last frame mid-tween.

## Scoring tie-in
Visual quality (20 pts) is scored from these checks. Critical defects
(black sections, corrupted frames, missing scenes) override an otherwise
high score.
