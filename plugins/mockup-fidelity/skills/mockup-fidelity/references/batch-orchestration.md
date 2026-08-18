# Batch orchestration — sequential Workflow fan-out for large, serial-resource audits

Phase 6 of `SKILL.md` fans out one sub-agent per screen with the `Agent` tool, capped at ≈5 waves. That is right for a handful of screens on a web target where rendering is parallelisable. It is the **wrong** shape for two situations that recur:

- **A large inventory** — 30, 50, 66 mock frames — where you want *one fresh agent per frame, with no context bleed* (each re-reads the skill and owns one surface end-to-end: audit → fix → verify → commit), and you want the run to survive your own context compaction.
- **A React Native target**, where the simulator is a **serial resource** — exactly one screen can be navigated/screenshotted/measured at a time. Parallel agents would fight over the sim, the Metro connection, and the single `_latest.json` the harness POSTs. (`SKILL.md` Phase 6 already flags this; this doc is how you honour it at scale.)

The tool that fits both is **`Workflow` with a strictly sequential `for … await agent()` loop** — never `parallel()`/`pipeline()` across frames. The workflow runs in the background, awaits one agent at a time, survives compaction, and is **resumable** (cached completed agents on `resumeFromRunId`). This doc is the hard-won context for making that actually run — every item below is a trap that produced a silent no-op or a broken commit in a real run.

