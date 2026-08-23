# design-craft, calibrated for Gemini

This skill was written against a Claude model's failure modes, and several of its most deliberate
decisions are *removals* — verification scaffolding especially. On this family a removal leaves a
vacuum that fills with something plausible. Read this once, in full, **before** §2 Workflow, then
follow the skill with the overrides below: the canon transfers, the assumption that a rule stated in
prose gets executed does not. design-craft is registered in two marketplaces; this copy
(`fledgeling-plugins`) is canonical, and the `diolog-plugins` mirror is deliberately left without a
copy of this file, because a duplicate drifts with nothing checking it.

## Epistemic status

**`[docs]`** is Google's published guidance, quoted verbatim and gated by `verify_quotes.py`.
**`[measured-here]`** is `Egress Gemini`, 17 Aug 2026 — a Gemini model given a macOS + Windows 11
CI-runner mock brief, invoking **this skill** plus `ux-craft`; **n=1**, read from the written record
(`geminify/references/evidence.md` §1.1) rather than the raw transcript. **`[measured-family]`** is
106 benchmark tasks scoring `gemini-3.7-flash` against `claude-opus-5`, plus the `COD Dossier` run
(n=1). **`[derived]`** is marked in place.

**Name the tier the evidence is about.** Every measured claim here is flash-tier, and **none of it
may be projected onto the Pro tier**, whose thinking default and knowledge floor both differ:
**[docs]** *"If thinking_level is not specified, Gemini 3 will default to high"*, while 3.7 Flash
defaults to `MEDIUM`. On Pro the overrides stand as `[docs]`-grounded discipline and every rate
becomes an open question. This skill's work is what **[docs]** *"complex prompts requiring deep
reasoning, such as multi-step planning, verified code generation"* describes, but raising the level
fixes nothing here — **[measured-family]** paired across the 106 tasks, `high` beat `medium` on 24,
lost on 24, tied on 58.

