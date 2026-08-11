---
name: braindump
description: >
  Write a context-compaction summary that survives being the only thing the next session
  has, and prove it against the transcript it replaced and against Claude Code's own
  /compact. Use this whenever someone is about to run /compact, asks what to keep before
  compacting, wants to hand a long session off to a fresh one, writes a handover or
  continuation note, or asks why a session "forgot" something after compaction. Also use it
  when someone asks how good their compaction summaries are, wants to measure or improve
  them, or is tuning when auto-compaction fires. Ships a deterministic scorer
  (scripts/score_retention.py) and a head-to-head benchmark against the built-in /compact
  (scripts/benchmark_vs_compact.py), so "this summary is good" is a number rather than a
  feeling.
---

# Compaction quality

A compaction summary is the only *deliberate* artifact that survives. It is not the only thing
that carries through — measured at the wall, roughly 168k tokens of residue survive a 1M-window
compaction (system prompt, tools, recent turns; `post ≈ 50,958 + 0.117 × pre`, n=1,037) and the
summary itself is ~3% of that. What the residue keeps is the *recent* end of the window. What has
exactly one chance to survive is everything else: the reasoning, the files you read, the dead ends
you ruled out, and above all the middle of a long session — summariser faithfulness is measured as
U-shaped, strong at both ends and weakest in the middle (PoSum-Bench). So the summary is not a
recap for a human. It is the **input to a stranger who has to continue your work** and who will
confidently redo whatever you left out.

Write it as **two tiers**, not one. That single structural decision carries most of the
value here, and the evidence for it is in `references/evidence.md`.

## The two tiers

**Tier 1 — pinned. Reproduced verbatim, never compressed, placed first.**

Four categories, and only these four. Keeping this tier short is as important as filling
it: instruction-following degrades as instruction count rises — measured on Sonnet 4.6, follow-rate
falls from 0.964 at one stacked instruction to 0.447 at twenty — so a bloated pinned tier defeats
itself. Treat ~20 pinned items as the ceiling, and consolidate before exceeding it.

1. **Standing constraints and prohibitions** — every "always", "never", "don't", scope
   fence and boundary the user or the project set. Quote them word for word.
2. **User corrections** — every time the user rejected, redirected or corrected you.
   Quoted, with what it supersedes. A correction from a peer agent or subagent counts:
   in a fleet run it is often the most consequential one in the window.
3. **Rejected approaches and dead ends, each with its reason** — "tried X, failed because
   Y, don't retry unless Z". Sweep for **two kinds**, because they live in different parts
   of the transcript and a single undifferentiated sweep returns only whichever is nearer:
   - **Method dead ends** — how to work. A verification command that lies, a shell quoting
     trap, a tool invoked the wrong way, a check that reads green when it is not.
   - **Product dead ends** — what to build. A rejected architecture, a library that emits
     the wrong artifact, a coercion that corrupts stored data, a route deliberately not
     added.
4. **Exact identifiers** — absolute paths, commands, error strings, failing test names,
   IDs, ports, versions, flags. The tokens a successor cannot re-derive or guess.

Measured on a paired case: two summaries of the same window, one written by this skill and
one by the wire addendum, each pinned seven or eight rejected approaches with reasons — and
the two sets were **almost disjoint**. One returned only method dead ends, the other only
product dead ends, and the items each missed were sitting in its own context. Naming the two
kinds is what stops a sweep from stopping at the first pile it finds.
(`references/case-study-paired.md`.)

**Tier 2 — narrative. Genuinely summarised.**

Task state, what was built and why, what remains. Ordinary summarisation competence
applies; the marginal return on effort here is low.

The split exists because the failure is not bad prose, it is a specific span being absent.
ConstraintRot reports constraint-violation rates of 0% when the governing constraint survives
into the summary and 38% when it is dropped — read from the abstract only, so treat the
percentages as unreplicated (`references/evidence.md § Errata`). The direction is what the design
rests on, and the paired case supports it independently: presence very nearly determines
compliance, so the job is recall of a small set of must-survive items, not overall summary quality.

## What actually gets lost — measured on real events

`scripts/benchmark_vs_compact.py` scores the built-in `/compact` against the transcripts it
replaced, using the summaries already on disk. Across **121 real compaction events**:

