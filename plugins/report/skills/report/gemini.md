# report, calibrated for Gemini

Read this once before Phase 0, then run the skill as written with these overrides.

A number *measured*, one *read off a single sample* and one *inferred* render identically. `claims.json` turns that
distinction into cells — the move throughout: a discipline gets read, a cell gets filled.

## Epistemic status

| Tier | Used here for |
|---|---|
| `[docs]` | Google's published guidance, verbatim from `geminify/references/gemini-corpus.md`. Most of this file rests on it. |
| `[measured-family]` | Gemini runs of *other* work: `Egress Gemini` (17 Aug 2026, a UI mock, n=1), `COD Dossier` (23 Aug 2026, a research-and-authoring pipeline, n=1), and 106 benchmark tasks scoring `gemini-3.7-flash` against `claude-opus-5`. None ran this skill. |
| `[measured-here]` | `scan_skill.py` over this SKILL.md and its eight references, 23 Aug 2026: 3,038 lines, 32 categorical matches over 16 distinct scopes, 13 bounds, 2 qualitative skill references, 6 modules, **0 emphasis tokens**. A scan of the text, not a run. |
| `[derived]` | My reasoning from those, said as such. |

**The tier those numbers are about is Flash** — `gemini-3.7-flash`, plus one `3.7-flash-high` session. Nothing measures
3.1 Pro, so none of it projects there, where the overrides hold as `[docs]`-grounded discipline while every
`[measured-family]` number stays open. Defaults drift inside the family too — **[docs]** *"The default thinking effort
is now medium, changed from high in Gemini 3 Flash Preview."* This work is what `HIGH` is for, *"suitable for complex
prompts requiring deep reasoning, such as multi-step planning, verified code generation, or advanced function calling
scenarios"* — though raising it is no remedy: paired across the 106 tasks, `high` beat `medium` on 24, lost on 24, tied
on 58.

**Unmeasured on this skill:** no Gemini run of `report` has been observed — not the three-reading collapse, not citation
integrity surviving simplification, not the six-capture protocol, not Override 1's conversion. **[docs]** A caution
about this file's shape: *"Avoid writing a prompt with non-linear logic or conditionals that require the model to piece
together fragmented instructions from multiple different places in the prompt."* Read it in one pass — each override
names the phase it lands on.

## Route out first, or know what to distrust

**[docs]** *"Avoid using prompts that ask the model to perform a task for which it has a known, fundamental
limitation."* **[measured-family]** On the 106-task corpus the gap is not uniform: four of eight work buckets are level
with opus, and two collapse. Two of report's deliverables land there.

