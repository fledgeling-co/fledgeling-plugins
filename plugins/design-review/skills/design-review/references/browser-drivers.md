# Browser drivers

Five ways to reach a render. Use whichever the project already has — no reason to install a second stack.

| Path | Script / tools | Best when |
|---|---|---|
| Playwright | `scripts/run_review.py` | Python project, or nothing installed yet |
| Puppeteer | `scripts/run_review.mjs` | Node project already using it |
| chrome-devtools-mcp | MCP tools | You want CWV traces and Lighthouse without wiring them yourself |
| agent-browser | CLI or MCP | Fast snapshot/ref loop, `vitals`, `a11y`, session reuse |
| claude-in-chrome | `mcp__claude-in-chrome__*` | Already connected, reviewing a live/authenticated surface |

Both scripts write the same layout and manifest shape, so `analyze_styles.py` and `annotate.py` read either interchangeably.

One measured difference: Puppeteer's `console` event surfaces failed subresource loads (a missing favicon shows as `Failed to load resource: … 404`) where Playwright's does not. Neither is wrong — Puppeteer is stricter on console capture, Playwright reports the same failure through `requestfailed` only for network-level failures, not HTTP error statuses. If the console count differs between runners on the same page, that is why. Check `failedRequests` and the network list before treating a console-error count as a finding.

If none exists: run `scan_source.py` and the static checks, then say in the summary that rendered verification did not happen. Never imply a page was seen.

Then name what would unlock the rest. "No browser was available" tells the reader they got a partial review; it does not tell them how to get the whole one. Close with the cheapest path that fits their stack — a Node project already has `npx puppeteer`, a Python one `pip install playwright && playwright install chromium`, and a Chrome already running with `--remote-debugging-port=9222` needs only chrome-devtools-mcp pointed at it. One line, with the specific command, and say which checks it would turn on: contrast against live backgrounds, overflow, target geometry, focus rendering, per-viewport layout.

---

## chrome-devtools-mcp

The strongest fit for this skill, because it carries performance and network natively — the two gate categories the other paths make you assemble by hand.

Install:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

Or `claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest`. Needs Node LTS and current-stable-or-newer Chrome. The browser starts lazily, on first tool that needs it.

To review a surface behind auth, attach to an existing Chrome rather than launching a fresh profile: `--browser-url=http://127.0.0.1:9222`, with Chrome started using `--remote-debugging-port=9222` and a non-default `--user-data-dir`.

**Tools this review uses.** Names below are exact; the per-tool descriptions in the project README are terse, so treat any behaviour not stated here as worth confirming against `docs/tool-reference.md` rather than assumed.

*Navigation and setup* — `navigate_page`, `new_page`, `select_page`, `list_pages`, `close_page`, `wait_for`, `resize_page`, `emulate`.

*Evidence* — `evaluate_script` (runs the probes), `take_screenshot`, `take_snapshot` (structured page representation that element-targeting tools rely on), `list_console_messages`, `get_console_message`.

*Gates* — `performance_start_trace`, `performance_stop_trace`, `performance_analyze_insight`, `lighthouse_audit`, `list_network_requests`, `get_network_request`.

*Interaction staging* — `hover`, `click`, `press_key`, `fill`, `fill_form`, `handle_dialog`.

### Running the probes

```
evaluate_script   <contents of scripts/probes.js>
evaluate_script   JSON.stringify(window.__designReviewProbes.runAll())
```

Save the payload to disk so `analyze_styles.py` can read it. If one call is too large, pull sections:

```
JSON.stringify(window.__designReviewProbes.probeContrast())
JSON.stringify(window.__designReviewProbes.probeOverflow())
JSON.stringify(window.__designReviewProbes.probeTargets())
JSON.stringify(window.__designReviewProbes.probeSemantics())
JSON.stringify(window.__designReviewProbes.dumpStyles())
```

### Viewport matrix

`resize_page` per width, re-running the probes at each. Matrix is 375 / 768 / 1280 / 1920 plus two or three in-between widths.

`--viewport` sets the launch default if you'd rather fix it once.

### Performance gates

This is where chrome-devtools-mcp earns its place. Rather than inferring CWV from a lab screenshot:

```
performance_start_trace
  <reload or drive the interaction under test>
performance_stop_trace
performance_analyze_insight
```

