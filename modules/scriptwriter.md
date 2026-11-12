# Scriptwriter

Produces `script/documentary_script.md` and `script/narration.json` (schema:
`schemas/script.schema.json`), from the template
`templates/documentary_script.md`, using verified research only.

## Shape of a documentary script

- **Central question** stated or implied early; the film is its investigation.
- **Opening hook** in the first 15 seconds: a concrete image, claim or
  contradiction — never "In this documentary we will explore…".
- **Progression**: each act answers part of the question and opens the next
  one; information arrives in escalating order of interest.
- **Conflict / tension**: human stakes, contradictions, reversals — explicit.
- **Payoff and ending**: answer the central question, land the emotional
  note, end on one strong beat. No "thanks for watching".

## Narration prose

Write for the ear: short declarative sentences, concrete nouns, active voice,
one idea per sentence. Read every line aloud before it enters the script.

Avoid:
- generic AI-narration phrasing ("delve", "tapestry", "it is important to
  note", "in today's fast-paced world");
- information dumps (three numbers per sentence maximum);
- repeating what the picture already shows;
- hedging every sentence — hedge only what `fact_check.md` requires;
- unsupported claims (check against `research/claims.json`).

## Segment contract

Every narration segment maps to exactly one scene and carries: scene ID,
planned start/end time, narration text, word count, estimated speaking
duration = words ÷ speaking rate (default 150 wpm for English; configurable
per project in `production_plan.md`; Chinese ≈ 4.5 characters/second), visual
purpose, emotional intention, sound-design note, transition out.

Timing: estimate from real word counts; leave breathing room (music and
picture beats need silence). Do not cram narration into a duration that can't
hold it — extend the scene or cut words. Narration text is what `tts.py`
receives as `text`; keep `narration.json` in exactly that shape
(`[{id, text, voice?, speed?, lang?}]` plus production metadata allowed as
extra keys).
