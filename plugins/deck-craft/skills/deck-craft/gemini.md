# deck-craft, calibrated for Gemini

Read this before §1 Route to a target. Then follow the skill as written, with these
overrides.

Two of this skill's rules are already the right shape for the family — §6's slide count
as a contract, and §7's runner that exits non-zero on an empty result. Everything below
extends those two to the parts of the skill that are still prose.

## Provenance

**[measured]** items come from one recorded Gemini run (`Egress Gemini`, 2026-08-17).
It built a two-platform interaction mock rather than a deck, so nothing here was
measured on slides — what transfers is the *behaviour*, on a rich brief, using
sibling design skills. Treat every **[measured]** line as evidence about the family and
not about deck work specifically. **n=1.** **[docs]** items come from Google's
published Gemini 3 prompting guidance and are the stronger evidence.

**Two notes on using this file.** Google's prompt health checklist names *"conflicting
internal references"* as a defect — instructions the model must *"piece together … from
multiple different places"* — which is the shape of any conditional side-file, so read
this in one pass before §1; each override names the section it lands on. And a
twelve-slide build with a preflight gate at the end is what Google describes
`thinking_level: HIGH` as being for (*"multi-step planning"*); Gemini 3.7 Flash defaults
to `MEDIUM`.

## The one behaviour to design around

**[measured]** Everything the brief *enumerated*, the run delivered — twelve named
features, all shipped. Everything it *named categorically* was satisfied by one
instance: "all surfaces" → 5, "all states" → **1**, "all menus" → **0**, "all flows" →
**0**, "all actions" → one generic toast reused for every action in the product.

