# gemini.md — `ship-feature`

Read this once, then `SKILL.md` and `references/orchestration-model.md`. Each override names the rule it lands on.

`ship-feature` is the riskiest shape in this repo for this family, and not because the engineering is hard: ten stages
under nine headings, each ending in an artifact somebody else reads, and a **fourteen-box** gate in front of the one
irreversible act in the run. Nothing the conductor itself emits is compiled; a merge happens because a checklist reads
green. So the failure to design against is not a worse feature — it is a green box in front of a gate that never ran. This
is the canonical copy; the `diolog-plugins` mirror is left alone, per geminify's one-target-one-file rule.

## Epistemic status

- **Tiers used:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]` — **no Gemini run of `ship-feature` has
  been observed**, at any tier. The `[measured-family]` sources are two single sessions (n=1 each) and a 106-task
  benchmark at two effort levels, all in `geminify/references/evidence.md`; none watched a model conduct a pipeline.
- **Second pass.** `SKILL.md` now names every stage skill in full (`shipyard:triage`, `test-campaign:test-campaign`) where
  it wrote bare names. Override 3 carries that; the rest were re-checked against the current file and stand.
- **The tier the evidence is about.** Every measured rate below was observed on `gemini-3.7-flash` (one session on
  `gemini-3.7-flash-high`) — **flash-tier claims, not to be projected onto the Pro tier**. **[docs]** The defaults drift
  inside the family: "If thinking_level is not specified, Gemini 3 will default to high." against, from the 3.5 Flash
  release notes, "The default thinking effort is now medium, changed from high in Gemini 3 Flash Preview." On Pro these
  overrides stand as `[docs]`-grounded discipline; every `[measured-family]` number is an open question.
- **Unmeasured on this skill:** nothing measures Gemini invoking a stage skill and carrying its artifact forward · nothing
  measures a conductor's judgement seams (blocker vs flake, small remainder vs child spec, weak rung vs `unoracled`) · the
  bound-following rate below was measured on UI assertions, so its transfer to `one branch, one merge` is `[derived]` ·
  and no run has been measured *with* a `gemini.md` against one without.
- **The self-limitation.** **[docs]** A conditional side file is the shape the health checklist warns about: "Avoid
  writing a prompt with non-linear logic or conditionals that require the model to piece together fragmented instructions
  from multiple different places in the prompt." Read it in one pass, up front, never mid-phase.

## Route out before you start: two shapes, two rows

The pipeline's own hands touch code in three places — phase 6's `fix the branch code minimally`, phase 8's rebase conflict
resolution, and phase 4b re-running `work` on a small remainder. Both shapes below are measured far enough behind to hand
out rather than attempt, and the skill already owns the mechanism: its lane table routes executor slices through `defer
--task implementation --shape <shape>`; what this adds is that the conductor's *own* edits go the same way.
**[measured-family]** Only those two — four of eight buckets are level or ahead (§2.1), so routing it all out would be
wrong.

| shape | where it lands in this pipeline | measured |
|---|---|---|
| `brownfield-integration` | phase 4b re-work, phase 5 gap-fix edits, phase 6 bug fixes | 24 against opus's 50 |
| `regression-sensitive` | phase 8's rebase onto fresh `INT` and the post-rebase re-run | 42 against 65 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape brownfield-integration
```

**Two shapes omitted, and why.** `static-page` is not this skill's work — the conductor authors no self-contained page,
and `shipyard:design`'s mocks are that shape on that stage's account. `visual-design` likewise: judging a rendered surface
belongs to `design-review` and `be-my-witness`, and the corpus abstains on judging. **[docs]** "Avoid using prompts that
ask the model to perform a task for which it has a known, fundamental limitation." Conducting is not one of them.

## What transfers intact

Four rules are already written the way this family needs. **`Never skip a stage; never fake a gate`**, with its sharpest
clause — `A gate whose pass and whose could-not-run look identical from the outside has not been run` — is
verification-as-an-instruction already, and the most load-bearing sentence in the file. **`Evidence is what the bundle
holds, not what the note says about it`**, requiring a path and a value read from it, is the grounding rule stated better
than most vendor prose. **Phase 4b's decision tree is a closed set** — A nothing outstanding, B small remainder, C child
spec, `When in doubt, prefer B over C` — which is **[docs]** the multiple-choice remedy exactly: "The response is correct,
but the model didn't stay within the bounds of the options." Phase 7 adds a second closed set on that pattern: `A
requirement marked Unverified — no oracle routes back to phase 6, not to gap-fix`. The overrides give these four
denominators, not new wording.

## The scan

`scan_skill.py` over `SKILL.md` and its three references (470 lines): **21 quota candidates, 3 bound rows, 21 relative
qualifiers, 0 qualitative skill references, 0 shouted passages.** The 21 dedupe to **11** distinct file+phrase rows; I
bound **10** into the ledger and dropped **1** as prose — `rejecting any row that reduces to` at `SKILL.md:147`, which is
`shipyard:verify`'s rule about its own critic, not a scope this conductor enumerates. Two rows the scanner could not see
are added by hand: phase 8's `every box actually checked now` (`box` is not in its vocabulary), the highest-stakes
categorical here, and phase 7's `oracle rung each piece of evidence stands on`.

Modules fired: `gate` (7), `delegation` (7), `visual` (4), `authorship` (3). **`visual` is dropped and not written**: all
four hits are the conductor checking that a *rendering stage* produced its artifact — a mock index, a Playwright suite, a
screenshot `shipyard:verify` proves the subject of. It captures nothing and judges no crop. `bounded-constraint` missed
the trigger threshold but is written by hand from the three bound rows (override 5); `emphasis` did not fire and none is
written — the skill never shouts, which is right for this family.

## Override 1 — the ledger, and the fourteen boxes (`## The phases`, `## Definition of done`)

