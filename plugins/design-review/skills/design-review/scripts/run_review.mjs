#!/usr/bin/env node
/**
 * run_review.mjs — Obscura equivalent of run_review.py.
 *
 * Same output layout, same manifest shape, so analyze_styles.py and annotate.py
 * read either interchangeably. Both drive the same engine over CDP; pick the
 * language the project already speaks.
 *
 *   node run_review.mjs --url http://localhost:3000 --out ./review-work
 *   node run_review.mjs --url ... --states --tile
 *   node run_review.mjs --url ... --viewports 375,1280
 *
 * Needs `obscura` on PATH and nothing else — Node 22 has a global WebSocket, so
 * the CDP client below has no npm dependency. The script starts its own
 * `obscura serve` and shuts it down again; point it at a running one with
 * --cdp-port if you would rather share a session.
 *
 * A dev server on 127.0.0.1 or localhost is blocked by default, so the serve is
 * started with --allow-private-network. Without it every capture fails as an
 * SSRF block, which reads like a broken page rather than a blocked fetch.
 */

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { spawn, spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const PROBES_JS = path.join(HERE, 'probes.js');

if (spawnSync('obscura', ['--version'], { stdio: 'ignore' }).error) {
  console.error(
    'Obscura is not on PATH.\n' +
    '  download the aarch64-macos release from\n' +
    '  https://github.com/h4ckf0r0day/obscura and put it in ~/.local/bin\n' +
    'If no browser is available at all, say so in the review summary and run the\n' +
    'static checks only — never imply a page was seen.'
  );
  process.exit(1);
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
    motionFrames: 6, motionInterval: 200, cdpPort: null,
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
      case '--cdp-port': a.cdpPort = Number(next()); break;
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

// ---------------------------------------------------------------------------
// Obscura driver. `obscura serve` speaks Chrome-compatible CDP, so a raw
// WebSocket is the whole client — no puppeteer, no playwright, no `ws`.
// ---------------------------------------------------------------------------

async function startObscura(port) {
  const proc = spawn(
    'obscura',
    ['--allow-private-network', 'serve', '--port', String(port), '--quiet'],
    { stdio: ['ignore', 'ignore', 'pipe'] }
  );
  const deadline = Date.now() + 15000;
  while (Date.now() < deadline) {
    try {
      const r = await fetch(`http://127.0.0.1:${port}/json/version`);
      if (r.ok) return proc;
    } catch { /* not up yet */ }
    await sleep(200);
  }
  proc.kill();
  throw new Error(`obscura serve did not come up on port ${port}`);
}

async function connect(port) {
  const version = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json();
  const ws = new WebSocket(version.webSocketDebuggerUrl);
  const pending = new Map();
  const listeners = [];
  ws.addEventListener('message', e => {
    const msg = JSON.parse(e.data);
    if (msg.id && pending.has(msg.id)) {
      const { resolve } = pending.get(msg.id);
      pending.delete(msg.id);
      resolve(msg);
    } else if (msg.method) {
      for (const fn of listeners) fn(msg);
    }
  });
  await new Promise((res, rej) => {
    ws.addEventListener('open', res);
    ws.addEventListener('error', rej);
  });

  let nextId = 0;
  const send = (method, params = {}, sessionId) => new Promise(resolve => {
    const id = ++nextId;
    pending.set(id, { resolve });
    ws.send(JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) }));
  });

  return { ws, send, on: fn => listeners.push(fn), close: () => ws.close() };
}

/**
 * A page: one Obscura target plus the bookkeeping the review needs from it.
 *
 * Obscura does not emit Runtime.consoleAPICalled or Log.entryAdded, so the
 * console gate is served by a page-side hook installed before navigation. It
 * records everything the page's own scripts log plus uncaught errors and
 * rejections. It cannot see browser-emitted subresource failures ("Failed to
 * load resource … 404") — those come from the network list instead, which is
 * why both are written out and why a console count alone is never a finding.
 */
const CONSOLE_HOOK = `
(() => {
  if (window.__drConsole) return;
  window.__drConsole = [];
  const push = (type, text) => { try { window.__drConsole.push({ type, text: String(text).slice(0, 500) }); } catch (e) {} };
  const fmt = v => {
    if (typeof v === 'string') return v;
    if (v instanceof Error) return v.stack || v.message;
    try { return JSON.stringify(v); } catch (e) { return String(v); }
  };
  for (const k of ['log', 'info', 'warn', 'error', 'debug']) {
    const orig = console[k];
    console[k] = (...a) => { push(k, a.map(fmt).join(' ')); if (orig) orig.apply(console, a); };
  }
  addEventListener('error', e => push('pageerror', e.message || e.error));
  addEventListener('unhandledrejection', e => push('pageerror', e.reason));
})();`;

