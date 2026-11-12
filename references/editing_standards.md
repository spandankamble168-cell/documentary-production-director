# Editing Standards

## Cut logic
- Cut when the information changes, not on a metronome. Shot length serves
  content: data cards and establishing shots breathe; pickups are short.
- No two consecutive shots with identical framing; no more than ~90 s without
  a shot change.
- Transitions: hard cut default. Cross-fade for time/place jumps. Wipes/whips
  only when the style calls for it. A transition is punctuation, not decoration.

## Rhythm
- Open on the hook (no title card before the first image unless branded).
- Ends within ~2 s of the last narration word; no trailing black + silence.
- Act boundaries: palette/music/pace shift together.

## Dead time and repetition (defect watchlist)
- silence ≥ 2 s not intended (check `audio_analysis.json` silence segments);
- frozen picture ≥ 2 s not intended (check consecutive frames);
- the same shot/animation used twice as filler;
- narration repeating the script's earlier statement.

## Sync
- Narration segment N starts within ±0.3 s of its scene's planned start.
- Picture referenced by narration ("as you can see…") must be visible at that
  moment — verify by reading frames at the narration timestamp.
- Music changes land on cuts or narration starts, not mid-word.

## Assembly discipline
- All scenes normalized (resolution/fps/pixel format) before concat.
- Round folders immutable: fixes go to a new round, never overwrite.
- Final duration within ±0.5 s of plan (ffprobe-verified, never assumed).
