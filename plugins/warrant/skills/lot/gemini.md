# gemini.md — `lot`

Read this once, now, then read `SKILL.md` and follow it with the overrides below; each names the
section it lands on. `lot` accepts a queue under a declared risk limit, and almost everything it does
is arithmetic a script already performs — which is the half that suits this model. The other half is
a set of ordering constraints that no script can fully close: six ways a verdict leaks into a blind
queue, two classes that must be reviewed in full rather than sampled, and a rule against bare
percentages that binds the prose a run writes and not the numbers a script prints.

## Epistemic status

- **Tiers used:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]`: **no Gemini run of
  `lot` has been observed**, at any tier.
- **`[measured-family]` sources:** two single sessions (n=1 each) and a 106-task benchmark at two
  effort levels — `geminify/references/evidence.md`. None watched a model plan a sample, build a
  blinded queue, or report a lot decision.
- **The tier the evidence is about.** Every measured rate below was observed on `gemini-3.7-flash`
  (one session on `gemini-3.7-flash-high`) — flash-tier claims, **not** to be projected onto the Pro
  tier. **[docs]** The default drifts inside the family: *"If thinking_level is not specified, Gemini
  3 will default to high."* against, from the 3.5 Flash release notes, *"The default thinking effort
  is now medium, changed from high in Gemini 3 Flash Preview."* On Pro these overrides stand as
  `[docs]`-grounded discipline and every `[measured-family]` number is open.
- **Unmeasured on this skill:** no Gemini run of `lot` · no evidence a `gemini.md` fixes anything on
  either source · nothing measures this family blinding a queue, rotating seeds, or handling a
  sequential stopping rule · the categorical-collapse observation was made on a UI brief, so its
  transfer to a census class is `[derived]` · the mammography evidence behind the blinding rule
  (`C7`, `C8`) is observational and about radiologists, not about this pipeline.
- **The self-limitation.** **[docs]** A conditional side file is the shape the checklist warns about:
  *"Avoid writing a prompt with non-linear logic or conditionals that require the model to piece
  together fragmented instructions from multiple different places in the prompt."* One pass, then work
  from `SKILL.md`.

## There is no route-out block here

geminify writes one only where the benchmark measured the work, and `lot` fails both conditions.
**Its work class is one the corpus abstains on:** the bench measures a model *building* an artifact,
while `lot` sizes a sample, blinds a queue and reports a decision — `verification` and `completeness`,
where `lane_pick.py` returns the policy answer unchanged. **And none of the four measured shapes is a
thing it produces:** `static-page` and `visual-design` (nothing is rendered here),
`brownfield-integration` (three scripts writing fresh JSON artifacts), `regression-sensitive` (no
passing contract to preserve). One clause worth adding rather than omitting silently: the reviewer
*interface* `references/positioning.md` governs is a `static-page` / `visual-design` shape, and if a
session drifts into building one, that is a different skill's work and geminify's route-out applies
there rather than here. **[docs]** *"Avoid using prompts that ask the model to perform a task for
which it has a known, fundamental limitation."*

## What transfers intact, and what the scan found

**Three scan rows dropped, three scopes added by hand.** The scan reported `every item` (line 13),
which describes the practice `lot` replaces rather than a scope the run fills, and `significantly` /
`significant` (lines 53, 57), which are the mammography studies' statistical term of art quoted from
`C7` and `C8` — not this skill's own qualifiers, and rewriting them would misquote the source. **0
bound rows**, 9 distributives and 14 prohibitions counted rather than listed. The real scopes have no
word in the scan's deliverable vocabulary — leak channels, census classes and defect classes — and
they are in the ledger below.

**Every rate the scripts print already carries its population.** `_cli.rate()` renders a percentage
with its numerator and denominator or refuses to render one, `lot_report.py` exits 2 if the population
is absent, and `escape_report.py` refuses a rate outright. Override 4 exists because that discipline
stops at the script's stdout.

**Modules.** The scan fired none at its 3-trigger threshold. `gate` is written below on two triggers,
because three of the five procedure steps are a script whose exit code is the deliverable — the
threshold missed it on vocabulary rather than substance. Nothing else is written: `visual`, `states`,
`platform-values`, `authorship` (its grounded clause is cited inside Override 4 rather than as a
section, because here it is core C2 applied to one number), `delegation`, `injection`,
`bounded-constraint` (no bound rows), `count-contract` (`lot_report.py` already exits 2 on any of six
absent fields, so extending it would restate the core), and `emphasis` — **0** shouted tokens in 114
lines.

## Override 1 — the six leak channels are cells, and the script closes two of them (`### 2`)

`This is the most important ordering constraint in the plugin`, and `references/positioning.md` names
six channels of which `all of which have to be closed for the queue to be blind`. `blind_queue.py`
builds `from an allowlist rather than by stripping fields, so a verdict cannot reach it by
construction` — which closes the payload and refuses `--carry verdict` with exit 2. The other four are
decisions a run makes and no script sees.