async function newPage(cdp, { width, height, dpr }) {
  const created = await cdp.send('Target.createTarget', { url: 'about:blank' });
  const targetId = created.result?.targetId;
  const attached = await cdp.send('Target.attachToTarget', { targetId, flatten: true });
  const sessionId = attached.result?.sessionId;

  for (const domain of ['Page', 'Runtime', 'Network', 'DOM']) {
    await cdp.send(`${domain}.enable`, {}, sessionId);
  }

  // Failed subresources come from the network list, not the console: Obscura
  // reports an HTTP error as a normal response with a 4xx/5xx status rather
  // than as Network.loadingFailed.
  const failed = [];
  let inflight = 0;
  let lastActivity = Date.now();
  cdp.on(msg => {
    if (msg.sessionId && msg.sessionId !== sessionId) return;
    if (msg.method === 'Network.requestWillBeSent') { inflight++; lastActivity = Date.now(); }
    if (msg.method === 'Network.loadingFinished' || msg.method === 'Network.loadingFailed') {
      inflight = Math.max(0, inflight - 1); lastActivity = Date.now();
    }
    if (msg.method === 'Network.loadingFailed') {
      failed.push({ url: '(unknown)', failure: String(msg.params?.errorText ?? '').slice(0, 200) });
    }
    if (msg.method === 'Network.responseReceived') {
      const r = msg.params?.response ?? {};
      if (r.status >= 400) {
        failed.push({ url: String(r.url ?? '').slice(0, 200), failure: `HTTP ${r.status}` });
      }
    }
  });

  await cdp.send('Page.addScriptToEvaluateOnNewDocument', { source: CONSOLE_HOOK }, sessionId);

  const page = {
    targetId,
    sessionId,
    failed,
    async setViewport(w, h, deviceScaleFactor) {
      await cdp.send('Emulation.setDeviceMetricsOverride',
        { width: w, height: h, deviceScaleFactor, mobile: w <= 480 }, sessionId);
    },
    async goto(url, timeoutMs = 30000) {
      const r = await cdp.send('Page.navigate', { url }, sessionId);
      if (r.error) throw new Error(`navigate failed: ${JSON.stringify(r.error)}`);
      const deadline = Date.now() + timeoutMs;
      while (Date.now() < deadline) {
        const state = await page.evaluate('document.readyState');
        if (state === 'complete' || state === 'interactive') return;
        await sleep(150);
      }
    },
    async evaluate(expression, { awaitPromise = false } = {}) {
      const r = await cdp.send('Runtime.evaluate',
        { expression, returnByValue: true, awaitPromise }, sessionId);
      if (r.error || r.result?.exceptionDetails) return undefined;
      return r.result?.result?.value;
    },
    async consoleMessages() {
      const raw = await page.evaluate('JSON.stringify(window.__drConsole || [])');
      try { return JSON.parse(raw ?? '[]'); } catch { return []; }
    },
    networkQuiet(idleMs) { return inflight === 0 && Date.now() - lastActivity > idleMs; },
    async screenshot(file, { fullPage = false, clip = null } = {}) {
      let params = { format: 'png' };
      if (clip) {
        params.clip = { ...clip, scale: 1 };
        params.captureBeyondViewport = true;
      } else if (fullPage) {
        const m = await cdp.send('Page.getLayoutMetrics', {}, sessionId);
        const size = m.result?.contentSize ?? m.result?.cssContentSize;
        if (size) {
          params.clip = { x: 0, y: 0, width: size.width, height: size.height, scale: 1 };
          params.captureBeyondViewport = true;
        }
      }
      const r = await cdp.send('Page.captureScreenshot', params, sessionId);
      const data = r.result?.data;
      if (!data) return false;
      fs.writeFileSync(file, Buffer.from(data, 'base64'));
      return true;
    },
    /** Element box in viewport coordinates, or null when the selector misses. */
    async boxOf(selector) {
      const raw = await page.evaluate(
        `(() => { const e = document.querySelector(${JSON.stringify(selector)});
          if (!e) return null; const r = e.getBoundingClientRect();
          return JSON.stringify({ x: r.left, y: r.top, width: r.width, height: r.height }); })()`
      );
      return raw ? JSON.parse(raw) : null;
    },
    async mouseMove(x, y) {
      await cdp.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y }, sessionId);
    },
    async pressKey(key, code, keyCode) {
      await cdp.send('Input.dispatchKeyEvent',
        { type: 'keyDown', key, code, windowsVirtualKeyCode: keyCode }, sessionId);
      await cdp.send('Input.dispatchKeyEvent',
        { type: 'keyUp', key, code, windowsVirtualKeyCode: keyCode }, sessionId);
    },
    async close() { await cdp.send('Target.closeTarget', { targetId }); },
  };

  await page.setViewport(width, height, dpr);
  return page;
}

