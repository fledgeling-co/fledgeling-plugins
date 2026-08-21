# Evals — recover-claude-code

Iteration 1, 2026-08-21. Three cases, each run twice: once by an Opus 5 subagent given the
skill, once by an Opus 5 subagent given the same prompt and no skill. The baseline is
no-skill-at-all, because this skill is new and the question worth answering is whether it
earns its place in a context window.

Graded by `scripts/grade_evals.py` against the assertions in `evals/evals.json`. The grader
is pattern-based so the same grade can be reproduced and compared against a later iteration.

## Result

| | with skill | no skill |
|---|---|---|
| **Total** | **23/23 (100%)** | **20/23 (86%)** |
| 0 · crash with owed work | 10/10 | 10/10 |
| 1 · live session must not be touched | 7/7 | 7/7 |
| 2 · why the last recovery cold-started | 6/6 | **3/6** |

**The whole delta is one eval, and that is the honest headline.** Two of the three cases are
non-discriminating: given a fixture it can read, Opus 5 works out the liveness gate and the
split-project-directory trap on its own. Both baselines found that the workflow script sat
under `-Users-someone-Dev-orderly` while its journal sat under `-Users-someone-Dev`. Both
refused to resume the live session and explained why a quiet session is not a dead one. On
those two cases the skill adds tooling and speed, not judgement.

Where it does earn its place is the third case, which asks *why* a resume cold-started and how
to get an agent's context back. That is not derivable from the fixture — it needs the runtime
internals. The baseline missed all three of:

- that an in-flight agent is the **first cache miss** on resume and re-runs from its original
  prompt with an empty head,
- that the miss is **sticky**, so later calls re-run even when their results are on disk and
  their work is already committed,
- the **promotion** route — copy the sidechain transcript, rewrite `sessionId`, drop
  `isSidechain` and `agentId`, resume it.

It also reached a wrong mechanism confidently. It attributed the cold start to the *transcript*
being in the wrong project directory, so that `--resume` "silently yields a brand-new
session". Resume with an explicit id does not do that; the directory that actually diverges is
the **script's**, and the cold start comes from the journal being owed a result. A plausible,
articulate, wrong diagnosis is the failure mode this skill exists to prevent, and the baseline
produced one.

## What the runs changed about the skill

Every one of these was a defect found by a runner, fixed the same day.

| Found by | Defect | Fix |
|---|---|---|
| eval 2, with skill | `splice_result.py` pointed at a "Relocating a run" section of SKILL.md that did not exist, leaving the last step of the splice path undocumented | Added the section, with the path formula, the move, and why the original is kept |
| eval 0, with skill | The fixture's agent transcripts carried neither `isSidechain` nor `agentId`, so promotion was only exercising the `sessionId` rewrite | Fixture now writes faithful sidechains |
| evals 0 and 1, both configs | The fixture's declared-live pid `424242` exceeds macOS `pid_max`, so `ps -p 424242` errors with "process id too large" instead of returning empty — two runners had to special-case it, and one noted a naive reading would have called the live session dead | Fixture pid is now `42424`, which queries cleanly as absent |
| eval 0 and 2, with skill | Concurrent runners shared one fixture and overwrote each other's promoted transcripts | Known harness limitation; iteration 2 should copy the fixture per runner |

## Mechanical verification, independent of the runs

- `scripts/selftest.py` — 10 assertions against a fixture built in the shapes a real crash
  leaves. All pass. Two of them exist because they were live defects: the script-path lookup
  across project directories, and not calling an agent failed for mentioning a rate limit.
- The scanner was run against the real machine mid-recovery: it classified 21 live sessions
  correctly with their names and pids and reported nothing to recover, which was true — the
  crash had already been recovered by hand. An earlier version of the same code called all 21
  dead, because its anti-pid-recycling guard compared `procStart` to `ps lstart` and those are
  formatted differently and in different time zones.
- `open_tabs.py --dry-run` was inspected end to end: the generated bootstrap and brief are in
  the repository history of this change.
- Every script compiles and is stdlib-only.

## What was not tested

- **No tab was ever opened by a runner.** Every eval ran with `--dry-run`, so the
  accessibility path is verified by direct measurement (tab count 21 → 22 through the File
  menu, text typed and executed) rather than by an eval.
- **The splice path was never run to completion**, because completing it needs an interrupted
  agent finished to a real conclusion. `splice_result.py --list` was exercised; the append was
  not.
- **No real crash was recovered end to end by the skill.** The crash it was built from had
  already been recovered by hand before the skill existed. The next real crash is the test
  that matters, and until then the end-to-end claim is unproven.
- **One eval affordance is asymmetric.** The with-skill prompts told runners to set
  `RCC_FAKE_LIVE_PIDS`, which only exists because the skill's scanner exists; baselines had no
  equivalent and had to establish liveness by hand. That handicapped the baseline on liveness
  confirmation specifically. Both configs still scored 7/7 on eval 1, so it did not change that
  result, but the numbers above are not a clean comparison on that dimension.
- **No blind judge panel was run.** The assertions are structural and checkable, and a panel
  would be judging which of two correct plans reads better, which is not the question.

## Reproducing

```bash
cd plugins/recover-claude-code/skills/recover-claude-code
python3 scripts/selftest.py                              # 10 assertions, exit 0
python3 scripts/grade_evals.py /tmp/rcc-workspace/iteration-1
```

The eval workspace is outside the repository (`/tmp/rcc-workspace`), so it does not survive a
reboot. The assertions, the fixture builder and the grader do, which is what makes iteration 2
comparable to this one.
