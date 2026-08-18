export const meta = {
  name: 'mockup-fidelity-section-parallel',
  description: 'Web↔web: align a page to its reference one SECTION per agent in parallel — each runs structure-diff → style-diff → overlay → fix its composite → re-verify. Reference is measured ONCE and reused.',
  phases: [{ title: 'Section align' }],
}

// args = { sections:[{name, anchor, composite}], refUrl, targetUrl, mainRepo, skill, viewport }
//   name      label, e.g. "module-cards"
//   anchor    a unique on-screen TEXT in that section (scopes the diffs + scroll)
//   composite the target component file to edit, e.g. components/composites/ModuleCards.tsx
let raw = args
if (typeof raw === 'string') { try { raw = JSON.parse(raw) } catch (e) { raw = {} } }
const SECTIONS = Array.isArray(raw?.sections) ? raw.sections : []
const REF = raw?.refUrl || 'http://localhost:8770/<mock>.html'
const TGT = raw?.targetUrl || 'http://localhost:3000/'
const MAIN = raw?.mainRepo || '/ABS/PATH/TO/repo'
const SKILL = raw?.skill || '/ABS/PATH/TO/plugins/mockup-fidelity/skills/mockup-fidelity/SKILL.md'
const VP = raw?.viewport || '1440x2400'
const DIFF = `${MAIN}/.mockup-fidelity`
log(`section-parallel: ${SECTIONS.length} section(s); ref=${REF} target=${TGT}`)
if (!SECTIONS.length) { log('No sections — nothing to do.'); return [] }

// CONTRACT: the reference is immutable — measure it ONCE before fan-out (caller should
// have copied extract-mock.js/structure-diff.mjs/diff.mjs/overlay.mjs into $DIFF and
// extracted the whole-page ref dump to $DIFF/ref.json). Each agent re-extracts only ITS
// target section and reuses the shared ref dump (never re-renders the reference).

function brief(sec) {
  return `You are a web↔web fidelity auditor aligning ONE section — "${sec.name}" — of ${TGT} to the reference ${REF}. Source of truth = the reference. Edit ONLY styling/layout in the target composite \`${sec.composite}\`; never change real functionality. Honor repo guardrails (no mocks/stubs/fallbacks).

STEP 0 — METHOD: skim ${SKILL}. The key rule for THIS task: STRUCTURE before STYLE. The per-property style differ is BLIND to layout (a 2×2 grid rendered 1×4, a missing icon node, a row that should be a column, dash-vs-check bullets). Run the structure diff and the overlay FIRST.

Each \`obscura fetch\` is its own stateless render, so lanes cannot collide over a shared session — but they do each cost a full page load, so batch what you can into one \`--eval\`. Localhost needs \`--allow-private-network\` or the fetch fails as an SSRF block.

1. SCREENSHOT both sides at the same viewport (${VP}), scoped to this section (scroll to the text "${sec.anchor}"):
   - reference: \`obscura --allow-private-network fetch ${REF} --eval "(() => { const e = [...document.querySelectorAll('*')].find(n => n.textContent.includes('${sec.anchor}')); e && e.scrollIntoView(); return 'ok'; })()" --screenshot ${DIFF}/${sec.name}-REF.png\`
   - target: same command against ${TGT}, writing \`${DIFF}/${sec.name}-TGT.png\`
   READ both PNGs and list every STRUCTURAL difference (grid columns, card anatomy, icon presence/position, number/badge position, bullet style, dividers, alignment, density).
2. VISUAL OVERLAY (catches what the eye misses fast): \`node ${DIFF}/overlay.mjs --ref ${DIFF}/${sec.name}-REF.png --app ${DIFF}/${sec.name}-TGT.png --out ${DIFF}/${sec.name}-overlay.html\`, screenshot it (\`obscura fetch "file://${DIFF}/${sec.name}-overlay.html" --screenshot ${DIFF}/${sec.name}-overlay.png\`), READ — bright regions in the difference view = where they diverge.
3. STRUCTURE DIFF (re-extract only the target; reuse the shared ${DIFF}/ref.json):
   - \`obscura --allow-private-network fetch ${TGT} --eval "(() => { window.MF_FRAME_SELECTOR='body'; window.MF_CHROME_SELECTOR='__none__'; return ($(cat ${DIFF}/extract-mock.js))(); })()" --output ${DIFF}/${sec.name}-tgt.json\` — the globals and the extraction go in ONE eval because each fetch is a fresh page, and \`--output\` writes the value verbatim so there is nothing to unwrap.
   - \`node ${DIFF}/structure-diff.mjs --mock ${DIFF}/ref.json --app ${DIFF}/${sec.name}-tgt.json --anchor "${sec.anchor}" --out ${DIFF}/${sec.name}-structure.md\` — READ it. Fix every layout mismatch / MISSING / EXTRA in \`${sec.composite}\` (grid columns, add missing icon/divider nodes, fix flex-direction/order, remove app-extras).
4. STYLE DIFF: \`node ${DIFF}/diff.mjs --mock ${DIFF}/ref.json --app ${DIFF}/${sec.name}-tgt.json --anchor "${sec.anchor}" --out ${DIFF}/${sec.name}-style.md\` — fix the remaining computed-style deltas (padding/radius/bg/border/shadow/font/size/colour) with literal px/hex where no token matches.
5. RE-VERIFY: re-extract the target section, re-run structure-diff + style-diff to confirm they drop, re-screenshot and READ it against the reference PNG. Iterate until the section matches.

SHARED-FILE CAUTION: edit ONLY \`${sec.composite}\` and styles it owns. If a fix needs a shared ELEMENT (Card/Heading/tokens), NOTE it in your output as a coordination item rather than editing it (another section may touch the same file) — the orchestrator serializes shared edits.

OUTPUT (return): SECTION "${sec.name}" — structural gaps found (grid/icons/order/missing/extra) + how fixed; style deltas fixed; any shared-element/token change NEEDED (so the orchestrator can serialize it); a final statement that the re-screenshot now matches the reference (or what still differs + why). Back every "matches" with the re-run diff + the re-read screenshot, never a code-read.`
}

const results = await parallel(SECTIONS.map((sec) => () =>
  agent(brief(sec), { label: `section-${sec.name}`, phase: 'Section align', agentType: 'general-purpose' })
))
return results.filter(Boolean)
