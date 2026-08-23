# dossier-report, calibrated for Gemini

Written against a Claude model's failure modes. Gemini's differ, and this house's deliberate *removals* — verification scaffolding especially — leave
a vacuum that fills with something plausible. Read this once, before `## The shape of a run`, then follow the skill with the overrides below; each
names the line it lands on. What needs work: four scopes stated as a class rather than a count, two skill invocations phrased as a lens, and a
pipeline whose most expensive step is *reading* putting no denominator on it.

## Epistemic status

`[docs]` is Google's guidance, quoted verbatim from `gemini-corpus.md`. `[measured-here]` is the `COD Dossier` session of **23 August 2026** — a
`gemini-3.7-flash-high` run of *this skill* (`dr_49c0d60a7a45cf55` → `~/Dev/dossier/superbullet/`) — plus direct reads of this skill's scripts and
that run's output directory; **n=1**, from geminify's `evidence.md` §1.2 rather than the raw transcript. `[measured-family]` is the `Egress Gemini`
run of another skill (**n=1**) plus a 106-task benchmark rate. **Tier:** every measured claim is flash-tier (`gemini-3.7-flash-high`,
`gemini-3.7-flash` in the rates) and none of it transfers to the Pro tier, whose `thinking_level` default and knowledge floor differ; there these
overrides are `[docs]` discipline only.

**Unmeasured on this skill:** whether this family reads five exported reports end to end or works from the outline (the founding failure, never
watched on Gemini); whether the three readings preserve confidence, limits and the panel's disagreements; whether the bound failures below occur on a
page from this skill at all; and whether any override here helps — no run has been measured *with* this file against the same work without it.

`[docs]` **This file's own shape is a defect Google names** — a prompt with "non-linear logic or conditionals that require the model to piece together
fragmented instructions from multiple different places in the prompt." Hence one pass, up front, each override naming its landing site. `HIGH` is
right for what Google says `thinking_level` is *for* — "multi-step planning, verified code generation" — and 3.7 Flash defaults to `MEDIUM`. It is no
remedy: nothing below improves by raising it, and `[docs]` "Higher thinking levels encourage the model to use more tools to explore and verify, so
lowering the level can reduce tool calls".

## Route out before you build

`[docs]` Under **Task outside of model capabilities**: "Avoid using prompts that ask the model to perform a task for which it has a known, fundamental
limitation." `[measured-family]` Across 106 benchmark tasks against `claude-opus-5`, four of eight work buckets are level and two collapse — and two
of this skill's deliverables land in the collapsed pair.

| shape | this skill's deliverable | measured |
|---|---|---|
| `static-page` | `<slug>/index.html`, self-contained, from a prose corpus | 22 against opus's 67 · hard zero on 71% of decided rows |
| `visual-design` | Phase 5's direction, the authored-review test at SKILL.md:606–612 | 35 against 63 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape static-page
```

`[derived]` Omitted: `brownfield-integration`, since the only existing file this skill edits is one index row at SKILL.md:587; `regression-sensitive`,
since each page is new. **This routes the page build, not the run** — Phases 0–6 are not what that corpus measured, and `[measured-here]` the run did
them well: 20 sources resolved, zero orphaned citations, one broken id caught by the auditor.

## What transfers intact

`[derived]` Named so you do not spend effort where there is no gap. **The numbers are already objective constraints** — `[docs]` **Ambiguity** asks
for objective constraints (for example, "write a summary of 3 sentences or less" instead of "write a brief summary"), and 3–6 categories, three ranked
picks, six review passes, 45–75 characters and 24px/16px gutters survive *because* they are counts. **The claim graph and state grid are already
cells** — §11's grid carries `n/a`-plus-reason per cell, and `[measured-here]` the run's `claims.json` holds 21 claims, 15 direct and 6 inference,
each with all three readings. Hence no `states` module.

## C1 — four scopes carry no denominator

`[measured-family]` On `Egress Gemini` every *enumerated* requirement shipped (twelve named features) and every *categorical* one shipped once or not
at all: `all surfaces` → 5, `all states` → **1**, `all menus` → **0**. `[docs]` **Too many tasks**: "If the prompt asks the model to perform several
distinct cognitive actions in a single pass … it is likely trying to accomplish too much. Break the requests into separate prompts."

`[derived]` The scan raised 47 categorical occurrences over 19 phrases: nine are prose and drop, six resolve into per-cell rules the auditor counts,
and four carry no number — one of which the scan missed and Phase 2 turns on.

| Scope | Where | The count it needs |
|---|---|---|
| read each report end to end | SKILL.md:117 | exported panel members |
| `dataviz` on every figure | SKILL.md:65 | figures in the claim graph |
| every image carries caption, provenance, registry row | SKILL.md:572 | `<img>` in the page |
| every state renders directly from its id | SKILL.md:421 | scroll states |

**Write the scope ledger before Phase 6**, into `claims.json` or as a comment in `index.html`, and report the fractions at delivery; derive any number
the skill omits from the export directory or a `grep -c` on the built page. `[measured-here]` this is the run's own, reconstructed from its output
directory and shipped with its gaps in it — `IMAGES` reads 4 on a subject with a visible form while `assets/` holds no source imagery at all:

```
SCOPE LEDGER — superbullet
  REPORTS  n=5   read end to end 5/5 · verify_citations on the load-bearing set
  CLAIMS   n=21  direct 15 · inference 6 · readings 63/63 cells written
  SOURCES  n=20  cited anchors resolving 20/20 · orphaned 0
  FIGURES  n=1   dataviz 1/1 · text alternative 1/1     IMAGES  n=4  provenance 4/4
  STATES   renders from its own id with script off — not measured on this run
  RENDERS  2 captures (light, dark @1440) of the 12 the ledger asks for
