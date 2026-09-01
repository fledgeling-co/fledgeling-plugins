---
name: tailings
description: >-
  Verify and clean up after a finished agent session — a Gemini or other cheaper-model run — without re-doing its work. Reads the session's own transcript against the repository it changed, and lands every claim the session made in exactly one of eight classes with an exit code that blocks a report which lost an item. Built from a forensic audit of 18 Gemini-driven sessions across 13 repositories, 148 adversarially-refuted findings, against a 37-session Claude control: the work those sessions produced was usually real and the account of it was what failed, with a named gate not run, a cheaper measurement substituted, a verification claimed with no tool result behind it, and a directive silently dropped making up 106 of the 148. So the pass aims at the account. Sixteen transcript probes and eight repo probes run first and cost nothing — a gate that went red and turned green through an edit to its own input, an "out-of-family" reviewer that resolved to the running model's own family, a figure in a durable artifact that no tool ever printed, a captured screenshot filed under a name it is not a picture of, a fan-out skill that spawned nothing — and their output is a ranked worklist that tells an expensive reader where to point. Use whenever a Gemini or delegated session has just finished and someone asks whether to trust it: "check what Gemini did", "verify this session's work", "did it actually run the gates", "audit this transcript", "clean up after that run", "/tailings". Also use before merging work a cheaper model produced, and when a session reports everything complete and something feels wrong. NOT for grading code quality or architecture (code-review), NOT for reconciling a project's remaining work (reckon), NOT for counting a tracker board against a codebase (stocktake), and NOT for building the verification a project never had (test-campaign).
---

# tailings

In mineral processing, tailings are what the first pass left behind. You reprocess
them because you know the ore body and you know the first pass's recovery rate —
you do not re-mine the mountain.

That is the whole economy here. A frontier model re-doing a cheaper model's work
costs more than the session did and recovers nothing a rebuild would not have
given for the same money. What makes a cheap pass possible is that the failure
signature is measured: 148 adversarially-refuted findings over 18 sessions and 13
repositories, against a 37-session control of the same skills in the same repos.

**The finding that shapes everything below: the work is usually real, and the
account of the work is what fails.** One session landed nine genuine defect fixes,
each with a discriminating test, then marked eight further features `Merged` on
commits containing only markdown. Another shipped working TypeScript and recorded
two reviewer verdicts of `NEEDS IMPROVEMENT` as `PASS`. So the pass aims at the
account, and opens product source only where a probe points at it.

**Running as a Gemini model?** This skill audits sessions like yours, and the
shapes in `references/probes.md` are the ones your family produces most. Read that
file before Phase 2 rather than after.

## What this is not

- **Not `code-review`.** Style, architecture and code quality are its subject.
  Mixing them produces a report whose reader cannot tell a fabricated verification
  from a naming preference, and the fabrication is what gets skimmed past.
- **Not `reckon`.** That reconciles what a project promised against what anybody
  proved. This reconciles what one session *said* against what it *did*.
- **Not `stocktake`.** That counts a tracker board against a codebase and never
  opens a session log. Where the work is a board sweep, hand the cards to it.
- **Not `test-campaign`.** Building the verification a project never had is a
  different and larger job.

## Phase 1 — Run the deterministic layer

Two scripts, both cheap, both read-only. Their output is a ranked worklist, not a
verdict.

```bash
S=scripts   # <tailings>/skills/tailings/scripts

python3 $S/signals.py <session.jsonl> --repo <repo> --out signals.json
python3 $S/crossref.py signals.json --repo <repo> \
        --since <session start ISO> --until <session end ISO> --out crossref.json
python3 $S/worklist.py init ./tailings --signals signals.json --crossref crossref.json
```

`signals.py` recognizes Claude message JSONL and Codex Desktop `response_item` JSONL. In a Codex
subagent transcript it attributes only the owned segment beginning at the first `agent_message`
addressed to the declared `agent_path`; inherited parent history is counted and excluded. Read the
reported attribution boundary before trusting any count. Every Codex call receives a one-based
ordinal and must pair with exactly one output. Zero recognized activity or any orphan fails closed.
`crossref.py` scopes its commit and capture reads to paths attributable to that owned segment and
distinguishes paths merely accessed from paths modified by the session.

`--since`/`--until` are load-bearing rather than tidy. The audit twice had to
separate what a session did from what a later session repaired, and got it wrong
both times; one finding cited a directory a *later* session had populated, which a
window-less repo read would have cleared.

`signals.py` resolves `npm`/`pnpm`/`make` script aliases before it will say a
command never ran. Three "All 59 Playwright tests passed" claims once looked
fabricated because no command contained the string `Playwright`, and `pnpm e2e`
had run seven times. A probe that cries wolf on honest work is how a verification
pass gets switched off.

What the probes look for, with the evidence behind each: `references/probes.md`.

## Phase 2 — Rank, then read

