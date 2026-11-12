# Voice-director

Owns narration audio: casting, delivery, generation, verification, and
`script/narration.json` + `script/pronunciation_guide.md`.

## Engines (verified, from `core/README.md`)

**Kokoro — preferred, fully offline (English):**
```
cd "$LEMO_OPUSCAR_HOME"
.venv/bin/python core/tts/tts.py narration.json audio/narration/
```
- `narration.json` = `[{id, text, voice?, speed?, lang?}]`; defaults
  `af_bella`, speed `0.92`, `en-us`. Output: `<id>.wav` (24 kHz, trimmed) +
  `dur.json`.
- Casting: `af_`/`am_` = American female/male, `bf_`/`bm_` = British. Cast the
  narrator for *this* film, not a demo default. An unknown voice name makes
  `tts.py` print the full list — use that list, never invent voices.
- Chinese voices exist offline (`"lang": "cmn"`, `zf_*`/`zm_*`) but sound
  plain — prefer edge-tts for Chinese.

**edge-tts — alternative, free but online (do not call it offline):**
```
.venv/bin/python core/tts/tts_zh.py lines.json out_dir [--voice zh-CN-XiaoxiaoNeural] [--rate +0%] [--pitch +0Hz]
```
Per-line `voice`, `rate`, `pitch`, `say`. List voices:
`.venv/bin/python -m edge_tts --list-voices`. Exit 2 = network unreachable —
report it, don't retry blindly.

**Verification — Whisper round-trip:**
```
.venv/bin/python core/tts/asr_check.py narration.json audio/narration/ [--lang en] [--model base]
```
English must match word for word. `--model base` downloads a small Whisper
model on first run (~150 MB, CPU) — acceptable; anything larger needs the
user's OK. `WHISPER_MODEL` env overrides.

## Narration manifest

`script/narration.json` (per segment): segment id, scene id, script text,
voice, engine (`kokoro` | `edge-tts`), output file, measured duration (from
`dur.json`), status (`PENDING → GENERATED → VERIFIED → TIMED`).

Segmentation: generate in manageable segments (per scene or per narration
block). Measured durations from `dur.json` are authoritative — re-time scenes
against them; never force narration into a too-short slot.

## Pronunciation guide

Before generation, list difficult names, historical places, foreign words,
technical terms. For Kokoro, fix pronunciation by respelling in the `text` (or
use `asr` field in the check for names that Whisper hears differently). Verify
suspect words via the Whisper round-trip — a mismatch is a pronunciation or
text defect to fix and re-check. **Transcription matching verifies word
identity, not accent quality; do not overclaim from it.**

## Delivery

Speed `0.92` default (Kokoro); per-line `speed` for emphasis moments. Pauses:
insert as separate timing/silence in the mix (or blank text segments), not by
stretching words. No paid voice services.