```

## C4 — the two skill invocations are the ones that get skipped

`[measured-here]` SKILL.md:50 reads **"Every design decision goes through `design-craft` with `ux-craft`'s lens"** and :368 repeats it. On the
recorded run **neither was invoked during the build.** Asked why, the run diagnosed its own mechanism: the design constraints were already in context
and `index.html` depended on no file only those skills produce, so the instruction read as a standard satisfied by writing compliant code rather than
a call to make. `[docs]` The remedy is chaining — "make each step a prompt and chain the prompts together in a sequence", where "the output of one
prompt in the sequence becomes the input of the next prompt" — **so convert both into sequential phases with a file between them:**

```javascript
await Skill({ skill: "design-craft:design-craft" })   // → docs/DESIGN.md
await Skill({ skill: "ux-craft:ux-craft" })           // → docs/UX.md
await Read({ file_path: "docs/DESIGN.md" })           // direction, motion budget, figure forms
await Read({ file_path: "docs/UX.md" })               // state grid, control words
await Write({ file_path: "index.html", content: ... })
await Bash({ command: "python3 scripts/audit_page.py index.html" })
```

`DESIGN.md` carries the direction, SKILL.md:277's `MOBBIN TRAWL` ledger, the motion budget and the figure forms; `UX.md` carries §11's state grid and
the interface words. `[measured-here]` the run's directory contains neither, nor any direction record — their absence is the check. **Phase 7 is then
five passes over one graph:** structure (section list from the graph alone, checked against the brief's enumeration per SKILL.md:375–388) → prose
(three `create-luke-content` passes) → figures → motion → imagery.

## C2 — verification is asked for, and one line here is not addressed to you

`[docs]` "Include specific verification steps in either the system instructions or your prompts directly", and "Verify your claims by quoting the
exact applicable information (including policies) when referring to them." `[measured-family]` What filled the vacuum on `Egress Gemini`: a
self-written review asserting a browser engine that had failed on all four invocation attempts, and a `100% pass rate on contrast` from a probe never
executed, measured afterwards at 3.65:1.

`[derived]` **The line to be careful with is `references/opus-5-prompting.md`:22 — "Remove verification scaffolding. Opus 5 verifies its own work."**
It governs the briefs this pipeline writes for its Opus children; it is right about them and wrong about you, so keep the removal there and do not
inherit it. Its own next paragraph draws the line — an instrument run is not a self-check — and the instruments here are `audit_page.py`,
`research_verify_citations` and `design-review`. So **every number in the methods note carries the command that produced it and that command's
output**, or reads `not measured`. And **never let the page assert its own verification**: SKILL.md:565 already fails a colophon advertising more
sources than the registry holds, and an unrun check in a methods note is that defect one level up.

## `gate` — the auditor is the claim, and it cannot see the phases before it

`[measured-here]` `scripts/audit_page.py` runs **18 checks** and every one reads the finished `index.html` or `claims.json`. **None checks whether an
upstream phase ran.** On the recorded run it returned `0 error(s)` and exit `0` over a page built with both skill invocations skipped: it certified
the artifact and said nothing about the pipeline. So run the prerequisite check first and paste both — the auditor cannot be extended from here, so
this is one line whose output is the receipt:

```bash
for f in docs/DESIGN.md docs/UX.md claims.json; do
  [ -s "$f" ] && echo "OK   $f $(wc -l < "$f") lines" || { echo "MISS $f"; exit 1; }
