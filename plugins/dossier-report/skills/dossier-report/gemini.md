# dossier-report, calibrated for Gemini

This skill was written against a Claude model's failure modes. Gemini's differ, and this
house's deliberate *removals* — verification scaffolding especially — leave a vacuum on
this family that fills with something plausible. Read this once, before `## The shape of
a run`, then follow the skill as written with the overrides below; each names the line it
lands on. Little here disputes the skill: what needs work is a handful of scopes stated
as a class rather than a count, and a pipeline whose most expensive step is *reading*
putting no denominator on it.

## Epistemic status

`[docs]` is Google's published guidance, quoted verbatim from `gemini-corpus.md`.
`[measured-family]` is one recorded Gemini run of *another* skill, **n=1**. `[derived]`
is reasoning from those two onto this skill's own text.

**No `[measured-here]` tier appears below.** No Gemini run of `dossier-report` has been
recorded, and the family run was a build-a-UI brief in another repo, so every inference
from it onto a research pipeline travels further than the tag suggests.

**Unmeasured on this skill:** whether this family reads five exported reports end to end
or works from the outline (the founding failure, never watched on Gemini); whether the
three readings preserve confidence, limits and the panel's disagreements; whether
`audit_page.py`'s `PASS` lines get pasted or paraphrased; whether the `MOBBIN TRAWL`
ledger comes from opened images or titles; cost behaviour; any rate for anything.

`[docs]` **This file's own shape is a defect Google names** — a prompt with "non-linear
logic or conditionals that require the model to piece together fragmented instructions
from multiple different places in the prompt." Hence one pass, up front, every override
naming its landing site. `HIGH` is also the right `thinking_level` here — "multi-step
planning, verified code generation" — and Gemini 3.7 Flash defaults to `MEDIUM`.

## What transfers intact

`[derived]` Named so you do not spend effort where there is no gap.

- **The numbers are already objective constraints.** `[docs]` **Ambiguity** asks for
  "objective constraints (for example, "write a summary of 3 sentences or less" instead
  of "write a brief summary")". This skill mostly complies — 3–6 categories, three ranked
  picks, three to five TLDR claims, six review passes, 45–75 characters, 24px/16px
  gutters, 120–250ms, 44×44px — and those survive *because* they are counts. The scan's
  71 relative-qualifier hits dedupe to six phrases, five of them false positives:
  `Brief` is a register name, `short labels` sits in a Mobbin query, three are
  statistical terms inside cited studies.
- **The claim graph and the state grid are already cells rather than prose.** Phase 3's
  build-failure conditions are mechanical, and `page-craft.md` §11's grid carries `n/a`
  plus a reason per cell — which is why no `states` section appears below.
- **The auditor already knows the vacuous-pass problem.** SKILL.md:559: a `claims.json`
  no block references means the per-claim check "has nothing to test and passes
  vacuously". And the register is calm — two emphasis tokens in 3,235 lines, where
  `[docs]` **Overt manipulation** warns that escalating language means performance "will
  no longer improve and in many cases will get worse".

## C1 — four scopes carry no denominator

`[measured-family]` On the recorded run every *enumerated* requirement shipped — twelve
named features — and every *categorical* one shipped once or not at all: `all surfaces`
→ 5, `all states` → **1**, `all menus` → **0**. `[docs]` **Too many tasks** compounds
**Ambiguity**: "If the prompt asks the model to perform several distinct cognitive
actions in a single pass … it is likely trying to accomplish too much. Break the requests
into separate prompts."

`[derived]` The scan raised 47 categorical occurrences over 19 distinct phrases. Eleven
are prose ("the whole page", inside an argument against pinning) and are dropped; eight
are deliverable scopes, and four carry no number anywhere in the skill:

| Scope | Where | The count it needs |
|---|---|---|
| every research report, read end to end | SKILL.md:115 | exported members |
| `dataviz` on every figure | SKILL.md:63 | figures in the claim graph |
| every image carries caption, provenance, registry row | SKILL.md:570 | `<img>` in the page |
| every state renders directly from its id | SKILL.md:419 | scroll states |

The other four resolve into per-cell rules the auditor counts, and the skill diagnoses
the trap unaided at `page-craft.md:739`: a categorical instruction ships as one state; a
grid with cells in it does not.

**The override: write the scope ledger before Phase 6** — into `claims.json`, or as a
comment in `index.html`; report the fractions at delivery. Where a number is not given,
derive it and state it, from the export directory or a `grep -c` on the built page.

