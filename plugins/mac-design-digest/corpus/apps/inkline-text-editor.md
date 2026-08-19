# Inkline Text Editor — profile

- **Source:** macapp.supply (Mac App Store, `id6764860305`, category Dev, paid) · **Surfaces digested:** main editor (single), main editor (expanded file tree), split editor, editor + Git panel, editor + Terminal panel, Settings window — all dark · **Last updated:** 2026-07-19
- **One-sentence identity:** Zed's dark editor idiom (Dracula-family graphite, activity-view sidebar, bottom terminal/git drawer) rebuilt inside a genuinely native macOS shell — real proxy-icon titlebar and SF Pro/SF Mono, but a fixed brand-violet accent instead of the system's; think "Zed's clothes on AppKit bones," a native-shipped cousin of VS Code and Panic's Nova.
- **Cluster:** unassigned — proposed `developer-dark-ide` (see cluster_hint in observations JSON)
- **Lineage:** native (med confidence) — chrome is unambiguously AppKit (genuine traffic lights, centred NSWindow proxy-icon + POSIX-path title, native pop-up buttons with double chevrons, SF Pro UI confirmed by Settings' "UI font family: System"). No Electron tells (no tracked-uppercase headers, no kebab menus, no hand cursor). BUT the entire interior — tab bar, sidebar activity switcher, bottom drawer — is custom-drawn in the cross-platform-editor idiom, so AppKit-vs-native-shell-around-a-web-editor cannot be fully separated from stills. Interior editor-idiom departures are recorded as tells, not learned as mac canon.
- **Era (chrome):** custom (dark-only graphite, Dracula-family) — **not** Liquid Glass. Surfaces are opaque graphite with a cool blue-violet tint; no lensing/vibrancy/scroll-edge evidence. Borrows Big Sur+ rounded geometry (pill tabs, capsule primary buttons) without the material layer.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/editor-canvas | `#282934` | (measured)(confirmed) | darkest surface; editor content; cool graphite, blue-violet tint (B>R,G) |
| bg/sidebar+panel | `#37383F` | (measured)(confirmed) | file-tree sidebar + bottom panels; one step lighter than canvas |
| bg/titlebar+toolbar | `~#393B45` | (measured)(confirmed) | chrome band is the lightest graphite → inverted-from-native depth (chrome brighter than content) |
| bg/status-bar | `~#38373E` | (measured)(confirmed) | full-width bottom bar |
| bg/settings-window | `#24252C` | (measured)(inferred) | Settings is a separate window, base surface |
| bg/settings-card | `#363841` | (measured)(inferred) | grouped outlined section boxes (Profiles / Typography / Themes) |
| bg/terminal+theme-card | `~#0B0A0E` | (measured)(inferred) | embedded terminal + theme-preview cards are near-black, darker than canvas |
| accent/primary (brand violet) | `~#8B7CC8–#9280D0` | (estimated)(confirmed) | primary buttons, search focus ring, active-tab + selected-theme-card border, markdown `#` heading. A **fixed brand hue, not `controlAccentColor`** |
| text/primary | `~#E8E8EC` near-white | (estimated)(confirmed) | body/UI text, active file name (bold) |
| text/secondary | `~#6B6E86` muted lavender-grey | (estimated)(confirmed) | line-number gutter, status-bar metadata, settings descriptions |
| type/ui-body | 13pt SF Pro (System) | (estimated)(confirmed) | Settings confirms "UI font family: System"; native macOS 13pt body |
| type/ui-section-title | `~17pt` SF Pro Semibold | (estimated)(inferred) | Settings section headers (Title2-class) |
| type/editor-mono | `~13pt` SF Mono-class, lh `~18–19pt` (~1.45×) | (estimated)(confirmed) | code buffer |
| type/status-bar | `~11pt` (Subheadline-class) | (estimated)(confirmed) | "4 lines · 191 chars" / "Markdown · UTF-8 · LF · Ln 1, Col 1" |
| chrome/sidebar-width | `~300pt` | (estimated)(confirmed) | wider than kit's 256pt example — deviation, see Defects |
| row/file-tree | `~24pt` (kit Small tier) | (estimated)(confirmed) | icon↔label gap ~6–7pt |
| row/settings-nav | `~32pt` (kit Medium tier) | (estimated)(inferred) | 10 icon+label destinations |
| chrome/titlebar+tab band | `~80pt` total (titlebar ~36 + tab row ~44) | (estimated)(confirmed) | reads like an expanded-toolbar height (kit expanded = 77pt) |
| radius/tab-pill | `~7–9pt` | (estimated)(confirmed) | browser-style closable document tabs |
| radius/settings-card | `~10–12pt` | (estimated)(inferred) | outlined section boxes |
| radius/primary-button | capsule / large | (estimated)(inferred) | Save Profile, Import Font — pill-ish |
| chrome/traffic-lights | standard 68×14 cluster, ~14pt inset | (measured)(confirmed) | genuine — a strong native tell |
| syntax/palette | keyword magenta-pink · type green · identifier blue · string yellow · muted grey punctuation, on `#282934` | (estimated)(confirmed) | Dracula-family; default theme literally named "Dracula Solid" |

## Layout skeletons

**Main editor window (shots 1, 2)** — three-zone native window:
1. Native titlebar (~36pt): traffic lights leading; centred document proxy-icon + `File.ext – /abs/path`; a sidebar-toggle glyph far trailing.
2. Toolbar band (~44pt): over the sidebar, a rounded segmented view-switcher (folder = Explorer active, git-branch = Source Control); in the content region a `+` new-tab button, then browser-style closable document tabs (circled ✕ + label, active tab a lighter raised pill); trailing borderless monochrome group — back/forward chevrons, search magnifier, an "A|" (font/appearance) glyph, a sliders (editor-settings) glyph.
3. Body: source-list sidebar (~300pt) holding a flat file tree — blue folder glyphs (disclosure chevrons), full-colour language file-type icons (php, C, C++, Go, Kotlin, Rust, C#, Java, Swift, JS, TS, CSS, npm, toml, md); right, the editor pane — muted-lavender line-number gutter + SF Mono buffer.
4. Full-width status bar (~30pt): left doc metrics; right language · encoding · line-ending · caret position, each in a subtle capsule.

**Split editor (shot 3)** — the editor pane divides into two side-by-side buffers, **each with its own independent tab strip**; shared sidebar and status bar. Trailing toolbar controls collapse to the left pane's strip.

**Bottom drawer (shots 4, 5)** — a panel slides up across the bottom of the editor stack (editor panes shrink above it). Header row: leading `<` collapse chevron, a segmented mode-switcher (terminal / git-branch / debug-bug), a mode label ("Git" / "Terminal · Running 95876"), then mode content controls. Git mode: text tabs Changes | History | Branches | Stashes (Changes active = subtle inset pill fill), trailing refresh + close; body "No repository / No changes". Terminal mode: trailing action cluster (+, ✕, split, trash, refresh, stop) + close ✕; body a near-black terminal with a monospace prompt.

**Settings (shot 6)** — separate window, no toolbar, inline left-aligned "Settings" title. Left nav sidebar (~its own column): a search field ("Search settings", violet focus ring) then 10 SF-Symbol + label destinations (General, Privacy, Appearance, Languages, Toolchains, Extensions, Debug, Editor, Shortcuts, Advanced) at ~32pt rows. Right: a scroll of grouped **outlined section-cards** (Profiles, Interface Typography, Themes), each = Title2 header + secondary description + controls (native pop-up buttons with double chevrons, `Import Font…`, one filled-violet primary `Save Profile` with quiet/disabled `Delete`/`Apply` siblings). Themes renders a card grid (Dracula Solid selected w/ violet border, Ayu Dark) each with a "Dark" capsule badge + a 4-chip swatch row.

## Signature moves
- **[GOLDEN-NUGGET] Zed idiom on native bones.** The Themes pane literally says "Zed-compatible themes drive the editor colors" and credits "Zed and the extension/theme maintainers." The whole product ports Zed/VS-Code's dark-editor grammar — activity-view sidebar switcher, closable browser tabs, bottom terminal/git/debug drawer, per-file-type colour icons — into a genuinely native macOS window. This is the app's entire character in one decision: familiar dev-tool muscle memory (Jakob's Law) delivered as a real Mac citizen.
- **[GOLDEN-NUGGET] Fixed brand-violet accent.** `~#8B7CC8` binds primary buttons, focus rings, the active document tab, the selected theme card, and markdown headings — internally rigorous, but it overrides the user's system accent (native rule: accent is the user's, not the app's). Systematic + purposeful (brand cohesion) → signature; the native cost is logged as a tell.
- **Inverted-depth graphite.** Chrome (`~#393B45`) is *lighter* than the editor canvas (`#282934`), which is lighter than the terminal/theme cards (`~#0B0A0E`). Depth is a three-step tonal stack (not shadow, not glass) with the darkest layer as the innermost content — the reverse of native's "content brighter than chrome" instinct, but a coherent editor convention.
- **Per-language file-type iconography.** A full colour glyph set (shot 2) — a craft touch that most native file browsers (which use monochrome Finder-style icons) skip.

## Defects
- **Contrast Dilution (structural).** Tab-bar edges, editor-pane outlines, and Settings-card borders sit well under 3:1 against the graphite ground — grouping survives mostly by fill-step, not by visible edge. → native-tells #10 / rubric #10. Canon fix: dark separators drawn from the Fills tiers to reach ~3:1.
- **Selection grammar deviation (native tell #3).** The sidebar's active file is shown by **bold near-white weight only — no inset rounded accent fill, no accent-tinted glyph.** Defensible as a "current document" (Zed) indicator, but native list/sidebar selection expects a subtle inset rounded fill. Excluded from macOS canon.
- **Accent not bound to system accent (native tell #6).** Fixed brand violet rather than `controlAccentColor`; consistent but non-native. Signature-with-a-cost.
- **Sidebar wider than kit (~300pt vs 256pt example)** and holds only navigation (correct) — a size deviation to record, not a fault.
- **Line Length Fatigue (soft).** README prose renders full editor width (>100ch) and Settings card descriptions run ~100ch. Editor prose is user content (N/A-ish); the Settings descriptions are the app's own layout and could cap ~65–75ch.
- **Terminal-panel trailing toolbar** packs ~6–7 icon actions into one tight cluster — dense (borderline crowding), though monochrome icons keep it from Focal Collision.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main editor (shot 1) | 12/14 | #10 sub-3:1 structural borders; #6 prose measure (editor content, soft/na) |
| main editor, file tree (shot 2) | 12/14 | #10 borders; adds file-type-icon evidence |
| split editor (shot 3) | 12/14 | #10 borders; per-pane tab strips both low-contrast |
| editor + Git panel (shot 4) | 12/14 | #10 borders; panel header divider barely visible |
| editor + Terminal panel (shot 5) | 11/14 | #10 borders; #8/#11 dense trailing icon cluster in panel header |
| Settings (shot 6) | 13/14 | #6 card-description measure ~100ch |

Native-tells audit (10-pt): editor surfaces ~7/10 (fail #3 selection grammar, #6 accent binding; #2/#8/#9/#10 pass); Settings ~9/10 (fail #6 accent binding; exemplary dialog grammar — one filled primary, quiet/disabled siblings).
