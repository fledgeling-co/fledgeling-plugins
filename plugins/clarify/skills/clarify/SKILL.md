---
name: clarify
description: >
  Decide whether to interrupt the user with a question, then ask it so it takes one click to
  answer. Use this whenever you are about to ask the user something mid-task, when you hit a
  fork with several defensible answers, when a request is ambiguous enough that two readings
  would produce different work, before anything destructive or irreversible, and whenever
  someone types /clarify or says "ask me what you need", "what do you need from me", "check
  with me first", or "stop guessing". Sweeps for the answer in the conversation, the repo and
  earlier agent output before asking anything, kills questions whose answer would not change
  the work, then emits a single batched AskUserQuestion — plain wording, a marked
  recommendation with its reason, options described by what changes if chosen — and treats any
  note the user attaches to an answer as binding. Not for routine judgment calls you should
  make yourself, and not a substitute for investigating first.
license: MIT
---

# Clarify

Asking is expensive. It costs the user a context switch, and it costs you their confidence if
the answer was somewhere you could have looked. Not asking is also expensive: work built on a
guess gets thrown away, and the user finds out last.

So this is two jobs, and they fail differently:

| Job | The failure it prevents |
| --- | --- |
| **The gate** — should this be a question at all? | Interrupting for something already on disk, something that changes nothing, or something you were supposed to decide |
| **The craft** — what does the question look like? | A question that costs more to answer than to ignore |
| **The handling** — what happens to the answer? | Reading the option label and discarding the note attached to it |

Most agents fail the gate, then fail the craft, then never notice they failed the handling.

## The gate

Run these in order. The first one that resolves ends it.

### 1. Is it already answered?

Sweep before you compose anything. The answer usually exists:

- **This conversation** — including what the user mentioned in passing, three messages ago,
  while talking about something else. This is the most common place the answer already is.
- **The repo** — `CLAUDE.md`, `README`, config files, the manifest, existing code that already
  made this decision once.
- **Work already done this session** — a subagent's findings, a plan file, a failed run's
  partial output, a research report, tool output you have not re-read. Long sessions are where
  answers get lost, and re-asking is how the user finds out you lost one.
- **The files themselves** — open them. A question about code you have not read is not a
  clarifying question, it is a substitute for reading.

When you find it, use it and **say where you found it** in one clause. That is what makes the
difference between "I read your setup" and "I assumed".

### 2. Would the answer change the work?

If both branches produce substantially the same deliverable, there is no question here. Pick
the sensible default, name it in one clause, and carry on. Asking about a choice that does not
propagate spends the user's attention on nothing and trains them to skim the next one.

### 3. Is it yours to settle, or theirs?

**Yours:** conventional defaults, matters of craft, local reversible actions, anything where
one option is standard and nothing in the project contradicts it.

**Theirs:** taste, cost, scope, risk tolerance, priorities, deadlines, and anything about
*their* system or preference that is not written down anywhere you can reach.

If you are unsure, ask which way the mistake is cheaper to undo. Cheap to undo is yours.

### The override: unrecoverable beats routine

Ask before anything destructive, irreversible, outward-facing, or costly — even when a
conventional default exists, and even when the user's instruction implies it. Dropping a
production table has a conventional default too. "Decide the routine ones yourself" is about
the cost of asking, and it stops applying the moment being wrong cannot be undone.

Actions that earn a question regardless: deleting data or branches, force-pushing, publishing,
sending anything to a person or an external service, spending money, touching production.

### The trap in the other direction

**Do not ask as a way of avoiding the work.** Presenting three approaches you have not
evaluated is not clarification, it is handing the thinking back. The test is the
recommendation: if you cannot say which option you would pick and why, you have not
investigated enough to be asking yet. Go and find out, then ask about what is genuinely left.

This is the strongest rule here, because it is self-enforcing. Every question below requires a
reasoned recommendation, and you cannot write one you have not earned.

## The craft

One `AskUserQuestion` call. Up to four questions in it. Serialising — asking one, waiting,
asking the next — is the expensive failure: each round is a fresh context switch for the user,
and later questions often become answerable once the earlier ones land.

Before the call, in one or two sentences: what you already worked out, and what you checked and
ruled out. This frames the questions as narrowing rather than starting over, and it shows the
sweep happened.

Say plainly that they can add a note to any answer. The note field is where the real constraint
usually arrives — the thing that was not any of your options.

### Shape

