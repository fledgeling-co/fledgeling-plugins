# React web targets — measuring two DOM surfaces (the web↔web case)

When **both** sides render to a browser DOM — a React/Next reference *and* a
React/Next target — this is the easiest case the skill handles, and a fundamentally
different one from React Native. Everything is `getComputedStyle`: the reference and
the target go through the **same** analyzer (`assets/diff/analyze.js`), the **same**
harness (`assets/diff/capture.mjs`), and the **same** browser (`obscura`) — one
command measures both sides. There is **no** simulator, no
Metro, no CDP/Fusebox handshake, no `axe`, and no in-app harness — the entire
`references/react-native.md` apparatus is bypassed. Read this doc for a web target;
read `react-native.md` for a native one.

> The canonical example: aligning Diolog's `apps/web` (served at `diolog.ai`)
> against the `web-design-system` preview app (served at `diolog.mock`). Both are
> React rendering real DOM with the same `tw-` Tailwind tokens and fonts, so they
> are measured identically.

## Why web↔web is *simpler* than the RN case (and what changes because of it)

Three properties make a DOM↔DOM audit both easier and more precise. Each one changes
a rule that the RN-shaped parts of the skill state:

1. **One measurement path for both sides.** The reference is DOM (always was) and the
   target is *also* DOM, so `capture.mjs` runs `analyze.js` against **both** in one
   invocation (`--ref` = reference URL, `--target` = target URL). The structure
   layer and the style layer are the *same* extraction — you don't need a separate
   structural tool (no `axe describe-ui` / Maestro hierarchy). The fidelity probe
   (`fidelity-probe.md`) is also pure DOM, so it runs unchanged on both sides for the
   breadth/skeleton pass (Phase 3A/3B).

2. **Same viewport ⇒ geometry is directly comparable.** Render the reference and the
   target at the *identical* viewport (≥1680×… for the desktop multi-column app). The
   RN rationale "the mock frame width ≠ the device width, so compare insets not
   absolute x" no longer binds — when both frames are the same width, the differ's
   inset comparison effectively *is* an absolute-position comparison, and a
   left-inset/right-inset mismatch is a true geometry defect, not a frame-width
   artifact. (The differ already prefers the extracted `frame.w` for a DOM target, so
   its `scrolled` guard still correctly skips a horizontally-overflowing region like a
   kanban board or a tab strip.)

3. **The chrome boundary INVERTS — web chrome is IN SCOPE.** The "native chrome wins"
   exemption in `SKILL.md` Phase 1 and `react-native.md` §7 is **React-Native-only**.
   On the web, the app chrome — sidebar, window frame, top/app header, nav rail — is
   drawn in DOM on **both** sides, so it is content you audit, not OS chrome you
   concede. Concretely: the default `CHROME` selector skips
   `.sb, .island, .tabbar, .homebar, .nav, …` — and `.nav` will wrongly drop a web
   nav. **Override it on both sides** so nothing is skipped:
   `window.MF_CHROME_SELECTOR = '__none__'` (any selector that matches nothing), or set
   it to the app's *actual* OS-level chrome if there genuinely is some. There is no
   "native tab bar" to wave through here.

## The pipeline (both sides through `analyze.js`, one command)

```
reference URL (React) ─┐
                       ├─ capture.mjs ─ obscura serve/CDP ─ analyze.js MODE A (ref) + MODE B (target)
target URL    (React) ─┘                                              │
                                                                      ├─ + odiff element-crop raster
                                                                      ├─ + IoU text-less pairing
                                                                      ▼
                              reference.analysis.json  ·  target.findings.json
                              { summary, findings, inconclusive, noiseExcluded, analysis }
                                                                      ▼
                                            exit 0 clean · 1 findings · 3 inconclusive
```

```bash
node assets/diff/capture.mjs \
  --ref  "<reference-url>" \
  --target "<target-url>" \
  --out .mockup-fidelity/<screen> \
  --chrome-selector __none__ \
  --assert
```

`--chrome-selector __none__` is the web inversion in flag form — it is the harness default for exactly
this reason, but pass it explicitly so the intent is on the command line.

