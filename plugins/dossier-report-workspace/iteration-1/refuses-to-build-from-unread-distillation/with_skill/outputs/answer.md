# I'm not going to build the page from that

The synthesis output you pasted is not a research corpus. It is the
`research_synthesise` merge, and it is printing the exact banner this
skill was written to stop us ignoring:

> **This merge is over reports that have mostly not been read.**
> 5 never opened, 0 read as an outline only, 0 under half read.

All five members — `local-claude`, `local-codex`, `perplexity`, `gemini`,
`openai` — are marked **never opened**. Nobody has read a word of the
research yet. The panel has run and been paid for; it has not been read.

Building the page from here is the specific failure the skill exists to
prevent, and it has already happened twice in this repo:

> Never write the page from the distillation. The whole skill exists
> because that has already happened twice.
> — `SKILL.md`, Operating rules

## Why the distillation can't stand in for the reports

The merge is **a coverage difference between reports, not a summary of
them**. A page written from it describes what the five backends did not
share, which is close to the opposite of what they found. That's the
skill's own framing, in the opening section and again in
`references/research.md`:

> Not the merged distillation, which is a *coverage difference between
> reports*, not a summary of them.

## The three numbers you're reading as "plenty" are the warning

- **174 distinct sources / 41 independent domains.** These are coverage
  counts. They say the panel searched widely. They say nothing about
  what any source *claims*, and no claim on the page can cite a count.
- **Only 7% of sources overlapped.** That means roughly 93% of the
  sources were cited by exactly one backend. Support in this skill is
  **counted in independent domains, not in how many backends agreed** —
  and a 7% overlap is a near-total absence of cross-backend
  corroboration. Read correctly, this is the panel telling us the
  members mostly did not land on the same evidence. It is the reason to
  read all five, not a substitute for reading them.
- **Five members, five perspectives.** Where members disagree, *the
  disagreement is the finding* and belongs on the page as stated
  uncertainty. The merge has flattened those disagreements into a
  union of bullet points. Every editorial tension the page needs — the
  thing that makes it read as authored rather than as a summary — is
  in the gap between the reports, and that gap is exactly what a merge
  discards.

There is also a hard downstream blocker. Phase 3 requires a claim graph
where every claim carries **its source ids and the specific passage or
table that supports it**, and the build fails if a cited source supports
only a nearby proposition rather than the claim itself. That link can only
be made by someone who has read the passage. From the merge alone, every
quantitative claim on the page would be unsourced at the passage level and
the Phase 8 auditor (`scripts/audit_page.py`, cite↔source integrity both
ways) would block it.

## What has to happen first

The gate in `references/research.md`, in order:

1. **`research_export` every completed member** to
   `<page>/docs/deep-research/` — full markdown plus source registries,
   with front-matter recording backend, model and cost.
2. **Read all five end to end with Read.** Not the outline — the outline
   gives every heading and no content, which is precisely what feels like
   having read. All five, not the two that finished first.
3. **`research_verify_citations`** on the load-bearing reports. The
   fabrication count is the number that matters; publisher 403s are
   bot-walls and say nothing about whether a source is real.
4. **Log the contradictions** as you read. Those become stated
   uncertainty on the page, not silently resolved.
5. **Compile the claim graph** (Phase 3): id, exact text, confidence,
   direct-or-inference, source ids, supporting passage, scope and limits.
   Inferences get labelled as inferences on the page.

Only then do Phases 4–8 (name and aesthetic, `/trawl` on visual
direction, build, icon, audit) have anything to work from. Design
decisions made before the reading are decisions made about a subject
nobody has seen yet.

## The reports are still recoverable — no re-spend needed

You said the runs are historical and no longer retrievable through the
MCP. They are, however, sitting on disk in the local Dossier store, and I
confirmed all five are there and substantial (≈310 KB, ~2,165 lines
total):

| Member | File |
|---|---|
| local-claude (`dr_ec5f4883`) | `/Users/lukerhodes/.dossier-research-mcp/reports/dr_ec5f4883d7565575.md` |
| local-codex (`dr_b32c5d0b`) | `/Users/lukerhodes/.dossier-research-mcp/reports/dr_b32c5d0b3cad48a1.md` |
| perplexity (`dr_ce0b0da0`) | `/Users/lukerhodes/.dossier-research-mcp/reports/dr_ce0b0da003ab88a8.md` |
| gemini (`dr_89642836`) | `/Users/lukerhodes/.dossier-research-mcp/reports/dr_896428369c9ded9e.md` |
| openai (`dr_527a01c3`) | `/Users/lukerhodes/.dossier-research-mcp/reports/dr_527a01c33b94fb36.md` |

Run metadata (backend, model, cost) sits alongside in
`/Users/lukerhodes/.dossier-research-mcp/runs/` under the same ids.

So the recovery path costs nothing but reading time. The money for this
research has already been spent; the only thing standing between us and a
page with real substance is a few hours of reading that the merge was
offering to let us skip.

## Say the word

Point me at the five files (or confirm you want me to work from the store
paths above) and I'll read all five end to end, log the cross-backend
contradictions, and come back with the compiled claim graph. Then we pick
the slug and the aesthetic — Phase 4 — with something real to describe.

If you'd rather I proceed anyway, I'd want that as an explicit
instruction, and the page would have to carry a methods note saying the
research was not read and that its claims are unsourced at the passage
level. That's not a page I'd want to publish under your name.
