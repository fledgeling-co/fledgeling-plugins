// mockup-fidelity CAPTURE HARNESS (v2.5.0) — the Node-side orchestrator around the browser-injectable
// analyze.js. It adds the trustworthy RENDERED signals that a getComputedStyle dump (and therefore
// analyze.js alone) structurally cannot provide:
//
//   1. ELEMENT-SCOPED RASTER DIFF (odiff).  A full-page screenshot is captured per side; each PAIRED element
//      (paired by analyze.js MODE B's structure — text/structure pairing, plus the v2.5.0 IoU text-less
//      pairing) is cropped from both screenshots by its bounding box and the two equal-size crops are run
//      through odiff. A localized mismatch% with computed styles MATCHING ⇒ a layout/occlusion/rendering
//      anomaly the DOM passes are blind to — most importantly a MISSING DECORATIVE CHILD (a trailing → svg,
//      a divider, an icon) the structure pass passed because both element boxes exist.
//
//   2. IoU TEXT-LESS PAIRING.  analyze.js pairs by text + structural path; a bare <svg> / icon / decorative
//      div has no text. After the normal pairing we pair the remaining text-less nodes across sides by
//      Intersection-over-Union of bounding boxes (≥0.9), so an arrow/icon becomes a paired candidate the
//      raster + presence checks can evaluate.
//
// WHAT THIS HARNESS NO LONGER DOES — the CDP RENDERED-FONT layer. It used `CSS.getPlatformFontsForNode` to
// record the ACTUAL rendered typeface per text node, which caught the headline case: live resolves to its
// loaded web font ("Inter Medium", isCustomFont:true) while the target silently falls back to the system
// face ("Helvetica", isCustomFont:false) with getComputedStyle font-family still listing Inter first on BOTH
// sides. Obscura cannot support that check at any level:
//   · `CSS.getPlatformFontsForNode` returns `{}`, and `DOM.requestNode` — the only route from a Text node to
//     a nodeId — is not implemented;
//   · more fundamentally, Obscura DOES NOT LOAD WEB FONTS. A working remote woff2 and a 404'd one measure
//     identically, `document.fonts` reports every @font-face as `unloaded` forever, and named families
//     collapse onto three generic metric buckets (Georgia==serif, Arial==Impact==sans-serif, Courier
//     New==monospace).
// So the FONT class is not measurable here at all, and the harness reports the layer as UNAVAILABLE rather
// than reporting zero divergences — a silent zero on this layer reads as "the fonts match", which is the
// exact defect the layer existed to catch. Confirm typeface identity in a real browser.
//
// All of this is orchestrated HERE in Node (obscura + odiff-bin) because a real full-page screenshot and the
// per-element crops are unreachable from inside a single injected eval. analyze.js's injectable MODE A/B
// contract is UNCHANGED — this harness injects it verbatim and consumes its JSON, then ENRICHES the findings
// with bbox-delta + odiff mismatch% where relevant.
//
// RASTER DETERMINISM: Obscura is one static binary rasterising the same way on every machine, so glyph-edge
// noise is stable without a hinting flag. NOTE (documented in run.md): stable is not the same as faithful.
// It is a Rust engine, not packaged Chrome, and a raster mismatch is a TRIGGER to go and measure, never on
// its own the verdict that the target is wrong.
//
// USAGE:
//   node capture.mjs --ref <refURL|file> --target <targetURL|file> --out <dir> [options]
//     --ref       reference (LIVE rendered URL, e.g. https://diolog.app/) — required
//     --target    target (e.g. http://diolog.site/) — required
//     --out       output directory for artifacts (created if absent) — required
//     --analyze   path to analyze.js (default: ./analyze.js next to this file)
//     --width     viewport width (default 1280)
//     --height    viewport height (default 2000)
//     --frame-selector / --frame-title / --frame-index  forwarded to analyze.js __MF_OPTS__
//     --chrome-selector  forwarded (default '__none__' for web↔web so app chrome is measured)
//     --iou       IoU threshold for text-less pairing (default 0.9)
//     --raster-min  minimum element area (px²) to raster-diff (default 64; skips 1px slivers)
//     --raster-max  max paired elements to raster-diff (default 600; protects runtime)
//     --no-raster   skip the odiff raster layer (analyze.js only)
//     --cdp-port    attach to an `obscura serve` already running instead of starting one
//     --assert      EXIT NONZERO on a result that is not a clean, complete pass. This is the whole
//                   point of the flag: the blocking gate used to be prose an agent graded itself
//                   against, and the skill's own evidence says prose loses to effort pressure while
//                   programmatic artifact-forcing wins. Three-valued, because a check that could not
//                   run is neither a pass nor a fail:
//                     0  clean AND complete — no high findings, every detector class could run
//                     1  FINDINGS — at least one high-severity finding
//                     2  usage / fatal error (unchanged)
//                     3  INCONCLUSIVE — a detector class the verdict depends on could not run in this
//                        engine. Distinct from 1 on purpose: 1 means "these differ", 3 means "nobody
//                        asked". Pass --allow-inconclusive to downgrade 3 to 0 once every silenced
//                        class has been checked elsewhere and recorded in the ledger.
//     --allow-inconclusive  treat an inconclusive class as acceptable (exit 0/1 only). Use it ONLY
//                   after each class in `inconclusive[]` has been confirmed in a real browser and the
//                   ledger records where. It is not a way to make the number go green.
//
// OUTPUT (in --out):
//   reference.analysis.json   MODE-A analysis of the reference
//   target.findings.json      MODE-B { summary, findings, noiseExcluded, analysis } ENRICHED with
//                             raster blocks + summary.layers
//   reference.full.png        full-page reference screenshot (raster source)
//   target.full.png           full-page target screenshot (raster source)
//   raster/*.png              per-element diff crops for raster findings (diff masks)

