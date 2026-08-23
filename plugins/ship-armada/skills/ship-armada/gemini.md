# ship-armada, calibrated for Gemini

Read this once, before *Startup protocol*; each override names the section it lands on. `ship-armada`
is a conductor — nothing it emits is compiled, and everything it emits is acted on by something else.
So the risk is not a worse plan. It is a freshness check run on 3 of 70 index rows, a project ticked
on the dispatch return, and a state change that happened in the session but never in `ARMADA.md` —
*a directive that was routed but never recorded in the manifest and changelog did not happen*.

## Route out before you build — one branch of Dispatch, and nothing else

Four of the five modes are work the benchmark abstains on — Survey reports, Plan proposes, Route
hands over, Daemon re-surveys, all `referral`, `completeness` and `verification` shapes, where
`lane_pick.py` returns the policy answer unchanged. **One branch is different:** Dispatch's *a direct
worktree edit + `code-review` gate for mechanical changes (e.g. a model-ID swap) that need no spec
pipeline* is this skill writing code, in an existing multi-file repo, under a passing contract.

| shape | where it lands | measured (`evidence.md` §2.1–2.3) |
|---|---|---|
| `brownfield-integration` | the direct worktree edit in Dispatch | 16.1 against opus's 46.4; hard zero on 79% of decided rows |
| `regression-sensitive` | a cross-project rollout that must not break a passing suite | 42 against 65 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape brownfield-integration
```

Omitted deliberately: `static-page` (this skill authors markdown — briefs, entries, campaign rows —
never a self-contained page) and `visual-design` (it renders nothing). **[docs]** "Avoid using prompts
that ask the model to perform a task for which it has a known, fundamental limitation." Conducting is
not one of them, and where no lane is available this block says which paragraph of the report to
distrust.

## Epistemic status

| Tier | Used here | Source |
|---|---|---|
| `[docs]` | throughout; most of this file rests on it | Google's published guidance, verbatim from `geminify/references/gemini-corpus.md` |
| `[measured-family]` | two n=1 sessions + a 106-task corpus | Gemini runs of *other* skills; `geminify/references/evidence.md` |
| `[measured-here]` | measurements of text and files, **not of a run** | 23 Aug 2026 — `scan_skill.py` on this SKILL.md + `references/manifest.md`: 155 lines, **2** quota rows, **2** bound rows, 12 relative qualifiers, **0** qualitative skill references, 2 emphasis tokens, **1** module at three triggers. `~/Dev/ARMADA.md`: 1,057 lines, ≈93k tokens, **70** index rows, **71** `###` entries |
| `[derived]` | marked where used | my reasoning from the two above |

**The tier the evidence is about.** Every measured rate here is flash-tier — `gemini-3.7-flash` across
106 benchmark tasks plus two flash sessions — and none is measured on the Pro tier or should be
projected there: on Pro these overrides stand as `[docs]`-grounded discipline while every
`[measured-family]` number is open. **[docs]** Defaults drift inside the family too, from the 3.5 Flash
release notes: "The default thinking effort is now medium, changed from high in Gemini 3 Flash Preview."

**Unmeasured on this skill:** no Gemini run of `ship-armada` at any tier · no comparison between a run
with this file and one without · **neither source watched a model coordinate other agents** · the
bound-failure rates below were measured on rendered-UI assertions, so their transfer to `at most 3
projects concurrently` is `[derived]` · the bench tasks are single-shot, so whether this family
*holds* a cap across a multi-hour dispatch is untested. **[docs]** And a conditional side-file is
itself the shape the checklist warns about — "Avoid writing a prompt with non-linear logic or
conditionals that require the model to piece together fragmented instructions from multiple different
places in the prompt." Read it in one pass.

## What transferred intact

- **The concurrency rails are already numbers** — *at most 3 projects concurrently*, *one fleet per
  repo*, *one armada session at a time*. **[measured-family]** `evidence.md` §2.1: on the optimality
  bucket, where the brief states a numeric bound, Gemini scored 74.7 against opus's 75.0, while the
  prose-shaped buckets produced hard zeros on 71% and 79% of decided rows.
- **The completion gate is already a script with an exit code**, and the skill already says *Read its
  output rather than re-deriving the check by hand*. Override 2 only says where that output goes.
- **The modes are already a closed set**, with *state which you're in* — **[docs]** Google's remedy
  for an answer landing outside the offered options: "you can rephrase the instructions as a multiple
  choice question and ask the model to choose an option." Not blocking on a question is the rule too:
  **[docs]** "For exploratory tasks (like searches), missing *optional* parameters is a LOW risk."
