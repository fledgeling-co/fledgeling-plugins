# gemini.md — `ledger`

Read this once, now, then read `SKILL.md` and follow it with the overrides below; each names the
section it lands on. `ledger` is the smallest skill in the plugin and the one with the least room for
recovery: it appends rows to a hash chain that no later step may correct, and its integrity property
is, in the target's own words, `the whole value`. Two of this model's measured failure directions land
directly on it — a retry that repeats a call whose effect already happened, and a stated
one-per-thing bound that nothing reads back.

## Epistemic status

- **Tiers used:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]`: **no Gemini run of
  `ledger` has been observed**, at any tier.
- **`[measured-family]` sources:** two single sessions (n=1 each) and a 106-task benchmark at two
  effort levels — `geminify/references/evidence.md`. None watched a model append to an audit record.
- **The tier the evidence is about.** Every measured rate below was observed on `gemini-3.7-flash`
  (one session on `gemini-3.7-flash-high`) — flash-tier claims, **not** to be projected onto the Pro
  tier. **[docs]** The default drifts inside the family: *"If thinking_level is not specified, Gemini
  3 will default to high."* against, from the 3.5 Flash release notes, *"The default thinking effort
  is now medium, changed from high in Gemini 3 Flash Preview."* On Pro these overrides stand as
  `[docs]`-grounded discipline and every `[measured-family]` number is open.
- **Unmeasured on this skill:** no Gemini run of `ledger` · no evidence a `gemini.md` fixes anything
  on either source · the bound-following rate in §2.2 was measured on CSS assertions in UI briefs, so
  its transfer to a row-per-decision bound is `[derived]` · nothing measures this family appending to
  a hash chain, recovering from a partial write, or choosing between two audit sinks.
- **The self-limitation.** **[docs]** A conditional side file is the shape the checklist warns about:
  *"Avoid writing a prompt with non-linear logic or conditionals that require the model to piece
  together fragmented instructions from multiple different places in the prompt."* One pass, then work
  from `SKILL.md`.

## There is no route-out block here

geminify writes one only where the benchmark measured the work, and `ledger` fails both conditions.
**Its work class is one the corpus abstains on:** the bench measures a model *building* an artifact,
while `ledger` appends a record and runs a verifier over it — `verification`, where `lane_pick.py`
returns the policy answer unchanged. **And none of the four measured shapes is a thing it produces:**
`static-page` and `visual-design` (nothing is rendered), `brownfield-integration` (the one place it
touches existing code — emitting into the repository's own audit-capture module — is a call site, not
a multi-file edit under several acceptance criteria), `regression-sensitive` (`ledger_verify.py` is
the contract rather than something that must survive one). **[docs]** *"Avoid using prompts that ask
the model to perform a task for which it has a known, fundamental limitation."*

## What transfers intact, and what the scan found

**One quota row and one bound row, both kept, no rows dropped.** The scan found `Each row` (line 27)
and `one row per` (line 5) over 80 lines, with 6 distributives and 9 prohibitions counted rather than
listed. Both are real and both are below: the quota row is the eight fields a row has to carry, the
bound row is the one this skill can be destroyed by.

**The gate discipline is already written, in the target's own words, and it is geminify's own
lesson.** `Verify by exit code rather than by reading the output. Piping a gate through grep reports
grep's status, and that has already turned a failure into a pass once in this marketplace.` Nothing
below strengthens that; Override 4 only adds the negative control.

**Modules.** The scan fired none at its 3-trigger threshold. Two are written anyway, and the counts
are disclosed rather than hidden. `gate` (2 triggers): `ledger_verify.py`'s exit code is the entire
deliverable of step 2. `bounded-constraint` (1 trigger): the scan found a real bound row, and a bound
ledger is that module's content rather than the core's. Nothing else is written: `visual`, `states`,
`platform-values`, `authorship`, `delegation`, `injection`, `count-contract` (the row count is already
printed by `ledger_verify.py`, so extending it would restate the core), and `emphasis` — **0** shouted
tokens in 80 lines.

## Override 1 — one row per decision, read back off the chain (`## Procedure 1`, `## Constraints`)

