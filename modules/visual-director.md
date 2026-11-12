# Visual-director

Allocates every scene to an engine and owns `production/engine_manifest.json`
(validates against `schemas/engine_manifest.schema.json`) and
`assets/asset_manifest.json`.

## Engine selection defaults

| Scene requirement | Engine | Why |
|---|---|---|
| Titles, lower thirds, credits | HyperFrames | typographic precision, templates |
| Historical timelines, maps, charts, statistics, infographics | HyperFrames | data-graphics strength |
| UI/document/letter animations | HyperFrames | clip timing control |
| Cinematic 3D environments, atmospheric reenactments, stylized artistic sequences, camera movement in 3D | Lemo-Opuscar | three.js scenes with real camera grammar |
| Assembly, mastering, cross-fades between scene clips | FFmpeg | single source of truth for the final file |

These are defaults, not law — a HybridFrames chart *inside* a Lemo-Opuscar 3D
world is legitimate if the `engine_manifest.json` records it. Every scene gets:
`scene_id`, `engine`, `reason`, `source_location`, `dependencies`, `render_command`,
`output_path`, `duration_sec`, `resolution`, `fps`, `status`
(`PLANNED → IN_PROGRESS → RENDERED → VERIFIED`).

## HyperFrames specifics (verified commands only)

- New composition: `npx hyperframes init <dir> --skip-skills --skill=hyperframes`.
- Contract: every timed element `class="clip"` with `data-start`/`data-duration`;
  root `data-duration` is the film length; `window.__timelines[<composition-id>]`;
  no `Date.now()`, unseeded `Math.random()`, network fetches, timers or
  `repeat: -1`; fonts beyond the bundled set need `@font-face` from `assets/fonts/`.
- Gate: `npx hyperframes check --json` must pass (fix every error, weigh every
  warning), then `npx hyperframes snapshot` and actually read the PNGs.
- Render: `npx hyperframes render --quality looks -o out.mp4` (`draft` while
  iterating, `delivery` for final). Verify duration with ffprobe against root
  `data-duration`.
- Do not assume Pro features; prefer local render over cloud commands.

## Lemo-Opuscar specifics

- Scenes are pages implementing the page contract (`window.READY = true`,
  `window.render(t)`, `window.DUR`, optional `window.EV`, optional `TEXTS(t)`).
- Stills first: `node core/render/still.mjs <scene> <t>…` — read them before
  rendering video. Video: `node core/render/video.mjs <scene> --fps 24 --out out.mp4`
  (up to 6 workers; each parallel version needs its own `--out`).
- Text timing: `node core/render/readcheck.mjs <scene>` must pass before a scene
  with readable text counts as done.

## Assets

`assets/asset_manifest.json` records: id, filename, path, type, source, licence,
attribution requirement, associated scene, usage restrictions. Prefer original
generated assets and public-domain / CC0 / properly licensed material. Never
assume a free download allows commercial use; never bulk-download libraries
without asking the user.
