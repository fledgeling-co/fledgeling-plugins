// mockup-fidelity SINGLE-SCRIPT analyzer + differ — the browser-injectable mechanical analytic.
//
// THIS REPLACES the three-file two-step pipeline (extract-mock.js + diff.mjs +
// structure-diff.mjs). It is ONE self-contained, eval-injectable browser IIFE — no Node,
// no imports — that runs via `obscura serve` + CDP Runtime.evaluate and returns a JSON
// STRING.
//
// It has two MODES, selected by whether a reference analysis is present on globalThis:
//
//   MODE A (no globalThis.__MF_REFERENCE__):
//     Capture and RETURN the full ANALYSIS of the current page — the union of everything
//     extract-mock.js captured plus every per-element field the detectors need. Run this on
//     the LIVE reference first; save the returned JSON as reference.json.
//
//   MODE B (globalThis.__MF_REFERENCE__ = <a MODE-A analysis object>):
//     Capture the current (TARGET) page analysis, then compute the FULL DIFF IN-PAGE across
//     ALL detector classes — the exact comparisons diff.mjs + structure-diff.mjs did (pairing
//     by stable key/path then geometry fallback, repeated-text disambiguation, the non-text
//     container pass, the v1.16 detectors, etc.) — and RETURN a structured, PRIORITISED,
//     ACTIONABLE result the skill's logic can act on directly:
//       { summary:{score, totalFindings, byClass:{…}},
//         findings:[ { id, locator, section, class, property, target, reference,
//                      deltaPx?, severity, suggestedChange } ],
//         noiseExcluded:{ repeatedTextMispairs, illustrationInternals },
//         analysis:<the target analysis> }
//
// Options (optional) via globalThis.__MF_OPTS__:
//   { frameSelector, frameTitle, frameIndex, frameContainer, captionSelector,
//     chromeSelector, geom (force on/off), geomTolCenter, geomTolSize, geomTolHeight }
//   For a web↔web comparison set chromeSelector:'__none__' so the app nav/header is measured.
//
// WHY computed, never source: getComputedStyle on the RENDERED DOM is the only truth — a
// class `.ai-card` may declare no box-shadow yet `class="card ai-card"` still HAS one
// (inherited). Read the computed value, never the individual class rules. Authoring-agnostic:
// works the same on a hand-written HTML mockup, a React/Next route, or a StyleX app.
//
// EVERY detector from the prior pipeline is ported (lose none): geometry center-x/w/h,
// line-height-normal, icon-glyph, text-wrap, pseudo-border-fold, hard-break, line-count,
// gap-sibling, non-text-container bg/gradient/divider/border/shadow, repeated-text
// disambiguation, wrap-point, rendered-font, media-geometry, AND the v1.16 additions:
// layout-structure, vertical-rhythm, value-precision, transform/opacity/filter,
// pseudo-content, animation. Plus the structure-diff layout/child-count/missing/extra pass.
//
// v2.5.0 — the RASTER + CDP-rendered-font + IoU-text-less + systematic-pseudo layer. analyze.js gains the
//   SYSTEMATIC PSEUDO-ELEMENT STYLE capture (`pseudoStyle` per node: ::before/::after content, border-
//   width/-color, background/-image, box-shadow, position, border-radius) and a MODE-B pass that compares
//   it for EVERY paired element (not just illustrations / not just the border-fold), so a pseudo-DRAWN
//   border or overlay present/different on one side is caught universally. The other v2.5.0 layers
//   (element-scoped odiff raster diff, IoU bounding-box pairing for text-less nodes) run
//   in the Node-side HARNESS `capture.mjs` (`obscura serve` over CDP + odiff-bin), which injects THIS analyze.js
//   verbatim (MODE A on the reference, MODE B on the target — contract unchanged) and ENRICHES its findings
//   with bbox-delta + odiff mismatch%. The third layer — the CDP rendered-font check
//   (CSS.getPlatformFontsForNode) — is UNAVAILABLE under Obscura: it returns {}, DOM.requestNode is not
//   implemented, and no web font is ever loaded, so both sides render the same fallback face. The harness
//   records that layer as `available:false` rather than as zero divergences. Confirm any typeface question
//   in a real browser. See run.md § v2.5.0 and capture.mjs.
//
// v2.4.0 — three additive low-noise detectors closing recall-test blind spots:
//   (1) PER-ELEMENT VERTICAL OFFSET (`position/rel-offset`) — a matched element MOVED inside its parent
//       (a flex align-items/justify change, a top-margin shift) at the SAME size, caught per-element (not
//       only via the parent's layout/align-items diff). Pure-move guarded (own w&h ~equal) + deduped per
//       parent (a whole column shifting by one delta = ONE finding + a [×N] summary).
//   (2) BLOCK-FLOW GAP between NON-TEXT containers (`spacing/gap→next-sibling(block-flow)`) — the gap to a
//       paired block container's next sibling (next.top − this.bottom, INCLUDING margin), so block-flow
//       margin/padding spacing between block boxes is checked, not only flex/grid `gap` or text-paired gaps.
//   (3) VALUE-BASED LINE-HEIGHT — the line-height check now compares the RESOLVED px value with a tight
//       ~0.6px tolerance (was a max(2, 0.12·fs) height-proxy floor that swallowed a 0.75px label delta);
//       AND the illustration-internal STYLE pass gained `font/illo-line-height` so internal text rows are
//       line-height-checked directly.

