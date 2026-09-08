---
name: atlas-review
description: >-
  Atlas/Bella review conductor. Takes the open PRs from arrival to reviewed, fixed, merged, pushed and reported. Use when someone wants the Atlas pull requests dealt with: "review the open PRs", "land Elysee's stack", "go through the PRs and merge them", "the CEO has pushed some work", "review and merge what's open". Runs code-review:code-review on each PR and then FIXES what it finds, because that skill reports and applies nothing; rebases onto main rather than merge-committing; pulls so local main is the real main; then does the three stages a PR stack always needs and nobody asks for (extending the tests to cover what the PRs added, doing the backend wiring the product owner deliberately left, and acting on the notes they sent with it), then iterates on unit and automated UI tests until they actually pass. Gates the MERGED tree rather than the branches, because 20-35% of clean textual merges carry a semantic conflict no branch-isolated check can see. Treats a test touched by the diff as unproven until an injected mutant makes it fail, because 75% of compiling LLM-written tests are vacuous and static reading scores Low on exactly the shapes that matter. Writes every PR comment and the CEO-facing report through create-luke-content:create-luke-content, and publishes a branded single-column HTML page a non-technical reader can finish. NOT for cutting a release (use atlas-publish:atlas-publish), NOT for a repo's whole backlog (use ship-fleet:ship-fleet), and NOT for reviewing one diff in isolation (use code-review:code-review directly).
allowed-tools: Read, Grep, Glob, Bash, Agent, Write, Edit, AskUserQuestion
---

# atlas-review, the Atlas review conductor

You take the open pull requests on the Atlas/Bella monorepo and drive them to **merged,
pushed, and reported**. The reporting half is not decoration: the person who opened these
PRs is a non-technical product owner, and a merge they cannot read about is a merge they
have to take on trust.

The sibling of `atlas-publish`, which starts where you finish. That skill's boundary is
"draft is where automation stops" because publishing reaches phones. Yours is different:
merging and pushing to `main` is recoverable, so you finish the job. What you do **not** do
is release.

**Running as a Gemini model?** Read `gemini.md` in this directory first, then follow this
file with the overrides it names. Other models skip it.

## The loop, in the product owner's own words

Nine stages. Stages 6 to 8 are the ones nobody asks for and every stack needs.

```
1 review the open PRs          → code-review:code-review, per PR
2 resolve what it found        → YOURS. code-review reports and fixes nothing
3 commit and push
4 merge to main by REBASE      → not a merge commit
5 pull                         → local main is now the real main
6 update the tests             → cover what the PRs actually added
7 do the backend work          → plus whatever the owner's notes ask for
8 test and iterate until green → unit AND automated UI, not one or the other
9 commit and push
```

Stage 2 exists because `code-review` is read-only by design. Stage 6 exists because a PR
that adds four screens adds no coverage for them. Stage 7 exists because the product owner
writes the UI and says so: *"I tried not to touch anything backend/API wise and will leave
that to you."* Their notes arrive as prose, not tickets, and they are a work item.

## The one rule that changes what you trust

**A test the diff touched is unproven until an injected fault makes it fail.**

Not a style preference. Meta's TestGen-LLM deployment filtered **75% of compiling
LLM-written tests as vacuous**, and 30-54% of generated tests carry structural smells.
Worse for you: static reading is measured **Low** at catching exactly the two shapes that
dominate: a mock that swallows the attribute under test, and a guard over a collection
that is empty. An LLM reading a test treats a mock as a valid fixture.

So reading a test tells you nothing about whether it can fail. Breaking the line it covers
and watching it go red is the only evidence, and it is cheap.

Eighteen such checks were found in one Atlas session and **not one was found by running
the tests**. The shapes to expect are in `references/void-checks.md`; the worst was a guard
written so "a new navigator cannot be missed" that filtered the population down to
navigators which already declared the anchor, so a missing one was excluded by the check
itself.

## Gate the merged tree, not the branches

Four green branches do not make a green merge. **20-35% of clean textual merges introduce a
semantic conflict** that branch-isolated CI cannot see, and two fired in one Atlas session:
a campaign row reading `fail` while its registry twin read `pass`, and eighteen stale
production-write declarations after three branches each rewrote the same two files.

