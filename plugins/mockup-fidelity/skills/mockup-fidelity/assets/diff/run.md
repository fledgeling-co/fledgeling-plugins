# Running the differ — `capture.mjs` (harness) and `analyze.js` (injectable)

Two artifacts, one contract. **`analyze.js`** is a single self-contained, eval-injectable **browser**
IIFE — no Node, no imports — that both captures a page's full analysis and computes the entire diff
in-page, returning a **JSON string**. **`capture.mjs`** is the Node harness that drives it (`obscura serve`
over CDP + `odiff-bin`), injects it verbatim, and layers on the rendered signals an injected eval cannot
reach: a full-page screenshot, per-element raster crops, and IoU pairing for text-less nodes.

**For web↔web, use the harness.** The raw `mfeval.mjs` flow below remains correct and is still the route
for the multi-width responsive capture and for RN-adjacent cases the harness does not cover.

The detector inventory and the rationale behind every threshold live in
[`../../references/issue-to-check-map.md`](../../references/issue-to-check-map.md); the engine's measured
limits live in
[`../../references/engine-capability-matrix.md`](../../references/engine-capability-matrix.md). This file is
the operator manual: flags, contracts, commands, and the traps in getting a payload into a page.

## Before you read a score: nine detector classes are switched OFF here

A runtime preflight in `analyze.js` probes the engine and switches off every class it cannot measure —
**shadow, gradient (the CSS half), text-transform, transition, animation, flex shorthand,
pseudo-elements, `::placeholder`, and SVG glyph extent** — reporting `available:false` with a verbatim
reason instead of agreeing. Three consequences you have to hold while reading any artifact:

- **Pseudo-element measurement is REFUSED, not merely unavailable.** `getComputedStyle(el, '::after')`
  ignores the pseudo argument and returns the element's own computed style, so reading it would fold the
  element's own border in as if the pseudo drew it.
- **Icon-glyph and trailing-arrow checks fall back to svg PRESENCE** (the laid-out box) because
  `getBBox()` returns an all-zero rect without throwing. Those findings are labelled presence-only: a
  MISSING arrow is caught, a wrong-size or swapped glyph is not.
- **Zero findings in a silenced class is not a pass** — it is a question nobody asked. `summary.scoreCovers`
  gives the score its denominator and `summary.scoreCaveat` says the rest in words.

All of it is measured, dated and versioned in
[`engine-capability-matrix.md`](../../references/engine-capability-matrix.md) — the single home for these
facts. Re-measure there, not here.

## The harness — `capture.mjs`

```bash
npm install            # in assets/diff — installs odiff-bin@4.3.8 (prebuilt binaries, no node-gyp).
                       # The browser is `obscura` on PATH; there is no browser package to install.
node capture.mjs --ref <referenceURL> --target <targetURL> --out .mockup-fidelity/<screen> \
  --chrome-selector __none__ --assert
#   e.g. --ref https://diolog.app/ --target http://diolog.site/ --out ./mf-home --width 1280 --height 2000
```

| flag | default | meaning |
|---|---|---|
| `--ref` / `--target` | — (required) | reference (the LIVE URL) and target — a URL or a local file path |
| `--out` | — (required) | artifact directory (created) |
| `--analyze` | `./analyze.js` | path to the analyzer to inject |
| `--width` / `--height` | `1280` / `2000` | viewport (the same on both sides) |
| `--frame-selector` / `--frame-title` / `--frame-index` | — | forwarded to `analyze.js __MF_OPTS__` |
| `--chrome-selector` | `__none__` | forwarded — `__none__` so web app chrome IS measured |
| `--iou` | `0.9` | IoU threshold for text-less pairing |
| `--raster-min` | `64` | min element area (px²) to raster-diff (skips 1px slivers) |
| `--raster-max` | `600` | cap on paired elements raster-diffed (runtime guard) |
| `--no-raster` | off | skip the raster layer |
| `--cdp-port` | — | attach to an `obscura serve` already running instead of starting one |
| `--assert` | off | exit nonzero unless the run is a clean **and complete** pass (below) |
| `--allow-inconclusive` | off | downgrade exit 3 to 0 — only after every silenced class is confirmed elsewhere |

**`--assert` exit codes are three-valued, because a check that could not run is neither a pass nor a fail:**

