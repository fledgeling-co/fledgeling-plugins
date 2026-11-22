// Capture a served website the way a visitor meets it, in a real browser, and report what broke.
//
//   node scroll_capture.mjs <url> <outdir> [--widths 1440,390] [--selectors "section,[data-section]"]
//                                          [--engine auto|agent-browser|playwright]
//
// Runs four passes and writes one PNG per section per pass plus report.json:
//   default        Chromium at each width, scrolled to each section in twelve eased steps so
//                  scroll-triggered reveals actually fire before the capture
//   reduced-motion the same with prefers-reduced-motion: reduce emulated
//   no-webgl       Chromium launched with WebGL and 3D APIs disabled, so the fallback path shows
//   touch          a phone viewport with touch and a mobile user agent
//
// Per pass and width it records scrollWidth against innerWidth (horizontal overflow, the defect
// phone layouts fail on most), uncaught exceptions, elements still at opacity 0 after scrolling
// past them (a reveal that never fired), and <video> elements playing under reduced motion.
// Exit 1 on any overflow, exception, stuck reveal or video in the wrong state.
//
// Chrome's own --screenshot captures scroll position 0 and nothing else, so a scroll-driven page
// reports as fine while everything below the fold is unverified. That is why this exists.
//
// Engines. agent-browser (Chrome for Testing, on PATH) is the default because it needs nothing
// installed in the project. Playwright is used when --engine playwright is passed, or under auto
// when agent-browser is missing and @playwright/test resolves from the directory the command runs
// in. Both drive Chromium; neither is Safari. Headless engines can report a WebGL error on a 3D
// page that is the engine, not the page: the no-webgl pass is the one that checks the fallback.
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";
import { pathToFileURL } from "node:url";

const [url, outArg, ...rest] = process.argv.slice(2);
// Absolute, always: agent-browser 0.43.0 given a relative dot-prefixed path wrote every PNG into
// its own temp directory and reported success, so a capture run produced no files and passed.
const outdir = outArg ? path.resolve(outArg) : outArg;
if (!url || !outdir) {
  console.error("usage: node scroll_capture.mjs <url> <outdir> [--widths 1440,390] [--selectors css] [--engine auto|agent-browser|playwright]");
  process.exit(2);
}
const opt = (name, dflt) => {
  const i = rest.indexOf(name);
  return i >= 0 ? rest[i + 1] : dflt;
};
const widths = opt("--widths", "1440,390").split(",").map(Number);
const selectors = opt("--selectors", "section, [data-section], header, footer");
const wanted = opt("--engine", "auto");
fs.mkdirSync(outdir, { recursive: true });

// ---- in-page code, shared by both engines --------------------------------------------------
const targetsJS = (sel) => `JSON.stringify([...document.querySelectorAll(${JSON.stringify(sel)})].map((el, i) => ({
  i, top: el.getBoundingClientRect().top + window.scrollY, tag: el.tagName.toLowerCase(), id: el.id || el.dataset.section || "" })))`;
const scrollJS = (from, goal) => `(async () => {
  for (let s = 1; s <= 12; s++) {
    window.scrollTo(0, ${from} + ((${goal} - ${from}) * (1 - Math.cos((s / 12) * Math.PI))) / 2);
    await new Promise((r) => setTimeout(r, 25));
  }
  await new Promise((r) => setTimeout(r, 500));
  return "ok";
})()`;
const metricsJS = `(async () => {
  window.scrollTo(0, document.documentElement.scrollHeight);
  await new Promise((r) => setTimeout(r, 600));
  const stuck = [...document.querySelectorAll("body *")].filter((el) => {
    const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return r.bottom < window.innerHeight && r.width > 40 && r.height > 20 &&
      cs.opacity === "0" && cs.visibility !== "hidden" && !el.closest("[aria-hidden='true']");
  }).slice(0, 10).map((el) => el.tagName.toLowerCase() + (el.id ? "#" + el.id : "") + "." + [...el.classList].slice(0, 2).join("."));
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const videos = [...document.querySelectorAll("video")].map((v) => ({
    src: (v.currentSrc || "").split("/").pop(), playing: !v.paused && !v.ended && v.readyState > 2,
    ended: v.ended, autoplay: v.autoplay, poster: Boolean(v.poster) }));
  return JSON.stringify({ scrollWidth: document.documentElement.scrollWidth, innerWidth: window.innerWidth,
    height: document.documentElement.scrollHeight, stuck, reduce, videos,
    webgl: Boolean(document.createElement("canvas").getContext("webgl2") || document.createElement("canvas").getContext("webgl")) });
})()`;