Both only exist once the records sit in one tree. So the gate that decides is the one you
run **after** merging, and a branch's own green is a precondition rather than a verdict.

## Reading a gate, and the four ways it lies

Every one measured in this repo. `references/gates.md` carries the full set with commands.

- **Read turbo's own exit code.** Piping a gate through `tail` or `grep` reports *that
  tool's* status and has already turned a failure into a pass here. `tail` also buffers
  until the pipeline closes, so the log looks empty for ten minutes.
- **`--force`, always.** Turbo replays a stale FAILED from cache after the source is fixed.
- **`test:rn` is a separate turbo task from `test`.** Filtering `atlas-app` on `test` runs
  vitest and no jest, so the RN suite is silently absent.
- **A red gate under load is contention until proven otherwise.** `mongodb-memory-server`
  races for ephemeral ports; isolate the file before believing it.

## Where the operator comes in, and where they do not

Route everything through `clarify:clarify` first, then `AskUserQuestion`. What genuinely
reached the owner in a full Atlas session was four things, all taste, cost, scope or risk:
keeping a native component versus reaching five surfaces for screen-reader users; archiving
949 live listings; dropping a flow from the release gate; which of two contradicting
specifications was right.

What did **not** need them, and was asked anyway, was a credential documented in two files
in the repo. Sweep the repo and this conversation before composing a question. That failure
costs more than the question saves, because it tells the reader you did not look.

## Stage detail

Each stage has a reference; read it when you reach that stage, not up front.

| Stage | Reference | The thing that goes wrong |
|---|---|---|
| 1-2 review and fix | `references/review-and-fix.md` | Raw LLM review runs 40-70% false positives; verify before acting |
| 3-5 land it | `references/landing.md` | `git checkout --` and `git add -A` have each destroyed work here |
| 6 tests | `references/void-checks.md` | A number is not evidence; a killed mutant is |
| 7 backend and notes | `references/owner-notes.md` | The notes are a work item, not context |
| 8 iterate | `references/e2e-rig.md` | A device verdict can belong to another branch entirely |
| 9 report | `references/report.md` | The reader does not read code |

## Verify out of family before you act on a finding

Raw LLM review produces **40-70% false positives**, and **cross-model verification cuts
errors by up to half**. Both numbers are in `docs/deep-research/`. So a finding that would
change production code gets a second reading from a different model family before you
change anything. `clarify`'s lanes carry the commands, and the cheap one is a gateway call
rather than a paid CLI.

In one Atlas session an out-of-family lane refuted a reading its own author was confident
in, and was right. Treat a lane that disagrees as the more interesting result.

## What this skill will not do

- **It will not release.** No TestFlight build, no OTA bundle, no version bump for a store
  submission. That is `atlas-publish`, and its own boundary sits at draft.
- **It will not work the backlog.** Briefs, campaign items and the rest of the repo's
  remaining work belong to `ship-fleet:ship-fleet`. You finish when the open PRs are landed
  and reported.
- **It will not weaken a check to make it pass.** A test is never edited to go green, a
  waiver always carries a reason a reviewer could argue with, and a flow that cannot observe
  its own subject is not a passing flow.
- **It will not report a verdict it did not measure.** "Still passing" and "passed once,
  weeks ago" are different claims and the record says which.

## Compose, do not reimplement

| For | Call |
|---|---|
| The review itself | `code-review:code-review` |
| Every written word: PR comments, report prose, commit messages | `create-luke-content:create-luke-content` |
| The report's figures | `visualization:visualization` |
| The report's layout | `design-craft` + `ux-craft` |
| The status page and portfolio row | `status-update:status-update` |
| Asking the owner anything | `clarify:clarify` |
| How many runners this Mac can carry | `harbourmaster` |
| A fan-out that lost agents | `workflow-resume:workflow-resume` |

`create-luke-content` is not optional and not cosmetic. Its `voice_lint.py` is a gate, an em
dash is a hard failure, and prose that skips it reads as generic and gets rewritten. Run it
on the PR comment, the report and the commit message.

## Evidence

`references/evidence.md` carries the citations. The research corpus is in
`docs/deep-research/` so every claim above stays auditable from inside the repo, and the
Atlas-specific measurements are attributed to the session that made them rather than
presented as general truths.
