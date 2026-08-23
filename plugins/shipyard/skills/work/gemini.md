# gemini.md — `work`

Read this once, now, then read `SKILL.md` and the references it names and run every phase as
written. Each override names the phase or rule it lands on.

`work` is the one shipyard stage that writes product code, and the measured evidence speaks to it
most directly and least kindly: the two buckets where this family produces hard zeros are two of the
four shapes this skill's own executor table already names. Everything around the code is an audit —
seven phases, two tables that must reach all-✅ before the status moves, a completion record a
stranger grades afterwards. So the shape to design against is not a worse feature. It is a filled
Clause table in front of a check nobody ran.

## Epistemic status

- **Tiers used:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]` — **no Gemini run
  of `work` has been observed**, at any tier. The `[measured-family]` sources are two single sessions
  (n=1 each) and a 106-task benchmark at two effort levels, in `geminify/references/evidence.md`.
- **The tier the evidence is about.** Every measured rate below was observed on `gemini-3.7-flash`
  (one session on `gemini-3.7-flash-high`) — **flash-tier claims, not to be projected onto the Pro
  tier.** **[docs]** The defaults drift inside the family: *"If thinking_level is not specified,
  Gemini 3 will default to high."* against, from the 3.5 Flash release notes, *"The default thinking
  effort is now medium, changed from high in Gemini 3 Flash Preview."* On Pro these overrides stand
  as `[docs]`-grounded discipline; every `[measured-family]` number is an open question.
- **Unmeasured on this skill:** nothing measures Gemini running a worktree build under fan-out, or
  choosing an executor lane for its own slice · the bound-following rate below was measured on UI
  assertions, so its transfer to `≤4 concurrent agents` is `[derived]` · no Gemini agent has been
  observed running the `miss-classes.md` exercises · and no run has been measured *with* a
  `gemini.md` against one without.
- **The self-limitation.** **[docs]** A conditional side file is the shape the health checklist
  warns about: *"Avoid writing a prompt with non-linear logic or conditionals that require the model
  to piece together fragmented instructions from multiple different places in the prompt."* Read it
  in one pass, before Setup, never mid-phase.

## Route out before Phase B: two shapes, and the skill already ships the command

**[measured-family]** Two of eight measured work buckets do not merely score lower — they produce
**hard zeros** on most decided rows (§2.1): self-contained pages authored from prose, and brownfield
edits to an existing multi-file repo, the latter at 79% zeroed rows against opus's 43%. Four of the
other six are level or ahead, so routing the whole stage out would be wrong.

| shape | where it lands in this stage | measured |
|---|---|---|
| `brownfield-integration` | Phase B slices that edit existing code, span >2 files, or carry several ACs at once | 24 against opus's 50 |
| `regression-sensitive` | Phase B slices that must keep an existing suite or public API passing; Phase C's rebase | 42 against 65 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape brownfield-integration
```

The skill already routes *executor slices* this way — `name what the slice is and let defer pick`.
What this adds is that **your own edits go the same way**: Phase C's conflict resolution and Phase
E's fixes are code you write directly, and both are `brownfield-integration` by the skill's own
definition. **Two shapes omitted:** `static-page` is not this stage's work — a page authored from
prose belongs to `design`'s mocks — and `visual-design` is omitted because Phase D's UI-fidelity
lens compares a build against the mock index, measurement against an oracle rather than judged
aesthetic quality, and the corpus abstains on judging. `greenfield-module` (75 against 75) and
`react-ui` (63 against 69) are deliberately absent: naming them would route away work this family
does as well as opus.

## What transfers intact

Two of this skill's rules are already written the way this family needs, and the overrides give them
denominators rather than new wording. **The typed evidence rule** — static closes on `file:line`,
visual on a pasted measurement, behavioural on an exercised request or a red→green pair, persistence
on a producer plus a stored row — is verification-as-an-instruction with the admissible artifact
named per type, and its clause `an unclosable row is a blocker and the status stays put` closes the
escape hatch a categorical scope usually leaks through. And **`If you cannot classify it, omit
--shape and the router falls back to headroom alone`** is a closed set with a stated default —
**[docs]** the multiple-choice remedy exactly: *"The response is correct, but the model didn't stay
within the bounds of the options."*

## The scan

