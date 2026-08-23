# gemini.md — `should-compact`

Read this once, now, then read `SKILL.md` and follow it with the overrides below; each names the
section it lands on. `should-compact` is an unusual target, and the reason changes what this file is
for: it is *designed* for a small fast model — its own description asks for a scorer `cheap enough to
run on Haiku-class models and fast enough to sit in a hook` — so a flash-tier Gemini is the intended
runner here, not a degraded one. The terse resting state is therefore an advantage, with no preamble
to trim out of a 25-second hook: **[docs]** *"By default, Gemini 3 models provide direct and efficient
answers. If you need a more conversational or detailed response, you must explicitly request it in
your instructions."* The field where the whole deduction has to happen, `reasoning`, is the one
terseness eats first — which is Override 1.

## Epistemic status

- **Tiers used:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]`: **no Gemini run
  of `should-compact` has been observed**, at any tier.
- **`[measured-family]` sources:** two single sessions (n=1 each) and a 106-task benchmark at two
  effort levels — `geminify/references/evidence.md`. None watched a model score a boundary, run
  inside a hook, or emit a small fixed JSON object under a timeout; the categorical and bound
  failures below were measured on UI briefs, so their transfer here is `[derived]`.
- **The tier the evidence is about.** Every measured rate below was observed on `gemini-3.7-flash`
  (one session on `gemini-3.7-flash-high`) — flash-tier claims, **not** to be projected onto the Pro
  tier. **[docs]** The default drifts inside the family: *"If thinking_level is not specified, Gemini
  3 will default to high."* against, from the 3.5 Flash release notes, *"The default thinking effort
  is now medium, changed from high in Gemini 3 Flash Preview."* On Pro these overrides stand as
  `[docs]`-grounded discipline and every `[measured-family]` number is an open question.
- **Unmeasured on this skill:** no Gemini run of it · no evidence anywhere that a `gemini.md` fixes
  anything, on either source · nothing measures this family judging rather than building, which is
  the whole of this skill's work · its own numbers (998,289 · 99.8% · 267,313 · 31,189 · 98.07% ·
  4.7%) come from one operator's machine with Claude Code as the runner · `EVALS.md` scores this
  rubric on Haiku-class Claude models, not on this family.
- **The self-limitation.** **[docs]** A conditional side file is the shape the checklist warns about:
  *"Avoid writing a prompt with non-linear logic or conditionals that require the model to piece
  together fragmented instructions from multiple different places in the prompt."* Read it in one
  pass, then work from `SKILL.md`.

## There is no route-out block here

geminify writes a hand-this-work-to-another-model block only for skills whose work the benchmark
measured, and `should-compact` fails both conditions. Scoring a moment and deciding a verdict sit in
`verification`, a class the corpus abstains on — the bench measures a model *building* an artifact —
and it produces none of the four measured shapes: `static-page` and `visual-design` (it renders and
captures nothing), `brownfield-integration` (it edits no code, it appends to a log and prints JSON),
`regression-sensitive` (it holds no contract a test currently passes). **[docs]** *"Avoid using
prompts that ask the model to perform a task for which it has a known, fundamental limitation."*
Reading five booleans off ten turns is not one, and routing it out would defeat a skill whose premise
is running on every compaction.

## What transfers intact

More than usual, because this skill was written for a small model and the two design targets overlap;
naming it keeps the overrides off the parts with no gap. **Reasoning before the score is already the
documented order**, and the shipped example obeys it — `writing the deduction before the number is
what makes a small model's score stable`. **[docs]** the **Incorrect Chain of Thought (CoT) order**
entry asks for exactly that: *"Avoid providing examples that show the model generating its final,
structured answer before it has completed its step-by-step reasoning."* Do not reorder the keys.

**The numeric bands and the closed verdict set are the parts most likely to survive.**
**[measured-family]** the one bucket where this family matches opus is the one whose brief already
states a number — optimality, 74.7 against 75.0 (§2.1) — and `SKILL.md` states its bands numerically
throughout (0-3, 4-6, 7-10, ~20,000, ~40,000, 5-10 turns). A three-way `verdict` is **[docs]** the
multiple-choice fix for a model that answered correctly where *"The response is correct, but the
model didn't stay within the bounds of the options."*, so emit `compact`, `wait` or `hold` exactly.
`Expect most moments to be clean` guards against manufacturing a signal, and this family's error runs
the *other* way — §1.1.1's categorical scopes arrived as one instance or none — which is the
direction Override 1 covers.

