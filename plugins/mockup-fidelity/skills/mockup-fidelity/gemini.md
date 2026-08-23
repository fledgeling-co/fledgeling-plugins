# Running `mockup-fidelity` on Gemini

Read this once, whole, before the SKILL.md — every override names the section it lands on. **[docs]** the health
checklist warns against a prompt "with non-linear logic or conditionals that require the model to piece together
fragmented instructions from multiple different places in the prompt", which is what a conditional side-file
becomes unless it is read up front. The canon transfers; the assumption that a rule stated in prose gets
executed does not. This skill's promise is categorical — **every** mock element lands in one of three states —
and a categorical promise collapses to whatever got looked at.

## Epistemic status

| Tier | Here | Meaning |
|---|---|---|
| `[docs]` | throughout | Google published it; verbatim from `geminify/references/gemini-corpus.md` |
| `[measured-family]` | n=1 sessions + 106 tasks | Gemini runs of *other* skills and the benchmark corpus, both in `geminify/references/evidence.md` |
| `[measured-here]` | **none** | no Gemini run of `mockup-fidelity` exists. A Gemini model *graded* one of its evals (plugin `EVALS.md`, eval 9) — that measures the grader |
| `[derived]` | yes | my reasoning from the above, marked as such |
| `[target-measured]` | yes | this skill's own harness numbers, from the plugin's `EVALS.md` (18 Aug 2026) — facts about Obscura and `capture.mjs`, carrying no evidence about Gemini. Outside geminify's four tiers, named so it cannot be mistaken for one |

**The two `[measured-family]` sessions**, each n=1 and summarised in `geminify/references/evidence.md` §1: a
UI-mock run whose categorical scopes collapsed while every enumerated one landed, which reviewed itself with an
engine that never ran; and a research run that skipped both composed skills, retried one `Read` four times
against a token ceiling, and answered from memory about skills its prompt named. **Which model they are about:**
`gemini-3.7-flash`, one session at `-high` plus 106 benchmark tasks. Nothing was measured on the Pro tier, whose
thinking default differs — **[docs]** "If thinking_level is not specified, Gemini 3 will default to high",
against the 3.5 Flash note that "The default thinking effort is now medium, changed from high in Gemini 3 Flash
Preview." On Pro these overrides stand as documented discipline and every rate is open.

**Unmeasured on this skill.** Whether the Phase 3A ledger gets filled for every affordance or only the first
few; whether `inconclusive` is read before `findings` with the nine `reason` strings verbatim; whether the exit
code is quoted rather than an impression of the report; whether an authored justification passes as a citation
under THE LAW rule 5; whether the native lane's artifacts get produced in order; anything about React Native or
a real browser engine; whether these overrides help.

## Route out first — and only Phase 6

**[docs]** Under **Task outside of model capabilities**: "Avoid using prompts that ask the model to perform a
task for which it has a known, fundamental limitation." **[measured-family]** 106 tasks against `claude-opus-5`
(§2.1): four of eight buckets are level, and brownfield edits to a multi-file repo score 16 at `medium` and 20
at `high` against opus's 46, zero on 75–79% of decided rows. Phases 0–5 measure; **Phase 6 changes code**
(SKILL.md:423–436).

