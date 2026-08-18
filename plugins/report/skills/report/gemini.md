# report, calibrated for Gemini

Read this once before Phase 0, then run the skill as written with these overrides.

The skill opens on a distinction this file has to make about itself: three sentences render
identically — a number *measured*, one *read off a single sample*, one *inferred from two facts
established separately* — and a week later nobody can tell which. `claims.json` is that distinction
turned into cells, which is the whole difference on this family: a tier stated as a discipline gets
read, a tier stated as a cell gets filled. Below, that move applied to the other prose scopes.

## Epistemic status

| Tier | Used here for |
|---|---|
| `[docs]` | Google's published Gemini guidance, verbatim from `geminify/references/gemini-corpus.md`. The strongest tier, and most of this file rests on it. |
| `[measured-family]` | One recorded Gemini run — `Egress Gemini`, 2026-08-17 — of a *different* skill, a two-platform UI mock. **n=1.** It did not invoke this skill. |
| `[measured-here]` | `scan_skill.py` over this SKILL.md and its eight references, 2026-08-18: 3,036 lines, 32 quota rows, 5 modules, **0 emphasis tokens**. A scan of the text, not a Gemini run. |
| `[derived]` | My reasoning from those, said as such. |

Measurements quoted from the target's own references — the Obscura `:has()` finding, the twenty
divider violations, the 614KB hero — are its record of Claude runs, not evidence about this family.
**Unmeasured on this skill:** no Gemini run of `report` has been observed at all, so nothing below is
measured on this target — not the three-reading collapse, not citation integrity surviving
simplification, not the six-capture protocol, not whether `audit_report.py`'s exit code gets treated
as the verdict. No comparison exists between a run with this file and one without, and nothing here
is a rate.

**[docs]** A caution about this file's shape: *"Avoid writing a prompt with non-linear logic or
conditionals that require the model to piece together fragmented instructions from multiple different
places in the prompt."* Read it in one pass — each override names the phase it lands on.

## What transferred intact

- **`claims.json` is already the mechanical form.** `kind`, `confidence`, `sources`, `support`,
  `limits`, `from`, `reasoning` are named cells. **[docs]** *"When model outputs must be
  machine-readable or follow a specific format, use a widely recognized standard like JSON, XML,
  Markdown or YAML that can be parsed by common libraries."*
- **The gates are real gates.** `audit_report.py` exits 1 on any ERROR and checks ledger against
  page *both ways*; `export_pdf.mjs`, with poppler absent, reports A4 geometry and page count as
  `NOT checked` rather than as a pass — the `gate` module's hardest rule, already written.
- **Several scopes already carry numbers**, which is why they survive here: 3–6 categories, three
  ranked picks, three to five cited claims, six captures, 24px and 16px gutters, 45–75 characters,
  120–250ms. **[docs]** *"Instead, provide objective constraints"* — these already are.
- **The skill does not shout** — `[measured-here]` zero MANDATORY / CRITICAL / FORBIDDEN tokens in
  3,036 lines — and its substitution rule is the right instinct: *only one of them is fine*
  (SKILL.md:405). Extend it rather than replace it.
- **`report-craft.md:619` already states the failure this file is about:** *a categorical
  instruction — "all states designed" — ships as one state; a grid with cells in it does not.* The
  override applies that sentence to the four other categorical scopes.

## The quota ledger — filled, not described

**[measured-here]** The scan returned 32 categorical rows. I bound **18** and dropped **14** as
prose rather than deliverable scope: failure-story narrative (`product-verdicts.md:18`), quoted
example wording (`:179`), rationale clauses (`report-craft.md:62`, `:73`), study descriptions
(`visualisation.md:261`, `:264`), an evidence-file heading, "survives print at any size" twice.

**[docs]** *"Avoid using subjective or relative qualifiers that lack a concrete, measurable
definition."* Write this into the report directory before Phase 4 with your run's numbers. Filled
here from a nine-claim report with two figures and one image:

