# macOS Native Analysis — lineage, Liquid Glass, and the native-feel grammar

Distilled from the `macosify` plugin's analysis framework, HIG library, and its learnings corpus (patterns evidenced across 60+ real macOS screenshots). Use during Workflow A on every macOS screenshot: it supplies the **lineage classification**, the **Liquid Glass evidence rules**, and the **native-tells audit** that the cross-platform rubric in knowledge-base.md doesn't cover. If the macosify plugin is installed, its deeper resources are available (see §6).

## 1. Framework lineage classification — run before taking taste evidence

Not everything running on a Mac is *of* the Mac. Classify every screenshot's lineage first, because **only native-reading evidence may feed macOS canon and style clusters** — an iOS-derived app's density or selection styling must never be learned as "mac taste":

| Lineage | What it is | Tells | Corpus treatment |
|---|---|---|---|
| **AppKit-native** (incl. macOS-correct SwiftUI) | True Mac app | 13pt body, compact 20–28pt controls, real menu bar, source-list sidebar with *inset rounded* selection, pop-up/pull-down buttons, concentric corners | ✅ Full evidence: feeds profiles, patterns, clusters, canon |
| **Mac Catalyst** | UIKit iPad app bridged | Real Mac *frame* (traffic lights, sidebar) wrapping an iOS *body*: inset-grouped card tables, `UISwitch` pills, ~17pt density, per-row chevrons, sheet with in-content ✕/back | ⚠ Profile it, but mark `lineage: catalyst`; its iOS-derived properties are recorded as tells + corrections, excluded from macOS canon |
| **iOS-on-Apple-Silicon** | Unmodified iPad app | 44pt touch controls everywhere, iOS tab bar, full-screen modal sheets, no pointer affordances | ❌ Contrast evidence only |
| **Web/Electron** | Web UI in a Mac window | 16px web body, card grids, tracked-UPPERCASE headers, pointer-hand cursor, ⋮ kebab menus, full-bleed flat selection, persistent bottom format bars | ❌ Contrast evidence only (unless the user is deliberately studying good Electron apps — then a separate non-native cluster) |

Judge lineage from the **body, not the frame** — Catalyst gets the chrome and sidebar mostly right. **Density is the strongest single discriminator**: check body size (13pt vs 17px) and control height (24 vs 44) first. Record lineage with a confidence; when ambiguous, say so.

**Era sub-classification for native apps:** pre-Tahoe captures (flat opaque chrome, hard 1px dividers, saturated full-bleed blue selection, small window radius, bezeled/gradient controls) are *legacy-native* — an era marker, not an iOS tell. Record era in the app profile; legacy evidence supports timeless rules (layout, hierarchy) but not current-material rules.

## 2. Liquid Glass evidence rules (macOS 26+)

Liquid Glass is a lensing material (light bends at edges, adaptive tinting), not Gaussian blur — and it obeys a strict grammar you can audit from stills:

- **The Golden Rule:** glass belongs ONLY to the floating functional layer — toolbar, sidebar, menus, popovers, sheets, alerts, floating pills. Content (lists, tables, canvases, cards, charts, form rows) stays opaque. Glass-in-content and glass-on-glass are the two cardinal defects.
- **Absence of glass is legitimate.** The rule forbids glass in content; it never mandates glass on chrome. A fully flat opaque window (settings forms, choosers, pro-tool chrome like Xcode) passes. Don't record "missing glass" as a defect on a pro-density app.
- **Container morphing signature:** adjacent glass controls sharing one continuous refractive edge (not N separately-bordered pills) = a glass container grouping. Separately-bordered adjacent glass = the glass-on-glass risk, note it.
- **Scroll-edge effect:** the bright translucent fade where content slides under a glass toolbar is the *bar's* edge treatment, not a glass card behind content. Expect it wherever content meets floating chrome; a hard opaque bar-line there is a pre-Tahoe or non-native tell.
- **Dark-mode humility:** large dark glass reads near-opaque graphite and doesn't flip appearance — from one still you usually *cannot* distinguish Regular glass from solid material or Reduce Transparency. Record `(insufficient-evidence)` rather than asserting; content-layer cards with their own gradients/imagery are never glass.
- **Tint discipline:** tint only the one primary action; recessive controls on glass are translucent fills/vibrancy, never nested glass.

## 3. The native-feel grammar (highest-leverage observed rules)

The loudest tells from the learnings corpus — what most determines whether a surface reads native. Use these when digesting (is this app honouring or deviating?) and when generating:

1. **Selection = flat inset rounded fill with accent-tinted text/glyph** — never a full-bleed bar, never a glossy saturated capsule. Same grammar in sidebar and content lists. (System Settings' stronger solid-accent fill is its house style, not the general rule.)
2. **Sidebar section headers: system font, semibold, secondary colour, sentence/title case — never tracked uppercase.** The #1 sidebar authenticity tell.
3. **Accent is the user's, not the app's:** selection, focus rings, carets, the one primary action bind to the system accent. Per-item identity colours (calendar dots, chart series) come from the 12-hue system palette and are separate. Status colour is always paired with a glyph/label, never alone.
4. **Density:** 13pt body, visible controls 20–28pt padded to 44pt hit targets, rows ~24–28pt. Hierarchy from the label tiers (primary/~55%/~25%), not size inflation.
5. **One prominent action per view**, trailing; Cancel leading; ≤3 alert buttons; destructive never default; "…" suffix means opens-a-further-view; disabled controls dim, never disappear.
6. **Pop-up vs pull-down:** double up/down chevron + label-shows-value = pick a value; single chevron + static title = actions menu. Steppers always pair with an editable field.
7. **Control by meaning:** checkbox for independent settings, radio for exclusive sets, switch only for emphasized/group toggles (~22pt, accent), segmented control for in-view scope switching — never main navigation (that's a sidebar or tab view).
8. **Toolbar:** borderless monochrome SF Symbols in ≤3 groups (pro tools legitimately exceed), one trailing primary; every toolbar action also a menu-bar command.
9. **Forms:** right-aligned colon-terminated labels + left-aligned controls on one shared edge, flat on one opaque surface — not stacked labels, not iOS inset-grouped cards.
10. **Chrome truths:** coloured traffic lights = focused window (grey = inactive; settings windows dim minimize/zoom); alerts/sheets have no traffic lights; the default cursor is the arrow, not the pointer hand.

## 4. Geometry rules for measurement

- **Concentric corners:** child radius = parent radius − padding; capsule = height/2. Nested radii that don't step down concentrically are a construction defect worth naming.
- **Traffic-light inset is algorithmic, not fixed:** the left inset ≈ the top inset, both derived from titlebar height. Use the ratio to *infer the chrome archetype* (tall unified toolbar → large inset; compact strip → small). If the window top is cropped, record the archetype as missing data — don't invent it.
- **Window corner radius is fragmented** across frameworks in the macOS 26 era (~16pt is only a secondary-source approximation) — always record the *observed* radius per app; never assume a constant. This is also why the kit JSON carries none.
- **Semantics before pixels:** before measuring, name what each region *is* (toolbar / source list / content table / inspector / sheet) in platform vocabulary. It prevents web-vocabulary drift ("nav bar", "card grid") from contaminating profiles, and mis-identified regions produce mis-attributed tokens.

**Hard HIG numbers** (Apple-stated; everything else is adaptive): 4.5:1 / 3:1 contrast · ≤3 alert buttons · 1pt split dividers · 15/11pt scrollbars · ≤3 toolbar groups · ≤5–7 segments · 1-level submenus · 8pt grid, 4pt subdivisions · 13pt body (recommended default; 10pt the stated minimum) · 1024px icon canvas.

**Two numbers that look hard and are not**, both scoped here because reading them as macOS constants produces a wrong digest:

- **44×44pt hit targets** is the *touch* figure. On the desktop, visible controls sit on the 20–28pt ladder with padded hit areas, and the floor that binds is WCAG's 24px; 44pt binds only touch-adjacent or dual-platform work. Recording a 24pt mac button as a Target Starvation defect against a 44pt bar is the error this scoping prevents.
- **Control heights are not published as a table.** Apple states control sizes semantically — mini / small / regular-medium / large / extra large — and tells developers not to hard-code heights; mini through medium grew taller in macOS 26. So the 20–28pt ladder above is *observed and kit-derived*, and a height read off a kit is `(specified)` for that kit revision rather than a platform constant. Record the kit version beside it (see `evidence.md` §2).

## 5. Native-tells audit (supplementary rubric for macOS surfaces)

Run alongside the 14-point rubric on every macOS UI screenshot; score pass/fail/n-a with evidence:

1. Lineage reads AppKit-native (or macOS-correct SwiftUI)?
2. Glass only on floating chrome; content opaque; no glass-on-glass?
3. Selection grammar: inset rounded fill, accent text/glyph?
4. Sidebar headers sentence/title case, system font?
5. Density: 13pt-class body, 20–28pt controls, desktop row heights?
6. Accent bound consistently (selection + focus + primary action one hue; identity colours separate)?
7. One prominent action per view; dialog button grammar correct?
8. Concentric corners; radii step down child < parent?
9. Toolbar: borderless symbols, grouped, single primary?
10. Real chrome: genuine traffic lights, no faked frame, focus states consistent?

For *generated* mocks these ten are mandatory passes except where the target cluster deliberately deviates (record which and why).

## 6. Deeper sources (macosify plugin, when installed)

At `plugins/macosify/` in the same marketplace (paths relative to its plugin root):
- `reference/hig/` — 37-file HIG library with per-component "common non-native mistakes"; `index.md` maps components to files. Read the matching file when digesting an unfamiliar surface type.
- `reference/DESIGN.md` — token-level native system (916 lines) incl. material ramp, motion tokens, and the full native-feel checklist.
- `learnings/macos-ui-learnings.md` — the accumulating evidence file behind §3 (with per-rule confidence, origins, sightings, and open conflicts — e.g. System Settings' disputed lineage). Treat as a sibling corpus: high-confidence entries there corroborate like a digested app; don't write to it from this skill.
- `reference/macos-26-ui-analysis-framework.md` — AX-tree extraction schema and SwiftUI/AppKit element mappings, useful when a digest must feed native code generation.

These complement but never override this skill's provenance ladder: user's observed evidence → official kit `(specified)` → HIG → these references.
