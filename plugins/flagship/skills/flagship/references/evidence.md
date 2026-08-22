# Evidence

Every rule in this skill traces to something measured on one machine across one evening —
2026-08-22, sixteen concurrent Claude Code sessions over twelve repositories in `~/Dev`. The
skill is a distillation of that run rather than a survey of the field, and it is honest about
which: no external research panel was run, because the corpus that mattered was produced in the
session itself and is reproducible from the transcripts and the repos.

## What sits behind each section

| Section | Source |
|---|---|
| The authority boundary | Ten sessions independently refusing a channel-closure instruction; two refusing a relayed push authorisation; one refusing a self-contradictory notarisation brief; four already in Phase 5 on their own user's instruction |
| The heavy-slot token | `harbourmaster` SKILL.md (load average 830 across 16 cores while a fleet started its eighth runner from a hard-coded 8) intersected with `ship-armada`'s 3-concurrent-projects policy |
| berths ≠ load | Three independent measurements of `in_use 0` with 5, 2 and n Opus runners live; workflow-inner agents never register as claimants |
| Thermal sampling | Two sessions measuring the verdict flip in opposite directions inside 40–60s; the unconfounded reading held load flat at 0.38–0.47 per core across three samples while thermal moved |
| `df -h /` | APFS system volume reporting ~5% used against a data volume at 87% |
| Lane probing | `lane_pick.py` advertising a lane at 16.6% used with no binary on `PATH`; a lane at 84% by meter returning `402`; a lane returning another project's verdict without `--new-project` |
| The split verify stage | The surviving out-of-family lane being a one-shot that cannot execute a suite or walk a diff |
| R1–R5 and the corpus state | `~/Dev/perch/docs/features-for-triage/supervision-decision-rules.md`; `packages/core/src/decision_prior.ts` and `decision_store.ts`; `decision-panel-log.jsonl` (76 records, 68 abstentions); `escalation.sqlite` (0/0) |
| Precedent is global | 35.3% of exact-match recoveries first typed in a different project |
| The 36% override rate | The original 184-question set; not re-measured across the ~714 calls since |
| Absence read as success | Fifteen instrument failures, attributions in `propagation.md` |
| Both zero/members rules | Derived by two sessions, each after being wrong first |
| Gap-fix briefing | One session's rule, one session's refinement, one session's conditional routing after measuring citation density across five verdicts |
| Non-AC findings | One fleet's sixteen-wave admission; one session losing 3 of 5 merges in a day; one losing 1 of 7 with merge-body verdicts limiting the damage |
| The fifth diagnostic channel | A runner death read across four channels where the tool mix (45 Bash calls, no Write/Edit) settled it |
| Ghostty tab mechanics | `recover-claude-code`'s `open_tabs.py` and its SKILL.md |
| `git ls-remote` before a push | 453 commits against an origin URL for a repository that had never been created |

## The honest limits

- **One machine, one operator, one evening.** The rules about *this* portfolio's tooling
  (`reckon`, `capture-lineage`, `defer`) will age as those tools are fixed; several were fixed
  during the evening itself. The rules about authority, about absence read as success, and about
  reading a machine honestly are the ones expected to hold.
- **The decision corpus is thinner than the policy.** R1–R5 is written and its feature is
  `Status: Not started`. Treat the router as policy and the store as aspiration until the
  corpus is populated.
- **No comparative eval was run.** See `EVALS.md`, which says so rather than omitting it.
