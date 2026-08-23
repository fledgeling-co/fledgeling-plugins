# tui-design, calibrated for Gemini

Read this in one pass before `## The loop`, then run the skill as written. Every override
names the section of `SKILL.md` it lands on, because **[docs]** a conditional side-file is
the shape Google's checklist warns about under **Conflicting internal references**:
"Avoid writing a prompt with non-linear logic or conditionals that require the model to
piece together fragmented instructions from multiple different places in the prompt."

This skill starts well placed: `SKILL.md:14` names the failure exactly — `len("🚀 Deploy")`
is 8 and it occupies 9 — and `tui_mock.py` makes that uncommittable by hand. What does not
cross is the assumption that a rule stated in prose gets executed. `SKILL.md:126` says
`compile every state and size in one round`; here that yields one compile, of the ideal
state, at the design size, and the design gates pass on it.

## Route out before you start (§The loop)

**[docs]** The health checklist says it under **Task outside of model capabilities**:
"Avoid using prompts that ask the model to perform a task for which it has a known,
fundamental limitation." Two of this skill's shapes sit far enough behind to hand off first:

| shape | what it is here | **[measured-family]** |
|---|---|---|
| `static-page` | a screen authored from a prose brief, no app and no theme to read | 22 against opus's 67, hard zero on 71% of decided rows |
| `visual-design` | a direction pair judged on which screen reads better | 35 against 63 |

The handoff is a pointer rather than a pinned model, because the numbers move:
`python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape static-page`.

**[derived]** Two bounds on that. The corpus holds no terminal tasks, so mapping `spec.json`
onto `static-page` argues from shape rather than measurement; and the compiler removes the
mechanism those bench tasks failed on. Where no lane is free, do the work and distrust the
**composition** — the role ladder, what earns colour, what goes on the border — not the
geometry. Rows omitted: `brownfield-integration` (edits no repo; step 0 *reads* a theme) and
`regression-sensitive` (nothing is passing yet to break).

## Epistemic status

Four tiers, never mixed. **[docs]** is Google's published Gemini 3 guidance quoted verbatim —
the strongest tier and most of this file. **[measured-family]** is Gemini runs that are *not*
this skill: two sessions (n=1 each) on web and desktop work, plus 106 benchmark tasks.
**[measured-here]** is runs of this skill's own scripts on this machine, 23 Aug 2026, which
is not a Gemini run. **[derived]** is my reasoning from those, marked.

**The tier those measurements are about.** Every measured rate here is flash-tier
(`gemini-3.7-flash`, plus one `gemini-3.7-flash-high` session) and none of it transfers to
the Pro tier, where the overrides hold as `[docs]`-grounded discipline while every
`[measured-family]` number is open. Defaults drift across the family too: **[docs]** "If
thinking_level is not specified, Gemini 3 will default to high", then "The default thinking
effort is now medium, changed from high in Gemini 3 Flash Preview." Compiling twelve frames
through three enforced gates is what Google describes `HIGH` as being for — "multi-step
planning, verified code generation" — and 3.7 Flash defaults to `MEDIUM`. Raise it for that
reason only: paired across 106 tasks, `high` beat `medium` on 24, lost on 24, tied on 58.

**Unmeasured on this skill** — none of this has been seen on a Gemini run of `tui-design`:

- **No Gemini run of this skill exists.** n=0; the family sessions touched no spec, no
  compiler and no cell grid, so **whether the categorical collapse reaches specs** and
  **whether a fit report gets pasted or summarised** are family patterns applied to this
  skill's nouns rather than observations here.
- **Whether a reference input helps**, and **whether describe-before-judge helps on a *text*
  dump** — Google claims the first for UI generation and states the second about images, so
  Override 5 is `[derived]` where it reaches a ruler dump.
- **Whether any of this works.** No run has been measured with this file in place against
  the same work without it.

## What transferred intact

- **The spec containing no column numbers** (`SKILL.md:83`) — a format that cannot hold
  arithmetic cannot hold wrong arithmetic, and it is the one defence needing no prompting.
- **`--gate` combining every exit code** (`SKILL.md:100`); an exit code is a verdict this
  family will not talk its way past. **[measured-here]** it still discriminates: compiled,
  `assets/example-failing.json` exits **1** on three enforced gates and
  `assets/example-dashboard.json` exits **0**. `examined=0` is never a pass (`SKILL.md:161`).
- **The fence at `SKILL.md:282`**, quoted verbatim into any subagent brief with the read-only
  scope beside it. **[docs]** Under **Prompt injection risk**: "Check if there are explicit
  safeguards surrounding untrusted user input that is inserted into the prompt, as this can
  be a major security risk." Nothing to add.

## Override 1 — the spec ledger, written before the first compile (§The loop, step 1)

**[docs]** Under **Ambiguity**: "Avoid using subjective or relative qualifiers that lack a
concrete, measurable definition. Instead, provide objective constraints (for example,
'write a summary of 3 sentences or less' instead of 'write a brief summary')." `Every state`
is a relative qualifier; `6 states × 2 sizes = 12 specs` is an objective constraint, and a
grid gets filled where a sentence gets skimmed. **[measured-family]** asked for all states,
one run delivered **1 of 6** while delivering all twelve enumerated features — and the gates
cannot see that absence, because `role-ladder` passes on the frame that exists.

