# The join, and why it is the weak step

Everything else in this skill is mechanical. Reading statuses, applying the
legality table, counting denominators, clustering blockers — all deterministic,
all re-runnable, all checkable by the gate.

Tying a brief to a registry entity is not. Briefs are markdown files named by
a human; requirements and cases carry generated ids. Nothing binds them but
words. **A reconciliation gate sitting on top of a bad join is theatre**: the
partition will be perfectly total and perfectly wrong, and it will pass.

So the join publishes how it was made, and the gate treats its two mechanisms
very differently.

## The two mechanisms

**Cited edges — confidence 1.0.** Somebody wrote the link down. Three forms:

- a brief's body naming a registry id (`REQ-0004`, `DEF-0015`)
- a registry note naming the brief's project id (`DEF-0015` recording
  "DEF-0015 / SCR-0075")
- `reckon-sources` frontmatter on a brief this skill generated earlier

These are evidence. A retirement may rest on one.

**Overlap edges — confidence is the score.** Jaccard similarity over content
words between the brief's title and opening, and the registry entity's text,
above a threshold (default 0.18). The best-scoring target wins, and only if a
brief has no cited edge at all.

These are guesses. Useful for orientation, and the gate refuses to retire a
brief on one — `selftest.py` demonstrates that refusal firing.

## What to check by hand

Three things, in this order. All of them are quick, and the first two change
conclusions rather than polish them.

**Unjoined briefs.** These land in `unbuilt`, and that class is really
"registry-silent". A brief joined to nothing is either genuinely unbuilt or a
join the script missed, and those are opposite conclusions about the same
item. Skim the titles: a brief about a surface the campaign clearly covered is
a missed join, not unbuilt work.

**Overlap edges above the threshold but below about 0.35.** This is where
false positives live — two documents sharing vocabulary without sharing a
subject. Cut the ones that are wrong; a wrong edge can move a brief into
`broken` or `undecided` on somebody else's evidence.

**Anything the ledger marks `retirable`.** Retiring deletes stated intent, so
this is the one class where being wrong costs something you cannot get back.
The gate has already refused every retirement on a guessed join; read the
survivors anyway.

## When the join is weak overall

Below 50% of briefs joined to anything, `reckon.py` sets `join.weak` and
withholds retirement across the board — every brief that would have been
`retirable` becomes `undecided` instead, with the reason recorded.

This is a claim degrading, not a run failing. The gate stays at exit 0 and
prints a warning with the percentage. A gate that refuses to produce output
gets switched off, and a switched-off gate catches nothing; a gate that says
"here is your answer, and here is the part of it I will not stand behind" gets
used.

## Making the join stronger in a repo

The join is only as good as the citations people write, and two cheap habits
raise it permanently:

**Cite the brief id in campaign notes.** A defect recording "DEF-0015 /
SCR-0075" costs nothing to write and produces a confidence-1.0 edge forever.
The scrim campaign does this and it is why 55% of its briefs join at all.

**Keep the project id in the brief filename.** `SCR-0075-dead-credential-...`
gives the reverse-citation scan a token to look for. A brief called
`fix-the-thing.md` can only ever be matched by guesswork.

Where a repo does neither, expect a weak join and expect the report to say so.
That is the report working, not failing — an unjoinable queue genuinely cannot
support conclusions about which of its briefs are finished.

## Tuning

`--join-threshold` (default 0.18) sets where an overlap edge is proposed at
all. Lower it to propose more and review more; raise it to propose only
confident matches and leave more briefs unjoined.

Prefer raising it. An unjoined brief is visibly unresolved and gets read; a
wrong edge is invisible and gets believed.
