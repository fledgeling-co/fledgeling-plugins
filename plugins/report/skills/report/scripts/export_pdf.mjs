// export_pdf.mjs — print a report to A4 PDF, then CHECK THE PDF rather than assuming it.
//
//   node scripts/export_pdf.mjs docs/reports/<slug>/index.html --out docs/reports/<slug>/report.pdf
//
// A PDF that wrote successfully and paginated wrongly is the normal failure, not a rare one:
// printToPDF returns 200 whether the report landed on four clean sheets or twenty with a chart
// sliced across two of them. So this verifies what came out — real A4 geometry, a page count in
// the right relationship to the block count, surviving link annotations, and no transient
// animation text ("Loading…", "0%") frozen into the ink because the printer caught a tween
// mid-flight.
//
// Where poppler (pdfinfo / pdftotext) is absent it says which checks it could not run rather
// than reporting a pass. A gate that cannot fail is indistinguishable from one that passes.

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { open, parseArgs } from './lib/harness.mjs';

// execFile, never exec: no shell, so a path containing a space or a metacharacter is just a path.
const run = (cmd, argv) =>
  execFileSync(cmd, argv, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
const have = (cmd) => {
  try { run(cmd, ['-v']); return true; } catch (e) { return e.code !== 'ENOENT'; }
};

const A4_PT = { w: 595, h: 842 };     // 210 × 297 mm at 72dpi
const TOL = 3;                         // points; rounding in the producer, not a real difference

// Text that means "this frame was mid-animation when it printed".
// Deliberately NOT matching a bare "0%" on its own line: that is what a percentage axis
// prints, and an earlier version of this list failed every report that drew one. A gate
// with a false positive gets switched off, which costs more than the defect it caught.
const TRANSIENT = [
  /\bloading\b/i, /\bcalculating\b/i, /\bchecking\b/i, /\banalysing\b/i, /\banalyzing\b/i,
  /\bplease wait\b/i, /\bundefined\b/, /\bNaN\b/, /\[object Object\]/,
];

const args = parseArgs();
const src = path.resolve(args.file);
const out = path.resolve(args.out || src.replace(/\.html?$/i, '.pdf'));

// --- which reading -----------------------------------------------------------------------
// The report ships three registers over one ledger. Exactly one prints, and the PDF stamps
// which — a document carrying one of three readings with nothing saying which is ambiguous
// the moment it is forwarded.
//
// The register is selected by REWRITING THE SOURCE, not by setting .checked from script.
// The registers are resolved by a :has(#rd-<name>:checked) selector, and at least one engine
// in this stack does not re-evaluate :has() when checked is set programmatically — so a
// scripted toggle silently exports the default register under a different filename. Rewriting
// cannot fail that way on any engine. The temp file is a sibling so relative assets resolve.
const READINGS = ['primer', 'brief', 'technical'];
let printSrc = src, temp = null;

if (args.reading) {
  if (!READINGS.includes(args.reading)) {
    console.error(`export_pdf: --reading must be one of ${READINGS.join(', ')}`);
    process.exit(2);
  }
  const html = fs.readFileSync(src, 'utf8');
  if (!html.includes('id="rd-' + args.reading + '"')) {
    console.error(`export_pdf: ${path.basename(src)} has no #rd-${args.reading} control`);
    process.exit(2);
  }
  const picked = html
    .replace(/(<input[^>]*name="reading"[^>]*?)\s+checked/g, '$1')
    .replace(new RegExp(`(<input[^>]*id="rd-${args.reading}"[^>]*?)(\\s*/?>)`),
             '$1 checked$2')
    .replace(/(<html[^>]*\bdata-active-reading=")[^"]*(")/, `$1${args.reading}$2`);
  temp = path.join(path.dirname(src), `.export-${args.reading}-${path.basename(src)}`);
  fs.writeFileSync(temp, picked);
  printSrc = temp;
}

// Print with reduced motion forced. The static branch is the authored print frame, so this is
// the composition the report intends to put on paper — not whatever the tween happened to reach.
const b = await open(printSrc, { settleMs: 2000, reducedMotion: true });

let blocks = 0, figures = 0, reading = null;
try {
  blocks = await b.ev('document.querySelectorAll(".block").length');
  figures = await b.ev('document.querySelectorAll("figure, .fig").length');
  // Read the register back off the rendered page rather than trusting the flag: this is the
  // one check that proves the rewrite actually took.
  reading = await b.ev(
    '(document.querySelector(\'input[name="reading"]:checked\')||{}).value || null');
  const r = await b.send('Page.printToPDF', {
    printBackground: true,
    preferCSSPageSize: true,        // honour @page { size: A4 } instead of guessing at letter
    marginTop: 0, marginBottom: 0, marginLeft: 0, marginRight: 0,
    displayHeaderFooter: false,
    generateTaggedPDF: true,        // structure survives for screen readers
  });
  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, Buffer.from(r.result.data, 'base64'));
} finally {
  await b.close();
  if (temp) { try { fs.unlinkSync(temp); } catch {} }
}

const rows = [];
const add = (level, check, detail) => rows.push({ level, check, detail });
const kb = (fs.statSync(out).size / 1024).toFixed(0);

add('PASS', 'wrote', `${path.relative(process.cwd(), out)} (${kb} KB)`);

if (args.reading) {
  add(reading === args.reading ? 'PASS' : 'FAIL', 'reading',
    reading === args.reading
      ? `${reading} register printed`
      : `asked for ${args.reading}, the page printed ${reading || 'none'} — the register did not switch`);
} else if (reading) {
  add('PASS', 'reading', `${reading} register printed (default)`);
}

// --- link annotations -------------------------------------------------------------------
// Uncompressed annot dicts are the common case for this producer. A compressed object stream
// would undercount, so 0 is reported as "check by hand" rather than as a failure.
const bytes = fs.readFileSync(out).toString('latin1');
const links = (bytes.match(/\/URI\s*\(/g) || []).length;
add(links > 0 ? 'PASS' : 'WARN', 'link annots',
  links > 0 ? `${links} URI annotation(s) survived`
            : 'none found — either the report has no external links, or they did not survive');

// --- geometry and page count ------------------------------------------------------------
if (have('pdfinfo')) {
  const info = run('pdfinfo', [out]);
  const pages = Number((info.match(/^Pages:\s+(\d+)/m) || [])[1] || 0);
  const size = (info.match(/^Page size:\s+([\d.]+) x ([\d.]+)/m) || []);
  const w = Number(size[1] || 0), h = Number(size[2] || 0);

  const isA4 = Math.abs(w - A4_PT.w) <= TOL && Math.abs(h - A4_PT.h) <= TOL;
  add(isA4 ? 'PASS' : 'FAIL', 'A4 geometry',
    isA4 ? `${w} × ${h} pt`
         : `${w} × ${h} pt — expected ${A4_PT.w} × ${A4_PT.h}. @page size is not being honoured`);

  // Blocks are page-safe, so pages should be in the same neighbourhood as blocks. Far more pages
  // than blocks means something is breaking where it should not; far fewer is usually fine
  // (short blocks share a sheet) and is only worth a note.
  add('PASS', 'pages', `${pages} page(s) from ${blocks} block(s), ${figures} figure(s)`);
  if (blocks && pages > blocks * 2.5) {
    add('WARN', 'pagination',
      `${pages} pages for ${blocks} blocks — check for a block breaking mid-figure`);
  }
  if (pages === 0) add('FAIL', 'pages', 'the PDF has no pages');
} else {
  add('WARN', 'pdfinfo', 'poppler not installed — A4 geometry and page count NOT checked (brew install poppler)');
}

// --- transient text in the ink ----------------------------------------------------------
if (have('pdftotext')) {
  const txt = run('pdftotext', [out, '-']);
  const caught = TRANSIENT.filter(re => re.test(txt)).map(String);
  add(caught.length ? 'FAIL' : 'PASS', 'transient text',
    caught.length ? `animation/placeholder text reached the ink: ${caught.join(', ')}`
                  : 'no loading or placeholder text in the printed output');

  const words = (txt.match(/\S+/g) || []).length;
  add(words > 50 ? 'PASS' : 'FAIL', 'text layer',
    `${words} words extractable` + (words > 50 ? '' : ' — the report printed as images, or printed empty'));
} else {
  add('WARN', 'pdftotext', 'poppler not installed — ink contents NOT checked (brew install poppler)');
}

if (args.json) {
  console.log(JSON.stringify({ out, blocks, figures, rows }, null, 2));
} else {
  console.log('\n=== PDF EXPORT ===\n');
  for (const r of rows) {
    const mark = { PASS: 'ok  ', FAIL: 'FAIL', WARN: 'warn' }[r.level];
    console.log(`${mark}  ${r.check.padEnd(16)} ${r.detail}`);
  }
  const fails = rows.filter(r => r.level === 'FAIL').length;
  const warns = rows.filter(r => r.level === 'WARN').length;
  console.log(`\n${fails} error(s), ${warns} warning(s)\n`);
}

process.exit(rows.some(r => r.level === 'FAIL') ? 1 : 0);
