/* demo-video-craft starter kit: the window runtime. A scene is a list of steps run over live HTML states inside a
   host-app window (K.play). Every value a scene animates is a function of timeline time (GSAP, paused, seeked by
   HyperFrames), so any frame renders on its own and a render repeats exactly. From a delivered series, Nov 2026. */
(function () {
  const K = {};
  // The stage the camera frames into. With no captions it is the whole frame; with a caption band, reserve it
  // (round 1 of the source series used { cx: 960, cy: 452, w: 1920, h: 860 } above a 180 px band).
  const STAGE = (window.TL && TL.stage) || { cx: 960, cy: 520, w: 1920, h: 1040 };
  K.STAGE = STAGE;

  // ---- time: the beat map lives in timeline.json (window.TL), in film seconds ------------------------------------
  K.scene = function (id, build) {
    const tl = gsap.timeline({ paused: true });
    window.__timelines = window.__timelines || {};
    const ready = document.fonts && document.fonts.load
      ? Promise.all((TL.fonts || ['400 15px Inter', '600 15px Inter', '600 40px "Inter Tight"']).map((f) => document.fonts.load(f))).then(() => document.fonts.ready)
      : Promise.resolve();
    return ready.then(() => {
      const t0 = TL.scenes[id].start;
      const at = (abs) => Math.max(0, abs - t0);           // film seconds to scene seconds
      // A scene that is not on screen yet is display:none, where every rect measures zero. Show it for the
      // measuring, then put every ancestor back exactly as the runtime had it.
      const shown = [];
      let el = document.querySelector('[data-composition-id="' + id + '"] .k-sc') || document.querySelector('[data-composition-id="' + id + '"]');
      for (; el && el !== document.documentElement; el = el.parentElement) {
        if (getComputedStyle(el).display === 'none') {
          shown.push([el, el.style.getPropertyValue('display'), el.style.getPropertyPriority('display')]);
          el.style.setProperty('display', 'block', 'important');
        }
      }
      try {
        build(tl, { at, t0, dur: TL.scenes[id].dur });
      } catch (err) {
        // A scene that cannot build says so on its own frames, so a render can never pass with it silently static.
        const box = document.querySelector('[data-composition-id="' + id + '"] .k-sc') || document.body;
        const note = document.createElement('div');
        note.style.cssText = 'position:absolute;left:40px;top:40px;z-index:999;background:#B42318;color:#fff;font:600 28px Inter;padding:16px 20px;border-radius:8px;max-width:1700px';
        note.textContent = `Scene ${id} failed: ${err.message}`;
        box.appendChild(note);
        console.error(`scene ${id}:`, err);
      } finally {
        shown.forEach(([e, v, pr]) => (v ? e.style.setProperty('display', v, pr) : e.style.removeProperty('display')));
      }
      window.__timelines[id] = tl;
      return tl;
    });
  };
  K.line = (id) => { const l = TL.lines[id]; if (!l) throw new Error('no line ' + id); return l; };
  /** Start of a word in a narration line (film seconds). `w` is an index or the word's text (first match). */
  K.word = function (id, w, which) {
    const l = K.line(id);
    let i = w;
    if (typeof w === 'string') {
      const norm = (s) => s.toLowerCase().replace(/[^a-z0-9$.%]/g, '');
      const hits = l.words.map((x, j) => (norm(x[0]).startsWith(norm(w)) ? j : -1)).filter((j) => j >= 0);
      if (!hits.length) throw new Error(`no word "${w}" in ${id}`);
      i = hits[Math.min(which || 0, hits.length - 1)];
    }
    return l.words[i][1];
  };
  K.wordEnd = (id, w, which) => { const l = K.line(id); const s = K.word(id, w, which); return l.words.find((x) => x[1] === s)[2]; };
  K.beat = (name) => { const b = TL.beats[name]; if (b === undefined) throw new Error('no beat ' + name); return b; };

  // ---- geometry: rects in a window's own CSS pixels, measured once at identity -----------------------------------
  K.rectOf = function (el, win) {
    const w = win.getBoundingClientRect(), r = el.getBoundingClientRect();
    const s = w.width / win.offsetWidth || 1;
    return { x: (r.left - w.left) / s, y: (r.top - w.top) / s, w: r.width / s, h: r.height / s };
  };
  K.rectsOf = function (el, win) {
    const w = win.getBoundingClientRect(); const s = (w.width / win.offsetWidth) || 1;
    return [...el.getClientRects()].map((r) => ({ x: (r.left - w.left) / s, y: (r.top - w.top) / s, w: r.width / s, h: r.height / s }));
  };
  /** The first element under `root` matching `sel` whose text contains `text`. */
  K.find = function (root, sel, text) {
    const el = [...root.querySelectorAll(sel)].find((e) => !text || e.textContent.includes(text));
    if (!el) throw new Error(`no ${sel} containing "${text}"`);
    return el;
  };
  K.union = (...rs) => {
    const x = Math.min(...rs.map((r) => r.x)), y = Math.min(...rs.map((r) => r.y));
    return { x, y, w: Math.max(...rs.map((r) => r.x + r.w)) - x, h: Math.max(...rs.map((r) => r.y + r.h)) - y };
  };
  K.pad = (r, p, py) => ({ x: r.x - p, y: r.y - (py === undefined ? p : py), w: r.w + 2 * p, h: r.h + 2 * (py === undefined ? p : py) });
  K.shift = (r, dy) => ({ x: r.x, y: r.y - dy, w: r.w, h: r.h });

  // ---- the camera: frame a rect of a window in the stage -------------------------------------------------------
  /** The transform that centres `rect` in the stage, filling `fill` of the stage width (capped by height). */
  K.frame = function (win, rect, fill, opts) {
    opts = opts || {};
    const ww = win.offsetWidth, wh = win.offsetHeight;
    let s = Math.min((fill || 0.62) * STAGE.w / rect.w, (opts.fillH || 0.92) * STAGE.h / rect.h, opts.max || 3.2);
    if (opts.scale) s = opts.scale;
    const cx = rect.x + rect.w / 2, cy = rect.y + rect.h / 2;
    let x = (opts.cx || STAGE.cx) - s * cx, y = (opts.cy || STAGE.cy) - s * cy;
    if (!opts.free) {                                   // never show past a window edge once it is larger than the frame
      if (ww * s >= 1920) x = Math.min(0, Math.max(1920 - ww * s, x));
      if (wh * s >= 1080) y = Math.min(0, Math.max(1080 - wh * s, y));
    }
    return { x, y, scale: s, transformOrigin: '0 0' };
  };
  K.orient = function (win, s) {                        // the whole window, centred, to orient (2-4 s at most)
    s = s || 1.12;
    return { x: (1920 - win.offsetWidth * s) / 2, y: (1080 - win.offsetHeight * s) / 2 - 36, scale: s, transformOrigin: '0 0' };
  };
  K.move = function (tl, win, to, t, dur, ease) {
    tl.to(win, { ...to, duration: dur || 1.1, ease: ease || 'power2.inOut' }, t);
  };

  // ---- the thread: messages arrive, the composer types, the thread scrolls -------------------------------------
  K.items = (win) => [...win.querySelectorAll('.cf-col > *')];
  K.hide = (els) => gsap.set(els, { opacity: 0, y: 14 });
  K.arrive = function (tl, el, t, opts) {
    opts = opts || {};
    tl.fromTo(el, { opacity: 0, y: opts.y === undefined ? 16 : opts.y, filter: 'blur(8px)' }, { opacity: 1, y: 0, filter: 'blur(0px)', duration: opts.dur || 0.6, ease: 'expo.out', immediateRender: false }, t);
  };
  K.leave = function (tl, el, t, dur) { tl.to(el, { opacity: 0, duration: dur || 0.25, ease: 'power3.in' }, t); };
  /** Type `text` into the host's composer, then send it: the composer clears and the message lands. */
  K.composer = function (win) {
    const box = win.querySelector('.cf-composer');
    const ph = box.querySelector('.ph');
    let typed = box.querySelector('.typed');
    if (!typed) { typed = document.createElement('div'); typed.className = 'ph typed'; ph.after(typed); gsap.set(typed, { textContent: '' }); }
    return { box, ph, typed };
  };
  K.type = function (tl, win, text, t, cps) {
    const c = K.composer(win);
    const dur = text.length / (cps || 34);
    tl.set(c.ph, { opacity: 0 }, t);
    const p = { n: 0 };
    tl.to(p, { n: text.length, duration: dur, ease: 'none', onUpdate: () => { c.typed.textContent = text.slice(0, Math.round(p.n)); } }, t);
    return t + dur;
  };
  K.send = function (tl, win, t) {
    const c = K.composer(win);
    tl.set(c.typed, { textContent: '' }, t);
    tl.set(c.ph, { opacity: 1 }, t + 0.05);
  };
  K.scroll = function (tl, win, dy, t, dur) {
    tl.to(win.querySelector('.cf-col'), { y: -dy, duration: dur || 0.9, ease: 'power2.inOut' }, t);
  };

  // ---- the hand: a cursor that travels in shallow arcs and presses ---------------------------------------------
  const CURSOR = '<svg width="40" height="40" viewBox="0 0 46 46"><path d="M8 5.5 L39 20.2 c1.6.8 1.4 3.1-.3 3.6 L26.6 27.4 c-.6.2-1.1.6-1.3 1.2 L21.7 40 c-.5 1.7-2.8 1.9-3.6.3 L6.2 9.2 C5.4 7.4 6.6 5 8 5.5 Z" fill="currentColor" stroke="#fff" stroke-width="2.6" stroke-linejoin="round"/></svg>';
  K.cursor = function (win, x, y) {
    const c = document.createElement('div');
    c.className = 'k-cursor'; c.innerHTML = CURSOR;
    win.appendChild(c);
    gsap.set(c, { x, y, opacity: 0 });
    return c;
  };
  K.point = function (tl, c, rect, t, dur) {
    const x = rect.x + rect.w * 0.55, y = rect.y + rect.h * 0.55;
    tl.to(c, { opacity: 1, duration: 0.2 }, t);
    tl.to(c, { x, duration: dur || 0.7, ease: 'power2.inOut' }, t);
    tl.to(c, { y, duration: dur || 0.7, ease: 'power1.inOut' }, t);
    return t + (dur || 0.7);
  };
  K.press = function (tl, el, t, c) {
    tl.to(el, { scale: 0.965, filter: 'brightness(0.86)', duration: 0.09, ease: 'power2.out' }, t);
    tl.to(el, { scale: 1, filter: 'brightness(1)', duration: 0.22, ease: 'power2.out' }, t + 0.12);
    if (c) { tl.to(c, { scale: 0.86, duration: 0.09 }, t); tl.to(c, { scale: 1, duration: 0.2 }, t + 0.12); }
  };

  // ---- the evidence grammar: how the product marks a claim against its source ----------------------------------
  // ok: 2px green underline · bad: wavy red underline · review: the blue highlight · none: dotted grey underline
  const WAVE = "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 3 Q2.5 0 5 3 T10 3' fill='none' stroke='%23B42318' stroke-width='1.6'/%3E%3C/svg%3E\")";
  /** Marks travel with the text they mark: they live in the nearest container that scrolls or moves with it. */
  K.ink = function (tl, el, win, kind, t, dur) {
    // A mark lives in the row (or quote, lead tile, card, bubble) that carries its text, so it lifts, dims, scales and
    // scrolls with that row; measured relative to that box, it is right whatever the box's offset. Add your product's
    // row classes to this list, and give them position: relative in the stylesheet.
    const box = el.closest('.dc-row, .pv-row, .dc-quote, .dc-lead > div, .dc-head, .jdoc, .cf-col > *, .pv-box, .k-art, .k-solo, .k-win') || win;
    if (getComputedStyle(box).position === 'static') box.style.position = 'relative';
    const marks = K.rectsOf(el, box).map((r) => {
      const m = document.createElement('div');
      m.className = 'k-ink ' + kind;
      box.appendChild(m);
      if (kind === 'review') gsap.set(m, { x: r.x - 2, y: r.y, width: r.w + 4, height: r.h });
      else gsap.set(m, { x: r.x, y: r.y + r.h - (kind === 'bad' ? 3 : 1), width: r.w, height: kind === 'bad' ? 6 : 2 });
      if (kind === 'bad') m.style.backgroundImage = WAVE;
      gsap.set(m, { clipPath: 'inset(0 100% 0 0)' });
      return m;
    });
    const each = (dur || 0.5) / marks.length;
    marks.forEach((m, i) => tl.to(m, { clipPath: 'inset(0 0% 0 0)', duration: each, ease: 'power2.inOut' }, t + i * each));
    return marks;
  };
  /** The carrier: a red mark becomes a green line when the figure is fixed. */
  K.inkTo = function (tl, marks, kind, t) {
    marks.forEach((m) => {
      tl.set(m, { attr: { class: 'k-ink ' + kind } }, t);
      if (kind === 'ok') tl.fromTo(m, { height: 6, backgroundImage: m.style.backgroundImage }, { height: 2, y: '+=4', backgroundImage: 'none', duration: 0.35, ease: 'power2.out', immediateRender: false }, t);
    });
  };

  // ---- a code typed into the product's approval view, one digit at a time --------------------------------------
  K.code = function (tl, win, digits, t, gap) {
    const boxes = [...win.querySelectorAll('.cd')];
    boxes.forEach((b, i) => {
      const at = t + i * (gap || 0.16);
      tl.set(b, { textContent: digits[i], attr: { class: 'cd on' } }, at);
      if (i > 0) tl.set(boxes[i - 1], { attr: { class: 'cd' } }, at);
    });
    return t + boxes.length * (gap || 0.16);
  };

  // ---- the captions: the narration's own words, timed by Scribe's word timings --------------------------------
  K.captions = function (host, chunks) {
    const tl = gsap.timeline({ paused: true });
    chunks.forEach(([text, a, b], i) => {
      const el = document.createElement('div');
      el.className = 'k-cap'; el.id = 'cap' + (i + 1);
      const span = document.createElement('span'); span.textContent = text; el.appendChild(span);
      host.appendChild(el);
      gsap.set(el, { opacity: 0 });
      tl.to(el, { opacity: 1, duration: 0.12, ease: 'none' }, a);
      tl.to(el, { opacity: 0, duration: 0.1, ease: 'none' }, Math.max(a + 0.3, b - 0.1));
    });
    return tl;
  };

  // ---- a scene as a list of steps: [when, op, ...args], in film time ----------------------------------------
  // when: seconds into the scene (a number) or a narration expression: "b4.start", "b4.end-0.3", "b4.word:check+0.2",
  // "b4.word:figure#1" (the second "figure"). Targets: {i:[2,3], w:'#w1'} items · {s:'.dg-lead', w, t:'text', in:2}
  // an element (first match containing t, inside item `in`) · {u:[...]} a union · [x,y,w,h] · any of them with p:pad.
  K.when = function (x) {
    if (typeof x === 'number') return null;
    const bm = /^([A-Za-z_][A-Za-z0-9_]*)([+\-][0-9.]+)?$/.exec(x);
    if (bm && TL.beats && TL.beats[bm[1]] !== undefined) return TL.beats[bm[1]] + +(bm[2] || 0);
    const m = /^([a-z0-9]+)\.(start|end|word:([^+\-#]+)(?:#(\d+))?)([+\-][0-9.]+)?$/.exec(x);
    if (!m) throw new Error('when not understood: ' + x);
    const l = K.line(m[1]);
    let v = m[2] === 'start' ? l.start : m[2] === 'end' ? l.end : K.word(m[1], m[3], +(m[4] || 0));
    return v + +(m[5] || 0);
  };
  K.play = function (id, spec) {
    return K.scene(id, (tl, ctx) => {
      const host = document.querySelector('[data-composition-id="' + id + '"]');
      const q = (sel) => { const e = host.querySelector(sel); if (!e) throw new Error(`${id}: no ${sel}`); return e; };
      const cam = q(spec.cam || '.k-cam');
      const sc = q('.k-sc');
      const T = (x) => (typeof x === 'number' ? x : ctx.at(K.when(x)));
      const W = {};
      (spec.windows || []).forEach((sel) => { W[sel] = q(sel); });
      const items = {}, itemRects = {};
      Object.entries(W).forEach(([k, w]) => { items[k] = K.items(w); itemRects[k] = items[k].map((e) => K.rectOf(e, cam)); });
      const thread = {};
      Object.entries(W).forEach(([k, w]) => { const t = w.querySelector('.cf-convo'); if (t) thread[k] = K.rectOf(t, cam); });
      // Measure in the layout a target is seen in: with the side panel open, the conversation moves left.
      const opened = (w, fn) => {
        const cf = W[w] && W[w].querySelector('.k-cf');
        if (!cf) return fn();
        cf.classList.add('k-open');
        try { return fn(); } finally { cf.classList.remove('k-open'); }
      };
      const dy = {};
      Object.keys(W).forEach((k) => { dy[k] = 0; });
      const padR = (r, p) => (p === undefined ? r : Array.isArray(p) ? K.pad(r, p[0], p[1]) : K.pad(r, p));
      const el = (t) => {
        const w = W[t.w] || cam;
        const scope = t.in !== undefined ? items[t.w][t.in] : w;
        const e = t.t ? K.find(scope, t.s, t.t) : scope.querySelector(t.s);
        if (!e) throw new Error(`${id}: no ${t.s} ${t.t || ''}`);
        return e;
      };
      const rect = (t) => {
        if (Array.isArray(t)) return { x: t[0], y: t[1], w: t[2], h: t[3] };
        let r;
        if (t.u) r = K.union(...t.u.map(rect));
        else if (t.i !== undefined) {
          const ids = Array.isArray(t.i) ? t.i : [t.i];
          const rs = t.open ? opened(t.w, () => ids.map((i) => K.rectOf(items[t.w][i], cam))) : ids.map((i) => itemRects[t.w][i]);
          r = K.shift(K.union(...rs), dy[t.w]);
        } else {
          const e = el(t);
          const inPanel = !!e.closest('.cf-panel');
          r = (t.open || inPanel) ? opened(t.w, () => K.rectOf(e, cam)) : K.rectOf(e, cam);
          if (t.w && e.closest('.cf-col')) r = K.shift(r, dy[t.w]);
        }
        return padR(r, t.p);
      };
      let cur = null;
      const cursor = () => cur || (cur = K.cursor(cam, (spec.cursorFrom || [1100, 820])[0], (spec.cursorFrom || [1100, 820])[1]));
      const inks = {};

      // hidden at the start: items that arrive later, windows that open later
      Object.entries(spec.hidden || {}).forEach(([k, v]) => {
        const list = typeof v === 'number' ? items[k].slice(v) : v.map((i) => items[k][i]);
        K.hide(list);
      });
      (spec.closed || []).forEach((k) => gsap.set(W[k], { opacity: 0 }));
      if (spec.ground) {
        const g = document.createElement('div');
        g.style.cssText = `position:absolute;inset:0;background:${spec.ground[0]};z-index:30`;
        sc.appendChild(g);
        tl.to(g, { opacity: 0, duration: spec.ground[2] || 0.55, ease: 'power2.out' }, spec.ground[1] || 0.05);
      }
      const st = spec.start || {};
      gsap.set(cam, st.orient ? K.orient(cam, st.orient) : K.frame(cam, rect(st.frame), st.fill || 0.6, st.opts));

      const steps = (spec.steps || []).map((s, n) => ({ t: T(s[0]), n, s })).sort((a, b) => a.t - b.t || a.n - b.n);
      steps.forEach(({ t, s }) => {
        const [, op, a, b, c, d] = s;
        switch (op) {
          case 'frame': K.move(tl, cam, K.frame(cam, rect(a), b || 0.6, d), t, c || 1.0); break;
          case 'cut': tl.set(cam, K.frame(cam, rect(a), b || 0.6, c), t); break;
          case 'orient': K.move(tl, cam, K.orient(cam, a), t, b || 1.1); break;
          case 'zoom': K.move(tl, cam, K.frame(cam, rect(a), 0.02, { scale: b || 8, free: true }), t, c || 0.7, 'power3.in'); break;
          case 'arrive': {
            const ids = Array.isArray(b) ? b : [b];
            ids.forEach((i, k) => K.arrive(tl, items[a][i], t + k * ((c && c.gap) || 0.3), c));
            break;
          }
          case 'scroll': {
            const r = itemRects[a][b], th = thread[a];
            dy[a] = Math.max(0, r.y + r.h - (th.y + th.h - (d || 24)));
            K.scroll(tl, W[a], dy[a], t, c || 0.9);
            break;
          }
          case 'ink': inks[d || ('ink' + t)] = K.ink(tl, el(a), W[a.w] || cam, b, t, c || 0.5); break;
          case 'inkTo': K.inkTo(tl, inks[a], b, t); break;
          case 'inkOff': tl.to(inks[a], { opacity: 0, duration: 0.25 }, t); break;
          case 'type': {
            if (T(c) - t < 0.05) {
              // already written when the scene opens: on screen from its first frame, so it can be read at once
              const cc = K.composer(W[a]);
              gsap.set(cc.ph, { opacity: 0 }); gsap.set(cc.typed, { textContent: b });
              break;
            }
            K.type(tl, W[a], b, t, b.length / Math.max(0.5, T(c) - t));
            break;
          }
          case 'send': K.send(tl, W[a], t); break;
          case 'click': {
            const e = el(a), r = rect(a), lead = (b && b.lead) || 0.8;
            K.point(tl, cursor(), r, t - lead, lead - 0.08);
            K.press(tl, e, t, cursor());
            const ring = document.createElement('div');
            ring.className = 'k3-ring';
            cam.appendChild(ring);
            gsap.set(ring, { x: r.x + r.w * 0.55, y: r.y + r.h * 0.55, opacity: 0 });
            tl.fromTo(ring, { scale: 0.2, opacity: 0.6 }, { scale: 1, opacity: 0, duration: 0.5, ease: 'power2.out', immediateRender: false }, t);
            if (!b || !b.keep) tl.to(cursor(), { opacity: 0, duration: 0.2 }, t + ((b && b.hideAfter) || 0.45));
            break;
          }
          case 'show': tl.to(W[a], { opacity: 1, duration: b || 0.14, ease: 'none' }, t); break;
          case 'hide': tl.to(W[a], { opacity: 0, duration: b || 0.2, ease: 'none' }, t); break;
          case 'text': tl.set(el(a), { textContent: b }, t); break;
          case 'fade': tl.to(el(a), { opacity: b, duration: c || 0.4, ease: 'power2.inOut' }, t); break;
          case 'swap': {
            const x = el(a), y = el(b);
            tl.to(x, { opacity: 0, duration: 0.22, ease: 'power2.in' }, t);       // the old state fades before it goes
            tl.set(x, { display: 'none' }, t + 0.22);
            tl.set(y, { display: 'block' }, t + 0.22);
            tl.fromTo(y, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.45, ease: 'expo.out', immediateRender: false }, t + 0.22);
            break;
          }
          case 'code': K.code(tl, W[a], b, t, c || 0.15); break;
          case 'iris': {
            const o = document.createElement('div');
            const at = b || [960, 452];
            o.style.cssText = `position:absolute;inset:0;z-index:60;background:${a};clip-path:circle(0px at ${at[0]}px ${at[1]}px)`;
            sc.appendChild(o);
            tl.to(o, { clipPath: `circle(1300px at ${at[0]}px ${at[1]}px)`, duration: c || 0.5, ease: 'power2.in' }, t);
            break;
          }
          case 'chip': {
            // a time chip on the stage: [when, 'chip', text, [x, y], until]
            const o = document.createElement('div');
            o.className = 'k-chip';
            o.textContent = a;
            sc.appendChild(o);
            gsap.set(o, { x: b[0], y: b[1], opacity: 0, scale: 0.94 });
            tl.to(o, { opacity: 1, scale: 1, duration: 0.5, ease: 'expo.out' }, t);
            if (c !== undefined) tl.to(o, { opacity: 0, duration: 0.25, ease: 'power3.in' }, T(c));
            break;
          }
          case 'title': {
            // a chapter line on the ground: [when, 'title', text, [x, y], until, size]
            const o = document.createElement('div');
            o.className = 'k-title';
            o.textContent = a;
            if (d) o.style.fontSize = d + 'px';
            sc.appendChild(o);
            gsap.set(o, { x: b[0], y: b[1], opacity: 0, filter: 'blur(8px)' });
            tl.to(o, { opacity: 1, filter: 'blur(0px)', duration: 0.25, ease: 'power4.out' }, t);
            if (c !== undefined) tl.to(o, { opacity: 0, filter: 'blur(6px)', duration: 0.2, ease: 'power3.in' }, T(c));
            break;
          }
          case 'unpanel': {
            // [when, 'unpanel', '#w1', dur]: the side panel closes and the sidebar comes back
            const w = W[a], dur = b || 0.45;
            tl.to(w.querySelector('.cf-panel'), { width: 0, duration: dur, ease: 'power2.inOut' }, t);
            tl.to(w.querySelector('.cf-side'), { width: 232, duration: dur, ease: 'power2.inOut' }, t);
            tl.to(w.querySelectorAll('.cf-side > *'), { opacity: 1, duration: dur * 0.6, ease: 'power2.out' }, t + dur * 0.4);
            break;
          }
          case 'panel': {
            // [when, 'panel', '#w1', dur]: the product's view opens in the side panel; the sidebar folds away and its
            // children fade over half the fold, or their text clips mid-fold (hf.sh check: clipped_text)
            const w = W[a], dur = b || 0.5;
            tl.to(w.querySelector('.cf-side'), { width: 0, duration: dur, ease: 'power2.inOut' }, t);
            tl.to(w.querySelectorAll('.cf-side > *'), { opacity: 0, duration: dur * 0.5, ease: 'power2.out' }, t);
            tl.to(w.querySelector('.cf-panel'), { width: 600, duration: dur, ease: 'power2.inOut' }, t);
            break;
          }
          case 'tool': {
            // [when, 'tool', {i, w}, [status texts], dur]: a running tool line narrates, then finishes
            const e = el(a.s ? a : { s: '.tl', w: a.w, in: a.i }), line = e.closest('.cf-tool') || e, txt = line.querySelector('.tl');
            const msgs = b || [], dur = c || 1.6, spin = line.querySelector('.spin');
            msgs.forEach((m, k) => tl.set(txt, { textContent: m }, t + (k * dur) / Math.max(1, msgs.length)));
            if (spin) tl.fromTo(spin, { rotation: 0 }, { rotation: 360 * Math.max(1, Math.round(dur / 0.8)), duration: dur, ease: 'none', immediateRender: false }, t);
            tl.set(line, { attr: { class: 'cf-tool done' } }, t + dur);
            tl.set(txt, { textContent: line.dataset.done }, t + dur);
            break;
          }
          case 'count': {
            // [when, 'count', target, dur]: a figure rolls from what it shows to its data-to value
            const e = el(a), to = e.dataset.to, from = e.textContent;
            const re = /^([^0-9]*)([0-9][0-9,]*\.?[0-9]*)(.*)$/;
            const mf = re.exec(from), mt = re.exec(to);
            if (!mf || !mt) throw new Error(`count: cannot roll "${from}" to "${to}"`);
            const dec = (mt[2].split('.')[1] || '').length, o = { v: parseFloat(mf[2].replace(/,/g, '')) };
            const fmt = (v) => mt[1] + v.toFixed(dec) + mt[3];
            tl.to(o, { v: parseFloat(mt[2].replace(/,/g, '')), duration: b || 1.1, ease: 'power2.out', onUpdate: () => { e.textContent = fmt(o.v); } }, t);
            tl.set(e, { textContent: to }, t + (b || 1.1));
            break;
          }
          case 'stream': {
            // [when, 'stream', {i, w}, dur]: Claude's own sentence appears a word at a time
            const p = items[a.w][a.i].querySelector('p');
            const words = p.textContent.split(' ');
            p.innerHTML = words.map((x) => `<span class="sw">${x}</span>`).join(' ');
            const ws = [...p.querySelectorAll('.sw')];
            gsap.set(ws, { opacity: 0 });
            ws.forEach((x, k) => tl.set(x, { opacity: 1 }, t + (k * (b || 1.2)) / ws.length));
            break;
          }
          case 'drag': {
            // [when, 'drag', {from:[x,y], to: target, file: name}, dur]: a file carried in and dropped
            const g = document.createElement('div');
            g.className = 'k-ghost';
            g.innerHTML = `<svg aria-hidden="true"><use href="#i-doc"/></svg><span>${a.file}</span>`;
            cam.appendChild(g);
            const r = rect(a.to), dur = b || 1.2, first = t < 0.02;     // a drag that opens the scene is on screen at frame 0
            gsap.set(g, { x: a.from[0], y: a.from[1], opacity: first ? 1 : 0, rotation: -4 });
            tl.to(g, { opacity: 1, duration: 0.15 }, t);
            tl.to(g, { x: r.x + r.w / 2 - 150, duration: dur, ease: 'power2.inOut' }, t);
            tl.to(g, { y: r.y + r.h / 2 - 26, duration: dur, ease: 'power1.inOut' }, t);
            tl.to(g, { rotation: 0, duration: dur * 0.6, ease: 'power2.out' }, t + dur * 0.4);
            tl.to(g, { opacity: 0, scale: 0.9, duration: 0.2 }, t + dur + 0.05);
            const cur = cursor();
            if (first) gsap.set(cur, { x: a.from[0] + 120, y: a.from[1] + 30, opacity: 1 });
            tl.to(cur, { opacity: 1, duration: 0.15 }, t);
            tl.fromTo(cur, { x: a.from[0] + 120, y: a.from[1] + 30 }, { x: r.x + r.w / 2 - 30, duration: dur, ease: 'power2.inOut', immediateRender: false }, t);
            tl.to(cur, { y: r.y + r.h / 2 + 4, duration: dur, ease: 'power1.inOut' }, t);
            tl.to(cur, { opacity: 0, duration: 0.2 }, t + dur + 0.3);
            break;
          }
          case 'label': {
            // [when, 'label', html, [x, y], until]: an identity label ("<mark> Dana Ruiz · advisor, in Claude"). Top left,
            // clear of the composer band; never a disclaimer the owner has not asked for
            const o = document.createElement('div');
            o.className = 'k-label';
            o.innerHTML = a;
            sc.appendChild(o);
            if (b[0] < 0) { o.style.left = 'auto'; o.style.right = (-b[0]) + 'px'; gsap.set(o, { y: b[1], opacity: 0 }); }
            else gsap.set(o, { x: b[0], y: b[1], opacity: 0 });
            tl.to(o, { opacity: 1, duration: 0.3, ease: 'power2.out' }, t);
            if (c !== undefined) tl.to(o, { opacity: 0, duration: 0.2 }, T(c));
            break;
          }
          case 'class': tl.set(el(a), { attr: { class: b } }, t); break;
          case 'enter': {
            // [when, 'enter', {from, dur}]: the scene arrives through blur, sliding in from a side or settling from a push
            const o = a || {}, from = o.from === 'right' ? { x: 240 } : o.from === 'left' ? { x: -240 } : { scale: o.from === 'push' ? 0.94 : 1.03 };
            tl.fromTo(sc, { opacity: 0, filter: 'blur(14px)', ...from }, { opacity: 1, filter: 'blur(0px)', x: 0, scale: 1, duration: o.dur || 0.5, ease: 'expo.out', immediateRender: false }, t);
            break;
          }
          case 'exit': {
            // [when, 'exit', {to, dur}]: the scene leaves through blur, shorter than it arrived
            const o = a || {}, to = o.to === 'left' ? { x: -240 } : o.to === 'right' ? { x: 240 } : { scale: 0.985 };
            tl.to(sc, { opacity: 0, filter: 'blur(14px)', ...to, duration: o.dur || 0.3, ease: 'power2.in' }, t);
            break;
          }
          case 'wheel': {
            // [when, 'wheel', {s, w, in}, index]: the focused row lifts; the rest of its list recede by distance
            const first = el(a), rows = [...first.parentElement.children].filter((x) => x.matches(a.s.split(' ').pop()));
            rows.forEach((r, i) => {
              const d = Math.abs(i - b);
              tl.to(r, { opacity: d === 0 ? 1 : Math.max(0.3, 1 - 0.36 * d), filter: 'blur(' + (d === 0 ? 0 : Math.min(2.2, 0.9 * d)) + 'px)', scale: d === 0 ? 1.025 : 1, duration: 0.42, ease: 'power2.out' }, t);
              tl.set(r, { attr: { 'data-focus': d === 0 ? '1' : '0' } }, t);
            });
            break;
          }
          case 'unwheel': { const first = el(a); tl.to([...first.parentElement.children], { opacity: 1, filter: 'blur(0px)', scale: 1, duration: 0.3 }, t); break; }
          case 'call': a(tl, t, { W, items, rect, el, cam, sc, T, dy }); break;
          default: throw new Error(`${id}: unknown step ${op}`);
        }
      });
    });
  };

  window.K = K;
})();
