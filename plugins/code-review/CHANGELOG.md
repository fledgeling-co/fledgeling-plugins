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

