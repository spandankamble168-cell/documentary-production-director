# Critic Report — Round {N}

*Inspect the actual MP4. Evidence types: `observed` (frames read as images,
cited by filename) and `measured` (FFmpeg/FFprobe numbers, cited by file).
Nothing else scores.*

## Render under review
- File: {path} · Round: {n} · Inspected: {date}
- Spec target: {1920×1080 / 24 fps / target duration}

## Inspection performed
- [x] Metadata (`video_metadata.json`) — {one-line summary}
- [x] Scene detection (`scenes.json`) — {n cuts found}
- [x] Frames extracted: {n} (every {k}s + {list of suspicious timestamps})
- [x] Contact sheet: `contact_sheet.jpg`
- [x] Visual inspection: {PERFORMED — agent read frames | NOT AVAILABLE}
- [x] Audio analysis (`audio_analysis.json`) — {LUFS / TP / silence summary}
- [ ] Audio listening: NOT EVALUATED {unless genuinely performed}

## Scores
| Category | Score | Evidence (cited) |
|---|---|---|
| Visual quality (20) | {n or NOT EVALUATED} | {frame files / reason} |
| Cinematography (15) | {n} | {…} |
| Animation (15) | {n} | {…} |
| Editing & pacing (15) | {n} | {…} |
| Narration (10) | {n} | {asr_check + levels} |
| Sound design & audio (10) | {n} | {measurements} |
| Story-to-visual sync (10) | {n} | {frames at narration timestamps} |
| Technical quality (5) | {n} | {metadata} |
| **TOTAL (100)** | **{n}** | band: {Exceptional…Major revision} |

Critical-defect cap applied: {yes/no — why}

## Defects
| ID | Timestamp | Scene | Sev | Category | Description | Required correction |
|---|---|---|---|---|---|---|
| DEFECT-001 | 00:00:18.4 | SCENE-006 | HIGH | CINEMATOGRAPHY | push-in too fast | ease over full scene |

## Comparison with previous round
{SSIM/PSNR + what changed; regressions found or none.}

## Verdict
{APPROVED | CORRECTIONS_REQUIRED (round {n+1} package issued) |
 MANUAL_INTERVENTION (round limit / unresolved critical)}
