# Production-manager

Owns `project.json`, the project layout, render rounds, and assembly. Makes
work resumable.

## Project state (`project.json`)

```json
{
  "name": "my-documentary",
  "created": "2026-11-12T10:00:00",
  "updated": "2026-11-12T12:30:00",
  "target": { "duration_sec": 600, "resolution": "1920x1080", "fps": 24, "language": "en" },
  "stage": "production",
  "stages_completed": ["brief", "research", "script", "storyboard"],
  "stages_pending": ["audio", "production", "assembly", "qc", "delivery"],
  "current_render": "renders/round-01/final.mp4",
  "render_round": 1,
  "correction_round": 0,
  "score": null,
  "open_defects": [],
  "approval_status": "PENDING",
  "history": [ { "ts": "...", "event": "stage completed: research" } ]
}
```

Rules: update after every meaningful event; append to `history`; never delete
entries. `scripts/project_status.py <project>` prints the state;
`scripts/validate_project.py` validates layout and JSON integrity.

## Render rounds

- `renders/round-01/` … one folder per full assembly; `renders/final/` only for
  the approved cut. Never overwrite a previous round.
- `render_round` increments when assembly runs; `correction_round` increments
  when the Critic issues a correction package. Max **five** correction rounds —
  after that, report unresolved defects and whether manual intervention is
  required.

## Assembly (FFmpeg)

1. Collect rendered scene clips in scene order (engine manifest paths).
2. Normalize: all scenes to target resolution/fps/pixel format before concat
   (`ffmpeg -vf scale=1920:1080,fps=24 -pix_fmt yuv420p`).
3. Concat with transitions as planned (`xfade` for cross-fades; hard cuts
   otherwise). Cross-fades are transitions, not decoration.
4. Audio: narration/music/SFX pre-mix (Sound-designer) →
   `sh $LIB/core/render/mux.sh video.mp4 mix.wav out.mp4 [fps=24] [grain=2]`
   from the Lemo library (masters to −14 LUFS, true peak ≤ −1 dBTP).
5. Verify with `scripts/inspect_video.py`: duration vs plan ±0.5 s, resolution,
   fps, streams present. **"Assembled" ≠ "approved"** — the Critic decides.

## Disk and memory discipline

Long renders: chunked, one scene at a time. Never load a whole video into
memory. Clean intermediate stills only after their scene is VERIFIED. Keep
rounds on disk until approval (they are the comparison baseline).