```
SCOPE LEDGER — <slug>
  REPORTS   n=5   read end to end 5/5  ·  verify_citations on 3 (load-bearing)
  CLAIMS    n=41  direct 33 · inference 8  ·  inferences with non-empty `from` 8/8
  READINGS  n=3 × 41 = 123 cells · written 118 · omitted 5 (each with omitReason)
  FIGURES   n=7  dataviz 7/7 · text alternative 7/7   IMAGES  n=6  provenance 6/6
  STATES    n=9  renders from its own id with script off 9/9
  RENDERS   n=3 readings × 2 themes × 2 viewports = 12 captures, 12 opened
```

## C4 — Phase 7 is five passes, not one

`[docs]` The remedy for an overloaded pass is chaining: "make each step a prompt and
chain the prompts together in a sequence." `[derived]` Phase 7 asks for structure, prose
in three registers, figures, motion and imagery at once. Run it as five passes over one
claim graph: **structure** (section list from the graph alone, then checked against the
brief's enumeration per SKILL.md:373–386) → **prose** (three `create-luke-content`
passes, one per reading, each from the graph) → **figures** → **motion** → **imagery**.

## C2 — verification is asked for, and one line here is not addressed to you

`[docs]` "Include specific verification steps in either the system instructions or your
prompts directly", and "Verify your claims by quoting the exact applicable information
(including policies) when referring to them."

`[measured-family]` What filled the vacuum: a self-written review asserting a browser
engine that failed on all four invocation attempts and never ran, a claimed `100% pass
rate on contrast` from a probe never executed — measured afterwards at 3.65:1 — and an
audited-target count nothing produced. A requested *shape* completed where the procedure
was not.

`[derived]` **The line to be careful with is `references/opus-5-prompting.md`:22 —
"Remove verification scaffolding. Opus 5 verifies its own work."** That file governs the
briefs this pipeline writes for its Opus children; it is right about them and wrong about
you. Keep the removal in the child briefs, do not inherit it. Its next paragraph draws
the line: an instrument run is not a self-check, and the instruments here are
`audit_page.py`, `research_verify_citations` and `design-review`.

1. **Every number in the methods note carries the command that produced it and that
   command's output.** If you cannot paste it, write `not measured`. A denominator of
   zero is a gate that never ran, never a pass.
2. **Never let the page assert its own verification.** SKILL.md:562 already fails a
   colophon "advertising more sources than the registry holds"; a methods note
   advertising an unrun check is the same defect.

## `gate` — the auditor's output is the claim

`[derived]` This skill's auditor is the same idea as the quote-checker that gated this
file, pointed at a different corpus — a citation that does not resolve is a build
failure.

- **Paste the run, not a claim about it** — one row per check, then `N error(s), M
  warning(s)`; exit 0 means every ERROR check passed. Its `PASS` details carry their own
  denominator (`all 41 cited anchors resolve to a source`), and a pass line with a zero
  in it is the gate reporting it found nothing to check.
- **Prove it can fail first.** `[docs]` Use code execution "whenever the model needs to
  perform any kind of arithmetic, counting, or calculation" rather than reasoning about
  what it would say. Then break one thing: delete an `<li id="rN">` and confirm
  `cite->source` turns ERROR. Uniform green is a predicate matching nothing, and
  `check_readings` returns early on an unparseable page. If the runner could not run at
  all, the page is ungated and the methods note says so.

## `visual` — twelve renders, all opened, each described

`[measured-family]` The recorded run made 3 render calls and opened **4 images** for a
five-surface artifact. SKILL.md:576 says it already — **"Open the renders yourself
first"** — and :579 names the failure: "reporting success on a page nobody opened".

`[docs]` "Ask the model to describe the images before performing the task in the
prompt", and "point out which parts of the image are most relevant to the prompt." A
prompt can fail "because the model did not understand the image at all, or because it did
not perform the correct reasoning steps afterward" — hence description before verdict.

**Twelve captures, not six**: Phase 9's six passes are three readings × two themes at
1440 and 390. Open every one — rendering a file is not seeing it — and name the band, the
markers and the gutters in a crop before saying anything is wrong with them.

**Set the register in the served source.** SKILL.md:580–583 carries the trap: setting
`.checked` from script does not re-evaluate `:has()` on Obscura, so a scripted toggle
"reports three passes" on one register — a vacuous pass that looks exactly like a real
one. Serve three files, one radio `checked` in each, and report `12 of 12 opened`.

## `authorship` — the claim graph is the limit of truth

