// feature-check.mjs (v2.1.0) — RUNNER step for the RENDERED-GLYPH-SHAPE / font-feature-effectiveness
// self-check, used ONLY when the engine's canvas lacks `ctx.fontFeatureSettings` (the current case).
//
// NOT USABLE UNDER OBSCURA. Obscura does not load web fonts at all — a working remote woff2 and a 404'd
// one measure identically, and every @font-face stays `unloaded` — so the on/off probe pairs render the
// same fallback face on both rows and every pair comes back identical. Identical here MEANS "the feature
// is ineffective", so running this against an Obscura screenshot reports every requested feature as a
// defect, confidently and wrongly. Capture the page in a real browser when this check is wanted; there is
// no Obscura-side substitute, because the signal is the rasterised glyph of a font it never fetched.
//
// WHY a runner step. A requested OpenType feature (cv11 single-story 'a', ss01, onum, …) can be DECLARED
// and the font can APPLY, yet have NO EFFECT because the self-hosted woff2 is a SUBSET that STRIPPED that
// feature's glyph — and the single-vs-default letterform is the SAME WIDTH, so width / DOM-span / glyph-
// extent checks are structurally blind. The only signal is the rasterised glyph SHAPE. analyze.js can do
// this fully in-page IF canvas exposes `fontFeatureSettings`; the engines in use do NOT (analyze.js tests
// `'fontFeatureSettings' in ctx` and falls back to this runner path). In the fallback, analyze.js MODE A
// rendered persistent on-screen probe PAIRS (the requested-ffs row directly above the `normal` row, same
// family/size/weight) and recorded each pair's on/off rects in `analysis.featureCheck.probes`. This script
// screenshots the page, pixel-diffs each on/off pair, and emits a verdict map `{ key, effective }`:
//   identical pair (≈0% different pixels) ⇒ the requested feature is INEFFECTIVE (font lacks the glyph);
//   different pair                        ⇒ effective.
// Inject the result back via `globalThis.__MF_FEATURE_DIFFS__` (per side) and re-run analyze.js MODE B so
// it emits the `font/feature-ineffective` finding inline (and escalates when the reference IS effective).
//
//   # 1) capture MODE A (leaves the probe host in the page) → analysis json (has featureCheck.probes)
//   # 2) screenshot the page at the SAME viewport, from a browser that loads web fonts
//   # 3) pixel-diff the probe pairs:
//   node feature-check.mjs --analysis target.json --png page.png --out target-featdiffs.json
//   #    → [{ key, effective, pctDifferent }]  (effective:false = INEFFECTIVE feature, the defect)
//
// Zero dependencies — decodes a non-interlaced 8-bit PNG with node:zlib.

import { readFileSync, writeFileSync } from 'node:fs';
import zlib from 'node:zlib';

function arg(name, def) {
  const i = process.argv.indexOf('--' + name);
  return i >= 0 ? process.argv[i + 1] : def;
}

function decodePNG(path) {
  const b = readFileSync(path);
  if (b.readUInt32BE(0) !== 0x89504e47) throw new Error('not a PNG: ' + path);
  let off = 8, w = 0, h = 0, bitDepth = 0, colorType = 0;
  const idat = [];
  while (off < b.length) {
    const len = b.readUInt32BE(off);
    const type = b.toString('ascii', off + 4, off + 8);
    const data = b.subarray(off + 8, off + 8 + len);
    if (type === 'IHDR') { w = data.readUInt32BE(0); h = data.readUInt32BE(4); bitDepth = data[8]; colorType = data[9]; }
    else if (type === 'IDAT') idat.push(data);
    else if (type === 'IEND') break;
    off += 12 + len;
  }
  if (bitDepth !== 8) throw new Error('unsupported bitDepth ' + bitDepth);
  const channels = colorType === 6 ? 4 : colorType === 2 ? 3 : colorType === 0 ? 1 : colorType === 4 ? 2 : 0;
  if (!channels) throw new Error('unsupported colorType ' + colorType);
  const raw = zlib.inflateSync(Buffer.concat(idat));
  const stride = w * channels;
  const out = Buffer.alloc(h * stride);
  const paeth = (a, bb, c) => { const p = a + bb - c, pa = Math.abs(p - a), pb = Math.abs(p - bb), pc = Math.abs(p - c); return pa <= pb && pa <= pc ? a : pb <= pc ? bb : c; };
  let pos = 0;
  for (let y = 0; y < h; y++) {
    const f = raw[pos++];
    for (let x = 0; x < stride; x++) {
      const rb = raw[pos++];
      const a = x >= channels ? out[y * stride + x - channels] : 0;
      const up = y > 0 ? out[(y - 1) * stride + x] : 0;
      const ul = (x >= channels && y > 0) ? out[(y - 1) * stride + x - channels] : 0;
      let v;
      if (f === 0) v = rb; else if (f === 1) v = rb + a; else if (f === 2) v = rb + up;
      else if (f === 3) v = rb + ((a + up) >> 1); else if (f === 4) v = rb + paeth(a, up, ul); else v = rb;
      out[y * stride + x] = v & 0xff;
    }
  }
  return { w, h, channels, data: out };
}

