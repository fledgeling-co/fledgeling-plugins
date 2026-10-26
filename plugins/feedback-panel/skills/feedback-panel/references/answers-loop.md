# The answers loop

The author's export comes back as JSON. Each answer is a decision; the work is applying it
faithfully and showing what it changed.

## 1. Diff the answers against what was built

For each answer, record one of four outcomes in `answers-diff.md`:

- **Matches the build**: `is_default` is true and nothing was built differently. No change.
- **Differs**: the chosen option is not what was built. List what has to change, by file.
- **Note adds a condition**: a non-empty note narrows or extends the answer ("use a made up
  company, but split examples across ASX and Nasdaq"). Treat the note as part of the answer.
- **Unbuildable as answered**: the answer needs something missing (assets, a credential, a
  capability). Say what, and who supplies it.

New requests that arrive with the answers (a new page, a new section) join the same list.

## 2. Ask two families how, not whether

Send the differing answers, their notes and any new request to two lanes with the "Applying
answers" brief in `panel-briefs.md`. Where they agree, build it. Where they split, take the
option that keeps the project's standards (a sourced claim, an accessibility floor, a recorded
rule the author has not overridden) and record the split as a follow-up question. Where an
answer overrides a written project rule, the answer wins: update the rule and record the date
and the author in the decisions log, so the next session does not undo it.

Check names, tickers, firms and quoted facts that the answers introduce against the web before
publishing them; a made-up company name that collides with a real one is worse than the
placeholder it replaced.

## 3. Build and record

Build through the project's own gates. Update, in the same change: the decisions log (one
dated entry listing each answer and what it changed), the project's design and copy rules
where an answer changed them, and the positioning or research file an answer names.

## 4. Rebuild the report

If the build raised new questions, rebuild the report in questions mode with only those
questions, a new `storage_key`, the push-back from this round, and "What we changed from your
answers" as the understood section. When those come back answered, switch to answers mode
(see `report-contract.md`) rather than writing a third questionnaire.