> This is an *orchestration* pattern, not a new audit method. Every agent still does the full `SKILL.md` method on its one frame — measure, never eyeball; mock wins; breadth (present/divergent/**absent** + app-extra) before depth; differ to zero unexplained. The orchestrator's only jobs are: serialise the sim, protect the harness from commits, checkpoint health, and keep the inventory current.

---

## The invariants (break one and the run silently fails)

### 1. `args` may arrive as a JSON *string* — parse defensively or the run is a silent no-op
The `Workflow` tool's `args` is supposed to reach the script as a parsed JSON value, but it can arrive **stringified**. If your script does `const FRAMES = Array.isArray(args) ? args : []`, a stringified array fails the `isArray` check, `FRAMES` is `[]`, and the workflow returns instantly (≈4 ms, 0 agents) having done **nothing** — and that looks like success. Always parse defensively and log what you got:

```js
let raw = args
if (typeof raw === 'string') { try { raw = JSON.parse(raw) } catch (e) { raw = [] } }
const FRAMES = Array.isArray(raw) ? raw : (raw && Array.isArray(raw.frames) ? raw.frames : [])
log(`args typeof=${typeof args}; resolved ${FRAMES.length} frame(s)`)   // diagnoses the no-op instantly
if (!FRAMES.length) { log('No frames passed in args — nothing to do.'); return [] }
```

### 2. Workflow scripts have NO filesystem/Node access — the frame list MUST come through `args`
You cannot `readFileSync` a batch list, an inventory, or a config inside the script. Everything the script branches on comes through `args` (and the few globals: `log`, `agent`, `parallel`, `pipeline`, `budget`, `workflow`). So invariant #1 isn't optional polish — `args` is the *only* channel, and a stringified-args no-op means the batch never ran.

### 3. Strictly sequential — `for … await`, never `parallel()`
The sim is serial. The loop awaits each agent fully (including its commit) before starting the next:

```js
const results = []
for (const f of FRAMES) {
  log(`Frame ${f.n} — ${f.title} — starting (sole sim user)`)
  const ledger = await agent(brief(f.n, f.title), { label: `frame-${f.n}`, phase: 'Re-audit', agentType: 'general-purpose' })
  results.push({ n: f.n, title: f.title, ledger })
  log(`Frame ${f.n} — done`)
}
return results
```
The Workflow concurrency cap is irrelevant here — the discipline is the *await-one-at-a-time* loop, which guarantees two agents never touch the sim at once.

### 4. `agentType: 'general-purpose'` — the frame agent needs the full tool set
A per-frame agent drives the sim (`xcrun simctl`), runs Maestro, extracts the mock (`obscura`), runs the differ (`node`), edits code (`Edit`/`Write`), runs `tsc`, and commits (`git`). The default workflow subagent may not carry all of that — pass `agentType: 'general-purpose'` (or another agent type that has Bash + Edit + Read) so it can.

### 5. Workflow agents can't call the `Skill` tool — point them at `SKILL.md` by absolute path, and embed THE LAW verbatim
A sub-agent typically has no `Skill` tool, so "invoke the mockup-fidelity skill" must mean **read and follow** `SKILL.md` at its absolute path (and its `references/`). Two more reasons to **also embed THE LAW (the ⛔ gate's five-plus rules) verbatim in the brief**: (a) the *installed marketplace* copy can be a stale version behind the *source* repo — embedding the law makes the agent enforce the current law regardless of which `SKILL.md` it reads; (b) it survives an agent that skims the skill under effort pressure.

---

## Protect the dev harness from every commit (the part that quietly corrupts the tree)

Each per-frame agent commits. The RN render harness (`assets/rn-harness/` — `.audit/measure.js` + a one-line `if (__DEV__) { try { require('../.audit/measure'); } catch {} }` in the app root, e.g. `app/_layout.tsx`) must **never** land in any of those commits. The `try/catch` guards *runtime*, but **Metro resolves `require` statically at build time**, so a committed harness line breaks a production bundle (it points at a git-excluded path). Protect it at the orchestrator level **once**, before launching any batch — don't rely on 50 agents each remembering not to stage it:

```bash
# 1. .audit/ never tracked (covers the probe file)
printf '\n# mockup-fidelity harness (never commit)\n/apps/<app>/.audit/\n' >> .git/info/exclude
# 1b. also exclude unrelated root untracked artifacts so a stray `git add -A` can't sweep them
for d in .design-review/ .email-mockups/ .mockup-shots/ ; do grep -qx "/$d" .git/info/exclude || echo "/$d" >> .git/info/exclude; done

# 2. hide the one-line dev edit in the TRACKED app root via skip-worktree
#    (gitignore is wrong here — the file is tracked; you only want to mask the local edit, not untrack it)
git update-index --skip-worktree apps/<app>/app/_layout.tsx
git ls-files -v apps/<app>/app/_layout.tsx   # → leading "S" confirms skip-worktree
git status --short | grep <app> || echo "harness invisible to git = good"
```

Now `git add -A` (if an agent ignores discipline) cannot include the harness. **Teardown** (after the last batch): `git update-index --no-skip-worktree apps/<app>/app/_layout.tsx`, remove the require line, `rm -rf apps/<app>/.audit`, and confirm the app boots clean.

**Per-frame git discipline (put it in the brief, verbatim):**
- Commit on the working branch (e.g. `staging`). **NEVER push** — the orchestrator/human decides when.
- **NEVER `git add -A` / `git add .` at the repo root** (it sweeps unrelated untracked files, and would catch the harness if protection ever lapses). Stage only the specific changed files under the app dir with explicit paths.
- **Never edit or stage the harnessed app root** (`app/_layout.tsx`). If a frame genuinely needs a root-layout change, the agent STOPS and reports — it does not commit it.
- Run the target's typecheck (`npx tsc --noEmit`) clean **before** committing.
- If a frame already matches (no divergences), make **no** commit — report "no changes".

---

## Checkpoint between batches — the sim wedges, and a long unattended run hides it

Run the inventory in **batches** (≈6 frames per `Workflow` invocation), not one 50-frame run, so you get a recovery point. Workflow scripts can't run shell, so the health check lives in the **orchestrator** (the main loop) between batches:

- **Probe the toolchain:** mock port, Metro port, collector port all answering; collector dump (`_latest-styles.json`) mtime is *fresh* (an agent navigating the sim refreshes it every ~1.5 s — a stale dump means the harness detached or the app crashed).
- **Recover if wedged:** relaunch the app (`xcrun simctl terminate … && xcrun simctl launch …`), confirm a fresh dump lands before the next batch. Confirm the sim still targets the right Metro (a plain RN debug build silently reconnects to `:8081`; pin `RCT_jsLocation`).
- **Confirm harness still protected** (skip-worktree flag still `S`; `.audit/` still excluded) and the tree is otherwise clean.
- **Update the inventory from the per-frame ledger files on disk** (next point), not from memory.

**Durability — write the ledger to disk AND return it.** A workflow's `return` value comes back only in the completion `<task-notification>`; have each agent ALSO write its ledger to `.mockup-fidelity/reaudit/frame-<n>.md`. Then results survive a lost notification, and the orchestrator updates the master inventory by reading those files. Validate the pipeline with a **small first batch (1–3 frames)** before scaling — confirm one agent really drove the sim, diffed, fixed, ran `tsc`, committed *without leaking the harness*, and returned a ledger.

**Resume a stalled batch** with `Workflow({ scriptPath, resumeFromRunId })` — completed `agent()` calls return cached results; only the failed/remaining frames re-run.

**A usage/session/weekly limit is a PAUSE, not a failure.** A long fan-out can hit an API usage cap mid-run — the remaining frames come back as failures with a "resets at <time>" message. The committed/ledgered frames are intact; the workflow is resumable. Two habits make this painless: (a) run **small batches (≈5-7 frames)** rather than one 80-frame run, so each batch is a durable checkpoint and a cap costs you at most one batch; (b) when a cap hits, note the reset time, and resume the failed frames after it. Don't mistake a cap for a broken pipeline.

---

## The reusable serial script

`assets/orchestration/reaudit-batch.workflow.js` is the generalised version of the script that ran a 54-frame RN re-audit: a `CONFIG` block (sim UDID, ports, app dir, mock path, skill path, branch) you fill in, the defensive `args` parse from invariant #1, THE LAW embedded verbatim, the per-frame git/harness discipline, and the sequential `await` loop. Pass `args` as the batch's frame list: `[{ "n": 15, "title": "Search · AI-interpreted" }, …]`. Edit the `CONFIG` for your project; the LAW and discipline are reusable as-is.

---

## Parallelism on a serial target — N independent lanes (the 4× speedup)

A single sim caps you at one agent. You break that cap **only** by running N fully **independent lanes** — never N agents sharing one stack. A **lane = `{ git worktree + APFS-cloned node_modules + RN harness (own collector port) + its own Metro (own port) + its own iOS sim }`**. Nothing mutable is shared: edits, commits, Metro hot-reload, and harness dumps are all per-lane, so the lanes physically cannot corrupt each other. With a 16-core/128 GB box, four lanes (4 sims + 4 Metros + 4 agents) run comfortably. Why each piece must be per-lane:

- **Worktree per lane.** If lanes shared one tree: (a) any agent's file save would hot-reload **all** sims (Metro rebuilds the whole bundle, not per-file), corrupting the other lanes mid-measurement; (b) concurrent `git commit` would race on `index.lock`. Worktrees give each lane its own working files **and** its own git index, so commits on each lane's own branch don't contend. This is the `Workflow` `isolation:'worktree'` rationale, done explicitly so each worktree also gets its own Metro.
- **node_modules by APFS CLONEFILE, never a symlink.** A symlinked `node_modules` **breaks Metro's resolver** — it won't crawl through the symlink and dies with `Unable to resolve module ./node_modules/<entry>` (red screen, no bundle). `cp -cR src dst` makes an APFS copy-on-write clone: a *real* directory Metro can crawl, created in seconds with near-zero extra disk. (This matches the known "symlinks satisfy tsc but break bundlers" gotcha — Metro is in the bundler camp.) Fall back to a real `npm/pnpm install` only off-APFS.
- **Harness collector port per lane — and its OUT dir OUTSIDE the watch root.** Each worktree's `_layout.tsx` require sets its own `global.__MF_COLLECTOR='http://localhost:<8799+K>/dump'` before `require('../.audit/measure')`; one collector per port writes that lane's `_latest.json` to **`/tmp/<app>-laneK-dump`, never inside the worktree** (a dump written into the Metro watch root triggers the infinite reload loop — see `assets/rn-harness/README.md` GOTCHA #1). Point each lane's `appDump` at its `/tmp` file.
- **`.env` (and any gitignored runtime config) COPIED into each lane worktree.** A fresh `git worktree` checkout does NOT carry gitignored files — so the lane's app boots without `.env`, and dev-login secrets / BFF origin / feature gates are missing (symptom: the dev-login button never renders, or every request hits the wrong/empty backend). `cp <main>/<app>/.env <lane>/<app>/.env` during bring-up, then start that lane's Metro so the values inline. (Env is read at bundle time — copy it BEFORE `expo start`.)
- **Metro/sim port per lane.** Metro on `8082+K`; the sim's `RCT_jsLocation` pinned to that port (a plain RN debug build otherwise reconnects to `:8081`). Start Metro with `--clear` so it crawls the freshly-cloned `node_modules`.

**Assignment: a worker-pool over a shared in-memory queue — not a file ledger.** The workflow script holds `const queue = [...FRAMES]`; it spawns one `worker(lane)` per lane inside a single `parallel([...])`; each worker loops `queue.shift()` → `await agent(brief(frame, lane))` until the queue drains. `shift()` is **race-free** because the workflow script is single-threaded JS that only yields at `await` — so two workers never claim the same frame, and the work **self-balances** (a lane with light frames just pulls more). This is strictly better than a mutable file "which sim is busy" ledger (no lock-file races). A **persisted `_lanes.json`** still earns its place as the static lane→{sim,metro,collector,worktree,branch} map — written by the setup script, read by the workflow via `args`, and used for health checks/recovery.

**Each new sim needs a human login.** A freshly-created sim's app starts logged out and Auth0/OTP can't be automated — bring the lane up to its first harness dump (proves the stack works) and hand the sim to the user to authenticate before assigning it frames. Lane 0 is typically already authenticated.

**Merge-back is the one real tax.** Each lane commits to its own `reaudit-lane-K` branch; the orchestrator merges all lane branches into the base at the end. Disjoint files merge clean; **two lanes editing the same shared primitive/token will conflict** (the known parallel-worktree-shared-file hazard). Mitigate by partitioning frames so co-dependent screens land on the same lane, and resolve the rest at merge. Teardown per lane: `git update-index --no-skip-worktree …/_layout.tsx`, `git worktree remove --force`, delete the branch, kill that lane's Metro/collector, shut down (or delete) the sim.

**⛔ The isolation leak — agents editing the MAIN tree instead of their lane worktree.** This is the failure that silently destroys parallel-lane verification: a per-lane agent edits and commits files in the **main repo** path (or another lane's) rather than its OWN `worktree/<app>`. The edit then lands in the wrong tree, while the agent's sim renders ITS lane's Metro (the *unedited* bundle) — so the differ "passes" against a screen that never had the fix, and the commit is **committed-but-never-rendered-verified**. It looks green and is hollow. Defenses, all required: (a) the brief must state, unmissably, "edit ONLY under `<lane.worktree>/<app>`; run ALL git as `git -C <lane.worktree>`; before committing, assert `git -C <lane.worktree> rev-parse --abbrev-ref HEAD` equals your lane branch"; (b) use ABSOLUTE worktree paths in every Edit/Write, never the main path; (c) after the run, treat any frame whose commit you can't confirm rendered as **verification debt** and run a **VERIFY sweep** — re-render each suspect frame on the now-current branch and re-diff, fixing whatever didn't actually render. A verify sweep on a leaky run routinely finds real survivors (fixes that were committed but never rendered).

**Scripts:** `assets/orchestration/lanes-up.sh` brings up lanes (worktree + clonefile + harness + sim + Metro + collector, waits for the first dump, writes `_lanes.json`); `assets/orchestration/reaudit-parallel.workflow.js` is the worker-pool driver — pass `args = { lanes: <rows from _lanes.json>, frames: [{n,title}], mainRepo, mockFile, mockUrl, skill }`. Validate one extra lane end-to-end (bundle builds, dump lands, isolated from lane 0, **and a test edit in the lane worktree hot-reloads ONLY that lane's sim**) before scaling to four.

**Differ-hardening re-pass.** When you *upgrade the differ* (e.g. it gains a new check class — see `assets/diff/README.md`), re-run the already-"matched" frames through `assets/orchestration/reaudit-differ.workflow.js` (same `args` shape, same 4-lane infra). Its per-frame brief is differ-centric, not full-audit: drive to the **populated** surface, run the hardened differ, and fix only the *new* finding classes it now surfaces (the inset/row-edge mismatches, the `⚠︎⚠︎ WRONG-STATE` bucket that proves a frame was previously measured in the wrong state, the `◆ App-EXTRA` rows). It re-runs the differ to a clean report and commits only if it changed something — so a frame the upgrade vindicates costs one cheap pass and no commit. This is how you retroactively close a whole defect class across an inventory the old differ had already green-lit.

### Bring-up gotchas (each cost a real debug cycle)

- **Pre-extract the mock ONCE, serially, before launching the lanes — then forbid agents from opening a browser.** The reference is immutable for the whole pass, so N agents re-extracting it would each re-render the same mock for a file they could have shared. (They can no longer *corrupt* each other — every `obscura fetch` is its own render — but the waste is real and the lanes run faster with no browser step.) Per frame, one call that sets `window.MF_FRAME_TITLE` and extracts in the same `--eval`, writing `mock-<n>.json`; the parallel brief points agents at the file. Note `obscura fetch --output` writes the returned value **verbatim**, so a pre-extracted file is single-encoded — `JSON.parse` it once. Files written by the previous runner are double-encoded; the differ tolerates both, so parse defensively when you *validate* one.
- **Serve-path, not root.** `python3 -m http.server` over the mock's directory serves a *directory listing* at `/`; the figures live at `/<mock>.html`. `analyze.js` then returns `{"error":"frame-not-found"}` (zero `<figure>`s) and every diff is garbage. Point `mockUrl` (and `--ref`) at the full `…/<mock>.html`, and sanity-check `document.querySelectorAll('figure').length > 0` before trusting a single extract.
- **`--clear` Metro after swapping node_modules.** Metro caches resolution — *including the broken symlink state* — so the `cp -cR` clonefile that fixes the files won't take until you restart the bundler with `--clear`. The first bundle then takes ~60–120 s; a lane is "ready" when **its collector writes the first dump**, not when Metro prints `packager-status:running`. Launch the app only *after* Metro is serving, or you get a red "Unable to resolve module" / no-bundle screen; relaunch once Metro is up.
- **Node-count is a free health signal; a fresh sim's first launch can raise the RN Dev Menu.** A dump with >100 nodes is a real mounted screen; ~10 nodes means a splash / loading / the RN Dev Menu captured the screen. Relaunch to clear it — and because **auth tokens live in secure-store, a relaunch never logs the user out**, so you can relaunch freely to reset a lane to a clean state between frames or after a wedge.
- **Full sim UDID required** — `xcrun simctl` rejects a truncated prefix with "Invalid device". `simctl create "name" "iPhone 16 Pro Max"` auto-picks the newest runtime; keep every lane on **one** device type so all lanes share a viewport.
- **Per-lane collector filename.** The harness collector asset writes `_latest.json`; a customised collector may write something else (`_latest-styles.json`). Point each lane's `appDump` at whatever **that** lane's collector actually writes — don't assume one name across lanes.
- **Sizing.** The Metro+sim pair is the heavy part; four lanes (4 Metro + 4 sims + 4 agents) sat comfortably on 16 cores / 128 GB. Scale lane count to cores, not ambition.
- **Recovery — the queue doesn't re-enqueue a dropped frame.** `queue.shift()` removes a frame before its agent runs; if that agent dies (not just reports BLOCKED), the frame is lost from the queue. After the run, diff the inventory against the written `frame-<n>.md` ledgers and re-run the gaps (a tiny serial batch on any one live lane).
