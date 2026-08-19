# Corner Time — profile

- **Source:** macapp.supply (cover.png only — a marketing composite; no standalone UI shots supplied) · **Surfaces digested:** settings window (Format pane, dark mode) + the product's own output surface (chromeless corner-clock overlay) · **Last updated:** 2026-07-19
- **One-sentence identity:** A tiny native SwiftUI settings pane — Alcove/Bartender-class config-window plumbing — wrapped around one genuinely good idea: a WYSIWYG preview card that renders the corner clock live above the toggles that shape it, so an ephemeral, off-to-one-side overlay becomes tangible while you configure it.
- **Cluster:** menu-bar-utility config pane (proposed; peers Alcove-settings, Bartender, Itsycal/Dato, Bauhaus Clock's options)
- **Lineage:** native (high confidence) — macOS-correct SwiftUI: genuine traffic lights + circled Help button, native capsule switches (blue-on / gray-off), a segmented `Picker`, and an inset-grouped settings card with hairline row dividers. Density reads 13–15pt labels / ~24pt controls, not iOS 17pt/44pt.
- **Era (chrome):** big-sur (continuous native material era, Big Sur→Sequoia). Liquid Glass can be neither confirmed nor denied — dark-mode humility: a dark translucent window reads near-opaque graphite in a still, and no lensing/edge-refraction is visible. The blue cast on the window suggests a translucent window material tinted by the desktop behind it (native vibrancy), not a painted flat fill.

> ⚠ **Cover-composite discipline.** The only asset is a 1200×630 OG marketing image. Three layers, kept separate: (1) the **app window** on the left — the primary design evidence; (2) the **corner overlay** top-right ("Tue Apr 1  9:41 AM" with a hand-drawn arrow pointing at it) — the app's *actual runtime output*, a legitimate second surface; (3) the **brand layer** — blue Sonoma-style ribbon wallpaper + white display headline + cyan wordmark. The window is a stylized *render*, not a captured screenshot (see Defects: the red+gray+gray traffic lights are a non-real macOS state), so every control metric is `(estimated)` at an unknowable scale — though the traffic-light cluster measures ~60px against the native 68pt, so cover-px ≈ logical-pt to within ~10%.

## Tokens

### App window (settings pane, dark mode) — the design evidence

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window | dark blue-gray ~`#2B3542` (estimated)(inferred) | | NOT the kit's neutral `#1E1E1E` dark — blue-shifted; reads as a translucent window material picking up the blue desktop (vibrancy), not a flat paint |
| bg/card | ~`#333E4C`, one step lighter than window (estimated)(inferred) | | the grouped settings card + preview card sit on a slightly-elevated surface (base-vs-elevated dark depth) |
| type/row-label | ~15pt SF Pro Regular, primary white (estimated)(inferred) | | "Use 24-hour format" etc. — a touch above the 13pt kit Body |
| type/preview-title | ~17pt SF Pro Semibold, white (estimated)(inferred) | | "Corner Time" bottom-left of the preview card |
| type/tab-label | ~13pt SF Pro, selected primary / unselected ~55% (estimated)(inferred) | | Format(selected) · Style · General |
| type/clock | ~11–12pt SF Pro, white | (estimated)(inferred) | the live "Tue Apr 1 9:41 AM" inside the preview card |
| accent/on | system blue ~`#0A84FF`/`#0088FF` (estimated)(inferred) | | "on" switch fill; reserved to switch state only — cannot confirm it tracks `controlAccentColor` vs hardcoded blue |
| control/switch | capsule ~36×21px, white knob; off = gray track, knob-left (estimated)(inferred) | | native-scale macOS/SwiftUI Toggle, not an iOS 51×31 UISwitch |
| control/segmented | 3 equal segments, ~24–28pt tall; selected = neutral inset rounded fill (estimated)(inferred) | | selection is *neutral* gray, correct — segmented selection never takes accent |
| row/height | ~52px, comfortable (estimated)(inferred) | | taller than the kit's 40pt Large row — consumer-comfortable density for a 4-row pane |
| divider/row | hairline, left-inset to label edge, very faint (estimated)(inferred) | | low contrast — see Defects #10 |
| radius/preview-card | ~12px (estimated)(inferred) | | thumbnail of desktop + overlay |
| radius/settings-card | ~14px (estimated)(inferred) | | concentric: card > rows |
| pad/window-inset | ~20px content inset each side (estimated)(inferred) | | preview card, segmented control, settings card all share this left/right axis |
| chrome/traffic-lights | ~14px dots, ~60px cluster, top-left (estimated)(inferred) | | reads native scale; **state is stylized** (see Defects) |
| chrome/help | circled "?" glyph, titlebar top-right (estimated)(inferred) | | standard macOS Help button — a genuine native affordance |

### Corner overlay (the product's actual output) — second surface

| Token | Value | Provenance | Notes |
|---|---|---|---|
| overlay/text | "Tue Apr 1  9:41 AM" — SF Pro, white, ~24px in the hero render (estimated)(inferred) | | chromeless: no container, no background, no shadow visible — pure antialiased system text in the screen corner |
| overlay/composition | day + weekday + time on one line, top-right corner inset (estimated)(inferred) | | deliberately mimics the real menu-bar clock's typography so it reads as a system feature, not an app |

### Brand / marketing layer (NOT app-UI tokens)

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/backdrop | blue Sonoma/Sequoia-style flowing-ribbon wallpaper ~`#3E6FB0`→`#2C517F` (estimated)(inferred) | | signals "at home on your macOS desktop" |
| brand/wordmark | "Corner Time" cyan-mint ~`#5EC8D8`, medium weight (estimated)(inferred) | | |
| brand/headline | "Always-visible Clock for Fullscreen & Hidden Menu Bar" — white SF Pro Display Bold, ~48–56px, left-aligned (estimated)(inferred) | | |
| brand/pointer | hand-drawn white arrow from wordmark up to the live corner overlay (estimated)(inferred) | | marketing device: literally points at the feature where it lives on screen |

## Layout skeletons

**Settings window (portrait utility panel, ~299px wide):** single-column vertical stack, one shared ~20px left/right inset axis for all three blocks. Top→bottom: (1) **titlebar** — traffic lights leading, Help "?" trailing; (2) **WYSIWYG preview card** (~258×157, r≈12) — a desktop-wallpaper thumbnail with the live clock overlay top-right and the "Corner Time" label bottom-left, i.e. a scaled render of the actual product output; (3) **segmented control** Format · Style · General (in-view pane switch); (4) **inset-grouped settings card** (r≈14) of 4 rows, each `label … trailing switch`, separated by faint left-inset hairlines: Use 24-hour format (off) · Display seconds (off) · Show date (on) · Show day of the week (on). Proximity is correct — the segmented control is separated from the card by a gap larger than the intra-card row gaps.

**Corner overlay (runtime output):** a single line of chromeless SF Pro text, corner-inset (top-right in the render). No window, no chrome, no grid — maximal restraint; the entire "UI" is one string styled to pass as the system clock.

## Signature moves

- **[GOLDEN-NUGGET] The live WYSIWYG preview card.** The app's whole output is an ephemeral overlay you may not even be looking at while you configure it (it lives in a *corner*, in fullscreen, or where a hidden menu bar was). Rendering the actual clock, on the actual wallpaper, *directly above the toggles that shape it* collapses the imagination gap — flip "Show date" and see the result, not a description. This is the description–experience gap answered in the layout itself, and it is the single decision that lifts an otherwise stock settings pane into something owned. Every corner-overlay/config utility should copy it.
- **The product disappears into the OS.** The runtime surface is chromeless SF Pro white text deliberately typeset to mimic the real menu-bar clock — so a third-party overlay reads as a native system feature (Jakob's Law working *for* the app). The restraint is the taste: the app's best design choice is to have almost no visible design.

## Defects

- **#10 UI contrast (mild).** Row-divider hairlines and the off-state switch track are faint against the dark blue window — borderline below the 3:1 non-text floor. Contrast-Dilution-adjacent, but conventional for macOS grouped lists; a half-step lighter divider would clear it.
- **Traffic-light state is non-real (render artifact, not an app defect).** The window shows a lit red + two gray lights — a state real macOS never produces (a focused/key window colors all three; an inactive window grays all three). This confirms the window is a stylized marketing render; treat its chrome as illustrative, not as a claim about the shipped app's window state.
- **Segmented control doing pane navigation (minor, borderline).** Format/Style/General switches *content sections*, which HIG assigns to an in-window tab view, not a segmented control ("a segmented control is not a tab bar"). It's a near-universal accepted SwiftUI `Picker(.segmented)` idiom for small settings windows, so this is a pattern quibble, not a violation — but a proper tab view or toolbar tabs would be the more strictly-native choice.
- **Row height ~52pt** runs taller than the kit's 40pt Large row — a consumer-comfortable density choice, defensible for a 4-row pane, noted not faulted.
- **Verdict: competent and *quietly* characterful.** Not "competent but anonymous" — the preview card is a real signature — but everything around it is faithful platform-default chrome. The character is in one component and in the restraint, not in a committed aesthetic direction.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| settings window (Format pane, dark) | 13/14 | #10 faint dividers/off-switch track borderline <3:1; #14 focus state unverifiable in a static render (absence noted, not counted as fail); #5/#6 line-height & measure N/A (no text blocks) counted as pass |
| native-tells audit | 9/10 | #10 traffic-light state stylized (red+gray+gray — non-real macOS); #3 pass but segmented-as-pane-nav noted; #4/#7/#9 N/A (no sidebar/dialog/toolbar); #2 glass indeterminate in dark (humility) |
| corner overlay (runtime output) | N/A | single chromeless text element — most checks N/A; contributes brand/typography evidence only, like a screensaver canvas |