import { compare } from 'odiff-bin';
import { spawn, spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join, resolve, isAbsolute } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));

if (spawnSync('obscura', ['--version'], { stdio: 'ignore' }).error) {
  console.error('ERROR: obscura is not on PATH. Download the aarch64-macos release from\n' +
                '       https://github.com/h4ckf0r0day/obscura and put it in ~/.local/bin');
  process.exit(2);
}


// ---------- arg parsing ----------
function parseArgs(argv) {
  const a = {};
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    if (!k.startsWith('--')) continue;
    const name = k.slice(2);
    const next = argv[i + 1];
    if (next == null || next.startsWith('--')) { a[name] = true; }
    else { a[name] = next; i++; }
  }
  return a;
}
const args = parseArgs(process.argv.slice(2));
const ASSERT = !!args.assert;
const ALLOW_INCONCLUSIVE = !!args['allow-inconclusive'];
let EXIT_CODE = 0;
function need(name) {
  if (args[name] == null || args[name] === true) {
    console.error(`ERROR: --${name} is required`);
    process.exit(2);
  }
  return args[name];
}

const REF = need('ref');
const TARGET = need('target');
const OUT = resolve(need('out'));
const ANALYZE_PATH = args.analyze ? resolve(String(args.analyze)) : join(__dirname, 'analyze.js');
const VW = parseInt(args.width ?? '1280', 10);
const VH = parseInt(args.height ?? '2000', 10);
const IOU_THRESHOLD = parseFloat(args.iou ?? '0.9');
const RASTER_MIN_AREA = parseInt(args['raster-min'] ?? '64', 10);
const RASTER_MAX = parseInt(args['raster-max'] ?? '600', 10);
const DO_RASTER = !args['no-raster'];
const CHROME_SELECTOR = args['chrome-selector'] ?? '__none__';
const CDP_PORT = args['cdp-port'] ? parseInt(String(args['cdp-port']), 10) : null;

if (!existsSync(ANALYZE_PATH)) { console.error(`ERROR: analyze.js not found at ${ANALYZE_PATH}`); process.exit(2); }
mkdirSync(OUT, { recursive: true });
const RASTER_DIR = join(OUT, 'raster');
if (DO_RASTER) mkdirSync(RASTER_DIR, { recursive: true });

const ANALYZE_SRC = readFileSync(ANALYZE_PATH, 'utf8');

// resolve a ref/target that may be a URL or a local file path → a goto-able target.
function toNavTarget(s) {
  if (/^https?:\/\//i.test(s) || /^file:\/\//i.test(s)) return s;
  // a local file path
  const p = isAbsolute(s) ? s : resolve(s);
  return 'file://' + p;
}

// ---------- Obscura driver ----------
// `obscura serve` speaks Chrome-compatible CDP, so a raw WebSocket is the whole client — Node 22 has a
// global WebSocket, and there is no browser package to install. --allow-private-network is not optional:
// a target on 127.0.0.1 or a 192.168.* host is blocked by default and the navigation fails as an SSRF
// block, which reads like a broken page rather than a blocked fetch.
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function startObscura(port) {
  const proc = spawn('obscura', ['--allow-private-network', 'serve', '--port', String(port), '--quiet'],
    { stdio: 'ignore' });
  const deadline = Date.now() + 15000;
  while (Date.now() < deadline) {
    try { if ((await fetch(`http://127.0.0.1:${port}/json/version`)).ok) return proc; } catch (e) {}
    await sleep(200);
  }
  proc.kill();
  throw new Error(`obscura serve did not come up on port ${port}`);
}

async function connectCdp(port) {
  const version = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json();
  const ws = new WebSocket(version.webSocketDebuggerUrl);
  const pending = new Map();
  ws.addEventListener('message', (e) => {
    const msg = JSON.parse(e.data);
    if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
  });
  await new Promise((res, rej) => { ws.addEventListener('open', res); ws.addEventListener('error', rej); });
  let nextId = 0;
  const send = (method, params = {}, sessionId) => new Promise((resolve) => {
    const id = ++nextId;
    pending.set(id, resolve);
    ws.send(JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) }));
  });
  return { send, close: () => ws.close() };
}

