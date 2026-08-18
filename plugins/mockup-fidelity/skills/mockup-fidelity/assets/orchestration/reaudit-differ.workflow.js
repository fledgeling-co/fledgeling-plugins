export const meta = {
  name: 'mockup-fidelity-differ-repass',
  description: 'Re-pass previously-FIXED frames with the HARDENED differ across 4 lanes; fix the new inset / row-edge / wrong-state / app-extra findings the old differ missed.',
  phases: [{ title: 'Differ re-pass' }],
}

// args = { lanes:[...], frames:[{n,title}], mainRepo, mockFile, mockUrl, skill }
let raw = args
if (typeof raw === 'string') { try { raw = JSON.parse(raw) } catch (e) { raw = {} } }
const LANES = Array.isArray(raw?.lanes) ? raw.lanes : []
const FRAMES = Array.isArray(raw?.frames) ? raw.frames : []
const MAIN = raw?.mainRepo || '/ABS/PATH/TO/main-repo'
const MOCK = raw?.mockFile || 'docs/ui-mockups/<mock>.html'
const MOCKURL = raw?.mockUrl || 'http://localhost:8770/<mock>.html'
const SKILL = raw?.skill || '/ABS/PATH/TO/plugins/mockup-fidelity/skills/mockup-fidelity/SKILL.md'
log(`args typeof=${typeof args}; ${LANES.length} lane(s), ${FRAMES.length} frame(s)`)
if (!LANES.length || !FRAMES.length) { log('Need lanes and frames — nothing to do.'); return [] }

function brief(f, lane) {
  return `You are a FRESH UI fidelity auditor on LANE ${lane.id}, running a DIFFER-HARDENING RE-PASS on ONE frame that a prior audit already marked FIXED. The computed-style differ was just upgraded to catch a class it used to miss; your job is to drive the frame, run the HARDENED differ, and fix anything it NOW surfaces. YOUR LANE OWNS sim ${lane.simUdid} — never touch another lane.

STEP 0 — METHOD: skim ${SKILL} (measure, never eyeball; mock wins; verify the POPULATED state).

WHAT THE HARDENED DIFFER NOW CATCHES (these are the findings to hunt):
- left-inset on ANY left-anchored element, INCLUDING wide flex titles (a list-row title spans wide; the old differ skipped it — this is how a list-row name shipped at the wrong inset).
- row-left-inset / row-right-inset — a row pushed in by a leading TILE/ICON/AVATAR, or a displaced trailing icon/badge (non-text, never probed before).
- ⚠︎⚠︎ WRONG-STATE — a mock probe present elsewhere in the app dump = you measured the WRONG STATE; drive to the populated surface and re-measure.
- ◆ App-EXTRA — text the app renders that the mock lacks (remove per "mock wins", or cite as real data).

TASK for frame '${f.title}' (mock #${f.n}, the ${f.n}th <figure> in ${MAIN}/${MOCK}); app surface in this lane's worktree ${lane.worktree}/${lane.appDir}:
1. Drive sim ${lane.simUdid} to the frame's POPULATED surface (tap CTAs by accessibilityLabel; for a company-surface frame open a company then its tab; for a drill-in drive the affordance). Wait 8-12s for any AI stream. Verify real data is on screen (no empty/loading/—/504 fallback).
2. The harness POSTs to collector :${lane.collectorPort} → \`${lane.appDump}\` every ~1.5s. Pick a unique on-screen text as the anchor.
3. Run the HARDENED differ:
   \`node ${MAIN}/.mockup-fidelity/diff/diff.mjs --mock ${MAIN}/.mockup-fidelity/reaudit/mock-${f.n}.json --app ${lane.appDump} --anchor "<unique screen text>" --out ${MAIN}/.mockup-fidelity/reaudit/repass-${f.n}.md\`
   READ the report.
4. If ⚠︎⚠︎ WRONG-STATE rows appear, you measured the wrong surface — navigate correctly and re-run before trusting anything.
5. FIX every ❌ mismatch (mock wins) — especially the inset/row-edge class — editing files under \`${lane.worktree}/${lane.appDir}\`. For ◆ App-EXTRA, remove elements the mock lacks (or cite real data). Skip a row ONLY with an EXTERNAL citation (ticket / pre-existing code comment / recorded decision / guardrail) — never a reason you author now.
6. Re-run the differ → confirm the report is clean (0 unexplained ❌, 0 WRONG-STATE). Screenshot \`xcrun simctl io ${lane.simUdid} screenshot /tmp/repass-${f.n}.png\` and READ it.
7. \`cd ${lane.worktree}/${lane.appDir} && npx tsc --noEmit\` clean for your changed files.

HARNESS/GIT: the worktree harness (\`.audit/\`, \`app/_layout.tsx\`) is commit-protected (excluded + skip-worktree) — never edit/stage it. Commit on \`${lane.branch}\` in THIS worktree (\`git -C ${lane.worktree} ...\`), staging ONLY your changed files under \`${lane.appDir}/\` with explicit paths. NEVER push, NEVER \`git add -A\`. Message: \`fix(<app>): frame ${f.n} ${f.title} — differ re-pass <summary>\` + Co-Authored-By trailer. If the differ is already clean (nothing the hardened checks caught), make NO commit.

OUTPUT (write to \`${MAIN}/.mockup-fidelity/reaudit/repass-${f.n}.md\` AND return): VERDICT (CLEAN-ALREADY / FIXED-NEW / BLOCKED+reason); NEW FINDINGS the hardened differ caught (each: property, target vs mock, the file:line fix); WRONG-STATE encountered (y/n); APP-EXTRA removed; COMMIT (sha or none); SCREENSHOT confirmed (y).

Stay within this ONE frame on YOUR lane. If the surface genuinely can't render its populated state, report BLOCKED with the reason.`
}

const queue = [...FRAMES]
const results = []
async function worker(lane) {
  const done = []
  while (queue.length) {
    const f = queue.shift(); if (!f) break
    log(`Lane ${lane.id} (sim ${lane.simUdid}) -> repass frame ${f.n} ${f.title} [${queue.length} left]`)
    const ledger = await agent(brief(f, lane), { label: `lane${lane.id}-repass-${f.n}`, phase: 'Differ re-pass', agentType: 'general-purpose' })
    done.push({ lane: lane.id, n: f.n, title: f.title, ledger })
    log(`Lane ${lane.id} done frame ${f.n}`)
  }
  log(`Lane ${lane.id} drained.`)
  return done
}
const perLane = await parallel(LANES.map(lane => () => worker(lane)))
for (const d of perLane) if (Array.isArray(d)) results.push(...d)
return results
