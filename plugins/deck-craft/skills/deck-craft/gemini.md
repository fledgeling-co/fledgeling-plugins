# deck-craft, calibrated for Gemini

Read this in one pass before §1 Route to a target, then follow the skill with these overrides;
each names the section it lands on. Two of this skill's rules are already right for this family —
§6's slide count as a contract, and §7's runner that exits non-zero rather than passing on an empty
result — and everything below extends those into the parts still written as prose. **This is the
canonical copy:** `deck-craft` is registered in two marketplaces, this file belongs to the
`fledgeling-plugins` copy, and the `diolog-plugins` mirror is deliberately left without one.

## Epistemic status

`[docs]` is Google's guidance quoted verbatim, and is the stronger tier. `[measured-family]` is
Gemini runs that were **not** this skill: two recorded sessions (a two-platform UI mock, a
research-and-authoring pipeline) plus 106 benchmark tasks scored against `claude-opus-5`.
`[derived]` is reasoning from those. Every measured number is flash-tier — `gemini-3.7-flash` on
the benchmark, `gemini-3.7-flash-high` in one session — and none of it is to be projected onto the
Pro tier, where these overrides stand as `[docs]`-grounded discipline and every rate is open.
Defaults drift inside the family too: **[docs]** *"If thinking_level is not specified, Gemini 3
will default to high"*, while the corpus table puts 3.7 Flash at `MEDIUM`. `HIGH` is what Google
describes as being for *"multi-step planning, verified code generation"*, which is this work — but
no remedy for anything below: paired across 106 tasks, `high` beat `medium` on 24, lost on 24.

**Unmeasured on this skill.** No recorded Gemini run of `deck-craft` exists, so nothing here was
observed on a deck this skill built. The reference-input lever (§3) is `[docs]` only, §5's
fabrication passage was not exercised either way, and the `.pptx` / `lecturn.deck/1` and Diolog
template-assembly lanes have no comparable shape in the corpus. **No evidence this file helps**: no
run has been measured with a `gemini.md` against the same work without one. **[docs]** A conditional
side-file is itself the *"Conflicting internal references"* shape the checklist warns about —
instructions the model must *"piece together"* … *"from multiple different places"* — hence one pass.

## Route out before you build

**[docs]** Under **Task outside of model capabilities**: *"Avoid using prompts that ask the model
to perform a task for which it has a known, fundamental limitation."* **[measured-family]** On
benchmark `diolog-2.0`, 106 tasks, the gap is not uniform, so shape matters more than headline:

| shape | deck-craft work it describes | gem | opus | n |
|---|---|--:|--:|--:|
| `deck` | the build lane, all three targets | 49 | 61 | 8 |
| `static-page` | an HTML deck: one self-contained file from a prose brief | 22 | 67 | 7 |
| `visual-design` | §3's direction and the cover — "does it look designed" | 35 | 63 | 14 |
| `regression-sensitive` | §7's targeted edit: fix slide 4, the rest still gates clean | 42 | 65 | 13 |

