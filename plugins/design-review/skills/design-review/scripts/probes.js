/**
 * probes.js — deterministic in-page probes for design review.
 *
 * Everything here reads the DOM at rest. That is the limit of what it can see:
 * an entrance has finished, a transient overlay is opacity 0. Motion bugs and
 * mid-transition defects need frame capture, not this file.
 *
 * Usage (Playwright):
 *   const probes = fs.readFileSync('probes.js', 'utf8');
 *   await page.addScriptTag({ content: probes });
 *   const result = await page.evaluate(() => window.__designReviewProbes.runAll());
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
    if (parseFloat(cs.opacity) === 0) return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
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

  /** Walk ancestors to find the first opaque-enough background. */
  function effectiveBackground(el) {
    let node = el;
    let stack = [];
    while (node && node !== document.documentElement.parentElement) {
      const cs = getComputedStyle(node);
      const c = parseColor(cs.backgroundColor);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') {
        return { color: null, unresolved: 'background-image', node: cssPath(node) };
      }
      if (c && c.a > 0) {
        stack.push(c);
        if (c.a >= 0.999) break;
      }
      node = node.parentElement;
    }
    if (!stack.length) return { color: { r: 255, g: 255, b: 255, a: 1 }, assumed: true };
    let base = stack.pop();
    if (base.a < 0.999) base = composite(base, { r: 255, g: 255, b: 255, a: 1 });
    while (stack.length) base = composite(stack.pop(), base);
    return { color: base };
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
   */
  function probeContrast() {
    const out = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const seen = new Set();
    let n;
    while ((n = walker.nextNode()) && out.length < 600) {
      const text = n.textContent.trim();
      if (!text) continue;
      const el = n.parentElement;
      if (!el || seen.has(el) || !visible(el)) continue;
      seen.add(el);
      const cs = getComputedStyle(el);
      const fg = parseColor(cs.color);
      if (!fg) continue;
      const bgInfo = effectiveBackground(el);
      if (!bgInfo.color) {
        out.push({
          selector: cssPath(el), text: text.slice(0, 60),
          skipped: bgInfo.unresolved, note: 'background not resolvable — check visually',
        });
        continue;
      }
      const fgFlat = fg.a < 0.999 ? composite(fg, bgInfo.color) : fg;
      const size = parseFloat(cs.fontSize);
      const weight = parseInt(cs.fontWeight, 10) || 400;
      const isLarge = size >= 24 || (size >= 18.66 && weight >= 700);
      const required = isLarge ? 3.0 : 4.5;
      const ratio = contrastRatio(fgFlat, bgInfo.color);
      if (ratio < required) {
        out.push({
          selector: cssPath(el),
          text: text.slice(0, 60),
          color: cs.color,
          background: `rgb(${Math.round(bgInfo.color.r)}, ${Math.round(bgInfo.color.g)}, ${Math.round(bgInfo.color.b)})`,
          fontSize: size, fontWeight: weight, isLarge,
          ratio: Math.round(ratio * 100) / 100,
          required,
          bgAssumed: !!bgInfo.assumed,
        });
      }
    }
    return out;
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
   * The evidence base for the systematisation pass. Every visible element's
   * design-relevant computed values, so variance and token adherence can be
   * measured offline rather than judged by eye.
   */
  function dumpStyles() {
    const nodes = [...document.querySelectorAll('*')].filter(visible).slice(0, MAX_NODES);
    return nodes.map(el => {
      const cs = getComputedStyle(el);
      const r = el.getBoundingClientRect();
      return {
        selector: cssPath(el),
        tag: el.tagName.toLowerCase(),
        hasText: !!(el.childNodes.length && [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())),
        fontFamily: cs.fontFamily,
        fontSize: cs.fontSize,
        fontWeight: cs.fontWeight,
        lineHeight: cs.lineHeight,
        letterSpacing: cs.letterSpacing,
        textTransform: cs.textTransform,
        color: cs.color,
        backgroundColor: cs.backgroundColor,
        borderRadius: cs.borderRadius,
        borderWidth: cs.borderWidth,
        borderColor: cs.borderColor,
        boxShadow: cs.boxShadow,
        margin: [cs.marginTop, cs.marginRight, cs.marginBottom, cs.marginLeft].join(' '),
        padding: [cs.paddingTop, cs.paddingRight, cs.paddingBottom, cs.paddingLeft].join(' '),
        gap: cs.gap,
        display: cs.display,
        maxWidth: cs.maxWidth,
        zIndex: cs.zIndex,
        transition: cs.transition,
        transitionProperty: cs.transitionProperty,
        transitionDuration: cs.transitionDuration,
        transitionTimingFunction: cs.transitionTimingFunction,
        animation: cs.animation,
        opacity: cs.opacity,
        cursor: cs.cursor,
        fontVariantNumeric: cs.fontVariantNumeric,
        width: Math.round(r.width),
        height: Math.round(r.height),
      };
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

  /* ------------------------------------------------------------------ run */

  function runAll() {
    return {
      url: location.href,
      viewport: { width: window.innerWidth, height: window.innerHeight, dpr: window.devicePixelRatio },
      contrast: probeContrast(),
      overflow: probeOverflow(),
      images: probeImages(),
      targets: probeTargets(),
      semantics: probeSemantics(),
      focus: probeFocusStyles(),
      styles: dumpStyles(),
      prefersReducedMotionSupported: matchMedia('(prefers-reduced-motion: reduce)').media !== 'not all',
    };
  }

  window.__designReviewProbes = {
    runAll, probeContrast, probeOverflow, probeImages, probeTargets,
    probeSemantics, probeFocusStyles, dumpStyles, probeInk, contrastRatio,
  };
})();
