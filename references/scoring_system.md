# Scoring System

100 points. Evidence-based or NOT EVALUATED (null). Never invented, never
inflated.

## Weights
| Category | Max | Primary evidence |
|---|---:|---|
| Visual quality | 20 | frames read as images (artifacts, clutter, grading, text) |
| Cinematography | 15 | frames (framing, variety, motivation, continuity) |
| Animation | 15 | consecutive frames (easing, weight, glitches, freezes) |
| Editing & pacing | 15 | scene map + frames + narration timing |
| Narration | 10 | Whisper verification results + measured levels |
| Sound design & audio | 10 | audio_analysis.json + mix plan conformance |
| Story-to-visual sync | 10 | narration timestamps vs frames at those times |
| Technical quality | 5 | video_metadata.json + audio_analysis.json |

## Bands
| Score | Band | Action |
|---|---|---|
| 95–100 | Exceptional | approve |
| 90–94 | Excellent | approve (note LOW defects) |
| 85–89 | Very good | approve or one small round |
| 80–84 | Good | approve with noted defects, or one round |
| 70–79 | Needs improvement | corrections required |
| 60–69 | Poor | corrections required |
| < 60 | Major revision | corrections required |

## Scoring rules
1. Every non-null score cites at least one piece of evidence (frame filename,
   timestamp, measurement) in `critic_report.json` → `evidence[]`.
2. A category that could not be inspected → `null` with the reason recorded;
   it contributes 0 to total and the total is reported as "X / (100 −
   uninspected points)".
3. A category with mixed evidence scores to its weakest substantiated level —
   not the average of hope.
4. **Critical defects cap the total at 69** regardless of category scores
   (corrupt video, missing sections, missing required narration, wrong aspect
   ratio, major clipping, missing scenes, black sections, severe sync failure).
5. Regression on a previously fixed defect: score the new round no higher than
   the round that introduced the defect.
6. Scores may not rise between rounds without new evidence — the same frames
   and measurements cannot yield a better number twice.

## Approval gates
- No unresolved CRITICAL defects.
- All categories scored or null-with-reason.
- Spec conformance (duration ±0.5 s, resolution, fps).
- Audio pass: no clipping, narration intelligibility verified, sync in tolerance.
- Total ≥ 80, or explicit user acceptance of a lower score.