// A page: one Obscura target with just the surface this harness uses. `evaluate` takes an EXPRESSION
// string rather than a function, which is what analyze.js already expects — it is an async IIFE whose
// source IS the expression.
async function newPage(cdp, { width, height }) {
  const created = await cdp.send('Target.createTarget', { url: 'about:blank' });
  const targetId = created.result?.targetId;
  const attached = await cdp.send('Target.attachToTarget', { targetId, flatten: true });
  const sessionId = attached.result?.sessionId;
  for (const domain of ['Page', 'Runtime', 'DOM']) await cdp.send(`${domain}.enable`, {}, sessionId);
  if (width && height) {
    await cdp.send('Emulation.setDeviceMetricsOverride',
      { width, height, deviceScaleFactor: 1, mobile: false }, sessionId);
  }
  const page = {
    sessionId,
    async goto(url, timeoutMs = 45000) {
      const r = await cdp.send('Page.navigate', { url }, sessionId);
      if (r.error) throw new Error(`navigate failed: ${JSON.stringify(r.error)}`);
      const deadline = Date.now() + timeoutMs;
      while (Date.now() < deadline) {
        if (await page.evaluate('document.readyState') === 'complete') return;
        await sleep(150);
      }
    },
    async evaluate(expression) {
      const r = await cdp.send('Runtime.evaluate',
        { expression, returnByValue: true, awaitPromise: true }, sessionId);
      if (r.error) throw new Error(JSON.stringify(r.error));
      if (r.result?.exceptionDetails) {
        throw new Error(r.result.exceptionDetails.exception?.description
          || r.result.exceptionDetails.text || 'evaluate threw');
      }
      return r.result?.result?.value;
    },
    async fullPageScreenshot(file) {
      const m = await cdp.send('Page.getLayoutMetrics', {}, sessionId);
      const size = m.result?.contentSize ?? m.result?.cssContentSize;
      const params = { format: 'png' };
      if (size) {
        params.clip = { x: 0, y: 0, width: size.width, height: size.height, scale: 1 };
        params.captureBeyondViewport = true;
      }
      const r = await cdp.send('Page.captureScreenshot', params, sessionId);
      const data = r.result?.data;
      if (!data) return false;
      writeFileSync(file, Buffer.from(data, 'base64'));
      return true;
    },
    async close() { await cdp.send('Target.closeTarget', { targetId }); },
  };
  return page;
}

// ---------- analyze.js injection (MODE A / MODE B) ----------
// analyze.js is an `(async function(){…})()` IIFE that READS globals and RETURNS a JSON string. We set the
// globals first, then evaluate the IIFE source as an expression and await it — Runtime.evaluate with
// awaitPromise:true resolves the returned promise, so the JSON comes back in one round trip.
async function runAnalyze(page, { reference } = {}) {
  await page.evaluate(
    `(() => {
      globalThis.__MF_OPTS__ = ${JSON.stringify(buildOpts())};
      globalThis.__MF_REFERENCE__ = ${JSON.stringify(reference ?? null)};
      globalThis.__MF_REFERENCE_BYWIDTH__ = null;
      globalThis.__MF_TARGET_BYWIDTH__ = null;
    })()`,
  );
  // analyze.js source IS the IIFE expression (it ends with `})()`), so evaluating it returns the promise.
  const raw = await page.evaluate(ANALYZE_SRC);
  let v = raw;
  if (typeof v === 'string') { try { v = JSON.parse(v); } catch (e) { /* leave as string */ } }
  return v;
}

function buildOpts() {
  const o = { chromeSelector: CHROME_SELECTOR };
  if (args['frame-selector']) o.frameSelector = String(args['frame-selector']);
  if (args['frame-title']) o.frameTitle = String(args['frame-title']);
  if (args['frame-index']) o.frameIndex = parseInt(String(args['frame-index']), 10);
  return o;
}

// ---------- frame origin (for screenshot↔analysis coordinate mapping) ----------
// analyze.js records each node's rect as FRAME-RELATIVE (x/y relative to the frame root's top-left). For the
// raster crop we need VIEWPORT/page coordinates. We read the frame root's bounding rect in page coords here,
// using the SAME frame-selection logic analyze.js uses, so node.rect.{x,y} + frameOrigin = page coords.
async function readFrameOrigin(page) {
  return await page.evaluate(`((opts) => {
    const SEL = opts.frameSelector;
    const TITLE = opts.frameTitle;
    const INDEX = opts.frameIndex;
    const FRAME_SEL = 'figure, .frame';
    const CAP_SEL = 'figcaption, .cap';
    const ROOT_PROBES = ['.scr', '.screen', '.frame', '.phone'];
    const screenOf = (fig) => {
      if (!fig) return null;
      for (const s of ROOT_PROBES) { const hit = fig.querySelector(s); if (hit) return hit; }
      return fig;
    };
    let root;
    if (SEL) root = document.querySelector(SEL);
    else if (INDEX != null) root = screenOf([...document.querySelectorAll(FRAME_SEL)][INDEX - 1]);
    else if (TITLE) {
      const fig = [...document.querySelectorAll(FRAME_SEL)].find(
        (f) => ((f.querySelector(CAP_SEL) || {}).textContent || '').replace(/\\s+/g, ' ').includes(TITLE),
      );
      root = screenOf(fig);
    } else root = document.body;
    if (!root) return { x: 0, y: 0, found: false };
    const r = root.getBoundingClientRect();
    // page (document) coords = client rect + scroll offset
    return { x: r.left + (window.scrollX || 0), y: r.top + (window.scrollY || 0), found: true, dpr: window.devicePixelRatio || 1 };
  })(${JSON.stringify(buildOpts())})`);
}

