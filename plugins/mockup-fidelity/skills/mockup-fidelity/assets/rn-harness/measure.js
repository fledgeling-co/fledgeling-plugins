/* eslint-disable */
// Dev-only UI-fidelity measurement probe (mockup-fidelity audit). Gitignored;
// remove after the audit. Walks the rendered fiber tree and POSTs a structural
// + geometric + style snapshot to the local collector (:8799). No-op unless __DEV__.
//
// Per host node it captures: id/parent/depth (containment tree), flexDir + the
// flattened StyleSheet (layout + style), the EFFECTIVE text style (RN Text
// inheritance merged from ancestor Text), text + numberOfLines/ellipsizeMode
// (truncation), image/icon source + name, testID/a11y/role, the foreground
// screen seq (RNSScreen isolation), and rect{x,y,w,h} via measureInWindow.
if (typeof __DEV__ !== 'undefined' && __DEV__) {
  (function () {
    var RN;
    try { RN = require('react-native'); } catch (e) { return; }
    var flatten = RN.StyleSheet.flatten;
    var Font; try { Font = require('expo-font'); } catch (e) {} // declared-vs-loaded font detection
    var hook = global.__REACT_DEVTOOLS_GLOBAL_HOOK__;
    var COLLECTOR = (typeof global.__MF_COLLECTOR === "string") ? global.__MF_COLLECTOR : "http://localhost:8799/dump";
    var SCREEN_TYPES = { RNSScreen: 1, RNSTabsScreenIOS: 1 };
    // text props that cascade through nested RN <Text>
    var TEXT_INHERIT = ['color', 'fontFamily', 'fontSize', 'fontWeight', 'fontStyle',
      'lineHeight', 'letterSpacing', 'textAlign', 'textTransform', 'textDecorationLine',
      'fontVariant', 'writingDirection', 'textShadowColor', 'textShadowRadius'];

    function getRoots() {
      var roots = [];
      if (!hook) return roots;
      try {
        var ids = hook.renderers ? Array.from(hook.renderers.keys()) : [1];
        for (var i = 0; i < ids.length; i++) {
          if (typeof hook.getFiberRoots === 'function') {
            var set = hook.getFiberRoots(ids[i]);
            set && set.forEach(function (r) { roots.push(r); });
          }
        }
      } catch (e) {}
      return roots;
    }

    function textOf(props) {
      if (!props) return undefined;
      var c = props.children;
      if (typeof c === 'string' || typeof c === 'number') return String(c);
      if (Array.isArray(c)) {
        var s = c.filter(function (x) { return typeof x === 'string' || typeof x === 'number'; }).join('');
        return s || undefined;
      }
      return undefined;
    }

    function isText(t) { return t === 'RCTText' || t === 'RCTSinglelineTextInputView' || t === 'RCTMultilineTextInputView'; }

    function compName(t) {
      if (!t) return undefined;
      return t.displayName || t.name ||
        (t.render && (t.render.displayName || t.render.name)) ||
        (t.type && (t.type.displayName || t.type.name)) || undefined;
    }

    function walk(fiber, ctx) {
      if (!fiber || ctx.out.length > 9000) return;
      var cur = ctx.sc, textCtx = ctx.text, parent = ctx.parent;
      var owner = ctx.owner, press = ctx.press, icon = ctx.icon, iconColor = ctx.iconColor, gradient = ctx.gradient;
      var t = fiber.type;
      // composite component: capture identity + interactivity + icon name/colour + gradient stops for descendants
      if (t && typeof t !== 'string') {
        var nm = compName(t);
        var cp = fiber.memoizedProps || {};
        if (nm) owner = nm;
        if (cp.onPress || cp.onPressIn || cp.onLongPress) press = true;
        if (nm === 'Icon') { if (typeof cp.name === 'string') icon = cp.name; if (cp.color != null) iconColor = cp.color; if (cp.size != null) iconColor = iconColor; }
        if (nm && /Gradient/.test(nm) && cp.colors) gradient = { colors: cp.colors, locations: cp.locations, start: cp.start, end: cp.end, angle: cp.angle };
      }
      if (typeof t === 'string') {
        var p = fiber.memoizedProps || {};
        if (SCREEN_TYPES[t]) {
          ctx.seq.n++;
          var as = p.activityState;
          cur = { seq: ctx.seq.n, active: (as === undefined || as === null) ? (p.active !== 0 && p.active !== false) : (as >= 2) };
        }
        var style; try { style = flatten(p.style) || {}; } catch (e) { style = {}; }
        var id = ctx.out.length;
        // effective text style = inherited Text props merged with own
        var eff, fontLoaded;
        if (isText(t)) {
          eff = {}; for (var k = 0; k < TEXT_INHERIT.length; k++) { var kk = TEXT_INHERIT[k]; if (textCtx[kk] !== undefined) eff[kk] = textCtx[kk]; if (style[kk] !== undefined) eff[kk] = style[kk]; }
          // did the declared font actually load? (catches serif-rendered-as-fallback)
          if (Font && Font.isLoaded && eff.fontFamily) { try { fontLoaded = Font.isLoaded(eff.fontFamily); } catch (e) {} }
        }
        var src = p.source && typeof p.source === 'object' ? (p.source.uri || p.source.testUri || null) : (typeof p.source === 'number' ? 'bundled' : undefined);
        var pOp = (ctx.opacity == null ? 1 : ctx.opacity);
        var effOp = pOp * (typeof style.opacity === 'number' ? style.opacity : 1);
        // SVG shape internals — captures icon/illustration content (fill/stroke/path)
        var svg;
        if (t.indexOf('RNSVG') === 0) {
          svg = {}; var SK = ['fill', 'stroke', 'strokeWidth', 'strokeOpacity', 'fillOpacity', 'd', 'points', 'cx', 'cy', 'r', 'rx', 'ry', 'x1', 'y1', 'x2', 'y2'];
          for (var si = 0; si < SK.length; si++) { if (p[SK[si]] !== undefined) svg[SK[si]] = p[SK[si]]; }
        }
        // native nav-header / tab-bar config — the JS-controlled props on the RNS* host nodes
        // (title, largeTitle, tint, tab label/icon/badge); the final native PIXEL render still needs a screenshot
        var cfg;
        if (t === 'RNSScreenStackHeaderConfig' || t === 'RNSScreenStackHeaderSubview' || t === 'RNSTabsHostIOS' || t === 'RNSTabsScreenIOS' || t === 'RNSScreen') {
          cfg = {}; for (var ck in p) { if (ck === 'children' || ck === 'style') continue; var v = p[ck]; var tv = typeof v; if (v != null && (tv === 'string' || tv === 'number' || tv === 'boolean')) cfg[ck] = v; }
        }
        var node = {
          id: id, parent: parent, depth: ctx.depth,
          type: t, testID: p.testID, a11y: p.accessibilityLabel, role: p.accessibilityRole || p.role,
          a11yState: p.accessibilityState, pointerEvents: p.pointerEvents || style.pointerEvents,
          placeholder: p.placeholder, placeholderTextColor: p.placeholderTextColor,
          numberOfLines: p.numberOfLines, ellipsizeMode: p.ellipsizeMode,
          source: src, resizeMode: p.resizeMode, name: typeof p.name === 'string' ? p.name : undefined,
          text: textOf(p),
          scr: cur.seq, act: cur.active,
          flexDir: style.flexDirection, align: style.alignItems, justify: style.justifyContent,
          owner: owner, icon: icon, iconColor: iconColor, gradient: gradient, svg: svg, cfg: cfg,
          press: press || !!(p.onPress || p.onPressIn || p.onLongPress),
          effOpacity: Math.round(effOp * 100) / 100,
          effStyle: eff, fontLoaded: fontLoaded, style: style,
        };
        ctx.out.push(node);
        if (fiber.stateNode) {
          ctx.refs.push({ node: node, ref: fiber.stateNode });
        }
        parent = id;
        // extend the inherited text context for descendants
        if (isText(t)) { var nt = {}; for (var kkk in textCtx) nt[kkk] = textCtx[kkk]; for (var ki = 0; ki < TEXT_INHERIT.length; ki++) { if (style[TEXT_INHERIT[ki]] !== undefined) nt[TEXT_INHERIT[ki]] = style[TEXT_INHERIT[ki]]; } textCtx = nt; }
      }
      walk(fiber.child, { out: ctx.out, refs: ctx.refs, seq: ctx.seq, depth: ctx.depth + 1, sc: cur, text: textCtx, parent: parent, opacity: (typeof t === 'string' ? (ctx.out[parent] && ctx.out[parent].effOpacity) : ctx.opacity), owner: owner, press: press, icon: icon, iconColor: iconColor, gradient: gradient });
      walk(fiber.sibling, { out: ctx.out, refs: ctx.refs, seq: ctx.seq, depth: ctx.depth, sc: ctx.sc, text: ctx.text, parent: ctx.parent, opacity: ctx.opacity, owner: ctx.owner, press: ctx.press, icon: ctx.icon, iconColor: ctx.iconColor, gradient: ctx.gradient });
    }

    function dump(screen) {
      var out = [], refs = [], seq = { n: 0 };
      var roots = getRoots();
      for (var i = 0; i < roots.length; i++) {
        try { walk(roots[i].current, { out: out, refs: refs, seq: seq, depth: 0, sc: { seq: 0, active: true }, text: {}, parent: -1 }); } catch (e) {}
      }
      var posted = false;
      function post() {
        if (posted) return; posted = true;
        try {
          fetch(COLLECTOR + '?screen=' + encodeURIComponent(screen || 'latest'), {
            method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(out),
          }).catch(function () {});
        } catch (e) {}
      }
      var nfm = global.nativeFabricUIManager;
      // async geometry pass — Fabric: canonical.measureInWindow / canonical.measure / nativeFabricUIManager(shadowNode)
      if (refs.length === 0) { post(); return out.length; }
      var settled = 0, total = refs.length;
      function fin() { settled++; if (settled >= total) post(); }
      function r1(v) { return Math.round(v * 10) / 10; } // sub-pixel (1 decimal)
      function setRect(node, x, y, w, h) { if (typeof x === 'number' && (w || h)) node.rect = { x: r1(x), y: r1(y), w: r1(w), h: r1(h) }; }
      refs.forEach(function (r) {
        var sn = r.ref, c = sn && sn.canonical, shadow = sn && sn.node;
        try {
          if (c && typeof c.measureInWindow === 'function') { c.measureInWindow(function (x, y, w, h) { setRect(r.node, x, y, w, h); fin(); }); return; }
          if (c && typeof c.measure === 'function') { c.measure(function (x, y, w, h, px, py) { setRect(r.node, px, py, w, h); fin(); }); return; }
          if (nfm && shadow && typeof nfm.measureInWindow === 'function') { nfm.measureInWindow(shadow, function (x, y, w, h) { setRect(r.node, x, y, w, h); fin(); }); return; }
          if (nfm && shadow && typeof nfm.measure === 'function') { nfm.measure(shadow, function (x, y, w, h, px, py) { setRect(r.node, px, py, w, h); fin(); }); return; }
          fin();
        } catch (e) { fin(); }
      });
      setTimeout(post, 700);
      return out.length;
    }

    global.__auditDump = dump;
    setInterval(function () { dump('latest'); }, 1500);
    console.log('[audit] enhanced measure probe active; hook=', !!hook);
  })();
}