**Read `inconclusive` before `findings`.** Nine detector classes cannot run on this engine
(`engine-capability-matrix.md`), and a web↔web pair is where that bites hardest: both sides are the same
engine, so every silenced class agrees perfectly. `--assert` returns 3 rather than 0 for that reason.

No `--anchor` is needed for a web target — anchoring exists to scope a *multi-screen* RN dump (the harness
keeps every tab and pushed screen mounted). A DOM capture is already scoped to the one frame root you
selected.

### Frame selection — `MF_FRAME_SELECTOR`, not `MF_FRAME_TITLE`

`MF_FRAME_TITLE` / `MF_FRAME_INDEX` are the HTML phone-gallery mechanisms (match a
`<figcaption>`/`.cap` among many `<figure>`/`.frame` containers). A React web app is
not a gallery — it renders one screen at a time — so select the **screen content
root** with `MF_FRAME_SELECTOR` (any CSS selector). The reliable move is to tag the
content root yourself, then select the tag, so the selector is stable across both
sides regardless of class-name churn:

```js
// in the rendered page, via the browser tool: tag the content column (the area
// RIGHT of the sidebar — i.e. exclude shared chrome only if you mean to; usually
// you tag the <main>/content column and KEEP the chrome in a separate frame).
// Tagging, the frame globals and the extraction all go in ONE eval: every `obscura fetch`
// is a fresh render, so a global set by a previous call is gone.
obscura --allow-private-network fetch "<target-url>" --eval "(() => {
  document.querySelectorAll('[data-mf-root]').forEach(e => e.removeAttribute('data-mf-root'));
  const root = document.querySelector('main') /* or your content-column heuristic */;
  root.setAttribute('data-mf-root', '');
  return document.querySelector('[data-mf-root]') ? 'tagged' : 'no-root';
})()"
```

That eval only *finds and verifies your selector*. It cannot run the analyzer: `analyze.js`'s `capture()`
is async, and neither `obscura fetch --eval` nor the MCP `browser_evaluate` awaits a promise — both return
`{}` for an async IIFE. Once you know the selector works, hand it to the harness, which drives
`obscura serve` over CDP with `awaitPromise` and does the tagging itself:

```bash
node assets/diff/capture.mjs --ref "<reference-url>" --target "<target-url>" \
  --out .mockup-fidelity/<screen> --frame-selector '[data-mf-root]' \
  --chrome-selector __none__ --assert
```

The reference is immutable for the whole pass; the harness measures it once into
`reference.analysis.json` and re-measures only the target after a fix.
>
> **A viewport other than 1280×720 needs CDP**, not `fetch` — `obscura fetch` renders at a
> fixed size with no resize flag. Use `assets/diff/mfeval.mjs`, which sets
> `Emulation.setDeviceMetricsOverride` and runs the same `--setup` / `--eval` pair in one
> page.

## Rendering a protected target (the Diolog quickstart)

The reference (`diolog.mock`) is unauthenticated. The target (`diolog.ai`) needs the
dev session and a company with **populated** data — an empty screen grades nothing
(`SKILL.md` Done-criteria: verify the *populated* state, never the fallback).

Both of these need CLICKING (an SPA sidebar; a login flow), so they are the `obscura mcp`
lane — a session that survives a click — not `obscura fetch`, which discards the page
between calls. Both hosts are local, so the MCP server needs
`OBSCURA_ALLOW_PRIVATE_NETWORK=1` in its env or every navigation fails as an SSRF block.

```
# REFERENCE — the web-design-system preview app (React via Babel/CDN, real DOM)
browser_navigate   http://diolog.mock/preview/preview.html
#   the preview app is an SPA navigated in-app (no URL routing): browser_snapshot to find
#   the sidebar item by its label (e.g. "Tasks"), browser_click it, then tag the content
#   root and extract with browser_evaluate.

# TARGET — apps/web
browser_navigate   http://diolog.ai/login
#   browser_click "Log in as Luke (dev)" → /select-company → pick the company with real
#   data (the internal "Diolog" company has real Tasks; NH3 is the demo tenant), then:
browser_navigate   http://diolog.ai/quorum/board      # the route for that screen
```

