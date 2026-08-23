# gemini.md — `feedback`

Read this once, now, then read `SKILL.md` and follow it with the overrides below; each names the
section it lands on. `feedback` is the plugin's calibration, and everything it produces is a count
with a caveat attached. Two properties make it the riskiest skill here for this model: it asks for
figures whose denominators do not exist, and it asks the run to record which model version was live
at the time — a fact about the past that a model will answer from self-knowledge if nothing stops it.

## Epistemic status

- **Tiers used:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]`: **no Gemini run of
  `feedback` has been observed**, at any tier.
- **`[measured-family]` sources:** two single sessions (n=1 each) and a 106-task benchmark at two
  effort levels — `geminify/references/evidence.md`. None watched a model build a regression corpus
  or report an escape.
- **The tier the evidence is about.** Every measured rate below was observed on `gemini-3.7-flash`
  (one session on `gemini-3.7-flash-high`) — flash-tier claims, **not** to be projected onto the Pro
  tier. **[docs]** The default drifts inside the family: *"If thinking_level is not specified, Gemini
  3 will default to high."* against, from the 3.5 Flash release notes, *"The default thinking effort
  is now medium, changed from high in Gemini 3 Flash Preview."* On Pro these overrides stand as
  `[docs]`-grounded discipline and every `[measured-family]` number is open.
- **Unmeasured on this skill:** no Gemini run of `feedback` · no evidence a `gemini.md` fixes anything
  on either source · nothing measures this family recording a defect escape, reasoning about a
  missing denominator, or reading a churn proxy · the categorical-collapse and fabrication
  observations were made on UI and research briefs, so their transfer here is `[derived]`.
- **The self-limitation.** **[docs]** A conditional side file is the shape the checklist warns about:
  *"Avoid writing a prompt with non-linear logic or conditionals that require the model to piece
  together fragmented instructions from multiple different places in the prompt."* One pass, then work
  from `SKILL.md`.

## There is no route-out block here

geminify writes one only where the benchmark measured the work, and `feedback` fails both conditions.
**Its work class is one the corpus abstains on:** the bench measures a model *building* an artifact,
while `feedback` records what went wrong and re-runs a corpus — `verification` and `completeness`,
where `lane_pick.py` returns the policy answer unchanged. **And none of the four measured shapes is a
thing it produces:** `static-page` and `visual-design` (nothing is rendered), `brownfield-integration`
(`regress_build.py` writes a fresh directory per escape and is idempotent),
`regression-sensitive` — which is the near miss worth naming, because `feedback` *builds* the
regression corpus rather than editing code that must keep passing one. **[docs]** *"Avoid using
prompts that ask the model to perform a task for which it has a known, fundamental limitation."*

## What transfers intact, and what the scan found

**Two scan rows dropped, two added by hand.** The scan reported `each case` (line 50) and `every case`
(line 104): the first describes what `regress_run.py` prints, the second is a retention policy — both
prose, neither a scope the run enumerates. The real scopes have no word in the scan's deliverable
vocabulary, because they are escapes and classes: `--all # every escape not yet built`, and `Every
historical escape runs against the current lanes`. Those are in the ledger below. **0 bound rows**, 9
distributives and 9 prohibitions counted rather than listed.

**The three limits are the skill, and they transfer intact.** `No false-rejection rate`, `A numerator
with no denominator`, `No bound on what is still hidden` are already stated with the mechanism that
enforces each — and `escape_report.py` `refuses to print a rate — asked for one, it exits 1 with the
reason`. Nothing in the target needs strengthening; Override 2 exists because the script cannot gate
the prose the run writes around it.

**Modules.** The scan fired none at its 3-trigger threshold. `gate` is written below on two triggers,
because five of the five procedure steps are a script whose exit code is the deliverable — that is
what the module is for, and the threshold missed it on vocabulary rather than substance. Nothing else
is written: `visual`, `states`, `platform-values`, `authorship` (its grounded clause is cited inside
Override 2 rather than as a section, because here it is core C2 applied to one number),
`delegation`, `injection`, `bounded-constraint` (no bound rows), `count-contract`, and `emphasis` —
**0** shouted tokens in 108 lines.

## Override 1 — the corpus has four denominators, and they get printed (`### 2`, `### 3`, `### 5`)

