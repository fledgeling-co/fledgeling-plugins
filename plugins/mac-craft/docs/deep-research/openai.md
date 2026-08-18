---
title: "macOS 26 and 27 HTML Mockup Semantic Standards and Deterministic Validation"
run_id: dr_7a00e7598e33e9c1
question: "macOS application interface design conventions as of August 2026: what the current macOS design language (the \"Liquid Glass\" / Tahoe-era system from macOS 26 onward) specifies for application chrome — window and titlebar structure, unified toolbars, sidebars and split views, translucency/material layers, control metrics and the type ramp, accent-colour and selection semantics, dark-mode authoring, concentric corner radii, scroll-edge effects, and the reduced-transparency / increased-contrast / reduced-motion accessibility variants. Second, the diagnostic differences between a native macOS interface and a web or iOS interface rendered on the desktop: which affordances (cursor behaviour, hit-target sizing, hover semantics, text casing, focus rings, keyboard-first navigation, menu-bar command completeness, context menus, drag and drop, window state restoration) users and reviewers read as \"not a real Mac app\", and what published evidence exists on desktop-specific usability expectations distinct from mobile and web. Third, automated deterministic verification of desktop UI mockups authored as HTML: what can be checked programmatically without a full browser engine (WCAG contrast computed from declared colours, focus-visible and ARIA/role presence, token-versus-literal colour discipline, control-height conformance, layout-overflow and text-truncation detection), which open-source linters and accessibility engines (axe-core, Pa11y, Lighthouse, Deque, IBM Equal Access, contrast algorithms including APCA versus WCAG 2.x) support headless or DOM-free static analysis, and what published guidance says about false-pass risk in self-reported design audits."
provider: openai
model: gpt-5.6-terra
tier: fast
archetype: technical
sources: 85
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 3.50
completed: 2026-08-18T01:36:32.837Z
---
## Executive Summary

- **(High Confidence)** **Adopt a “native structure, not pixel imitation” policy for macOS 26 Tahoe and macOS 27 Golden Gate.** Use the platform’s window frame/titlebar, integrated toolbar, sidebar/split-view, semantic colors, standard materials, and system controls as the implementation target; mockups should represent those semantic layers rather than prescribe fixed translucent RGBA values or fixed corner radii. Liquid Glass is adaptive to content, appearance, user material preference, and accessibility settings, so a static HTML blur is not a faithful specification. [Apple HIG, Materials](https://developer.apple.com/design/human-interface-guidelines/materials/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/materials?utm_source=openai))

- **(High Confidence)** **Use macOS-specific metrics, not iOS touch metrics.** Apple’s published accessibility target is a default macOS control size of **28×28 pt** and a minimum of **20×20 pt**, compared with iOS/iPadOS’s **44×44 pt** default and **28×28 pt** minimum. macOS body text is **13 pt / 16 pt line height**, with a published minimum text size of **10 pt**. These are Apple-specified guidance values, not measurements from screenshots. [Apple HIG, Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/accessibility?utm_source=openai)) [Apple HIG, Typography](https://developer.apple.com/design/human-interface-guidelines/typography/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/typography?changes=_5&utm_source=openai))

- **(High Confidence)** **The most reliable “not a real Mac app” tells are behavioural, not visual:** an app with no complete menu-bar command set, weak keyboard navigation, missing context menus, browser-style cursor treatment, touch-sized controls, mobile-density layouts, no drag-and-drop affordances, or no restoration of window/work state violates explicit Apple macOS guidance. The evidence is strongest for these platform expectations; there is little direct empirical literature proving that a particular visual defect alone causes reviewers to label an app “web-like.” [Apple HIG, Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos?changes=l_8_2&utm_source=openai))

- **(High Confidence)** **Do not accept a mockup’s self-reported “PASS.”** A no-browser deterministic gate can reliably fail declared opaque foreground/background pairs below WCAG 2.2 thresholds, including the observed **1.00:1** failure case; it can also enforce token discipline, required roles/names, focus-visible declarations, explicit control dimensions, and a restricted geometry contract. It must return **INDETERMINATE/FAIL**, never PASS, for transparency, gradients, images, backdrop filters, inherited opacity, arbitrary CSS layout, or dynamic content that prevents exact computation. WCAG requires at least **4.5:1** for normal text and **3:1** for large text; values must not be rounded upward. [W3C, Understanding SC 1.4.3 Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum) ([w3.org](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum?utm_source=openai))

