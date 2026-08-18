export const meta = {
  name: 'mockup-fidelity-batch',
  description: 'Sequentially audit a batch of mock frames, one fresh general-purpose agent per frame (never parallel — a sim/serial target is a single resource).',
  phases: [{ title: 'Audit' }],
}

// ─────────────────────────────────────────────────────────────────────────────
// Reusable sequential batch driver for the mockup-fidelity skill.
// See references/batch-orchestration.md for the full rationale and the invariants
// each line below defends. Fill in CONFIG; the LAW + git/harness discipline are
// reusable verbatim. Pass `args` = this batch's frame list, e.g.
//   [{ "n": 15, "title": "Search · AI-interpreted" }, { "n": 17, "title": "Browse · by index" }]
// ─────────────────────────────────────────────────────────────────────────────
const CONFIG = {
  skill:   '/ABS/PATH/TO/plugins/mockup-fidelity/skills/mockup-fidelity/SKILL.md', // read+follow (sub-agents have no Skill tool)
  mockFile: 'docs/ui-mockups/<mock>.html',   // path passed to the agent for context
  mockUrl:  'http://localhost:8770/',         // the SERVED mock (extract-mock reads getComputedStyle here)
  appDir:   'apps/<app>',                      // target app dir; commits are scoped under here
  rootFile: 'apps/<app>/app/_layout.tsx',     // the skip-worktree'd file carrying the harness require
  simUdid:  '<SIM-UDID>',                      // serial resource — one agent at a time
  bundleId: '<com.example.app>',
  metroPort: 8082,                             // pin RCT_jsLocation; a plain RN debug build defaults to 8081
  collector: '.mockup-fidelity/_latest-styles.json', // harness POSTs here every ~1.5s
  branch:   'staging',
  // Project-specific recorded decisions the agent may rely on (these ARE citations — keep the list external/pre-existing):
  standingDecisions: 'mock wins on everything visible; a guardrail-honest divergence is legit ONLY with a cited guardrail; keep wired features (if a fix would delete one, STOP and report); line-height 1.5x for prose; content gutter 20; screen root background #fff; monogram font-weight 600.',
}

// Invariant #1 — args can arrive as a JSON STRING; parse defensively or the run is a silent no-op.
let raw = args
if (typeof raw === 'string') { try { raw = JSON.parse(raw) } catch (e) { raw = [] } }
const FRAMES = Array.isArray(raw) ? raw : (raw && Array.isArray(raw.frames) ? raw.frames : [])
log(`args typeof=${typeof args}; resolved ${FRAMES.length} frame(s)`)
if (!FRAMES.length) { log('No frames passed in args — nothing to do.'); return [] }