/**
 * Network idle plus an explicit wait for async renderers. Charts and canvas need
 * 2-4s after idle; a screenshot of a half-rendered chart generates a false
 * finding, which costs more than the wait does.
 */
async function waitSettled(page, extraMs) {
  const deadline = Date.now() + 15000;
  while (Date.now() < deadline && !page.networkQuiet(500)) {
    await sleep(150); // polling and websockets never go idle — the deadline ends it
  }
  await page.evaluate('document.fonts && document.fonts.ready', { awaitPromise: true });
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
  await page.evaluate(`(async () => {
      const step = Math.max(200, Math.round(window.innerHeight * 0.8));
      const end = document.documentElement.scrollHeight;
      for (let y = 0; y < end; y += step) {
        window.scrollTo(0, y);
        await new Promise(r => setTimeout(r, 90));
      }
      window.scrollTo(0, 0);
      await new Promise(r => setTimeout(r, 400));
    })()`, { awaitPromise: true });
}

/**
 * Drain running animations, then RETURN how many were still running.
 *
 * Draining is not the point; the returned count is. A gate that samples during
 * an entrance animation reports precise, confident, wrong numbers — on a real
 * run a 400ms-after-scroll axe pass read a `#E85A2A` accent as `#6a2d18` and
 * reported a surface getting worse after a fix that provably removed its
 * failures. Any count above zero invalidates the colour numbers in that row.
 *
 * Obscura does not execute CSS animations or transitions, so under it this
 * returns 0 whatever the page declares. A zero here is therefore the absence of
 * a signal, not proof of settling — which is exactly why the summary says so
 * rather than printing a clean row.
 */
async function proveSettled(page, timeoutMs = 5000) {
  const v = await page.evaluate(`(async () => {
      const deadline = Date.now() + ${timeoutMs};
      const running = () => (document.getAnimations ? document.getAnimations() : [])
        .filter(a => a.playState === 'running');
      while (Date.now() < deadline && running().length) {
        await new Promise(r => setTimeout(r, 100));
      }
      return running().length;
    })()`, { awaitPromise: true });
  return typeof v === 'number' ? v : -1;
}

