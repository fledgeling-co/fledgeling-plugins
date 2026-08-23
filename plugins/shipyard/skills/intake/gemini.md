# shipyard:intake, calibrated for Gemini

Read this in one pass before `## Inputs`, then run the skill as written. Each override names the section it lands on, because a
conditional side-file is otherwise the shape Google's checklist warns about — **[docs]** *"Avoid writing a prompt with
non-linear logic or conditionals that require the model to piece together fragmented instructions from multiple different
places in the prompt."*

**No route-out block here, and that is a decision.** **[docs]** The checklist's **Task outside of model capabilities** entry —
*"Avoid using prompts that ask the model to perform a task for which it has a known, fundamental limitation"* — is the sentence
such a block applies, but geminify's corpus measures a model building **code and rendered pages**. This stage writes markdown
briefs and runs research: `static-page` and `visual-design` are shapes it never produces, `brownfield-integration` and
`regression-sensitive` are about editing a working codebase. No row lands, so routing stays on policy and every override below
applies to work that stays here.

## What transferred intact

Naming these matters: effort spent re-hardening a working rule is effort not spent on the decomposition.

- **The brief template is already a filled few-shot example** (SKILL.md:63–80) — five metadata fields, three body sections,
  each with its own bracketed instruction. **[docs]** *"We recommend to always include few-shot examples in your prompts …
  you can remove instructions from your prompt if your examples are clear enough in showing the task at hand"*, and **Missing
  output format specification** asks for exactly this: *"use a clear, explicit instruction to specify the format and show the
  output structure in your few-shot examples."* Most geminify targets have to be given this. This one has it.
- **The platform set is enumerated, not categorical** — `iPhone, iPad, Mac, and Web always; Windows optional` (SKILL.md:46–48).
  **[measured-family]** Enumerated requirements are what one Gemini run delivered in full: twelve named features, twelve
  present. Categorical ones collapsed. This line is on the right side of that split already.
- **The procedure is already a chain with file outputs.** Step 2 writes `docs/deep-research/<slug>.md`, step 5's `research:`
  field points at it, step 6 registers the files. **[docs]** *"Chain prompts: For complex tasks that involve multiple
  sequential steps, make each step a prompt and chain the prompts together in a sequence. In this sequential chain of prompts,
  the output of one prompt in the sequence becomes the input of the next prompt."* Override 4 closes the one link that is
  missing rather than rebuilding the chain.
- **`A human deletes a file to veto`** (SKILL.md:99) and the assumption line naming `the alternative it beat`. Both convert a
  question into an artifact, which is the same move every override below makes.

## Epistemic status

| Tier | Used here for |
|---|---|
| `[docs]` | Google's published guidance, quoted verbatim from `geminify/references/gemini-corpus.md` |
| `[measured-family]` | `Egress Gemini` (2026-08-17, **n=1**), `COD Dossier` (2026-08-23, **n=1**), and 106 benchmark tasks scoring `gemini-3.7-flash` at two effort levels against `claude-opus-5` |
| `[derived]` | reasoning from those two, labelled as such |

**Which model the measured claims are about.** Every measured rate behind this file is flash-tier — `gemini-3.7-flash`, plus
one `gemini-3.7-flash-high` session — and none of it transfers to the Pro tier, where the thinking default and the knowledge
floor differ: **[docs]** *"If thinking_level is not specified, Gemini 3 will default to high"*, against the 3.5 Flash note that
*"The default thinking effort is now medium, changed from high in Gemini 3 Flash Preview."* On Pro the overrides hold as
`[docs]`-grounded discipline and every `[measured-family]` number is open.

**Unmeasured on this skill:**

- No Gemini run of `shipyard:intake` exists, and no run anywhere has been measured **with** a `gemini.md` in place against the
  same work without one. Every override is a derived mechanism, not a demonstrated fix.
- **Nothing measures a model ideating.** Both sessions and all 106 benchmark tasks watch a model produce a specified artifact.
  Step 4's divergent pass — proposing features nobody asked for — is a work class the corpus is silent on, so Override 1's
  reading of it (a categorical scope with no number collapses) is transfer by mechanism, not by measurement.
