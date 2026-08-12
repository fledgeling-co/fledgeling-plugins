// harness.mjs — serve a report, drive an isolated headless Chrome over CDP, tear down cleanly.
//
// Node 22+ only (native WebSocket, native fetch). Zero npm dependencies, on purpose: a skill's
// scripts have to run in a bare checkout with no install step, on a machine that has never seen
// this repo before.
//
// It serves the report's own directory over http (never file://, where relative assets and fonts
// behave differently from how they will in a browser), launches its OWN Chrome with its OWN temp
// profile on its OWN port, and kills only what it started. A Chrome you happened to have open is
// never touched.
//
// Taken from the report skill's harness, which solved this problem first.

import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import net from 'node:net';
import os from 'node:os';

const MIME = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8', '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp',
  '.woff2': 'font/woff2', '.woff': 'font/woff', '.avif': 'image/avif',
};

function freePort() {
  return new Promise((res, rej) => {
    const s = net.createServer();
    s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => res(p)); });
    s.on('error', rej);
  });
}

const CHROME_CANDIDATES = [
  process.env.CHROME_BIN,
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser',
].filter(Boolean);

function findChrome() {
  for (const c of CHROME_CANDIDATES) if (fs.existsSync(c)) return c;
  throw new Error(
    'No Chrome found. Set CHROME_BIN to a Chrome/Chromium binary.\n' +
    'Without it the PDF cannot be produced — this is a hard stop, not a degraded pass.'
  );
}

/**
 * Open a report for inspection or printing.
 * @param {string} file  path to the .html file
 * @param {object} opts  { width, height, dpr, settleMs, reducedMotion, media }
 * @returns {Promise<object>} { url, ev, send, shot, close }
 */
export async function open(file, opts = {}) {
  const {
    width = 1280, height = 900, dpr = 1, settleMs = 1500,
    reducedMotion = false, media = null,
  } = opts;

  const abs = path.resolve(file);
  if (!fs.existsSync(abs)) throw new Error(`No such file: ${abs}`);
  const dir = path.dirname(abs);
  const base = path.basename(abs);

  const httpPort = await freePort();
  const server = createServer((req, res) => {
    const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, '');
    const target = path.join(dir, rel || base);
    // Contain the served tree: a report must not be able to read outside its own directory.
    if (!target.startsWith(dir) || !fs.existsSync(target) || fs.statSync(target).isDirectory()) {
      res.writeHead(404).end('not found'); return;
    }
    res.writeHead(200, {
      'Content-Type': MIME[path.extname(target)] || 'application/octet-stream',
      'Cache-Control': 'no-store',   // a stale cache lies to you, and you chase a ghost for an hour
    });
    fs.createReadStream(target).pipe(res);
  });
  await new Promise(r => server.listen(httpPort, '127.0.0.1', r));

  const cdpPort = await freePort();
  const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'report-'));
  const chrome = spawn(findChrome(), [
    '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run',
    '--no-default-browser-check', '--disable-extensions',
    `--remote-debugging-port=${cdpPort}`, `--user-data-dir=${profile}`,
    ...(reducedMotion ? ['--force-prefers-reduced-motion'] : []),
    'about:blank',
  ], { stdio: 'ignore' });

  let target = null;
  for (let i = 0; i < 100; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${cdpPort}/json`)).json();
      target = list.find(t => t.type === 'page');
      if (target) break;
    } catch { /* not up yet */ }
    await new Promise(r => setTimeout(r, 100));
  }
  if (!target) {
    chrome.kill('SIGKILL'); server.close();
    throw new Error('Chrome did not expose a CDP target');
  }

  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((res, rej) => {
    ws.addEventListener('open', res, { once: true });
    ws.addEventListener('error', rej, { once: true });
  });

  let id = 0;
  const pending = new Map();
  ws.addEventListener('message', e => {
    const m = JSON.parse(e.data);
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
  });
  const send = (method, params = {}) => {
    const i = ++id;
    return new Promise(r => { pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
  };
  const ev = async (expression) => {
    const r = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
    if (r.result?.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails).slice(0, 800));
    return r.result.result.value;
  };

  await send('Page.enable');
  await send('Runtime.enable');
  await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: dpr, mobile: false });

  const features = [];
  if (reducedMotion) features.push({ name: 'prefers-reduced-motion', value: 'reduce' });
  if (media || features.length) {
    await send('Emulation.setEmulatedMedia', { media: media || '', features });
  }

  const url = `http://127.0.0.1:${httpPort}/${base}?v=${Date.now()}`;
  await send('Page.navigate', { url });
  await ev('document.fonts.ready.then(()=>true)').catch(() => {});
  await new Promise(r => setTimeout(r, settleMs));

  const shot = async (out, rect = null, scale = 1) => {
    const params = { format: 'png', captureBeyondViewport: true };
    if (rect) params.clip = { x: rect.x, y: rect.y, width: rect.w, height: rect.h, scale };
    const r = await send('Page.captureScreenshot', params);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, Buffer.from(r.result.data, 'base64'));
    return out;
  };

  const close = async () => {
    try { ws.close(); } catch {}
    chrome.kill('SIGKILL');                       // ours, and only ours
    await new Promise(r => server.close(r));
    fs.rmSync(profile, { recursive: true, force: true });
  };

  return { url, ev, send, shot, close, cdpPort, httpPort };
}

/** <file> [--out path] [--json] */
export function parseArgs(argv = process.argv.slice(2)) {
  const out = { file: null, out: null, json: false, rest: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--out') out.out = argv[++i];
    else if (a === '--json') out.json = true;
    else if (!out.file && !a.startsWith('--')) out.file = a;
    else out.rest.push(a);
  }
  if (!out.file) {
    console.error('usage: node scripts/export_pdf.mjs <report.html> [--out report.pdf] [--json]');
    process.exit(2);
  }
  return out;
}