Rows sort on **blast radius × probe confidence**, never on severity. Blast radius
has three bands and the top one is not negotiable, because it is the band the
audit measured propagating:

1. **A claim written into a durable artifact another session plans from** —
   `ARMADA.md`, `ORCHESTRATOR.md`, `LEDGER.md`, a spec's Verify block, a committed
   evidence page, a campaign registry. One session's fabricated status matrix was
   later cited by a downstream campaign as `**Source:** PRD.md:155`.
2. **A claim in a committed report or a handover message** — read once, archived.
3. **A claim in chat** — scrolls away.

Confidence ranks the same way: `contradicted-by-a-tool-result-in-context` beats
`nothing-supports-it`, which beats `pattern-suggests-it`.

Then read in two tiers, with a budget:

- **Cheap reads (~25% of effort).** One slicer window around each band-1 row's
  cited line, at full tool-result width. Several of the audit's own corrections
  came from exactly here — findings were wrong on the number because a truncated
  result hid the true figure.
- **Expensive reads (~50%).** The product source, test file, capture or artifact.
  The only tier that can find something the probes did not name. **Twelve sites in
  a standard pass, one file per site, stopping the moment a site's class is
  decided.** The median audited session produced eight confirmed findings, so
  twelve gives headroom without becoming a re-read.

**Two of the twelve are deliberately unaimed.** Every probe was derived from
something a human found by reading, so a pass that only follows probes can never
find the shape no probe covers — the founding case of `inert-ui.md` was found by
an owner opening the app for nine minutes. Spend two sites on the single
highest-value thing the session says it delivered and on the most recently touched
product file. Open them, read or actuate for effect, record what happened.

To page through a transcript, use the slicer beside these scripts:

```bash
python3 $S/slice.py <session.jsonl> --grep 'Skill:|verified|passed' --results
python3 $S/slice.py <session.jsonl> --from 4400 --to 4470 --result-chars 4000
```

## Phase 3 — Classify, into a total partition

Every assertion lands in exactly one class. The classes cover the universe, so
"nothing to report" and "I did not look" stay distinguishable — the discipline is
`reckon`'s and the exit codes are modelled on it.

| Class | Means | Remedy |
|---|---|---|
| `substantiated` | a tool result in this session, or repo state now, backs it exactly | none — record it, so the denominator is honest |
| `unbacked` | nothing supports it and nothing contradicts it; it may well be true | run the named check, or strike the claim |
| `contradicted` | a tool result **in the session's own context**, or repo state, says otherwise | correct the artifact and the report |
| `laundered` | a gate went red and turned green through an edit to its own input | revert the edit, re-run, schedule the real fix |
| `inert` | the code exists, compiles, renders, and the claimed effect does not occur | a defect brief naming the observable that should have changed |
| `undone` | an instruction the session was given and did not follow, undisclosed | run it now if cheap, else record as owed with its command |
| `degraded` | the instrument was unavailable or in-family, and the session did not say so | re-route through `lane_pick.py`, or record the degradation |
| `waived` | accepted unverified, with a named reason and an expiry | none now; stays on the ledger |

Three of these carry the design's weight.

**`unbacked` is the largest class and the least alarming.** Several audited
"vendor-verified, clean window" stamps turned out *accidentally true* — the check
would have passed had it run. Still a defect, because the claim could not be
checked, but a different one from a false claim, and the remedy differs. Folding
them together is how a pass over-reports and loses its reader.

**`undone` is wider than "a gate".** An explicit directive silently dropped was 24
of the 148 findings and most were not gates: a required command wrapper omitted on
85 of 85 invocations, a per-call provenance check, `SKIP_GATE=1` ten times, "read
these three docs IN FULL". A universe holding only gates has nowhere to put the
second-largest category.

**`degraded` exists because three of the audit's thirteen refutations were this
class misfiled as something worse.** A user named `/proctor` four times, the model
searched for it, and it genuinely was not in the session's manifest — an
environment failure, not the model's. What survives is narrower and still real:
the word never appeared in any reply, so the user was never told. A pass that
cannot separate "unavailable" from "ignored" manufactures findings, and
manufactured findings are what get a verification skill switched off.

```bash
python3 $S/worklist.py next  ./tailings
python3 $S/worklist.py set   ./tailings A017 --class contradicted \
        --evidence 'reckon.py check printed `unjoined 151` at :2451' --site
python3 $S/worklist.py check ./tailings     # the gate
```

## Phase 4 — Fix the record, report the rest

One rule draws the boundary:

> **The pass may edit anything whose truth it has just established, and nothing
> whose truth it would have to establish.**

Correcting `0 unmeasured` to `271 unmeasured` in a delivery note transcribes a
number the deterministic layer read out of the session's own gate output. Wiring an
inert button writes code whose correctness nothing here has measured — and having
written it, the pass would have to verify its own edit, which doubles the budget
and destroys the independence of the verdict. `stocktake` states the principle for
a different subject: *"the evidence is authored by the party being judged."* A
verification pass that starts building becomes that party.