| class | retention by the built-in `/compact` | events |
|---|---:|---:|
| user corrections | 63.1% | 34 |
| standing constraints | 33.8% | 74 |
| **rejected approaches** | **0.3%** | 68 |
| identifiers | 48.6% | 120 |
| file paths | 16.4% | 119 |

Read the last row first: low recall on bulk is **correct**. Most paths are transient reads
and tool noise, and a summary carrying them all would be worse.

Read the bold row second. **Negative knowledge does not survive compaction at all.** Two
thirds of standing constraints go too. Those are the rows that make the next session repeat
work the user already paid for, and they are cheap to keep — a handful of items each.

These are exact-match figures, so read them as a floor on the built-in rather than a scale to
be beaten: the same matcher scores a full pinned block at 0.0% on the rejected-approach row.
The claim they carry is "the built-in drops this class", which a separately-observed
untouched `/compact` reproduces — one buried fragment out of fifteen traceable dead ends
(`references/case-study-paired.md`). To compare two arms, read `--against`, not this table.

## The keep/drop decision

One question per item: *if this is missing, does the next session do something **wrong**, or
merely something **slower**?*

**Wrong** is unrecoverable. It goes in Tier 1, verbatim:

- Corrections and rejected approaches, with the *reason* — "rejected: adds a dependency"
  survives paraphrase, "rejected" does not.
- Constraints stated once. They never repeat in the transcript, so they have exactly one
  chance to survive.
- Verbatim strings that cannot be re-derived: error text, IDs, hashes, ports, version pins,
  the precise wording of an acceptance criterion.
- Where the work actually stands, including what is broken. A summary that reads as
  finished when tests are failing is worse than no summary.
- Corrections to your own earlier claims. If you said something wrong and fixed it, the
  *fix* must survive, or the wrong version carries forward.

**Slower** is recoverable. Drop it:

- File contents. They are on disk; a path plus what matters about it beats a paste.
- Tool output you can regenerate.
- Intermediate reasoning that reached a conclusion you are keeping. Keep the conclusion.
- Anything already in a file, spec, commit message or todo list. Point at it.
- Exploration that found nothing — unless somebody might repeat it, in which case one line.

The asymmetry is deliberate. Re-reading a file costs seconds. Repeating a mistake the user
corrected costs their trust.

## Preserve exactly, never paraphrase

Inside Tier 1, reproduce byte for byte. Paraphrase destroys the only value these have: a
path that is *nearly* right sends the next session to the wrong file, and an error string
that is *nearly* right does not match a search.

The failure is subtler than dropping things. A constraint of "use type hints everywhere"
was compacted to "the user prefers a consistent code style with type hints" — the absolute
quantifier silently deleted, the requirement changed. Scope boundaries mutate the same way:
"remove the calls in `a.py`, leave `b.py` untouched" became a global removal instruction.

**The pinned tier never contains file contents.** Not a code block, not a pasted comment, not a
config stanza — a path plus the one sentence that matters, always. The two rules above collide in
practice and the wrong one wins: handed a distinctive comment or a schema line, "preserve exactly,
never paraphrase" reads as a licence to paste, and the paste lands *inside* the pinned block as a
Tier-1 item. Measured: on the eval written to catch exactly this, both the skill arm and the
plain-baseline arm pasted a nine-line header comment and a schema fragment, and both blew the
length cap. The skill arm put the comment in its pinned block.

"The user quoted it in this conversation" is not a reason to pin it. What makes an item Tier 1 is
that a successor **cannot re-derive** it — an error string, an id, a port, a decision with its
reason. Anything sitting in a file on disk is re-derivable by definition, so it is a path and a
clause, however precisely it was quoted at you.

Compress the prose *around* the quotes freely. Fragments are fine; drop articles, hedging
and connective filler. The tokens you save are what buys room for Tier 1.

## Order of work: extract, then compress, then verify

1. **Extract first.** Walk the transcript for Tier 1 items and quote them before writing any
   prose. Extraction before generation measurably improves faithfulness, and doing it second
   means the narrative has already decided what mattered.
2. **Then compress** Tier 2 into the remaining budget.
3. **Then verify against the transcript** — not against your summary. Re-read the source
   asking "did every correction, constraint and dead end reach Tier 1?" That is a retrieval
   check with external evidence, and it is not the redundant kind: it looks for spans you
   never wrote down, which re-reading your own output cannot surface. Re-reading only your
   own summary is intrinsic self-correction, which does not reliably improve output and
   sometimes degrades it.

