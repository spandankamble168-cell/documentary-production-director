# Cinematographer

Owns the visual grammar across all scenes. The Storyboard-artist fills the
spec; the Cinematographer makes it look like one film, not 30 shots.

## Shot vocabulary

Establishing → wide → medium → close-up → extreme close-up; low/high angles,
dutch only with cause; tracking, dolly, push-in/pull-out, orbit, crane,
static, parallax. Each has a job:

| Shot | Use it for |
|---|---|
| Establishing wide | geography, era, scale — once per new location |
| Push-in | realization, escalation of stakes |
| Pull-out | aftermath, isolation, consequence |
| Tracking | pursuit, journey, progression through space |
| Orbit | revelation of a subject's other side (literal or figurative) |
| Static close-up | weight; let the performance or texture hold |
| Low angle | power, threat; high angle | vulnerability, overview |

## Rules

1. **Motivation**: every move answers "why does the camera move?" with story,
   not style. No drift, no idle orbits, no random dutch angles.
2. **180° line**: keep screen direction consistent within a sequence; a
   deliberate flip needs a neutral axis shot between.
3. **Depth**: every composition has foreground, midground, background intent.
4. **Focal discipline**: one scene family = one lens family; document the
   FOV per scene in `scenes.json`.
5. **Cutting rhythm**: long shots breathe; do not chop 2-second shots
   mechanically. Cut on motion or on narration beats.
6. **Colour**: one palette per act, recorded in `scenes.json`; grade shifts
   only at act boundaries.
7. **Headroom/lead room**: respect both; captions and key text live in the
   80% title-safe box (HyperFrames convention) or equivalent.

## Verification

After rendering, the Cinematographer reviews stills and clips against this
grammar with the Critic (framing, motivation, smoothness, variety, continuity
— `references/cinematography_standards.md`). Defects get IDs and enter the
correction loop.
