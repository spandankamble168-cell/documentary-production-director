# Director

The Director is the running agent in MODE A. It owns the whole production and
delegates stage work to the modules below. It never does two stages at once and
never silently skips one.

## Stage sequence and gates

| # | Stage | Owner | Gate to pass |
|---|---|---|---|
| 0 | Brief + project scaffold | Director | `project.json` exists; one round of questions answered (or sensible defaults recorded in `production_plan.md`) |
| 1 | Research | Researcher → Fact-checker | `research/claims.json` — every load-bearing claim has a verification status |
| 2 | Script | Scriptwriter → Story-editor | `script/documentary_script.md` + `narration.json`; timing estimates from real word counts |
| 3 | Storyboard | Storyboard-artist → Cinematographer | `storyboard/scenes.json` validates against `scene_spec.schema.json` |
| 4 | Assets + engine allocation | Visual-director | `assets/asset_manifest.json` + `production/engine_manifest.json` complete |
| 5 | Audio | Voice-director → Sound-designer | narration WAVs verified by Whisper check; music/SFX plan on disk |
| 6 | Scene rendering | Animation-director | every scene rendered; stills checked by eye before a scene counts as done |
| 7 | Assembly | Production-manager | `renders/round-XX/` MP4 built with mux |
| 8 | QC | Critic → Quality-controller | approval or a new correction round |

## The brief (one round of questions)

Ask once, in a single message, only what the user can decide:
- topic, target duration, aspect ratio (default 1920×1080), language;
- must-include facts, names, products, places;
- the user's own material (recordings, photos, data, logos, fonts);
- storyboard review wanted? (default: no).

Everything else: fill with sensible defaults, sum up the brief in the
`production_brief.md` template, and start. Do not return with more questions.

## Treatment

Before any scene work, write `production_plan.md` from
`templates/production_brief.md`: premise, central question, angle, conflict,
structure (3 candidate structures, one chosen with reasons), tone, visual
approach, per-act scene list. Keep the user's topic first — never bend it
toward a demo or a template.

## Interruption and resumption

Update `project.json` after every stage transition (see
`modules/production-manager.md`). If a session dies, the next session reads
`project.json` via `scripts/project_status.py` and resumes at the current
stage — research already verified is not re-verified, rendered scenes are not
re-rendered.

## Handoff to the Critic

When assembly produces a render, update `project.json` (`current_render`,
`render_round`), then act as the Critic: inspect the actual MP4 per
`modules/critic.md`. "Render finished" is a build event, never a quality
judgement.