| code | meaning |
|---|---|
| `0` | clean AND complete — no high-severity findings, and every detector class ran |
| `1` | FINDINGS — at least one high-severity finding |
| `2` | usage / fatal error |
| `3` | INCONCLUSIVE — a detector class the verdict depended on could not run in this engine |

`3` is checked BEFORE `1` and wins: an inconclusive run is not reported as a findings run. `1` means
"these differ", `3` means "nobody asked". `--allow-inconclusive` downgrades `3` once every class in
`inconclusive[]` has been confirmed in a real browser and the ledger records where — it is not a way to
make the number go green.

The preflight block prints on **every** run, not only under `--assert`, because the number a reader takes
away is "0 findings" and that block is the sentence saying what those zeros cover. Reason strings are
relayed verbatim; a paraphrase is what turns "this layer cannot run here" into "the shadows match".

Outputs in `--out`: `reference.analysis.json` (MODE A), **`target.findings.json`** (MODE B + the raster
layers), `{reference,target}.full.png` (raster sources), `raster/pair-N-diff.png` (diff crops for raster
findings).

> **The target dir needs its own `node_modules`.** When the skill copies `assets/diff/*` into a project's
> `.mockup-fidelity/`, run `npm install` there too (the harness imports `odiff-bin`). `obscura` comes from
> PATH, not from `node_modules`.

## The architecture

> *A script injected into the page performs a full analysis AND diff; the skill's logic uses the output to
> determine what to change.*

`analyze.js` has two MODES, selected by whether a reference analysis is present on `globalThis`:

- **MODE A** (`globalThis.__MF_REFERENCE__` absent / null): capture and RETURN the full **analysis** of the
  current page — every per-element field the detectors need (`comp`, `glyph`, `wrap`, `hardBreak`, `lines`,
  `bgLayer`, `fullBleedMedia`, `divider`, `hasSvgChild`, `arrowGlyph`, `exactW`, `featReq`, `pseudoContent`,
  `pseudoStyle`, `istates`, `anims`, `fid`, `rect`, …) plus the `capabilities` preflight block. Shape:
  `{ title, viewportW, frame:{w,h,contentH}, fonts, capabilities, nodes:[…] }`.
  **Run this on the LIVE reference first.**
- **MODE B** (`globalThis.__MF_REFERENCE__` = a MODE-A analysis object): capture the current (TARGET) page
  analysis, then compute the **full diff in-page** across every detector class that the preflight left
  available, and RETURN a structured, prioritised, **actionable** result.

### MODE B return shape

```jsonc
{
  "summary": {
    "score": 20,                // 0–100, DISCRIMINATING: 100·e^(−penalty/900), penalty weighted
                                // high=5 med=2 low=0.5. Never hard-floors on a full page, so it ranks
                                // pages and tracks progress (near-clean≈85, ~400 findings≈30, very
                                // divergent≈9). Quote it only WITH scoreCaveat when one is present.
    "scoreCovers": { "detectorClassesProbed": 9, "ran": 0, "silenced": 9, "fraction": 0 },
    "scoreCaveat": "…INCONCLUSIVE, not 20% matching. Quote it with this sentence or not at all.",
    "conclusive": false, "inconclusiveCount": 9,
    "capabilities": { "reference": {…}, "target": {…} },   // the preflight verdicts, per side
    "totalFindings": 519,
    "bySeverity": { "high": 165, "med": 292, "low": 62 },
    "byClass": { "border": 30, "font": 57, "container-bg": 20, "structure": 112, "geometry": 84,
                 "rhythm": 2, "spacing": 69, "media": 1, "icon": 6, "wrap": 32, "value": 2,
                 "transform": 1, "extra": 60, "interaction": 12, "responsive": 21, "position": 3,
                 "raster": 5 },
    "frame": { "reference": {…}, "target": {…}, "sameViewport": true, "geometry": true },
    "layers": { "analyze": 514, "cdpRenderedFont": { "available": false, "reason": "…" },
                "raster": { "pairsCompared": 40, "mismatches": 31, "emitted": 5 },
                "iouTextlessPairs": 16 }        // harness-only (capture.mjs)
  },
  "findings": [
    {
      "id": "mf1",
      "locator": "text \"Book a demo\"  ·  a.framer-xxx  ·  @540,17 97×40",
      "section": "Compliance coverage",        // nearest section eyebrow/heading
      "class": "gradient",                    // geometry|font|container-bg|border|shadow|gradient|layout|
                                              // structure|rhythm|value|transform|pseudo|animation|wrap|
                                              // icon|spacing|media|fonts|screen-bg|extra|interaction|
                                              // responsive|position|raster
      "property": "bg-media-layer",
      "target": "none", "reference": "img",
      "deltaPx": 17,                          // present where a pixel delta is meaningful
      "severity": "high",                     // high|med|low
      "suggestedChange": "add the full-bleed img gradient/media layer to this container (FLAT on target)"
    }
  ],
  "inconclusive": [                            // TOP-LEVEL, not under summary. Survives every layer.
    { "capability": "pseudoElements", "sides": ["reference","target"],
      "detectors": ["border/pseudo-*", "pseudo/content (missing bullets and counters)", "…"],
      "reason": "<verbatim engine reason>", "measured": {…} }
  ],
  "noiseExcluded": {                           // confident NOISE kept OUT of findings/total/score
    "repeatedTextMispairs": [ { "text": "diolog", "chosenY": 23, "otherCount": 1 } ],
    "illustrationInternals": [ … ],            // incl. suppressed placeholder-TEXT entries
    "unpairedSameText":   [ { "side": "target", "text": "…", "tag": "div", "y": 412 } ],
    "crossDomStructure":  [ { "detector": "layout", "candidates": 40, "paired": 0, "unpaired": 40 } ]
  },
  "rasterDetail": [ … ],                       // harness-only: full per-pair raster evidence
  "analysis": { /* the full TARGET analysis, so you can re-diff or inspect without re-measuring */ }
}
```

