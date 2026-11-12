# Documentary Standards

Baseline quality bar for every film this skill produces.

## Structure
- Runtime honored within ±5% of target; the ending is not padded to reach it.
- Acts: hook → development (escalating questions) → climax/reveal → payoff.
  The central question is answerable after watching.
- Every fact presented is backed by `research/claims.json`; hedged claims are
  hedged deliberately, not habitually.

## Content rules
- Show before tell: prefer a scene that demonstrates over narration that
  describes.
- No stock-phrase narration, no information dumps, no filler segments.
- Attribution on screen (lower third, caption, source card) for quotations,
  statistics and archive-like material.
- Reconstruction is labeled as reconstruction.
- Sensitive topics (violence, tragedy, real named people): no gratuitous
  imagery; allegations are attributed and unproven-flagged.

## Technical delivery defaults
| Item | Default |
|---|---|
| Resolution | 1920×1080 (16:9) |
| Frame rate | 24 fps (30 for HyperFrames data segments if mixed, normalized at assembly) |
| Audio master | −14 LUFS integrated, true peak ≤ −1 dBTP (via mux.sh) |
| Narration | intelligible over music; music ducks ≥ 6 dB under voice |
| Subtitles | when narration quality can't be guaranteed, or on user request |
| File | H.264 yuv420p + AAC, playable everywhere |

## Deliverables (delivery/)
- final MP4, subtitles (.srt if made), score summary, list of remaining known
  LOW defects, asset/licence credits file.