| The skill's work | Shape | Measured |
|---|---|---|
| `index.html` and `tldr.html` — one self-contained page, everything inlined | `static-page` | 22 against opus's 67, a hard zero on 71% of decided rows |
| the generated design system, the skeleton, the rendered result | `visual-design` | 35 against 63 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape static-page
```

Two shapes are omitted because report never produces them: `brownfield-integration` (a fresh directory, no existing code
edited) and `regression-sensitive`. Phases 0–2 are extraction, which the corpus does not measure. **[docs]** One
documented mitigation for the row that collapses hardest: *"For UI generation, the model shows high design adherence and
parity based on a reference input, whether it's a screenshot, an image, or a full design system."* Report can supply one
— a project `DESIGN.md`, the Phase 3 captures — where every corpus task in that bucket had none.

## What transferred intact

`claims.json` is already the mechanical form: `kind`, `confidence`, `sources`, `support`, `limits` and `from` are named
cells, and **[docs]** *"When model outputs must be machine-readable or follow a specific format, use a widely recognized
standard like JSON, XML, Markdown or YAML that can be parsed by common libraries."* The gates are real —
`audit_report.py` exits 1 on any ERROR and checks ledger against page *both ways*, and `export_pdf.mjs` reports A4
geometry as `NOT checked` rather than as a pass. Several scopes already carry numbers (3–6 categories, three ranked
picks, six captures, 24px gutters), and the skill does not shout: `[measured-here]` zero MANDATORY / CRITICAL /
FORBIDDEN tokens in 3,038 lines.

## The quota ledger — filled, not described

**[measured-here]** The scan returned 32 categorical matches over 16 distinct scopes; I bound **5** and dropped **11**
as prose rather than deliverable scope — rationale clauses, study descriptions, quoted example wording, headings, a
licence clause, a billing line. **[docs]** *"Avoid using subjective or relative qualifiers that lack a concrete,
measurable definition."* Write it into the report directory before Phase 4 with your run's numbers; filled here from a
nine-claim report with two figures and an image:

| Scope, and where the skill states it | Denominator | Filled | Delivery line |
|---|---|---|---|
| **every claim** × three readings — SKILL.md:36, :47, :196; `readings.md:288` | 9 claims × 3 registers = **27** wordings | 25 written, 2 `omit` + `omitReason` | `27/27 accounted: 25 written, 2 omitted with reasons` |
| **every claim** carries its marker in every register — `report-craft.md:212`, backlinks `:438` | 27 renderings, ≥1 marker each | 27 | `cite→source and source→cite green on all three slices` |
| **every figure** through `dataviz`, checked at 400px — SKILL.md:82, :394; `report-craft.md:518` | 2 figures × 3 registers = **6** static frames | 6 frames, 6 width checks | `6/6 frames, 6/6 checked at 400px` |
| **every image** carries caption + provenance + registry row + alt — SKILL.md:578; `source-imagery.md:46` | 1 image × 4 fields = **4** cells | 4 | `1 image, 4/4 fields, basis "captured here"` |
| **every control** gets micro-interaction feedback — SKILL.md:4; state grid `report-craft.md:618` | 6 rows × 7 columns = **42** cells | 34 real, 8 `n/a: fetches nothing` | `42/42 resolved, 34 real, 8 n/a with reasons` |

**[measured-family]** Why a table and not the sentence: on the observed run every enumerated requirement shipped (12 of
12 named features) and every categorical one shipped once or not at all — *all states* → 1, *all menus* → 0, *all flows*
→ 0. **[derived]** Here those scopes *multiply*, so a collapse loses two thirds of the document behind a page that
audits as complete on `brief`.

## The bound ledger — the other direction, and the one that audits clean

**[measured-family]** Across the 106 tasks, 58% of failing UI assertions at `medium` and **86%** at `high` stated a
*bound* rather than asking for a thing, against 8% for opus. The most-repeated one failed on every instance in its set
on a run that passed 37 of its 39 other assertions: the rule was read and agreed with, and the default idiom supplied
the value underneath. **[docs]** Google names where a constraint goes, in the **Recap**: *"Concise repeat of the key
points of the prompt, especially the constraints and response format, at the end of the prompt."* So one row per bound ×
instance, filled from the artifact rather than from the brief:

| instance | property | stated bound | readback | observed | within? |
|---|---|---|---|---|---|
| `index.html` prose blocks | measure | 45–75 characters (SKILL.md:380) | `getComputedStyle($0).width` ÷ the `ch` advance | 68ch · 71ch · **93ch** | **no** — 2 of 3 |
| `tldr.html` × 3 registers | printed sheets | one A4 per reading (SKILL.md:544) | `export_pdf.mjs tldr --reading <r>` page count | 1 · 1 · **2** | **no** |
| verdict categories | picks per category | exactly three (`product-verdicts.md:27`) | `jq '[.claims[]\|select(.category)]\|group_by(.category)\|map(length)'` | 3 · 3 · **2** | **no** |
| the page | external requests | zero (SKILL.md:521) | `audit_report.py` → `self-contained` | `no external assets off the allowlist` | yes |
| `<video>` | autoplay attributes | none (SKILL.md:507) | `grep -c autoplay index.html` | 0 | yes |

**[derived]** Two of the skill's prohibitions become counted properties there — *no autoplay*, *zero network requests* —
because a prohibition in prose reads as style advice. The auditor reaches neither the measure nor the pick count, so
read those two off the artifact.

## Override 1 — chained passes with file outputs, not lenses (Phases 2–5)

SKILL.md:67 reads *Design work goes through `design-craft` with `ux-craft`'s lens*, and SKILL.md:71 anticipates the
failure: *Neither is a gesture at a skill name.*

**[measured-family]** That phrasing is the one measured to fail. On `COD Dossier` the skill said *"Every design decision
goes through `design-craft` with `ux-craft`'s lens"* and neither `Skill()` call ran; its own diagnosis named the
mechanism — nothing downstream needed a file only those skills produce. A Pro-tier transcript reclassified a project
rule the same way, as *"might be a general guideline for agents"*. **[derived]** And it is checkable here:
`audit_report.py:965` requires `DESIGN.md` to exist but never reads it, and nothing is required of the `ux-craft` half.

- **Phase 2 → three chained passes over `claims.json`**, each from the ledger, never from another register's prose
  (SKILL.md:200–202: *one pass plus two rewrites produces one register and two translations of it*).
- **Phase 3 → `DESIGN.md`** with the `MOBBIN TRAWL` block the skill specifies (SKILL.md:255–261), its `TOOK` and `LEFT`
  lines, the palette, type pairing and motion signature.
- **Phase 4 → `UX.md`** with the block sequence, the seven-column state grid (`report-craft.md:618`) and the copy on
  every control. Phase 5 reads all three before the first line of markup.

```bash
for f in DESIGN.md UX.md; do            # the auditor will not check these
  grep -q . "docs/reports/<slug>/$f" || { echo "ungated: $f missing or empty"; exit 1; }
