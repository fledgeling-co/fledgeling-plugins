# Gates, and the four ways they lie

Every fact here was measured in the Atlas monorepo. The general shapes are corroborated in
`docs/deep-research/` under exit-code masking and Turborepo caching.

## The commands

```bash
# per app, always with --force
pnpm turbo run lint typecheck test --filter=<app> --concurrency=1 --force

# atlas-app needs BOTH; test:rn is a separate turbo task
pnpm turbo run test:rn --filter=atlas-app --concurrency=1 --force

# the merged tree, which is the gate that decides
pnpm turbo run lint typecheck test test:rn \
  --filter=atlas-app --filter=atlas-api --filter=atlas-admin --filter=atlas-products \
  --concurrency=1 --force
```

Launch a long gate detached and poll it, because an agent is killed after 180 seconds of
silence:

```bash
nohup sh -c 'pnpm turbo run ... > /tmp/gate.log 2>&1; echo "TURBO_EXIT=$?" >> /tmp/gate.log' &
disown
```

A bare `&` inside a single tool call dies with that call, and a `cd` inside a backgrounded
command does not apply, so use absolute paths.

## 1. The pipe reports its own status

`... | tail -5` exits with `tail`'s status. This has already turned a failing gate into a
reported pass in this repo: turbo had failed 10 of 16 tasks and the run was recorded green.
`tail` also buffers until the pipeline closes, which produced an empty log for ten minutes
and an incorrect diagnosis of machine load.

Read the exit code you actually care about. Write it to the log with `echo "TURBO_EXIT=$?"`
and grep for that.

## 2. Turbo replays a stale result

Without `--force`, turbo can replay a cached FAILED after the source is fixed, and a cached
PASSED after it is broken. Two runs in one session reported a stale red; `--force` gave the
true result both times.

## 3. `test` does not include `test:rn`

`atlas-app` carries a Node-env vitest suite as `test` and a jest React Native suite as
`test:rn`. They are separate turbo tasks. A gate filtered to `atlas-app` on `test` alone
runs roughly 660 cases and silently skips roughly 1,250.

## 4. A red gate under load is contention until proven otherwise

`mongodb-memory-server` races for ephemeral ports; the failure reads
`Instance failed to start within 10000ms` and looks like a test failure. Isolate the single
file before believing a red. Equally, a suite that shells out to a package manager can time
out under load and take its whole runner down: one such test made three coverage maps go
missing and 17 files read as untested when 16 were covered.

## The push gate

`.husky/pre-push` runs the full monorepo gate plus `pnpm audit`, which is currently red on
transitive advisories unrelated to any change here.

```bash
SKIP_AUDIT=1 git push origin main                 # the normal case
SKIP_AUDIT=1 SKIP_VERCEL_BUILD=1 git push ...     # from a worktree
git push --no-verify origin --delete <branch>     # a DELETION fires the full gate otherwise
```

Only skip the audit when the diff touches no `package.json` or lockfile. Push every branch
in one command with several refspecs so the gate runs once rather than per branch; it takes
roughly fifteen minutes.
