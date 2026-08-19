# Eval 9 — run of 2026-08-20

The raw material behind the table in `plugins/mockup-fidelity/EVALS.md`. Kept so the 9-against-2
result can be checked rather than taken on trust.

| File | What it is |
| --- | --- |
| `task.txt` | The prompt both arms received, identical on both sides |
| `arm-with-skill.md` | The answer from the arm given SKILL.md, `native-lane.md` and `engine-capability-matrix.md` (62,150 bytes of context) |
| `arm-baseline.md` | The answer from the arm given the task alone (712 bytes) |
| `grading.md` | The grader's per-assertion marks with the quoted sentence deciding each one |

Both arms were `claude-fable-5` at `--effort high`, run from `/tmp/mfeval` with no path into this
repository, so neither could read `fixtures/mac-settings/ANSWER-KEY.md` or the `Divergence` table
in `main.swift`. The grader was `gemini-3.7-flash-high`, given the answer key and both answers
unlabelled as to which was which.

Two things this run does not establish. The prompt is the written-answer form, because a headless
`claude -p` has no proctor MCP tools — so no arm drove the fixture, and assertion 6 was unreachable
for both. And `claude -p` loads the operator's global `CLAUDE.md`, so the baseline arm is not a
clean room; it quotes measured Obscura notes it was never handed here.