// luminance at a pixel
const lum = (img, x, y) => {
  if (x < 0 || y < 0 || x >= img.w || y >= img.h) return 255;
  const i = (y * img.w + x) * img.channels;
  if (img.channels >= 3) return (img.data[i] + img.data[i + 1] + img.data[i + 2]) / 3;
  return img.data[i];
};

// diff two equal-size rects (on vs off) by overlaying; returns pct of pixels whose luminance differs > thr.
function rectDiff(img, on, off, dpr, thr = 28) {
  const W = Math.round(Math.min(on.w, off.w) * dpr), H = Math.round(Math.min(on.h, off.h) * dpr);
  const ox = Math.round(on.x * dpr), oy = Math.round(on.y * dpr);
  const fx = Math.round(off.x * dpr), fy = Math.round(off.y * dpr);
  let diff = 0, total = 0, ink = 0;
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    total++;
    const a = lum(img, ox + x, oy + y), b = lum(img, fx + x, fy + y);
    if (a < 200 || b < 200) ink++;
    if (Math.abs(a - b) > thr) diff++;
  }
  return { pctDifferent: +(100 * diff / Math.max(1, total)).toFixed(3), diffPixels: diff, total, inkPixels: ink };
}

const analysisPath = arg('analysis');
const pngPath = arg('png');
const outPath = arg('out');
if (!analysisPath || !pngPath) {
  console.error('usage: node feature-check.mjs --analysis <analysis.json> --png <page.png> [--out verdicts.json] [--dpr N] [--threshold-pct P]');
  process.exit(2);
}
let analysis = JSON.parse(readFileSync(analysisPath, 'utf8'));
if (typeof analysis === 'string') analysis = JSON.parse(analysis);
if (analysis.analysis && analysis.analysis.featureCheck) analysis = analysis.analysis; // a MODE-B result
const fc = analysis.featureCheck;
if (!fc || !fc.ran) { console.error('no featureCheck.ran in analysis — page requests no OpenType features, nothing to check'); writeFileSync(outPath || 'featdiffs.json', '[]'); process.exit(0); }
if (fc.mechanism !== 'runner-screenshot' || !fc.probes || !fc.probes.length) {
  // canvas path already resolved effectiveness in-page; nothing for the runner to do.
  console.error('featureCheck resolved in-page (' + fc.mechanism + ') — no runner pixel-diff needed');
  writeFileSync(outPath || 'featdiffs.json', JSON.stringify(fc.combos.map(c => ({ key: c.key, effective: c.effective })), null, 2));
  process.exit(0);
}

const img = decodePNG(pngPath);
const dpr = +arg('dpr', fc.dpr || (img.w >= 2000 ? 2 : 1));
const minInk = 4;                       // a pair with almost no ink is not a usable probe
const effThresholdPct = +arg('threshold-pct', 0.4); // > this %-of-pixels-different ⇒ EFFECTIVE
const verdicts = [];
for (const p of fc.probes) {
  const combo = fc.combos[p.idx];
  const d = rectDiff(img, p.onRect, p.offRect, dpr);
  const effective = d.inkPixels < minInk ? null : d.pctDifferent > effThresholdPct;
  verdicts.push({ key: p.key, idx: p.idx, features: combo && combo.features, first: combo && combo.first, effective, pctDifferent: d.pctDifferent, inkPixels: d.inkPixels });
}
const out = JSON.stringify(verdicts, null, 2);
if (outPath) writeFileSync(outPath, out);
const ineffective = verdicts.filter(v => v.effective === false);
console.error(`feature-check: ${verdicts.length} combo(s); ${ineffective.length} INEFFECTIVE (font lacks the requested glyph): ` + ineffective.map(v => (v.features || []).join('+') + '@' + v.first).join(', '));
if (!outPath) console.log(out);
