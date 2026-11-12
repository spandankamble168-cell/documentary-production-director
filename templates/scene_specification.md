# Scene Specification — {SCENE-ID} ({TITLE})

*Full production spec for one scene. Machine form lives in
`storyboard/scenes.json`; the render bookkeeping in
`production/engine_manifest.json`.*

## Identity
- Scene: {SCENE-ID} · Duration: {n}s · Engine: {hyperframes | lemo-opuscar}
- Narration: {NARR-IDs} · Status: {PLANNED / IN_PROGRESS / RENDERED / VERIFIED}

## Environment & characters
- Environment: {place, era, time of day, weather}
- Characters: {design / wardrobe / position / screen direction / consistency}
- Foreground: {…} · Background: {…} · Atmosphere: {dust, haze, particles…}

## Camera
- Position: {…} · Angle: {eye / low / high / dutch-with-cause}
- Movement: {static / push-in / pull-out / track / dolly / orbit / crane / parallax}
- Motivation: {why the story moves the camera}
- Start framing → end framing: {…}
- Focal length / FOV: {…} · Composition: {thirds / centered / leading lines…}

## Light & colour
- Lighting: {key, fill, direction, quality}
- Palette: {act palette; any scene-local accents}

## Animation content
- {What moves, how, easing, duration of each move; end state lands before clip end}

## Audio
- SFX: {aligned to visible actions} · Music: {cue, intensity, ducking}
- Transition in/out: {…}

## Render
- Source location: {path in project}
- Render command: {the verified command for this engine}
- Output: {output path} · Resolution: {WxH} · FPS: {n}

## Expected result
{One sentence: what the finished shot shows and feels like.}