**The braindump handoff already travels as a file.** The scan flags **0** qualitative skill
references, which is earned: `SKILL.md` says `Pass the log path to /braindump:braindump`, and the
hook emits the FACTS block as `newCustomInstructions`. **[measured-family]** §1.2.1 recorded a run
skipping both skills it was told to compose with, its own diagnosis being that nothing downstream
depended on a file only those skills produce. Keep that trap closed by naming the path, not a lens.

**Modules that did not fire.** None reached the three-trigger threshold: `gate` and
`bounded-constraint` at 2 hits, `visual`, `platform-values` and `authorship` at 1. The gate material
is not absent — it lands in Override 6, because `A silent gate is not a gate that agreed` is C2
applied to this subject. The scan's one regex bound row and four relative qualifiers (`enough`,
`clean`, `short`, `appropriate`) are prose rather than deliverable scope and were dropped; the bounds
worth binding came out of the 39 counted prohibitions by hand, into Override 2's ledger.

## Override 1 — `reasoning` is a clause per signal, each naming the turn it came from (`## What you produce`, `## The rubric`)

`signals` is what everything downstream branches on, and every entry is a **claim about the buffer**.
**[measured-family]** §1.1.2 (n=1): a run wrote its own review as five well-formed rows, all `PASS`,
asserting a browser engine as verified when it had failed all four invocation attempts, and `100%
pass rate on contrast` from a probe never executed — measured afterwards, every primary button
3.65:1 and one glyph at 1.00:1, invisible. A five-field boolean object with an obvious shape and
nothing compiling it is the same genre. `[derived]`: a run that reads one signal and infers the other
four has satisfied a set of five with one instance, §1.1.1's collapse in miniature.

Terseness is the other half. `reasoning` is not a summary of the score, it is the deduction the score
is read off, and a one-clause `reasoning` leaves a score with nothing behind it — the anchoring
failure `SKILL.md` orders the keys to prevent. The objective constraint replacing `say why in one
line`: **at least four clauses and at most eight** — the four hard-hold signals, the floor/wall
arithmetic with its two numbers, the boundary and the turn that closed it (or its absence), and the
log tail's last entry. The single human-readable line stays one line.

**[docs]** *"Include specific verification steps in either the system instructions or your prompts
directly."* and *"Verify your claims by quoting the exact applicable information (including policies)
when referring to them."* What earns each clause — the target's own rubric as a readback:

| signal | true when | the clause that earns it |
|---|---|---|
| `open_tool_chain` | a `tool_use` in the last turn has no matching `tool_result` | `turn -1 issued Edit on src/gate.ts, no result yet` |
| `unsaved_edit` | a file was read and a change described, with no write | `turn -3 read it, turn -2 described the change, nothing written` |
| `active_error` | a traceback is the live working state | `no traceback in the last 8 turns` |
| `below_floor` | context under ~20,000 tokens | `est. 612,000 from the transcript size` |
| `at_the_wall` | within ~40,000 tokens of the caller-supplied wall | `612,000 against a supplied wall of 1,000,000` |

A signal you could not read is not `false`. Name the turn you could not see and score under Override
5's rule. **[docs]** *"provide instructions for handling missing data rather than assuming inserted
data will always be present and well-formed."*

## Override 2 — the consistency bounds get read back before the object is emitted (`## The score has to agree with the signals you just wrote`)

The highest-value override here, because **one of these bounds has an external enforcer and the rest
do not**. `precompact_gate.sh` enforces the wall rule independently by reading the transcript size —
but reading it confirms that the hook parses `"score"` out of your JSON and nothing else, recomputes
headroom itself, and vetoes on `score < THRESHOLD && headroom_ok`. Your `block`, `verdict` and
`signals` are never read on that path, so a score disagreeing with your own signals is not cosmetic:
it *is* the veto, and `SKILL.md` names the consequence — `a gate branching on score would veto a
session that the signals say is perfectly safe to compact`.

**[measured-family]** §2.2 is why this needs a readback rather than a firmer restatement: across 106
tasks, 58% of failing UI assertions at `medium` and **86%** at `high` were bound-shaped — a stated
maximum exceeded — against 8% for opus and 6% for the OpenAI lane, and the most-repeated bound failed
on *every* instance in its set while the same run passed 37 of 39 other assertions. A bound is
violated by what you did not write, so it survives every check that looks at what you did.

