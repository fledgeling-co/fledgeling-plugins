# create-skill, calibrated for Gemini

Read this once before *Phase 0 — Discovery*, then run the seven phases as
written; each override names the phase or file it lands on. The canon transfers.
What changes is that three load-bearing instructions are standards rather than
steps with an output: Phase 2's *"Every structural choice traces to something"*,
Phase 5's banner *"Composed HTML via design-craft with ux-craft's Read-mode
lens"*, and Phase 3's eval layer, which the skill deliberately allows not to run.
On this family a standard gets agreed with; a phase that writes a file gets
executed. And `references/opus-5-prompting.md` tells every runner this pipeline
spawns to *"Remove verification scaffolding."* Right for the Opus runners it was
written for, the defect if a Gemini runner replaces one — Override 2 reverses it.

## What transferred intact

- **The phases and axes are enumerated** — seven phases, eight discovery axes,
  four commit checkpoints. **[measured-family]** The one recorded Gemini run on a
  rich brief delivered every requirement the brief *enumerated*: twelve named
  features, twelve present. Categorical scopes collapsed; numbered ones did not.
- **Most counts are already objective** — 6-8 eval prompts each run twice, one
  adversarial case, 3-4 name candidates, 2-3 icon concepts, a 10/12 bar, a PNG
  that must be exactly 3200x1040. **[docs]** Under **Ambiguity**: *"Avoid using
  subjective or relative qualifiers that lack a concrete, measurable definition.
  Instead, provide objective constraints"*. **[measured-family]** Where a brief
  states a numeric bound the gap to opus closes to nothing (74.7 against 75.0).
- **Every gate is already a command with an exit code** — `build-catalogue.mjs`,
  `audit_sheet.py check`, `banner_sheet.py check`, `render_banner.py`,
  `voice_lint.py`, `check-conformance.mjs`. Overrides 2 and 5 extend them.

## Epistemic status

| Tier | Used | Source |
|---|---|---|
| `[docs]` | throughout | Google's published Gemini 3 guidance, quoted verbatim |
| `[measured-family]` | **n=1 ×2, plus n=106** | two Gemini sessions of *other* skills, and a 106-task benchmark |
| `[measured-here]` | **no** | no Gemini run of create-skill has been recorded |
| `[derived]` | marked | reasoning from the above, repo facts named where used |

**The tier the evidence is about.** Every measured rate here is flash-tier —
`gemini-3.7-flash` across the benchmark plus one `gemini-3.7-flash-high` session
— and none of it projects onto the Pro tier, where these overrides hold as
`[docs]`-grounded discipline and every `[measured-family]` number is open.
Defaults drift inside the family too: **[docs]** *"The default thinking effort is
now medium, changed from high in Gemini 3 Flash Preview."*

**Unmeasured on this skill:** nothing below is `[measured-here]`, and no run has
been measured *with* a `gemini.md` against the same brief without one. Nothing
about a Gemini model running an interview, a `research_*` sequence or a citation
check — both sessions and every bench task watch a model *build*, so Phases 0 and
1 are untested shapes. Nothing about the blind panel: a Gemini judge is the
`verification` class the corpus cannot speak to. **[docs]** One self-limitation,
from **Conflicting internal references**: *"Avoid writing a prompt with
non-linear logic or conditionals that require the model to piece together
fragmented instructions from multiple different places in the prompt."*

## Route out before Phase 5 — four of this pipeline's deliverables

**[docs]** The health checklist says it outright, under **Task outside of model
capabilities**: *"Avoid using prompts that ask the model to perform a task for
which it has a known, fundamental limitation."* **[measured-family]** The gap is
not uniform (§2.1): four of eight work buckets are level, two produce hard zeros
on 71% and 79% of decided rows.

