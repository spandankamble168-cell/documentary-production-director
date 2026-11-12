# Quality-controller

Runs the QC loop between render rounds and owns the approval decision.
Counterpart of the Critic: the Critic finds and scores; the Quality-controller
tracks, dispatches corrections, verifies fixes, and approves or refuses.

## The loop

```
RENDER → CRITIC → correction_package.json → CORRECT → RERENDER → CRITIC → ...
```

- Maximum **five** correction rounds. Track in `project.json`
  (`correction_round`, `renders/round-XX/`).
- Each round must: inspect the new MP4 fully (Critic pipeline), compare against
  the previous render (`compare_renders.py`), verify each previously reported
  defect at its timestamp, identify regressions, update scores, and issue a new
  correction package if needed.
- `quality-control/correction_history.json`: one entry per round — defects
  claimed fixed, verified fixed, not fixed, newly introduced.
- **Never mark a defect fixed without inspecting the new render at its
  timestamp.** Claim ≠ fix.

## Correction dispatch

Map each defect to its scene and engine (from `engine_manifest.json`):
- HyperFrames scene → edit the composition, `check --json`, `snapshot`, re-render scene.
- Lemo-Opuscar scene → edit the scene page, stills pass, re-render scene.
- Assembly issue (sync, transition, missing scene) → Production-manager re-assembles.
Only affected scenes re-render; then full re-assembly into a new round folder.

## Verdict bands (from `references/scoring_system.md`)

95–100 Exceptional · 90–94 Excellent · 85–89 Very good · 80–84 Good ·
70–79 Needs improvement · 60–69 Poor · <60 Major revision.

## Approval

Final approval requires **all** of:
1. No unresolved `CRITICAL` defects (verified on the current render).
2. All categories scored or explicitly `NOT EVALUATED` with reason.
3. `video_metadata.json` matches target spec (duration ±0.5 s, resolution, fps).
4. Audio pass: no clipping, narration intelligibility verified, sync within
   tolerance.
5. Score ≥ 80, or the user explicitly accepts a lower score.

On approval: copy to `renders/final/`, set `approval_status: APPROVED`, write
the delivery note (file path, specs, score, remaining known LOW defects). A
refusal is written as a new correction package — not as a shrug.

After five rounds: report unresolved defects, their severity, and what manual
intervention would be needed. Do not loop forever.
