---
name: decision-panel
description: >-
  Put one decision to a panel of four model families and decide it for the user. Frames the
  question and its options from the conversation and the repo, runs two rounds across Fable,
  GPT-6 Astra, Gemini Argon and Grok (each resolved at run time to the newest model), settles it
  with evidence first and votes second, records every model's position and the dissent on a
  self-contained HTML decision page, then acts on the result. Use when the user explicitly asks
  for a panel to decide: "have the panel decide", "put this to the panel", "panel this", "let the
  models decide between X and Y", "decide this for me with the panel", "/decision-panel:decision-panel", for
  choices that deserve deliberate, recorded judgement such as architecture, product direction,
  pricing, vendor or tool selection, or whether a plan is a good one. The panel decides on the
  user's behalf; actions that are destructive, irreversible, outward-facing or cost money still
  wait for their confirmation. Not for quick forks met during other work (clarify:clarify refers
  those on its own), not for reviewing someone's feedback (feedback-panel:feedback-panel), and
  not for code review (code-review:code-review).
---

# Decision panel

The user brings a decision and asks the panel to make it. Four model families read the same
evidence, all four pick an option without seeing the others, a second round settles any split,
and the user gets one page saying what was decided, why, who disagreed and what happens next.

It is deliberately heavier than `clarify:clarify`, which refers a fork to one model on its own
initiative before deciding whether to bother the user. This skill runs only when the user asks
for it, uses all four lanes, and leaves a record. It differs from `feedback-panel:feedback-panel`
in its input: there is no stakeholder feedback to triage, only a decision.

Three findings shape the procedure (`references/evidence.md`). Model families share mistakes,
so evidence in the repo outranks a majority. Judges favour the option they read first, so the
option order is swapped between lanes. Second rounds can talk a model out of a right answer, so
round two runs only on a split, and a change of mind has to cite new evidence.

## Procedure

Work in a directory outside the repo, such as `<scratchpad>/decision-panel/<slug>/` (use
`/tmp/decision-panel/<slug>/` when there is no scratchpad). Pass absolute paths everywhere:
`run_panel.sh` runs each lane from `/tmp`.

### 1. Frame the decision

Write `decision.md`: the question in one sentence; two to four options, lettered A to D, each
with what choosing it means in practice; the constraints, each with its source (the user's own
words quoted, `CLAUDE.md`, a decisions log, a file:line); and the files a lane must read. Take
all of it from the conversation and the repo. When the user named no options, draft them from
the evidence; the panel may still propose a better one.

Before sending anything, check what leaves the machine. The lanes are third-party CLIs on the
user's subscriptions, so send repo paths and the user's own material only. Leave out secrets,
credentials, personal data and any client's confidential material; reference a path instead of
pasting it. If the decision cannot be framed without such material, sanitise it or tell the user
what blocks the panel and stop. Honour an active `OPT-OUT: external-models` instruction.

### 2. Round one

Fill the round-one brief in `references/briefs.md` twice, `brief-r1a.md` with the options in
A-to-D order and `brief-r1b.md` in reverse, then run both into one directory:

```bash
S=<this skill>/scripts
$S/run_panel.sh --brief <wd>/brief-r1a.md --out <wd>/r1 --lanes fable,argon --add-dir <repo> --add-dir <wd> --timeout 900 --min-bytes 600 &
$S/run_panel.sh --brief <wd>/brief-r1b.md --out <wd>/r1 --lanes astra,grok  --add-dir <repo> --add-dir <wd> --timeout 900 --min-bytes 600 &
wait
$S/tally.py <wd>/r1
```

Run them in the background; a round takes up to fifteen minutes. `tally.py` reads each lane's
`VERDICT` line and the model id from its log, and returns `decided`, `decided_split` or
`round_two` (exit 0, 0 or 3).

Read every answer in full before trusting the tally. A lane whose file is empty, answers a
different project, or stops before its last section is a failure: re-run it once, and if it
fails again, report it on the page and continue with the lanes that answered. A failed lane
never counts as a vote or as agreement.