- **It does not shout, and composition is already executable.** The two emphasis tokens are `EVERY`
  in the description and the anti-pattern quoted at :103; the scan found **0** qualitative skill
  references, because Route step 3 invokes `intake` and names the directory it writes to — with one
  exception, in Override 3.

## The quota ledger — two scanned rows, one moved in by hand

**[measured-here]** Both scanned rows name countable deliverables, so **none was dropped as prose**;
the scan missed the one that matters most, because its vocabulary does not cover *each index row*.
**[measured-family]** Why they become a table rather than sentences: on the observed run every
enumerated requirement shipped (twelve named features, all present) while every categorical one shipped
once or not at all — *all states* → 1, *all menus* → 0, *all flows* → 0. **[derived]** Here that is a
freshness check run over the three repos in front of you and reported as covering the portfolio. Ship
it filled, `n/a: <reason>` where the skill's own rule excuses a cell:

| Scope, and where the skill states it | Denominator | Filled | Delivery line |
|---|---|---|---|
| **each index row's `updated` stamp** — :25 | **70** index rows in the live file | 70 compared against `git log -1 --format=%cs` | `70/70 rows compared, 9 stale` |
| stale entries refreshed — :26 | the 9 stale rows | 3 refreshed; 6 `n/a: not touched this session`, named in the report | `3 refreshed, 6 named unrefreshed` |
| **each finding** mapped to projects — :92 | 4 radar findings this tick | 3 mapped to named projects, 1 dropped | `4/4 mapped, 1 dropped (names no project)` |
| **every state change** written to `ARMADA.md` — :111 | 6 state changes this session | 6 written | `6/6 in the manifest, 6 changelog lines` |
| **[derived]** completion receipt per dispatched project — :108 | 3 projects in the campaign | 3 exit codes pasted | `3/3 receipts, exit 0 / 0 / 1` |

Row 1 is a loop, not a reading: parse `project` and `updated` out of each index row, run `git -C
~/Dev/<p> log -1 --format=%cs`, print `STALE` where the commit date is newer, `tee` the result.
**[docs]** Code execution "should be enabled whenever the model needs to perform any kind of
arithmetic, counting, or calculation."

## The bound ledger — the direction this family fails in

**[measured-here]** The scan returned two bound rows — *at most 3* at :70, *a single row* at :48 — and
`bounded-constraint` fired at 2 of 3 triggers, so it is not written as a module. Four more move in by
hand from the prose prohibitions the scan counted but did not list. **[measured-family]** They earn a
readback because this is the direction this family fails in: `evidence.md` §2.2 — 58% of failing
assertions at `medium` and 86% at `high` stated a **bound**, against 8% for opus, and the
most-repeated one failed on *every* instance in its set on a run that passed 37 of its 39 other
assertions. The rule was read and agreed with; a default idiom supplied the value underneath it, so
this ships a command rather than a firmer sentence. **[docs]** The **Recap** is where constraints go:
a "Concise repeat of the key points of the prompt, especially the constraints and response format, at
the end of the prompt."

| Bound, and where stated | Readback | Observed | Within? |
|---|---|---|---|
| concurrent projects **≤ 3** — :70 | count repos with a live `ai/*` worktree across the dispatched set | 3 | at cap |
| fleets per repo = **1** — :70, :107 | the same listing, grouped by repo | 1 · 1 · 1 | yes |
| tiers per campaign row = **1** — :48 | tier of each project in the row, against the bound-directory list at :37 | 2 rows, 1 tier each | yes |
| manifest entry **≤ 20 lines** — manifest.md:24 | `awk '/^### <p> /,/^### [^<]/' ~/Dev/ARMADA.md \| wc -l` | 12 | yes |
| AI/tech opportunities **≤ 4** — manifest.md:37 | count `;` + 1 in the field | 3 | yes |
| changelog lines per routed directive = **1** — :68 | added lines under `## Changelog` in the diff | 1 | yes |

**[derived]** Why the readback beats describing it: `ARMADA.md` carries **71** `###` entries against
**70** index rows — `finance-swift` has an entry and no row, and no instrument reads that back.

## Override 1 — the manifest does not fit in one `Read` (Startup 1–2)