- **(High Confidence)** **axe-core, Pa11y, Lighthouse, and IBM Equal Access are supplements to—not replacements for—the static gate.** axe-core requires a rendered DOM and its `color-contrast` rule is known not to work in JSDOM; Pa11y runs Headless Chrome; Lighthouse uses Chrome; IBM Equal Access supports Node builds but still works with parsing/browser engines. They belong in a second, rendered-browser verification stage. [Deque axe-core repository](https://github.com/dequelabs/axe-core) ([github.com](https://github.com/dequelabs/axe-core?utm_source=openai)) [Pa11y repository](https://github.com/pa11y/pa11y) ([github.com](https://github.com/pa11y/pa11y?utm_source=openai)) [IBM Equal Access repository](https://github.com/IBMa/equal-access) ([github.com](https://github.com/ibma/equal-access?utm_source=openai))

- **(Medium Confidence)** **Treat macOS 27 guidance as beta-era guidance on August 18, 2026.** Apple’s current documentation identifies macOS Golden Gate 27 as beta. Its refinements include edge-extending sidebars, semi-bold sidebar selection, tighter window radii, updated scroll-edge behavior, optional interactive glass response, and a public concentric-corner API. Build the mockup profile around these behaviours, but version it as `macos-27-beta` until the shipping HIG/release notes stabilize. [Apple, macOS Release Notes](https://developer.apple.com/documentation/macos-release-notes) ([developer.apple.com](https://developer.apple.com/documentation/macos-release-notes?utm_source=openai)) [Apple WWDC26, Modernize your AppKit app](https://developer.apple.com/videos/play/wwdc2026/289/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/289/?utm_source=openai))

- **(High Confidence)** **Recommended decision:** ship a two-stage quality gate: (1) a deterministic, DOM-free “mock contract” linter that has authority to fail release candidates; and (2) a browser/AppKit validation suite that is required before implementation sign-off but is explicitly labelled as supplemental. <INFERENCE from="[Apple’s adaptive-material guidance; W3C’s statement that tools cannot determine conformance; axe-core’s JSDOM contrast limitation]">A restricted static contract is the only way to make contrast and geometry failures deterministic without trusting a browser engine or an author’s PASS field.</INFERENCE> [Apple HIG, Materials](https://developer.apple.com/design/human-interface-guidelines/materials/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/materials?utm_source=openai)) [W3C, Evaluating Web Accessibility](https://www.w3.org/WAI/test-evaluate/) ([w3.org](https://www.w3.org/WAI/test-evaluate/?utm_source=openai)) [Deque axe-core repository](https://github.com/dequelabs/axe-core) ([github.com](https://github.com/dequelabs/axe-core?utm_source=openai))

## Detailed Findings

### 1. What are the macOS 26/27 interface conventions, the native-vs-web diagnostics, and the deterministic verification approach for HTML mockups?

### 1.1 Decision standard for the mockup skill

**Finding — High Confidence.** The skill should author HTML as a **semantic implementation brief for SwiftUI/AppKit**, not as a visual clone of macOS. The deliverable should contain:

1. `mockup.html` — self-contained visual reference.
2. `tokens.json` — semantic design token table.
3. `states.json` — state and accessibility matrix.
4. `mock-contract.json` — deterministic geometry, contrast, and role assertions that the gate independently recalculates.
5. `gate-report.json` — machine-generated failures, warnings, and indeterminate results; authors may not write this file.

Apple’s current guidance is to let standard framework components automatically acquire Liquid Glass and related system updates; custom backgrounds and custom glass should be limited because the material is contextual and adaptive. [Apple HIG, Materials](https://developer.apple.com/design/human-interface-guidelines/materials/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/materials?utm_source=openai)) [Apple WWDC25, Build a SwiftUI app with the new design](https://developer.apple.com/videos/play/wwdc2025/323/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/323/?utm_source=openai))

#### Application-chrome convention table

| Area | Current convention | Mockup specification rule | Confidence |
|---|---|---|---|
| Window frame and titlebar | A macOS window has a frame and body; the frame can contain window controls and a toolbar. People move windows by dragging the frame and commonly resize from edges. Key, main, and inactive windows have distinct appearances. [Apple HIG, Windows](https://developer.apple.com/design/human-interface-guidelines/windows) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/windows?utm_source=openai)) | Represent the titlebar/frame as a separate semantic layer: `windowFrame`, `titlebar`, `toolbar`, and `content`. Include active and inactive window states. Do not hard-code traffic-light colors. | High |
| Window title | Provide a useful, concise content/location title; Apple advises keeping it under **15 characters** where possible and not using the app name as the title. [Apple HIG, Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/toolbars?changes=_2&utm_source=openai)) | Require `window.titlePurpose` and `window.title`. Flag an app-name-only title. | High |
| Unified toolbar | On macOS, the toolbar lives in the top window frame, either below or integrated with the titlebar. Toolbar items are not the sole command location because people can hide or customize toolbars. [Apple HIG, Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/toolbars?changes=_2&utm_source=openai)) | Require every toolbar command to map to a menu-bar command ID in `states.json`. Do not depict a web-app header as the only command surface. | High |
| Tahoe Liquid Glass toolbar | macOS 26 moves toolbar items onto floating Liquid Glass surfaces, groups related items, and adds a scroll-edge effect to retain legibility as content passes underneath. [Apple WWDC25, Build a SwiftUI app with the new design](https://developer.apple.com/videos/play/wwdc2025/323/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/323/?utm_source=openai)) | Specify `material: functional-glass` rather than an arbitrary CSS `backdrop-filter`. Require group boundaries and primary-action tint semantics. | High |
| macOS 27 toolbar refinement | In macOS 27 beta, automatic `NSScrollEdgeEffectStyle` resolves to a hard edge when free-floating title text is present; bordered toolbar items over a sidebar adopt Liquid Glass. [Apple WWDC26, Modernize your AppKit app](https://developer.apple.com/videos/play/wwdc2026/289/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/289/?utm_source=openai)) | Profile as `macos-27-beta`; require an explicit `scrollEdgeStyle: auto|hard|soft` token, not a fixed blur amount. | Medium |
| Sidebar and split view | Sidebars support top-level navigation; Apple recommends no more than two hierarchy levels in a sidebar and a split view with a content list for deeper hierarchies. [Apple HIG, Sidebars](https://developer.apple.com/design/human-interface-guidelines/sidebars/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/sidebars?changes=_11&utm_source=openai)) | Require `navigationDepth` metadata. Fail a sidebar tree deeper than two levels unless a middle list pane is declared. | High |
| Sidebar visual layer | In macOS 26, sidebars can float in the Liquid Glass functional layer and content can extend behind them. In macOS 27 beta, sidebars extend to window edges while content still flows behind them. [Apple HIG, Sidebars](https://developer.apple.com/design/human-interface-guidelines/sidebars/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/sidebars?changes=_11&utm_source=openai)) [Apple WWDC26 Platforms State of the Union](https://developer.apple.com/videos/play/wwdc2026/112/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/112/?time=173&utm_source=openai)) | Specify pane role and material separately: `sidebar`, `contentList`, `detail`, `inspector`; do not paint every pane as translucent glass. | High for macOS 26; Medium for macOS 27 beta |
| Materials | Liquid Glass is for the functional layer—controls and navigation—not the content layer. Apple says to use it sparingly and rely on standard materials inside content. [Apple HIG, Materials](https://developer.apple.com/design/human-interface-guidelines/materials/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/materials?utm_source=openai)) | Fail custom glass on ordinary cards, tables, documents, and list content unless marked as a transient interactive control. | High |
| Accent and selection | macOS supports a user-selected accent color affecting buttons, selection highlighting, and sidebar icons. If a person picks a non-multicolor system accent, it replaces the app accent except fixed-color semantic sidebar icons. [Apple HIG, Color](https://developer.apple.com/design/human-interface-guidelines/color/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/color?changes=_5_2&utm_source=openai)) | Use `accent`, `selectionActive`, `selectionInactive`, and `destructive` semantic tokens. Never make selection depend solely on an app-brand hex code. | High |
| Selection semantics | Focused list items use white text over an accent-colored highlight; unfocused selected items use standard text over a gray highlight. macOS 27 beta changes sidebar selection emphasis to semi-bold text. [Apple HIG, Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection/?utm_source=openai)) [Apple WWDC26, Modernize your AppKit app](https://developer.apple.com/videos/play/wwdc2026/289/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/289/?utm_source=openai)) | Model `selectedActiveWindow` and `selectedInactiveWindow` separately. Do not reuse hover styling as selection. | High for baseline; Medium for macOS 27 beta |
| Dark mode | Apple says people expect applications to follow the system appearance; use semantic adaptive colors and supply light, dark, and increased-contrast variants for custom colors. Apple advises against hard-coded color values. [Apple HIG, Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/dark-mode?utm_source=openai)) [Apple HIG, Color](https://developer.apple.com/design/human-interface-guidelines/color/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/color?changes=l_8&utm_source=openai)) | Require a complete light/dark/high-contrast token map. Fail literals in component CSS except inside the token-definition block. | High |
| Concentric corner radii | Apple’s current geometry API computes a corner radius as the container radius minus the distance from the view corner to the container corner. macOS 27 adds AppKit support for container-concentric corners. [Apple Developer Documentation, `concentricCornerRadii(in:)`](https://developer.apple.com/documentation/swiftui/geometryproxy/concentriccornerradii%28in%3A%29) ([developer.apple.com](https://developer.apple.com/documentation/swiftui/geometryproxy/concentriccornerradii%28in%3A%29?changes=lat_3_5&utm_source=openai)) [Apple WWDC26, Modernize your AppKit app](https://developer.apple.com/videos/play/wwdc2026/289/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/289/?utm_source=openai)) | Do not prescribe a universal `12px` or `16px` radius. Specify `cornerRelationship: containerConcentric` or `independent`. | High |
| Scroll-edge effect | Apple recommends one scroll-edge effect per view; in split views, panes can each have one but should use consistent heights. [Apple WWDC25, Get to know the new design system](https://developer.apple.com/videos/play/wwdc2025/356/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/356/?time=0&utm_source=openai)) | Add a `scrollEdge` object per scrollable pane and reject two stacked effects in one pane. | High |

### 1.2 Published metrics and type ramp

**Finding — High Confidence.** Apple publishes a macOS type ramp and general minimum/default target sizes. It does **not** publish one universal numeric height/radius table for every Tahoe or Golden Gate control. Therefore, use published typographic and accessibility values as enforceable mockup constraints; use semantic control-size names and framework components for detailed AppKit/SwiftUI geometry.

| Parameter | Published value | Source status | Gate implication |
|---|---:|---|---|
| macOS default control size | **28×28 pt** | Apple HIG accessibility recommendation. [Apple HIG, Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/accessibility?utm_source=openai)) | `default` interactive targets must be at least 28 pt in the mock contract. |
| macOS minimum control size | **20×20 pt** | Apple HIG accessibility recommendation. [Apple HIG, Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/accessibility?utm_source=openai)) | Hard fail below 20 pt unless explicitly noninteractive. |
| macOS default text size | **13 pt** | Apple HIG typography recommendation. [Apple HIG, Typography](https://developer.apple.com/design/human-interface-guidelines/typography/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/typography?changes=_5&utm_source=openai)) | Default body token must map to 13 pt/16 pt. |
| macOS minimum text size | **10 pt** | Apple HIG typography recommendation. [Apple HIG, Typography](https://developer.apple.com/design/human-interface-guidelines/typography/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/typography?changes=_5&utm_source=openai)) | Hard fail for meaningful text below 10 pt. |
| `Large Title` | Regular **26 pt**, **32 pt** line height | Apple HIG macOS built-in text style. [Apple HIG, Typography](https://developer.apple.com/design/human-interface-guidelines/typography/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/typography?changes=_5&utm_source=openai)) | Token: `type.largeTitle`. |
| `Title 1` | Regular **22 pt**, **26 pt** line height | Apple HIG macOS built-in text style. [Apple HIG, Typography](https://developer.apple.com/design/human-interface-guidelines/typography/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/typography?changes=_5&utm_source=openai)) | Token: `type.title1`. |
| `Title 2` | Regular **17 pt**, **22 pt** line height | Apple HIG macOS built-in text style. [Apple HIG, Typography](https://developer.apple.com/design/human-interface-guidelines/typography/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/typography?changes=_5&utm_source=openai)) | Token: `type.title2`. |
| `Title 3` | Regular **15 pt**, **20 pt** line height | Apple HIG macOS built-in text style. [Apple HIG, Typography](https://developer.apple.com/design/human-interface-guidelines/typography/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/typography?changes=_5&utm_source=openai)) | Token: `type.title3`. |
| `Headline` | Bold **13 pt**, **16 pt** line height | Apple HIG macOS built-in text style. [Apple HIG, Typography](https://developer.apple.com/design/human-interface-guidelines/typography/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/typography?changes=_5&utm_source=openai)) | Token: `type.headline`. |
| `Body` | Regular **13 pt**, **16 pt** line height | Apple HIG macOS built-in text style. [Apple HIG, Typography](https://developer.apple.com/design/human-interface-guidelines/typography/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/typography?changes=_5&utm_source=openai)) | Token: `type.body`. |
| `Callout` | Regular **12 pt**, **15 pt** line height | Apple HIG macOS built-in text style. [Apple HIG, Typography](https://developer.apple.com/design/human-interface-guidelines/typography/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/typography?changes=_5&utm_source=openai)) | Token: `type.callout`. |
| `Subheadline` | Regular **11 pt**, **14 pt** line height | Apple HIG macOS built-in text style. [Apple HIG, Typography](https://developer.apple.com/design/human-interface-guidelines/typography/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/typography?changes=_5&utm_source=openai)) | Token: `type.subheadline`. |
| `Footnote` / captions | **10 pt**, **13 pt** line height | Apple HIG macOS built-in text styles. [Apple HIG, Typography](https://developer.apple.com/design/human-interface-guidelines/typography/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/typography?changes=_5&utm_source=openai)) | Token: `type.footnote`, `type.caption`. |

**Control-height boundary.** Apple stated that most macOS controls became “slightly taller” under the macOS 26 design, but did not publish a general numeric replacement height in the cited WWDC session. [Apple WWDC25, Build a SwiftUI app with the new design](https://developer.apple.com/videos/play/wwdc2025/323/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/323/?utm_source=openai)) <MISSING_DATA>[A complete public Apple table mapping every macOS 26/27 standard control size to exact point heights was sought; no authoritative universal table was found. The needed artifact would be an Apple-published control specification or inspectable platform UI kit.]</MISSING_DATA>

### 1.3 State matrix for HTML mockups and SwiftUI/AppKit handoff

| Component/state | HTML mockup semantic token requirement | SwiftUI/AppKit implementation expectation | Evidence / confidence |
|---|---|---|---|
| Window: key | `window.active`, `titlebar.active`, `control.active` | System-provided window appearance; titlebar controls use active coloration. | Apple distinguishes key, main, and inactive window appearance. [Apple HIG, Windows](https://developer.apple.com/design/human-interface-guidelines/windows) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/windows?utm_source=openai)) **High** |
| Window: inactive | `window.inactive`, `text.inactive`, `selection.inactive` | Reduce vibrancy and use system inactive appearance; do not merely lower all opacity. | Inactive windows do not use vibrancy and appear subdued. [Apple HIG, Windows](https://developer.apple.com/design/human-interface-guidelines/windows) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/windows?utm_source=openai)) **High** |
| Sidebar row: selected, key window | `selection.active.bg`, `selection.active.fg`, `fontWeight.selected` | Accent highlight with readable selected text; macOS 27 sidebar selection adds semi-bold emphasis. | Apple describes accent/white focused selection; WWDC26 describes semi-bold sidebar selection. [Apple HIG, Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection/?utm_source=openai)) [Apple WWDC26, Modernize your AppKit app](https://developer.apple.com/videos/play/wwdc2026/289/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/289/?utm_source=openai)) **Medium for 27 beta** |
| Sidebar row: selected, inactive window | `selection.inactive.bg`, `selection.inactive.fg` | Gray inactive selection; retain selection identity. | Apple distinguishes unfocused selection from focused selection. [Apple HIG, Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection/?utm_source=openai)) **High** |
| Button: default / hover / pressed | `control.default`, `control.hover`, `control.pressed` | Mouse hover feedback, tooltip where icon-only or unclear, standard press state. | macOS displays tooltips after hovering over a button; AppKit supports pointer tracking. [Apple HIG, Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/buttons?changes=latest_1__8&utm_source=openai)) [Apple Developer Documentation, `NSTrackingArea`](https://developer.apple.com/documentation/appkit/nstrackingarea) ([developer.apple.com](https://developer.apple.com/documentation/appkit/nstrackingarea?changes=_7&utm_source=openai)) **High** |
| Keyboard focus | `focus.ring`, `focus.visible` | Full Keyboard Access must reach controls and menus; use native focus behaviour wherever possible. | Apple asks developers to support Full Keyboard Access and standard shortcuts. [Apple HIG, Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/keyboards/?utm_source=openai)) **High** |
| Disabled / unavailable | `control.disabled`, `menu.unavailable` | Preserve readable distinction; menu commands can appear dimmed where unavailable. | Apple menu guidance distinguishes unavailable commands. [Apple HIG, Menus](https://developer.apple.com/design/human-interface-guidelines/menus) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/menus?utm_source=openai)) **High** |
| Reduced Transparency | `material.reducedTransparency` must be opaque | Avoid semitransparent window and component backgrounds. | Apple explicitly directs opaque backgrounds when Reduce Transparency is enabled. [Apple Developer Documentation, `accessibilityReduceTransparency`](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducetransparency) ([developer.apple.com](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducetransparency?changes=_2&utm_source=openai)) **High** |
| Increased Contrast | `contrast.increased` token set | Use stronger differentiation, bolder lines, and increased-contrast semantic colors. | AppKit says to present a high-contrast UI; SwiftUI exposes `ColorSchemeContrast`. [Apple Developer Documentation, `accessibilityDisplayShouldIncreaseContrast`](https://developer.apple.com/documentation/appkit/nsworkspace/accessibilitydisplayshouldincreasecontrast) ([developer.apple.com](https://developer.apple.com/documentation/appkit/nsworkspace/accessibilitydisplayshouldincreasecontrast?changes=_2___8_8&language=objc&utm_source=openai)) [Apple Developer Documentation, `ColorSchemeContrast`](https://developer.apple.com/documentation/swiftui/colorschemecontrast) ([developer.apple.com](https://developer.apple.com/documentation/swiftui/colorschemecontrast?utm_source=openai)) **High** |
| Reduced Motion | `motion.reduced` | Replace large depth, scale, blur, bounce, and multi-axis transitions with subdued fades/highlights when motion conveys meaning. | Apple says Reduce Motion should avoid large animations, especially simulated 3D, and gives implementation guidance. [Apple Developer Documentation, `accessibilityReduceMotion`](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducemotion) ([developer.apple.com](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducemotion?changes=_3&utm_source=openai)) [Apple App Store Connect, Reduced Motion evaluation criteria](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/reduced-motion-evaluation-criteria) ([developer.apple.com](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/reduced-motion-evaluation-criteria?utm_source=openai)) **High** |
| Show Borders / increased contrast on macOS 27 | `accessibility.showBorders` | Add clear boundaries for custom controls where the environment indicates it. | macOS 27 adds the show-borders environment value according to Apple’s WWDC26 session. [Apple WWDC26 Platforms State of the Union](https://developer.apple.com/videos/play/wwdc2026/112/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/112/?time=173&utm_source=openai)) **Medium; beta-era** |

### 1.4 Native macOS versus web/iOS-on-desktop diagnostic list

**Finding — High Confidence for platform expectations; Medium Confidence for the “reviewer perception” conclusion.** Apple’s HIG establishes the behaviours below as macOS conventions. It does not provide a controlled study proving that each individual omission makes reviewers call an interface “web-like.” The diagnostic conclusion is therefore an inference, not a measured causal result.

| Diagnostic | Native macOS expectation | “Web/iOS-on-desktop” tell | Evidence strength |
|---|---|---|---|
| Cursor behaviour | macOS provides standard arrow, closed-hand, contextual-menu, copy, drag-link, and operation-not-allowed pointers. Contextual-menu cursor usage is associated with Control-click. [Apple HIG, Pointing devices](https://developer.apple.com/design/human-interface-guidelines/pointing-devices/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/pointing-devices?changes=_1&utm_source=openai)) | Universal hand cursor, no operation cursor during drag/drop, or no cursor state change for resizable/drag targets. <INFERENCE from="[Apple pointer taxonomy]">Indiscriminate browser-style `cursor:pointer` is inconsistent with a platform where the arrow is the standard interaction pointer.</INFERENCE> | High for expectation; Medium for perception |
| Hit-target sizing | macOS default **28×28 pt**, minimum **20×20 pt**; iOS default **44×44 pt**, minimum **28×28 pt**. [Apple HIG, Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/accessibility?utm_source=openai)) | Uniform 44 pt mobile targets and excessive vertical whitespace in dense desktop inspectors/tables; conversely, sub-20 pt controls are inaccessible. | High |
| Hover semantics | macOS shows a tooltip after a moment of hover over buttons; AppKit supports entered/exited/moved/cursor-update tracking. [Apple HIG, Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/buttons?changes=latest_1__8&utm_source=openai)) [Apple Developer Documentation, `NSTrackingArea`](https://developer.apple.com/documentation/appkit/nstrackingarea) ([developer.apple.com](https://developer.apple.com/documentation/appkit/nstrackingarea?changes=_7&utm_source=openai)) | No hover feedback, tooltip-free icon-only toolbar controls, or hover used as the only way to reveal a required action. | High |
| Text casing | Apple generally uses title-style capitalization for menu labels and recommends consistent capitalization across UI element types. [Apple HIG, Menus](https://developer.apple.com/design/human-interface-guidelines/menus) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/menus?utm_source=openai)) [Apple HIG, Writing](https://developer.apple.com/design/human-interface-guidelines/writing/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/writing?changes=l_1&utm_source=openai)) | All-caps controls, inconsistent sentence/title casing, or web-marketing language in menus. | High |
| Focus rings and keyboard-first operation | Full Keyboard Access can navigate and activate windows, menus, controls, and drag/drop; standard keyboard shortcuts should be respected. [Apple HIG, Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/keyboards/?utm_source=openai)) | Mouse-only mock flows, no visible focus state, tab stops not represented, or shortcut collisions. | High |
| Menu-bar command completeness | Menu-bar menus in macOS contain all commands; every toolbar item should also be available as a menu command. [Apple HIG, Menus](https://developer.apple.com/design/human-interface-guidelines/menus) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/menus?utm_source=openai)) [Apple HIG, Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/toolbars?changes=_2&utm_source=openai)) | Toolbar-only actions, a hamburger menu replacing the menu bar, or no `File`, `Edit`, `View`, `Window`, and app-command mapping where applicable. | High |
| Context menus | Secondary click or Control-click reveals relevant contextual actions; context-menu commands must also exist in the main interface/menu bar. [Apple HIG, Context menus](https://developer.apple.com/design/human-interface-guidelines/context-menus/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/context-menus?changes=__3&utm_source=openai)) | No right-click/secondary-click affordance for selected objects, or hidden-only actions. | High |
| Drag and drop | Apple says people often try drag and drop broadly; macOS supports pointer, Full Keyboard Access, and VoiceOver drag/drop, including cross-app drag. [Apple HIG, Drag and drop](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop?utm_source=openai)) | No drag affordance in file/list/canvas workflows, modal “move” flows for directly manipulable content, or no alternate command path. | High |
| Window management | macOS users commonly run multiple apps and windows, moving, resizing, minimizing, and switching among them. [Apple HIG, Windows](https://developer.apple.com/design/human-interface-guidelines/windows) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/windows?utm_source=openai)) | Fixed mobile-card layouts, no resize strategy, or content that assumes one maximized viewport. | High |
| State restoration | Apple says to restore previous state, including scroll position and windows’ prior state and location. [Apple HIG, Launching](https://developer.apple.com/design/human-interface-guidelines/launching/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/launching/?utm_source=openai)) | Relaunch begins at a generic home screen, discards documents/panes/selection, or forgets window arrangement. | High |
| Desktop density and precision | Apple calls out large displays, less nested modality, multiple apps, high-precision input, configurable windows, and customizable toolbars. [Apple HIG, Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos?changes=l_8_2&utm_source=openai)) | Phone-like stacked navigation, oversized cards, mandatory modal funnels, and lack of precision selection/editing. | High |

### 1.5 Deterministic HTML mockup gate without a browser engine

**Finding — High Confidence.** A no-browser gate can be deterministic only if the HTML mockup format is constrained. It cannot accurately evaluate arbitrary HTML/CSS because accurate painting depends on cascade, fonts, layout algorithms, transforms, clipping, z-order, device scale, image pixels, blending, and dynamic script. The correct architecture is a **restricted mock contract**, not an attempted reimplementation of Chromium/WebKit.

#### Required artifact structure

```text
mock/
  mockup.html
  tokens.json
  states.json
  mock-contract.json
  gate.config.json
  gate-report.json        # generated only; must not be committed as source-of-truth
```

#### Minimal contract example

```json
{
  "$schema": "https://example.invalid/mock-contract/v1",
  "profile": "macos-27-beta",
  "canvas": { "widthPt": 1440, "heightPt": 960 },
  "tokens": "./tokens.json",
  "elements": [
    {
      "id": "saveButton",
      "role": "button",
      "name": "Save",
      "controlSize": "default",
      "boxPt": [1280, 16, 72, 28],
      "foreground": "color.control.primaryText",
      "background": "color.control.accentFill",
      "states": ["default", "hover", "focus-visible", "pressed", "disabled"]
    },
    {
      "id": "sidebarRowProjects",
      "role": "option",
      "name": "Projects",
      "boxPt": [16, 148, 216, 28],
      "foreground": "color.selection.activeText",
      "background": "color.selection.activeFill",
      "states": ["default", "hover", "selected-active", "selected-inactive"]
    }
  ]
}
```

#### Gate policy: checkable without a rendering engine

| Check | Deterministically automatable without browser? | Decision rule |
|---|---|---|
| HTML parse validity, duplicate IDs, broken `aria-labelledby`, missing labels | Yes | Parse HTML with a standards-oriented parser; fail malformed references and unnamed interactive elements. |
| ARIA role presence and static role/property consistency | Yes, within declared markup | Fail invalid roles, invalid `aria-*` properties, unnamed `button`, `textbox`, `checkbox`, `menuitem`, `option`, and custom `[data-interactive]` elements. |
| `:focus-visible` coverage | Yes, syntactically | Require a focus-visible selector or a declared native-focus exemption for every interactive component family. |
| Token-versus-literal color discipline | Yes | Allow literal colors only in token-definition files; component CSS may use `var(--token)` or a permitted semantic alias. |
| WCAG 2.x contrast for flat, opaque colors | Yes | Resolve token → sRGB color; composite only when every layer is known and opaque; calculate relative luminance and ratio. Fail ordinary text under **4.5:1** and large text under **3:1**. [W3C, SC 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum) ([w3.org](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum?utm_source=openai)) |
| Alpha compositing over known solid background | Yes | Composite foreground alpha over exactly one known opaque background, then calculate contrast. |
| Liquid Glass, image, gradient, filter, backdrop-filter, inherited opacity, video, canvas | No exact contrast result | Emit `INDETERMINATE_CONTRAST`; fail strict CI unless an explicit rendered-engine exception exists. |
| Control target dimensions | Yes, if `boxPt` is required | Enforce macOS default **28×28 pt** and hard minimum **20×20 pt** for interactive elements. [Apple HIG, Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/accessibility?utm_source=openai)) |
| Overlap and parent-bound overflow | Yes, for supplied explicit boxes | Compute rectangle intersections and containment. Fail unintended overlap or overflow. |
| CSS layout overflow in arbitrary flex/grid/absolute/transform layouts | No | Static parser may flag risk patterns, but cannot prove final overflow without layout. Return `INDETERMINATE_LAYOUT`, not PASS. |
| Text truncation | Partly | Detect declared `text-overflow: ellipsis`, `overflow: hidden`, or line-clamp. Require an explicit `truncation: intentional|forbidden` contract. Exact visual clipping requires a renderer and font shaping. |
| Text fits a supplied box | Conditionally | Deterministic only for a restricted font and shaping implementation plus a declared string/box. Treat CSS-generated, locale-varying, or fallback-font text as indeterminate. |
| Keyboard navigation order | Partly | Validate explicit `tabindex` errors and named targets statically; actual focus order and dynamic focus traps require a running UI. |
| Menu command completeness | Yes, as a specification relation | Require every toolbar/context command ID to map to a declared menu-bar command ID. |
| Window restoration | Yes, as a mock handoff requirement | Require `restoration` fields in state matrix; runtime restoration needs an AppKit test. |

#### Contrast algorithm policy

**WCAG 2.2 must be the hard release gate for declared opaque text/background combinations.** WCAG requires **4.5:1** normal-text contrast and **3:1** large-text contrast, and explicitly says calculations must not be rounded up. [W3C, SC 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum) ([w3.org](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum?utm_source=openai))

**APCA should be a recorded advisory metric, not the sole conformance gate.** APCA is a candidate perceptual contrast method for future WCAG work, but WCAG 3 is not an adopted recommendation and APCA’s own documentation says one cannot claim “WCAG 3 compliant” today. [Myndex, SAPC-APCA documentation](https://github.com/Myndex/SAPC-APCA) ([github.com](https://github.com/Myndex/SAPC-APCA?utm_source=openai)) [Myndex, APCA minimum compliance](https://github.com/Myndex/SAPC-APCA/blob/master/documentation/minimum_compliance.md) ([github.com](https://github.com/Myndex/SAPC-APCA/blob/master/documentation/minimum_compliance.md?utm_source=openai))

```json
{
  "contrast": {
    "requiredAlgorithm": "wcag2",
    "normalTextMinimum": 4.5,
    "largeTextMinimum": 3.0,
    "advisoryAlgorithms": ["apca"],
    "unknownPaintResult": "fail",
    "rounding": "none"
  }
}
```

**Specific remediation for the reported 1.00:1 false pass:** a ratio of **1.00:1** means the declared foreground and effective background resolve to equal relative luminance. The gate must calculate and report the actual pair, source token chain, alpha-compositing steps, threshold, and failure—not accept a manually supplied `contrast: "PASS"` field. [W3C, SC 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum) ([w3.org](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum?utm_source=openai))

#### Suggested gate exit policy

| Exit code | Meaning | CI action |
|---:|---|---|
| `0` | No errors; no indeterminate checks in strict mode | Eligible for visual/reviewer handoff |
| `1` | Invalid contract, malformed HTML/CSS, or missing required artifact | Block |
| `2` | Contrast, minimum target, semantic, token, overflow, or command-map failure | Block |
| `3` | Indeterminate paint/layout/text-fit result under strict mode | Block unless approved rendered-engine exception |
| `4` | Contract/profile version mismatch, such as `macos-27-beta` rules applied to a `macos-26` mock | Block |

#### Deterministic gate pseudocode

```ts
for (const element of contract.elements) {
  assertUniqueId(element.id);
  assertRoleAndAccessibleName(htmlAst, element);
  assertDeclaredStates(element.states, REQUIRED_STATES[element.role]);

  assertMinControlSize(element.boxPt, element.role, profile);
  assertWithinCanvas(element.boxPt, contract.canvas);
  assertNoUnapprovedOverlap(element.boxPt, contract.elements);

  assertNoLiteralColors(componentCssFor(element));
  const fg = resolveColorToken(element.foreground, tokens);
  const bg = resolveColorToken(element.background, tokens);

  if (isFlatOpaque(fg) && isFlatOpaque(bg)) {
    const ratio = wcagContrast(fg, bg);
    assertContrast(ratio, textThreshold(element));
  } else {
    emitIndeterminate("INDETERMINATE_CONTRAST", element.id);
  }

  assertFocusVisibleCss(htmlAst, cssAst, element);
  assertTruncationDeclared(cssAst, element);
  assertToolbarAndContextCommandsInMenuMap(element, states);
}
```

<INFERENCE from="[Apple’s published control sizes; WCAG contrast thresholds; W3C’s warning that tools cannot determine conformance]">The gate should be intentionally conservative: a result is PASS only when the input model permits an exact calculation; otherwise the result must be FAIL or INDETERMINATE. This eliminates the observed failure mode in which prose claims PASS despite a mathematically invalid contrast pair.</INFERENCE> [Apple HIG, Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/accessibility?utm_source=openai)) [W3C, SC 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum) ([w3.org](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum?utm_source=openai)) [W3C, Evaluating Web Accessibility](https://www.w3.org/WAI/test-evaluate/) ([w3.org](https://www.w3.org/WAI/test-evaluate/?utm_source=openai))

### 2. What is the current state, and what is the strongest supporting evidence for it?

**Finding — High Confidence.** The strongest evidence is first-party Apple HIG, AppKit/SwiftUI documentation, and WWDC sessions. Together they show a two-release transition:

- **macOS 26 Tahoe:** introduced Liquid Glass as an adaptive, functional layer for controls/navigation; floating toolbars; inset glass sidebars; scroll-edge effects; automatic updates for standard framework controls; and stronger concentric-corner guidance. [Apple WWDC25, Meet Liquid Glass](https://developer.apple.com/videos/play/wwdc2025/219/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/219/?utm_source=openai)) [Apple WWDC25, Get to know the new design system](https://developer.apple.com/videos/play/wwdc2025/356/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/356/?time=0&utm_source=openai))

- **macOS 27 Golden Gate beta:** refines Liquid Glass readability and personalization, makes sidebars edge-extending, adjusts sidebar selection and toolbar/scroll-edge behavior, standardizes tighter window corners, and adds interactive glass and AppKit concentric-corner support. [Apple WWDC26 Platforms State of the Union](https://developer.apple.com/videos/play/wwdc2026/112/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/112/?time=173&utm_source=openai)) [Apple WWDC26, Modernize your AppKit app](https://developer.apple.com/videos/play/wwdc2026/289/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/289/?utm_source=openai))

#### Tool and verification comparison

| Tool / approach | Parameter Count | Context Window | Latency | Cost | License | DOM-free? | Practical role |
|---|---:|---:|---|---|---|---|---|
| Custom restricted mock-contract gate | N/A | Entire mock artifact | <MISSING_DATA>[Benchmark not performed; depends on implementation and artifact size.]</MISSING_DATA> | Internal engineering cost | Team-selected | **Yes** | Authoritative deterministic checks for declared tokens, colors, roles, geometry, state coverage, and command maps. |
| `eslint-plugin-jsx-a11y` | N/A | Source AST | Build-time | Free | MIT [jsx-eslint repository](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y) ([github.com](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y)) | **Yes, JSX only** | Static source lint; useful only if mockups are generated from JSX. |
| axe-core | N/A | Rendered DOM | Test-time | Free/open source | MPL-2.0 [Deque axe-core repository](https://github.com/dequelabs/axe-core) ([github.com](https://github.com/dequelabs/axe-core)) | No | Rendered DOM/ARIA accessibility tests; not the static contrast authority. |
| Pa11y | N/A | Browser page and scripted states | Test-time | Free/open source | LGPL-3.0 [Pa11y repository](https://github.com/pa11y/pa11y) ([github.com](https://github.com/pa11y/pa11y)) | No; uses Headless Chrome | Browser-stage regression testing and workflow actions. |
| Lighthouse | N/A | Chrome page load | Test-time; variable | Free/open source | Apache-2.0 [Lighthouse repository](https://github.com/GoogleChrome/lighthouse) ([github.com](https://github.com/GoogleChrome/lighthouse)) | No | Broad browser audit; accessibility score is a triage signal, not a conformance result. |
| IBM Equal Access | N/A | HTML parser or browser integration | Test-time | Free/open source | Apache-2.0 [IBM Equal Access repository](https://github.com/IBMa/equal-access) ([github.com](https://github.com/ibma/equal-access)) | Partly; Node engine exists but integrations use HTML parsing/browser engines | Alternate automated checker and baseline comparison. |
| APCA (`apca-w3`) | N/A | Foreground/background input pairs | Build-time | Free package, subject to APCA trademark/use terms | Verify package/repository terms before embedding | Yes for known colors | Advisory perceptual contrast metric; not current WCAG conformance. |

**Tool reality check — High Confidence.** axe-core’s own repository says it detects “on average **57%** of WCAG issues automatically,” and reports incomplete items where manual review is required. That is a vendor-provided coverage statement, not an independent benchmark. [Deque axe-core repository](https://github.com/dequelabs/axe-core) ([github.com](https://github.com/dequelabs/axe-core))

**Tool limitation — High Confidence.** axe-core requires a complete attached DOM; its repository states that its `color-contrast` rule does not work in JSDOM. Therefore, a JSDOM-based axe run cannot be accepted as proof that an HTML mockup’s contrast is valid. [Deque axe-core repository](https://github.com/dequelabs/axe-core) ([github.com](https://github.com/dequelabs/axe-core?utm_source=openai)) [Deque axe-core JSDOM example](https://github.com/dequelabs/axe-core/blob/develop/doc/examples/jest_react/README.md) ([github.com](https://github.com/dequelabs/axe-core/blob/develop/doc/examples/jest_react/README.md?utm_source=openai))

### 3. What are the contrasting viewpoints or competing evidence?

**Liquid Glass visual unification versus macOS interaction specificity.** Apple’s 2025 design system deliberately creates a shared visual family across platforms, including Liquid Glass, sidebars, controls, and navigation components. [Apple WWDC25, Meet Liquid Glass](https://developer.apple.com/videos/play/wwdc2025/219/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/219/?utm_source=openai)) However, Apple’s macOS guidance remains explicit that Mac users expect large displays, multiple concurrently visible apps and windows, high-precision input, keyboard shortcuts, menu-bar access, configurable windows, and toolbar customization. [Apple HIG, Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos?changes=l_8_2&utm_source=openai))

<CONFLICTING_EVIDENCE>[Visual convergence across Apple platforms is intentional, but platform interaction convergence is not complete. Apple promotes one shared design language while separately requiring macOS-specific input, windowing, menu, keyboard, and personalization behaviour. The resolution is to share semantic visual language while preserving Mac-native interaction architecture.]</CONFLICTING_EVIDENCE>

**WCAG 2.x versus APCA.** WCAG 2.2 is the current W3C Recommendation-based conformance framework and supplies the enforceable **4.5:1** and **3:1** thresholds used by mainstream accessibility tooling. [W3C, SC 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum) ([w3.org](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum?utm_source=openai)) APCA aims to model perceptual contrast more directly and is presented by its maintainers as a candidate method for WCAG 3, but it is still evolving; its own documentation warns against claiming WCAG 3 compliance. [Myndex, SAPC-APCA documentation](https://github.com/Myndex/SAPC-APCA) ([github.com](https://github.com/Myndex/SAPC-APCA?utm_source=openai)) [Myndex, APCA minimum compliance](https://github.com/Myndex/SAPC-APCA/blob/master/documentation/minimum_compliance.md) ([github.com](https://github.com/Myndex/SAPC-APCA/blob/master/documentation/minimum_compliance.md?utm_source=openai))

<CONFLICTING_EVIDENCE>[WCAG 2.x offers stable, broadly accepted conformance thresholds; APCA offers potentially richer perceptual diagnostics but is not a completed WCAG conformance standard. Use WCAG 2.2 for hard blocking and record APCA as advisory.]</CONFLICTING_EVIDENCE>

**Automated PASS versus conformance.** Deque describes axe as designed for zero false positives subject to bugs, while W3C states that no tool alone can determine whether a site meets accessibility standards and warns that tools can produce false or misleading results. [Deque axe-core repository](https://github.com/dequelabs/axe-core) ([github.com](https://github.com/dequelabs/axe-core?utm_source=openai)) [W3C, Selecting Web Accessibility Evaluation Tools](https://www.w3.org/WAI/test-evaluate/tools/selecting/) ([w3.org](https://www.w3.org/WAI/test-evaluate/tools/selecting/?utm_source=openai))

<CONFLICTING_EVIDENCE>[Rule-level precision can be high for a narrow, fully observable condition, while page-level accessibility conformance cannot be inferred from a passing tool score. Resolve this by making the static gate authoritative only for explicitly computable invariants and treating all other results as indeterminate or requiring human/rendered review.]</CONFLICTING_EVIDENCE>

### 4. What changed recently, and what is the trajectory?

**Finding — High Confidence.** The trajectory from macOS 26 to macOS 27 is toward **more adaptive system-owned material, fewer fixed visual constants, stronger contextual readability, and more formal geometry relationships.**

- Apple introduced Liquid Glass in macOS 26 as a dynamic material whose appearance adapts to what is behind it, including light/dark transitions and greater separation when content scrolls underneath. [Apple WWDC25, Meet Liquid Glass](https://developer.apple.com/videos/play/wwdc2025/219/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/219/?utm_source=openai))

- In macOS 27 beta, Apple says Liquid Glass has improved diffusion of complex content, brighter highlights/darker edges, a user-facing clarity/tint slider, better accessibility adaptation, edge-expanding sidebars, tighter window radii, and more consistent toolbar scroll-edge treatment. [Apple WWDC26 Platforms State of the Union](https://developer.apple.com/videos/play/wwdc2026/112/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/112/?time=173&utm_source=openai))

- AppKit now exposes a container-concentric corner API and macOS 27 adds optional interactive glass response for controls. [Apple WWDC26, Modernize your AppKit app](https://developer.apple.com/videos/play/wwdc2026/289/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/289/?utm_source=openai))

- Apple’s June 8, 2026 sidebar guidance update clarified sidebar icon-color behaviour and adaptable sidebar style, reinforcing that user accent-color preference remains a platform-level customization concern. [Apple HIG, Sidebars](https://developer.apple.com/design/human-interface-guidelines/sidebars/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/sidebars?changes=_11&utm_source=openai))

<INFERENCE from="[macOS 27’s user-adjustable Liquid Glass appearance; accessibility adaptation; automatic framework updates]">The mockup skill should stop encoding material as immutable CSS paint values. Its durable handoff unit should be a semantic material role plus accessibility/state variants, allowing SwiftUI/AppKit to adopt shipping-system changes without redesigning each mock.</INFERENCE> [Apple WWDC26 Platforms State of the Union](https://developer.apple.com/videos/play/wwdc2026/112/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/112/?time=173&utm_source=openai))

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| Liquid Glass is a functional layer for controls/navigation and should not be used broadly in content. | Apple Human Interface Guidelines, Materials | Current page crawled August 2026 | First-party platform design guidance; meets source discipline as authoritative Apple HIG. | https://developer.apple.com/design/human-interface-guidelines/materials/ |
| macOS toolbar is in the top window frame, below or integrated with titlebar; toolbar commands must also be menu commands. | Apple Human Interface Guidelines, Toolbars | Current page crawled August 2026 | First-party platform design guidance; authoritative Apple HIG. | https://developer.apple.com/design/human-interface-guidelines/toolbars |
| macOS windows support frame/body structure, active/inactive states, resizing, movement, and multi-window workflows. | Apple Human Interface Guidelines, Windows | Current page crawled August 2026 | First-party platform design guidance; authoritative Apple HIG. | https://developer.apple.com/design/human-interface-guidelines/windows |
| macOS target sizes are 28×28 pt default and 20×20 pt minimum. | Apple Human Interface Guidelines, Accessibility | Current page crawled August 2026 | First-party accessibility guidance; authoritative Apple HIG. | https://developer.apple.com/design/human-interface-guidelines/accessibility/ |
| macOS built-in text ramp includes Body 13 pt / 16 pt and minimum readable text size of 10 pt. | Apple Human Interface Guidelines, Typography | Current page crawled August 2026 | First-party typography specification; authoritative Apple HIG. | https://developer.apple.com/design/human-interface-guidelines/typography/ |
| Sidebar depth should generally be no more than two levels; deeper hierarchies should use a split view. | Apple Human Interface Guidelines, Sidebars | Updated June 8, 2026 | First-party platform design guidance; authoritative Apple HIG. | https://developer.apple.com/design/human-interface-guidelines/sidebars/ |
| macOS 27 beta introduces/refines edge-to-edge sidebars, selection emphasis, scroll-edge behaviour, interactive glass, and concentric corners. | Apple WWDC26, Modernize your AppKit app | June 2026 | First-party Apple engineering/design session; authoritative but beta-era. | https://developer.apple.com/videos/play/wwdc2026/289/ |
| macOS 27 is Golden Gate beta as of the cited release notes. | Apple macOS Release Notes | August 2026 crawl | First-party release documentation; authoritative current release status. | https://developer.apple.com/documentation/macos-release-notes |
| WCAG normal text threshold is 4.5:1, large text threshold is 3:1, and ratios must not be rounded upward. | W3C, Understanding SC 1.4.3 | Current WCAG 2.2 explanation | Standards-body guidance; authoritative accessibility reference. | https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum |
| No automated tool alone determines accessibility conformance; human evaluation is required. | W3C WAI, Evaluating Web Accessibility | Current page crawled August 2026 | Standards-body evaluation methodology guidance; authoritative. | https://www.w3.org/WAI/test-evaluate/ |
| axe-core requires DOM rendering for complete tests and its color-contrast rule does not work in JSDOM. | Deque axe-core source repository | Current repository crawl August 2026 | Maintainer primary source and source code documentation. | https://github.com/dequelabs/axe-core |
| Pa11y uses Headless Chrome/Puppeteer and browser-context runners. | Pa11y source repository | Current repository crawl August 2026 | Maintainer primary source and source code documentation. | https://github.com/pa11y/pa11y |
| IBM Equal Access provides Node artifacts but uses HTML parsing/browser engines for integration. | IBM Equal Access source repository | Current repository crawl August 2026 | Maintainer primary source and source code documentation. | https://github.com/IBMa/equal-access |
| APCA is a candidate future contrast method, not a current WCAG 3 conformance basis. | Myndex SAPC-APCA documentation | Current repository crawl August 2026 | Algorithm maintainer primary documentation; not a W3C conformance source. | https://github.com/Myndex/SAPC-APCA |

## Knowledge Gaps

### Apple-published visual measurements

<MISSING_DATA>[Exact macOS 26/27 point values for every standard control height, toolbar height, titlebar height, sidebar row height, corner radius, blur radius, glass opacity, and scroll-edge blur were sought. Apple publishes semantic APIs, dynamic system components, control-size guidance, and typography values, but no complete public fixed-value table was located. A shipping-design-kit specification or an official Apple control-metrics reference would be needed.]</MISSING_DATA>

### Mac-reviewer perception studies

<INSUFFICIENT_EVIDENCE>[The investigation found strong first-party documentation for the behaviours Mac users are expected to encounter, but not a recent peer-reviewed controlled study that quantifies which individual affordance failures cause reviewers to label an interface “not a real Mac app.” The diagnostic list is grounded in Apple expectations and marked as inference where it asserts reviewer perception.]</INSUFFICIENT_EVIDENCE>

### DOM-free text-layout certainty

<MISSING_DATA>[A browser-free parser cannot exactly establish glyph shaping, fallback-font selection, CSS line breaking, flex/grid layout, transforms, or painted clipping for arbitrary HTML/CSS. Exact verification requires either a deliberately restricted mock layout grammar or a rendering engine using the deployment font stack.]</MISSING_DATA>

### Performance, API schema, rate-limit, and cost data

<INSUFFICIENT_EVIDENCE>[The named open-source tools are locally executable packages rather than hosted APIs with common published request-rate limits or usage pricing. No universal latency or cost figures apply. A reproducible benchmark suite running the proposed gate, Playwright/axe, Pa11y, and Lighthouse on representative mockups would be needed.]</INSUFFICIENT_EVIDENCE>

## Recommended Next Steps

1. **Implement `mock-contract/v1` and make the static gate blocking.**  
   **Rationale:** It directly prevents prose-based self-certification and can catch a 1.00:1 contrast failure from declared opaque tokens before a browser, screenshot, or human review occurs.

2. **Create two explicit profiles: `macos-26-production` and `macos-27-beta`.**  
   **Rationale:** macOS 27 is still beta as of August 18, 2026; versioning prevents beta appearance rules from silently overwriting stable Tahoe implementation instructions. [Apple macOS Release Notes](https://developer.apple.com/documentation/macos-release-notes) ([developer.apple.com](https://developer.apple.com/documentation/macos-release-notes?utm_source=openai))

3. **Add a second-stage rendered test suite using Playwright plus axe-core, with scripted states for menu, context menu, selected/inactive window, reduced transparency, increased contrast, and reduced motion.**  
   **Rationale:** Static validation cannot prove painted contrast over glass, actual focus order, truncation, layout, or state transitions; axe-core itself requires a complete DOM and has known JSDOM contrast limits. [Deque axe-core repository](https://github.com/dequelabs/axe-core) ([github.com](https://github.com/dequelabs/axe-core/blob/develop/doc/context.md?utm_source=openai))

4. **Require a SwiftUI/AppKit implementation checklist alongside every mockup.**  
   **Rationale:** The checklist should map each HTML command to menu-bar commands, shortcuts, context menus, drag/drop alternatives, window restoration, and accessibility environment variants. This turns the mockup into a usable implementation contract rather than a decorative picture. [Apple HIG, Designing for macOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos/) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos?changes=l_8_2&utm_source=openai))

5. **Benchmark the gate against a seeded defect corpus.**  
   **Rationale:** Include deliberate failures: equal foreground/background colors, alpha-over-glass ambiguity, missing `focus-visible`, 19 pt controls, toolbar-only commands, unnamed custom controls, hidden text overflow, and missing inactive-selection state. Report precision, indeterminate rate, and median runtime rather than allowing authors to report PASS.

## Sources

- [Materials | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/materials?utm_source=openai)
- [Accessibility | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/accessibility?utm_source=openai)
- [Typography | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/typography?changes=_5&utm_source=openai)
- [Designing for macOS | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos?changes=l_8_2&utm_source=openai)
- [Understanding Success Criterion 1.4.3: Contrast (Minimum) | WAI | W3C](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum?utm_source=openai)
- [GitHub - dequelabs/axe-core: Accessibility engine for automated Web UI testing · GitHub](https://github.com/dequelabs/axe-core?utm_source=openai)
- [GitHub - pa11y/pa11y: Pa11y is your automated accessibility testing pal · GitHub](https://github.com/pa11y/pa11y?utm_source=openai)
- [GitHub - IBMa/equal-access: IBM Equal Access Accessibility Checker contains tools to automate acc...](https://github.com/ibma/equal-access?utm_source=openai)
- [macOS Release Notes | Apple Developer Documentation](https://developer.apple.com/documentation/macos-release-notes?utm_source=openai)
- [Modernize your AppKit app - WWDC26 - Videos - Apple Developer](https://developer.apple.com/videos/play/wwdc2026/289/?utm_source=openai)
- [Evaluating Web Accessibility Overview | Web Accessibility Initiative (WAI) | W3C](https://www.w3.org/WAI/test-evaluate/?utm_source=openai)
- [Build a SwiftUI app with the new design - WWDC25 - Videos - Apple Developer](https://developer.apple.com/videos/play/wwdc2025/323/?utm_source=openai)
- [Windows | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/windows?utm_source=openai)
- [Toolbars | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/toolbars?changes=_2&utm_source=openai)
- [Sidebars | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/sidebars?changes=_11&utm_source=openai)
- [Platforms State of the Union (ASL) - WWDC26 - Videos - Apple Developer](https://developer.apple.com/videos/play/wwdc2026/112/?time=173&utm_source=openai)
- [Color | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/color?changes=_5_2&utm_source=openai)
- [Focus and selection | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection/?utm_source=openai)
- [Dark Mode | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/dark-mode?utm_source=openai)
- [Color | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/color?changes=l_8&utm_source=openai)
- [concentricCornerRadii(in:) | Apple Developer Documentation](https://developer.apple.com/documentation/swiftui/geometryproxy/concentriccornerradii%28in%3A%29?changes=lat_3_5&utm_source=openai)
- [Get to know the new design system - WWDC25 - Videos - Apple Developer](https://developer.apple.com/videos/play/wwdc2025/356/?time=0&utm_source=openai)
- [Buttons | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/buttons?changes=latest_1__8&utm_source=openai)
- [NSTrackingArea | Apple Developer Documentation](https://developer.apple.com/documentation/appkit/nstrackingarea?changes=_7&utm_source=openai)
- [Keyboards | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/keyboards/?utm_source=openai)
- [Menus | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/menus?utm_source=openai)
- [accessibilityReduceTransparency | Apple Developer Documentation](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducetransparency?changes=_2&utm_source=openai)
- [accessibilityDisplayShouldIncreaseContrast | Apple Developer Documentation](https://developer.apple.com/documentation/appkit/nsworkspace/accessibilitydisplayshouldincreasecontrast?changes=_2___8_8&language=objc&utm_source=openai)
- [ColorSchemeContrast | Apple Developer Documentation](https://developer.apple.com/documentation/swiftui/colorschemecontrast?utm_source=openai)
- [accessibilityReduceMotion | Apple Developer Documentation](https://developer.apple.com/documentation/swiftui/environmentvalues/accessibilityreducemotion?changes=_3&utm_source=openai)
- [Reduced Motion evaluation criteria - Manage App Accessibility - App Store Connect - Help - Apple ...](https://developer.apple.com/help/app-store-connect/manage-app-accessibility/reduced-motion-evaluation-criteria?utm_source=openai)
- [Pointing devices | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/pointing-devices?changes=_1&utm_source=openai)
- [Writing | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/writing?changes=l_1&utm_source=openai)
- [Context menus | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/context-menus?changes=__3&utm_source=openai)
- [Drag and drop | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop?utm_source=openai)
- [Launching | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/launching/?utm_source=openai)
- [GitHub - Myndex/SAPC-APCA: APCA (Accessible Perceptual Contrast Algorithm) is a new method for pr...](https://github.com/Myndex/SAPC-APCA?utm_source=openai)
- [SAPC-APCA/documentation/minimum_compliance.md at master · Myndex/SAPC-APCA · GitHub](https://github.com/Myndex/SAPC-APCA/blob/master/documentation/minimum_compliance.md?utm_source=openai)
- [Meet Liquid Glass - WWDC25 - Videos - Apple Developer](https://developer.apple.com/videos/play/wwdc2025/219/?utm_source=openai)
- [GitHub - jsx-eslint/eslint-plugin-jsx-a11y: Static AST checker for a11y rules on JSX elements. · ...](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y)
- [GitHub - dequelabs/axe-core: Accessibility engine for automated Web UI testing · GitHub](https://github.com/dequelabs/axe-core)
- [GitHub - pa11y/pa11y: Pa11y is your automated accessibility testing pal · GitHub](https://github.com/pa11y/pa11y)
- [GitHub - GoogleChrome/lighthouse: Automated auditing, performance metrics, and best practices for...](https://github.com/GoogleChrome/lighthouse)
- [GitHub - IBMa/equal-access: IBM Equal Access Accessibility Checker contains tools to automate acc...](https://github.com/ibma/equal-access)
- [axe-core/doc/examples/jest_react/README.md at develop · dequelabs/axe-core · GitHub](https://github.com/dequelabs/axe-core/blob/develop/doc/examples/jest_react/README.md?utm_source=openai)
- [Selecting Web Accessibility Evaluation Tools | Web Accessibility Initiative (WAI) | W3C](https://www.w3.org/WAI/test-evaluate/tools/selecting/?utm_source=openai)
- [axe-core/doc/context.md at develop · dequelabs/axe-core · GitHub](https://github.com/dequelabs/axe-core/blob/develop/doc/context.md?utm_source=openai)
