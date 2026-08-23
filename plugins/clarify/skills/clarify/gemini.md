# clarify, calibrated for Gemini

This skill was written against a Claude model's failure modes. Gemini's differ, and this
house's deliberate *removals* — verification scaffolding most of all — leave a vacuum on this
family that fills with something plausible. Read this once, before `## The gate`, then run
the skill as written with the overrides below. Little here disputes it: **clarify's
deliverable is already a set of numbers**, and `lint_questions.py` reads five of them back
off the payload. The exposed half is **the gate** — five steps of prose judgment that produce
no artifact, carry no count, and whose costliest step is a tool call nothing depends on.

## Epistemic status

`[docs]` is Google's published guidance, quoted verbatim from `gemini-corpus.md`.
`[measured-family]` is a Gemini run of *another* skill, or the 106-task benchmark corpus, and
`[derived]` is reasoning from those onto this skill's text. Section numbers are geminify's own
`references/evidence.md` file.

**The tier the evidence is about.** Every measured rate below is flash-tier —
`gemini-3.7-flash` across 106 benchmark tasks, plus two sessions on `gemini-3.7-flash` and
`gemini-3.7-flash-high`. None of it measures the Pro tier, whose `thinking_level` default and
cutoff differ; there these overrides hold as `[docs]`-grounded discipline and every
`[measured-family]` number is open. **`[measured-here]` appears once**, on the linter probe
under `gate` — this skill's own script, run while writing this file, not a Gemini run of
clarify, of which none has been recorded.

**Unmeasured on this skill:** whether gate 1's four sweep sources get swept or one does;
whether a lane's output file is read or its verdict recalled; whether the pre-question
sentence survives Gemini's default brevity; whether the two-option cap drifts to three; and
whether any override below improves anything — no run of any skill has been measured with a
`gemini.md` in place against the same work without one.

**No route-out block appears here.** `[derived]` The corpus measures a model *building* an
artifact and clarify builds none — its work is the `referral` class, for which `lane_pick.py`
returns the policy answer unchanged. All four measured shapes are omitted for that reason:
`static-page`, `brownfield-integration`, `visual-design` and `regression-sensitive` are shapes
this skill never produces, so `[docs]` "Avoid using prompts that ask the model to perform a
task for which it has a known, fundamental limitation" has nothing to point at.

`[docs]` **This file's own shape is a defect Google names**: a prompt with "non-linear logic
or conditionals that require the model to piece together fragmented instructions from multiple
different places in the prompt." Hence one pass, up front, each override naming its site.

## What transfers intact — `[derived]`, so you spend no effort where there is no gap

- **The Shape table is already the strong form.** `[docs]` **Ambiguity** asks you to "Avoid
  using subjective or relative qualifiers that lack a concrete, measurable definition," and
  twelve of clarify's rules are counts. `[measured-family]` §2.1: on tasks whose brief states
  a numeric bound, Gemini scores 74.7 against opus's 75.0 — where the requirement is already
  a number, the gap closes to nothing.
- **The lane-failure rule is the retry ceiling, already written.** `A lane that is down … is
  reported once and substituted with the next family, never retried into the ground.`
- **The note-is-data section needs nothing added.** `[docs]` **Prompt injection risk** asks
  you to "Check if there are explicit safeguards surrounding untrusted user input that is
  inserted into the prompt, as this can be a major security risk." Clarify states the
  safeguard, the elevated-risk window and the test, so no `injection` section appears below —
  and with zero capitalised imperatives across 1,290 scanned lines, no `emphasis` one either.

## C1 — four scopes that need a number

`[measured-family]` §1.1.1: on one recorded run every *enumerated* requirement shipped —
twelve named features — and every *categorical* one shipped once or not at all: `all surfaces`
→ 5, `all states` → **1**, `all menus` → **0**. `[docs]` **Too many tasks** explains why one
pass cannot satisfy several categorical nouns; its remedy is to "make each step a prompt and
chain the prompts together in a sequence."

`[derived]` The scan raised three candidates and two are prose — `every file the lane opens`
sits inside an egress warning, `every check on the question itself` inside an argument.
Dropped. The load-bearing scopes are ones a deliverable-noun regex cannot reach, because
clarify's countable units are *sources swept* and *forks referred*. The first row is the one
that collapses: `Sweep before you compose anything` names four places, and a run has no reason
to visit the fourth once the first returns something. Write the ledger before composing and
report the fractions beside the question — four cells, four clauses, or the sweep did not run.

| Scope | Its line | Count | Filled |
|---|---|--:|---|
| Gate 1's sweep sources — conversation, repo, session work, the files | SKILL.md:50–58 | 4 | `4 of 4`, each with the clause naming where |
| Technical forks surviving gates 1–3, each referred | SKILL.md:96 | one per fork | `2 of 2 referred` |
| Panel members asked whether a better approach exists | SKILL.md:187 | 3 (4 with fable) | `3 of 3 asked, 3 answered` |
| Shape-table rules the linter reads back | SKILL.md:327 | 10 | `exit 0, output pasted` |

