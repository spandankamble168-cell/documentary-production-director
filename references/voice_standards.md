# Voice Standards

## Engine choice
| Need | Engine | Notes |
|---|---|---|
| English narration | **Kokoro** (`core/tts/tts.py`) | offline, 24 kHz, free |
| Chinese narration | **edge-tts** (`core/tts/tts_zh.py`) | free Microsoft service — **online**, say so; Kokoro `cmn` voices work offline but sound plain |
| Verification | **Whisper** (`core/tts/asr_check.py`) | local CPU; `base` model default |

Never introduce paid voice services. Never describe edge-tts as offline.

## Casting
- Kokoro voice codes: `af_*`/`am_*` American, `bf_*`/`bm_*` British; unknown
  code → `tts.py` prints the full list (use it; never invent codes).
- Cast for the film's tone (documentary gravitas vs friendly explainer);
  consistency: one narrator voice per film, secondary voices only for quotes
  in other languages.
- Default speed `0.92`; raise to ~1.0 only for dense informational passages;
  never above 1.1.

## Delivery
- One segment = one scene's narration block (10–35 s audio typically).
- Pauses are mix decisions (silence between segments), not stretched words.
- Emphasis by rewriting the sentence, not by shouting the TTS.

## Pronunciation guide (`script/pronunciation_guide.md`)
- List before generation: proper names, historical places, foreign terms,
  technical jargon, acronyms.
- Fix by respelling in TTS `text` (Kokoro uses espeak-ng phonemization —
  respell, verify, repeat); use the `asr` field in `asr_check.py` for names
  Whisper legitimately hears differently.
- Whisper round-trip verifies **word identity**; it does not certify accent or
  pleasantness. Don't overclaim.

## Pipeline order
1. narration.json (segments bound to scenes)
2. generate WAVs (`tts.py` / `tts_zh.py`) → `dur.json` gives measured durations
3. `asr_check.py` verification — every line must pass
4. re-time scenes against measured durations; re-render any scene whose
   narration length changed materially
5. statuses in narration.json: PENDING → GENERATED → VERIFIED → TIMED