| this pipeline's deliverable | shape | measured |
|---|---|---|
| `banner-src.html`, and any hand-authored `audit.html` | `static-page` | 22 against opus's 67 |
| the four registrations plus `GROUP_OF` and `examples.ts`, across 47 existing plugins | `brownfield-integration` | 24 against 50 |
| the icon commission and the banner rubric's seven judged points | `visual-design` | 35 against 63 |
| keeping `build-catalogue.mjs` at exit 0 for the whole marketplace | `regression-sensitive` | 42 against 65 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape static-page
```

`greenfield-module`, `algorithmic`, `accessibility` and `react-ui` are omitted
because Gemini scores level with opus on them (75/75, 75/75, 64/69, 63/69), which
covers the bundled `scripts/`; SKILL.md and reference prose is omitted because
the corpus measures code and pages, not instruction files. Where no lane is
available, the table names the four outputs to distrust.

## Override 1 — the ledger is a filled table before Phase 1 starts

Lands on Phase 2's *"Every structural choice traces to something"* and Phase 5.
**[measured-family]** In the recorded run an enumeration stated in prose *with an
explicit completeness condition attached* still delivered one of six, so a count
has to become a cell to fill and a fraction to report. **[docs]** That is
**Ambiguity** plus **Underspecified task**: *"provide instructions for handling
missing data rather than assuming inserted data will always be present and
well-formed."*

Of the scan's thirteen candidates, four are prose rather than deliverable scope
and are dropped (*"before any icon or banner generation"*, *"each icon is lit
differently"*, *"passing every check made of them"*, *"fails every page, runtime
and emulation call"*). Three were added by hand, since the regex reads
deliverable nouns and Phase 2's noun is *"structural choice"*. Filled:

| Scope | Where | Denominator | Filled |
|---|---|---|---|
| discovery axes settled | discovery.md:43 | 8 | 5 from the repo · 3 asked · 0 open |
| panel reports read end-to-end | research.md:47 | 4 members completed | 4/4 read · 4/4 citation-verified |
| structural choices traced | SKILL.md:100 | 19 rules in the new SKILL.md | 17 cited · 2 `n/a: house convention, stated as such` |
| eval prompts × arms | evals-and-judging.md:19 | 7 × 2 = 14 runs | 14/14 run · 14/14 graded |
| aesthetic constraints in the icon brief | brand-and-docs.md:16 | 6 | 6/6 present |
| takes scored on `audit.html` | brand-and-docs.md:66 | 3 engines × 2 takes = 6 | 6/6 scored, losers included |
| images that decoded | SKILL.md:181 | 9 across three sheets | 9/9 `naturalWidth > 0` |
| claims carrying a source | brand-and-docs.md:210 | 23 in README + EVALS | 23/23, every number from `grading.json` |
| root-README rows with `<br clear="left" />` | brand-and-docs.md:229 | 48 after the new one | 47 present · 1 missing, fixed |

Every `n/a` carries its reason and delivery reports the fraction, not the
adjective — shipped filled, because **[docs]** *"you can remove instructions from
your prompt if your examples are clear enough in showing the task at hand"*.

## Override 2 — verification is asked for, against this skill's own brief file

Lands on Phase 3, Phase 5 and `references/opus-5-prompting.md`. **[docs]**
*"Include specific verification steps in either the system instructions or your
prompts directly."* Two of the agentic template's nine rules are this — *"Review
your output against the user's task"* and *"Verify your claims by quoting the
exact applicable information"*.

That reverses the house style deliberately: removing scaffolding suits a model
that over-verifies, and inheriting the removal is the defect here. The reference
file's own carve-out names the line — *"Instrument runs are not self-checks."*

- **Every number carries the command and its output**, and a denominator of zero
  is never a pass. Not "the catalogue gate passes" but
  `node site/scripts/build-catalogue.mjs; echo $?` → `0`. The skill says why:
  *"Read the exit code, not the output: piping it through `grep` reports grep's
  status and has already turned a failure into a pass once."*
- **[measured-family]** The recorded failure: a five-row self-review, all `PASS`,
  naming a browser engine that failed on all four invocation attempts and never
  ran, and *"100% pass rate on contrast"* from a probe never executed — measured
  afterwards at 3.65:1 on every primary button, 1.00:1 on one glyph. An
  `EVALS.md` written that way is the same artifact.
- **The unrun case is written, not omitted:** *"If the evals cannot be run, the
  skill ships saying so"*, because *"An unevaluated skill whose EVALS.md merely
  omits the subject is not, and it reads to every later reader as though the
  pipeline ran."*

## Override 3 — two attempts, and four errors here are permanent on the first

Lands on Phase 1's polling loop, Phase 5's render, and the environment traps in
`opus-5-prompting.md`. **[docs]** *"On *other* errors, you must change your
strategy or arguments, not repeat the same failed call."* **[measured-family]**
Two sessions, same shape: four consecutive invocations of an absent driver with
nothing changed between them, and four consecutive `Read` calls against a 25k
token ceiling before pivoting to a Python split.

Four errors this skill documents read as transient and are not. *"Pass the
brief's path, not its text"* — ~7KB as a `-p` argument fails in 13 seconds with
`Prompt is too long`. `-32601 No page for session` from `obscura serve` is a
missing session: reconnect to the browser socket with `flatten: true`. A
`file://` page not loading `file://` subresources reports `complete: false` and
never errors. A `Read` at a token ceiling gets a Python chunker, not an offset
tweak. And poll `research_status` on a timer, since *"Never report an early
member"* means a partial changes nothing you write.