// ======================================================================
// SIDE CAPTURE — one page: analyze.js + frame origin + screenshot
// ======================================================================
async function captureSide(cdp, navTarget, { reference, label } = {}) {
  const page = await newPage(cdp, { width: VW, height: VH });
  try {
    await page.goto(navTarget);
    try { await page.evaluate('document.fonts && document.fonts.ready'); } catch (e) {}
    await sleep(2500);

    const analysis = await runAnalyze(page, { reference });
    const frameOrigin = await readFrameOrigin(page);

    let pngPath = null;
    if (DO_RASTER) {
      pngPath = join(OUT, `${label}.full.png`);
      await page.fullPageScreenshot(pngPath);
    }
    return { analysis, frameOrigin, pngPath };
  } finally {
    await page.close();
  }
}


// ======================================================================
// MODE-B PAIRING REPLAY — recover {mock node, target node} pairs from analyze.js's analyses.
// ======================================================================
// analyze.js computes the pairing internally but only surfaces findings (with a TARGET locator), not the
// explicit pair list. We re-derive the same pairing chain here (fid → tag+text → structural path), then ADD
// the v2.5.0 IoU TEXT-LESS pairing for the remaining bare svg/icon/decorative-div nodes. The result is the
// list of element pairs the raster + font layers operate on. (This intentionally mirrors analyze.js's
// `matchedPairs`; we replicate it rather than change analyze.js's contract.)
function normText(s) { return String(s ?? '').replace(/\s+/g, ' ').trim(); }
function buildKidsPath(nodes) {
  const kids = new Map();
  for (const n of nodes) { if (!kids.has(n.parent)) kids.set(n.parent, []); kids.get(n.parent).push(n); }
  const byIndex = new Map(nodes.map((n) => [n.i, n]));
  const pathOf = (n) => {
    const parts = []; let cur = n, hops = 0;
    while (cur && cur.parent >= 0 && hops++ < 40) {
      const sibs = kids.get(cur.parent) || [];
      parts.unshift(`${cur.tag}[${sibs.indexOf(cur)}]`);
      cur = byIndex.get(cur.parent);
    }
    return parts.join('/');
  };
  return { kids, byIndex, pathOf };
}
function iou(a, b) {
  if (!a || !b) return 0;
  const ax2 = a.x + a.w, ay2 = a.y + a.h, bx2 = b.x + b.w, by2 = b.y + b.h;
  const ix = Math.max(0, Math.min(ax2, bx2) - Math.max(a.x, b.x));
  const iy = Math.max(0, Math.min(ay2, by2) - Math.max(a.y, b.y));
  const inter = ix * iy;
  if (inter <= 0) return 0;
  const union = a.w * a.h + b.w * b.h - inter;
  return union > 0 ? inter / union : 0;
}
function buildPairs(refAnalysis, tgtAnalysis) {
  const mock = refAnalysis.nodes || [];
  const app = tgtAnalysis.nodes || [];
  const pairs = []; // { mock, app, via }
  const usedApp = new Set();
  const take = (m, a, via) => { if (a && !usedApp.has(a.i)) { pairs.push({ mock: m, app: a, via }); usedApp.add(a.i); return true; } return false; };

  // (0) fid
  const byFid = new Map(); for (const a of app) if (a.fid) byFid.set(a.fid, a);
  for (const m of mock) if (m.fid && byFid.has(m.fid)) take(m, byFid.get(m.fid), 'fid');
  const paired = new Set(pairs.map((p) => p.mock.i));

  // (1) tag + normalised text
  const byText = new Map();
  for (const a of app) { const t = normText(a.text).slice(0, 60); if (t.length < 2) continue; const k = a.tag + '|' + t; if (!byText.has(k)) byText.set(k, []); byText.get(k).push(a); }
  for (const m of mock) {
    if (paired.has(m.i)) continue;
    const t = normText(m.text).slice(0, 60); if (t.length < 2) continue;
    const cand = (byText.get(m.tag + '|' + t) || []).find((a) => !usedApp.has(a.i));
    if (take(m, cand, 'text')) paired.add(m.i);
  }

  // (2) structural path
  const mp = buildKidsPath(mock), ap = buildKidsPath(app);
  const byPath = new Map(); for (const a of app) { const p = ap.pathOf(a); if (!byPath.has(p)) byPath.set(p, a); }
  for (const m of mock) {
    if (paired.has(m.i)) continue;
    const cand = byPath.get(mp.pathOf(m));
    if (take(m, cand, 'path')) paired.add(m.i);
  }

  // (3) v2.5.0 — IoU TEXT-LESS pairing for the remaining bare svg/icon/decorative-div nodes.
  //     Pair remaining unpaired TEXT-LESS mock nodes to unpaired TEXT-LESS app nodes by bbox IoU ≥ threshold.
  const isTextless = (n) => !normText(n.text) && (n.rect?.w || 0) > 0 && (n.rect?.h || 0) > 0;
  const textlessApp = app.filter((a) => isTextless(a) && !usedApp.has(a.i));
  let iouPaired = 0;
  for (const m of mock) {
    if (paired.has(m.i) || !isTextless(m)) continue;
    let best = null, bestIoU = 0;
    for (const a of textlessApp) {
      if (usedApp.has(a.i)) continue;
      const ov = iou(m.rect, a.rect);
      if (ov > bestIoU) { bestIoU = ov; best = a; }
    }
    if (best && bestIoU >= IOU_THRESHOLD) {
      if (take(m, best, 'iou')) { paired.add(m.i); iouPaired++; }
    }
  }
  return { pairs, iouPaired };
}

