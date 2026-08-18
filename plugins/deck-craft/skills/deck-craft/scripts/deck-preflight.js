/*
 * deck-preflight — the computable half of the deck gate.
 *
 * An in-page IIFE returning a JSON string. It runs the checks that do not need
 * an eye, so the looking you do afterwards is spent on judgment rather than on
 * finding a collision a rectangle comparison finds in 30ms.
 *
 * Drive it with `scripts/run-preflight.sh <url>`, or paste it into any
 * evaluate-JS channel:
 *
 *   obscura --allow-private-network fetch "$URL" --wait 3 \
 *     --eval "$(cat deck-preflight.js)"
 *
 * The whole file is ONE expression on purpose. Several evaluate-JS channels
 * (Obscura's `--eval` among them) return the value of the *first* statement,
 * so a payload of `window.cfg = {...}; (() => {…})()` silently evaluates to
 * null — a gate that looks like it ran and reported nothing. So the config is
 * substituted into this file's own final argument, replacing the string literal
 * __DECKCFG__ on the last line (written bare here so that this sentence does not
 * count as a second placeholder — the runner refuses to substitute unless it
 * finds exactly one). A string that survives substitution means
 * nothing was substituted, and the probe falls back to window.__deckPreflight
 * and then to defaults.
 *   { slideSelector, canvasW, canvasH, accent, regulated, bodyFloor, ... }
 *
 * That placeholder is load-bearing, and its shape is chosen from a measured
 * failure. Until 18 Aug 2026 the runner substituted by rewriting this file's
 * last two lines with a `sed` anchored on their literal text and three-space
 * indentation. Reproduced on this machine: reformatting the tail to the shape a
 * standard formatter emits —
 *   })(\n  typeof __DECKCFG !== "undefined"\n    ? __DECKCFG\n    : ...\n)
 * matches NEITHER anchor, so both substitutions no-op, the file stays valid
 * JavaScript, the payload falls through to `{}`, and `regulated` reverts to
 * false. A `--regulated` run then printed `[DECK-PREFLIGHT PASS] 0 blockers
 * across 3 slides examined` with all four disclosure checks never having run.
 *
 * A string literal is atomic: no formatter splits one across lines, so the only
 * thing that can change is its quote style, and the runner accepts either. The
 * runner asserts the placeholder is present exactly once BEFORE substituting,
 * and asserts the config this file echoes back matches what was asked AFTER.
 * Neither guard alone is enough — the first cannot see a substitution that
 * landed wrong, and the second cannot run if the probe never returned.
 *
 * What it CANNOT tell you, and why the looking still happens afterwards:
 * every rule here was written after someone met the defect it catches, so it
 * is structurally blind to the one nobody has met yet. A clean run means no
 * known computable defect is present. It never means the deck is good.
 */
