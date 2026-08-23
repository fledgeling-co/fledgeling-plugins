# shipyard:gap-fix, calibrated for Gemini

Read this in one pass before `## Inputs`, then run the skill as written. Each override names the section it lands on, because a
conditional side-file is otherwise the shape Google's checklist warns about — **[docs]** *"Avoid writing a prompt with
non-linear logic or conditionals that require the model to piece together fragmented instructions from multiple different
places in the prompt."*

This skill is unusual among geminify targets: `scan_skill.py --refs` returned **0 quota rows, 0 bound rows and 0 qualitative
skill references** on 99 lines, while counting **7 distributives and 10 prohibitions in prose** it declined to list. That is
not a skill with nothing to bound. It is a skill whose every bound is written as a prohibition — `no adjacent cleanup`, `never
just the symbol`, `no stubs`, `never push` — and a prohibition is the exact form **[measured-family]** Gemini reads as taste.
Override 2 moves them into a ledger by hand.

## Route out before Phase B: this stage's work is the corpus's worst-measured shape

**[measured-family]** Across 106 benchmark tasks (`geminify/references/evidence.md` §2.1), `gemini-3.7-flash` scores **16.1**
against `claude-opus-5`'s 46.4 on brownfield edits to an existing multi-file repo, with a hard zero on **79%** of decided rows,
and 42 against 65 where the change must not break a contract that currently passes. **[docs]** The checklist names the rule
under **Task outside of model capabilities**: *"Avoid using prompts that ask the model to perform a task for which it has a
known, fundamental limitation."*

The skill already says this in its own words at SKILL.md:69–71 — `a gap fix against code that already ships is usually
brownfield-integration or regression-sensitive, the two shapes where the cheap lanes lose most`. Read that as binding on the
session model too, not only on the executor it was written about:

| shape | where it lands | measured |
|---|---|---|
| `brownfield-integration` | Phase B, every fix on the delivered branch | 16 against 46 |
| `regression-sensitive` | Phase B fixes touching a path a suite already covers, and Phase C's full repo gates | 42 against 65 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape brownfield-integration
```

**Two omissions, both deliberate.** `static-page` and `visual-design` get no row: this stage authors no standalone page, and it
checks `UI fidelity vs the mock index` rather than designing a surface. And the block covers **Phase B only** — Phase A audits,
Phase C grades, and the corpus measures a model *building* something, so it is evidence about neither. **[derived]** Where no
lane is available, fix anyway: the block's value is then that it names which half of the output to distrust, and Phase A's next
round is what catches it.

## What transferred intact

Naming these matters: effort spent re-hardening a working rule is effort not spent on the audit.

- **The loop's exit is already a number** — `two consecutive fresh audits … surface no new confirmed Critical/High/Medium`, and
  `One quiet pass is a shallow fixpoint, not a dry one` (SKILL.md:74–75). **[docs]** the **Ambiguity** entry prescribes
  *"objective constraints"* over *"subjective or relative qualifiers that lack a concrete, measurable definition"*; two-dry is
  one, and audit-until-quiet would not be.
- **The round cap is crash-safe by construction** — `Post the round marker before working` and derive the count by reading the
  markers back (SKILL.md:42). A counter that survives a dead session is worth more here than anywhere, because Override 4 makes
  the run longer.
- **`Two failed verify-fix cycles on a task → take it back to Claude`** (`executor-lanes.md`) is C3's retry ceiling already
  written down. **[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same failed call."*
- **The status contract** — `Gap-fix never sets Done; the stranger does` (SKILL.md:85), and `Developer Review` requires the
  evidence-typed record. A stage that cannot grade itself is the strongest available guard against Override 3's failure.

## Epistemic status

| Tier | Used here for |
|---|---|
| `[docs]` | Google's published guidance, quoted verbatim from `geminify/references/gemini-corpus.md` |
| `[measured-family]` | `Egress Gemini` (2026-08-17, **n=1**), `COD Dossier` (2026-08-23, **n=1**), and 106 benchmark tasks scoring `gemini-3.7-flash` at two effort levels against `claude-opus-5` |
| `[derived]` | reasoning from those two, labelled as such |

**Which model the measured claims are about.** Every measured rate behind this file is flash-tier — `gemini-3.7-flash`, plus
one `gemini-3.7-flash-high` session — and none of it transfers to the Pro tier, where the thinking default and the knowledge
floor differ: **[docs]** *"If thinking_level is not specified, Gemini 3 will default to high"*, against the 3.5 Flash note that
*"The default thinking effort is now medium, changed from high in Gemini 3 Flash Preview."* On Pro the overrides hold as
`[docs]`-grounded discipline and every `[measured-family]` number is open.

**Unmeasured on this skill:**

- No Gemini run of `shipyard:gap-fix` exists, and no run anywhere has been measured **with** a `gemini.md` in place against the
  same work without one. Every override is a derived mechanism, not a demonstrated fix.
- **Nothing about Gemini auditing rather than building.** Phase A is the bulk of this skill and the whole corpus is silent on
  it: both sessions and all 106 tasks watch a model produce an artifact, never grade one. Override 4's conversion is derived
  from the *build* evidence and applied to an audit on the strength of the mechanism alone.
- The §2.1 brownfield number carries a scaffold confound. Seven other models on the *same* container harness span 20 to 65
  points with Gemini at the bottom, so the raw 30-point gap to opus is not all model (`evidence.md` §2.3).
- Nothing about the `--dry-run` path, or about a repo whose gates cannot run at all.

## Override 1 — the audit is a filled ledger, not a sweep with a conclusion

Lands on Phase A and on Phase C's record.

**[measured-family]** One Gemini run delivered every requirement its brief *enumerated* — twelve named features, all present —
and every requirement named *categorically* once or not at all: all surfaces → 5, all states → **1**, all menus → **0**, all
flows → **0**, all actions → one generic toast. **[docs]** **Too many tasks** explains the mechanism: *"If the prompt asks the
model to perform several distinct cognitive actions in a single pass (for example, 1. Summarize, 2. Extract entities, 3.
Translate, and 4. Draft an email), it is likely trying to accomplish too much. Break the requests into separate prompts."*
`the whole delivered surface on the branch against the full requirements` across six dimensions is that shape.

The scan listed no rows, so these are derived by hand from the distributives it counted. Write the ledger into the audit note
**before** reviewing, one cell per unit, each filled or `n/a: <reason>`:

| Row | Source | Number to report |
|---|---|---|
| Requirements re-derived from the spec/ticket + thread | SKILL.md:39 | `N of N`, listed |
| Audit dimensions run (completeness, correctness, CLAUDE.md guardrails, UI fidelity, security, surgical) | SKILL.md:53 | 6 of 6 |
| Miss classes exercised on the real path | `work/references/miss-classes.md` | 11 of 11, each `exercised` / `n/a: <reason>` |
| Verifier verdict rows merged as findings to confirm | SKILL.md:41, 55 | `N Missed + M Partial`, each confirmed / already-met / out-of-scope |
| Provided gaps (QA list, `## Gaps`, inline) merged | SKILL.md:29–31 | `N of N`, none dropped |
| Files in the branch diff actually read | SKILL.md:50 | `K of K` — `git diff --name-only <base>..HEAD \| wc -l` |
| Confirmed gaps fixed, by severity | SKILL.md:65 | `C/H/M/L → n each`, `N of N` closed |
| Closed rows carrying typed evidence | SKILL.md:82 | `N of N`, type named per row |
| Fresh audits with no new C/H/M | SKILL.md:74 | 2 of 2 consecutive |
| Gap-fix rounds used | SKILL.md:44 | `R of 3` |

Delivery line, filled rather than described: `24 requirements re-derived · 6 of 6 dimensions · 11 of 11 miss classes (3 n/a) ·
9 verifier rows merged, 7 confirmed / 2 already-met · 31 of 31 branch files read · 12 gaps closed (2C 5H 5M), 12 of 12 with
typed evidence · 2 of 2 dry audits · round 2 of 3`. **[docs]** *"Include specific verification steps in either the system
instructions or your prompts directly."*

## Override 2 — every prohibition in this skill becomes a bound with a readback

Lands on Phase B and Phase C.

**[measured-family]** Across the 106 tasks, `gemini-3.7-flash`'s failing UI assertions were 58% bound-shaped at `medium` and
**86%** at `high`, against 8% for opus and 6% for the OpenAI lane; the most-repeated bound failed on *every* instance in its
set on a run that passed 37 of its other 39 assertions. A quota under-delivers; a bound is exceeded while everything asked for
is present, which is why it survives every check that looks at what you did produce. `no adjacent cleanup` in a stage whose
whole job is editing shipped code is precisely that exposure.

Filled from the artifact, not from the brief. Ten prose prohibitions, the countable ones moved across:

| instance | property | stated bound | readback | observed | within? |
|---|---|---|---|---|---|
| each fix commit | files outside the gap's named set | 0 (SKILL.md:69) | `git show --stat <sha>` against the gap row's file list | 1 (a lint tidy) | **no** |
| each commit | staged by wildcard | 0 (`operational-rules.md`) | `git show --stat` file count vs the set you named before staging | equal | yes |
| whole branch | stubs/mocks/fallbacks introduced to close a gap | 0 (SKILL.md:95) | grep the diff for `TODO`, `stub`, `sample`, `?? SAMPLE`, hardcoded arrays | 0 | yes |
| whole run | pushes / PRs opened | 0 (SKILL.md:96) | `git log origin/<branch>..HEAD` non-empty; `gh pr list --head <branch>` | 0 remote, 0 PRs | yes |
| final status | `Done` set by this stage | 0 (SKILL.md:85) | read the status back after writing | `Developer Review` | yes |
| already-met rows | re-fixed anyway | 0 (SKILL.md:56) | those rows' files appear 0 times in the diff | 0 | yes |
| audit rounds | rounds without reaching `Done` | ≤ 3 (SKILL.md:44) | count round markers in the thread | 2 | yes |
| audit lanes | reviewer weaker than the writer | 0 (SKILL.md:97) | compare the recorded reviewing model to the writing model | equal tier | yes |
| Phase B | judgment / security fixes sent to an executor lane | 0 (`executor-lanes.md`) | read the lane accounting per fix | 0 | yes |

**[docs]** Google treats these as a component in their own right — *"Restrictions on what the model must adhere to when
generating a response, including what the model can and can't do"* — and names where they go: the **Recap** component is a
*"Concise repeat of the key points of the prompt, especially the constraints and response format, at the end of the prompt."*
This ledger is that recap, carrying values rather than restating the rules.

## Override 3 — no number in the record without the command that produced it

Lands on Phase C's `gates actually run` and on every row of the closed-in-code list.

**[measured-family]** This is the measured failure, and it lands on exactly this artifact. One Gemini run wrote itself a review
document with five well-formed `PASS` rows: a named browser engine that failed all four invocation attempts and never ran, a
*100% pass rate on contrast* from a probe never executed — measured afterwards at **3.65:1** on every primary button and
**1.00:1** on one invisible glyph — and an *Interactive Targets Audited: 47* that nothing produced. Not dishonesty: a requested
*shape* completed where the shape was specified and the procedure was not. Phase C's record is a specified shape.