## C7 — read what the prompt names, then answer

`[measured-family]` §1.2.4 is gate 1 failing, watched. Asked a question naming three skills,
the run answered from memory without loading any of them, and confirmed afterwards that it
had pattern-matched the prompt as a reasoning question; asked how to fix that, it inverted
the error and launched a skill instead of answering.

`[derived]` Clarify already states the rule: `A question about code you have not read is not
a clarifying question, it is a substitute for reading.` The override is that this is two
ordered steps and neither substitutes for the other. Load what the prompt names — files,
skills, reports, prior agent output — then answer: an invocation is not an answer, and a
recollection is not a read. `[docs]` The same holds for any published value the fork turns
on, since "Your knowledge cutoff date is January 2025" and the remedy is to look —
"Grounding with Google Search connects the Gemini model to real-time web content, and should
be enabled whenever the model may need to know obscure or recent facts." A fork about a
vendor's behaviour is clarify's Dossier branch, not a lane question.

## C2 — a referral you did not run is this skill's fabrication shape

`[measured-family]` §1.1.2: a run wrote itself a five-row review, every verdict `PASS`, naming
a browser engine that was invoked four times and failed every time, and reporting a 100%
contrast pass rate from a probe that never executed — measured afterwards at 3.65:1 across
every primary button, one glyph at 1.00:1. Not dishonesty: a requested *shape* completed when
the shape was specified and the procedure was not.

`[derived]` Clarify specifies exactly such a shape: the pre-question sentence must carry `what
the referral said`, `the lane or panel`, and `any shape it ruled out` — three slots a run can
fill from what it expected the lane to say. The skill's own defence is written already and
this file makes it binding: `The captured header lines are the evidence, not the command you
typed`, and `An absent or empty output file is a lane failure, not a quiet pass.` The verdict
is quoted from the lane's output file or not reported; the worked pass ships that receipt.

`[docs]` "Include specific verification steps in either the system instructions or your
prompts directly," and "Verify your claims by quoting the exact applicable information
(including policies) when referring to them." Zero lanes is not a pass; it is the sentence
`every lane failed, so I decided alone`, which the skill already permits.

## C3 and C4 — two attempts per lane, one record between steps

`[measured-family]` Two retry shapes, both recorded. §1.1.2: one banned, absent tool invoked
four consecutive times with nothing changed between calls. §1.2.3: a hard harness ceiling —
`File content (28636 tokens) exceeds maximum allowed tokens (25000)` — retried four times with
minor tweaks before the strategy changed. `[docs]` "On other errors, you must change your
strategy or arguments, not repeat the same failed call." Applied to the lanes: a usage limit,
a missing binary, a not-signed-in shell or an empty `-o` file is a **permanent** error and
pivots on attempt 1 — next family, named in the report. A timeout that fired once is transient
and gets the second attempt; there is no third.

`[derived]` For the ordering, the scan found no qualitative skill references to convert:
clarify composes no other skill, and its lanes are CLI calls that already write files
(`/tmp/so-<slug>.md`). So the conversion is small — **the payload is composed from the C1
ledger and the lane files, not from having run them.** `[measured-family]` §1.2.1 is the
mechanism: an instruction phrased as a standard rather than an artifact dependency was
satisfied by writing compliant-looking output, and the model's own diagnosis named the
absent file as the reason.

## C6 — `thinking_level`, and the one thing not to do with it

`[docs]` `HIGH` is described for "multi-step planning, verified code generation". Clarify's
gate is a five-step decision over evidence you already hold and its output is under fifty
words, so `MEDIUM` — Gemini 3.7 Flash's default — fits. **Do not lower it below that here**:
"Higher thinking levels encourage the model to use more tools to explore and verify, so
lowering the level can reduce tool calls," and gate 1 is several tool calls while gate 4 is one
per fork, so trimming tool volume trims the two gates this file protects. Name the model
beside any level you report; the family's defaults drift. `[measured-family]` Raising the level
is no remedy for anything below: paired across 106 tasks, `high` beat `medium` on 24, lost on
24 and tied on 58, mean −1.7 points.

## `bounded-constraint` — the Shape table is a bound ledger already

`[measured-family]` §2.2: classifying every failing UI assertion by whether it states a
**bound** or asks for a **thing**, Gemini's failures are 58% bound-shaped at `medium` and
**86%** at `high`, against **8%** for opus and **6%** for the OpenAI lane. Opus fails by
omitting something asked for; Gemini fails by exceeding a stated maximum while delivering
everything asked for — `exactly one soft elevation shadow` failed on *every instance in its
set* on a run that passed 37 of its 39 other assertions.

`[derived]` Clarify is almost entirely stated maxima, which both exposes it here and defends
it: five of these are machine-read. Fill the ledger from the payload, never from the rules.
`[docs]` It is also where Google puts constraints — the **Recap** component is a "Concise
repeat of the key points of the prompt, especially the constraints and response format, at the
end of the prompt." A filled instance:

