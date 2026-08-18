/**
 * probes.js — deterministic in-page probes for design review.
 *
 * Everything here reads the DOM at rest. That is the limit of what it can see:
 * an entrance has finished, a transient overlay is opacity 0. Motion bugs and
 * mid-transition defects need frame capture, not this file.
 *
 * "At rest" is a precondition, not an assumption. Scroll the whole document and
 * drain `document.getAnimations()` BEFORE calling `runAll()` — a scroll-reveal
 * system leaves most of a long page hidden and lazy images unloaded, and a
 * colour probe sampled mid-entrance returns confident, precise, wrong numbers.
 * `runAll().settled` records whether that actually happened.
 *
 * Usage (CDP, against `obscura serve`):
 *   const probes = fs.readFileSync('probes.js', 'utf8');
 *   await send('Runtime.evaluate', { expression: probes }, sessionId);
 *   const r = await send('Runtime.evaluate',
 *     { expression: 'JSON.stringify(window.__designReviewProbes.runAll())',
 *       returnByValue: true, awaitPromise: true }, sessionId);
 *
 * Every probe returns plain JSON-serialisable data. No findings, no judgment —
 * later stages reason over this.
 */
(function () {
  'use strict';

  const MAX_NODES = 4000;

  function cssPath(el) {
    if (!el || el.nodeType !== 1) return '';
    if (el.id) return `#${el.id}`;
    const parts = [];
    let node = el;
    while (node && node.nodeType === 1 && parts.length < 6) {
      let seg = node.tagName.toLowerCase();
      if (node.classList.length) {
        seg += '.' + [...node.classList].slice(0, 2).join('.');
      }
      const parent = node.parentElement;
      if (parent) {
        const sameTag = [...parent.children].filter(c => c.tagName === node.tagName);
        if (sameTag.length > 1) seg += `:nth-of-type(${sameTag.indexOf(node) + 1})`;
      }
      parts.unshift(seg);
      node = node.parentElement;
    }
    return parts.join(' > ');
  }

  function visible(el) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    // An entry animation that starts at `opacity: 0` is stranded part-way on an
    // engine that never runs it: measured at 0.03 and frozen there forever, not
    // at 0. So an exact `=== 0` test lets a stranded element through into every
    // geometric probe, where it looks exactly like a z-index bug. Anything under
    // 0.05 is treated as not visible and counted, because a real design does not
    // ship 3%-opacity text and the alternative is a page of invented overlaps.
    const op = parseFloat(cs.opacity);
    if (!(op > 0.05)) return false;
    // Content inside a collapsed <details>, or skipped by content-visibility,
    // still returns a non-zero rect in Chrome. Every probe that reasons about
    // geometry has to exclude it or it invents overlaps that no user can see.
    if (el.closest && el.closest('details:not([open])')) return false;
    // Behind an open dialog. A drawer or modal marks the page inert, and text
    // under a scrim is not overlapping the text on top of it — it is in a
    // different stacking layer and nobody sees both.
    if (el.closest && el.closest('[inert]')) return false;
    if (typeof el.checkVisibility === 'function' &&
        !el.checkVisibility({ contentVisibilityAuto: true,
                              opacityProperty: true, visibilityProperty: true })) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }

  /**
   * Elements this engine stranded rather than the page hiding.
   *
   * An `opacity: 0` entry keyframe leaves its element at ~0.0036 on a read taken
   * before the document has been scrolled and settled (after it, the same element
   * reads 1 — the value is provisional, not permanent),
   * which is a false-positive source in both directions: it reads as a defect
   * that is really an engine artifact, and it reads as visible to any test using
   * an exact zero. Reported as its own population so a reviewer can tell a
   * stranded entrance from a genuinely hidden element.
   */
  function probeStrandedElements() {
    const stranded = [];
    for (const el of [...document.querySelectorAll('body *')].slice(0, MAX_NODES)) {
      const cs = getComputedStyle(el);
      const op = parseFloat(cs.opacity);
      if (op > 0 && op <= 0.05) {
        stranded.push({ selector: cssPath(el), opacity: cs.opacity,
                        text: (el.textContent || '').trim().slice(0, 40) });
      }
      if (stranded.length >= 40) break;
    }
    return {
      count: stranded.length,
      sample: stranded,
      note: stranded.length
        ? 'Near-zero but non-zero opacity. On an engine that does not execute animations this is usually a stranded entry keyframe, not a design defect — and it is excluded from geometric probes.'
        : null,
    };
  }

  /* ---------------------------------------------- engine capability */

  /**
   * Which CSS channels this engine will actually answer.
   *
   * The rule this file enforces everywhere, and the one it used to apply to
   * exactly one layer: **a check whose "pass" and "cannot run" look identical
   * must report which one it is.** Six metrics here read channels that return
   * `""` or `0px` on the review engine whatever the CSS says. Five of them
   * therefore reported clean forever. The sixth was worse: `probeContrast`
   * guarded the unresolvable-backdrop case with `if (cs.backgroundImage &&
   * cs.backgroundImage !== 'none')`, an empty string is falsy, so the guard
   * never fired, the ancestor walk climbed past the gradient to the opaque
   * white `body`, and white 72px display type on a purple gradient was
   * reported at **1.0:1** — a fabricated Tier 1 Blocker, with `bgAssumed:
   * false` beside it.
   *
   * Measured 18 Aug 2026 against `evals/fixtures/landing.html` on obscura
   * 0.2.0: five of seven reported contrast failures on that fixture were scored
   * against `rgb(255,255,255)` on a purple gradient, `skipped` was 0, and
   * `bgAssumed` was false on all seven. One of the five — the h1 — does not fail
   * at all (worst stop 3.53:1 against a 3.0 floor); the other four are real
   * failures whose ratios were wrong by 1.9 to 2.5 points.
   *
   * So capability is **measured, not assumed**, against a scratch element whose
   * values this function sets itself. Ground truth is known, so an answer that
   * disagrees with it is an unreadable channel rather than a surprising page.
   * Measuring beats hardcoding for two reasons: an engine that gains a property
   * is believed the day it does, and a different engine is characterised
   * without editing this file.
   *
   * **The ground truth is planted through a stylesheet, never inline, and that
   * detail is the whole measurement.** Measured 18 Aug 2026 on obscura 0.2.0:
   * this engine hands back an inline declaration verbatim without resolving it,
   * and resolves a stylesheet-set property properly — which for these
   * properties means empty or zero. The same element, same values, two routes:
   *
   *   property            inline        via stylesheet
   *   background-image    the gradient  `""`
   *   border-radius       `24px`        `0px`
   *   text-transform      `uppercase`   `""`
   *   box-shadow          the shadow    `""`
   *   gap                 `13px`        `normal`
   *   padding             `16px`        `0px`
   *
   * A first version of this probe set its values inline and concluded the engine
   * could read all six. Real pages use stylesheets, so that reading would have
   * disabled every fallback below on exactly the pages that need it. It is the
   * same lesson the browser-drivers reference already carries about CDP — assert
   * the observable the way the page will actually produce it.
   */
  function probeEngineCapability() {
    const CLS = '__drCapProbe';
    const sheet = document.createElement('style');
    sheet.textContent = `.${CLS}{` + [
      'position:absolute', 'left:-99999px', 'top:0', 'width:40px', 'height:40px',
      'padding:16px', 'margin:40px', 'border:1px solid #123456', 'border-radius:24px',
      'box-shadow:0 8px 32px rgba(0,0,0,0.18)', 'text-transform:uppercase',
      'background-image:linear-gradient(90deg,#000000,#ffffff)',
      'outline:2px solid #654321', 'display:flex', 'flex:1 1 auto', 'gap:13px',
      'transition:all 0.3s ease-in', 'letter-spacing:1px', 'font-size:17px',
      'background-color:rgb(1,2,3)', 'color:rgb(4,5,6)',
    ].join(';') + `}.${CLS}::after{content:"CAPOK"}`;
    document.head.appendChild(sheet);

    const probe = document.createElement('div');
    probe.setAttribute('aria-hidden', 'true');
    probe.className = CLS;
    const child = document.createElement('span');
    child.textContent = 'Xx';
    probe.appendChild(child);
    document.body.appendChild(probe);

    const cs = getComputedStyle(probe);
    const nonEmpty = v => typeof v === 'string' && v.trim() !== '';
    const px = v => nonEmpty(v) && parseFloat(v) > 0;
    // A shorthand answering `0px` against a 16px padding is not reporting the
    // padding — it is reporting that it does not compose. That is the whole
    // reason the test plants a known value instead of reading a real page.
    const ch = (name, ok) => {
      let raw;
      try { raw = cs[name]; } catch (e) { raw = undefined; }
      return { got: raw === undefined ? null : String(raw), readable: !!ok(raw) };
    };

    const channels = {
      backgroundImage: ch('backgroundImage', v => nonEmpty(v) && v !== 'none'),
      boxShadow: ch('boxShadow', v => nonEmpty(v) && v !== 'none'),
      textTransform: ch('textTransform', v => nonEmpty(v) && v !== 'none'),
      outline: ch('outline', nonEmpty),
      outlineWidth: ch('outlineWidth', px),
      flex: ch('flex', nonEmpty),
      flexGrow: ch('flexGrow', nonEmpty),
      borderRadius: ch('borderRadius', px),
      borderTopLeftRadius: ch('borderTopLeftRadius', px),
      borderWidth: ch('borderWidth', px),
      borderTopWidth: ch('borderTopWidth', px),
      padding: ch('padding', px),
      paddingTop: ch('paddingTop', px),
      margin: ch('margin', px),
      marginTop: ch('marginTop', px),
      gap: ch('gap', px),
      rowGap: ch('rowGap', px),
      columnGap: ch('columnGap', px),
      transitionProperty: ch('transitionProperty', nonEmpty),
      transitionDuration: ch('transitionDuration', v => nonEmpty(v) && parseFloat(v) > 0),
      // The shorthand is probed too, and it needs a stricter test than
      // "non-empty": this engine answers `none` for it, which is a resolved
      // value that carries no transition and would be trusted by any
      // emptiness check. Demand the duration we planted.
      transition: ch('transition', v => nonEmpty(v) && /0\.3s|300ms/.test(v)),
      letterSpacing: ch('letterSpacing', px),
      fontSize: ch('fontSize', px),
      color: ch('color', nonEmpty),
      backgroundColor: ch('backgroundColor', nonEmpty),
      // `borderColor` resolves to `rgb(0, 0, 0)` on every node here whether or
      // not a border colour is set, which is the same failure as an empty string
      // wearing a plausible value: non-empty, parseable, and not a measurement.
      // A truthiness test passes it, so the planted colour is the test.
      borderColor: ch('borderColor', v => nonEmpty(v) && /18,\s*52,\s*86|#123456/i.test(v)),
      borderTopColor: ch('borderTopColor', v => nonEmpty(v) && /18,\s*52,\s*86|#123456/i.test(v)),
    };

    // Pseudo-element content. A gate reading `::after` content to check an icon
    // or a required-field marker gets `""` here whether or not one is set. The
    // rule is already in the scratch sheet, planted the same way a page would.
    let pseudoContent = { got: null, readable: false };
    try {
      const got = getComputedStyle(probe, '::after').content;
      pseudoContent = { got: got === undefined ? null : String(got),
                        readable: typeof got === 'string' && got.indexOf('CAPOK') !== -1 };
    } catch (e) { /* leave unreadable */ }

    // The fallback channel gets the same treatment as the channels it covers.
    // Assuming the fallback works is the same mistake one level down.
    let declarationChannel = { readable: false, note: 'CSSOM style accessors not verified' };
    try {
      const style = document.createElement('style');
      style.textContent = '.__drCapDecl{text-transform:uppercase;background:linear-gradient(90deg,#000,#fff)}';
      document.head.appendChild(style);
      const sheet = style.sheet;
      const rule = sheet && sheet.cssRules && sheet.cssRules[0];
      const tt = rule && rule.style ? rule.style.textTransform : '';
      const bg = rule && rule.style ? (rule.style.background || rule.style.backgroundImage) : '';
      declarationChannel = {
        readable: tt === 'uppercase' && /linear-gradient/.test(String(bg)),
        selectorText: rule ? rule.selectorText : null,
        textTransform: tt || null,
        background: bg || null,
        note: 'Declared values read from document.styleSheets, used where a computed channel is unreadable.',
      };
      style.remove();
    } catch (e) { declarationChannel.error = String(e && e.message); }

    // SVG path geometry. Returns an all-zero box on this engine and does NOT
    // throw, so a try/catch is no defence — the zero has to be recognised.
    let svgBBox = { readable: false, got: null };
    try {
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      path.setAttribute('d', 'M0 0 L 40 0 L 40 40 Z');
      svg.appendChild(path);
      probe.appendChild(svg);
      const b = path.getBBox();
      svgBBox = { readable: !!(b && b.width > 0 && b.height > 0),
                  got: b ? `${b.width}x${b.height}` : null };
    } catch (e) { svgBBox.error = String(e && e.message); }

    probe.remove();
    sheet.remove();

    // Media emulation. `Emulation.setEmulatedMedia` is accepted and inert here,
    // so the print and reduced-motion passes are impossible rather than clean.
    // A CDP method returning without an error proves only that it was accepted.
    const media = {
      printEmulated: (() => { try { return matchMedia('print').matches; } catch (e) { return null; } })(),
      reducedMotionQuerySupported: (() => {
        try { return matchMedia('(prefers-reduced-motion: reduce)').media !== 'not all'; }
        catch (e) { return null; }
      })(),
      reducedMotionActive: (() => {
        try { return matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return null; }
      })(),
      widthQueryWorks: (() => {
        try { return matchMedia('(min-width: 1px)').matches && !matchMedia('(min-width: 99999px)').matches; }
        catch (e) { return null; }
      })(),
    };

    // Animation execution. Declare one, then ask whether it is running. Zero
    // here is the absence of a signal, never a settled page.
    let animation = { readable: false, got: null };
    try {
      const style = document.createElement('style');
      style.textContent = '@keyframes __drCapSpin{from{opacity:.2}to{opacity:1}}' +
                          '.__drCapAnim{animation:__drCapSpin 9s linear infinite}';
      document.head.appendChild(style);
      const a = document.createElement('div');
      a.className = '__drCapAnim';
      a.setAttribute('aria-hidden', 'true');
      a.style.cssText = 'position:absolute;left:-99999px;width:10px;height:10px';
      document.body.appendChild(a);
      const n = document.getAnimations ? document.getAnimations().length : -1;
      animation = { readable: n > 0, got: n, note: n > 0 ? null : 'CSS animations do not execute on this engine' };
      a.remove(); style.remove();
    } catch (e) { animation.error = String(e && e.message); }

    // Web fonts. A loaded face and a 404'd one measure identically here, so the
    // whole font-fidelity class is unavailable rather than zero-divergence.
    const fonts = (() => {
      try {
        if (!document.fonts) return { readable: false, got: 'no document.fonts' };
        const faces = [...document.fonts];
        const loaded = faces.filter(f => f.status === 'loaded').length;
        return { readable: faces.length === 0 || loaded > 0,
                 declaredFaces: faces.length, loadedFaces: loaded,
                 note: faces.length && !loaded ? 'every @font-face stayed unloaded' : null };
      } catch (e) { return { readable: false, got: String(e && e.message) }; }
    })();

    const unreadable = Object.keys(channels).filter(k => !channels[k].readable);
    if (!pseudoContent.readable) unreadable.push('::after content');
    if (!svgBBox.readable) unreadable.push('SVG getBBox');
    if (!animation.readable) unreadable.push('CSS animation execution');
    if (!fonts.readable) unreadable.push('web font loading');
    if (media.printEmulated === false) unreadable.push('print media emulation');

    return {
      channels,
      pseudoContent,
      declarationChannel,
      svgBBox,
      media,
      animation,
      fonts,
      // The headline number. A reviewer reading a probe dump should not have to
      // work out which of its zeros are real.
      unreadableCount: unreadable.length,
      unreadable,
      note: 'readable:false means the engine does not answer this question. It never means the CSS is absent.',
    };
  }

  /* ------------------------------------------- declared-style fallback */

  /**
   * Selector-to-declaration index, built from the stylesheets the page actually
   * loaded. This is the witness for every property whose computed channel this
   * engine does not implement.
   *
   * It is the trick `probeFocusStyles()` already used for `outline` and
   * `box-shadow` and that nothing else in this file applied. Measured 18 Aug
   * 2026 on obscura 0.2.0, the declared channel answers every property the
   * computed channel drops: `.hero` background reads
   * `linear-gradient(135deg,#6366F1,#A855F7,#EC4899)`, `.eyebrow`
   * text-transform reads `uppercase`, `.card` box-shadow reads
   * `0 8px 32px rgba(0,0,0,.18)`, `.btn` transition reads `all 0.3s ease-in`,
   * `.grid` gap reads `13px` — and computed `gap`, `rowGap` and `columnGap` are
   * all `normal` on that same element, so gap has no longhand escape.
   *
   * Two structural facts about this engine's CSSOM, both measured, both
   * load-bearing:
   *
   * - A top-level rule is a real `CSSStyleRule`: `selectorText` and the `style`
   *   accessors work exactly. No parsing needed for the common case.
   * - An `@media` or `@supports` block is a bare `CSSRule` with `type: 0`, no
   *   `conditionText`, no `media`, no `cssRules` and no `style` — but `cssText`
   *   carries the whole block verbatim. So at-rules are recovered by parsing
   *   `cssText` and gating the condition with `matchMedia`, which does work for
   *   width queries. An earlier read of this concluded at-rules were dropped
   *   entirely; they are not, they are unmodelled, and the difference is a
   *   whole class of responsive declarations.
   *
   * **A declaration is not a rendering.** It says what the author asked for;
   * the computed value says what the cascade resolved. On an engine that
   * answers both they agree, and where they disagree the computed value wins.
   * Every value sourced here is tagged `declared` so a finding built on it can
   * be read for what it is, and so nobody quotes it as a measurement.
   */
  function buildDeclaredIndex() {
    const PROPS = ['background', 'background-image', 'background-color', 'box-shadow',
                   'text-transform', 'transition', 'transition-property',
                   'transition-duration', 'gap', 'row-gap', 'column-gap',
                   'border-radius', 'border-width', 'letter-spacing', 'outline'];
    const camel = p => p.replace(/-([a-z])/g, (m, c) => c.toUpperCase());
    // Source order is the tie-break the cascade uses at equal specificity, so
    // rules are kept in the order they were read and the last match wins.
    const rules = [];
    let sheetsRead = 0, sheetsUnreadable = 0, atRulesParsed = 0, rulesUnparsed = 0;
    let atRuleConditionsSkipped = 0;

    const addDecl = (selectorText, styleLike, under) => {
      if (!selectorText) return;
      const decls = {};
      let any = false;
      for (const p of PROPS) {
        let v = '';
        try {
          v = typeof styleLike.getPropertyValue === 'function'
            ? styleLike.getPropertyValue(p) : (styleLike[camel(p)] || '');
        } catch (e) { v = ''; }
        if (v && String(v).trim()) { decls[camel(p)] = String(v).trim(); any = true; }
      }
      if (any) rules.push({ selectorText, decls, under: under || null });
    };

    // Minimal declaration parser, used ONLY for at-rule bodies this engine does
    // not model. Deliberately not a CSS parser: it splits `sel { a:b; c:d }`
    // blocks and nothing else, because that is all the recovered text contains.
    const parseBlocks = (css, under) => {
      const re = /([^{}]+)\{([^{}]*)\}/g;
      let m;
      while ((m = re.exec(css))) {
        const sel = m[1].trim();
        if (!sel || sel.charAt(0) === '@') continue;
        const body = m[2];
        const bag = {};
        for (const part of body.split(';')) {
          const i = part.indexOf(':');
          if (i < 1) continue;
          const prop = part.slice(0, i).trim().toLowerCase();
          const val = part.slice(i + 1).trim();
          if (val) bag[prop] = val;
        }
        addDecl(sel, { getPropertyValue: p => bag[p] || '' }, under);
      }
    };

    for (let i = 0; i < document.styleSheets.length; i++) {
      const ss = document.styleSheets[i];
      let cssRules = null;
      try { cssRules = ss.cssRules; } catch (e) { cssRules = null; }
      if (!cssRules) { sheetsUnreadable++; continue; }
      sheetsRead++;
      for (let j = 0; j < cssRules.length; j++) {
        const r = cssRules[j];
        if (r.type === 1 && r.style && r.selectorText) {
          addDecl(r.selectorText, r.style, null);
          continue;
        }
        // Unmodelled group rule. `cssText` is the only witness.
        const text = (() => { try { return String(r.cssText || ''); } catch (e) { return ''; } })();
        const at = text.match(/^\s*@(media|supports)\s*([^{]*)\{([\s\S]*)\}\s*$/);
        if (at) {
          const kind = at[1], cond = at[2].trim(), body = at[3];
          let applies = null;
          if (kind === 'media') {
            try { applies = matchMedia(cond).matches; } catch (e) { applies = null; }
          } else {
            try { applies = CSS && CSS.supports ? CSS.supports(cond.replace(/^\(|\)$/g, '')) : null; }
            catch (e) { applies = null; }
          }
          if (applies === true) { parseBlocks(body, `@${kind} ${cond}`); atRulesParsed++; }
          else if (applies === false) { atRulesParsed++; }
          else { atRuleConditionsSkipped++; }
          continue;
        }
        if (r.style && r.selectorText) { addDecl(r.selectorText, r.style, null); continue; }
        // @font-face, @keyframes, @import and friends carry no declarations we
        // index. Counted so the denominator is real rather than implied.
        if (!/^\s*@(font-face|keyframes|import|charset|namespace|page|layer|property)/i.test(text)) {
          rulesUnparsed++;
        }
      }
    }

    /** Last matching declaration wins, inline style beats every stylesheet. */
    function declaredValue(el, prop) {
      const key = camel(prop);
      try {
        const inline = el.style && el.style.getPropertyValue ? el.style.getPropertyValue(prop) : '';
        if (inline && inline.trim()) return { value: inline.trim(), from: 'inline' };
      } catch (e) { /* fall through */ }
      let hit = null;
      for (const r of rules) {
        if (!(key in r.decls)) continue;
        let matches = false;
        try { matches = el.matches(r.selectorText); } catch (e) { matches = false; }
        if (matches) hit = { value: r.decls[key], from: r.under ? `sheet ${r.under}` : 'sheet',
                             selector: r.selectorText };
      }
      return hit;
    }

    /** Resolve a `var(--x)` reference off the element it applies to. */
    function resolveVars(el, value) {
      if (!value || value.indexOf('var(') === -1) return value;
      let out = value, guard = 0;
      const cs = getComputedStyle(el);
      while (out.indexOf('var(') !== -1 && guard++ < 8) {
        out = out.replace(/var\(\s*(--[\w-]+)\s*(?:,([^()]*))?\)/g, (m, name, fallback) => {
          let v = '';
          try { v = cs.getPropertyValue(name); } catch (e) { v = ''; }
          v = (v || '').trim();
          return v || (fallback || '').trim() || m;
        });
        if (/var\(/.test(out) && guard >= 8) break;
      }
      return out;
    }

    return {
      declaredValue,
      resolveVars,
      stats: {
        sheetsRead, sheetsUnreadable, indexedRules: rules.length,
        atRulesParsed, atRuleConditionsSkipped, rulesUnparsed,
        // The unmeasurable population for this channel. A cross-origin sheet
        // makes every declaration in it invisible, and that is a coverage gap
        // rather than an absence of declarations.
        partial: sheetsUnreadable > 0 || atRuleConditionsSkipped > 0 || rulesUnparsed > 0,
      },
    };
  }

  // Built once per run. `runAll()` refreshes it; a direct probe call builds it
  // lazily so calling one probe from the console still works.
  let DECLARED = null;
  let CAPABILITY = null;
  function declared() { if (!DECLARED) DECLARED = buildDeclaredIndex(); return DECLARED; }
  function capability() { if (!CAPABILITY) CAPABILITY = probeEngineCapability(); return CAPABILITY; }

  /**
   * Build both indexes and return the capability report.
   *
   * A runner calling probes one at a time (which is how a probe that overruns
   * costs its own key instead of the whole review) needs the caches populated
   * once, deliberately, rather than by whichever probe happens to run first.
   * Returns the capability so this doubles as the roster's first entry.
   */
  function initRun() {
    CAPABILITY = probeEngineCapability();
    DECLARED = buildDeclaredIndex();
    return Object.assign({}, CAPABILITY, { declaredIndex: DECLARED.stats });
  }

  /**
   * The value of `prop` on `el`, and where it came from.
   *
   * Computed first, because it is the resolved cascade. Declared second, and
   * only when the engine has been measured unable to answer the computed
   * channel — never as a general-purpose second opinion, which would let a
   * declaration override a computed value that disagreed with it.
   *
   * Returns `{ value, source }` where source is `computed`, `declared` or
   * `unreadable`. `unreadable` is the state this whole mechanism exists to make
   * visible: it is not `null`, not `""`, and not zero.
   */
  function styleValue(el, prop, computedKey) {
    const cap = capability();
    const key = computedKey || prop.replace(/-([a-z])/g, (m, c) => c.toUpperCase());
    const chan = cap.channels[key];
    if (!chan || chan.readable) {
      let v = '';
      try { v = getComputedStyle(el)[key]; } catch (e) { v = ''; }
      if (v !== undefined && v !== null && String(v).trim() !== '') {
        return { value: String(v), source: 'computed' };
      }
      // A readable channel returning empty on this element is a real absence.
      if (chan && chan.readable) return { value: null, source: 'computed' };
    }
    if (!cap.declarationChannel.readable) {
      return { value: null, source: 'unreadable', reason: 'computed channel and declared channel both unavailable' };
    }
    const d = declared().declaredValue(el, prop);
    if (!d) {
      // Nothing declared for it anywhere the index could see. That is an
      // absence only if the index was complete.
      return declared().stats.partial
        ? { value: null, source: 'unreadable', reason: 'no declaration found and the declaration index is partial' }
        : { value: null, source: 'declared', absent: true };
    }
    return { value: declared().resolveVars(el, d.value), source: 'declared',
             selector: d.selector, from: d.from };
  }

  /* ---------------------------------------------------------------- colour */

  function parseColor(str) {
    if (!str) return null;
    const m = str.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const parts = m[1].split(/[,\s/]+/).filter(Boolean).map(Number);
    if (parts.length < 3 || parts.some(Number.isNaN)) return null;
    return { r: parts[0], g: parts[1], b: parts[2], a: parts.length > 3 ? parts[3] : 1 };
  }

  function srgbToLin(c) {
    const s = c / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  }

  function relLuminance(c) {
    return 0.2126 * srgbToLin(c.r) + 0.7152 * srgbToLin(c.g) + 0.0722 * srgbToLin(c.b);
  }

  function composite(fg, bg) {
    // fg over bg, both {r,g,b,a}
    const a = fg.a;
    return {
      r: fg.r * a + bg.r * (1 - a),
      g: fg.g * a + bg.g * (1 - a),
      b: fg.b * a + bg.b * (1 - a),
      a: 1,
    };
  }

  /**
   * Colour stops out of a gradient declaration.
   *
   * A gradient is not one backdrop, it is a range of them, and WCAG's ratio has
   * to hold everywhere the text actually sits. So the honest reduction is the
   * **worst stop**, not an average and not the first one: a white heading over
   * `#6366F1 → #A855F7 → #EC4899` is legible against all three, and a heading
   * that failed against only the lightest stop would still be a real failure at
   * that end of the sweep.
   *
   * This reads stops, not pixels. It cannot see where the sweep sits under a
   * given glyph, so it answers "is there any stop this text fails against",
   * which is the conservative direction. Positional stops, `color-mix()` and
   * image URLs are not reduced at all — those stay unresolved rather than
   * guessed.
   */
  function gradientStops(decl) {
    if (!decl) return null;
    const s = String(decl);
    if (!/gradient\(/i.test(s)) return null;
    const open = s.indexOf('(');
    const close = s.lastIndexOf(')');
    if (open < 0 || close < open) return null;
    const inner = s.slice(open + 1, close);
    // Split on top-level commas so `rgba(0,0,0,.5)` survives.
    const parts = [];
    let depth = 0, buf = '';
    for (const c of inner) {
      if (c === '(') depth++;
      if (c === ')') depth--;
      if (c === ',' && depth === 0) { parts.push(buf); buf = ''; continue; }
      buf += c;
    }
    if (buf.trim()) parts.push(buf);

    const stops = [];
    for (const raw of parts) {
      const p = raw.trim();
      if (!p) continue;
      // Direction / interpolation prefixes carry no colour.
      if (/^(to\b|-?[\d.]+(deg|rad|grad|turn)\b|at\b|circle\b|ellipse\b|closest|farthest|in\s)/i.test(p)) continue;
      const colourText = p.replace(/\s+-?[\d.]+(%|px|em|rem)\s*$/g, '')
                          .replace(/\s+-?[\d.]+(%|px|em|rem)\s+-?[\d.]+(%|px|em|rem)\s*$/g, '')
                          .trim();
      const c = parseNamedOrFunctional(colourText);
      if (c) stops.push(c);
    }
    return stops.length ? stops : null;
  }

  /**
   * A colour from a declaration rather than from a computed value. Declarations
   * carry hex and named forms that `parseColor()`'s rgb() matcher never sees.
   * Anything outside this set returns null and becomes unresolved, deliberately:
   * a wrong backdrop is what produced the fabricated Blocker in the first place.
   */
  function parseNamedOrFunctional(text) {
    if (!text) return null;
    const t = String(text).trim().toLowerCase();
    const rgb = parseColor(t);
    if (rgb) return rgb;
    let m = t.match(/^#([0-9a-f]{3,8})$/);
    if (m) {
      let h = m[1];
      if (h.length === 3 || h.length === 4) h = h.split('').map(c => c + c).join('');
      if (h.length !== 6 && h.length !== 8) return null;
      return { r: parseInt(h.slice(0, 2), 16), g: parseInt(h.slice(2, 4), 16),
               b: parseInt(h.slice(4, 6), 16),
               a: h.length === 8 ? parseInt(h.slice(6, 8), 16) / 255 : 1 };
    }
    const NAMED = {
      white: [255, 255, 255], black: [0, 0, 0], red: [255, 0, 0], green: [0, 128, 0],
      blue: [0, 0, 255], yellow: [255, 255, 0], gray: [128, 128, 128], grey: [128, 128, 128],
      silver: [192, 192, 192], navy: [0, 0, 128], teal: [0, 128, 128], purple: [128, 0, 128],
      orange: [255, 165, 0], transparent: null,
    };
    if (t in NAMED) {
      const v = NAMED[t];
      return v ? { r: v[0], g: v[1], b: v[2], a: 1 } : { r: 0, g: 0, b: 0, a: 0 };
    }
    return null;
  }

  /**
   * Walk ancestors to find the first opaque-enough background.
   *
   * Three outcomes, and keeping them apart is the point:
   *
   * - `color` — a resolved opaque backdrop. Safe to compute a ratio against.
   * - `range` — a gradient whose stops were recovered. Ratio is computed against
   *   the worst stop and the record says so.
   * - `unresolved` — the backdrop cannot be established. **This is not a pass
   *   and not a failure.** It goes into a reported population and gets looked
   *   at by eye. The old code reached this state and silently kept walking,
   *   which is how white-on-gradient became 1.0:1.
   *
   * The guard that used to fail: `if (cs.backgroundImage && cs.backgroundImage
   * !== 'none')`. An unreadable channel returns `""`, which is falsy, so an
   * image was indistinguishable from no image. Capability is consulted now
   * instead of truthiness.
   */
  function effectiveBackground(el) {
    const cap = capability();
    const bgImageReadable = cap.channels.backgroundImage.readable;
    let node = el;
    const stack = [];
    while (node && node.nodeType === 1 && node !== document.documentElement.parentElement) {
      const cs = getComputedStyle(node);
      const c = parseColor(cs.backgroundColor);

      // What is painted behind this node, image-wise. Computed first; declared
      // only where the computed channel has been measured unreadable.
      let imageDecl = null, imageSource = null;
      if (bgImageReadable) {
        const v = cs.backgroundImage;
        if (v && v !== 'none') { imageDecl = v; imageSource = 'computed'; }
      } else if (cap.declarationChannel.readable) {
        const d = declared().declaredValue(node, 'background-image') ||
                  declared().declaredValue(node, 'background');
        if (d) {
          const resolved = declared().resolveVars(node, d.value);
          if (/gradient\(|url\(|image-set\(/i.test(resolved)) {
            imageDecl = resolved; imageSource = 'declared';
          }
        }
      } else {
        // Neither channel answers. Every backdrop on this page is unconfirmable,
        // which is a whole-gate outcome rather than a per-element one.
        return { unresolved: 'background-image channel unreadable and no declaration index',
                 node: cssPath(node) };
      }

      if (imageDecl) {
        const stops = gradientStops(imageDecl);
        if (stops) {
          // Composite each stop under anything translucent already stacked over it.
          const flatten = (base) => {
            let out = base;
            for (let i = stack.length - 1; i >= 0; i--) out = composite(stack[i], out);
            return out;
          };
          return { range: stops.map(flatten), declaration: imageDecl.slice(0, 120),
                   source: imageSource, node: cssPath(node) };
        }
        return { unresolved: imageSource === 'declared'
                   ? 'background-image declared but not reducible to colour stops'
                   : 'background-image',
                 declaration: imageDecl.slice(0, 120), source: imageSource, node: cssPath(node) };
      }

      if (c && c.a > 0) {
        if (c.a >= 0.999) {
          let base = c;
          while (stack.length) base = composite(stack.pop(), base);
          return { color: base, node: cssPath(node) };
        }
        stack.push(c);
      }
      node = node.parentElement;
    }
    // Ran out of ancestors with nothing opaque. The canvas is the user agent's,
    // conventionally white, and that assumption is carried on the record.
    let base = { r: 255, g: 255, b: 255, a: 1 };
    while (stack.length) base = composite(stack.pop(), base);
    return { color: base, assumed: true };
  }

  function contrastRatio(a, b) {
    const l1 = relLuminance(a);
    const l2 = relLuminance(b);
    const light = Math.max(l1, l2);
    const dark = Math.min(l1, l2);
    return (light + 0.05) / (dark + 0.05);
  }

  /**
   * Text contrast. WCAG 2.2: 4.5:1 normal, 3:1 large.
   * Large = >=24px, or >=18.66px at weight >=700.
   * Thresholds are inclusive with no rounding — 4.499 fails.
   *
   * Returns an object, not an array. The array form could only carry failures,
   * so "no failures" and "the probe never ran" serialised identically, and an
   * element whose backdrop could not be resolved had nowhere to go but into the
   * failure list or into silence. Four populations now, and they sum to
   * `examined`:
   *
   *   failures + passes + unresolved + assumed-backdrop passes/failures
   *
   * `unresolved` is the one that matters. It is the honest home for a gradient
   * this engine will not reduce, and it must reach the report as a number — a
   * gate that quietly drops the cases it could not judge is reporting a
   * denominator it did not measure.
   */
  function probeContrast() {
    const failures = [];
    const unresolved = [];
    const ratios = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const seen = new Set();
    let n, examined = 0, passes = 0, assumedBackdrop = 0, gradientJudged = 0;

    while ((n = walker.nextNode()) && examined < 600) {
      const text = n.textContent.trim();
      if (!text) continue;
      const el = n.parentElement;
      if (!el || seen.has(el) || !visible(el)) continue;
      seen.add(el);
      const cs = getComputedStyle(el);
      const fg = parseColor(cs.color);
      if (!fg) continue;
      examined++;

      const bgInfo = effectiveBackground(el);
      const size = parseFloat(cs.fontSize);
      const weight = parseInt(cs.fontWeight, 10) || 400;
      const isLarge = size >= 24 || (size >= 18.66 && weight >= 700);
      const required = isLarge ? 3.0 : 4.5;

      if (bgInfo.unresolved) {
        unresolved.push({
          selector: cssPath(el), text: text.slice(0, 60), color: cs.color,
          fontSize: size, fontWeight: weight, isLarge, required,
          reason: bgInfo.unresolved,
          declaration: bgInfo.declaration || null,
          at: bgInfo.node || null,
          note: 'Backdrop not resolvable on this engine — confirm by eye against the capture. Not a pass and not a failure.',
        });
        continue;
      }

      // A gradient: score against the worst stop and say which.
      const candidates = bgInfo.range || [bgInfo.color];
      let worst = null;
      const allStops = [];
      for (const bg of candidates) {
        const fgFlat = fg.a < 0.999 ? composite(fg, bg) : fg;
        const ratio = contrastRatio(fgFlat, bg);
        allStops.push(Math.round(ratio * 100) / 100);
        if (!worst || ratio < worst.ratio) worst = { ratio, bg };
      }
      if (bgInfo.range) gradientJudged++;
      if (bgInfo.assumed) assumedBackdrop++;

      // Every examined element's ratio, pass or fail, and every stop of a
      // gradient rather than only the worst one.
      //
      // Recording failures alone made this probe unable to support its own
      // report. A review legitimately quotes a ratio for an element that
      // PASSED ("the body text is fine at 8.3:1") and legitimately quotes the
      // intermediate stops of a gradient it scored — and `audit_run.py claims`,
      // checking the report against the run, called both of those fabrications
      // because the run had not written them down. A gate that fires on correct
      // work is worse than no gate: it gets switched off, and then nothing is
      // checked. So the population the report may quote from is the population
      // the probe records.
      ratios.push({
        selector: cssPath(el),
        ratio: Math.round(worst.ratio * 100) / 100,
        stops: allStops.length > 1 ? allStops : undefined,
        required,
        passed: worst.ratio >= required,
      });

      if (worst.ratio < required) {
        failures.push({
          selector: cssPath(el),
          text: text.slice(0, 60),
          color: cs.color,
          background: `rgb(${Math.round(worst.bg.r)}, ${Math.round(worst.bg.g)}, ${Math.round(worst.bg.b)})`,
          fontSize: size, fontWeight: weight, isLarge,
          ratio: Math.round(worst.ratio * 100) / 100,
          stops: allStops.length > 1 ? allStops : undefined,
          required,
          // Where the backdrop came from, on every record. A ratio measured
          // against a declared gradient stop is a weaker claim than one
          // measured against a computed opaque colour, and the reader gets to
          // know which they are holding.
          backdropSource: bgInfo.range ? (bgInfo.source === 'declared' ? 'declared-gradient-stop'
                                                                      : 'computed-gradient-stop')
                        : bgInfo.assumed ? 'assumed-white-canvas' : 'computed',
          backdropStops: bgInfo.range ? bgInfo.range.length : undefined,
          // A gradient-stop failure that fails against EVERY stop is
          // unconditional; one that fails against some is conditional on where
          // the glyph sits. Severity follows this, so it is recorded rather
          // than re-derived.
          failsAllStops: allStops.every(r => r < required),
          declaration: bgInfo.declaration || undefined,
          bgAssumed: !!bgInfo.assumed,
        });
      } else {
        passes++;
      }
    }

    return {
      examined,
      failures,
      failureCount: failures.length,
      passCount: passes,
      // The full ratio population, so a report quoting a passing element's
      // ratio or an intermediate gradient stop is quoting the run.
      ratios,
      // The three numbers that used to be invisible.
      unresolved,
      unresolvedCount: unresolved.length,
      assumedBackdropCount: assumedBackdrop,
      gradientJudgedCount: gradientJudged,
      capped: examined >= 600,
      note: unresolved.length
        ? `${unresolved.length} of ${examined} text nodes have a backdrop this engine cannot resolve. They are neither passes nor failures and must be confirmed by eye.`
        : null,
    };
  }

  /* -------------------------------------------------------------- overflow */

  function probeOverflow() {
    const escaping = [];
    const all = [...document.querySelectorAll('*')].slice(0, MAX_NODES);
    for (const el of all) {
      const cs = getComputedStyle(el);
      if (cs.overflow !== 'visible') continue;
      if (el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1) {
        escaping.push({
          selector: cssPath(el),
          scrollWidth: el.scrollWidth, clientWidth: el.clientWidth,
          scrollHeight: el.scrollHeight, clientHeight: el.clientHeight,
        });
      }
    }
    return {
      pageOverflowsHorizontally: document.documentElement.scrollWidth > window.innerWidth,
      documentScrollWidth: document.documentElement.scrollWidth,
      innerWidth: window.innerWidth,
      escaping: escaping.slice(0, 60),
    };
  }

  /* ------------------------------------------------------------ image crop */

  /**
   * Rendered vs natural aspect ratio. An <img> carrying BOTH a height attribute
   * and a CSS aspect-ratio has two definite dimensions, so aspect-ratio is
   * ignored and the photo over-crops. Anything over ~1.4x is a heavy crop.
   */
  function probeImages() {
    return [...document.images]
      .filter(i => i.naturalWidth && i.naturalHeight)
      .map(i => {
        const r = i.getBoundingClientRect();
        if (!r.width || !r.height) return null;
        const rendered = r.width / r.height;
        const natural = i.naturalWidth / i.naturalHeight;
        const crop = Math.max(rendered / natural, natural / rendered);
        const cs = getComputedStyle(i);
        return {
          src: (i.currentSrc || i.src || '').slice(-100),
          selector: cssPath(i),
          renderedAR: Math.round(rendered * 100) / 100,
          naturalAR: Math.round(natural * 100) / 100,
          cropFactor: Math.round(crop * 100) / 100,
          objectFit: cs.objectFit,
          hasHeightAttr: i.hasAttribute('height'),
          cssAspectRatio: cs.aspectRatio,
          hasExplicitDims: i.hasAttribute('width') && i.hasAttribute('height'),
          heavyCrop: crop > 1.4,
        };
      })
      .filter(Boolean);
  }

  /* ----------------------------------------------------------- target size */

  /**
   * 24x24 CSS px is the WCAG 2.2 AA floor (2.5.8). 44x44 is AAA (2.5.5) and the
   * platform HIG bar. Under 24 is a failure; under 44 is a craft recommendation
   * on touch surfaces. The spacing exception is not evaluated here — an
   * undersized target can still pass 2.5.8 if a 24px exclusion circle does not
   * intersect its neighbours', so treat sub-24 hits as candidates to verify.
   */
  function probeTargets() {
    const sel = 'a[href], button, input, select, textarea, [role="button"], [role="link"], [role="checkbox"], [role="tab"], [onclick], [tabindex]:not([tabindex="-1"])';
    return [...document.querySelectorAll(sel)]
      .filter(visible)
      .map(el => {
        const r = el.getBoundingClientRect();
        return {
          selector: cssPath(el),
          tag: el.tagName.toLowerCase(),
          label: (el.getAttribute('aria-label') || el.textContent || '').trim().slice(0, 40),
          width: Math.round(r.width), height: Math.round(r.height),
          belowAA: r.width < 24 || r.height < 24,
          belowAAA: r.width < 44 || r.height < 44,
        };
      })
      .filter(t => t.belowAAA)
      .slice(0, 120);
  }

  /* -------------------------------------------------------------- semantics */

  function probeSemantics() {
    const headings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => ({
      level: Number(h.tagName[1]),
      text: h.textContent.trim().slice(0, 70),
      selector: cssPath(h),
    }));

    const skips = [];
    for (let i = 1; i < headings.length; i++) {
      if (headings[i].level - headings[i - 1].level > 1) {
        skips.push({ from: headings[i - 1].level, to: headings[i].level, at: headings[i].text });
      }
    }

    const imgs = [...document.images];
    const inputs = [...document.querySelectorAll('input, select, textarea')]
      .filter(i => i.type !== 'hidden');

    const unlabelled = inputs.filter(i => {
      if (i.getAttribute('aria-label') || i.getAttribute('aria-labelledby')) return false;
      if (i.id && document.querySelector(`label[for="${CSS.escape(i.id)}"]`)) return false;
      if (i.closest('label')) return false;
      return true;
    }).map(i => ({
      selector: cssPath(i),
      type: i.type,
      hasPlaceholder: !!i.placeholder,
      placeholderOnly: !!i.placeholder,
    }));

    const emptyLinks = [...document.querySelectorAll('a[href]')].filter(a =>
      !a.textContent.trim() && !a.getAttribute('aria-label') && !a.querySelector('img[alt]:not([alt=""])')
    ).map(a => ({ selector: cssPath(a), href: a.getAttribute('href') }));

    const emptyButtons = [...document.querySelectorAll('button, [role="button"]')].filter(b =>
      !b.textContent.trim() && !b.getAttribute('aria-label') && !b.getAttribute('aria-labelledby')
    ).map(b => ({ selector: cssPath(b) }));

    const divButtons = [...document.querySelectorAll('[role="button"], [onclick]')]
      .filter(el => !['BUTTON', 'A', 'INPUT'].includes(el.tagName))
      .map(el => ({
        selector: cssPath(el),
        tabindex: el.getAttribute('tabindex'),
        // A div with role=button and no key handler binds nothing. We cannot see
        // listeners from here, so surface it as needing a source check.
        needsKeyHandlerCheck: true,
      }));

    const positiveTabindex = [...document.querySelectorAll('[tabindex]')]
      .filter(el => Number(el.getAttribute('tabindex')) > 0)
      .map(el => ({ selector: cssPath(el), tabindex: el.getAttribute('tabindex') }));

    return {
      lang: document.documentElement.getAttribute('lang') || null,
      title: document.title || null,
      h1Count: headings.filter(h => h.level === 1).length,
      headingSkips: skips,
      headings: headings.slice(0, 80),
      landmarks: {
        main: document.querySelectorAll('main, [role="main"]').length,
        nav: document.querySelectorAll('nav, [role="navigation"]').length,
        header: document.querySelectorAll('header, [role="banner"]').length,
        footer: document.querySelectorAll('footer, [role="contentinfo"]').length,
      },
      images: { total: imgs.length, missingAlt: imgs.filter(i => !i.hasAttribute('alt')).length },
      unlabelledInputs: unlabelled,
      emptyLinks, emptyButtons, divButtons, positiveTabindex,
      skipLink: detectSkipLink(),
      labelValuePairs: probeLabelValuePairs(),
    };
  }

  /**
   * A skip link is the first focusable element and says where it goes. Any
   * `a[href^="#"]` is not enough — an empty `<a href="#">` anywhere on the page
   * matched that, which reported a skip link on pages with none.
   */
  function detectSkipLink() {
    const focusable = document.querySelector(
      'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    if (!focusable || focusable.tagName !== 'A') return false;
    const href = focusable.getAttribute('href') || '';
    if (!href.startsWith('#') || href === '#') return false;
    const text = (focusable.textContent || focusable.getAttribute('aria-label') || '').trim();
    if (!text) return false;
    // Must point at something that exists, or it skips nowhere.
    let target = null;
    try { target = document.querySelector(`#${CSS.escape(href.slice(1))}`); } catch { /* bad id */ }
    return { text: text.slice(0, 60), href, targetExists: !!target };
  }

  /**
   * On stat tiles and metadata rows the value outranks its label — the number
   * is the content and the label whispers. Inverted pairs are common and easy
   * to miss by eye, so measure rather than judge: find containers holding
   * exactly two text nodes, and compare their rendered size and weight.
   *
   * Reports pairs, not verdicts. Whether a given pair is genuinely a stat tile
   * is a judgment the reader makes with the crop in front of them.
   */
  function probeLabelValuePairs() {
    const pairs = [];
    // Match on structure, not class names. A stat tile is often a bare
    // `<div><span>Revenue</span><br><b>591</b></div>` with no useful class, so
    // selecting on [class*="stat"] finds the label and misses the container.
    const read = el => {
      const s = getComputedStyle(el);
      return {
        text: (el.textContent || '').trim().slice(0, 40),
        fontSize: parseFloat(s.fontSize),
        fontWeight: Number(s.fontWeight) || 400,
        tabularNums: /tabular-nums/.test(s.fontVariantNumeric),
      };
    };
    // Leading digit, currency symbol or sign — "£1,248.00", "591", "2.4%", "+12".
    const numeric = t => /^[^\p{L}]*[\d]/u.test(t.trim()) && /\d/.test(t);

    for (const c of document.querySelectorAll('body *')) {
      const kids = [...c.children].filter(el => (el.textContent || '').trim());
      if (kids.length !== 2) continue;
      const [a, b] = kids.map(read);
      // Short strings only. A paragraph next to a heading is not a stat pair.
      if (a.text.length > 30 || b.text.length > 30) continue;
      const aNum = numeric(a.text), bNum = numeric(b.text);
      if (aNum === bNum) continue;          // both or neither numeric
      const value = aNum ? a : b;
      const label = aNum ? b : a;
      if (!label.text) continue;
      pairs.push({
        selector: cssPath(c),
        label, value,
        valueOutranks: value.fontSize > label.fontSize || value.fontWeight > label.fontWeight,
        inverted: label.fontSize > value.fontSize,
      });
    }
    return pairs.slice(0, 40);
  }

  /* ------------------------------------------------------------ focus ring */

  function probeFocusStyles() {
    // Read author stylesheets for outline suppression. Cross-origin sheets throw.
    const suppressed = [];
    const hasFocusVisible = [];
    for (const sheet of document.styleSheets) {
      let rules;
      try { rules = sheet.cssRules; } catch { continue; }
      if (!rules) continue;
      for (const rule of rules) {
        if (!rule.selectorText || !rule.style) continue;
        const sel = rule.selectorText;
        if (/:focus\b/.test(sel) || /:focus-within/.test(sel)) {
          const o = rule.style.outline || rule.style.outlineStyle || rule.style.outlineWidth;
          if (o && /none|0(px)?$/.test(o.trim())) {
            // `outline: none` expands to outline-color, so outline-color is not
            // evidence of a replacement. Only a visible ring drawn some other
            // way counts: a box-shadow, a real border, or a re-declared outline
            // with a non-zero width.
            const boxShadow = rule.style.boxShadow;
            const border = rule.style.border || rule.style.borderWidth ||
                           rule.style.borderBottom || rule.style.borderBottomWidth;
            const reWidth = rule.style.outlineWidth;
            const hasShadow = !!boxShadow && boxShadow.trim() !== 'none';
            const hasBorder = !!border && !/^(none|0(px)?)$/.test(border.trim());
            // `outline: none` expands outline-width to `initial`, so only an
            // explicit non-zero length counts as a re-declared ring.
            const hasWidth = !!reWidth && /^[\d.]+(px|em|rem)$/.test(reWidth.trim())
                             && parseFloat(reWidth) > 0;
            suppressed.push({
              selector: sel,
              outline: o,
              hasReplacement: hasShadow || hasBorder || hasWidth,
              replacement: hasShadow ? `box-shadow: ${boxShadow}`
                         : hasBorder ? `border: ${border}`
                         : hasWidth ? `outline-width: ${reWidth}`
                         : null,
            });
          }
        }
        if (/:focus-visible/.test(sel)) hasFocusVisible.push(sel);
      }
    }
    return {
      suppressed,
      // A replacement declared in a *different* rule won't be seen here, so a
      // suppression with no replacement is a candidate to confirm by tabbing,
      // not a proven failure.
      note: 'Replacements declared in a separate rule are not detected. Confirm by tabbing.',
      usesFocusVisible: hasFocusVisible.length > 0,
      focusVisibleSelectors: hasFocusVisible.slice(0, 30),
    };
  }

  /* -------------------------------------------------- computed style dump */

  /**
   * The visibility test the systematisation pass wants, which is not the one the
   * geometric probes want.
   *
   * A geometric probe must exclude a stranded element or it invents overlaps.
   * `dumpStyles()` is counting design decisions — how many distinct radii, how
   * many shadows, whether caps are tracked — and a stranded element's tokens are
   * perfectly real. Measured on `evals/fixtures/landing.html`: the three `.card`
   * elements carry the page's only `box-shadow` and one of its two radii, and on
   * a capture taken before the reveal pass they read at opacity 0.0036 because
   * their entry animation never runs. Using one filter for both jobs threw the
   * fixture's whole shadow population away and reported `0 distinct shadows`,
   * which reads as a surface with no elevation at all. (After the reveal pass
   * they read 1, so on a properly settled run this filter changes nothing — it
   * is insurance for the one-shot capture, which is exactly when it is needed.)
   *
   * So: hidden by the author stays excluded; stranded by the engine is included.
   */
  function visibleForStyle(el) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return false;
    if (el.closest && el.closest('details:not([open])')) return false;
    // Deliberately NOT testing opacity: a near-zero value here is the engine's
    // stranded entrance, and an exact zero is usually the same thing pre-reveal.
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }

  /**
   * The evidence base for the systematisation pass. Every visible element's
   * design-relevant computed values, so variance and token adherence can be
   * measured offline rather than judged by eye.
   *
   * Five keys here used to be structurally dead on the review engine, and the
   * consequence was worse than missing data: `analyze_styles.py` counted the
   * empties as zeros, so `0 distinct radii` and `0 shadows` read as a perfectly
   * tokenised surface, and the untracked-caps tell and the `transition: all`
   * detector could never fire. Measured 18 Aug 2026 on obscura 0.2.0 against
   * `evals/fixtures/landing.html`, which plants every one of them:
   *
   *   borderRadius        `0px`     ← shorthand; `borderTopLeftRadius` gives 24px
   *   borderWidth         `0px`     ← shorthand; `borderLeftWidth` gives 1px
   *   gap                 `normal`  ← and `rowGap`/`columnGap` are ALSO `normal`,
   *                                   so gap has no longhand escape at all
   *   textTransform       `""`
   *   boxShadow           `""`
   *   transitionProperty  `""`
   *   transitionDuration  `""`
   *
   * Three routes, in this order: compose from longhands where they answer, read
   * the declaration where they do not, and emit `null` with the channel named
   * where neither works. Every value carries a `*_src` tag so a metric built on
   * a declaration is never quoted as a measurement, and so the consumer can
   * report an unmeasurable channel as unmeasurable instead of as zero.
   */
  function dumpStyles() {
    const cap = capability();
    const nodes = [...document.querySelectorAll('*')].filter(visibleForStyle).slice(0, MAX_NODES);
    const C = cap.channels;

    // Compose a shorthand from its longhands when the shorthand does not
    // compose but the parts do. This is what already rescued margin and padding.
    const compose = (cs, keys) => keys.map(k => cs[k]).join(' ');

    return nodes.map(el => {
      const cs = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      const row = {
        selector: cssPath(el),
        tag: el.tagName.toLowerCase(),
        hasText: !!(el.childNodes.length && [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())),
        fontFamily: cs.fontFamily,
        fontSize: cs.fontSize,
        fontWeight: cs.fontWeight,
        lineHeight: cs.lineHeight,
        letterSpacing: cs.letterSpacing,
        color: cs.color,
        backgroundColor: cs.backgroundColor,
        borderColor: cs.borderColor,
        margin: compose(cs, ['marginTop', 'marginRight', 'marginBottom', 'marginLeft']),
        padding: compose(cs, ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft']),
        display: cs.display,
        maxWidth: cs.maxWidth,
        zIndex: cs.zIndex,
        opacity: cs.opacity,
        cursor: cs.cursor,
        fontVariantNumeric: cs.fontVariantNumeric,
        width: Math.round(r.width),
        height: Math.round(r.height),
      };

      // Fonts are recorded, but the engine may not load them. The consumer needs
      // to know that a family count here is a count of what the CSS asked for.
      row.fontFamily_src = cap.fonts.readable ? 'computed' : 'declared-only (web fonts do not load on this engine)';

      const shorthandOrLonghand = (key, longhands, prop) => {
        if (C[key] && C[key].readable) return { value: cs[key], src: 'computed' };
        const composed = compose(cs, longhands);
        if (longhands.every(k => C[k] === undefined || C[k].readable) &&
            /[1-9]/.test(composed)) return { value: composed, src: 'computed-longhand' };
        const sv = styleValue(el, prop, key);
        return { value: sv.value, src: sv.source === 'declared' ? 'declared' : sv.source };
      };

      const br = shorthandOrLonghand('borderRadius',
        ['borderTopLeftRadius', 'borderTopRightRadius', 'borderBottomRightRadius', 'borderBottomLeftRadius'],
        'border-radius');
      row.borderRadius = br.value; row.borderRadius_src = br.src;

      const bw = shorthandOrLonghand('borderWidth',
        ['borderTopWidth', 'borderRightWidth', 'borderBottomWidth', 'borderLeftWidth'],
        'border-width');
      row.borderWidth = bw.value; row.borderWidth_src = bw.src;

      // Gap is the one with no longhand escape measured on this engine, so it
      // goes straight to the declaration.
      const gap = (C.gap.readable || C.rowGap.readable)
        ? { value: C.gap.readable ? cs.gap : compose(cs, ['rowGap', 'columnGap']), src: 'computed' }
        : (() => { const sv = styleValue(el, 'gap', 'gap');
                   return { value: sv.value, src: sv.source }; })();
      row.gap = gap.value; row.gap_src = gap.src;

      for (const [key, prop] of [['textTransform', 'text-transform'],
                                 ['boxShadow', 'box-shadow'],
                                 ['transitionProperty', 'transition-property'],
                                 ['transitionDuration', 'transition-duration']]) {
        const sv = styleValue(el, prop, key);
        row[key] = sv.value;
        row[key + '_src'] = sv.source;
        if (sv.source === 'unreadable') row[key + '_reason'] = sv.reason;
      }

      // `transition: all 0.3s ease-in` declares property and duration together,
      // and the declaration index carries the shorthand where the longhands are
      // dead. Split it so the consumer's existing property/duration logic works.
      if (row.transitionProperty_src !== 'computed' || row.transitionDuration_src !== 'computed') {
        const t = styleValue(el, 'transition', 'transition');
        // `none` is this engine's resolved answer for the shorthand and means
        // nothing here — a transition set in a stylesheet resolves to it too.
        const usable = t.value && !/^(none|all)$/i.test(String(t.value).trim());
        if (usable) {
          row.transitionShorthand = t.value;
          row.transitionShorthand_src = t.source;
          const first = String(t.value).split(',')[0].trim();
          const dur = first.match(/(^|\s)(-?[\d.]+m?s)(\s|$)/);
          const prop = first.split(/\s+/)[0];
          if (!row.transitionProperty && prop) {
            row.transitionProperty = prop; row.transitionProperty_src = t.source;
          }
          if (!row.transitionDuration && dur) {
            row.transitionDuration = dur[2]; row.transitionDuration_src = t.source;
          }
        }
      }

      return row;
    });
  }

  /* ------------------------------------------------------------- ink probe */

  /**
   * Where the glyph actually sits inside its box. getBoundingClientRect returns
   * the box; ink position depends on line-height and font metrics, which is how
   * "the CSS is correct" and "it looks wrong" are both true at once.
   */
  function probeInk(selector) {
    const el = document.querySelector(selector);
    if (!el) return { error: 'not found', selector };
    const cs = getComputedStyle(el);
    const text = el.textContent.trim();
    if (!text) return { error: 'no text', selector };

    const probe = document.createElement('span');
    probe.style.cssText = 'display:inline-block;width:0;height:0;vertical-align:baseline';
    el.insertBefore(probe, el.firstChild);
    const baselineY = probe.getBoundingClientRect().top;
    probe.remove();

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    ctx.font = `${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`;
    const m = ctx.measureText(text);

    const box = el.getBoundingClientRect();
    const fontSize = parseFloat(cs.fontSize);
    const lineHeight = cs.lineHeight === 'normal' ? fontSize * 1.2 : parseFloat(cs.lineHeight);

    return {
      selector,
      boxTop: box.top,
      inkTop: baselineY - m.actualBoundingBoxAscent,
      inkBottom: baselineY + m.actualBoundingBoxDescent,
      inkOffsetFromBoxTop: (baselineY - m.actualBoundingBoxAscent) - box.top,
      fontSize, lineHeight,
      lineHeightRatio: Math.round((lineHeight / fontSize) * 1000) / 1000,
      // Below ~0.95 the box is shorter than the glyph, so centring lies.
      boxShorterThanGlyph: lineHeight < fontSize * 0.95,
    };
  }


  /* ------------------------------------------------------- layout integrity */

  /* Thresholds. Every one is a judgement call made once, here, rather than
     per-review. Tune them against a surface you already know is sound. */
  const LI = {
    columnDriftPx: 4,        // per-column edge deviation inside one repeated group.
                             // Below ~4 this fires on sub-pixel layout and text metrics.
    headerDriftPx: 8,        // column header centre vs the body column it labels
    railDriftPx: 8,          // left edges of regions that should share a rail
    zeroGapPx: 1,            // "touching" — a gap this small was not designed
    overlapMinPx: 3,         // text boxes must intersect by this much on BOTH axes;
                             // a 1px abutment between adjacent inline spans is not an overlap
    deadSpaceRatio: 0.55,    // shortest child / tallest child, below which the row is lopsided
    deadSpaceMinPx: 200,     // only containers at least this tall can hold a void
    controlTextMax: 24,      // longest text a chip-shaped thing can carry and still read as a control
    semanticTokenTexts: 3,   // distinct strings a semantic token may carry before it means nothing
    bandMinHeightPx: 80,     // below this, a band is too short to hold a void worth reporting
    bandInkMinPx: 24,        // ink height below this inside a tall band is "nearly empty"
    bandFillMin: 0.25,       // ink height / box height. Below this the band is mostly its own margins
    spilledTrackRatio: 0.75, // an implicit trailing grid row this much shorter than the
                             // authored rows is an orphan, not a ragged last row of cards
    dividerGutterPx: 16,     // hard floor between a text ink box and a vertical rule.
                             // Below this the rule reads as attached to the words rather
                             // than as the boundary between two cells
    dividerGutterWantPx: 24, // what a divided cell should actually carry at >=900px wide
    maxReported: 40,         // per-probe cap, so one bad page cannot flood the report
  };

  const FOCUSABLE =
    'a[href],button,input,select,textarea,summary,[tabindex]:not([tabindex="-1"]),' +
    '[role="button"],[role="switch"],[role="checkbox"],[role="radio"],[role="link"],[role="tab"]';

  function cap(list) {
    const out = list.slice(0, LI.maxReported);
    if (list.length > out.length) out.push({ truncated: list.length - out.length });
    return out;
  }

  function shortText(el) {
    return (el.textContent || '').trim().replace(/\s+/g, ' ');
  }

  function classSig(el) {
    return el.tagName + '.' + (typeof el.className === 'string' ? el.className : '').trim();
  }

  function mode(nums) {
    const c = new Map();
    for (const n of nums) c.set(n, (c.get(n) || 0) + 1);
    let best = null, bestN = -1;
    for (const [v, n] of c) if (n > bestN) { best = v; bestN = n; }
    return best;
  }

  /**
   * The spine of this whole section. A "repeated group" is any container with
   * three or more visible element children sharing a class signature — a table
   * body, a card grid, a settings list, a nav. Almost every layout defect worth
   * finding lives inside one, or between one and the thing that labels it.
   */
  function findRepeatedGroups() {
    const groups = [];
    for (const parent of document.querySelectorAll('body *')) {
      const kids = [...parent.children].filter(visible);
      if (kids.length < 3) continue;
      const sigs = kids.map(classSig);
      const common = mode(sigs);
      const members = kids.filter((k, i) => sigs[i] === common);
      if (members.length < 3) continue;
      // Skip groups whose members are themselves the parents of a bigger group,
      // so a page reports its rows rather than every ancestor of those rows.
      groups.push({ parent, members, sig: common });
    }
    return groups;
  }

  /**
   * Two defects, both invisible to a contrast or overflow check:
   *  - shape: sibling rows with different child counts, so one row's optional
   *    element steals width from the columns before it
   *  - drift: rows with equal child counts whose nth column does not line up
   */
  function probeRepeatedGroupIntegrity() {
    const shape = [], drift = [];
    for (const g of findRepeatedGroups()) {
      const rows = g.members.map(m => ({
        el: m,
        kids: [...m.children].filter(visible),
        text: shortText(m).slice(0, 40),
      }));
      const counts = rows.map(r => r.kids.length);
      const modal = mode(counts);
      // Only column-sets. A member whose children stack vertically is a nav
      // group or a stack, and those legitimately hold different item counts.
      const horizontal = rows.filter(r => r.kids.length >= 2).every(r => {
        const a = r.kids[0].getBoundingClientRect(), b = r.kids[1].getBoundingClientRect();
        return b.left >= a.right - 1;
      });
      if (horizontal && modal >= 2 && counts.some(c => c !== modal)) {
        shape.push({
          group: cssPath(g.parent), sig: g.sig, modalChildren: modal,
          odd: rows.filter(r => r.kids.length !== modal)
            .map(r => ({ selector: cssPath(r.el), children: r.kids.length, text: r.text })),
          note: 'Sibling rows with different child counts. An optional element in a fixed ' +
                'row usually steals width from every column before it.',
        });
      }
      // Drift only means anything when the members stack vertically, i.e. they
      // are rows. In a horizontal group the members ARE the columns, and their
      // nth-child edges are supposed to differ.
      const stacked = rows.length >= 2 && rows.every((r, i) =>
        i === 0 || r.el.getBoundingClientRect().top >=
                   rows[i - 1].el.getBoundingClientRect().bottom - 1);
      const full = stacked ? rows.filter(r => r.kids.length === modal && modal >= 2) : [];
      // A label/value pair is not a table. When the LAST column's right edges
      // all agree, the row is right-aligned and the intermediate edges are free
      // by construction: the label ends wherever its value happens to start.
      const lastRights = full.map(r => Math.round(r.kids[modal - 1].getBoundingClientRect().right));
      const rightAligned = full.length >= 2 &&
        lastRights.every(v => Math.abs(v - mode(lastRights)) <= LI.columnDriftPx);
      if (full.length >= 3 && !(rightAligned && modal <= 3)) {
        for (let i = 0; i < modal; i++) {
          const rights = full.map(r => Math.round(r.kids[i].getBoundingClientRect().right));
          const m = mode(rights);
          const off = full.filter((r, j) => Math.abs(rights[j] - m) > LI.columnDriftPx);
          if (off.length && off.length < full.length) {
            drift.push({
              group: cssPath(g.parent), column: i, modalRight: m,
              offenders: off.map(r => ({
                selector: cssPath(r.el), text: r.text,
                right: Math.round(r.kids[i].getBoundingClientRect().right),
              })),
            });
          }
        }
      }
    }
    return { shapeMismatch: cap(shape), columnDrift: cap(drift) };
  }

  /**
   * A column header written as its own grid and a row written with its own fixed
   * widths are two independent lists of numbers. Nothing keeps them equal, and
   * nothing in a WCAG pass notices when they diverge.
   */
  function probeColumnHeaderAlignment() {
    const out = [];
    for (const g of findRepeatedGroups()) {
      const first = g.members[0];
      const bodyCols = [...first.children].filter(visible);
      if (bodyCols.length < 3) continue;
      // On a single-page app every screen is in the DOM, so the sibling of a
      // group can be a header belonging to a hidden screen. visible() covers the
      // element; its column count has to match the body it claims to label.
      const candidates = [g.parent.previousElementSibling,
                          g.parent.parentElement && g.parent.parentElement.previousElementSibling]
        .filter(e => e && visible(e) && e.getBoundingClientRect().width > 0);
      for (let head of candidates) {
        if (!head || !visible(head)) continue;
        // The sibling is often a wrapper holding the header plus a filter row.
        // Descend to the child that actually looks like a header rather than
        // comparing the wrapper's children, which produces confident nonsense.
        if (![...head.children].every(c => shortText(c).length <= 30)) {
          const inner = [...head.children].find(c => visible(c) &&
            [...c.children].length >= 3 &&
            [...c.children].every(g => shortText(g).length <= 30));
          if (!inner) continue;
          head = inner;
        }
        const hc = [...head.children].filter(visible);
        if (hc.length < 3) continue;
        if (!hc.every(c => shortText(c).length <= 30)) continue;
        // A header labels the row beneath it, so its first column starts where
        // the row's does. Without this the walk latches onto any short-text
        // sibling — a filter bar, a section head — and reports large deltas
        // against something that was never a header.
        if (Math.abs(hc[0].getBoundingClientRect().left -
                     bodyCols[0].getBoundingClientRect().left) > LI.headerDriftPx) continue;
        // Index-matching only means anything when the two have the same column
        // count. A row that leads with an icon the header omits would otherwise
        // produce large, confident, meaningless deltas.
        if (hc.length !== bodyCols.length) {
          out.push({
            header: cssPath(head), body: cssPath(first),
            headerColumns: hc.length, bodyColumns: bodyCols.length,
            countMismatch: true,
            note: 'Header and row have different column counts, so the header cannot ' +
                  'be verified against the body. Measure the pair by hand, then decide ' +
                  'whether the header is missing a column or the row has an extra one.',
          });
          continue;
        }
        const mid = e => { const r = e.getBoundingClientRect(); return Math.round(r.left + r.width / 2); };
        const cols = [];
        for (let i = 0; i < hc.length; i++) {
          const d = mid(hc[i]) - mid(bodyCols[i]);
          if (Math.abs(d) > LI.headerDriftPx) {
            cols.push({ index: i, label: shortText(hc[i]).slice(0, 24), deltaPx: d });
          }
        }
        // A real header is nearly aligned and drifts a little. When most columns
        // are wildly off, the candidate is an unrelated sibling — a card head, a
        // toolbar — and reporting it as a misaligned header is worse than silence.
        const wild = cols.filter(c => Math.abs(c.deltaPx) > LI.headerDriftPx * 10).length;
        if (cols.length && wild === 0) {
          out.push({
            header: cssPath(head), body: cssPath(first), columns: cols,
            note: 'Header columns do not sit over the body columns they label.',
          });
        }
      }
    }
    return cap(out);
  }

  /**
   * Proximity is the primary grouping signal, so a zero gap before a heading
   * welds that heading to the block above it, and a group whose inner gap
   * matches its outer gap has no grouping at all.
   */
  function probeSiblingGaps() {
    const touching = [];
    const isHeading = el =>
      /^H[1-6]$/.test(el.tagName) || !!el.querySelector('h1,h2,h3,h4,h5,h6');
    for (const parent of document.querySelectorAll('main, main *, section, article')) {
      const kids = [...parent.children].filter(visible);
      if (kids.length < 2) continue;
      for (let i = 1; i < kids.length; i++) {
        const a = kids[i - 1].getBoundingClientRect();
        const b = kids[i].getBoundingClientRect();
        if (b.top < a.top) continue;                 // not stacked; skip
        const gap = Math.round(b.top - a.bottom);
        // A card head touching its own body is one component, not two blocks
        // that failed to separate.
        const sameCard = kids[i - 1].closest('[class*="card"],[class*="panel"]') ===
                         kids[i].closest('[class*="card"],[class*="panel"]') &&
                         kids[i].closest('[class*="card"],[class*="panel"]') !== null;
        if (!sameCard && kids[i - 1].parentElement.closest('[class*="card"],[class*="panel"]')) continue;
        if (gap <= LI.zeroGapPx && gap >= -LI.zeroGapPx && isHeading(kids[i]) && !isHeading(kids[i - 1])) {
          touching.push({
            above: cssPath(kids[i - 1]), heading: cssPath(kids[i]),
            headingText: shortText(kids[i]).slice(0, 40), gapPx: gap,
            note: 'A section heading touching the block above it. Usually a container ' +
                  'that sits outside the wrapper carrying the section margin.',
          });
        }
      }
    }
    return cap(touching);
  }

  /**
   * Regions that read as one column should start on one rail. A full-bleed
   * header over capped-and-centred content diverges further the wider the
   * viewport gets, which is why it survives a review run at one width.
   */
  function probeSharedRails() {
    // Only headings that sit on the page rail. One inside a card, panel or
    // dialog is indented by that container's padding and says nothing about
    // whether the page's regions agree.
    const INSET = '[class*="card"],[class*="panel"],[class*="sheet"],[class*="modal"],' +
                  'dialog,aside,figure,blockquote';
    const heads = [...document.querySelectorAll('h1,h2,h3')].filter(visible)
      .filter(h => shortText(h).length > 0)
      .filter(h => !h.closest(INSET));
    // Every early return has to carry the SAME keys as the full one. This one
    // did not, and the consumer read `L["rails"]["exceedsThreshold"]` unguarded:
    // measured 18 Aug 2026, `run_review.py` died with `KeyError:
    // 'exceedsThreshold'` on the first viewport of this skill's own eval
    // fixture, wrote probes for one width, orphaned two captures and reported a
    // traceback instead of a review. A partial result shape is the same class of
    // defect as a partial result.
    if (heads.length < 2) {
      return { clusters: [], disagreementPx: 0, exceedsThreshold: false,
               skipped: 'fewer than two page-rail headings on this surface' };
    }
    const lefts = heads.map(h => ({ left: Math.round(h.getBoundingClientRect().left), el: h }));
    const clusters = [];
    for (const x of lefts.sort((a, b) => a.left - b.left)) {
      const c = clusters.find(k => Math.abs(k.left - x.left) <= 4);
      if (c) { c.members.push(x); } else { clusters.push({ left: x.left, members: [x] }); }
    }
    const spread = clusters.length
      ? clusters[clusters.length - 1].left - clusters[0].left : 0;
    return {
      disagreementPx: spread,
      exceedsThreshold: spread > LI.railDriftPx && clusters.length > 1,
      clusters: clusters.map(c => ({
        left: c.left, count: c.members.length,
        sample: c.members.slice(0, 3).map(m => shortText(m.el).slice(0, 32)),
      })),
    };
  }

  /**
   * Is this node inside a floating layer — fixed, sticky, or an explicit
   * z-index stacking context? A toast, a sticky header and a popover are all
   * MEANT to cover content, so an intersection across that boundary is not an
   * overlap. Only same-layer intersections are.
   */
  function floatLayer(el) {
    for (let n = el; n && n !== document.body; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.position === 'fixed' || cs.position === 'sticky') return n;
      if (cs.position !== 'static' && cs.zIndex !== 'auto' && +cs.zIndex > 0) return n;
    }
    return null;
  }

  /** Two pieces of text occupying the same pixels. Includes SVG annotation. */
  function probeTextOverlap() {
    const nodes = [];
    for (const el of document.querySelectorAll('body *')) {
      if (!visible(el)) continue;
      const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
      if (!own) continue;
      // floatLayer() walks ancestors calling getComputedStyle, so it is resolved
      // ONCE per node here rather than twice per PAIR in the loop below. That
      // single change is most of the win: measured on a 12-slide deck with ~250
      // text nodes, this probe took 26.8s of a 27.6s sweep and blew the CDP
      // socket's 30s timeout, which surfaced as the whole review crashing on
      // its third viewport rather than as a slow probe.
      const layer = floatLayer(el);
      // Per-fragment, not the bounding box. An inline element that wraps returns
      // a bounding rect spanning both lines, which "overlaps" everything sitting
      // between them. getClientRects() gives one rect per line fragment.
      for (const r of el.getClientRects()) {
        if (r.width < 1 || r.height < 1) continue;
        nodes.push({ el, r, layer, t: shortText(el).slice(0, 30), i: nodes.length });
      }
    }
    // Sweep line. Sorted by top edge, the inner loop stops as soon as a
    // candidate starts at or below the current node's bottom, because every
    // node after it starts lower still and cannot overlap vertically. The
    // cheap rect test runs before contains() and the layer comparison, so the
    // expensive checks only ever see pairs that already share pixels.
    const byTop = nodes.slice().sort((a, b) => a.r.top - b.r.top || a.i - b.i);
    const out = [];
    for (let i = 0; i < byTop.length; i++) {
      const a = byTop[i];
      for (let j = i + 1; j < byTop.length; j++) {
        const b = byTop[j];
        if (b.r.top >= a.r.bottom) break;
        const w = Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left);
        if (w < LI.overlapMinPx) continue;
        const h = Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top);
        if (h < LI.overlapMinPx) continue;
        if (a.layer !== b.layer) continue;
        if (a.el.contains(b.el) || b.el.contains(a.el)) continue;
        const p = a.i <= b.i ? a : b, q = a.i <= b.i ? b : a;
        out.push({
          _i: p.i, _j: q.i,
          a: cssPath(p.el), aText: p.t, b: cssPath(q.el), bText: q.t,
          overlapPx2: Math.round(w * h),
        });
      }
    }
    // Emit in document order. The sweep visits pairs geometrically, so without
    // this the output would reorder run to run and cap() would keep a different
    // subset — a diff against an earlier run would show churn that is not there.
    out.sort((x, y) => x._i - y._i || x._j - y._j);
    for (const o of out) { delete o._i; delete o._j; }
    return cap(out);
  }

  /**
   * A tall container whose ink sits in one end. At page scale this reads as
   * generous whitespace; it is usually a cross-axis alignment applied to a
   * column that is shorter than its neighbour.
   */
  function probeDeadSpace() {
    const out = [];
    for (const el of document.querySelectorAll('main *')) {
      if (!visible(el)) continue;
      const cs = getComputedStyle(el);
      if (!/flex|grid/.test(cs.display)) continue;
      const r = el.getBoundingClientRect();
      if (r.height < LI.deadSpaceMinPx || r.width < 240) continue;
      const kids = [...el.children].filter(visible);
      if (kids.length < 2) continue;
      // A void needs a ROW. In a column stack, children of different heights are
      // the point, not a defect.
      const rects0 = kids.map(k => k.getBoundingClientRect());
      const sideBySide = rects0.every((r, i) => i === 0 || r.left >= rects0[i - 1].right - 1);
      if (!sideBySide) continue;
      // The void does not live in the short child — with a cross-axis alignment
      // the short child's box IS its content. It lives in the container, beside
      // whichever sibling set the height.
      const rects = kids.map(k => k.getBoundingClientRect());
      const tallest = Math.max(...rects.map(x => x.height));
      const shortest = Math.min(...rects.map(x => x.height));
      if (tallest < LI.deadSpaceMinPx) continue;
      if (shortest > tallest * LI.deadSpaceRatio) continue;
      out.push({
        selector: cssPath(el), display: cs.display,
        alignItems: cs.alignItems, heightPx: Math.round(r.height),
        tallestChildPx: Math.round(tallest), shortestChildPx: Math.round(shortest),
        voidPx: Math.round(tallest - shortest),
        shortChild: cssPath(kids[rects.findIndex(x => x.height === shortest)]),
        shortChildText: shortText(kids[rects.findIndex(x => x.height === shortest)]).slice(0, 40),
        note: 'Uneven column heights in a flex/grid row. At page scale the gap beside ' +
              'the short column reads as whitespace rather than as a hole.',
      });
    }
    return cap(out);
  }

  /**
   * The union box of everything a subtree actually PAINTS: text runs (per line
   * fragment), replaced elements, and any box carrying a border or a painted
   * background. This is deliberately not `getBoundingClientRect()` — a band
   * whose only child is a full-height empty wrapper has a perfectly healthy box
   * and paints nothing at all.
   */
  function inkBox(root) {
    let top = Infinity, bottom = -Infinity, any = false;
    const push = (r) => {
      if (r.width <= 0 || r.height <= 0) return;
      any = true;
      if (r.top < top) top = r.top;
      if (r.bottom > bottom) bottom = r.bottom;
    };
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let t;
    while ((t = walker.nextNode())) {
      if (!t.nodeValue || !t.nodeValue.trim()) continue;
      const range = document.createRange();
      range.selectNodeContents(t);
      // Per-fragment rects, not the bounding box: a wrapped inline otherwise
      // claims ink across the whole gap between its two lines.
      for (const r of range.getClientRects()) push(r);
    }
    for (const el of root.querySelectorAll('img,svg,canvas,video,picture,hr')) {
      if (visible(el)) push(el.getBoundingClientRect());
    }
    for (const el of root.querySelectorAll('*')) {
      if (!visible(el)) continue;
      const cs = getComputedStyle(el);
      const bordered = ['Top', 'Right', 'Bottom', 'Left']
        .some(s => parseFloat(cs['border' + s + 'Width']) > 0);
      const bg = cs.backgroundColor;
      const painted = bg && !/rgba\(0,\s*0,\s*0,\s*0\)|^transparent$/.test(bg);
      if (bordered || painted || cs.backgroundImage !== 'none') push(el.getBoundingClientRect());
    }
    return any ? { top, bottom, height: bottom - top } : null;
  }

  /**
   * The COLUMN form of dead space, which `probeDeadSpace()` above is structurally
   * blind to: it only fires on side-by-side flex/grid rows, so the defect class
   * "a section that renders nothing still occupies its own margins" — 200px of
   * padding around an absence — never matched it.
   *
   * Two outputs, because they answer different questions:
   *
   *   voids — bands that render nothing, or a sliver in a tall box
   *   seams — the ink-to-ink gap between consecutive bands, i.e. the band rhythm
   *
   * `seams` is reported unfiltered on purpose. A page whose bands measure 92px,
   * 205px and 229px ink-to-ink has no single band that trips a threshold and is
   * still three-quarters dead space; only the whole table shows it.
   */
  function probeColumnVoids() {
    const main = document.querySelector('main') || document.body;
    const bands = [...main.children].filter(visible);
    const voids = [];
    const seams = [];
    let prevInk = null;

    bands.forEach((el, i) => {
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      const ink = r.height < 1 ? null : inkBox(el);
      const fill = ink && r.height ? ink.height / r.height : 0;

      if (r.height < 1) {
        voids.push({
          selector: cssPath(el), kind: 'zero-height', heightPx: 0,
          note: 'Band is in the DOM and contributes nothing. A disabled section ' +
                'should be absent, not collapsed.',
        });
      } else if (!ink) {
        voids.push({
          selector: cssPath(el), kind: 'no-ink', heightPx: Math.round(r.height),
          paddingTop: cs.paddingTop, paddingBottom: cs.paddingBottom,
          note: 'Band occupies vertical space and paints nothing. Its own margins ' +
                'became the content.',
        });
      } else if (r.height >= LI.bandMinHeightPx && ink.height < LI.bandInkMinPx) {
        voids.push({
          selector: cssPath(el), kind: 'near-empty',
          heightPx: Math.round(r.height), inkPx: Math.round(ink.height),
          fillPct: Math.round(fill * 100),
          text: shortText(el).slice(0, 60),
          note: 'A sliver of content in a tall box.',
        });
      } else if (r.height >= LI.bandMinHeightPx && fill < LI.bandFillMin) {
        voids.push({
          selector: cssPath(el), kind: 'low-fill',
          heightPx: Math.round(r.height), inkPx: Math.round(ink.height),
          fillPct: Math.round(fill * 100),
          leadPx: Math.round(ink.top - r.top),
          trailPx: Math.round(r.bottom - ink.bottom),
          text: shortText(el).slice(0, 60),
          note: 'Band is mostly padding. Judge against the surface\'s own band ' +
                'rhythm before calling it a defect — a deliberately sparse foot ' +
                'measures the same as a section that lost its content.',
        });
      }

      seams.push({
        i, selector: cssPath(el),
        heightPx: Math.round(r.height),
        inkPx: ink ? Math.round(ink.height) : 0,
        fillPct: Math.round(fill * 100),
        leadPx: ink ? Math.round(ink.top - r.top) : null,
        trailPx: ink ? Math.round(r.bottom - ink.bottom) : null,
        inkGapFromPrevPx: ink && prevInk ? Math.round(ink.top - prevInk.bottom) : null,
        text: shortText(el).slice(0, 60),
      });
      if (ink) prevInk = ink;
    });

    return { bands: bands.length, voids: cap(voids), seams: cap(seams) };
  }

  /**
   * The check that catches a settings list made of labels. A chip-shaped thing
   * carrying a short string in the trailing column of a repeated row is read as
   * a control by every user; if the row holds nothing focusable, it is not one.
   */
  function probeAffordanceGaps() {
    const looksLikeControl = el => {
      const cs = getComputedStyle(el);
      const radius = parseFloat(cs.borderTopLeftRadius) || 0;
      const bg = cs.backgroundColor;
      const opaque = bg && bg !== 'transparent' && !/rgba\(0,\s*0,\s*0,\s*0\)/.test(bg);
      const t = shortText(el);
      return radius >= 10 && opaque && t.length > 0 && t.length <= LI.controlTextMax;
    };
    const rows = [], orphans = [];
    for (const g of findRepeatedGroups()) {
      for (const row of g.members) {
        if (row.matches(FOCUSABLE) || row.querySelector(FOCUSABLE)) continue;
        const chips = [...row.querySelectorAll('*')].filter(e => visible(e) && looksLikeControl(e));
        if (!chips.length) continue;
        rows.push({
          row: cssPath(row), text: shortText(row).slice(0, 48),
          controlLike: chips.map(c => shortText(c).slice(0, 20)),
          note: 'Row reads as a setting but contains nothing focusable.',
        });
      }
    }
    for (const el of document.querySelectorAll('body *')) {
      if (!visible(el)) continue;
      if (getComputedStyle(el).cursor !== 'pointer') continue;
      if (el.matches(FOCUSABLE) || el.closest(FOCUSABLE)) continue;
      orphans.push({ selector: cssPath(el), text: shortText(el).slice(0, 32) });
    }
    return { unactionableRows: cap(rows), pointerCursorNotFocusable: cap(orphans) };
  }

  /**
   * One class carrying many unrelated strings. A status token that means four
   * different things has stopped being a signal, and no colour check notices
   * because every instance passes contrast individually.
   */
  function probeTokenOverload() {
    const SEMANTIC = /(warn|error|danger|success|ok|info|alert|critical|caution|positive|negative|good|bad)/i;
    const byToken = new Map();
    for (const el of document.querySelectorAll('body *')) {
      if (!visible(el)) continue;
      const cls = typeof el.className === 'string' ? el.className.trim() : '';
      if (!cls) continue;
      const t = shortText(el);
      if (!t || t.length > 32) continue;
      for (const token of cls.split(/\s+/)) {
        if (!token) continue;
        if (!byToken.has(token)) byToken.set(token, new Set());
        byToken.get(token).add(t);
      }
    }
    const out = [];
    for (const [token, texts] of byToken) {
      const n = texts.size;
      // Only semantic tokens. A format utility (.num, .t-data, .caption) is
      // supposed to carry many different strings; that is its whole job.
      if (SEMANTIC.test(token) && n >= LI.semanticTokenTexts) {
        out.push({
          token, distinctTexts: n, sample: [...texts].slice(0, 8),
          note: 'A semantic token carrying several unrelated meanings. Each instance ' +
                'passes contrast on its own, so no colour check notices.',
        });
      }
    }
    out.sort((a, b) => b.distinctTexts - a.distinctTexts);
    return cap(out);
  }

  /**
   * The component inventory. This is the worklist stage 5 works through, and it
   * exists because "inspect crops, not pages" is an instruction with nothing to
   * enumerate. A reviewer given six viewports and nine states will walk both
   * exhaustively and then judge components ad hoc, because only two of the three
   * came with a list. This is the third list.
   *
   * A component type is a class signature carrying visible text or media. For
   * each, it returns the instance count and one representative crop box, so
   * every type can be cropped, opened, and ticked off — and so the report can
   * state coverage as a fraction rather than a feeling.
   */
  function probeComponentInventory() {
    const types = new Map();
    for (const el of document.querySelectorAll('body *')) {
      if (!visible(el)) continue;
      const cls = typeof el.className === 'string' ? el.className.trim() : '';
      if (!cls) continue;
      // Skip pure layout wrappers: no own text, no media, and a single child.
      const ownText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
      const media = el.matches('img,svg,canvas,video,picture,input,select,textarea,button,a');
      const container = el.children.length >= 2;
      if (!ownText && !media && !container) continue;
      const sig = el.tagName.toLowerCase() + '.' + cls.split(/\s+/).slice(0, 3).join('.');
      if (!types.has(sig)) {
        const r = el.getBoundingClientRect();
        types.set(sig, {
          type: sig, count: 0,
          representative: cssPath(el),
          crop: { x: Math.round(r.left + scrollX), y: Math.round(r.top + scrollY),
                  width: Math.round(r.width), height: Math.round(r.height) },
          sampleText: shortText(el).slice(0, 48),
          interactive: media && el.matches(FOCUSABLE),
        });
      }
      types.get(sig).count++;
    }
    const list = [...types.values()].sort((a, b) => b.count - a.count);
    return {
      distinctTypes: list.length,
      totalInstances: list.reduce((n, t) => n + t.count, 0),
      types: list.slice(0, 200),
      note: 'Every entry is one crop. Coverage is types-opened over distinctTypes, ' +
            'and it belongs in the report as a number.',
    };
  }

  /* --------------------------------------------------- tokens and settling */

  /**
   * A custom property that is DECLARED, emitted onto the page, and read by no
   * rule. This is a live defect class, not tidiness: the contract carries the
   * token, every record sets it, the injector emits it, a reviewer greps and
   * finds it present — and the value it was supposed to override is still being
   * painted, because nothing on the page ever says `var(--that-one)`.
   *
   * Measured consequence on a real build: `--primary-on-dark` was declared,
   * emitted per tenant, and consumed by no CSS rule, so every accent word on
   * every dark band painted in raw `--primary`. The company's own name, at 72px
   * on its own hero, sat at 2.14:1 — the least readable thing on the page.
   *
   * Two honest limits, both reported rather than hidden:
   *   - A cross-origin stylesheet cannot be read. `unreadableSheets > 0` means
   *     this probe's answer is partial and must be said so.
   *   - A token read from JavaScript (`getComputedStyle(el).getPropertyValue`)
   *     is consumed and invisible here. Grep the source before acting.
   */
  function probeUnconsumedTokens() {
    const declared = new Map();
    const consumed = new Set();
    let unreadableSheets = 0;

    const harvest = (style, origin) => {
      for (let i = 0; i < style.length; i++) {
        const prop = style[i];
        if (prop.startsWith('--') && !declared.has(prop)) {
          declared.set(prop, {
            value: style.getPropertyValue(prop).trim().slice(0, 60),
            declaredIn: origin,
          });
        }
      }
      // Harvest references from the declaration TEXT, not property by property.
      // `background: var(--canvas)` is stored as a pending-substitution value, so
      // getPropertyValue('background') returns the empty string and a per-property
      // scan reports the token as unread. That false positive is exactly the kind
      // this probe exists to rule out, so it must not generate one.
      const refs = (style.cssText || '').match(/var\(\s*(--[\w-]+)/g);
      if (refs) for (const m of refs) consumed.add(m.replace(/var\(\s*/, ''));
    };

    const walk = (rules, origin) => {
      for (const rule of rules) {
        if (rule.style) harvest(rule.style, rule.selectorText || origin);
        if (rule.cssRules) walk(rule.cssRules, origin);
      }
    };

    for (const sheet of document.styleSheets) {
      let rules = null;
      try { rules = sheet.cssRules; } catch (e) { rules = null; }
      if (!rules) { unreadableSheets++; continue; }
      walk(rules, sheet.href ? 'sheet' : 'inline');
    }
    for (const el of [...document.querySelectorAll('[style]')].slice(0, MAX_NODES)) {
      harvest(el.style, 'inline style');
    }

    const unconsumed = [...declared.entries()]
      .filter(([name]) => !consumed.has(name))
      .map(([name, meta]) => ({ token: name, value: meta.value, declaredIn: meta.declaredIn }));

    return {
      declared: declared.size,
      consumed: consumed.size,
      unreadableSheets,
      unconsumed: cap(unconsumed),
      note: unreadableSheets
        ? 'Partial: some stylesheets are cross-origin and could not be read.'
        : 'A token here may still be read from JavaScript — check the source before acting.',
    };
  }

  /**
   * Proof that the page was at rest when it was measured.
   *
   * A colour or accessibility gate sampled mid-animation reports precise,
   * confident, wrong numbers, and they look exactly like real ones. On a real
   * run an axe pass fired 400ms into a 700ms entrance with an 80ms stagger, read
   * a `#E85A2A` accent as `#6a2d18`, and reported a surface getting *worse* after
   * a fix that provably removed its failures.
   *
   * So every result carries this beside it. A run with `runningAnimations > 0`
   * is not a clean gate; it is an unusable one.
   */
  function probeAnimationSettled() {
    const running = (document.getAnimations ? document.getAnimations() : [])
      .filter(a => a.playState === 'running');
    const partial = [...document.querySelectorAll('body *')].slice(0, MAX_NODES)
      .filter(el => {
        const o = parseFloat(getComputedStyle(el).opacity);
        return o > 0 && o < 0.99;
      });
    return {
      runningAnimations: running.length,
      runningSample: running.slice(0, 5).map(a => {
        const t = a.effect && a.effect.target;
        return t && t.tagName ? cssPath(t) : 'unknown';
      }),
      partiallyTransparentElements: partial.length,
      settled: running.length === 0,
    };
  }

  /**
   * The implicit track. A grid renders MORE children than its declared column
   * list can hold, `grid-auto-flow: row` (the default) puts the remainder on a
   * row nobody authored, and nothing warns. The real instance: a five-child
   * index row declaring four columns dropped its trailing arrow onto its own
   * line under the row number — `grid-template-rows: 27.5px 16px` where one
   * track was intended — on every row, of every tenant, at every width, costing
   * ~450px of dead height on one page. A 16px orphan row reads as generous
   * padding in a screenshot, which is why it survived every look; only the
   * computed track list names it.
   *
   * Two outputs, both from computed geometry:
   *   spilledRows — children past the end of a ROW TEMPLATE. A gallery whose
   *                 columns are all the same width is excluded: wrapping is the
   *                 point there and a ragged last row is a layout decision. An
   *                 unequal, content-sized track list is a template for one row,
   *                 and a child past its end is an orphan.
   *   emptyCells  — a grid child that computes to zero width or height. The
   *                 element is in the DOM, holds a cell, and paints nothing:
   *                 `<time datetime="">` in a date column for a record that
   *                 carries no dates, with the variant class that would have
   *                 dropped the column existing in the stylesheet and applied by
   *                 nothing. Note this cannot use `visible()`, which requires a
   *                 non-zero rect — the zero rect IS the finding.
   */
  function probeImplicitTracks() {
    const spilledRows = [];
    const emptyCells = [];
    const grids = [];

    const pxList = (s) => {
      if (!s || s === 'none' || /[a-df-oq-z(]/i.test(s.replace(/px/g, ''))) return [];
      const out = s.trim().split(/\s+/).map(parseFloat);
      return out.some(Number.isNaN) ? [] : out;
    };

    // A grid ITEM, which is not the same set as a visible element: a cell can be
    // zero-sized and still occupy a track. Absolutely-positioned children and
    // `display: contents` children are not grid items at all.
    const placed = (el) => {
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.display === 'contents') return false;
      if (cs.visibility === 'hidden') return false;
      if (cs.position === 'absolute' || cs.position === 'fixed') return false;
      if (el.closest && (el.closest('details:not([open])') || el.closest('[inert]'))) return false;
      return true;
    };

    for (const el of document.querySelectorAll('*')) {
      const cs = getComputedStyle(el);
      if (cs.display !== 'grid' && cs.display !== 'inline-grid') continue;
      if (!visible(el)) continue;
      grids.push(el);
    }

    // How many times this exact shape occurs on the page. The defect is almost
    // never one row — it is every row of a repeated group, which is what makes
    // 16px of orphan worth ~450px on a single page.
    const sigCount = new Map();
    for (const el of grids) {
      const s = classSig(el);
      sigCount.set(s, (sigCount.get(s) || 0) + 1);
    }

    for (const el of grids) {
      const cs = getComputedStyle(el);
      const kids = [...el.children].filter(placed);
      if (kids.length < 2) continue;

      for (const k of kids) {
        const kr = k.getBoundingClientRect();
        if (kr.width >= 1 && kr.height >= 1) continue;
        emptyCells.push({
          selector: cssPath(k), parent: cssPath(el),
          widthPx: Math.round(kr.width), heightPx: Math.round(kr.height),
          html: k.outerHTML.slice(0, 80),
          note: 'A grid child occupying a cell and painting nothing. The field ' +
                'behind it is absent — emit no element rather than an empty one, ' +
                'and drop the track with it.',
        });
      }

      const cols = pxList(cs.gridTemplateColumns);
      const rows = pxList(cs.gridTemplateRows);
      if (cols.length < 2 || rows.length < 2) continue;
      if (!cs.gridAutoFlow.startsWith('row')) continue;
      if (kids.length <= cols.length) continue;
      // Equal columns => a gallery. Wrapping is intended; skip it.
      if (cols.every((w) => Math.abs(w - cols[0]) < 1)) continue;

      // Row bands, from the used track sizes rather than from child tops —
      // `align-items` moves a child inside its row and would break clustering.
      const r = el.getBoundingClientRect();
      const gap = parseFloat(cs.rowGap) || 0;
      let y = r.top + (parseFloat(cs.borderTopWidth) || 0) + (parseFloat(cs.paddingTop) || 0);
      const bands = rows.map((h) => { const top = y; y += h + gap; return { top, bottom: top + h }; });

      const perRow = rows.map(() => 0);
      for (const k of kids) {
        const kr = k.getBoundingClientRect();
        const mid = kr.top + kr.height / 2;
        let idx = bands.findIndex((b) => mid >= b.top - 1 && mid <= b.bottom + 1);
        if (idx < 0) idx = mid < bands[0].top ? 0 : bands.length - 1;
        perRow[idx] += 1;
      }

      // A FULL last row is wrapping that works. A short one is the orphan.
      const last = rows.length - 1;
      if (!perRow[last] || perRow[last] >= cols.length) continue;

      const tallestOther = Math.max(...rows.slice(0, last));
      const twins = sigCount.get(classSig(el)) || 1;

      spilledRows.push({
        selector: cssPath(el),
        gridTemplateColumns: cs.gridTemplateColumns,
        gridTemplateRows: cs.gridTemplateRows,
        declaredColumns: cols.length,
        children: kids.length,
        childrenOnLastRow: perRow[last],
        orphanRowPx: Math.round(rows[last]),
        // The tell that it was never meant to be there: an orphan row is much
        // shorter than the rows above it, because it holds one small thing.
        shortOrphan: rows[last] < LI.spilledTrackRatio * tallestOther,
        heightPx: Math.round(r.height),
        wouldBePx: Math.round(r.height - rows[last] - gap),
        repeatedInstances: twins,
        text: shortText(el).slice(0, 60),
        note: 'More children than declared columns, so the remainder sits on an ' +
              'implicit row. Count the children against the track list — and ' +
              'check every @media variant, where a shorter track list against ' +
              'the same children is the same bug one column worse.',
      });
    }

    return { spilledRows: cap(spilledRows), emptyCells: cap(emptyCells) };
  }

  /**
   * A vertical rule is drawn in a gap, never beside words.
   *
   * The defect this exists for: a stat row divided into cells, where the label
   * and the number start immediately to the right of the rule. Every automated
   * gate passes it — the contrast is fine, nothing overflows, the grid is even —
   * and it reads as a table that has been squeezed rather than a set of cells
   * that were spaced.
   *
   * Measure the TEXT INK BOX, never the element box. A cell with
   * `padding-left: 24px` and a rule on its own left border passes an
   * element-box check by construction, which is exactly how this ships: the
   * padding belongs to a different element from the one carrying the border,
   * so the declared gutter and the perceived one are different numbers.
   * `Range.getClientRects()` gives one box per line box, so wrapped text is
   * measured where it actually lands.
   */
  function probeDividerProximity() {
    const wide = window.innerWidth >= 900;
    const want = wide ? LI.dividerGutterWantPx : LI.dividerGutterPx;
    const rules = [];

    const paint = (colorStr, styleStr, width) => {
      if (!(width > 0)) return false;
      if (styleStr === 'none' || styleStr === 'hidden') return false;
      const c = parseColor(colorStr);
      return !!c && c.a > 0.05;
    };

    // (a) Real vertical borders. This is how nearly every divided row is built.
    //
    // A border is only a DIVIDER if it stands between two things. A border on a
    // box that also has top and bottom borders is that box's own outline, and
    // measuring the box's own text against it measures the padding — which is
    // exactly what a padding is for.
    //
    // Measured 18 Aug 2026 on `evals/fixtures/landing.html`: without this test
    // the probe returned three violations and zero true positives, every one
    // naming a hero button's own 1px border as the divider and the button's own
    // label as the encroaching ink, and one reporting `gapPx: -139.5` — a
    // negative distance, which this measurement cannot produce. A probe with a
    // 3:0 false-positive rate is worse than an absent one, because it is the
    // reason the whole layout set stops being read.
    let selfOutlineSkipped = 0;
    for (const el of [...document.querySelectorAll('*')].slice(0, MAX_NODES)) {
      if (!visible(el)) continue;
      const r = el.getBoundingClientRect();
      if (r.height < 24 || r.width < 4) continue;
      const cs = getComputedStyle(el);
      // Painted on the perpendicular axis too? Then it is a frame, not a rule.
      const framed =
        paint(cs.borderTopColor, cs.borderTopStyle, parseFloat(cs.borderTopWidth) || 0) &&
        paint(cs.borderBottomColor, cs.borderBottomStyle, parseFloat(cs.borderBottomWidth) || 0);
      for (const side of ['Left', 'Right']) {
        const w = parseFloat(cs[`border${side}Width`]) || 0;
        if (!paint(cs[`border${side}Color`], cs[`border${side}Style`], w)) continue;
        if (framed) { selfOutlineSkipped++; continue; }
        rules.push({
          kind: `border-${side.toLowerCase()}`,
          owner: cssPath(el),
          ownerEl: el,
          x: side === 'Left' ? r.left + w / 2 : r.right - w / 2,
          top: r.top, bottom: r.bottom,
          declaredPadPx: Math.round(parseFloat(cs[`padding${side}`]) || 0),
        });
      }
    }

    // (b) Elements standing in for a rule: a thin tall painted box.
    for (const el of document.querySelectorAll(
      'hr,[role="separator"],[class*="divider"],[class*="rule"],[class*="separator"]')) {
      if (!visible(el)) continue;
      const r = el.getBoundingClientRect();
      if (r.width > 3 || r.height < 24) continue;
      rules.push({
        kind: 'element-rule', owner: cssPath(el),
        x: r.left + r.width / 2, top: r.top, bottom: r.bottom, declaredPadPx: null,
      });
    }

    // (c) Multi-column rules. The line sits between generated column boxes, which
    // have no node to measure, so this is reported rather than measured — saying
    // "unmeasurable" is the honest output, and silence would read as a pass.
    const columnRules = [];
    for (const el of document.querySelectorAll('*')) {
      const cs = getComputedStyle(el);
      const w = parseFloat(cs.columnRuleWidth) || 0;
      if (!paint(cs.columnRuleColor, cs.columnRuleStyle, w)) continue;
      const gap = parseFloat(cs.columnGap);
      columnRules.push({
        el: cssPath(el),
        columnGapPx: Number.isFinite(gap) ? Math.round(gap) : null,
        ruleWidthPx: w,
        sufficient: Number.isFinite(gap) ? (gap - w) / 2 >= want : null,
        note: 'column-rule sits in the column gap; each side gets (gap - rule) / 2. ' +
              'Not measured against real text — check by eye at this viewport.',
      });
    }

    if (!rules.length) {
      return {
        rules: 0, floorPx: LI.dividerGutterPx, wantPx: want,
        violations: [], crossings: [], clipped: [], columnRules: cap(columnRules),
        selfOutlineSkipped,
        note: selfOutlineSkipped
          ? `${selfOutlineSkipped} side border(s) skipped as box outlines rather than dividers (they also paint top and bottom).`
          : null,
      };
    }

    // Text ink boxes, one per line box.
    const texts = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    for (let n = walker.nextNode(); n && texts.length < MAX_NODES; n = walker.nextNode()) {
      const t = n.textContent.trim();
      if (!t) continue;
      const el = n.parentElement;
      if (!el || !visible(el)) continue;
      const range = document.createRange();
      range.selectNodeContents(n);
      for (const box of range.getClientRects()) {
        if (box.width < 1 || box.height < 1) continue;
        texts.push({ box, text: t.slice(0, 48), el });
      }
    }

    // Worst offence per (rule, element) pair. A three-line cell against one rule
    // is one defect to fix, not three rows in a report.
    const worst = new Map();
    const crossings = [];
    for (const rule of rules) {
      for (const t of texts) {
        const b = t.box;
        // Only text the rule actually runs alongside.
        if (b.bottom <= rule.top + 2 || b.top >= rule.bottom - 2) continue;
        if (b.left < rule.x - 0.5 && b.right > rule.x + 0.5) {
          crossings.push({
            rule: rule.owner, kind: rule.kind, text: t.text, el: cssPath(t.el),
            note: 'text runs through the rule — the divider is drawn over the words',
          });
          continue;
        }
        const gap = b.left >= rule.x ? b.left - rule.x : rule.x - b.right;
        // A negative gap is not a small gap. This measurement is a distance
        // between a rule and an ink box on one side of it, so a negative value
        // means the box straddles the rule in a way the crossing test above did
        // not catch — the text is ON the rule, not near it. Reporting it as
        // `gapPx: -139.5` was arithmetically meaningless and read as the worst
        // violation on the page.
        if (!(gap >= 0)) {
          crossings.push({
            rule: rule.owner, kind: rule.kind, text: t.text, el: cssPath(t.el),
            note: 'ink box straddles the rule — measured as a crossing, not a gap',
          });
          continue;
        }
        if (gap >= want) continue;
        const key = `${rule.owner}|${rule.kind}|${cssPath(t.el)}`;
        const prev = worst.get(key);
        if (!prev || gap < prev.gapPx) {
          worst.set(key, {
            rule: rule.owner, kind: rule.kind, el: cssPath(t.el), text: t.text,
            gapPx: Math.round(gap * 10) / 10,
            declaredPadPx: rule.declaredPadPx,
            side: b.left >= rule.x ? 'after' : 'before',
            belowFloor: gap < LI.dividerGutterPx,
          });
        }
      }
    }

    // Text cut off by an ancestor that clips. The row that is too tight is
    // usually also the row whose last cell loses its final words.
    //
    // MEASURED CAVEAT, Obscura, 14 Aug 2026: on a `overflow-x: hidden;
    // white-space: nowrap` box whose text is twice its width, Obscura reports
    // `overflowX` as `auto` and clamps the text's own client rect to the
    // container width, so the overflow is arithmetically invisible. Both halves
    // of this check therefore under-report on that engine, and an empty
    // `clipped` array is not evidence that nothing is cut. Chrome returns the
    // true inline extent and the check works there. `auto` and `scroll` are
    // accepted below because a horizontally scrolling row that cuts its last
    // cell is the same defect to a reader who never scrolls it.
    const clipped = [];
    const CLIPS = new Set(['hidden', 'clip', 'auto', 'scroll']);
    for (const t of texts) {
      for (let n = t.el; n && n !== document.body; n = n.parentElement) {
        const cs = getComputedStyle(n);
        if (!CLIPS.has(cs.overflowX)) continue;
        const c = n.getBoundingClientRect();
        if (t.box.right > c.right + 0.5 || t.box.left < c.left - 0.5) {
          clipped.push({
            el: cssPath(t.el), clipper: cssPath(n), text: t.text,
            overflow: cs.overflowX,
            overflowPx: Math.round(Math.max(t.box.right - c.right, c.left - t.box.left)),
          });
        }
        break;
      }
    }

    const violations = [...worst.values()].sort((a, b) => a.gapPx - b.gapPx);
    return {
      rules: rules.length,
      floorPx: LI.dividerGutterPx,
      wantPx: want,
      viewportWidth: window.innerWidth,
      violations: cap(violations),
      belowFloor: violations.filter(v => v.belowFloor).length,
      crossings: cap(crossings),
      clipped: cap(clipped),
      columnRules: cap(columnRules),
      // How many side borders were rejected as box outlines. A reviewer seeing
      // zero violations should be able to tell "no dividers were tight" from
      // "everything that looked like a divider was a button".
      selfOutlineSkipped,
      note: selfOutlineSkipped
        ? `${selfOutlineSkipped} side border(s) skipped as box outlines rather than dividers (they also paint top and bottom).`
        : null,
    };
  }

  function probeLayoutIntegrity() {
    const g = probeRepeatedGroupIntegrity();
    return {
      thresholds: LI,
      repeatedGroups: findRepeatedGroups().length,
      shapeMismatch: g.shapeMismatch,
      columnDrift: g.columnDrift,
      columnHeaderAlignment: probeColumnHeaderAlignment(),
      touchingHeadings: probeSiblingGaps(),
      rails: probeSharedRails(),
      textOverlap: probeTextOverlap(),
      deadSpace: probeDeadSpace(),
      columnVoids: probeColumnVoids(),
      implicitTracks: probeImplicitTracks(),
      dividerProximity: probeDividerProximity(),
      affordance: probeAffordanceGaps(),
      tokenOverload: probeTokenOverload(),
      inventory: probeComponentInventory(),
    };
  }

  /* ------------------------------------------------------------------ run */

  function runAll() {
    // Capability first, and the declaration index second, because every probe
    // below may consult them. Rebuilt per run rather than cached across
    // navigations: the index is a property of the document that is loaded now,
    // and a stale one would answer for a page that is gone.
    CAPABILITY = probeEngineCapability();
    DECLARED = buildDeclaredIndex();

    return {
      url: location.href,
      viewport: { width: window.innerWidth, height: window.innerHeight, dpr: window.devicePixelRatio },
      // What this engine will and will not answer, measured on this page. Read
      // this before reading any zero below it: an unreadable channel and a clean
      // surface produce the same number, and this is the only thing that tells
      // them apart.
      capability: CAPABILITY,
      declaredIndex: DECLARED.stats,
      // Every count below is meaningless without this pair. `settled: false` means
      // the numbers were sampled mid-animation and must be re-taken, not reported.
      settled: probeAnimationSettled(),
      stranded: probeStrandedElements(),
      contrast: probeContrast(),
      overflow: probeOverflow(),
      images: probeImages(),
      targets: probeTargets(),
      semantics: probeSemantics(),
      focus: probeFocusStyles(),
      layout: probeLayoutIntegrity(),
      tokens: probeUnconsumedTokens(),
      styles: dumpStyles(),
      prefersReducedMotionSupported: matchMedia('(prefers-reduced-motion: reduce)').media !== 'not all',
    };
  }

  window.__designReviewProbes = {
    runAll, probeContrast, probeOverflow, probeImages, probeTargets,
    probeSemantics, probeFocusStyles, dumpStyles, probeInk, contrastRatio,
    probeLayoutIntegrity, probeRepeatedGroupIntegrity, probeColumnHeaderAlignment,
    probeSiblingGaps, probeSharedRails, probeTextOverlap, probeDeadSpace,
    probeColumnVoids, inkBox, probeUnconsumedTokens, probeAnimationSettled,
    probeImplicitTracks, probeDividerProximity,
    probeAffordanceGaps, probeTokenOverload, findRepeatedGroups,
    probeComponentInventory,
    // The capability layer, exported so it can be run alone. `probeEngineCapability()`
    // in a console is the fastest way to characterise a new engine.
    initRun, probeEngineCapability, buildDeclaredIndex, styleValue, gradientStops,
    effectiveBackground, probeStrandedElements,
  };
})();