Write the grid to disk before compiling anything — one cell per state × size, holding a spec
filename or `n/a: <reason>`. Filled, for one screen:

| state | 100×30 | 80×24 |
|---|---|---|
| first-run / empty | `dash-empty-100x30.json` | `dash-empty-80x24.json` |
| loading | `dash-loading-100x30.json` | `dash-loading-80x24.json` |
| ideal | `dash-ideal-100x30.json` | `dash-ideal-80x24.json` |
| partial | `dash-partial-100x30.json` | `dash-partial-80x24.json` |
| error | `dash-error-100x30.json` | `dash-error-80x24.json` |
| done | `dash-done-100x30.json` | `n/a: inline, alt_screen already released` |

Report the fraction at delivery: `11 of 12 cells compiled, 1 n/a with a reason; --gate run on
all 11`. Three screens is 36 specs, not 12 — state the denominator first. **[docs]** And run
it as passes: under **Too many tasks**, "If the prompt asks the model to perform several
distinct cognitive actions in a single pass … it is likely trying to accomplish too much.
Break the requests into separate prompts."

## Override 2 — paste the gate output, never a sentence about it (§The loop, step 3)

**[docs]** "Include specific verification steps in either the system instructions or your
prompts directly." And from the agentic template: "Verify your claims by quoting the exact
applicable information (including policies) when referring to them." **[measured-family]**
one run asserted a 100% contrast pass rate from a probe that never executed; measured
afterwards, every primary button was 3.65:1 and one glyph 1.00:1 — the inverse of the truth.
**[measured-here]**, this skill's gates on the compiled `assets/example-failing.json`, exit 1:

```
ENFORCED
  role-ladder      examined=8    2 failing
      [high] role label reads at 1.82:1 on #111318, below its 4.5:1 floor
      [high] text-dim (16.87:1) out-contrasts text (4.54:1) — the hierarchy is inverted
  state-carrier    examined=1    1 failing
  focus-channels   examined=1    1 failing
```

- **Every number names the frame and the command that produced it.** `0 failing on
  dash-ideal-100x30.json` is a result; `the gates were clean` is not, and neither is a
  `REPORTED` line, which has no pass mark.
- **The receipt check the gates cannot make.** They read one frame, so they see neither the
  eleven ledger cells never compiled nor whether step 0's theme search happened. Assert both
  and paste the result — `for f in dash-*.json; do test -s "$f" || echo "MISSING $f"; done`,
  plus the line `SKILL.md:54` asks for naming the theme file you matched. **[measured-family]**
  an auditor checking only final properties let two skipped upstream steps through with exit 0.

## Override 3 — the bound ledger, read off the compiled frame (§Deciding the design)

This failure reaches a passing-looking artifact, and it points the opposite way to Override 1.
**[measured-family]** across 106 benchmark tasks, **58%** of Gemini's failing UI assertions
at `medium` and **86%** at `high` state a *bound* — `exactly N`, `no`, `not`, `only` —
against 8% for opus; one rule, `has exactly one soft elevation shadow`, failed on every
instance in its set on a run that passed 37 of its 39 other assertions. A bound is violated
by what you did not write, so it survives every check that looks at what you did. **[docs]**
Google treats these as a component in their own right — "Restrictions on what the model must
adhere to when generating a response, including what the model can and can't do." — and the
**Recap** is where they go: "Concise repeat of the key points of the prompt, especially the
constraints and response format, at the end of the prompt."

Three of this skill's bounds are already read back for you, which is why they hold:
`role-ladder`, `state-carrier` and `focus-channels` each read the produced frame. The ones
living only in prose go in the ledger. Filled, **[measured-here]**, against the compiled
`assets/example-dashboard.json`:

| bound (`SKILL.md`) | stated | readback | observed | within? |
|---|---|---|---|---|
| `exactly one column carries category colour` (:232) | 1 | columns in the `table` region whose `fg` is an `ok`/`warn`/`danger` role | **0** | `n/a`: category is carried as text; the only `ok` ink is a 5-cell meter at r5 c81–85 |
| `Signal focus twice` (:229) | ≥ 2 channels | `focus_signals[].channels` in the frame JSON | 2 (`border-colour`, `title-colour`) | yes |
| fits the floor (:60) | ≤ 80 cols | compile the same spec at `80x24` | `fit findings: 0` | yes |

Report `N of N bounds within`. **[derived]** A bound stated as taste — `Reach for reverse
over a coloured fill` — reads as style advice and gets improvised past; a counted property
with a readback is what makes it survive.

## Override 4 — the fit report is the deliverable, and a crash is not one (§The loop, step 3)

**[docs]** The retry rule is explicit: retry transient errors within any stated limit, but
"you must change your strategy or arguments, not repeat the same failed call."
**[measured-family]** one run invoked a banned, absent tool four times unchanged and reported
it as the engine that verified the work; another retried a `Read` against a hard token
ceiling four times before pivoting. A capacity or `not found` error is permanent: one attempt
is the whole budget, then change approach.

