// capture-subtree.js — browser-context capture of a rendered subtree with its COMPUTED
// styles inlined (improvement #7 — "extract the HTML and render it inside a React
// component" instead of rebuilding a decorative illustration from a screenshot by eye).
//
// Many sections are DECORATIVE and not CMS-editable — a hero product-illustration, a
// stat panel, a logo cloud. For those the fastest, pixel-EXACT conversion is to lift
// the reference's rendered subtree (its DOM + the resolved styles) and emit it as a
// React component, rather than hand-rebuilding it. This eval walks the subtree under
// MF_CAPTURE_SELECTOR, inlines a curated computed-style set onto every node (so it
// renders identically with no external CSS), strips classes/ids/scripts, and returns
// BOTH a cleaned `html` string AND a structured `tree` (for to-stylex.mjs to turn into
// an embed component or a StyleX skeleton).
//
//   obscura --allow-private-network fetch "http://localhost:<port>/<mock>.html" \
//     --eval "(() => { window.MF_CAPTURE_SELECTOR = '#hero .vignette'; return ($(cat capture-subtree.js))(); })()" \
//     --output capture.hero.json
//   node to-stylex.mjs --capture capture.hero.json --name HeroVignette --mode embed   # or --mode stylex
//
// The selector and the capture go in ONE eval: each fetch is a fresh page, so a global set by an
// earlier call is gone. The wrapping `(…)()` matters too — this file is a bare arrow function and
// --eval takes an expression.
//
// CHOOSE the mode by editability: `embed` for decorative/static (pixel-exact, fast);
// `stylex` for anything that must become a real, token-driven, CMS-editable component.
() => {
  const SEL = window.MF_CAPTURE_SELECTOR;
  const root = SEL ? document.querySelector(SEL) : document.body;
  if (!root) return JSON.stringify({ error: 'capture-root-not-found', selector: SEL });

  // The computed properties worth carrying so the lifted markup renders faithfully
  // without its original stylesheet. Defaults are dropped to keep the output small.
  //
  // SHORTHANDS ARE NOT TRUSTWORTHY under Obscura, so every shorthand here is paired
  // with its longhands and the longhands are listed AFTER it (later declarations win
  // in the inline style string). Measured: `padding`, `margin` and `borderRadius`
  // resolve to "0px" whatever the element sets; `border`, `background`, `boxShadow`,
  // `textTransform`, `flex` and `gap` resolve to the EMPTY STRING and are dropped by
  // the `v === ''` guard below. An empty value from getComputedStyle therefore means
  // "this engine does not report the property", NOT "the element does not set it" —
  // so a lift made here can be quietly missing a shadow, a gradient or a border that
  // is plainly visible in the render. Compare the lifted component against the
  // reference before trusting it as pixel-exact.
  const KEEP = [
    'display', 'flexDirection', 'flexWrap', 'alignItems', 'justifyContent', 'gap',
    'rowGap', 'columnGap',
    'gridTemplateColumns', 'gridTemplateRows', 'gridAutoFlow',
    'position', 'top', 'right', 'bottom', 'left', 'zIndex', 'overflow',
    'width', 'height', 'maxWidth', 'minWidth', 'flex',
    'margin', 'marginTop', 'marginRight', 'marginBottom', 'marginLeft',
    'padding', 'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
    'fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'lineHeight', 'letterSpacing',
    'textAlign', 'textTransform', 'color', 'whiteSpace',
    'background', 'backgroundColor', 'backgroundImage',
    'borderRadius', 'border', 'borderTop', 'borderBottom', 'borderLeft', 'borderRight',
    'borderTopLeftRadius', 'borderTopRightRadius', 'borderBottomRightRadius', 'borderBottomLeftRadius',
    'borderTopWidth', 'borderTopStyle', 'borderTopColor',
    'borderRightWidth', 'borderRightStyle', 'borderRightColor',
    'borderBottomWidth', 'borderBottomStyle', 'borderBottomColor',
    'borderLeftWidth', 'borderLeftStyle', 'borderLeftColor',
    'boxShadow', 'opacity', 'transform',
  ];
  const DEFAULTS = {
    display: 'block', position: 'static', margin: '0px', padding: '0px',
    marginTop: '0px', marginRight: '0px', marginBottom: '0px', marginLeft: '0px',
    paddingTop: '0px', paddingRight: '0px', paddingBottom: '0px', paddingLeft: '0px',
    border: '0px none rgb(0, 0, 0)', borderRadius: '0px', boxShadow: 'none',
    borderTopLeftRadius: '0px', borderTopRightRadius: '0px',
    borderBottomRightRadius: '0px', borderBottomLeftRadius: '0px',
    backgroundColor: 'rgba(0, 0, 0, 0)', backgroundImage: 'none', opacity: '1',
    transform: 'none', overflow: 'visible', zIndex: 'auto', textTransform: 'none',
    fontStyle: 'normal', whiteSpace: 'normal', flex: '0 1 auto', minWidth: 'auto',
    maxWidth: 'none', flexWrap: 'nowrap', gridAutoFlow: 'row',
    // flex/grid container props are noise on a non-container; drop their initial values
    flexDirection: 'row', alignItems: 'normal', justifyContent: 'normal', gap: 'normal',
    rowGap: 'normal', columnGap: 'normal',
    gridTemplateColumns: 'none', gridTemplateRows: 'none', letterSpacing: 'normal',
    top: 'auto', right: 'auto', bottom: 'auto', left: 'auto',
  };
  // `border` resolves to a noisy longhand string even when there's no border; drop it
  // unless a width is actually set.
  const skipBorder = (cs) => parseFloat(cs.borderTopWidth) === 0 && parseFloat(cs.borderBottomWidth) === 0 && parseFloat(cs.borderLeftWidth) === 0 && parseFloat(cs.borderRightWidth) === 0;
  const camelToKebab = (s) => s.replace(/[A-Z]/g, (m) => '-' + m.toLowerCase());

  function styleFor(el) {
    const cs = getComputedStyle(el);
    const noBorder = skipBorder(cs);
    const style = {};
    for (const p of KEEP) {
      const v = cs[p];
      if (v == null || v === '') continue;
      if (DEFAULTS[p] != null && v === DEFAULTS[p]) continue;
      // drop the border longhands when there's no real border — but NEVER borderRadius
      // (a card commonly has rounded corners with NO border; dropping it flattens it).
      if (noBorder && p !== 'borderRadius' && /^border/.test(p)) continue;
      // drop the verbose `background` shorthand when it's just the transparent default
      if (p === 'background' && /^rgba\(0, 0, 0, 0\)/.test(v)) continue;
      style[p] = v;
    }
    return style;
  }

  function walk(el) {
    const node = { tag: el.tagName.toLowerCase(), style: styleFor(el), text: '', children: [] };
    for (const n of el.childNodes) {
      if (n.nodeType === 3) { const t = n.textContent.replace(/\s+/g, ' '); if (t.trim()) node.text += t; }
      else if (n.nodeType === 1 && n.tagName.toLowerCase() !== 'script' && n.tagName.toLowerCase() !== 'style') {
        // carry through svg/img wholesale (icons/images) — keep their key attrs
        const tag = n.tagName.toLowerCase();
        if (tag === 'svg' || tag === 'path' || tag === 'img') {
          node.children.push({ tag, style: styleFor(n), raw: n.outerHTML, children: [] });
        } else {
          node.children.push(walk(n));
        }
      }
    }
    node.text = node.text.replace(/\s+/g, ' ').trim();
    return node;
  }

  // Cleaned, self-contained HTML (inlined styles, no classes) for the `embed` mode.
  function toHtml(node, indent) {
    if (node.raw) return ' '.repeat(indent) + node.raw;
    // Inline into a DOUBLE-quoted style attr, so any DOUBLE quotes in a value (a multi-word
    // font-family like "JetBrains Mono") would terminate the attribute early and silently drop
    // every following declaration (font, colour, size) — the element then falls back to
    // inherited sans-serif/black. Single-quote value-internal quotes to keep the attr intact.
    const styleStr = Object.entries(node.style).map(([k, v]) => `${camelToKebab(k)}:${String(v).replace(/"/g, "'")}`).join(';');
    const open = `<${node.tag}${styleStr ? ` style="${styleStr}"` : ''}>`;
    const inner = node.text && !node.children.length
      ? node.text
      : '\n' + node.children.map((c) => toHtml(c, indent + 2)).join('\n') + (node.text ? '\n' + ' '.repeat(indent + 2) + node.text : '') + '\n' + ' '.repeat(indent);
    return ' '.repeat(indent) + open + inner + `</${node.tag}>`;
  }

  const tree = walk(root);
  return JSON.stringify({ selector: SEL || 'body', tree, html: toHtml(tree, 0) });
}