// ======================================================================
// RASTER LAYER — crop each paired element from both full-page PNGs and odiff the equal-size crops.
// ======================================================================
// We crop each full-page PNG by re-opening it in a fresh data-URL page and slicing it on a <canvas>. That
// keeps deps to obscura + odiff only (no sharp / no native image lib), and odiff needs each side's crop as
// its own PNG file. (Runtime.evaluate interpolations in this file are only JSON-stringified NUMBERS —
// frame-origin coords and node indices — never untrusted strings, so there is no injection path; the
// analyze.js source string passed to page.evaluate is read from disk and is the trusted skill asset.)
async function cropFromPng(cdp, pngPath, rect, dpr, outPath) {
  // rect is in PAGE coordinates (frame-relative + frameOrigin already applied by caller). Screenshot pixels
  // are page-px × dpr; with deviceScaleFactor:1 dpr==1, so page coords == screenshot px.
  const page = await newPage(cdp, {});
  try {
    const dataUrl = 'data:image/png;base64,' + readFileSync(pngPath).toString('base64');
    const cropUrl = await page.evaluate(`(async (url, r, scale) => {
      const img = new Image();
      await new Promise((res, rej) => { img.onload = res; img.onerror = rej; img.src = url; });
      const sx = Math.max(0, Math.round(r.x * scale));
      const sy = Math.max(0, Math.round(r.y * scale));
      const sw = Math.max(1, Math.round(r.w * scale));
      const sh = Math.max(1, Math.round(r.h * scale));
      const c = document.createElement('canvas');
      c.width = sw; c.height = sh;
      const g = c.getContext('2d');
      g.drawImage(img, sx, sy, sw, sh, 0, 0, sw, sh);
      return c.toDataURL('image/png');
    })(${JSON.stringify(dataUrl)}, ${JSON.stringify(rect)}, ${JSON.stringify(dpr || 1)})`);
    if (!cropUrl) return false;
    const b64 = String(cropUrl).split(',')[1];
    writeFileSync(outPath, Buffer.from(b64, 'base64'));
    return true;
  } finally {
    await page.close();
  }
}

async function rasterLayer(cdp, pairs, refSide, tgtSide) {
  const refOrigin = refSide.frameOrigin || { x: 0, y: 0, dpr: 1 };
  const tgtOrigin = tgtSide.frameOrigin || { x: 0, y: 0, dpr: 1 };
  const refDpr = refOrigin.dpr || 1, tgtDpr = tgtOrigin.dpr || 1;
  // candidate pairs: both rects sized, area ≥ min, sort by area desc and cap.
  const cands = pairs.pairs
    .filter((p) => p.mock.rect && p.app.rect && p.mock.rect.w > 0 && p.mock.rect.h > 0 && p.app.rect.w > 0 && p.app.rect.h > 0)
    .filter((p) => (p.mock.rect.w * p.mock.rect.h) >= RASTER_MIN_AREA)
    .sort((a, b) => (b.mock.rect.w * b.mock.rect.h) - (a.mock.rect.w * a.mock.rect.h))
    .slice(0, RASTER_MAX);

  const results = []; // { pairIndex, via, ref/app rects, match, mismatchPct, diffPath, classifiedAs, sizeMismatch }
  let i = 0;
  for (const p of cands) {
    i++;
    // crop dimensions must match for a meaningful pixel-diff. We crop each side at its own rect, then odiff
    // with failOnLayoutDiff:false so a small size mismatch reports a real pixel-diff% rather than refusing.
    const refRect = { x: (refOrigin.x || 0) + p.mock.rect.x, y: (refOrigin.y || 0) + p.mock.rect.y, w: p.mock.rect.w, h: p.mock.rect.h };
    const tgtRect = { x: (tgtOrigin.x || 0) + p.app.rect.x, y: (tgtOrigin.y || 0) + p.app.rect.y, w: p.app.rect.w, h: p.app.rect.h };
    const refCrop = join(RASTER_DIR, `pair-${i}-ref.png`);
    const tgtCrop = join(RASTER_DIR, `pair-${i}-tgt.png`);
    const diffCrop = join(RASTER_DIR, `pair-${i}-diff.png`);
    let okR = false, okT = false;
    try { okR = await cropFromPng(cdp, refSide.pngPath, refRect, refDpr, refCrop); } catch (e) {}
    try { okT = await cropFromPng(cdp, tgtSide.pngPath, tgtRect, tgtDpr, tgtCrop); } catch (e) {}
    if (!okR || !okT) continue;
    let res;
    try {
      res = await compare(refCrop, tgtCrop, diffCrop, { failOnLayoutDiff: false, outputDiffMask: false, antialiasing: true });
    } catch (e) { res = { match: null, reason: 'odiff-error', error: String(e && e.message || e) }; }
    const sizeMismatch = !(Math.abs(p.mock.rect.w - p.app.rect.w) <= 1 && Math.abs(p.mock.rect.h - p.app.rect.h) <= 1);
    const mismatchPct = typeof res.diffPercentage === 'number' ? +res.diffPercentage.toFixed(2) : null;
    results.push({
      pairIndex: i, via: p.via,
      mockI: p.mock.i, appI: p.app.i,
      tag: p.app.tag, text: normText(p.app.text).slice(0, 48) || null,
      refRect: { x: +refRect.x.toFixed(1), y: +refRect.y.toFixed(1), w: refRect.w, h: refRect.h },
      tgtRect: { x: +tgtRect.x.toFixed(1), y: +tgtRect.y.toFixed(1), w: tgtRect.w, h: tgtRect.h },
      match: res.match === true,
      mismatchPct, reason: res.reason || null, sizeMismatch,
      diffPath: res.match === false ? diffCrop : null,
    });
  }
  return results;
}

