# Animation-director

Implements and renders the scenes assigned by the Visual-director. Owns the
actual page/code work in `production/hyperframes/` and `production/lemo-opuscar/`.

## Lemo-Opuscar scene implementation

Library root: `$LEMO_OPUSCAR_HOME` (env `LEMO_OPUSCAR_HOME` overrides).
Read `$LIB/AGENTS.md` and the chosen style's `STYLE.md` before writing a scene;
copy what you need into the project folder — never build inside `$LIB/styles/`.

Page contract (from `core/README.md`, verified):
- `window.READY = true` once fonts/images loaded; `window.render(t)` draws the
  deterministic frame at second `t`; `window.DUR` = length; optional
  `window.EV = [{t, type, …}]` for sound/cues (exported by `events.mjs`);
  optional `TEXTS(t)` for readcheck.
- Viewport 1920×1080 default; `--size WxH`; `--q 'k=v&…'` passes parameters.
- Use `core/lib.js` helpers (seeded random, easings, `seg`, `env`),
  `core/three/post.js` for DOF/GTAO/bloom/grade, `core/post/crt.js` for CRT/VHS.
- Bundled OFL fonts in `core/fonts/`; HDRIs in `core/assets/polyhaven/` (CC0).

Render loop per scene (never skip the still pass):
```
node core/render/still.mjs <scene> 0.5 2 4 6 … [--range a:b:step]   # read the JPEGs, fix, repeat
node core/render/readcheck.mjs <scene>                              # if the scene has readable text
node core/render/video.mjs <scene> --fps 24 --out <scene>/out/video.mp4
```
A WebGL blank (lost context) exits 1 — retry; if persistent, ask for
`LEMO_ANGLE=swiftshader` (software, slow).

## HyperFrames scene implementation

Follow the HyperFrames contract in `modules/visual-director.md` and the
HyperFrames skill docs. One scene = one sub-composition. `check --json` clean,
snapshots read by eye, then render.

## Animation quality bar

- Motion has weight and easing (`ss`, `eio`, `eo`, `spring` — not linear
  unless mechanical).
- Deterministic: no `Date.now()`, unseeded randomness, timers, `repeat: -1`.
- Nothing freezes mid-motion or snaps at the end frame; land end states just
  before clip end.
- Camera moves eased and motivated (see `cinematographer.md`).

## Resource discipline

Render one scene at a time; `RENDER_SLOTS` limits concurrency. Headless
Chromium is CPU-heavy — don't render two scenes simultaneously on this laptop
unless a render is long and the user is waiting. Report render failures
honestly; retry with a fix, not a blind loop.
