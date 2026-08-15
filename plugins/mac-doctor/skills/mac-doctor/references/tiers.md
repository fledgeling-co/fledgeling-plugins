# Tiers

Each tier includes everything the shorter tiers do. Sizes quoted are what was
measured on the machine this skill was built for (2026-08-09, 94% full) — they
are there to show which targets are worth the risk, not as expectations.

## Thresholds

Free space on `/System/Volumes/Data` drives urgency:

| Free | State | Behaviour |
| --- | --- | --- |
| > 15% | healthy | tiers run on schedule |
| 5–15% | tight | pull the 12h/1d tiers forward; surface pending 7d proposals |
| 2–5% | low | run every tier now; lead every report with the pending proposals |
| < 2% | critical | as above, plus name the single largest reclaimable item and its gate |

Urgency changes *when* tiers run, never *what* they may delete unprompted. A
machine at 2% is where a wrong deletion is least recoverable.

Read free space from `df -k /System/Volumes/Data`. Note that APFS reports
"Container Free Space" larger than `df` avail — the difference is purgeable
space the OS will reclaim under pressure. Report `df` avail as the real number;
quoting the container figure overstates what is available.

## 15m — pulse

Cheap, silent, no judgement calls. Should complete in seconds.

- Orphan process families passing the gate in `processes.md`. Families, not
  PIDs — 167 leaked MCP servers is one finding with a count. Implemented in
  `scripts/runaway.sh`, which never signals on first sight: a process must be
  seen runaway on three separate runs spanning at least half an hour, because
  one sample cannot tell a spin loop from a build. Idle orphan families are
  reported and never killed; only sustained CPU and leaked automation browser
  trees are reaped unattended.
- Exited Docker containers (`docker container prune -f`), only ones in `exited`
  or `created` state.
- Exited Apple `container` containers (`container prune`, which removes all
  stopped ones). This is a **second engine, not a synonym for Docker** — it has
  its own store under `~/Library/Application Support/com.apple.container`,
  measured at **94 GB** on the reference machine while `docker system df`
  reported the disk as healthy. Check `command -v container` first; the CLI
  ships at `/usr/local/bin/container` and is absent on most machines.
- Leaked automation browser trees: a Playwright/Puppeteer driver whose parent is
  gone and which holds no established connections, killed as a whole tree
  (server → browser → renderers), SIGTERM then SIGKILL. Chromium ignores
  SIGTERM; that escalation is normal.
- Temp dirs from finished runs: `/tmp/playwright-*`, `/tmp/.org.chromium.*`,
  `$TMPDIR/claude-*` older than 24h with no live owner.
- Emit a threshold alert if free space crossed a band since the last run.

## 1h — sweep

Adds build output, which is regenerable by definition.

- `dist/`, `build/`, `.next/`, `.turbo/`, `.parcel-cache/`, `target/` under
  `~/Dev` where the repo has had no file modified in 7 days and no live process
  has it as a cwd. Confirm the repo has a build script before treating its
  output as regenerable.
- `.pytest_cache/`, `__pycache__/`, `.ruff_cache/`, `.mypy_cache/`.
- Xcode DerivedData for projects whose source has not been touched in 14 days.
  Measured at 43G total. Per-project, never the whole directory — wiping it all
  costs a full rebuild of everything.

## 12h — prune

Adds shared caches. Dry-run first, report the total, then execute.

- Package managers: `npm cache clean --force` (9.4G), `pnpm store prune` (8.5G),
  `bun pm cache rm` (1.4G), `yarn cache clean`, `uv cache prune`. These are
  network-refillable; the cost of being wrong is a slower next install.
- `docker image prune -f` (dangling only, ~3.7G reclaimable) and
  `docker builder prune -f`. Not `-a` — that removes images nothing is running
  right now, which includes everything you will run tomorrow.
- `container image prune` for the Apple engine, and `container image ls` to
  report old tags separately. Its store grows the same way Docker's does and
  nothing else on the machine reports it: a 94 GB store came down to 54 GB on
  stopped containers and old tags alone. Size it by measuring
  `~/Library/Application Support/com.apple.container` directly — the CLI has no
  `system df` equivalent, so a total is otherwise invisible.
- Tool caches under `~/Library/Caches` with a known owner and refill path:
  `ms-playwright`, `typescript`, `go-build`, `pip`, `deno`, `electron`,
  `org.swift.swiftpm`. CocoaPods (13G, the largest single cache) refills slowly
  over a metered network — propose it at 7d rather than pruning it here.
- Rotate `~/.claude/shell-snapshots` and `~/.claude/paste-cache` beyond 7 days.

## 1d — deep

Adds things that are unreferenced but not free to rebuild.

- `docker volume prune -f` — unused volumes only (~6.8G of 33.1G; 83 volumes
  with 30 active). A named volume holding a dev database is unused whenever its
  container is down, so check `~/.claude/mac-doctor/protected` first and report
  named volumes separately from anonymous ones.
- `xcrun simctl delete unavailable` — devices whose runtime is gone.
- Agent-CLI state rotation: `~/.claude/file-history` (401M),
  `~/.claude/security` (349M), and the equivalents under `~/.codex` (5.6G),
  `~/.cursor` (3.3G), `~/.grok`, `~/.gemini`. Rotate by age, keep the newest.
- `brew cleanup --prune=7`.
- Report the worktree audit so the 7d proposal is already costed.

## 7d — audit

Proposes, never acts. Present with `AskUserQuestion`, grouped by target with
sizes and a recommendation.

- **Worktrees.** Measured on the reference machine: 217 directories across 15
  repos totalling **620 GB** — about 36% of everything on the disk, and the
  largest single consumer by a wide margin. Almost none is reclaimable: every
  one was registered and clean, so the gate returned zero candidates. Two roots
  dominate (dAIolog 304 GB, anvil 239 GB). Surface them as a **review** item
  ("217 live worktrees, 620 GB, biggest two repos are 88% of it") rather than a
  deletion proposal. The user decides which sessions are finished; the skill
  does not guess.
- **node_modules in dormant repos** — 264 directories under ~/Dev; offer those
  in repos untouched for 30+ days, with the reinstall command.
- **Old simulator runtimes** (19G in CoreSimulator) — list by iOS version so the
  user keeps the ones they test against.
- **Session transcripts** — 13G across 23,214 `.jsonl` files. Offer archival of
  transcripts older than 90 days to a compressed tarball, not deletion; they are
  the record this skill mined its own evidence from.
- **CocoaPods cache** (13G) and other slow-refill caches.
- **Docker.raw compaction** — the sparse file was 56G against 44G of real data.
  Reclaiming needs the Docker VM stopped, so it is a proposal with a procedure,
  never an action.

## When a tier finds nothing

Say so in one line and stop. A frequent tier that is usually boring is working
correctly, and padding the report trains the reader to skim past the run that
actually mattered.
