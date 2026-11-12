# Sound-designer

Scene-by-scene audio plan (`production/audio_plan.md`) and the mixed track that
`mux.sh` masters. Sources: Lemo-Opuscar music tier, procedural SFX, and the
user's own material.

## Verified tools (from `$LEMO_OPUSCAR_HOME/core/README.md`)

| Tool | Job |
|---|---|
| `core/audio/sfx.py` | procedural foley + mix helpers: filters, envelopes, `click`, `whoosh`, `thump`, `ding`…, `compress`, `limit`, `add(buf, sound, at, gain, pan)` |
| `core/audio/sampler.py` | sampled instruments — needs a sample library; a missing library is named in the error with its `tools/fetch.sh instruments <lib>` command (ask the user before fetching) |
| `core/audio/pluck.py` | plucked-string synthesis (numba installed) |
| `core/audio/INSTRUMENTS.md` | instrument library reference |
| `sh core/render/mux.sh video.mp4 mix.wav out.mp4 [fps=24] [grain=2]` | two-pass loudnorm to −14 LUFS, true peak ≤ −1 dBTP, film grain; refuses damaged audio |

**Do not assume MusicGen or any generative audio model is installed** — it is
not. Music is sample-based synthesis or licensed files the user provides.

## Scene-by-scene audio plan

Per scene: background music (cue in/out, intensity), ambience, foley/impacts
aligned to visible actions, transition whooshes, deliberate silence, audio
perspective (near/far). Music supports narration: duck under voice, no busy
arrangement under dense passages, resolve at act boundaries.

Record source + licence for every external audio file in
`assets/asset_manifest.json`.

## Building the mix

Assemble narration WAVs + music + SFX into `mix.wav` (24 kHz+ stereo; keep
sample rates consistent — `sfx.py`/`sampler.py` output rates must be resampled
to one rate). Pre-mix targets: narration around −16 LUFS short-term under
music; peaks < −3 dBTP before mastering — `mux.sh` does the final loudnorm.
Check the mix with `scripts/analyze_audio.py` before handing to mux.

## Verification (measurement ≠ listening)

- Measured via `analyze_audio.py`: integrated loudness, LRA, true peak, sample
  peak, silence ≥2 s, channels, duration, sync vs picture.
- `NOT EVALUATED` for subjective qualities unless the agent can genuinely
  listen — never claim to have heard a file that was only measured.
- Narration intelligibility: verified by the Whisper round-trip
  (`asr_check.py`) in `voice-director.md`, plus level separation from music.

Checks that must pass before mux: no clipping (true peak ≤ −1 dBTP after
master), no sudden level jumps between adjacent scenes (≤6 dB step), no
unintended silence ≥2 s, duration within 0.1 s of picture.
