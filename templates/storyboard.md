# Storyboard — {TITLE}

*One table row per scene; full per-scene spec in `scenes.json`
(`schemas/scene_spec.schema.json`). Camera vocabulary per
`references/cinematography_standards.md`.*

| Scene | Dur | Narration | Engine | Shot / angle | Movement (motivated by) | Key composition | Palette |
|---|---|---|---|---|---|---|---|
| SCENE-001 | 8.0s | NARR-001 | hyperframes | wide / eye | static | {…} | act-1 A |
| SCENE-002 | 12.0s | NARR-002 | lemo-opuscar | medium / low | push-in (realization) | {…} | act-1 A |

## Scene details
### SCENE-001 — {working title}
- Environment: {place, time, weather, era}
- Characters: {design, position, screen direction, consistency notes}
- Camera: {position, angle, FOV} · Movement: {type, start→end framing, motivation}
- Lighting: {…} · Palette: {…}
- Animation: {what moves, easing, timing}
- Foreground / Background / Atmosphere: {…}
- SFX: {…} · Music: {cue in/out, intensity}
- Transition: {…}
- Expected result: {one sentence on the finished shot}

{repeat per scene}

## Continuity ledger
- {characters consistent: …}
- {environments consistent: …}
- {props: …} · {screen direction: …} · {palette per act: …}

## Engine allocation summary
| Engine | Scenes | Rationale |
|---|---|---|
| hyperframes | {list} | titles, timelines, maps, charts |
| lemo-opuscar | {list} | cinematic 3D, atmosphere, reenactment |
| ffmpeg-assembly | — | concat/transitions/mux only |

Total duration: {sum}s (target {T}s ±5%)
