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
      if (full.length >= 3) {
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
    if (heads.length < 2) return { clusters: [], disagreementPx: 0 };
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
      // Per-fragment, not the bounding box. An inline element that wraps returns
      // a bounding rect spanning both lines, which "overlaps" everything sitting
      // between them. getClientRects() gives one rect per line fragment.
      for (const r of el.getClientRects()) {
        if (r.width < 1 || r.height < 1) continue;
        nodes.push({ el, r, t: shortText(el).slice(0, 30) });
      }
    }
    const out = [];
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const a = nodes[i], b = nodes[j];
        if (a.el.contains(b.el) || b.el.contains(a.el)) continue;
        if (floatLayer(a.el) !== floatLayer(b.el)) continue;
        const w = Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left);
        const h = Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top);
        if (w >= LI.overlapMinPx && h >= LI.overlapMinPx) {
          out.push({
            a: cssPath(a.el), aText: a.t, b: cssPath(b.el), bText: b.t,
            overlapPx2: Math.round(w * h),
          });
        }
      }
    }
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
      affordance: probeAffordanceGaps(),
      tokenOverload: probeTokenOverload(),
      inventory: probeComponentInventory(),
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
      layout: probeLayoutIntegrity(),
      styles: dumpStyles(),
      prefersReducedMotionSupported: matchMedia('(prefers-reduced-motion: reduce)').media !== 'not all',
    };
  }

  window.__designReviewProbes = {
    runAll, probeContrast, probeOverflow, probeImages, probeTargets,
    probeSemantics, probeFocusStyles, dumpStyles, probeInk, contrastRatio,
    probeLayoutIntegrity, probeRepeatedGroupIntegrity, probeColumnHeaderAlignment,
    probeSiblingGaps, probeSharedRails, probeTextOverlap, probeDeadSpace,
    probeAffordanceGaps, probeTokenOverload, findRepeatedGroups,
    probeComponentInventory,
  };
})();
