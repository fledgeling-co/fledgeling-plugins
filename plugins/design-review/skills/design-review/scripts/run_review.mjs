#!/usr/bin/env node
/**
 * run_review.mjs — Puppeteer equivalent of run_review.py.
 *
 * Same output layout, same manifest shape, so analyze_styles.py and annotate.py
 * read either interchangeably. Use whichever browser stack the project already
 * has; there is no reason to install a second one.
 *
 *   npm i puppeteer
 *   node run_review.mjs --url http://localhost:3000 --out ./review-work
 *   node run_review.mjs --url ... --states --motion --tile
 *   node run_review.mjs --url ... --viewports 375,1280
 *
 * Puppeteer-core with an existing Chrome also works:
 *   node run_review.mjs --url ... --executable-path "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
 */

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const PROBES_JS = path.join(HERE, 'probes.js');

let puppeteer;
try {
  puppeteer = (await import('puppeteer')).default;
} catch {
  try {
    puppeteer = (await import('puppeteer-core')).default;
  } catch {
    console.error(
      'Puppeteer is not installed.\n' +
      '  npm i puppeteer        (bundles Chromium)\n' +
      '  npm i puppeteer-core   (then pass --executable-path)\n' +
      'If no browser automation is available at all, say so in the review summary\n' +
      'and run the static checks only — never imply a page was seen.'
    );
    process.exit(1);
  }
}

// The review matrix. 375 is the true stress test; breakpoint transitions break
// more often than breakpoints, hence the in-between widths.
const DEFAULT_VIEWPORTS = [
  [375, 812], [600, 900], [768, 1024], [1024, 900], [1280, 900], [1920, 1080],
];

const DPR_OVERVIEW = 1;
const DPR_DETAIL = 2;

function parseArgs(argv) {
  const a = {
    url: null, out: './review-work', viewports: null, settleMs: 2500,
    dpr: DPR_OVERVIEW, tile: false, states: false, stateSelectors: null,
    motion: false, motionSelector: 'body', motionClass: 'seen',
    motionFrames: 6, motionInterval: 200, executablePath: null,
  };
  for (let i = 2; i < argv.length; i++) {
    const k = argv[i];
    const next = () => argv[++i];
    switch (k) {
      case '--url': a.url = next(); break;
      case '--out': a.out = next(); break;
      case '--viewports': a.viewports = next(); break;
      case '--settle-ms': a.settleMs = Number(next()); break;
      case '--dpr': a.dpr = Number(next()); break;
      case '--tile': a.tile = true; break;
      case '--states': a.states = true; break;
      case '--state-selectors': a.stateSelectors = next(); break;
      case '--motion': a.motion = true; break;
      case '--motion-selector': a.motionSelector = next(); break;
      case '--motion-class': a.motionClass = next(); break;
      case '--motion-frames': a.motionFrames = Number(next()); break;
      case '--motion-interval': a.motionInterval = Number(next()); break;
      case '--executable-path': a.executablePath = next(); break;
      default:
        console.error(`Unknown argument: ${k}`);
        process.exit(1);
    }
  }
  if (!a.url) { console.error('--url is required'); process.exit(1); }
  return a;
}

const sleep = ms => new Promise(r => setTimeout(r, ms));
const mkdir = p => fs.mkdirSync(p, { recursive: true });

/**
 * Network idle plus an explicit wait for async renderers. Charts and canvas need
 * 2-4s after idle; a screenshot of a half-rendered chart generates a false
 * finding, which costs more than the wait does.
 */
async function waitSettled(page, extraMs) {
  try {
    await page.waitForNetworkIdle({ idleTime: 500, timeout: 15000 });
  } catch { /* polling and websockets never go idle — carry on */ }
  try {
    await page.evaluate(() => document.fonts && document.fonts.ready);
  } catch { /* no font API */ }
  await sleep(extraMs);
}

/**
 * Scroll the whole document, then return to the top, before probing.
 *
 * Two defect classes hide behind a page that was never scrolled, and both have
 * been misreported as real findings: a scroll-reveal system leaves every band
 * below the fold at opacity 0, so a load-time capture reads as a blank page;
 * and `loading="lazy"` images have naturalWidth 0 until they enter the viewport,
 * so an image probe reports five of eight as broken.
 */