| Element | Rule | Why |
| --- | --- | --- |
| Questions per call | 1-4 | Beyond four, later answers get skimmed |
| Options per question | 2-4 | More options slows the decision without improving it |
| `header` | ≤ 12 characters | It renders as a chip; longer gets cut |
| Question text | ≤ 20 words, ends in `?` | It has to be readable at a glance, mid-task |
| Option label | ≤ 5 words | It is a label, not a sentence |
| Option description | ≤ 30 words | Say what changes; stop |
| `(Recommended)` | Exactly one, listed first, single-select only | An unranked menu makes them do your job |
| `multiSelect` | Only when the options genuinely combine | Exclusive choices marked multi-select read as a mistake |
| `Other` | Never author it | It is added automatically; authoring it wastes a slot |

Run `scripts/lint_questions.py` on the payload before you send it. It checks every mechanical
rule above, plus near-duplicate options and vocabulary that reads as internal jargon. It
deliberately does not check whether the question was worth asking — that is the gate's job and
no script can do it.

```bash
python3 scripts/lint_questions.py payload.json    # exit 0 clean, 1 on any error
```

### Wording: describe the consequence, not the mechanism

This is the highest-leverage rewrite, and the one most agents skip. A fork is technical; the
*decision* rarely is. Translate it.

**Instead of:**
> Which backpressure strategy should the ingest pipeline adopt when the queue saturates —
> drop-newest, drop-oldest, or blocking backpressure with a bounded channel?

**Ask:**
> When the queue fills up, what should give?
> - **Slow everything down (Recommended)** — Nothing is lost, but the whole app feels sluggish
>   under load. Safest for billing data.
> - **Drop the newest data** — Stays fast, but you lose the most recent events during a spike.
> - **Drop the oldest data** — Stays fast, keeps recent events, loses history.

Same fork. The second one is answerable by someone who has never heard the word backpressure,
and it is answerable in about two seconds by someone who has.

The moves that do it:

- **Name the consequence, not the mechanism.** "You lose recent events" beats "drop-newest".
- **Put the trade-off in the description**, so the choice is visible without expanding anything.
- **Drop internal vocabulary** — file paths, class names, unexpanded acronyms. If a term has to
  appear, spend three words explaining it.
- **Cut the preamble.** "Given the constraints we discussed, which approach would you prefer
  that we adopt going forward" is fourteen words of throat-clearing. "What should give?" is the
  question.
- **Never ask two things in one question.** If it contains "and", check whether it is two
  questions wearing one coat.

### Options must be genuinely different

Three phrasings of one idea is one option, not three. Before sending, read the labels
side by side: if two would lead to the same work, collapse them and find the fork that
actually exists. The linter catches the obvious cases; near-synonyms dressed in different
vocabulary get past it, so read them yourself.

### The recommendation carries evidence, not preference

Mark exactly one option `(Recommended)`, list it first, and put the *reason* in its
description — drawn from the repo, the constraints, or the trade-off. "Recommended" alone is a
preference. "Recommended, because everything else here already uses it" is a recommendation.

A recommendation the user rejects is worth more than an open question they answer briefly: it
tells you which assumption of yours was wrong.

## The handling

The answer arrives with two parts, and the second one is the one that gets dropped.

**Read the note.** Answers can carry free-text notes attached to the chosen option, and any
`Other` answer is free text outright. The note is not decoration — it usually carries the
constraint that none of your options covered, which is exactly why the user typed it.

- **A note qualifies, narrows, or overrides the label.** Someone who picks *Postgres* and adds
  "it has to run embedded, no server process" has not chosen server Postgres. Act on the whole
  answer.
- **When the note and the label genuinely conflict**, say so plainly and say which you are
  proceeding on. Do not silently resolve it in favour of the label because the label was
  easier to parse.
- **Carry the constraint into the artifact.** If the note changed the plan, the plan should
  show it.

**Then close the loop:**

- Record what stayed assumed. Anything the user did not settle is a stated assumption, not a
  quietly resolved one.
- Do not re-ask an axis that was answered, including one answered inside a note.
- Get on with the work. The question was to unblock it, not to replace it.

## When the answer is too vague to build on

"Make it better" does not determine an output, a trigger or a done condition. Do not build
against it and do not guess.

Offer two or three concrete readings of the vague answer and let the user pick. That converts
an open question into a discrete one and usually resolves in a single round — which is exactly
what the rest of this skill is for.

## Worked examples

`references/patterns.md` carries before-and-after pairs for the cases that recur: the question
that was already answered, the fork that changes nothing, the jargon translation, the
near-synonym collapse, the note that overrides its label, and the destructive action that gets
asked about despite a default. Read it when a question you are composing does not obviously fit
the rules above.

`references/evidence.md` carries the research behind the numbers — why four questions and not
six, why a marked recommendation helps rather than biases, and where the evidence is contested.
