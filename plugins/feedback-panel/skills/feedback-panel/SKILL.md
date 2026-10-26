---
name: feedback-panel
description: Review a stakeholder's feedback on a project with a panel of model families, decide what to build, what to ask and what to push back on, and hand the feedback author a self-contained HTML report with multiple-choice questions, preselected recommendations, the reasoning inside each question, and a JSON export they send back. Then apply the answers that come back, build the agreed changes, and turn the report into a record of the answers. Use when someone pastes or points at feedback on a website, app, deck, document or design and wants it reviewed, triaged, challenged or turned into questions — "review this feedback", "what do you make of Amy's notes", "have codex and gemini check this too", "turn these comments into questions for her", "push back where it's wrong", "here are her answers, work through them" — even when they never say "panel" or "report". Not for reviewing code diffs (code-review:code-review), a project's own backlog (whats-left:whats-left), or a single fork you need settled (clarify:clarify).
---

# Feedback panel

Feedback from a colleague or client arrives as a list of requests written from one point of
view. Most of it is clear and should be built as written. Some of it depends on a fact only its
author holds, some quietly reverses an earlier decision, and some would weaken the project if
built as written. This skill separates those three, gets independent readings from different
model families so the split is not one model's opinion, and gives the author one page they can
answer in a few minutes.

The deliverable at each stage is a file, not a chat message: the triage, the panel answers, the
report, the build. The author reads the report; you read the files.

## The people

Name two roles before starting, from the conversation or the repo, and ask only if neither
says:

- **The author**: who wrote the feedback and owns the product calls in it (positioning, copy,
  taste, scope).
- **The technical owner**: who knows what the product actually does today (capabilities,
  integrations, data).

Every question in the report is labelled for one of them, or both. A question about what the
product can do goes to the technical owner even when the author raised it.

## Procedure

Work in a directory outside the repo, `/tmp/feedback-panel/<slug>/`, and copy the final report
and panel answers into the repo's `docs/reviews/` at the end. Keep the feedback verbatim in
`feedback.md` there; every later step reads that file rather than a paraphrase.

### 1. Ground every point in the project

Read the feedback in full, then the project: its `CLAUDE.md`, design rules, decisions log,
research and positioning docs, the pages or files each point names, and any team files the
repo points to. Give each point one disposition and a `file:line` citation:

- **Understood**: clear, consistent with recorded decisions, buildable as written.
- **Question**: needs a fact only a person holds, or two readings would produce different work.
- **Push back**: built as written it would contradict a recorded decision, a standard
  (accessibility, legal, a sourced claim), the evidence, or the project as a whole.

Run `shipyard:triage` in concepts-only mode for the readiness frame (no tracker writes, no
code changes). Before any point becomes a question, put it through `clarify:clarify`: most
candidate questions are answered by the repo or have a safe default, and those become
"Understood" with the assumption stated. Write the result to `triage.md` with the questions
numbered most consequential first.

### 2. A second family checks the triage

Send the feedback and `triage.md` to one lane from a different family than yours, read-only,
asking it to do the same triage independently and then list where it disagrees. Record the
disagreements; they are inputs to the panel, not verdicts.

### 3. The panel, two rounds

Run three families at high effort with `scripts/run_panel.sh --min-bytes 1500` and the round-one brief in
`references/panel-briefs.md`. Each lane gets the feedback, the triage and the project paths,
and returns a determination per question and a ruling per push-back (uphold, modify, withdraw)
with evidence. Then run round two with only the points where the lanes split, quoting each
lane's position back to the others in swapped order.

A lane that returns an empty file, an off-topic answer (another project's ids, another
product), or an answer cut off before its last section is a lane failure. Re-run it once with
the fix the log names, or send only the missing sections; if it fails again, report it and
continue with the families you have. Never count a failed lane as agreement.

Reconcile into `decisions.json`: per point, the decision, how each model landed (agrees,
differed, and their one-line position), claims considered and dismissed with who made them,
and the evidence. A two-to-one split is a decision with the dissent recorded; a split you
cannot settle from the files becomes a question.

### 4. Design and UX refinement

When the feedback touches a user-facing surface, run `design-craft:design-craft`,
`ux-craft:ux-craft` and `design-review:design-review` over the decisions that change what a
visitor sees, and revise any decision they overturn. Record the change in that decision's
reasoning ("Design and UX review: …"), because the author will see a different recommendation
from the panel's.

### 5. Build the report

Write the spec and render it:

```bash
python3 scripts/build_report.py --check spec.json
python3 scripts/build_report.py spec.json docs/reviews/<date>-feedback-report.html
```

`references/report-contract.md` is the spec format and the rules the author's corrections
produced; read it before writing the spec. The four that matter most: each question starts on
its recommended or default answer, the reasoning sits inside each question, every question
names who it is for, and nothing in the report is there for you rather than for the author.

Write the copy through the voice skill the project uses for documents (a company or person
content skill when the author reads it as that voice, otherwise `agent-voice:agent-voice` in
its document register). Open the file in a browser and check it at 390px and desktop width.

### 6. Build what needs no answer, then the defaults

When asked to start work, build the "Understood" points first. When asked to continue, build
on the preselected answers, and keep a list of everything that rests on a default so a
different answer can undo it. Ship through the project's own gates and deploy rules.

### 7. Apply the answers

The author's export is JSON with an answer, an `is_default` flag and an optional note per
question. Follow `references/answers-loop.md`: diff each answer against what was built, send
the changed ones (and any new request that came with them) to two families for how to
implement them, build, then rebuild the report.

When the follow-up questions are answered too, switch the report to answers mode: the
questions are replaced by each answer and what it changed, and the push-back stays. When asked
to resolve the "Other things we noticed" items, fix them and mark each one resolved in place.

## Lanes

| Lane | Family | Command (in `scripts/run_panel.sh`) |
|---|---|---|
| `fable` | Anthropic | `claude --model claude-fable-5-1 --effort high -p` |
| `astra` | OpenAI | `codex exec -m gpt-6-astra -c model_reasoning_effort="high" -s read-only` |
| `argon` | Google | `agy --new-project --model gemini-4-argon-high --add-dir <repo> -p` |
| `grok` | xAI | `grok -m grok-4.6 --effort high -p` |

Use the families the user names. When they name none, use three lanes from three families,
none of them the family writing the report if another is available. Model ids change: confirm
each with the CLI's model list before the first run and override with `FP_<LANE>_MODEL`.

## Scope and length

Deliver the stage the user asked for and stop. Reviewing feedback does not include building
it, and building the defaults does not include deploying unless the project's rules or the
user say so. Ask before any deploy, publish, data write outside the repo, or message to the
author.

The report states each question in one heading line, its "why" in two to four sentences, and
each push-back's reason in one to three sentences. The triage is one line per feedback point
plus the numbered questions. Chat replies are three to five lines: what was produced, where it is, and
what needs the user.

Delegate only the lanes and, for a large project, one read-only explorer per independent
surface; do the reconciling and the report yourself. Do not delegate a check you can run in a
few tool calls.
