/* demo-video-craft starter kit: the stage runtime (K3.stage). Components sit alone on a plain ground and move with a
   calm reference film's grammar: a blur-in arrival, a blur-out exit, a component that grows out of the one before
   it or travels to its twin (moveTo), a list that turns with its focused row sharp and the rest receding, a
   carousel, a large cursor that glides in arcs and presses, wires that draw and carry dots. Uses kit.js (K.scene,
   K.when, K.ink, K.inkTo). Every value is a function of timeline time. */
(function () {
  const K3 = {};
  // A large cursor in the brand's ink (CSS color): a rounded arrow with a white keyline and a soft shadow
  const ARROW = '<svg width="46" height="46" viewBox="0 0 46 46"><path d="M8 5.5 L39 20.2 c1.6.8 1.4 3.1-.3 3.6 L26.6 27.4 c-.6.2-1.1.6-1.3 1.2 L21.7 40 c-.5 1.7-2.8 1.9-3.6.3 L6.2 9.2 C5.4 7.4 6.6 5 8 5.5 Z" fill="currentColor" stroke="#fff" stroke-width="2.6" stroke-linejoin="round"/></svg>';

  K3.stage = function (id, spec) {
    return K.scene(id, (tl, ctx) => {
      const root = document.querySelector('[data-composition-id="' + id + '"] .k-sc');
      const q = (sel) => { const e = root.querySelector(sel); if (!e) throw new Error(id + ': no ' + sel); return e; };
      const qa = (sel) => [...root.querySelectorAll(sel)];
      const T = (x) => (typeof x === 'number' ? x : ctx.at(K.when(x)));
      const R = root.getBoundingClientRect();
      const rect = (sel) => { const r = q(sel).getBoundingClientRect(); return { x: r.left - R.left, y: r.top - R.top, w: r.width, h: r.height }; };

      gsap.set(qa('.k3'), { xPercent: -50, yPercent: -50 });     // left/top name each component's centre
      // Every rect a step will need is measured at rest, before any component is set to its hidden start.
      const rects = {};
      (spec.steps || []).forEach((s) => {
        const [, op, a] = s;
        if ((op === 'cur' || op === 'press' || op === 'grow') && typeof a === 'string' && !rects[a]) rects[a] = rect(a);
        if (op === 'grow' && s[3] && s[3].from && !rects[s[3].from]) rects[s[3].from] = rect(s[3].from);
        if (op === 'moveTo') { if (!rects[a]) rects[a] = rect(a); if (!rects[s[3].to]) rects[s[3].to] = rect(s[3].to); }
        if (op === 'link') { if (!rects[a]) rects[a] = rect(a); if (!rects[s[3]]) rects[s[3]] = rect(s[3]); }
      });
      const comps = qa('.k3, .k3-hide');
      comps.forEach((c) => { if (!c.classList.contains('k3-shown')) gsap.set(c, { opacity: 0 }); });

      // the cursor, created once per scene; it enters from the edge it is told to
      let cur = null, cx = 0, cy = 0;
      const cursor = () => {
        if (cur) return cur;
        cur = document.createElement('div');
        cur.className = 'k3-cursor';
        cur.innerHTML = ARROW;
        root.appendChild(cur);
        const from = spec.cursorFrom || [1980, 760];
        cx = from[0]; cy = from[1];
        gsap.set(cur, { x: cx, y: cy, opacity: 0 });
        return cur;
      };
      const steps = (spec.steps || []).map((s, n) => ({ t: T(s[0]), n, s })).sort((a, b) => a.t - b.t || a.n - b.n);
      const inks = {}, links = {}, NS = 'http://www.w3.org/2000/svg';
      let svg = null;
      const wires = () => {
        if (svg) return svg;
        svg = document.createElementNS(NS, 'svg');
        svg.setAttribute('class', 'k3-wires'); svg.setAttribute('width', String(K.W)); svg.setAttribute('height', String(K.H));
        root.insertBefore(svg, root.firstChild);
        return svg;
      };
      steps.forEach(({ t, s }) => {
        const [, op, a, b, c] = s;
        switch (op) {
          case 'in': {
            // [when, 'in', sel, {dur, y, x, blur, scale}]: the arrival: blur clears as it rises
            const o = b || {}, e = q(a);
            tl.fromTo(e, { opacity: 0, y: o.y === undefined ? 18 : o.y, x: o.x || 0, scale: o.scale || 0.985, filter: `blur(${o.blur === undefined ? 10 : o.blur}px)` },
              { opacity: 1, y: 0, x: 0, scale: 1, filter: 'blur(0px)', duration: o.dur || 0.6, ease: 'expo.out', immediateRender: false }, t);
            break;
          }
          case 'out': {
            // [when, 'out', sel, {dur}]: blur and fade, shorter than the arrival
            const o = b || {};
            tl.to(q(a), { opacity: 0, filter: `blur(${o.blur || 10}px)`, scale: o.scale || 0.985, y: o.y || 0, duration: o.dur || 0.32, ease: 'power2.in' }, t);
            break;
          }
          case 'to': {
            // [when, 'to', sel, {dur, ease, ...gsap vars}]: dur and ease are the step's, never passed through as properties
            const { dur, ease, ...v } = b || {};
            tl.to(q(a), { ...v, duration: dur || 0.8, ease: ease || 'power3.inOut' }, t);
            break;
          }
          case 'grow': {
            // [when, 'grow', sel, {from: sel, dur}]: the component grows out of the one before it (button into card)
            const o = b || {}, e = q(a), to = rects[a], fr = rects[o.from];
            const sx = fr.w / to.w, dx = (fr.x + fr.w / 2) - (to.x + to.w / 2), dy = (fr.y + fr.h / 2) - (to.y + to.h / 2);
            tl.fromTo(e, { opacity: 0, x: dx, y: dy, scale: Math.max(0.2, sx), filter: 'blur(6px)' },
              { opacity: 1, x: 0, y: 0, scale: 1, filter: 'blur(0px)', duration: o.dur || 0.55, ease: 'expo.out', immediateRender: false }, t);
            if (o.hide !== false) tl.to(q(o.from), { opacity: 0, duration: 0.18, ease: 'power2.in' }, t);
            break;
          }
          case 'type': {
            // [when, 'type', sel, text, {cps}]: fast typing with a caret; the line then holds until something else happens
            const box = q(a), ph = box.querySelector('.ph'), cps = (c && c.cps) || 52;
            let ty = box.querySelector('.k3-typed');
            if (!ty) { ty = document.createElement('div'); ty.className = 'k3-typed'; ph.after(ty); }
            const caret = '<i class="k3-caret"></i>';
            tl.set(ph, { opacity: 0 }, t);
            const p = { n: 0 };
            tl.to(p, { n: b.length, duration: b.length / cps, ease: 'none', onUpdate: () => { ty.innerHTML = b.slice(0, Math.round(p.n)) + caret; } }, t);
            tl.call(() => { ty.innerHTML = b + caret; }, null, t + b.length / cps + 0.01);
            break;
          }
          case 'cur': {
            // [when, 'cur', sel, {dur, dx, dy}]: the cursor glides to a control in a shallow arc
            const o = b || {}, r = rects[a], k = cursor();
            const x = r.x + r.w * (o.ax === undefined ? 0.6 : o.ax) + (o.dx || 0), y = r.y + r.h * (o.ay === undefined ? 0.62 : o.ay) + (o.dy || 0), d = o.dur || 0.75;
            tl.to(k, { opacity: 1, duration: 0.2 }, t);
            tl.to(k, { x, duration: d, ease: 'power2.inOut' }, t);
            tl.to(k, { y, duration: d, ease: 'power1.inOut' }, t);
            cx = x; cy = y;
            break;
          }
          case 'press': {
            // [when, 'press', sel]: control and cursor press together, with a ring where the tip lands
            const e = q(a), k = cursor();
            tl.to(e, { scale: 0.96, duration: 0.09, ease: 'power2.out' }, t);
            tl.to(e, { scale: 1, duration: 0.24, ease: 'power2.out' }, t + 0.11);
            tl.to(k, { scale: 0.84, duration: 0.09 }, t);
            tl.to(k, { scale: 1, duration: 0.22 }, t + 0.11);
            const ring = document.createElement('div');
            ring.className = 'k3-ring';
            root.appendChild(ring);
            gsap.set(ring, { x: cx - 2, y: cy - 2, scale: 0.2, opacity: 0 });
            tl.fromTo(ring, { scale: 0.2, opacity: 0.55 }, { scale: 1, opacity: 0, duration: 0.5, ease: 'power2.out', immediateRender: false }, t);
            break;
          }
          case 'curout': if (cur) tl.to(cur, { opacity: 0, duration: 0.25 }, t); break;
          case 'wheel': {
            // [when, 'wheel', rowsSel, index, {dur}]: the focused row lifts; the rest recede by distance
            const rows = qa(a), dur = (c && c.dur) || 0.45;
            rows.forEach((r, i) => {
              const d = Math.abs(i - b);
              tl.to(r, { opacity: d === 0 ? 1 : Math.max(0.28, 1 - 0.38 * d), filter: `blur(${d === 0 ? 0 : Math.min(2.4, 0.9 * d)}px)`, scale: d === 0 ? 1.03 : 1, duration: dur, ease: 'power2.out' }, t);
              tl.set(r, { attr: { 'data-focus': d === 0 ? '1' : '0' } }, t);
            });
            break;
          }
          case 'unwheel': tl.to(qa(a), { opacity: 1, filter: 'blur(0px)', scale: 1, duration: 0.35, ease: 'power2.out' }, t); break;
          case 'track': {
            // [when, 'track', trackSel, index, {gap, dur}]: a carousel; the active card sharp, its neighbours faded
            const tr = q(a), items = [...tr.children], gap = (c && c.gap) || 760, dur = (c && c.dur) || 0.6;
            tl.to(tr, { x: -b * gap, duration: dur, ease: 'power3.inOut' }, t);
            items.forEach((it, i) => {
              const d = Math.abs(i - b);
              tl.to(it, { opacity: d === 0 ? 1 : 0.22, filter: `blur(${d === 0 ? 0 : 2.5}px)`, scale: d === 0 ? 1 : 0.94, duration: dur, ease: 'power3.inOut' }, t);
            });
            break;
          }
          case 'title': {
            // [when, 'title', sel, {stagger, dur}]: a chapter line that builds word by word, blur clearing. Never on
            // frame 0: the opener's line is complete from its first frame
            const e = q(a), words = [...e.querySelectorAll('.w')], o = b || {};
            gsap.set(e, { opacity: 1 });
            words.forEach((w, i) => tl.fromTo(w, { opacity: 0, filter: 'blur(8px)', y: 10 }, { opacity: 1, filter: 'blur(0px)', y: 0, duration: o.dur || 0.5, ease: 'expo.out', immediateRender: false }, t + i * (o.stagger || 0.08)));
            break;
          }
          case 'tool': {
            // [when, 'tool', sel, [status texts], dur]: the tool line narrates in the present tense, then finishes
            const line = q(a), txt = line.querySelector('.tl'), msgs = b || [], dur = c || 1.6, spin = line.querySelector('.spin');
            msgs.forEach((m, k) => tl.set(txt, { textContent: m }, t + (k * dur) / Math.max(1, msgs.length)));
            if (spin) tl.fromTo(spin, { rotation: 0 }, { rotation: 360 * Math.max(1, Math.round(dur / 0.8)), duration: dur, ease: 'none', immediateRender: false }, t);
            tl.set(line, { attr: { class: 'cf-tool done' } }, t + dur);
            tl.set(txt, { textContent: line.dataset.done }, t + dur);
            break;
          }
          case 'stream': {
            // [when, 'stream', sel, dur]: Claude's own sentence, a word at a time
            const p = q(a), words = p.textContent.split(' ');
            p.innerHTML = words.map((x) => '<span class="sw">' + x + '</span>').join(' ');
            const ws = [...p.querySelectorAll('.sw')];
            gsap.set(ws, { opacity: 0 });
            ws.forEach((x, k) => tl.set(x, { opacity: 1 }, t + (k * (b || 1.2)) / ws.length));
            break;
          }
          case 'count': {
            const e = q(a), to = e.dataset.to, from = e.textContent, re = /^([^0-9]*)([0-9][0-9,]*\.?[0-9]*)(.*)$/;
            const mf = re.exec(from), mt = re.exec(to);
            const dec = (mt[2].split('.')[1] || '').length, o = { v: parseFloat(mf[2].replace(/,/g, '')) };
            tl.to(o, { v: parseFloat(mt[2].replace(/,/g, '')), duration: b || 1.0, ease: 'power2.out', onUpdate: () => { e.textContent = mt[1] + o.v.toFixed(dec) + mt[3]; } }, t);
            tl.set(e, { textContent: to }, t + (b || 1.0));
            break;
          }
          case 'ink': inks[c && c.name || ('ink' + t)] = K.ink(tl, q(a), root, b, t, (c && c.dur) || 0.5); break;
          case 'inkTo': K.inkTo(tl, inks[a], b, t); break;
          case 'text': tl.set(q(a), { textContent: b }, t); break;
          case 'html': tl.set(q(a), { innerHTML: b }, t); break;
          case 'class': tl.set(q(a), { attr: { class: b } }, t); break;
          case 'show': tl.set(q(a), { opacity: 1 }, t); break;
          case 'swap': {
            // [when, 'swap', selA, selB]: one state of a component replaced by the next in place
            const x = q(a), y = q(b);
            tl.to(x, { opacity: 0, filter: 'blur(6px)', duration: 0.2, ease: 'power2.in' }, t);
            tl.fromTo(y, { opacity: 0, filter: 'blur(6px)', y: 8 }, { opacity: 1, filter: 'blur(0px)', y: 0, duration: 0.45, ease: 'expo.out', immediateRender: false }, t + 0.12);
            break;
          }
          case 'drag': {
            // [when, 'drag', {from:[x,y], to: sel, file}, dur]: a file carried in by the cursor and dropped
            const g = document.createElement('div');
            g.className = 'k3-ghost';
            g.innerHTML = '<svg aria-hidden="true"><use href="#i-doc"/></svg><span>' + a.file + '</span>';
            root.appendChild(g);
            const r = rect(a.to), d = b || 1.2, k = cursor();
            const tx = r.x + r.w / 2 - 160, ty = r.y + r.h / 2 - 30;
            gsap.set(g, { x: a.from[0], y: a.from[1], opacity: 0, rotation: -5 });
            tl.to(g, { opacity: 1, duration: 0.15 }, t);
            tl.to(g, { x: tx, duration: d, ease: 'power2.inOut' }, t);
            tl.to(g, { y: ty, duration: d, ease: 'power1.inOut' }, t);
            tl.to(g, { rotation: 0, duration: d * 0.6, ease: 'power2.out' }, t + d * 0.4);
            tl.to(g, { opacity: 0, scale: 0.92, duration: 0.2 }, t + d + 0.05);
            tl.set(k, { x: a.from[0] + 230, y: a.from[1] + 34 }, t);
            tl.to(k, { opacity: 1, duration: 0.15 }, t);
            tl.to(k, { x: tx + 230, duration: d, ease: 'power2.inOut' }, t);
            tl.to(k, { y: ty + 34, duration: d, ease: 'power1.inOut' }, t);
            cx = tx + 230; cy = ty + 34;
            break;
          }
          case 'label': {
            const o = document.createElement('div');
            o.className = 'k-label';
            o.innerHTML = a;
            root.appendChild(o);
            gsap.set(o, { x: b[0], y: b[1], opacity: 0 });
            tl.to(o, { opacity: 1, duration: 0.3 }, t);
            if (c !== undefined) tl.to(o, { opacity: 0, duration: 0.2 }, T(c));
            break;
          }
          case 'moveTo': {
            // [when, 'moveTo', sel, {to: sel, dur}]: a component travels to where another (a hidden twin) rests
            const o = b || {}, A = rects[a], B = rects[o.to];
            tl.to(q(a), { x: (B.x + B.w / 2) - (A.x + A.w / 2), y: (B.y + B.h / 2) - (A.y + A.h / 2), scale: B.w / A.w, duration: o.dur || 0.8, ease: 'power3.inOut' }, t);
            break;
          }
          case 'link': {
            // [when, 'link', fromSel, toSel, {name, dur, gap, dir}]: a line draws itself from one component's right edge to
            // another's left, or with dir 'down' from one's bottom to the other's top (a portrait diagram)
            const o = c || {}, A = rects[a], B = rects[b], g = o.gap === undefined ? 12 : o.gap;
            const p = document.createElementNS(NS, 'path');
            if (o.dir === 'down') {
              const x1 = A.x + A.w / 2, y1 = A.y + A.h + g, x2 = B.x + B.w / 2, y2 = B.y - g, my = (y1 + y2) / 2;
              p.setAttribute('d', 'M' + x1 + ' ' + y1 + ' C' + x1 + ' ' + my + ' ' + x2 + ' ' + my + ' ' + x2 + ' ' + y2);
            } else {
              const x1 = A.x + A.w + g, y1 = A.y + A.h / 2, x2 = B.x - g, y2 = B.y + B.h / 2, mx = (x1 + x2) / 2;
              p.setAttribute('d', 'M' + x1 + ' ' + y1 + ' C' + mx + ' ' + y1 + ' ' + mx + ' ' + y2 + ' ' + x2 + ' ' + y2);
            }
            p.setAttribute('class', 'k3-wire');
            wires().appendChild(p);
            const L = p.getTotalLength();
            gsap.set(p, { strokeDasharray: L, strokeDashoffset: L });
            tl.to(p, { strokeDashoffset: 0, duration: o.dur || 0.55, ease: 'power2.inOut' }, t);
            links[o.name || (a + '>' + b)] = p;
            break;
          }
          case 'flow': {
            // [when, 'flow', [link names], {dur, travel, every, stagger}]: dots run along each line, one after another
            const o = b || {}, travel = o.travel || 0.85, every = o.every || 0.5, d = o.dur || 3;
            a.forEach((name, pi) => {
              const p = links[name];
              if (!p) throw new Error(id + ': no link ' + name);
              const L = p.getTotalLength();
              for (let s0 = t + (o.stagger || 0) * pi; s0 + travel <= t + d; s0 += every) {
                const dot = document.createElementNS(NS, 'circle');
                dot.setAttribute('r', o.r || 6);
                dot.setAttribute('class', 'k3-dot');
                wires().appendChild(dot);
                const p0 = p.getPointAtLength(0), st = { u: 0 };
                gsap.set(dot, { attr: { cx: p0.x, cy: p0.y }, opacity: 0 });
                tl.to(st, { u: 1, duration: travel, ease: 'power1.inOut', onUpdate: () => { const pt = p.getPointAtLength(st.u * L); dot.setAttribute('cx', pt.x); dot.setAttribute('cy', pt.y); } }, s0);
                tl.fromTo(dot, { opacity: 0 }, { opacity: 1, duration: 0.1, immediateRender: false }, s0);
                tl.to(dot, { opacity: 0, duration: 0.12 }, s0 + travel - 0.12);
              }
            });
            break;
          }
          case 'call': a(tl, t, { q, qa, rect, root, T }); break;
          default: throw new Error(id + ': unknown step ' + op);
        }
      });
    });
  };
  window.K3 = K3;
})();