async function revealPass(page) {
  try {
    await page.evaluate(async () => {
      const step = Math.max(200, Math.round(window.innerHeight * 0.8));
      const end = document.documentElement.scrollHeight;
      for (let y = 0; y < end; y += step) {
        window.scrollTo(0, y);
        await new Promise(r => setTimeout(r, 90));
      }
      window.scrollTo(0, 0);
      await new Promise(r => setTimeout(r, 400));
    });
  } catch { /* no document — carry on */ }
}

/**
 * Drain running animations, then RETURN how many were still running.
 *
 * Draining is not the point; the returned count is. A gate that samples during
 * an entrance animation reports precise, confident, wrong numbers — on a real
 * run a 400ms-after-scroll axe pass read a `#E85A2A` accent as `#6a2d18` and
 * reported a surface getting worse after a fix that provably removed its
 * failures. Any count above zero invalidates the colour numbers in that row.
 */
async function proveSettled(page, timeoutMs = 5000) {
  try {
    return await page.evaluate(async (timeout) => {
      const deadline = Date.now() + timeout;
      const running = () => (document.getAnimations ? document.getAnimations() : [])
        .filter(a => a.playState === 'running');
      while (Date.now() < deadline && running().length) {
        await new Promise(r => setTimeout(r, 100));
      }
      return running().length;
    }, timeoutMs);
  } catch { return -1; }
}

function attachLogging(page) {
  const console_ = [];
  const failed = [];
  page.on('console', m => console_.push({ type: m.type(), text: m.text().slice(0, 500) }));
  page.on('pageerror', e => console_.push({ type: 'pageerror', text: String(e).slice(0, 500) }));
  page.on('requestfailed', r => failed.push({
    url: r.url().slice(0, 200),
    failure: (r.failure()?.errorText ?? '').slice(0, 200),
  }));
  return { console_, failed };
}

async function captureViewport(browser, url, width, height, out, settleMs, tile, dpr) {
  const page = await browser.newPage();
  await page.setViewport({ width, height, deviceScaleFactor: dpr });
  const { console_, failed } = attachLogging(page);

  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await waitSettled(page, settleMs);
  await revealPass(page);
  const stillRunning = await proveSettled(page);

  const tag = `${width}x${height}`;
  for (const d of ['shots', 'probes', 'console']) mkdir(path.join(out, d));

  await page.screenshot({ path: path.join(out, 'shots', `${tag}-fold.png`) });
  await page.screenshot({ path: path.join(out, 'shots', `${tag}-full.png`), fullPage: true });

  await page.addScriptTag({ content: fs.readFileSync(PROBES_JS, 'utf8') });
  const probes = await page.evaluate(() => window.__designReviewProbes.runAll());
  fs.writeFileSync(path.join(out, 'probes', `${tag}.json`), JSON.stringify(probes, null, 2));

  fs.writeFileSync(
    path.join(out, 'console', `${tag}.json`),
    JSON.stringify({ messages: console_, failedRequests: failed }, null, 2)
  );

  const tiles = [];
  if (tile) {
    // Never feed a monolithic full-page scroll to a vision model: extreme aspect
    // ratios hit image-token compression limits. Tile instead.
    mkdir(path.join(out, 'tiles'));
    const total = await page.evaluate(() => document.documentElement.scrollHeight);
    let offset = 0, idx = 0;
    while (offset < total && idx < 30) {
      await page.evaluate(y => window.scrollTo(0, y), offset);
      await sleep(220);
      const name = `${tag}-tile-${String(idx).padStart(2, '0')}.png`;
      await page.screenshot({ path: path.join(out, 'tiles', name) });
      tiles.push(name);
      offset += height;
      idx += 1;
    }
    await page.evaluate(() => window.scrollTo(0, 0));
  }

  const errors = console_.filter(m => m.type === 'error' || m.type === 'pageerror');
  const result = {
    viewport: tag,
    dpr,
    shots: { fold: `${tag}-fold.png`, full: `${tag}-full.png` },
    tiles,
    // Settling proof. Any non-zero value here invalidates every colour number in
    // this row — do not report them, re-measure.
    animationsRunningAtMeasure: stillRunning,
    elementsBelowFullOpacity: probes.settled.partiallyTransparentElements,
    consoleErrorCount: errors.length,
    failedRequestCount: failed.length,
    pageOverflowsHorizontally: probes.overflow.pageOverflowsHorizontally,
    escapingElementCount: probes.overflow.escaping.length,
    // Numerator AND denominator. `contrastFailureCount: 0` on its own cannot be
    // told apart from a probe that never ran.
    contrastFailureCount: probes.contrast.filter(c => 'ratio' in c).length,
    contrastExamined: probes.contrastExamined,
    layoutFindingCount: (() => {
      const L = probes.layout; if (!L) return 0;
      return L.shapeMismatch.length + L.columnDrift.length + L.columnHeaderAlignment.length +
             L.touchingHeadings.length + L.textOverlap.length + L.deadSpace.length +
             (L.columnVoids ? L.columnVoids.voids.length : 0) +
             L.affordance.unactionableRows.length + L.affordance.pointerCursorNotFocusable.length +
             L.tokenOverload.length + (L.rails.exceedsThreshold ? 1 : 0);
    })(),
    componentTypeCount: probes.layout ? probes.layout.inventory.distinctTypes : null,
    targetsBelowAA: probes.targets.filter(t => t.belowAA).length,
    heavyCropImages: probes.images.filter(i => i.heavyCrop).length,
    // WCAG 2.4.2 Page Titled is Level A and is the cheapest gate in the set.
    missingTitle: !(probes.semantics.title || '').trim(),
    unconsumedTokenCount: probes.tokens
      ? probes.tokens.unconsumed.filter(t => 'token' in t).length : 0,
  };
  await page.close();
  return result;
}

