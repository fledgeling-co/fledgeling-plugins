export const meta = {
  name: 'mockup-fidelity-parallel',
  description: 'Audit a queue of mock frames across N independent lanes (worktree+Metro+collector+sim) in parallel; each lane runs its frames sequentially (one agent per sim at a time).',
  phases: [{ title: 'Audit' }],
}

// ─────────────────────────────────────────────────────────────────────────────
// PARALLEL driver for the mockup-fidelity skill on a SERIAL target (RN sim).
// A serial sim caps you at one agent — UNLESS you run N fully independent LANES,
// each = its own { git worktree + Metro port + collector port + iOS sim }. Bring
// the lanes up with lanes-up.sh first (it writes the lane ledger this script reads
// via args). See references/batch-orchestration.md "Parallelism on a serial target".
//
// Pass args = { lanes: [<lane rows from _lanes.json>], frames: [{n,title}], mainRepo, mockFile, mockUrl, skill }
// Each lane row: { id, simUdid, metroPort, collectorPort, worktree, appDir, appDump, branch }
// ─────────────────────────────────────────────────────────────────────────────

// Defensive parse — Workflow args can arrive as a JSON STRING (else silent no-op).
let raw = args
if (typeof raw === 'string') { try { raw = JSON.parse(raw) } catch (e) { raw = {} } }
const LANES = Array.isArray(raw?.lanes) ? raw.lanes : []
const FRAMES = Array.isArray(raw?.frames) ? raw.frames : []
const MAIN = raw?.mainRepo || '/ABS/PATH/TO/main-repo'
const MOCK = raw?.mockFile || 'docs/ui-mockups/<mock>.html'
const MOCKURL = raw?.mockUrl || 'http://localhost:8770/'
const SKILL = raw?.skill || '/ABS/PATH/TO/plugins/mockup-fidelity/skills/mockup-fidelity/SKILL.md'
log(`args typeof=${typeof args}; ${LANES.length} lane(s), ${FRAMES.length} frame(s)`)
if (!LANES.length || !FRAMES.length) { log('Need both lanes and frames in args — nothing to do.'); return [] }