Then `lighthouse_audit` for a scored pass.

Two honesty constraints on what you report:

- These are **lab** numbers from one run on one machine. The CWV thresholds — LCP ≤2.5s, INP ≤200ms, CLS ≤0.1 — are defined at the **75th percentile of real users**. A passing lab run is a signal, not conformance. Say which you have
- Trace URLs may be sent to the Google CrUX API for field data unless the server runs with `--no-performance-crux`. On a private or pre-release surface, set that flag

### Screenshots

`take_screenshot`. Server flags worth setting: `--screenshotFormat` (`jpeg`/`png`/`webp`), `--screenshotQuality`, `--screenshotMaxWidth`, `--screenshotMaxHeight`.

Non-PNG formats are roughly 3–5× smaller, which matters when a review opens dozens of crops — but JPEG artifacts sit exactly where 1px drift and hairline defects live. Use PNG for detail crops and a compressed format for overview captures.

For long pages, capture in viewport-sized steps rather than one tall image. Extreme aspect ratios hit image-token compression limits.

### Network

`list_network_requests` then `get_network_request` for detail. Failed requests are the difference between "this layout is broken" and "this asset 404'd" — two findings that look identical in a screenshot.

`--redactNetworkHeaders` masks sensitive headers before they reach the client. Use it on anything authenticated.

### Security

The server exposes browser contents to the MCP client. Don't point it at a surface carrying data the user hasn't agreed to share. File-writing tools are confined to the OS temp dir unless the client negotiates MCP roots or the server runs with `--allowUnrestrictedPaths`.

---

## agent-browser

A Rust CLI and daemon speaking CDP directly. No Node at runtime, and the daemon persists between commands, which makes a long review cheap — each call reuses the same page rather than relaunching.

```bash
npm install -g agent-browser     # or: brew install agent-browser
agent-browser install            # downloads Chrome for Testing, first time only
```

Two ways to drive it. The CLI is usually simpler for a review because the output pipes straight to the analysis scripts:

```bash
agent-browser open http://localhost:3000
agent-browser screenshot shots/1280-full.png
agent-browser eval "$(cat scripts/probes.js); JSON.stringify(window.__designReviewProbes.runAll())" --json > probes/1280x900.json
agent-browser close
```

Or as MCP, when you'd rather stay in tool calls:

```json
{
  "mcpServers": {
    "agent-browser": { "command": "agent-browser", "args": ["mcp"] }
  }
}
```

Tools: `agent_browser_open`, `agent_browser_snapshot`, `agent_browser_click`, `agent_browser_fill`, `agent_browser_type`, `agent_browser_press`, `agent_browser_wait_for_selector`, `agent_browser_screenshot`, `agent_browser_get_url`, `agent_browser_eval`, `agent_browser_close`, `agent_browser_tools_profiles`.

The default `core` profile omits what this review wants most. Load the wider set:

```bash
agent-browser mcp --tools core,network,debug,state
agent-browser mcp --tools all
```

### What it adds over the other paths

Three built-in commands map directly onto review stages, which saves assembling them by hand:

- **`agent-browser vitals`** — Core Web Vitals without starting a trace manually
- **`agent-browser a11y`** — an accessibility pass. Treat it as one input, not the answer: tooling of this class detects roughly a fifth to under two-thirds of what an expert manual audit finds, and ~2.49% of keyboard failures
- **`agent-browser diff`** — before/after comparison, useful across review rounds when checking whether a fix moved anything it shouldn't have

Also worth using: `console` and `errors` for the console gate, `network requests` (and HAR) to separate a broken asset from a broken layout, `trace` and `profiler` for frame cost, and `react *` if the surface is React and a re-render is the suspected cause of a focus-loss or scroll-reset symptom.

### The snapshot/ref loop

Its interaction model differs from the others. Rather than CSS selectors, take a snapshot and act on the refs it returns:

```bash
agent-browser snapshot -i --json     # accessibility tree with @e1, @e2 … refs
agent-browser click @e2
agent-browser fill @e3 "test@example.com"
agent-browser snapshot -i --json     # re-snapshot after the page changes
```

Re-snapshot after anything that changes the DOM; stale refs are the main failure mode.

