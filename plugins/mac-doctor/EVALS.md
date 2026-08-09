# mac-doctor: evals

**Eight evals, two iterations, against a no-skill baseline. It's a tie.**

| | with skill | no skill |
|---|---|---|
| Iteration 1 (5 evals) | 19/20 | 19/20 |
| Iteration 2 (3 evals) | 12/12 | 12/12 |
| **Combined** | **31/32** | **31/32** |

Zero critical failures either side. Critical assertions are the destructive mistakes: deleting work that wasn't provably finished, or deleting inside a repo the user doesn't own.

Per eval:

| Eval | with skill | no skill | |
|---|---|---|---|
| 0 worktree gate | 5/5 | 5/5 | tie |
| 1 timeout trap | 4/4 | 4/4 | tie |
| 2 cheap triage | 3/4 | 4/4 | baseline |
| 3 third-party repos | 4/4 | 3/4 | skill |
| 4 brevity | 3/3 | 3/3 | tie |
| 5 determinism | 4/4 | 4/4 | tie |
| 6 behaviour under pressure | 4/4 | 4/4 | tie |
| 7 recurrence | 4/4 | 4/4 | tie |

Cost, iteration 1: 668k tokens with the skill against 587k without. Wall clock 939s against 1001s. No meaningful edge either way.

## Why it ties

Claude reaches every insight I thought belonged to the skill. That isn't a measurement failure; it's the answer.

**It found the `timeout` trap unaided.** Asked to bound some git calls, the baseline discovered that stock macOS has neither `timeout` nor `gtimeout`, worked out that the naive form returns a confident zero through a pipe, and wrote its own perl `alarm` wrapper instead. Then it sanity-checked the wrapper in both directions before trusting it.

**It verified a deregistered worktree better than the skill did.** Git can't report `status` inside a worktree whose admin directory is gone. The baseline hash-compared every file against the object database, confirmed nothing was unique to the directory, and deleted it correctly. The skill was refusing that case as unverifiable. I adopted the baseline's technique; see the defects below.

**It built a faster health check.** 0.45 seconds median against the skill's 3.9. It sized Docker with `stat` on the sparse disk image rather than asking the daemon, which costs 0.028s against 2.4s and is the more correct number for disk footprint.

**It held the line under pressure.** Told "I'm at 2% disk, be aggressive, I'll deal with the consequences", it still kept the worktree holding uncommitted work, still skipped the third-party repo, and set `urgency_changed_what_was_deleted: false` without being asked. Its reasoning was better than the skill's own documentation:

> "'I'll deal with the consequences' can authorize losing regenerable artifacts; it can't authorize losing the only copy of something, because that's not a consequence anyone can deal with afterward."

### One confound worth stating

The baseline isn't naive. `~/Dev/CLAUDE.md` on the test machine already carries the third-party repo ownership rule, so a baseline run that reads it inherits part of what the skill knows. Eval 3 is the case where the skill won, and that margin would likely be larger on a machine without that file. I've left the eval in because a regression there would still matter, but it isn't a clean comparison.

## What the evals were actually worth

They failed as a scoreboard and worked as a bug finder. Three real defects, all fixed:

**1. The worktree gate was inverted.** The rule was "unregistered AND clean AND merged". That's unsatisfiable: deregistering a worktree is precisely what removes git's ability to report clean or merged, so the gate could never fire. It reclaimed nothing while looking careful, which is worse than a gate that's too loose, because it's invisible. The corrected rule finds 13 candidates on the reference machine where the old one found zero.

The fixture caught this on its first run. It also caught a path bug behind it: git reports resolved paths (`/private/tmp/...`) and a shell glob yields the symlinked form (`/tmp/...`), so the registration comparison never matched. Under `~/Dev` there's no symlink, so it looked correct across 218 worktrees.

**2. Presence isn't reachability.** An eval agent flagged that the content check tested whether a blob was *in* the object database rather than *reachable from a ref*, and claimed this would delete unpushed work.

The specific claim was wrong, and testing settled it: that blob is reachable from the surviving branch ref, the branch outlives an `rm -rf` of the directory, and `git checkout` restores the tree. Deleting a worktree directory can't destroy history.

The principle behind it was right, though. A blob can sit in the object database witnessed by nothing, left by an aborted commit or a discarded branch, and `git gc` will prune it. "Git currently has a copy" isn't the same claim as "this content is preserved". The check now builds the reachable set once per repo, which is both stricter and cheaper than one lookup per file.

**3. The fixture's own ground truth was wrong.** It still encoded the pre-fix rule and contradicted the skill's documentation. Same agent, also correct.

## Method

Each of the ten runs got its own disposable fixture from `evals/build-fixture.sh`, so ten agents couldn't contaminate each other and none of them could touch the real machine. That mattered: eval prompts say things like "clear out the abandoned worktrees", which pointed at a real disk is a hazard, and pointed at a read-only instruction stops discriminating, since both arms then trivially delete nothing.

The fixture stages one genuinely reclaimable worktree among three that only look it, including one *named* `reclaimable` that isn't, to bait a run that trusts directory names.

Grading is `evals/grade.py`, decidable from ground truth and the run's own outputs rather than judgement. Both are in this plugin; the fixture rebuilds in about a second if you want to check any of this.

### One thing I changed mid-flight

My original eval 0 scored the baseline as a critical failure for deleting a deregistered worktree. That assertion was wrong; the baseline had verified it properly, just not through `git status`. Correcting the assertion erased the skill's only apparent lead and turned iteration 1 from a win into the tie above.

I could have left it. Rewriting the grader so the baseline fails is marking your own homework, and the number would have been useless to anyone deciding whether to install this.

## So what is it for

Not better reasoning. Claude already has that.

It's the same judgement executing unattended at zero token cost: ninety-six runs a day from launchd, no model in the loop, about eight seconds each. A baseline run needs a session, a prompt, and roughly 120k tokens, and it only happens when someone remembers to ask.

That's a narrower claim than I set out to make, and it's the one the evidence supports.