**[docs]** "Avoid using subjective or relative qualifiers that lack a concrete, measurable definition. Instead, provide
objective constraints (for example, 'write a summary of 3 sentences or less' instead of 'write a brief summary')."
**[measured-family]** Why this is override 1: one run delivered **12 of 12** requirements the brief *enumerated* and
satisfied every requirement named *categorically* with one instance or none — all surfaces → 5, all states → **1**, all
menus → **0**, all flows → **0** (§1.1.1, n=1) — while the skill it followed stated six states *and* an explicit
completeness condition in prose.

Write this into the run's notes before phase 1; report the fractions at phase 8. `Comprehensive` in `e2e-and-finalize.md`
stays a relative qualifier until row 5 carries numbers. Filled against a three-surface feature with two children, as the
exemplar the rest are measured against:

| # | categorical, in the skill's words | denominator | filled | reported |
|---|---|---|---|---|
| 1 | `invoke each stage skill` | 10 stages | 9 invoked, `shipyard:design` n/a: non-UI, reason recorded | `9 of 10, 1 n/a` |
| 2 | `every stage persists its artifact` | 10 paths | 9 exist and are non-empty | `9 of 10` |
| 3 | the oracle `every stage measures against` | 11 criteria from triage | 11 carried into e2e + verify | `11 of 11` |
| 4 | `every row ✅` on reachability + clause | 6 + 14 = 20 rows | 20, each with typed evidence | `20 of 20 typed` |
| 5 | `every user flow, every action, every interaction, and every menu` | 4 flows · 11 actions · 6 menus · 3 surfaces × 5 states | 21 AC rows traced | `21 of 21 AC-traced` |
| 6 | the pre-merge gate, `every box actually checked now` | **14** boxes | 13 green, 1 unrunnable | `13 of 14 — STOP at box 8` |
| 7 | `every finding` across the three review gates | 3 gates, 11 findings | 9 fixed, 2 rejected with a reason | `11 of 11 dispositioned` |
| 8 | re-read at `each phase boundary` | 9 boundaries | 9 re-read from disk | `9 of 9` |
| 9 | `the oracle rung each piece of evidence stands on` | 11 requirements in verify's table | 9 at a strong rung, 2 `unoracled` | `11 of 11 rung-tagged · 2 → 6a` |

A cell that cannot be filled reads `n/a: <reason>` — **[docs]** "provide instructions for handling missing data rather
than assuming inserted data will always be present and well-formed." Row 6 is the one to write first: the only row where
the honest answer `13 of 14` is a **stop** and the plausible answer is a merge. Row 9 is the easiest to fake, a rung being
a word — an `unoracled` case is a requirement returned to phase 6a for an oracle, not a soft pass.

## Override 2 — every box carries its command, its output, and its prerequisite (phase 8)

**[docs]** "Include specific verification steps in either the system instructions or your prompts directly." And "Verify
your claims by quoting the exact applicable information (including policies) when referring to them."

**[measured-family]** What fills the vacuum when verification is left to prose (§1.1.2, n=1): a review asserting a browser
engine as *Engine Verified* when it had failed all four invocation attempts and never ran, and a `100% pass rate on
contrast` from a probe never executed — measured afterwards at 3.65:1 on every primary button and one glyph at 1.00:1,
invisible. Five well-formed `PASS` rows, shape specified and procedure not. A fourteen-box checklist in front of a merge
is that shape with higher stakes, so the gate is a paste, not a tick. Filled, for `DIO-0412` at phase 8:

```
prereq  docs/specs/spec-DIO-0412.md     Developer Review · Progress + Gap-fix notes present
prereq  docs/plans/plan-DIO-0412.md     committed 7c21e0d · 14 of 14 AC boxes reconciled
prereq  design/mocks/DIO-0412/INDEX.md  15 cells, 0 unwaived empty · spec §Verification COMPLETE, lane wire-verified
$ pnpm --dir $WT typecheck && pnpm lint             → tsc 0 errors · eslint 0 problems
$ pnpm --dir $WT exec playwright test e2e/DIO-0412 --repeat-each=2   → 42 passed (2 runs) · 0 flaky
$ pnpm --dir $WT exec playwright test --grep @a11y  → 9 passed · axe violations 0
$ git worktree list | grep -c .worktrees/           → 1
$ git branch --list 'ai/*'                          → ai/dio-0412
box 8   S3 sign-off                                 → n/a: not classified S3 at triage
```

Two rules a paste enforces and a tick cannot. **A denominator of zero is a gate that never ran** — `0 tests passed` and
`no tests found` print differently and mean opposite things, and the skill's own line is that an unrunnable box is `a
blocker, not an implied pass`. **[measured-family]** And check the **prerequisite before the property**: on `COD Dossier`
(§1.2.2, n=1) a deterministic auditor validated tags, citations and contrast floors thoroughly, had no check that its
upstream artifacts existed, and passed two skipped skill invocations with exit code 0 — which is why the `prereq` lines
come first. **[docs]** For the arithmetic: "Gemini's code execution tool enables the model to generate and run Python
code, and should be enabled whenever the model needs to perform any kind of arithmetic, counting, or calculation." Take
the runner's number; never total tests in prose.

## Override 3 — the stage is the invocation, its full name, and its artifact (`orchestration-model.md` §1, §3)

The scan's `0 qualitative skill references` is what makes this necessary, not unnecessary. **[measured-family]** §1.2.1
(n=1): a skill instructed that every design decision `goes through` two named skills, and the run invoked neither — its
own diagnosis being that the rules were already in context and nothing downstream depended on a file only those skills
produce. `ship-feature` creates that condition **by design**: `Its SKILL.md loads into your context, you execute it`. A
conductor that has read `shipyard:plan`'s rules can write a plausible plan inline, and the pipeline looks like it ran.
Corroborated outside this repo (§7.2): Antigravity subagents ignoring instructed skills, and a Gemini 3 **Pro** transcript
reclassifying a `GEMINI.md` rule as guidance — so it binds on every tier.

**[docs]** The remedy is the chain: "make each step a prompt and chain the prompts together in a sequence." Forced
execution exists natively — **[docs]** "any: Model is constrained to always predict a function call." — but a skill file
cannot set it, so the artifact dependency is the lever. Every stage is a real `Skill(...)` call under the full
`plugin:skill` name the SKILL.md now uses, whose completion is a **path** the next phase opens before it starts:

```
0. Skill(shipyard:intake)             → docs/features-to-triage/<slug>.md   phase 1 reads the brief
1. Skill(shipyard:triage)             → docs/specs/spec-<ID>.md             phase 2 reads it, or does not start
2. Skill(shipyard:plan)               → docs/plans/plan-<ID>.md (sha)       ┐ parallel; phase 4 reads both
   Skill(shipyard:design)             → design/mocks/<ID>/INDEX.md          ┘
3. Skill(shipyard:work)               → ## Progress on the spec             phase 4b classifies from this file
4. Skill(shipyard:gap-fix)            → ## Gap-fix on the spec              phase 6 reads spec + children
5. Skill(test-campaign:test-campaign) → apps/web/e2e + AC matrix + unoracled list   phase 7 cites it
6. Task(shipyard:verify)              → per-requirement verdict + oracle rung       phase 8 box 6 reads it
```

**Two names the SKILL.md still leaves bare, and they are yours to resolve before the call:** phase 7's `Spawn the verify
stage` is `shipyard:verify`; phase 6's `otherwise acceptance-e2e` is `acceptance-e2e:acceptance-e2e`. Resolve both against
the installed skill list rather than guessing a prefix, and if one does not load, say so in the sentence where it fails —
a silent `Unknown skill` reads downstream exactly like a stage that ran.

A missing artifact means the stage did not run, whatever the transcript says — the skill's own rule 2, `The pipeline's
memory is on disk`, promoted into the thing that decides whether a phase may begin. The same ordering governs files named
to *you*: read, then answer. **[measured-family]** §1.2.4 recorded both halves failing in one session — a question naming
three skills answered from memory without loading any, then a skill launched instead of an answer.

## Override 4 — two attempts, then a different move (`## Machine admission`, phase 8)

**[docs]** "On other errors, you must change your strategy or arguments, not repeat the same failed call."
**[measured-family]** Both n=1 sessions ran the loop: one invoked a banned, absent tool four consecutive times unchanged
(§1.1.2); the other hit a 25,000-token `Read` ceiling and retried four times before pivoting to a Python split (§1.2.3).