function brief(f, lane) {
  return `You are a FRESH single-frame UI fidelity auditor on LANE ${lane.id}. No prior context. Audit EXACTLY ONE mock frame end-to-end (audit -> fix -> verify -> commit) and return a ledger. YOUR LANE OWNS sim ${lane.simUdid} — never touch any other sim, worktree, Metro, or collector.

STEP 0 — METHOD. Read IN FULL and follow as your method: ${SKILL} (and its references/). Measure, never eyeball; the mock is the source of truth; breadth (present/divergent/ABSENT + app-extra) before depth; differ to zero unexplained; a visible difference is a DEFECT until an EXTERNAL citation proves it intentional.

TASK: Audit ONLY the frame titled '${f.title}' (mock frame #${f.n} — the ${f.n}th <figure>) in ${MAIN}/${MOCK} against its surface in this lane's worktree at ${lane.worktree}/${lane.appDir}. Breadth-first per THE LAW. Drive every interactive affordance to the surface it opens and audit that too. Fix EVERY divergence (mock wins): wrong label/style/icon, missing element, AND app-EXTRA elements (badges/lines/wrappers/extra controls the mock lacks — remove them). Verify the POPULATED state, never a fallback.

THE LAW:
- This frame is a DISTINCT surface (state/drill-in/sheet/fallback/variant suffixes are NOT sub-states).
- PRESENT = MEASURED (rendered label + style + icon glyph), never purpose-inferred. Same purpose + different label/style/icon = DIVERGENT.
- A citation is EXTERNAL/PRE-EXISTING ONLY (ticket / code comment predating this audit / recorded product decision / guardrail). A justification you author DURING this audit ("app-ahead", "recorded decision", "conveys it via X", "richer treatment") is BANNED — no external citation => DEFECT, fix it (mock wins).
- App-EXTRA elements are DIVERGENT too — mock wins by REMOVING extras, not only adding missing.
- "0 unexplained" from the differ is NOT a breadth verdict — fill the present/divergent/ABSENT ledger from the structure artifacts FIRST. Native chrome = tab bar / nav-back / system sheets / status bar ONLY. Never fabricate data.

STANDING DECISIONS (replace with the project's recorded decisions): mock wins on everything visible; a guardrail-honest divergence is legit ONLY with a cited guardrail; keep wired features (if a fix would delete one, STOP and report).

YOUR LANE'S TOOLCHAIN (already running — do NOT restart servers, do NOT touch other lanes):
- Worktree (edit/tsc/commit HERE): ${lane.worktree}  (app dir: ${lane.appDir})
- Sim: ${lane.simUdid}, bundle <com.example.app>, connected to Metro :${lane.metroPort}. Screenshot: \`xcrun simctl io ${lane.simUdid} screenshot /tmp/frame-${f.n}.png\` then READ that PNG by eye.
- App rendered tree: this lane's harness POSTs to collector :${lane.collectorPort}, which writes \`${lane.appDump}\` every ~1.5s (holds ALL mounted screens — scope to the foreground via the differ's --anchor).
- Mock computed styles: ALREADY PRE-EXTRACTED at \`${MAIN}/.mockup-fidelity/reaudit/mock-${f.n}.json\` — use it directly as the differ's --mock input. Do NOT re-extract it: \`obscura fetch\` would re-render the whole mock once per lane for a file all ${LANES.length} lanes already share. (If you need a VISUAL mock screenshot for eyeball confirmation, the served mock is \`${MOCKURL}\`, frame title '${f.title}' — use sparingly.)
- Differ (shared tools, lane-specific inputs): \`node ${MAIN}/.mockup-fidelity/diff/diff.mjs --mock ${MAIN}/.mockup-fidelity/reaudit/mock-${f.n}.json --app ${lane.appDump} --anchor "<screen text>" --out ${MAIN}/.mockup-fidelity/reaudit/report-${f.n}.md\`, then READ the report.
- Maestro/sim nav targets sim ${lane.simUdid} ONLY (use \`--device ${lane.simUdid}\` / \`xcrun simctl ... ${lane.simUdid}\`; never drive another lane's sim). Wait 8-12s for AI streams.
- Typecheck: \`cd ${lane.worktree}/${lane.appDir} && npx tsc --noEmit\` — clean BEFORE committing.

HARNESS / GIT DISCIPLINE (critical):
- This worktree's harness (\`${lane.appDir}/.audit/\` and the require line in \`${lane.appDir}/app/_layout.tsx\`) is commit-protected (git-excluded + skip-worktree). DO NOT edit, remove, or stage \`app/_layout.tsx\` or anything under \`.audit/\`. If your frame needs a root-layout change, STOP and report.
- You are on branch \`${lane.branch}\` in THIS worktree. Commit HERE (\`git -C ${lane.worktree} ...\`). NEVER push. NEVER \`git add -A\`/\`git add .\`. Stage ONLY the specific files you changed under \`${lane.appDir}/\` with explicit paths. (The orchestrator merges all lane branches back at the end.)
- Commit message: \`fix(<app>): frame ${f.n} ${f.title} — <short summary>\` + a \`Co-Authored-By:\` trailer.
- If NO divergences (frame already matches), make NO commit — report "no changes".

OUTPUT (both): (1) Write your ledger to \`${MAIN}/.mockup-fidelity/reaudit/frame-${f.n}.md\`. (2) Return it. Ledger MUST contain: VERDICT (MATCH/FIXED/BLOCKED+reason); PRESENT (measured & matching, brief); DIVERGENT->FIXED (each, file:line, mock value); ABSENT (each missing mock element — FIXED-added, or EXTERNAL citation; no citation = DEFECT you fixed); APP-EXTRA->REMOVED (each, file:line); COMMIT (sha+subject on ${lane.branch}, or "none"); SCREENSHOT (confirm you READ /tmp/frame-${f.n}.png).

Stay within this ONE frame on YOUR lane. If blocked, report BLOCKED and stop.`
}

// Shared work queue — race-free because the workflow script is single-threaded JS (only yields at await).
const queue = [...FRAMES]
const results = []

async function worker(lane) {
  const done = []
  while (queue.length) {
    const f = queue.shift()
    if (!f) break
    log(`Lane ${lane.id} (sim ${lane.simUdid}) -> frame ${f.n} ${f.title} [${queue.length} left]`)
    const ledger = await agent(brief(f, lane), { label: `lane${lane.id}-frame-${f.n}`, phase: 'Audit', agentType: 'general-purpose' })
    done.push({ lane: lane.id, n: f.n, title: f.title, ledger })
    log(`Lane ${lane.id} done frame ${f.n}`)
  }
  log(`Lane ${lane.id} drained.`)
  return done
}

const perLane = await parallel(LANES.map(lane => () => worker(lane)))
for (const d of perLane) if (Array.isArray(d)) results.push(...d)
return results
