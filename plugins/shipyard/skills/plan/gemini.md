# shipyard:plan, calibrated for Gemini

Read this in one pass before `## Inputs`, then run the skill as written. Each override names the section it lands on, because a
conditional side-file is otherwise the shape Google's checklist warns about — **[docs]** *"Avoid writing a prompt with
non-linear logic or conditionals that require the model to piece together fragmented instructions from multiple different
places in the prompt."*

This stage is the pipeline's amplifier — `everything downstream amplifies it` — so the two failure directions below both cost
more here than anywhere. One under-delivers the test strategy's categorical nouns; the other over-delivers the plan itself,
past a length budget the skill states four times in numbers.

**No route-out block here, and that is a decision.** **[docs]** The checklist's **Task outside of model capabilities** entry —
*"Avoid using prompts that ask the model to perform a task for which it has a known, fundamental limitation"* — is the sentence
such a block applies, but geminify's corpus measures a model **building** something. This stage builds a markdown document and
runs review gates: `static-page` and `visual-design` are shapes it never produces, and `brownfield-integration` /
`regression-sensitive` are about editing working code, which this stage explicitly does not do. **[derived]** The inverse is
worth stating instead: this is where `--shape` gets *named* for the worker, so a slice classified `greenfield-module` when it is
really `brownfield-integration` mis-routes the executor lane and the corpus's own numbers stop applying downstream.

## What transferred intact

Naming these matters: effort spent re-hardening a working rule is effort not spent on the test strategy.

- **The tier budgets are already objective constraints** — Trivial <50, Small <120, Standard <350, Large <700 lines, with a
  named Standard↔Large tie-breaker. **[docs]** the **Ambiguity** entry prescribes *"objective constraints"* over *"subjective
  or relative qualifiers that lack a concrete, measurable definition"*, and these are among the cleanest in the ecosystem.
  Override 2 reads them back off the written file, which is the half that is missing.
- **`every backtick-quoted path in the plan exists (ls / git ls-files)`** (SKILL.md:90). A mechanical check with a command
  attached is exactly what Override 3 asks every other claim to become; this one is already there.
- **The lane ladder handles its own failures** — `empty output = lane failure → next lane; all lanes down → in-family strong-
  model review, recorded as a downgrade` (SKILL.md:99–100). **[docs]** *"On *other* errors, you must change your strategy or
  arguments, not repeat the same failed call."* That is C3's retry ceiling, already written down and already routing.
- **`Ambiguity is not a reason to bail; plan every requirement`** (SKILL.md:114) with assumptions recorded rather than
  questions asked. **[docs]** the agentic template's risk rule agrees — *"Prefer calling the tool with the available
  information over asking the user"* — and the divergence test upstream of it makes the choice recorded rather than silent.

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

- No Gemini run of `shipyard:plan` exists, and no run anywhere has been measured **with** a `gemini.md` in place against the
  same work without one. Every override is a derived mechanism, not a demonstrated fix.
- **Nothing measures a model planning rather than building.** Both sessions and all 106 tasks watch a model produce a code or
  page artifact. §2.4 is the closest thing — Gemini's failed backend rows pass a median 0.86 of their verifier's tests while
  scoring zero on the binary AND across groups, which is a last-mile shape rather than a collapse — and it says nothing about
  whether the plan that preceded it was good.
- Nothing measures the review gate at step 5 under this family, or `agy` as the lane running it.
- The state-matrix guidance in Override 4 is derived from a run that *built* a mock, not from one that planned coverage for it.

## Override 1 — the test strategy is a filled table, not a comprehensive intention

Lands on step 3's **Test strategy** bullet and on step 5.

**[measured-family]** One Gemini run delivered every requirement its brief *enumerated* — twelve named features, all present —
and every requirement named *categorically* once or not at all: all surfaces → 5, all states → **1**, all menus → **0**, all
user flows → **0**, all actions → one generic toast. This skill asks for `every user flow, action, and menu the feature adds`
(SKILL.md:57). Those are the same three nouns, and two of them came back zero. **[docs]** **Too many tasks** explains why one
pass cannot carry them: *"If the prompt asks the model to perform several distinct cognitive actions in a single pass (for
example, 1. Summarize, 2. Extract entities, 3. Translate, and 4. Draft an email), it is likely trying to accomplish too much.
Break the requests into separate prompts."*