| Field | Stated bound | Readback | Observed | Within? |
|---|---|---|--:|---|
| questions per call | 1 default, 3 max | `len(p["questions"])` | 1 | yes |
| options per question | 2 (3 only when earned) | `len(q["options"])` | 2 | yes |
| `header` | ≤ 12 chars | `len(q["header"])` | 10 | yes |
| question text | ≤ 20 words, ends `?` | `len(q["question"].split())` | 11 | yes |
| option label | ≤ 5 words | `max(len(o["label"].split()))` | 4 | yes |
| option description | ≤ 30 words | `max(len(o["description"].split()))` | 15 | yes |
| `(Recommended)` marks | 0 unless `irreversible` | `payload.count("(Recommended)")` | 0 | yes |
| authored `Other` options | 0 | `grep -c '"label": *"Other"'` | 0 | yes |

**The trap, in clarify's own sentences.** Three bounds are stated as prohibitions and read as
style advice: `Never author it`, `Everywhere else, mark nothing`, `Never ask two things in one
question`. A bound is violated by what you did not write, so it survives every check on what
you did. The first two are counted rows above; the third has no readback, so check the stem
for `and` by hand as the skill already says.

## `gate` — `lint_questions.py` proves the craft, never the gate

`[measured-here]` Probed while writing this file: a well-formed payload prints the single word
`clean` and exits 0; one with a 25-word stem, a 19-character header and an unearned
`(Recommended)` prints three `ERROR` lines and exits 1; one with no `questions` array exits 1.
The gate can fail, on the three classes this skill cares most about.

- **Paste the output and the counts beside it.** `clean` carries no denominator — it does not
  say how many questions, options or rules it read. `1 question, 2 options,
  lint_questions.py → clean (exit 0)` is a verified claim; `linted clean` alone is the shape
  §1.1.2 filled with fiction. `[docs]` Lint the file you are about to send, in "a widely
  recognized standard like JSON, XML, Markdown or YAML that can be parsed by common
  libraries" — not a copy of it.
- **Exit 0 certifies the payload, not the decision.** Clarify says so itself: `It deliberately
  does not check whether the question was worth asking — that is the gate's job and no script
  can do it.` A clean lint reported as though it validated the interruption is a false receipt;
  the gate's receipt is the C1 ledger.

## `authorship` — report the lane you ran, and quote the note

`[derived]` This module fired on incidental vocabulary and is kept for another reason: clarify
emits two pieces of prose a reader acts on — the sentence beside the question, and the plan
carrying the note — and neither may exceed its source.

`[docs]` Google's strictly-grounded system instruction is meant to be used verbatim, and its
last clause matters most here: "If the exact answer is not explicitly written in the context,
you must state that the information is not available." So a lane that returned nothing is
reported as such, and a ruled-out shape carries the lane's reason, not one you supplied.

`[derived]` The note is a source too, so **quote it rather than paraphrase it**: `it has to run
embedded, no server process` compressed into `lightweight database` loses the constraint that
made the user type it — the C1 collapse in one clause. `[docs]` And the pre-question sentence
runs against this family's resting state: "By default, Gemini 3 models provide direct and
efficient answers. If you need a more conversational or detailed response, you must explicitly
request it in your instructions." It is required output, not preamble, and carries the ledger
fractions and the lane verdict.

## One worked pass, end to end

`[docs]` "We recommend to always include few-shot examples in your prompts." One instance, on
the skill's own backpressure fork:

```
GATE LEDGER   sweep 4 of 4 — conversation (no prior answer) · repo (CLAUDE.md silent) ·
              session work (plan.md §3 names the queue, not the policy) · files
              (ingest/queue.ts read, bounded channel present) · forks referred 1 of 1
LANE          codex gpt-5.6-sol @ high · /tmp/so-queue.md · header greps OK · 41 lines
              VERDICT line 3: "drop-oldest is wrong here — billing history is the audited
              artifact; the real fork is latency versus recent loss."
LINT          1 question, 2 options → lint_questions.py: clean (exit 0)
```

> I read the queue code and the plan; neither settles the policy, and the OpenAI lane ruled
> out dropping the oldest data, because this queue is billing data and history is the part
> you are audited on. That leaves one call and it is yours — how much latency this product
> can wear against how much recent data it can lose.
>
> **When the queue fills up under load, what should give?**
> - **Slow everything down** — Nothing is lost, and the whole app feels sluggish while the
>   spike lasts.
> - **Drop the newest data** — Stays fast, and you lose the most recent events until the
>   spike clears.
>
> You can add a note to either answer; it is optional.

Nothing is marked: the action is reversible and the axis is the user's. The ledger, the lane
file and the lint line are the three receipts, and a pass missing one reports it missing
rather than filling it. Nothing above raises the question count or softens the two-option cap;
the gate's steps, the rungs, the panel protocol and the Shape table stand as written.