/**
 * Stage interaction states deliberately. Hover contaminates a selected-state
 * capture unless the pointer moves away first, so each state is isolated.
 */
async function captureStates(browser, url, out, settleMs, selectors) {
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900, deviceScaleFactor: DPR_DETAIL });
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await waitSettled(page, settleMs);
  mkdir(path.join(out, 'states'));

  const captured = [];
  const sels = selectors?.length ? selectors : ['button', 'a[href]', 'input', '[role="button"]'];

  for (const sel of sels) {
    try {
      const el = await page.$(sel);
      if (!el) continue;
      const safe = sel.replace(/[[\]'" ]/g, '_').slice(0, 30);

      await el.scrollIntoView();
      await page.mouse.move(0, 0);
      await sleep(150);
      let name = `${safe}-rest.png`;
      await el.screenshot({ path: path.join(out, 'states', name) });
      captured.push(name);

      await el.hover();
      await sleep(400); // let the transition finish
      name = `${safe}-hover.png`;
      await el.screenshot({ path: path.join(out, 'states', name) });
      captured.push(name);

      await page.keyboard.press('Tab');
      await sleep(200);
      name = `${safe}-focus-page.png`;
      await page.screenshot({ path: path.join(out, 'states', name) });
      captured.push(name);
    } catch { continue; }
  }

  // Two at-rest checks that catch content which only exists because an
  // animation ran.
  try {
    await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);
    await page.reload({ waitUntil: 'domcontentloaded' });
    await waitSettled(page, settleMs);
    await page.screenshot({ path: path.join(out, 'states', 'page-reduced-motion.png'), fullPage: true });
    captured.push('page-reduced-motion.png');
  } catch { /* feature emulation unsupported */ }

  try {
    await page.emulateMediaFeatures([]);
    await page.emulateMediaType('print');
    await page.reload({ waitUntil: 'domcontentloaded' });
    await waitSettled(page, settleMs);
    await page.screenshot({ path: path.join(out, 'states', 'page-print.png'), fullPage: true });
    captured.push('page-print.png');
  } catch { /* print emulation unsupported */ }
  finally {
    try { await page.emulateMediaType('screen'); } catch { /* ignore */ }
  }

  await page.close();
  return captured;
}

/**
 * Mid-flight frames. Every static check reads the DOM at rest, where an
 * entrance has finished and a transient overlay is invisible. A whole class of
 * defect lives in neither state.
 */
async function captureMotion(browser, url, out, settleMs, selector, triggerClass, frames, intervalMs) {
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900, deviceScaleFactor: DPR_DETAIL });
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await waitSettled(page, settleMs);
  mkdir(path.join(out, 'motion'));

  await page.evaluate(([sel, cls]) => {
    const el = document.querySelector(sel);
    if (!el) return false;
    el.classList.remove(cls);
    void el.offsetWidth;      // force reflow — this restarts the animation
    el.classList.add(cls);
    return true;
  }, [selector, triggerClass]);

  const captured = [];
  for (let i = 0; i < frames; i++) {
    const name = `frame-t${String(i * intervalMs).padStart(3, '0')}.png`;
    await page.screenshot({ path: path.join(out, 'motion', name) });
    captured.push(name);
    await sleep(intervalMs);
  }

  await page.close();
  return captured;
}