`scan_skill.py --refs` listed **2** quota rows over 276 lines and counted **21 distributives** it declined to list. One listed
row survives — `comprehensive` at SKILL.md:4, which is the checklist's own example of a qualifier needing a number — and
`every section` at SKILL.md:120 is dropped as prose about the reader rather than a deliverable. The rest are recovered by hand:

| Row | Source | Number to report |
|---|---|---|
| Test portfolio layers addressed or waived | test-strategy.md:10–17 | 6 of 6 — unit, contract, e2e, visual, a11y, regression |
| User flows with an e2e spec named | SKILL.md:57 | `N of N` — the row that came back 0 |
| Actions with an e2e spec named | SKILL.md:57 | `N of N` — the other row that came back 0 |
| Menus with an e2e spec named | SKILL.md:57 | `N of N` |
| Visual coverage cells from the design stage's matrix | SKILL.md:58 | `surfaces × states`, each covered or waived with a reason |
| Acceptance criteria falsifiable at the base commit | SKILL.md:59 | `N of N`, each with the observation that would show it false |
| Test seams named (existing preferred, highest possible) | SKILL.md:55 | `N of N`, and `0` unconfirmed seams |
| Parity-inventory behaviours, where a path is replaced | SKILL.md:61–63 | `N of N` marked keep / port / drop-with-rationale |
| Audit emit surfaces enumerated for **this** repo | SKILL.md:72 | `N of N` found by grep — see Override 5 |
| Emit call sites located, with their registry rows | SKILL.md:70–74 | `N of N` (file + function + row), or one line saying none exist |
| Scope-narrowing comparisons run | SKILL.md:81 | `every out-of-scope line × every triage assumption`, `N × M` compared |
| Backtick-quoted paths checked to exist | SKILL.md:90 | `N of N`, exempting only `to be created` |
| Review-gate questions answered by the lane | SKILL.md:96–98 | 6 of 6, each with a verdict |

Delivery line, filled rather than described: `6 of 6 layers · 4 flows / 7 actions / 2 menus, all with named specs · 30 matrix
cells, 27 covered, 3 waived · 6 of 6 ACs falsifiable at base · 3 seams, 0 unconfirmed · parity n/a (no replacement path) · 3 of
3 emit surfaces grepped, 2 call sites + 2 registry rows · 41 of 41 paths exist · gate 6 of 6, verdict accept`. **[docs]**
*"Include specific verification steps in either the system instructions or your prompts directly."*

## Override 2 — the plan's own length budget, read back off the written file

Lands on step 3, on the `Guidelines` block and on `plan-tiers.md`.

**[measured-family]** This is the failure direction that reaches a passing-looking artifact. Across 106 benchmark tasks,
`gemini-3.7-flash`'s failing UI assertions were 58% bound-shaped at `medium` and **86%** at `high`, against 8% for opus and 6%
for the OpenAI lane; the single most-repeated bound failed on *every* instance in its set while the same run passed 37 of its
other 39 assertions. A quota under-delivers; a bound is exceeded while everything asked for is present. The default idiom
supplies the excess and nothing reads it back — and a plan's default idiom is a full section list.

That matters more here than in most targets because the skill says what the cost is: `padding with empty sections is worse than
omitting them, because the worker treats every section as work` (SKILL.md:120). An over-length plan is not untidy; it is extra
work ordered by accident. The scan listed **3** bound rows and counted **19 prohibitions**; the countable ones, filled from the
file rather than from the brief:

| instance | property | stated bound | readback | observed | within? |
|---|---|---|---|---|---|
| the plan | line count for its tier | Trivial <50 · Small <120 · Standard <350 · Large <700 | `wc -l docs/plans/<id>.md` | 412 at Standard | **no** |
| the plan | tier stated | exactly 1, same name in file and summary | grep `**Plan size:**` and compare to the console line | 1, matching | yes |
| Trivial/Small | banned headings present | 0 of 6 (Edge Cases, Testing, Requirements Traceability, Prerequisites, Acceptance criteria, multi-step verification) | `grep -c '^## '` against the banned list | 2 | **no** |
| any tier | `## Verify` blocks | exactly 1, bullets inside it | count `^## Verify` and the steps beneath | 1 | yes |
| any tier | sections whose body is "no changes required" | 0 | grep the bodies for the empty-section phrasings | 0 | yes |
| Standard | Requirements Traceability table | 0 (a Large-tier device) | grep for the table header | 0 | yes |
| Audit coverage | rows per qualifying path | exactly 1 (plan-tiers.md:110) | count rows against the paths found in Override 5 | 2 rows, 3 paths | **no** |
| Audit coverage | section present when nothing qualifies | 1 line saying so, never omitted | grep for the section at every tier | present | yes |
| acceptance criteria | bullets | 3–8 | count `- [ ]` | 6 | yes |