- Nothing measures research quality, Dossier panel behaviour, or citation verification under this family.
- The scan's own reading of this skill needed correcting by hand: 9 of its 10 relative-qualifier rows matched the **noun**
  `brief` (a document), not the qualifier Google's checklist is about. One real row survives, at SKILL.md:19.

## Override 1 — the quota ledger, and the row that will come back as one

Lands on step 3 (*Decompose*) and step 4 (*Ideate past the ask*).

**[measured-family]** One Gemini run delivered every requirement its brief *enumerated* — twelve named features, all present —
and every requirement named *categorically* once or not at all: all surfaces → 5, all states → **1**, all menus → **0**, all
user flows → **0**, all actions → one generic toast reused across the product. **[docs]** The **Ambiguity** entry prescribes
the fix: *"Avoid using subjective or relative qualifiers that lack a concrete, measurable definition. Instead, provide
objective constraints (for example, "write a summary of 3 sentences or less" instead of "write a brief summary")."*

`the additional features the target audience would likely want or benefit from` is the categorical scope in this skill, and
`Propose what earns its place` is the qualifier attached to it. **[derived]** On the measured shape that lands as one proposed
brief, or none — and a stage whose whole purpose is generosity would have failed silently, because one brief is a plausible
answer. `scan_skill.py --refs` listed **0** quota rows here (its vocabulary is deliverable nouns like surface, state and
component, which a brief-writing stage does not use), so these are derived by hand from the two distributives it counted:

| Row | Source | Number to report |
|---|---|---|
| Prior-art sources checked for duplicates | SKILL.md:31–36 | 4 of 4 — `features-to-triage/`, ledger/board, `deep-research/`, out-of-scope record |
| Asked-for features decomposed from the idea | SKILL.md:44 | `N`, each a demoable vertical slice |
| Companion classes considered in step 4 | SKILL.md:56 | 5 of 5 — settings, onboarding, sharing, offline, notifications — each `proposed` or `n/a: <reason>` |
| Second-order ideas the research surfaced | SKILL.md:57 | `K of K` research findings converted or dismissed with a reason |
| `proposed-by-ai` briefs written | SKILL.md:58 | `M`, and `M` is reported beside `N`, never merged with it |
| Metadata fields filled per brief | SKILL.md:65–70 | 5 of 5 (`research:` omitted only where none ran) |
| Body sections filled per brief | SKILL.md:72–79 | 3 of 3 |
| Acceptance-sketch bullets per brief | SKILL.md:76 | 3–8, counted |
| Assumption lines per brief | SKILL.md:79 | `N of N` decisions made while decomposing, each naming the alternative |
| Briefs registered on the lane | SKILL.md:82–88 | `N+M of N+M` (tasks created, or files written + fleet inbox appended) |

Delivery line, filled rather than described: `4 of 4 duplicate sources checked (2 near-matches, 1 previously rejected —
surfaced) · 3 asked-for briefs · 5 of 5 companion classes considered, 2 proposed, 3 n/a · 4 proposed-by-ai briefs · 7 briefs ×
5 metadata fields, 35 of 35 · 7 × 3 sections · sketches 4–6 bullets · 11 assumption lines`. **[docs]** *"Include specific
verification steps in either the system instructions or your prompts directly."*

## Override 2 — the bounds, read back off the briefs rather than agreed with

Lands on step 5 and on the `Rules` block. It points the opposite way to Override 1, which is why it is separate.

**[measured-family]** Across 106 benchmark tasks, `gemini-3.7-flash`'s failing UI assertions were 58% bound-shaped at `medium`
and **86%** at `high`, against 8% for opus and 6% for the OpenAI lane; the most-repeated bound failed on *every* instance in its
set on a run that passed 37 of its other 39 assertions. A quota under-delivers; a bound is exceeded while everything asked for
is present, so it survives every check that looks at what you did produce. `Briefs, not specs` is that exposure exactly — a
brief carrying file paths still looks like a good brief.

The scan listed **1** bound row and counted **6 prohibitions in prose**; the countable ones move across:

| instance | property | stated bound | readback | observed | within? |
|---|---|---|---|---|---|
| each brief | features per file | exactly 1 (SKILL.md:61) | count `^# ` headings per file | 1 | yes |
| each brief | implementation detail | 0 file paths, 0 architecture, 0 decisions (SKILL.md:94) | grep for `/`-bearing backticks, `src/`, `component`, `endpoint`, `schema` | 2 in one brief | **no** |
| each brief | ids allocated | 0 (SKILL.md:82) | grep for the ledger's id pattern | 0 | yes |
| each proposal | bundled into an asked-for brief | 0 (SKILL.md:99) | every `proposed-by-ai: true` is its own file | 0 | yes |
| whole run | questions put to the user | 0 unless the gate survives (SKILL.md:96–98) | count `AskUserQuestion` calls; each needs its recorded gate step | 0 | yes |
| whole run | proposed briefs vs asked-for | `ten padded briefs bury the three good ones` (SKILL.md:59) | ratio `M : N`, stated in the summary | 4 : 3 | stated |
| research | panels bought before the free lane | 0 (SKILL.md:101) | read the run's tool order: `research_plan` then local, then paid | 0 | yes |

**[docs]** Google treats these as a component in their own right — *"Restrictions on what the model must adhere to when
generating a response, including what the model can and can't do"* — and names where they go: the **Recap** component is a
*"Concise repeat of the key points of the prompt, especially the constraints and response format, at the end of the prompt."*
**[derived]** The trap: a bound written as a prohibition reads as style advice. `No file paths, no architecture, no
implementation decisions` and `0 path-shaped strings across 7 briefs` are the same requirement, and only the second gets read.

## Override 3 — research claims carry the command that checked them, and the cost

Lands on step 2 and on step 6's closing summary.

**[measured-family]** This is the measured failure and it is a research-shaped one. A Gemini run wrote itself a review with
five well-formed `PASS` rows — a named engine that failed all four invocation attempts and never ran, a *100% pass rate on
contrast* from a probe never executed, and an audited-target count nothing produced. Not dishonesty: a requested **shape**
completed where the shape was specified and the procedure was not. A `research:` line in a brief is a specified shape, and a
`docs/deep-research/<slug>.md` that no panel wrote satisfies it just as well from the outside.

**[docs]** *"Verify your claims by quoting the exact applicable information (including policies) when referring to them"*, and
*"Include specific verification steps in either the system instructions or your prompts directly."* So:

- A brief's `research:` field points at a file that exists and is non-empty — check it, do not assume the step ran.
- `research_verify_citations` runs **before** any finding reaches a brief, and its output is pasted. A resolving URL is not a
  supporting one, and support is counted in independent domains rather than in how many backends agreed.
- The cost is stated as a number from `research_plan`, not as an impression. A denominator of zero is a panel that never ran.
- Where research was skipped as `already concrete and internal` (SKILL.md:43), the summary says so in one line. Silence reads
  as forgotten.

**[derived]** All of this reverses the house style deliberately. Stripping verification scaffolding is right for a model that
over-verifies; inheriting that removal here is the defect this file exists to undo.

## Override 4 — the one link in the chain that nothing downstream requires

Lands on step 4's `Run the trawl skill for a divergent pass`.

**[measured-family]** On `COD Dossier`, a skill said *every design decision goes through `design-craft` with `ux-craft`'s
lens*; **neither** skill was invoked. The model's own diagnosis named the mechanism: the general rules were already in context,
and the artifact it was writing did not depend on any concrete file those skills produce, so the instruction read as a standard
to satisfy rather than a call to make. The same shape is reported outside this repo — an Antigravity user's subagents ignoring
instructed skills, and a Gemini 3 **Pro** transcript reclassifying a `GEMINI.md` rule as *"a general guideline"* (`evidence.md`
§7.2) — which is why the conversion is worth doing on every tier.

`scan_skill.py` flagged **0** qualitative skill references here, and the phrasing is imperative rather than lens-shaped.
**[derived]** The exposure survives anyway, because step 5 can write every brief without `trawl` having produced anything. So:

```
Step 2   Dossier panel      → docs/deep-research/<slug>.md              (already required by step 5's research: field)
Step 4   Skill trawl        → docs/features-to-triage/.ideation/<slug>-trawl.md
                              one line per divergent idea, each kept-or-dropped with a reason
Step 5   write the briefs   — opens both files first; a step-4 brief cites the .ideation line it came from
Step 6   register           — an empty or absent .ideation file means step 4 did not run, and the summary says so
```

**[docs]** *"When model outputs must be machine-readable or follow a specific format, use a widely recognized standard like
JSON, XML, Markdown or YAML that can be parsed by common libraries"* — which is what makes `M proposed briefs from K ideation
lines` checkable rather than recalled.

## Override 5 — read the four sources, then answer; and market facts get read, never recalled

Lands on step 1 and on step 2.

**[measured-family]** On `COD Dossier`, asked a question naming three skills, the run answered from memory without loading any;
asked to fix that, it inverted the error and launched a skill instead of answering. There is no stable mapping from "named in
the prompt" to "loaded". Two ordered steps, neither substituting for the other: `docs/features-to-triage/`, the ledger/board,
`docs/deep-research/` and the out-of-scope record get **read**, and *then* the decomposition gets written. A duplicate check
run from memory is how `night theme` gets written beside `dark-mode`.

**The same rule is why step 2 exists at all.** **[docs]** *"Your knowledge cutoff date is January 2025"*, and for this model
*"The knowledge cutoff date for Gemini 3.7 Flash is March 2026 — users can expect updated information for some domains while in
others they may experience the model's knowledge is limited to January 2025 (in line with the Gemini 3 Model Family)."* Market
norms, prior art and what a competing product does today are exactly the facts that go stale, and the remedy is stated:
*"Grounding with Google Search connects the Gemini model to real-time web content, and should be enabled whenever the model may
need to know obscure or recent facts."* **[measured-family]** The observable form of a stale fact is not a hedge — one run
returned a *previous-generation published value* (a superseded platform accent colour) with full confidence. An `audience` line
or a competitor claim written from recall will read exactly like one that was sourced.

**[measured-family]** And the retry ceiling on the way there: a `Read` against a hard 25k-token ceiling was retried four times
with offset tweaks in one run before a Python split worked. **[docs]** *"On *other* errors, you must change your strategy or
arguments, not repeat the same failed call."* A long research export gets ranged reads or a script on the first refusal.

## `thinking_level`

**[docs]** A duplicate sweep, a research pass, a decomposition, a divergent pass and seven briefs is what Google describes
`HIGH` as being for — *"multi-step planning, verified code generation"* — and Gemini 3.7 Flash defaults to `MEDIUM`. Leave
sampling parameters alone: *"we strongly recommend keeping them at their default values for Gemini 3.x models."*

**[measured-family]** Write that as what the level is *for*, never as a remedy. Paired across all 106 benchmark tasks, `high`
beat `medium` on 24, lost on 24 and tied on 58 — mean −1.7 points — and the bound failures got *worse* at `high` (86% of
failures against 58%). Nothing in Overrides 1–3 improves by raising it. **[docs]** The one honest reason to prefer `HIGH` here
is tool volume: *"Higher thinking levels encourage the model to use more tools to explore and verify, so lowering the level can
reduce tool calls"*, and this stage's exposure is too few sources read.

## Modules not written, and why

The scan fired **none** — core only, at the ≥3-trigger threshold, which is the right result for a stage that renders nothing
and ships no probe. Two were close enough to name. **`authorship`** reached its triggers only through `research` and
`citation`; its content is the grounding discipline, which arrives as core in Override 5 and as the citation check in
Override 3 rather than as a module. **`bounded-constraint`** did not fire on 1 listed bound row, yet its mechanism is what
Override 2 carries, from the 6 counted prohibitions the scan declined to list. **`visual`**, **`gate`**, **`states`**,
**`platform-values`**, **`delegation`**, **`injection`** and **`count-contract`** did not fire and are not written.
**`emphasis`** found **0** shouted words in 101 lines — nothing to de-escalate.