// ======================================================================
// FONT LAYER — UNAVAILABLE under Obscura, and reported as such rather than as zero divergences.
// ======================================================================
// The layer paired reference vs target CDP rendered fonts and emitted a finding when the genuinely-RENDERED
// typeface differed — a custom face on one side, a system fallback on the other. Obscura cannot answer the
// question at any level (see the header): the CDP call returns nothing, and web fonts never load, so both
// sides fall back identically and every comparison would agree. An agreeing comparison here is precisely the
// wrong answer, so nothing is compared and the summary carries the reason instead.
const FONT_LAYER_UNAVAILABLE = {
  available: false,
  reason: 'Obscura does not load web fonts and CSS.getPlatformFontsForNode returns nothing. Typeface '
        + 'identity cannot be measured here — confirm it in a real browser.',
  compared: 0,
};

// ======================================================================
// ENRICHMENT — fold the raster layer into the analyze.js findings payload (the deterministic
// "diff-as-instruction" shape): each finding carries bbox-delta + odiff mismatch% where relevant. We ADD
// new findings for the raster class and ATTACH raster evidence onto existing findings whose locator targets
// the same element box.
// ======================================================================
function enrich(modeB, rasterResults, pairs) {
  // Defensive: modeB may be an error or a bare analysis (MODE A) if injection was dropped.
  if (!modeB || !modeB.findings) {
    return { ...(modeB || {}), _harnessNote: 'MODE-B result missing findings; raster layer attached separately', renderedFont: FONT_LAYER_UNAVAILABLE, raster: rasterResults };
  }
  const findings = modeB.findings;
  let nextId = findings.length;
  const newFindings = [];

  // ---- ELEMENT-SCOPED RASTER findings — visual diffs the DOM passes are blind to ----
  // Classify per the research:
  //   · odiff mismatch + computed-style MATCHES ⇒ layout/occlusion/rendering anomaly (incl. a missing
  //     decorative child the DOM passed). Localized small-element ⇒ likely a style/glyph diff.
  // We only EMIT a raster finding above a meaningful threshold so antialiased text edges don't flood.
  const RASTER_FIND_PCT = 12; // % — below this, a crop diff is edge/antialias noise (odiff antialiasing:true already suppresses most)
  // index existing findings by the target element index they reference (via locator bbox heuristics is
  // unreliable; instead we map appI → whether any non-raster finding already exists for it).
  const findingTargetText = new Set(findings.map((x) => normText(String(x.locator || '')).toLowerCase()));
  for (const r of (rasterResults || [])) {
    if (r.match !== false || r.mismatchPct == null || r.mismatchPct < RASTER_FIND_PCT) continue;
    // a size mismatch (the two element boxes differ in size) is itself a geometry finding analyze.js already
    // emits; the raster value here CORROBORATES it. A SAME-SIZE box with a high pixel-diff and no other
    // finding is the interesting case — a missing decorative child / occlusion / rendering anomaly.
    const classifiedAs = r.sizeMismatch
      ? 'geometry/occlusion (element boxes differ in size — corroborates a geometry/wrap finding)'
      : 'rendering-anomaly (same-size box, pixels differ — a missing decorative child / occlusion / glyph or paint difference the DOM passes did not catch)';
    const sev = r.sizeMismatch ? 'med' : 'high';
    newFindings.push({
      id: 'mf-raster-' + (++nextId),
      locator: `${r.tag}${r.text ? ` "${r.text}"` : ''}  ·  @${Math.round(r.tgtRect.x)},${Math.round(r.tgtRect.y)} ${r.tgtRect.w}×${r.tgtRect.h}`,
      section: null,
      class: 'raster',
      property: 'element-raster-diff',
      target: `${r.mismatchPct}% pixels differ`,
      reference: '0% (pixel-identical crop)',
      deltaPx: r.sizeMismatch ? Math.round(Math.max(Math.abs(r.refRect.w - r.tgtRect.w), Math.abs(r.refRect.h - r.tgtRect.h))) : undefined,
      severity: sev,
      raster: {
        mismatchPct: r.mismatchPct,
        classifiedAs,
        sizeMismatch: r.sizeMismatch,
        pairedVia: r.via,
        refRect: r.refRect, targetRect: r.tgtRect,
        diffImage: r.diffPath,
      },
      bboxDelta: { dw: +(r.tgtRect.w - r.refRect.w).toFixed(1), dh: +(r.tgtRect.h - r.refRect.h).toFixed(1) },
      suggestedChange: r.sizeMismatch
        ? `this element's box differs in size (${r.refRect.w}×${r.refRect.h} ref vs ${r.tgtRect.w}×${r.tgtRect.h} target) AND its rendered pixels differ ${r.mismatchPct}% — confirm the geometry/wrap finding for this element and re-check after fixing the size`
        : `this element's box is the SAME size on both sides but its rendered pixels differ by ${r.mismatchPct}% — inspect ${r.diffPath} (the diff crop). The DOM passes matched it, so the difference is a MISSING DECORATIVE CHILD (a trailing → svg, a divider, an icon), an occlusion, or a paint/glyph difference. Add/restore whatever the reference draws here that the target does not.`,
    });
  }

  // ---- merge + re-sort + re-summarise ----
  const allFindings = findings.concat(newFindings);
  const sevRank = { high: 0, med: 1, low: 2 };
  allFindings.sort((a, b) => (sevRank[a.severity] - sevRank[b.severity]) || ((b.deltaPx || 0) - (a.deltaPx || 0)));
  const byClass = {}; for (const f of allFindings) byClass[f.class] = (byClass[f.class] || 0) + 1;
  const bySev = { high: 0, med: 0, low: 0 }; for (const f of allFindings) bySev[f.severity]++;
  const penalty = bySev.high * 5 + bySev.med * 2 + bySev.low * 0.5;
  const score = Math.max(1, Math.round(100 * Math.exp(-penalty / 900)));

  return {
    summary: {
      ...(modeB.summary || {}),
      score,
      totalFindings: allFindings.length,
      bySeverity: bySev,
      byClass,
      layers: {
        analyze: (modeB.findings || []).length,
        cdpRenderedFont: FONT_LAYER_UNAVAILABLE,
        raster: { pairsCompared: (rasterResults || []).length, mismatches: (rasterResults || []).filter((r) => r.match === false).length, emitted: newFindings.filter((f) => f.class === 'raster').length },
        iouTextlessPairs: pairs.iouPaired,
      },
    },
    findings: allFindings,
    // Carried through verbatim. The harness re-summarises severities and score, and an earlier version
    // of this function dropped `inconclusive` on the floor while `summary.conclusive` still said false —
    // so the artifact disagreed with itself and the assert fell through to the findings branch. The
    // three-valued outcome only works if the third value survives every layer that touches the object.
    inconclusive: modeB.inconclusive || [],
    noiseExcluded: modeB.noiseExcluded || {},
    rasterDetail: rasterResults || [],
    analysis: modeB.analysis,
  };
}