**[docs]** Google treats these as a component in their own right — *"Restrictions on what the model must adhere to when
generating a response, including what the model can and can't do"* — and names where they go: the **Recap** component is a
*"Concise repeat of the key points of the prompt, especially the constraints and response format, at the end of the prompt."*
**[derived]** The trap: a bound written as a prohibition reads as style advice. `Don't pad the plan` and `412 lines against a
<350 budget` are the same finding, and only the second one survives contact with a model that agrees with the rule and then
writes the sections anyway.

## Override 3 — every gate in this skill reports its command and its output

Lands on step 5 and on step 6.

**[measured-family]** One Gemini run wrote itself a review document with five well-formed `PASS` rows: a named engine that
failed all four invocation attempts and never ran, a *100% pass rate* from a probe never executed, and an audited-target count
nothing produced. Not dishonesty — a requested **shape** completed where the shape was specified and the procedure was not.
Step 5 asks for exactly such a shape: `Record verdict + tally in the plan's gate note`.

**[docs]** *"Verify your claims by quoting the exact applicable information (including policies) when referring to them."* So:

- **The path check** pastes its command and its result — `git ls-files -- <paths>` with the miss list, not "paths verified".
  A denominator of zero is a check that never ran.
- **The out-of-family lane** is wire-verified rather than trusted: the captured header greps for model and effort, and an
  **empty or absent output file is a lane failure**, not a quiet pass. Where every lane is down, the note records an in-family
  review as a **downgrade**, which is the honest line — not an omission.
- **The commit claim carries the sha.** `Never claim repo presence without the sha` (SKILL.md:106) is the same rule in this
  skill's own words: the claim has to be checkable against `git ls-files`.
- **Rendered-appearance statements carry `(measured: …)` or `(assumed from source — verify in browser before building on it)`.**
  **[measured-family]** A false reference-implementation premise read off a class string becomes the worker's unchallenged
  truth, and one measured run's artifact scored 3.65:1 on every primary button while its own review claimed a 100% contrast
  pass — the inverse of the truth, in a document that read as complete.

**[derived]** All of this reverses the house style deliberately. Stripping verification scaffolding is right for a model that
over-verifies; inheriting that removal here is the defect this file exists to undo.

## Override 4 — `states`: the matrix arrives as cells, or it arrives as one

Lands on step 3's `visual/state coverage read off the design stage's state matrix`.

**[docs]** **Underspecified task**: *"Ensure that the prompt's instructions provide a clear path for handling edge cases and
unexpected inputs, and provide instructions for handling missing data rather than assuming inserted data will always be present
and well-formed."* **[measured-family]** And the measured shape: a run given six named states *and* an explicit completeness
condition delivered **one** — the populated one — with zero focus, active or disabled rules anywhere in the artifact.

So the plan's state coverage is a table with one row per surface × state, each cell naming the spec that covers it or a waiver
reason, copied forward from the design stage's matrix rather than summarised. Where design has not run, the row is
`awaiting mock index` (SKILL.md:32) — a named absence, which is greppable, rather than silence. The minimum enumerations live
in `test-strategy.md:24–31` and are worth writing out rather than referencing: nav 4 states, forms 6, tables/lists 4, modals 4,
permissions 3, responsive 3. **[derived]** A plan that says `visual coverage per the state matrix` has satisfied the sentence
and specified nothing; a plan with 30 rows has ordered 30 checks.

## Override 5 — the repo's values get grepped, and every file named in the prompt gets read

Lands on step 3's **Audit coverage** bullet and on `## Inputs`.

**[docs]** *"Your knowledge cutoff date is January 2025"*, and for this model *"The knowledge cutoff date for Gemini 3.7 Flash
is March 2026 — users can expect updated information for some domains while in others they may experience the model's knowledge
is limited to January 2025 (in line with the Gemini 3 Model Family)."* **[measured-family]** The observable form of that is not
a hedge: one run returned a *previous-generation published value* — a superseded platform accent colour — with full confidence,
inside an artifact that was otherwise specific and plausible.