done
grep -q "MOBBIN TRAWL" "docs/reports/<slug>/DESIGN.md" || echo "ungated: no trawl ledger"
```

**[docs]** The remedy is Google's own, under **Too many tasks**: *"Break the requests into separate prompts."* And
*"make each step a prompt and chain the prompts together in a sequence."*

## Override 2 — the tier is a cell that gets filled (Phase 1)

- **`confidence` is about the evidence, not the feeling** (`evidence-harvest.md:61`): `high` = a command with its output
  in the transcript, or a file with a line range; `medium` = one sample, or a paywalled verdict; `low` = one unrepeated
  observation.
- **`limits` is never empty on a `medium` or `low` row** — the auditor only warns there, so treat the warning as a
  block. **[docs]** *"provide instructions for handling missing data rather than assuming inserted data will always be
  present and well-formed."*
- **`support` names the passage, not the file** — `worker.ts:88-104 — maxRetries = 3 guards the catch`.

**[docs]** Adopt the strictly-grounded system instruction for the Phase 2 writing pass, and note its last clause: *"If
the exact answer is not explicitly written in the context, you must state that the information is not available."* That
is the skill's *"The session did not establish this" is publishable* rule, mechanised. **[derived]** A ratio you
computed is *your* claim, so it is an `inference` with a non-empty `from`; and *a reading may change the words, never
what is claimed* becomes checkable by diffing each register's numbers against `claims.json` for unit, direction,
magnitude and the hedge.

## Override 3 — verification is asked for, and this reverses the house style (Phase 7)

**[docs]** *"Include specific verification steps in either the system instructions or your prompts directly."* From the
agentic template, *"Review your output against the user's task"* and *"Verify your claims by quoting the exact
applicable information"*. Counting is a tool call: *"Gemini's code execution tool enables the model to generate and run
Python code, and should be enabled whenever the model needs to perform any kind of arithmetic, counting, or
calculation."*

**[measured-family]** Skills here strip verification scaffolding because Claude over-verifies; what fills it is
well-formed and false — a review naming a browser engine that never ran across four failed invocations, and *"100% pass
rate on contrast"* from a probe never executed, measured afterwards at 3.65:1 on every primary button. The delivery note
is the fix, shipped filled:

```
GATES — docs/reports/queue-drops/
  receipts                 DESIGN.md 84 lines (MOBBIN TRAWL present), UX.md 61 lines
  audit_report.py          exit 0   38 ok, 0 error, 3 warn (ledger:limits c14 → filled, re-run)
  export_pdf.mjs           exit 0   brief 7 pages / 9 blocks A4 595x842pt; technical 9; tldr 1 + 2
    design-review            3 of 6 captures — dark not taken, theme emulation inert (said in the report)
