# gemini.md — `oracle`

Read this once, now, then read `SKILL.md` and follow it with the overrides below; each names the
section it lands on. `oracle` is the best-suited skill in this plugin for this model and the
worst-suited in exactly one step. Best, because steps 2–6 are four stdlib scripts with exit codes and
**[measured-family]** the single work bucket where this family matches opus is the one whose brief
already states a number — optimality, 74.7 against 75.0 (`geminify/references/evidence.md` §2.1).
Worst, because step 1 asks for a markup pass across an existing product's templates, which is the
shape that produced hard zeros on 79% of decided rows (§2.1). The route-out block below is about that
one step and nothing else.

## Epistemic status

- **Tiers used:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]`: **no Gemini run of
  `oracle` has been observed**, at any tier.
- **`[measured-family]` sources:** two single sessions (n=1 each) and a 106-task benchmark at two
  effort levels — `geminify/references/evidence.md`. None watched a model trace a rendered figure to
  its source record.
- **The tier the evidence is about.** Every measured rate below was observed on `gemini-3.7-flash`
  (one session on `gemini-3.7-flash-high`) — flash-tier claims, **not** to be projected onto the Pro
  tier. **[docs]** The default drifts inside the family: *"If thinking_level is not specified, Gemini
  3 will default to high."* against, from the 3.5 Flash release notes, *"The default thinking effort
  is now medium, changed from high in Gemini 3 Flash Preview."* On Pro these overrides stand as
  `[docs]`-grounded discipline and every `[measured-family]` number is open.
- **Unmeasured on this skill:** no Gemini run of `oracle` · no evidence a `gemini.md` fixes anything
  on either source · the categorical-collapse rate was measured on UI briefs, so its transfer to a
  set of `data-figure-id` attributes is `[derived]` · nothing measures this family adding markup to
  someone else's templates, recomputing a total against a source record, or reading the `C17`/`I7`
  evidence this skill rests on.
- **The self-limitation.** **[docs]** A conditional side file is the shape the checklist warns about:
  *"Avoid writing a prompt with non-linear logic or conditionals that require the model to piece
  together fragmented instructions from multiple different places in the prompt."* One pass, then
  work from `SKILL.md`.

## Route out of step 1, and only step 1

Step 1 is not pipeline work: `Mark up the surface once. Four attributes, and they are a change to the
product rather than to the pipeline`. That is an edit to existing multi-file templates, under several
acceptance conditions at once, that must not change what those templates already render.

| shape | where it lands here | measured |
|---|---|---|
| `brownfield-integration` | adding four attributes across a product's existing view templates | 16 against opus's 46, zero on 79% of decided rows |
| `regression-sensitive` | the same edit, against surfaces whose current output existing tests assert on | 42 against 65 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape brownfield-integration
```

**[docs]** *"Avoid using prompts that ask the model to perform a task for which it has a known,
fundamental limitation."* **Two rows are omitted deliberately:** `static-page`, because `oracle`
authors no page — it reads one — and `visual-design`, because judging a rendered surface is
`warrant:panel`'s work and the corpus abstains on judging anyway. Steps 2–6 stay here: invoking a
script and reading its exit code is not the shape the benchmark measured. Where no lane is available,
do step 1 anyway and treat the markup diff as the part of the output to distrust — re-render the
surface set and diff it before running the gate.

## What transfers intact

**The denominator rule is already code, not prose.** `_cli.rate()` renders a percentage with its
numerator and denominator or refuses to render one, `lot_report.py` exits 2 if the population is
absent, and `escape_report.py` refuses to print a rate at all. `bounded-constraint` reached three
triggers across this skill and its binding references and is **not** written below, for the same
reason: the bound is enforced by the script rather than restated for a reader.

**Absent evidence is already a distinct answer.** `A class no surface matched comes out not-green
rather than absent, because no evidence is a different answer from a pass.` That is core C2's
denominator-of-zero rule, shipped as code before this file existed. Keep it; do not read a class with
zero surfaces as clean.

**The tool choice is stated rather than left to taste.** `Parse HTML with html.parser, not with a
regex.` survives literal instruction-following intact, which is the one thing **[measured-family]**
§1.1.6 recorded going right — the enumerated requirements all shipped.

**Modules not written, and why.** `visual` reached only two triggers and would be wrong anyway: this
skill's thesis is that `A vision judge cannot catch that, because nothing on the screen looks wrong`,
so a capture protocol here would argue against the file it sits beside. `states`, `platform-values`,
`injection`, `count-contract` and `delegation` never reached the threshold. `emphasis` scored **0**
shouted tokens. `gate` did fire — at two triggers on `SKILL.md` alone, because this skill writes
`Exit 2` rather than the trigger's literal `exit code`, and at three once its binding references are
included; `scan_skill.py --refs` globs `<skill>/references/*.md` and this plugin keeps its references
one level up, so run it over both.