| Phase 6 work | shape | measured |
|---|---|---|
| add the missing region, move the control, wire absent data | `brownfield-integration` | 16–20 against 46 |
| a fix that must not regress a screen the harness already exits clean on | `regression-sensitive` | 42 against 65 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape brownfield-integration
```

`[derived]` Absent by decision: `static-page`, because this skill never authors a page from prose and
`references/mechanical-conversion.md` lifts an already-rendered subtree; `visual-design`, because nothing here
judges aesthetics; and any row for the audit half, because the corpus watches a model *build*. Where no lane is
free, the block says which half to distrust — the ledger is measured, the code change is not (SKILL.md:428).

## What transfers intact

- **The three-valued vocabulary** (SKILL.md:405–412) — `DEFECT` / `INTENTIONAL — <citation>` / `INCONCLUSIVE —
  <capability>` / `✓ fixed+reverified` is already the slot a "could not run" needs; most skills have none.
- **The exit code as the gate** (215–217), **the artifact precondition** (208–213) and **reference
  immutability** (323): no artifact, no verdict is a precondition, not an exhortation.
- **The untrusted-content sentence** opening every sub-agent brief (443–444) — Google's delimited-data guard,
  written.
- **The two ask gates** (67–78): **[docs]** the agentic template prefers "calling the tool with the available
  information over asking the user" on low-risk reads, which is the rest of this skill.

## C1 · The quota ledger — 18 categorical scopes, each with a number

**[docs]** Under **Ambiguity**: "Avoid using subjective or relative qualifiers that lack a concrete, measurable
definition." **[measured-family]** the enumerated requirements all landed; the categorical ones landed once or
not at all. This skill's exposure is SKILL.md:348 — *for every affordance the reference shows, mark its state in
the target*. Write the ledger into `.mockup-fidelity/LEDGER.md` **before** the first capture; a scope with no
number gets satisfied once. Six of the eighteen gate a verdict and are tabled; twelve take the same shape (208,
210, 277, 298, 467 and six reference files).

| Categorical scope (line) | Number | Report as |
|---|---|---|
| `Every capture` probes per detector class — 133 | 9 classes | `9 probed · R ran · S silenced` |
| `Inventory EVERY frame` — 254 | F frames, incl. every `· empty` / `· dark` / `(sheet)` suffix | `F frames · A audited · X excluded with reason` |
| `each cell` from structure artifacts — 349 | C affordances per frame | `C of C cells, 0 TODO` |
| every mock affordance class — 240–243 | **11** named: header element, button, card, section, eyebrow, badge, chip, search field, meaningful icon, list row, CTA | `11 of 11 swept per frame` |
| `every element` the app renders that the mock does not — 265 | E per matched region | `E extras across R regions` |
| `each control` × `each state` probed — fidelity-probe.md:5,15,22 | C × S | `C×S probes, 0 unopened` |

**The exemplar, filled** — the skill's own fixture pair, `[target-measured]` from the plugin's `EVALS.md`:

```
screen   reference.html → target-10-defects.html   frames 1 of 1 audited · 0 excluded
classes  9 probed · 0 ran · 9 silenced             artifacts 4 of 4 on disk
findings 49 (26 high)  ·  planted 10 · caught 8 · inconclusive 2 · false pass 0
score    83 — not quotable bare: scoreCovers.fraction = 0        exit 3, not 0
```

**[docs]** **Ambiguity** again on the last line: 83 beside nine closed shutters reads as 83% right.
`count-contract` (3 hits) extends this — derive the count when the brief omits one, and cover the cells.

## C2 · Verification is asked for, not assumed

**[docs]** "Include specific verification steps in either the system instructions or your prompts directly", and
from the agentic template, "Verify your claims by quoting the exact applicable information (including policies)
when referring to them."

`[derived]` SKILL.md:222–224 already forbids the fabricated review — a tool that cannot run is a blocker to
report, quoting what the tool said. So every number carries its command and that command's pasted output; a
denominator of zero is never a pass (`scoreCovers.fraction = 0` means the score is about nothing); and each
`reason` string is relayed byte-for-byte (148–151), because a paraphrase is how "this layer cannot run here"
becomes "the shadows match". **This engine cannot return 0**: `[target-measured]` all nine probed classes are
silenced on Obscura 0.2.0, so `--assert` exits 3 even on a byte-identical control, and the verdict is
INCONCLUSIVE with nine rows.

## C3 · Two attempts per tool · C4 · Passes, and the native lane as a chain

**[docs]** "you must change your strategy or arguments, not repeat the same failed call." Two attempts on
`capture.mjs`, `obscura serve`, `axe describe-ui` or a Metro CDP attach; a permanent error gets one; a
**capacity** error — a token ceiling, a payload cap — gets **zero**, pivot on attempt 1 to chunked or
line-ranged reads, the loop the second session fell into. `feature-check.mjs` gets zero: its verdict inverts
here. **[docs]** Under **Too many tasks**, "Break the requests into separate prompts", and the remedy, "make
each step a prompt and chain the prompts together in a sequence." The phases are that chain: breadth ledger,
structure, style.

**The one qualitative skill reference, converted.** SKILL.md:328 says the target side `goes through proctor`.
**[measured-family]** on the one run carrying that phrasing both composed skills were skipped, and the model's
own diagnosis was that nothing depended on a file only those skills produce. `native-lane.md:218–234` names the
files; make them sequential preconditions, each phase opening what the last wrote:

```
proctor_doctor + proctor_apps attach → grants and lanes recorded
proctor_inspect            → target.inspect.json     Tier A, or reflectorUnavailable — and Tier B means
                                                     every style class is inconclusive before a style row
