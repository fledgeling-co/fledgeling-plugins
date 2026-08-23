# mac-craft, calibrated for Gemini

Read this in one pass before § Knowledge sources, then run the skill as written. Each
override names the section of `SKILL.md` it lands on. **[docs]** Under **Conflicting
internal references**, Google asks you to avoid a prompt whose logic requires the model to
"piece together fragmented instructions from multiple different places in the prompt" —
which is what a conditional side-file is, so this one is short and adds nothing the skill
already enforces.

The delta is small: `references/model-calibration.md` is already a Gemini calibration for
this pipeline and `scripts/mock_check.py` already turns seven prose audits into an exit
code. What is left is the gap between a check firing once per mock and a scope stated per
control — and a class of stated *limit* nothing here reads back at all.

## Route out before you build

Two of the three shapes mac-craft ships are where the corpus measured this family furthest
behind. Pick the lane before step 5, not after the gate.

| this skill's work | shape | measured |
|---|---|---|
| the self-contained HTML/CSS mock — step 5's default deliverable | `static-page` | 22 against opus's 67 |
| the committed direction, signature move, lookalike and slop passes | `visual-design` | 35 against 63 |
| a targeted edit under § Running this twice, everything else untouched | `regression-sensitive` | 42 against 65 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape static-page
```

**[docs]** The checklist says it under **Task outside of model capabilities**: "Avoid using
prompts that ask the model to perform a task for which it has a known, fundamental
limitation." **[measured-family]** `geminify/references/evidence.md` §2.1 — static-page is not
a lower score but a hard zero on 71% of decided rows at `medium`.

**Two rows are absent, and half this skill gets none.** `brownfield-integration` does not
apply: step 0 *reads* `Assets.xcassets` and existing SwiftUI views and never edits them, so
mac-craft authors new files rather than integrating with old ones. The **review** half — `why
doesn't this feel like a Mac app`, the audit rows, the native-tells score — gets no row,
because the corpus watched a model build and says nothing about how it judges. Where no lane
is available this block still earns its place, by naming what to distrust first.

## Epistemic status

| Tier | Used here | Source |
|---|---|---|
| `[docs]` | yes, throughout | Google's published Gemini 3 guidance, quoted verbatim |
| `[measured-family]` | yes — **n=1** plus a 106-task rate | `Egress Gemini`, 2026-08-17, a Gemini run on a two-platform Mac/Windows mock invoking this skill's **predecessor** (`mac-design-studio`); and `geminify/references/evidence.md` §2 |
| `[measured-here]` | no | no Gemini run of `mac-craft` as it stands has been recorded |
| `[derived]` | yes | reasoning from the two above, plus reading `scripts/mock_check.py` |

**Which model these numbers are about.** Every measured rate here is flash-tier —
`gemini-3.7-flash`, plus one `3.7-flash-high` session — and none may be projected onto the Pro
tier, whose defaults differ: **[docs]** "If thinking_level is not specified, Gemini 3 will
default to high", against the 3.5 Flash release note that "The default thinking effort is now
medium, changed from high in Gemini 3 Flash Preview." On Pro, read every override as
`[docs]`-grounded discipline and every rate as an open question. The family evidence otherwise
sits unusually close to this target: the measured artifact *was* a Mac mock, so the 3.65:1
primary buttons and the 1.00:1 glyph were measured on the thing this skill makes — still one
run, on the predecessor file, and not a rate.

**Unmeasured on this skill:** no Gemini run against the rebuilt `SKILL.md` or against
`mock_check.py`, so every claim that the gate closes the measured gap is `[derived]`; no
comparison of a run *with* this file against one without it; the single-accent bound, the
10pt floor and the Liquid-Glass placement rule never measured on this family, so Override 2
imports its rate from a different corpus; and the direction catalogue, essence test,
lookalike check and variety discipline untested here in either direction.

## What transfers intact — do not re-derive these

- **The retry ceiling** — `model-calibration.md:92-98` already says two attempts, one for a
  `command not found`, and never re-pitch a refused capability. **[docs]** matching "change
  your strategy or arguments, not repeat the same failed call." One extension: a hard
  capacity error — a `Read` refused for exceeding a token ceiling on `kit-macos-27.md` —
  pivots on attempt **1** to line-ranged reads or a splitter, never on attempt 2.
- **`thinking_level`** — `model-calibration.md:65-67` already sets it. **[docs]** a committed
  multi-surface design with a seven-row audit is what `HIGH` is for — "multi-step planning,
  verified code generation" — and 3.7 Flash defaults to `MEDIUM`. Raise it for that reason
  only, never as a fix for anything below: paired over 106 tasks, `high` beat `medium` on 24,
  lost on 24 and tied on 58.