**[measured-family]** §2.2 — across 106 benchmark tasks, **58%** of this family's failing UI
assertions at `medium` and **86%** at `high` were bound-shaped (`exactly N`, `no`, `not`, `only`),
against **8%** for opus and **6%** for the OpenAI lane, and the single most-repeated bound failed on
*every* instance in its set while the same run passed 37 of its 39 other assertions. A bound is
violated by what you did not write, so it survives every check that looks at what you did.

`ledger`'s bound is `one row per decision`, and its violation has a named cause in the target itself:
`the effect already happened, and raising invites a retry that appends the row twice`. So the readback
is a count of rows carrying that item id, run after the append, not a belief about whether the call
succeeded. This ledger ships filled rather than described:

| instance | property | stated bound | readback | observed | within? |
|---|---|---|---|---|---|
| `DIO-1417` | ledger rows for this decision | one row per decision | `grep -c DIO-1417 .warrant/ledger.jsonl` | 2 | **no** — a retry after a timeout |
| `DIO-1418` | ledger rows for this decision | one row per decision | same | 1 | yes |

A duplicate is not repaired by deletion. It is recorded, and the correcting row references it —
Override 3.

**[docs]** Google treats constraints as a component in their own right: *"Restrictions on what the
model must adhere to when generating a response, including what the model can and can't do."* And
*"Ensure that all requirements, constraints, options, and preferences are exhaustively incorporated
into your plan."*

## Override 2 — the eight fields are cells to fill, not a table to read (`## What a row has to carry`)

**[measured-family]** §1.1.1 (n=1): a run delivered **12 of 12** requirements a brief *enumerated* and
satisfied every requirement it named *categorically* with one instance or none — all surfaces → 5,
all states → **1**, all menus → **0**. `Each row carries` is prose; eight cells with values are not.
**[docs]** *"Avoid using subjective or relative qualifiers that lack a concrete, measurable
definition."*

The consequence of one missing cell is stated in the target and it is not a warning: a row without a
defect class `cannot be counted and blocks the promotion rather than being skipped`. Write one row at
full fidelity first — **[docs]** *"We recommend to always include few-shot examples in your prompts."*,
and *"you can remove instructions from your prompt if your examples are clear enough in showing the
task at hand"*:

| flag | value | read from |
|---|---|---|
| `--item` | `DIO-1417` | the item under decision |
| `--class` | `disclosure-figure-unsourced` | the warrant's class list — never a new name coined here |
| `--warrant-version` | `4` | `.warrant/warrant.toml` |
| `--model-id` / `--model-version` | `gpt-5.6-sol` / `2026-07-14` | `.warrant/lanes.toml`, the pinned pair |
| `--evidence-digest` | `sha256:9f3c…a41` | the evidence bundle actually judged |
| `--verdict` | `inconclusive` | including this one: it is a valid terminal answer (`C13`) |
| `--tier` | `1` | the class's tier at the time, not the tier being sought |
| outcome | appended later, referencing this row | never edited into it |

Report `8 of 8 fields on 12 of 12 rows`. A cell you cannot fill reads `n/a: <reason>` — **[docs]**
*"provide instructions for handling missing data rather than assuming inserted data will always be
present and well-formed."* And `inconclusive` is written when it is true rather than forced to
`pass` or `fail`: **[docs]** *"Avoid premature conclusions: There may be multiple relevant options for
a given situation."*

## Override 3 — never rewrite a row, and never retry an append (`## Constraints`, `### 3`)

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same failed
call."* **[measured-family]** Both n=1 sessions ran the loop: four consecutive invocations of one
banned, absent tool with nothing changed between them (§1.1.2), and four consecutive `Read` calls
against a 25,000-token ceiling before pivoting to a Python split (§1.2.3). `gemini-cli` ships a loop
detector whose halt message names *"repetitive tool calls"* (§7.2).

Here the retry ceiling is **zero, not two**, and it is the only place in this plugin where that is
true. `ledger.py` has an external effect the moment it appends. When a call fails, times out or
returns nothing readable, the next action is a **read of the chain**, never a second append:

```bash
tail -n 3 .warrant/ledger.jsonl        # did the row land?
python3 scripts/ledger_verify.py --root .   # is the chain still intact?
```

