#!/usr/bin/env node
// mfeval.mjs — run an injectable against a page at a chosen viewport, and write what it returns.
//
// This is the shell-facing replacement for the `playwright-cli open / resize / eval --filename`
// quartet. Neither of Obscura's cheaper entry points can stand in for it:
//   · `obscura fetch` renders at a fixed 1280x720 with no way to resize, and does NOT await a
//     returned promise — analyze.js is an async IIFE, so it comes back as `{}`;
//   · `obscura mcp`'s browser_evaluate holds a session but likewise does not await, and exposes
//     no viewport control.
// So this drives `obscura serve` over CDP, where Emulation.setDeviceMetricsOverride and
// Runtime.evaluate{awaitPromise:true} both work. Node 22 has a global WebSocket, so there is no
// package to install.
//
// USAGE:
//   node mfeval.mjs --url <url> [--width 1280] [--height 2000] \
//     [--setup <file.js|-e "expr">] --eval <file.js> [--out <file>] [--settle 1500] [--cdp-port N]
//
//     --setup   an expression evaluated BEFORE --eval, in the same page. This is where the
//               __MF_* globals go; a fresh `obscura fetch` per call would lose them.
//     --eval    the injectable (analyze.js, extract-mock.js …). A file whose contents are a bare
//               function expression is called for you; an IIFE is evaluated as-is.
//     --out     write the returned value here. Written VERBATIM — a returned JSON string lands as
//               JSON, with no second layer of encoding to unwrap. Omitted → stdout.
//
// Localhost is blocked by default, so the server is started with --allow-private-network; without
// it every navigation fails as an SSRF block, which reads like a broken page.

import { readFileSync, writeFileSync } from 'node:fs';
import { spawn, spawnSync } from 'node:child_process';

if (spawnSync('obscura', ['--version'], { stdio: 'ignore' }).error) {
  console.error('ERROR: obscura is not on PATH. Download the aarch64-macos release from\n' +
                '       https://github.com/h4ckf0r0day/obscura and put it in ~/.local/bin');
  process.exit(2);
}

const argv = process.argv.slice(2);
const arg = (name, def) => { const i = argv.indexOf('--' + name); return i >= 0 ? argv[i + 1] : def; };
const URL_ = arg('url');
const EVAL_FILE = arg('eval');
if (!URL_ || !EVAL_FILE) {
  console.error('usage: node mfeval.mjs --url <url> --eval <file.js> [--setup <file.js|-e expr>] [--out f] [--width W] [--height H] [--settle MS]');
  process.exit(2);
}
const WIDTH = parseInt(arg('width', '1280'), 10);
const HEIGHT = parseInt(arg('height', '2000'), 10);
const SETTLE = parseInt(arg('settle', '1500'), 10);
const OUT = arg('out');
const PORT = parseInt(arg('cdp-port', String(9200 + Math.floor(Math.random() * 300))), 10);
const OWN_SERVER = argv.indexOf('--cdp-port') < 0;

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// A file holding a bare function expression (`() => {…}`) has to be CALLED; an IIFE already is.
function asExpression(src) {
  const t = src.trim().replace(/;\s*$/, '');
  return /\)\s*\(\s*\)$/.test(t) ? t : `(${t})()`;
}

function setupExpression() {
  const i = argv.indexOf('--setup');
  if (i < 0) return null;
  const v = argv[i + 1];
  if (v === '-e') return argv[i + 2];
  return asExpression(readFileSync(v, 'utf8'));
}

let server = null;
if (OWN_SERVER) {
  server = spawn('obscura', ['--allow-private-network', 'serve', '--port', String(PORT), '--quiet'],
    { stdio: 'ignore' });
  const deadline = Date.now() + 15000;
  let up = false;
  while (Date.now() < deadline && !up) {
    try { up = (await fetch(`http://127.0.0.1:${PORT}/json/version`)).ok; } catch (e) {}
    if (!up) await sleep(200);
  }
  if (!up) { server.kill(); console.error(`obscura serve did not come up on port ${PORT}`); process.exit(1); }
}

const version = await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json();
const ws = new WebSocket(version.webSocketDebuggerUrl);
const pending = new Map();
let nextId = 0;
const send = (method, params = {}, sessionId) => new Promise((resolve) => {
  const id = ++nextId;
  pending.set(id, resolve);
  ws.send(JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) }));
});
ws.addEventListener('message', (e) => {
  const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
});
await new Promise((res, rej) => { ws.addEventListener('open', res); ws.addEventListener('error', rej); });

const created = await send('Target.createTarget', { url: 'about:blank' });
const targetId = created.result.targetId;
const sid = (await send('Target.attachToTarget', { targetId, flatten: true })).result.sessionId;
for (const d of ['Page', 'Runtime', 'DOM']) await send(`${d}.enable`, {}, sid);
await send('Emulation.setDeviceMetricsOverride',
  { width: WIDTH, height: HEIGHT, deviceScaleFactor: 1, mobile: WIDTH <= 480 }, sid);

const evaluate = async (expression) => {
  const r = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true }, sid);
  if (r.error) throw new Error(JSON.stringify(r.error));
  if (r.result?.exceptionDetails) {
    throw new Error(r.result.exceptionDetails.exception?.description
      ?? r.result.exceptionDetails.text ?? 'evaluate threw');
  }
  return r.result?.result?.value;
};

await send('Page.navigate', { url: URL_ }, sid);
{
  const deadline = Date.now() + 45000;
  while (Date.now() < deadline && await evaluate('document.readyState') !== 'complete') await sleep(150);
}
await sleep(SETTLE);

const setup = setupExpression();
if (setup) await evaluate(setup);

const value = await evaluate(asExpression(readFileSync(EVAL_FILE, 'utf8')));
const text = typeof value === 'string' ? value : JSON.stringify(value);

if (OUT) writeFileSync(OUT, text ?? 'null');
else process.stdout.write((text ?? 'null') + '\n');

await send('Target.closeTarget', { targetId });
ws.close();
if (server) server.kill();
process.exit(0);