**[docs]** Google treats these as a component in their own right — *"Restrictions on what the model
must adhere to when generating a response, including what the model can and can't do."* — and puts
them in the **Recap**: *"Concise repeat of the key points of the prompt, especially the constraints
and response format, at the end of the prompt."* Fill this before emitting; rows 1-3 ship showing a
violation:

| bound, in `SKILL.md`'s own words | stated limit | readback over your own object | observed | within? |
|---|---|---|---|---|
| `0-3 is reserved for the four vetoes in that table and nothing else` | `score >= 4` when no hard-hold signal is true | `any(hard.values()) or score >= 4` | all four false, score 3 | **no** |
| `set block: false` at the wall | `block` false whenever `at_the_wall` | `not (at_the_wall and block)` | wall true, block true | **no** |
| `compact` (7-10), `wait` (4-6) or `hold` (0-3) | verdict matches its band | `verdict == band(score)` | score 8, verdict `wait` | **no** |
| `if you cannot point at the turn that closed the phase, you are looking at 4-6, not 8` | `boundary` non-null only at score >= 7, with its turn cited | the naming clause exists in `reasoning` | `planning→implementation`, turn cited | yes |
| `must not clamp it upward or downward` | the wall is the caller's exact value | `wall == int(SHOULD_COMPACT_WINDOW_TOKENS)` | 350,000 supplied, 350,000 used | yes |

Row 1's hard-hold four are `open_tool_chain`, `unsaved_edit`, `active_error` and `below_floor`;
`at_the_wall` is not one, because `SKILL.md` is explicit that it `does not change the score`.
**[docs]** *"Inhibit your response: only take an action after all the above reasoning is completed.
Once you've taken an action, you cannot take it back."* A veto at the wall converts a lossy
compaction into a hard overflow. Check the rows before you print, not after.

## Override 3 — a second worked example, at the hold end (`## What you produce`)

`SKILL.md` ships one example: score 8, every signal `false`, a named boundary. **[docs]** *"We
recommend to always include few-shot examples in your prompts."*, *"Make sure that the structure and
formatting of few-shot examples are the same to avoid responses with undesired formats."* — but also
*"if you include too many examples, the model may start to overfit the response to the examples"*,
and one is the most overfittable number there is. `[derived]`: an open tool chain was present at only
**4.7%** of 1,522 real automatic compactions, so a run copying the shipped exemplar is right nineteen
calls in twenty and wrong on exactly the traffic this skill exists for. The hold end, at full
fidelity:

```json
{
  "reasoning": "Turn -1 issued Edit on src/gate.ts and no tool_result has returned, so open_tool_chain is true from that turn alone. Turn -3 read the same file and turn -2 described the change in prose with nothing written, so unsaved_edit is true. No traceback in the last 8 turns. Transcript estimate 612,000 tokens against a caller-supplied wall of 1,000,000, so neither below_floor nor at_the_wall. Log tail's last entry is 13:02Z at 7/10; no phase has closed since.",
  "signals": {"open_tool_chain": true, "unsaved_edit": true, "active_error": false, "below_floor": false, "at_the_wall": false},
  "boundary": null, "score": 1, "verdict": "hold", "block": true
}
```

The human line beside it reads `1/10 — hold. An edit is open across src/gate.ts and the tool result
has not come back; compacting here splits the pair and throws away the line numbers.`

## Override 4 — the wall, the floor and the hook contract are read, never recalled (`## Running as a PreCompact hook`)

**[docs]** *"Your knowledge cutoff date is January 2025."*, and from the model card, *"The knowledge
cutoff date for Gemini 3.7 Flash is March 2026"*. Three values sit on the wrong side of that, and one
has a *wrong* answer in training data. **The trigger point:** published guidance says Claude Code
compacts at 80–95% of the window; `references/evidence.md` measured 99.8% here across 235 events, so
a headroom rule built on the recalled figure never fires. **The wall:** read
`SHOULD_COMPACT_WINDOW_TOKENS`, unclamped — a 1M assumption makes the at-the-wall rule inert on every
proxied session, where Relay's managed minimum is 350,000. **The exit codes:** `exit 1` is a
*warning* and compaction proceeds; the veto is `exit 2` with the reason on stderr, and a prior about
UNIX exit codes gets that backwards — `SKILL.md` calls it `the trap`.