`scan_skill.py` over `SKILL.md` and `references/miss-classes.md` (311 lines): **6 quota candidates,
1 bound row, 9 relative qualifiers, 0 qualitative skill references, 0 shouted passages.** I bound
**3** of the listed 5 into the ledger below and dropped **2** as prose — both are headings, and row
1 carries the second anyway. The one bound row found is the harbourmaster weight legend, also prose;
the five real bounds in override 5 were moved across by hand. Modules fired: `delegation` (7),
`gate` (4), `visual` (3), all three written — `visual` narrowly, because this stage measures and
ties captures rather than authoring them. `emphasis` did not fire and none is written.

## Override 1 — the quota ledger (`## Running it`, Phase A, Phase D)

**[docs]** *"Avoid using subjective or relative qualifiers that lack a concrete, measurable
definition."* **[measured-family]** Why this is override 1: one run delivered **12 of 12**
requirements a brief *enumerated* and satisfied every requirement named *categorically* with one
instance or none — all surfaces → 5, all states → **1**, all menus → **0**, all flows → **0**
(§1.1.1, n=1); the skill it followed named six states in prose *and* stated an explicit completeness
condition. So the count becomes a cell to fill, not a sentence to read. Write this into the run's
notes at Phase A and report the fractions in the Phase F record; filled against a three-slice
feature, as the exemplar the rest are measured against:

| # | categorical, in the skill's words | denominator | filled | reported |
|---|---|---|---|---|
| 1 | `Every phase A–F (+D′) runs to completion` | 7 phases | 7 run, each with its artifact | `7 of 7` |
| 2 | `every Acceptance Criterion, Constraint & Decision, and triage Assumption` (Clause table) | 11 AC + 4 C&D + 6 assumptions = 21 | 21 rows, each typed | `21 of 21 typed` |
| 3 | `for every new user-facing capability its UI→producer wire` (Reachability table) | 5 capabilities | 5 traced UI → BFF → producer | `5 of 5` |
| 4 | `every row closes per the typed evidence rule` | 26 rows (21 + 5) | 24 closed, 2 blockers named | `24 of 26 — status stays put` |
| 5 | `Exercise every miss-class in references/miss-classes.md on the real path` | 11 classes | 8 applicable, 3 n/a: no untrusted surface, no money path, no tenant write | `8 of 11, 3 n/a` |
| 6 | `every route/component/string/behaviour changed or inverted` (affected-test sweep) | 14 greps → 9 hits | 9 updated and RUN | `9 of 9 run` |
| 7 | `every new endpoint/exported fn/action-seam field` (wire-through gate) | 12 symbols | 12 reach a real non-test caller | `12 of 12` |
| 8 | `every unticked box appears in the note` (plan AC reconciliation) | 14 boxes | 12 ticked, 2 as Dropped rows | `14 of 14 accounted` |

A cell that cannot be filled reads `n/a: <reason>` — **[docs]** *"provide instructions for handling
missing data rather than assuming inserted data will always be present and well-formed."* Row 4 goes
first: it is the only row where the honest answer is a **stop** and the plausible one is
`Developer Review`.

## Override 2 — every gate is a pasted command, and the prerequisite is checked first (Phases B, F)

**[docs]** *"Include specific verification steps in either the system instructions or your prompts
directly."* And *"Verify your claims by quoting the exact applicable information."*

**[measured-family]** What fills the vacuum when verification is left to prose (§1.1.2, n=1): a
review asserting a browser engine as verified when that engine had failed all four invocation
attempts and never ran, and a `100% pass rate on contrast` from a probe never executed — measured
afterwards at 3.65:1 on every primary button and one glyph at 1.00:1, invisible. Five well-formed
`PASS` rows, where the shape was specified and the procedure was not. This skill's Phase F record is
that shape, so the gate is a paste:

```
prereq  docs/plans/plan-DIO-0412.md          committed 7c21e0d · 14 AC boxes read
prereq  design/mocks/DIO-0412/INDEX.md       15 cells, 0 unwaived empty
$ pnpm --dir $WT typecheck                   → tsc 0 errors
$ pnpm --dir $WT test -- --run src/billing   → 46 passed, 0 failed (6 files)
$ grep -rn "createInvoiceDraft" apps/ --include=*.ts | grep -v spec  → 3 non-test callers
red@a91c4f2 → green@7c21e0d                  billing.e2e.spec.ts:118 (AC-07)
gate 6  visual regression suite              → n/a: repo ships none — recorded as absent
```