For a review specifically, the snapshot doubles as evidence: it *is* the accessibility tree, so it answers name/role/value questions directly rather than through inference from pixels.

### Batching and sessions

The daemon persists, so chained commands reuse the page. `batch` collapses a predictable sequence into one call:

```bash
agent-browser batch "open http://localhost:3000" "snapshot -i" "screenshot shots/fold.png"
```

`--session` and `--restore` keep authenticated state between runs — the cleanest way to review a surface behind a login without scripting the login each time. `--allowed-domains` bounds what the browser may reach, which is worth setting when reviewing a page that loads third-party embeds.

Defaults to note: 25s per-operation timeout, and the daemon idles out after an hour. A long review may need `agent-browser open` again mid-session.

---

Call `tabs_context_mcp` first. Never reuse a tab id from an earlier session; create a fresh tab with `tabs_create_mcp` unless the user pointed at an existing one. If a tool reports an invalid tab, call `tabs_context_mcp` again rather than retrying the id.

Inject and run the probes:

```
javascript_tool  action=javascript_exec  text=<contents of scripts/probes.js>
javascript_tool  action=javascript_exec  text=JSON.stringify(window.__designReviewProbes.runAll())
```

`resize_window` per viewport. Window chrome means requested and actual sizes differ — read the real figure back:

```
javascript_tool  text=JSON.stringify({w: innerWidth, h: innerHeight, dpr: devicePixelRatio})
```

`computer action=screenshot` captures the viewport; `computer action=zoom` with a `region` captures a rectangle, which is the crop mechanism. Pass `save_to_disk: true` when a capture needs to persist for the report or for `annotate.py`.

`read_console_messages` — always pass a `pattern` (`"error|warning|failed|uncaught"`), because unfiltered output buries the signal.

`browser_batch` runs a predictable sequence in one round trip: navigate → resize → screenshot, or hover → wait → screenshot. Coordinates inside a batch refer to the screenshot taken *before* the batch, so don't chain a click onto a screenshot within one.

---

## Staging interaction states

Same in every path. Hover contaminates a selected-state capture, so isolate each:

- **Rest** — move the pointer to a corner first, then capture
- **Hover** — hover, wait ~400ms for the transition, then capture
- **Focus** — press Tab, then capture. Repeat to walk the order
- **Active** — hard to hold; toggle the class via script instead

## Keyboard path

Automated tooling catches roughly 2.49% of keyboard failures, so a manual pass here is worth more than anywhere else.

```js
(() => { const r=[]; let last=null;
  for (let i=0;i<40;i++){ const a=document.activeElement;
    if (a===last) break; last=a;
    r.push({tag:a.tagName, text:(a.textContent||'').trim().slice(0,40),
            ring:getComputedStyle(a).outlineStyle});
  } return JSON.stringify(r); })()
```

Then check by hand: is focus visible at every stop, does the order match the visual order, does Escape close what it should, can you reach and operate everything a mouse can.

Whether the order *makes sense for the task* is a human judgment. Report what you observed; defer the verdict.

## Mid-flight frames

Restart deterministically, then capture on a short interval:

```js
const el = document.querySelector('SELECTOR');
el.classList.remove('seen');
void el.offsetWidth;      // force reflow — this restarts the animation
el.classList.add('seen');
```

Batch the screenshot calls so the interval stays tight; per-call latency otherwise smears it.

## Reduced motion and print

Playwright and Puppeteer emulate both directly, and the scripts already do. chrome-devtools-mcp has `emulate`. claude-in-chrome cannot force either — `matchMedia(...)` only reads the current setting. If you cannot emulate, say the check was not performed rather than inferring the reduced-motion rendering from the normal one.

## What not to do

Do not trigger `alert`, `confirm` or `prompt` through claude-in-chrome. A modal blocks every subsequent browser event and the session stops responding until a human dismisses it. chrome-devtools-mcp has `handle_dialog`, so the risk is lower there, but the review still has no reason to open one.

Do not submit forms, accept consent banners, or click irreversible controls on a surface under review. A review reads; it does not act. If confirming a finding needs a form submitted, say so and ask.

## When automation fails

Stop after two or three failed attempts and report what you tried. An automation problem is a finding about the review, not about the design — be clear which one you're reporting.