async function captureViewport(cdp, url, width, height, out, settleMs, tile, dpr) {
  const page = await newPage(cdp, { width, height, dpr });

  await page.goto(url);
  await waitSettled(page, settleMs);
  await revealPass(page);
  const stillRunning = await proveSettled(page);

  const tag = `${width}x${height}`;
  for (const d of ['shots', 'probes', 'console']) mkdir(path.join(out, d));

  await page.screenshot(path.join(out, 'shots', `${tag}-fold.png`));
  await page.screenshot(path.join(out, 'shots', `${tag}-full.png`), { fullPage: true });

  await page.evaluate(fs.readFileSync(PROBES_JS, 'utf8'));
  const probes = JSON.parse(
    await page.evaluate('JSON.stringify(window.__designReviewProbes.runAll())')
  );
  fs.writeFileSync(path.join(out, 'probes', `${tag}.json`), JSON.stringify(probes, null, 2));

  const console_ = await page.consoleMessages();
  fs.writeFileSync(
    path.join(out, 'console', `${tag}.json`),
    JSON.stringify({ messages: console_, failedRequests: page.failed }, null, 2)
  );

  const tiles = [];
  if (tile) {
    // Never feed a monolithic full-page scroll to a vision model: extreme aspect
    // ratios hit image-token compression limits. Tile instead.
    mkdir(path.join(out, 'tiles'));
    const total = await page.evaluate('document.documentElement.scrollHeight');
    let offset = 0, idx = 0;
    while (offset < total && idx < 30) {
      await page.evaluate(`window.scrollTo(0, ${offset})`);
      await sleep(220);
      const name = `${tag}-tile-${String(idx).padStart(2, '0')}.png`;
      await page.screenshot(path.join(out, 'tiles', name));
      tiles.push(name);
      offset += height;
      idx += 1;
    }
    await page.evaluate('window.scrollTo(0, 0)');
  }

  const errors = console_.filter(m => m.type === 'error' || m.type === 'pageerror');
  const result = {
    viewport: tag,
    dpr,
    shots: { fold: `${tag}-fold.png`, full: `${tag}-full.png` },
    tiles,
    // Settling proof on an engine that runs animations. Obscura does not, so a
    // zero here means "no signal" — see proveSettled.
    animationsRunningAtMeasure: stillRunning,
    elementsBelowFullOpacity: probes.settled.partiallyTransparentElements,
    consoleErrorCount: errors.length,
    failedRequestCount: page.failed.length,
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
             (L.implicitTracks ? L.implicitTracks.spilledRows.length + L.implicitTracks.emptyCells.length : 0) +
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
async function captureStates(cdp, url, out, settleMs, selectors) {
  const page = await newPage(cdp, { width: 1280, height: 900, dpr: DPR_DETAIL });
  await page.goto(url);
  await waitSettled(page, settleMs);
  mkdir(path.join(out, 'states'));

  const captured = [];
  const skipped = [];
  const sels = selectors?.length ? selectors : ['button', 'a[href]', 'input', '[role="button"]'];

  for (const sel of sels) {
    const box = await page.boxOf(sel);
    if (!box || box.width <= 0 || box.height <= 0) continue;
    const safe = sel.replace(/[[\]'" ]/g, '_').slice(0, 30);

    await page.evaluate(
      `document.querySelector(${JSON.stringify(sel)}).scrollIntoView({ block: 'center' })`);
    await sleep(150);
    const rest = await page.boxOf(sel);
    if (!rest) continue;
    const clip = { x: rest.x, y: rest.y, width: rest.width, height: rest.height };

    await page.mouseMove(0, 0);
    await sleep(150);
    let name = `${safe}-rest.png`;
    await page.screenshot(path.join(out, 'states', name), { clip });
    captured.push(name);

    await page.mouseMove(rest.x + rest.width / 2, rest.y + rest.height / 2);
    await sleep(400); // let the transition finish
    name = `${safe}-hover.png`;
    await page.screenshot(path.join(out, 'states', name), { clip });
    captured.push(name);

    await page.pressKey('Tab', 'Tab', 9);
    await sleep(200);
    name = `${safe}-focus-page.png`;
    await page.screenshot(path.join(out, 'states', name));
    captured.push(name);
  }

  // Reduced motion and print are two at-rest checks that catch content which
  // only exists because an animation ran. Obscura accepts
  // Emulation.setEmulatedMedia and then ignores it — matchMedia and the cascade
  // do not change — so capturing here would write the ordinary rendering under
  // a name claiming otherwise. Record the gap instead; a review that shows a
  // screen-media screenshot labelled `page-print.png` is worse than one that
  // says the check did not run.
  skipped.push('page-reduced-motion.png (Obscura cannot emulate prefers-reduced-motion)');
  skipped.push('page-print.png (Obscura cannot emulate print media)');

  await page.close();
  return { captured, skipped };
}

async function main() {
  const args = parseArgs(process.argv);

  if (args.url.startsWith('file://')) {
    console.error(
      'WARNING: file:// breaks module scripts, fetches and some fonts. ' +
      'Serve over HTTP instead (python3 -m http.server).'
    );
  }

  if (args.motion) {
    console.error(
      'ERROR: --motion is unavailable under Obscura. It does not execute CSS\n' +
      'animations or transitions — a declared `animation: fade 3s` never advances\n' +
      'and document.getAnimations() reports none — so the frames would be N copies\n' +
      'of one still. Report the motion pass as not performed rather than reading a\n' +
      'mid-flight defect off identical frames.'
    );
    process.exit(1);
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

  const manifest = { url: args.url, viewports: [], states: [], statesSkipped: [], motion: [] };

  const port = args.cdpPort ?? 9200 + Math.floor(Math.random() * 300);
  const server = args.cdpPort ? null : await startObscura(port);
  const cdp = await connect(port);

  try {
    for (const [w, h] of sizes) {
      console.error(`  capturing ${w}x${h} ...`);
      manifest.viewports.push(
        await captureViewport(cdp, args.url, w, h, out, args.settleMs, args.tile, args.dpr)
      );
    }

    if (args.states) {
      console.error('  staging interaction states ...');
      const sels = args.stateSelectors ? args.stateSelectors.split(',').map(s => s.trim()) : [];
      const staged = await captureStates(cdp, args.url, out, args.settleMs, sels);
      manifest.states = staged.captured;
      manifest.statesSkipped = staged.skipped;
    }
  } finally {
    cdp.close();
    if (server) server.kill();
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

  if (manifest.statesSkipped.length) {
    console.log('\nNot captured:');
    for (const s of manifest.statesSkipped) console.log(`  ${s}`);
  }

  console.log('\nObscura does not run CSS animations or transitions, so');
  console.log('animationsRunningAtMeasure is 0 on every row whatever the page declares.');
  console.log('That zero is the absence of a signal, not proof the surface had settled —');
  console.log('any finding that turns on entrance timing needs a different engine.');

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