`static-page` is the severe one — hard zeros on 71% of decided rows at `medium`. The handoff is a
lane picker rather than a pinned model, because the numbers move:

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape static-page
```

**Omitted deliberately.** `brownfield-integration` (24 against 50), because a deck is one file plus
assets and the JSON lane is a validated emit rather than a multi-file edit; and `greenfield-module`,
`algorithmic`, `accessibility`, `react-ui`, which sit level here, so naming them would route away work
this family does as well as opus. The **review lane gets none** — it judges rather than builds, and
the corpus measures only building. Where the work stays anyway, this block names what to distrust.

## §6's count contract, extended to the cells

**[measured-family]** Everything a brief *enumerated*, the recorded run delivered: twelve named
features, all shipped. Everything named *categorically* got one instance — "all surfaces" → 5, "all
states" → **1**, "all menus" → **0**, "all flows" → **0**, "all actions" → one reused toast.

**[docs]** Under **Ambiguity**: *"Avoid using subjective or relative qualifiers that lack a
concrete, measurable definition. Instead, provide objective constraints (for example, 'write a
summary of 3 sentences or less' instead of 'write a brief summary')."* And these models *"provide
direct and efficient answers"* by default; a fuller response *"must explicitly request it in your
instructions."*

§6 already knows this — *"A named slide count is a contract. Twelve slides means twelve, each
gated."* That sentence is why §6 survives here while the prose around it does not. **Derive the
count when the brief omits one**, from a `recipes.md` spine or the time budget: an unnumbered brief
is where the collapse happens, and here expect compression rather than the padding §6 warns about.
Then **make the contract cover the cells**, shipped filled in the direction comment before slide 1,
every cell real or `n/a: <reason>`:

```
slides    12 of 12 authored          figures  9 of 9 carry source + as-at (3 slides n/a: no figures)
gated     12 of 12 through the gate  images   6 of 6 generated, 6 of 6 opened before placing
crops     12 of 12 opened @1470×956  titles  12 of 12 checked against the source's own tense
```

## The bound ledger — the failure that reaches a passing-looking deck

**[measured-family]** The benchmark's UI verifiers print their assertions. Classified by whether
one states a **bound** (`exactly N`, `no`, `not`, `only`) or asks for a **thing**: Gemini's
failing assertions were 58% bound-shaped at `medium` and **86%** at `high`, against **8%** for
opus. One rule — `has exactly one soft elevation shadow` — failed on *every card and every toast
in its set*, on a run that passed 37 of its 39 others.

Two directions, then. A categorical scope collapses to one instance; a stated maximum is exceeded on
every instance. deck-craft states many maxima, and they are what a beautiful deck breaks quietly —
`Spend the accent once per slide`, `One hue, counted across the whole deck`, body never below 24px,
cover titles at most two lines, bars from zero. **[docs]** Google treats these as a component in
their own right — *"Restrictions on what the model must adhere to when generating a response"* — and
the **Recap** is where they go: a *"Concise repeat of the key points of the prompt, especially the
constraints and response format, at the end of the prompt."* **[derived]** So the recap is a table
with values, filled from the **built deck** rather than the brief. These rows are the skill's own §7
two-decks measurement in that shape, on a deck that **passed the gate**:

| instance | property | bound | readback | observed | within? |
|---|---|---|---|---|---|
| deck | hue families | 1 | `summary.hueFamilies` | 3 | **no** |
| slide 4 | accent marks | 1 per slide | `summary.accentOverspent` mean/max | 3.7 / 7 | **no** |
| deck | external references | 0 | `summary.externalRefs` | 3 font requests | **no** |
| cover | title lines | ≤ 2 | `summary.titleWrap` | 2 | yes |

Report `N of N instances within bound`, read off the **produced** value on **every** instance: a
default idiom supplies the value underneath a rule that was read and agreed with, so restating the
rule changes nothing. **The trap:** a prohibition reads as taste — *"An accent on four elements is
a decoration, not a signal"* and "exactly one accent per slide" are one requirement, one counted.

## Verification is asked for here, not assumed

**[docs]** *"Include specific verification steps in either the system instructions or your prompts
directly … ask Gemini to verify its sources, review its reasoning, identify potential errors."*

**[measured-family]** What fills the vacuum otherwise: the recorded run wrote its own review
claiming a browser engine that had **failed on all four invocation attempts**; *"100% pass rate on
contrast (≥4.5:1 on text)"* from a probe never executed — measured afterwards, every primary button
**3.65:1** and one glyph **1.00:1**, invisible; and an audited-target count of 47 nothing produced.
Five rows, all **PASS**, under a *"Verification Status"* column reading "Verified & Tested". Four
additions to §7:

1. **Paste the verdict line, not a sentence about it** — `[DECK-PREFLIGHT PASS] 0 blockers across
   12 slides examined`, blocker counts beside it. "Gate clean" with no output is the artifact above.
2. **Read the exit code, not the absence of a FAIL line.** §7 spells it out: *"Only exit 0 is a
   pass, and four other codes exist because they are not."* `[DECK-PREFLIGHT ZERO DENOMINATOR]`
   and `[DECK-PREFLIGHT CONFIG DID NOT REACH THE PROBE]` both used to print `PASS`.
3. **Record the receipt, not only the result.** **[measured-family]** On the research run an
   auditor checked its deliverable thoroughly, had no check that the upstream artifacts existed,
   and returned exit 0 over a skipped pass. Here those are the direction contract and the source
   document, so quote a gate result only beside the echoed config and the denominator examined.
4. **Never let the deck assert its own verification.** §5 forbids printing the gate's working on a
   slide (measured: `Constant ratio 1.1765%` beside a real axis note on three slides); its twin is
   that "Verified & Tested" column. §7's *"Do not hand-roll a substitute probe"* holds hardest here.

## Tool discipline: the retry ceiling, and reading what the prompt names

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same
failed call."* **[measured-family]** Two shapes, one session each: four invocations of a banned,
absent driver with nothing changed; and four `Read` calls against `File content exceeds maximum
allowed tokens (25000)` with minor offset tweaks before pivoting to a script. Both land here. §7:
*"If the runner could not run, the deck is not gated"* — a `command not found` is permanent, one
attempt is the budget. And `layout-specs.md` is 1,860 lines, so a whole read **will** hit that
ceiling; take §10's pivot on attempt 1, not after four. *"Read it by id, never whole."*

**[measured-family]** A related reflex costs a whole answer: asked a question naming three skills,
the recorded run answered from memory without loading any of them, then inverted the error and
launched a skill instead of answering. The rule is two ordered steps — **read what the prompt names,
then answer** — neither substituting for the other. Here that is §2's source material (*"you cannot
compress what you haven't read"*), §1's one target reference, and `visual-craft.md` on every build.
§7's delegation cap stays a number too: one imagery agent (§4b), one wide review at twelve slides or
more, and *"Never spawn an agent to verify another agent's findings."*

## The looking, with a fraction and a method

The skill's strongest passage is the two decks that returned identical clean gates where one carried
a clipped table row, three hues, no display tier, its checker's arithmetic on three slides and four
fabricated facts. *"Run the gate to clear the floor, then do the looking, because the looking is
where the difference was."* **[measured-family]** Here the looking is the first thing to get thinned:
the recorded run made **3** render calls and opened **4 images** for 5 surfaces × 2 platforms. So
give §7's walk a denominator — one crop per slide at 1470×956, every one opened, `12 of 12 opened` —
and the same for §4b's *"view every returned image yourself before placing it"*: `6 of 6 opened`.

**[docs]** Google supplies the method the skill leaves to judgment: *"Ask the model to describe
the images before performing the task in the prompt."* Then *"point out which parts of the image
are most relevant"* rather than handing over a whole frame; and when a capture looks wrong, ask
what is in the image first, which separates *"the model did not understand the image at all"* from
*"it did not perform the correct reasoning steps afterward"* — the split `deck-review.md` needs to
tell a real defect from this rasterizer's dropped text runs. **[docs]** One lever the corpus never
tested: *"For UI generation, the model shows high design adherence and parity based on a reference
input, whether it's a screenshot, an image, or a full design system."* Every static-page task in
the benchmark was a prose brief with no reference — the bucket that collapsed. §3 already says to
ground in a `DESIGN.md`, a token file, the product's own UI or a prior deck; supply that as an
actual input rather than a described one. Unmeasured here.

## The direction is three chosen values, written down

**[docs]** A documented Gemini failure is answering correctly while not staying *"within the
bounds of the options"*, and the fix that worked was reframing the task as multiple choice. §3
already supplies the closed set, so write the three axes as three *values* in the five-block
contract before drawing, not as prose you reasoned through:

```
SCHEME light paper · FORMALITY boardroom (runner-up: technical-report) · DENSITY data-heavy
```

**[measured-family]** One correction to §3's attractor list, which is calibrated on a different
model. The recorded run reached for *neither* warm-paper-plus-serif nor near-black-plus-acid:
given two published design systems it produced a neon cyan accent in **no** vendor palette, a
240px rail where the platform specifies 320, and a previous-generation accent on a
current-generation surface — the same failure through the opposite door. It then declared **11**
CSS custom properties beside **45 raw hex literals**, so the direction could be neither enforced
nor switched. So keep §3's defence test, add a provenance clause (the sentence names this deck's
subject or a published value), and count the token layer before slide 2.

## Grounding, published values, and the three states of a figure

**[docs]** Google publishes a system instruction for this posture, worth adopting verbatim on a
regulated deck: *"rely **only** on the facts that are directly mentioned in that context … Do not
assume or infer from the provided facts; simply report them exactly as they appear … If the exact
answer is not explicitly written in the context, you must state that the information is not
available."* The knowledge floor is why: *"The knowledge cutoff date for Gemini 3.7 Flash is March
2026"*, with some domains still at January 2025.

**[derived]** That last clause is `deck-charts.md` §6's unavailable-value state in Google's own
words. Its three states — a figure with provenance, a figure marked illustrative, a value stated
unavailable — are the enumeration here most likely to collapse to one, so count them per slide.
`investor-relations.md`'s published values (ISO 9241-303, IBCS, ASX GN14, ASIC RG 230, SEC Reg
FD/G) and `layout-specs.md`'s per-template caps rot the way a previous-generation accent colour
does, so tabulate them before slide 1: one row per value, the number **and its source tier**, and
a cell you cannot tag is a value you invented. §5's fabrication passage stays as written — *"a
ratio you derived is your claim, not the issuer's disclosure"*, and *"A target is not an
achievement, and the title is where that gets lost."*

## What transferred intact — do not spend overrides here

**[measured-family]** The recorded runs' *content* discipline held: real CIDR blocks, real port
numbers, plausible job identifiers, a licence cap cited by clause, no lorem ipsum, no invented
headline figure, no web-slop tells, and all 20 cited anchors resolved on the research run. §5's
"real content, real states" needs no help, and §7's untrusted-content fence is already right: the
skill ships the verbatim sentence for both the imagery agent and the review lens, because an agent
cannot see this skill. The nearest thing to a slide-level failure in either run was a 4-step rail
highlighting step **2** while its body rendered step **1**'s content — on a deck, a section marker
drifting from the slide it labels, invisible in source and obvious in a crop, so add that to the
per-slide gate.

**[docs]** One register note, since §7 was rewritten for it on 18 Aug 2026. Under **Overt
manipulation**: *"Remove language outside of the core task from the prompt that attempts to
influence performance using emotional appeals, flattery, or artificial pressure … foundation model
performance will no longer improve and in many cases will get worse."* The two capitalised rules
that remain — §5's `NEVER` on synthetic portraits of real named people and its twin in
`visual-craft.md` — are content-bearing: read them for the rule, give the capitals no extra weight,
and never read urgency as a substitute for the run.

## The delivery note

Keep §7's brevity rule — outcome first, no slide-by-slide recap — and add four filled lines:

```
Built:       12 of 12 slides · 12 gated · 12 crops opened at 1470×956
Gate:        [DECK-PREFLIGHT PASS] 0 blockers across 12 slides examined  (exit 0)
Bounds:      18 of 18 instances within bound  (hues 1, accent max 2, typeBelowFloor 0)
Not checked: web-font fidelity (unmeasurable under Obscura), the PDF export, animation
             — and this file's own overrides, unmeasured on decks
```

**[docs]** That last line is the rule rather than modesty: *"Avoid using prompts that ask the model
to perform a task for which it has a known, fundamental limitation."* §9 says the same of the gate —
*"A clean gate means no known computable defect."* Neither it nor this file is a verification.