Do the sweep yourself. A subagent returns what it judged salient, and salience is the
judgment being replaced here — the whole method is that these items are exempt from
summarisation rather than well-summarised.

### Sweep the whole window, not the recent stretch

The measured failure is not forgetting to look. It is looking near the end.

In the paired case, the addendum arm rebuilt its pinned block from the transcript and
returned every dead end from the last two hours and none of the older ones — with a
finished pinned block containing the missing eight sitting in its own context. Recent work
is denser, more vivid and more recently attended to, so an unguided sweep terminates there.

Two habits that fix it:

- **Start at the oldest turn in the window and walk forward, and slow down in the middle.** The
  items with one chance left are the ones stated once, long ago — and the measured danger zone is
  the *middle* of a long window: summariser faithfulness is U-shaped (strong at both ends, weakest
  in the middle), and the residue a compaction preserves is the recent end, so the middle is the
  region where a missed item has no second chance anywhere.
- **Sweep once per category, not once overall.** Ask "every standing constraint", then
  "every correction", then "every method dead end", then "every product dead end". Four
  passes over one window beat one pass looking for four things. Sweep by *meaning*, not by
  keyword: a constraint phrased unlike anything in the current task is precisely the
  low-lexical-overlap needle retrieval misses.

If a previous summary is in your context, treat it as a **checklist, not a source**: every
Tier 1 item it carries is one you must decide about explicitly — re-pin it, or point at
where it now lives durably. Silently rebuilding from scratch is how eight items were lost.

### Pin it, or point at it — decide per item, never drop on assumption

Tier 1 has exactly two safe destinations. For each item, pick one:

- **Pin** it verbatim in the block, or
- **Point** at a durable file *and the section inside it* that provably contains it — you
  wrote it there, or you have just read it there.

"It's somewhere in the repo" is not a destination. A rejected approach nobody finds is a
rejected approach somebody retries, and that is the *wrong*-not-*slower* side of the
keep/drop rule.

In the paired case this is the whole difference in the method-dead-end column: the arm that
dropped them had first consolidated them into a named file section and pointed there, and
the pointer checked out. The same arm pinned the product dead ends verbatim, because those
had no durable home.

### The re-read list — instruction files leave with the compaction

A session is steered by files that sit *in* the context as instructions: the CLAUDE.md chain, any
SKILL.md whose procedure is mid-execution, the plan or spec being implemented, a rules file the
user pointed at. Compaction removes them exactly like everything else — and a successor that
resumes without them follows the summary's paraphrase of the rules instead of the rules. That is
the same mutation failure as paraphrasing a constraint, applied to whole files: "use type hints
everywhere" became "prefers a consistent code style" one sentence at a time, and a paraphrased
CLAUDE.md degrades the same way at file scale.

So the pinned block ends with a **REREAD list**: one path per line, each a file whose instructions
were actively steering the session when the summary was written. The successor re-reads them before
continuing. A path is cheaper than a paraphrase and cannot mutate.

What qualifies is *steering*, not *having been read*:

- the CLAUDE.md files in scope for the work (global, project, subdirectory);
- a SKILL.md whose procedure is partway through — highest priority, because a half-executed
  procedure with no instructions is how a successor confidently freelances the second half;
- the plan or spec file the work is implementing;
- any file the user explicitly said to follow.