```

A denominator of zero is a gate that never ran, never a pass. Where a runner could not run, name the axis the artifact
is ungated on, as `export_pdf.mjs` already does for itself.

## Override 4 — retries, reads, and the delegation cap (any phase that shells out)

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same failed call."*
**[measured-family]** Four consecutive invocations of one banned, absent tool with nothing changed between them; four
`Read` calls against a 25k token ceiling before pivoting to a Python split. Two attempts per tool, then change approach
— a permanent error or capacity limit pivots on attempt 1. Read constraints first: poppler may be absent, the Mobbin MCP
may not be installed. The same run shows the other half: asked a question naming three skills, it answered from memory
without loading any; asked to fix that, it launched a skill instead of answering. Report requests routinely name
material, and Phase 0's *answer these from the conversation* means the conversation you have read. Load what the prompt
names, **then** answer: two ordered steps, neither substituting for the other.

The skill also caps delegation — delegate only for a wide sweep reconstructing a long session, *keep the count low* — so
write the number down: **one subagent maximum, for the Phase 1 harvest; zero elsewhere.** **[docs]** Google's guidance
on a model that answered correctly but *"didn't stay within the bounds of the options"* prescribes reframing as a closed
choice, so settle the live forks in writing before Phase 4: `/report tldr` versus the full report, the build lane per
figure, whether the verdict layer applies.

## Override 5 — six captures, and describe the crop before judging it (Phase 7)

The skill says *six captures, not one* — three readings × light and dark — and knows why a scripted toggle cannot
produce them: setting `.checked` from script does not re-evaluate the `:has()` selector on Obscura. Rewrite the served
source instead, as `export_pdf.mjs` does, and mark a cell done only when it was opened:

| | light | dark |
|---|---|---|
| primer | opened, described | opened, described |
| brief | opened, described | **not taken** — theme emulation inert on this engine |
| technical | opened, described | **not taken** |

**[docs]** *"Ask the model to describe the images before performing the task in the prompt."* Google's example returns a
one-line caption for a whole airport board, and thirteen rows once the prompt names what to extract. So per capture:
name what is in it — register indicator, TLDR block, figure and caption, citation markers, gutters — **then** judge it.
And *"To improve the response, point out which parts of the image are most relevant to the prompt."*

## Override 6 — vendor values get read, not recalled (Phases 3, 5, verdict layer)

**[docs]** *"Your knowledge cutoff date is January 2025."* For 3.7 Flash, *"users can expect updated information for
some domains while in others they may experience the model's knowledge is limited to January 2025"*.
**[measured-family]** The informative failure on that run was not a guess but Windows 10's published accent colour on a
Windows 11 app. So fill a table before the first line of prose, each cell carrying its source tier — *stamp prices,
versions and availability with a date* (`product-verdicts.md:208`), mechanised:

| Value | What I wrote | Read from | As at |
|---|---|---|---|
| `@tanstack/charts` release | `0.14.0`, pre-alpha | its README, fetched this session | 18 Aug 2026 |
| GSAP plugin licensing | free, commercial use included | the GSAP/Webflow announcement, fetched | 18 Aug 2026 |

A cell you cannot tag is a value you invented. **[docs]** *"Grounding with Google Search connects the Gemini model to
real-time web content, and should be enabled whenever the model may need to know obscure or recent facts."*

## One worked example, before the set

**[docs]** *"We recommend to always include few-shot examples in your prompts."* And *"you can remove instructions from
your prompt if your examples are clear enough in showing the task at hand."*

```json
{ "id": "c7",
  "text": "Cache reads were 95.4% of tokens sent across the 28-window sample.",
  "kind": "direct", "confidence": "high", "sources": ["s3"],
  "support": "logs/bench-2026-08-07.txt:1180-1204, summed per window",
  "limits": "One tenant, 28 consecutive days. Not a spend share — see c9.",
  "readings": {
    "primer": "Almost 19 out of every 20 words sent were ones the computer had seen before.",
    "brief": "95.4% of tokens sent are cache reads, so the headline rate is not the rate you pay.",
    "technical": "Cache-read share is 95.4% of 3.48B raw tokens, n=340 across 28 windows." } }
```

**[docs]** *"Make sure that the structure and formatting of few-shot examples are the same to avoid responses with
undesired formats."* Every later row keeps those keys in that order. And *"By default, Gemini 3 models provide direct
and efficient answers"*, so Primer reads as finished long before the ledger's last row: the exit condition is the
ledgers' fractions.

## Modules deliberately not written

The scan fired six — `authorship`, `visual`, `gate`, `bounded-constraint`, `platform-values`, `delegation` — all above.
Four did not. **`states`** (2 triggers): the grid at `report-craft.md:618` already has cells and an `n/a` rule, so it is
a quota row instead. **`count-contract`**: the skill already promises counts. **`injection`**: cited sources, kept as
data by `kind`. **`emphasis`**: none.
