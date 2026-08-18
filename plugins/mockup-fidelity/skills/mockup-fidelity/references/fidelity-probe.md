# Fidelity probe — one-pass capture

The validation pass's biggest time sink is **re-navigating to the same surface to check one more thing**. Each visit costs a login + load + state-setup, and Phase 3 has ~8 render-time checks; doing them as separate visits multiplies that cost. This probe collapses all of them into **one `eval` per surface/state**: it runs inside the already-rendered page and returns a JSON snapshot carrying every render-time signal the validation needs. Capture once, then classify offline from the JSON (and the screenshot) — never re-open the page to re-check a single property.

It carries **two axes**, read in order: a **structural axis** for the structure-before-styling diff (SKILL.md Phase 3B) — `skeleton` (the nested landmark-region tree) and each control's `id` (stable identity) + `anchor` (containment path + position within its container), which is how you catch a *relocated* control without comparing meaningless absolute coordinates — and a **styling axis** for the per-property pass (Phase 3C) — region `style`, fingerprints, thin/empty flags, broken icons, editors. (Use the present/divergent/absent ledger of Phase 3A for breadth first; this probe powers 3B and 3C.)

What it is and isn't:
- It **augments** the screenshots — it does not replace rendering. The probe only runs because the page is rendered, so its output is *rendered evidence* (the live DOM), exactly what this skill demands — never source-read inference. Screenshots remain mandatory ledger evidence.
- It is a **detection** snapshot (enough signal to find, prove, and classify drift). Hand the confirmed stylistic gaps to the per-property styling pass (Phase 3C) and fix them in Phase 6; don't try to pixel-align here. For a React Native target with no DOM, resolve styles from the component's StyleSheet + tokens instead (see `react-native.md`).

## Usage

1. `Read` this file, copy the `probeFidelity` function, and inject it into the rendered page with whatever browser tool you're using, calling it once and returning `JSON.stringify(...)`. Save the result to a workspace file so the audit, the fix loop, and any sub-agents read from disk instead of re-navigating.
2. Pass the elements/regions/variants you care about as `{ elements: { label: cssSelector } }` — named matches are the highest-signal output. Variant sets (urgent vs normal row, each status colour, sizes) should be passed as one selector that matches all siblings, or one label per variant; the probe records each so you can compare them **against each other** (the `variantsIdentical` check) without another visit.
3. Run it identically on the **reference** and the **target** for each state. The reference never changes during an audit — capture it **once** and reuse that JSON for every later diff and every fix-loop iteration; only the target is re-captured after a fix.

Per-tool injection:
- **agent-browser** — wrap in an IIFE; the eval result comes back double-JSON-encoded, so decode twice: `(function(){ /* paste fn */ return JSON.stringify(probeFidelity({elements:{...}})); })()`
- **Obscura** — `obscura fetch <url> --eval "(() => { /* paste fn */ return probeFidelity({elements:{...}}); })()"` (`--eval` takes an expression, not a function, and does not await a promise)
- **Obscura MCP** (`browser_evaluate`) — for a state you must click your way to; the param is `expression`, and like `--eval` it does not await a promise.

Open every gated state (modal/drawer/popover/expanded) in the **same** session — drive each trigger, then probe that state before moving on — so all states are captured in one navigation rather than one navigation per modal.

## The probe