**[measured-family]** §1.1.1 (n=1): a run delivered **12 of 12** requirements a brief *enumerated* and
satisfied every requirement it named *categorically* with one instance or none — all surfaces → 5,
all states → **1**, all menus → **0**, all flows → **0**. `--all` is a categorical scope wearing a
flag. **[docs]** *"Avoid using subjective or relative qualifiers that lack a concrete, measurable
definition."*

Print the four numbers before running anything, then report the fraction after:

```bash
python3 - <<'PY'
import json, pathlib
esc = [json.loads(l) for l in pathlib.Path(".warrant/escapes.jsonl").read_text().splitlines() if l.strip()]
built = {p.name for p in pathlib.Path(".warrant/regression").glob("*") if p.is_dir()}
cls = sorted({e["class"] for e in esc})
print("escapes", len(esc), "· built", len(built), "· unbuilt",
      len([e for e in esc if e["id"] not in built]), "· classes with escapes", len(cls))
PY
```

| scope, in `feedback`'s own words | denominator | done | reported |
|---|---|---|---|
| escapes recorded this session | 3 | 3 | `3 of 3, each with its evidence digest` |
| `every escape not yet built` | 4 | 4 | `4 of 4 built; 17 in the corpus total` |
| `Every historical escape runs against the current lanes` | 17 | 17 | `17 of 17 run, 1 no longer caught` |
| warrant classes with no escape reported | 6 of 9 | 6 | `6 of 9 classes have no reported escape` |

A cell you cannot fill reads `n/a: <reason>` — **[docs]** *"provide instructions for handling missing
data rather than assuming inserted data will always be present and well-formed."* And the last row is
reported in the target's own words: `Report a class with no escapes as having no escapes rather than
as reliable.`

## Override 2 — do not compute the rate the script refuses to print (`## What this measures, and what it cannot`)

`escape_report.py` `emits counts, classes and trends, and refuses to print a rate`. That refusal is
mechanical and it does not reach the sentence the run writes underneath the output. Three escapes
over forty closed items is not 7.5%; it is three escapes and an unknown denominator, and writing the
percentage anywhere — a summary line, a table cell, a commit message — is `C19` reproduced by hand:
published proficiency-test failure rates differ by more than twentyfold on the denominator alone,
1.4% of 670,489 challenges against 32.4% of lab-parameter results, both correct.

**[docs]** *"Verify your claims by quoting the exact applicable information (including policies) when
referring to them."* And the grounded instruction's last clause is the exact form the honest sentence
takes: *"If the exact answer is not explicitly written in the context, you must state that the
information is not available."* Also *"Treat the provided context as the absolute limit of truth; any
facts or details that are not directly mentioned in the context must be considered **completely
untruthful** and **completely unsupported**."*

**[measured-family]** §1.1.2 (n=1) is what the alternative looks like: a run wrote its own review as
five well-formed rows, all `PASS`, asserting a browser engine it never ran and `100% pass rate on
contrast` from a probe never executed — measured afterwards, every primary button 3.65:1 and one
glyph 1.00:1, invisible. A percentage is the most believable thing a report can invent, because
nothing about it looks invented.

## Override 3 — record the version that was live, not the one you are (`### 1`, `## Constraints`)

`Record the model versions that were live at the time, not the current ones. An escape attributed to
today's version is an escape nobody can reproduce.` This is core C7 pointed at the one source a model
always has to hand and must not use: itself.

`feedback_record.py` captures the warrant version and the model ids and versions from `.warrant/`, so
the values come from `lanes.toml` and the ledger row for that item — not from what you know about
what you are. If the pinned version at the time cannot be recovered, the field is recorded as
unrecoverable and the escape says so; a plausible version string is worse than a blank, because it
will silently satisfy `ratchet`'s version-change comparison. **[docs]** *"Do not assume or infer from
the provided facts; simply report them exactly as they appear."*

The same rule covers a file named in a prompt. **[measured-family]** §1.2.4 recorded both halves
failing in one session — answering from memory when three skills were named, then launching a skill
when an answer was wanted. Read, then answer, as two ordered steps.

## Override 4 — an empty corpus exits 0, and that is not a pass (`### 3`)

**[measured-family]** §1.2.2: an auditor validated tags, citations and contrast floors thoroughly, had
no check that its prerequisite artifacts existed, and returned exit 0 over two skipped skill
invocations. `regress_run.py` has the same shape available to it: a corpus with nothing in it runs
nothing and returns success, and `a class may be closed by machine only while the machine demonstrably
catches everything it has previously missed in that class` is then satisfied by an empty set.