**[measured-here]** `~/Dev/ARMADA.md` is 1,057 lines and ≈93k tokens, roughly 3.7× the harness
ceiling; a plain `Read` returns `File content exceeds maximum allowed tokens (25000)` and nothing
else. **[measured-family]** `evidence.md` §1.2.3: the session that hit this exact ceiling retried
`Read` **four consecutive times** with minor parameter tweaks before pivoting to a Python split.
**[docs]** "On *other* errors, you must change your strategy or arguments, not repeat the same failed
call." A capacity ceiling pivots on attempt **1**.

Startup step 1 already prescribes the fix — *the index table first; load full entries only for
projects you will touch this session* — so execute it as addressing rather than reading:
`sed -n '/^## Index/,/^## Projects/p'` for the index, `grep -n '^### <project>'` then a line-ranged
`sed` per entry, `tail -20` for the changelog shape. Two attempts per tool otherwise; a permanent
error — `command not found`, no git repo, no commits since the stamp — gets one, and the answer is a
report line rather than a third attempt. **[docs]** A sweep across 70 repos has a vendor form worth
borrowing verbatim: "You have a limited action budget of <n> tool calls. Use them efficiently."

## Override 2 — the completion check ships a receipt (Safety rails, Dispatch)

**[docs]** "Include specific verification steps in either the system instructions or your prompts
directly", and "Verify your claims by quoting the exact applicable information (including policies)
when referring to them." **[derived]** Skills here are written for a model that over-verifies, so
verification scaffolding is stripped on purpose; inheriting that removal is the defect. This skill
already owns the instrument — it just does not say that the instrument's *output* is the deliverable.
**[measured-family]** What fills the vacuum is well-formed and false: a run's own review asserted a
browser engine that had failed all four invocation attempts and never ran, and a *100% pass rate on
contrast* from a probe never executed, measured afterwards at 3.65:1 on every primary button; and
`evidence.md` §1.2.2 is the closer parallel — an auditor that checked the deliverable thoroughly but
never whether an upstream pass had run, so a skipped step cleared the gate at exit 0. So every project
ticked carries `check_completion.sh <repo>`'s pasted output **and** its exit code, because *a project
is complete when its ledger says so, never when its dispatch returns*. A denominator of zero is a gate
that never ran; `Done` needs the cross-family verdict as well as the exit code, or the row reads
`merged (unverified)`; and where the script could not run, name the axis the project is unchecked on.

## Override 3 — Route is a chain; keep every step's artifact (Route 1–5, Startup 3)

**[docs]** The remedy for a pass carrying several distinct cognitive actions is the chain — "make
each step a prompt and chain the prompts together in a sequence", where "the output of one prompt in
the sequence becomes the input of the next prompt." Route already is that chain, and each step names
a file: research → `docs/deep-research/<slug>.md` → `intake` → `docs/features-to-triage/*.md` → the
`ORCHESTRATOR.md` ledger line → the `ARMADA.md` entry and changelog. Keep it literal, in that order,
each phase reading the previous file rather than the conversation. **[measured-family]**
`evidence.md` §1.2.1: a run skipped two skill invocations phrased as a lens or a standard, and its
own diagnosis named the mechanism — the next step did not mechanically depend on a file only those
skills produce. Startup step 3 carries the same phrasing, refreshing stale entries *using the
`armada-sync` protocol*, so convert it:

```javascript
await Skill({ skill: "armada-sync:armada-sync" })   // per entry → rewrites the ### section + index row
// then re-run the freshness loop; the refreshed rows must now compare clean. That re-run is the
// dependency: without it "refreshed" is a claim; with it, the quota ledger's row 2 has a numerator.
```

## Override 4 — the radar is fetched, and a named file is read before it is answered about

**[docs]** "Your knowledge cutoff date is January 2025", and Google's clause for time-sensitive work
is blunt: "Remember it is 2026 this year." **[measured-family]** The informative failure on the
observed run was not a guess but Windows 10's published accent colour written onto a Windows 11 app.
**[derived]** Upgrade radar is that hazard exactly — model IDs, deprecations and prompting guidance
are the class of fact this family supplies from memory — and the skill already says to *check what's
newly possible before assuming the manifest's opportunities are current*. Fetch all three URLs, quote
the line each finding rests on, date the check in the campaign row.