Three rules a paste enforces and a tick cannot. **A denominator of zero is a gate that never ran** —
`0 tests passed` and `no tests found` print differently, and the skill's own line is that a gate you
could not run is `a blocker, never an implied pass`. **The prerequisite comes before the property**:
**[measured-family]** on `COD Dossier` (§1.2.2, n=1) a deterministic auditor validated tags,
citations and contrast floors thoroughly, had no check that its upstream artifacts existed, and
passed two entirely skipped skill invocations with exit code 0. And **prove the check can fail** —
the red→green pair is that proof, and the eight cannot-fail shapes in `evidence-rules.md` are what
makes a green one worthless. **[docs]** For the arithmetic: *"Gemini's code execution tool enables
the model to generate and run Python code, and should be enabled whenever the model needs to perform
any kind of arithmetic, counting, or calculation."* Take the runner's number, never a prose total.

## Override 3 — the phases are a chain of files, not a checklist (Phases A → F)

The scan's `0 qualitative skill references` is what makes this necessary, not unnecessary.
**[measured-family]** §1.2.1 (n=1): a skill instructed that every design decision `goes through` two
named skills, and the run invoked neither — its own diagnosis being that the rules were already in
context and nothing downstream depended on a file only those skills produce. Corroborated outside
this repo (§7.2) by a Gemini 3 **Pro** transcript reclassifying a `GEMINI.md` rule as guidance, so
it binds on every tier. **[docs]** The remedy is the chain: *"make each step a prompt and chain the
prompts together in a sequence."* Each phase ends in an artifact the next opens before it starts:

```
A  build spec + Clause/Reachability tables  →  written to the notes  ; B reads them for slice scope
B  the diff in $WT + gate output            →  git log + gate paste  ; C rebases what B committed
C  rebase onto INT + re-run gate            →  new sha, gate paste   ; D measures at that sha
D  filled (never regenerated) A tables      →  findings list         ; E works the list
E  fixes + re-run evidence per fixed row    →  new artifacts         ; D′ grades against them
D′ fresh same-family validation             →  discrepancy list      ; F reconciles or routes to E
F  completion record + AC reconciliation    →  the status move
```

The skill already says `carry this same checklist into Phase D and fill it in, never regenerate it`
— that sentence is the chain. **The same ordering governs the inputs**: read, then answer, as two
ordered steps. **[measured-family]** §1.2.4 recorded both halves failing in one session — a question
naming three skills answered from memory without loading any, then, asked to fix it, a skill
launched instead of an answer. The plan, spec thread and mock index named in your invocation are
**read from the main tree at absolute paths** before Phase A, and re-read at each boundary rather
than recalled. This stage's incident ledger says it from the other side: a relative path under `-C`
resolves inside the worktree, finds nothing, and `the run builds from the task description alone,
looking successful and grounded in nothing`.

## Override 4 — measure the render; tie the capture to its subject (Phase D, Phase F)

**[docs]** *"Ask the model to describe the images before performing the task in the prompt."* And
*"To improve the response, point out which parts of the image are most relevant to the prompt."*
**[measured-family]** One run produced 3 render calls and 4 opened images for a 10-cell artifact and
improvised an accessibility floor to zero — `aria-*` 0, `:focus-visible` 0, twelve `<div onclick>`
carrying the navigation of both apps (§1.1.3). So Phase D's UI-fidelity lens gets a capture
denominator: one capture per surface × state named in the mock index, all opened, the fraction
reported beside the lens; name what is in the crop before judging it.

**[docs]** Hand the mock index over as a reference rather than describing it — *"For UI
generation, the model shows high design adherence and parity based on a reference input, whether
it's a screenshot, an image, or a full design system."* That is the documented strong path, and
unmeasured on this corpus, so treat it as guidance rather than a promise. Admissibility is the
skill's own Phase F check: the URL the browser **ended up at**, no two clauses sharing one sha256 —
`a filename is written by whoever ran the capture, not by the app`.

## Override 5 — the bound ledger, read off what you did (`## Running it`, Phase B, `## Guidelines`)

