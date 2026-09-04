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

**Unjoined briefs.** These land in `unjoined`, which is its own class and its
own outcome. A brief joined to nothing is either genuinely unbuilt or a join
the script missed, and those are opposite conclusions about the same item, so
the script rules on neither: `unjoined` is decision work, and the row carries
the three nearest candidates the join scored and rejected. Skim the titles: a
brief about a surface the campaign clearly covered is a missed join, and the
near-miss list usually names it.

They used to land in `unbuilt`, and that was the same mistake this skill exists
to catch. On one real registry 75 of 91 briefs went that way on a 17.6% join,
every one of them naming an item that had shipped, and the report opened by
claiming 183 pieces of product work. An entity absent from the evidence is not
an entity that failed.

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

**Which briefs that 50% is taken over matters, and until 1.9.4 it was taken
over the wrong ones.** `classify` settles a brief whose declared status is
waived, deferred, retired, consumed, scaffolded or historical from that status,
*before* it reads the join at all. Such a brief was never a candidate the join
was asked about, so counting it in the ratio rates the inferential step on rows
it never touched — and the more history a project archives, the harder it
becomes for that project to retire anything. Measured on perch, 2026-09-02: a
published 98/224 = 43.8% withheld every retirement claim, over a join that had
reached 56 of 56 of the briefs whose class it actually decides. Four briefs the
project's own orchestrator recorded as merged sat `undecided`.

So the ledger carries two figures and gates on the second:

| field | population | what it says |
| --- | --- | --- |
| `denominators.briefs_joined` | every brief | how much of the queue the registry can see at all |
| `denominators.briefs_joined_adjudicated` | briefs whose declared status does not settle them | whether the inferential step is working — **this is what `join.weak` reads** |

Both are published, per the rule that there is a denominator per axis and never
one blended percent: dropping the first would hide how much of a queue is
archive, and gating on it is the defect. The warning names which population it
speaks for, and quotes the other one beside it when they differ.

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

The scan requires that shape — letters, then digits. A queue named `03-menu-bar-
key-equivalents.md` used to produce the token `03-menu`, which is a position in
a directory listing matched against free prose and then labelled a citation at
confidence 1.0. A guess that can carry a retirement is worse than no edge.

Where a repo does neither, expect a weak join and expect the report to say so.
That is the report working, not failing — an unjoinable queue genuinely cannot
support conclusions about which of its briefs are finished.

## Tuning

`--join-threshold` (default 0.18) sets where an overlap edge is proposed at
all. Lower it to propose more and review more; raise it to propose only
confident matches and leave more briefs unjoined.

Prefer raising it. An unjoined brief is visibly unresolved and gets read; a
wrong edge is invisible and gets believed.