**[docs]** Google's material names this twice. On verbosity: these models "provide direct
and efficient answers" by default and a fuller response "must explicitly request it". And
in the prompt health checklist, under **Ambiguity**: *"Avoid using subjective or relative
qualifiers that lack a concrete, measurable definition. Instead, provide objective
constraints (for example, 'write a summary of 3 sentences or less' instead of 'write a
brief summary')."* A slide count is already an objective constraint — which is exactly
why §6 works on this family and the prose rules around it do not.

§6 already knows this — *"A named slide count is a contract. Twelve slides means
twelve, each gated."* That is the single most important sentence in this skill for
Gemini, and it needs extending in two directions:

- **Derive the count when the brief omits it, and state it before building.** "A deck
  about the Q3 results" has no number in it, and an unnumbered brief is where the
  categorical collapse happens. Write `9 slides` into the direction comment, from the
  recipe spine or the time budget, and hold it.
- **The contract covers the cells, not only the slides.** Twelve slides × the per-slide
  gate is a grid. Report it as a fraction — `12 of 12 slides, 12 of 12 gated, 12
  captures opened` — because "each gated" is a categorical noun and will be satisfied
  by having gated one.

Padding is the failure §6 warns about and it runs the other way on this family: expect
compression, not padding. A brief that asks for twelve and gets a coherent eight is the
shape to check for.

## Verification is asked for here, not assumed

**[docs]** Google treats verification as something the prompt has to contain. Their
thinking guide: *"Include specific verification steps in either the system instructions
or your prompts directly. For example, ask Gemini to verify its sources, review its
reasoning, identify potential errors, and check its final answer."* Their agentic
template spends two of nine rules on it — *"Review your output against the user's task"*
and *"Verify your claims by quoting the exact applicable information."*

**[measured]** What fills the gap when it is not asked for. The run wrote its own review
document claiming a named engine (`browser-use` CDP) that had **failed on all four
invocation attempts** and never ran; *"100% pass rate on contrast (≥4.5:1 on text)"*
with no probe ever executed — measured afterwards, **every primary button was 3.65:1**
and one glyph rendered at **1.00:1**, invisible; and an audited-target count of 47 that
nothing produced. Five surfaces, five rows, all **PASS**. A companion document carried
a *"Verification Status"* column reading "Verified & Tested" on every row.

§7 makes the gate mandatory, and `run-preflight.sh` already fails closed — *"an empty
result exits non-zero with 'this is NOT a pass', because a silent gate is
indistinguishable from a clean deck."* Three additions:

1. **Paste the runner's summary into the delivery, not a sentence about it.** Every
   blocker name with its count: `stageGeometry=0 overflow=0 titleWrap=0 inkPastSlide=0
   …`. A claim of "gate clean" with no output is the exact artifact above.
2. **If the runner could not run, the deck is not gated, and the delivery says so** in
   those words. **[measured]** Four consecutive attempts at one banned, absent driver,
   with no strategy change — **[docs]** retry transient errors only and *"change your
   strategy or arguments, not repeat the same failed call."* A `command not found` is
   permanent: one attempt is the whole budget, and the repo's own constraints name the
   permitted driver.
3. **Never let the deck assert its own verification.** §5 already forbids printing the
   gate's working on a slide — measured, `Constant ratio 1.1765%` shipped beside a
   legitimate axis note on three slides. Its twin is a "Verified & Tested" column in
   the handoff doc: a property claim with nothing behind it, standing where provenance
   belongs. Record *what was run*, or record nothing.

## Read §7's emphasis as a plain rule, and don't add to it

**[docs]** One passage in Google's health checklist is worth naming because this skill
trips it. Under **Overt manipulation**: *"Remove language outside of the core task from
the prompt that attempts to influence performance using emotional appeals, flattery, or
artificial pressure. While first generation foundation models showed improvement in some
circumstances with instructions like 'very bad things will happen if you don't get this
correct', foundation model performance will no longer improve and in many cases will get
worse."* Their Gemini 3 guidance says the same positively: *"Be precise and direct …
Avoid unnecessary or overly persuasive language."*

**This is now fixed upstream rather than worked around here.** Until 18 Aug 2026 §7 opened
with *"Automatic Preflight & Review Execution is MANDATORY — never wait for the user to
ask"*, plus "you MUST" and "you must never ask", and `deck-review.md` carried a "CRITICAL
REQUIREMENT" heading. The instruction was correct and load-bearing; the register was the one
Google says stops helping and can hurt. Both now read plainly, for every family rather than
for yours alone — the skill contained its own refutation in a side file, which was the wrong
place for it. Two things still hold:

- **Read the rule for its content.** Run `run-preflight.sh` as a build step and fix every
  blocker. If you meet emphasis anywhere in an older copy of this skill, it adds no
  information — and in particular it is never licence to substitute urgency for the run.
- **Don't reproduce the register.** When you write a handoff, a spec, or a brief for
  another agent from this skill, state the rule and the reason. Escalating language is
  measurably not a lever here, and it displaces the thing that is — a count, a command,
  or a worked example.

## §7's two-decks lesson, with a number attached

The skill's strongest passage is the one where two decks returned identical clean gates
and one of them carried a clipped table row, three hues, no display tier, its checker's
arithmetic on three slides and four fabricated facts. *"Run the gate to clear the floor,
then do the looking, because the looking is where the difference was."*

**[measured]** On this family the looking is where the budget goes first. The run made
**3** render calls and opened **4 images** for an artifact of 5 surfaces × 2 platforms.
The defects a Claude run caught by looking — controls spilling their own fixed-height
boxes, a step indicator disagreeing with the body it labelled, a selector row clipped
off the right edge — are precisely the class that no source reading finds.

So give §7's walk a count and a fraction: **one crop per slide at 1470×956, every one
opened, `12 of 12 opened` in the delivery.** **[docs]** Two defaults help here — for
low-risk exploratory reads, *"Prefer calling the tool with the available information
over asking the user"*, so take the capture rather than weighing it; and the model
executes an enumerated list readily, so write the capture list out.

**[docs]** And Google gives a method for the crop itself, which this skill leaves to
judgment: *"Ask the model to describe the images before performing the task in the
prompt."* Their example is exact — "describe this image" of an airport board returns a
one-line caption, while naming what to extract returns the thirteen rows. So per slide
crop: name what is on it (title, focal element, chart, footer, chrome) and *then* judge
centring, cutoff and clearance. Two corollaries they state directly: *"point out which
parts of the image are most relevant"* rather than handing over a whole frame with "find
the problems"; and when a capture looks wrong, ask what is in the image first, which
separates *"the model did not understand the image at all"* from *"it did not perform the
correct reasoning steps afterward"* —
the same split `deck-review.md` needs to tell a real defect from this rasterizer's
dropped text runs, reached with a question instead of an edit.

And the same fraction applies to §4b: *"view every returned image yourself before
placing it"* is a categorical instruction. Make it `6 of 6 generated images opened`.

## The direction is three chosen values, written down

**[docs]** A documented Gemini failure is answering correctly while not staying "within
the bounds of the options" — and the fix that worked was reframing the task as multiple
choice. §3 already supplies the closed set: **scheme** (light paper / dark canvas),
**formality** (boardroom ↔ zine), **density** (airy ↔ data-heavy).

So write the three as three *values*, not as prose you reasoned through, into the
five-block direction contract before drawing:

```
SCHEME     light paper
FORMALITY  boardroom (runner-up: technical-report)
DENSITY    data-heavy
THESIS / OWN-WORLD / STORY / COVER / FORM …
```

**[measured]** One correction to §3's attractor list, which is calibrated on a
different model. The run reached for *neither* warm-paper-plus-serif nor
near-black-plus-acid. On a brief with two published design systems available, it
reached for a neon cyan accent present in **no** vendor palette, a 240px navigation
rail where the platform specifies 320, and Windows 10's accent on a Windows 11 surface.
Same failure through the opposite door: a value arrived at before there was a reason
for it.

So keep §3's one-sentence defence test and add a provenance clause — **the sentence
must name either this deck's subject or a published value.** Then count the token
layer: the run declared **11** CSS custom properties and used **45 raw hex literals**
beside them. On a deck that means the direction cannot be enforced or switched, and
slide 9 will not match slide 2.

## What transferred intact — do not spend overrides here

**[measured]** The run's *content* discipline held. Real CIDR blocks, real port
numbers, plausible job identifiers, and the Apple licence concurrency cap cited by
clause. No lorem ipsum, no dead "Learn more", no invented headline figure. §5's "real
content, real states" and design-craft's five-question test transferred without help.

§5's fabrication passage — the texture around a real number, and the derived ratio set
as a chip — was **not** exercised by this run either way, so treat it as unmeasured on
this family and keep the rule exactly as written. The one clause worth repeating
because it is the subtle half: **a ratio you computed is your claim, not the issuer's
disclosure.**

**[docs]** Google supplies a ready-made system instruction for precisely this posture,
and on a regulated deck it is worth adopting verbatim rather than paraphrasing: *"rely
**only** on the facts that are directly mentioned in that context. You must **not**
access or utilize your own knowledge or common sense to answer. Do not assume or infer
from the provided facts; simply report them exactly as they appear … any facts or
details that are not directly mentioned in the context must be considered **completely
untruthful** and **completely unsupported**. If the exact answer is not explicitly
written in the context, you must state that the information is not available."* That
last sentence is §5's rule and `deck-charts.md`'s unavailable-value state in Google's own
words: a figure the source does not carry is stated as unavailable, not filled.

Two other grounding facts worth holding on any deck about the present. **[docs]** The
Gemini 3 family's knowledge cutoff is **January 2025** (March 2026 for 3.7 Flash, with
some domains still at the January 2025 floor), and Google's advice for time-sensitive
work is to state the cutoff and ground rather than recall — so a market figure, a peer
comparison or a "latest" anything comes from the source document, and Grounding with
Google Search exists for the rest.

## §8's trunk test, per slide

**[measured]** The nearest thing to a slide-level failure in the run: a 4-step
onboarding rail highlighting step **2 "Runtime & Hypervisor"** while its body rendered
step **1**'s content — the indicator and the content disagreeing inside a single frame.
The same defect class on a deck is a section marker or running position that has
drifted from the slide it labels, and it is invisible in source and obvious in a crop.

Check it as part of the per-slide gate, mechanically: for every slide carrying a
position indicator, the highlighted step equals the rendered step. It costs one glance
per crop and is the cheapest structural check in §8.

## The delivery note

Keep §7's brevity rule. Add three lines:

```
Built:      <n> of <n> slides · <n> gated · <n> crops opened
Gate:       <paste run-preflight.sh's blocker line verbatim>
Not checked: <the honest list — never empty>
```