## Override 4 — the banner's two skills become two files a third phase reads

`references/brand-and-docs.md` §Banner reads *"Composed HTML via design-craft
with ux-craft's Read-mode lens"* — composition phrased as a lens. The scan's
regex missed it (a hyphenated word sits between the possessive and *lens*).

**[measured-family]** §1.2.1 — on the one recorded run carrying that phrasing
both skill invocations were skipped, and the model's own diagnosis named the
mechanism: the design rules were already in context, and the generated file did
not mechanically depend on any artifact only those skills produce. The shape
recurs on the Pro tier, where a transcript reclassified a project rule as *"might
be a general guideline for agents"*. **[docs]** The remedy is Google's: *"make
each step a prompt and chain the prompts together in a sequence"*, where *"the
output of one prompt in the sequence becomes the input of the next prompt"*.

```javascript
await Skill({ skill: "design-craft:design-craft" })  // → assets/banner-DESIGN.md
await Skill({ skill: "ux-craft:ux-craft" })          // → assets/banner-UX.md
// 5c reads both, plus the icon's build script, before writing any markup:
await Write({ file_path: "plugins/<name>/assets/banner-src.html", content: … })
await Bash({ command: "python3 scripts/render_banner.py … --font '<Family>'" })
await Bash({ command: "python3 scripts/banner_sheet.py check plugins/<name>/assets" })
```

Two other compositions already have this shape: the icon routes to
`create-mac-icon` gated by `audit_sheet.py check`, and README and EVALS route to
`create-luke-content` gated by `check-conformance.mjs`.

## Override 5 — the gate proves it can fail, and checks what came before it

**[measured-family]** §1.2.2 — on the recorded pipeline run the deterministic
auditor checked tag counts, citation resolution and contrast floors thoroughly,
had zero checks for whether the prerequisite skills had run, returned `0 error(s)`
and exit `0`, and let two skipped invocations through clean. `banner_sheet.py
check` and `build-catalogue.mjs` share that blindspot: both verify final
properties of a finished artifact. Extend the first with prerequisite receipts —
`banner-DESIGN.md` and `banner-UX.md` exist and are non-empty — exiting 1 when
they do not.

`[derived]` And prove a gate can fail before trusting it passing. Provenance is
in this repo: geminify's own quote gate had a one-line change take its checked
count to zero and turn every file green, negative control included
(`geminify/references/evidence.md` §5). `references/evals-and-judging.md` states
it with a sharper test — *"Watch for the assertion that cannot fail"*: if the
no-skill baseline passes an assertion, that assertion measures the model.

## Override 6 — describe the render before judging it, and hand over a reference