**[measured-family]** §1.1.1 (n=1): a run delivered **12 of 12** requirements a brief *enumerated* and
satisfied every requirement it named *categorically* with one instance or none — all surfaces → 5,
all states → **1**, all menus → **0**, all flows → **0**. Six channels named in prose is that shape.
**[docs]** *"Avoid using subjective or relative qualifiers that lack a concrete, measurable
definition."* Ship this filled:

| channel | closed by | check | closed? |
|---|---|---|---|
| a verdict field in the payload | `blind_queue.py` allowlist | exit 0, no `verdict` key in the queue | yes |
| a colour, icon or badge derived from the verdict | the allowlist | no derived field carried | yes |
| **ordering** — sorted by verdict, or failures grouped | you | queue order is the seeded shuffle, not the input order | yes |
| **the sample itself** — only machine-failed items sampled | you | sample drawn from the whole lot of 240, not from the 31 fails | yes |
| filenames, directory names or ids encoding the outcome | you | ids are opaque item ids | yes |
| a linked artefact whose first line is the verdict | you | linked evidence bundle opens on the evidence, not the verdict | `n/a: no linked artefacts in this lot` |

Report `5 of 6 closed, 1 n/a with reason`. **[docs]** *"provide instructions for handling missing data
rather than assuming inserted data will always be present and well-formed."*

## Override 2 — census means every one of them (`### 4`)

`Census-review two classes rather than sampling them, both named in the warrant: disclosure content,
and every item the panel marked inconclusive.` A census has a denominator by definition and it is the
scope most likely to collapse: reviewing three inconclusive items out of nineteen and calling the
class covered reads as done and is not.

Count them first, then report the fraction:

```bash
python3 - <<'PY'
import json, pathlib
rows = [json.loads(l) for l in pathlib.Path(".warrant/ledger.jsonl").read_text().splitlines() if l.strip()]
inc = [r for r in rows if r.get("verdict") == "inconclusive"]
print("inconclusive", len(inc), "· disclosure-class items",
      len([r for r in rows if r.get("class", "").startswith("disclosure")]))
PY
```

| census class | denominator | reviewed | reported |
|---|---|---|---|
| items the panel marked `inconclusive` | 19 | 19 | `19 of 19 reviewed in full` |
| disclosure content | 12 | 12 | `12 of 12 reviewed in full` |
| defect classes the sampled audit covered | 9 | 6 | `6 of 9 classes appeared in the sample` |

The third row is the target's own instruction: `Say which classes the audit covered.` `Roughly three
quarters of what code review finds does not affect visible functionality at all (C6), so a lot audited
only on functional defects has been audited on the minority of what a reviewer would produce.` And
`inconclusive` is a valid terminal answer (`C13`), never a retry — **[docs]** *"Avoid premature
conclusions: There may be multiple relevant options for a given situation."*

## Override 3 — exit 3 is a precondition, and the flag is a confession (`### 0`, `### 1`)

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same failed
call."* **[measured-family]** Both n=1 sessions ran the loop: four consecutive invocations of one
banned, absent tool with nothing changed between them (§1.1.2), and four consecutive `Read` calls
against a 25,000-token ceiling before pivoting to a Python split (§1.2.3). `gemini-cli` ships a loop
detector whose halt message names *"repetitive tool calls"* (§7.2).

Here the pivot that matters is the one *away* from the obvious workaround. `lot_plan.py exits 3
without .warrant/suite-health.json, naming assay as the step that produces it.` The correct next
action is to run `assay`, not to add `--unmeasured-suite`. That flag `plans anyway and records the
omission in the plan and on every run`, which is a confession travelling with the artifact rather than
a way past the gate — `so a plan built over an unmeasured suite cannot pass as one built over a
measured one`. If it is used, the delivery note leads with it.

The other two nonzero exits are findings, not obstacles. `blind_queue.py` exit 2 `naming every way the
field would have leaked, by field name and by value` — read the names and fix the queue; retrying with
`--carry verdict` is the one arrangement the evidence forbids. `lot_report.py` exit 2 on an absent
field means supply the field, never drop it from the report.

## Override 4 — no bare percentage, anywhere the scripts cannot reach (`## Constraints`)

`Never print a bare percentage.` The scripts obey this mechanically; the sentence a run writes
underneath them does not. `Published proficiency-test failure rates differ by more than twentyfold
depending on the denominator — 1.4% of 670,489 challenges across 665 laboratories against 32.4% of
lab-parameter results across three, both correct (C19).`

Three specific numbers in this skill are easy to strip: a sample's error rate quoted without the
sample size, a seed recovery figure quoted without how many seeds were planted, and `roughly three
quarters` (`C6`) restated as a property of this lot rather than of the cited corpus. **[docs]**
*"Verify your claims by quoting the exact applicable information (including policies) when referring
to them."*, and the grounded instruction's last clause is the form the honest sentence takes: *"If the
exact answer is not explicitly written in the context, you must state that the information is not
available."*