## Override 1 — the markup pass has a denominator, and it is per surface (`## Procedure`, step 1)

The scan found one quota row, `Each figure` at line 55. The larger one it missed sits in a table
header: `On every displayed figure`. **[measured-family]** §1.1.1 (n=1) is exactly this failure —
twelve enumerated features all delivered, and every requirement named categorically delivered once or
not at all: all surfaces → 5, all states → **1**, all menus → **0**. Four attributes on every figure
across a surface set is a categorical scope with no number attached, and the gate cannot catch a
surface nobody opened. **[docs]** *"Avoid using subjective or relative qualifiers that lack a
concrete, measurable definition."*

Get the denominators before marking anything up:

```bash
python3 scripts/lineage_extract.py --root <repo> --input <rendered.html> --json | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d['figures']), 'figures')"
ls dist/**/*.html | wc -l    # the surface denominator
```

Fill this and report the fraction; every number in your copy comes from those commands, not this
file:

| scope, in oracle's own words | denominator | done | reported |
|---|---|---|---|
| surfaces in the `--glob` set marked up | 6 | 6 | `6 of 6` |
| `On every displayed figure` — `data-figure-id` | 212 | 212 | `212 of 212` |
| the same figures — `data-source-ref` | 212 | 198 | `198 of 212, 14 unsourced and named` |
| derived figures carrying `data-source-expr` | 23 | 21 | `21 of 23, 2 n/a: no expression, the value is stored` |
| defect classes rolled up | 7 | 7 | `7 of 7, 4 green` |

A cell you cannot fill reads `n/a: <reason>` — **[docs]** *"provide instructions for handling missing
data rather than assuming inserted data will always be present and well-formed."* A figure nobody
marked up is unsourced, never sourced.

## Override 2 — the exit codes are the output; type no figure by hand (`## Output`)

**[measured-family]** §1.1.2 (n=1): a run wrote its own verification document as five well-formed
rows, all `PASS`, asserting a browser engine as verified when it had failed all four invocation
attempts, `100% pass rate on contrast` from a probe never executed — measured afterwards, every
primary button 3.65:1 and one glyph 1.00:1, invisible — and `Interactive Targets Audited: 47`, a
number nothing produced. Forty cells' worth of work, five rows. A coverage report is the same genre.

So the delivery note is a transcript, not a summary. **[docs]** *"Include specific verification steps
in either the system instructions or your prompts directly."* and *"Verify your claims by quoting the
exact applicable information (including policies) when referring to them."* Ship it filled:

```
lineage   lineage_extract.py --input dist/reports/portfolio.html --json
          → 212 figures · 198 with data-source-ref · 14 without
gate      lineage_gate.py --glob 'dist/**/*.html'                    → exit 2 · 14 unsourced · 6 surfaces
tick      tick_and_tie.py --input dist/... --sources data/           → exit 2 · 1 mismatch: FIG-payout-total
taxonomy  taxonomy_check.py --taxonomy taxonomy.json --records data/ → exit 0
rollup    rollup_classes.py --root .                                 → exit 0 · 7 classes · 4 green
control   lineage_gate.py --selftest                                 → exit 0 · every rule fired
```

**[docs]** *"When model outputs must be machine-readable or follow a specific format, use a widely
recognized standard like JSON, XML, Markdown or YAML that can be parsed by common libraries."* — that
surface is `--json` mode, and `In --json mode, stdout carries the JSON object and nothing else`, so
count over it in Python rather than by eye over the human summary. **[docs]** *"Gemini's code
execution tool enables the model to generate and run Python code, and should be enabled whenever the
model needs to perform any kind of arithmetic, counting, or calculation."*

## Override 3 — prove the gate can fail, then read what it actually measured (`## Constraints`)

**[measured-family]** §1.2.2: an auditor validated tags, citations and contrast floors thoroughly,
had no check that its prerequisite artifacts existed, and returned exit 0 over two skipped skill
invocations. **[derived]** geminify's own quote gate went green across every file after a change took
its checked count to zero, caught only by re-running the negative control (§5). The script contract
already ships the control, and it is not optional:

```bash
python3 scripts/lineage_gate.py --selftest   # exit 0 only if every rule fired
```

Then read the receipt before the verdict. A green `lineage_gate.py` over a glob that matched zero
files is a green over nothing, so read `surfaces_matched` out of `.warrant/oracle-coverage.json`
rather than the headline; the skill's own rule for the class layer says the same — `A class no
surface matched comes out not-green rather than absent`. And `rollup_classes.py` is a prerequisite
for `ratchet`, not an optional tidy-up: skip it and `every class reads as having no evidence`.

## Override 4 — two attempts, and three exits that are not transients (`## Procedure`)

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same
failed call."* **[measured-family]** Both n=1 sessions ran the loop: four consecutive invocations of
one banned, absent tool with nothing changed between them (§1.1.2), and four consecutive `Read` calls
against a 25,000-token ceiling before pivoting to a Python split (§1.2.3). `gemini-cli` ships a loop
detector whose halt message names *"repetitive tool calls"* (§7.2).