- **Recall is not a source** — `model-calibration.md:54-59` states the January 2025 floor and
  `SKILL.md:171` makes an untaggable cell a defect. **[docs]** the remedy is grounding:
  "Grounding with Google Search connects the Gemini model to real-time web content, and
  should be enabled whenever the model may need to know obscure or recent facts." The rule
  that breaks first is `SKILL.md:177`, on a second platform: **[measured-family]** the run's
  Windows theme was the macOS theme with the caption buttons moved and a 3px bar added —
  same 48px titlebar, no Mica, and Windows **10**'s `#0078D4` accent on a Windows 11 app.
  Not a guess; a superseded published value returned confidently, which is what **[docs]**
  "The knowledge cutoff date for Gemini 3.7 Flash is March 2026 — users can expect updated
  information for some domains while in others they may experience the model's knowledge is
  limited to January 2025 (in line with the Gemini 3 Model Family)." looks like from outside.
  `mock_check.py [metrics]` cross-checks only `kit` rows, so nothing catches a reskin for you.
- **The untrusted-content guard** — `SKILL.md:275-276` ships the verbatim sentence for any
  agent brief and `SKILL.md:278-279` caps the agent budget. **[docs]** that is the **Prompt
  injection risk** control: "Check if there are explicit safeguards surrounding untrusted
  user input that is inserted into the prompt, as this can be a major security risk." One
  addition, and no `injection` section: never delegate a check of your own output.
- **Verification asked for, not assumed** — `SKILL.md:206` already says to paste the counters
  verbatim and that `examined=0` is never a pass. **[docs]** Google's own instruction,
  "Include specific verification steps in either the system instructions or your prompts
  directly," discharged by an exit code rather than prose.
- **The register.** The scan found zero shouted directives in 1,585 lines across `SKILL.md`
  and its references. Nothing to de-escalate; no `emphasis` module.

## Override 1 — the quota ledger, because a gate that fires once is not a denominator

**Lands on:** step 5 (build the artifact) and step 6 (gate it).

`SKILL.md:188` reads `Every control carries hover/focus/active/disabled`, and
`mac-essence.md:21` names six async states. **[derived]** `check_keyboard` in
`scripts/mock_check.py` FAILs only when `:focus-visible` **and** `:focus` are both zero
across the whole file, and `check_states` emits a NOTE per missing pseudo-class at
`examined=1` — so **one** focus rule and **one** `:hover` rule anywhere clear both. Those
two checks are a presence signal; the scope in the sentence is per control, and nothing
counts it. **[measured-family]** that is the gap the run fell into — six `:hover` rules
total for two entire apps, `:focus-visible` 0, `:focus` 0, `:active` 0, `:disabled` 0, and
12 `<div onclick>` carrying the navigation.