Findings are **sorted** high→low severity, then by `deltaPx`. The four `noiseExcluded` buckets are excluded
from `findings` / `totalFindings` / `score` so the headline reflects only confident findings; inspect them
separately. A single repeating root cause (every `<li>` missing the same `•`, a site-wide `cv11`) is deduped
to at most three rows plus one `[×N elements]` summary finding.

## The `globalThis.__MF_*` contract

Everything the injectable reads, set in `--setup` in the **same page**:

| global | what it does |
|---|---|
| `__MF_REFERENCE__` | a MODE-A analysis object → selects MODE B. Absent/null → MODE A. |
| `__MF_OPTS__` | the options object below. |
| `__MF_REFERENCE_BYWIDTH__` | `{390,768,1280}` → reference analyses keyed by `viewportW` (responsive). |
| `__MF_TARGET_BYWIDTH__` | the same for the target. `responsive` runs only when BOTH are present and share at least the 390 + 1280 entries; otherwise the pass is skipped. |
| `__MF_FEATURE_DIFFS__` | `{reference:[{key,effective}], target:[…]}` from `feature-check.mjs` — real browser only. |
| `__MF_PROBE__` | exposed BY the injectable: call it to run the capability preflight alone, without a full capture. |

### Options (`__MF_OPTS__`)

```jsonc
{
  "frameSelector": "#screen .scr",   // a CSS selector for the frame root (a React/StyleX screen root)
  "frameTitle": "Discover · home",   // OR a figcaption/caption substring (HTML gallery)
  "frameIndex": 13,                  // OR a 1-based gallery ordinal, when captions repeat
  "frameContainer": "figure, .frame", "captionSelector": "figcaption, .cap",
  "chromeSelector": "__none__",      // WEB↔WEB: "__none__" so the app nav/header IS measured (it is
                                     // content on both sides). The default skip-list is RN native chrome.
  "geom": true,                      // force geometry on/off (auto-on when frames match within 5%)
  "geomTolCenter": 6, "geomTolSize": 10, "geomTolHeight": 2
}
```

`frameTitle` searches the union `figure, .frame` for a container whose `figcaption, .cap` text includes the
title, then takes the inner `.scr`/`.screen` as the frame root — so **both common gallery markups work out
of the box**. Override `frameContainer` / `captionSelector` for a third markup.

## The flow — `mfeval.mjs`

`mfeval.mjs` is the shell-facing runner: it navigates at a chosen viewport, evaluates a `--setup`
expression in that same page, then evaluates the injectable and writes what it returns. It exists because
neither cheaper entry point can do this job — `obscura fetch` renders at a fixed 1280×720 with no resize
and does not await a returned promise, and `obscura mcp`'s `browser_evaluate` holds a session but likewise
does not await and has no viewport control.

