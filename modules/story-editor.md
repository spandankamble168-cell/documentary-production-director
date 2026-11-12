# Story-editor

The script's structural editor. Runs on `script/documentary_script.md` before
storyboarding, as a deliberate second pass — same agent, editor's criteria.

## What the Story-editor decides

1. **Order**: does each beat arrive at the moment of maximum curiosity?
   Rearrange before rewriting.
2. **Length**: is every segment earning its duration? Cut or compress any
   segment whose information could arrive in half the time.
3. **Curiosity gaps**: each act should end with the viewer wanting one
   specific answer. If an act ends on a settled statement, open a gap or merge
   it forward.
4. **Repetition**: the same fact stated twice, the same visual idea twice,
   the same emotional beat twice — cut the weaker instance.
5. **Transitions**: mechanical connectors ("next", "another example") are
   replaced by causal or contrastive ones ("but", "meanwhile", "years
   earlier").
6. **Pacing curve**: alternate dense and airy passages; no more than ~90 s of
   continuous dense narration without a visual-only beat.
7. **Opening and ending**: the hook is concrete and the ending answers the
   central question — if not, send back to the Scriptwriter with notes.

## Output

A revision of `documentary_script.md` + `narration.json` plus a short
`script/story_notes.md`: what was changed and why. The word count and timing
estimates are recomputed after edits (see `scriptwriter.md`). Record accepted
notes in `project.json` history so a later session doesn't re-litigate them.