**[measured-family]** §1.2.4 recorded both halves of the recall failure in one session: asked a
question naming three skills, the run answered from memory without loading any; asked to fix it, it
launched a skill instead of answering. Read, then answer, as two ordered steps — which lands here,
since the hook payload names `transcript_path` and the caller may name a log path. `why did it
compact in the middle of that` is answered from the log and the buffer, never from recollection.

## Override 5 — one attempt, a two-call budget, and what `conservatively` means (`## What you read`)

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same
failed call."* **[measured-family]** both n=1 sessions ran the loop: four consecutive invocations of
one banned, absent tool with nothing changed between them (§1.1.2), and four consecutive `Read` calls
against a 25,000-token ceiling before pivoting to a Python split (§1.2.3) — a class documented beyond
this repo, since `gemini-cli` ships a loop detector naming *"repetitive tool calls"* (§7.2).

Where it lands: the hook bounds the scorer at 25 seconds and treats a timeout as a failure to score,
which fails open — four retries spends the budget and the gate goes silent, the exact failure
Override 6 is about. **[docs]** *"You have a limited action budget of <n> tool calls. Use them
efficiently."* Set n = 2: one `session_log.py tail`, one `session_log.py append`. **Never `Read` the
transcript** — `SKILL.md` says `Do not read the full transcript`, and a 600k session hits §1.2.3's
ceiling on attempt 1.

One relative qualifier to replace, because it decides a veto: `score conservatively` when the buffer
and log cannot answer. **[docs]** *"Avoid using subjective or relative qualifiers that lack a
concrete, measurable definition."* Read it as the rule the same file implies — **score 4-6, `verdict`
`wait`, `block` false, and name the missing input in `reasoning`.** 0-3 is reserved for the four
vetoes, and a signal you could not read is not one of them.

## Override 6 — prove the gate speaks, and prove it from outside itself (`### A silent gate is not a gate that agreed`)

That section is C2 in its strongest form and transfers intact; this is the receipt discipline around
it. **[measured-family]** §1.2.2: an auditor validated tag counts, citations and contrast floors
thoroughly, had no check that its prerequisite artifacts existed, and returned `0 error(s)` and exit
0 over two skipped skill invocations. This skill's own record is the same shape — a gate on both
matchers, invoked on 1,522 automatic compactions across seven days, vetoed none, and its veto text
appeared **zero** times in 3,778 transcripts. So run both checks and **paste their output**, never a
claim about them. A delivery note ships filled:

```
grep -rl "should-compact:" ~/.claude/projects --include='*.jsonl' | wc -l   → 34
printf '{"session_id":…,"trigger":"auto",…}' | precompact_gate.sh; echo $?  → EXIT=2
                                                stderr: should-compact: 1/10 — mid-edit
```

A denominator of zero is a gate that never ran, never a pass. And `SKILL.md` asks for the second
check `whenever the gate gains a new input — a session id, a model, a budget`: adding this file is
one.

## Override 7 — `thinking_level`, and the one place lowering it is on the table

**[docs]** `HIGH` is described as suitable for *"multi-step planning, verified code generation"* and
3.7 Flash defaults to `MEDIUM`. This skill is not that: it reads ten turns, checks four booleans and
two numbers, and prints an object. `MEDIUM` is the level, and **[docs]** *"Higher thinking levels
encourage the model to use more tools to explore and verify, so lowering the level can reduce tool
calls."* — the right direction where Override 5 caps the budget at two calls and the hook's 25-second
bound binds. This is the rare target where lowering is a defensible knob; measure it against
`EVALS.md` first. **[measured-family]** Do not *raise* it as a remedy for anything above: paired
across 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on 58, mean −1.7 points (§2.3),
while the bound-shaped share of failures rose from 58% to 86% (§2.2) — the failure Override 2 exists
for gets worse.

## Recap

1. `reasoning` is four to eight clauses, one per signal, each naming the turn or log line it came
   from. A signal you could not read is not `false`.
2. Fill Override 2's bound ledger before emitting. `score` is the only field the hook reads, so a
   score disagreeing with your own signals *is* the veto. Hold both exemplars in view — the shipped
   8/10 and the 1/10 above; the interesting case is 4.7% of traffic.
3. Read the wall from `SHOULD_COMPACT_WINDOW_TOKENS` unclamped, the trigger point from
   `references/evidence.md`, the exit codes from `SKILL.md`. Two tool calls, one attempt each, never
   the full transcript; unscoreable means 4-6, `wait`, `block` false.
4. Paste both inertness checks' output, exit code included — zero vetoes over hundreds of
   compactions is a finding, not a clean bill.