**Unmeasured on this skill.** No Gemini run of design-craft has been observed *with* this file in
place, so nothing here is known to work. Family- or docs-only besides: the bound ledger (bench
corpus) · the reference-input lever · the artifact-dependency conversion, the capacity pivot and the
read-then-answer rule (`COD Dossier`, n=1 each) · the route-out numbers (different harness, pinned
at `temperature: 0` against Google's own advice) · prerequisite-receipt gating. And **[docs]** the
checklist calls *"conflicting internal references"* a defect — a prompt requiring *"the model to
piece together fragmented instructions from multiple different places"* — which is this file's own
shape, so read it in one pass; every override below names the section it lands on.

## Route out first: three shapes to hand to another model

**[docs]** under **Task outside of model capabilities**: *"Avoid using prompts that ask the model to
perform a task for which it has a known, fundamental limitation."* **[measured-family]** the gap is
not uniform — four of eight work buckets are level with opus, two produce hard zeros — so three of
this skill's deliverables are worth routing:

| shape | the design-craft work it covers | measured |
|---|---|---|
| `static-page` | §18's core output: a self-contained HTML artifact from a prose brief | 22 vs opus's 67; zero on 71% of rows |
| `visual-design` | §6/§17 — judged aesthetic quality of a rendered surface | 35 vs 63 |
| `regression-sensitive` | §19's surgical iteration, where `Everything else stays` is literal | 42 vs 65 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape static-page
```

Omitted: `brownfield-integration`, because §4 *reads* a codebase rather than refactoring a multi-file
repo under several acceptance criteria; and the level buckets, because naming them would route away
work this family does as well as opus — `accessibility` 64 vs 69 (so §10's audit stays here),
`react-ui` 63 vs 69, `algorithmic` and `greenfield-module` 75 vs 75. Where the work stays anyway,
this block's value is naming what to distrust first.

## The central override: every categorical noun becomes a count

**[measured-here]** every requirement the brief *enumerated* was delivered — twelve named features,
all present. Every requirement named *categorically* was delivered once or not at all: all surfaces
→ **5** · all states → **1**, the populated one · all menus → **0** · all user flows → **0** · all
actions → one generic `triggerAction()` toast for the whole app. The Claude comparison on a
near-identical brief: 10 surfaces × 5 states × 2 platforms.

**[docs]** Google names both mechanisms. Under **Ambiguity**: *"Avoid using subjective or relative
qualifiers that lack a concrete, measurable definition. Instead, provide objective constraints (for
example, 'write a summary of 3 sentences or less' instead of 'write a brief summary')."* Under **Too
many tasks**, a prompt asking *"the model to perform several distinct cognitive actions in a single
pass … is likely trying to accomplish too much."* `All surfaces, states, menus, flows and actions` is
five cognitive actions over five ambiguous nouns, so the collapse is over-determined. §10 already
knows this — a categorical instruction (`"all states accessible"`) is `improvised to zero, and has
been` — but here that sentence governs the **build**, not the audit. The scan found **124** such
quantifiers over countable deliverables across this skill and its 33 references, led by §2.5 (`every
unit`, `each capture`), §10 (`every control`, `every animation`), §14 (`each component`) and §17
(`all interaction` states). Write the inventory in before the markup:

```
SURFACES (n=10):   overview · runners · queue · job detail · isolation · peers · activity ·
                   quarantine · github · settings
STATES (n=5 each): ideal · loading · empty · partial · error      → 10 × 5 = 50 cells
PLATFORMS (n=2):   macOS · Windows 11                             → 100 cells
MENUS (n=16):      9 macOS menu-bar · 1 Windows app · 3 context · status popover · 2 field
FLOWS (n=10, 28 steps): pair-out(4) pair-in(3) cancel(3) clear-queue(2) unpair(2) self-test(2)
                   repair(4) recover(1) eula(1) onboarding(6)
INTERACTIVE (n=?): counted off the skeleton — hover/focus-visible/active/disabled each, plus
                   loading where §11 says async                   → 5 states each
```

If the brief gives no numbers, **derive them and state them** from the product's docs, data model or
route table: a declared count is a contract, a categorical noun is not. §19's `Deliver the whole
count` already locks the unit count; extend it down to the **cells** and report the fraction. `48 of
50 state cells rendered, 2 n/a (no async here)` is a result; `All states designed` is the sentence
that shipped one state.

## The bound ledger: the same failure pointing the other way

**[measured-family]** across the 106 tasks, Gemini's failing UI assertions were 58% bound-shaped
(`exactly N`, `no`, `not`, `only`) at `medium` and **86%** at `high`, against **8%** for opus. The
most-repeated rule — `has exactly one soft elevation shadow` — failed on *every card and every toast
in its set*, on a run that passed 37 of its 39 other assertions. The shape is over-delivery: a stated
maximum exceeded while everything asked for is present, so it survives every check that looks at what
you did. That rule is §6 word for word — `shadows with an offset and a soft blur, from one light
source`. **[derived]** a bound stated as a prohibition reads as taste, and taste is what the default
idiom overrides, so convert each of the scan's **43** bounds into a counted property with a readback
and report `N of N instances within bound`. **[docs]** Google treats these as a component in their own
right — *"Restrictions on what the model must adhere to when generating a response, including what
the model can and can't do"* — and the **Recap** is where they go: a *"Concise repeat of the key
points of the prompt, especially the constraints and response format, at the end of the prompt."*
This ledger is that recap, carrying values:

| instance | property | bound (§) | readback | observed | within? |
|---|---|---|---|---|---|
| `.card` ×7 | elevation shadows | exactly 1 (§6) | count comma-separated layers in the winning rule | `0 1px 2px …, 0 8px 24px …` (2) | **no** |
| `h1.hero` | `clamp()` max | ≤ 6rem/96px (§8) | `getComputedStyle($0).fontSize` at 1440 | `104px` | **no** |
| transitions | duration | 0.2–0.3s, never `all` (§11) | `transitionDuration` + `transitionProperty` | `0.25s`, `background-color` | yes |

Known limits says `boxShadow` returns empty on Obscura, where `absent ≠ unset`, so read that bound off
the **source** — count the layers in the rule that wins the cascade — never off the computed value.
Same for `outline`, `flex`, `backgroundImage` and `textTransform`.

## Verification is asked for here, not assumed

**[docs]** *"Include specific verification steps in either the system instructions or your prompts
directly."* Google's agentic template spends two of nine rules on it — *"Review your output against
the user's task"* and *"Verify your claims by quoting the exact applicable information"*. The house
style around this skill strips verification scaffolding because Opus 5 over-verifies when told to
double-check; **do not inherit that removal.** **[measured-here]** what filled the vacuum: a
self-written `DESIGN-REVIEW.md`, five rows, all `PASS`. *Engine Verified: Google Chrome via
`browser-use` CDP Harness* — banned by that repo, not installed, failed all four invocation attempts,
no harness ever ran. *100% pass rate on contrast* — no probe executed; measured afterwards, every
primary button 3.65:1 and one `+` glyph at **1.00:1**, the same colour as its own background,
invisible. Five surfaces × the review's eight per-surface stages is 40 cells; the document had five
rows. That is a model completing a *shape* whose procedure was never specified, which is why every fix
here is a command whose output gets pasted. Run `python3 scripts/design-lint.py <file>` and **paste
the output** — it computes WCAG from source across hex, `rgba()`, `hsl()` and `oklch()`, follows
tokens to `:root`, composites `opacity`, fails at critical. Then:

1. **A number carries its command, and a zero denominator is not a pass.** `checked=41 failures=2` is
   a result; `failures=0` alone is not, `100% pass` is not a measurement, `checked=0` is a gate that
   never ran. If you cannot paste the output, write `not measured`. **[docs]** *"Gemini's code
   execution tool enables the model to generate and run Python code, and should be enabled whenever
   the model needs to perform any kind of arithmetic, counting, or calculation."*
2. **Prove the gate can fail, and gate the prerequisites too.** `design-lint.py --selftest` exits 3
   when a rule can no longer fire; **[measured-family]** geminify's own quote gate once went green
   across every file because a normalisation step had taken the checked count to zero. And on `COD
   Dossier` an auditor validated tags, citations and contrast with *zero* checks on whether the
   upstream skills ran, so skipped invocations passed with exit 0 — confirm the files each pass was
   meant to leave (below) exist and are non-empty, and say so when they do not.
3. **Never let the artifact assert its own verification.** A `Verification Status: Verified & Tested`
   column is a property claim with nothing behind it: record the probe, the denominator and the date,
   or record nothing. `contrast-unmeasurable` goes into the note verbatim.

## Skill composition is a file dependency, not a lens

**[measured-family]** `COD Dossier` was told every design decision `goes through design-craft with
ux-craft's lens` and invoked **neither**. Its own diagnosis named the mechanism: the constraints were
already in context and the code step depended on no file those skills produce, so it read the
instruction as a qualitative standard satisfied by writing compliant-looking code — a shape reported
outside this repo too, on the Pro tier. Two instructions here have that phrasing: §2.5 / autonomous
mode (`every unit goes through references/unit-critique-gate.md at its stated round budget`) and §16
(ux-craft as a `standing dependency, not an optional extra`). **[docs]** the remedy is chaining:
*"make each step a prompt and chain the prompts together in a sequence"*, where *"the output of one
prompt in the sequence becomes the input of the next prompt."*

```javascript
await Skill({ skill: "ux-craft:ux-craft" })          // → UX.md: flows, states, error paths
// direction.json: visitor mode · palette · type ramp · the bound table above
await Read({ file_path: "UX.md" })                   // before any markup exists
await Write({ file_path: "runner-console.html", … }) // unit 1, then lint it
await Read({ file_path: "critique-01.md" })          // unit 2 starts from unit 1's findings
```

Those files are cheap and they are what makes a pass unskippable. Then build in passes, one per axis:
surfaces, then a states pass across them, then menus, then flows — a single pass asked to satisfy all
five satisfies the first.

## Look, and prove you looked

**[measured-here]** 3 render calls and **4 images opened** for 5 surfaces × 2 platforms, against
roughly 40 for the Claude comparison's 100 cells — and what those caught (overlays landing 1000px
off-screen, labels spilling their buttons, a stepper whose highlighted step disagreed with its own
body) is the class no source reading finds. §2.5 already says `a screenshot enters your knowledge
only when you open it`; here it needs a denominator rather than `inspect once in a batched round`. So:
**≥1 capture per surface × state × platform**, all opened, fraction reported — `100 of 100 cells
captured, 100 opened`. They are cheap and the batch is one round.