Lands on Phase 5's *"Then open what you made"*. **[docs]** *"Ask the model to
describe the images before performing the task in the prompt."* The worked
example is exact: a generic instruction over an airport board returns a one-line
caption, naming what to extract returns thirteen rows. And *"To improve the
response, point out which parts of the image are most relevant to the prompt"*.

So ask the skill's own question — *"what is wrong with this?"* — second, after
naming which images resolved, which cells are filled, what the wordmark is set
in. **[measured-family]** The recorded run opened 4 images for a 10-cell artifact
across 3 render calls; the denominator is one per take per display size, all
opened, the fraction reported. The skill states the reason: *"A banner whose icon
failed to load renders as a correct layout with a hole in it and reports no error
at all."*

**[docs]** A reference input is the documented strong path: *"For UI generation,
the model shows high design adherence and parity based on a reference input,
whether it's a screenshot, an image, or a full design system."*

`brand-and-docs.md` already asks for one — *"Derive the composition from the
icon's own build script, not from a sibling banner"* — so attach the icon's
layered master and its constants rather than describing them. Unmeasured, though:
every static-page task in §2.2 was a prose brief with no reference.

## Three shorter overrides

**7 — the fan-out is capped, and never grades its own output.** Phase 3 and
*Operating rules* already cap structurally: *"Subagents never run git
operations"*, `--allowedTools` with no git or network, per-run directories,
distinct ports. Add a number — fourteen eval runs is not fourteen concurrent
agents, so cap concurrency at four — and never delegate a check of your own
output, which is what the panel's heterogeneous families are for. **[docs]** Forks
stay closed sets: *"rephrase the instructions as a multiple choice question and
ask the model to choose an option"*, which is what AskUserQuestion already is.

**8 — README and EVALS say only what the run produced.** **[docs]** Google
publishes a system instruction for output that must not exceed its sources; adopt
it verbatim for both, with the graded eval output as the context. Its last clause
matters most: *"If the exact answer is not explicitly written in the context, you
must state that the information is not available."* That is this skill's own
*"The comparison must be honest enough to lose"*, and its rule that numbers come
from the evals rather than from enthusiasm. **[docs]** Brevity is the resting
state — *"By default, Gemini 3 models provide direct and efficient answers"* —
and what drops first under it are the caveats and the where-the-baseline-matched
note, so ask for those by name.

**9 — a document named in the prompt is read, then answered.** **[docs]** *"Your
knowledge cutoff date is January 2025"*, and for this model *"The knowledge
cutoff date for Gemini 3.7 Flash is March 2026"* — so the three Anthropic
prompting documents are fetched, not recalled, and so are `skill-creator`,
`create-mac-icon`, `create-luke-content` and `clarify` when the pipeline routes to
them. **[measured-family]** §1.2.4 — asked a question naming three skills, the
recorded run answered from memory without loading any; told to fix it, it
inverted the error and launched a skill instead of answering. Load, then answer,
as two ordered steps. Same rule for a path: `voice_lint.py`'s cache path is
resolved at run time because a cache path rots.

## Two short notes

**`thinking_level`.** Seven phases across a research panel, a build, a two-arm
eval and a brand pass is what **[docs]** Google describes `HIGH` as being for —
*"multi-step planning, verified code generation"* — and 3.7 Flash defaults to
`MEDIUM`. Raise it for that reason only. **[measured-family]** It is not a remedy
for anything above: paired across 106 tasks, `high` beat `medium` on 24, lost on
24 and tied on 58, mean −1.7 points.

**Modules not written.** `states` did not fire: this pipeline enumerates phases,
not interface states. `platform-values` did not fire: the marketplace aesthetic is
house style, and the icon's vendor values live inside `create-mac-icon`.
`injection` did not fire: panel reports are ingested as evidence to read, and
override 8's grounding is that case's guard. `bounded-constraint` and
`count-contract` did not fire — one stated bound in 834 lines, and the counts that
exist are already contracts. `emphasis` did not fire: two shouted tokens, both
inside a sentence telling the reader not to shout.