```js
// fidelity-probe — one-pass UI fidelity snapshot. Runs IN the rendered page.
// Returns JSON-serialisable detection signal for the whole surface in one call.
function probeFidelity(opts) {
  opts = opts || {};
  var rootSel = opts.root || 'body';
  var named = opts.elements || null;        // { label: cssSelector } — the things you care about
  var maxEls = opts.max || 400;
  var root = document.querySelector(rootSel) || document.body;
  var cls = function (el) { return (el.getAttribute && el.getAttribute('class')) || ''; };

  function sideBorder(cs, side) {
    var w = cs.getPropertyValue('border-' + side + '-width');
    if (parseFloat(w) === 0) return '0';    // a 0-width border still reports style+colour; ignore it
    return w + ' ' + cs.getPropertyValue('border-' + side + '-style') + ' ' + cs.getPropertyValue('border-' + side + '-color');
  }
  function styleOf(el) {
    var cs = getComputedStyle(el);
    return {
      display: cs.display, position: cs.position,
      bg: cs.backgroundColor,
      bgImage: cs.backgroundImage === 'none' ? '' : cs.backgroundImage,
      borderTop: sideBorder(cs, 'top'), borderRight: sideBorder(cs, 'right'),
      borderBottom: sideBorder(cs, 'bottom'), borderLeft: sideBorder(cs, 'left'),
      radius: [cs.borderTopLeftRadius, cs.borderTopRightRadius, cs.borderBottomRightRadius, cs.borderBottomLeftRadius].join(' '),
      shadow: cs.boxShadow === 'none' ? '' : cs.boxShadow,
      color: cs.color,
      font: cs.fontWeight + ' ' + cs.fontSize + '/' + cs.lineHeight + ' ' + (cs.fontFamily || '').split(',')[0],
      letterSpacing: cs.letterSpacing,
      pad: [cs.paddingTop, cs.paddingRight, cs.paddingBottom, cs.paddingLeft].join(' '),
      margin: [cs.marginTop, cs.marginRight, cs.marginBottom, cs.marginLeft].join(' '),
      gap: cs.rowGap + ' ' + cs.columnGap,
      opacity: cs.opacity, visibility: cs.visibility
    };
  }
  // visual fingerprint — equal fp on two sibling variants ⇒ a variant prop isn't wired
  function fingerprint(s) { return [s.bg, s.borderTop, s.borderLeft, s.radius, s.shadow, s.color, s.font].join(' | '); }
  function svgInfo(el) {
    var svg = el.querySelector('svg');
    if (!svg) return { hasSvg: false, paths: 0 };
    return { hasSvg: true, paths: svg.querySelectorAll('path,line,circle,rect,polygon,polyline').length };
  }

  var ctlSel = 'button,a[href],[role="button"],[role="tab"],[role="menuitem"],input,select,textarea,[contenteditable="true"]';

  // --- structural identity + placement (3A: skeleton / anchor diff) ----------
  // A stable cross-surface identity. Absolute coords differ between two surfaces
  // (a 59px icon sidebar vs a 250px labelled one shifts everything); identity +
  // containment do NOT — so this is what you pair controls by, never box.x.
  function stableId(el) {
    var al = el.getAttribute && (el.getAttribute('aria-label') || el.getAttribute('title'));
    if (al && al.trim()) return al.trim().slice(0, 40);
    var t = (el.textContent || '').trim();
    if (t) return t.slice(0, 40);
    var nm = el.getAttribute && el.getAttribute('name');
    if (nm) return '@' + nm;
    return el.tagName.toLowerCase()
      + (el.getAttribute && el.getAttribute('role') ? '[' + el.getAttribute('role') + ']' : '')
      + (svgInfo(el).hasSvg ? '{icon}' : '');
  }
  // Is this a structural "landmark" region — a node worth a row in the skeleton
  // and a segment in a control's containment path? Semantic tags, ARIA, or a
  // sizeable box that paints its own surface (bg/border).
  function isLandmark(el) {
    if (!el || el === document.body || el.nodeType !== 1) return false;
    var tag = el.tagName.toLowerCase();
    if (/^(header|nav|main|aside|section|footer|form|dialog|ul|ol|table)$/.test(tag)) return true;
    if (el.getAttribute && (el.getAttribute('role') || el.getAttribute('aria-label'))) return true;
    var r = el.getBoundingClientRect();
    if (r.width < 80 || r.height < 28) return false;
    var cs = getComputedStyle(el);
    var hasBg = cs.backgroundColor && cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== 'transparent';
    var hasBorder = ['top', 'right', 'bottom', 'left'].some(function (sd) { return parseFloat(cs.getPropertyValue('border-' + sd + '-width')) > 0; });
    return hasBg || hasBorder;
  }
  function landmarkLabel(el) {
    var al = el.getAttribute && (el.getAttribute('aria-label') || el.getAttribute('role'));
    var c = cls(el) ? '.' + ('' + cls(el)).trim().split(/\s+/).slice(0, 2).join('.') : '';
    return el.tagName.toLowerCase() + (al ? '[' + al + ']' : '') + (el.id ? '#' + el.id : c);
  }
  // The nearest landmark ancestor of `el`, or null.
  function nearestLandmark(el) {
    var n = el.parentElement, h = 0;
    while (n && n !== document.body && h < 40) { if (isLandmark(n)) return n; n = n.parentElement; h++; }
    return null;
  }
  // Containment anchor: the chain of landmark ancestors (outer→inner) + the
  // control's position WITHIN its nearest landmark (left/centre/right) + sibling
  // index. Diff THIS across surfaces, not box.x — a different `container` means a
  // relocated control (the kebab moved from `header > nav` to the right cluster).
  function anchorOf(el) {
    var path = [], n = el.parentElement, hops = 0;
    while (n && n !== document.body && hops < 40 && path.length < 4) { if (isLandmark(n)) path.unshift(landmarkLabel(n)); n = n.parentElement; hops++; }
    var within = '', container = nearestLandmark(el);
    if (container) {
      var cr = container.getBoundingClientRect(), er = el.getBoundingClientRect();
      if (cr.width > 0) { var f = (er.left + er.width / 2 - cr.left) / cr.width; within = f < 0.34 ? 'left' : (f > 0.66 ? 'right' : 'center'); }
    }
    var sib = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : -1;
    return { container: path.join(' > '), within: within, sibIndex: sib };
  }

  function rec(el, label) {
    var r = el.getBoundingClientRect();
    var s = styleOf(el);
    var txt = (el.textContent || '').trim();
    var svg = svgInfo(el);
    var isEditor = !!(el.matches && el.matches('textarea,[contenteditable="true"],[role="textbox"],.ProseMirror,.cm-editor,.tiptap,.ql-editor'))
                 || !!el.querySelector('[contenteditable="true"],.ProseMirror,.cm-editor,.ql-editor');
    return {
      label: label, id: stableId(el), tag: el.tagName.toLowerCase(), role: (el.getAttribute && el.getAttribute('role')) || '',
      box: { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) },
      anchor: anchorOf(el),
      textLen: txt.length, text: txt.slice(0, 80), childCount: el.childElementCount,
      svg: svg, editor: isEditor, style: s, fp: fingerprint(s),
      // thin/empty: exists but paints essentially nothing (content didn't reach the DOM)
      empty: (r.height < 2 || r.width < 2) || (txt.length === 0 && el.childElementCount === 0 && !svg.hasSvg)
    };
  }

  var out = {
    meta: { url: location.href, title: document.title,
            viewport: { w: window.innerWidth, h: window.innerHeight, dpr: window.devicePixelRatio }, capturedRoot: rootSel },
    named: {}, skeleton: [], controls: [], editors: [], regions: []
  };

  // (1) explicitly named elements / regions / variant sets — highest-signal; pass these in
  if (named) Object.keys(named).forEach(function (label) {
    var nodes = root.querySelectorAll(named[label]);
    if (!nodes.length) { out.named[label] = { label: label, missing: true, selector: named[label] }; return; }
    out.named[label] = nodes.length === 1
      ? rec(nodes[0], label)
      : Array.prototype.slice.call(nodes, 0, 24).map(function (n, i) { return rec(n, label + '[' + i + ']'); });
  });

  // (2) every interactive control — presence + STABLE IDENTITY + containment anchor in one capture
  // (control-placement / relocated-control / extras / broken-icon checks). Pair across surfaces by `id`,
  // diff by `anchor` (container path + within) — NOT by box.x, which differs whenever the surrounding chrome does.
  Array.prototype.slice.call(root.querySelectorAll(ctlSel), 0, maxEls).forEach(function (el) {
    var r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return;
    var svg = svgInfo(el), txt = (el.textContent || '').trim();
    out.controls.push({
      id: stableId(el), tag: el.tagName.toLowerCase(), role: (el.getAttribute('role') || ''), type: (el.getAttribute('type') || ''),
      text: txt.slice(0, 60), textLen: txt.length,
      box: { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) },
      anchor: anchorOf(el),
      iconOnly: txt.length === 0 && svg.hasSvg, brokenIcon: svg.hasSvg && svg.paths === 0, childCount: el.childElementCount
    });
  });

  // (3) rich editors / contenteditable (editor-rendered-as-static-text check)
  Array.prototype.slice.call(root.querySelectorAll('textarea,[contenteditable="true"],[role="textbox"],.ProseMirror,.cm-editor,.tiptap,.ql-editor'), 0, 40)
    .forEach(function (el) { var r = el.getBoundingClientRect();
      out.editors.push({ tag: el.tagName.toLowerCase(), cls: ('' + cls(el)).slice(0, 80), box: { w: Math.round(r.width), h: Math.round(r.height) } }); });

  // (4) significant region containers (region-wrapper / separator check): sizeable elements carrying bg/border/shadow
  var seen = 0;
  Array.prototype.slice.call(root.querySelectorAll('*')).some(function (el) {
    if (seen >= maxEls) return true;
    var r = el.getBoundingClientRect();
    if (r.width < 80 || r.height < 40) return false;
    var cs = getComputedStyle(el);
    var hasBg = cs.backgroundColor && cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== 'transparent';
    var hasBorder = ['top', 'right', 'bottom', 'left'].some(function (sd) { return parseFloat(cs.getPropertyValue('border-' + sd + '-width')) > 0; });
    var hasShadow = cs.boxShadow && cs.boxShadow !== 'none';
    if (!(hasBg || hasBorder || hasShadow)) return false;
    seen++;
    var label = el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
      (cls(el) ? '.' + ('' + cls(el)).trim().split(/\s+/).slice(0, 2).join('.') : '');
    out.regions.push(rec(el, label));
    return false;
  });

  // (5) structural skeleton (FRAME-FIRST / placement diff — Phase 3B): the ordered, nested
  // tree of landmark regions, each carrying the stable ids of the controls DIRECTLY inside it
  // (a control is attributed to its nearest landmark). Diff this tree across surfaces BEFORE any
  // styling check — an extra wrapper, a dropped region, or a control under a different parent is a
  // structural defect that a flat list and a downscaled screenshot both miss.
  function buildSkeleton(node, depth) {
    var kids = [], children = node.children ? Array.prototype.slice.call(node.children) : [];
    for (var i = 0; i < children.length && kids.length < 80; i++) {
      var ch = children[i];
      if (isLandmark(ch)) {
        var r = ch.getBoundingClientRect();
        var directControls = Array.prototype.slice.call(ch.querySelectorAll(ctlSel))
          .filter(function (c) { return nearestLandmark(c) === ch; })
          .map(function (c) { return stableId(c); }).slice(0, 24);
        kids.push({
          tag: ch.tagName.toLowerCase(), label: landmarkLabel(ch),
          box: { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) },
          controls: directControls,
          children: depth < 4 ? buildSkeleton(ch, depth + 1) : []
        });
      } else if (depth < 8) {
        // descend through plain wrappers so landmarks nested in non-landmark divs still surface
        var deeper = buildSkeleton(ch, depth);
        if (deeper.length) kids = kids.concat(deeper);
      }
    }
    return kids;
  }
  out.skeleton = buildSkeleton(root, 0);

  return out;
}
```

