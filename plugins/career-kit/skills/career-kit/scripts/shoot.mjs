// Screenshot a page at several scroll positions with a real browser, and report what broke.
//
//   node shoot.mjs <url> <width> <height> <out-prefix> <name=scrollY|name=sel:css> ...
//   node shoot.mjs http://127.0.0.1:8943/ 1280 900 /tmp/site top=0 work=sel:#work
//
// Chrome's own --screenshot flag captures the page at scroll 0 and nothing else, so a
// scroll-driven page reports as fine while everything below the fold is unverified. This
// drives Chrome over CDP instead: it eases to each target in twelve steps so scroll-reveal
// animations actually fire, waits for them, then captures.
//
// It prints one JSON line per run — {sw, iw, h} — where sw is scrollWidth and iw is
// innerWidth. sw > iw is a horizontal overflow, which is the defect that phone layouts fail
// on most often. Console errors and uncaught exceptions are printed at the end as ERR/EXC
// lines; a page that captured cleanly and logged an exception has not passed.
//
// Piping this to `head` kills it with EPIPE. Redirect to a file and read the file.
import { spawn } from "node:child_process";
import fs from "node:fs";

const [url, w, h, out, ...targets] = process.argv.slice(2);
if (!out) { console.error("usage: node shoot.mjs <url> <w> <h> <out-prefix> name=<y|sel:css> ..."); process.exit(2); }
const CHROME = process.env.CHROME_BIN
  || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const port = 9333 + Math.floor(Math.random() * 500);
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${port}`,
  `--window-size=${w},${h}`, "--hide-scrollbars",
  `--user-data-dir=/tmp/cdp/prof${port}`, "about:blank"], { stdio: "ignore" });
const sleep = ms => new Promise(r => setTimeout(r, ms));

let tab;
for (let i = 0; i < 40 && !tab; i++) {
  try {
    const list = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
    tab = list.find(t => t.type === "page");
  } catch { /* chrome is still starting */ }
  if (!tab) await sleep(250);
}
if (!tab) { chrome.kill(); console.error("chrome did not open a debuggable page"); process.exit(1); }

const ws = new WebSocket(tab.webSocketDebuggerUrl);
await new Promise(r => ws.onopen = r);
let id = 0; const pending = new Map(); const logs = [];
ws.onmessage = e => {
  const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result); pending.delete(m.id); }
  if (m.method === "Runtime.exceptionThrown")
    logs.push("EXC " + JSON.stringify(m.params.exceptionDetails).slice(0, 300));
  if (m.method === "Runtime.consoleAPICalled" && m.params.type === "error")
    logs.push("ERR " + m.params.args.map(a => a.value).join(" "));
};
const send = (method, params = {}) =>
  new Promise(r => { pending.set(++id, r); ws.send(JSON.stringify({ id, method, params })); });

await send("Runtime.enable");
await send("Page.enable");
await send("Emulation.setDeviceMetricsOverride",
  { width: +w, height: +h, deviceScaleFactor: 1, mobile: +w < 600 });
await send("Page.navigate", { url });
await sleep(2500);

const evaluate = async expr =>
  (await send("Runtime.evaluate", { expression: expr, returnByValue: true })).result?.value;
console.log(JSON.stringify(await evaluate(
  "({sw:document.scrollingElement.scrollWidth,iw:innerWidth," +
  "h:document.scrollingElement.scrollHeight})")));

for (const t of targets) {
  const [name, v] = t.split("=");
  const y = v.startsWith("sel:")
    ? await evaluate(`Math.max(0,Math.round(document.querySelector(${JSON.stringify(v.slice(4))})` +
                     `.getBoundingClientRect().top+scrollY-64))`)
    : +v;
  const steps = 12, from = await evaluate("scrollY");
  for (let i = 1; i <= steps; i++) {
    await evaluate(`scrollTo(0,${from}+(${y}-${from})*${i / steps})`);
    await sleep(90);
  }
  await sleep(1500);
  const r = await send("Page.captureScreenshot", { format: "png" });
  fs.writeFileSync(`${out}-${name}.png`, Buffer.from(r.data, "base64"));
  console.log(name, y);
}
if (logs.length) console.log(logs.join("\n"));
ws.close();
chrome.kill();
