# Audio Standards

## Loudness targets (measured, not guessed)
| Item | Target | Tool |
|---|---|---|
| Final master integrated loudness | −14 LUFS | `core/render/mux.sh` (two-pass loudnorm) |
| Final true peak | ≤ −1 dBTP | `mux.sh` limiter, re-encode loop |
| Narration pre-mix level | ≈ −16 LUFS short-term under music | sfx.py `compress`/`limit` |
| Music under narration | ducked ≥ 6 dB vs solo level | mix automation |
| LRA (final) | ≤ 12 LU | measurement |

## Rules
- One sample rate through the whole mix chain (resample everything to the
  narration project rate — Kokoro outputs 24 kHz; upsample for the mix, master
  at 48 kHz).
- No sudden level steps > 6 dB between adjacent scenes (fade 50–150 ms).
- No unintended silence ≥ 2 s (`silencedetect` check).
- No clipping at any stage: pre-mix peaks < −3 dBTP; master verifies ≤ −1 dBTP.
- Mono narration voices summed to stereo with identical L/R (no phase risk).
- Music supports narration: no busy arrangements, no vocal-like leads under
  voice, resolve at act boundaries.

## Provenance
- Every external audio file recorded in `asset_manifest.json` with licence.
  CC0/public-domain preferred; "free download" ≠ "commercial use allowed".
- Sample libraries from Lemo `tools/fetch.sh instruments <lib>`: record the
  library name and its licence; fetch only after asking the user.
- `sfx.py` / `sampler.py` / `pluck.py` outputs are original (generated) —
  record the tool, not a licence.

## Measurement vs listening (never conflate)
- `analyze_audio.py` = numbers (LUFS, peaks, silence, channels). Real and
  citable.
- Subjective judgement (does the score feel right?) = `NOT EVALUATED` unless
  genuine listening capability exists.
- Narration intelligibility is verified objectively via the Whisper round-trip
  (`asr_check.py`), plus the measured voice-vs-music level separation.
