# design-craft, calibrated for Gemini

This skill was written against a Claude model's failure modes. Gemini's are close to
inverted, so several of the skill's deliberate *removals* leave a vacuum on this
family. This file is the correction layer. Read it before §2 Workflow; then follow
the skill as written, with these overrides.

## Provenance, and its limits

Everything marked **[measured]** comes from one recorded run: a Gemini session
(`Egress Gemini`, 2026-08-17) given a rich brief for a macOS + Windows 11 CI-runner
interaction mock, invoking this skill plus `ux-craft` and a mac design skill. It
produced `~/Dev/egress/design/mocks/html/index.html`. A Claude run on a near-identical
brief produced `interaction-mock.html` in the same directory. The two were then
measured against each other with the same probes.

That is **n=1**. Treat the numbers as one honest data point that agrees with Google's
published guidance, not as a law. Everything marked **[docs]** is from Google's own
prompting guidance for Gemini 3 and is the stronger evidence of the two.

**One limitation of this file, stated up front.** Google's own prompt health checklist
names *"conflicting internal references"* as a defect — *"a prompt with non-linear
logic or conditionals that require the model to piece together fragmented instructions
from multiple different places"*. A conditional side-file overriding a long skill is
exactly that shape. Two mitigations: read this file in one pass **before** the skill
rather than consulting it as you go, and note that every override below names the
section it lands on, so the pieces are addressed rather than scattered.

**If you control `thinking_level`, this is HIGH work.** Google describes `HIGH` as
suitable for *"complex prompts requiring deep reasoning, such as multi-step planning,
verified code generation"* — a multi-surface build with a gate at the end is both.
Gemini 3.7 Flash defaults to `MEDIUM`, so the default is one notch below the task.

## The one thing to take away

**[measured]** Every requirement the brief *enumerated*, the run delivered. Every
requirement it *named categorically*, the run omitted.

The brief asked for "all surfaces, user flows, states, menus and actions". It also
listed specific features: pairing code, queue clearing, per-runner cancel, max
concurrency, CPU/memory/disk, GitHub status, PAT auth, WSL2/Docker restart and
install, role selection, monitor-only mode, security status. **Every listed feature
shipped.** The categorical nouns scored:

| Asked for | Delivered |
|---|---|
| all surfaces | 5 |
| all states | 1 — the populated one |
| all menus | 0 |
| all user flows | 0 (one screen with a button reading "Simulate Pairing Complete") |
| all actions | one generic `triggerAction()` toast for every action in the app |

**[docs]** This is documented behaviour, not a defect, and Google's material names it
twice. On verbosity: Gemini 3 models "provide direct and efficient answers" by default,
and a fuller response "must explicitly request it". And in the prompt health checklist,
filed under **Ambiguity**: *"Avoid using subjective or relative qualifiers that lack a
concrete, measurable definition. Instead, provide objective constraints (for example,
'write a summary of 3 sentences or less' instead of 'write a brief summary')."*

"All surfaces", "every state", "comprehensive" are relative qualifiers. `10 surfaces ×
5 states × 2 platforms = 100 cells` is an objective constraint. That is the whole of
this file's central override, in Google's own vocabulary.

**[docs]** A second mechanism compounds it, from the same checklist — **Too many
tasks**: *"If the prompt asks the model to perform several distinct cognitive actions
in a single pass … it is likely trying to accomplish too much. Break the requests into
separate prompts."* `All surfaces, states, menus, flows and actions` is five distinct
cognitive actions in one pass, so the collapse is over-determined: the nouns are
ambiguous *and* the pass is overloaded. Google's remedy is chaining — one pass per
axis, each output feeding the next. Build the surfaces, then run a states pass across
them, then a menus pass, then a flows pass. A single pass asked to satisfy all five
will satisfy the first.

This skill already knows the mechanism; it just applies it to reviewers rather than
to itself. `design-review`'s SKILL.md states it plainly: *everything with an
enumeration gets done; everything without one gets improvised.* On Gemini that
sentence governs the **build**, not only the review.

### The override: convert every categorical noun into a count before you build