Two things to know about `browser_evaluate`: it takes an **expression** (wrap a function
as `(() => {…})()`), and it does **not** await a promise — an async expression returns
`{}`. There is also no viewport tool, so a run that must match a specific width has to go
through `mfeval.mjs`/CDP instead, and a protected target then needs its cookies carried
across (`browser_storage_state` out, `Network.setCookie`-equivalent in).

Map each reference surface to its target route. The preview app's `REGISTRY`
(`apps/web-design-system/preview/app.jsx`) lists every mock page id/label; `apps/web`'s
routes live under `apps/web/app/(app)/…`. A worked correspondence:

| Preview page (id · label) | `apps/web` route |
|---|---|
| `dashboard` · Dashboard | `/dashboard` |
| `quorum` · Tasks | `/quorum/board` (also `/list`, `/my-issues`) |
| `conversations` · Conversations | `/conversations` |
| `documents` · Documents | `/documents` |
| `inbox` · Inbox | `/inbox` |
| `calendar` · Calendar | `/calendar` |
| `workflows` · Workflows | `/workflows` |
| `social` · Chatter / Monitoring | `/social` (chatter) |

Some target routes are **feature-flag-gated** (Tasks is behind the `quorum` flag,
resolved by the API). If the route 404s, the flag is off for that environment — flip
it at `/admin/feature-flags` or pick a company/env where it's on, rather than treating
the screen as absent.

## Expect the app to be *ahead* of the mock — classify, don't panic

A real, populated web target routinely renders **more** than a mock sample frame:
extra rows of live data, additional status columns, richer states. In the Tasks
dry-run the mock showed Backlog/Todo/In-progress/Done while the app had Backlog,
Needs-More-Info, Todo, Ready-for-AI, Developer-Review, Done, Verified, Canceled — so
the differ reported a large `⚠︎ unmatched` (mock text the app re-labels/omits) and a
large `◆ App-EXTRA` (live data + extra columns). That is **not** a wall of defects; it
is the breadth signal the ⛔ gate is about. Resolve each per THE LAW: a genuine
absence is a DEFECT (mock wins — build it); a richer real feature is `◆ app-ahead`
*only with an external citation* (a ticket / a recorded product decision), never a
reason you author during the audit. The differ's `◆ App-EXTRA` bucket is a scan aid
for exactly this — confirm each extra is real data or remove/cite it.

## Orchestration — web is parallel, not serial

There is **no serial resource** on the web (no single simulator). Do **not** reach for
the RN `references/batch-orchestration.md` (sequential Workflow loop / N-lane
sim-cloning) — that exists solely to serialise one sim. The web target uses the plain
`SKILL.md` Phase 6 shape: fan out one `Agent` per screen/region in waves of ≈5, hand
each the already-captured reference dump (no agent re-renders the reference), and have
each render only its own target route. Concurrent Obscura runs cannot interfere — each
`fetch` is its own process and its own page — so the wave size is about page-load cost,
not contention. Serialise only edits to a **shared** primitive/token file, exactly as on
any parallel-worktree job.

## What still applies unchanged

- **The differ's text-probe blind spots** (`assets/diff/README.md`): non-text visual
  elements (dividers, standalone icons, images), app-extra non-text elements,
  between-element spacing, icon-glyph correctness, element width/height, and the
  always-dynamic-text primitive-choice gap. A green `❌` list is necessary, not
  sufficient — finish every screen with the fidelity-probe breadth/skeleton pass
  (3A/3B) and a screenshot for the visual classes.
- **The artifact contract and the completeness critic** (`measurement-enforcement.md`):
  four artifacts per screen, the ledger generated from them, the blind critic before
  done. A DOM target satisfies the structure + style artifacts from the **same**
  `analyze.js` capture (it carries the nested tree via `i`/`parent`/`depth` + geometry
  *and* the computed `comp` styles), so `target.structure.json` and
  `target.styles.json` can both be derived from it.
- **The functional-gaps document** (`functional-gaps.md`): always produced.
- **Ask before removing working functionality** when honouring the mock would regress a
  richer wired feature the app already has (very common on the web, per "app is ahead"
  above).