**[docs]** Then describe the crop before judging it: *"Ask the model to describe the images before
performing the task in the prompt"*, and *"To improve the response, point out which parts of the
image are most relevant to the prompt."* Where a verdict looks wrong, their disambiguation step
separates *"the model did not understand the image at all"* from *"it did not perform the correct
reasoning steps afterward"*, so ask what is in the image before arguing with the verdict.

Then ask the crop `what is wrong with this?`, never `is this done?`, and name three candidate failure
modes for that component, ruling each out by pointing at pixels, or it is unreviewed. And supply a
reference input wherever §4 can find one — **[docs]** *"For UI generation, the model shows high
design adherence and parity based on a reference input, whether it's a screenshot, an image, or a
full design system."* §4's design-system library and §2's Mobbin trawl are exactly that; every
static-page task in the benchmark was a prose brief with none. Unmeasured, but the documented strong
path: prefer it.

## Tool discipline: two attempts, and read before you answer

**[measured-here]** four consecutive invocations of the same banned, absent tool with no change of
strategy; **[measured-family]** four consecutive `Read` calls against a 25k token ceiling before
pivoting to a Python split. **[docs]** *"On *other* errors, you must change your strategy or
arguments, not repeat the same failed call."* So: two attempts per tool, then change approach; a
`command not found` or an erroring `--help` is permanent, so one attempt is the whole budget; a
capacity error pivots on attempt 1 to chunking or line-ranged reads. Read the repo's constraints
first — this house allows exactly one browser driver (Obscura) and names the banned ones.