**[measured-here]** The fit report already contains the finding. Compiling
`assets/example-dashboard.json` at 70×20 returns exit 1 and, verbatim:

```
fit findings: 5
  {"kind": "column-too-narrow", "column": "JOB", "wanted": 20, "had": 16}
  {"kind": "truncated", "row": 10, "col": 26, "where": "table:cell", "wanted": 20, "had": 16, "text": "PaymentProcessingJob"}
```

Paste that JSON and change the spec — a narrower column, a shorter label, a different split.
Do not raise the size to make it pass; that is the undisclosed requirement `SKILL.md:62`
names. **A traceback is not a fit report:** **[measured-here]** the same spec at 50×14 raises
`TypeError: Canvas.note() got multiple values for argument 'kind'` instead of reporting
`zero-size-node`. Report that as a tool defect at that size and compile at a size that works;
do not read it as the design failing, and do not retry it unchanged.

## Override 5 — a reference in, a description out (§The loop, steps 0 and 4)

**[docs]** Google's launch material for this model says of web work: "For UI generation, the
model shows high design adherence and parity based on a reference input, whether it's a
screenshot, an image, or a full design system." **[measured-family]** every static-page task
in the benchmark that collapsed was a prose brief with **no** reference input, so the corpus
measured the mode the vendor does not claim — suggestive together, not settled. `SKILL.md:48`
already asks for that reference: the project's own `theme.go` / `.tcss` / `Style` constants,
lifted as exact values into the spec's `roles`. **[derived]** Do step 0 first and in full;
where the search genuinely finds nothing, say so and supply the next best — a compiled
`assets/example-dashboard.json`, or a named app from `../tui-craft/references/patterns.md`.

Coming back the other way: **[docs]** "Ask the model to describe the images before performing
the task in the prompt", and "To improve the response, point out which parts of the image are
most relevant to the prompt." **[derived]** The ruler dump is text, so this applies the rule
rather than instancing it, but it prevents the failure `SKILL.md:117` names — the same grid
answers `what is wrong with this?` and `is this done?` differently. Per dump: **name what is
in it** (each panel, its column span, the footer row, where each border column sits), **then**
judge, pointing at `rows 4–12, columns 40–79, the Hosts panel` rather than the whole frame.
`SKILL.md:255` names where a gate is narrower than it looks — `border-integrity` has a known
false positive on stacked panels, firing on this plugin's own `example-dashboard.json` — so a
finding is a claim about the dump, never a restatement of the gate.

## Override 6 — read the file the prompt names, then answer (§The loop, steps 0 and 2)

**[docs]** "Your knowledge cutoff date is January 2025." **[measured-family]** Asked a
question naming three skills, one run answered from memory without loading any of them;
asked to fix that, it inverted the error and launched a skill instead of answering. The rule
is **load, then answer**, two ordered steps with neither substituting for the other. Here:
`references/spec-format.md` is read before a spec node is written — the node keys, the
`flex`/`w`/`h` split and the shelf slots are not recalled — and `references/composition.md`
before a role ladder is authored. Same for any file the reader names in the prompt.

## Override 7 — a composed skill is a phase with an output file (§Deciding the design)

`SKILL.md:240` calls `ux-craft` and `design-craft` `standing dependencies rather than
optional extras`. **[measured-family]** that is the phrasing one run skipped outright: told
every design decision goes through `design-craft` with `ux-craft`'s lens, it invoked neither,
and its own diagnosis named the mechanism — the rules were in context already and nothing
downstream depended on a file only those skills produce. **[docs]** The remedy is chaining:
"Chain prompts: For complex tasks that involve multiple sequential steps, make each step a
prompt and chain the prompts together in a sequence."

```
Phase 1  Skill ux-craft      → UX.md      (the six states, the trunk test, the error copy)
Phase 2  Skill design-craft  → DESIGN.md  (hierarchy and restraint, minus the type scale)
Phase 3  write spec.json     — reads UX.md for the state list, DESIGN.md for the ladder
Phase 4  tui_mock.py --gate  — refuse to start if either file is missing or empty
```

**[derived]** Phase 4's refusal is the half that makes it stick, and it is Override 2's
receipt check again. Where a skill is genuinely unavailable, `SKILL.md:245` requires you to
name the substitution — write that into `UX.md` so the next phase reads the gap.

## Modules not written, and why

The scan fired `visual`, `gate` and `bounded-constraint` at threshold; they are Overrides 5,
2 and 3. `states` did not clear it and nothing is lost — the six states are Override 1's
ledger rows. `injection` did not either, and `SKILL.md:282`'s fence is already verbatim and
read-only-scoped. `platform-values`, `authorship`, `delegation` and `count-contract` scored
below threshold on a skill that cites no vendor SDK and spawns nothing routinely. `emphasis`
scored **0**: this skill shouts nowhere, and nothing here adds capitals — **[docs]** under
**Overt manipulation**, "foundation model performance will no longer improve and in many
cases will get worse."