**The same rule covers files the directive names.** **[measured-family]** `evidence.md` §1.2.4: asked
a question naming three skills, the run answered from memory without loading any, then inverted the
error and launched a skill when an answer was wanted. Read-then-answer is two ordered steps, neither
substituting for the other — so in Route step 1, a directive naming a project is a directive to load
that project's `ARMADA.md` entry, `CLAUDE.md` and `ORCHESTRATOR.md` *before* the brief is written.
Matching on the index row alone is how a brief lands in the wrong repo with an assumption inside it.

## Module `delegation` — the only module the scan earned

Fired at 6 triggers (`subagent`, `fan-out`, `fan out`, `spawn`, `orchestrat`, `runner`).

- **Cap the spawn by enumeration.** Startup step 3 fans out *one entry each, in parallel via
  subagents when there are several*, and the rebuild fans out *one reviewer per repo* over a 70-repo
  portfolio. Write the list of names before spawning; the list is the cap.
- **Never delegate a check of your own output.** The skill holds this twice — *Never hand the
  portfolio orchestration itself to a subagent*, and under `tiered`, *Verification is yours, not the
  fleet's*. **[docs]** "Inhibit your response: only take an action after all the above reasoning is
  completed. Once you've taken an action, you cannot take it back."
- **Resolve the vehicle as a closed set and write the choice down.** *Choose the smallest sufficient
  vehicle* is a relative qualifier, and **[docs]** the remedy is objective constraints: "Avoid using
  subjective or relative qualifiers that lack a concrete, measurable definition." Use the count — 1
  open item → `ship-feature`; ≥2 → `ship-fleet`; a mechanical change needing no spec pipeline →
  worktree edit + `code-review`, which reads the route-out block first. Record which, before dispatch.

## One worked example, before the set

**[docs]** "We recommend to always include few-shot examples in your prompts", and the checklist asks
for the structure to be shown rather than described. The skill specifies a campaign's *fields* and
shows no instance, so fill one row and its delivery block before the batch:

```
| C7 | opus-5 model-ID sweep (bound tier) | dossier · atlas · diolog-web | running | worktree edit +
  code-review (mechanical, 1 file each) · brownfield-integration → lane_pick.py, glm@high · radar
  checked 2026-08-23 against migration-guide.md · verify retained by armada |

ARMADA DISPATCH — C7
  freshness  70/70 index rows compared, 9 stale, 3 refreshed, 6 named   (/tmp/armada-freshness.txt)
  bounds     6/6 within: 3 concurrent, 1 fleet/repo, 1 tier/row, entries 12 lines
  receipts   dossier exit 0 · atlas exit 0 · diolog-web exit 1 (2 open rows, 1 unmerged ai/* branch)
  verdicts   2 Done with cross-family verdicts · 1 merged (unverified)
  manifest   3 entries updated, 3 index rows, 4 changelog lines
```

**[docs]** "Make sure that the structure and formatting of few-shot examples are the same to avoid
responses with undesired formats" — later rows keep that field order, and a campaign spanning both
tiers is two rows, per :48.

## `thinking_level`, and the modules not written

**[docs]** `HIGH` is "suitable for complex prompts requiring deep reasoning, such as multi-step
planning, verified code generation, or advanced function calling scenarios", and Gemini 3.7 Flash
defaults to `MEDIUM`. **[derived]** Plan and Dispatch — dependency-ordered campaigns across a 70-repo
portfolio — are that description almost exactly, so name `HIGH` there and treat the uplift as
unmeasured; Survey and the daemon tick are lookup-shaped and the default suits them.
**[measured-family]** It is a remedy for nothing above: paired across the 106 tasks, `high` beat
`medium` on 24, lost on 24 and tied on 58, mean −1.7 points, and the bound-shaped share of failures
went *up*, 58% → 86%. **[docs]** It also couples to tool volume — "Higher thinking levels encourage
the model to use more tools to explore and verify, so lowering the level can reduce tool calls" —
worth knowing before a 70-repo sweep, not a reason to lower it under the loop.

**[measured-here]** Eight modules did not fire, and the skill earns that: it renders nothing
(`visual`), enumerates no unhappy paths (`states`), cites no vendor design values (`platform-values`,
1 trigger), ingests nothing it did not author (`injection`, 1 trigger), and writes no prose a reader
acts on unmediated (`authorship`, 1 trigger — every claim lands in a file another skill re-reads).
Three near-misses at 2 of 3 sit in the core instead: `gate` (`scripts/check_completion.sh`) is
Override 2, `bounded-constraint` is the bound ledger, and `count-contract` folds into the quota
ledger, whose denominators the manifest supplies.
