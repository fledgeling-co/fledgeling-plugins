# tui-craft, calibrated for Gemini

Read this in one pass before `## The loop`, then run the skill as written. Each override names the
section of `SKILL.md` it lands on, because **[docs]** a conditional side-file is the shape
Google's checklist warns about — **Conflicting internal references**: "Avoid writing a prompt with
non-linear logic or conditionals that require the model to piece together fragmented instructions
from multiple different places in the prompt."

This skill starts well placed: one width function measures both the composed frame and the
capture, and `SKILL.md:234` already requires every finding to carry `its row and column, what the
cell holds, what it should hold, and which capture it came from`. What does not cross is the
assumption that a rule stated in prose gets executed. `SKILL.md:86` says *"Every state you intend
to claim anything about gets its own capture — the six states below are six captures, not one
screenshot and some optimism."* Here that yields one, gated green.

## Route out before you start (§The loop, step 6)

**[docs]** The health checklist says it under **Task outside of model capabilities**: "Avoid using
prompts that ask the model to perform a task for which it has a known, fundamental limitation."
That applies to the *fixing* half of the loop, not the reviewing half:

| shape | what it is here | **[measured-family]** |
|---|---|---|
| `brownfield-integration` | editing an existing multi-file TUI repo against several criteria at once | 24 against opus's 50 |
| `regression-sensitive` | a fix that must not tear the other eleven frames now gating clean | 42 against 65 |

A pointer, not a pinned model, because the numbers move: `python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape brownfield-integration`.

`visual-design` (35 against 63) belongs here only for a polish pass judged on how the screen
reads; `static-page` is omitted, because this skill authors no self-contained artifact.
**[derived]** The corpus holds no terminal tasks, so the mapping argues from shape, and it
measures a model *building*, so it says nothing about the review half.

## Epistemic status

Tiers, never mixed: **[docs]** is Google's published guidance quoted verbatim, the strongest tier
and most of this file; **[measured-family]** is Gemini runs that are *not* this skill (two
sessions, n=1 each, plus 106 benchmark tasks); **[measured-here]** is this skill's own scripts on
this machine, 18 and 23 Aug 2026; **[derived]** is my reasoning.

**The tier those measurements are about.** Every measured rate here is flash-tier
(`gemini-3.7-flash`, plus one `gemini-3.7-flash-high` session) and none of it may be projected
onto the Pro tier, where these overrides hold as `[docs]`-grounded discipline while every
`[measured-family]` number is open. Defaults drift too — **[docs]** "The default thinking effort
is now medium, changed from high in Gemini 3 Flash Preview." A capture-and-gate loop across twelve
frames is what Google calls `HIGH` work — "multi-step planning, verified code generation" — and
3.7 Flash defaults to `MEDIUM`. Raise it for that reason only: paired across 106 tasks, `high`
beat `medium` on 24, lost on 24, tied on 58.

**Unmeasured on this skill** — none of this has been observed on a Gemini run of `tui-craft`:

- **No Gemini run of this skill exists.** n=0; the family sessions touched no cell grid, no pty
  and no ruler dump, so **whether the categorical collapse reaches captures** and **whether gate
  output gets pasted or summarised** are family patterns applied to this skill's nouns.
- **Whether the fence holds here**, and **whether describe-before-judge helps on a *text* dump** —
  the >50%→<2% figure is GPT-family by the skill's own `references/evidence.md`, and Google's
  describe-first instruction is about images. And **whether any of this works**: no run has been
  measured with this file in place.

## What transferred intact

- **The frame-kind distinction.** `captured` versus `mock` is a typed field carrying provenance,
  so a drawing cannot be quietly promoted to evidence.
- **`--strict` as the invocation, not an option** (`SKILL.md:142`) — an exit code is a verdict
  this family will not talk its way past — and `--self-test` behind it. **[measured-here]** it
  still passes: `gates: TRUSTED`, including `ok   render-proof fires on plain command output`.