## Reading the snapshot offline (each Phase 3 check → a field, no re-visit)

Diff the reference JSON against the target JSON — every Phase 3 signal is already in hand.

**Do the structural diff first (Phase 3B), before any styling field:**

- **Skeleton / frame** — diff `skeleton` (the nested landmark tree) tree-to-tree: a region in one side's tree but not the other (an extra header strip; a dropped section), a different *order*, or a different *nesting* is a structural `DEFECT`. This is the frame check — reconcile the skeletons before you read a single style.
- **Control placement / relocation (the anchor table)** — pair `controls` across surfaces by **`id`** (stable identity), then diff each pair's **`anchor`** (`container` path + `within`), **never `box.x`** — absolute coordinates differ whenever the surrounding chrome does, so they can't be compared. Same `id`, different `anchor.container` ⇒ a **relocated control** (e.g. the kebab moved from `header > nav` to the right cluster). Same `id` missing on one side ⇒ missing affordance / added extra. Build the anchor table from this; "present" alone is never a pass.

**Then the per-property styling fields (Phase 3C):**

- **Region containers / separators** — compare `regions[].style` (`bg`, `border*`, `radius`, `shadow`): a reference region with a background/border/shadow whose target counterpart reads bare is a missing wrapper/divider.
- **Container spacing** — diff `regions[].style.pad` / `margin` / `gap` (and the same on `named` records) between sides: the *same* wrapper with a different padding / label margin / gap is a spacing drift (the rail that's looser or tighter than the reference, even when the outer container's padding matches). Flag it with the measured numbers; hand the exact alignment to the per-property styling pass (Phase 3C / fix in Phase 6) — don't let it fall through "the wrapper is there ✓".
- **Editors & rich affordances** — reference `editors` non-empty but target `editors` empty (or the same region's `editor:false`) ⇒ a rich editor rendered as static text.
- **Data-driven emptiness / thin renders** — `empty:true`, `textLen:0` where the reference has text, or `box.h` near zero ⇒ content didn't reach the DOM.
- **Broken icons** — `controls[].brokenIcon` / a `named` record with `svg.hasSvg && svg.paths===0` ⇒ an icon that renders a blank square.
- **Un-wired variants** — among a `named` variant array, if two siblings share the same `fp`, the variant prop is dead.
- **Missing named element** — `named[label].missing === true`.

A row in the ledger still needs its screenshot pair; the probe gives you the exact, measured *why* behind each row in one pass.
