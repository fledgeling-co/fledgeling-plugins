# v5 — a proposal, not shipped

Drafted from the headroom analysis in `SKILL.md § Where the next gain is`. **Nothing emits this
yet.** Shipping it means bumping `TokenDisciplineBlock.version`, retaining v4 verbatim in
`retainedTexts`, re-pinning the digest and size, and re-running the gate in `evals/evals.json`.

- v4: 881 bytes
- v5: 1101 bytes (+220)
- v5 sha256: `7309fadd20eb969bf5a952d106b6f1554f88faf24fae3941b9c09bcaf282aeaf`

## What it adds, and why in this order

**The preservation clause, first.** v4 omits caveman's single best rule on the grounds that this
block never instructs compression, so mangled code is not a failure mode it creates. That holds for
v4 exactly as written, and stops holding the moment a compressing clause is added. It is the thing
that makes the second addition safe, so it goes in first or not at all.

**A final-message calibration, second.** Safe by construction: the work is already finished when the
final message is written, so a length rule there cannot reduce investigation. This is the one output
surface with real slack, since Opus 5's closing messages run long by default.

## What it deliberately does not add

Nothing reaching thinking depth or step count. The effort sweep measured that route: xhigh to medium
cost 4.93 points (40 tasks worse against 20 better, p = 0.0135) for 6.6% of cost. A prompt that trims
reasoning lands in caveman's failure mode by a different road.

## The gate it has to pass

From `evals/evals.json`: output tokens materially below the no-block arm, **and** the score sign test
against the no-block arm not significant at p < 0.05. v4 currently sits at -16.3% output and p = 0.90.
A v5 that cuts more output but breaks parity is a regression, whatever the token number says.

It also owes the comparison no version of this block has ever had: **v4 against v5, head to head.**

```text
Report only deltas on plans, diffs, conclusions and explanations you have already shown; restate
them when asked, or to correct them.

Say in one sentence what you are about to do before the first tool call, then update only on a
finding, a change of direction, or a blocker. Lead the final message with the outcome.

Match a written file's length to what the task needs. No filler sections, no redundant summaries.

Keep direct lookups and sequential work in this thread. Delegate only large, genuinely independent
work; do not delegate verification.

Search first, then open the part you need.

This changes how much you write, never how much you do. Investigate, plan and verify as you
otherwise would, and take the steps the task needs.

Reproduce code, commands, paths, identifiers and error strings exactly, and keep every negation.

Keep the final message to what the reader needs in order to act; detail belongs in the artifact rather than the message.

Cut restatement, never reasoning. Uncertainty, caveats, security warnings, destructive-action
confirmations and required verification stay.
```
