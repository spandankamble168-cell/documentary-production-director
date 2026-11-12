# Animation Standards

## Determinism
- Every visible frame is a pure function of timeline time: no `Date.now()`,
  unseeded `Math.random()`, network fetches, timers, or `repeat: -1`
  (HyperFrames contract; same discipline in Lemo-Opuscar `render(t)`).

## Motion quality
- **Easing**: everything eases (ss/eio/eo/spring from `core/lib.js`, GSAP
  eases in HyperFrames). Linear motion only for mechanical subjects.
- **Weight**: objects accelerate in and settle out; nothing floats unless it
  is meant to (underwater, space, dream).
- **Anticipation & follow-through** on character/object actions: a move starts
  with a counter-move and ends with settle.
- **No frozen frames** mid-scene unless a deliberate hold; no end-frame snap.
- **Land early**: end states complete just before the clip's end (HyperFrames
  rule 1); holds show the finished composition, not the tween's last 10%.

## Timing
- Entrance/exit durations: 0.3–0.8 s for UI elements, longer for scenery.
- Text: typewriter/decoder effects must satisfy readcheck (full text visible
  ≥ characters ÷ 4.5 CJK / ÷ 15 latin + 1.5 s minimum).
- Camera and character motion sampled at the scene fps must be smooth:
  consecutive-frame displacement small and consistent (jitter is a defect).

## Text & legibility
- Contrast against background (HyperFrames `check` runs a contrast audit —
  fix every error, weigh every warning).
- Minimum readable size: ~2.5% of frame height for captions, ~3.5% for titles.
- No text over busy high-frequency backgrounds without a scrim/plate.

## Defect watchlist (Critic)
tweening `display`/`visibility`, transforms fighting GSAP, double transforms,
media started by script (`play()`), missing `id` on `<audio>`, fonts resolving
by name that aren't bundled, asset paths with leading `/`, frozen elements,
repeating loops, lip-sync errors (where inspectable).
