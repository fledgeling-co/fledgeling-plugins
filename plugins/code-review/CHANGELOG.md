## 1.4.0 - 2026-11-24

- **CI mode.** A third mode beside `review` and `prepush`, selected when `GITHUB_ACTIONS=true` on a
  pull request event, so the review can run as a job on a self-hosted runner such as egress with a
  frontier model behind it. `references/ci-mode.md` carries the rules: skip drafts, forks, bots and
  commenters without write access; review only the commits since the last review's marker; post one
  `COMMENT` review and one check whose conclusion is `success` or `neutral`, never `failure`; resolve
  only threads this reviewer opened; never post a candidate that Verify did not reach before the
  job's deadline. It never approves, requests changes, edits or pushes.
- **Instruction files come from the base branch** in PR and CI mode (`git show "$BASE:CLAUDE.md"`),
  so a pull request cannot rewrite the rules it is reviewed against. An edit to an instruction file
  inside the diff is reviewed as a finding. Prepush mode still reads the working tree.
- **`REVIEW.md` is read**, from the same source as the other instruction files. Its additions
  (severity definitions, always-check items) apply at every depth. Its subtractions (skipped paths,
  nit caps, dropped classes) apply in PR and CI mode only when changes to the base need a pull
  request, because on an unprotected base anyone with push access could silence the reviewer; every
  subtraction that applies is printed in the coverage ledger.
- **CI mode says when the review may start to block.** The check stays neutral; a team that wants
  to block makes its workflow fail on the verdict line, after two weeks or 20 merged pull requests
  of comparing the review's findings with what reviewers did. A required check is pinned to the app
  that creates it, since any token with status access can post a status of the same name.
- `gemini.md` refreshed: instruction files and `REVIEW.md` read from the base, and `ci` mode's two
  bounds (check never `failure`, review event `COMMENT`) added to the readback table.

## 1.3.1 - 2026-08-30

Every skill name written in a prompt or a cross-reference now carries its full
`plugin:skill` form. A bare name is not resolvable by the Skill tool, so a runner told to
invoke one gets `Unknown skill` and carries on without it.

Measured across 51,763 session transcripts over 21 days: 53 of 77 Skill invocations failed,
a 68% failure rate. Bare names were 27 of those. Four more came from agents that knew a
prefix was needed and invented one (`plugin:`, or the marketplace name).

# code-review changelog

## 1.2.0 - 2026-08-21

- New trigger-fired angle **K, capability withdrawn and the test that keeps it withdrawn**. Fires when
  a diff removes a capability from something that runs (a tool from an agent's permitted set, a
  permission from a role, a command from an allowlist, a syscall from a sandbox profile) or adds an
  assertion that a capability is absent. Angle B could not catch this class: it asks what a deletion
  enforced, and a withdrawn capability enforced nothing, so B finds no invariant and passes while the
  breakage sits downstream with no line to look at.
- The angle asks three things in order: what the thing can no longer do and whether anything still
  needs it done, whether the comment's justification matches the commit's, and whether a test now
  asserts the absence. The last converts a temporary change into a specification, because restoring
  the capability then breaks the suite.
- `evidence.md` records the five measurements behind it, the one place two research members contradict
  each other, and the recorded failure it was built from. Also states what is not measured: nobody has
  shown that reviewing for this shape shortens anything.