**[docs]** Google's remedy is a number rather than a scope word. Under **Ambiguity**:
"Avoid using subjective or relative qualifiers that lack a concrete, measurable definition.
Instead, provide objective constraints (for example, 'write a summary of 3 sentences or
less' instead of 'write a brief summary')."

So write this into the spec **before** the first line of CSS, filled as it is here — a
two-surface commission, light and dark:

```
mac-craft:quota
axis                        formula                          due   built
surface × appearance        2 surfaces × 2 appearances         4     4
async states                6 × 2 async surfaces              12    11 + 1 n/a (no partial-load path)
control states              4 × 14 interactive controls       56    52 + 4 n/a (static labels, no :disabled)
captures opened             surface × state × appearance      16    16
metric rows, tier-tagged    1 per metric used                  9     9
audit rows                  7 rows × 2 surfaces               14    14
menu-bar commands           1 per toolbar command              6     6
```

Report the fraction in the delivery — `52 of 56 control-state cells, 4 n/a with reasons ·
11 of 12 async cells · 16 of 16 captures opened`. An `n/a` carries its reason or it is an
open cell.

**Run step 5 as passes with a file between them.** **[docs]** Under **Too many tasks**,
"Break the requests into separate prompts", the remedy being to "make each step a prompt and
chain the prompts together in a sequence." The scan flagged no qualitative skill references,
but `SKILL.md:75` phrases `ux-craft` as `a standing dependency, not a conditional one` — the
shape that went unexecuted on the one measured run carrying it
(`geminify/references/evidence.md` §1.2.1), because nothing downstream needed a file only
that skill produces. So make each dependency emit one: direction → `<app-slug>-spec.md`;
structure and metrics → state matrix and tier-tagged token table appended to it, with
`ux-craft`'s trunk-test result; build → the mock written **from that file**, not the brief;
gate and render → counters and captures appended; audits → seven rows each citing a counter
already in the file. A phase that produced no file did not run, and the next phase says so
rather than proceeding on remembered intent.

## Override 2 — the bound ledger, for the limits the gate never reads back

**Lands on:** step 4 (apply the system) and step 6's audit rows.

Override 1 catches a categorical scope collapsing to one instance. This catches the
opposite: a stated *maximum* exceeded on every instance while everything asked for is
delivered — so the artifact looks complete and survives every check that reads what you did
write. **[measured-family]** `geminify/references/evidence.md` §2.2 — 58% of failing UI
assertions at `medium` and **86%** at `high` were bound-shaped, against 8% for opus and 6%
for the OpenAI lane; the most-repeated one, `has exactly one soft elevation shadow`, failed
on *every* card and toast in its set on a run that passed 37 of its 39 other assertions.

mac-craft states its bounds in that exact register: `exactly one saturated moment per view`
(`corpus-evidence.md:54`, canon, 15 members), `10pt hard minimum`, `Liquid Glass on floating
chrome only`, `no magic numbers` (`SKILL.md:180-183`), `no more than two levels` of sidebar
hierarchy (`evidence.md:49`), `arrow cursor in chrome`. **[derived]** `mock_check.py` reads
exactly one of those back — `check_tokens` FAILs above six distinct colour literals outside
the token block. Accent count, glass placement, hierarchy depth and the type floor have no
readback at all.

**[docs]** Google treats these as a component in their own right — "Restrictions on what the
model must adhere to when generating a response, including what the model can and can't
do." — and names where they belong: the **Recap** component is a "Concise repeat of the key
points of the prompt, especially the constraints and response format, at the end of the
prompt." So the ledger sits beside the quota ledger, one row per bound × instance, each
filled from the **produced** value rather than from the rule. Shipped filled:

| instance | property | stated bound | readback | observed | within? |
|---|---|---|---|---|---|
| Accounts, light | saturated accent moments | exactly 1 per view | count painted `var(--accent)` fills in the DOM | 3 — CTA, selected row, sparkline | **no** |
| Accounts, light | Liquid Glass surfaces | floating chrome only | each `backdrop-filter` selector mapped to its element | 2 — toolbar, popover | yes |
| Accounts, light | smallest type | 10pt floor | `getComputedStyle(el).fontSize` per text run | min 11px | yes |
| Sidebar | hierarchy depth | ≤ 2 levels | deepest nested list in the DOM | 2 | yes |
| whole mock | undeclared palette | ≤ 6 distinct literals outside `:root` | `mock_check.py` `[tokens]` counters | `distinct_outside=2` | yes |

Report `N of N instances within bound`, and name which of the skill's own prohibitions you
converted. `avoid heavy chrome` and `exactly one saturated moment` are the same class of
requirement; the first reads as taste and gets treated as taste, so convert it into a counted
property with a readback before building rather than arguing with it afterwards.

## Override 3 — the state matrix is cells with copy, not a list in prose

**Lands on:** step 5, second bullet, and the state matrix in step 7's delivery.

`SKILL.md:188` already distinguishes rendered from specified states. Keep that, and make the
specified half an artifact. **[docs]** Under **Underspecified task**, Google asks you to
"provide instructions for handling missing data rather than assuming inserted data will
always be present and well-formed." A matrix of cells is that instruction; a sentence naming
six states is not. One surface worked in full, as the exemplar the rest are measured against:

```
surface   state     rendered   real copy shipped in the cell
Accounts  ideal     yes        4 accounts, live balances
Accounts  empty     yes        "No accounts yet" · "Add your first account" · illustration
Accounts  loading   spec       skeleton rows ×4, no spinner, 200ms delay before it shows
Accounts  partial   spec       "2 of 4 accounts synced" + per-row retry, list stays usable
Accounts  error     spec       "Couldn't reach Ledgerline. Check your connection." + Retry
Accounts  done      spec       toast "Synced 4 accounts", auto-dismiss 4s, undo not applicable
```

**[docs]** Authoring one instance in full before the set is the strongest single lever
Google names: "We recommend to always include few-shot examples in your prompts", and "you
can remove instructions from your prompt if your examples are clear enough in showing the
task at hand." Their **Missing output format specification** entry adds the corollary — "show
the output structure in your few-shot examples." The same holds one level up: build one
surface in one appearance completely, gate it and look at it before the rest, because a
second surface authored first inherits every defect the gate would have named.

## Override 4 — supply a reference, then describe the crop before scoring it

**Lands on:** step 2's corpus trawl, and step 6 after the gate.

**[docs]** Google's claim for this model is conditional on an input a prose brief does not
carry: "For UI generation, the model shows high design adherence and parity based on a
reference input, whether it's a screenshot, an image, or a full design system." So open the
corpus profile's captures and the `patterns/` skeleton for the surface you are drawing *as
images* before step 5. **[measured-family]** every static-page task in the collapsed bucket
was a prose brief with no reference — the mode Google does not claim — so this is the
documented strong path, unmeasured here; name the references you opened rather than
promising the effect. `SKILL.md:213-217` already asks for one capture per surface × state ×
appearance, all opened, with the fraction reported; **[measured-family]** the run made 3
render calls and opened 4 images for 5 surfaces × 2 platforms, then scored all five PASS.

**[docs]** Google gives a method rather than a caution: "Ask the model to describe the images
before performing the task in the prompt." Their worked example is the whole argument —
"Describe this image." of an airport board returns a one-line caption, while naming the
extraction returns the thirteen rows. Two corollaries stated directly: "point out which parts
of the image are most relevant to the prompt", and, when a verdict looks wrong, a
disambiguation step separating "the model did not understand the image at all" from "it did
not perform the correct reasoning steps afterward".

Per capture, in order: name the chrome height, control heights, casing, radii, focus ring and
the copy you can **see** — then score. `SKILL.md:326-328` is where this pays: a native radio
or checkbox photographs as nothing in this house's browser, and a described crop calls that a
rendering fact rather than a missing affordance.

## Override 5 — prove the gate can fail, and give it its prerequisites

**Lands on:** step 6, `scripts/gate_tests.sh`, and step 7's delivery.

Run the adversarial suite, not only the gate, and paste both:

```
bash scripts/gate_tests.sh                 # 19 mocks, each built to defeat one check
python3 scripts/mock_check.py ledgerline-accounts.html; echo "exit $?"
gate  exit 0  examined=76 failures=0 unresolved=0 contexts=4
```

**[derived]** A green gate and an inert gate are the same output. The signature of an inert
one is uniform numbers across varied inputs — identical `examined=` counts on mocks that
differ — so read the counters against each other, not only against zero. `examined=0` exits 2
by design; record it as unperformed, and never pipe the gate through `grep`, which replaces
its exit code with grep's.

**The gate cannot see what did not happen.** `mock_check.py` takes one HTML path and nothing
else, so a commission missing its `<app-slug>-spec.md`, its token table or its `captures/`
directory still exits 0. **[measured-family]** `geminify/references/evidence.md` §1.2.2 — a
comparable auditor validated its final artifact thoroughly, had no prerequisite check, and
two skipped upstream passes cleared it silently. Paste an existence receipt before the exit
code; a zero or a missing path there is a failed gate whatever `mock_check.py` returned:

```
prereq  spec=ledgerline-accounts-spec.md (68 lines)  token-rows=9  captures/=16 files  gate_tests=19 PASS
```

**[docs]** Where the delivery needs arithmetic — contrast ratios, cell fractions — do it in
code: "should be enabled whenever the model needs to perform any kind of arithmetic,
counting, or calculation." The prose is bounded the same way `SKILL.md:191` bounds the
mock's placeholders — **[docs]** "If the exact answer is not explicitly written in the
context, you must state that the information is not available." A contrast ratio comes from
the gate's output; a native-tells score is documented expectations presented as that, never
as perception research (`SKILL.md:329-331`); and **what you did not check** is never empty,
since `SKILL.md:303-304` already names motion and type fidelity as unverifiable here — its
floor, not its ceiling.

## Override 6 — read what the prompt names, then answer; and the fork is a closed set

**Lands on:** § Knowledge sources and step 2.

**[measured-family]** `geminify/references/evidence.md` §1.2.4 — asked a question naming three
skills, a run answered from memory without loading any of them, then inverted the error and
launched a skill when the user wanted an answer. mac-craft names files constantly: `TASTE.md`,
one cluster profile, the `patterns/` entries for the surfaces being drawn, `ux-craft`'s own
`flows-and-forms.md` at the absolute path `SKILL.md:75` gives. Load-then-answer is two ordered
steps — read every file the prompt or § Knowledge sources names, *then* write the answer —
neither substituting for the other; say which files you opened.

**[docs]** For the direction fork, Google's iteration guidance is to reframe as multiple choice
when a model answers correctly but "didn't stay within the bounds of the options". Present 2–3
directions as A/B/C with one paragraph and one trade-off each, take the user's letter, and write
the chosen letter and its name into the spec before building — `SKILL.md:126-127` already
requires that identity to hold for the rest of the session.

## Modules considered and not written

`injection` and `emphasis` did not fire on the scan, and both are covered under what transfers
intact. `count-contract` did not fire either: this skill promises tier tags and audit rows, not
a count — which is why Override 1 creates one rather than extends one. `authorship` fired and
is discharged inside Override 5 rather than by a section of its own.