| Scope, and where the skill states it | Denominator | Filled | Delivery line |
|---|---|---|---|
| **every claim** × three readings — SKILL.md:34, :47, :196; `readings.md:288` | 9 claims × 3 registers = **27** wordings | 25 written, 2 `omit` + `omitReason` | `27/27 accounted: 25 written, 2 omitted with reasons` |
| **every claim** carries its marker in every register — `report-craft.md:212`, backlinks `:438` | 27 renderings, ≥1 marker each | 27 | `cite→source and source→cite green on all three slices` |
| **every figure** through `dataviz`, checked at 400px — SKILL.md:80, :394; `report-craft.md:518`; `visualisation.md:91` | 2 figures × 3 registers = **6** static frames | 6 frames, 6 width checks, `tabular-nums` on both | `6/6 frames, 6/6 checked at 400px` |
| **every image** carries caption + provenance + registry row + alt — SKILL.md:576; `evidence-harvest.md:200`; `source-imagery.md:46`, `:81`, `:146` | 1 image × 4 fields = **4** cells | 4 | `1 image, 4/4 fields, basis "captured here"` |
| **every control** gets micro-interaction feedback — SKILL.md:4; state grid `report-craft.md:618`–`619` | 6 rows × 7 columns = **42** cells | 34 real, 8 `n/a: fetches nothing` | `42/42 resolved, 34 real, 8 n/a with reasons` |

**[measured-family]** Why a table and not the sentence: on the observed run every enumerated
requirement shipped (12 of 12 named features) and every categorical one shipped once or not at all
— *all states* → 1, *all menus* → 0, *all flows* → 0. **[derived]** Here the categorical scopes are
*multiplied* rather than listed — registers × claims, registers × figures, rows × columns — so a
collapse loses two thirds of the document while leaving a page that audits as complete on `brief`.

## Override 1 — the tier is a cell that gets filled (Phase 1)

- **`confidence` is about the evidence, not the feeling** (`evidence-harvest.md:61`). Make it
  derivable: `high` = a command with its output in the transcript, or a file with a line range;
  `medium` = one sample, one workload, one tenant, or a published verdict whose measurements are
  paywalled; `low` = a single unrepeated observation.
- **`limits` is never empty on a `medium` or `low` row.** The auditor only warns there; treat the
  warning as a block. **[docs]** *"provide instructions for handling missing data rather than
  assuming inserted data will always be present and well-formed."*
- **`support` names the passage, not the file.** `worker.ts:88-104 — maxRetries = 3 guards the
  catch` is support; `See the worker file` is not.

**[docs]** Adopt the strictly-grounded system instruction for the Phase 2 writing pass, and note
its last clause: *"If the exact answer is not explicitly written in the context, you must state that
the information is not available."* Also *"Do not assume or infer from the provided facts; simply
report them exactly as they appear."* That is the skill's *"The session did not establish this" is
publishable* rule with a mechanism behind it, so give the writing pass the ledger rows and nothing
else. **[derived]** One carve-out: a ratio you computed from two rows is *your* claim, so it is an
`inference` row with a non-empty `from`, as `product-verdicts.md` requires of a ranking.

## Override 2 — three passes from the ledger, never one pass and two rewrites (Phase 2)

The skill forbids the shortcut at SKILL.md:198–200: *Three passes from the ledger produce three
registers of one argument; one pass plus two rewrites produces one register and two translations
of it, and it reads that way.*

**[docs]** Google's remedy is structural. Under **Too many tasks**: *"Break the requests into
separate prompts."* And *"make each step a prompt and chain the prompts together in a sequence."*
So run Phase 2 as three chained passes each taking the ledger as input, never another register's
finished prose.

**[derived]** *A reading may change the words, it may never change what is claimed* is where the
model's default fights the skill, because the caveat-free sentence genuinely reads better. Make it
checkable: after each register, diff its numbers against `claims.json` — unit present, direction
unchanged, magnitude unchanged, hedge present wherever `confidence` is not `high`. **[docs]**
Arithmetic is a tool call: *"Gemini's code execution tool enables the model to generate and run
Python code, and should be enabled whenever the model needs to perform any kind of arithmetic,
counting, or calculation."* That covers §3's front-page recomputation and every Primer
re-expression such as 95.4% becoming `about 19 in every 20`.