**[measured-family]** asked a question naming three skills, the `COD Dossier` run answered from memory
without loading any of them, then inverted the error by launching a skill instead of answering.
**[docs]** the knowledge floor is January 2025 for this family and the remedy is grounding:
*"Grounding with Google Search connects the Gemini model to real-time web content, and should be
enabled whenever the model may need to know obscure or recent facts."* Two ordered steps, neither
substituting for the other: **load what the prompt names, then answer it yourself.**

## Values, claims, closed sets, and one worked example

**[measured-here]** eight metric errors in one artifact, including all-caps tracked micro-labels on a
Windows surface whose design system mandates sentence case, and Windows **10**'s `#0078D4` accent on
a Windows 11 app — not a guess, a previous-generation *published* value returned confidently. §6's
tell-list catches web tropes, not wrong-platform values, so for §4 and §6 fill a metric table before
the first line of code: one row per property, each cell carrying its value **and its source tier**
(`read from <file>` / `published at <url>` / `derived, because …`). A cell you cannot tag is a value
you invented, and a second platform needs its own published source or it is a reskin of the first.

For §5's truth rule, **[docs]** Google's strictly-grounded instruction ends on the clause that
matters: *"If the exact answer is not explicitly written in the context, you must state that the
information is not available."* That is §5's honest placeholder in Google's words; demonstration
content is the opposite and stays at full fidelity, labelled synthetic. And **[docs]** a documented
Gemini failure is answering correctly while not staying *"within the bounds of the options"*, fixed
by reframing the task as multiple choice — so resolve visitor mode, aesthetic direction, refinement
vs redesign and output format as closed enumerations written into the artifact: `Visitor mode:
OPERATE (not Persuade/Read/Experience)`. §2's delegation posture needs no strengthening (`Delegate
rarely, and never to check yourself`) and the injection guard the Environment notes ship stays
verbatim. Every block in this file ships filled rather than described, because **[docs]** *"We
recommend to always include few-shot examples in your prompts … you can remove instructions from
your prompt if your examples are clear enough in showing the task at hand"* — so before producing a
set of anything, author **one** at full fidelity, in the artifact, and measure the rest against it.

## What transferred intact, and where §10 and §14 land differently

**[measured-here]** §5's content discipline held — real CIDRs, real port numbers, plausible job IDs,
the Apple licence cap cited by clause, no lorem ipsum, no dead `Learn more` — as did §6's web-slop
tells and every enumerated requirement. Instruction-following was not weak; it was literal.
**[measured-family]** the accessibility bucket scores 64 against opus's 69, so §10 is not a routing
candidate; it is a counting problem. The lint already gates contrast, a removed focus ring, `div
onclick`, an unsized inline SVG, `transition: all`, `:invalid` where `:user-invalid` belongs, and the
absence of any `:focus-visible` rule; the rest of §10 is prose, and prose was improvised to zero —
**[measured-here]** `aria-*` 0 · `role=` 0 · `tabindex` 0 · `:focus-visible` 0 · `:active` 0 ·
`:disabled` 0 · `prefers-reduced-motion` 0 · **12 `<div onclick>`** carrying the whole navigation of
both apps, keyboard-dead. Treat §10 as cells: every interactive element × {hover, focus-visible,
active, disabled} + loading where async, counted and greppable — which is also §11's state list, and
what **[docs]** **Underspecified task** asks for: *"provide instructions for handling missing data
rather than assuming inserted data will always be present and well-formed."* §14 is the other
measurable one: **[measured-here]** 11 CSS custom properties declared and **45 raw hex literals**
alongside them, against the comparison's 102 tokens and 86 `var()` uses, so `A token nothing reads
is not applied` gets a number beside it.

## The delivery note, on this family

Keep the skill's brevity rules — they are not the problem. Add four lines:

```
Inventory:   10 of 10 surfaces · 48 of 50 state cells (2 n/a: no async) · 16 menus · 10 flows
Bounds:      31 of 32 instances within bound — .card ×7 shadow layers = 2, stated 1  [FIX]
Verified:    design-lint.py checked=41 critical=0 major=2 minor=6 · 100 of 100 crops opened
Not checked: motion · print · reduced-motion · type fidelity (SKILL.md Known limits) ·
             1 contrast-unmeasurable pair (gradient ground, .hero__eyebrow)
```

Those four lines are the difference between a review and a claim, and on this family they have to be
asked for.

*Modules the scan earned and this file carries: `visual`, `gate`, `states`, `platform-values`,
`authorship`, `delegation`, `bounded-constraint`, `count-contract`. `emphasis` did not fire — one
token across 4,443 lines — and `injection` fell below the trigger threshold because its guard already
ships verbatim in the Environment notes rather than being described.*