const passes = [
  { name: "default" },
  { name: "reduced-motion", reduce: true },
  { name: "no-webgl", args: ["--disable-webgl", "--disable-webgl2", "--disable-3d-apis"] },
  { name: "touch", touch: true, only: [390] },
];

// ---- engine: agent-browser ------------------------------------------------------------------
function hasAgentBrowser() {
  try { execFileSync("agent-browser", ["--version"], { stdio: "ignore" }); return true; } catch { return false; }
}
function agentBrowserEngine() {
  const tag = `cw-capture-${process.pid}`;
  return {
    name: "agent-browser",
    async run(pass, width, visit) {
      const session = `${tag}-${pass.name}-${width}`;
      const ab = (args, input) => execFileSync("agent-browser", ["--session", session, ...args],
        { encoding: "utf8", input, stdio: [input ? "pipe" : "ignore", "pipe", "pipe"], timeout: 120000 });
      const evalJS = (code) => {
        const out = JSON.parse(ab(["--json", "eval", "--stdin"], code));
        if (!out.success) throw new Error(out.error || "eval failed");
        return out.data.result;
      };
      const errors = [];
      try {
        const launch = pass.args ? ["--args", pass.args.join(",")] : [];
        ab([...launch, "open", "about:blank"]);
        if (pass.touch) ab(["set", "device", "iPhone 16"]);
        else ab(["set", "viewport", String(width), String(width < 600 ? 844 : 900), width < 600 ? "2" : "1"]);
        ab(["set", "media", "light", ...(pass.reduce ? ["reduced-motion"] : [])]);
        try { ab(["open", url]); } catch (e) { errors.push(`load: ${String(e.stderr || e.message).slice(0, 300)}`); }
        ab(["wait", "400"]);
        return await visit({
          errors,
          targets: () => JSON.parse(evalJS(targetsJS(selectors))),
          scrollTo: (from, goal) => evalJS(scrollJS(from, goal)),
          shot: (file, full) => {
            ab(["screenshot", ...(full ? ["--full"] : []), file]);
            if (!fs.existsSync(file)) throw new Error(`screenshot reported success but ${file} does not exist`);
          },
          metrics: () => JSON.parse(evalJS(metricsJS)),
          // `errors` prints nothing when the page threw nothing, and one "✗ <message>" line (plus
          // indented stack lines) per uncaught exception.
          pageErrors: () => ab(["errors"]).split("\n").filter((l) => l.startsWith("✗"))
            .map((l) => `exception: ${l.replace(/^✗\s*/, "").slice(0, 300)}`),
        });
      } finally {
        try { ab(["close"]); } catch {}
      }
    },
  };
}

