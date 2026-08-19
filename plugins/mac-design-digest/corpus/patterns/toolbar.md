# Pattern: toolbar

Cross-app synthesis of the window toolbar (unified titlebar toolbar, floating-glass toolbar islands, and side-rail toolbars). Native-lineage evidence only. Kit floor: `kit/macos-27.md` — unified toolbar **52pt** (=8+36+8), unified-compact **40pt**, expanded **77pt**; toolbar controls are the **XL 36pt** tier; leading nav cluster = 20×20 buttons in a **73×36 glass group**; trailing search field **159×36**; Scroll Edge Effect overlay under the glass toolbar.

## Evidence

| App | Surface | Key values | Provenance |
|---|---|---|---|
| Letterboxx | reader (light, Tahoe) | **floating glass symbol-group** at detail-pane top-right: ~8 borderless monochrome SF Symbols (edit, chevron, copy, share, clipboard) + A/ⓘ/A trio, **one continuous glass edge (container morph)**; content stays opaque | (measured)(confirmed) |
| Atlas | gallery (light, Tahoe) | **chromeless — no toolbar bar**; four floating glass islands: `[traffic-light capsule][sidebar-toggle glass square]` top-left; bottom-center dark-glass segmented switcher (~44–52pt); bottom-right ~44pt circular import button | (estimated)(inferred) |
| Glance | doc window (dark, Tahoe) | glass-capsule toolbar, **~36pt (XL) controls, 3 groups**: zoom −/+ **morphed pair (one continuous container)** · icon pull-down · share; centred document title + "Edited" | (estimated)(inferred) |
| Fantastical | calendar (native) | content-top-left: `Today` capsule pop-over flanked by ‹ ›; centred **Day/Week/Month/Quarter/Year capsule segmented control**; "+" create trailing on sidebar | (estimated)(inferred) |
| Inkline | editor (dark, custom) | titlebar ~36pt (proxy-icon + POSIX path) + tab band ~44pt (~80pt total); rounded segmented view-switcher; `+` new-tab + browser tabs; trailing borderless group (back/fwd, search, A\|, sliders) | (estimated)(confirmed) |
| Compresto | converter (light, Tahoe) | unified translucent titlebar ~33pt, **centred bold title**, 3 trailing borderless SF Symbols (pin/clipboard/gear) in **one group** | (estimated)(inferred) |
| Sketch | canvas (custom) | **no unified toolbar** — floating opaque-white **capsule pill-clusters** over canvas, ≤4 function groups, borderless mono symbols + one full-colour brand glyph; standalone circular tool button above sidebar | (estimated)(inferred) |
| Room Service | dashboard (dark) | custom top bar: leading `PRO`+version badge; trailing borderless SF-Symbol cluster (⌘K, dark-mode, quick-actions, doc, terminal) in a capsule group | (measured)(inferred) |
| Zipic | batch results (light) | **toolbar-as-side-rail**: thin left vertical icon rail ~44–52px, borderless monochrome SF Symbols (add/archive/sort top; info/sliders pinned bottom) | (estimated)(inferred) |
| Picmal | batch table (legacy-native) | titlebar-centred 2-segment `Convert\|Compress` mode switch; primary lives in bottom bar not toolbar | (estimated)(inferred) |
| Presentify | annotation bar (native) | floating dark capsule: drag-handle · 5 colour swatches · dividers · draw-tool cluster; colour reserved to the ink swatches, all else monochrome | (estimated)(inferred) |
| Codeshot | utility (legacy-native) | minimal titlebar; centred pop-up accessory ("swift"), no real toolbar | (estimated)(inferred) |

## Converged rules

- **Toolbar symbols are borderless, monochrome SF Symbols, chunked into ≤3–4 function groups** — apps: Letterboxx, Glance, Compresto, Inkline, Sketch, Room Service, Zipic, Presentify — **(canon)**. Colour appears only where it is *data/identity* (Presentify's ink swatches, Sketch's one brand glyph), never as generic button tint.
- **Grouped controls share one continuous rounded/glass container per cluster (container morphing)** — apps: Letterboxx (one glass edge), Glance (morphed zoom pair), Canary Mail (capsule button groups), Dropzone (leading/trailing grouped containers with internal divider), Room Service (capsule cluster) — **(canon)**.
- **Exactly one prominent action per region; the rest are quiet borderless glyphs** — apps: Fantastical ("+"), Compresto (1 trailing group), Glance, Letterboxx, Presentify — **(canon)**. Corpus-wide the opposite (two saturated primaries) is the Focal Collision defect (macUSB).
- **Content stays opaque; glass lives only on the toolbar/chrome layer** — apps: Atlas, Letterboxx, Glance (clean glass discipline) — **(canon)** for Liquid-Glass-era builds. Contrast: Compresto puts the whole window on glass = logged glass-in-content defect.
- **Toolbar controls sit at the XL 36pt tier on a 40–52pt band** — apps: Glance (~36pt XL controls), Inkline (~80pt titlebar+tab), Room Service, Compresto (~33pt titlebar) — **(recurring→canon)** consistent with the kit's 52/40/77pt bands.
- **Segmented controls are for in-view scope, rendered as a native capsule with a raised white selected segment** — apps: Fantastical (Day/Week/Month), Atlas (Grid/Canvas/Infinity), Glance — **(canon)**; using a segmented control as *primary navigation* with a saturated-fill selection is the recurring native-tell defect (Mole, Mac 4 Breakfast, Satu, Picmal).

## Divergences

- **Where the toolbar lives.** Unified titlebar toolbar (Compresto, Inkline, Room Service) vs **floating glass islands over content** (Atlas, Letterboxx, Sketch's capsule pills, Glance) vs **side-rail** (Zipic). The floating-island split tracks the content-forward / Liquid-Glass clusters (gallery, canvas, reader) that want maximal content and dissolve chrome; the unified bar is the default for form/utility windows. Both are native-legal.
- **Titlebar title placement.** Centred document title (Glance, Compresto) vs left-aligned content-title (Autoshelf, Inkline path) vs personable centred window title (Atlas "HELLO, ATLAS"). Convention-level, not a lineage split.
- **Colour on the toolbar.** Almost always monochrome; the deliberate exceptions are a single full-colour identity glyph (Sketch's brand diamond, Glance's pull-down icon) used as a Von-Restorff anchor — a signature, flagged as a soft deviation from the borderless-monochrome norm.

## Generation guidance

- **Default to a unified toolbar** at **52pt** (8 + 36 XL controls + 8), or 40pt compact for a dense utility. Controls are the XL 36pt tier.
- **Group by function, ≤3–4 clusters**, each cluster in one continuous rounded/glass container with internal dividers (container morphing). Leading = navigation (back/forward, sidebar toggle); centre = title or in-view segmented scope switch; trailing = actions + a 159×36 search field.
- **All glyphs borderless + monochrome SF Symbols.** Spend colour only on data/identity, and at most one full-colour brand glyph as a deliberate focal anchor.
- **One prominent action per region.** Never two saturated filled primaries in the same view (Focal Collision). If a create/convert action needs prominence, make it the lone accent and keep everything else quiet.
- **Liquid-Glass builds:** float the toolbar as glass islands over edge-to-edge content and keep every content item opaque with its own soft shadow (Atlas/Letterboxx reference). Add the Scroll Edge Effect overlay under the glass so content stays legible as it scrolls under. Never seat lists/cards on the glass (Compresto's glass-in-content miss).
- **Segmented controls only for in-view scope**, styled as a native capsule with a raised neutral/white selected segment — not as top-level navigation, and never with a saturated accent-fill selected segment.