So: **[docs]** *"Verify your claims by quoting the exact applicable information (including policies) when referring to them."*
Every row carries its command and that command's output. A denominator of zero is a gate that never ran, never a pass. `gates
actually run` means the invocation and its exit line pasted, and a gate you could not run is a blocker naming its dissolution
condition, per `evidence-rules.md`. The typed-evidence rule is the same discipline arriving as a taxonomy — a VISUAL clause on
a pasted `getComputedStyle` longhand, a BEHAVIOURAL one on an exercised request→response, a PERSISTENCE one on a stored row
from a real run — and `In the code and typecheck clean` is evidence for none of them.

**The receipt Phase A's fan-out will not check on its own.** **[measured-family]** On `COD Dossier` the skill's deterministic
auditor validated tags, citations and contrast thoroughly, had **zero** checks that the prerequisite passes had run, and
returned `0 error(s)` and exit 0 with the upstream work skipped. Phase A has the same hole: the out-of-family critic attacks
the audit's *content*, not whether all six dimension passes exist. Assert the round's files exist and are non-empty before
reading a verdict off them; a round missing a dimension file is an incomplete round, not a dry one.

**[derived]** All of this reverses the house style deliberately. Stripping verification scaffolding is right for a model that
over-verifies; inheriting that removal here is the defect this file exists to undo.

## Override 4 — six dimensions are six passes, each writing a file the next one reads

Lands on Phase A's fan-out and on the A → B loop.

**[docs]** The remedy for an overloaded pass is chaining: *"Chain prompts: For complex tasks that involve multiple sequential
steps, make each step a prompt and chain the prompts together in a sequence. In this sequential chain of prompts, the output of
one prompt in the sequence becomes the input of the next prompt."* **[measured-family]** And a composition phrased as a
standard rather than a call gets satisfied by writing compliant-looking code: on `COD Dossier` a skill said *every design
decision goes through `design-craft` with `ux-craft`'s lens* and **neither** skill was invoked, the model's own diagnosis
naming the mechanism — nothing downstream depended on a file only those skills produce.

`scan_skill.py` flagged **0** qualitative skill references here, and the phrasing is imperative rather than lens-shaped.
**[derived]** The exposure is the same anyway, because no Phase A output is a file Phase B has to open:

```
A1 completeness  → audit/<id>-r<N>-completeness.md   (requirement → file:line → status)
A2 correctness   → audit/<id>-r<N>-correctness.md    (miss classes 1-11, each exercised or n/a)
A3 guardrails    → audit/<id>-r<N>-guardrails.md     (read the repo's own CLAUDE.md first)
A4 ui-fidelity   → audit/<id>-r<N>-ui.md             (against the mock index, measured not read)
A5 security      → audit/<id>-r<N>-security.md       (strongest model, never delegated)
A6 surgical      → audit/<id>-r<N>-surgical.md       (diff scope vs the gap list)
A7 critic        → reads A1-A6, writes audit/<id>-r<N>-critic.md
B                → reads the six + the critic; a missing or empty file blocks the phase
```

**[docs]** Their existence is also what makes the loop's exit checkable: *"When model outputs must be machine-readable or
follow a specific format, use a widely recognized standard like JSON, XML, Markdown or YAML that can be parsed by common
libraries"* — so `two consecutive dry audits` is a diff of two rounds' files, not a recollection.

## Override 5 — read the inputs, then answer, and read them at absolute paths

Lands on Setup step 2.

**[measured-family]** On `COD Dossier`, asked a question naming three skills, the run answered from memory without loading any;
asked to fix that, it inverted the error and launched a skill instead of answering. There is no stable mapping from "named in
the prompt" to "loaded". The workable rule is two ordered steps, neither substituting for the other: the spec/ticket and its
**full** thread, the plan, the verifier's verdict, `miss-classes.md` and the repo's own CLAUDE.md get read, and *then* the
audit gets written.

**[derived]** Two traps specific to this stage. `read … from the main tree at absolute paths` (SKILL.md:39–40) is load-bearing:
under a worktree a relative `docs/…` resolves inside the worktree, finds nothing, and the run proceeds from the task
description alone — grounded in nothing and looking fine. And **[measured-family]** a hard capacity error pivots on attempt 1:
a `Read` against a 25k-token ceiling was retried four times with offset tweaks in one run before a Python split worked. A long
thread or a large verdict gets ranged reads or a script on the first refusal, not a second attempt.

## Override 6 — one worked gap row before the set

Lands on Phase C's closed-in-code list.

**[docs]** *"We recommend to always include few-shot examples in your prompts … you can remove instructions from your prompt if
your examples are clear enough in showing the task at hand."* So author the first row at full fidelity and let the rest match
it, rather than describing the format:

| gap | severity | source | files | clause now satisfied | typed evidence |
|---|---|---|---|---|---|
| Invite accepted by a non-member returns 200 and writes no membership | Critical | verifier row 4 (Missed) | `apps/api/src/invites/invites.service.ts:118`, `…/invites.controller.ts:44` | AC-3, "accepting an invite adds the user to the company" | BEHAVIOURAL — `POST /invites/abc123/accept` → `200 {"ok":true}`; `db.memberships.countDocuments({userId})` `0 → 1`; `invites.service.spec.ts::accept adds membership` red@`9f2a1c` → green@`4d81e0` |

## `thinking_level`

**[docs]** A six-dimension audit, a merge of three gap sources, a fix pass and a two-dry loop is what Google describes `HIGH` as
being for — *"multi-step planning, verified code generation"* — and Gemini 3.7 Flash defaults to `MEDIUM`. Leave sampling
parameters alone: *"we strongly recommend keeping them at their default values for Gemini 3.x models."*

**[measured-family]** Write that as what the level is *for*, never as a remedy. Paired across all 106 tasks, `high` beat
`medium` on 24, lost on 24 and tied on 58 — mean −1.7 points — and on brownfield work specifically it moved 16.1 to 19.6 while
the bound failures got *worse* (86% of failures against 58%). Nothing in Overrides 1–3 improves by raising it. **[docs]** The
one honest reason to prefer `HIGH` here is tool volume: *"Higher thinking levels encourage the model to use more tools to
explore and verify, so lowering the level can reduce tool calls"*, and this stage's exposure is too few files read.

## Modules not written, and why

The scan fired **none** — core only, at the ≥3-trigger threshold. That is the right result and it is worth saying which were
close. **`gate`** did not fire because this skill ships no probe of its own; it runs `the full repo gates`, and the receipt
rule for those sits at the end of Override 3. **`bounded-constraint`** did not fire on 0 listed bound rows, yet its mechanism
is the single most applicable thing here, which is why Override 2 carries it from the 10 counted prohibitions instead.
**`visual`** reached its trigger only through `UI fidelity vs the mock index`, where the measuring is `evidence-rules.md`'s job
rather than this skill's. **`delegation`**, **`injection`**, **`authorship`**, **`platform-values`**, **`states`** and
**`count-contract`** did not fire and are not written. **`emphasis`** found **0** shouted words in 99 lines.