**[derived]** This skill has a matching trap of its own, and it is the sharpest specific in this file. Step 3 names Diolog's
three emit helpers, its registry file, its two enforcing specs and a reference ticket, while step 1 says
`read the repo's shape, don't assume any particular framework`, and `plan-tiers.md` reaches for NestJS modules and Mongoose
schemas throughout. Those are one repo's values sitting in shared guidance. Recalled into a repo that has neither, they produce
a plan naming a registry file that does not exist — a plan `grounded in assumption`, which step 5's path check is there to
catch. So: grep for the repo's *own* emit surfaces before writing the row, and let the count be whatever the grep returns.

**The same rule covers files named in the prompt.** **[measured-family]** On `COD Dossier`, asked a question naming three
skills, the run answered from memory without loading any; asked to fix that, it inverted the error and launched a skill instead
of answering. Two ordered steps, neither substituting for the other: the spec/ticket and its **full** thread, the triage
Assumptions, the design mock index, `plan-tiers.md` and `test-strategy.md` get read, and *then* the plan gets written.
**[measured-family]** And when a read refuses on capacity — one run retried a 25k-token-capped `Read` four times with offset
tweaks before a Python split worked — pivot on attempt 1 to a ranged read or a script.

## Override 6 — one worked step at full fidelity, then the rest

Lands on step 2's synthesis and step 3's template.

**[docs]** *"We recommend to always include few-shot examples in your prompts … you can remove instructions from your prompt if
your examples are clear enough in showing the task at hand."* Investigation follows the same rule as the writing: **[docs]**
*"Chain prompts: For complex tasks that involve multiple sequential steps, make each step a prompt and chain the prompts
together in a sequence. In this sequential chain of prompts, the output of one prompt in the sequence becomes the input of the
next prompt"* — which is what the Workflow fan-out already is, one reader per subsystem, each returning exact files, closest
analogue and contracts, synthesized by you rather than by them. Cap each wave at 4.

Then author step 1 of the plan completely and let the rest match it:

```markdown
### 1. Add `companyId` scoping to the invite lookup
- **File:** `apps/api/src/invites/invites.service.ts`
- **Action:** Modify
- **Details:** `findByToken` currently queries `{ token }`; add `companyId` from the authenticated principal, not the body.
- **Reference:** `memberships.service.ts:88` `findForActor` — same guard shape, same fail-closed default.
- **Verify:** `POST /invites/<token>/accept` as a member of another company → 404, and the existing accept path still 200s.
- **Fulfils:** AC-2 (cross-tenant invite acceptance is refused).
```

## `thinking_level`

**[docs]** This skill's work is the literal example: `HIGH` is *"suitable for complex prompts requiring deep reasoning, such as
multi-step planning, verified code generation, or advanced function calling scenarios"*, and Gemini 3.7 Flash defaults to
`MEDIUM`. Leave sampling parameters alone: *"we strongly recommend keeping them at their default values for Gemini 3.x
models."*

**[measured-family]** Write it as what the level is *for*, never as a remedy. Paired across all 106 benchmark tasks, `high`
beat `medium` on 24, lost on 24 and tied on 58 — mean −1.7 points — and the bound failures got *worse* at `high` (86% of
failures against 58%), which is the direction Override 2 guards. Nothing in Overrides 1–3 improves by raising it. **[docs]**
The one honest reason to prefer `HIGH` here is tool volume: *"Higher thinking levels encourage the model to use more tools to
explore and verify, so lowering the level can reduce tool calls"*, and step 2's whole value is files opened.

## Modules not written, and why

The scan fired `states` (3 hits) — Override 4. **`gate`** did not fire: this skill ships no probe, and the receipt rules for
the two mechanical checks it *does* run sit in Override 3. **`bounded-constraint`** did not fire on 3 listed bound rows, yet
its mechanism is the most applicable thing here, which is why Override 2 carries it from the 19 counted prohibitions the scan
declined to list. **`delegation`** reached its triggers through the Workflow fan-out; its content — cap the spawn count, never
delegate a check of your own output — is one clause in Override 6 and the `REVIEWER ≥ WRITER` rule the skill already carries,
so it is not written as a module. **`visual`**, **`platform-values`**, **`authorship`**, **`injection`** and
**`count-contract`** did not fire and are not written. **`emphasis`** found **0** shouted words across 276 scanned lines, and
the scan flagged **0** qualitative skill references to convert into artifact-gated phases.