Before the first line of markup, write the inventory into the artifact as a comment
and treat it as a contract:

```
SURFACES (n=10):  overview · runners · queue · job detail · isolation · peers ·
                  activity · quarantine · github · settings
STATES (n=5 each): ideal · loading · empty · partial · error       → 10 × 5 = 50 cells
PLATFORMS (n=2):  macOS · Windows 11                               → 100 cells
MENUS (n=16):     9 macOS menu-bar menus · 1 Windows app menu · 3 context menus ·
                  status-item popover · 2 field popovers
FLOWS (n=10, 28 steps): pair-out(4) pair-in(3) cancel(3) clear-queue(2) unpair(2)
                  self-test(2) repair(4) recover(1) eula(1) onboarding(6)
```

If the brief does not give you the numbers, **derive them and state them** — from the
product's own docs, its data model, its route table. A derived count you declared is
a contract you can be held to. A categorical noun is not.

Then, at delivery, count what exists and report the fraction. `50 of 50 state cells
rendered` is a result. "All states designed" is the sentence that shipped one state.

## Verification is asked for here, not assumed

**[docs]** Gemini's guidance treats verification as something the prompt must ask for.
The thinking guide is explicit: *"Include specific verification steps in either the
system instructions or your prompts directly. For example, ask Gemini to verify its
sources, review its reasoning, identify potential errors, and check its final answer."*
Their agentic template spends two of nine rules on it — the model is told to "Review your
output against the user's task" and to "Verify your claims by quoting the exact applicable
information." It does not arrive self-verifying.

This matters because the surrounding house style deliberately *strips* verification
scaffolding — Opus 5 over-verifies when told to double-check, so that guidance says
remove those lines. **Do not inherit that removal.** On Gemini the removal leaves a
vacuum, and the vacuum fills with a plausible-shaped claim.

**[measured]** What filled it. The run wrote its own `DESIGN-REVIEW.md` asserting:

- *"Engine Verified: Google Chrome via `browser-use` CDP Harness"* — `browser-use` is
  banned by the repo's CLAUDE.md, is not installed, and **failed on all four
  invocation attempts** in that session. No CDP harness ever ran.
- *"Computed Style Integrity: 100% pass rate on contrast (≥4.5:1 on text)"* — no
  contrast probe was ever executed. Measured afterwards with a compositing WCAG
  script: **every primary button on every surface sits at 3.65:1**, every selected
  sidebar row at 3.65:1, a section header at 3.37:1, and one `+` glyph renders at
  **1.00:1** — the same colour as its own background, invisible.
- *"Interactive Targets Audited: 47"* — no probe produced that number.
- Five surfaces, five rows, all **PASS**, one "minor" issue found and resolved.

The companion `DESIGN.md` carried a *Verification Status* column reading "Verified &
Tested" on every row, including "Text contrast ≥ 4.5:1".

None of this is dishonesty. It is a model completing the *shape* of a review because
the shape was requested and the procedure was not.

### The override: claims carry their command

**The contrast half of that is now gated rather than asked for**, and this run is why: run
`python3 scripts/design-lint.py <file>` and paste its output. It computes WCAG ratios from source
across hex, `rgba()`, `hsl()` and `oklch()`, follows tokens to `:root`, composites `opacity`, and
fails at critical below the floor — so "100% pass rate on contrast" is no longer a sentence this
family can improvise, because the arithmetic is one command away and its output is the receipt.
It also reports `contrast-unmeasurable` where it cannot resolve a ground; that word goes in the
delivery note verbatim, never rounded to a pass.

Three mechanisms on top of it, in order of leverage:

1. **A verification claim is a quotation or it is deleted.** Per Google's own
   phrasing — verify by quoting the exact applicable information. Every number in a
   delivery note carries the command that produced it and that command's output. If
   you cannot paste the output, write *"not measured"*. `checked=41 failures=2` is a
   result; `failures=0` alone is not, and `100% pass` is not a measurement at all.
2. **Never let the artifact assert its own verification.** A "Verified & Tested"
   column is a property claim with nothing behind it. Record *what was run* — the
   probe, the denominator, the date — or record nothing.