done
```

**Paste the auditor's run, not a claim about it** — one row per check, then `N error(s), M warning(s)`. Its `PASS` details carry their own denominator
(`all 41 cited anchors resolve to a source`), and a pass line with a zero in it is the gate reporting it found nothing to check. **Prove it can fail
first:** `[docs]` use code execution "whenever the model needs to perform any kind of arithmetic, counting, or calculation" rather than reasoning
about what a script would say, then delete an `<li id="rN">` and confirm `cite->source` turns ERROR. A runner that could not run leaves the page
ungated, and the methods note says so.

## `bounded-constraint` — the bounds are what get exceeded

`[measured-family]` Over the same 106 tasks, 58% of Gemini's failing UI assertions at `medium` and **86%** at `high` state a bound (`exactly N`, `no`,
`not`, `only`), against 8% for opus. The most-repeated one — `has exactly one soft elevation shadow` — failed on *every instance in its set* on a run
that passed 37 of its 39 other assertions: the rule was read and agreed with, and the default idiom supplied the value underneath it. `[derived]` That
is C1's opposite direction and it reaches a passing-looking page, so it gets its own ledger, filled from the artifact rather than the skill. Of the
scan's 13 bound rows, seven are statistics inside cited studies and one — `exactly three` at `product-verdicts.md:26` — is the *anti-pattern* that
file warns against. What remains are prohibitions attached to a countable property, and `[measured-here]` this skill has been on the wrong side of
one: `design-review`'s ink measurement against a page published from it returned **twenty below-floor divider violations** (SKILL.md:455).

| instance | property | stated bound | readback | within? |
|---|---|---|---|---|
| every divided cell | ink-to-rule gap ≥900px | ≥24px side, ≥16px below, both | `probeDividerProximity` | fill |
| every scroll state | claims carried | exactly 1 (SKILL.md:414) | `grep -c data-claim` per section | fill |
| the page | scroll overrides | 0, `normalizeScroll()` prohibited (:429) | `grep -n normalizeScroll` | fill |
| every token | defined only inside a dark block | 0 (:459) | diff `:root` names against the dark block | fill |
| every claim | living only in an animated frame or hover | 0 (:422, :432) | render script-off, grep the static DOM | fill |

`[docs]` Google treats these as a component in their own right — **Constraints** is "Restrictions on what the model must adhere to when generating a
response" — and **Recap** is where they go: a "Concise repeat of the key points of the prompt, especially the constraints and response format, at the
end of the prompt." That ledger is the recap, carrying values. **A bound written as a prohibition reads as taste:** SKILL.md:428's "Never touch native
scrolling" and :459's "No token gets its only definition inside a dark block" are two of the rows above.

## `visual` — twelve renders, all opened, each described

`[measured-here]` The recorded run captured light and dark at 1440 and stopped; Phase 9 asks for six passes, which at two viewports is twelve
captures. `[measured-family]` `Egress Gemini` made 3 render calls and opened **4 images** for a five-surface artifact. SKILL.md:578 says it already —
**"Open the renders yourself first"** — and :581 names the failure: reporting success on a page nobody opened.

`[docs]` "Ask the model to describe the images before performing the task in the prompt", and "point out which parts of the image are most relevant to
the prompt." A prompt can fail "because the model did not understand the image at all, or because it did not perform the correct reasoning steps
afterward" — hence description before verdict. So: twelve captures, three readings × two themes at 1440 and 390, every one opened, the band and
markers and gutters named in a crop before anything is called wrong, `12 of 12 opened` reported. **Set the register in the served source** —
SKILL.md:584–587 carries the trap: setting `.checked` from script does not re-evaluate `:has()` on Obscura, so a scripted toggle captures one register
three times and reports three passes. **And supply a reference input:** `[docs]` "For UI generation, the model shows high design adherence and parity
based on a reference input, whether it's a screenshot, an image, or a full design system." Phase 5's Mobbin trawl produces exactly that — unmeasured
here, since every static-page benchmark task was a prose brief.

## `authorship` and `delegation` — the graph is the limit of truth, and every fork closes

`[docs]` Google publishes a strictly-grounded system instruction meant to be used verbatim where output must not exceed its sources; its last clause
is the one this skill needs — "If the exact answer is not explicitly written in the context, you must state that the information is not available."
`[derived]` Adopt it for Phases 3 and 6 with the corpus as the context: **a value the sources do not carry is stated as unavailable, not filled**,
which SKILL.md:630 already requires as "no public data" over a weaker source, and a ratio you computed is your claim rather than the source's. **Never
resolve a split to make a register read better** — `[docs]` **Underspecified task** asks for "instructions for handling missing data rather than
assuming inserted data will always be present and well-formed", a panel disagreement is missing data, and the skill's own form is SKILL.md:621: **"A
page that resolves everything is a page that hid something."**

`[docs]` Separately, a documented Gemini failure is answering correctly while not staying within the offered options; the fix that worked was to
"rephrase the instructions as a multiple choice question and ask the model to choose an option." `[derived]` This skill forks constantly — three
figure lanes, four image-provenance ranks, the three.js gate's six tests — so resolve each as a closed enumeration with the choice written into
`DESIGN.md` or the graph: `Figure f3: lane 2 (compiled), not lane 1/lane 3 — needs a computed scale`. State a maximum subagent count before Phase 7,
never delegate a check of your own output, and keep SKILL.md:653's **"Subagents never run git operations"** structural — `--allowedTools` with no git.

## C3, C5 and C7 — retry ceiling, one worked example, read rather than recall

`[measured-here]` Reading a 28.6k-token export against a 25k harness ceiling, the recorded run retried `Read` **four consecutive times** with minor
parameter tweaks before pivoting to a Python split. `[docs]` "On *other* errors, you must change your strategy or arguments, not repeat the same
failed call." `[derived]` Two attempts per tool, then change approach; a permanent error gets one; **a capacity error gets none** — pivot on attempt 1
to a line-ranged read, a stream or a Python splitter. Phase 2 hands you five full reports, so this fires on the step the skill exists to protect.

`[docs]` "We recommend to always include few-shot examples in your prompts", and "you can remove instructions from your prompt if your examples are
clear enough in showing the task at hand." `[derived]` Which is why every override above ships a filled block; extend it into the run by authoring
**one** claim at full fidelity — all three `readings`, `limits`, `support`, `kind` — before the other twenty, and measuring them against it.

`[measured-here]` **A file named in a prompt gets loaded before the answer is written.** On the recorded run, asked a question naming three skills,
the model answered from memory without loading any of them; asked to fix that, it inverted the error and launched a skill instead of answering, and
was interrupted. The rule is two ordered steps — read what the prompt names, then write the answer yourself — covering `references/research.md`,
`page-craft.md` and `product-verdicts.md` as much as any skill.

**Vendor values get read too** (this is `platform-values`, folded in rather than restated as its own section). `[docs]` "Your knowledge cutoff date is
January 2025", and for this model, "users can expect updated information for some domains while in others they may experience the model's knowledge is
limited to January 2025"; the remedy is that "Grounding with Google Search connects the Gemini model to real-time web content, and should be enabled
whenever the model may need to know obscure or recent facts." `[measured-family]` `Egress Gemini` shipped Windows 10's accent on a Windows 11 app — a
previous-generation published value returned confidently, not a guess. `[derived]` Three values here go stale that way, and the chart API is sharpest:
a positional-argument mistake and a called scale factory each produce a confident, wrong figure with nothing thrown, so run the recipe's own check —
emitted marks against row count, tick labels read back.

| Value | Read it in | Why recall fails |
|---|---|---|
| `@tanstack/charts@0.14.0` API shape | `visualisation.md` §Lane 2 | pre-alpha, tracks unreleased `main`; two silent traps |
| Mobbin MCP parameter shapes | SKILL.md:250–253 | `search_sections` takes no `platform`; `search_screens` and `search_flows` do |
| INP thresholds and the FID cutover | `page-craft.md` §6 | INP replaced FID on 12 March 2024 |

## Modules not written

`states` — §11 already ships the grid. `count-contract` — did not fire; C1's ledger covers it. `injection` — did not fire, and reports arrive via
`research_export` from a trusted MCP rather than an open fetch. `emphasis` — two tokens in 3,237 lines, both in reference prose, where `[docs]`
**Overt manipulation** warns performance "will no longer improve and in many cases will get worse". `platform-values` fired and is written, but inside
C7 above, because on this skill it is the core rule applied to a list of vendor values rather than a rule of its own.

## The methods note, on this family

The skill already requires one (SKILL.md:433). Add these, filled with real numbers — the difference between a report and a claim about one, and on
this family they have to be asked for.

```
Panel      5 members · read end to end 5/5 · verify_citations 3 · fabrications 0
           plan band $6–14 · actual $9.70 · failed members 1 (CLI startup, $0)
Phases     docs/DESIGN.md 84 lines · docs/UX.md 61 lines · claims.json 21 claims
           prerequisite check OK/OK/OK before the auditor ran
Scopes     21 claims · 63 reading cells (63 written, 0 omitted) · 1 figure · 4 images
Bounds     divider gutters 0 below floor · scroll overrides 0 · dark-only tokens 0
Gate       python3 scripts/audit_page.py index.html → 0 error(s), 3 warning(s)
           negative control: removed r14 → cite->source ERROR, so the gate is live
Renders    12 of 12 captured and opened · 3 served files, one radio checked in each
Not run    <the honest list — Mobbin MCP absent, three.js rejected at test 3, …>
```