Four failures here look transient and are not; each pivots on **attempt 1**. **`governor-run` exit 75** is scheduling
information carrying `retry_after_sec` — do other work, do not loop, do not report the item blocked. **Exit 64** means the
invocation was wrong, usually a weight above the machine's capacity; an identical second call fails identically. **A spec
over the `Read` ceiling** takes line-ranged reads on the first refusal. **A rebase conflict** integrates both sides. And
**an empty `$HM` is not an error** — proceed unwrapped, say so once.

## Override 5 — cap the spawns; never grade your own pipeline (`## Hard rules`)

`SKILL.md` states the cap plainly: `you spawn only what this file names (the verify agent, the parallel design/plan
invocations)`. **[measured-family]** A stated maximum is the shape this family exceeds rather than forgets: classifying
every failing UI assertion by whether it states a bound or asks for a thing, **58%** of Gemini's failures at `medium` and
**86%** at `high` were bound-shaped, against 8% for opus and 6% for the OpenAI lane; one rule failed on *every* instance
in its set on a run that passed 37 of 39 other assertions (§2.2). A bound is violated by what you did not write, so it
survives every check that looks at what you did.

**[docs]** Google treats these as a component in their own right — "Restrictions on what the model must adhere to when
generating a response, including what the model can and can't do." — and asks that "all requirements, constraints,
options, and preferences are exhaustively incorporated into your plan." So read the caps back off what you did. Of the
three bounds the scan found, two are prose (a frontmatter scope exclusion, a weight legend) and the third is the skill's
central invariant, joined by two prohibitions moved across by hand:

| bound, in the skill's words | countable property | readback | observed | within? |
|---|---|---|---|---|
| `you spawn only what this file names` | agents the conductor spawned | count this run's Task calls | 1 (verify) | yes |
| `exactly one` feature branch from phase 5 | `ai/*` branches · worktrees | `git branch --list 'ai/*'` · `git worktree list` | 1 · 1 | yes |
| `three failed rounds parks the item` | verify → gap-fix rounds | count verdict comments on the spec | 2 | yes |

Report `3 of 3 bounds within`. Two more bind without being counts: **`shipyard:verify` runs as a fresh agent** — `its
value is exactly that it does not share your context` — so grading your own pipeline inline deletes the run's only
independent reading; and **the conducting is never delegated**, since a subagent handed a stage returns a summary and
loses the thread. **[docs]** At a seam, prefer the tool call — "Prefer calling the tool with the available information
over asking the user" — and where a fork is open, keep it open: "Avoid premature conclusions: There may be multiple
relevant options for a given situation."

## Override 6 — the report may not exceed the artifacts (`## Hard rules`)

Everything emitted at the close is prose a human acts on: the merge note, the blocker list, the `Dropped or changed vs
spec/plan` disclosure, the `Open follow-ups at merge` list, the Reviewing-models line, the S3 acknowledgement. **[docs]**
Google's strictly-grounded system instruction is meant to be used verbatim, and its last clause binds here: "If the exact
answer is not explicitly written in the context, you must state that the information is not available." A missing verdict
is unavailable, never a pass; an unlogged downgrade is a skip; and the wire-verified model id is what goes in the report,
not the requested one — **[docs]** "Your knowledge cutoff date is January 2025." `Never fabricate an answer to an
Essential Question` is this clause already; the addition is that it covers the closing report.

## Override 7 — `thinking_level`, and what it is not for

**[docs]** `HIGH` is described as suitable for "multi-step planning, verified code generation, or advanced function
calling scenarios." Conducting ten stages to an irreversible merge is that work, and Gemini 3.7 Flash defaults to
`MEDIUM`; the uplift is unmeasured on this corpus. **[measured-family]** Do not raise it as a remedy for anything above:
paired across 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on 58, mean **−1.7 points** (§2.3), and the
bound-shaped share of failures *rose* from 58% to 86%. **[docs]** "Higher thinking levels encourage the model to use more
tools to explore and verify, so lowering the level can reduce tool calls." — fewer tool calls is the wrong direction for a
conductor whose characteristic error is ticking a box it did not run.

## Recap

**[docs]** "Concise repeat of the key points of the prompt, especially the constraints and response format, at the end of
the prompt."

1. Write the nine-row ledger before phase 1; report `N of N` at phase 8. Row 6 is fourteen boxes; row 9 is oracle rungs.
2. Every box is a pasted command and its output, prerequisite before property; a zero denominator is unrun, an
   unrunnable box a stop.
3. Every stage is a real invocation under its full `plugin:skill` name, whose completion is a path the next phase opens.
4. One retry on a transient error; none on exit 75, exit 64, a read ceiling or a rebase conflict.
5. One verify agent, one branch, one worktree, three rounds — read back off git, not off this file.
6. The closing report states as unavailable whatever the artifacts do not carry.
