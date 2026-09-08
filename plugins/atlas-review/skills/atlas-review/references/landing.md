# Stages 3 to 5: commit, push, rebase, pull

## The shape

```bash
gh pr merge <n> --rebase --delete-branch     # rebase, not a merge commit
git pull --ff-only origin main               # local main becomes the real main
```

Rebase keeps the history linear, which matters on a stack where each PR was branched from
the one before. Merge each PR in stack order and confirm each landed before starting the
next: two simultaneous merges into one integration branch is how a stack corrupts.

`gh pr merge --delete-branch` closes any PR whose base was the branch just deleted. On a
stack that is usually what you want, but it happened unexpectedly once and closed a PR
nobody had reviewed.

## Three commands that have destroyed work here

- **`git checkout -- <file>`** reverts to HEAD, not to the working copy. It has wiped an
  agent's uncommitted implementation three times in this repo. Use `cp` backups.
- **`git add -A` during a conflict** committed conflict markers to `main` twice. Stage the
  files you resolved, by name.
- **`pkill -f <pattern>`** matches across roughly nineteen concurrent sessions that share
  command strings. Scope by working directory: `lsof -a -p <pid> -d cwd -Fn`, and kill by
  exact pid.

## Conflicts: compose, do not pick

In one session, **five of five conflicts had two true sides**. The right move each time was
composing both, not choosing one:

- Two branches each asserted something different about the same flow; both assertions were
  wanted and one was required by a guard.
- A CI script needed an option from one branch and a fix from the other; dropping either
  reintroduced a defect that had already been found once.
- Two records disagreed on a count. Neither was right for the merged tree, so the count was
  **derived from the data file** rather than chosen.

That last one generalises. Where a conflict is over a number that some file already
determines, compute it rather than picking a side.

One warning from experience: a conflict resolution is not the place to improve the code.
Changing a string while resolving one broke a test and the change was wrong anyway.

## Worktree hygiene

Remove a worktree in the same turn its branch merges, from the main checkout, after three
checks: the tree is clean, the branch is merged, and no process is running in it. A worktree
you cannot prove is finished is one to ask about.

```bash
git -C <main> worktree remove <path>   # the verb; rm -rf leaves a registered ghost
git -C <main> branch -d ai/<slug>      # -d refuses if unmerged
```

Held worktrees are legitimate: one holding a running packager that an installed app is bound
to should stay, and the reason belongs in the report.