Then, if it landed, stop; if it did not, append once. **[docs]** *"Inhibit your response: only take an
action after all the above reasoning is completed. Once you've taken an action, you cannot take it
back."*

And a wrong row stays. `Never rewrite a row to correct it. Append a correcting row that references the
original. The wrong row is part of the record, and removing it is the edit an auditor is looking for.`
This is the instruction most likely to be quietly improved on by a model asked to fix an error, and
the improvement destroys the artifact: every hash after the edited row breaks, which is the property
`ledger_verify.py` exists to detect.

## Override 4 — the exit code is the answer, and prove it can fail (`### 2`)

**[measured-family]** §1.2.2: an auditor validated tags, citations and contrast floors thoroughly, had
no check that its prerequisite artifacts existed, and returned exit 0 over two skipped steps.
**[derived]** geminify's own quote gate went green across every file after a change took its checked
count to zero, caught only by re-running the negative control (§5). Run the control the plugin
already ships:

```bash
python3 scripts/ledger_verify.py --selftest   # exit 0 only if every rule fired
python3 scripts/ledger_verify.py --root .     # → rows 214 · exit 0
```

Paste both, with the row count, into the delivery note — **[docs]** *"Include specific verification
steps in either the system instructions or your prompts directly."* and *"Verify your claims by
quoting the exact applicable information (including policies) when referring to them."* A verify over
an empty or absent ledger is not an intact chain; it is no chain, and it is reported as absent.
**[docs]** *"When model outputs must be machine-readable or follow a specific format, use a widely
recognized standard like JSON, XML, Markdown or YAML that can be parsed by common libraries."* — count
rows over `.warrant/ledger.jsonl` in Python rather than by eye, and **[docs]** *"Gemini's code
execution tool enables the model to generate and run Python code, and should be enabled whenever the
model needs to perform any kind of arithmetic, counting, or calculation."*

## Override 5 — look for the existing chain before writing a second one (`## Where this writes`)

The target names a specific sink: `The target repository already has a hash-chained, encrypted audit
log at apps/api/src/modules/audit-log/audit-capture.ts`, and `Emit into that rather than building a
second chain: two audit records of the same event diverge, and the divergence is discovered by the
auditor.` `.warrant/ledger.jsonl` is the fallback, and it is also the default a run reaches for
without looking.

So the first act of this skill is a read, not a write: search the repository for an existing
append-only or hash-chained audit sink and record what was found. **[measured-family]** §1.2.4 — asked
a question naming three skills, a run answered from memory without loading any of them, then inverted
the error by launching a skill when an answer was wanted. Read, then act, as two ordered steps. The
delivery note names the sink chosen and the evidence for the choice, in one line: `sink
.warrant/ledger.jsonl · searched apps/api for audit-capture · none found`.

## Override 6 — `thinking_level`, and what it is not for

**[docs]** `HIGH` is described as suitable for *"multi-step planning, verified code generation, or
advanced function calling scenarios"*; 3.7 Flash defaults to `MEDIUM`. `ledger` is one append and one
verify — run the default. **[measured-family]** Do not raise it as a remedy for anything above: paired
across 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on 58, mean −1.7 points, while the
bound-shaped share of failures *rose* from 58% to 86% (§2.2, §2.3) — the wrong direction for Override
1. **[docs]** *"Higher thinking levels encourage the model to use more tools to explore and verify, so
lowering the level can reduce tool calls."*

## Recap

**[docs]** *"Concise repeat of the key points of the prompt, especially the constraints and response
format, at the end of the prompt."*

1. One row per decision, checked by counting rows for that item id after the append — not by
   believing the call succeeded.
2. Eight cells per row, each read from a file rather than recalled; report `8 of 8` and let
   `inconclusive` stand.
3. Zero retries on an append. Read the chain, then append once or not at all; never rewrite a row,
   append a correcting row that references it.
4. Paste `ledger_verify.py`'s exit code and row count, and run `--selftest` before believing a clean
   chain.
5. Search for the repository's existing audit sink before writing to `.warrant/ledger.jsonl`, and name
   the sink you chose.