**[measured-family]** A stated maximum is the shape this family exceeds rather than forgets.
Classifying every failing UI assertion by whether it states a bound or asks for a thing: **58%** of
Gemini's failures at `medium` and **86%** at `high` were bound-shaped, against 8% for opus and 6% for
the OpenAI lane; one rule failed on *every* instance in its set on a run that passed 37 of its 39
other assertions (§2.2). A bound is violated by what you did not write, so it survives every check
that looks at what you did.

**[docs]** Google treats these as a component in their own right — *"Restrictions on what the model
must adhere to when generating a response, including what the model can and can't do."* — and asks
that *"all requirements, constraints, options, and preferences are exhaustively incorporated into
your plan."* Five of this skill's bounds are prohibitions in prose, read back as counted properties:

| bound, in the skill's words | countable property | readback | observed | within? |
|---|---|---|---|---|
| `Cap each wave at ≤4 concurrent agents` | agents live in one wave | count Task calls per wave | 4 · 3 · 2 | yes |
| `never two agents in one file` | files claimed by >1 slice | intersect the wave's file scopes | 0 overlaps | yes |
| `no drive-by refactors` — `every changed line traces to a checklist row` | changed files with no Clause row | `git diff --name-only` minus the table's paths | 1 (`utils/date.ts`) | **no — disclosed as out-of-slice** |
| `one targeted re-audit` after Phase E, `not a loop until quiet` | re-audit rounds | count round markers in the notes | 1 | yes |
| `never git add .` | staged paths not in your edit set | `git -C $WT diff --cached --name-only` | 9 of 9 authored | yes |

Report `4 of 5 bounds within, 1 disclosed`. Two more bind without being counts: **the never-delegate
list holds** — a mechanical fix may take an executor lane, a diagnosis-hard one may not — and **D′
runs as a fresh agent** receiving only the ticket text, the plan path, the branch name and the mock
index, because a validator holding the build transcript is grading its own premises. **[docs]** At a
seam, prefer the tool call to the question: *"Prefer calling the tool with the available information
over asking the user"*.

## Override 6 — two attempts, then a different move (`## Machine admission`, Phase C)

**[docs]** *"On other errors, you must change your strategy or arguments, not repeat the same failed
call."* **[measured-family]** Both n=1 sessions ran the loop: one invoked a banned, absent tool four
consecutive times with nothing changed between attempts (§1.1.2); the other hit a 25,000-token
`Read` ceiling and retried four times with minor tweaks before pivoting to a Python split (§1.2.3).
Four failures here look transient and are not; each pivots on **attempt 1**. **`governor-run` exit
75** carries `retry_after_sec` — do other work, do not loop the call. **Exit 64** means the
invocation was wrong, usually a weight above the machine's whole capacity. **A plan or spec over the
`Read` ceiling** takes line-ranged reads or a Python split on the first refusal. **A rebase
conflict** is resolved by integrating both sides, never by re-running the rebase. And an **empty
`$HM` is not an error** — proceed unwrapped, say so once, carry on.

## Override 7 — `thinking_level`, and what it is not for

**[docs]** `HIGH` is described as suitable for *"multi-step planning, verified code generation"* —
this stage's whole description. Gemini 3.7 Flash defaults to `MEDIUM`; the uplift here is unmeasured
on this corpus. **[measured-family]** Do not raise it as a remedy for anything above: paired across
106 tasks, `high` beat `medium` on 24, lost on 24 and tied on 58, mean **−1.7 points** (§2.3), and
the bound-shaped share of failures *rose* from 58% to 86%. **[docs]** *"Higher thinking levels
encourage the model to use more tools to explore and verify, so lowering the level can reduce tool
calls."* — the wrong direction for a stage whose error is a table row filled without the exercise.

## Recap

**[docs]** *"Concise repeat of the key points of the prompt, especially the constraints and response
format, at the end of the prompt."*

1. Route `brownfield-integration` and `regression-sensitive` slices — and your own Phase C and E edits — through `lane_pick.py` first.
2. Write the eight-row ledger at Phase A; report `N of N` in the Phase F record. Row 4 can stop the run.
3. Every gate is a pasted command and its output, prerequisite checked before property. Zero is unrun, not pass.
4. Each phase opens the previous phase's file before it starts; the plan is read from disk, never recalled.
5. One capture per mock-index cell, tied to the URL the browser ended up at, no sha256 shared; five bounds read back off git and the diff, not off this file.