A file that was merely read as data does not qualify; listing everything opened re-imports the bulk
the compaction exists to shed. Anthropic's own prompting guidance names compaction as a hydration
point — inject refreshed context "through tools … or during context compaction" — so this is the
documented pattern, not a workaround. It is also the most-requested compaction fix in Claude Code's
own issue tracker (auto re-reading of CLAUDE.md/MEMORY.md after compaction, e.g. #21925, #31409,
#9796, filed because "the compaction summary neither preserves nor references them"): the REREAD
list is the precise form of the fix those reports ask for crudely.

## Structure

Claude Code's `/compact` produces nine sections, and a summary landing in a Claude Code
session should match them — the harness expects that shape and matching it costs nothing:

1. Primary Request and Intent · 2. Key Technical Concepts · 3. Files and Code Sections ·
4. Errors and fixes · 5. Problem Solving · 6. All user messages · 7. Pending Tasks ·
8. Current Work · 9. Optional Next Step

Put **Tier 1 first, before section 1**, as an explicit pinned block, and close that block with the
REREAD list. Do not scatter it through the nine sections: the whole point is that these items are
exempt from summarisation rather than well-summarised, and burying a constraint inside "Errors and
fixes" invites the paraphrase that kills it.

Two additions inside the standard shape:

- **Mark user corrections as standing instructions**, not as history. A correction is a
  rule that still binds; a self-caught slip is past tense.
- **Make "Current Work" state the failure mode, and the unfinished obligation.** "Tests
  green" and "tests failing on 2 auth cases" lead to completely different next actions —
  and so do "tree clean" and "tree clean, but the deliverable this turn promised was never
  printed". Report the state of the work *and* the state of the turn in progress. A summary
  written while a task is half-done inherits that task, and a clean tree is not evidence
  the obligation was met.

  In the paired case, the arm that scored better on every other axis said "Wave 1 complete…
  Nothing is failing" and omitted the half-finished deliverable of the turn it was written
  in; the other arm named it. Accurate about the tree, wrong about the obligation.

Outside Claude Code, use whatever shape fits, but keep the pinned tier and sections 1, 4, 7
and 8.

## Length

Observed median for `/compact` is about 20.6k characters. That is a ceiling, not a target. A
summary is too long when it contains material the next session could regenerate, too short
when a correction or constraint is missing. If you are over budget, cut file contents and
intermediate reasoning first. **Never cut Tier 1 to fit.**

Judge the two tiers on different scales. The pinned block is measured in **items carried**;
the narrative is measured by **whether anything in it is regenerable**. A pinned block does
not buy the narrative any slack — the keep/drop rule still applies to every line after it.

The paired case makes the point concretely: one summary was 2.06× the other's length with a
pinned block the same size, and the extra ten thousand characters were a pasted source
comment, a code fragment, a table format and shell commands — all regenerable, all things
the keep/drop rule already excludes. Length went entirely to the half that did not need it,
and the longer summary still carried eight fewer dead ends.

Write the summary to the length the material needs. Do not pad the nine sections to look
thorough; an empty section that says "none" is better than a paragraph restating section 1.

## When to compact — and when to do something else

Compaction is the lossiest tool available, not the default one. Measured against other
context-management strategies it is the weakest: roughly +2.6 to +2.7 points on task
success, and *negative* for one frontier model, where moving work into tool calls bought
+9.4 to +13.3. Simply masking old tool outputs matched summarisation's solve rate at about
half the cost.

So before compacting, ask whether the cheaper thing works: clear old tool results, offload
state to a file, or start a fresh session pointed at a progress file.

When you do compact, the boundary matters:

| boundary | compact? | why |
|---|---|---|
| research → planning | yes | research bulk is spent; the plan is the distillate |
| planning → implementation | yes | the plan is in a file; free the context |
| after a failed approach | yes | clear the dead-end reasoning, keep the "don't do X" |
| debugging → next feature | yes | traces pollute unrelated work |
| implementation → testing | maybe | keep if tests reference recent code |
| mid-implementation | no | partial state and variable names are expensive to lose |

Auto-compaction fires at a median of 998,550 `preTokens` — 99.9% of a 1M window — with no
idea where a task boundary is. Compacting deliberately at a boundary beats being compacted
arbitrarily at the ceiling, which is the whole argument for doing it by hand.

## The escape hatch: write it down instead

For anything in Tier 1 that must survive *several* compactions, do not trust the summary
channel at all. Write it to a durable file the next session reads — `CLAUDE.md`, a progress
file, a decisions log — and have the summary point at it. Compaction is a lossy channel by
construction, and routing the load-bearing minority around it is more reliable than
compressing it well.

## Scoring

Do not trust your own read of a summary you just wrote — you know what it means, which is
exactly the knowledge the next session lacks.

```bash
python3 scripts/score_retention.py --transcript <session.jsonl> --summary <summary.md>
python3 scripts/score_retention.py --transcript <w.jsonl> --summary <a.md> --against <b.md>
python3 scripts/score_retention.py --scan-history          # baseline across your history
python3 scripts/benchmark_vs_compact.py --arms cli         # score the built-in, free
python3 scripts/benchmark_vs_compact.py --arms cli,skill -n 8   # head-to-head
python3 scripts/benchmark_vs_compact.py --arms cli,pinning,pinning2 -n 8  # addendum v1 vs v2
```

The correction and rejected-approach lists are the part that matters. A dropped path is a
slower next session; a dropped correction is a wrong one. Bulk percentages are context, not
a score to maximise — pushing paths toward 100% would mean pasting the transcript back in.

**Two matchers, and they answer different questions.** `exact` is substring identity: right
for a path, an id or an error string, where nearly-right is worthless. `soft` is
distinctive-token overlap: right for a constraint or a rejected approach, which a summary
legitimately restates in its own words while keeping the reason. Read the semantic classes
on `soft`. Scored on exact alone, two summaries carrying seven or eight correctly-reasoned
rejections apiece both report **0.0%** — an instrument that scores a full pinned block the
same as an empty one cannot tell you whether pinning worked.

**`--against` is what settles a comparison, not the percentages.** It scores two summaries of
one window and then prints, per class, the spans each kept that the other dropped. Prefer the
disjoint sets, because the spans a detector finds are sampled from the transcript and a long
window's sample is dominated by its recent, denser portion — so a recall percentage quietly
rewards a summary that swept only the recent end. On the paired case, soft recall ranks the
recency-biased summary nearly twice as high on rejected approaches, while reading the two
blocks shows near-disjoint sets of comparable size. Use recall to check a class did not
vanish; use the disjoint sets to decide which summary is better.

**The free baseline poisons itself once the addendum ships.** A harness that splices the
pinned-block instruction into live compactions leaves *its* summaries on disk looking like any
other `/compact` event, so the `cli` arm quietly starts measuring the treatment. Measured on this
machine: **27 events** in the corpus already carried the addendum marker. `find_events` now excludes
them by default and says how many it dropped; `--include-treated` keeps them when the wire arm is
what you want to measure. Any baseline number taken before that filter existed is contaminated by
however many treated events the sample happened to draw.

**Two confounds the benchmark reports beside every score, because they will otherwise decide
the result:** summary length, and extractiveness. A summary that "wins" by copying more has
not won, and judges reward copied text regardless of whether it helped.

## The honest limits

- **The 0.3% is a floor on the built-in, not a gap between arms.** It was measured with the
  exact matcher, and that matcher scores a *full* pinned block at 0.0% too. What it supports
  is the observation that the built-in prompt carries almost no negative knowledge, which
  the paired case independently reproduces. What it cannot support is any claim that one arm
  beat another by some number of points. Rank arms with `--against` and read the disjoint
  sets; use `soft` recall only to check a class did not vanish entirely.
- Exact retention is string match, so a faithfully *paraphrased* correction scores as lost.
  The soft matcher exists for exactly this and is reported beside it; the miss list is there
  so you can read the spans and judge.
- The scorer measures what was carried, not whether the summary is coherent or accurate
  about state. A summary can score well and still misdescribe where the work stands — the
  paired case has one that does.
- The correction and rejection detectors are keyword heuristics. They miss politely-phrased
  corrections and flag some non-corrections; treat the output as a candidate list to read,
  not a count to report. They also sample spans from the transcript, so a long window's span
  population leans recent — which makes recall over it a poor way to rank two summaries.
- **On most real sessions the detectors find nothing, so the transcript benchmark cannot
  discriminate.** Measured over 30 random compaction events: corrections yield zero spans in
  **93%** of events (median 0, max 1), rejected approaches zero in **70%** (median 0, max 13),
  constraints zero in 26%; a fifth of events have no span in any of the three classes. That is
  why the 121-event table's correction row rests on 34 events rather than 121. The consequence
  is practical: a head-to-head at n=8 will report `n/a` for the classes you care about most of
  the time, and a controlled scenario with known ground truth — the eval set — is the better
  instrument for "does the method work". Use the transcript benchmark for the confounds it
  measures reliably (length, extractiveness, structure) and for the rare high-yield session.
- The head-to-head is paired on identical transcripts, but n is small. Report the effect and
  the sample, never a bare percentage.
- Evidence, with citations and the numbers' provenance: `references/evidence.md`. The paired
  three-arm case, and the instrument faults it exposed: `references/case-study-paired.md`.
