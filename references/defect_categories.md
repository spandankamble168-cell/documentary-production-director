# Defect Categories

## Severity
| Severity | Meaning | Approval impact |
|---|---|---|
| CRITICAL | breaks the film (corruption, missing content, sync failure, clipping) | blocks approval |
| HIGH | clearly visible/harmful to quality | must fix before approval |
| MEDIUM | noticeable, hurts score | fix in normal rounds |
| LOW | polish | may ship if approved at ≥80 with note |

## Categories and typical evidence
| Category | Typical defects | Typical evidence |
|---|---|---|
| TECHNICAL | wrong resolution/fps, codec issue, container problem, duration mismatch | video_metadata.json |
| VISUAL_QUALITY | artifacts, banding, black frames, missing textures, overexposure | frame filenames |
| CINEMATOGRAPHY | bad framing, unmotivated move, broken screen direction, repetitive shots | frame filenames + timestamps |
| ANIMATION | frozen elements, jitter, end-snap, tween fighting, lost WebGL blank | consecutive frame pairs |
| EDITING | abrupt cuts, dead time, repetition, wrong order | scene map + timestamps |
| NARRATION | missing segment, mismatch vs script, wrong words (Whisper), bad pronunciation | asr_check output + narration.json |
| AUDIO | clipping, loudness off target, level jumps, unintended silence, sync offset | audio_analysis.json numbers |
| SYNC | narration starts off-scene, referenced visual absent | frames at narration timestamps |
| CONTENT | unsupported claim, unattributed quote, unlabeled reconstruction | claims.json vs script |
| LICENCE | unattributed asset, non-commercial asset in use | asset_manifest.json |

## ID and status lifecycle
- `DEFECT-###` — IDs are never reused; numbering continues across rounds.
- Status: `OPEN → CLAIMED_FIXED → (verified on new render) VERIFIED_FIXED |
  NOT_FIXED | WONT_FIX`; a regression gets a **new** DEFECT ID referencing the
  old one in `root_cause`.
- A defect can only be closed by inspecting the new render at its timestamp —
  claimed ≠ fixed.

## Writing a good defect
- Description: what is wrong, where, how visible. One defect per finding.
- Evidence: concrete (file + timestamp + what was seen/measured).
- Required correction: an instruction a director can execute (scene, engine,
  what to change) — not "make it better".
- Expected result: what the fixed frame/audio should show.
- Verification: exactly how the fix will be checked (which timestamps/frames).