Two more sentences that must survive into the report because they bound what the decision means. `The
sample bounds the lot, not the item` — a passing lot audit says nothing about any particular item in
it, including the sampled ones. And `Report a seed the reviewer missed as a finding about the review,
not about the item.` **[measured-family]** §1.1.2 (n=1) is what the alternative looks like: five
well-formed `PASS` rows, a browser engine asserted as verified after failing all four invocation
attempts, and `100% pass rate on contrast` from a probe never executed.

## Override 5 — paste the report, prove the gate can fail, read the oracle mix (`### 5`)

**[measured-family]** §1.2.2: an auditor validated tags, citations and contrast floors thoroughly, had
no check that its prerequisite artifacts existed, and returned exit 0 over two skipped steps.
**[derived]** geminify's own quote gate went green across every file after a change took its checked
count to zero, caught only by re-running the negative control (§5). The plugin ships the control:

```
plan     lot_plan.py --root . --lot 240 --lot-id 2026-08-23
         → suite-health present · TER 0.02 · initial sample 34 · stop-clean at 34 · escalate at 2
queue    blind_queue.py --root . --items items.json --lot-id 2026-08-23 --seeds seeds.local.json
         → 34 rows, 0 verdict-bearing fields · operator key mode 600 · exit 0
report   lot_report.py --plan plan.json --result result.json --review review.json --key key.json
         → population 240 · TER 0.02 · sample 34 · seeds recovered 4 of 5 · ACCEPT
         → oracle mix: effect 11 · state 15 · render 8
control  lot_plan.py --selftest · blind_queue.py --selftest · lot_report.py --selftest → exit 0
```

**[docs]** *"Include specific verification steps in either the system instructions or your prompts
directly."* The oracle mix is the row to read rather than skim: `The renderer says so when no sampled
case stands on an effect rung, rather than leaving a reader to notice.` A mix with zero effect-rung
cases means the lot was audited on whether the surface looked right. **[docs]** *"When model outputs
must be machine-readable or follow a specific format, use a widely recognized standard like JSON,
XML, Markdown or YAML that can be parsed by common libraries."*, and count over those files in Python
— **[docs]** *"Gemini's code execution tool enables the model to generate and run Python code, and
should be enabled whenever the model needs to perform any kind of arithmetic, counting, or
calculation."*

## Override 6 — the evidence is read, never recalled (`### 2`, `references/positioning.md`)

**[docs]** *"Your knowledge cutoff date is January 2025."*, and from the 3.7 Flash model card, *"The
knowledge cutoff date for Gemini 3.7 Flash is March 2026 — users can expect updated information for
some domains while in others they may experience the model's knowledge is limited to January 2025 (in
line with the Gemini 3 Model Family)."* **[measured-family]** §1.1.4: a previous-generation published
value returned confidently, eight metric errors in one artifact — a recalled fact, not a guess.

`C5`, `C6`, `C7`, `C8` and `C19` are claim ids resolving in `warrant/references/evidence.md` and
`docs/deep-research/claims.json`, and every one carries a bound: `C7` and `C8` are observational
rather than randomised, and `positioning.md` says outright that they are `not evidence that automated
verification is harmful` — they measure *placement*. Restating either as a general claim about
automation misquotes the strongest evidence in the corpus. **[docs]** *"Do not assume or infer from
the provided facts; simply report them exactly as they appear."*

`SKILL.md` names `references/positioning.md`; read it before step 2 rather than after.
**[measured-family]** §1.2.4 recorded both halves failing in one session — answering from memory when
three skills were named, then launching a skill when an answer was wanted. Read, then act.

## Override 7 — `thinking_level`, and what it is not for

**[docs]** `HIGH` is described as suitable for *"multi-step planning, verified code generation, or
advanced function calling scenarios"*; 3.7 Flash defaults to `MEDIUM`. `lot` is three commands and a
careful read of their output — run the default. **[measured-family]** Do not raise it as a remedy for
anything above: paired across 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on 58, mean
−1.7 points (§2.3). **[docs]** *"Higher thinking levels encourage the model to use more tools to
explore and verify, so lowering the level can reduce tool calls."*

## Recap

**[docs]** *"Concise repeat of the key points of the prompt, especially the constraints and response
format, at the end of the prompt."*

1. Fill the six-channel leak table and report `N of 6 closed`; the script closes two, the other four
   are ordering, sample composition, naming and linked artefacts.
2. Census means all of them: count the `inconclusive` items and the disclosure items first, review
   every one, and say which defect classes the sample actually covered.
3. Exit 3 sends you to `assay`, not to `--unmeasured-suite`; exit 2 from `blind_queue.py` names the
   leak; exit 2 from `lot_report.py` means supply the field.
4. Write no bare percentage, and carry `the sample bounds the lot, not the item` and the seed rule
   into the report.
5. Paste the three commands with their numbers, run `--selftest` before believing them, and read the
   oracle mix for an effect-rung case before calling the lot audited.