(async function () {
  'use strict';

  const OPTS = (typeof globalThis !== 'undefined' && globalThis.__MF_OPTS__) || {};
  const REFERENCE = (typeof globalThis !== 'undefined' && globalThis.__MF_REFERENCE__) || null;
  // RESPONSIVE-TRANSITION inputs — the runner extracts BOTH sides at WIDTHS=[390,768,1280] (MODE A
  // each), then on the final MODE-B run hands analyze.js the reference + target analyses keyed by
  // width. With these present, MODE B additionally computes the desktop→mobile layout TRANSITION
  // per side and emits a finding wherever the transitions DIVERGE (live collapses a 2-col grid to
  // 1-col at 390 but the target stays 2-col; live nav→hamburger, target doesn't), plus the normal
  // per-width findings surfaced at 390/768. Each value is a MODE-A analysis object (or its JSON).
  const REFERENCE_BYWIDTH = (typeof globalThis !== 'undefined' && globalThis.__MF_REFERENCE_BYWIDTH__) || null;
  const TARGET_BYWIDTH = (typeof globalThis !== 'undefined' && globalThis.__MF_TARGET_BYWIDTH__) || null;

  // ======================================================================
  // PART 0 — THE CAPABILITY PREFLIGHT
  // ======================================================================
  // A check whose "pass" and "cannot run" look identical must report which one it is. Both sides of
  // this diff render in the SAME engine, so a property the engine does not implement comes back the
  // same on both — and the comparison emits nothing. Not a miss you can see: a PASS you cannot.
  //
  // Measured on this machine 18 Aug 2026, obscura 0.2.0: `boxShadow`, `backgroundImage`,
  // `textTransform`, `transitionProperty/Duration`, `animationName/Duration` and `flex`/`flexGrow` all
  // return `""` for a rule that is unambiguously set; `path.getBBox()` returns an all-zero rect and
  // does NOT throw; and `getComputedStyle(el, '::after')` silently IGNORES the pseudo argument and
  // returns the ELEMENT's own computed style — so a pseudo read is not merely empty, it is a
  // plausible WRONG value that would fold the element's own border in as if the pseudo drew it.
  //
  // `CSS.supports()` is NOT a usable substitute, measured on the same run: it answered `true` for
  // `text-transform`, `background-image`, `animation` and `flex` (all of which compute to `""`), and
  // `false` for `letter-spacing` (which works). Four false-positives and one false-negative out of
  // ten. Only a ROUND TRIP through the engine's own cascade — set a declaration on a live probe node,
  // read the computed value back, compare — answers the question the differ actually asks.
  //
  // Every probe below is therefore set-and-read-back. `available:false` carries the reason string, and
  // the reason is relayed verbatim rather than paraphrased: it names the engine and what it returned.
  function probeCapabilities() {
    const caps = {};
    const mark = (key, ok, reason, detail) => {
      caps[key] = ok ? { available: true } : { available: false, reason, ...(detail ? { measured: detail } : {}) };
    };
    let host = null;
    try {
      host = document.createElement('div');
      // Off-screen but LAID OUT — a display:none node resolves used values differently, which would
      // make the probe answer a question nobody asked.
      host.setAttribute('style', 'position:absolute;left:-9999px;top:0;width:120px;height:40px;');
      document.body.appendChild(host);
    } catch (e) {
      return { probeFailed: { available: false, reason: 'could not mount a probe node: ' + (e && e.message) } };
    }
    // roundTrip — set `decl` on the probe via a real stylesheet rule (the path every authored page
    // takes; an inline style attribute is echoed back VERBATIM by this engine even when the property
    // is unimplemented, so an inline probe would report a false PASS).
    let sheet = null, ruleIdx = 0;
    try {
      const st = document.createElement('style');
      document.head.appendChild(st);
      sheet = st.sheet;
    } catch (e) {}
    const readWith = (prop, decl) => {
      if (!sheet) return { err: 'no probe stylesheet' };
      const cls = 'mfprobe' + (ruleIdx++);
      try { sheet.insertRule('.' + cls + '{' + decl + '}', sheet.cssRules.length); } catch (e) { return { err: 'insertRule refused: ' + (e && e.message) }; }
      host.className = cls;
      let got = null;
      try { got = getComputedStyle(host)[prop]; } catch (e) { host.className = ''; return { err: 'getComputedStyle threw: ' + (e && e.message) }; }
      host.className = '';
      return { got: got };
    };
    // TWO SENTINELS, NOT ONE — the probe is METAMORPHIC: changing the input must change the
    // observation. A single sentinel can accidentally equal an initial value, an engine fallback or a
    // hard-coded constant, and a stub that returns the same thing for every input passes a one-shot
    // probe. Requiring the two reads to DIFFER is what catches a constant-return reader, and it names
    // that case separately (NON_DISCRIMINATING_READ) so the reason a class was switched off is legible.
    const roundTrip = (prop, declA, declB, expectFn) => {
      const a = readWith(prop, declA);
      if (a.err) return { ok: false, got: null, why: a.err };
      const b = readWith(prop, declB);
      if (b.err) return { ok: false, got: null, why: b.err };
      if (!expectFn(a.got)) return { ok: false, got: a.got, why: 'EMPTY_OR_UNEXPECTED_COMPUTED_VALUE' };
      if (a.got === b.got) return { ok: false, got: a.got, why: 'NON_DISCRIMINATING_READ (both sentinels read back as ' + JSON.stringify(a.got) + ', so this reader cannot tell two different declarations apart)' };
      return { ok: true, got: a.got, second: b.got };
    };
    const nonEmpty = v => v != null && v !== '' && v !== 'none' && v !== 'normal';

    // --- shadow -------------------------------------------------------------
    {
      const r = roundTrip('boxShadow', 'box-shadow: 3px 5px 7px 11px rgb(1,2,3);', 'box-shadow: 2px 4px 6px 8px rgb(17,19,23);', nonEmpty);
      mark('shadow', r.ok, 'box-shadow was set to `3px 5px 7px 11px rgb(1,2,3)` and getComputedStyle returned ' + JSON.stringify(r.got) + '. This engine does not compute box-shadow and there is no working longhand, so the shadow class cannot be measured here on EITHER side — a shadow present on one side and absent on the other reads as agreement. Confirm shadow presence and depth in a real browser.', r.got);
    }
    // --- gradient / background-image ----------------------------------------
    {
      const r = roundTrip('backgroundImage', 'background-image: linear-gradient(rgb(1,2,3), rgb(4,5,6));', 'background-image: linear-gradient(45deg, rgb(7,8,9), rgb(10,11,12));', nonEmpty);
      mark('gradient', r.ok, 'background-image was set to `linear-gradient(rgb(1,2,3), rgb(4,5,6))` and getComputedStyle returned ' + JSON.stringify(r.got) + '. CSS gradients and `url()` backgrounds cannot be measured here. The full-bleed MEDIA-child half of the backdrop check (an <img>/<svg> layer) is unaffected and still runs; the CSS half does not.', r.got);
    }
    // --- text-transform -----------------------------------------------------
    {
      const r = roundTrip('textTransform', 'text-transform: uppercase;', 'text-transform: lowercase;', v => v === 'uppercase');
      mark('textTransform', r.ok, 'text-transform was set to `uppercase` and getComputedStyle returned ' + JSON.stringify(r.got) + '. An all-caps-vs-title-case header whose SOURCE text is identical cannot be measured here at all. Where the two sides differ in their SOURCE text the case difference surfaces as a `breadth/unpaired-mock-text` row rather than as a text-transform finding — so it arrives, but under a different name and only if you work the breadth rows.', r.got);
    }
    // --- transition ---------------------------------------------------------
    {
      const r = roundTrip('transitionDuration', 'transition: color 1s;', 'transition: color 2.5s;', v => nonEmpty(v) && v !== '0s');
      mark('transition', r.ok, 'transition was set to `color 1s` and getComputedStyle().transitionDuration returned ' + JSON.stringify(r.got) + '. Declared transitions cannot be measured here.', r.got);
    }
    // --- animation ----------------------------------------------------------
    {
      const r = roundTrip('animationName', 'animation: mfprobekfa 2s infinite;', 'animation: mfprobekfb 3s infinite;', nonEmpty);
      let running = null;
      try { running = document.getAnimations ? document.getAnimations().length : null; } catch (e) {}
      mark('animation', r.ok, 'animation was set to `mfprobekfa 2s infinite` and getComputedStyle().animationName returned ' + JSON.stringify(r.got) + '; document.getAnimations() reported ' + running + '. This engine executes no CSS animations or transitions, so the motion class cannot be measured. An `opacity:0` entry keyframe also STRANDS its element at near-zero opacity here — treat a washed-out element as an engine artefact to verify in a real browser, never as an application defect.', r.got);
    }
    // --- flex shorthand -----------------------------------------------------
    {
      const a = roundTrip('flex', 'display:flex; flex: 1 1 auto;', 'display:flex; flex: 2 0 30px;', nonEmpty);
      const b = roundTrip('flexGrow', 'display:flex; flex: 1 1 auto;', 'display:flex; flex: 2 0 30px;', nonEmpty);
      mark('flexShorthand', a.ok || b.ok, 'flex was set to `1 1 auto`; getComputedStyle().flex returned ' + JSON.stringify(a.got) + ' and .flexGrow returned ' + JSON.stringify(b.got) + '. Unlike padding and margin, whose longhands ARE correct here, flex has no working longhand — so flex-grow/shrink/basis reasoning has nothing to read. `display`, `flexDirection`, `rowGap` and `columnGap` are unaffected and still carry the layout class.', a.got);
    }
    // --- pseudo-elements: REFUSED, not merely unavailable --------------------
    // This one is different in kind. The others return an empty value; this returns a WRONG one.
    {
      let verdict = false, detail = null;
      try {
        const cls = 'mfprobe' + (ruleIdx++);
        if (sheet) {
          sheet.insertRule('.' + cls + '{border-top:9px solid rgb(9,9,9)}', sheet.cssRules.length);
          sheet.insertRule('.' + cls + '::after{content:"X";border-top:3px solid rgb(3,3,3)}', sheet.cssRules.length);
          host.className = cls;
          const own = getComputedStyle(host);
          const ps = getComputedStyle(host, '::after');
          detail = { pseudoContent: ps.content, pseudoBorderTopWidth: ps.borderTopWidth, elementBorderTopWidth: own.borderTopWidth };
          // Sound only when the pseudo read returns the PSEUDO's own declaration (3px) and its content.
          verdict = ps.content !== '' && ps.content !== 'none' && parseFloat(ps.borderTopWidth) === 3;
          host.className = '';
        }
      } catch (e) { detail = { threw: e && e.message }; }
      mark('pseudoElements', verdict, 'A probe declared `border-top: 9px` on the element and `content:"X"; border-top: 3px` on its ::after. getComputedStyle(el, "::after") returned content ' + JSON.stringify(detail && detail.pseudoContent) + ' and borderTopWidth ' + JSON.stringify(detail && detail.pseudoBorderTopWidth) + ', while the ELEMENT\'s own borderTopWidth is ' + JSON.stringify(detail && detail.elementBorderTopWidth) + '. The pseudo argument is ignored and the element\'s own style is returned. This is REFUSED rather than merely unavailable: reading it would fold the element\'s own border in as if the pseudo drew it, double-reporting one defect as two and inventing values on both sides. The ::after border fold, the pseudo-content marker check (missing bullets and counters) and the systematic pseudoStyle comparison are all off here. A border, hairline, overlay or marker drawn on ::before/::after must be confirmed in a real browser.', detail);
    }
    // --- ::placeholder ------------------------------------------------------
    {
      let verdict = false, detail = null;
      try {
        const inp = document.createElement('input');
        inp.setAttribute('style', 'position:absolute;left:-9999px;top:0;');
        inp.className = 'mfprobeph';
        inp.placeholder = 'x';
        document.body.appendChild(inp);
        if (sheet) {
          sheet.insertRule('.mfprobeph{color:rgb(8,8,8)}', sheet.cssRules.length);
          sheet.insertRule('.mfprobeph::placeholder{color:rgb(1,2,3)}', sheet.cssRules.length);
        }
        const ph = getComputedStyle(inp, '::placeholder').color;
        detail = { placeholderColor: ph, inputColor: getComputedStyle(inp).color };
        verdict = /\b1\b/.test(String(ph)) && /\b2\b/.test(String(ph));
        inp.remove();
      } catch (e) { detail = { threw: e && e.message }; }
      mark('placeholder', verdict, '::placeholder colour was set to `rgb(1,2,3)` on an input whose own colour is `rgb(8,8,8)`; getComputedStyle(input, "::placeholder").color returned ' + JSON.stringify(detail && detail.placeholderColor) + '. The pseudo argument is ignored, so this reports the input\'s own colour on both sides. SKILL.md names ::placeholder colour as one of the two properties most often silently wrong; here it is unmeasurable. Confirm it in a real browser.', detail);
    }
    // --- SVG glyph extent ---------------------------------------------------
    {
      let verdict = false, detail = null;
      try {
        const NS = 'http://www.w3.org/2000/svg';
        const svg = document.createElementNS(NS, 'svg');
        svg.setAttribute('width', '20'); svg.setAttribute('height', '20');
        svg.setAttribute('style', 'position:absolute;left:-9999px;top:0;');
        const p = document.createElementNS(NS, 'path');
        p.setAttribute('d', 'M2 2 L14 9 Z'); p.setAttribute('fill', 'black');
        svg.appendChild(p); document.body.appendChild(svg);
        const b = p.getBBox ? p.getBBox() : null;
        detail = b ? { x: b.x, y: b.y, width: b.width, height: b.height } : { getBBox: 'absent' };
        verdict = !!(b && b.width > 0 && b.height > 0);
        svg.remove();
      } catch (e) { detail = { threw: e && e.message }; }
      mark('svgGlyphExtent', verdict, 'A path `M2 2 L14 9 Z` was measured with getBBox(), which returned ' + JSON.stringify(detail) + ' and did NOT throw. The drawn-glyph extent is unavailable, so icon-glyph size and the glyph-based trailing-arrow check cannot run. Arrow and icon PRESENCE falls back to `hasSvgChild`, which is captured and is a real signal — a missing trailing arrow is caught, a WRONG-SIZE or SWAPPED glyph is not. Findings from the fallback are labelled presence-only.', detail);
    }
    try { host.remove(); } catch (e) {}
    return caps;
  }
  // Callable on its own, so the preflight can be read without a full capture.
  try { globalThis.__MF_PROBE__ = probeCapabilities; } catch (e) {}

  // ======================================================================
  // PART 1 — CAPTURE THE CURRENT PAGE ANALYSIS  (the old extract-mock.js)
  // ======================================================================
  async function capture() {
    // Await webfont loading so the DOM-span rendered-font probe measures the FINAL faces, not a flash of
    // fallback. document.fonts.ready resolves once all pending @font-face loads settle.
    try { if (document.fonts && document.fonts.ready) await document.fonts.ready; } catch (e) {}
    const SEL = OPTS.frameSelector ?? (typeof window !== 'undefined' && window.MF_FRAME_SELECTOR);
    const TITLE = OPTS.frameTitle ?? (typeof window !== 'undefined' && window.MF_FRAME_TITLE);
    const INDEX = OPTS.frameIndex ?? (typeof window !== 'undefined' && window.MF_FRAME_INDEX); // 1-based ordinal
    const FRAME_SEL = OPTS.frameContainer || (typeof window !== 'undefined' && window.MF_FRAME_CONTAINER) || 'figure, .frame';
    const CAP_SEL = OPTS.captionSelector || (typeof window !== 'undefined' && window.MF_CAPTION_SELECTOR) || 'figcaption, .cap';
    const ROOT_PROBES = ['.scr', '.screen', '.frame', '.phone'];
    let CHROME = OPTS.chromeSelector ?? (typeof window !== 'undefined' && window.MF_CHROME_SELECTOR);
    if (CHROME == null) CHROME = '.sb, .island, .tabbar, .homebar, .nav, .statusbar, .notch';
    const CHROME_NONE = CHROME === '__none__';

    const screenOf = (fig) => {
      if (!fig) return null;
      for (const s of ROOT_PROBES) { const hit = fig.querySelector(s); if (hit) return hit; }
      return fig;
    };

    let root;
    if (SEL) root = document.querySelector(SEL);
    else if (INDEX != null && INDEX !== false) root = screenOf([...document.querySelectorAll(FRAME_SEL)][INDEX - 1]);
    else if (TITLE) {
      const fig = [...document.querySelectorAll(FRAME_SEL)].find(
        f => (f.querySelector(CAP_SEL)?.textContent || '').replace(/\s+/g, ' ').includes(TITLE),
      );
      root = screenOf(fig);
    } else root = document.body;
    if (!root) return { error: 'frame-not-found', selector: SEL, title: TITLE, index: INDEX };
    // THE PREFLIGHT RUNS BEFORE THE WALK. Every detector class below that reads a property this engine
    // does not compute is switched OFF here rather than left to return agreement, and the reason travels
    // in the artifact so the verdict can name what it could not measure.
    const CAPS = probeCapabilities();
    const CAN = k => !!(CAPS[k] && CAPS[k].available);
    const f = root.getBoundingClientRect();

    const PROPS = [
      'fontSize', 'fontWeight', 'fontFamily', 'fontStyle', 'color', 'backgroundColor',
      'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
      'marginTop', 'marginRight', 'marginBottom', 'marginLeft',
      'borderTopLeftRadius', 'borderTopWidth', 'borderTopColor',
      'borderBottomWidth', 'borderBottomColor',
      'boxShadow', 'display', 'flexDirection', 'alignItems', 'justifyContent',
      'textAlign', 'letterSpacing', 'lineHeight', 'opacity', 'textTransform',
      'textWrap', 'textWrapStyle',
      'gridTemplateColumns', 'gridAutoFlow', 'gap', 'columnGap', 'rowGap',
      'position', 'flexWrap', 'gridTemplateRows',
      'backgroundImage',
      'borderTopRightRadius', 'borderBottomLeftRadius', 'borderBottomRightRadius',
      'transform', 'filter',
      'transitionProperty', 'transitionDuration',
      // TYPOGRAPHIC-DECLARATION props (v2.5.1) — declared shaping that changes the RENDERED result but not
      // which font FILE loads, so the family-KIND check, the CDP getPlatformFontsForNode probe, and the
      // antialiased raster diff are ALL blind to them: font-feature-settings (cvXX single-vs-double-story 'a'),
      // font-variation-settings (a wght/opsz axis applied live but not on target), and the FULL font-family
      // DECLARATION (a long system stack vs `Inter, sans-serif` — same kind, different declared cascade).
      'fontFeatureSettings', 'fontVariationSettings',
    ];

    // RENDERED-FONT fingerprint (v2.0.2 — DOM-SPAN probe, NOT canvas).
    //
    // The old check used canvas `measureText`, which IGNORES `unicode-range` subsetting and does NOT
    // replicate the browser's real DOM font-matching cascade — so it could neither see a DOM-level
    // fallback (a registered face that the page is actually NOT applying to its text) nor avoid
    // over/under-firing on correctly-rendered nodes. The ground truth is the RENDERED width of a real
    // hidden DOM span: lay the probe string out twice for the SAME (family, weight, style, size) combo
    // — once with `'<NamedFamily>', <fallback>` and once with the bare `<fallback>` — and compare the
    // measured widths. If the named family is genuinely applying, the two widths differ (the named
    // face has distinct metrics); if width(named+fallback) === width(fallback) the browser fell back to
    // the generic, i.e. the named family is NOT being applied. We do this against BOTH a monospace and a
    // serif fallback: only if BOTH collapse to their fallback width do we conclude the named family does
    // not apply (a single fallback could coincidentally match the named face's metrics; two distinct
    // generics matching is decisive). This sees the real DOM cascade + unicode-range, unlike canvas.
    const GENERIC = /^(serif|sans-serif|monospace|system-ui|cursive|fantasy|ui-sans-serif|ui-serif|ui-monospace|-apple-system|"?BlinkMacSystemFont"?)$/i;
    const firstFamily = (fam) => String(fam || '').split(',')[0].replace(/["']/g, '').trim();
    // a single offscreen measuring host reused for every probe span (kept out of layout flow).
    const _probeHost = (() => {
      try {
        const h = document.createElement('div');
        h.setAttribute('aria-hidden', 'true');
        h.style.cssText = 'position:absolute;left:-99999px;top:-99999px;visibility:hidden;white-space:nowrap;pointer-events:none;contain:layout style;';
        (document.body || document.documentElement).appendChild(h);
        return h;
      } catch (e) { return null; }
    })();
    const FONT_PROBE = 'Diolog workspace 20 — investor-facing AaBbGg mmiiWW';
    const _probeWidth = (family, weight, style, size) => {
      if (!_probeHost) return 0;
      const s = document.createElement('span');
      s.textContent = FONT_PROBE;
      s.style.fontFamily = family;
      s.style.fontWeight = String(weight || '400');
      s.style.fontStyle = style || 'normal';
      s.style.fontSize = size || '16px';
      s.style.letterSpacing = 'normal';
      s.style.whiteSpace = 'nowrap';
      _probeHost.appendChild(s);
      const w = +s.getBoundingClientRect().width.toFixed(2);
      _probeHost.removeChild(s);
      return w;
    };
    const _fontCache = new Map();
    // Per distinct (firstFamily, weight, style, fontSize) combo, decide whether the named family ACTUALLY
    // renders (applies:true) or the browser falls back to the generic (applies:false), via the DOM-span
    // double-fallback probe described above. Cached per combo.
    const fontRender = (cs) => {
      const fam = cs.fontFamily, w = cs.fontWeight || '400', st = cs.fontStyle || 'normal', sz = cs.fontSize || '16px';
      const first = firstFamily(fam);
      if (!first || GENERIC.test(first)) return null;
      const key = first + '|' + w + '|' + st + '|' + sz;
      if (_fontCache.has(key)) return _fontCache.get(key);
      const FB_TOL = 0.5; // px — widths within this of the fallback baseline count as "collapsed to fallback"
      // probe against TWO distinct generic fallbacks so a coincidental metric match can't fool us.
      const probeFallback = (generic) => {
        const wNamed = _probeWidth(`'${first}', ${generic}`, w, st, sz);
        const wFb = _probeWidth(generic, w, st, sz);
        return { wNamed, wFb, distinct: Math.abs(wNamed - wFb) > FB_TOL };
      };
      const mono = probeFallback('monospace');
      const serif = probeFallback('serif');
      // applies = the named face is distinct from AT LEAST ONE fallback (its real metrics show through).
      // NOT applying (DOM fallback) = it collapsed to BOTH the monospace AND the serif baseline.
      const applies = mono.distinct || serif.distinct;
      // document.fonts.check is recorded only as a positive corroborator (never a suppressor) — it is
      // unreliable both ways (true while faux-rendering, etc.); the DOM-span metric is the authority.
      let available = false;
      try { available = document.fonts.check(`${st} ${w} ${sz} "${first}"`); } catch (e) {}
      // `rendering` retained for backward-compat with any downstream reader, but is now the DOM truth.
      const v = {
        family: first, applies, available, rendering: applies,
        wNamedMono: mono.wNamed, wFbMono: mono.wFb,
        wNamedSerif: serif.wNamed, wFbSerif: serif.wFb,
      };
      _fontCache.set(key, v);
      return v;
    };

    // EXACT-TEXT WIDTH (v2.2.0 — the FONT-METRIC / VERSION probe). Render the node's OWN text (the same
    // representative string on both sides, capped to ~80 chars) in an offscreen nowrap span using the
    // element's EXACT computed font — family, weight, style, size, letter-spacing, word-spacing AND
    // font-feature-settings — and return the rendered width. Two builds of the SAME family at the SAME
    // declared size (e.g. rsms Inter v4 vs Google Inter v20) have DIFFERENT per-glyph advance widths, so
    // the SAME string renders to a CONSISTENTLY different width — a uniform ~1-2% ratio across every node
    // in that family. That ratio is the only directly-measurable signal of a font-VERSION mismatch: the
    // declared props are identical and the family applies on both sides, yet the rendered text is wider/
    // narrower (which is what makes a block wrap to a different line count). Unlike the cv11 case (#31,
    // same-width letterform), a font-version drift IS a width difference, so we measure it here in-page.
    // Reuses the same offscreen `_probeHost`. Returns { w, fam, sample } or null for non-text/generic.
    const EXACT_CAP = 80; // chars — long enough for a stable per-family ratio, short enough to keep the dump small
    const exactTextWidth = (cs, rawText) => {
      if (!_probeHost) return null;
      const fam = cs.fontFamily;
      const first = firstFamily(fam);
      if (!first || GENERIC.test(first)) return null; // only a NAMED family can have a version mismatch
      const t = String(rawText || '').replace(/\s+/g, ' ').trim().slice(0, EXACT_CAP);
      if (t.length < 4) return null; // too short to give a stable, low-noise width
      const s = document.createElement('span');
      s.textContent = t;
      // copy the EXACT rendering inputs so the measured width matches the in-flow render of this combo.
      s.style.fontFamily = fam;
      s.style.fontWeight = String(cs.fontWeight || '400');
      s.style.fontStyle = cs.fontStyle || 'normal';
      s.style.fontSize = cs.fontSize || '16px';
      s.style.letterSpacing = cs.letterSpacing && cs.letterSpacing !== 'normal' ? cs.letterSpacing : 'normal';
      s.style.wordSpacing = cs.wordSpacing && cs.wordSpacing !== 'normal' ? cs.wordSpacing : 'normal';
      try { s.style.fontFeatureSettings = cs.fontFeatureSettings && cs.fontFeatureSettings !== 'normal' ? cs.fontFeatureSettings : 'normal'; } catch (e) {}
      s.style.whiteSpace = 'nowrap';
      _probeHost.appendChild(s);
      const w = +s.getBoundingClientRect().width.toFixed(2);
      _probeHost.removeChild(s);
      if (!(w > 0)) return null;
      return { w, fam: first, sample: t };
    };

    // INTERACTION-STATE RULE INDEX — getComputedStyle resolves only the CURRENT (resting) state;
    // a :hover/:focus/:focus-visible/:active override lives in a stylesheet rule that never applies
    // unless the element is actually in that state (which we cannot force during a static dump). So
    // we read document.styleSheets directly: for each interaction pseudo we collect the rule whose
    // selectorText carries it, STRIP the pseudo, and remember the rule's base selector + the visual
    // declarations it sets. Per state per element we then test element.matches(baseSelector) and fold
    // the matching rules' declarations into an override-set. Cross-origin sheets (Framer's CDN <link>)
    // throw on .cssRules access — we try/catch each sheet; if EVERY sheet is unreadable we record
    // states:'unreadable' on the node so the differ can honestly report "cross-origin unreadable"
    // rather than a false "matches".
    const ISTATE_PSEUDOS = [':hover', ':focus-visible', ':focus', ':active'];
    const ISTATE_VISUAL = [
      'background-color', 'color', 'border-top-width', 'border-top-color',
      'border-bottom-width', 'border-bottom-color', 'box-shadow', 'outline-width',
      'outline-color', 'outline-style', 'opacity', 'transform', 'text-decoration-line',
      'text-decoration', 'filter',
    ];
    // Build: rulesByPseudo[pseudo] = [{ base, decls:{prop:value} }, …]; track readability.
    const rulesByPseudo = Object.create(null);
    for (const p of ISTATE_PSEUDOS) rulesByPseudo[p] = [];
    let sheetsTotal = 0, sheetsReadable = 0;
    const stripPseudoFor = (selText, pseudo) => {
      // Only handle selectors that actually contain THIS pseudo; split a comma-list and keep the
      // sub-selectors that end in (or contain) the pseudo, then strip it to get the base.
      const subs = selText.split(',');
      const bases = [];
      for (let s of subs) {
        s = s.trim();
        if (!s.toLowerCase().includes(pseudo)) continue;
        // strip every occurrence of the pseudo (and a trailing :hover etc.) from this sub-selector
        const base = s.replace(new RegExp(pseudo.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi'), '').trim();
        if (base) bases.push(base);
      }
      return bases;
    };
    const collectRules = (rules) => {
      for (const rule of rules) {
        try {
          if (rule.type === 4 /* @media */ || rule.type === 12 /* @layer */ || rule.cssRules) {
            if (rule.cssRules && rule.type !== 1) { collectRules(rule.cssRules); continue; }
          }
        } catch (e) {}
        const sel = rule.selectorText;
        if (!sel) continue;
        const low = sel.toLowerCase();
        for (const pseudo of ISTATE_PSEUDOS) {
          if (!low.includes(pseudo)) continue;
          const bases = stripPseudoFor(sel, pseudo);
          if (!bases.length) continue;
          const decls = {};
          let any = false;
          for (const prop of ISTATE_VISUAL) {
            const v = rule.style.getPropertyValue(prop);
            if (v) { decls[prop] = v.trim(); any = true; }
          }
          // a state with NO visual declaration is not interesting (e.g. :focus { outline:none } IS,
          // but :hover { cursor:pointer } is not) — only keep states that touch a visual property.
          if (any) for (const base of bases) rulesByPseudo[pseudo].push({ base, decls });
        }
      }
    };
    try {
      for (const sheet of document.styleSheets) {
        sheetsTotal++;
        let rules = null;
        try { rules = sheet.cssRules; } catch (e) { rules = null; } // cross-origin → SecurityError
        if (!rules) continue;
        sheetsReadable++;
        try { collectRules(rules); } catch (e) {}
      }
    } catch (e) {}
    // A page with NO same-origin readable sheets at all → interaction states are globally unreadable.
    const ISTATES_UNREADABLE = sheetsTotal > 0 && sheetsReadable === 0;
    const INTERACTIVE_SEL = 'a, button, input, select, textarea, summary, [role="button"], [role="link"], [role="tab"], [role="menuitem"], [tabindex], [onclick]';
    const isInteractive = (el) => {
      try {
        if (el.matches && el.matches(INTERACTIVE_SEL)) return true;
        const cs2 = getComputedStyle(el);
        return cs2.cursor === 'pointer';
      } catch (e) { return false; }
    };
    // For one element, resolve each pseudo's override-set: union of matching rules' declarations
    // (later rules win, mirroring cascade order within our collected list).
    const interactionStatesFor = (el) => {
      if (ISTATES_UNREADABLE) return { states: 'unreadable' };
      const result = { states: {} };
      let foundAny = false;
      for (const pseudo of ISTATE_PSEUDOS) {
        const set = {};
        let hit = false;
        for (const { base, decls } of rulesByPseudo[pseudo]) {
          let m = false;
          try { m = el.matches(base); } catch (e) { m = false; }
          if (!m) continue;
          hit = true;
          for (const k in decls) set[k] = decls[k];
        }
        if (hit && Object.keys(set).length) {
          // normalise the pseudo key (drop the colon)
          result.states[pseudo.replace(/^:/, '')] = set;
          foundAny = true;
        }
      }
      if (!foundAny) result.states = {}; // readable, but this element has no interaction override
      return result;
    };

    // SVG GLYPH EXTENT — the union path bbox of an <svg>'s drawn shapes, in RENDERED px (scaled from the
    // viewBox to the element's box). A bbox with w>0 AND h>0 means a VISIBLE glyph is actually drawn — the
    // ground truth for "is there a real arrow here?", which `<svg>`-presence alone cannot tell (a hidden /
    // empty / display:none svg has presence but no drawn glyph). Reused by the icon-glyph capture and by the
    // button trailing-arrow capture (FIX 2).
    const svgGlyphExtent = (svgEl) => {
      try {
        const sr = svgEl.getBoundingClientRect();
        if (sr.width <= 0 || sr.height <= 0) return null; // not laid out / hidden → no visible glyph
        const vb = svgEl.viewBox && svgEl.viewBox.baseVal;
        const sx = vb && vb.width ? sr.width / vb.width : 1;
        const sy = vb && vb.height ? sr.height / vb.height : 1;
        let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
        for (const g of svgEl.querySelectorAll('path, line, polyline, polygon, rect, circle, ellipse')) {
          const b = g.getBBox && g.getBBox();
          if (!b || (b.width === 0 && b.height === 0)) continue;
          minX = Math.min(minX, b.x); minY = Math.min(minY, b.y);
          maxX = Math.max(maxX, b.x + b.width); maxY = Math.max(maxY, b.y + b.height);
        }
        if (!isFinite(minX)) return null;
        const w = +((maxX - minX) * sx).toFixed(1), h = +((maxY - minY) * sy).toFixed(1);
        if (w <= 0 || h <= 0) return null;
        return { w, h };
      } catch (e) { return null; }
    };

    const out = [];
    const walk = (el, depth, parent) => {
      if (!CHROME_NONE && CHROME && el.matches && el.matches(CHROME)) return;
      const cs = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      let directText = '';
      for (const n of el.childNodes) if (n.nodeType === 3) directText += n.textContent;
      directText = directText.replace(/\s+/g, ' ').trim();
      const comp = {};
      for (const p of PROPS) comp[p] = cs[p];

      // PSEUDO-ELEMENT BORDER/SHADOW fold — a card's border/elevation drawn on a ::after/::before
      // overlay is invisible to getComputedStyle(element); fold a rendering pseudo's border/shadow
      // into the element's effective values when the element itself has none.
      // GATED on the preflight. Where the engine ignores the pseudo argument and hands back the
      // element's own style, folding would copy the element's border onto itself — inventing a value
      // and double-reporting one defect. Refused, with the reason recorded in `capabilities`.
      if (CAN('pseudoElements')) for (const ps of ['::after', '::before']) {
        const pc = getComputedStyle(el, ps);
        if (!pc || pc.content === 'none' || pc.content === 'normal') continue;
        if ((parseFloat(comp.borderTopWidth) || 0) === 0 && (parseFloat(pc.borderTopWidth) || 0) > 0) {
          comp.borderTopWidth = pc.borderTopWidth; comp.borderTopColor = pc.borderTopColor;
          comp.borderBottomWidth = comp.borderBottomWidth && parseFloat(comp.borderBottomWidth) ? comp.borderBottomWidth : pc.borderBottomWidth;
          comp._borderFromPseudo = ps;
        }
        if ((!comp.boxShadow || comp.boxShadow === 'none') && pc.boxShadow && pc.boxShadow !== 'none') {
          comp.boxShadow = pc.boxShadow; comp._shadowFromPseudo = ps;
        }
      }

      // PSEUDO-ELEMENT CONTENT — a custom bullet/quote/arrow/counter/url() icon drawn via
      // ::before/::after content, invisible to getComputedStyle(element) and the text-probe loop.
      let pseudoContent = null;
      if (CAN('pseudoElements')) for (const ps of ['::before', '::after']) {
        const pc = getComputedStyle(el, ps);
        if (!pc) continue;
        const raw = pc.content;
        if (!raw || raw === 'none' || raw === 'normal') continue;
        if (raw === '""' || raw === "''") continue;
        const val = raw.replace(/^["']|["']$/g, '');
        if (!val) continue;
        (pseudoContent ||= {})[ps] = { content: val.slice(0, 40), fontSize: pc.fontSize, color: pc.color };
      }

      // SYSTEMATIC PSEUDO-ELEMENT STYLE (v2.5.0) — extract getComputedStyle(el,'::before') and
      // (el,'::after') for EVERY element (not just illustrations / not just the border-fold), so a
      // pseudo-DRAWN border, overlay, or decorative shape is checked UNIVERSALLY in MODE B — independent of
      // whether the element itself has a border. The fold above only copies a pseudo border/shadow into the
      // element's effective `comp` WHEN the element itself has none; it cannot catch a side that draws a
      // DIFFERENT pseudo border/overlay than the other, or a pseudo overlay present on one side only. This
      // records the rendering pseudo's own box properties for a direct cross-side comparison. Recorded only
      // for a pseudo that actually RENDERS (content set / non-none) to keep the dump small.
      let pseudoStyle = null;
      if (CAN('pseudoElements')) for (const ps of ['::before', '::after']) {
        const pc = getComputedStyle(el, ps);
        if (!pc) continue;
        const content = pc.content;
        if (!content || content === 'none' || content === 'normal') continue; // a non-rendering pseudo
        const bw = parseFloat(pc.borderTopWidth) || 0;
        const bg = pc.backgroundColor;
        const bgImg = pc.backgroundImage;
        const radius = parseFloat(pc.borderTopLeftRadius) || 0;
        const hasBg = (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') || (bgImg && bgImg !== 'none');
        // only keep a pseudo that draws SOMETHING visual (a border, a fill, a radius'd shape) — a bare
        // content:'' with no paint is noise.
        if (bw <= 0 && !hasBg && radius <= 0 && (content === '""' || content === "''")) continue;
        (pseudoStyle ||= {})[ps] = {
          content: content.replace(/^["']|["']$/g, '').slice(0, 40),
          borderTopWidth: pc.borderTopWidth, borderTopColor: pc.borderTopColor,
          borderBottomWidth: pc.borderBottomWidth, borderBottomColor: pc.borderBottomColor,
          background: bg, backgroundImage: (bgImg && bgImg !== 'none') ? String(bgImg).slice(0, 100) : 'none',
          position: pc.position, borderTopLeftRadius: pc.borderTopLeftRadius,
          boxShadow: (pc.boxShadow && pc.boxShadow !== 'none') ? String(pc.boxShadow).slice(0, 120) : 'none',
        };
      }

      // ANIMATION / TRANSITION presence — count of running animations.
      let anims = 0;
      try { anims = (el.getAnimations ? el.getAnimations() : []).filter(a => a.playState === 'running' || a.playState === 'paused').length; } catch (e) {}

      // ICON GLYPH extent — for an <svg>, the union path bbox in rendered px (the visible glyph).
      let glyph = null;
      if (el.tagName.toLowerCase() === 'svg') {
        glyph = svgGlyphExtent(el);
        // Presence-only fallback, same reasoning as the trailing-arrow one below: with getBBox
        // unavailable the glyph is null on BOTH sides, so `icon-glyph-w/h` compares two empty sets and
        // reports agreement. The laid-out svg BOX is a real measurement — it catches a resized or
        // missing icon — and it is labelled so no claim is made about the drawn path.
        if (!glyph && !CAN('svgGlyphExtent') && r.width > 0 && r.height > 0) {
          glyph = { w: +r.width.toFixed(1), h: +r.height.toFixed(1), presenceOnly: true };
        }
      }

      // HARD LINE BREAK + LINE COUNT — an explicit <br> reads as identical text but breaks differently.
      let hardBreak = false;
      for (const c of el.children) if (c.tagName === 'BR') { hardBreak = true; break; }
      let lines = null;
      if (directText) { try { const rng = document.createRange(); rng.selectNodeContents(el); lines = rng.getClientRects().length; } catch (e) {} }

      // WRAP-POINT — line count can match while the break POSITION differs. Reconstruct line boxes.
      let wrap = null;
      if (directText && lines && lines > 1 && /\s/.test(directText)) {
        try {
          const tn = [...el.childNodes].find(n => n.nodeType === 3 && n.textContent.replace(/\s+/g, ' ').trim());
          if (tn) {
            const s = tn.textContent; const rng2 = document.createRange();
            let curTop = null, cur = '', lineArr = [], firstEndX = null;
            for (let i = 0; i < s.length; i++) {
              rng2.setStart(tn, i); rng2.setEnd(tn, i + 1);
              const rects = rng2.getClientRects(); if (!rects.length) { cur += s[i]; continue; }
              const top = Math.round(rects[0].top);
              if (curTop === null) curTop = top;
              if (Math.abs(top - curTop) > 3) {
                if (lineArr.length === 0) firstEndX = +(rects[0].left - f.left).toFixed(1);
                lineArr.push(cur.replace(/\s+/g, ' ').trim()); cur = ''; curTop = top;
              }
              cur += s[i];
            }
            if (cur.trim()) lineArr.push(cur.replace(/\s+/g, ' ').trim());
            if (lineArr.length > 1) wrap = { first: lineArr[0], n: lineArr.length, endX: firstEndX };
          }
        } catch (e) {}
      }

      const fontRn = directText ? fontRender(cs) : null;
      // EXACT-TEXT WIDTH (v2.2.0) — this node's own text rendered nowrap in its exact computed font, so
      // MODE B can ratio target/reference per matched element and detect a font-VERSION (metric) mismatch.
      const exactW = directText ? exactTextWidth(cs, directText) : null;

      // FONT-FEATURE REQUEST (v2.1.0) — the computed `font-feature-settings` this text node REQUESTS
      // (cvXX / ssXX / onum / lnum / tnum / pnum / zero / case / …). Recorded only for text nodes that
      // actually request a non-default feature, so the post-walk RENDERED-GLYPH-SHAPE self-check can test
      // whether each requested feature has any EFFECT (a subset webfont that stripped the cvXX glyph
      // renders the default letterform despite the request — same WIDTH, so width/DOM-span checks are
      // blind; only the rasterised glyph SHAPE reveals it). `firstFamily`/`weight`/`style`/`size` give the
      // exact rendering inputs the self-check re-creates.
      let featReq = null;
      if (directText) {
        const ffs = String(cs.fontFeatureSettings || 'normal');
        const fff = firstFamily(cs.fontFamily);
        if (ffs && ffs !== 'normal' && fff && !GENERIC.test(fff)) {
          featReq = {
            ffs,
            family: cs.fontFamily,
            first: fff,
            weight: cs.fontWeight || '400',
            style: cs.fontStyle || 'normal',
            size: cs.fontSize || '16px',
            features: (ffs.match(/["']([a-z]{2}\d{2}|[a-z]{3,4})["']|\b(onum|lnum|tnum|pnum|zero|case|smcp|c2sc|liga|dlig|salt|swsh|hist|frac|ordn|sups|subs)\b/gi) || []).slice(0, 12),
          };
        }
      }

      // INTERACTION STATES — only resolve overrides for interactive elements (keeps the dump small).
      let istates = null;
      if (isInteractive(el)) istates = interactionStatesFor(el);

      // FULL-BLEED BACKGROUND LAYER (direct child) — a "background" that is an <img>/canvas/svg child.
      let bgLayer = null;
      if (r.width > 200) for (const c of el.children) {
        const t = c.tagName.toLowerCase();
        if (t === 'img' || t === 'canvas' || t === 'svg' || t === 'video') {
          const cr = c.getBoundingClientRect();
          if (cr.width >= 0.9 * r.width && cr.height >= 0.7 * r.height) {
            bgLayer = { tag: t, src: (c.getAttribute('src') || c.getAttribute('href') || c.currentSrc || '').slice(0, 100) };
            break;
          }
        }
      }

      // CONTAINER FULL-BLEED MEDIA (any descendant) — a section's gradient/texture is frequently an
      // absolutely-positioned descendant sized to cover the section (a sibling of the content column).
      let fullBleedMedia = null;
      if (r.width >= 400 && r.height >= 120) {
        for (const d of el.querySelectorAll('img, canvas, svg, video')) {
          const dr = d.getBoundingClientRect();
          if (dr.width >= 0.9 * r.width && dr.height >= 0.6 * r.height) {
            fullBleedMedia = { tag: d.tagName.toLowerCase(), src: (d.getAttribute('src') || d.getAttribute('href') || d.currentSrc || '').slice(0, 100) };
            break;
          }
        }
        if (!fullBleedMedia) {
          for (const d of el.querySelectorAll('div, span')) {
            const dcs = getComputedStyle(d);
            if (!dcs.backgroundImage || dcs.backgroundImage === 'none') continue;
            if (!/absolute|fixed/.test(dcs.position)) continue;
            const dr = d.getBoundingClientRect();
            if (dr.width >= 0.9 * r.width && dr.height >= 0.6 * r.height) {
              fullBleedMedia = { tag: 'css-bg', src: dcs.backgroundImage.slice(0, 100) };
              break;
            }
          }
        }
      }

      // THIN-LINE DIVIDER — a ≥page-wide 1–2px hairline (hr / thin bg box / wide border-top/bottom).
      // Read from the FOLDED comp so an ::after rule counts as a real divider.
      let divider = null;
      {
        const bt = parseFloat(comp.borderTopWidth) || 0, bb = parseFloat(comp.borderBottomWidth) || 0;
        const wide = r.width >= 0.4 * f.width;
        const bgSolid = cs.backgroundColor && cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== 'transparent';
        if (wide && !directText && r.height > 0 && r.height <= 3 && (bgSolid || el.tagName === 'HR')) {
          divider = { kind: 'line', thickness: +r.height.toFixed(1), color: cs.backgroundColor };
        } else if (wide && (bt >= 1 || bb >= 1)) {
          const side = bt >= 1 ? 'top' : 'bottom';
          divider = { kind: 'border-' + side, thickness: side === 'top' ? bt : bb, color: side === 'top' ? comp.borderTopColor : comp.borderBottomColor };
        }
      }

      // SVG CHILD presence — a button/link with a trailing arrow carries an <svg> child.
      let hasSvgChild = false;
      for (const c of el.children) { const t = c.tagName.toLowerCase(); if (t === 'svg' || (t === 'img' && (c.getAttribute('src') || '').includes('.svg'))) { hasSvgChild = true; break; } }

      // TRAILING ARROW GLYPH (FIX 2 — glyph-based, not svg-presence). For a button/link, measure the
      // RENDERED glyph bbox of its TRAILING svg (the rightmost svg within the element's own box). A glyph
      // with w>0 AND h>0 = a VISIBLE arrow is actually drawn; a hidden / empty / display:none decorative
      // svg yields null here even though `hasSvgChild` is true — that is exactly the case svg-presence
      // got wrong. We scan svgs inside the element (not crossing into a nested button/link), take the one
      // whose horizontal centre is furthest right (the trailing position), and record its visible extent.
      let arrowGlyph = null;
      {
        const tag = el.tagName.toLowerCase();
        const linkish = tag === 'a' || tag === 'button' || (el.matches && el.matches('[role="button"], [role="link"]'));
        if (linkish && r.width > 0) {
          let best = null, bestCx = -Infinity;
          for (const sv of el.querySelectorAll('svg')) {
            // skip svgs that belong to a NESTED interactive element (their own button/link owns them)
            const owner = sv.closest('a, button, [role="button"], [role="link"]');
            if (owner && owner !== el) continue;
            const svr = sv.getBoundingClientRect();
            if (svr.width <= 0 || svr.height <= 0) continue;
            const cx = svr.left + svr.width / 2;
            // trailing = rightmost svg whose centre is past the element's horizontal midpoint
            if (cx >= r.left + r.width * 0.5 && cx > bestCx) { bestCx = cx; best = sv; }
          }
          // if no svg is in the trailing half, fall back to the rightmost svg overall (still the "trailing" one)
          if (!best) {
            for (const sv of el.querySelectorAll('svg')) {
              const owner = sv.closest('a, button, [role="button"], [role="link"]');
              if (owner && owner !== el) continue;
              const svr = sv.getBoundingClientRect();
              if (svr.width <= 0 || svr.height <= 0) continue;
              const cx = svr.left + svr.width / 2;
              if (cx > bestCx) { bestCx = cx; best = sv; }
            }
          }
          if (best) arrowGlyph = svgGlyphExtent(best);
          // PRESENCE-ONLY FALLBACK — repairs a regression a fix introduced. v2.0.2 replaced a
          // `hasSvgChild` presence check with this glyph measurement because a decorative or hidden svg
          // read as a match. Where getBBox is unavailable the glyph is null for EVERY button on BOTH
          // sides, so the replacement is strictly worse than what it replaced: a missing trailing arrow
          // now passes where presence would have caught it. Fall back to the laid-out box of the
          // trailing svg and LABEL the finding presence-only, so a missing arrow is still caught while
          // no claim is made about the glyph's size or shape.
          if (!arrowGlyph && best && !CAN('svgGlyphExtent')) {
            const br = best.getBoundingClientRect();
            if (br.width > 0 && br.height > 0) {
              arrowGlyph = { w: +br.width.toFixed(1), h: +br.height.toFixed(1), presenceOnly: true };
            }
          }
        }
      }

      const myIndex = out.length;
      const fid =
        el.getAttribute('data-fid') ||
        el.getAttribute('data-fidelity-id') ||
        el.getAttribute('data-testid') ||
        null;
      out.push({
        i: myIndex, parent, depth,
        tag: el.tagName.toLowerCase(),
        cls: el.getAttribute('class') || '',
        fid,
        text: directText,
        isPh: el.classList.contains('ph') || el.classList.contains('placeholder'),
        rect: {
          x: +(r.left - f.left).toFixed(1),
          y: +(r.top - f.top).toFixed(1),
          w: +r.width.toFixed(1),
          h: +r.height.toFixed(1),
        },
        glyph, hardBreak, lines, wrap, bgLayer, fullBleedMedia, divider, hasSvgChild, arrowGlyph,
        fontRn, exactW, featReq, pseudoContent, pseudoStyle, anims, istates, comp,
      });
      for (const c of el.children) walk(c, depth + 1, myIndex);
    };
    walk(root, 0, -1);
    // tear down the offscreen font-probe host now that every combo has been measured + cached.
    try { if (_probeHost && _probeHost.parentNode) _probeHost.parentNode.removeChild(_probeHost); } catch (e) {}

    // LOADED FONT FACES — a range-weight face from a single file faux-weight-synthesizes other weights.
    const fonts = (() => {
      try {
        const seen = new Set(), out2 = [];
        for (const ff of document.fonts) {
          if (ff.status !== 'loaded') continue;
          const k = ff.family + '|' + ff.weight + '|' + ff.style;
          if (seen.has(k)) continue; seen.add(k);
          out2.push({ family: ff.family.replace(/["']/g, ''), weight: ff.weight, style: ff.style });
        }
        return out2;
      } catch (e) { return []; }
    })();

    // ======================================================================
    // RENDERED-GLYPH-SHAPE / FEATURE-EFFECTIVENESS SELF-CHECK (v2.1.0)
    // ======================================================================
    // The differ compares DECLARED font props (family/weight/size/letter-spacing/font-feature-settings)
    // and whether the font APPLIES (DOM-span, not fallback) — but a requested OpenType feature
    // (cv11 single-story 'a', ss01, onum old-style figures, …) can be DECLARED + the family can APPLY,
    // yet have NO EFFECT because the self-hosted woff2 is a SUBSET that STRIPPED that feature's glyph.
    // cv11 single-vs-double-story 'a' are the SAME WIDTH, so width / DOM-span / glyph-extent checks are
    // structurally blind. The only signal is the rasterised glyph SHAPE.
    //
    // SELF-CHECK: for each distinct (family, weight, style, size, font-feature-settings) combo used by a
    // text node that REQUESTS a feature, render a feature-sensitive probe ('a g l 0 1 …') TWICE in the
    // element's exact computed font — once WITH the requested font-feature-settings and once with
    // `normal` — and test whether they render DIFFERENTLY. WITH==WITHOUT (no pixel difference) ⇒ the
    // requested feature is INEFFECTIVE (the font lacks the glyph) ⇒ a `font/feature-ineffective` finding.
    //
    // RASTERISATION MECHANISM — chosen by capability TEST, not assumption:
    //  · canvas `ctx.fontFeatureSettings` (CanvasRenderingContext2D): if THIS engine supports it we draw
    //    both variants to a canvas with the loaded document font and compare `getImageData` pixel hashes —
    //    fully IN-PAGE, no runner round-trip. (No engine in use implements it today — we test
    //    `'fontFeatureSettings' in ctx` at runtime and only take this path when true.)
    //  · RUNNER-ASSISTED fallback (when canvas lacks the property): an SVG-`<img>` rasteriser cannot see
    //    the page's loaded @font-face faces, so we instead render persistent on-screen probe-PAIR nodes
    //    (`data-mf-fprobe`, the requested-ffs row directly above the normal row, same family/size/weight)
    //    and record each pair's on/off RECTS + metadata in `featureCheck.probes`. The run.md flow then
    //    screenshots the page and `feature-check.mjs` pixel-diffs each pair: identical pair ⇒ ineffective.
    //    MODE B also consumes runner-injected results via `globalThis.__MF_FEATURE_DIFFS__` to emit the
    //    finding inline. Probe nodes are parked off the visible frame (top-left of the viewport, high z)
    //    so they don't disturb the measured layout (capture already finished the walk before they mount).
    const featureCheck = (() => {
      try {
        // distinct combos that request a feature
        const combos = new Map();
        for (const n of out) {
          if (!n.featReq) continue;
          const fr = n.featReq;
          const key = fr.first + '|' + fr.weight + '|' + fr.style + '|' + fr.size + '|' + fr.ffs;
          if (!combos.has(key)) combos.set(key, { key, ...fr, sampleText: norm(n.text).slice(0, 8) || 'a', nodeIdxs: [] });
          combos.get(key).nodeIdxs.push(n.i);
        }
        if (!combos.size) return { ran: false, reason: 'no feature-requesting text', canvasSupported: null, probes: [], combos: [] };

        // capability TEST — does this engine's 2D context expose fontFeatureSettings?
        let canvasSupported = false;
        try {
          const tc = document.createElement('canvas').getContext('2d');
          canvasSupported = !!tc && ('fontFeatureSettings' in tc);
        } catch (e) { canvasSupported = false; }

        // a feature-sensitive probe string (covers cvXX 'a g l', figures, ligatures) — kept short.
        const PROBE = 'a g l 0 1 ffi';

        // ---- (A) IN-PAGE CANVAS path (preferred when supported) ----
        if (canvasSupported) {
          const W = 220, H = 64;
          const cv = document.createElement('canvas'); cv.width = W; cv.height = H;
          const ctx = cv.getContext('2d');
          const hashOf = (ffs, combo) => {
            ctx.clearRect(0, 0, W, H); ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, W, H);
            ctx.fillStyle = '#000';
            ctx.textBaseline = 'middle';
            ctx.font = `${combo.style} ${combo.weight} ${px(combo.size) || 16}px ${combo.family}`;
            try { ctx.fontFeatureSettings = ffs; } catch (e) {}
            ctx.fillText(PROBE, 2, H / 2);
            let dark = 0, sum = 0;
            try {
              const d = ctx.getImageData(0, 0, W, H).data;
              for (let i = 0; i < d.length; i += 4) { const lum = (d[i] + d[i + 1] + d[i + 2]) / 3; if (lum < 140) { dark++; sum = (sum * 131 + (i >> 2)) % 2147483647; } }
            } catch (e) { return null; }
            return dark + ':' + sum;
          };
          const combosOut = [];
          for (const c of combos.values()) {
            const hOn = hashOf(c.ffs, c), hOff = hashOf('normal', c);
            const effective = hOn != null && hOff != null ? hOn !== hOff : null;
            combosOut.push({ key: c.key, first: c.first, weight: c.weight, style: c.style, size: c.size, ffs: c.ffs, features: c.features, nodeIdxs: c.nodeIdxs, effective, mechanism: 'canvas-fontFeatureSettings', hOn, hOff });
          }
          return { ran: true, mechanism: 'canvas-fontFeatureSettings', canvasSupported: true, probes: [], combos: combosOut };
        }

        // ---- (B) RUNNER-ASSISTED path — render persistent probe PAIRS for screenshot+pixel-diff ----
        const host = document.createElement('div');
        host.id = 'mf-fprobe-host';
        host.setAttribute('aria-hidden', 'true');
        host.style.cssText = 'position:fixed;left:0;top:0;z-index:2147483647;background:#fff;margin:0;padding:0;pointer-events:none;';
        const PW = 240, PH = 30; // per probe-row
        let row = 0;
        const probes = [];
        const combosOut = [];
        for (const c of combos.values()) {
          const yOn = row * PH, yOff = (row + 1) * PH;
          const mk = (ffs, y, tag) => {
            const d = document.createElement('div');
            d.setAttribute('data-mf-fprobe', tag);
            d.textContent = PROBE;
            d.style.cssText = 'position:absolute;left:0;top:' + y + 'px;width:' + PW + 'px;height:' + PH + 'px;line-height:' + PH + 'px;'
              + 'background:#fff;color:#000;white-space:nowrap;overflow:hidden;letter-spacing:normal;'
              + 'font-family:' + c.family + ';font-weight:' + c.weight + ';font-style:' + c.style + ';font-size:' + c.size + ';'
              + 'font-feature-settings:' + ffs + ';';
            host.appendChild(d);
            return d;
          };
          const idx = combosOut.length;
          mk(c.ffs, yOn, 'on:' + idx);
          mk('normal', yOff, 'off:' + idx);
          // rects are relative to the viewport (position:fixed host at 0,0) → screenshot pixel coords (×DPR).
          probes.push({ idx, key: c.key, onRect: { x: 0, y: yOn, w: PW, h: PH }, offRect: { x: 0, y: yOff, w: PW, h: PH } });
          combosOut.push({ key: c.key, first: c.first, weight: c.weight, style: c.style, size: c.size, ffs: c.ffs, features: c.features, nodeIdxs: c.nodeIdxs, effective: null, mechanism: 'runner-screenshot' });
          row += 2;
        }
        (document.body || document.documentElement).appendChild(host);
        let dpr = 1; try { dpr = window.devicePixelRatio || 1; } catch (e) {}
        return { ran: true, mechanism: 'runner-screenshot', canvasSupported: false, dpr, hostId: 'mf-fprobe-host', probes, combos: combosOut };
      } catch (e) {
        return { ran: false, reason: 'error:' + (e && e.message), canvasSupported: null, probes: [], combos: [] };
      }
    })();

    // FRAME content height — drift-aware (true scroll/content extent under the root).
    let contentH = f.height;
    try {
      let maxB = 0; for (const n of out) maxB = Math.max(maxB, (n.rect.y || 0) + (n.rect.h || 0));
      const scrollH = root === document.body ? Math.max(document.documentElement.scrollHeight || 0, document.body.scrollHeight || 0) : 0;
      contentH = Math.max(f.height, maxB, scrollH);
    } catch (e) {}

    // VIEWPORT WIDTH — the runner injects analyze.js at multiple WIDTHS=[390,768,1280]; the
    // responsive detector keys reference/target analyses by this. Record the real window inner
    // width (the injection viewport), independent of the frame's own measured width.
    let viewportW = f.width;
    try { viewportW = window.innerWidth || document.documentElement.clientWidth || f.width; } catch (e) {}

    return { title: TITLE || SEL || 'body', viewportW, frame: { w: f.width, h: f.height, contentH }, capabilities: CAPS, fonts, featureCheck, nodes: out };
  }

  // ======================================================================
  // SHARED NORMALISERS (the old diff.mjs / structure-diff.mjs helpers)
  // ======================================================================
  const TOL_PX = 1.5;
  const NORMAL_LH = 1.2;
  const norm = s => String(s ?? '').replace(/\s+/g, ' ').trim();
  function toHex(c) {
    if (c == null) return null;
    let s = String(c).trim().toLowerCase();
    if (!s || s === 'transparent' || s === 'none') return 'transparent';
    if (s.startsWith('#')) return s.length === 4 ? '#' + [...s.slice(1)].map(x => x + x).join('') : s.slice(0, 7);
    const m = s.match(/rgba?\(([^)]+)\)/);
    if (m) {
      const p = m[1].split(',').map(x => parseFloat(x));
      if (p.length >= 4 && p[3] === 0) return 'transparent';
      return '#' + p.slice(0, 3).map(n => Math.round(n).toString(16).padStart(2, '0')).join('');
    }
    return s;
  }
  const px = v => { if (v == null) return null; if (typeof v === 'number') return v; const m = String(v).match(/-?[\d.]+/); return m ? parseFloat(m[0]) : null; };
  function weightFromFamily(fam) {
    if (!fam) return null;
    if (/SemiBold|_600|Semibold/.test(fam)) return 600;
    if (/Medium|_500/.test(fam)) return 500;
    if (/Bold|_700|800|900/.test(fam)) return 700;
    if (/Regular|_400|Normal/.test(fam)) return 400;
    return null;
  }
  const close = (a, b, t = TOL_PX) => a != null && b != null && Math.abs(a - b) <= t;
  function familyKind(fam) {
    if (!fam) return null;
    if (/Mono|JetBrains/i.test(fam)) return 'mono';
    if (/Newsreader|Georgia|GT Super|Times/i.test(fam)) return 'serif';
    if (/\bserif\b/i.test(fam) && !/sans-?serif/i.test(fam)) return 'serif';
    return 'sans';
  }
  const alignNorm = a => { const v = String(a ?? 'left'); return v === 'start' ? 'left' : v === 'end' ? 'right' : v; };
  const lsPx = v => { if (v == null) return null; if (/normal/i.test(String(v))) return 0; return px(v); };

  // ======================================================================
  // PART 2 — THE DIFF  (MODE B): everything diff.mjs + structure-diff.mjs did,
  // re-emitted as PRIORITISED, ACTIONABLE findings.
  // ======================================================================
  function diff(refDoc, appDoc) {
    if (refDoc.error) return { error: 'reference-extract-error', detail: refDoc };
    if (appDoc.error) return { error: 'target-extract-error', detail: appDoc };

    // Capability blocks, hoisted: several detector passes below must know whether a class is even
    // measurable before they emit, and a finding that misreports WHICH property is wrong is worse
    // than no finding. Declared here so no pass reaches them in their temporal dead zone.
    const capsOf = d => (d && d.capabilities) || {};
    const rCaps = capsOf(refDoc), tCaps = capsOf(appDoc);
    const mock = refDoc.nodes || [];
    const mockDoc = refDoc;
    const appAll = appDoc.nodes || [];
    const APP_IS_DOM = appAll.some(n => n && n.comp); // analyze.js always emits comp → true

    // findings sink (replaces diff.mjs rows + structure-diff fails)
    const findings = [];
    // noiseExcluded — confident-noise buckets kept OUT of `findings` / `totalFindings` / `score` so the
    // headline reflects only confident findings. Consumers can inspect each bucket separately.
    //   · repeatedTextMispairs   — co-text candidates not chosen by the nearest-Y disambiguator.
    //   · illustrationInternals  — unpaired media/illustration internals (never per-pixel diffed).
    //   · unpairedSameText (v2.0.1, FIX 3) — a text string present on BOTH sides that the
    //       fid→text→path matcher failed to pair AND the normalised-text/nearest-Y fallback also could
    //       not confidently pair (so reporting it as missing/extra would be a phantom). NOT a real absence.
    //   · crossDomStructure (v2.0.1, FIX 3) — residual structure/layout rows that cannot be reliably
    //       paired across the two DOMs (e.g. the Framer↔StyleX 'layout' class pairs 0 wide containers),
    //       so they are demoted out of the confident set rather than reported as defects.
    const noiseExcluded = { repeatedTextMispairs: [], illustrationInternals: [], unpairedSameText: [], crossDomStructure: [] };
    let _fid = 0;

    // SECTION resolver — nearest preceding section eyebrow/heading for a node's locator.
    const isSectionLead = t => {
      const tx = norm(t.text);
      if (!tx || (t.rect?.h || 0) <= 0 || (t.rect?.w || 0) < 60) return false;
      const sz = px(t.comp?.fontSize) || 0;
      const eyebrow = /^[A-Z0-9 ·&,'’\-]+$/.test(tx) && tx.length <= 40;
      return eyebrow || sz >= 18;
    };
    const appLeads = appAll.filter(isSectionLead).sort((a, b) => (a.rect?.y || 0) - (b.rect?.y || 0));
    const mockLeads = mock.filter(isSectionLead).sort((a, b) => (a.rect?.y || 0) - (b.rect?.y || 0));
    const sectionFor = (node, leads) => {
      if (!node || !node.rect) return null;
      const y = node.rect.y;
      let best = null;
      for (const l of leads) { if ((l.rect?.y || 0) <= y + 4) best = l; else break; }
      return best ? norm(best.text).slice(0, 40) : null;
    };

    // best-effort CSS/text locator for a TARGET node
    const locatorFor = (n) => {
      if (!n) return null;
      const parts = [];
      if (n.fid) parts.push(`[data-testid/fid="${n.fid}"]`);
      const t = norm(n.text);
      if (t) parts.push(`text "${t.slice(0, 40)}"`);
      const cls = (n.cls || '').split(/\s+/).filter(Boolean).slice(0, 2).join('.');
      const tagcls = n.tag + (cls ? '.' + cls : '');
      parts.push(tagcls);
      if (n.rect) parts.push(`@${Math.round(n.rect.x)},${Math.round(n.rect.y)} ${Math.round(n.rect.w)}×${Math.round(n.rect.h)}`);
      return parts.join('  ·  ');
    };

    // SEVERITY model: layout/structure/missing > value/geometry > cosmetic micro-deltas.
    const SEV = {
      // class -> default severity (overridable per-finding)
      layout: 'high', structure: 'high', container: 'high', gradient: 'high',
      'container-bg': 'high', border: 'high', shadow: 'med', rhythm: 'med',
      geometry: 'med', font: 'med', value: 'med', transform: 'med', pseudo: 'med',
      animation: 'low', wrap: 'med', icon: 'med', spacing: 'med', media: 'med',
      'screen-bg': 'high', fonts: 'high', text: 'med', extra: 'low',
      interaction: 'med', responsive: 'high', position: 'med',
    };

    const add = (o) => {
      const cls = o.class;
      const severity = o.severity || SEV[cls] || 'med';
      findings.push({
        id: 'mf' + (++_fid),
        locator: o.locator ?? null,
        section: o.section ?? null,
        class: cls,
        property: o.property,
        target: o.target,
        reference: o.reference,
        ...(o.deltaPx != null ? { deltaPx: o.deltaPx } : {}),
        severity,
        suggestedChange: o.suggestedChange,
      });
    };

    // ---------- target (app) accessors (DOM shape; analyze.js always produces comp) ----------
    const A = {
      text: n => norm(n.text),
      placeholder: n => norm(n.placeholder ?? (n.isPh ? n.text : '')),
      fontSize: n => n.effStyle?.fontSize ?? px(n.comp?.fontSize),
      weight: n => weightFromFamily(n.effStyle?.fontFamily) ?? (n.comp?.fontWeight ? parseInt(n.comp.fontWeight, 10) : null),
      family: n => familyKind(n.effStyle?.fontFamily ?? n.comp?.fontFamily),
      align: n => alignNorm(n.effStyle?.textAlign ?? n.comp?.textAlign),
      color: n => toHex(n.effStyle?.color ?? n.comp?.color),
      phColor: n => toHex(n.placeholderTextColor ?? n.comp?.color),
      lineHeight: n => n.effStyle?.lineHeight ?? px(n.comp?.lineHeight) ?? null,
      rect: n => n.rect,
      box: n => {
        const c = n.comp || {};
        return {
          bg: toHex(c.backgroundColor), radius: px(c.borderTopLeftRadius),
          padLeft: px(c.paddingLeft), padTop: px(c.paddingTop), padBottom: px(c.paddingBottom),
          shadow: !!c.boxShadow && c.boxShadow !== 'none',
        };
      },
      isBox: n => {
        const b = A.box(n);
        return (b.bg && b.bg !== 'transparent') || b.shadow || (n.comp && px(n.comp.borderTopWidth) > 0);
      },
    };

    const appById = new Map(appAll.map(n => [n.i, n]));
    const app = appAll; // DOM dump: already scoped to the frame root

    const appContentW = Math.max(...app.map(n => (A.rect(n)?.x || 0) + (A.rect(n)?.w || 0)), 0);
    const appFrameW = (appDoc.frame?.w) || appContentW || (mockDoc.frame?.w || 393);
    const mockFrameW = mockDoc.frame?.w || 393;

    const sameViewport = mockDoc.frame?.w && Math.abs(appFrameW - mockFrameW) < 0.05 * mockFrameW;
    const GEOM = OPTS.geom === false ? false : (OPTS.geom === true ? true : sameViewport);
    const GEOM_TOL_CENTER = px(OPTS.geomTolCenter) ?? 6;
    const GEOM_TOL_SIZE = px(OPTS.geomTolSize) ?? 10;
    const GEOM_TOL_HEIGHT = px(OPTS.geomTolHeight) ?? 2;

    function appStyledAncestor(node) {
      if (A.isBox(node)) return node;
      let cur = appById.get(node.parent); let hops = 0;
      while (cur && hops++ < 12) { if (A.isBox(cur)) return cur; cur = appById.get(cur.parent); }
      return null;
    }
    function mockOwnBox(node) {
      const c = node.comp || {};
      const box = (toHex(c.backgroundColor) !== 'transparent' && c.backgroundColor) || (c.boxShadow && c.boxShadow !== 'none') || px(c.borderTopWidth) > 0;
      return box && node.tag !== 'body' && !/\b(body|scr|frame|screen)\b/.test(node.cls);
    }
    function mockStyledAncestor(node) {
      if (mockOwnBox(node)) return node;
      let cur = node.parent >= 0 ? mock[node.parent] : null; let hops = 0;
      while (cur && hops++ < 12) { if (mockOwnBox(cur)) return cur; cur = cur.parent >= 0 ? mock[cur.parent] : null; }
      return null;
    }
    const mockHasShadow = c => !!c && !!c.boxShadow && c.boxShadow !== 'none';

    // ============= ILLUSTRATION-INTERNAL CLASSIFIER (v2.3.0) =============
    // A product ILLUSTRATION / mockup card (the ReadinessMockup "Morrow Vale Resources" card, a hero
    // product-shot, a readiness/preview panel) carries PLACEHOLDER content — fake tickers ("ASX:MVR"),
    // demo numbers, sample row labels — that LEGITIMATELY differs between the reference and the rebuild.
    // The old behaviour treated those nodes' TEXT as missing/extra/wrong-state findings → a flood, OR (the
    // miss this fix closes) dropped them ENTIRELY as noise, so their real, checkable STYLING (a card border,
    // a row label's letter-spacing, a corner radius) was NEVER compared and real defects went unchecked.
    //
    // The correct split: SUPPRESS the placeholder TEXT-content comparison for illustration internals (a
    // different demo number/ticker is not a finding), but STILL run the COMPUTED-STYLE / box / letter-spacing
    // / geometry comparison on them (their styling is real). To do that we (a) identify illustration ROOTS on
    // each side, (b) mark every descendant index as an illustration-internal, and (c) gate the text passes to
    // route an internal's text finding into `noiseExcluded.illustrationInternals` instead of `findings`,
    // while a dedicated style pass (below) pairs internals across sides BY POSITION/STRUCTURE (not text) and
    // emits border/radius/shadow/bg/colour/letter-spacing/font/padding/gap/geometry findings for them.
    //
    // An illustration ROOT = a sizeable, styled, TEXT-LESS-at-its-own-level card/panel that is NOT a page
    // section wrapper — same geometry heuristic the media-rel-y pass already uses for `isMockupCard`, plus a
    // class-name hint (mockup / illustration / readiness / product / preview / device / screenshot / demo /
    // ph / placeholder). It must be reasonably deep (not the body/screen/frame root) and NOT span the full
    // frame width (a full-bleed section is a real section, not an illustration).
    const ILLO_CLASS_HINT = /\b(mockup|mock-?up|illustration|illo|readiness|product-?(shot|card|preview|mock)|preview|device|screenshot|screen-?shot|demo|figure|hero-?(visual|art|image|graphic)|placeholder)\b/i;
    const isIlloRoot = (n, frameW) => {
      if (!n || !n.rect) return false;
      const r = n.rect;
      if (n.tag === 'body' || /\b(body|scr|frame|screen)\b/.test(n.cls || '')) return false;
      if ((r.w || 0) >= 0.92 * frameW) return false;            // full-bleed → a real section, not an illustration
      const classHint = ILLO_CLASS_HINT.test(n.cls || '');
      const c = n.comp || {};
      const styled = (toHex(c.backgroundColor) !== 'transparent' && c.backgroundColor) ||
                     (c.boxShadow && c.boxShadow !== 'none') ||
                     px(c.borderTopWidth) > 0 || px(c.borderTopLeftRadius) >= 8;
      const ownText = norm(n.text);                              // text on the ROOT level itself (rare for a card)
      // geometry-qualifying mockup card (matches the media-rel-y pass): wide + tall + styled + no own text
      const cardLike = (r.w || 0) >= 280 && (r.h || 0) >= 240 && styled && !ownText;
      // class-hinted illustration: a named mockup/illustration container of non-trivial size
      const namedIllo = classHint && (r.w || 0) >= 180 && (r.h || 0) >= 140;
      return cardLike || namedIllo;
    };
    // Build the descendant-index SET for a side: every node whose ancestor chain hits an illustration root.
    // We DON'T include the root itself in the suppression set (the root's OWN border/bg is a legitimate,
    // non-placeholder finding the normal container pass should still catch) — only its INTERNALS.
    const illoDescSet = (nodes, getParent, frameW) => {
      const roots = [];
      for (const n of nodes) if (isIlloRoot(n, frameW)) roots.push(n);
      const rootIdx = new Set(roots.map(n => n.i));
      const desc = new Set();          // indices that are INSIDE an illustration (excluding the root)
      const rootOf = new Map();        // internal index -> the illustration root it belongs to
      for (const n of nodes) {
        let cur = n, hops = 0, hitRoot = null;
        while (cur && hops++ < 60) {
          const p = getParent(cur);
          if (p == null) break;
          if (rootIdx.has(p.i)) { hitRoot = p; break; }
          // if an ANCESTOR is itself an internal we've already recorded, inherit its root (faster + robust)
          cur = p;
        }
        if (hitRoot) { desc.add(n.i); rootOf.set(n.i, hitRoot); }
      }
      return { roots, rootIdx, desc, rootOf };
    };
    const mockParentOf = n => (n && n.parent >= 0 ? mock[n.parent] : null);
    const appParentOf = n => (n && n.parent >= 0 ? appById.get(n.parent) : null);
    const mockIllo = illoDescSet(mock, mockParentOf, mockFrameW);
    const appIllo = illoDescSet(appAll, appParentOf, appFrameW);
    // is THIS node an illustration-internal (placeholder content lives here) on its side?
    const mockIsIlloInternal = n => n && mockIllo.desc.has(n.i);
    const appIsIlloInternal = n => n && appIllo.desc.has(n.i);

    // EFFECTIVE BACKDROP (v2.0.1, FIX 2) — a section's full-bleed gradient/media may be expressed two ways:
    //   (a) a full-bleed <img>/canvas/svg/video child OR positioned css-bg descendant (captured as
    //       `node.fullBleedMedia`), OR
    //   (b) a CSS `background-image` (a linear/radial/conic-gradient OR a url(...)) ON THE ELEMENT ITSELF.
    // The old container pass only looked at (a), so a target that paints its hero gradient via
    // `background-image:url(hero-gradient.svg)` on the <section> (no child img) was reported
    // `bg-media-layer absent` while the reference used a full-bleed <img> — a false "FLAT/absent".
    // `effectiveBackdrop(node)` returns the backdrop on EITHER side as { kind, src } (or null), so the
    // comparison is "does this side have a backdrop at all?" rather than "does it have a child img?".
    const cssBgImage = c => {
      const bi = c && c.backgroundImage;
      if (!bi || bi === 'none') return null;
      if (/gradient/i.test(bi)) return { kind: 'css-gradient', src: bi.slice(0, 100) };
      if (/url\(/i.test(bi)) return { kind: 'css-image', src: bi.slice(0, 100) };
      return null;
    };
    const effectiveBackdrop = (node) => {
      if (!node) return null;
      if (node.fullBleedMedia) return { kind: node.fullBleedMedia.tag, src: node.fullBleedMedia.src };
      const own = cssBgImage(node.comp);
      if (own) return own;
      return null;
    };

    function isButtonish(n) {
      if (!n) return false;
      if (n.tag === 'a' || n.tag === 'button') return true;
      const c = n.comp || {}, r = n.rect || {};
      const hasBox = (toHex(c.backgroundColor) !== 'transparent' && c.backgroundColor) || (c.boxShadow && c.boxShadow !== 'none') || (px(c.borderTopWidth) > 0) || px(c.borderTopLeftRadius) >= 4;
      return !!hasBox && r.h > 0 && r.h <= 64 && px(c.paddingLeft) >= 8;
    }
    function buttonAncestor(node, byId) { let cur = node, hops = 0; while (cur && hops++ < 6) { if (isButtonish(cur)) return cur; cur = byId.get(cur.parent); } return null; }
    function mockButtonAncestor(node) { let cur = node, hops = 0; while (cur && hops++ < 6) { if (isButtonish(cur)) return cur; cur = cur.parent >= 0 ? mock[cur.parent] : null; } return null; }

    const CHROME_TXT = /^\d{1,2}:\d{2}$|signal_cellular|wifi|battery_full/;

    const childrenByParent = arr => { const m = new Map(); for (const n of arr) { if (!m.has(n.parent)) m.set(n.parent, []); m.get(n.parent).push(n); } for (const v of m.values()) v.sort((a, b) => (a.i ?? 0) - (b.i ?? 0)); return m; };
    const mockKids = childrenByParent(mock), appKids = childrenByParent(appAll);
    const nextSibGap = (node, kids) => { const sibs = kids.get(node.parent); if (!sibs) return null; const idx = sibs.indexOf(node); const nx = sibs[idx + 1]; if (!nx || !node.rect || !nx.rect || nx.rect.h <= 0 || node.rect.h <= 0) return null; return +(nx.rect.y - (node.rect.y + node.rect.h)).toFixed(1); };

    // ============= SCREEN BACKGROUND (top-level) =============
    {
      const mockBg = toHex(mock[0]?.comp?.backgroundColor);
      const deviceW = appDoc.frame?.w || appFrameW;
      const appRoot = app
        .filter(n => {
          const bg = n.comp && n.comp.backgroundColor;
          const r = n.rect || {};
          const isRoot = (r.x ?? 99) <= 2 && (r.w || 0) >= 0.9 * deviceW;
          return bg && toHex(bg) !== 'transparent' && isRoot;
        })
        .sort((a, b) => (a.depth ?? 99) - (b.depth ?? 99))[0];
      const appBg = appRoot ? toHex(appRoot.comp?.backgroundColor) : null;
      if (mockBg && mockBg !== 'transparent' && appBg !== mockBg) {
        add({
          locator: '[screen background] — shallowest full-width backgrounded container',
          section: null, class: 'screen-bg', property: 'background-color',
          target: appBg, reference: mockBg,
          suggestedChange: `set the page/root background-color to ${mockBg}`,
        });
      }
    }

    // ============= TEXT-PROBE PASS (per mock text/placeholder) =============
    const unmatched = [];
    const unpairedMock = [];   // mock text probes with no counterpart anywhere — surfaced, per THE LAW rule 2
    let pairedTextCount = 0;  // the denominator: a 0/N pairing collapse must not read as a clean page
    // FONT-METRIC / VERSION accumulator (v2.2.0). Per matched text element we render the SAME exact string
    // in each side's exact computed font (capture-side `exactW`) and store the per-family width RATIO
    // target/reference. A font-VERSION mismatch is UNIFORM — every node in that family shows ~the same
    // ratio — so after the pass we aggregate per family (median) and emit ONE finding per family when the
    // median deviates from 1.0 by more than a tolerance. Keyed by the lowercased first font-family name.
    const fontMetricRatios = new Map(); // famKey -> [{ ratio, loc, sect, refW, tgtW, sample }]

    // ============= TYPOGRAPHIC-DECLARATION accumulator (v2.5.1) =============
    // Three DECLARED typographic properties change what is RENDERED but NOT which font file loads, so they
    // slip every existing layer: the family-KIND check (#1170) only compares serif/sans/mono; the CDP
    // getPlatformFontsForNode probe (#37) reports the same font FILE because a cvXX/axis variant is a glyph
    // WITHIN the file; and the odiff raster runs antialiasing:true so a single-vs-double-story glyph edge
    // looks like font-smoothing noise and is suppressed. Class = "same font, different declared shaping".
    //   1. font-feature-settings — cvXX/ssXX/onum/tnum/… (the cv11 single-vs-double-story 'a' homepage bug)
    //   2. font-variation-settings — a wght/opsz/slnt axis applied on one side but not the other
    //   3. the FULL font-family DECLARATION — `'Inter', system-ui, …, sans-serif` vs `Inter, sans-serif`
    //      (same KIND, different declared cascade — caught alongside, NOT replacing, the kind check)
    // These props are almost always set SITE-WIDE, so a single divergence repeats on every element. We
    // ACCUMULATE here per (property | normalizedTarget | normalizedReference) and emit ONE deduped
    // root-cause finding + a `[×N elements]` count after the loop (same pattern as rendered-width-ratio /
    // pseudo dedup) — a whole-site cv11 or stack difference surfaces as ONE finding, never hundreds.
    const typoDecl = new Map(); // `${property}|${normTgt}|${normRef}` -> { property, target, reference, loc, sect, count, sc }
    // font-feature-settings / font-variation-settings normaliser: lowercase, strip quotes, collapse
    // whitespace, split the comma list, sort it (order is semantically irrelevant), rejoin. '' → 'normal'.
    const normFeatureLike = (v) => {
      let s = String(v ?? '').toLowerCase().replace(/["']/g, '').replace(/\s+/g, ' ').trim();
      if (s === '' || s === 'normal') return 'normal';
      const parts = s.split(',').map(p => p.trim()).filter(Boolean).sort();
      return parts.length ? parts.join(', ') : 'normal';
    };
    // full font-family DECLARATION normaliser: lowercase, drop quotes, collapse whitespace, normalise the
    // comma separators — so `'Inter', system-ui` and `inter ,  system-ui` compare equal but a genuinely
    // different stack (`inter, sans-serif` vs `inter, system-ui, …, sans-serif`) does NOT.
    const normFamilyDecl = (v) => String(v ?? '').toLowerCase().replace(/["']/g, '').replace(/\s+/g, ' ')
      .split(',').map(p => p.trim()).filter(Boolean).join(', ');
    // describe the cvXX/ssXX/axis features ADDED vs REMOVED going target→reference, for the suggestedChange.
    const featureDelta = (normTgt, normRef) => {
      const setOf = s => new Set(s === 'normal' ? [] : s.split(', '));
      const t = setOf(normTgt), r = setOf(normRef);
      const added = [...t].filter(x => !r.has(x));   // present on target, absent on reference
      const removed = [...r].filter(x => !t.has(x)); // present on reference, absent on target
      const bits = [];
      if (removed.length) bits.push(`add ${removed.join(' ')}`);
      if (added.length) bits.push(`remove ${added.join(' ')}`);
      return bits.join('; ');
    };
    const addTypo = (property, normTgt, normRef, loc, sect, sc) => {
      const key = property + '|' + normTgt + '|' + normRef;
      let e = typoDecl.get(key);
      if (!e) { e = { property, target: normTgt, reference: normRef, loc, sect, count: 0, sc }; typoDecl.set(key, e); }
      e.count++;
    };

    for (const mn of mock) {
      const isPh = mn.isPh, text = norm(mn.text);
      if (!text && !isPh) continue;
      if (CHROME_TXT.test(text)) continue;

      // REPEATED-TEXT DISAMBIGUATION — pick the same-text candidate by nearest normalised-Y.
      const cands = isPh ? app.filter(n => A.placeholder(n) === text) : app.filter(n => A.text(n) === text);
      let an;
      if (cands.length <= 1) an = cands[0];
      else {
        const mYn = (mn.rect?.y ?? 0) / (mockDoc.frame?.h || 1);
        const scored = cands
          .map(n => ({ n, d: Math.abs(((A.rect(n)?.y ?? 0) / (appDoc.frame?.h || mockDoc.frame?.h || 1)) - mYn) }))
          .sort((a, b) => a.d - b.d);
        an = scored[0].n;
        // record the non-chosen co-text candidates as known noise sources (mispair risk)
        if (scored.length > 1) noiseExcluded.repeatedTextMispairs.push({ text, chosenY: Math.round(A.rect(an)?.y || 0), otherCount: scored.length - 1 });
      }
      if (!an) { if (text) unmatched.push({ text, tag: mn.tag, cls: mn.cls, node: mn }); continue; }
      if (text) pairedTextCount++;

      const sect = sectionFor(an, appLeads);
      const loc = locatorFor(an);
      const el = isPh ? `[placeholder] "${text}"` : `"${text}"`;

      if (!isPh) {
        const mFs = px(mn.comp.fontSize);
        if (mFs != null && !close(A.fontSize(an), mFs, 0.6)) add({ locator: loc, section: sect, class: 'font', property: 'font-size', target: A.fontSize(an), reference: mFs, deltaPx: +(Math.abs((A.fontSize(an) || 0) - mFs)).toFixed(1), suggestedChange: `set font-size: ${mFs}px on ${el}` });
        const mW = parseInt(mn.comp.fontWeight, 10);
        if (mW && A.weight(an) !== mW) add({ locator: loc, section: sect, class: 'font', property: 'font-weight', target: A.weight(an), reference: mW, suggestedChange: `set font-weight: ${mW} on ${el}` });
        const mC = toHex(mn.comp.color);
        if (mC && mC !== 'transparent' && A.color(an) !== mC) add({ locator: loc, section: sect, class: 'font', property: 'color', target: A.color(an), reference: mC, suggestedChange: `set color: ${mC} on ${el}` });
        // line-height (resolve `normal` → ~1.2×). v2.4.0: VALUE-based — compare the RESOLVED line-height px
        // on both sides with a tight tolerance (LH_TOL ~0.6px), not the loose max(2, 0.12·fs) height-proxy
        // tolerance that swallowed a 0.75px label line-height delta (recall MISS #5). The old floor existed
        // because a non-text height proxy is noisy; but the line-height VALUE itself is a precise computed
        // number, so a sub-px-but-real delta (1.45 vs 1.40 → 21.75 vs 21px) IS a defect worth flagging.
        const aLh = A.lineHeight(an);
        let mLh = px(mn.comp.lineHeight);
        if (mLh == null && /normal/i.test(mn.comp.lineHeight || '') && px(mn.comp.fontSize) != null) mLh = px(mn.comp.fontSize) * NORMAL_LH;
        // resolve the TARGET's `normal` the same way so a value-based compare is apples-to-apples.
        let aLhResolved = aLh;
        if (aLhResolved == null && /normal/i.test(String(an.comp?.lineHeight || '')) && A.fontSize(an) != null) aLhResolved = A.fontSize(an) * NORMAL_LH;
        const LH_TOL = 0.6;
        if (mLh != null && aLhResolved != null && !close(aLhResolved, mLh, LH_TOL)) add({ locator: loc, section: sect, class: 'font', property: 'line-height', target: +aLhResolved.toFixed(2), reference: +mLh.toFixed(2), deltaPx: +(Math.abs(aLhResolved - mLh)).toFixed(2), suggestedChange: `set line-height: ${+mLh.toFixed(2)}px on ${el} (currently ${+aLhResolved.toFixed(2)}px — a ${+(Math.abs(aLhResolved - mLh)).toFixed(2)}px delta)` });
        const mFam = familyKind(mn.comp.fontFamily);
        if (mFam && A.family(an) !== mFam) add({ locator: loc, section: sect, class: 'font', property: 'font-family-kind', target: A.family(an), reference: mFam, severity: 'high', suggestedChange: `switch ${el} to a ${mFam} typeface (mock is ${mFam}, target is ${A.family(an)})` });
        if (A.align(an) !== alignNorm(mn.comp.textAlign)) add({ locator: loc, section: sect, class: 'font', property: 'text-align', target: A.align(an), reference: alignNorm(mn.comp.textAlign), suggestedChange: `set text-align: ${alignNorm(mn.comp.textAlign)} on ${el}` });
        // text-wrap (balance vs wrap)
        if (/\s/.test(text)) {
          const wrapOf = c => /balance/.test(`${c.textWrap || ''} ${c.textWrapStyle || ''}`) ? 'balance' : /pretty/.test(`${c.textWrap || ''} ${c.textWrapStyle || ''}`) ? 'pretty' : 'wrap';
          const mw = wrapOf(mn.comp), aw = an.comp ? wrapOf(an.comp) : 'wrap';
          if (aw !== mw) add({ locator: loc, section: sect, class: 'wrap', property: 'text-wrap', target: aw, reference: mw, suggestedChange: `set text-wrap: ${mw} on ${el}` });
        }
        if (mn.hardBreak !== undefined && !!an.hardBreak !== !!mn.hardBreak) add({ locator: loc, section: sect, class: 'wrap', property: 'hard-break(<br>)', target: !!an.hardBreak, reference: !!mn.hardBreak, suggestedChange: mn.hardBreak ? `add an explicit <br> in ${el} to match the mock's hard line break` : `remove the <br> in ${el}` });
        if (mn.lines != null && an.lines != null && an.lines !== mn.lines) {
          // A height-DIFFERING line-count is a REAL wrap divergence (the case-study symptom: live wraps to
          // 4 lines/112px, target to 3 lines/84px), NOT span-splitting — so it is emitted as a confident
          // finding, never bucketed into noiseExcluded. When the box heights also differ we escalate (the
          // wrap genuinely changed the rendered height) and point at the font-metric root cause, since a
          // same-declared-font width drift (the rendered-width-ratio check above) is its usual cause.
          const mH = mn.rect?.h, aH = an.rect?.h;
          const heightsDiffer = mH != null && aH != null && Math.abs(aH - mH) > 2;
          add({ locator: loc, section: sect, class: 'wrap', property: 'line-count', target: an.lines, reference: mn.lines, ...(heightsDiffer ? { deltaPx: Math.round(Math.abs(aH - mH)), severity: 'high' } : {}), suggestedChange: heightsDiffer ? `${el} wraps to ${an.lines} lines (${Math.round(aH)}px tall) but the reference wraps to ${mn.lines} lines (${Math.round(mH)}px) — a real wrap divergence. Check the container width AND, if the declared font/size match, the rendered-width-ratio finding (a font-version metric drift renders the SAME text wider/narrower, changing where it wraps)` : `make ${el} wrap to ${mn.lines} line(s) (adjust max-width / text-wrap)` });
        }
        if (mn.bgLayer && (!an.bgLayer || an.bgLayer.tag !== mn.bgLayer.tag)) add({ locator: loc, section: sect, class: 'media', property: 'bg-media-layer', target: an.bgLayer ? an.bgLayer.tag : 'none', reference: mn.bgLayer.tag, suggestedChange: `add the ${mn.bgLayer.tag} background layer the mock renders behind ${el}` });
        if (mn.wrap && an.wrap && mn.wrap.first && an.wrap.first && an.wrap.first !== mn.wrap.first) add({ locator: loc, section: sect, class: 'wrap', property: 'wrap-point(line1)', target: an.wrap.first, reference: mn.wrap.first, suggestedChange: `adjust ${el} so line 1 ends with "${mn.wrap.first}" (mock breaks differently)` });
        // RENDERED-FONT (v2.0.2 — DOM-span apply/fallback comparison, no canvas).
        // The capture's `fontRn.applies` is now a RENDERED-DOM truth (a hidden span laid out twice and
        // measured): true = the named family's real metrics show through, false = the browser fell back to
        // the generic for that (family,weight,style,size) combo. This SEES a real DOM-level fallback
        // (a registered face the page never actually applies — the Inter-400 fallback class) and does NOT
        // flood on correctly-rendered nodes, unlike the old canvas heuristic.
        //
        // MODE-B RULE: emit a high-severity finding ONLY when the two sides DISAGREE on whether the same
        // declared family applies — the REFERENCE applies its named family for this combo but the TARGET
        // falls back (or vice-versa). Both-apply or both-fall-back → no finding (matched behaviour).
        if (mn.fontRn && an.fontRn && mn.fontRn.family.toLowerCase() === an.fontRn.family.toLowerCase()) {
          const r = mn.fontRn, t = an.fontRn;
          if (r.applies && !t.applies) {
            add({ locator: loc, section: sect, class: 'font', property: 'rendered-font', target: `fallback (${t.family} declared, not applied)`, reference: `${r.family} (applied)`, severity: 'high', suggestedChange: `the reference renders ${r.family} but ${el} falls back to the generic face — ensure the ${t.family} webfont actually loads AND applies (declared but not rendering; check @font-face load + unicode-range + that the family is wired to this element)` });
          } else if (!r.applies && t.applies) {
            add({ locator: loc, section: sect, class: 'font', property: 'rendered-font', target: `${t.family} (applied)`, reference: `fallback (${r.family} declared, not applied)`, severity: 'high', suggestedChange: `the reference falls back to a generic face for ${el} but the target applies ${t.family} — match the reference (the reference does NOT render its named face here)` });
          }
        }
        // TYPOGRAPHIC-DECLARATION (v2.5.1) — accumulate the three declared-shaping divergences for this
        // matched text element, deduped per (property|normTarget|normRef) and emitted once after the loop.
        // Scoped exactly like the other font checks: illustration internals carry placeholder content but
        // this is a STYLE comparison (the site-wide feature/axis/stack is real), so we DON'T suppress it —
        // it's the same computed declaration on every node. (No new illustration suppression needed; the
        // dedup collapses repeats whether or not a node is inside a mockup card.)
        {
          // 1. font-feature-settings — cvXX / ssXX / onum / tnum / … that differ between the sides.
          const tFfs = normFeatureLike(an.comp?.fontFeatureSettings);
          const rFfs = normFeatureLike(mn.comp?.fontFeatureSettings);
          if (tFfs !== rFfs) {
            const delta = featureDelta(tFfs, rFfs);
            addTypo('feature-settings', tFfs, rFfs, loc, sect,
              `${el} declares font-feature-settings: ${tFfs} but the reference uses ${rFfs}${delta ? ` — ${delta}` : ''}. These OpenType features (e.g. cv11 single-story 'a') change the rendered LETTERFORM at the SAME width, so the family-kind / CDP-rendered-font / antialiased-raster checks are all blind to them — set font-feature-settings: ${rFfs === 'normal' ? 'normal' : `"${rFfs.split(', ').join('", "')}"`} to match the reference`);
          }
          // 2. font-variation-settings — a wght/opsz/slnt/… axis applied on one side but not the other.
          const tFvs = normFeatureLike(an.comp?.fontVariationSettings);
          const rFvs = normFeatureLike(mn.comp?.fontVariationSettings);
          if (tFvs !== rFvs) {
            const delta = featureDelta(tFvs, rFvs);
            addTypo('variation-settings', tFvs, rFvs, loc, sect,
              `${el} declares font-variation-settings: ${tFvs} but the reference uses ${rFvs}${delta ? ` — ${delta}` : ''}. A variable-font axis (wght/opsz/slnt) applied on one side and not the other shifts the rendered weight/optical-size without changing the loaded file — set font-variation-settings: ${rFvs} to match the reference`);
          }
          // 3. the FULL font-family DECLARATION — differs even though the KIND (#1170) matched.
          const tFam = normFamilyDecl(an.comp?.fontFamily);
          const rFam = normFamilyDecl(mn.comp?.fontFamily);
          if (tFam && rFam && tFam !== rFam) {
            addTypo('family-exact', tFam, rFam, loc, sect,
              `${el} declares font-family: ${tFam} but the reference declares ${rFam} — the same typeface KIND but a different declared CASCADE (a different first family or fallback stack), which can resolve to a different rendered face on a machine missing the primary. Set the full font-family stack to "${mn.comp?.fontFamily}" to match the reference`);
          }
        }
        // FONT-METRIC / VERSION (v2.2.0) — accumulate the per-family rendered-width RATIO for this matched
        // element. Only when BOTH sides measured an exact width for the SAME first font-family AND that
        // family genuinely APPLIES on both (a fallback would itself change the width and is already reported
        // by rendered-font above). The SAME representative string is rendered in each side's exact computed
        // font, so any width difference at the same declared size is a per-glyph ADVANCE difference ⇒ a
        // different font VERSION/metrics. Aggregated + emitted once-per-family after the loop.
        if (mn.exactW && an.exactW && mn.exactW.w > 0 && an.exactW.w > 0 &&
            mn.exactW.fam.toLowerCase() === an.exactW.fam.toLowerCase()) {
          const bothApply = (!mn.fontRn || mn.fontRn.applies !== false) && (!an.fontRn || an.fontRn.applies !== false);
          if (bothApply) {
            const ratio = an.exactW.w / mn.exactW.w; // target / reference
            const famKey = an.exactW.fam.toLowerCase();
            if (!fontMetricRatios.has(famKey)) fontMetricRatios.set(famKey, []);
            fontMetricRatios.get(famKey).push({ ratio, fam: an.exactW.fam, loc, sect, refW: mn.exactW.w, tgtW: an.exactW.w, sample: an.exactW.sample });
          }
        }
        // BUTTON arrow + geometry + tracking
        {
          const aBtn = buttonAncestor(an, appById), mBtn = mockButtonAncestor(mn);
          if (mBtn && aBtn) {
            // BUTTON ARROW (FIX 2 — GLYPH-based, not svg-presence). Compare the RENDERED trailing-arrow
            // glyph drawn on each side (`arrowGlyph` = the visible union-path bbox of the button's trailing
            // svg, w&h>0 ⇒ a real arrow is painted). svg-presence was wrong both ways: a decorative/hidden
            // svg read as a match, while a genuinely VISIBLE arrow that one side lacks read as fine. Flag an
            // interaction/structure finding when one side draws a visible arrow glyph and the other does not.
            const mArrow = mBtn.arrowGlyph && mBtn.arrowGlyph.w > 0 && mBtn.arrowGlyph.h > 0 ? mBtn.arrowGlyph : null;
            const aArrow = aBtn.arrowGlyph && aBtn.arrowGlyph.w > 0 && aBtn.arrowGlyph.h > 0 ? aBtn.arrowGlyph : null;
            if (!!mArrow !== !!aArrow) {
              if (aArrow && !mArrow) {
                add({ locator: loc, section: sect, class: 'structure', property: 'button-arrow(glyph)', target: `visible arrow ${aArrow.w}×${aArrow.h}px`, reference: 'no arrow drawn', severity: 'med', suggestedChange: `remove the trailing arrow glyph from ${el} — the target draws a visible ${aArrow.w}×${aArrow.h}px arrow the reference button does not` });
              } else if (mArrow && !aArrow) {
                add({ locator: loc, section: sect, class: 'structure', property: mArrow.presenceOnly ? 'button-arrow(presence-only)' : 'button-arrow(glyph)', target: mArrow.presenceOnly ? 'no trailing svg' : 'no arrow drawn', reference: mArrow.presenceOnly ? `a trailing svg of ${mArrow.w}×${mArrow.h}px (BOX, not glyph — the drawn extent is unmeasurable in this engine)` : `visible arrow ${mArrow.w}×${mArrow.h}px`, severity: 'med', suggestedChange: `add the trailing arrow the reference button carries on ${el} (${mArrow.presenceOnly ? `an svg of ${mArrow.w}×${mArrow.h}px — presence-only: the drawn-glyph extent is unavailable in this engine, so a HIDDEN or EMPTY svg would also read as present` : `a visible ${mArrow.w}×${mArrow.h}px arrow`}) — target has none` });
              }
            } else if (mArrow && aArrow && !(mArrow.presenceOnly || aArrow.presenceOnly) && (!close(aArrow.w, mArrow.w, 1.5) || !close(aArrow.h, mArrow.h, 1.5))) {
              // both draw an arrow but the glyph size differs meaningfully → an arrow-size mismatch.
              add({ locator: loc, section: sect, class: 'icon', property: 'button-arrow-glyph-size', target: `${aArrow.w}×${aArrow.h}px`, reference: `${mArrow.w}×${mArrow.h}px`, deltaPx: Math.round(Math.max(Math.abs(aArrow.w - mArrow.w), Math.abs(aArrow.h - mArrow.h))), suggestedChange: `set the trailing arrow glyph on ${el} to ${mArrow.w}×${mArrow.h}px (currently ${aArrow.w}×${aArrow.h}px)` });
            }
            if (mBtn.rect && aBtn.rect) {
              if (!close(aBtn.rect.h, mBtn.rect.h, 3)) add({ locator: loc, section: sect, class: 'geometry', property: 'button-height', target: Math.round(aBtn.rect.h), reference: Math.round(mBtn.rect.h), deltaPx: Math.round(Math.abs(aBtn.rect.h - mBtn.rect.h)), suggestedChange: `set the button height to ${Math.round(mBtn.rect.h)}px on ${el}` });
              if (!close(aBtn.rect.w, mBtn.rect.w, 8)) add({ locator: loc, section: sect, class: 'geometry', property: 'button-width', target: Math.round(aBtn.rect.w), reference: Math.round(mBtn.rect.w), deltaPx: Math.round(Math.abs(aBtn.rect.w - mBtn.rect.w)), suggestedChange: `set the button width to ~${Math.round(mBtn.rect.w)}px on ${el} (padding/tracking)` });
            }
            const mLs = lsPx(mBtn.comp?.letterSpacing), aLs = lsPx(aBtn.comp?.letterSpacing);
            if (mLs != null && aLs != null && !close(aLs, mLs, 0.2)) add({ locator: loc, section: sect, class: 'font', property: 'button-letter-spacing', target: aLs, reference: mLs, suggestedChange: `set letter-spacing: ${mLs}px on ${el}` });
          }
        }
        // sibling gaps
        if (GEOM) {
          const mGn = nextSibGap(mn, mockKids), aGn = nextSibGap(an, appKids);
          if (mGn != null && aGn != null && (mGn > 1 || aGn > 1) && !close(aGn, mGn, 3)) add({ locator: loc, section: sect, class: 'spacing', property: 'gap→next-sibling', target: aGn, reference: mGn, deltaPx: Math.round(Math.abs(aGn - mGn)), suggestedChange: `set the gap to the next sibling to ${mGn}px (gap/margin) after ${el}` });
          const mSibs = mockKids.get(mn.parent), aSibs = appKids.get(an.parent);
          const mPrev = mSibs && mSibs[mSibs.indexOf(mn) - 1], aPrev = aSibs && aSibs[aSibs.indexOf(an) - 1];
          if (mPrev && aPrev && mPrev.rect && aPrev.rect && mn.rect && an.rect) {
            const mGp = +(mn.rect.y - (mPrev.rect.y + mPrev.rect.h)).toFixed(1), aGp = +(an.rect.y - (aPrev.rect.y + aPrev.rect.h)).toFixed(1);
            if ((mGp > 1 || aGp > 1) && !close(aGp, mGp, 3)) add({ locator: loc, section: sect, class: 'spacing', property: 'gap←prev-sibling', target: aGp, reference: mGp, deltaPx: Math.round(Math.abs(aGp - mGp)), suggestedChange: `set the gap from the previous sibling to ${mGp}px before ${el}` });
          }
        }
      } else {
        const mC = toHex(mn.comp.color);
        if (A.phColor(an) !== mC) add({ locator: loc, section: sect, class: 'font', property: 'placeholder-color', target: A.phColor(an), reference: mC, suggestedChange: `set ::placeholder color to ${mC} on ${el}` });
        const mFs = px(mn.comp.fontSize);
        if (mFs != null && !close(A.fontSize(an), mFs, 0.6)) add({ locator: loc, section: sect, class: 'font', property: 'font-size', target: A.fontSize(an), reference: mFs, suggestedChange: `set placeholder font-size: ${mFs}px on ${el}` });
      }

      // gutter inset + row edges + absolute geometry
      const ar = A.rect(an), aX = ar?.x, aW = ar?.w, mX = mn.rect?.x, mW = mn.rect?.w;
      if (aX != null && mX != null) {
        const leftAnch = mX < 0.33 * mockFrameW, rightAnch = mX + (mW || 0) > 0.67 * mockFrameW;
        const rowEdges = (nodes, getRect, cy, frameW) => {
          let min = Infinity, max = -Infinity;
          for (const n of nodes) {
            const r = getRect(n); if (!r || r.w <= 0 || r.x == null) continue;
            if (r.w >= 0.9 * frameW && (r.x || 0) <= 2) continue;
            if (r.y <= cy && r.y + r.h >= cy) { min = Math.min(min, r.x); max = Math.max(max, r.x + r.w); }
          }
          return { min, max };
        };
        const me = rowEdges(mock, n => n.rect, mn.rect.y + mn.rect.h / 2, mockFrameW);
        const ae = rowEdges(app, A.rect, ar.y + ar.h / 2, appFrameW);
        const scrolled = ae.min < -2 || ae.max > appFrameW + 2;
        if (!scrolled) {
          if (leftAnch && !close(aX, mX)) add({ locator: loc, section: sect, class: 'geometry', property: 'left-inset', target: aX, reference: mX, deltaPx: Math.round(Math.abs(aX - mX)), suggestedChange: `align ${el} to a ${mX}px left gutter inset (currently ${aX}px)` });
          if (rightAnch && !leftAnch && aW != null && mW != null) {
            const aRi = +(appFrameW - (aX + aW)).toFixed(1), mRi = +(mockFrameW - (mX + mW)).toFixed(1);
            if (!close(aRi, mRi)) add({ locator: loc, section: sect, class: 'geometry', property: 'right-inset', target: aRi, reference: mRi, deltaPx: Math.round(Math.abs(aRi - mRi)), suggestedChange: `align ${el} to a ${mRi}px right gutter inset (currently ${aRi}px)` });
          }
          if (isFinite(me.min) && isFinite(ae.min) && me.min < 0.5 * mockFrameW && !close(ae.min, me.min)) add({ locator: loc, section: sect, class: 'geometry', property: 'row-left-inset', target: +ae.min.toFixed(1), reference: +me.min.toFixed(1), deltaPx: Math.round(Math.abs(ae.min - me.min)), suggestedChange: `the row's leftmost content should start at ${+me.min.toFixed(1)}px (a leading icon/tile is mis-inset) near ${el}` });
          if (isFinite(me.max) && isFinite(ae.max) && (mockFrameW - me.max) < 0.5 * mockFrameW && !close(appFrameW - ae.max, mockFrameW - me.max)) add({ locator: loc, section: sect, class: 'geometry', property: 'row-right-inset', target: +(appFrameW - ae.max).toFixed(1), reference: +(mockFrameW - me.max).toFixed(1), deltaPx: Math.round(Math.abs((appFrameW - ae.max) - (mockFrameW - me.max))), suggestedChange: `the row's rightmost content (trailing icon/badge) should end at a ${+(mockFrameW - me.max).toFixed(1)}px right inset near ${el}` });
          if (GEOM && aW != null && mW != null) {
            const centered = !leftAnch && !rightAnch;
            if (centered) {
              const aCx = aX + aW / 2, mCx = mX + mW / 2;
              if (!close(aCx, mCx, GEOM_TOL_CENTER)) add({ locator: loc, section: sect, class: 'geometry', property: 'center-x', target: Math.round(aCx), reference: Math.round(mCx), deltaPx: Math.round(Math.abs(aCx - mCx)), suggestedChange: `re-centre ${el} — its centre-x should be ${Math.round(mCx)}px (currently ${Math.round(aCx)}px)` });
              if (!close(aW, mW, GEOM_TOL_SIZE)) add({ locator: loc, section: sect, class: 'geometry', property: 'width', target: Math.round(aW), reference: Math.round(mW), deltaPx: Math.round(Math.abs(aW - mW)), suggestedChange: `set ${el} width to ~${Math.round(mW)}px (constrains wrap point/tracking)` });
            }
            const aH = ar?.h, mH = mn.rect?.h;
            if (aH != null && mH != null && !close(aH, mH, GEOM_TOL_HEIGHT)) add({ locator: loc, section: sect, class: 'geometry', property: 'height', target: Math.round(aH), reference: Math.round(mH), deltaPx: Math.round(Math.abs(aH - mH)), suggestedChange: `${el} renders ${Math.round(aH)}px tall vs ${Math.round(mH)}px — check line-height/wrap/box growth` });
          }
        }
      }

      // nearest styled-ancestor box
      const ab = appStyledAncestor(an), mb = mockStyledAncestor(mn);
      if (mb) {
        const abox = ab ? A.box(ab) : {};
        const mBoxBg = toHex(mb.comp.backgroundColor);
        if (abox.bg !== mBoxBg) add({ locator: loc, section: sect, class: 'container-bg', property: 'box-background', target: abox.bg, reference: mBoxBg, suggestedChange: `set the containing box background to ${mBoxBg} (around ${el})` });
        const mR = px(mb.comp.borderTopLeftRadius);
        if (mR != null && !close(abox.radius, mR, 2.5)) add({ locator: loc, section: sect, class: 'border', property: 'box-border-radius', target: abox.radius, reference: mR, deltaPx: Math.round(Math.abs((abox.radius || 0) - mR)), suggestedChange: `set the containing box border-radius to ${mR}px (around ${el})` });
        if (!!abox.shadow !== mockHasShadow(mb.comp)) add({ locator: loc, section: sect, class: 'shadow', property: 'box-shadow', target: abox.shadow ? 'yes' : 'no', reference: mockHasShadow(mb.comp) ? 'yes' : 'no', suggestedChange: mockHasShadow(mb.comp) ? `add a box-shadow to the containing box (around ${el})` : `remove the box-shadow from the containing box (around ${el})` });
        const mPL = px(mb.comp.paddingLeft);
        if (mPL != null && !close(abox.padLeft, mPL)) add({ locator: loc, section: sect, class: 'spacing', property: 'box-pad-left', target: abox.padLeft, reference: mPL, deltaPx: Math.round(Math.abs((abox.padLeft || 0) - mPL)), suggestedChange: `set padding-left: ${mPL}px on the containing box (around ${el})` });
        const mPT = px(mb.comp.paddingTop);
        if (mPT != null && !close(abox.padTop, mPT)) add({ locator: loc, section: sect, class: 'spacing', property: 'box-pad-top', target: abox.padTop, reference: mPT, deltaPx: Math.round(Math.abs((abox.padTop || 0) - mPT)), suggestedChange: `set padding-top: ${mPT}px on the containing box (around ${el})` });
        const mPB = px(mb.comp.paddingBottom);
        if (mPB != null && !close(abox.padBottom, mPB)) add({ locator: loc, section: sect, class: 'spacing', property: 'box-pad-bottom', target: abox.padBottom, reference: mPB, deltaPx: Math.round(Math.abs((abox.padBottom || 0) - mPB)), suggestedChange: `set padding-bottom: ${mPB}px on the containing box (around ${el})` });
      }
    }

    // ============= FONT-METRIC / VERSION MISMATCH (v2.2.0) =============
    // The text-probe pass measured, per matched element, the rendered width of the SAME representative
    // string in each side's EXACT computed font (same family/weight/size/letter-spacing/feature-settings).
    // A font-VERSION mismatch (e.g. the target self-hosts rsms Inter v4 while live uses Google Inter v20)
    // is UNIFORM: every element in that family renders ~the same width RATIO target/reference at the same
    // declared size. We aggregate per family and emit ONE high finding per family when the MEDIAN ratio
    // deviates from 1.0 by more than `FM_TOL` — the real case is ~1.8% (ratio ≈ 0.982); a sub-pixel
    // single-element diff (well under the tolerance) does NOT fire, and a per-element flood is impossible
    // because the emit is deduped to one row per family. This is the ROOT CAUSE behind a height-differing
    // line-count: same declared font + size, consistently different rendered WIDTH ⇒ a different version.
    {
      const FM_TOL = 0.007;     // 0.7% — below the ~1.8% real case, above sub-pixel single-glyph noise
      const FM_MIN_SAMPLES = 3; // require a few matched elements so one outlier can't fake a uniform shift
      const median = arr => { const s = [...arr].sort((a, b) => a - b); const n = s.length; return n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2; };
      for (const [, rows] of fontMetricRatios) {
        if (rows.length < FM_MIN_SAMPLES) continue;
        const ratios = rows.map(r => r.ratio);
        const med = median(ratios);
        if (Math.abs(med - 1) <= FM_TOL) continue; // within tolerance → same version, no finding
        // CONSISTENCY guard: a font-version mismatch is uniform, so MOST elements should agree with the
        // median direction. If the ratios are scattered (some wider, some narrower) it is NOT a version
        // drift (more likely per-element noise / mixed faces) — require ≥70% on the median's side.
        const sameDir = ratios.filter(r => (med > 1 ? r > 1 + FM_TOL / 2 : r < 1 - FM_TOL / 2)).length;
        if (sameDir / ratios.length < 0.7) continue;
        const fam = rows[0].fam;
        const pct = +(Math.abs(med - 1) * 100).toFixed(1);
        const dir = med < 1 ? 'narrower' : 'wider';
        const rep = rows.find(r => Math.abs(r.ratio - med) === Math.min(...ratios.map(x => Math.abs(x - med)))) || rows[0];
        add({
          locator: rep.loc || `[font-metric ${fam}]`, section: rep.sect, class: 'font', property: 'rendered-width-ratio',
          target: `${fam} renders ${med.toFixed(3)}x (≈${pct}% ${dir}) than reference at the same size`,
          reference: '1.00',
          severity: 'high',
          suggestedChange: `${fam} at the SAME declared size renders ${pct}% ${dir} on the target than on the reference (e.g. "${(rep.sample || '').slice(0, 32)}" = ${rep.tgtW}px vs ${rep.refW}px) across ${rows.length} matched text elements — same family + size, consistently different rendered WIDTH ⇒ the two sides use a DIFFERENT FONT VERSION/metrics (this is what makes a block wrap to a different line count). Self-host the SAME font VERSION the reference uses (e.g. Google Inter v20 ≈ rsms Inter v3.19, NOT v4)`,
        });
      }
    }

    // ============= TYPOGRAPHIC-DECLARATION MISMATCH (v2.5.1) =============
    // Emit the accumulated font-feature-settings / font-variation-settings / full-font-family-DECLARATION
    // divergences, DEDUPED to ONE root-cause finding per (property|normTarget|normRef) + a `[×N elements]`
    // count. These properties are almost always set SITE-WIDE, so a single divergence repeats on every text
    // element — the dedup turns a whole-site cv11 or stack difference into ONE finding, never hundreds. MED
    // severity (a declared-shaping drift, not a structural defect). Each closes a class the family-kind
    // check, the CDP rendered-font probe (#37), and the antialiased raster diff are all structurally blind
    // to (the font FILE is identical; only the requested glyph/axis/cascade differs).
    {
      const PROP_LABEL = {
        'feature-settings': 'font-feature-settings',
        'variation-settings': 'font-variation-settings',
        'family-exact': 'font-family (full declaration)',
      };
      for (const e of typoDecl.values()) {
        const n = e.count;
        add({
          locator: e.loc, section: e.sect, class: 'font', property: e.property,
          target: e.target, reference: e.reference, severity: 'med',
          suggestedChange: `${e.sc}${n > 1 ? ` [×${n} elements — ${PROP_LABEL[e.property] || e.property} is declared site-wide]` : ''}`,
        });
      }
    }

    // ============= FONT FACES (synthesis risk + missing family) =============
    {
      const mockFonts = mockDoc.fonts || [], appFonts = appDoc.fonts || [];
      const isRange = w => /\s/.test(String(w));
      const appRange = appFonts.find(f => isRange(f.weight) && !/placeholder/i.test(f.family));
      const mockHasRange = mockFonts.some(f => isRange(f.weight));
      if (appRange && mockFonts.length && !mockHasRange) {
        const mockWeights = mockFonts.filter(f => f.family.toLowerCase() === appRange.family.toLowerCase()).map(f => f.weight).join('/') || 'static instances';
        add({ locator: `[fonts] ${appRange.family}`, section: null, class: 'fonts', property: 'weight-range-synthesis-risk', target: appRange.weight, reference: mockWeights, suggestedChange: `load discrete STATIC instances of ${appRange.family} (mock uses ${mockWeights}) — a single range-weight file faux-synthesises weights and blurs text on HiDPI` });
      }
      const appFamilies = new Set(appFonts.map(f => f.family.toLowerCase()));
      for (const fam of new Set(mockFonts.filter(f => !/placeholder/i.test(f.family)).map(f => f.family))) {
        if (!appFamilies.has(fam.toLowerCase())) add({ locator: `[fonts] ${fam}`, section: null, class: 'fonts', property: 'family-not-loaded', target: 'absent', reference: 'loaded', suggestedChange: `load the ${fam} webfont (mock loads it; target falls back)` });
      }
    }

    // ============= ICON GLYPH sizes (position-paired) =============
    if (GEOM) {
      const mockIcons = mock.filter(n => n.glyph && n.glyph.w > 0);
      const appIcons = app.filter(n => n.glyph && n.glyph.w > 0);
      const usedApp = new Set();
      for (const mi of mockIcons) {
        const mcx = mi.rect.x + mi.rect.w / 2, mcy = mi.rect.y + mi.rect.h / 2;
        let best = null, bestD = Infinity;
        for (const ai of appIcons) {
          if (usedApp.has(ai.i)) continue;
          const d = Math.hypot((ai.rect.x + ai.rect.w / 2) - mcx, (ai.rect.y + ai.rect.h / 2) - mcy);
          if (d < bestD) { bestD = d; best = ai; }
        }
        if (best && bestD <= GEOM_TOL_CENTER * 4) {
          usedApp.add(best.i);
          const loc = `[icon @${Math.round(mcx)},${Math.round(mcy)}]`;
          const sect = sectionFor(best, appLeads);
          const _po = !!(best.glyph.presenceOnly || mi.glyph.presenceOnly);
          const _poNote = _po ? ' [presence-only: the drawn-glyph extent is unavailable in this engine, so this is the svg BOX, not the path]' : '';
          if (!close(best.glyph.w, mi.glyph.w, 1.5)) add({ locator: loc, section: sect, class: 'icon', property: _po ? 'icon-box-w(presence-only)' : 'icon-glyph-w', target: best.glyph.w, reference: mi.glyph.w, deltaPx: +(Math.abs(best.glyph.w - mi.glyph.w)).toFixed(1), suggestedChange: `the ${_po ? 'icon box' : 'drawn icon glyph'} width should be ${mi.glyph.w}px (currently ${best.glyph.w}px) at ${loc}` + _poNote });
          if (!close(best.glyph.h, mi.glyph.h, 1.5)) add({ locator: loc, section: sect, class: 'icon', property: _po ? 'icon-box-h(presence-only)' : 'icon-glyph-h', target: best.glyph.h, reference: mi.glyph.h, deltaPx: +(Math.abs(best.glyph.h - mi.glyph.h)).toFixed(1), suggestedChange: `the ${_po ? 'icon box' : 'drawn icon glyph'} height should be ${mi.glyph.h}px (currently ${best.glyph.h}px) at ${loc}` + _poNote });
        }
      }
    }

    // ============= RENDERED-GLYPH-SHAPE / FONT-FEATURE EFFECTIVENESS (v2.1.0) =============
    // Two complementary signals, both reading the per-side `featureCheck` (capture-side self-check) that
    // tested, per requested OpenType feature, whether rendering the same probe WITH vs WITHOUT the
    // requested `font-feature-settings` produces a different GLYPH SHAPE:
    //   (A) FEATURE-EFFECTIVENESS SELF-CHECK (strongest) — flag the TARGET's requested features that are
    //       INEFFECTIVE (font lacks the glyph → renders default). This is the homepage cv11 bug: cv11
    //       declared + applied identically to live, the controlled span widths matched, yet the target's
    //       self-hosted Inter woff2 was a subset that stripped the cv11 glyph, so the requested cv11 had
    //       no effect (double-story 'a' instead of single-story).
    //   (B) CROSS-SIDE ESCALATION (MODE B) — when the REFERENCE's same feature IS effective but the
    //       TARGET's is not, that is a real cross-side letterform divergence despite identical computed
    //       font props → raise the severity and name the reference.
    // `effective` is resolved EITHER in-page (canvas-fontFeatureSettings supported) OR by the runner
    // (screenshot pixel-diff of the probe pairs, merged into featureCheck.combos before this pass).
    {
      const tfc = appDoc.featureCheck, rfc = refDoc.featureCheck;
      const featureLabel = combo => {
        const feats = (combo.features && combo.features.length) ? combo.features.map(s => String(s).replace(/["']/g, '')).join(', ') : combo.ffs;
        return feats;
      };
      // index the reference combos by (first-family|features) so we can find the reference's verdict for
      // the SAME requested feature on the SAME family, even if weight/size differ slightly.
      const refByFeat = new Map();
      if (rfc && rfc.combos) for (const rc of rfc.combos) {
        const fk = (rc.first || '').toLowerCase() + '|' + (rc.ffs || '');
        if (!refByFeat.has(fk)) refByFeat.set(fk, rc);
      }
      const fcLoc = combo => {
        // a representative locator: the first target text node that uses this combo.
        const ni = (combo.nodeIdxs || [])[0];
        const n = ni != null ? appAll[ni] : null;
        return n ? locatorFor(n) : `[text in ${combo.first} ${combo.size}/${combo.weight} feat:${featureLabel(combo)}]`;
      };
      const fcSect = combo => { const ni = (combo.nodeIdxs || [])[0]; const n = ni != null ? appAll[ni] : null; return n ? sectionFor(n, appLeads) : null; };
      const featSeen = new Set();
      if (tfc && tfc.combos) {
        for (const tc of tfc.combos) {
          if (tc.effective !== false) continue; // only INEFFECTIVE features are a defect (null = not yet resolved)
          const fk = (tc.first || '').toLowerCase() + '|' + (tc.ffs || '');
          if (featSeen.has(fk)) continue; featSeen.add(fk);
          const rc = refByFeat.get(fk);
          const lbl = featureLabel(tc);
          const loc = fcLoc(tc), sect = fcSect(tc), count = (tc.nodeIdxs || []).length;
          if (rc && rc.effective === true) {
            // (B) cross-side divergence: reference renders the distinct letterform, target does not.
            add({
              locator: loc, section: sect, class: 'font', property: 'feature-ineffective',
              target: `${lbl} requested but font lacks the glyph (renders default letterform)`,
              reference: `${lbl} effective (distinct letterform rendered)`,
              severity: 'high',
              suggestedChange: `the reference renders a DISTINCT letterform for the requested ${lbl} on ${tc.first} (e.g. cv11 single-story 'a') but the target renders the DEFAULT glyph at the SAME width — its self-hosted ${tc.first} woff2 is a SUBSET that STRIPPED the ${lbl} glyph. Self-host a FULL ${tc.first} (the complete font with the cvXX/ssXX glyphs) so the declared font-feature-settings actually takes effect${count > 1 ? ` — affects ${count} text nodes` : ''}`,
            });
          } else {
            // (A) self-check absolute: the target requests a feature that has no effect (font lacks glyph).
            add({
              locator: loc, section: sect, class: 'font', property: 'feature-ineffective',
              target: `${lbl} requested but font lacks the glyph (renders default)`,
              reference: rc && rc.effective === false ? `${lbl} also ineffective on reference` : `${lbl} requested`,
              severity: rc && rc.effective === false ? 'low' : 'high',
              suggestedChange: `self-host a full ${tc.first} that contains the ${lbl} glyphs (a subset woff2 strips them) — the requested font-feature-settings:${tc.ffs} has NO EFFECT on the rendered glyph shape (same width as the default, so width/DOM-span checks can't see it)${count > 1 ? ` — affects ${count} text nodes` : ''}`,
            });
          }
        }
      }
      // honesty: if the target requested features but the verdict could not be resolved (runner pixel-diff
      // not supplied AND canvas unsupported), surface ONE low note so a silent "no finding" isn't mistaken
      // for "all features effective".
      if (tfc && tfc.ran && tfc.mechanism === 'runner-screenshot' && tfc.combos && tfc.combos.some(c => c.effective == null)) {
        const pending = tfc.combos.filter(c => c.effective == null).length;
        add({
          locator: '[font-feature self-check]', section: null, class: 'font', property: 'feature-check-pending',
          target: `${pending} feature combo(s) unresolved`, reference: 'glyph-shape pixel-diff needed',
          severity: 'low',
          suggestedChange: `this engine lacks canvas fontFeatureSettings, so the rendered-glyph-shape self-check needs the RUNNER step: screenshot the page and run feature-check.mjs over analysis.featureCheck.probes (pixel-diff each on/off probe pair); inject the result via globalThis.__MF_FEATURE_DIFFS__ and re-run MODE B to resolve ${pending} requested OpenType feature(s). The runner step needs a browser that loads web fonts — see run.md § v2.1.0`,
        });
      }
    }

    // ============= NON-TEXT CONTAINER PASS =============
    {
      const kidsByParent = arr => { const m = new Map(); for (const n of arr) { if (!m.has(n.parent)) m.set(n.parent, []); m.get(n.parent).push(n); } return m; };
      const mKidsP = kidsByParent(mock), aKidsP = kidsByParent(appAll);
      const pathOf = (nodes, kids, n) => {
        const parts = []; let cur = n, hops = 0;
        while (cur && cur.parent >= 0 && hops++ < 40) { const sibs = kids.get(cur.parent) || []; parts.unshift(`${cur.tag}[${sibs.indexOf(cur)}]`); cur = nodes[cur.parent]; }
        return parts.join('/');
      };
      const isContainer = n => {
        if (!n || n.tag === 'body' || /\b(body|scr|frame|screen)\b/.test(n.cls || '')) return false;
        if (norm(n.text)) return false;
        const c = n.comp || {}, r = n.rect || {};
        if ((r.w || 0) < 80 || (r.h || 0) < 8) return false;
        const hasBg = toHex(c.backgroundColor) !== 'transparent' && c.backgroundColor;
        const hasBorder = (px(c.borderTopWidth) || 0) > 0 || (px(c.borderBottomWidth) || 0) > 0;
        const hasRadius = (px(c.borderTopLeftRadius) || 0) >= 4;
        const hasShadow = c.boxShadow && c.boxShadow !== 'none';
        return !!(hasBg || hasBorder || hasRadius || hasShadow || n.fullBleedMedia || n.divider);
      };
      const mockContainers = mock.filter(isContainer);
      const appByPath = new Map();
      for (const a of appAll) if (isContainer(a)) { const p = pathOf(appAll, aKidsP, a); if (!appByPath.has(p)) appByPath.set(p, a); }
      const geomKey = a => `${Math.round((a.rect.x || 0) / 8) * 8}|${Math.round((a.rect.w || 0) / 8) * 8}`;
      const appByGeom = new Map();
      for (const a of appAll) if (isContainer(a)) { const k = geomKey(a); if (!appByGeom.has(k)) appByGeom.set(k, []); appByGeom.get(k).push(a); }
      const cUsed = new Set();
      const mediaDedupKey = n => (n.fullBleedMedia ? 'media|' + n.fullBleedMedia.src : 'div|' + (n.divider?.kind || '')) + '|' + Math.round((n.rect.y || 0) / 24);
      const absentSeen = new Set();
      for (const m of mockContainers) {
        const mp = pathOf(mock, mKidsP, m);
        let a = appByPath.get(mp);
        if (!a) {
          const bucket = (appByGeom.get(geomKey(m)) || []).filter(n => !cUsed.has(n.i));
          if (bucket.length) {
            const mYn = (m.rect.y || 0) / (mockDoc.frame?.h || 1), mH = m.rect.h || 0;
            const scored = bucket.map(n => {
              const dY = Math.abs((n.rect.y || 0) / (appDoc.frame?.h || 1) - mYn);
              const dH = Math.abs((n.rect.h || 0) - mH);
              const hOk = dH <= Math.max(60, 0.4 * mH);
              const cost = dY + (dH / (mockDoc.frame?.h || 1)) * 0.5 + (n.tag === m.tag ? 0 : 0.005);
              return { n, dY, hOk, cost };
            }).filter(s => s.hOk).sort((x, y) => x.cost - y.cost)[0];
            if (scored && scored.dY <= 0.04) a = scored.n;
          }
        }
        const sect = sectionFor(m, mockLeads);
        if (!a) {
          // unpaired reference container — only an honest absence if it has a real backdrop or divider.
          const mBd = effectiveBackdrop(m);
          if (!mBd && !m.divider) continue;
          const dk = mediaDedupKey(m);
          if (absentSeen.has(dk)) continue; absentSeen.add(dk);
          const loc = `[container ${m.tag} @y${Math.round(m.rect.y)} w${Math.round(m.rect.w)}]`;
          if (mBd) add({ locator: loc, section: sect, class: 'gradient', property: 'bg-media-layer', target: 'absent', reference: `backdrop ${mBd.kind}`, severity: 'high', suggestedChange: `add the full-bleed ${mBd.kind} background/gradient layer this section has on the mock (it is FLAT on target)` });
          else add({ locator: loc, section: sect, class: 'border', property: 'divider', target: 'absent', reference: `divider ${m.divider.kind}`, severity: 'high', suggestedChange: `add the ${m.divider.kind} ${m.divider.thickness}px page-wide rule the mock has here` });
          continue;
        }
        cUsed.add(a.i);
        const mc = m.comp || {}, ac = a.comp || {};
        const loc = locatorFor(a) || `[container ${m.tag}.${(m.cls || '').split(/\s+/)[0]} @y${Math.round(m.rect.y)} w${Math.round(m.rect.w)}]`;
        const mBg = toHex(mc.backgroundColor), aBg = toHex(ac.backgroundColor);
        if (mBg !== aBg) {
          // WHEN THE GRADIENT CLASS IS SILENCED, A FLAT-COLOUR FINDING CAN POINT THE WRONG WAY.
          // `backgroundColor` is the only half of the backdrop this engine reports. If the reference
          // paints a gradient, its backgroundColor is whatever sits UNDERNEATH it — often white — so the
          // finding reads "target #eaf1ff vs reference #ffffff" and a developer sets the band to flat
          // white, deleting the flat colour that was the closest thing to the gradient. All three judges
          // on the blind panel named this row independently as the one that would ship a defect.
          const gradientBlind = !((tCaps.gradient && tCaps.gradient.available) && (rCaps.gradient && rCaps.gradient.available));
          const suspect = gradientBlind && (mBg === 'transparent' || mBg === '#ffffff') && aBg !== 'transparent';
          add({
            locator: loc, section: sect, class: 'container-bg', property: suspect ? 'background(gradient-blind)' : 'background',
            target: aBg, reference: mBg, severity: suspect ? 'med' : 'high',
            suggestedChange: suspect
              ? `the reference reports ${mBg} and the target ${aBg} — but this engine cannot read background-image, so ${mBg} may be the layer UNDERNEATH a gradient the reference paints and this differ cannot see. Do NOT set the container to ${mBg} on this evidence: open the reference in a real browser, read its background-image, and match that. Setting the flat value here can delete the closest approximation you already had.`
              : `set the container background to ${mBg}`,
          });
        }
        // FIX 2 — compare EFFECTIVE backdrops (full-bleed media OR css background-image on the element).
        // Only "absent" when one side has a backdrop and the other has NONE; if both have one but they
        // differ, that is a lower-severity value-precision divergence, not a missing layer.
        {
          const mBd = effectiveBackdrop(m), aBd = effectiveBackdrop(a);
          if (mBd && !aBd) {
            const dk = mediaDedupKey(m);
            if (!absentSeen.has(dk)) { absentSeen.add(dk); add({ locator: loc, section: sect, class: 'gradient', property: 'bg-media-layer', target: 'none', reference: mBd.kind, severity: 'high', suggestedChange: `add the full-bleed ${mBd.kind} gradient/media layer to this container (FLAT on target)` }); }
          } else if (mBd && aBd && mBd.kind !== aBd.kind && mBd.src !== aBd.src) {
            // both sides HAVE a backdrop but it is expressed/valued differently → precision, not absence.
            add({ locator: loc, section: sect, class: 'value', property: 'backdrop-differs', target: aBd.kind, reference: mBd.kind, severity: 'med', suggestedChange: `the container backdrop differs (mock: ${mBd.kind}, target: ${aBd.kind}) — match the reference's gradient/media backdrop` });
          }
        }
        const mBt = px(mc.borderTopWidth) || 0, aBt = px(ac.borderTopWidth) || 0;
        if (Math.abs(mBt - aBt) > 0.5) add({ locator: loc, section: sect, class: 'border', property: 'border-top-width', target: aBt, reference: mBt, suggestedChange: mBt > aBt ? `add a ${mBt}px top border (color ${toHex(mc.borderTopColor)}) to this container — the mock has it, the target lost it` : `remove the ${aBt}px top border from this container` });
        else if (mBt > 0 && toHex(mc.borderTopColor) !== toHex(ac.borderTopColor)) add({ locator: loc, section: sect, class: 'border', property: 'border-top-color', target: toHex(ac.borderTopColor), reference: toHex(mc.borderTopColor), suggestedChange: `set the container top border color to ${toHex(mc.borderTopColor)}` });
        const mBb = px(mc.borderBottomWidth) || 0, aBb = px(ac.borderBottomWidth) || 0;
        if (Math.abs(mBb - aBb) > 0.5) add({ locator: loc, section: sect, class: 'border', property: 'border-bottom-width', target: aBb, reference: mBb, suggestedChange: mBb > aBb ? `add a ${mBb}px bottom border to this container` : `remove the ${aBb}px bottom border from this container` });
        const mR = px(mc.borderTopLeftRadius), aR = px(ac.borderTopLeftRadius);
        if (mR != null && aR != null && !close(mR, aR, 2.5)) add({ locator: loc, section: sect, class: 'border', property: 'border-radius', target: aR, reference: mR, deltaPx: Math.round(Math.abs(mR - aR)), suggestedChange: `set the container border-radius to ${mR}px` });
        const mSh = mockHasShadow(mc), aSh = mockHasShadow(ac);
        if (mSh !== aSh) add({ locator: loc, section: sect, class: 'shadow', property: 'shadow', target: aSh ? 'yes' : 'no', reference: mSh ? 'yes' : 'no', suggestedChange: mSh ? `add the box-shadow the mock container has` : `remove the box-shadow — the mock container is flat` });
        if (m.divider && !a.divider) {
          const dk = mediaDedupKey(m);
          if (!absentSeen.has(dk)) { absentSeen.add(dk); add({ locator: loc, section: sect, class: 'border', property: 'divider', target: 'absent', reference: `${m.divider.kind} ${m.divider.thickness}px`, severity: 'high', suggestedChange: `add the ${m.divider.kind} ${m.divider.thickness}px rule the mock has on this container` }); }
        }
      }
    }

    // ============= MEDIA / ILLUSTRATION GEOMETRY (rel-y vs section) =============
    if (GEOM) {
      const frameW = mockDoc.frame?.w || mockFrameW;
      const isMediaEl = n => ['img', 'canvas', 'svg', 'picture', 'video'].includes(n.tag) && (n.rect?.w || 0) >= 120 && (n.rect?.h || 0) >= 100 && (n.rect?.w || 0) < 0.9 * frameW;
      const isMockupCard = n => (n.rect?.w || 0) >= 280 && (n.rect?.w || 0) < 0.9 * frameW && (n.rect?.h || 0) >= 260 && (px(n.comp?.borderTopLeftRadius) >= 8 || (toHex(n.comp?.backgroundColor) !== 'transparent' && n.comp?.backgroundColor)) && !norm(n.text);
      const mMedia = mock.filter(n => isMediaEl(n) || isMockupCard(n));
      const aMedia = app.filter(n => isMediaEl(n) || isMockupCard(n));
      const anchorOf = (node, nodes) => {
        let best = null, bestScore = Infinity;
        const my = node.rect.y;
        for (const t of nodes) {
          if (!isSectionLead(t)) continue;
          const tMid = t.rect.y + (t.rect.h || 0) / 2;
          const dist = Math.abs(my - tMid);
          if (dist > 280) continue;
          const tx = norm(t.text);
          const eyebrow = /^[A-Z0-9 ·&,'’\-]+$/.test(tx) && tx.length <= 40;
          const score = dist - (eyebrow ? 12 : 0);
          if (score < bestScore) { bestScore = score; best = t; }
        }
        return best;
      };
      const anchorByText = (txt, nodes) => {
        const t = norm(txt); let best = null, bestW = -1;
        for (const n of nodes) { if (isSectionLead(n) && norm(n.text) === t && (n.rect?.w || 0) > bestW) { best = n; bestW = n.rect.w; } }
        return best;
      };
      const aUsed = new Set();
      for (const m of mMedia) {
        const mAnchor = anchorOf(m, mock);
        if (!mAnchor) continue;
        const mRelY = m.rect.y - (mAnchor.rect.y + mAnchor.rect.h);
        const cands = aMedia.filter(n => !aUsed.has(n.i) && close(n.rect.x, m.rect.x, 24) && close(n.rect.w, m.rect.w, 40));
        let a = cands.find(c => { const aAnc = anchorOf(c, app); return aAnc && norm(aAnc.text) === norm(mAnchor.text); });
        if (!a && cands.length) {
          const mYn = (m.rect.y || 0) / (mockDoc.frame?.h || 1);
          a = cands.map(n => ({ n, d: Math.abs((n.rect.y || 0) / (appDoc.frame?.h || 1) - mYn) })).sort((x, y) => x.d - y.d)[0].n;
        }
        if (!a) { noiseExcluded.illustrationInternals.push({ note: 'unpaired media', y: Math.round(m.rect.y) }); continue; }
        aUsed.add(a.i);
        const aAnchor = anchorByText(mAnchor.text, app) || anchorOf(a, app);
        if (!aAnchor) continue;
        const aRelY = a.rect.y - (aAnchor.rect.y + aAnchor.rect.h);
        const inSection = Math.abs(aRelY) <= 320 && Math.abs(mRelY) <= 320;
        if (!inSection) continue;
        if (!close(aRelY, mRelY, 8)) add({ locator: `[media ${m.tag} @y${Math.round(m.rect.y)} w${Math.round(m.rect.w)}]`, section: norm(mAnchor.text).slice(0, 40), class: 'media', property: 'media-rel-y(vs section)', target: Math.round(aRelY), reference: Math.round(mRelY), deltaPx: Math.round(Math.abs(aRelY - mRelY)), suggestedChange: `move this media so its top sits ${Math.round(mRelY)}px from the "${norm(mAnchor.text).slice(0, 24)}" section lead (currently ${Math.round(aRelY)}px)` });
      }
    }

    // ============= ILLUSTRATION-INTERNAL STYLE PASS (v2.3.0) =============
    // The text passes now SUPPRESS illustration internals' placeholder TEXT-content findings (above). This
    // pass restores their STYLE coverage — the half of the old over-broad exclusion that was wrongly dropped.
    // It pairs illustration ROOTS across sides (geometry: x/w + nearest frame-normalised Y), then pairs each
    // root's INTERNALS across sides BY POSITION/STRUCTURE — NOT by text, because the text is placeholder and
    // differs (e.g. "ASX:MVR" vs "ASX:XYZ"). For each paired internal it compares the COMPUTED STYLE: border
    // (incl. the ::after/::before fold already in `comp`), border-radius, box-shadow, background/text colour,
    // letter-spacing, font-size/weight/family, padding, and geometry (size). It does NOT compare the text
    // STRING (suppressed by design). To avoid flooding on a repeated mockup row (N identical rows with the
    // same style), identical findings are deduped to a few rows + a `[×N]` summary.
    {
      const mockRoots = mockIllo.roots;
      const appRoots = appIllo.roots;
      if (mockRoots.length && appRoots.length) {
        // helpers scoped to this pass
        const fH_m = mockDoc.frame?.h || 1, fH_a = appDoc.frame?.h || 1;
        const subtreeOf = (nodes, getKids, rootI) => {
          const out = [], stack = [rootI];
          while (stack.length) { const cur = stack.pop(); for (const k of (getKids.get(cur) || [])) { out.push(k); stack.push(k.i); } }
          return out;
        };
        const mKidsMap = mockKids, aKidsMap = appKids;     // already built (childrenByParent), parent->kids
        const appUsedRoot = new Set();
        // pair each mock illustration root to the nearest unused app illustration root by x/w + normalised Y
        const rootPairs = [];
        for (const mr of mockRoots) {
          const cands = appRoots.filter(a => !appUsedRoot.has(a.i) && close(a.rect.x, mr.rect.x, 40) && close(a.rect.w, mr.rect.w, 60));
          if (!cands.length) continue;
          const myN = (mr.rect.y || 0) / fH_m;
          const best = cands.map(a => ({ a, d: Math.abs((a.rect.y || 0) / fH_a - myN) })).sort((x, y) => x.d - y.d)[0];
          if (best && best.d <= 0.06) { appUsedRoot.add(best.a.i); rootPairs.push({ mr, ar: best.a }); }
        }
        // collect raw style findings here, then dedup by a (property|targetVal|referenceVal) signature.
        const illoRaw = [];
        const pushIllo = (o) => illoRaw.push(o);
        for (const { mr, ar } of rootPairs) {
          const mSubs = subtreeOf(mock, mKidsMap, mr.i).filter(n => (n.rect?.w || 0) > 0 && (n.rect?.h || 0) > 0);
          const aSubs = subtreeOf(appAll, aKidsMap, ar.i).filter(n => (n.rect?.w || 0) > 0 && (n.rect?.h || 0) > 0);
          if (!mSubs.length || !aSubs.length) continue;
          const sect = sectionFor(mr, mockLeads);
          const aUsed = new Set();
          // pair an internal by RELATIVE position inside its root (offset from the root's top-left, both
          // normalised by the root size so a slightly-different-size rebuilt card still aligns) + tag.
          const relOf = (n, root) => ({
            rx: ((n.rect.x - root.rect.x) / Math.max(1, root.rect.w)),
            ry: ((n.rect.y - root.rect.y) / Math.max(1, root.rect.h)),
          });
          for (const ms of mSubs) {
            const mr2 = relOf(ms, mr);
            // candidate app internals: same-ish relative position; prefer same tag, then nearest by rel-dist.
            let best = null, bestCost = Infinity;
            for (const as of aSubs) {
              if (aUsed.has(as.i)) continue;
              const ar2 = relOf(as, ar);
              const dPos = Math.abs(mr2.rx - ar2.rx) + Math.abs(mr2.ry - ar2.ry);
              if (dPos > 0.14) continue;                     // not the same position inside the card
              const cost = dPos + (as.tag === ms.tag ? 0 : 0.03) + Math.abs((as.rect.w - ms.rect.w)) / Math.max(1, ar.rect.w) * 0.2;
              if (cost < bestCost) { bestCost = cost; best = as; }
            }
            if (!best) continue;
            aUsed.add(best.i);
            const as = best;
            const mc = ms.comp || {}, ac = as.comp || {};
            const loc = `[illustration ${ms.tag}${ms.cls ? '.' + (ms.cls.split(/\s+/)[0]) : ''} @rel ${(relOf(ms, mr).rx * 100).toFixed(0)}%,${(relOf(ms, mr).ry * 100).toFixed(0)}%]`;
            // --- BORDER (folded ::after/::before already in comp) ---
            const mBt = px(mc.borderTopWidth) || 0, aBt = px(ac.borderTopWidth) || 0;
            if (!close(aBt, mBt, 0.6)) pushIllo({ loc, sect, class: 'border', property: 'illo-border-width', target: aBt, reference: mBt, deltaPx: Math.round(Math.abs(aBt - mBt)), sc: `set the illustration sub-element border to ${mBt}px (mock draws ${mBt}px${mc._borderFromPseudo ? ' via ' + mc._borderFromPseudo : ''}, target ${aBt}px)` });
            else if (mBt >= 0.6 && toHex(mc.borderTopColor) !== toHex(ac.borderTopColor)) pushIllo({ loc, sect, class: 'border', property: 'illo-border-color', target: toHex(ac.borderTopColor), reference: toHex(mc.borderTopColor), sc: `set the illustration sub-element border colour to ${toHex(mc.borderTopColor)}` });
            // --- BORDER-RADIUS ---
            const mRad = px(mc.borderTopLeftRadius), aRad = px(ac.borderTopLeftRadius);
            if (mRad != null && aRad != null && !close(aRad, mRad, 2.5)) pushIllo({ loc, sect, class: 'border', property: 'illo-border-radius', target: aRad, reference: mRad, deltaPx: Math.round(Math.abs(aRad - mRad)), sc: `set the illustration sub-element border-radius to ${mRad}px` });
            // --- BOX-SHADOW presence ---
            if (mockHasShadow(mc) !== mockHasShadow(ac)) pushIllo({ loc, sect, class: 'shadow', property: 'illo-box-shadow', target: mockHasShadow(ac) ? 'yes' : 'no', reference: mockHasShadow(mc) ? 'yes' : 'no', sc: mockHasShadow(mc) ? 'add the box-shadow the mock draws on this illustration sub-element' : 'remove the box-shadow from this illustration sub-element' });
            // --- BACKGROUND colour ---
            const mBg = toHex(mc.backgroundColor), aBg = toHex(ac.backgroundColor);
            if (mBg && mBg !== aBg && !(mBg === 'transparent' && aBg === 'transparent')) pushIllo({ loc, sect, class: 'container-bg', property: 'illo-background', target: aBg, reference: mBg, sc: `set the illustration sub-element background to ${mBg}` });
            // --- TEXT colour + LETTER-SPACING + FONT (only when this internal carries its OWN text; style,
            //     not the string — the string is suppressed) ---
            if (norm(ms.text) && norm(as.text)) {
              const mCol = toHex(mc.color), aCol = toHex(ac.color);
              if (mCol && mCol !== 'transparent' && mCol !== aCol) pushIllo({ loc, sect, class: 'font', property: 'illo-color', target: aCol, reference: mCol, sc: `set the illustration label colour to ${mCol}` });
              const mLs = lsPx(mc.letterSpacing), aLs = lsPx(ac.letterSpacing);
              if (mLs != null && aLs != null && !close(aLs, mLs, 0.2)) pushIllo({ loc, sect, class: 'font', property: 'illo-letter-spacing', target: aLs, reference: mLs, deltaPx: +(Math.abs(aLs - mLs)).toFixed(2), sc: `set the illustration label letter-spacing to ${mLs}px (mock ${mLs}px, target ${aLs}px)` });
              // LINE-HEIGHT (v2.4.0) — the illustration STYLE pass had NO line-height comparison, so a row
              // label's line-height drift inside a mockup card went fully unchecked (recall MISS #5). Resolve
              // each side's `normal` to ~1.2×fs, then compare the px VALUE with the same tight tolerance the
              // top-level value-based check uses (~0.6px) so a 0.75px label delta fires.
              {
                const fsM = px(mc.fontSize), fsA = px(ac.fontSize);
                let mLh = px(mc.lineHeight); if (mLh == null && /normal/i.test(String(mc.lineHeight || '')) && fsM != null) mLh = fsM * NORMAL_LH;
                let aLh2 = px(ac.lineHeight); if (aLh2 == null && /normal/i.test(String(ac.lineHeight || '')) && fsA != null) aLh2 = fsA * NORMAL_LH;
                if (mLh != null && aLh2 != null && !close(aLh2, mLh, 0.6)) pushIllo({ loc, sect, class: 'font', property: 'illo-line-height', target: +aLh2.toFixed(2), reference: +mLh.toFixed(2), deltaPx: +(Math.abs(aLh2 - mLh)).toFixed(2), sc: `set the illustration label line-height to ${+mLh.toFixed(2)}px (mock ${+mLh.toFixed(2)}px, target ${+aLh2.toFixed(2)}px)` });
              }
              const mFs = px(mc.fontSize), aFs = px(ac.fontSize);
              if (mFs != null && aFs != null && !close(aFs, mFs, 0.6)) pushIllo({ loc, sect, class: 'font', property: 'illo-font-size', target: aFs, reference: mFs, deltaPx: Math.round(Math.abs(aFs - mFs)), sc: `set the illustration label font-size to ${mFs}px` });
              const mW = parseInt(mc.fontWeight, 10), aW = parseInt(ac.fontWeight, 10);
              if (mW && aW && mW !== aW) pushIllo({ loc, sect, class: 'font', property: 'illo-font-weight', target: aW, reference: mW, sc: `set the illustration label font-weight to ${mW}` });
              const mFam = familyKind(mc.fontFamily), aFam = familyKind(ac.fontFamily);
              if (mFam && aFam && mFam !== aFam) pushIllo({ loc, sect, class: 'font', property: 'illo-font-family-kind', target: aFam, reference: mFam, sc: `switch the illustration label to a ${mFam} typeface` });
            }
            // --- PADDING (left/top) ---
            const mPL = px(mc.paddingLeft), aPL = px(ac.paddingLeft);
            if (mPL != null && aPL != null && !close(aPL, mPL, 2)) pushIllo({ loc, sect, class: 'spacing', property: 'illo-pad-left', target: aPL, reference: mPL, deltaPx: Math.round(Math.abs(aPL - mPL)), sc: `set padding-left: ${mPL}px on this illustration sub-element` });
            const mPT = px(mc.paddingTop), aPT = px(ac.paddingTop);
            if (mPT != null && aPT != null && !close(aPT, mPT, 2)) pushIllo({ loc, sect, class: 'spacing', property: 'illo-pad-top', target: aPT, reference: mPT, deltaPx: Math.round(Math.abs(aPT - mPT)), sc: `set padding-top: ${mPT}px on this illustration sub-element` });
            // --- GEOMETRY (rendered size, same-viewport only) ---
            if (GEOM) {
              if (!close(as.rect.w, ms.rect.w, 6)) pushIllo({ loc, sect, class: 'geometry', property: 'illo-width', target: Math.round(as.rect.w), reference: Math.round(ms.rect.w), deltaPx: Math.round(Math.abs(as.rect.w - ms.rect.w)), sc: `set the illustration sub-element width to ~${Math.round(ms.rect.w)}px` });
              if (!close(as.rect.h, ms.rect.h, 4)) pushIllo({ loc, sect, class: 'geometry', property: 'illo-height', target: Math.round(as.rect.h), reference: Math.round(ms.rect.h), deltaPx: Math.round(Math.abs(as.rect.h - ms.rect.h)), sc: `set the illustration sub-element height to ~${Math.round(ms.rect.h)}px` });
            }
          }
        }
        // DEDUP — a mockup with N identical rows produces N copies of the same (property|target|reference).
        // Emit up to 3 distinct locators per signature + a [×N] summary so a repeated row-style reports once.
        const groups = new Map();
        for (const r of illoRaw) { const k = r.property + '|' + r.class + '|' + String(r.target) + '|' + String(r.reference); if (!groups.has(k)) groups.set(k, []); groups.get(k).push(r); }
        for (const [, g] of groups) {
          g.slice(0, 3).forEach(r => add({ locator: r.loc, section: r.sect, class: r.class, property: r.property, target: r.target, reference: r.reference, ...(r.deltaPx != null ? { deltaPx: r.deltaPx } : {}), suggestedChange: r.sc }));
          if (g.length > 3) add({ locator: `[×${g.length} illustration sub-elements]`, section: g[0].sect, class: g[0].class, property: g[0].property, target: g[0].target, reference: g[0].reference, ...(g[0].deltaPx != null ? { deltaPx: g[0].deltaPx } : {}), suggestedChange: `${g[0].sc} — applies to ${g.length} repeated mockup rows (one root cause)` });
        }
      }
    }

    // ============= v1.16 SHARED CONTAINER PAIRING =============
    function pairContainers(predicate, opts = {}) {
      const { geomFallback = true, appPredicate = predicate } = opts;
      const kidsByParent = arr => { const m = new Map(); for (const n of arr) { if (!m.has(n.parent)) m.set(n.parent, []); m.get(n.parent).push(n); } return m; };
      const mKidsP = kidsByParent(mock), aKidsP = kidsByParent(appAll);
      const pathOf = (nodes, kids, n) => {
        const parts = []; let cur = n, hops = 0;
        while (cur && cur.parent >= 0 && hops++ < 40) { const sibs = kids.get(cur.parent) || []; parts.unshift(`${cur.tag}[${sibs.indexOf(cur)}]`); cur = nodes[cur.parent]; }
        return parts.join('/');
      };
      const geomKey = a => `${Math.round((a.rect?.x || 0) / 8) * 8}|${Math.round((a.rect?.w || 0) / 8) * 8}`;
      const appByPath = new Map(), appByGeom = new Map();
      for (const a of appAll) if (appPredicate(a)) {
        const p = pathOf(appAll, aKidsP, a); if (!appByPath.has(p)) appByPath.set(p, a);
        const k = geomKey(a); if (!appByGeom.has(k)) appByGeom.set(k, []); appByGeom.get(k).push(a);
      }
      const out = [], used = new Set();
      for (const m of mock.filter(predicate)) {
        let a = appByPath.get(pathOf(mock, mKidsP, m));
        if (a && used.has(a.i)) a = null;
        if (!a && geomFallback) {
          const bucket = (appByGeom.get(geomKey(m)) || []).filter(n => !used.has(n.i));
          if (bucket.length) {
            const mYn = (m.rect?.y || 0) / (mockDoc.frame?.h || 1), mH = m.rect?.h || 0;
            const scored = bucket.map(n => {
              const dY = Math.abs((n.rect?.y || 0) / (appDoc.frame?.h || 1) - mYn);
              const dH = Math.abs((n.rect?.h || 0) - mH);
              const hOk = dH <= Math.max(60, 0.4 * mH);
              return { n, dY, hOk, cost: dY + (dH / (mockDoc.frame?.h || 1)) * 0.5 + (n.tag === m.tag ? 0 : 0.005) };
            }).filter(s => s.hOk).sort((x, y) => x.cost - y.cost)[0];
            if (scored && scored.dY <= 0.04) a = scored.n;
          }
        }
        if (a) { used.add(a.i); out.push({ m, a }); }
      }
      return out;
    }
    const clabel = m => locatorFor(m) || `[container ${m.tag}.${(m.cls || '').split(/\s+/)[0]} @y${Math.round(m.rect?.y || 0)} w${Math.round(m.rect?.w || 0)}]`;

    // ---------- (1) LAYOUT STRUCTURE ----------
    {
      const trackSig = gt => {
        if (!gt || gt === 'none') return { n: 0, sig: 'none' };
        let depth = 0, tok = '', toks = [];
        for (const ch of gt) {
          if (ch === '(') { depth++; tok += ch; }
          else if (ch === ')') { depth--; tok += ch; }
          else if (ch === ' ' && depth === 0) { if (tok) toks.push(tok); tok = ''; }
          else tok += ch;
        }
        if (tok) toks.push(tok);
        const bucket = t => {
          if (/fr$/.test(t)) return 'fr';
          if (/auto|min-content|max-content|minmax/.test(t)) return 'flex';
          const v = parseFloat(t); return isNaN(v) ? t : 'p' + Math.round(v / 40);
        };
        return { n: toks.length, sig: toks.map(bucket).join('|') };
      };
      const isFlexGrid = n => /flex|grid/.test(n.comp?.display || '');
      const bigBox = n => { if (!n || n.tag === 'body' || /\b(body|scr|frame|screen)\b/.test(n.cls || '')) return false; const r = n.rect || {}; return (r.w || 0) >= 240 && (r.h || 0) >= 24; };
      const pairs = pairContainers(n => bigBox(n) && isFlexGrid(n), { geomFallback: false, appPredicate: bigBox });
      // FIX 3 — record cross-DOM 'layout' pairing health. PATH-only pairing across the Framer↔StyleX DOMs
      // commonly pairs 0 of N wide flex/grid containers (their structural paths don't align); rather than
      // letting that surface as silent under-coverage, log the unpaired count to noiseExcluded so a
      // consumer can see the layout class is structurally unreliable for this pair and inspect by eye.
      {
        const candCount = mock.filter(n => bigBox(n) && isFlexGrid(n)).length;
        if (candCount > 0 && pairs.length < candCount) noiseExcluded.crossDomStructure.push({ detector: 'layout', candidates: candCount, paired: pairs.length, unpaired: candCount - pairs.length });
      }
      for (const { m, a } of pairs) {
        let mc = m.comp || {}, ac = a.comp || {}; const lbl = clabel(m); const sect = sectionFor(m, mockLeads);
        let mDisp = mc.display, aDisp = ac.display;
        // ---- CLASS-SIGNATURE REPAIR (a compound-defect correction, measured 18 Aug 2026) ----
        // The path pairing above is deliberately geometry-fallback-FREE (#23) so a swarm of same-width
        // wrappers cannot mispair into contradictory flips. That guard is right, and it has a cost this
        // detector was silently paying: an ABSENT sibling EARLIER in the tree shifts every later sibling
        // index, so a container path-pairs to a DIFFERENT element and the layout class reports the wrong
        // property. Measured on a fixture carrying a removed card AND a flex-direction flip: in isolation
        // the flip reported `flex-direction column vs row`; with the removal also present it reported
        // `display block vs flex` on the same locator — the right element, the wrong reason, and a reader
        // who "fixes the display" changes nothing.
        //
        // A display disagreement between two path-paired containers is itself the mispair TELL: authors
        // very rarely write `display:block` where the reference has `display:flex` on the same component
        // without it being a wholly different element. So on that signal alone, look for the app-side
        // container whose CLASS SIGNATURE matches the mock's. Repair only on a UNIQUE match whose display
        // agrees — uniqueness is what preserves #23's protection, because a wrapper swarm has repeated
        // signatures and therefore declines the repair rather than guessing.
        let repairedFrom = null;
        if (mDisp !== aDisp && m.cls) {
          const sig = String(m.cls).trim().split(/\s+/).sort().join(' ');
          const sigOf = n => String(n.cls || '').trim().split(/\s+/).sort().join(' ');
          const cands = app.filter(n => bigBox(n) && sigOf(n) === sig && (n.comp || {}).display === mDisp);
          if (cands.length === 1) {
            repairedFrom = aDisp;
            ac = cands[0].comp || {}; aDisp = ac.display;
          }
        }
        if (mDisp !== aDisp) add({ locator: lbl, section: sect, class: 'layout', property: 'display', target: aDisp, reference: mDisp, suggestedChange: `change display ${aDisp}→${mDisp} on this container` });
        else if (repairedFrom) add({
          locator: lbl, section: sect, class: 'layout', property: 'container-pairing-repaired',
          target: `path pairing landed on a display:${repairedFrom} element`, reference: `display:${mDisp} with class "${m.cls}"`,
          severity: 'low',
          suggestedChange: `the structural path pairing for this container shifted — almost always because an element EARLIER in the tree is absent on the target, which renumbers every later sibling. It was re-paired by class signature, so the layout properties below are compared against the right element. Resolve the earlier ABSENT finding first, then re-run: a path shift can hide layout defects on everything after it.`,
        });
        if (/flex/.test(mDisp || '')) {
          if ((mc.flexDirection || 'row') !== (ac.flexDirection || 'row')) add({ locator: lbl, section: sect, class: 'layout', property: 'flex-direction', target: ac.flexDirection, reference: mc.flexDirection, suggestedChange: `change flex-direction ${ac.flexDirection || 'row'}→${mc.flexDirection || 'row'} (icon/label stacking)` });
          if ((mc.flexWrap || 'nowrap') !== (ac.flexWrap || 'nowrap')) add({ locator: lbl, section: sect, class: 'layout', property: 'flex-wrap', target: ac.flexWrap, reference: mc.flexWrap, suggestedChange: `change flex-wrap ${ac.flexWrap || 'nowrap'}→${mc.flexWrap || 'nowrap'}` });
        }
        if (/flex|grid/.test(mDisp || '') && /flex|grid/.test(aDisp || '')) {
          if ((mc.justifyContent || 'normal') !== (ac.justifyContent || 'normal')) add({ locator: lbl, section: sect, class: 'layout', property: 'justify-content', target: ac.justifyContent, reference: mc.justifyContent, suggestedChange: `change justify-content ${ac.justifyContent}→${mc.justifyContent}` });
          if ((mc.alignItems || 'normal') !== (ac.alignItems || 'normal')) add({ locator: lbl, section: sect, class: 'layout', property: 'align-items', target: ac.alignItems, reference: mc.alignItems, suggestedChange: `change align-items ${ac.alignItems}→${mc.alignItems}` });
          const mRg = px(mc.rowGap), aRg = px(ac.rowGap); if (mRg != null && aRg != null && !close(mRg, aRg, 3)) add({ locator: lbl, section: sect, class: 'layout', property: 'row-gap', target: aRg, reference: mRg, deltaPx: Math.round(Math.abs(mRg - aRg)), suggestedChange: `set row-gap: ${mRg}px` });
          const mCg = px(mc.columnGap), aCg = px(ac.columnGap); if (mCg != null && aCg != null && !close(mCg, aCg, 3)) add({ locator: lbl, section: sect, class: 'layout', property: 'column-gap', target: aCg, reference: mCg, deltaPx: Math.round(Math.abs(mCg - aCg)), suggestedChange: `set column-gap: ${mCg}px` });
        }
        if (/grid/.test(mDisp || '')) {
          const mt = trackSig(mc.gridTemplateColumns), at = trackSig(ac.gridTemplateColumns);
          if (mt.n !== at.n) add({ locator: lbl, section: sect, class: 'layout', property: 'grid-columns', target: at.n, reference: mt.n, suggestedChange: `change grid-template-columns to ${mt.n} tracks (currently ${at.n})` });
          else if (mt.sig !== at.sig) add({ locator: lbl, section: sect, class: 'layout', property: 'grid-col-ratio', target: at.sig, reference: mt.sig, suggestedChange: `change grid column ratio ${at.sig}→${mt.sig}` });
          const mtr = trackSig(mc.gridTemplateRows), atr = trackSig(ac.gridTemplateRows);
          if (mtr.n !== atr.n && (mtr.n > 1 || atr.n > 1)) add({ locator: lbl, section: sect, class: 'layout', property: 'grid-rows', target: atr.n, reference: mtr.n, suggestedChange: `change grid-template-rows to ${mtr.n} tracks` });
          if ((mc.gridAutoFlow || 'row') !== (ac.gridAutoFlow || 'row')) add({ locator: lbl, section: sect, class: 'layout', property: 'grid-auto-flow', target: ac.gridAutoFlow, reference: mc.gridAutoFlow, suggestedChange: `change grid-auto-flow ${ac.gridAutoFlow || 'row'}→${mc.gridAutoFlow || 'row'}` });
        }
      }
    }

    // ---------- (2) VERTICAL RHYTHM / CUMULATIVE DRIFT ----------
    if (GEOM) {
      const mH = mockDoc.frame?.contentH || mockDoc.frame?.h, aH = appDoc.frame?.contentH || appDoc.frame?.h;
      if (mH && aH && Math.abs(aH - mH) > 6) add({ locator: '[frame]', section: null, class: 'rhythm', property: 'doc-height', target: Math.round(aH), reference: Math.round(mH), deltaPx: Math.round(Math.abs(aH - mH)), suggestedChange: `total document height differs by ${Math.round(Math.abs(aH - mH))}px — close the per-section vertical-rhythm gaps below` });
      const headingish = n => {
        const t = norm(n.text); if (!t || t.length < 3 || t.length > 60) return false;
        if (CHROME_TXT.test(t)) return false;
        const sz = px(n.comp?.fontSize) || 0;
        const eyebrow = /^[A-Z0-9 ·&,'’\-]+$/.test(t) && t.length <= 40;
        return sz >= 18 || eyebrow;
      };
      const uniqByText = nodes => { const seen = new Map(), dup = new Set(); for (const n of nodes) { if (!headingish(n)) continue; const t = norm(n.text); if (seen.has(t)) dup.add(t); else seen.set(t, n); } for (const t of dup) seen.delete(t); return seen; };
      const mAnchors = uniqByText(mock), aAnchors = uniqByText(app);
      const common = [...mAnchors.keys()].filter(t => aAnchors.has(t))
        .map(t => ({ t, m: mAnchors.get(t), a: aAnchors.get(t) }))
        .sort((x, y) => (x.m.rect?.y || 0) - (y.m.rect?.y || 0));
      if (common.length >= 2) {
        let prevMy = null, prevAy = null, drifted = [];
        for (const c of common) {
          const my = c.m.rect?.y || 0, ay = c.a.rect?.y || 0;
          if (prevMy != null) { const dGap = (ay - prevAy) - (my - prevMy); if (Math.abs(dGap) > 12) drifted.push({ t: c.t, dGap }); }
          prevMy = my; prevAy = ay;
        }
        const last = common[common.length - 1];
        const cumTop = (last.a.rect?.y || 0) - (last.m.rect?.y || 0);
        if (Math.abs(cumTop) > 12) {
          const contrib = drifted.sort((a, b) => Math.abs(b.dGap) - Math.abs(a.dGap)).slice(0, 6).map(d => `"${d.t.slice(0, 16)}":${d.dGap > 0 ? '+' : ''}${Math.round(d.dGap)}`).join('  ');
          add({ locator: '[page]', section: null, class: 'rhythm', property: 'cumulative-top-drift', target: Math.round(cumTop), reference: 0, deltaPx: Math.abs(Math.round(cumTop)), suggestedChange: `the page accumulates ${Math.round(cumTop)}px of vertical drift; top gap contributors: ${contrib || '(none > 12px)'} — adjust those sections' top spacing` });
        }
      }
    }

    // ---------- (3) VALUE-PRECISION ----------
    {
      const parseShadow = s => {
        if (!s || s === 'none') return null;
        const layer = s.split(/,(?![^(]*\))/)[0].trim();
        const colorM = layer.match(/rgba?\([^)]+\)|#[0-9a-f]+/i);
        const color = colorM ? toHex(colorM[0]) : null;
        const nums = (colorM ? layer.replace(colorM[0], '') : layer).match(/-?[\d.]+px/g) || [];
        const [dx, dy, blur, spread] = nums.map(parseFloat);
        return { dx: dx || 0, dy: dy || 0, blur: blur || 0, spread: spread || 0, color };
      };
      const rgbOf = h => { if (!h || h === 'transparent') return null; const m = h.match(/^#([0-9a-f]{6})$/i); if (!m) return null; const x = m[1]; return [0, 2, 4].map(i => parseInt(x.slice(i, i + 2), 16)); };
      const colorDelta = (a, b) => { const ra = rgbOf(a), rb = rgbOf(b); if (!ra || !rb) return a === b ? 0 : 999; return Math.max(...ra.map((v, i) => Math.abs(v - rb[i]))); };
      const gradSig = g => {
        if (!g || g === 'none' || !/gradient/i.test(g)) return null;
        const fn = (g.match(/(repeating-)?(linear|radial|conic)-gradient/i) || [''])[0].toLowerCase();
        const angle = (g.match(/(\d+)deg/) || [, null])[1];
        const stops = (g.match(/rgba?\([^)]+\)|#[0-9a-f]{3,8}/gi) || []).map(toHex);
        return { fn, angle, n: stops.length, stops: stops.join('>') };
      };
      const styled = n => {
        if (!n || n.tag === 'body' || /\b(body|scr|frame|screen)\b/.test(n.cls || '')) return false;
        const c = n.comp || {}, r = n.rect || {};
        if ((r.w || 0) < 24 || (r.h || 0) < 8) return false;
        const hasShadow = c.boxShadow && c.boxShadow !== 'none';
        const hasGrad = c.backgroundImage && /gradient/i.test(c.backgroundImage);
        const hasRadius = (px(c.borderTopLeftRadius) || 0) >= 2;
        const hasBg = toHex(c.backgroundColor) !== 'transparent' && c.backgroundColor;
        return !!(hasShadow || hasGrad || hasRadius || hasBg);
      };
      const anyBox = n => { if (!n || n.tag === 'body' || /\b(body|scr|frame|screen)\b/.test(n.cls || '')) return false; const r = n.rect || {}; return (r.w || 0) >= 24 && (r.h || 0) >= 8; };
      for (const { m, a } of pairContainers(styled, { appPredicate: anyBox })) {
        const mc = m.comp || {}, ac = a.comp || {}; const lbl = clabel(m); const sect = sectionFor(m, mockLeads);
        const ms = parseShadow(mc.boxShadow), as = parseShadow(ac.boxShadow);
        if (ms && as) {
          const geomOff = Math.abs(ms.dx - as.dx) > 1.5 || Math.abs(ms.dy - as.dy) > 1.5 || Math.abs(ms.blur - as.blur) > 2 || Math.abs(ms.spread - as.spread) > 1.5;
          const colOff = ms.color && as.color && colorDelta(ms.color, as.color) > 24;
          if (geomOff || colOff) add({ locator: lbl, section: sect, class: 'shadow', property: 'shadow-value', target: `${as.dx},${as.dy},${as.blur},${as.spread} ${as.color || ''}`, reference: `${ms.dx},${ms.dy},${ms.blur},${ms.spread} ${ms.color || ''}`, suggestedChange: `set box-shadow to ${ms.dx}px ${ms.dy}px ${ms.blur}px ${ms.spread}px ${ms.color || ''}` });
        }
        const mg = gradSig(mc.backgroundImage), ag = gradSig(ac.backgroundImage);
        if (mg && ag) {
          if (mg.fn !== ag.fn) add({ locator: lbl, section: sect, class: 'gradient', property: 'gradient-type', target: ag.fn, reference: mg.fn, suggestedChange: `change gradient type to ${mg.fn}` });
          else if (mg.n !== ag.n) add({ locator: lbl, section: sect, class: 'gradient', property: 'gradient-stops', target: ag.n, reference: mg.n, suggestedChange: `use ${mg.n} gradient stops (currently ${ag.n})` });
          else if (mg.stops !== ag.stops) add({ locator: lbl, section: sect, class: 'gradient', property: 'gradient-colors', target: ag.stops, reference: mg.stops, suggestedChange: `set gradient stop colours to ${mg.stops}` });
          else if (mg.angle != null && ag.angle != null && Math.abs(+mg.angle - +ag.angle) > 3) add({ locator: lbl, section: sect, class: 'gradient', property: 'gradient-angle', target: ag.angle + 'deg', reference: mg.angle + 'deg', suggestedChange: `set gradient angle to ${mg.angle}deg` });
        } else if (mg && !ag) add({ locator: lbl, section: sect, class: 'gradient', property: 'gradient-present', target: 'none', reference: mg.fn, severity: 'high', suggestedChange: `add the ${mg.fn} background the mock has (target has none)` });
        const mBg = toHex(mc.backgroundColor), aBg = toHex(ac.backgroundColor);
        if (mBg !== 'transparent' && aBg !== 'transparent' && mBg !== aBg && colorDelta(mBg, aBg) > 12) add({ locator: lbl, section: sect, class: 'value', property: 'bg-color-precise', target: aBg, reference: mBg, suggestedChange: `set background-color to ${mBg} (currently ${aBg})` });
        if ((px(mc.borderTopWidth) || 0) > 0 && (px(ac.borderTopWidth) || 0) > 0) {
          const mBc = toHex(mc.borderTopColor), aBc = toHex(ac.borderTopColor);
          if (mBc !== aBc && colorDelta(mBc, aBc) > 12) add({ locator: lbl, section: sect, class: 'value', property: 'border-color-precise', target: aBc, reference: mBc, suggestedChange: `set border color to ${mBc}` });
        }
        const corners = c => ['borderTopLeftRadius', 'borderTopRightRadius', 'borderBottomLeftRadius', 'borderBottomRightRadius'].map(k => Math.round(px(c[k]) || 0));
        const mCr = corners(mc), aCr = corners(ac);
        if (mCr.some((v, i) => Math.abs(v - aCr[i]) > 2.5) && (mCr.some(v => v > 0) || aCr.some(v => v > 0))) add({ locator: lbl, section: sect, class: 'value', property: 'radius-corners', target: `[${aCr}]`, reference: `[${mCr}]`, suggestedChange: `set the 4-corner border-radius to [${mCr}]px (TL,TR,BL,BR)` });
      }
    }

    // ---------- (4) TRANSFORM / OPACITY / FILTER ----------
    {
      const decompose = t => {
        if (!t || t === 'none') return { scale: 1, rot: 0, tx: 0, ty: 0, id: true };
        const m2 = t.match(/^matrix\(([^)]+)\)/);
        if (m2) {
          const [a, b, c, d, e, fv] = m2[1].split(',').map(parseFloat);
          const scale = +Math.hypot(a, b).toFixed(3);
          const rot = +(Math.atan2(b, a) * 180 / Math.PI).toFixed(1);
          const id = Math.abs(scale - 1) < 0.01 && Math.abs(rot) < 0.5 && Math.abs(e) < 0.5 && Math.abs(fv) < 0.5;
          return { scale, rot, tx: +e.toFixed(1), ty: +fv.toFixed(1), id };
        }
        return { scale: 1, rot: 0, tx: 0, ty: 0, id: false, raw: t.slice(0, 30) };
      };
      const sized = n => { const r = n.rect || {}; return n.comp && (r.w || 0) >= 16 && (r.h || 0) >= 8 && n.tag !== 'body' && !/\b(body|scr|frame|screen)\b/.test(n.cls || ''); };
      const motionMock = n => sized(n) && ((n.comp.transform && n.comp.transform !== 'none') || (n.comp.filter && n.comp.filter !== 'none') || (parseFloat(n.comp.opacity ?? '1') < 0.99));
      for (const { m, a } of pairContainers(motionMock, { appPredicate: sized })) {
        const mc = m.comp || {}, ac = a.comp || {}; const lbl = clabel(m); const sect = sectionFor(m, mockLeads);
        const mt = decompose(mc.transform), at = decompose(ac.transform);
        if (!(mt.id && at.id)) {
          if (Math.abs(mt.scale - at.scale) > 0.02) add({ locator: lbl, section: sect, class: 'transform', property: 'transform-scale', target: at.scale, reference: mt.scale, suggestedChange: `set transform scale to ${mt.scale}` });
          else if (Math.abs(mt.rot - at.rot) > 1) add({ locator: lbl, section: sect, class: 'transform', property: 'transform-rotate', target: at.rot + '°', reference: mt.rot + '°', suggestedChange: `set transform rotate to ${mt.rot}deg` });
          else if (Math.abs(mt.tx - at.tx) > 2 || Math.abs(mt.ty - at.ty) > 2) add({ locator: lbl, section: sect, class: 'transform', property: 'transform-translate', target: `${at.tx},${at.ty}`, reference: `${mt.tx},${mt.ty}`, suggestedChange: `set transform translate to (${mt.tx}px, ${mt.ty}px) — check the centring technique` });
          else if (mt.raw || at.raw) add({ locator: lbl, section: sect, class: 'transform', property: 'transform', target: at.raw || ac.transform || 'none', reference: mt.raw || mc.transform || 'none', suggestedChange: `match the transform: ${mt.raw || mc.transform || 'none'}` });
        }
        const mo = parseFloat(mc.opacity ?? '1'), ao = parseFloat(ac.opacity ?? '1');
        if (!isNaN(mo) && !isNaN(ao) && Math.abs(mo - ao) > 0.05 && (mo < 0.99 || ao < 0.99)) add({ locator: lbl, section: sect, class: 'transform', property: 'opacity', target: +ao.toFixed(2), reference: +mo.toFixed(2), suggestedChange: `set opacity to ${+mo.toFixed(2)}` });
        const mf = (mc.filter && mc.filter !== 'none') ? mc.filter.slice(0, 40) : 'none';
        const af = (ac.filter && ac.filter !== 'none') ? ac.filter.slice(0, 40) : 'none';
        if (mf !== af) add({ locator: lbl, section: sect, class: 'transform', property: 'filter', target: af, reference: mf, suggestedChange: `set filter to ${mf}` });
      }
    }

    // ---------- (5) PSEUDO-ELEMENT CONTENT ----------
    {
      const appWithPseudo = appAll.filter(n => n.pseudoContent);
      const byText = new Map();
      for (const n of appWithPseudo) { const t = A.text(n); if (!t) continue; if (!byText.has(t)) byText.set(t, []); byText.get(t).push(n); }
      const used = new Set();
      const pRows = [];
      for (const m of mock) {
        if (!m.pseudoContent) continue;
        const mt = norm(m.text);
        let a = null;
        if (mt) { const cands = (byText.get(mt) || []).filter(n => !used.has(n.i) && n.tag === m.tag); a = cands.sort((x, y) => Math.abs((x.rect?.y || 0) - (m.rect?.y || 0)) - Math.abs((y.rect?.y || 0) - (m.rect?.y || 0)))[0]; }
        if (!a) { const cands = appWithPseudo.filter(n => !used.has(n.i) && n.tag === m.tag && Math.abs((n.rect?.x || 0) - (m.rect?.x || 0)) < 24); a = cands.sort((x, y) => Math.abs((x.rect?.y || 0) - (m.rect?.y || 0)) - Math.abs((y.rect?.y || 0) - (m.rect?.y || 0)))[0]; }
        const lbl = `["${mt.slice(0, 24) || m.tag}" pseudo]`;
        const sect = sectionFor(m, mockLeads);
        for (const ps of ['::before', '::after']) {
          const mp = m.pseudoContent[ps]; if (!mp) continue;
          const ap = a && a.pseudoContent && a.pseudoContent[ps];
          if (!ap) pRows.push({ lbl, sect, prop: `${ps}-content`, target: 'none', reference: mp.content, dk: `${ps}|none|${mp.content}|${m.tag}`, sc: `add the ${ps} { content: "${mp.content}" } marker the mock has` });
          else {
            if (a) used.add(a.i);
            if (mp.content !== ap.content) pRows.push({ lbl, sect, prop: `${ps}-content`, target: ap.content, reference: mp.content, dk: `${ps}|${ap.content}|${mp.content}|${m.tag}`, sc: `set ${ps} content to "${mp.content}"` });
            else {
              const mFs = px(mp.fontSize), aFs = px(ap.fontSize);
              if (mFs != null && aFs != null && !close(mFs, aFs, 1)) pRows.push({ lbl, sect, prop: `${ps}-content-size`, target: aFs, reference: mFs, dk: `${ps}|sz|${aFs}|${mFs}`, sc: `set ${ps} content font-size to ${mFs}px` });
              else if (toHex(mp.color) !== toHex(ap.color)) pRows.push({ lbl, sect, prop: `${ps}-content-color`, target: toHex(ap.color), reference: toHex(mp.color), dk: `${ps}|col|${toHex(ap.color)}|${toHex(mp.color)}`, sc: `set ${ps} content color to ${toHex(mp.color)}` });
            }
          }
        }
      }
      // DEDUP: collapse a repeating identical marker defect → 3 instances + one summary count.
      const groups = new Map();
      for (const r of pRows) { if (!groups.has(r.dk)) groups.set(r.dk, []); groups.get(r.dk).push(r); }
      for (const [, g] of groups) {
        g.slice(0, 3).forEach(r => add({ locator: r.lbl, section: r.sect, class: 'pseudo', property: r.prop, target: r.target, reference: r.reference, suggestedChange: r.sc }));
        if (g.length > 3) add({ locator: `[×${g.length} elements]`, section: g[0].sect, class: 'pseudo', property: g[0].prop, target: g[0].target, reference: g[0].reference, suggestedChange: `${g[0].sc} — applies to ${g.length} elements (one root cause)` });
      }
    }

    // ---------- (6) ANIMATION / TRANSITION PRESENCE ----------
    {
      const hasTransition = c => { const p = c?.transitionProperty, d = px(c?.transitionDuration); return !!(p && p !== 'none' && p !== 'all 0s' && d && d > 0); };
      const sized = n => { const r = n.rect || {}; return n.comp && (r.w || 0) >= 24 && (r.h || 0) >= 8 && n.tag !== 'body' && !/\b(body|scr|frame|screen)\b/.test(n.cls || ''); };
      const animRows = [], transRows = [];
      for (const { m, a } of pairContainers(n => sized(n) && ((n.anims || 0) > 0 || hasTransition(n.comp)), { appPredicate: sized })) {
        const mc = m.comp || {}, ac = a.comp || {}; const lbl = clabel(m); const sect = sectionFor(m, mockLeads);
        const mAnim = m.anims || 0, aAnim = a.anims || 0;
        if ((mAnim > 0) !== (aAnim > 0)) animRows.push({ lbl, sect, a: aAnim, m: mAnim });
        const mT = hasTransition(mc), aT = hasTransition(ac);
        if (mT !== aT) transRows.push({ lbl, sect, a: aT ? (ac.transitionProperty || '').slice(0, 24) : 'none', m: mT ? (mc.transitionProperty || '').slice(0, 24) : 'none' });
      }
      const emitCapped = (rows, prop, mk) => {
        rows.slice(0, 6).forEach(r => add({ locator: r.lbl, section: r.sect, class: 'animation', property: prop, target: r.a, reference: r.m, suggestedChange: mk(r) }));
        if (rows.length > 6) add({ locator: '[summary]', section: null, class: 'animation', property: prop, target: `${rows.length} elements differ`, reference: '(motion present on one side only)', suggestedChange: `${rows.length} elements differ in ${prop} — apply the mock's motion to this group` });
      };
      emitCapped(animRows, 'animation-presence', r => r.m > 0 ? `add the running animation the mock element has` : `remove the animation — the mock element is static`);
      emitCapped(transRows, 'transition-presence', r => r.m !== 'none' ? `add the CSS transition (${r.m}) the mock element has` : `remove the transition — the mock element has none`);
    }

    // ============= INTERACTION STATES (:hover / :focus / :focus-visible / :active) =============
    // For every interactive mock element that declares a state override, pair it to the target
    // element and diff the override-set per state. An element with `istates.states === 'unreadable'`
    // on EITHER side cannot be compared (cross-origin Framer sheet) — surface that honestly, once.
    {
      const hasStates = n => n && n.istates && n.istates.states && typeof n.istates.states === 'object';
      const isUnreadable = n => n && n.istates && n.istates.states === 'unreadable';
      const mockInteractive = mock.filter(n => n.istates); // captured only for interactive nodes
      const appInteractive = app.filter(n => n.istates);
      // pairing: text+tag first, then nearest-geometry within same tag.
      const appByTextTag = new Map();
      for (const a of appInteractive) { const k = a.tag + '|' + A.text(a); if (!appByTextTag.has(k)) appByTextTag.set(k, []); appByTextTag.get(k).push(a); }
      const iUsed = new Set();
      const VISUAL_KEYS = ['background-color', 'color', 'border-top-color', 'border-bottom-color', 'box-shadow', 'outline-width', 'outline-color', 'outline-style', 'opacity', 'transform', 'text-decoration-line', 'text-decoration', 'filter'];
      // normalise a declaration value for comparison (colours → hex, px numbers rounded)
      const normDecl = (prop, v) => {
        if (v == null) return null;
        if (/color/.test(prop)) return toHex(v);
        const s = String(v).trim().toLowerCase();
        if (s === 'none' || s === 'normal' || s === '') return 'none';
        return s.replace(/\s+/g, ' ');
      };
      const STATE_PRIORITY = ['hover', 'focus-visible', 'focus', 'active'];
      let unreadableReported = false;
      const interactionRows = [];
      for (const m of mockInteractive) {
        const mt = A.text(m);
        let a = null;
        const cands = (appByTextTag.get(m.tag + '|' + mt) || []).filter(n => !iUsed.has(n.i));
        if (cands.length) {
          if (cands.length === 1) a = cands[0];
          else {
            const myN = (m.rect?.y || 0) / (mockDoc.frame?.h || 1);
            a = cands.map(n => ({ n, d: Math.abs((n.rect?.y || 0) / (appDoc.frame?.h || 1) - myN) })).sort((x, y) => x.d - y.d)[0].n;
          }
        }
        if (!a) {
          // geometry fallback within same tag (a button with no stable text, e.g. icon-only)
          const geo = appInteractive.filter(n => !iUsed.has(n.i) && n.tag === m.tag && close(n.rect?.x, m.rect?.x, 24) && close(n.rect?.w, m.rect?.w, 40));
          if (geo.length) { const myN = (m.rect?.y || 0) / (mockDoc.frame?.h || 1); a = geo.map(n => ({ n, d: Math.abs((n.rect?.y || 0) / (appDoc.frame?.h || 1) - myN) })).sort((x, y) => x.d - y.d)[0].n; }
        }
        if (!a) continue;
        iUsed.add(a.i);
        const loc = locatorFor(a);
        const sect = sectionFor(a, appLeads);
        const el = mt ? `"${mt.slice(0, 32)}"` : `<${m.tag}>`;
        // cross-origin unreadable on either side → one honest finding, then stop comparing states.
        if (isUnreadable(m) || isUnreadable(a)) {
          if (!unreadableReported) {
            unreadableReported = true;
            const which = isUnreadable(m) && isUnreadable(a) ? 'both sides' : (isUnreadable(m) ? 'the reference' : 'the target');
            add({ locator: loc, section: sect, class: 'interaction', property: 'states-unreadable', target: isUnreadable(a) ? 'cross-origin unreadable' : 'readable', reference: isUnreadable(m) ? 'cross-origin unreadable' : 'readable', severity: 'low', suggestedChange: `interaction-state CSS is cross-origin unreadable on ${which} (e.g. a Framer CDN stylesheet) — :hover/:focus overrides cannot be diffed mechanically; verify hover/focus by eye, or host the reference same-origin to compare` });
          }
          continue;
        }
        if (!hasStates(m)) continue;
        const mStates = m.istates.states, aStates = (hasStates(a) ? a.istates.states : {});
        for (const st of STATE_PRIORITY) {
          const mSet = mStates[st];
          if (!mSet) continue; // mock has no override for this state → nothing required
          const aSet = aStates[st] || null;
          if (!aSet) {
            // mock has a state effect the target wholly lacks — summarise the effect.
            const effect = VISUAL_KEYS.filter(k => mSet[k] != null && normDecl(k, mSet[k]) !== 'none').map(k => `${k}:${mSet[k]}`).slice(0, 4).join('; ');
            interactionRows.push({ loc, sect, prop: `${st}-state`, target: 'no override', reference: effect || `:${st} effect`, sc: `add the :${st} state on ${el} (mock sets ${effect || 'visual changes'}; target has no :${st} override)`, dk: `${st}|absent|${m.tag}` });
            continue;
          }
          // both sides have a :state override — diff each visual property.
          for (const k of VISUAL_KEYS) {
            const mv = normDecl(k, mSet[k]), av = normDecl(k, aSet[k]);
            if (mSet[k] == null && aSet[k] == null) continue;
            if (mv === av) continue;
            const propName = st + '-' + (k === 'background-color' ? 'bg' : k === 'outline-width' || k === 'outline-color' || k === 'outline-style' ? 'outline' : k.replace('text-decoration-line', 'underline').replace('text-decoration', 'underline'));
            interactionRows.push({ loc, sect, prop: propName, target: aSet[k] ?? 'none', reference: mSet[k] ?? 'none', sc: `on :${st} of ${el}, set ${k} to ${mSet[k] ?? 'none'} (target: ${aSet[k] ?? 'none'})`, dk: `${st}|${k}|${m.tag}` });
          }
        }
      }
      // DEDUP a repeating identical interaction defect (every nav link missing the same hover) →
      // 3 rows + one [×N] summary, keeping the noise controlled.
      const igroups = new Map();
      for (const r of interactionRows) { if (!igroups.has(r.dk)) igroups.set(r.dk, []); igroups.get(r.dk).push(r); }
      for (const [, g] of igroups) {
        g.slice(0, 3).forEach(r => add({ locator: r.loc, section: r.sect, class: 'interaction', property: r.prop, target: r.target, reference: r.reference, suggestedChange: r.sc }));
        if (g.length > 3) add({ locator: `[×${g.length} elements]`, section: g[0].sect, class: 'interaction', property: g[0].prop, target: g[0].target, reference: g[0].reference, suggestedChange: `${g[0].sc} — applies to ${g.length} elements (one root cause)` });
      }
    }

    // ============= STRUCTURE-DIFF PASS (layout/child-count/missing/extra) =============
    {
      const childrenOf = (nodes, i) => nodes.filter((n) => n.parent === i);
      const sigText = n => norm(n.text).slice(0, 60);
      const pathOf = (nodes, n) => {
        const parts = []; let cur = n;
        while (cur && cur.parent !== -1) { const sibs = childrenOf(nodes, cur.parent); parts.unshift(`${cur.tag}[${sibs.indexOf(cur)}]`); cur = nodes[cur.parent]; }
        return parts.join('/');
      };
      function buildMatch(mockNodes, appNodes) {
        const pairs = new Map(); const usedApp = new Set();
        const take = (mn, an) => { if (an && !usedApp.has(an.i)) { pairs.set(mn.i, an); usedApp.add(an.i); return true; } return false; };
        const appByFid = new Map();
        for (const a of appNodes) if (a.fid) appByFid.set(a.fid, a);
        for (const m of mockNodes) if (m.fid && appByFid.has(m.fid)) take(m, appByFid.get(m.fid));
        // (1) same tag + same normalised text
        const appByText = new Map();
        for (const a of appNodes) { const t = sigText(a); if (t.length < 2) continue; const k = a.tag + '|' + t; if (!appByText.has(k)) appByText.set(k, []); appByText.get(k).push(a); }
        for (const m of mockNodes) { if (pairs.has(m.i)) continue; const t = sigText(m); if (t.length < 2) continue; const cands = appByText.get(m.tag + '|' + t) || []; take(m, cands.find((a) => !usedApp.has(a.i))); }
        // (2) structural path
        const appByPath = new Map();
        for (const a of appNodes) appByPath.set(pathOf(appNodes, a), a);
        for (const m of mockNodes) { if (pairs.has(m.i)) continue; take(m, appByPath.get(pathOf(mockNodes, m))); }
        // (3) FIX 3 — NORMALISED-TEXT fallback pairing IGNORING TAG, by nearest normalised-Y.
        // The Framer↔StyleX DOMs frequently render the SAME text under a different tag / at a different
        // structural path (an <h2> vs a <div>, a <a> nav link vs a <span>), so the same string was being
        // reported as BOTH missing (mock) AND extra (target) — a phantom. Here we pair any still-unpaired
        // mock text node to an unused app node carrying the SAME normalised text (any tag), choosing the
        // nearest by frame-height-normalised Y so page drift cancels. This is a CONFIDENT pairing (exact
        // text match) — it just relaxes the tag/path constraint.
        const appTextAnyTag = new Map();
        for (const a of appNodes) { if (usedApp.has(a.i)) continue; const t = sigText(a); if (t.length < 2) continue; if (!appTextAnyTag.has(t)) appTextAnyTag.set(t, []); appTextAnyTag.get(t).push(a); }
        const mockFrameH = mockDoc.frame?.h || 1, appFrameH = appDoc.frame?.h || 1;
        for (const m of mockNodes) {
          if (pairs.has(m.i)) continue;
          const t = sigText(m); if (t.length < 2) continue;
          const cands = (appTextAnyTag.get(t) || []).filter(a => !usedApp.has(a.i));
          if (!cands.length) continue;
          const myN = (m.rect?.y || 0) / mockFrameH;
          const best = cands.map(a => ({ a, d: Math.abs((a.rect?.y || 0) / appFrameH - myN) })).sort((x, y) => x.d - y.d)[0];
          if (best) take(m, best.a);
        }
        return { pairs, usedApp };
      }
      function isVisual(n) {
        if (['svg', 'img', 'hr', 'path'].includes(n.tag)) return true;
        const c = n.comp || {};
        const hasBg = c.backgroundColor && c.backgroundColor !== 'rgba(0, 0, 0, 0)' && c.backgroundColor !== 'transparent';
        const hasBorder = c.borderTopWidth && parseFloat(c.borderTopWidth) > 0;
        const small = n.rect && n.rect.w <= 80 && n.rect.h <= 80;
        return (hasBg || hasBorder) && small && !sigText(n);
      }
      function visualKind(n) {
        if (['svg', 'path', 'img'].includes(n.tag)) return 'icon/image';
        if (n.tag === 'hr') return 'divider';
        if (isVisual(n)) return 'icon/tile/dot';
        return 'text';
      }
      function colCount(gtc) {
        if (!gtc || gtc === 'none') return null;
        let depth = 0, count = 0, inTok = false;
        for (const ch of gtc) {
          if (ch === '(') depth++; else if (ch === ')') depth--;
          else if (ch === ' ' && depth === 0) inTok = false;
          else if (depth === 0 && !inTok) { inTok = true; count++; }
        }
        return count || null;
      }
      const { pairs, usedApp } = buildMatch(mock, appAll);
      const LAYOUT_PROPS = ['display', 'flexDirection', 'gridTemplateColumns', 'flexWrap', 'gap', 'columnGap', 'rowGap', 'justifyContent', 'alignItems'];
      const childCountSeen = new Set();
      for (const m of mock) {
        const a = pairs.get(m.i);
        if (!a) continue;
        const mc = m.comp || {}, ac = a.comp || {};
        const sect = sectionFor(m, mockLeads);
        for (const p of LAYOUT_PROPS) {
          let mv = mc[p], av = ac[p];
          if (p === 'gridTemplateColumns') { const mn = colCount(mv), an = colCount(av); if (mn !== an && (mn || an)) add({ locator: clabel(m), section: sect, class: 'structure', property: 'grid-columns', target: an ?? '—', reference: mn ?? '—', suggestedChange: `render this grid with ${mn ?? '—'} columns (currently ${an ?? '—'})` }); continue; }
          if (mv == null || av == null) continue;
          if (String(mv) !== String(av)) {
            if ((p.includes('gap') || p === 'justifyContent' || p === 'alignItems' || p === 'flexWrap') && !/flex|grid/.test(mc.display || '')) continue;
            // layout (1) detector already covers flex/grid containers ≥240 by path; emit here for the
            // structure-matched set (text/fid matched), which can reach smaller/text-anchored containers.
            add({ locator: clabel(m), section: sect, class: 'structure', property: p, target: String(av), reference: String(mv), suggestedChange: `set ${p} to ${mv} (currently ${av})` });
          }
        }
        const mKids = childrenOf(mock, m.i).length, aKids = childrenOf(appAll, a.i).length;
        if (mKids !== aKids && mKids > 0) {
          const key = clabel(m);
          if (!childCountSeen.has(key)) { childCountSeen.add(key); add({ locator: key, section: sect, class: 'structure', property: 'child-count', target: aKids, reference: mKids, suggestedChange: aKids < mKids ? `this container is missing ${mKids - aKids} child node(s) the mock has (a row/icon/divider/badge)` : `this container has ${aKids - mKids} extra child node(s) the mock lacks` }); }
        }
      }
      // FIX 3 — full normalised-text presence on each side. A `missing`/`extra` whose TEXT is present on
      // the OTHER side too is a pairing phantom (same string, different tag/path the matcher could not
      // confidently pair) — route it to noiseExcluded.unpairedSameText instead of findings.
      const mockTextSet = new Set(); for (const n of mock) { const t = sigText(n); if (t.length >= 2) mockTextSet.add(t); }
      const appTextSet = new Set(); for (const n of appAll) { const t = sigText(n); if (t.length >= 2) appTextSet.add(t); }
      const sameTextSeen = new Set();
      // MISSING (in mock, absent in target)
      const missingSeen = new Set();
      for (const m of mock) {
        if (pairs.has(m.i)) continue;
        if (!(sigText(m).length >= 2 || isVisual(m))) continue;
        const kind = visualKind(m), tx = sigText(m);
        // ILLUSTRATION-INTERNAL GUARD (v2.3.0): an unpaired TEXT node inside a product illustration is
        // placeholder content (a demo ticker/number/sample label) — its TEXT legitimately differs, so it is
        // NOT a real absence. Route to noiseExcluded.illustrationInternals; the illustration STYLE pass still
        // compares its computed style. A VISUAL internal (icon/divider/tile) with no text is kept (a missing
        // illustration sub-shape IS a real structural defect), so this suppresses TEXT internals only.
        if (mockIsIlloInternal(m) && tx) {
          noiseExcluded.illustrationInternals.push({ note: 'placeholder-text(mock)', text: tx.slice(0, 60), tag: m.tag, y: Math.round(m.rect?.y || 0) });
          continue;
        }
        // PHANTOM GUARD: this text exists on the target too → not a real absence.
        if (tx && appTextSet.has(tx)) {
          if (!sameTextSeen.has('m|' + tx)) { sameTextSeen.add('m|' + tx); noiseExcluded.unpairedSameText.push({ side: 'mock', text: tx.slice(0, 60), tag: m.tag, y: Math.round(m.rect?.y || 0) }); }
          continue;
        }
        const key = kind + '|' + tx + '|' + pathOf(mock, m);
        if (missingSeen.has(key)) continue; missingSeen.add(key);
        const sect = sectionFor(m, mockLeads);
        add({ locator: tx ? `"${tx}"` : `‹${m.tag}›  @${Math.round(m.rect?.x || 0)},${Math.round(m.rect?.y || 0)}`, section: sect, class: 'structure', property: 'missing', target: 'absent', reference: `${kind}${tx ? ` "${tx}"` : ` <${m.tag}>`}`, severity: kind === 'text' ? 'med' : 'high', suggestedChange: `build the ${kind} the mock has${tx ? ` ("${tx}")` : ` (a ${m.tag})`} — absent on target` });
      }
      // EXTRA (target-only)
      const extraSeen = new Set();
      for (const a of appAll) {
        if (usedApp.has(a.i)) continue;
        if (!(sigText(a).length >= 2 || isVisual(a))) continue;
        const tx = sigText(a);
        if (CHROME_TXT.test(tx)) continue;
        // ILLUSTRATION-INTERNAL GUARD (v2.3.0): a target-only TEXT node inside a product illustration is
        // placeholder content — its TEXT legitimately differs from the reference's placeholder, so it is NOT
        // a real extra. Route to noiseExcluded.illustrationInternals (the style pass still checks its style).
        if (appIsIlloInternal(a) && tx) {
          noiseExcluded.illustrationInternals.push({ note: 'placeholder-text(target)', text: tx.slice(0, 60), tag: a.tag, y: Math.round(a.rect?.y || 0) });
          continue;
        }
        // PHANTOM GUARD: this text exists on the reference too → not a real extra.
        if (tx && mockTextSet.has(tx)) {
          if (!sameTextSeen.has('a|' + tx)) { sameTextSeen.add('a|' + tx); noiseExcluded.unpairedSameText.push({ side: 'target', text: tx.slice(0, 60), tag: a.tag, y: Math.round(a.rect?.y || 0) }); }
          continue;
        }
        const kind = visualKind(a);
        const key = kind + '|' + tx;
        if (extraSeen.has(key)) continue; extraSeen.add(key);
        add({ locator: tx ? `"${tx}"` : `‹${a.tag}›  @${Math.round(a.rect?.x || 0)},${Math.round(a.rect?.y || 0)}`, section: sectionFor(a, appLeads), class: 'extra', property: 'extra', target: `${kind}${tx ? ` "${tx}"` : ` <${a.tag}>`}`, reference: 'absent (mock has no such node)', severity: 'low', suggestedChange: `the target renders this ${kind}${tx ? ` ("${tx}")` : ''} but the mock does not — remove it, or confirm it is legitimate real data / a cited divergence` });
      }
    }

    // ============= UNMATCHED mock probes (missing OR intentional swap) =============
    {
      const appAllText = new Set(appAll.filter(n => A.text(n)).map(n => A.text(n)));
      for (const u of unmatched) {
        if (!u.text) continue;
        // ILLUSTRATION-INTERNAL GUARD (v2.3.0): placeholder text inside an illustration that didn't pair is
        // not a wrong-state signal — its content legitimately differs. Bucket it, don't emit.
        if (mockIsIlloInternal(u.node)) {
          noiseExcluded.illustrationInternals.push({ note: 'placeholder-text(unmatched-mock)', text: norm(u.text).slice(0, 60), tag: u.tag, y: Math.round(u.node?.rect?.y || 0) });
          continue;
        }
        if (appAllText.has(norm(u.text))) {
          // present ELSEWHERE in the dump → wrong-state coverage signal, not an absence
          add({ locator: `${u.tag}.${(u.cls || '').split(/\s+/)[0]} — "${u.text}"`, section: sectionFor(u.node, mockLeads), class: 'structure', property: 'wrong-state', target: 'present elsewhere in dump', reference: 'expected on this surface', severity: 'med', suggestedChange: `"${u.text}" exists elsewhere in the target — you may have measured the wrong state/screen; re-measure the populated surface` });
          continue;
        }
        // A mock text probe that paired with NOTHING, and whose string appears nowhere in the target.
        //
        // This used to `continue` on the reasoning that "genuine absences are already covered by the
        // structure-diff missing pass". That assumption has a hole, and a blind judge panel found it: a
        // CHANGED string is neither a missing node nor a paired text node. The element still exists and
        // still pairs structurally, so the missing pass says nothing; its text never matched, so the
        // text-probe loop dropped it here. "Editor's picks" becoming "Movers today" produced ZERO
        // findings in either the old or the new differ, on a page where it was one of ten planted
        // defects — measured 18 Aug 2026.
        //
        // Worse than the miss: THE LAW's rule 2 requires the reader to resolve *every* unpaired mock node
        // to ABSENT-or-cited. That instruction referred to a list the artifact never produced. A gate
        // whose vocabulary describes an artifact that does not exist is the defect this rebuild is about,
        // one layer in. So the list exists now, as findings.
        unpairedMock.push(u);
        add({
          locator: `${u.tag}${u.cls ? '.' + String(u.cls).split(/\s+/)[0] : ''} — "${String(u.text).slice(0, 60)}"`,
          section: sectionFor(u.node, mockLeads), class: 'breadth', property: 'unpaired-mock-text',
          target: 'ABSENT or RENAMED — no element carries this text', reference: `"${String(u.text).slice(0, 60)}"`,
          severity: 'high',
          suggestedChange: `TWO READINGS, and you must pick one by looking: either the element is ABSENT (build it), or it EXISTS WITH DIFFERENT COPY (align the string, or cite the decision). Pairing here is by text, so a renamed label is indistinguishable from a deleted one until you check the target for an element of the same role in the same place — look for a position/geometry finding on a nearby node carrying unfamiliar text; that is usually the renamed one. Do NOT sweep several of these rows into one conclusion: a genuinely deleted card and a single rewritten heading produce identical rows, and closing the group on the deletion is how the rename ships.`,
        });
      }
      if (unpairedMock.length) {
        add({
          locator: `[${unpairedMock.length} unpaired mock text node${unpairedMock.length === 1 ? '' : 's'}]`,
          section: null, class: 'breadth', property: 'unpaired-mock-denominator',
          target: `${unpairedMock.length} of ${unpairedMock.length + pairedTextCount} mock text probes found no counterpart`,
          reference: `${unpairedMock.length + pairedTextCount} mock text probes attempted`,
          severity: 'low',
          suggestedChange: `THE LAW rule 2: every one of these resolves to ABSENT or to an external citation. This row is the denominator — a findings list with no breadth row above it means the pairing collapsed, which is not the same as the page matching.`,
        });
      }
    }

    // ============= SHARED MATCHED-PAIR SET (v2.4.0) =============
    // The per-element vertical-offset (Detector 1) and block-flow gap (Detector 2) passes both need a
    // confident mock→target element pairing that spans CONTAINERS (not just text nodes). Re-use the same
    // fid → tag+text → structural-path → geometry chain the structure pass uses, exposed here as a flat map.
    const matchedPairs = (() => {
      const pairs = new Map(), usedApp = new Set();
      const take = (mn, an) => { if (an && !usedApp.has(an.i)) { pairs.set(mn.i, an); usedApp.add(an.i); return true; } return false; };
      // (0) fid
      const byFid = new Map(); for (const a of appAll) if (a.fid) byFid.set(a.fid, a);
      for (const m of mock) if (m.fid && byFid.has(m.fid)) take(m, byFid.get(m.fid));
      // (1) tag + normalised text
      const byText = new Map();
      for (const a of appAll) { const t = norm(a.text).slice(0, 60); if (t.length < 2) continue; const k = a.tag + '|' + t; if (!byText.has(k)) byText.set(k, []); byText.get(k).push(a); }
      for (const m of mock) { if (pairs.has(m.i)) continue; const t = norm(m.text).slice(0, 60); if (t.length < 2) continue; take(m, (byText.get(m.tag + '|' + t) || []).find(a => !usedApp.has(a.i))); }
      // (2) structural path
      const kidsP = arr => { const mp = new Map(); for (const n of arr) { if (!mp.has(n.parent)) mp.set(n.parent, []); mp.get(n.parent).push(n); } return mp; };
      const mKidsP = kidsP(mock), aKidsP = kidsP(appAll);
      const pathOf = (nodes, kids, n) => { const parts = []; let cur = n, hops = 0; while (cur && cur.parent >= 0 && hops++ < 40) { const sibs = kids.get(cur.parent) || []; parts.unshift(`${cur.tag}[${sibs.indexOf(cur)}]`); cur = nodes[cur.parent]; } return parts.join('/'); };
      const byPath = new Map(); for (const a of appAll) { const p = pathOf(appAll, aKidsP, a); if (!byPath.has(p)) byPath.set(p, a); }
      for (const m of mock) { if (pairs.has(m.i)) continue; take(m, byPath.get(pathOf(mock, mKidsP, m))); }
      return pairs;
    })();

    // ============= PER-ELEMENT VERTICAL OFFSET — "moved without resizing" (v2.4.0, Detector 1) =====
    // A status/badge/label shifted DOWN (or up) by a parent alignment change (align-items center vs
    // flex-start, justify-content, a different top margin) — WITHOUT resizing — was caught only as the
    // PARENT's layout/align-items diff, never as the element ITSELF moving (recall WEAK #3, the "On track"
    // status moved ~14px down). There is no per-element top/dy detector (only page-level cumulative drift).
    //
    // For each MATCHED element we compute its top RELATIVE TO ITS DIRECT PARENT (its paired counterpart's
    // parent, frame-relative) on each side. If the element's SIZE matches (a pure move, not a reflow) but its
    // relative-in-parent offset differs by > VOFF_TOL (~4px), emit a position/rel-offset finding. NOISE GUARDS:
    //   · require the element to pair cleanly (matchedPairs) AND its OWN width+height ~equal (no reflow), so a
    //     wrap/growth that also shifts children isn't double-counted as a move;
    //   · require BOTH parents to themselves pair (matchedPairs), else "relative to parent" is meaningless;
    //   · DEDUP per parent — a whole column shifting by the same delta is ONE alignment change, not N findings:
    //     identical (parentKey|signed-delta) groups collapse to one row + a [×N] summary.
    if (GEOM) {
      const VOFF_TOL = 4;          // px — below this is sub-pixel/rounding noise
      const SIZE_TOL = 3;          // px — w/h must match this tightly to count as a PURE move (not a reflow)
      const voffRows = [];
      for (const [mi, a] of matchedPairs) {
        const m = mock[mi];
        if (!m || !m.rect || !a.rect) continue;
        if (m.rect.w <= 0 || m.rect.h <= 0 || a.rect.w <= 0 || a.rect.h <= 0) continue;
        // PURE MOVE guard — own width AND height must match (a reflow that grew the box is a different class,
        // already covered by geometry/height + wrap/line-count).
        if (!close(a.rect.w, m.rect.w, SIZE_TOL) || !close(a.rect.h, m.rect.h, SIZE_TOL)) continue;
        const mp = m.parent >= 0 ? mock[m.parent] : null;
        const ap = a.parent >= 0 ? appById.get(a.parent) : null;
        if (!mp || !ap || !mp.rect || !ap.rect) continue;
        // both parents must themselves pair (so "relative to parent" is the SAME parent on both sides).
        if (matchedPairs.get(mp.i) !== ap) continue;
        const mRel = m.rect.y - mp.rect.y;       // top relative to the direct parent's top
        const aRel = a.rect.y - ap.rect.y;
        const d = aRel - mRel;
        if (Math.abs(d) <= VOFF_TOL) continue;
        const loc = locatorFor(a);
        const sect = sectionFor(a, appLeads);
        const elTxt = norm(m.text);
        const el = elTxt ? `"${elTxt.slice(0, 32)}"` : `<${m.tag}>`;
        voffRows.push({
          loc, sect, mRel: +mRel.toFixed(1), aRel: +aRel.toFixed(1), d: +d.toFixed(1), el,
          // dedup key: same parent + same signed (rounded) delta = one alignment change
          dk: ap.i + '|' + Math.round(d),
        });
      }
      // DEDUP per parent+delta — a column of children that all shifted by the same amount is ONE change.
      const vg = new Map();
      for (const r of voffRows) { if (!vg.has(r.dk)) vg.set(r.dk, []); vg.get(r.dk).push(r); }
      for (const [, g] of vg) {
        const dir = g[0].d > 0 ? 'down' : 'up';
        g.slice(0, 3).forEach(r => add({
          locator: r.loc, section: r.sect, class: 'position', property: 'rel-offset',
          target: r.aRel, reference: r.mRel, deltaPx: Math.abs(Math.round(r.d)),
          suggestedChange: `${r.el} sits ${Math.abs(Math.round(r.d))}px too far ${dir} inside its parent (top ${r.aRel}px from the parent vs the mock's ${r.mRel}px) at the SAME size — a pure vertical move, usually a parent align-items/justify-content/margin change. Set the parent's vertical alignment (or this element's top margin) so it sits ${r.mRel}px from the parent top`,
        }));
        if (g.length > 3) add({
          locator: `[×${g.length} elements in one parent]`, section: g[0].sect, class: 'position', property: 'rel-offset',
          target: g[0].aRel, reference: g[0].mRel, deltaPx: Math.abs(Math.round(g[0].d)),
          suggestedChange: `${g.length} children of one parent all shifted ${Math.abs(Math.round(g[0].d))}px ${dir} at the same size — ONE parent alignment change (align-items/justify-content). Fix the parent's vertical alignment once`,
        });
      }
    }

    // ============= BLOCK-FLOW GAP between NON-TEXT containers (v2.4.0, Detector 2) =====
    // The existing gap→/←-sibling check (in the text-probe pass) only runs on TEXT-PAIRED nodes. A
    // case-study point list of NON-text containers spaced by block-flow MARGIN/PADDING (a display:block
    // <div> per point) is invisible: the layout-structure gap check only compares flex/grid `gap`, and the
    // text-probe gap check never reaches a text-less container (recall MISS #6: inter-point gap 38px ref vs
    // 33px broken produced NO finding). This pass runs the SAME geometry-based gap (next.top - this.bottom,
    // which INCLUDES margin) on PAIRED CONTAINERS, so block-flow spacing between block boxes is checked.
    //   · gap is computed from rendered geometry, so it captures margin-collapse + padding + the real flow,
    //     regardless of whether the spacing is margin, padding, or a flex/grid gap;
    //   · only emitted when BOTH the container AND its next sibling pair cleanly (so the gap is between the
    //     SAME two boxes on each side) and the delta > GAP_TOL (~3px);
    //   · DEDUP repeated identical gaps (N points spaced the same → one row + a [×N] summary), so a list of
    //     evenly-spaced points reports its single spacing defect once, not per point.
    if (GEOM) {
      const GAP_TOL = 3;
      const isBlockContainer = n => {
        if (!n || n.tag === 'body' || /\b(body|scr|frame|screen)\b/.test(n.cls || '')) return false;
        if (!n.rect || (n.rect.w || 0) < 40 || (n.rect.h || 0) < 8) return false;
        // a CONTAINER, not a leaf text run: it has children OR no direct text of its own. We want block-flow
        // boxes (points, rows, cards) — skip pure inline/text leaves (those go through the text-probe gap).
        const disp = n.comp?.display || '';
        if (/inline(?!-)/.test(disp)) return false;        // inline / inline boxes don't drive block-flow gap
        return true;
      };
      const bfRows = [];
      const bfSeen = new Set();
      for (const [mi, a] of matchedPairs) {
        const m = mock[mi];
        if (!isBlockContainer(m) || !isBlockContainer(a)) continue;
        // next block-flow sibling on the MOCK side (source order within the same parent)
        const mSibs = mockKids.get(m.parent); if (!mSibs) continue;
        const mIdx = mSibs.indexOf(m); if (mIdx < 0) continue;
        const mNext = mSibs[mIdx + 1];
        if (!mNext || !isBlockContainer(mNext)) continue;
        // the next sibling must ALSO pair, and to the app element that is the matched element's next sibling,
        // so the gap is measured between the SAME two boxes on both sides.
        const aNext = matchedPairs.get(mNext.i);
        if (!aNext) continue;
        const aSibs = appKids.get(a.parent);
        if (!aSibs || aSibs.indexOf(aNext) < 0 || aSibs.indexOf(a) < 0) continue;
        if (aSibs.indexOf(aNext) <= aSibs.indexOf(a)) continue; // aNext must come AFTER a in app source order too
        const mGap = +(mNext.rect.y - (m.rect.y + m.rect.h)).toFixed(1);
        const aGap = +(aNext.rect.y - (a.rect.y + a.rect.h)).toFixed(1);
        if (mGap <= 1 && aGap <= 1) continue;                  // both touching → no spacing to compare
        if (close(aGap, mGap, GAP_TOL)) continue;
        // de-dup an exact pair already produced via the text-probe gap path (a paired text node whose
        // styled box is this container) — key by the app box + next box so we don't double-report.
        const pk = a.i + '>' + aNext.i;
        if (bfSeen.has(pk)) continue; bfSeen.add(pk);
        const loc = locatorFor(a) || `[container ${a.tag} @y${Math.round(a.rect.y)}]`;
        const sect = sectionFor(a, appLeads);
        bfRows.push({ loc, sect, mGap, aGap, dk: 'bf|' + Math.round(mGap) + '|' + Math.round(aGap) });
      }
      const bg = new Map();
      for (const r of bfRows) { if (!bg.has(r.dk)) bg.set(r.dk, []); bg.get(r.dk).push(r); }
      for (const [, g] of bg) {
        g.slice(0, 3).forEach(r => add({
          locator: r.loc, section: r.sect, class: 'spacing', property: 'gap→next-sibling(block-flow)',
          target: r.aGap, reference: r.mGap, deltaPx: Math.round(Math.abs(r.aGap - r.mGap)),
          suggestedChange: `the block-flow gap to the next sibling is ${r.aGap}px but the mock's is ${r.mGap}px — this spacing is margin/padding on a display:block container (not a flex/grid gap). Set the margin/padding so the inter-element gap is ${r.mGap}px`,
        }));
        if (g.length > 3) add({
          locator: `[×${g.length} block-flow gaps]`, section: g[0].sect, class: 'spacing', property: 'gap→next-sibling(block-flow)',
          target: g[0].aGap, reference: g[0].mGap, deltaPx: Math.round(Math.abs(g[0].aGap - g[0].mGap)),
          suggestedChange: `${g.length} sibling block containers share the same wrong inter-element gap (${g[0].aGap}px vs the mock's ${g[0].mGap}px) — fix the per-item margin/padding once`,
        });
      }
    }

    // ============= SYSTEMATIC PSEUDO-ELEMENT comparison (v2.5.0) =====
    // The existing pseudo handling does two narrow things: (a) the capture-side FOLD copies a pseudo's
    // border/shadow into the element's effective `comp` ONLY when the element itself has none, and (b) the
    // PSEUDO-CONTENT detector compares the ::before/::after content STRING (bullets, counters, arrows). What
    // neither catches: a pseudo that draws a DIFFERENT border/overlay/fill on one side vs the other, or a
    // pseudo-drawn OVERLAY/border present on one side and absent on the other, on an ordinary (non-list,
    // non-illustration) element. Page-builders (Framer et al.) routinely draw a card's border, a focus ring,
    // a gradient overlay, or a hairline on `::after { content:""; border/background/box-shadow }`. This pass
    // compares getComputedStyle(el,'::before'|'::after') box properties for EVERY paired element.
    //   · runs over matchedPairs (every paired element, not just illustrations);
    //   · compares per pseudo: presence, border-top-width + colour, background (colour OR image), box-shadow
    //     presence, and border-radius — the properties a pseudo-drawn border/overlay carries;
    //   · DEDUP a repeating identical pseudo defect (every card's ::after border) to ≤3 rows + a [×N] summary.
    {
      const pseudoRaw = [];
      const hexT = c => toHex(c);
      for (const [mi, a] of matchedPairs) {
        const m = mock[mi];
        if (!m) continue;
        const mps = m.pseudoStyle || null, aps = a.pseudoStyle || null;
        if (!mps && !aps) continue;
        for (const ps of ['::before', '::after']) {
          const mp = mps && mps[ps], ap = aps && aps[ps];
          if (!mp && !ap) continue;
          const loc = locatorFor(a);
          const sect = sectionFor(a, appLeads);
          // PRESENCE — one side draws a rendering pseudo the other lacks entirely (a pseudo overlay/border).
          if (!!mp !== !!ap) {
            const present = mp || ap;
            const drawsBorder = (parseFloat(present.borderTopWidth) || 0) > 0;
            const drawsBg = present.background && hexT(present.background) !== 'transparent';
            const drawsImg = present.backgroundImage && present.backgroundImage !== 'none';
            const drawsShadow = present.boxShadow && present.boxShadow !== 'none';
            const what = drawsBorder ? `a ${present.borderTopWidth} ${hexT(present.borderTopColor)} border`
              : drawsImg ? 'a background-image overlay'
              : drawsBg ? `a ${hexT(present.background)} fill`
              : drawsShadow ? 'a box-shadow' : 'a decorative shape';
            pseudoRaw.push({
              loc, sect, class: mp ? 'border' : 'pseudo', property: `pseudo-${ps.replace(/:/g, '')}-presence`,
              target: ap ? `${ps} present` : `no ${ps}`, reference: mp ? `${ps} present (draws ${what})` : `no ${ps}`,
              dk: 'pp|' + ps + '|' + (mp ? 'ref' : 'tgt') + '|' + what,
              sc: mp ? `the reference draws ${what} on the ${ps} pseudo-element of ${loc} — the target's ${ps} renders nothing. Add the matching ${ps} { content:""; … } overlay`
                     : `the target draws ${what} on a ${ps} pseudo-element ${loc} that the reference does not — remove it (mock wins)`,
            });
            continue;
          }
          // BOTH present — compare the box properties.
          const mbw = parseFloat(mp.borderTopWidth) || 0, abw = parseFloat(ap.borderTopWidth) || 0;
          if (!close(abw, mbw, 0.6)) pseudoRaw.push({ loc, sect, class: 'border', property: `pseudo-${ps.replace(/:/g, '')}-border-width`, target: abw, reference: mbw, deltaPx: Math.round(Math.abs(abw - mbw)), dk: 'pbw|' + ps + '|' + abw + '|' + mbw, sc: `set the ${ps} pseudo border-width to ${mbw}px on ${loc} (a pseudo-drawn border — invisible to getComputedStyle(el))` });
          else if (mbw >= 0.6 && hexT(mp.borderTopColor) !== hexT(ap.borderTopColor)) pseudoRaw.push({ loc, sect, class: 'border', property: `pseudo-${ps.replace(/:/g, '')}-border-color`, target: hexT(ap.borderTopColor), reference: hexT(mp.borderTopColor), dk: 'pbc|' + ps + '|' + hexT(ap.borderTopColor) + '|' + hexT(mp.borderTopColor), sc: `set the ${ps} pseudo border colour to ${hexT(mp.borderTopColor)} on ${loc}` });
          const mbg = hexT(mp.background), abg = hexT(ap.background);
          if (mbg !== abg && !(mbg === 'transparent' && abg === 'transparent')) pseudoRaw.push({ loc, sect, class: 'container-bg', property: `pseudo-${ps.replace(/:/g, '')}-background`, target: abg, reference: mbg, dk: 'pbg|' + ps + '|' + abg + '|' + mbg, sc: `set the ${ps} pseudo background to ${mbg} on ${loc} (a pseudo-drawn fill/overlay)` });
          const mImg = mp.backgroundImage !== 'none', aImg = ap.backgroundImage !== 'none';
          if (mImg !== aImg) pseudoRaw.push({ loc, sect, class: 'container-bg', property: `pseudo-${ps.replace(/:/g, '')}-bg-image`, target: aImg ? 'present' : 'none', reference: mImg ? 'present' : 'none', dk: 'pbi|' + ps + '|' + aImg + '|' + mImg, sc: mImg ? `add the ${ps} pseudo background-image overlay the reference draws on ${loc}` : `remove the ${ps} pseudo background-image overlay from ${loc}` });
          const mSh = mp.boxShadow !== 'none', aSh = ap.boxShadow !== 'none';
          if (mSh !== aSh) pseudoRaw.push({ loc, sect, class: 'shadow', property: `pseudo-${ps.replace(/:/g, '')}-box-shadow`, target: aSh ? 'yes' : 'no', reference: mSh ? 'yes' : 'no', dk: 'psh|' + ps + '|' + aSh + '|' + mSh, sc: mSh ? `add the ${ps} pseudo box-shadow on ${loc}` : `remove the ${ps} pseudo box-shadow from ${loc}` });
          const mRad = parseFloat(mp.borderTopLeftRadius) || 0, aRad = parseFloat(ap.borderTopLeftRadius) || 0;
          if (!close(aRad, mRad, 2.5)) pseudoRaw.push({ loc, sect, class: 'border', property: `pseudo-${ps.replace(/:/g, '')}-border-radius`, target: aRad, reference: mRad, deltaPx: Math.round(Math.abs(aRad - mRad)), dk: 'prd|' + ps + '|' + aRad + '|' + mRad, sc: `set the ${ps} pseudo border-radius to ${mRad}px on ${loc}` });
        }
      }
      // DEDUP repeated identical pseudo defects (every card's ::after border) → ≤3 rows + a [×N] summary.
      const pg = new Map();
      for (const r of pseudoRaw) { if (!pg.has(r.dk)) pg.set(r.dk, []); pg.get(r.dk).push(r); }
      for (const [, g] of pg) {
        g.slice(0, 3).forEach(r => add({ locator: r.loc, section: r.sect, class: r.class, property: r.property, target: r.target, reference: r.reference, ...(r.deltaPx != null ? { deltaPx: r.deltaPx } : {}), suggestedChange: r.sc }));
        if (g.length > 3) add({ locator: `[×${g.length} elements]`, section: g[0].sect, class: g[0].class, property: g[0].property, target: g[0].target, reference: g[0].reference, ...(g[0].deltaPx != null ? { deltaPx: g[0].deltaPx } : {}), suggestedChange: `${g[0].sc} — applies to ${g.length} elements with the same pseudo-drawn defect (one root cause)` });
      }
    }

    // ============= RESPONSIVE — per-width findings + desktop→mobile TRANSITION divergence =====
    // Driven by globalThis.__MF_REFERENCE_BYWIDTH__ / __MF_TARGET_BYWIDTH__ (analyses keyed by
    // viewport width, each a MODE-A capture). We (1) compute, for KEY CONTAINERS (sections, grids,
    // flex rows, nav, card grids), the TRANSITION from desktop (1280) to mobile (390) per side —
    // display / flex-direction / grid track-count — and flag where the two sides' transitions
    // DIVERGE; and (2) surface the normal per-width container/nav findings at 390 and 768.
    // _MF_RESPONSIVE_DONE guards against re-entry: the per-width sub-diffs below call diff()
    // recursively, and must NOT re-run the responsive pass (the bywidth globals are still set).
    if (REFERENCE_BYWIDTH && TARGET_BYWIDTH && !diff._inResponsive) {
      diff._inResponsive = true;
      const unwrap = v => {
        if (v == null) return null;
        if (typeof v === 'string') { try { v = JSON.parse(v); } catch (e) { return null; } }
        if (v && v.analysis && v.analysis.nodes) v = v.analysis;
        return v && v.nodes ? v : null;
      };
      const refW = {}, tgtW = {};
      for (const k of Object.keys(REFERENCE_BYWIDTH)) { const u = unwrap(REFERENCE_BYWIDTH[k]); if (u) refW[+k] = u; }
      for (const k of Object.keys(TARGET_BYWIDTH)) { const u = unwrap(TARGET_BYWIDTH[k]); if (u) tgtW[+k] = u; }
      const WIDTHS = [390, 768, 1280].filter(w => refW[w] && tgtW[w]);

      // --- track-count helpers (reused from the layout detector) ---
      const colCountR = gtc => {
        if (!gtc || gtc === 'none') return 1;
        let depth = 0, count = 0, inTok = false;
        for (const ch of gtc) {
          if (ch === '(') depth++; else if (ch === ')') depth--;
          else if (ch === ' ' && depth === 0) inTok = false;
          else if (depth === 0 && !inTok) { inTok = true; count++; }
        }
        return count || 1;
      };
      // a KEY layout container: a wide flex/grid box, a <nav>, or a header.
      const isKeyContainer = n => {
        if (!n || n.tag === 'body' || /\b(body|scr|frame|screen)\b/.test(n.cls || '')) return false;
        if (norm(n.text)) return false;
        const c = n.comp || {}, r = n.rect || {};
        if ((r.w || 0) < 200 || (r.h || 0) < 16) return false;
        const flexgrid = /flex|grid/.test(c.display || '');
        const navish = n.tag === 'nav' || n.tag === 'header' || /\b(nav|header|menu|grid|cards?|row|cols?|columns?)\b/i.test(n.cls || '');
        return flexgrid || navish;
      };
      // layout signature of a container at one width.
      const layoutSig = n => {
        const c = n.comp || {};
        const disp = c.display || 'block';
        const fd = /flex/.test(disp) ? (c.flexDirection || 'row') : null;
        const cols = /grid/.test(disp) ? colCountR(c.gridTemplateColumns) : null;
        return { disp, fd, cols };
      };
      // pair a container across widths by a stable key: tag + first class token + rounded source order.
      const ckey = n => `${n.tag}.${(n.cls || '').split(/\s+/).filter(Boolean)[0] || ''}#${n.i}`;
      // Build, per side, a map keyed by ckey → { [width]: layoutSig }. Containers are paired across
      // widths by source-order index (n.i) within the same-side dump, which is stable because the
      // same page is re-measured at each width (DOM order does not change with viewport).
      const sideTransitions = (byWidth) => {
        const byKey = new Map();
        for (const w of WIDTHS) {
          for (const n of byWidth[w].nodes) {
            if (!isKeyContainer(n)) continue;
            const k = ckey(n);
            if (!byKey.has(k)) byKey.set(k, { node: n, sig: {} });
            byKey.get(k).sig[w] = layoutSig(n);
          }
        }
        return byKey;
      };
      // NAV→HAMBURGER heuristic per side: at mobile (390), the desktop nav's link row is hidden
      // (display:none or zero-height) AND/OR a toggle/burger control appears.
      const navCollapses = (byWidth) => {
        const desktop = byWidth[1280], mobile = byWidth[390];
        if (!desktop || !mobile) return null;
        const linkCountAt = doc => doc.nodes.filter(n => n.tag === 'a' && (n.rect?.h || 0) > 0 && (n.rect?.w || 0) > 0 && norm(n.text) && (n.rect?.y || 0) < 160).length;
        const burgerAt = doc => doc.nodes.some(n => {
          const cls = (n.cls || '').toLowerCase();
          const aria = '';
          const burgerCls = /(burger|hamburger|menu-toggle|nav-toggle|mobile-menu|menu-button|menutoggle)/.test(cls);
          const buttonish = (n.tag === 'button' || n.tag === 'a') && (n.rect?.y || 0) < 160 && (n.rect?.w || 0) <= 64 && (n.rect?.h || 0) <= 64 && !norm(n.text);
          return burgerCls || (buttonish && n.hasSvgChild);
        });
        const dLinks = linkCountAt(desktop), mLinks = linkCountAt(mobile);
        const collapsed = dLinks >= 3 && mLinks <= Math.max(1, Math.floor(dLinks / 2));
        const hasBurger = burgerAt(mobile) && !burgerAt(desktop);
        return { collapsed: collapsed || hasBurger, dLinks, mLinks, hasBurger };
      };

      const refTrans = sideTransitions(refW), tgtTrans = sideTransitions(tgtW);
      // ---- (a) TRANSITION DIVERGENCE: same container, the two sides transition differently ----
      const responsiveRows = [];
      const has1280 = WIDTHS.includes(1280), has390 = WIDTHS.includes(390);
      if (has1280 && has390) {
        // pair ref↔tgt key containers by best layout-signature match at 1280 (the desktop state we
        // already diff in MODE B), then compare their 1280→390 transition.
        const refList = [...refTrans.values()].filter(e => e.sig[1280] && e.sig[390]);
        const tgtList = [...tgtTrans.values()].filter(e => e.sig[1280] && e.sig[390]);
        const tUsed = new Set();
        const transOf = (sig) => `${sig[1280].disp}/${sig[1280].fd || '-'}/${sig[1280].cols || '-'} → ${sig[390].disp}/${sig[390].fd || '-'}/${sig[390].cols || '-'}`;
        for (const re of refList) {
          // candidate target containers: same desktop display + similar desktop width.
          const rd = re.sig[1280];
          let best = null, bestD = Infinity;
          for (let ti = 0; ti < tgtList.length; ti++) {
            if (tUsed.has(ti)) continue;
            const te = tgtList[ti];
            if (te.sig[1280].disp !== rd.disp) continue;
            const dW = Math.abs((te.node.rect?.w || 0) - (re.node.rect?.w || 0));
            const dY = Math.abs((te.node.rect?.y || 0) - (re.node.rect?.y || 0));
            const cost = dW + dY * 0.5;
            if (cost < bestD) { bestD = cost; best = ti; }
          }
          if (best == null || bestD > 200) continue;
          tUsed.add(best);
          const te = tgtList[best];
          const rTrans = transOf(re.sig), tTrans = transOf(te.sig);
          // a meaningful transition occurred on at least one side, and they differ.
          const rChanged = JSON.stringify(re.sig[1280]) !== JSON.stringify(re.sig[390]);
          const tChanged = JSON.stringify(te.sig[1280]) !== JSON.stringify(te.sig[390]);
          if (rTrans !== tTrans && (rChanged || tChanged)) {
            const lbl = `[${re.node.tag}.${(re.node.cls || '').split(/\s+/)[0] || ''} @1280 w${Math.round(re.node.rect?.w || 0)}]`;
            // describe the divergence in the most actionable terms (grid cols, flex direction, display).
            let prop = 'layout-transition', sc;
            const r1 = re.sig[1280], r3 = re.sig[390], t3 = te.sig[390];
            if (r1.cols != null) {
              prop = 'grid-cols-transition';
              sc = `at 390px the reference grid is ${r3.cols}-col but the target stays ${t3.cols}-col — add the responsive collapse (e.g. grid-template-columns: 1fr at the mobile breakpoint)`;
            } else if (r1.disp && /flex/.test(r1.disp)) {
              prop = 'flex-direction-transition';
              sc = `at 390px the reference is flex-direction:${r3.fd} but the target is ${t3.fd} — match the responsive stacking at the mobile breakpoint`;
            } else {
              sc = `the reference transitions ${rTrans} from desktop→mobile but the target transitions ${tTrans} — align the responsive behaviour`;
            }
            responsiveRows.push({ lbl, sect: null, prop, target: tTrans, reference: rTrans, sc, dk: `${prop}|${rTrans}|${tTrans}` });
          }
        }
        // ---- (b) NAV → HAMBURGER divergence ----
        const rNav = navCollapses(refW), tNav = navCollapses(tgtW);
        if (rNav && tNav && rNav.collapsed !== tNav.collapsed) {
          responsiveRows.push({
            lbl: '[nav/header @y<160]', sect: null, prop: 'nav-hamburger-transition',
            target: tNav.collapsed ? 'collapses to mobile menu' : `stays a ${tNav.mLinks}-link row`,
            reference: rNav.collapsed ? 'collapses to mobile menu' : `stays a ${rNav.mLinks}-link row`,
            sc: rNav.collapsed
              ? `at 390px the reference nav collapses to a mobile/hamburger menu (desktop ${rNav.dLinks} links → mobile ${rNav.mLinks}) but the target keeps a ${tNav.mLinks}-link row — add the responsive nav collapse`
              : `at 390px the target nav collapses to a mobile menu but the reference keeps a ${rNav.mLinks}-link row — the reference does NOT use a hamburger here`,
            dk: `nav|${rNav.collapsed}|${tNav.collapsed}`,
          });
        }
      }
      // emit transition-divergence findings (deduped, capped).
      const rgroups = new Map();
      for (const r of responsiveRows) { if (!rgroups.has(r.dk)) rgroups.set(r.dk, []); rgroups.get(r.dk).push(r); }
      let rEmitted = 0;
      for (const [, g] of rgroups) {
        if (rEmitted >= 12) break;
        g.slice(0, 3).forEach(r => { if (rEmitted++ < 12) add({ locator: r.lbl, section: r.sect, class: 'responsive', property: r.prop, target: r.target, reference: r.reference, severity: 'high', suggestedChange: r.sc }); });
        if (g.length > 3) add({ locator: `[×${g.length} containers]`, section: null, class: 'responsive', property: g[0].prop, target: g[0].target, reference: g[0].reference, severity: 'high', suggestedChange: `${g[0].sc} — applies to ${g.length} containers (one responsive root cause)` });
      }

      // ---- (c) PER-WIDTH findings at 390 / 768: run a focused MODE-B diff at each mobile width ----
      // (a thin re-diff: reuse THIS diff() on the per-width ref/target analyses, then re-tag the
      // findings' class with a width prefix so they don't drown the 1280 set; cap per width.)
      for (const w of [390, 768]) {
        if (!refW[w] || !tgtW[w]) continue;
        let sub = null;
        try {
          // diff() reads module-level GEOM from frame match; per-width frames match (same viewport) → geometry on.
          // _inResponsive is set, so this recursive call skips the responsive pass (no infinite loop).
          sub = diff(refW[w], tgtW[w]);
        } catch (e) { sub = null; }
        if (!sub || !sub.findings) continue;
        // surface the highest-signal mobile findings only (structure/layout/container/responsive),
        // capped, so the 1280 report stays the centre of gravity.
        const keep = sub.findings.filter(f => ['layout', 'structure', 'container-bg', 'gradient', 'border', 'geometry'].includes(f.class) && f.severity !== 'low').slice(0, 10);
        for (const f of keep) {
          add({ locator: `@${w}px ${f.locator || ''}`.trim(), section: f.section, class: 'responsive', property: `${w}px-${f.property}`, target: f.target, reference: f.reference, ...(f.deltaPx != null ? { deltaPx: f.deltaPx } : {}), severity: f.severity, suggestedChange: `at ${w}px viewport: ${f.suggestedChange}` });
        }
      }
      diff._inResponsive = false;
    }

    // ============= SUMMARY + SORT =============
    const sevRank = { high: 0, med: 1, low: 2 };
    findings.sort((a, b) => (sevRank[a.severity] - sevRank[b.severity]) || ((b.deltaPx || 0) - (a.deltaPx || 0)));
    const byClass = {};
    for (const f of findings) byClass[f.class] = (byClass[f.class] || 0) + 1;
    const bySev = { high: 0, med: 0, low: 0 };
    for (const f of findings) bySev[f.severity]++;
    // SCORE 0–100 (v2.0.1 — saturating, DISCRIMINATING). The old `100 − penalty` cliff hit 0 for any
    // full-page web↔web diff (a single page has hundreds of weighted points), so every page scored 0/100
    // and the metric could not rank pages or track progress. We instead map the weighted penalty through
    // an exponential decay `100·e^(−P/SCALE)`, which is monotonic, never hard-floors until P is enormous,
    // and spreads realistic full-page totals across the 5–85 band: a near-clean page (P≈150) ≈ 85, a
    // genuine page with ~350–450 findings (P≈900–1100) ≈ 28–34, a very-divergent page (P≈1800) ≈ 9.
    // Weights unchanged (high=5, med=2, low=0.5) so the relative cost of severities is preserved.
    const penalty = bySev.high * 5 + bySev.med * 2 + bySev.low * 0.5;
    const SCORE_SCALE = 900;
    const score = Math.max(1, Math.round(100 * Math.exp(-penalty / SCORE_SCALE)));

    // ============= INCONCLUSIVE CLASSES =============
    // The third value. A finding says "these differ"; zero findings in a class says "these agree" —
    // but only if the class could run. Every class the preflight switched off is listed here with the
    // verbatim reason and the detector classes it silences, so a reader and an exit code can both tell
    // a clean report from an unasked question. `detectors` names what a human must now check elsewhere.
    const SILENCED = {
      shadow: ['shadow/box-shadow', 'shadow/illo-box-shadow', 'value/shadow-precision'],
      gradient: ['gradient/*', 'container-bg/bg-image', 'value/gradient-signature'],
      textTransform: ['font/text-transform'],
      transition: ['animation/transition-presence'],
      animation: ['animation/animation-presence'],
      flexShorthand: ['layout/flex-grow', 'layout/flex-basis'],
      pseudoElements: ['border/pseudo-*', 'container-bg/pseudo-*', 'shadow/pseudo-*', 'pseudo/content (missing bullets and counters)', 'the ::after border fold feeding border/border-top-width'],
      placeholder: ['font/placeholder-color'],
      svgGlyphExtent: ['icon/icon-glyph-w', 'icon/icon-glyph-h', 'icon/button-arrow-glyph-size'],
    };
    const inconclusive = [];
    for (const key of Object.keys(SILENCED)) {
      const rc = rCaps[key], tc = tCaps[key];
      // Absent capabilities (an artifact captured before the preflight existed) are themselves
      // inconclusive — an unprobed engine is not a proven one.
      const sides = [];
      if (!rc) sides.push('reference (not probed)'); else if (!rc.available) sides.push('reference');
      if (!tc) sides.push('target (not probed)'); else if (!tc.available) sides.push('target');
      if (!sides.length) continue;
      inconclusive.push({
        capability: key,
        sides,
        detectors: SILENCED[key],
        reason: (tc && tc.reason) || (rc && rc.reason) || 'the capture carries no `capabilities` block, so this engine was never probed — re-capture with a current analyze.js.',
        ...(tc && tc.measured ? { measured: tc.measured } : {}),
      });
    }

    return {
      summary: {
        // COVERAGE IS NOT AGREEMENT. "every class that ran came back clean" and "this page matches"
        // are different claims, and a bare number cannot tell them apart: a score of 84 printed beside
        // nine unmeasured classes reads as 84% right. So the score is REPORTED WITH ITS DENOMINATOR —
        // `scoreCovers` says what fraction of the detector classes the score is even about, and
        // `scoreCaveat` says the rest in words. When classes are missing the number is not suppressed
        // (that would hide real progress between runs); it is qualified so it cannot be quoted alone.
        score,
        scoreCovers: (() => {
          const total = Object.keys(SILENCED).length;
          const ran = total - inconclusive.length;
          return { detectorClassesProbed: total, ran, silenced: inconclusive.length, fraction: +(ran / total).toFixed(3) };
        })(),
        ...(inconclusive.length ? { scoreCaveat: `This score covers only the detector classes that could run. ${inconclusive.length} of ${Object.keys(SILENCED).length} probed classes were silenced by the engine (${inconclusive.map(i => i.capability).join(', ')}), so the run is INCONCLUSIVE, not ${score}% matching. Quote it with this sentence or not at all.` } : {}),
        totalFindings: findings.length,
        bySeverity: bySev,
        byClass,
        frame: { reference: refDoc.frame, target: appDoc.frame, sameViewport: !!sameViewport, geometry: !!GEOM },
        // A verdict that omits this is a verdict about an unknown fraction of the surface.
        conclusive: inconclusive.length === 0,
        inconclusiveCount: inconclusive.length,
        capabilities: { reference: rCaps, target: tCaps },
      },
      findings,
      inconclusive,
      noiseExcluded,
      analysis: appDoc,
    };
  }

  // RUNNER-INJECTED FEATURE-EFFECTIVENESS RESULTS (v2.1.0).
  // When canvas `fontFeatureSettings` is unsupported, the rendered-glyph-shape self-check needs a
  // screenshot pixel-diff of the probe pairs (see capture()'s runner-screenshot path + feature-check.mjs).
  // The runner pixel-diffs each pair and injects `globalThis.__MF_FEATURE_DIFFS__` — a map keyed by side
  // ('reference'/'target') OR a flat array — of { key, effective } verdicts. We fold each verdict into the
  // matching analysis.featureCheck.combos[].effective BEFORE the diff so MODE B can emit the finding.
  const mergeFeatureDiffs = (analysis, side) => {
    const inj = (typeof globalThis !== 'undefined' && globalThis.__MF_FEATURE_DIFFS__) || null;
    if (!inj || !analysis || !analysis.featureCheck || !analysis.featureCheck.combos) return;
    let list = Array.isArray(inj) ? inj : (inj[side] || inj.combos || null);
    if (!list && !Array.isArray(inj)) {
      // a flat object keyed by combo-key → verdict
      list = Object.keys(inj).map(k => ({ key: k, effective: inj[k] && (inj[k].effective ?? inj[k]) }));
    }
    if (!Array.isArray(list)) return;
    const byKey = new Map(list.map(v => [v.key, v]));
    for (const c of analysis.featureCheck.combos) {
      const v = byKey.get(c.key);
      if (v && typeof v.effective === 'boolean') c.effective = v.effective;
      else if (v && typeof v.effective === 'number') c.effective = v.effective > 0; // pctDifferent>0 ⇒ effective
    }
  };

  // ======================================================================
  // ENTRYPOINT
  // ======================================================================
  const targetAnalysis = await capture();
  let result;
  if (REFERENCE) {
    // MODE B — the reference may be the analysis object, or { analysis }, or double-wrapped string.
    let ref = REFERENCE;
    if (typeof ref === 'string') { try { ref = JSON.parse(ref); } catch (e) {} }
    if (ref && ref.analysis && ref.analysis.nodes) ref = ref.analysis; // a saved MODE-B result → use its analysis
    mergeFeatureDiffs(ref, 'reference');
    mergeFeatureDiffs(targetAnalysis, 'target');
    result = diff(ref, targetAnalysis);
  } else {
    // MODE A — full analysis of the current page.
    result = targetAnalysis;
  }
  return JSON.stringify(result);
})()