- **Find wide, then filter** (`SKILL.md:228`). **[docs]** brevity is the resting state ("By
  default, Gemini 3 models provide direct and efficient answers"), so a severity filter applied
  during the looking compounds a default that already under-reports.

## Override 1 — the capture ledger, written before the first capture (§The loop, step 1)

**[docs]** Under **Ambiguity**: "Avoid using subjective or relative qualifiers that lack a
concrete, measurable definition. Instead, provide objective constraints (for example, 'write a
summary of 3 sentences or less' instead of 'write a brief summary')." `Every state` is a relative
qualifier; `6 states × 2 sizes = 12 captures` is an objective constraint, and the grid gets
executed where the sentence gets skimmed. **[measured-family]** asked for all states, one run
delivered **1 of 6** — the populated one — plus 0 menus and 0 flows, an absence the gates cannot
see because `render-proof` passes on a frame that exists.

Write the grid to disk before capturing anything — one cell per state × size, each holding a
filename or `n/a: <reason>`. Filled, for one screen:

| state | 100×30 | 80×24 |
|---|---|---|
| first-run / empty | `dashboard-empty-100x30.json` | `dashboard-empty-80x24.json` |
| loading | `dashboard-loading-100x30.json` | `dashboard-loading-80x24.json` |
| ideal | `dashboard-ideal-100x30.json` | `dashboard-ideal-80x24.json` |
| partial | `dashboard-partial-100x30.json` | `dashboard-partial-80x24.json` |
| error | `dashboard-error-100x30.json` | `dashboard-error-80x24.json` |
| done | `dashboard-done-100x30.json` | `n/a: inline, alt-screen already released` |

**[docs]** Under **Underspecified task**: "provide instructions for handling missing data rather
than assuming inserted data will always be present and well-formed." So each cell also names **how
the state was reached** — the `--keys` sequence, the empty fixture, the unreachable dependency
(`references/frameworks.md` carries that table). Report `12 of 12 cells captured, --strict run on
all 12`, and state the denominator first: three screens is 36 captures, not 12. Run it as passes —
**[docs]** under **Too many tasks**, "If the prompt asks the model to perform several distinct
cognitive actions in a single pass … it is likely trying to accomplish too much. Break the
requests into separate prompts."

## Override 2 — paste the gate output, never a sentence about it (§The loop, step 4)

**[docs]** "Include specific verification steps in either the system instructions or your prompts
directly." And: "Verify your claims by quoting the exact applicable information (including
policies) when referring to them." **[measured-here]**, this skill's gate on a real capture of
`less` at 80×24 — the shape every delivery carries, because **[measured-family]** one run asserted
`Computed Style Integrity: 100% pass rate on contrast` from a probe that never ran:

```
frame  80x24  kind=captured  parser=builtin  term=xterm-256color

[medium] colour-inventory  -  no bold and no dim anywhere in the frame — every glyph
                              carries the same weight, so the screen has no hierarchy
                              that survives a monochrome terminal
[info  ] ink-density       -  27% of cells carry a glyph

3 finding(s), 0 high
```

- **Every number names the file and the command that produced it.** `0 high on
  dashboard-ideal-100x30.json` is a result; `the gates were clean` is not, and `examined=0` is not
  a pass (`SKILL.md:206`) — write that sentence out.
- **The receipt check the gates cannot make.** `tui_gates.py` reads one frame, so it cannot see
  the eleven ledger cells never captured. Assert the ledger and paste the result — `for f in
  dashboard-*.json; do test -s "$f" || echo "MISSING $f"; done` — and run `--self-test` in the
  same round. **[measured-family]** an auditor checking only final deliverable properties let two
  skipped upstream steps through with exit 0.

## Override 3 — a refused capture is the deliverable, and it ends in a command (§The loop, step 3)

**[docs]** The retry rule is explicit: on transient errors retry within any stated limit, but "you
must change your strategy or arguments, not repeat the same failed call." **[measured-family]**
one run invoked a banned, absent tool four times unchanged and then reported it as the engine that
verified the work; another retried a `Read` against a token ceiling four times before pivoting. A
permanent error is one attempt, then a change of approach.

**[measured-here]** Running `tui_capture.py --cmd "./analytics-dash"` returned, verbatim:

```
capture-blocked: the command never ran — the shell exited 127 (not found).
It said: "/bin/sh: ./analytics-dash: No such file or directory"
```

Hand back this shape, filled, and nothing else:

> **capture blocked.** `./analytics-dash` never ran — the shell exited 127. It said:
> `/bin/sh: ./analytics-dash: No such file or directory`.
> Had it produced a frame, the border, column and overflow checks would all have passed on it,
> because a near-empty grid has no border to tear.
> ```bash
> python3 scripts/tui_capture.py --cmd "path/to/analytics-dash" --cols 100 --rows 30 \
>   --settle 1.2 --dump -o dashboard-ideal-100x30.json
> ```

`SKILL.md:116` and `SKILL.md:121` ask for those two sentences; **[derived]** they matter more here
because a model that fills a vacuum with a plausible artifact reads a bare refusal as licence to
read the source, the one move `SKILL.md:19` forbids.

## Override 4 — the bound ledger, read back off the frame (§What the gates decide)

**[measured-family]** Across 106 benchmark tasks, **58%** of Gemini's failing UI assertions at
`medium` and **86%** at `high` state a *bound* — `exactly N`, `no`, `not`, `only` — against 8% for
opus; `has exactly one soft elevation shadow` failed on every instance in its set on a run that
passed 37 of its 39 other assertions. This points the opposite way to Override 1: a bound is
violated by what you did not write, so it survives every check that looks at what you did.
**[docs]** Google treats these as a component in their own right — "Restrictions on what the model
must adhere to when generating a response, including what the model can and can't do."

The gates own the arithmetic bounds; the ones living in prose go in a ledger, one row per bound ×
instance, filled from the captured frame rather than from the brief:

| instance | property | stated bound | readback | observed | within? |
|---|---|---|---|---|---|
| Hosts panel, top rule | shelf anchors | ≤ 3 (`patterns.md:33`) | count the runs between the corners on that row | 3 | yes |
| Queue panel | pad columns each side | 1 (`SKILL.md:198`) | offset of first ink from the border column | 2 | **no** — `overflow-wrap` is blind inside it |
| every panel title | cells per glyph | 1 (anti-patterns §Generated tells) | the `w` field on each title cell | `🚀` w=2 | **no** — the border is off by one below |

Report `N of N instances within bound`. **[derived]** A bound stated as a prohibition — `emoji as
panel titles` — reads as style advice; a counted property with a readback is what makes it hold.

## Override 5 — describe the dump, then pin every finding to it (§The loop step 5, §Reviewing)

**[docs]** "Ask the model to describe the images before performing the task in the prompt", and
"To improve the response, point out which parts of the image are most relevant to the prompt."
**[derived]** The ruler dump is text, so this applies the rule rather than instancing it, but it
prevents the failure `SKILL.md:157` names: the same grid answers `what is wrong with this?` and
`is this done?` differently. Per dump, in order: **name what is in it** — panels, their column
spans, the footer row, each border column — **then** judge, pointing at a region rather than
handing over the whole frame.

**[docs]** Then a finding may not exceed its frame — Google's strictly-grounded system instruction
ends, "If the exact answer is not explicitly written in the context, you must state that the
information is not available." One worked finding, as the exemplar:

> **The Hosts panel loses its right border on row 10.** `dashboard-ideal-100x30.json`, r10 c75
> holds `e` where every other row of that panel holds `│`. The row above carries
> `web-03.syd.internal ✅` — the check mark is two cells wide and the app budgeted one, so every
> write after it on that row is offset by one. `border-integrity` fired here; `width-arithmetic`
> fired on the same row.

Anything you cannot pin to a file, a row and a column goes in a separate `suspected, not captured`
list, or is dropped — the guard against this family's move, the *shape* of a review produced for a
frame nobody opened. A finding is a claim about the dump rather than about the gate:
`SKILL.md:201` names `border-integrity`'s false positive on stacked panels.

## Override 6 — values are read, not recalled, and so are named files (§Terminal truths)

**[docs]** From the 3.7 Flash model card: "The knowledge cutoff date for Gemini 3.7 Flash is March
2026 — users can expect updated information for some domains while in others they may experience
the model's knowledge is limited to January 2025 (in line with the Gemini 3 Model Family)."

**[measured-family]** The failure this prevents is not a guess: one run put Windows 10's `#0078D4`
on a Windows 11 surface, a previous-generation *published* value returned confidently.
`references/terminal-truths.md` is full of that class — DEC 2026, OSC 11, Nerd Font private-use
ranges, a powerline separator's East Asian Width.

**The same rule covers files the prompt names.** **[measured-family]** asked a question naming
three skills, one run answered from memory without loading any; asked to fix that, it inverted the
error and launched a skill instead of answering. **Load, then answer**, two ordered steps with
neither substituting for the other: `references/patterns.md` §9 before the states are described,
§Generated tells before a generated-tell claim, any named file before the reply.

## Override 7 — a routed-out skill is a phase with an output file (§What the gates decide)

`SKILL.md:212` calls `ux-craft`, `design-craft` and `be-my-witness` `standing dependencies rather
than optional extras`. **[measured-family]** that is the phrasing one run skipped outright: told
every design decision goes through `design-craft` with `ux-craft`'s lens, it invoked neither, and
its own diagnosis named the mechanism — the rules were in context and nothing downstream depended
on a file only those skills produce. **[docs]** The remedy is chaining: "Chain prompts: For
complex tasks that involve multiple sequential steps, make each step a prompt and chain the
prompts together in a sequence."

So run them as ordered phases with artifacts between: `ux-craft` writes `UX.md` (the flow, the six
states, the trunk test), `design-craft` writes `DESIGN.md` (hierarchy and restraint, minus the
type scale), the build reads both, and the capture round refuses to start if either file is
missing or empty. **[derived]** That refusal is Override 2's receipt check again; where a skill is
unavailable, name the substitution in `UX.md` so the next phase reads the gap.

## Modules not written, and why

The scan fired seven at threshold. `visual`, `gate`, `states`, `bounded-constraint`,
`platform-values` and `authorship` are Overrides 5, 2, 1, 4, 6 and 5. `injection` fired too, and
the skill's fence is already verbatim and read-only-scoped, so the whole module is one addition:
wrap frame and dump in `<frame>` … `</frame>` in your own context too. `delegation` and
`count-contract` missed the threshold and are covered anyway — the spawn cap at `SKILL.md:356`,
the row/column contract at `SKILL.md:234`, the fence limits at `SKILL.md:345` and the reply
discipline at `SKILL.md:367` all transfer unchanged. `emphasis` scored **0**: this skill shouts
nowhere, and nothing here adds capitals — **[docs]** under **Overt manipulation**, "foundation
model performance will no longer improve and in many cases will get worse."