((__CFG_IN) => {
 try {
  const DEFAULTS = {
    slideSelector: null,     // auto-detected when null
    canvasW: 1920,
    canvasH: 1080,
    accent: null,            // e.g. '#D72229'; auto-detected when null
    regulated: false,        // true for investor / financial / health / compliance decks
    bodyFloor: 24,           // px on a 1920-wide canvas. Derived, not chosen:
                             // investor-relations.md §1.1 solves it from the
                             // ISO 9241-303 16-arcminute floor at VR 3.
    tinyFloor: 18,           // px on a 1920-wide canvas; below this is unreadable at distance
    deadBandPx: 594,         // empty band at a slide's foot worth reporting: 55% of a
                             // 1080 canvas. It was 120px (11%) until 18 Aug 2026, which
                             // contradicted this skill's own doctrine — deck-review.md
                             // says open space in a slide's bottom third is correct
                             // composition and warns against the reflex to centre it,
                             // and visual-craft.md agrees. A well-composed four-slide
                             // deck measured 31-53% empty at the foot and drew a warning
                             // on every slide, which is how a gate teaches people to
                             // ignore it. The failure this check is really a proxy for —
                             // a fluid section that stopped at content height — is now
                             // caught directly by stageGeometry, so this threshold only
                             // has to catch a slide whose content fills less than half
                             // of it.
    displayFloorPx: 96,      // a deck with no type this large has no display tier
    overlapMinPx2: 12,       // ignore sub-pixel kisses
    accentMarkBudget: 3,     // accent objects per slide, text and drawn marks together
    moduleRepeatMax: 3,      // identical top-level slide structures before it reads as monotony
  };
  // A closed key set, refused rather than ignored. `Object.assign` accepts
  // anything, so `regualted: true` or `slideSelectr: '.s'` used to run the whole
  // gate on defaults and report a clean deck. A misspelling in a config is a
  // config that did not arrive, and that is the failure this file exists to make
  // impossible — so it is an error return, not a note.
  const badKeys = Object.keys(__CFG_IN || {}).filter((k) => !(k in DEFAULTS));
  if (badKeys.length) {
    return JSON.stringify({
      error: 'unknown config key(s): ' + badKeys.join(', '),
      known: Object.keys(DEFAULTS),
      note: 'preflight did NOT run — this is not a pass. An unknown key means the ' +
            'config you meant to pass did not arrive; fix the key rather than re-running.',
    }, null, 1);
  }
  const CFG = Object.assign({}, DEFAULTS, __CFG_IN || {});

  const out = {
    config: {}, slides: 0, stage: [], type: {}, overflow: [], collisions: [],
    textOverlap: [], paintOrder: [], charts: [], accent: [], deadSpace: [],
    textOverImage: [], provenance: null, notes: [],
    inkExtent: [], chromeReserve: [], hues: null, displayTier: null,
    externalRefs: [], leakedArithmetic: [],
    titleWrap: [], stageContentOverflow: [], stageBottomClearance: [],
    verticalSquish: [], cardOverflow: [],
    genericName: null, moduleRepeats: [], nonIfrsUnpaired: [],
    titles: [], numerals: [], axisMisleaders: [],
  };

  // ── Locate the slides ────────────────────────────────────────────────────
  const CANDIDATES = ['.slide', '.slide-wrap', '.slide-stage', '.stage',
                      'section[data-screen-label]', '[data-slide]', '.deck-slide'];
  let sel = CFG.slideSelector;
  if (!sel) {
    let best = 0;
    for (const c of CANDIDATES) {
      const n = document.querySelectorAll(c).length;
      if (n > best) { best = n; sel = c; }
    }
  }
  const slides = [...document.querySelectorAll(sel || '.slide')];
  // Echoed so the runner can assert that the config it asked for actually
  // arrived. `configKeysReceived` is the direct signal: a runner that passed
  // four keys against a probe that received zero is the substitution having
  // silently no-opped, which is not inferable from the findings alone.
  out.config = { slideSelector: sel, canvas: `${CFG.canvasW}x${CFG.canvasH}`,
                 regulated: CFG.regulated, bodyFloor: CFG.bodyFloor,
                 configKeysReceived: Object.keys(__CFG_IN || {}).sort() };
  out.slides = slides.length;
  if (!slides.length) {
    // A zero denominator is the canonical silent pass, and it is not
    // hypothetical: measured 18 Aug 2026, one run in four of a four-slide deck
    // returned zero slides here (the probe reaching the DOM before the page's
    // own load handler had run), and because the runner read only the blocker
    // counts it printed `[DECK-PREFLIGHT PASS] 0 blockers across 0 slides
    // examined` and exited 0. So say it in the summary, where the exit code is
    // computed, and not only in a note.
    out.notes.push('No slides matched. Pass slideSelector via window.__deckPreflight — ' +
                   'a zero denominator is a gate that never ran, not a clean deck.');
    out.summary = { slidesExamined: 0, zeroDenominator: true };
    out.policy = { blockers: ['zeroDenominator'], warnings: [],
                   denominators: { '*': 'slidesExamined' } };
    out.consequences = { zeroDenominator: 'nothing was examined, so every count in this ' +
      'run is a zero over a denominator of zero — indistinguishable from a clean deck. ' +
      'Pass --selector with the deck\'s own slide class, and if the deck builds its ' +
      'slides at runtime, give the page longer to settle before probing' };
    return JSON.stringify(out, null, 1);
  }

  const idOf = (el, i) => el.id || el.dataset.screenLabel || `#${i + 1}`;
  const vis = (el) => {
    const cs = getComputedStyle(el);
    return cs.display !== 'none' && cs.visibility !== 'hidden' && +cs.opacity > 0.05;
  };
  const rect = (el) => el.getBoundingClientRect();
  // A text leaf: carries text of its own rather than inheriting it from a
  // child. Wrappers must not count, or a full-height container reads as ink
  // reaching the slide's foot and the dead-space check reports nothing.
  const isLeafText = (el) => {
    const t = (el.textContent || '').trim();
    return !!t && ![...el.children].some((c) => (c.textContent || '').trim());
  };
  // Shared by the accent budget and the text-over-image list. Defined here
  // rather than inside one check, because a helper scoped to one step is a
  // ReferenceError in the next and the run reports that step as NOT RUN.
  const norm = (c) => {
    const m = String(c).match(/\d+/g);
    return m && m.length >= 3 ? `${+m[0]},${+m[1]},${+m[2]}` : null;
  };

  // The authored canvas may reach the viewport two different ways, and they
  // need opposite arithmetic. `getComputedStyle` reports font sizes BEFORE any
  // transform, so:
  //   • a stage scaled with transform:scale() already reports authored px —
  //     factor 1. Dividing by the scale here inflates a correct 104px display
  //     to 125px and invents a type scale the deck does not have.
  //   • a slide with no transform is a fluid box, and its type is only as
  //     large as it looks: normalise by how far its rendered height falls
  //     short of the authored canvas.
  const scaleFromTransform = (t) => {
    if (!t || t === 'none') return null;
    const n = t.match(/matrix3d\(([^)]+)\)/);
    if (n) { const v = n[1].split(',').map(Number); return v[0]; }
    const m = t.match(/matrix\(([^)]+)\)/);
    if (m) { const v = m[1].split(',').map(Number); return v[0]; }
    const s = t.match(/scale\(?\s*([\d.]+)/);
    return s ? parseFloat(s[1]) : null;
  };
  const transformScaleOf = (slide) => {
    const inner = slide.querySelector('.stage, [style*="scale"]') || slide;
    const s = scaleFromTransform(getComputedStyle(inner).transform);
    return (s && s > 0.01 && s < 3) ? s : null;
  };
  // px measured on screen → px on the authored canvas
  const toCanvasPx = (slide) => {
    const ts = transformScaleOf(slide);
    if (ts) return 1;                                  // already authored units
    const h = rect(slide).height;
    return h ? CFG.canvasH / h : 1;
  };
  // screen distances (gaps, overlaps, dead bands) → authored units
  const distFactor = (slide) => {
    const ts = transformScaleOf(slide);
    if (ts) return 1 / ts;
    const h = rect(slide).height;
    return h ? CFG.canvasH / h : 1;
  };
  const scaleOf = (slide) => 1 / distFactor(slide);

  // Each check runs inside this so a single engine gap degrades one section
  // rather than returning null for the whole gate. A gate that fails silently
  // is worse than no gate: its output is indistinguishable from a clean deck.
  const step = (name, fn) => {
    try { fn(); } catch (e) { out.notes.push(`check "${name}" failed: ${e && e.message} — treat as NOT RUN, not as clean`); }
  };

  // ── 1. Stage geometry ────────────────────────────────────────────────────
  step('Stage geometry', () => {
    // A deck is fixed-size content. A slide whose box is not the authored aspect
    // ratio is a web section wearing a slide's name: it reflowed instead of
    // letterboxing, so the presenter cannot predict what the audience sees.
    const wantAR = CFG.canvasW / CFG.canvasH;
    slides.forEach((s, i) => {
      const r = rect(s);
      if (!r.width || !r.height) return;
      const ar = r.width / r.height;
      const row = { slide: idOf(s, i), w: Math.round(r.width), h: Math.round(r.height),
                    aspect: +ar.toFixed(3), wantAspect: +wantAR.toFixed(3) };
      row.aspectOff = Math.abs(ar - wantAR) > 0.02;
      row.clipL = Math.max(0, Math.round(-r.left));
      row.clipR = Math.max(0, Math.round(r.right - innerWidth));
      if (row.aspectOff || row.clipL || row.clipR) out.stage.push(row);
    });

  });

  // ── 2. Type floor ────────────────────────────────────────────────────────
  step('Type floor', () => {
    // Web density (13–16px) is the reflex to resist: it is unreadable from row
    // four. Sizes are normalised to the authored canvas before comparison.
    // Two-tier floor: primary body/titles floor is bodyFloor (24px);
    // accessory text (eyebrows, fine footnotes, captions, stat notes, table data cells)
    // has a tinyFloor (18px) threshold.
    const sizes = {};
    const belowFloor = [];
    const isAccessory = (el, cls) => {
      const c = (cls || '').toLowerCase();
      const tag = el.tagName.toLowerCase();
      return (
        tag === 'th' || tag === 'td' || tag === 'figcaption' ||
        c.includes('eyebrow') || c.includes('fine') || c.includes('foot') ||
        c.includes('note') || c.includes('caption') || c.includes('chip') ||
        c.includes('lab') || c.includes('small') || c.includes('tip') ||
        c.includes('unit') || c.includes('xax') || el.hasAttribute('data-accessory') ||
        !!el.closest('.foot, footer, [class*="foot"], .fine, figcaption, [class*="note"], .xax, table')
      );
    };

    slides.forEach((s, i) => {
      const f = toCanvasPx(s);
      s.querySelectorAll('*').forEach((el) => {
        const t = (el.textContent || '').trim();
        if (!t || !vis(el)) return;
        if ([...el.children].some((c) => (c.textContent || '').trim())) return; // leaf text only
        const cs = getComputedStyle(el);
        const authored = Math.round(parseFloat(cs.fontSize) * f);
        sizes[authored] = (sizes[authored] || 0) + 1;
        const cls = String(el.className || '');
        const floor = isAccessory(el, cls) ? CFG.tinyFloor : CFG.bodyFloor;
        if (authored < floor) {
          belowFloor.push({ slide: idOf(s, i), px: authored,
                            cls: cls.slice(0, 40),
                            text: t.slice(0, 44) });
        }
      });
    });
    const scale = Object.keys(sizes).map(Number).sort((a, b) => a - b);
    out.type = {
      distinctSizes: scale.length,
      scale,
      medianPx: scale.length ? scale[Math.floor(scale.length / 2)] : null,
      largestPx: scale[scale.length - 1] || null,
      belowBodyFloor: belowFloor.length,
      belowTinyFloor: belowFloor.filter((b) => b.px < CFG.tinyFloor).length,
      samples: belowFloor.slice(0, 25),
    };

  });

  // ── 3. Overflow against the slide box ────────────────────────────────────
  step('Overflow against the slide box', () => {
    slides.forEach((s, i) => {
      if (s.scrollHeight > s.clientHeight + 2 || s.scrollWidth > s.clientWidth + 2) {
        out.overflow.push({ slide: idOf(s, i), kind: 'slide',
                            overflowY: s.scrollHeight - s.clientHeight,
                            overflowX: s.scrollWidth - s.clientWidth });
      }
      s.querySelectorAll('table, pre, .scroll, [class*="table"], [class*="grid"]').forEach((el) => {
        const p = el.parentElement; if (!p) return;
        if (el.scrollWidth > p.clientWidth + 2) {
          out.overflow.push({ slide: idOf(s, i), kind: el.tagName.toLowerCase(),
                              cls: String(el.className || '').slice(0, 40),
                              overflowX: el.scrollWidth - p.clientWidth });
        }
      });
    });

  });

  // ── 4. Collision with slide chrome ───────────────────────────────────────
  step('Collision with slide chrome', () => {
    // "Nothing past the stage bounds" is silent about content running INTO the
    // footer, the page number or a floating control dock — all inside the bounds.
    // Exclude global floating navigation rails/progress lines positioned outside slide bodies.
    const chromeSel = '.foot, .footer, [class*="foot"], [class*="dock"], [class*="controls"], ' +
                      '[class*="page-num"], [class*="slide-number"]';
    const docks = [...document.querySelectorAll(chromeSel)].filter((el) => {
      const cs = getComputedStyle(el);
      return vis(el) && (cs.position === 'fixed' || cs.position === 'absolute' || cs.position === 'sticky');
    });
    slides.forEach((s, i) => {
      const k = scaleOf(s);
      docks.forEach((d) => {
        // A dock that lives inside ANOTHER slide is not this slide's chrome. On a
        // vertical scroll deck every slide coexists in the layout, so comparing
        // slide N's content against slide M's pinned footer manufactures
        // collisions that no viewer can ever see. Measured: 10 such phantoms on
        // a deck whose real collisions were 0.
        const owner = slides.find((x) => x.contains(d));
        if (owner && owner !== s) return;
        const dr = rect(d);
        if (!dr.height) return;
        s.querySelectorAll('p,li,td,th,h1,h2,h3,h4,figure,table').forEach((el) => {
          if (d.contains(el) || el.contains(d)) return;
          // Ignore full-bleed background images or scrims
          if (el.tagName === 'IMG' || el.classList.contains('photo') || el.classList.contains('scrim')) return;
          const r = rect(el);
          if (!r.width || !r.height || !vis(el)) return;
          const overlapY = Math.min(r.bottom, dr.bottom) - Math.max(r.top, dr.top);
          const overlapX = Math.min(r.right, dr.right) - Math.max(r.left, dr.left);
          if (overlapY > 4 && overlapX > 4) {
            out.collisions.push({ slide: idOf(s, i),
                                  chrome: String(d.className || d.tagName).slice(0, 30),
                                  text: (el.textContent || '').trim().slice(0, 40),
                                  byPx: Math.round(Math.min(overlapY, overlapX) / k) });
          }
        });
      });
    });

  });

  // ── 5. Text overlapping text ─────────────────────────────────────────────
  step('Text overlapping text', () => {
    // Two labels sharing pixels. The signature: a bar's "Complete" caption laid
    // over its "100%" value, or a three-line bullet running into the next one.
    slides.forEach((s, i) => {
      const k = scaleOf(s);
      const leaves = [...s.querySelectorAll('*')].filter((el) => {
        const t = (el.textContent || '').trim();
        return t && vis(el) && ![...el.children].some((c) => (c.textContent || '').trim());
      }).slice(0, 400);
      for (let a = 0; a < leaves.length; a++) {
        for (let b = a + 1; b < leaves.length; b++) {
          const A = leaves[a], B = leaves[b];
          if (A.contains(B) || B.contains(A)) continue;
          const ra = rect(A), rb = rect(B);
          const ox = Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left);
          const oy = Math.min(ra.bottom, rb.bottom) - Math.max(ra.top, rb.top);
          if (ox > 1 && oy > 1 && (ox * oy) / (k * k) > CFG.overlapMinPx2) {
            out.textOverlap.push({ slide: idOf(s, i),
                                   a: (A.textContent || '').trim().slice(0, 30),
                                   b: (B.textContent || '').trim().slice(0, 30),
                                   px2: Math.round((ox * oy) / (k * k)) });
          }
        }
      }
    });
    out.textOverlap = out.textOverlap.slice(0, 40);

  });

  // ── 6. Paint order over full-bleed imagery ───────────────────────────────
  step('Paint order over full-bleed imagery', () => {
    // A slide whose entire copy is invisible under its own photograph has
    // perfect layout: real boxes, real sizes, correct fonts. Overflow,
    // collision, contrast and inventory checks all pass. Only a hit test finds it.
    slides.forEach((s, i) => {
      const heads = [...s.querySelectorAll('h1,h2,h3,.title,[class*="title"],[class*="head"]')]
        .filter((el) => (el.textContent || '').trim() && vis(el)).slice(0, 3);
      heads.forEach((h) => {
        const r = rect(h);
        if (!r.width || !r.height) return;
        const hit = document.elementFromPoint(r.left + Math.min(8, r.width / 2), r.top + r.height / 2);
        if (hit && hit !== h && !h.contains(hit) && !hit.contains(h)) {
          out.paintOrder.push({ slide: idOf(s, i),
                                text: (h.textContent || '').trim().slice(0, 40),
                                coveredBy: String(hit.className || hit.tagName).slice(0, 40) });
        }
      });
    });

  });

  // ── 7. Chart integrity — the axis-honesty check ──────────────────────────
  step('Chart integrity — the axis-honesty check', () => {
    // Length is the encoding. If bar length is not proportional to value, the
    // chart overstates its own change; on a results slide that is compliance
    // exposure rather than a taste question. Within one bar group,
    // length / value must be constant. Where it is not, the implied baseline
    // is solved for, because "the axis starts at 71.4" is a fact someone can
    // act on in a way that "this chart looks off" is not.
    //
    // Two paths, and the declared one is the one to build against:
    //  • DECLARED — mark the group `data-chart="bars"` and each bar
    //    `data-value="81.4"`. Exact, no heuristics, and the deck documents
    //    its own charts.
    //  • DETECTED — for auditing a deck you did not write. Deliberately
    //    strict: a loose detector produces false positives, and a gate people
    //    learn to ignore is worse than no gate. Groups that fail the
    //    strictness tests are counted as UNVERIFIED rather than as passing,
    //    so the coverage gap stays visible.
    const num = (s) => {
      const m = String(s == null ? '' : s).replace(/[, ]/g, '').match(/-?\d+(?:\.\d+)?/);
      return m ? parseFloat(m[0]) : null;
    };
    let unverified = 0;

    const judge = (slideId, kind, bars, declaresAxis, minBars) => {
      const good = bars.filter((b) => b.value !== null && b.value > 0 && b.len > 0.5);
      // Three is the floor for a DETECTED group, because two boxes of unequal
      // height beside two numbers is a shape that card grids and date strings
      // both make, and a loose detector produces a gate people learn to ignore.
      // A DECLARED pair is different in kind: the author wrote `data-value` and
      // an inline percentage on both bars, so there is no detection and nothing
      // to be noisy about — the arithmetic is exact. That distinction matters
      // more here than anywhere else in the file, because the shared-scale ROI
      // pair (deck-charts.md Pattern C) is a TWO-bar construction and is the
      // shape behind the "20x annualised payback" incident. Declining to judge
      // it made the highest-risk chart in the highest-risk deck type the one
      // shape the gate skipped.
      if (good.length < (minBars || 3)) return false;
      const vals = good.map((b) => b.value);
      if (Math.max(...vals) / Math.min(...vals) > 1000) return false;  // mixed units/years
      const ratios = good.map((b) => b.len / b.value);
      const lo = Math.min(...ratios), hi = Math.max(...ratios);
      const drift = (hi - lo) / hi;
      const row = { slide: slideId, kind, n: good.length, values: vals,
                    lengths: good.map((b) => Math.round(b.len)),
                    ratioDrift: +drift.toFixed(3), zeroBased: drift <= 0.02,
                    declaresAxis: !!declaresAxis };
      if (!row.zeroBased) {
        const [p, q] = [good[0], good[good.length - 1]];
        const denom = p.len - q.len;
        if (Math.abs(denom) > 0.001) {
          row.impliedBaseline = +(((p.len * q.value - q.len * p.value) / denom)).toFixed(1);
          const real = (Math.max(...vals) - Math.min(...vals)) / Math.max(...vals);
          const shown = (Math.max(...row.lengths) - Math.min(...row.lengths)) / Math.max(...row.lengths);
          row.realChangePct = +(real * 100).toFixed(1);
          row.shownChangePct = +(shown * 100).toFixed(1);
          row.exaggeration = real > 0 ? +(shown / real).toFixed(1) : null;
        }
      }
      out.charts.push(row);
      return true;
    };

    slides.forEach((s, i) => {
      const id = idOf(s, i);
      const declaresAxis = /axis (begins|starts)|begins at zero|zero-based|from zero/i
        .test(s.textContent || '');

      // (a) DECLARED groups
      s.querySelectorAll('[data-chart]').forEach((g) => {
        const bars = [...g.querySelectorAll('[data-value]')].map((b) => {
          const r = rect(b);
          const inline = b.getAttribute('style') || '';
          const pct = inline.match(/(?:height|width)\s*:\s*([\d.]+)%/);
          const len = pct ? parseFloat(pct[1]) : Math.max(r.height, r.width);
          return { len, value: num(b.dataset.value), declared: !!pct };
        });
        // Two is enough only when every bar carries its own authored percentage.
        // A declared group whose lengths had to be measured is back to being a
        // measurement, and Obscura resolves neighbouring percentage heights to
        // one pixel value, so the three-bar floor still applies to it.
        const allDeclared = bars.length > 0 && bars.every((b) => b.declared);
        if (!judge(id, 'declared:' + g.dataset.chart, bars, declaresAxis,
                   allDeclared ? 2 : 3)) unverified++;
      });

      // (b) DETECTED — SVG columns on a shared baseline.
      // Labels are matched on the `x` ATTRIBUTE, not on a laid-out box: some
      // engines report a zero-width rect for <text>, which collapses every
      // horizontal distance to the same value and silently pairs all three
      // bars with the first label.
      s.querySelectorAll('svg').forEach((svg) => {
        if (svg.closest('[data-chart]')) return;
        const rects = [...svg.querySelectorAll('rect')]
          .filter((r) => parseFloat(r.getAttribute('height')) > 2 &&
                         parseFloat(r.getAttribute('width')) > 2);
        if (rects.length < 3) return;
        const baseline = rects.map((r) => parseFloat(r.getAttribute('y')) +
                                          parseFloat(r.getAttribute('height')));
        const sharesBase = Math.max(...baseline) - Math.min(...baseline) <= 2;
        const widths = rects.map((r) => parseFloat(r.getAttribute('width')));
        const sameWidth = Math.max(...widths) - Math.min(...widths) <= 2;
        if (!sharesBase || !sameWidth) { unverified++; return; }
        const texts = [...svg.querySelectorAll('text')]
          .filter((t) => /\d/.test(t.textContent || ''));
        const bars = rects.map((r) => {
          const cx = parseFloat(r.getAttribute('x')) + parseFloat(r.getAttribute('width')) / 2;
          const ry = parseFloat(r.getAttribute('y'));
          let best = null, bestD = 1e9;
          texts.forEach((t) => {
            const tx = parseFloat(t.getAttribute('x'));
            const ty = parseFloat(t.getAttribute('y'));
            if (!isFinite(tx) || !isFinite(ty)) return;
            if (ty > ry) return;                       // value labels sit above the bar
            const d = Math.abs(tx - cx);
            if (d < bestD) { bestD = d; best = t; }
          });
          return { len: parseFloat(r.getAttribute('height')),
                   value: best && bestD < widths[0] ? num(best.textContent) : null };
        });
        if (new Set(bars.map((b) => b.value)).size < bars.length) { unverified++; return; }
        if (!judge(id, 'svg-rect', bars, declaresAxis)) unverified++;
      });

      // (c) DETECTED — HTML columns: sibling cells, each holding one drawn bar
      // and one numeric label, all bars on a shared baseline and of equal
      // cross-width. Anything less strict matches card grids and date strings.
      s.querySelectorAll('*').forEach((p) => {
        if (p.closest('[data-chart]')) return;
        const kids = [...p.children].filter((c) => vis(c));
        if (kids.length < 3 || kids.length > 8) return;
        const cells = kids.map((c) => {
          const bar = c.querySelector('[class*="bar"],[class*="fill"],[style*="height:"],[style*="width:"]');
          if (!bar || bar === c) return null;
          const br = rect(bar);
          if (br.width < 4 || br.height < 4) return null;
          // Prefer the DECLARED length over the measured one. Percentage
          // heights are where rendering engines diverge: Obscura resolves
          // `height:84.0%` and `height:86.4%` to the same computed px and
          // returns a bounding rect that matches neither, which turns an
          // honest zero-based chart into a false axis-truncation finding.
          // A declared percentage is exact, engine-independent, and is the
          // number the author actually wrote.
          const inline = bar.getAttribute('style') || '';
          const pct = inline.match(/(?:height|width)\s*:\s*([\d.]+)%/);
          const labelEl = [...c.querySelectorAll('*')].find(
            (e) => e !== bar && !bar.contains(e) && !e.contains(bar) &&
                   isLeafText(e) && /\d/.test(e.textContent || ''));
          return { br, declared: pct ? parseFloat(pct[1]) : null,
                   value: num(labelEl && labelEl.textContent) };
        });
        if (cells.some((c) => !c)) return;
        const boxes = cells.map((c) => c.br);
        const vertical = boxes[0].height >= boxes[0].width;
        const base = boxes.map((b) => (vertical ? b.bottom : b.left));
        const cross = boxes.map((b) => (vertical ? b.width : b.height));
        if (Math.max(...base) - Math.min(...base) > 2) return;   // no shared baseline
        if (Math.max(...cross) - Math.min(...cross) > 2) return; // not uniform bars
        const lens = boxes.map((b) => (vertical ? b.height : b.width));
        if (new Set(lens.map(Math.round)).size < 2) return;      // all equal: not a chart
        // Declared lengths win where every bar has one; measurement is the
        // fallback for bars sized by the layout rather than by an author.
        const allDeclared = cells.every((c) => c.declared !== null);
        const bars = cells.map((c, n) => ({ len: allDeclared ? c.declared : lens[n],
                                            value: c.value }));
        if (allDeclared && new Set(bars.map((b) => b.len)).size < 2) return;
        if (new Set(bars.map((b) => b.value)).size < bars.length) { unverified++; return; }
        if (!judge(id, 'html-bar', bars, declaresAxis)) unverified++;
      });
    });

    // de-duplicate nested matches over the same value set
    const seen = new Set();
    out.charts = out.charts.filter((c) => {
      const k = c.slide + JSON.stringify(c.values);
      if (seen.has(k)) return false; seen.add(k); return true;
    });
    out.chartsUnverified = unverified;
  });

  // ── 8. Accent budget ─────────────────────────────────────────────────────
  step('Accent budget', () => {
    // One thing carries the colour. An accent on four elements is a decoration,
    // not a signal — the slide stopped saying which number matters.
    const norm2 = norm;
    let accent = CFG.accent ? norm2(CFG.accent.replace(/^#/, '').match(/../g)
      .map((h) => parseInt(h, 16)).join(',')) : null;
    if (!accent) {
      const tally = {};
      slides.forEach((s) => s.querySelectorAll('*').forEach((el) => {
        if (!vis(el)) return;
        const cs = getComputedStyle(el);
        [cs.color, cs.backgroundColor].forEach((c) => {
          const n = norm(c); if (!n) return;
          const [r, g, b] = n.split(',').map(Number);
          const mx = Math.max(r, g, b), mn = Math.min(r, g, b);
          if (mx - mn > 60 && mx > 80) tally[n] = (tally[n] || 0) + 1;   // saturated only
        });
      }));
      accent = Object.entries(tally).sort((a, b) => b[1] - a[1])[0]?.[0] || null;
    }
    if (accent) {
      slides.forEach((s, i) => {
        const k = scaleOf(s);
        let textMarks = 0, drawnMarks = 0;
        s.querySelectorAll('*').forEach((el) => {
          if (!vis(el)) return;
          const cs = getComputedStyle(el);
          const hasOwnText = !!(el.textContent || '').trim() &&
            ![...el.children].some((c) => (c.textContent || '').trim());
          if (hasOwnText) {
            if (norm(cs.color) === accent || norm(cs.backgroundColor) === accent) textMarks++;
            return;
          }
          // A DRAWN mark. Stated twice in this skill and never counted until
          // 18 Aug 2026: "an automated check walks text-bearing leaves, so
          // filled bars, rules, tracks and dots score zero while the eye counts
          // every one of them" (visual-craft.md), and "four accent-filled
          // 'complete' progress bars plus one accent chip read as five accent
          // objects to the eye and as one to the gate" (deck-charts.md). The eye
          // does not care whether a mark carries text, so neither does the
          // budget. Wrappers are excluded by requiring the fill on this element
          // and an area small enough not to be a panel: a full-bleed accent
          // ground is a scheme decision, not an accent spend.
          if ((el.textContent || '').trim()) return;         // wrapper of text elsewhere
          const filled = norm(cs.backgroundColor) === accent ||
                         norm(cs.fill) === accent || norm(cs.borderTopColor) === accent;
          if (!filled) return;
          const r = rect(el);
          const areaAuthored = (r.width / k) * (r.height / k);
          if (areaAuthored < 400) return;                    // sub-20px fleck: not a mark
          if (areaAuthored > CFG.canvasW * CFG.canvasH * 0.25) return;  // a ground, not a mark
          drawnMarks++;
        });
        const n = textMarks + drawnMarks;
        if (n > CFG.accentMarkBudget) {
          out.accent.push({ slide: idOf(s, i), accentRgb: accent, elements: n,
                            textMarks, drawnMarks, budget: CFG.accentMarkBudget });
        }
      });
    }

  });

  // ── 9. Dead space at the foot of a slide ─────────────────────────────────
  step('Dead space at the foot of a slide', () => {
    // Open space in a slide's bottom third is correct composition, not a defect.
    // What this reports is the band BELOW the lowest ink, which is where a
    // fluid section that stopped at content height gives itself away.
    slides.forEach((s, i) => {
      const k = scaleOf(s);
      const sr = rect(s);
      let lowest = sr.top;
      s.querySelectorAll('*').forEach((el) => {
        if (!vis(el)) return;
        const isInk = isLeafText(el) ||
          el.matches('img,svg,canvas,video,hr,[class*="bar"],[class*="rule"]');
        if (!isInk) return;
        const r = rect(el);
        if (r.height && r.bottom > lowest && r.bottom <= sr.bottom + 1) lowest = r.bottom;
      });
      const band = Math.round((sr.bottom - lowest) / k);
      if (band > CFG.deadBandPx) {
        out.deadSpace.push({ slide: idOf(s, i), emptyFootPx: band,
                             pctOfCanvas: +((band / CFG.canvasH) * 100).toFixed(1) });
      }
    });

  });

  // ── 10. Text set over raster, with no protecting layer ───────────────────
  step('Text set over raster, with no protecting layer', () => {
    // Not a pass/fail — a look-here list. A DOM probe cannot sample the pixels
    // under a photograph, so this narrows where a human eye is actually needed.
    slides.forEach((s, i) => {
      const media = [...s.querySelectorAll('img, video, [style*="background-image"]')]
        .filter((m) => { const r = rect(m); return r.width > 200 && r.height > 200; });
      if (!media.length) return;
      s.querySelectorAll('*').forEach((el) => {
        const t = (el.textContent || '').trim();
        if (!t || !vis(el)) return;
        if ([...el.children].some((c) => (c.textContent || '').trim())) return;
        const r = rect(el);
        const over = media.some((m) => {
          const mr = rect(m);
          return r.left >= mr.left - 2 && r.right <= mr.right + 2 &&
                 r.top >= mr.top - 2 && r.bottom <= mr.bottom + 2;
        });
        if (!over) return;
        // a protecting layer = an ancestor between text and media carrying a
        // non-transparent background or a backdrop filter
        let guard = false, p = el;
        for (let d = 0; d < 4 && p && p !== s; d++, p = p.parentElement) {
          const cs = getComputedStyle(p);
          const a = norm(cs.backgroundColor) && !/,\s*0\)/.test(cs.backgroundColor);
          if ((a && cs.backgroundColor !== 'rgba(0, 0, 0, 0)') ||
              cs.backdropFilter !== 'none' || /gradient/.test(cs.backgroundImage)) { guard = true; break; }
        }
        if (!guard) {
          out.textOverImage.push({ slide: idOf(s, i), text: t.slice(0, 40),
                                   sizePx: Math.round(parseFloat(getComputedStyle(el).fontSize) / scaleOf(s)),
                                   colour: getComputedStyle(el).color });
        }
      });
    });
    out.textOverImage = out.textOverImage.slice(0, 30);

  });

  // ── 11. Provenance, for decks a reader will act on ───────────────────────
  step('Provenance, for decks a reader will act on', () => {
    // A figure with no stated provenance is not neutral: it reads as
    // authoritative, because that is the default a reader applies.
    if (CFG.regulated) {
      const body = document.body.innerText || '';
      const has = (re) => re.test(body);
      out.provenance = {
        auditQualifier: has(/unaudited|audited|not subject to (external )?(audit|review)/i),
        asAtDate: has(/as at|as of|for the (quarter|period|year) end/i),
        axisDisclosure: out.charts.length ? has(/axis (begins|starts)|from zero|zero-based/i) : null,
        illustrativeMarked: has(/illustrative|indicative|generated|placeholder|synthetic/i),
        disclaimer: has(/disclaimer|forward.looking|no reliance|authorised for release/i),
      };
      out.provenance.missing = Object.entries(out.provenance)
        .filter(([k, v]) => v === false).map(([k]) => k);
    }

  });

  // ── 11. Ink extent — the check `scrollHeight` structurally cannot make ───
  step('Ink extent past the slide box', () => {
    // Measured on a real deck, 15 Aug 2026: a slide whose table ran 85px past
    // its own bottom edge reported scrollHeight === clientHeight === 624, so
    // the scroll-extent check above scored it CLEAN while an entire table row
    // sat clipped under the floating chrome. A clipping ancestor (or
    // overflow:hidden) erases scrollHeight; it does not move the ink. So
    // measure where the ink actually is, in authored px, per slide.
    slides.forEach((s, i) => {
      const k = scaleOf(s);
      const sr = rect(s);
      let worstB = 0, worstR = 0, whoB = '', whoR = '';
      s.querySelectorAll('*').forEach((el) => {
        const paints = isLeafText(el) || ['IMG', 'SVG', 'CANVAS', 'VIDEO'].includes(el.tagName);
        if (!paints || !vis(el)) return;
        const r = rect(el);
        if (!r.width || !r.height) return;
        const b = (r.bottom - sr.bottom) / k;
        const rt = (r.right - sr.right) / k;
        const label = ((el.textContent || '').trim() || el.tagName).slice(0, 34);
        if (b > worstB) { worstB = b; whoB = label; }
        if (rt > worstR) { worstR = rt; whoR = label; }
      });
      if (worstB > 2 || worstR > 2) {
        out.inkExtent.push({ slide: idOf(s, i),
                             pastBottomPx: Math.round(worstB), atBottom: whoB,
                             pastRightPx: Math.round(worstR), atRight: whoR });
      }
    });
  });

  // ── 12. Floating chrome against the slide BOX, not just its text ─────────
  step('Floating chrome reserve', () => {
    // A dock that clears the last line of text but sits over the slide's lower
    // edge still reads as chrome on top of the artwork, and it hides whatever
    // the next revision puts there. Measured: a controller overlapping the
    // stage on all 12 slides of one deck while the text-vs-dock check scored 0,
    // because the footer line happened to stop 17px short of it.
    const docks = [...document.querySelectorAll('*')].filter((el) => {
      if (!vis(el) || getComputedStyle(el).position !== 'fixed') return false;
      if (slides.some((s) => s.contains(el) || el.contains(s))) return false;
      const r = rect(el);
      return r.width > 40 && r.height > 16 && r.width < innerWidth * 0.92;
    });
    docks.forEach((d) => {
      const dr = rect(d);
      slides.forEach((s, i) => {
        const sr = rect(s);
        const oy = Math.min(sr.bottom, dr.bottom) - Math.max(sr.top, dr.top);
        const ox = Math.min(sr.right, dr.right) - Math.max(sr.left, dr.left);
        if (oy > 2 && ox > 2) {
          out.chromeReserve.push({ slide: idOf(s, i),
            chrome: String(d.className || d.id || d.tagName).slice(0, 24),
            overlapPx: Math.round(Math.min(oy, ox)) });
        }
      });
    });
  });

  // ── 13. Hue budget — one accent, counted across the whole deck ───────────
  step('Hue budget', () => {
    // "One accent, never two" is a rule every brand states and every generated
    // deck breaks the same way: status chips reach for green for done and blue
    // for in-progress, and the deck now carries three hues. Measured on two
    // decks from one brief and one DESIGN.md: 1 hue family against 3.
    const hueOf = (c) => {
      const m = String(c).match(/[\d.]+/g);
      if (!m || m.length < 3) return null;
      if (m.length > 3 && parseFloat(m[3]) < 0.06) return null;
      const v = m.slice(0, 3).map((x) => Number(x) / 255);
      const mx = Math.max.apply(null, v), mn = Math.min.apply(null, v), d = mx - mn;
      if (d < 0.10 || mx < 0.12) return 'neutral';
      let hh = 0;
      if (mx === v[0]) hh = 60 * (((v[1] - v[2]) / d) % 6);
      else if (mx === v[1]) hh = 60 * ((v[2] - v[0]) / d + 2);
      else hh = 60 * ((v[0] - v[1]) / d + 4);
      return Math.round(((hh + 360) % 360) / 30) * 30 % 360;
    };
    const fam = {};
    slides.forEach((s) => {
      s.querySelectorAll('*').forEach((el) => {
        if (!vis(el)) return;
        const r = rect(el); if (!r.width || !r.height) return;
        const cs = getComputedStyle(el);
        [isLeafText(el) ? cs.color : null, cs.backgroundColor].forEach((c) => {
          if (!c) return;
          const hv = hueOf(c);
          if (hv === null || hv === 'neutral') return;
          fam[hv] = (fam[hv] || 0) + 1;
        });
      });
    });
    // 3+ marks before a hue counts as a family: one stray swatch is not a palette.
    const fams = Object.keys(fam).filter((k) => fam[k] >= 3)
      .map((k) => ({ hue: Number(k), marks: fam[k] }))
      .sort((a, b) => b.marks - a.marks);
    out.hues = { families: fams, count: fams.length,
                 extra: fams.slice(1) };
  });

  // ── 14. Display tier ─────────────────────────────────────────────────────
  step('Display tier present', () => {
    // A deck whose largest type is 76px on a 1920 canvas has no display tier:
    // its cover reads as a web hero and every slide below inherits the flat
    // ramp. Measured across two decks from one brief: 132px against 76px, and
    // the smaller ramp carried 13 distinct sizes against 19.
    const mx = out.type && out.type.largestPx;
    if (mx && mx < CFG.displayFloorPx) {
      out.displayTier = { largestPx: mx, floorPx: CFG.displayFloorPx,
        note: 'no display tier: the deck\'s largest type is below the cover floor' };
    }
  });

  // ── 15. Single-file portability ──────────────────────────────────────────
  step('Single-file portability', () => {
    // A deck that <link>s a webfont opens in a different typeface offline, on a
    // plane, behind a strict CSP, and inside a sandboxed investor portal — the
    // four places a deck is most often actually read.
    out.externalRefs = [...document.querySelectorAll('link[href],script[src],img[src],source[src]')]
      .map((el) => el.getAttribute('href') || el.getAttribute('src') || '')
      .filter((u) => /^(https?:)?\/\//i.test(u))
      .slice(0, 12);
  });

  // ── 16. Checker arithmetic leaked into slide copy ────────────────────────
  step('Leaked gate arithmetic', () => {
    // A deck written to satisfy its own gate starts printing the gate's working
    // where the disclosure belongs. Measured: "Constant ratio 1.1765%" in the
    // chart note on three slides of one investor deck. The reader is owed the
    // axis disclosure and the as-at date; the author's proof of honesty is not
    // a disclosure and reads as one.
    const RX = /(constant ratio|ratio\s*[:=]\s*[\d.]+|scale factor\s*[:=]|zero-?based\s*[:=]\s*true|gate (passed|clean)|preflight)/i;
    slides.forEach((s, i) => {
      s.querySelectorAll('*').forEach((el) => {
        if (!isLeafText(el) || !vis(el)) return;
        const t = (el.textContent || '').trim();
        if (t && RX.test(t)) out.leakedArithmetic.push({ slide: idOf(s, i), text: t.slice(0, 72) });
      });
    });
  });

  // ── 17. Title line wrapping & heading explosion ───────────────────────────
  step('Title line wrapping and heading explosion', () => {
    // A headline wrapping onto 3+ lines (or cover title onto >2 lines) steals
    // 100-200px of vertical budget, forcing content downward into chrome or clipping.
    // Detects line count and awkward wrap explosions programmatically without screenshotting.
    slides.forEach((s, i) => {
      const k = scaleOf(s);
      const titles = [...s.querySelectorAll('h1, h2, .slide-title, [class*="slide-title"], [class*="hero-title"]')].filter(vis);
      titles.forEach((h) => {
        const cs = getComputedStyle(h);
        const lh = parseFloat(cs.lineHeight) || (parseFloat(cs.fontSize) * 1.15);
        const r = rect(h);
        if (!r.width || !r.height) return;
        // Count lines from the box, NOT from getClientRects(). A heading is a
        // block, and getClientRects() on a block returns exactly ONE rect per
        // spec — its border box — so `clientRects.length` is 1 for a title
        // wrapping onto five lines, and reading it first made this check
        // unfireable. A predicate that always returns 1 reports every deck
        // clean, which is indistinguishable from a deck with no wrapped titles.
        //
        // Both operands must be in the same space: getBoundingClientRect is
        // POST-transform while computed line-height and padding are authored
        // values, so the height is divided back up by the stage scale first.
        // Measured on a title at 64px/70.4px wrapping to three lines inside a
        // stage at k=0.646: r.height 136 gives 136/70.4 = 2 lines (wrong, and
        // under the threshold), where (136/0.646)/70.4 = 3 (right).
        const padY = (parseFloat(cs.paddingTop) || 0) + (parseFloat(cs.paddingBottom) || 0);
        const lines = Math.max(1, Math.round((r.height / (k || 1) - padY) / lh));
        // Computed font-size is ALREADY an authored value — an ancestor
        // transform scales the painted box, not the resolved CSS. Dividing it by
        // the stage scale inflated it by 1/k, which both mis-set the cover
        // threshold and printed a wrong number into the finding: a title
        // authored at 64px inside a stage at k=0.646 was reported as 99px.
        const authoredFontPx = parseFloat(cs.fontSize);
        const isCover = i === 0 || s.id === 'slide-1' || h.tagName.toLowerCase() === 'h1' || authoredFontPx >= CFG.displayFloorPx;
        const maxAllowed = isCover ? 2 : 3;
        if (lines > maxAllowed) {
          out.titleWrap.push({
            slide: idOf(s, i),
            text: (h.textContent || '').trim().slice(0, 48),
            lines,
            maxAllowed,
            fontSizePx: Math.round(authoredFontPx)
          });
        }
      });
    });
  });

  // ── 18. Internal stage & content overflow ──────────────────────────────────
  step('Internal stage content overflow', () => {
    // When a slide-wrapper has overflow:hidden and a scaled stage inside,
    // wrapper.scrollHeight matches clientHeight while stage content quietly overflows.
    // This probes the unscaled stage and its content boxes directly.
    slides.forEach((s, i) => {
      const k = scaleOf(s);
      const sr = rect(s);
      const stage = s.querySelector('.slide-stage, .stage, [class*="stage"]') || s;
      if (stage !== s && (stage.scrollHeight > CFG.canvasH + 4 || stage.scrollWidth > CFG.canvasW + 4)) {
        out.stageContentOverflow.push({
          slide: idOf(s, i),
          overflowY: Math.max(0, stage.scrollHeight - CFG.canvasH),
          overflowX: Math.max(0, stage.scrollWidth - CFG.canvasW),
          container: String(stage.className || stage.tagName).slice(0, 30)
        });
      }
      const contents = s.querySelectorAll('.stage-content, .slide-content, [class*="content"]');
      contents.forEach((c) => {
        if (!vis(c)) return;
        const cr = rect(c);
        const authoredH = cr.height / k;
        if (authoredH > CFG.canvasH - 16) {
          const lastChild = c.lastElementChild;
          if (lastChild) {
            const lcr = rect(lastChild);
            const bottomAuthored = (lcr.bottom - sr.top) / k;
            if (bottomAuthored > CFG.canvasH + 2) {
              out.stageContentOverflow.push({
                slide: idOf(s, i),
                overflowY: Math.round(bottomAuthored - CFG.canvasH),
                container: String(c.className || c.tagName).slice(0, 30)
              });
            }
          }
        }
      });
    });
  });

  // ── 19. Stage bottom clearance floor ───────────────────────────────────────
  step('Stage bottom clearance floor', () => {
    // Content running within a few pixels of the stage bottom border looks squeezed
    // and collides with presentation docks or hardware bezel clipping.
    slides.forEach((s, i) => {
      const k = scaleOf(s);
      const sr = rect(s);
      let lowestInk = sr.top;
      let hasFooter = false;
      let footerTop = sr.bottom;
      s.querySelectorAll('*').forEach((el) => {
        if (!vis(el)) return;
        if (el.matches('.foot, .footer, [class*="foot"], footer')) {
          hasFooter = true;
          const fr = rect(el);
          if (fr.top < footerTop) footerTop = fr.top;
          return;
        }
        const isInk = isLeafText(el) || el.matches('img,svg,canvas,video,hr,[class*="bar"],[class*="card"]');
        if (!isInk) return;
        const r = rect(el);
        if (r.height && r.bottom > lowestInk && r.bottom <= sr.bottom + 10) {
          lowestInk = r.bottom;
        }
      });
      const clearancePx = Math.round((sr.bottom - lowestInk) / k);
      if (!hasFooter && clearancePx < 16) {
        out.stageBottomClearance.push({
          slide: idOf(s, i),
          clearancePx,
          minRequiredPx: 20,
          note: 'content extends to canvas bottom edge with insufficient margin'
        });
      }
      if (hasFooter && footerTop > lowestInk) {
        const gapAboveFooter = Math.round((footerTop - lowestInk) / k);
        if (gapAboveFooter < 6) {
          out.stageBottomClearance.push({
            slide: idOf(s, i),
            clearancePx: gapAboveFooter,
            minRequiredPx: 10,
            note: 'content crowded against footer top edge'
          });
        }
      }
    });
  });

  // ── 20. Vertical block clearance ───────────────────────────────────────────
  step('Vertical block clearance', () => {
    // When elements in flex/grid are too large, vertical gaps collapse to 0,
    // squishing titles, card grids, highlight strips, and footers together.
    slides.forEach((s, i) => {
      const k = scaleOf(s);
      const stageContent = s.querySelector('.stage-content, .slide-content, .slide-stage, .stage') || s;
      const blocks = [...stageContent.children].filter((c) => vis(c) && !['IMG', 'VIDEO'].includes(c.tagName) && !c.classList.contains('stage-bg-image') && !c.classList.contains('stage-scrim-dark') && !c.classList.contains('scrim') && getComputedStyle(c).position !== 'absolute');
      for (let b = 0; b < blocks.length - 1; b++) {
        const topEl = blocks[b];
        const btmEl = blocks[b + 1];
        const rTop = rect(topEl);
        const rBtm = rect(btmEl);
        if (!rTop.height || !rBtm.height) continue;
        const gap = (rBtm.top - rTop.bottom) / k;
        // A small block sitting tight above a much larger one is a label and its
        // heading: an eyebrow over a title is a deliberate typographic unit, and
        // the gap between them is meant to be nothing. Measured 18 Aug 2026: this
        // check fired on all four slides of a correctly composed deck for exactly
        // that pair. Squish is two blocks of comparable weight collapsing into
        // each other, so require that before reporting one.
        const hTop = rTop.height / k, hBtm = rBtm.height / k;
        const labelPair = hTop < 40 && hBtm > hTop * 1.6;
        if (gap < 2 && gap >= -2 && !labelPair) {
          out.verticalSquish.push({
            slide: idOf(s, i),
            between: [String(topEl.className || topEl.tagName).slice(0, 24), String(btmEl.className || btmEl.tagName).slice(0, 24)],
            gapPx: Math.round(gap),
            minExpectedPx: 8
          });
        }
      }
    });
  });

  // ── 21. Card & panel container overflow ────────────────────────────────────
  step('Card & panel container overflow', () => {
    slides.forEach((s, i) => {
      s.querySelectorAll('.stat-card, .card-surface, [class*="card"], .chart-panel').forEach((card) => {
        if (!vis(card)) return;
        if (card.scrollHeight > card.clientHeight + 2 || card.scrollWidth > card.clientWidth + 2) {
          out.cardOverflow.push({
            slide: idOf(s, i),
            card: String(card.className || card.tagName).slice(0, 30),
            overflowY: Math.max(0, card.scrollHeight - card.clientHeight),
            overflowX: Math.max(0, card.scrollWidth - card.clientWidth)
          });
        }
      });
    });
  });

  // ── 22. The deck's own name ────────────────────────────────────────────────
  step('Generic deck name', () => {
    // The filename and the <title> are what the deck is CALLED. An HTML deck is
    // emailed, dropped in a Slack channel and attached to a board paper, so the
    // filename is what a director sees in their downloads folder — and
    // `deck.html` beside four other `deck.html` files is a real failure. This
    // skill's own copy-paste shell shipped `<title>Deck</title>` until
    // 18 Aug 2026, which is the deck-domain member of exactly this refusal set.
    const GENERIC_TITLES = new Set(['deck', 'the deck', 'presentation', 'slides',
      'slide deck', 'untitled', 'untitled deck', 'new deck', 'my deck', 'pitch deck',
      'document', 'name-this-from-the-content']);
    const GENERIC_FILES = new Set(['deck.html', 'deck.htm', 'presentation.html',
      'slides.html', 'index.html', 'page.html', 'main.html', 'untitled.html',
      'deck.json', 'presentation.json']);
    const title = (document.title || '').trim();
    const file = decodeURIComponent(String(location.pathname || '').split('/').pop() || '')
      .toLowerCase();
    const badTitle = !title || GENERIC_TITLES.has(title.toLowerCase());
    const badFile = GENERIC_FILES.has(file);
    if (badTitle || badFile) {
      out.genericName = {
        title: title || '(empty)', file: file || '(none)',
        titleGeneric: badTitle, fileGeneric: badFile,
        fix: 'name both the way the user would name this deck ' +
             '("alfabs-q4-fy26-investor-update"), never after the format or the tool',
      };
    }
  });

  // ── 23. Repeated-module monotony ───────────────────────────────────────────
  step('Repeated module monotony', () => {
    // Measured: seven of twelve slides on one deck were an identical card row,
    // while the comparison deck used stat tiles, an editorial photo split, a
    // data table, a progress matrix, a milestone grid, a shared-scale bar pair
    // and a full-bleed photograph across the same twelve. Every slide felt
    // reasonable on its own, which is why this needs counting across the set
    // rather than judging per slide. The signature is a structural hash, not
    // content: same tags, same class stems, same child count.
    const shapeOf = (s) => {
      const stage = s.querySelector('.stage, .slide-stage, .slide-content, .stage-content') || s;
      return [...stage.children].filter((c) => vis(c)).map((c) => {
        const cls = String(c.className || '').split(/\s+/).filter(Boolean)
          .map((x) => x.replace(/[-_]?\d+$/, '')).sort().join('.');
        return c.tagName.toLowerCase() + '[' + cls + ']:' +
               [...c.children].filter((g) => vis(g)).length;
      }).join('|');
    };
    const tally = {};
    slides.forEach((s, i) => {
      const h = shapeOf(s);
      if (!h) return;
      (tally[h] = tally[h] || []).push(idOf(s, i));
    });
    Object.entries(tally).forEach(([shape, ids]) => {
      if (ids.length > CFG.moduleRepeatMax) {
        out.moduleRepeats.push({ shape: shape.slice(0, 90), count: ids.length,
                                 of: slides.length, slides: ids.slice(0, 12),
                                 max: CFG.moduleRepeatMax });
      }
    });
  });

  // ── 24. A non-IFRS figure without a statutory companion, and prominence ────
  step('Non-IFRS figure without a statutory companion', () => {
    // The old --regulated check tested that SOME audit qualifier existed
    // somewhere in the deck. It never tested the slide LEADING on EBITDA, which
    // is what the regulators actually write down.
    //
    // SEC Regulation G and Item 10(e) of Regulation S-K require the most
    // directly comparable GAAP measure with EQUAL OR GREATER PROMINENCE plus a
    // quantitative reconciliation; ASIC RG 230 requires the same of non-IFRS
    // information. The SEC's December 2022 Compliance & Disclosure
    // Interpretations, Question 102.10, enumerate what "more prominent" means,
    // and three of the examples are mechanical: the non-GAAP measure presented
    // BEFORE the GAAP one, the GAAP measure OMITTED, and the non-GAAP measure
    // styled in bold or a LARGER FONT than the GAAP measure. Presence somewhere
    // in the deck satisfies none of the three.
    if (!CFG.regulated) return;
    const NON_IFRS = /\b(EBITDA|EBIT|underlying|adjusted|normalised|normalized|pro[- ]?forma|free cash flow|FCF|NPATA?|operating earnings|run[- ]rate)\b/i;
    const STATUTORY = /\b(statutory|IFRS|GAAP|AASB|reported (profit|loss|revenue|result)|net profit after tax|reconcil)/i;
    // A forward-looking non-GAAP measure is treated differently by both regimes:
    // the reconciliation may be omitted where it is impracticable, PROVIDED the
    // unavailable information and its probable significance are disclosed. A
    // slide in that shape is not asked for a reconciliation — it is asked for
    // that disclosure instead, so demanding the wrong thing of it would be a
    // false finding.
    const FORWARD = /\b(target\w*|guidance|outlook|forecast\w*|expect\w*|projected|anticipat\w*)\b/i;
    const IMPRACTICABLE = /\b(not reasonably (available|estimable)|cannot be (reliably )?(estimated|quantified)|without unreasonable effort|impracticab\w+)\b/i;
    slides.forEach((s, i) => {
      const t = s.innerText || s.textContent || '';
      if (!NON_IFRS.test(t)) return;
      const measure = (t.match(NON_IFRS) || [])[0];
      const forward = FORWARD.test(t);
      const f = toCanvasPx(s);
      let nonIfrsPx = 0, statPx = 0, nonIfrsIdx = -1, statIdx = -1, n = 0;
      s.querySelectorAll('*').forEach((el) => {
        if (!isLeafText(el) || !vis(el)) return;
        const txt = (el.textContent || '').trim();
        const px = Math.round(parseFloat(getComputedStyle(el).fontSize) * f);
        n++;
        if (NON_IFRS.test(txt)) {
          if (px > nonIfrsPx) nonIfrsPx = px;
          if (nonIfrsIdx < 0) nonIfrsIdx = n;
        }
        if (STATUTORY.test(txt)) {
          if (px > statPx) statPx = px;
          if (statIdx < 0) statIdx = n;
        }
      });
      const fails = [];
      if (!STATUTORY.test(t)) {
        if (forward && IMPRACTICABLE.test(t)) {
          // permitted: forward-looking, with the impracticability disclosure
        } else if (forward) {
          fails.push('no statutory companion and no impracticability disclosure — a ' +
                     'forward-looking non-IFRS measure may omit the reconciliation only ' +
                     'where it states what is unavailable and its probable significance');
        } else {
          fails.push('no statutory measure or reconciliation reference on this slide');
        }
      } else {
        if (statPx && nonIfrsPx && nonIfrsPx > statPx) {
          fails.push('the non-IFRS measure is set larger than the statutory one (' +
                     nonIfrsPx + 'px against ' + statPx + 'px), which CDI 102.10 names ' +
                     'as greater prominence');
        }
        if (statIdx > 0 && nonIfrsIdx > 0 && nonIfrsIdx < statIdx && nonIfrsPx >= statPx) {
          fails.push('the non-IFRS measure is presented before the statutory one at no ' +
                     'smaller size, which CDI 102.10 names as greater prominence');
        }
      }
      if (fails.length) {
        out.nonIfrsUnpaired.push({
          slide: idOf(s, i), measure, forwardLooking: forward,
          nonIfrsLargestPx: nonIfrsPx || null, statutoryLargestPx: statPx || null,
          failed: fails,
        });
      }
    });
  });

  // ── 25. Titles and numerals, harvested for the source cross-check ──────────
  step('Titles and numerals harvest', () => {
    // Neither of these is a finding on its own — they are the deck half of a
    // comparison the probe cannot make, because the source document is not in
    // the page. The runner does the other half with --source.
    //
    // Numerals exist because fabrication does not arrive as an invented headline
    // figure. It arrives as texture around a real one, and the sharpest case is
    // the DERIVED ratio: "20x annualised payback", computed by the deck from two
    // real figures and set as a chip. The arithmetic was right, which is why it
    // survived review — but a ratio you derived is your claim, not the issuer's
    // disclosure, and it is a figure no board approved. A derived figure is
    // exactly the figure that appears nowhere in the source.
    slides.forEach((s, i) => {
      const id = idOf(s, i);
      [...s.querySelectorAll('h1,h2,h3,.slide-title,[class*="slide-title"],[class*="hero-title"]')]
        .filter(vis).forEach((h) => {
          const t = (h.textContent || '').trim();
          if (t) out.titles.push({ slide: id, tag: h.tagName.toLowerCase(), text: t.slice(0, 140) });
        });
      const seen = new Set();
      s.querySelectorAll('*').forEach((el) => {
        if (!isLeafText(el) || !vis(el)) return;
        const t = (el.textContent || '').trim();
        // Two or more significant digits: a bare "3 divisions" is prose, and
        // 8.4 / 12.4% / 3,000 / 20x are claims.
        (t.match(/\d[\d,]*(?:\.\d+)?\s*(?:%|x|bn|m|k)?/gi) || []).forEach((raw) => {
          const digits = raw.replace(/[^\d]/g, '').replace(/^0+/, '');
          if (digits.length < 2) return;
          const key = raw.trim();
          if (seen.has(key)) return;
          seen.add(key);
          out.numerals.push({ slide: id, figure: key, context: t.slice(0, 70) });
        });
      });
    });
    out.numerals = out.numerals.slice(0, 300);
    out.titles = out.titles.slice(0, 60);
  });

  // ── 26. Axis misleaders beyond truncation ──────────────────────────────────
  step('Dual and inverted axes', () => {
    // Until 18 Aug 2026 the only axis misleader this gate knew was a truncated
    // baseline. The Misviz work ("Is this chart lying to me? Automating the
    // detection of misleading visualizations", arXiv 2508.21675) enumerates the
    // rest, and the useful part is its method: it detects them from AXIS
    // METADATA rather than from the underlying data table, which is exactly what
    // a DOM probe can reach. Two of its categories are cheap here and matter
    // more than they look — on the evidence gathered for this rebuild, dual axes
    // degrade reading accuracy further than truncation does, and this skill had
    // no check for them at all.
    //
    // A vertical tick run is three or more numeric <text> nodes sharing an x
    // attribute at distinct y values. Two runs with materially different ranges
    // is a dual axis. A run whose values RISE as y rises is inverted, because on
    // an ordinary vertical axis the larger number sits higher up the page.
    const numOf = (v) => {
      const m = String(v == null ? '' : v).replace(/[, %]/g, '').match(/-?\d+(?:\.\d+)?/);
      return m ? parseFloat(m[0]) : null;
    };
    slides.forEach((s, i) => {
      const id = idOf(s, i);
      s.querySelectorAll('svg').forEach((svg) => {
        const ticks = [...svg.querySelectorAll('text')]
          .map((t) => ({ x: parseFloat(t.getAttribute('x')),
                         y: parseFloat(t.getAttribute('y')),
                         v: numOf(t.textContent) }))
          .filter((t) => isFinite(t.x) && isFinite(t.y) && t.v !== null);
        if (ticks.length < 6) return;
        const runs = {};
        ticks.forEach((t) => {
          const key = Math.round(t.x / 4) * 4;
          (runs[key] = runs[key] || []).push(t);
        });
        const vertical = Object.entries(runs)
          .map(([x, ts]) => ({ x: Number(x), ts: ts.slice().sort((a, b) => a.y - b.y) }))
          .filter((r) => r.ts.length >= 3 &&
                         new Set(r.ts.map((t) => Math.round(t.y))).size === r.ts.length);
        if (vertical.length >= 2) {
          const spans = vertical.map((r) => {
            const vs = r.ts.map((t) => t.v);
            return { x: r.x, min: Math.min(...vs), max: Math.max(...vs) };
          }).sort((a, b) => a.x - b.x);
          const L = spans[0], R = spans[spans.length - 1];
          const hi = Math.max(Math.abs(L.max), Math.abs(R.max));
          const lo = Math.max(1e-9, Math.min(Math.abs(L.max), Math.abs(R.max)));
          if (hi / lo > 1.2) {
            out.axisMisleaders.push({ slide: id, kind: 'dualAxis',
              left: [L.min, L.max], right: [R.min, R.max],
              note: 'two vertical scales with different ranges on one chart, which ' +
                    'invites a reader to see a correlation the data does not carry' });
          }
        }
        vertical.forEach((r) => {
          const vs = r.ts.map((t) => t.v);            // sorted by y ascending
          const rising = vs.every((v, k) => k === 0 || v >= vs[k - 1]);
          const falling = vs.every((v, k) => k === 0 || v <= vs[k - 1]);
          if (rising && !falling && vs[vs.length - 1] > vs[0]) {
            out.axisMisleaders.push({ slide: id, kind: 'invertedAxis',
              ticksTopToBottom: vs,
              note: 'values increase down the axis, so the larger number sits lower' });
          }
        });
      });
      // The declared escape hatch. Both shapes are legitimate sometimes, and a
      // gate that refuses a legitimate construction with no way to say so is a
      // gate people learn to route around. An author who needs a second scale
      // declares it, and the finding becomes a recorded decision.
      s.querySelectorAll('[data-axis="dual"], [data-axis="inverted"]').forEach((g) => {
        out.axisMisleaders = out.axisMisleaders.filter((a) => a.slide !== id);
        out.notes.push('slide ' + id + ' declares data-axis="' +
                       g.getAttribute('data-axis') + '" — the axis shape is the ' +
                       'author\'s stated choice, so it is recorded rather than flagged');
      });
    });
    out.axisMisleaders = out.axisMisleaders.slice(0, 24);
  });

  // ── Summary ──────────────────────────────────────────────────────────────
  out.summary = {
    slidesExamined: slides.length,
    stageGeometry: out.stage.length,
    typeBelowFloor: out.type.belowBodyFloor,
    overflow: out.overflow.length,
    stageContentOverflow: out.stageContentOverflow.length,
    titleWrap: out.titleWrap.length,
    cardOverflow: out.cardOverflow.length,
    chromeCollisions: out.collisions.length,
    textOverlaps: out.textOverlap.length,
    invisibleText: out.paintOrder.length,
    chartsChecked: out.charts.length,
    chartsNotZeroBased: out.charts.filter((c) => !c.zeroBased).length,
    chartGroupsUnverified: out.chartsUnverified || 0,
    accentOverspent: out.accent.length,
    deadFootBands: out.deadSpace.length,
    stageBottomClearance: out.stageBottomClearance.length,
    verticalSquish: out.verticalSquish.length,
    unprotectedTextOverImage: out.textOverImage.length,
    provenanceMissing: out.provenance ? out.provenance.missing.length : null,
    inkPastSlide: out.inkExtent.length,
    chromeOverStage: out.chromeReserve.length,
    hueFamilies: out.hues ? out.hues.count : null,
    noDisplayTier: out.displayTier ? 1 : 0,
    externalRefs: out.externalRefs.length,
    leakedArithmetic: out.leakedArithmetic.length,
    genericName: out.genericName ? 1 : 0,
    moduleRepeats: out.moduleRepeats.length,
    nonIfrsUnpaired: out.nonIfrsUnpaired.length,
    axisMisleaders: out.axisMisleaders.length,
    checksNotRun: out.notes.filter((n) => /treat as NOT RUN/.test(n)).length,
  };

  // ── The policy, in the probe rather than in the runner ─────────────────────
  //
  // Until 18 Aug 2026 the blocker/warning split lived only in run-preflight.sh,
  // and six of this summary's keys reached NEITHER list: typeBelowFloor,
  // chartsChecked, chartGroupsUnverified, accentOverspent, deadFootBands and
  // unprotectedTextOverImage. Two consequences were measured on this machine:
  // a deck with 17 text elements below the 24px floor exited 0 and printed
  // "0 blockers across 3 slides examined", and a deck whose two axis-truncated
  // ROI bar pairs were both declined by the detector printed
  // `chartsNotZeroBased: 0` and passed — a zero over a denominator of zero,
  // which deck-review.md names as the canonical lie.
  //
  // It lives here now so that anything reading this JSON — a CI step, another
  // agent, a model reading the object rather than the verdict line — gets the
  // policy with the numbers instead of re-deriving it.
  out.policy = {
    blockers: ['stageGeometry', 'overflow', 'stageContentOverflow', 'titleWrap',
               'cardOverflow', 'inkPastSlide', 'chromeCollisions', 'chromeOverStage',
               'textOverlaps', 'invisibleText', 'provenanceMissing', 'chartsNotZeroBased',
               'leakedArithmetic', 'typeBelowFloor', 'nonIfrsUnpaired', 'genericName',
               'axisMisleaders', 'checksNotRun'],
    warnings: ['stageBottomClearance', 'verticalSquish', 'noDisplayTier', 'hueFamilies',
               'externalRefs', 'accentOverspent', 'deadFootBands',
               'unprotectedTextOverImage', 'chartGroupsUnverified', 'moduleRepeats'],
    denominators: { chartsNotZeroBased: 'chartsChecked', '*': 'slidesExamined' },
  };

  // ── The consequence of each finding, carried to the caller ────────────────
  //
  // Every one of these was already written, ten lines above its own check, in a
  // comment the model never sees because it reads JSON. The runner prints the
  // matching line beside each finding, so the output says what will happen
  // rather than only that a count is non-zero.
  out.consequences = {
    stageGeometry: 'the slide reflowed instead of letterboxing, so the presenter cannot predict what the audience sees; author at one canvas size and scale the whole stage',
    overflow: 'content runs past its box and clips at the container edge with no scrollbar and no warning',
    stageContentOverflow: 'the wrapper clips at overflow:hidden so scrollHeight matches clientHeight while stage content quietly overflows',
    titleWrap: 'a headline on 3+ lines steals 100-200px of vertical budget and pushes content down into the chrome',
    cardOverflow: 'text is clipped past the card bottom; the card looks complete and its last line is gone',
    inkPastSlide: 'ink sits outside the slide box. scrollHeight cannot see this: a clipping ancestor erases scrollHeight without moving the ink, so a whole table row can sit clipped under the chrome while the overflow check scores clean',
    chromeCollisions: 'content runs into the footer, page number or control dock — all inside the stage bounds, so an "escapes the stage" check is silent about it',
    chromeOverStage: 'a floating dock sits over the artwork, and it hides whatever the next revision puts there',
    textOverlaps: 'two labels share pixels; in a fixed stage nothing shrinks to fit and nothing warns you',
    invisibleText: 'the copy is painted under its own photograph. Layout, sizes, fonts, overflow, collision and contrast checks all pass; only a hit test finds it',
    provenanceMissing: 'a figure with no stated provenance is not neutral — it reads as authoritative, because that is the default a reader applies',
    chartsNotZeroBased: 'bar length is the encoding, so a truncated baseline overstates the change. Long & Kay (ACM CHI 2024) measured the distortion at 100/(100-t) and found footnotes do not cure it',
    leakedArithmetic: 'the gate\'s own working is printed where a disclosure belongs. The reader is owed the axis disclosure and the as-at date; your proof that the axis is honest is not a disclosure and reads as one',
    typeBelowFloor: 'body copy below the floor is unreadable from row four. 24px on a 1920 canvas is the ISO 9241-303 16-arcminute floor solved at a viewing ratio of 3, not a taste value',
    nonIfrsUnpaired: 'a slide leading on a non-IFRS measure with no statutory companion on it. SEC Reg G / Item 10(e) and ASIC RG 230 both require the statutory equivalent at equal or greater prominence, and deck-wide presence of the word does not satisfy a per-slide prominence test',
    genericName: 'the deck is named after the format or the tool. The filename is what a director sees in their downloads folder, beside four other files called the same thing',
    checksNotRun: 'a check threw and did not run. Its count came back null, which reads as zero, which is indistinguishable from clean — this is the failure mode the whole file is built to refuse',
    axisMisleaders: 'a dual or inverted axis. A dual axis invites a reader to see a correlation the data does not carry, and the evidence gathered for this gate rates it a WORSE distortion than a truncated baseline; an inverted axis puts the larger number lower down the page. Declare data-axis="dual" or "inverted" on the group if the shape is deliberate, and the finding becomes a recorded decision instead',
    stageBottomClearance: 'content crowded against the slide bottom or the footer looks squeezed and collides with a dock or a hardware bezel',
    verticalSquish: 'a vertical gap collapsed to zero between stacked blocks',
    noDisplayTier: 'the deck has no display tier, so the cover reads as a web hero and every slide below inherits the flatter ramp. Measured across two decks from one brief: 132px against 76px, and 19 distinct sizes against 13',
    hueFamilies: 'one accent is the rule and a second hue needs a reason. The predictable break is status chips: green for done, blue for in-progress, and the deck now carries three hues while every slide felt reasonable',
    externalRefs: 'the deck opens in a different typeface offline, on a plane, behind a strict CSP and inside a sandboxed investor portal — the four places a deck is most often actually read',
    accentOverspent: 'an accent on four objects is a decoration, not a signal. Drawn marks count: four accent-filled progress bars plus one chip read as five accent objects to the eye',
    deadFootBands: 'an empty band below the lowest ink, which is where a fluid section that stopped at content height gives itself away',
    unprotectedTextOverImage: 'a look-here list, not a failure: a DOM probe cannot sample the pixels under a photograph, so these are the places an eye is actually needed',
    chartGroupsUnverified: 'chart groups the detector declined. The coverage gap is the point — a zero over a denominator of zero is indistinguishable from a clean deck',
    moduleRepeats: 'the same module repeated across the deck. Measured: seven of twelve slides on one deck were an identical card row. Vary the module, not just its contents',
  };

  out.notes.push('Denominator: ' + slides.length + ' slides examined. A zero with no ' +
                 'denominator is not a result. This finds no known computable defect; ' +
                 'it does not find the defect nobody has met yet.');
  return JSON.stringify(out, null, 1);
 } catch (e) {
  // A gate that dies quietly is worse than no gate: its silence is
  // indistinguishable from a clean deck. Say so in the return value.
  return JSON.stringify({ error: String((e && e.stack) || e),
                          note: 'preflight did NOT run — this is not a pass' }, null, 1);
 }
})(((c) => (typeof c === 'string'
  ? ((typeof window !== 'undefined' && window.__deckPreflight) || {})
  : c))('__DECKCFG__'))