async function main() {
  const args = parseArgs(process.argv);

  if (args.url.startsWith('file://')) {
    console.error(
      'WARNING: file:// breaks module scripts, fetches and some fonts. ' +
      'Serve over HTTP instead (python3 -m http.server).'
    );
  }

  const out = path.resolve(args.out);
  mkdir(out);

  const defaults = new Map(DEFAULT_VIEWPORTS);
  const sizes = args.viewports
    ? args.viewports.split(',').map(w => {
        const width = Number(w.trim());
        return [width, defaults.get(width) ?? 900];
      })
    : DEFAULT_VIEWPORTS;

  const manifest = { url: args.url, viewports: [], states: [], motion: [] };

  const launchOpts = { headless: 'new' };
  if (args.executablePath) launchOpts.executablePath = args.executablePath;
  const browser = await puppeteer.launch(launchOpts);

  try {
    for (const [w, h] of sizes) {
      console.error(`  capturing ${w}x${h} ...`);
      manifest.viewports.push(
        await captureViewport(browser, args.url, w, h, out, args.settleMs, args.tile, args.dpr)
      );
    }

    if (args.states) {
      console.error('  staging interaction states ...');
      const sels = args.stateSelectors ? args.stateSelectors.split(',').map(s => s.trim()) : [];
      manifest.states = await captureStates(browser, args.url, out, args.settleMs, sels);
    }

    if (args.motion) {
      console.error('  capturing mid-flight frames ...');
      manifest.motion = await captureMotion(
        browser, args.url, out, args.settleMs,
        args.motionSelector, args.motionClass, args.motionFrames, args.motionInterval
      );
    }
  } finally {
    await browser.close();
  }

  fs.writeFileSync(path.join(out, 'manifest.json'), JSON.stringify(manifest, null, 2));

  console.log(`\nCaptured to ${out}`);
  console.log('\nPer viewport:');
  for (const v of manifest.viewports) {
    const flags = [];
    if (v.animationsRunningAtMeasure) {
      flags.push(`NOT SETTLED (${v.animationsRunningAtMeasure} animations running)`);
    }
    if (v.pageOverflowsHorizontally) flags.push('H-OVERFLOW');
    if (v.missingTitle) flags.push('NO <title> (WCAG 2.4.2, Level A)');
    if (v.consoleErrorCount) flags.push(`${v.consoleErrorCount} console errors`);
    flags.push(`contrast ${v.contrastFailureCount}/${v.contrastExamined} examined`);
    if (v.targetsBelowAA) flags.push(`${v.targetsBelowAA} targets <24px`);
    if (v.heavyCropImages) flags.push(`${v.heavyCropImages} heavy-crop images`);
    if (v.layoutFindingCount) flags.push(`${v.layoutFindingCount} layout findings`);
    if (v.unconsumedTokenCount) flags.push(`${v.unconsumedTokenCount} declared-but-unread tokens`);
    console.log(`  ${v.viewport.padStart(10)}  ${flags.join(' · ')}`);
  }

  if (manifest.viewports.some(v => v.animationsRunningAtMeasure)) {
    console.log('\nWARNING: at least one viewport was measured while animations were still');
    console.log('running. Colour and contrast numbers from those rows are not usable — a');
    console.log('mid-entrance sample reads a partially-composited colour as a real one.');
    console.log('Re-run with a longer --settle-ms before reporting any of them.');
  }

  const types = manifest.viewports.map(v => v.componentTypeCount).filter(n => n != null);
  if (types.length) {
    console.log(`\n${Math.max(...types)} distinct component types found. That is the`);
    console.log('denominator for the report\'s Coverage block — crop and open them in');
    console.log('priority order (layout-flagged, interactive, >=3 instances, task path).');
  }

  console.log('\nCaptures are evidence only once opened. Read the crops before');
  console.log('reporting anything about them. A clean gate run is not a verdict');
  console.log('on the design; it says no known computable defect is present.');
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