proctor_stability (5 runs) → target.stability.json   tolerance derived from measured variance
proctor_assert             → target.assert.json      skipped[] whole; ledger rows come from these files
```

A tier claimed without reading `target.inspect.json`, or a `tolerance` left at 1.0, is an assumed calibration.

## C5 · One worked screen first · C6 · `thinking_level`

**[docs]** "We recommend to always include few-shot examples in your prompts", and under **Missing output format
specification**, "use a clear, explicit instruction to specify the format and show the output structure in your
few-shot examples." Audit **one** frame end to end — inventory row, 4 artifacts, filled 3A ledger, bound ledger,
findings, quoted exit code, functional-gaps row; a later frame with a shorter ledger was not audited. **[docs]**
`HIGH` "Allows the model to use more tokens for thinking and is suitable for complex prompts requiring deep
reasoning, such as multi-step planning, verified code generation, or advanced function calling scenarios", and
Gemini 3.7 Flash defaults to `MEDIUM`. `[derived]` This skill is both at once, so `HIGH` is what the level is
*for* here — **[measured-family]** and not a remedy: paired across 106 tasks, `high` beat `medium` on 24, lost
on 24, tied on 58.

## C7 · Recall is not a source — capability facts and named files included

**[docs]** "Your knowledge cutoff date is January 2025." `platform-values` fired (4 hits) and folds in here,
because this skill reads token values rather than recalling them (SKILL.md:301–304). The live version of that
risk is engine capability: `references/engine-capability-matrix.md` says every row of itself is a measurement,
not an architectural truth, so read `summary.capabilities` off this run. **Read, then answer, as two ordered
steps:** **[measured-family]** a run asked about three skills named in its prompt answered from memory without
loading any, then inverted the error by launching a skill instead of answering. That lands twice — the reference
table at SKILL.md:38–56 routes to one of sixteen files, and the one matching your target is loaded before Phase
0; and a citation offered under THE LAW rule 5 is **opened and quoted** before the row is retired.

## Module `visual` (14 hits — the highest of any target scanned)

**[docs]** "Ask the model to describe the images before performing the task in the prompt." "To improve the
response, point out which parts of the image are most relevant to the prompt." The skill is stricter and right
to be — SKILL.md:179–181 puts frontier multimodal recall near 40% on fine-grained UI differences and under 23%
on hard cases. A screenshot never closes a row; it is the trigger to measure, and every `✓` cites two artifact
values. The capture denominator is frames × gated states, all opened in one session (`fidelity-probe.md:22`).
Describe a crop before judging it, and number both images (SKILL.md:182).

**[docs]** Google's launch material claims that "For UI generation, the model shows high design adherence and
parity based on a reference input, whether it's a screenshot, an image, or a full design system." `[derived]`
Phase 6 is that mode by construction, so hand the rendered reference and the token file to every fix and brief.

## Module `gate` (9 hits) — and the receipt the gate does not check

**[docs]** Under **Non-standard data format**: "When model outputs must be machine-readable or follow a specific
format, use a widely recognized standard like JSON, XML, Markdown or YAML that can be parsed by common
libraries." And on arithmetic, Gemini's "code execution tool enables the model to generate and run Python code,
and should be enabled whenever the model needs to perform any kind of arithmetic, counting, or calculation."
Paste the harness output; cite fields of `target.findings.json` and print the denominator with every fraction.
**Prove the gate can fail before trusting it passing** — `[target-measured]` the fixture pair is that control, 0
findings on the byte-identical target and 49 on the ten-defect one. `--allow-inconclusive` waits until every
silenced class has a ledger row naming where it was confirmed in a real browser (rule 7).

**[measured-family]** A gate that checks only the final artifact lets an upstream skip through: on one run the
auditor validated tags, citations and contrast, exited 0, and never checked that the composed skills had
produced anything. `[derived]` The same hole is open here, so before quoting any exit code check the receipts:
`PROJECT.md` with the frame→route map, this screen's 3A rows with no TODO, and `target.inspect.json`,
`target.stability.json`, `target.assert.json` non-empty in the native lane. A missing one fails the run.

## Module `bounded-constraint` (6 hits) — the half C1 misses

C1 catches a categorical scope collapsing to one instance; this catches a stated maximum exceeded on **every**
instance, the failure that reaches a passing-looking artifact. **[measured-family]** §2.2: 58% of failing UI
assertions at `medium` and 86% at `high` were bound-shaped, against 8% for opus, and `has exactly one soft
elevation shadow` failed on every card and toast in its set, on a run that passed 37 of its 39 others.

**[docs]** Google names constraints as a component of their own — "Restrictions on what the model must adhere to
when generating a response, including what the model can and can't do." — and the **Recap** component is where
they go: a "Concise repeat of the key points of the prompt, especially the constraints and response format, at
the end of the prompt." So a bound ledger sits beside the breadth ledger, one row per bound × instance, filled
from the artifact. The first two rows carry real values, `[target-measured]` from
`engine-capability-matrix.md:25–26`: **on this engine the most-failed bound in the corpus has no readback.**

| instance | property | stated bound | readback | observed | within? |
|---|---|---|---|---|---|
| any card | elevation shadows | exactly 1 | `getComputedStyle(el).boxShadow` | `""` — no longhand exists | **no — INCONCLUSIVE; route to the layer's `shadowOpacity` in the native lane** |
| any label | `text-transform` | uppercase only where the mock sets it | `getComputedStyle(el).textTransform` | `""` | **no — INCONCLUSIVE** |
| `LEDGER.md` | banned resolutions (SKILL.md:244–246, 403) | 0 occurrences | `grep -c 'app-ahead\|native chrome\|real-data\|probably fine' LEDGER.md` | fill from this run | |
| the fan-out | agents in flight (SKILL.md:434) | at most 5 | count of live `agent()` calls per wave | fill from this run | |

`[derived]` **A bound stated as a prohibition reads as style advice**, which is why the last two rows are
conversions. Two more belong on a real run: the ledger carries none of `⚠︎-unmatched`, `noiseExcluded`, `IoU`,
`MODE-B` (415, `grep -co`), and the simulator takes one session (`batch-orchestration.md:6`).

## Modules `states` (4 hits) and `delegation` (9 hits)

**[docs]** Under **Underspecified task**: "provide instructions for handling missing data rather than assuming
inserted data will always be present and well-formed." **[measured-family]** 1 of 6 named states delivered, from
a skill that named the six *and* stated a completeness condition in prose. `[derived]` So a frame suffixed `·
empty`, `· dark`, `(drill-in)`, `(sheet)` or `Composer` is its own inventory row with its own four artifacts;
SKILL.md:254's ban on `minor sub-state of X` has to become a row count to survive. A conditionally rendered
element is graded only in its **populated** state (465–466), and `UNSTABLE` (140–146) is a fourth state,
inconclusive. **[docs]** On a model that answered correctly but "didn't stay within the bounds of the options",
the remedy is to rephrase as multiple choice: cap the fan-out at SKILL.md:434's waves of ≈5; never delegate a
check of your own output, because the completeness critic in `references/measurement-enforcement.md` works by
being blind to the app and the mock; resolve every fork (auto-fix vs reviewed plan, embed vs StyleX, sequential
vs N-lane) into `PROJECT.md` first; and carry THE LAW and the preflight rule into every brief (446).

## Modules `authorship` (8 hits) and `emphasis` (10 tokens)

The ledger and the functional-gaps doc become tickets (SKILL.md:414), so a reader acts on them. **[docs]** adopt
the last clause of Google's strictly-grounded system instruction verbatim for both: "If the exact answer is not
explicitly written in the context, you must state that the information is not available." `[derived]` So a
`Current state` cell you cannot draw from an artifact reads `not measured` — THE LAW rule 5 from the other side.
The SKILL.md shouts (`⛔ THE LAW`, `EVERY`, `banned`, `NOT citations`); read those passages as plain rules of
equal weight. **[docs]** under **Overt manipulation**, escalating instructions no longer help: "foundation model
performance will no longer improve and in many cases will get worse". Also "Avoid unnecessary or overly
persuasive language." `[derived]` Capitals do not make the breadth ledger exist, filling its cells does; briefs
and tickets get plain declaratives.

## What I did not write, and why

- **`injection`** did not fire and gets no section: the skill already ships the guard sentence at
  SKILL.md:443–444. **`platform-values`** fired (4 hits) and folds into C7.
- **54 categorical candidates scanned, 36 distinct; 18 bound, 18 dropped as prose** — anti-pattern narration
  (SKILL.md:98), sequencing rules (`before any colour or spacing`, 356), doc-about-the-doc lines
  (`issue-to-check-map.md:4`, `evidence.md:9`) and caveats. The 322 distributives and 283 prohibitions counted
  but not listed went unreviewed; those attached to a countable property belong in the bound ledger.
- **Nothing in the skill was changed.** One item belongs to `improve-skill`: `evals/evals.json` points at
  `../EVALS.md` for the harness measurements, but that file lives at the plugin root, three levels up.
