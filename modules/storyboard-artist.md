# Storyboard-artist

Converts the approved script into production-ready scenes:
`storyboard/storyboard.md` (human-readable) and `storyboard/scenes.json`
(machine, validates against `schemas/storyboard.schema.json` and
`schemas/scene_spec.schema.json`), from `templates/storyboard.md` /
`templates/scene_specification.md`.

## Every scene carries

- `id` (`SCENE-001`…), duration, narration segment ID(s);
- environment (place, time of day, weather, era);
- characters: description, wardrobe-consistent rendering notes, positioning,
  screen direction;
- camera: position, angle, movement (with start and end framing), focal
  length/FOV, composition;
- lighting and colour palette;
- animation content and timing;
- foreground / background elements, atmosphere;
- sound effects, music cue, transition;
- `engine` (hyperframes | lemo-opuscar | ffmpeg-assembly) with the reason;
- `expected_result`: one sentence on what the finished shot shows.

Full vocabulary of camera work, shot types and continuity rules:
`cinematographer.md` and `references/cinematography_standards.md`.

## Rules

- Camera movement is motivated by story or information — never decorative.
  A static shot is a legitimate choice.
- Shot variety: no three consecutive scenes with the same camera angle and
  distance.
- Continuity is planned here, not discovered in render: characters,
  environments, props, lighting, palette and screen direction stay consistent
  within a sequence (see `references/cinematography_standards.md` §Continuity).
- Text that must be read by the viewer gets enough on-screen time
  (`readcheck` will enforce it for Lemo-Opuscar scenes — plan for it now).
- Total scene durations sum to the target runtime ±5%.

If the user asked to review a storyboard, stop and wait for approval here.
Otherwise proceed.
