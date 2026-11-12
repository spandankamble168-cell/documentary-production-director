# Cinematography Standards

## Shot choice serves information
Every shot answers: what must the viewer notice in these seconds? The camera
position, angle, and movement are chosen for that answer.

## Movement rules
- **Motivated**: push-in on realization, pull-out on aftermath, tracking on
  journey/pursuit, orbit on two-sided revelation. Static when the frame itself
  is the event.
- **Eased**: no linear camera moves; ease-in/out everywhere (Lemo `core/lib.js`
  easings; HyperFrames GSAP eases).
- **Speed**: a push-in over a 6 s scene should be barely noticeable per frame —
  check stills 1 s apart: if the change is jarring between consecutive stills,
  it is too fast.
- **One move per shot**: no compound moves unless the story demands it.
- Cut on motion or narration beats; avoid cutting mid-move to a mirrored move.

## Composition
- Foreground / midground / background intent in every scene.
- Rule of thirds as default; centered symmetry only with meaning.
- Headroom and lead room respected; key text in the 80% title-safe box.
- Depth cues: atmosphere, occlusion, parallax (Lemo scenes) or layered planes
  (HyperFrames).

## Continuity (planned in storyboard, verified in QC)
- Characters: consistent design, wardrobe, scale, screen direction within a
  sequence.
- Environments: consistent layout, light direction, palette per act.
- Props persist: what exists in frame stays in frame unless the story moves it.
- 180° line: conversing subjects keep left/right relation; deliberate flips
  need a neutral-axis shot between.
- Palette: one per act, recorded in `scenes.json`; grade shifts only at act
  boundaries.

## Defect watchlist (Critic)
excessive speed, unmotivated drift, repetitive compositions, broken screen
direction, mid-shot jumps, unexplained dutch angles, dead composition, safe-
area violations.