```bash
# (1) MODE A on the LIVE reference → reference.json
node mfeval.mjs --url "https://diolog.app/" --width 1280 --height 2000 \
  --setup -e "(() => { globalThis.__MF_OPTS__ = { chromeSelector: '__none__' }; globalThis.__MF_REFERENCE__ = null; return 'a'; })()" \
  --eval analyze.js --out reference.json
#   the LIVE rendered site, NOT a re-served scrape. --out writes the returned JSON verbatim —
#   there is no second layer of encoding to unwrap.

# (2) On the TARGET: set globalThis.__MF_REFERENCE__ = <reference.json>, then eval analyze.js → findings
node -e 'const fs=require("fs");let v=JSON.parse(fs.readFileSync("reference.json","utf8"));if(typeof v==="string")v=JSON.parse(v);fs.writeFileSync("__setref.js","(() => { globalThis.__MF_OPTS__ = { chromeSelector: \"__none__\" }; globalThis.__MF_REFERENCE__ = "+JSON.stringify(v)+"; return \"r\"; })()")'
node mfeval.mjs --url "http://diolog.site/" --width 1280 --height 2000 \
  --setup __setref.js --eval analyze.js --out findings.json    # MODE B → the actionable findings

# (3) Read the findings and apply each suggestedChange.
node -e 'let v=JSON.parse(require("fs").readFileSync("findings.json","utf8"));if(typeof v==="string")v=JSON.parse(v);console.log("score",v.summary.score,"·",v.summary.totalFindings,"findings","· conclusive",v.summary.conclusive);(v.inconclusive||[]).forEach(i=>console.log("  INCONCLUSIVE:",i.capability,"→",i.detectors.join(", ")));v.findings.filter(f=>f.severity==="high").slice(0,40).forEach(f=>console.log("["+f.severity+"] "+f.class+"/"+f.property+" @ "+(f.section||"-")+" :: "+f.suggestedChange))'
```

A target on `localhost` or `127.0.0.1` needs no extra flag — `mfeval.mjs` starts its `obscura serve` with
`--allow-private-network` already, because without it every navigation fails as an SSRF block and reads
like a broken page. Flags: `--url`, `--eval`, `--setup <file|-e expr>`, `--out`, `--width` (1280),
`--height` (2000), `--settle` (1500ms), `--cdp-port`.

### Two diagnostics that look like broken pages

- **`--setup` must be a *called* expression.** If your findings file comes out as a
  `{title,viewportW,…,nodes}` analysis (MODE A) instead of `{summary,findings,…}`, the reference injection
  did not land: check that `--setup` ran and that its file is a called expression (`(() => {…})()`, not a
  bare `() => {…}`). `--setup` and `--eval` run in the SAME page, which is the whole point of
  `mfeval.mjs` — every `obscura fetch` is a fresh render, so a global set by one call is gone by the next.
- **`capture()` is async**, so the injectable is `(async function(){…})()` resolving to the JSON string.
  `mfeval.mjs` and `capture.mjs` both evaluate with `awaitPromise:true`, so it resolves transparently.
  `obscura fetch --eval` and the MCP `browser_evaluate` do **not** await — they return `{}` for an async
  IIFE — so **neither can run `analyze.js`**.

## Multi-width (responsive) capture — the `ARG_MAX` finding

The `responsive` class needs both sides captured at `WIDTHS=[390, 768, 1280]`, then all six analyses handed
to one MODE-B run.