function brief(n, title) {
  return `You are a FRESH single-frame UI fidelity auditor. No prior context. Audit EXACTLY ONE mock frame end-to-end (audit -> fix -> verify -> commit) and return a ledger.

STEP 0 — METHOD. Read IN FULL and follow as your method: ${CONFIG.skill}
Also read its references/ directory. This skill IS your procedure: measure (never eyeball); the mock is the source of truth; breadth (present/divergent/ABSENT + app-extra) before depth; the differ to zero unexplained; a visible difference is a DEFECT until an EXTERNAL citation proves it intentional.

TASK: Audit ONLY the frame titled '${title}' (mock frame #${n} — the ${n}th <figure>) in ${CONFIG.mockFile} against its surface in ${CONFIG.appDir}, breadth-first per THE LAW. Drive every interactive affordance to the surface it opens and audit that too. Fix EVERY divergence (mock wins): wrong label/style/icon, missing element, AND app-EXTRA elements (badges/lines/wrappers/extra controls the mock lacks — remove them). Verify the POPULATED state, never a fallback.

THE LAW (enforce all):
- This frame is a DISTINCT surface (state/drill-in/sheet/fallback/variant suffixes are NOT sub-states to fold into a parent).
- PRESENT = MEASURED (rendered label + style + icon glyph), never purpose-inferred. Same purpose + different label/style/icon = DIVERGENT.
- A citation is EXTERNAL/PRE-EXISTING ONLY (a ticket, a code comment predating this audit, a recorded product decision, or a guardrail). A justification you author DURING this audit ("app-ahead", "recorded decision", "conveys it via X", "richer treatment") is BANNED — no external citation => it is a DEFECT, fix it (mock wins).
- App-EXTRA elements are DIVERGENT too — mock wins by REMOVING extras, not only by adding missing.
- "0 unexplained" from the differ is NOT a breadth verdict — the differ is blind to missing/substituted/extra elements; fill the present/divergent/ABSENT ledger from the structure artifacts FIRST. Native chrome the app legitimately renders = tab bar / nav-back / system sheets / status bar ONLY. Never fabricate data.

STANDING DECISIONS: ${CONFIG.standingDecisions}

TOOLCHAIN (already running — do NOT restart servers):
- Sim: UDID ${CONFIG.simUdid}, bundle ${CONFIG.bundleId}, connected to Metro :${CONFIG.metroPort}. Screenshot: \`xcrun simctl io ${CONFIG.simUdid} screenshot /tmp/frame-${n}.png\` then READ that PNG by eye to confirm.
- App rendered tree: the in-app harness POSTs to the collector which writes \`${CONFIG.collector}\` every ~1.5s; it holds ALL mounted screens — scope to the foreground via the differ's --anchor (a unique text on the target screen).
- Mock computed styles: \`obscura --allow-private-network fetch ${CONFIG.mockUrl} --eval "(() => { window.MF_FRAME_TITLE = '${title}'; return (\\$(cat .mockup-fidelity/diff/extract-mock.js))(); })()" --output .mockup-fidelity/reaudit/mock-${n}.json\` (MF_FRAME_TITLE substring-matches the figcaption; one stateless call sets the global and extracts, and --output writes the value verbatim).
- Differ: \`node .mockup-fidelity/diff/diff.mjs --mock .mockup-fidelity/reaudit/mock-${n}.json --app ${CONFIG.collector} --anchor "<screen text>" --out .mockup-fidelity/reaudit/report-${n}.md\`, then READ the report (every property mismatch + every unmatched probe = missing element OR intentional swap, you classify each).
- Maestro nav: tap CTAs by accessibilityLabel; launchApp restores the last route; submit text via keyboard Enter; wait 8-12s after triggering an AI stream before measuring.
- Typecheck: \`cd ${CONFIG.appDir} && npx tsc --noEmit\` — must be clean BEFORE committing.

HARNESS / GIT DISCIPLINE (critical — do NOT break):
- The audit harness (\`${CONFIG.appDir}/.audit/\` and the require line in \`${CONFIG.rootFile}\`) is commit-protected (\`.audit/\` git-excluded; root file on skip-worktree). DO NOT edit, remove, or stage \`${CONFIG.rootFile}\` or anything under \`.audit/\`. If your frame genuinely needs a root-layout change, STOP and report it — do NOT commit it.
- Commit on \`${CONFIG.branch}\`. NEVER push. NEVER \`git add -A\`/\`git add .\` at the repo root. Stage ONLY the specific files you changed under \`${CONFIG.appDir}/\` with explicit paths.
- Commit message: \`fix(<app>): frame ${n} ${title} — <short summary>\` with a \`Co-Authored-By:\` trailer.
- If you find NO divergences (frame already matches), make NO changes and NO commit — report "no changes".

OUTPUT (both): (1) Write your ledger to \`.mockup-fidelity/reaudit/frame-${n}.md\`. (2) Return it as your final message. Ledger MUST contain: VERDICT (MATCH / FIXED / BLOCKED+reason); PRESENT (measured-present & matching, brief); DIVERGENT->FIXED (each, file:line, mock value applied); ABSENT (each mock element missing from app — FIXED-added, or the EXTERNAL citation if intentionally absent; no citation = it was a DEFECT you fixed); APP-EXTRA->REMOVED (each, file:line); COMMIT (sha + subject, or "none"); SCREENSHOT (confirm you READ /tmp/frame-${n}.png and it matches).

Stay within this ONE frame. If blocked, report BLOCKED and stop — do not loop.`
}

const results = []
for (const f of FRAMES) {
  log(`Frame ${f.n} — ${f.title} — starting (sequential, sole sim user)`)
  const ledger = await agent(brief(f.n, f.title), { label: `frame-${f.n}`, phase: 'Audit', agentType: 'general-purpose' })
  results.push({ n: f.n, title: f.title, ledger })
  log(`Frame ${f.n} — ${f.title} — done`)
}
return results