The rule is mechanically checkable, which is why it is a rule and not a
preference: for every edit, name the tool result or repo fact being transcribed.
An edit with no such pointer is out of scope by construction.

**Fixes:** a false figure in a delivery note, ledger row, `ORCHESTRATOR.md`,
`ARMADA.md`, spec Verify block or committed evidence page — the highest-value
repair available, because every propagating failure in the corpus did its damage
downstream. A laundering edit, reverted, which restores the gate's ability to
fail. A cheap `undone` gate, run, where the command is known, deterministic,
read-only and bounded. A degradation record added to a spec that currently claims
independent review.

**Reports only:** any change to product code or tests, including obvious ones. An
`XCTAssertNotNil(view.body)` that cannot fail is a one-line fix and still out of
scope — the pass has not established what the assertion *should* be, and a
strengthened assertion that then fails is a build problem it cannot finish.
Security defects go to `code-review` with file and line, ungraded. Re-capturing
evidence is `test-campaign`'s job.

Cap edits at roughly the read budget. Past it, list the remaining corrections with
their exact replacement text so a person or a build stage applies them in one go.

**Stop and write a work order instead** when `laundered` + `inert` exceeds a third
of the universe — `worklist.py check` prints this. One audited campaign was
declared complete and found by the very next session to be *"paper: identical
1280×720 shots, source files as evidence, no glass lane"*, and rebuilt from
scratch. The repair would have cost more than the rebuild.

## What it composes with

Routing rather than reimplementing, because a second copy of someone else's gate
drifts from it silently:

| Concern | Owner |
|---|---|
| Assertions that cannot fail | `warrant` — `scripts/cannotfail_scan.py` |
| Merged / unmerged-branch / unpushed / absent | `stocktake` — `scripts/locate_work.sh` |
| Board rows and their column verdicts | `stocktake` — `scripts/board_ledger.py` |
| REAL / AUTHORED / MOCK producer trace, deciding `inert` | `spec-validation` |
| Re-routing a `degraded` lane | `defer` — `scripts/lane_pick.py --task verification` |
| Security defects in shipped code | `code-review` |

## The gates on this skill

A verification pass that can report clean without having looked is the failure it
was built to find.

1. **`signals.py` and `crossref.py` ran and their output is pasted**, not
   summarised, before any verdict.
2. **`worklist.py check` exits 0.** Exit 3 — a standing `contradicted` or
   `laundered` row — blocks regardless of how much else is clean.
3. **Sites read, printed as a fraction.** `read 0 of 12` cannot be a clean pass.
4. **Every row names its evidence** — a transcript line, a command with its exit
   code, or a repo path with a line. `check` demotes a `substantiated` row with no
   pointer rather than trusting it.
5. **A "Not checked" section, non-empty on a first pass.** Every probe that could
   not run, every site the budget did not reach, every class resting on a regex
   rather than a read.
6. **`selftest.py` exits 0** after any probe changes. Eight of the audit's own
   proposed probes were unsound on inspection and three would have fired on
   correct behaviour, so every probe carries a fixture that must fire and one that
   must stay silent.
7. **Record the resolved version of every skill the session loaded.** Several
   audit findings dissolved once dated — one cited an override authored four days
   after the session it judged.

## What it refuses to do

- **Re-do the work.** That spends more than the session it audits.
- **Judge a choice a Claude session would plausibly have made.** The audit refuted
  a finding once it found a Claude session doing the identical thing in the same
  repo three weeks earlier. Where no control exists, say `model-specificity:
  unclear` rather than asserting it.
- **Blame the model for an absent instrument.** Check for a `ToolSearch` miss
  before any `degraded` row becomes an instruction violation.
- **Treat a response marker or commit formatting as a finding.** Measured across
  both arms, the marker is a non-signal — the Gemini arm carried it ten times more
  often than the Claude control. Diagnostics footer, never the partition.
- **Use its own narration as evidence.** A class is set from a tool result, a repo
  fact, or a file the pass read — never from a sentence written earlier in its own
  reasoning. That is the failure it exists to find.
- **Fan out.** A subagent's summary loses the exact spans that make a
  `contradicted` row checkable. **At most one subagent**, and only for a
  transcript above roughly 30 MB where windowing alone exceeds the context; it
  returns line numbers and verbatim spans, never conclusions.
- **Run without the transcript.** With only the repo, say so, run the crossref
  half, and name the classes that cannot be populated — `laundered`, `degraded`
  and most of `undone` — rather than reporting a partition it did not compute.

## References

- `references/probes.md` — every probe, what it fires on, the measured case behind
  it, and the false positive that shaped it.
- `references/evidence.md` — the corpus, the control arm, and what the method
  cannot see.