So the corpus count is a prerequisite receipt, and it is printed beside the exit code. **A denominator
of zero is a gate that never ran, never a pass.** The chain is sequential and each step's output is
the next step's input — **[docs]** *"make each step a prompt and chain the prompts together in a
sequence."*:

```
1. feedback_record.py   → .warrant/escapes.jsonl  (escape id, digest, versions at the time)
2. regress_build.py --all ← escapes.jsonl        → .warrant/regression/<escape-id>/
3. regress_run.py       ← every directory in (2) → per-case lines + exit code
4. tier-2 claim         ← (3)'s exit code and its case count, never (3)'s exit code alone
```

Run the negative control before believing a clean gate: `python3 scripts/regress_run.py --selftest`
exits 0 `only if every rule fired`, pass and fail. **[derived]** geminify's own quote gate went green
across every file after a change took its checked count to zero, caught only by re-running the
negative control (§5).

## Override 5 — exit 2 is the finding, not the obstacle (`### 3`, `### 4`)

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same failed
call."* **[measured-family]** Both n=1 sessions ran the loop: four consecutive invocations of one
banned, absent tool with nothing changed between them (§1.1.2), and four consecutive `Read` calls
against a 25,000-token ceiling before pivoting to a Python split (§1.2.3). `gemini-cli` ships a loop
detector whose halt message names *"repetitive tool calls"* (§7.2).

`regress_run.py` exit 2 `names each case no longer caught`. That is the tier-2 entry condition
failing, and it is the most valuable output this skill produces. Do not re-run it, do not narrow
`--verdict-cmd` until it passes, and do not rebuild the case. Report the named cases; the fix belongs
to the lane or to the warrant.

And `falsealarm_proxy.py` output is what the target says it is: `These are candidates from a proxy,
and the output says so.` `Same evidence digest across a fail and a later pass is the strong case` —
anything weaker is churn. Report candidates as candidates, with the count, or report none.

## Override 6 — one escape at full fidelity before the rest (`### 1`)

**[docs]** *"We recommend to always include few-shot examples in your prompts."*, and *"you can remove
instructions from your prompt if your examples are clear enough in showing the task at hand"*. Record
one completely, then let the rest match its shape:

| field | value | where it came from |
|---|---|---|
| `--class` | `disclosure-figure-unsourced` | the warrant's class list, not invented for this escape |
| `--item` | `DIO-1417` | the ledger row for the wrong verdict |
| `--missed` | `the KPI tile cited filing-2026-q3 for a figure that filing does not contain` | the reporter's own words, quoted |
| `--evidence-digest` | `sha256:9f3c…a41` | the ledger row, so the escape is reproducible |
| `--expected-verdict` | `fail` | what the pipeline should have returned |

**[docs]** *"Avoid providing examples that show the model generating its final, structured answer
before it has completed its step-by-step reasoning."* — the digest and the versions are looked up
first, and the row is written after.

## Override 7 — `thinking_level`, and what it is not for

**[docs]** `HIGH` is described as suitable for *"multi-step planning, verified code generation, or
advanced function calling scenarios"*; 3.7 Flash defaults to `MEDIUM`. `feedback` is five commands in
a fixed order and a careful sentence about denominators — run the default. **[measured-family]** Do not
raise it as a remedy for anything above: paired across 106 tasks, `high` beat `medium` on 24, lost on
24 and tied on 58, mean −1.7 points (§2.3). **[docs]** *"Higher thinking levels encourage the model to
use more tools to explore and verify, so lowering the level can reduce tool calls."*

## Recap

**[docs]** *"Concise repeat of the key points of the prompt, especially the constraints and response
format, at the end of the prompt."*

1. Print the four denominators before acting, report `N of N` after, and say `6 of 9 classes have no
   reported escape` rather than that six classes are reliable.
2. Write no rate anywhere. Counts, classes and trends only; an absent denominator is stated as
   unavailable.
3. Take the model id and version from `lanes.toml` and the ledger row for that item, never from what
   you know about yourself; an unrecoverable version is recorded as unrecoverable.
4. Print the corpus case count beside `regress_run.py`'s exit code — zero cases exiting 0 is not a
   tier-2 entry condition met — and run `--selftest` before believing a clean gate.
5. Exit 2 names the cases no longer caught: report them and stop. Do not re-run, and report churn
   findings as candidates.