### 3. Round two, on a split only

When the tally says `round_two`, or one lane cites evidence the others did not read, fill the
round-two brief. If that evidence is an outside source, such as a vendor's documentation, fetch
it yourself first and quote the exact sentences in the brief, so the other lanes judge the
source rather than one model's paraphrase of it. In the brief: positions quoted as Reviewer A to D in shuffled order, options in a new order.
Save which reviewer was which model in `r2-mapping.json`, run all four lanes into `<wd>/r2`, and
tally again. A lane that changes its verdict without citing new evidence or a new step of
reasoning keeps its round-one verdict, and the page says so.

### 4. Decide

Settle it in this order:

1. **Evidence.** When a file, a measurement or a source settles the question, it decides,
   whatever the count.
2. **The panel's majority** of valid lanes, with the minority written down as dissent.
3. **A tie that survives round two** is broken by you, on the evidence, and recorded as a
   tie-break with your reasoning, on a page marked "decided, with dissent".

The user delegated the judgement by asking for the panel, so taste, cost and scope calls are
the panel's to make. Return the decision to the user only when the options turn on a fact
about them that is not written anywhere you can reach, such as their available hours, budget or
an employer's permission. Then the page's status is `needs_you`, and you ask that one question
with the question tool, following `clarify:clarify`'s rules for shape and wording.

### 5. Write the page

Write `decision.json` in the shape `scripts/build_decision.py --example` prints, then:

```bash
$S/build_decision.py --check <wd>/decision.json
$S/build_decision.py <wd>/decision.json <repo>/docs/decisions/<YYYY-MM-DD>-<slug>.html
```

`--check` fails on a winning option no valid lane chose without a recorded tie-break, a failed
lane counted as a vote, a split marked unanimous, or a missing next step. Outside a repo, write
the page into the working directory. Copy `decision.md`, `decision.json`, `r1/` and `r2/` into
`docs/decisions/<YYYY-MM-DD>-<slug>-panel/` beside the page, so the record can be audited later.

Write the page's prose through `agent-voice:agent-voice` in its document register. The page
leads with the decision, then why in two to four sentences, then what happens next. Each model
card carries the model id the lane ran, its verdict and a one-line position. Open the page when
it is written.

### 6. Act on it

Carry out the next steps that need no confirmation. For any step that is destructive,
irreversible, outward-facing or costs money, mark it `needs_confirmation` on the page and ask
the user before doing it, with the page link. Reply in three to five lines: the decision and its
tally, the page path, and anything that is waiting on the user.

## Lanes

| Lane | Family | Command (in `scripts/run_panel.sh`) | Resolved 7 Nov 2026 |
|---|---|---|---|
| `fable` | Anthropic | `claude --model fable --effort high -p` | claude-fable-5-1 |
| `astra` | OpenAI | `codex exec -m gpt-6-astra -c model_reasoning_effort="high" -s read-only` | gpt-6-astra (pinned; codex lists no models) |
| `argon` | Google | `agy --new-project --model "$(latest_model.py gemini --effort high)" -p` | gemini-4-argon-high |
| `grok` | xAI | `grok -m "$(latest_model.py grok)" --effort xhigh -p` | grok-4.7 |

Each lane runs the newest model its CLI offers, so a new release needs no edit here: `fable` is
the claude CLI alias, and `scripts/latest_model.py` reads `agy models` and `grok models` and
picks the highest version. Grok runs at `xhigh`, the most its CLI accepts. When the model
running this skill shares a family with a lane, keep the lane and say so on the page. Pin a
model with `FP_<LANE>_MODEL`, for example to repeat a decision on the same versions.

## Scope and cost

One decision per run. Two linked decisions are two runs, and the page for each links
the others. The lanes use the user's subscriptions and cost no metered money; paid research,
such as a Dossier `research_start`, needs the user's go-ahead first. Do not delegate the lanes
or the reconciling to subagents: the CLIs are the panel, and the reconciling is your job.