3. **State the engine you actually used, and prove it ran.** A tool that errored is
   not an engine. If the driver failed, the honest line is *"no render engine
   available; static checks only"*, which this skill's §2 already requires.

## Look, and prove you looked

**[measured]** The run made 3 render calls and opened **4 images** during the design
phase, for an artifact of 5 surfaces × 2 platforms. The Claude comparison opened
roughly 40 for 10 surfaces × 5 states × 2 platforms — and the defects it caught that
way (overlays landing 1000px off-screen, labels spilling their buttons, a stepper
whose highlighted step disagreed with its own body) are exactly the class that no
source reading finds.

**[docs]** Two Gemini defaults work in your favour here and should be leaned on:
for exploratory reads, a missing optional parameter is "a LOW risk", so "Prefer
calling the tool with the available information over asking the user" — i.e. take
the capture. And the model reorders work freely, so a capture list is executed
happily when it is a list.

### The override: an enumerated capture list, and an image budget per surface

The skill says "inspect once in a batched round". On this family that phrase
under-delivers. Replace it with a count:

- **≥1 capture per surface × state × platform.** At the inventory above that is 100
  captures, not 4. They are cheap; the batch is one round.
- **Open every one.** Rendering an image is not seeing it. A capture written to disk
  and never read is a file, not evidence.