Where it lands here: **do not `Read` a rendered surface at all.** A `dist/**/*.html` build page will
exceed the read ceiling, and `lineage_extract.py` is its reader — pivot on attempt 1, not attempt 4.
And the exit codes carry different answers that must not be retried into each other: `Exit 1 and exit
2 are different answers and callers depend on the difference: a missing file is not a failed gate`.
Exit 2 is a finding — fix the markup or the source, never re-run for a different verdict. Exit 3 is a
precondition: no warrant, no ledger, no corpus, and re-running changes nothing until `charter` has.
**[docs]** *"Inhibit your response: only take an action after all the above reasoning is completed.
Once you've taken an action, you cannot take it back."*

## Override 5 — tick one figure in full before the rest (`## Procedure`, step 3)

**[docs]** *"We recommend to always include few-shot examples in your prompts"*, and *"you can remove
instructions from your prompt if your examples are clear enough in showing the task at hand"*. Write
the first comparison at full fidelity, then let the rest match its shape. The skill states what the
row must carry and why: `Exit 2 names the figure, the rendered value, the source value and the
tolerance that was applied — all four, because a mismatch report missing the tolerance cannot be
acted on.`

| figure | source-ref | field / expr | rendered | source | tolerance | verdict |
|---|---|---|---|---|---|---|
| `FIG-payout-total` | `payouts/2026-Q2` | `sum(segments.amount)` | `1,284,500` | `1,284,050` | integer, exact | **mismatch** |
| `FIG-payout-count` | `payouts/2026-Q2` | `count(segments)` | `41` | `41` | integer, exact | tie |

The derived row is the one to write first. `The expression form is what catches a total that no
longer equals the sum of its parts, which is the most common wrong-number-on-a-right-looking-page
defect there is.`

## Override 6 — a missing source is a value, and it is this skill's thesis (`## Constraints`)

`Report a missing source as missing rather than inferring one from the value. An inferred source is
the failure this plane exists to detect, arriving through the detector.` That sentence is Google's
grounded-assistant instruction with a different subject, and the clause to adopt verbatim is its
last: **[docs]** *"If the exact answer is not explicitly written in the context, you must state that
the information is not available."* **[docs]** *"Do not assume or infer from the provided facts;
simply report them exactly as they appear."* An unsourced figure is unsourced, and a plausible source
supplied from the value is the defect wearing the detector's uniform.

The same rule covers this skill's evidence. **[docs]** *"Your knowledge cutoff date is January
2025."* The claim ids — `C17`'s roughly 85% precision and 84% recall, `I7`, `C19`'s twentyfold
denominator spread — resolve in `docs/deep-research/claims.json` and `references/evidence.md`. Read
them; never quote one from memory. **[measured-family]** §1.2.4 recorded both halves of that failing
in one session: answering from memory when three skills were named in the prompt, then launching a
skill when an answer was wanted. Read, then answer, as two ordered steps.

## Override 7 — `thinking_level`, and what it is not for

**[docs]** `HIGH` is described as suitable for *"multi-step planning, verified code generation, or
advanced function calling scenarios"*; 3.7 Flash defaults to `MEDIUM`. Steps 2–6 are not that — they
are five script invocations and a read of their exit codes — so run the default there. Step 1's
markup pass across an existing template tree genuinely is multi-step planning, and the uplift is
unmeasured on this corpus. **[measured-family]** Do not raise it as a remedy for anything above:
paired across 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on 58, mean −1.7 points
(§2.3). **[docs]** *"Higher thinking levels encourage the model to use more tools to explore and
verify, so lowering the level can reduce tool calls."*

## Recap

**[docs]** *"Concise repeat of the key points of the prompt, especially the constraints and response
format, at the end of the prompt."*

1. Route step 1's markup pass out where a lane exists; if you do it here, diff the re-rendered
   surfaces before gating and say the markup is the untrusted part.
2. Count surfaces and figures before marking up, report `N of N` after, `n/a: <reason>` on anything
   unfilled.
3. Type no figure into the report — every number comes from a named command's stdout, pasted with its
   exit code.
4. Run `--selftest` before believing a green gate, and read `surfaces_matched` before believing the
   gate was about the surfaces you meant.
5. Never `Read` a rendered page; pivot on attempt 1. Exit 2 is a finding, exit 3 is a precondition,
   and neither is a retry.
6. Tick one figure in full — id, source, expression, both values, tolerance — before the rest.
7. Report a missing source as missing, and read every `C`/`I` claim id out of `claims.json` rather
   than recalling it.