`[docs]` Google publishes a strictly-grounded system instruction meant to be used
verbatim where output must not exceed its sources. Its last clause is the one this skill
needs: "If the exact answer is not explicitly written in the context, you must state
that the information is not available." `[derived]` Adopt it for Phases 3 and 6 with the
corpus as the context.

- **A value the sources do not carry is stated as unavailable, not filled** —
  SKILL.md:628 already requires "no public data" rather than a weaker source. And a ratio
  you computed is your claim: a Primer re-expressing `95.4%` as `about 19 in every 20`
  has done arithmetic the graph should record.
- **Never resolve a split to make a register read better.** `[docs]` **Underspecified
  task** asks for "instructions for handling missing data rather than assuming inserted
  data will always be present and well-formed" — a panel disagreement is missing data,
  and the rule is SKILL.md:619: **"A page that resolves everything is a page that hid
  something."**

## `delegation` — cap the spawns, close the forks

`[docs]` A documented Gemini failure is answering correctly while not staying within the
offered options; the fix that worked was to "rephrase the instructions as a multiple
choice question and ask the model to choose an option." `[derived]` This skill forks
constantly — three figure lanes, four image-provenance ranks, the three.js gate's six
tests. Resolve each as a closed enumeration with the choice written into the direction
record or the graph: `Figure f3: lane 2 (compiled), not lane 1/lane 3 — needs a computed
scale`. State a maximum subagent count before Phase 7, and never delegate a check of your
own output. SKILL.md:651 binds one already — **"Subagents never run git operations"** —
and `opus-5-prompting.md` gives it structural form: `--allowedTools` with no git.

## `platform-values` — read the version, do not recall the API

`[docs]` "Your knowledge cutoff date is January 2025." The remedy: "Grounding with
Google Search connects the Gemini model to real-time web content, and should be enabled
whenever the model may need to know obscure or recent facts." `[measured-family]` The one
run shipped Windows 10's accent on a Windows 11 app — a previous-generation published
value returned confidently. `[derived]` The vendor values here that go stale:

| Value | Read it in | Why recall fails |
|---|---|---|
| `@tanstack/charts@0.14.0` API shape | `visualisation.md` §Lane 2 | pre-alpha, tracks unreleased `main`; two traps render a wrong chart with **no error** |
| Mobbin MCP parameter shapes | SKILL.md:248–251 | `search_sections` takes no `platform`; `search_screens` and `search_flows` do |
| INP thresholds and the FID cutover | `page-craft.md` §6 | INP replaced FID on 12 March 2024 |

The chart traps are sharpest: a positional-argument mistake and a called scale factory
each produce a confident, wrong figure with nothing thrown. Run the recipe's own check —
emitted marks against row count, and the tick labels read back.

## C3 and C5 — the retry ceiling, and one worked example

`[measured-family]` Four consecutive invocations of one banned, absent tool, no change
between them. `[docs]` "On *other* errors, you must change your strategy or arguments,
not repeat the same failed call." `[derived]` Two attempts per tool, then change
approach; a permanent error gets one. On Phase 5's Mobbin trawl and Phase 8's icon the
skill already gives the move — say so in the methods note and substitute deliberately.

`[docs]` "We recommend to always include few-shot examples in your prompts", and "you
can remove instructions from your prompt if your examples are clear enough in showing
the task at hand." `[derived]` Which is why every override above hands over a filled
block. Extend it into the run: before writing 41 claims, author **one** at full fidelity
— all three `readings`, `limits`, `support`, `kind` — and measure the rest against it.
Both `readings.md` and `product-verdicts.md` ship a worked JSON row; use those.

## Modules not written

`states` — §11 already ships the grid. `count-contract` — did not fire; C1's ledger
covers it. `injection` — did not fire, and reports arrive via `research_export` from a
trusted MCP rather than an open fetch. `emphasis` — two tokens, in reference prose.

## The methods note, on this family

The skill already requires one (SKILL.md:431). Add these, filled with real numbers:

```
Panel      5 members · read end to end 5/5 · verify_citations 3 · fabrications 0
           plan band $6–14 · actual $9.70 · failed members 1 (CLI startup, $0)
Scopes     41 claims · 123 reading cells (118 written, 5 omitted) · 7 figures · 6 images
Gate       python3 scripts/audit_page.py dist/index.html → 0 error(s), 3 warning(s)
           negative control: removed r14 → cite->source ERROR, so the gate is live
Renders    12 of 12 captured and opened · 3 served files, one radio checked in each
Not run    <the honest list — Mobbin MCP absent, three.js rejected at test 3, …>
```

`[derived]` Those lines are the difference between a report and a claim about one, and on
this family they have to be asked for.
