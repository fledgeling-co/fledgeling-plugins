// content-diff.mjs — text/CONTENT diff, separate from style (improvement #4).
//
// Some "it looks different" gaps are not CSS at all — they are CONTENT or DATA:
//   • the closing band's tone stored as `light` in the DB when the mock is dark
//   • a footer rendering SEO-long page titles ("Diolog for Investor Relations - less
//     time in the inbox") where the mock shows the short label ("Investor Relations")
//   • a card whose copy differs, a missing/extra section heading
// A computed-STYLE diff can never surface these (it compares how text is painted, not
// what the text says), and chasing them in CSS wastes time. This script extracts the
// ordered visible TEXT from both extract-mock dumps and diffs the sequences (LCS), so
// copy / label / heading divergence shows up as its own list — fix it in the CONTENT
// pipeline (DB seed, derivation, source JSON), not the stylesheet. Ideal end-state:
// seed the target's content store FROM the reference text so content parity holds by
// construction and only presentation is variable.
//
//   node content-diff.mjs --mock ref.json --app target.json [--out content-report.md]

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname } from 'node:path';

const args = Object.fromEntries(
  process.argv.slice(2).reduce((a, v, i, arr) => {
    if (v.startsWith('--')) a.push([v.slice(2), arr[i + 1]?.startsWith('--') ? true : arr[i + 1]]);
    return a;
  }, []),
);
if (!args.mock || !args.app) {
  console.error('usage: node content-diff.mjs --mock <ref.json> --app <target.json> [--out report.md]');
  process.exit(2);
}
const OUT = args.out || '.mockup-fidelity/diff/content-report.md';
const load = (p) => { let v = JSON.parse(readFileSync(p, 'utf8')); if (typeof v === 'string') v = JSON.parse(v); return v; };
const norm = (s) => String(s ?? '').replace(/\s+/g, ' ').trim();

const textSeq = (doc) => (doc.nodes || []).map((n) => norm(n.text)).filter((t) => t.length >= 2);
const M = textSeq(load(args.mock));
const A = textSeq(load(args.app));

// LCS over the two text sequences → the in-order alignment; the gaps are the diffs.
function lcs(a, b) {
  const n = a.length, m = b.length;
  const dp = Array.from({ length: n + 1 }, () => new Int32Array(m + 1));
  for (let i = n - 1; i >= 0; i--)
    for (let j = m - 1; j >= 0; j--)
      dp[i][j] = a[i] === b[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1]);
  const onlyA = [], onlyB = [];
  let i = 0, j = 0;
  while (i < n && j < m) {
    if (a[i] === b[j]) { i++; j++; }
    else if (dp[i + 1][j] >= dp[i][j + 1]) onlyA.push(a[i++]);
    else onlyB.push(b[j++]);
  }
  while (i < n) onlyA.push(a[i++]);
  while (j < m) onlyB.push(b[j++]);
  return { onlyA, onlyB, common: dp[0][0] };
}
const { onlyA: mockOnly, onlyB: appOnly, common } = lcs(M, A);

// Heuristic: a target string that CONTAINS a mock string (or vice-versa) is the same
// element with a longer/shorter label — that's a DATA/derivation bug (e.g. SEO title
// vs short nav label), called out separately from genuinely absent/added copy.
const labelMismatches = [];
const trulyMockOnly = [];
for (const t of mockOnly) {
  const longer = appOnly.find((a) => a.includes(t) || t.includes(a));
  if (longer) labelMismatches.push({ mock: t, app: longer });
  else trulyMockOnly.push(t);
}
const matchedApp = new Set(labelMismatches.map((x) => x.app));
const trulyAppOnly = appOnly.filter((a) => !matchedApp.has(a));

const L = [];
L.push('# Content diff (text / data — NOT styling)');
L.push(`- common in-order strings: ${common}  ·  **mock-only: ${trulyMockOnly.length}**  ·  **app-only: ${trulyAppOnly.length}**  ·  label-length mismatches: ${labelMismatches.length}`);
L.push('');
L.push('> These are CONTENT/DATA gaps — fix them in the content pipeline (DB seed, nav/footer derivation, source JSON), not in CSS. A style diff cannot see them.');
L.push('');
if (labelMismatches.length) {
  L.push('## ◑ Label-length mismatches (same element, longer/shorter text — a derivation/DATA bug)');
  L.push('| mock text | target text |', '|---|---|');
  for (const x of labelMismatches.slice(0, 120)) L.push(`| ${esc(x.mock)} | ${esc(x.app)} |`);
  L.push('');
}
if (trulyMockOnly.length) {
  L.push('## ⊖ In the mock, MISSING from the target (copy/headings to add)');
  for (const t of trulyMockOnly.slice(0, 200)) L.push(`- ${esc(t)}`);
  L.push('');
}
if (trulyAppOnly.length) {
  L.push('## ⊕ In the target, NOT in the mock (extra copy — remove or cite)');
  for (const t of trulyAppOnly.slice(0, 200)) L.push(`- ${esc(t)}`);
  L.push('');
}
if (!labelMismatches.length && !trulyMockOnly.length && !trulyAppOnly.length) {
  L.push('## ✓ Text content matches in order — any remaining difference is presentation, not content.');
}
function esc(s) { return String(s ?? '').replace(/\|/g, '\\|'); }
mkdirSync(dirname(OUT), { recursive: true });
writeFileSync(OUT, L.join('\n'));
console.log(`content-diff → ${OUT}  (mock-only:${trulyMockOnly.length} app-only:${trulyAppOnly.length} label:${labelMismatches.length})`);
