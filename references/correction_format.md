# Correction Format

## The package
One `quality-control/correction_package.json` per QC round (schema:
`schemas/correction_package.schema.json`). Example entry:

```json
{
  "defect_id": "DEFECT-001",
  "timestamp": "00:00:18.400",
  "scene_id": "SCENE-006",
  "severity": "HIGH",
  "category": "CINEMATOGRAPHY",
  "description": "Camera push-in is excessively fast.",
  "evidence": "frame_00-00-18.400.jpg vs frame_00-00-19.400.jpg: framing jumps ~15% in 1 s",
  "root_cause": "linear lerp over 2 s scene; should ease over full duration",
  "required_correction": "Ease the push-in (eio) across the full 6 s scene and halve its range.",
  "expected_result": "Smooth push-in; framing change between consecutive stills barely perceptible.",
  "affected_engine": "lemo-opuscar",
  "verification": "Re-extract frames at 18.0–23.0 s in the new render and read them."
}
```

## Executability rules
- `required_correction` names the scene, the engine and the concrete change.
- `reprocess_scope` lists exactly which scenes/steps re-render — nothing more.
- Affected-engine dispatch:
  - `hyperframes` → edit composition → `check --json` → `snapshot` → re-render scene clip
  - `lemo-opuscar` → edit scene page → stills pass → re-render scene clip
  - `ffmpeg-assembly` → re-assemble (transitions, concat, mux)
- Never re-render unaffected scenes "while we're at it" — it invalidates the
  comparison baseline.

## The round
1. New folder `renders/round-XX/` (previous rounds untouched).
2. Re-render only `reprocess_scope`.
3. Re-assemble → full QC pass on the new MP4 (Critic pipeline, not a spot check).
4. `regressions_checked[]`: every defect from all prior rounds, verified at its
   timestamp on the new render — `VERIFIED_FIXED | NOT_FIXED | REGRESSION | WONT_FIX`.
5. New/remaining defects get fresh DEFECT IDs; update `correction_history.json`.
6. Update `project.json` (`correction_round`, `open_defects`, `score`).

## Limits
- Max 5 rounds. On round 5: verdict `MANUAL_INTERVENTION`, list unresolved
  defects with severity and the manual step needed. Never approve with
  unresolved CRITICAL defects, no matter the round count.

## History file (`correction_history.json`)
```json
[{ "round": 1,
   "claimed_fixed": ["DEFECT-001"],
   "verified_fixed": ["DEFECT-001"],
   "not_fixed": [],
   "regressions": ["DEFECT-004 (new; introduced fixing DEFECT-002)"],
   "score_before": 74, "score_after": 86 }]
```