// ---- engine: Playwright ---------------------------------------------------------------------
// Resolve Playwright from the directory the command runs in, not from this file's location: an ESM
// import resolves relative to the importing file, so a script kept in a skill directory cannot see
// the project's node_modules, and the error reads like a missing browser.
async function loadPlaywright() {
  const fromCwd = createRequire(path.join(process.cwd(), "noop.js"));
  for (const name of ["@playwright/test", "playwright"]) {
    try {
      const mod = await import(pathToFileURL(fromCwd.resolve(name)).href);
      const chromium = mod.chromium ?? mod.default?.chromium;
      if (chromium) return chromium;
    } catch {}
  }
  return null;
}
function playwrightEngine(chromium) {
  return {
    name: "playwright",
    async run(pass, width, visit) {
      const browser = await chromium.launch(pass.args ? { args: pass.args } : {});
      const context = await browser.newContext({
        viewport: { width, height: width < 600 ? 844 : 900 }, deviceScaleFactor: width < 600 ? 2 : 1,
        colorScheme: "light", ...(pass.reduce ? { reducedMotion: "reduce" } : {}),
        ...(pass.touch ? { hasTouch: true, isMobile: true } : {}),
      });
      const page = await context.newPage();
      const errors = [];
      page.on("pageerror", (e) => errors.push(`exception: ${String(e).slice(0, 300)}`));
      try {
        await page.goto(url, { waitUntil: "networkidle", timeout: 60000 }).catch((e) => errors.push(`load: ${e.message}`));
        await page.waitForTimeout(400);
        return await visit({
          errors,
          targets: async () => JSON.parse(await page.evaluate(targetsJS(selectors))),
          scrollTo: (from, goal) => page.evaluate(scrollJS(from, goal)),
          shot: (file, full) => page.screenshot({ path: file, fullPage: Boolean(full) }),
          metrics: async () => JSON.parse(await page.evaluate(metricsJS)),
          pageErrors: () => [],
        });
      } finally {
        await browser.close();
      }
    },
  };
}

let engine;
if (wanted === "agent-browser" || (wanted === "auto" && hasAgentBrowser())) {
  if (!hasAgentBrowser()) { console.error("agent-browser is not on PATH"); process.exit(2); }
  engine = agentBrowserEngine();
} else {
  const chromium = await loadPlaywright();
  if (!chromium) {
    console.error("No engine: agent-browser is not on PATH and Playwright does not resolve from this directory. Install one: npm i -g agent-browser && agent-browser install, or npm i -D @playwright/test && npx playwright install chromium");
    process.exit(2);
  }
  engine = playwrightEngine(chromium);
}

const report = { url, engine: engine.name, runs: [], failures: [] };
for (const pass of passes) {
  for (const width of pass.only ?? widths) {
    const run = await engine.run(pass, width, async (p) => {
      const targets = await p.targets();
      let last = 0, shots = 0;
      for (const t of targets) {
        const goal = Math.max(0, Math.round(t.top - 20));
        await p.scrollTo(last, goal);
        last = goal;
        await p.shot(path.join(outdir, `${pass.name}-${width}-${String(t.i).padStart(2, "0")}-${t.id || t.tag}.png`));
        shots++;
      }
      const metrics = await p.metrics();
      await p.shot(path.join(outdir, `${pass.name}-${width}-full.png`), true);
      return { pass: pass.name, width, ...metrics, errors: [...p.errors, ...(await p.pageErrors())], shots };
    });
    report.runs.push(run);
    const tag = `${pass.name} @${width}`;
    if (run.scrollWidth > run.innerWidth) report.failures.push(`${tag}: horizontal overflow ${run.scrollWidth} > ${run.innerWidth}`);
    for (const e of run.errors) report.failures.push(`${tag}: ${e}`);
    if (run.stuck.length) report.failures.push(`${tag}: ${run.stuck.length} element(s) still invisible after scrolling past: ${run.stuck.join(", ")}`);
    for (const v of run.videos) if (run.reduce && v.playing) report.failures.push(`${tag}: video ${v.src} plays under reduced motion`);
    if (pass.name === "no-webgl" && run.webgl) report.failures.push(`${tag}: WebGL was still available, so this pass did not test the fallback`);
  }
}

fs.writeFileSync(path.join(outdir, "report.json"), JSON.stringify(report, null, 2));
for (const r of report.runs) {
  console.log(`${r.pass.padEnd(15)} ${String(r.width).padStart(5)}  sw=${r.scrollWidth} iw=${r.innerWidth}  height=${r.height}  errors=${r.errors.length}  stuck=${r.stuck.length}  videos=${r.videos.length}  webgl=${r.webgl}`);
}
for (const f of report.failures) console.log("FAIL", f);
console.log(`RESULT: ${report.failures.length} failure(s) on ${engine.name}; captures and report.json in ${outdir}`);
console.log("Not checked by this script: Safari, a real phone, touch drag against page scroll, and pace or skips in video. Open the PNGs, and say so in the report.");
process.exit(report.failures.length ? 1 : 0);