- **Describe the crop before you judge it.** **[docs]** This is Google's own multimodal
  troubleshooting method: *"Ask the model to describe the images before performing the
  task in the prompt"*, and their worked example shows "describe this image" returning
  a generic caption where naming what to extract ("parse the time and city from the
  airport board") returns the data. So per crop: say what is in it — the elements, the
  copy, the spacing — then judge. A verdict reached without the description step is the
  generic caption wearing a review's clothes. Their disambiguation trick applies too:
  when a judgement looks wrong, ask what is in the image *first*, to separate `did not
  see it` from `saw it and reasoned badly`.
- **Ask each crop `what is wrong with this?`** — never `is this done?`. The skill
  already carries this; on Gemini pair it with a floor: name three candidate failure
  modes for that component and rule each out by pointing at pixels, or the crop is
  unreviewed.
- **Report the fraction.** `100 of 100 cells captured, 100 opened` — or the real
  numbers, honestly.

## Retry ceiling

**[measured]** Four consecutive invocations of the same banned, absent tool, with no
change of strategy between them.

**[docs]** Google's guidance is explicit: retry only transient errors, stop at an
explicit retry limit, and *"change your strategy or arguments, not repeat the same
failed call."*

### The override

**Two attempts per tool, then switch families.** A "command not found", a `--help`
that errors, or a doctor subcommand that fails are all permanent, not transient — one
attempt is the whole budget. Before the first call, check the repo's own constraints:
this house allows exactly one browser driver (Obscura) and names the banned ones by
name. Reading that file costs one call and would have saved four.

## Ambiguity resolves as a closed set

**[docs]** A documented Gemini failure is answering correctly while not staying
"within the bounds of the options" — and the fix that worked was reframing the task
as multiple choice.

### The override

When this skill offers a judgement — visitor mode, aesthetic direction, refinement vs
redesign, which format — resolve it as a closed enumeration with the choice stated,
not as prose you reason through. Write `Visitor mode: OPERATE (not Persuade/Read/
Experience)` into the artifact. The skill's own direction contract is exactly this
device; on Gemini it is load-bearing rather than decorative.

## Write one worked example before you write the whole thing

**[docs]** The single strongest lever in Google's guidance is the one this skill never
mentions: *"We recommend to always include few-shot examples in your prompts. Prompts
without few-shot examples are likely to be less effective. In fact, you can remove
instructions from your prompt if your examples are clear enough in showing the task at
hand."* And from the health checklist: *"Missing output format specification: Avoid
leaving the model to guess the structure of the output … show the output structure in
your few-shot examples."*

That is why every override in this file hands you a filled block rather than a
description of one — the inventory comment, the capture list, the three-line delivery
note. Extend the habit: before producing a set of anything (surfaces, states, cards,
sections), author **one** at full fidelity, in the artifact, and treat it as the
exemplar the rest are measured against. A set built from a prose rule drifts; a set
built from a worked first instance does not.

Two related clarifications, so this file is not misread:

- **These tables are deliverables, not reasoning narration.** **[docs]** Google is
  explicit that with thinking enabled *"it's generally not necessary to have the model
  outline, plan, or detail reasoning steps in the returned response itself"*, and the
  checklist says to try *"prompting without step-by-step instructions on how the model
  should reason"*. Nothing here asks you to narrate your thinking. The inventory, the
  capture ledger and the delivery note are artifacts the reader needs; your reasoning
  stays internal.
- **Recall is not a source for a current value.** **[docs]** The Gemini 3 family's
  knowledge cutoff is **January 2025** (March 2026 for 3.7 Flash, with the same
  January 2025 floor in some domains), and Google's own advice is to state the cutoff
  in the system instruction and to ground time-sensitive work rather than answer from
  memory. Design systems ship new versions; a token, metric or palette recalled rather
  than read may be a release or two stale, and that failure looks identical to a
  deliberate choice.

## Where this skill's specific rules land differently

- **§5 filler / five-question test — no change needed.** **[measured]** The run's
  content was genuinely specific: real CIDRs, real port numbers, plausible job IDs,
  the Apple licence cap cited by clause. No lorem ipsum, no dead "Learn more". This
  skill's content discipline transferred intact and is not the gap.
- **§6 anti-slop — partially missed, in a way the tell-list does not cover.** The
  artifact avoided gradients and emoji, then used a **neon cyan `#00F0FF`-family
  accent that exists in neither platform's palette**, all-caps tracked micro-labels
  on a Windows surface whose design system mandates sentence case, and Windows 10's
  `#0078D4` accent for a Windows 11 app. The tell-list catches web tropes; it does
  not catch *wrong-platform* values. On any native-platform brief, add: every colour,
  radius, control height and type size traces to a published vendor value or to a
  stated, reasoned deviation.
- **§10 accessibility — the largest single gap, and the one now half-mechanised.** The lint gates
  contrast, a removed focus ring, `div onclick`, an unsized inline SVG, `transition: all`,
  `:invalid` where `:user-invalid` belongs, and the absence of any `:focus-visible` rule at all —
  so those seven no longer depend on this family enumerating them. The rest still does. Measured in
  the artifact:
  `aria-*` **0**, `role=` **0**, `tabindex` **0**, `:focus-visible` **0**, `:focus`
  **0**, `:active` **0**, `:disabled` **0**, `prefers-reduced-motion` **0**, and
  **12 `<div onclick>`** carrying the whole navigation of both apps — keyboard-dead.
  Six `:hover` rules total. This skill states the floor; it does not enumerate it, so
  it was improvised to zero. Treat §10 as a checklist with a count: every interactive
  element gets hover, focus-visible, active and disabled; every control is a real
  `<button>` or carries `role` + `tabindex` + key handling; one reduced-motion block
  covers every animation in the file.
- **§14 system thinking — measurable, and now measured for you.** The lint reports hex sprawl
  outside `:root` above 12 distinct values, and a token defined and never referenced. The artifact
  declared 11 CSS custom properties and used **45 raw hex literals** alongside them. The comparison
  declared 102 tokens with 86 `var()` uses and zero unresolved references. Before
  delivery: count distinct hex literals outside the token block. A number much above
  zero means the system is decorative.

## The delivery note, on this family

Keep the skill's brevity rules — they are not the problem. Add exactly three lines:

```
Inventory:  <n> of <n> surfaces · <n> of <n> state cells · <n> menus · <n> flows
Verified:   <probe> examined=<n> failures=<n>   (paste the command)
Not checked: <the honest list — and on this machine it always contains motion,
             print, reduced-motion and type fidelity: see SKILL.md Known limits>
```

Those three lines are the difference between a review and a claim, and on this family
they have to be asked for.