// ======================================================================
// MAIN
// ======================================================================
async function main() {
  const t0 = Date.now();
  const port = CDP_PORT ?? 9200 + Math.floor(Math.random() * 300);
  const server = CDP_PORT ? null : await startObscura(port);
  const cdp = await connectCdp(port);
  try {
    // (1) reference — MODE A
    console.error('[mf] capturing reference:', REF);
    const refSide = await captureSide(cdp, toNavTarget(REF), { reference: null, label: 'reference' });
    if (refSide.analysis?.error) { console.error('[mf] reference analyze error:', refSide.analysis.error); }
    writeFileSync(join(OUT, 'reference.analysis.json'), JSON.stringify(refSide.analysis));

    // (2) target — MODE B (inject the reference analysis)
    console.error('[mf] capturing target:', TARGET);
    const tgtSide = await captureSide(cdp, toNavTarget(TARGET), { reference: refSide.analysis, label: 'target' });

    const modeB = tgtSide.analysis;
    if (modeB?.error) console.error('[mf] MODE-B error:', modeB.error);

    // (3) pairs (replay analyze.js pairing + IoU text-less)
    let pairs = { pairs: [], iouPaired: 0 };
    if (refSide.analysis?.nodes && (modeB?.analysis?.nodes || modeB?.nodes)) {
      const tgtAnalysis = modeB.analysis?.nodes ? modeB.analysis : modeB;
      pairs = buildPairs(refSide.analysis, tgtAnalysis);
    }
    console.error('[mf] pairs:', pairs.pairs.length, '(', pairs.iouPaired, 'via IoU text-less )');

    console.error('[mf] font layer: UNAVAILABLE —', FONT_LAYER_UNAVAILABLE.reason);

    // (4) raster layer
    let rasterResults = [];
    if (DO_RASTER && refSide.pngPath && tgtSide.pngPath && pairs.pairs.length) {
      rasterResults = await rasterLayer(cdp, pairs, refSide, tgtSide);
      const mm = rasterResults.filter((r) => r.match === false).length;
      const emitted = rasterResults.filter((r) => r.match === false && (r.mismatchPct ?? 0) >= 12).length;
      console.error('[mf] raster pairs diffed:', rasterResults.length, 'mismatches:', mm, '· above the 12% emit threshold:', emitted);
      // A BARE ZERO HERE IS THE MOST MISREAD NUMBER IN THE RUN, and a blind judge panel named it as such
      // in the rebuilt report: "zero pixel mismatches across a page missing an entire card means the
      // raster comparator is broken, not that the pixels agree." Two reasons it is weak evidence on this
      // engine, both of which have to travel WITH the number rather than live in a doc:
      //   · every text crop is drawn in a FALLBACK face on both sides, because no web font loads — so the
      //     crops are stable and comparable but not faithful, and a genuine typographic difference is
      //     invisible to them;
      //   · a pair only gets diffed if analyze.js paired it. A missing element is UNPAIRED, so the crop
      //     that would have shown its absence was never taken. The raster layer is blind to exactly the
      //     defect class people most expect it to catch.
      if (mm === 0) {
        console.error('[mf]   NOTE 0 raster mismatches is not evidence the pixels agree. Only PAIRED elements');
        console.error('[mf]   are cropped, so a missing element is never rastered; and no web font loads here, so');
        console.error('[mf]   every text crop is a fallback face on both sides. Read this as "no extra signal",');
        console.error('[mf]   never as "the rendering matches".');
      }
    }

    // (5) enrich + write
    const enriched = enrich(modeB, rasterResults, pairs);
    writeFileSync(join(OUT, 'target.findings.json'), JSON.stringify(enriched));

    console.error('[mf] done in', ((Date.now() - t0) / 1000).toFixed(1) + 's',
      '· score', enriched.summary?.score, '· findings', enriched.summary?.totalFindings,
      '· layers', JSON.stringify(enriched.summary?.layers || {}));
    console.error('[mf] wrote:', join(OUT, 'target.findings.json'));

    // ---- THE PREFLIGHT REPORT ------------------------------------------------------------
    // Printed on every run, not only under --assert, because the number a reader takes away is
    // "0 findings" and this is the sentence that says what those 0 findings cover. The reason
    // strings are relayed VERBATIM: each one names the engine and what it actually returned, and a
    // paraphrase is what turns "this layer cannot run here" into "the shadows match".
    const inconclusive = enriched.inconclusive || [];
    if (inconclusive.length) {
      console.error('');
      console.error('[mf] ⚠ ' + inconclusive.length + ' DETECTOR CLASS' + (inconclusive.length === 1 ? '' : 'ES') + ' COULD NOT RUN IN THIS ENGINE.');
      console.error('[mf]   These are NOT passes. Zero findings in a silenced class means the question was never asked.');
      for (const inc of inconclusive) {
        console.error('[mf]   · ' + inc.capability + ' — silences: ' + inc.detectors.join(', '));
        console.error('[mf]     ' + inc.reason);
      }
      console.error('[mf]   Confirm each of these in a real browser and record where in the ledger.');
      if (enriched.summary?.scoreCaveat) console.error('[mf]   SCORE CAVEAT: ' + enriched.summary.scoreCaveat);
      console.error('');
    } else {
      console.error('[mf] preflight: every detector class ran (no inconclusive classes).');
    }

    if (ASSERT) {
      const high = enriched.summary?.bySeverity?.high || 0;
      if (inconclusive.length && !ALLOW_INCONCLUSIVE) {
        console.error('[mf] ASSERT FAIL (3) — INCONCLUSIVE: ' + inconclusive.length + ' detector class(es) could not run. This is not a pass.');
        EXIT_CODE = 3;
      } else if (high > 0) {
        console.error('[mf] ASSERT FAIL (1) — ' + high + ' high-severity finding(s).');
        EXIT_CODE = 1;
      } else {
        console.error('[mf] ASSERT PASS (0) — no high findings, and every detector class the verdict depends on ran.');
        EXIT_CODE = 0;
      }
    }
  } finally {
    cdp.close();
    if (server) server.kill();
  }
}

main()
  .then(() => { if (EXIT_CODE) process.exit(EXIT_CODE); })
  .catch((e) => { console.error('FATAL', e && e.stack || e); process.exit(2); });
