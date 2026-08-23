# email-digest on Gemini

Read this once, then read `SKILL.md` normally. The canon transfers — three tiers,
the anti-rules, the evidence classes. What does not transfer is the assumption
that a bound stated in prose gets read back off the rendered HTML. Each override
names the section it lands on, so this reads in one pass: **[docs]** the checklist
warns against "conditionals that require the model to piece together fragmented
instructions."

## Epistemic status

Tiers: `[docs]` (Google, quoted verbatim and gated), `[measured-family]` (Gemini
runs of *other* skills, plus a 106-task benchmark), `[measured-here]` (runs of
**this skill's own scripts** on this machine, 23 August 2026 — not a Gemini run),
`[derived]`. **Every measured rate here is flash-tier**: `gemini-3.7-flash` over
106 tasks at both effort levels, plus two single sessions. None of it projects
onto the Pro tier, where these overrides stand as `[docs]`-grounded discipline and
every `[measured-family]` number is open — **[docs]** "The default thinking effort
is now medium, changed from high in Gemini 3 Flash Preview."

**[docs]** Six sequential phases ending in a gated artifact is what Google
describes `HIGH` as being for — "multi-step planning, verified code generation" —
and 3.7 Flash defaults to `MEDIUM`. Not a remedy: **[measured-family]** paired
across 106 tasks, `high` beat `medium` on 24, lost on 24, tied on 58.

**Unmeasured on this skill** — n=0 Gemini runs of `email-digest`:

- Whether any override changes an outcome; nothing has been measured with a
  `gemini.md` in place against the same work without one.
- Whether the bound failure reaches **email** HTML — it was measured on CSS cards
  and toasts, not on nested tables with inline styles.
- Whether this skill's three qualitative skill routes get skipped here, and
  anything about Gemini *judging*. Step 6 reads; both sources watch a model build.

Modules skipped: `states` (an email has no loading, error or partial state, as
this skill's own evidence file records); `delegation` (no fan-out);
`count-contract` (it would restate override 2); `emphasis` (**0** shouted tokens).
`injection` nearly fired: item copy comes from sources the run did not author.

## Route out before you hand-write a template

**[docs]** "Avoid using prompts that ask the model to perform a task for which it
has a known, fundamental limitation." Two of this skill's shapes sit there — not
permission to give up, but a note on which output to distrust where no lane is free.

| shape | where it lands here | measured (gem-flash vs opus) |
|---|---|---|
| `static-page` | Step 4's *"or write your own template against the same rules"* branch | 22 against 67, hard zero on 71% of decided rows |
| `visual-design` | Step 4's palette, type scale and tier weighting, wherever `design-craft` is not installed | 35 against 63 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape static-page
```

**The cheaper move is already in the skill:** `render_digest.py` takes JSON and
emits the markup, so the run authors a payload rather than a page. Default to it.

**Rows omitted.** `brownfield-integration` and `regression-sensitive`, because the
deliverable is a new message and Step 1 only *reads* the project's tokens — both
land only when the job edits a template already exiting 0 on `lint_email.py`.
`accessibility` is deliberately absent (64 against 69, level): table roles, alt,
link text and heading outline are what the corpus gives no reason to route away.

## What transfers intact

- **The gate prints its denominators**. **[measured-here]**, on `--example`: `all
  9 tables marked presentational`, `all 31 stacks end web-safe`.
- **The counts are already numbers** — 2–4 featured, 2–5 spotlight, exactly three
  highlights, two tiles, 25–55 words, 90KB. **[measured-family]** the benchmark's
  optimality bucket, where the brief states a bound, scored 74.7 against 75.0.
- **The anti-rules hold because they are asserted, not asked for** — `SKILL.md:20`,
  *"`scripts/lint_email.py` asserts the absence of a cap as a rule"*.

## Override 1 — every bound gets read back off the artifact (Steps 2, 3, 4)

**[measured-family]** Across 106 tasks, Gemini's failing UI assertions were
bound-shaped — `exactly N`, `no`, `not`, `only` — **58%** of the time at `medium`
and **86%** at `high`, against **8%** for opus. `has exactly one soft elevation
shadow` failed on *every* card and *every* toast in its set on a run that passed
37 of its other 39 assertions: the rule was read, then a default idiom overrode it.

**[docs]** Google treats these as a component in their own right — "Restrictions
on what the model must adhere to when generating a response, including what the
model can and can't do." — and the **Recap** puts them "at the end of the prompt".
**[measured-here]**, `--example` through `lint_email.py`:

| instance | property | bound | readback | observed | within? |
|---|---|---|---|---|---|
| featured tier | items | 2–4 (`SKILL.md:75`) | `tier:featured` | `1 featured item(s)` | **no** |
| spotlight row | items | 2–5 (`SKILL.md:76`) | `tier:spotlight` | `0 spotlight` | **unproven** — short-circuits on zero |
| document | HTML bytes | ≤ 90KB (`SKILL.md:280`) | `size:budget` | `12.8KB of HTML` | yes |
| featured card 1 | body words | 25–55 (`SKILL.md:75`) | none ships | — | **no readback** |
| featured card 1 | primary actions | 1, accent once (`SKILL.md:222`) | none ships | — | **no readback** |

The last two rows are the point: bounds stated in prose that no check reads back.
**[docs]** Let the machine count them — code execution "should be enabled whenever
the model needs to perform any kind of arithmetic, counting, or calculation":

```bash
python3 -c "import json,sys;[print(len(i.get('body','').split()),i['title']) for i in json.load(open('payload.json'))['items'] if i.get('body')]"
grep -oi "$ACCENT" mail.html | wc -l   # one filled button per featured card, no more
```

**The trap.** A bound stated as a prohibition reads as taste. `SKILL.md:137` —
*"Every banner is decorative and carries `alt=""`"* — is a counted property in
style advice. Convert each into a row, and say which you converted.

## Override 2 — the quota ledger: every word, every table, every tier (Steps 3, 5)

**[docs]** Under **Ambiguity**: "Avoid using subjective or relative qualifiers
that lack a concrete, measurable definition." **[measured-family]** one run
delivered 12 of 12 enumerated features and **1 of 6** named states.

`SKILL.md:145` carries the categorical scope that matters most, and the skill
already predicts the failure: *"A digest whose featured copy was written properly
and whose eighteen tail lines were not reads as two different people, and the tail
is where most of the words are."* Filled, for a 24-item issue:

| block | strings | voiced | note |
|---|--:|--:|---|
| subject · preheader · heading · 3 highlights | 6 | 6 | linted with everything else, in one pass |
| featured headline + body | 4 | 4 | 2 cards |
| spotlight title + headline | 6 | 6 | 3 cards |
| research slug + summary | 4 | 4 | 2 tiles |
| tail `oneline` tags | 19 | 19 | the row that gets skipped |
| **total** | **39** | **39** | `39 of 39 strings, 0 improvised` |

**[docs]** Passes, not one sweep — under **Too many tasks**, "Break the requests
into separate prompts." One pass writes all 39, one runs the voice lint over the
whole set (`SKILL.md:166` — *"the only way it can see the repetition"*), one
renders. **[docs]** Anchor the set with a worked example: "We recommend to always
include few-shot examples in your prompts." Build featured card 1 complete —
banner with `alt=""`, headline as a text node beside it, body counted into 25–55
words, one filled primary and one muted subordinate — and measure the rest against
it. Two more categorical rules take the same shape and the gate *does* read these
back: `role="presentation"` on **every** nested layout table (`SKILL.md:268`), and
*"Every tier has to read completely with images stripped"* (`SKILL.md:141`).

## Override 3 — paste the gate, and `ok` beside a zero is not a pass (Step 5)

**[docs]** "Include specific verification steps in either the system instructions
or your prompts directly." **[measured-family]** the vacuum left where
verification scaffolding was removed filled with a browser engine that never ran.

`SKILL.md:257` names this skill's own instance — the `tiers` check, where *"no
tier markers means every tier rule below is measuring nothing while still printing
a verdict"*. **[measured-here]** on `--example`, two more reported `ok` over zero:

```
FAIL  tier:featured   1 featured item(s); 2 to 4, default 2 …
ok    tier:spotlight  0 spotlight
ok    tier:tail       0 one-liners
```

`tier:spotlight` short-circuits at zero and `tier:tail` only fires above twelve
items, so the delivery line is the error and warning counts **with** the tier
denominators beside them, never `the gate passed`.

**Prerequisite receipts, because `lint_email.py` checks the artifact and not the
pipeline.** **[measured-family]** on one run a thorough auditor validated tags,
citations and contrast, no check for whether the upstream skills ran, and exit 0
over two skipped invocations:

```bash
for f in TIERS.md copy.json DESIGN.md; do [ -s "$f" ] || { echo "receipt missing: $f"; exit 1; }; done
python3 scripts/lint_email.py mail.html --text mail.txt --subject "$SUBJECT"; echo "exit=$?"
python3 <ux-craft>/scripts/ux-lint.py --static mail.html; echo "exit=$?"
```

Both exit codes, both outputs pasted. `SKILL.md:347` asks for the honest line
where a route was substituted — *"say which substitution you made rather than
implying the pass happened"* — and a missing receipt writes it by command.

## Override 4 — three skills become three files (Steps 2, 3, 4)

`SKILL.md:59`, `SKILL.md:145` and `SKILL.md:206` route work through `ux-craft`,
the project's voice skill and `design-craft`, all three phrased as a standard
rather than a step — *"with `ux-craft`'s lens still on it"*.

**[measured-family]** On the one measured run carrying that phrasing, **both**
skill invocations were skipped, and the model's own diagnosis named the mechanism:
the rules were already in context, and nothing downstream mechanically depended on
a file only those skills produce. `render_digest.py` reads `payload.json` and
nothing else. **[docs]** The remedy is chaining: "make each step a prompt and
chain the prompts together in a sequence."

| phase | skill | writes | consumed by |
|---|---|---|---|
| A | `ux-craft` | `TIERS.md` — reading order, per-item tier, the ranking basis | the `tier` field on every item |
| B | the byline's voice skill | `copy.json` — all 39 strings above | every text field in `payload.json` |
| C | `design-craft` | `DESIGN.md` — palette and font stacks as literals | `brand.palette`, `brand.fonts` |
| D | — | `payload.json` → `mail.html`, `mail.txt` | `lint_email.py`, `ux-lint.py` |

Phase D cannot start until A, B and C have written their files; the receipt loop
above makes that true rather than intended. Where a skill is absent, write its
file anyway with the first line naming the substitution.

## Override 5 — values are read, and claims may not exceed their sources (Steps 1, 3, 4)

**[docs]** "Your knowledge cutoff date is January 2025." Google's remedy is
grounding, which "should be enabled whenever the model may need to know obscure or
recent facts". **[measured-family]** one run put Windows 10's `#0078D4` on a
Windows 11 surface — a previous-generation *published* value. Fill this before the
first markup; a cell you cannot tag is invented.

| value | used for | source | tier |
|---|---|---|---|
| Gmail CSS allowlist | no flex, grid, `position`, `transform` | Google's published allowlist, read at build time | **P** |
| ~102KB clip, budget 90KB | `size:budget` | Mailchimp / Litmus / Klaviyo; **documented by Google nowhere** | **M** |
| 86.24% missing table roles | `a11y:table-role` | Email Markup Consortium, 443,585 emails | **M** |
| `display:flex` support | the media-query fallback | Can I Email, last tested **2 Nov 2021** | **M, stale** |

The rule points inward twice. At `SKILL.md:36` — *"Discover rather than assume; a
hard-coded map goes stale silently"* — read the project's tokens rather than
recalling a palette. At `SKILL.md:196` the join between a skill and the work it
was used on must be sourced: *"an invented one is worse than none"*. **[docs]**
Google's strictly-grounded instruction ends where this does: "If the exact answer
is not explicitly written in the context, you must state that the information is
not available."

## Override 6 — look at it twice, and name what is in the frame (Step 6)

`SKILL.md:316` asks for two states, images loaded and images blocked, so the
denominator is two. **[docs]** "Ask the model to describe the images before
performing the task in the prompt", and "To improve the response, point out which
parts of the image are most relevant to the prompt." Per capture: name what is in
it — which tier, which rows, whether the research ground is present — then judge.

**[docs]** The documented strong path is worth taking: "For UI generation, the
model shows high design adherence and parity based on a reference input, whether
it's a screenshot, an image, or a full design system." Step 1 already discovers
one. **[measured-family]** every static-page task in the benchmark was a prose
brief with no reference, and that is the bucket that collapsed; with-reference is
unmeasured, so this is the documented mode, not a proven fix.

## Two short ones

**The retry ceiling (Steps 1, 4).** **[docs]** "On *other* errors, you must change
your strategy or arguments, not repeat the same failed call."
**[measured-family]** one run invoked an absent tool four times unchanged; another
retried a `Read` four times against a token ceiling before pivoting. The permanent
errors here are a banner URL that 404s and a payload the renderer rejects: one
attempt, then change the input rather than the flag.

**Read what the prompt names, then answer (References).** **[measured-family]**
asked a question naming three skills, one run answered from memory without loading
any; asked to fix it, it launched a skill instead of answering. `SKILL.md:24`
points at `references/evidence.md` for exactly the questions people ask this skill
— why there is no item cap, why no text-to-image gate. Load the file, then answer:
two ordered steps, neither substituting for the other.