## Override 3 — verification is asked for, and this reverses the house style (Phase 7)

**[docs]** *"Include specific verification steps in either the system instructions or your prompts
directly."* From the agentic template, *"Review your output against the user's task"* and *"Verify
your claims by quoting the exact applicable information"*. **[derived]** Skills here are written for
a model that over-verifies, so verification scaffolding gets stripped; inheriting that removal is
the defect, because `audit_report.py` and `export_pdf.mjs` only run if something runs them.

**[measured-family]** What fills the vacuum is well-formed and false: a review naming a browser
engine that failed all four invocation attempts and never ran, and *"100% pass rate on contrast"*
from a probe never executed — measured afterwards at 3.65:1 on every primary button and 1.00:1 on
one glyph. A requested shape completed without the procedure that earns it. The delivery note is
the fix, filled rather than described:

```
GATES — docs/reports/queue-drops/
  audit_report.py          exit 0   38 ok, 0 error, 3 warn
                           warn ledger:limits — c14 low, limits empty → filled, re-run
  export_pdf.mjs index     exit 0   brief printed, 7 pages / 9 blocks, A4 595x842pt
  export_pdf.mjs technical exit 0   technical printed, 9 pages
  export_pdf.mjs tldr      exit 0   1 page
  design-review            3 of 6 captures — dark not taken, theme emulation inert
                           REPORT SAYS: dark theme unmeasured on this report
```

A denominator of zero is a gate that never ran, never a pass — `0 errors` with no count of checks
beside it is not a result. Paste exit codes and counts, not a sentence about them; where a runner
could not run, name the axis the artifact is ungated on, as `export_pdf.mjs` already does for
itself. The substitution rule extends here: a methods-note line when a gate did not run.

## Override 4 — the retry ceiling (any phase that shells out)

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same
failed call."* **[measured-family]** Four consecutive invocations of one banned, absent tool with
nothing changed between them. So: two attempts per tool, then change approach; a permanent error —
`command not found`, a missing MCP — gets one, and the answer is the substitution line rather than a
fifth attempt. Read constraints first: poppler may be absent, the Mobbin MCP may not be installed,
`@tanstack/charts` is pre-alpha at `0.14.0`, `media-gen-pro` calls bill.

## Override 5 — six captures, and describe the crop before judging it (Phase 7)

The skill says *six captures, not one* — three readings × light and dark — and knows why a scripted
toggle cannot produce them: setting `.checked` from script does not re-evaluate the `:has()`
selector on Obscura, so three renders measure one register and report three passes. `export_pdf.mjs`
rewrites the source instead; do the same for captures, and mark a cell done only when it was opened:

| | light | dark |
|---|---|---|
| primer | opened, described | opened, described |
| brief | opened, described | **not taken** — theme emulation inert on this engine |
| technical | opened, described | **not taken** |

**[docs]** *"Ask the model to describe the images before performing the task in the prompt."*
Google's example is exact: "describe this image" of an airport board returns a one-line caption,
while naming what to extract returns the thirteen rows. So per capture, in order: name what is in
it — register indicator, TLDR block, figure and caption, citation markers, divider gutters —
**then** judge it. And *"To improve the response, point out which parts of the image are most
relevant to the prompt."* **[measured-family]** On the observed run, 3 render calls and 4 images
opened covered a 10-cell artifact.

## Override 6 — vendor values get read, not recalled (Phases 3, 5, verdict layer)

**[docs]** *"Your knowledge cutoff date is January 2025."* For 3.7 Flash, *"users can expect
updated information for some domains while in others they may experience the model's knowledge is
limited to January 2025"*. **[measured-family]** The informative failure on the observed run was
not a guess but Windows 10's published accent colour on a Windows 11 app. The skill's own rule
names the fix — *stamp prices, versions and availability with a date* (`product-verdicts.md:208`)
— so make it a table filled before the first line of prose, each cell carrying its source tier:

| Value | What I wrote | Read from | As at |
|---|---|---|---|
| `@tanstack/charts` release | `0.14.0`, pre-alpha | its README, fetched this session | 18 Aug 2026 |
| GSAP plugin licensing | free incl. commercial use | GSAP/Webflow announcement, fetched | 18 Aug 2026 |
| A candidate's price or version | — | the vendor's own pricing page, fetched | — |

A cell you cannot tag is a value you invented. **[docs]** *"Grounding with Google Search connects
the Gemini model to real-time web content, and should be enabled whenever the model may need to
know obscure or recent facts."* **[derived]** A remembered version number is exactly what
`evidence-harvest.md` bans — *a statistic you know but did not check here* — in technical clothes.

## Override 7 — the delegation cap, and the forks as closed sets

The skill already caps this: delegate only for a wide sweep reconstructing a long session, *keep
the count low*, subagents never run git operations. Write the number down: **one subagent maximum,
for the Phase 1 harvest; zero elsewhere** — a report is one argument in three registers, and
splitting the writing across agents produces three documents.

**[docs]** Google's guidance on a model that answered correctly but *"didn't stay within the
bounds of the options"* prescribes reframing as a closed choice. Several forks here stay live:
`/report tldr` versus the full report, three build lanes per figure, three.js against its six
tests, whether the verdict layer applies. Resolve each in writing before Phase 4. And **[docs]** on
low-risk reads, *"Prefer calling the tool with the available information over asking the user"* —
matching the skill's instruction to answer Phase 0 from the conversation first.

## One worked example, before the set

**[docs]** *"We recommend to always include few-shot examples in your prompts."* And *"you can
remove instructions from your prompt if your examples are clear enough in showing the task at
hand."* Author one claim at full fidelity before any other row:

```json
{ "id": "c7",
  "text": "Cache reads were 95.4% of tokens sent across the 28-window sample.",
  "kind": "direct", "confidence": "high", "sources": ["s3"],
  "support": "logs/bench-2026-08-07.txt:1180-1204, summed per window",
  "limits": "One tenant, 28 consecutive days. Not a spend share — see c9.",
  "readings": {
    "primer": "Almost 19 out of every 20 words sent were ones the computer had seen before.",
    "brief": "95.4% of tokens sent are cache reads, so the headline rate is not the rate you pay.",
    "technical": "Cache-read share is 95.4% of 3.48B raw tokens, n=340 across 28 windows." },
  "blocks": ["b3"] }
```

**[docs]** *"Make sure that the structure and formatting of few-shot examples are the same to avoid
responses with undesired formats."* Every later row carries the same keys in the same order,
`limits` included even where its value is `Read from source; no runtime measurement.`

## `thinking_level`, and where brevity bites

**[docs]** Harvesting a ledger, writing three registers over it, building the page and auditing
the artifact is what Google describes `HIGH` as being for — *"suitable for complex prompts
requiring deep reasoning, such as multi-step planning, verified code generation, or advanced
function calling scenarios"*. Gemini 3.7 Flash defaults to `MEDIUM`. **[docs]** And *"By default,
Gemini 3 models provide direct and efficient answers."* **[derived]** Brevity is the resting state,
so Primer — the register most vulnerable to losing a caveat — reaches a defensible length well
before the ledger's last row. The exit condition is the quota table's fractions.

## Modules deliberately not written

The scan fired five: `authorship`, `visual`, `gate`, `platform-values`, `delegation`, all above.
Four did not. **`states`** (2 triggers) — the grid at `report-craft.md:618` already has cells and an
`n/a`-with-reason rule, so it is bound as a quota row instead. **`count-contract`** — the skill
already promises counts, and deriving one where the brief omits it is folded into the quota table.
**`injection`** — repo research and fetched URLs are cited sources, `kind` keeps them data. And
**`emphasis`** — zero emphasis tokens, so nothing to defuse.
