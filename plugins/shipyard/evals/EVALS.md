# Does shipyard actually work? The evals, in full

The short version: on a like-for-like comparison against the skills it replaces, shipyard passed **37 of 37** structural checks where the originals passed **22 of 37**, and a blind panel of three model families preferred its outputs **17 votes to 4**. One eval lost its first blind round, the loss produced three new rules in the skills, and the re-judged pair flipped. Those numbers cover nine evals; a tenth was written afterwards for the 0.3.0 evidence-integrity rules and has not been run, which a section below states rather than folding into the total. The longer version includes the parts that didn't go smoothly, because a scorecard that only shows wins convinces nobody.

## How the comparison was run

Both arms ran the same prompts on the same fixture repo (a small notes app with a feature brief) using the same model (`claude-sonnet-5`), the same tool whitelist (no git, no network), and fresh fixture copies so neither arm could see the other's edits. The "old" arm is a snapshot of the predecessor skills at their final versions (feature-spec-pipeline 1.10.0 and diolog-tasks-pipeline 2.4.0 lineage), committed in `evals/baseline/` so the comparison stays reproducible.

Note: the skills are written for Opus-class runners; the evals ran on Sonnet for cost. Same model both arms, so the comparison is the skills, not the model.

## The report card (structural assertions)

An independent grader agent marked every assertion passed or failed with quoted evidence. It never saw the skills, only the eval definitions and the outputs.

| Eval | shipyard | originals |
|---|---|---|
| triage-assumption-protocol | 5/5 | 4/5 |
| plan-test-strategy | 5/5 | 2/5 |
| verify-failure-and-family | 5/5 | 3/5 |
| conductor-design-gates | 5/5 | 4/5 |
| intake-idea-expansion | 5/5 | 2/5 |
| status-machine-complete | 4/4 | 2/4 |
| evidence-rules-guard | 4/4 | 2/4 |
| adv-triage-rendered-claim | 2/2 | 1/2 |
| adv-plan-already-true-ac | 2/2 | 2/2 |
| **Total** | **37/37** | **22/37** |

Every failure on the old arm was a genuine absence rather than a wording quibble: no named test seams, no state matrix, no committed plan with a checkable sha, no record of which model family verified, no failure state after review, no intake stage at all, no AI-proposed briefs, no platforms line.

**The grader pushed back, and that's in the record too.** Its first pass flagged four assertions as vacuous, meaning they couldn't have failed on either arm's output. Two got adversarial follow-up evals written to force them (the `adv-` rows above); one of those now bites, and one still doesn't discriminate because the task prompt itself hints at the trap. It also flagged one old-arm failure as a close call that a charitable reading would flip, and caught the old plan arm labelling a source read as "MEASURED", which neither assertion punished. All of it is preserved verbatim in `evals/records/` (the grading files, the panel verdicts, and the un-blinding keys are committed; only the bulky raw run outputs are git-ignored).

## One eval defined after the run, and not scored

`verify-evidence-integrity` was added to `evals/evals.json` on 2026-08-20 and **has not been
run on either arm**. It is not in the 37/37 above, it is not in the panel below, and the
totals in this file are unchanged by it. Saying so matters more than usual here, because the
row it covers is exactly the shape that makes an unrun eval look run.

It exists because 0.3.0 added three rules to `verify` that the nine scored evals could not
have exercised: that a screenshot asserts a subject as well as a capture, that a green suite
can be green because an assertion cannot fail, and that a verdict row citing the verifier's
summary of an artifact is not citing the artifact. The eval hands the verifier a completion
record where every requirement looks closed (a screenshot for the visual row, a passing spec
for the behavioural one) and where the screenshot shares a sha256 with another requirement's,
the capture log records the browser finishing at `/login` rather than `/billing`, and the
spec's body is `await page.click(...)` followed by a bare `expect(page)`.

The old arm will fail most of its nine assertions, and that is not the interesting part. The
interesting part is whether the new arm reaches the right verdict *from the bundle* rather
than from noticing that the fixture looks like a trap, which is the same weakness the grader
already found in `adv-plan-already-true-ac`, where the task prompt hints at what it is
testing. Until it runs, treat this eval as a written intention.

## The blind taste test (panel of model families)

For each eval, both outputs became Option A and Option B in seeded-random order. Judges saw only the pair and a reader-interest question; never the skills, never which side was the baseline. Verdicts by family:

| Judge family | Harness | For shipyard | For originals |
|---|---|---|---|
| Claude | claude CLI | 5 | 2 |
| xAI (grok-4.6) | grok CLI | 5 | 2 |
| Gemini | agy CLI | 7 | 0 |
| GPT | codex CLI | seat empty (see below) | |

**Overall: 17 to 4.** The Claude judge was jointly the least favourable of the three that ran; given Claude wrote these skills, a house bias would have shown the opposite pattern.

**The fourth seat is empty and here's why.** The codex judge failed twice, honestly: the first attempt inherited a config default that burned its deadline before emitting a verdict, and the fixed invocation then hit the account's usage limit (locked until 20 August). The cursor seat was also usage-limited, so the Gemini family took it via the agy CLI. Per the operating rules, a rate-limited judge gets reported and substituted, not retried into the ground; no GPT-family verdicts exist in this panel and the tally says so.

## The loss, the fixes, and the flip

The triage eval lost its first blind round 1-2. The judges' reasons were specific and fair: the rebuilt triage had buried its shakiest call (who can manage a shared folder, a permissions decision) inside a twelve-item assumption list, behind gate accounting a product owner shouldn't have to read, while the baseline asked two clean questions with a copy-paste reply.

That became rules the same day: access-control and sharing-scope defaults are presumptively essential rather than assumable, and never buried mid-list; gate accounting leaves the owner-facing section entirely.

The re-judged pair (fresh random order, same judges) went 1-2 again, with the Claude judge flipping to shipyard on exactly the fixed axis and the Gemini judge flipping the other way on presentation clutter. Round three added the last two rules (the owner review and the pipeline record are separate artifacts; a question your own recommendation already settles is an assumption, not a question) and the third blind round went **2-1 to shipyard**, grok and agy both flipping.

The remaining dissent is worth keeping: the Claude judge now prefers the version that asks the access questions; grok and agy prefer the version that records decided assumptions and stays unblocked. That's the ask-versus-assume tension from the research literature showing up inside the panel itself, and it's a real trade-off, not a defect. Iteration stopped at three rounds, because past that, changes stop generalising and start fitting one case.

## What this cost, and what it can't tell you

The deep-research panel behind the design decisions cost about **$9.70** across four API backends (every citation machine-checked; zero fabricated of 99). The eval and judge runs spent subscription CLI quota, not API dollars.

Caveats, stated rather than buried: every cell is a single run, so sampling noise is real. The judges are models standing in for the people who'd actually use these outputs. The harness asks skills to narrate what they would run when a tool is missing, which cost the rebuilt verifier one judge's vote for describing ceremony it hadn't executed; that's now a rule in the verify skill, but the punishment was partly harness-induced. The graded records and un-blinding keys are committed under `evals/records/`; the raw run outputs are git-ignored for size, so to regenerate them: `bash evals/run_evals.sh` then `bash evals/run_blind_panel.sh <runs-dir>`.