```bash
# ── (1) MODE A on BOTH sides at all three widths ───────────────────────────────
WIDTHS="390 768 1280"
mka () { # url out width
  node mfeval.mjs --url "$1" --width "$3" --height 4000 --settle 1500 \
    --setup -e "(() => { globalThis.__MF_OPTS__={chromeSelector:'__none__'};
      globalThis.__MF_REFERENCE__=null; globalThis.__MF_REFERENCE_BYWIDTH__=null;
      globalThis.__MF_TARGET_BYWIDTH__=null; return 'a'; })()" \
    --eval analyze.js --out "$2"
}
for w in $WIDTHS; do
  mka "https://diolog.app/"  "home-ref-$w.json" "$w"     # LIVE reference
  mka "http://diolog.site/"  "home-tgt-$w.json" "$w"     # target
done

# ── (2) Inject the 6 captures via a CORS fetch, then MODE B at 1280 ────────────
node mfserve.js "$PWD" 8799 &                              # tiny CORS static server (mfserve.js)
cat > __setbywidth.js <<'JS'
(async () => {
  const B='http://localhost:8799/', S='home';
  const ld=async n=>{const r=await fetch(B+n);let v=await r.json();if(typeof v==='string')v=JSON.parse(v);return v;};
  const refBy={}, tgtBy={};
  for (const w of [390,768,1280]) { refBy[w]=await ld(S+'-ref-'+w+'.json'); tgtBy[w]=await ld(S+'-tgt-'+w+'.json'); }
  globalThis.__MF_OPTS__={chromeSelector:'__none__'};
  globalThis.__MF_REFERENCE__=refBy[1280];               // the 1280 single reference (drives the normal diff)
  globalThis.__MF_REFERENCE_BYWIDTH__=refBy;             // {390,768,1280} reference analyses
  globalThis.__MF_TARGET_BYWIDTH__=tgtBy;                // {390,768,1280} target analyses
  return 'set';
})()
JS
node mfeval.mjs --url "http://diolog.site/" --width 1280 --height 4000 \
  --setup __setbywidth.js --eval analyze.js --out home-findings.json   # MODE B + interaction + responsive
```

> **Why the localhost fetch, not `$(cat …)`?** **A single 1280 reference is already ~1MB and the three-width
> pair is ~6MB** — both blow the shell's `ARG_MAX` (1 MB on macOS), which fails with `argument list too
> long` if you pass the reference inline. The CORS server + in-page `fetch()` is the reliable injection path
> for any reference above a few hundred KB. The bundled `mfserve.js` is a ~12-line zero-dep static server
> that sets `Access-Control-Allow-Origin: *`; the page fetching from it is why `mfeval.mjs` runs Obscura
> with `--allow-private-network`.
>
> Note the `--setup` file here is an ASYNC IIFE, and `mfeval.mjs` awaits it — the shell-facing alternatives
> do not, which is the whole reason it exists.

The per-width sub-diff is re-entrancy-guarded (`diff._inResponsive`) so the 390/768 re-diffs do not
recursively re-run the responsive pass. `viewportW` is recorded on every MODE-A analysis (the injection
viewport, independent of the frame's own measured width) so the bywidth maps key cleanly even when a frame
is narrower than the viewport.

## `feature-check.mjs` — a real browser only, never an obscura capture

`feature-check.mjs` pixel-diffs the on/off probe pairs `capture()` mounts, returning `{key, effective}`
verdicts you inject via `__MF_FEATURE_DIFFS__` for MODE B:

```bash
node feature-check.mjs --analysis reference.json --png ref-page.png --out ref-featdiffs.json  # [--dpr N]
#   effective:false = the requested OpenType feature has NO effect (a subset font lacks the glyph).
```

The analysis and the screenshot must come from the SAME engine and the same run — a probe rect measured in
one browser and a PNG rasterised by another do not line up. **Under obscura the verdict inverts**: no web
font loads, so both probe rows render the same fallback face, every pair comes back identical, and identical
MEANS "ineffective" — every requested feature is reported as a defect, confidently and wrongly
([capability matrix](../../references/engine-capability-matrix.md)). If nothing resolves a combo, MODE B
emits ONE low `font/feature-check-pending` row rather than a silent pass.

## Notes

- **Same viewport on both sides**, so absolute geometry (center-x / width / height) compares like-for-like;
  geometry auto-enables when the two frames match within 5%.
- **Reference the LIVE URL, never a re-served scrape** — a runtime-hydrated framework (Framer, any SPA)
  resolves a different variant off-origin. `analyze.js` runs fine against `https://…`. The measured
  divergences are in [`README.md`](./README.md).
- **`data-fid` anchoring** — put the same `data-fid` (or `data-fidelity-id` / `data-testid`) on the matching
  reference + target nodes to make a region's pairing exact. It is the primary match key, and the reliable
  kill for a repeated-text mispair.
- **Authoring-agnostic.** The analyzer reads `getComputedStyle` from the **rendered DOM**, so the mock's
  authoring tech does not matter — served HTML+CSS, a React/Next route, or StyleX (whose atomic classes and
  `defineVars` variables resolve like any other CSS) all work. What matters is that it renders in a browser.
