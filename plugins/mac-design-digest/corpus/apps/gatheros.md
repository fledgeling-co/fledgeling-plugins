# GatherOS — profile

- **Source:** macapp.supply (meta.json) · **Surfaces digested:** 1 (Library / card-grid main window, light) — from a **marketing cover composite only** · **Last updated:** 2026-07-19
- **One-sentence identity:** Eagle/Cosmos-genre design-inspiration collector wearing a colourless gallery-white chrome so the saved artwork carries 100% of the palette — "Pinterest's moodboard discipline in a monochrome Mac frame."
- **Cluster:** unassigned (content-forward gallery — see cluster_hint; single non-native app, cannot seed a cluster)
- **Lineage:** web-electron (low) — reads custom/non-native; **could equally be bespoke SwiftUI going deliberately custom**. Either way the body is non-native-reading (underline scope tabs, black-not-accent pill CTA, faux monochrome window dots, no source list), so **none of this evidence feeds macOS canon.** Judged from body, not frame, per lineage rule; a clean @2x screenshot would raise confidence.
- **Era (chrome):** custom (flat white, colourless) — not Liquid Glass, not legacy-native. No glass, no vibrancy, no native materials observable.

> **Evidence-quality warning.** The only asset is a 1200×630 OG/marketing cover. The app window is **3D-perspective-transformed (~15–20° yaw + foreshortening)**, so NO clean pixel measurement is possible — every spatial/type token below is `(estimated)` with wide ranges or `(assumed)`, and nothing here is promotable. The left half of the cover is brand evidence (wordmark, headline, CTA); the right-half window is the design evidence. The two are analysed separately and never conflated.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/chrome | #FAFAFA (measured)(inferred) | | window/toolbar surface sampled at 250,250,250; near-white, faintly warm-neutral |
| bg/marketing | #FFFFFF (measured)(inferred) | | left-half brand backdrop is pure white |
| surface/card | #FFFFFF + soft ambient shadow (estimated)(inferred) | | collection cards float on ~1–2px-blur low-opacity shadow (elevated card, M3-Elevated-like) |
| text/primary | ~#1A1A1A near-black (estimated)(inferred) | | card titles, tab labels, wordmark |
| text/secondary | ~#9A9A9E grey (estimated)(inferred) | | "N saves" counts, deselected tabs — proper de-emphasis vs primary |
| accent/brand-action | #000000 (measured)(inferred) | | prominent actions are BLACK capsule pills, not the system accent — brand signature, non-native |
| accent/icon-mark | ~#3B7BF5 blue (estimated)(inferred) | | the only saturated brand hue, lives only in the app-icon "D" glyph; absent from the UI chrome |
| radius/card | ~10–14px (estimated)(inferred) | | white collection cards; perspective-distorted |
| radius/thumbnail | ~10–12px (estimated)(inferred) | | image inside card steps down from card radius → roughly concentric |
| radius/pill | capsule (estimated)(confirmed) | | both the product "Library" pill and the marketing "Download for Mac" pill are full capsules — consistent brand shape |
| type/card-title | ~13–14px semibold sans (estimated)(inferred) | | "Interfaces", "Branding", "Type" |
| type/card-meta | ~10–11px regular grey (estimated)(inferred) | | "5 saves" / "24 saves" |
| type/wordmark+headline | heavy geometric grotesque (Inter-Display-Black / TT-Norms class) (estimated)(inferred) | | marketing side; large, tight-tracked, black weight |
| chrome/scope-nav | underline tabs — All (active, short black underline) · Unsorted · Trash (estimated)(inferred) | | NON-native scope switch (web/iOS pattern); native would be segmented control or sidebar |
| chrome/library-picker | "Library ⌄" double-chevron pop-up button (estimated)(inferred) | | the ONE native-grammar-correct affordance: double chevron + shows-current-value = pick-a-value pop-up |
| chrome/window-dots | 3 monochrome grey dots, top-left (measured)(inferred) | | faux/inactive traffic lights — colourless, not genuine red/yellow/green focused lights |

## Layout skeletons

**Library / main window (light, card grid)** — perspective render, reading top→bottom:
- **Header strip** (near-white #FAFAFA, no hard bottom divider — bar fades into content): leading = app-icon squircle + "Library ⌄" pop-up (library switcher); centre = whitespace; trailing = search magnifier glyph only (no visible field bezel). Colourless.
- **Scope row**: underline tab group left-aligned (All / Unsorted / Trash), active tab marked by a short black underline bar + black text, others grey. A **black capsule pill** ("Library…", cut off at frame edge) pinned to the trailing edge of this row — the single prominent action.
- **Content: masonry card grid.** Upper band = row of smaller "collection" cards, each an image thumbnail on a white elevated card with a two-line caption below (bold title + grey "N saves"). Lower band = larger full-bleed image cards (a black card with an iridescent abstract shape; a "Bread" sky/cloud card with a small inline logo) — variable heights = Pinterest-style masonry.
- No source-list sidebar; navigation is the top pop-up + underline tabs. Content is the hero; chrome is a thin colourless frame around it.

## Signature moves
- **[GOLDEN-NUGGET] Colourless chrome as a gallery wall.** The entire UI is black / white / #FAFAFA / grey with ZERO accent tint anywhere in the chrome (the one blue lives only inside the app icon). The saved design thumbnails — themselves saturated and varied — therefore carry 100% of the screen's colour. The frame recedes so the collection pops. This is the app's whole aesthetic thesis in one decision, and it exploits Von Restorff in reverse: nothing in the chrome competes with the content.
- **The black capsule as the one brand action**, echoed identically from marketing ("Download for Mac") to product ("Library" pill) — a single, consistent, high-contrast action shape. Disciplined action-singularity, even if the colour choice (black, not system accent) is non-native.

## Defects
_(These are **non-native tells with their native corrections**, not macOS-canon defects — lineage is non-native, so they never counted toward canon regardless. Recorded so a future native mock doesn't inherit them.)_
- **Non-native scope switch** → underline tabs (All/Unsorted/Trash) for view scope. Native correction: a segmented control (in-view scope) or a source-list sidebar; underline tabs are a web/iOS import.
- **Accent not bound to system** → the one prominent action is a black filled pill. Native correction: prominent actions bind to the user's system accent (capsule bezel in macOS 27), not a hardcoded brand black.
- **Faked/colourless chrome** → three monochrome grey window dots. Native correction: genuine traffic lights (coloured when focused, grey only when the window is inactive). Ambiguous here — could be a deliberate inactive-window marketing render — so noted, not asserted.
- **Focal-collision: not present** — deliberately avoided; only one prominent action per view. Worth noting as a *pass* against a common anti-pattern.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| Library main window (marketing render) | 9/14 (low-confidence; perspective + single surface) | #1 grid unverifiable through perspective (looks systematic); #10 UI contrast — grey dots/dividers borderline <3:1; #11 Fitts — search glyph + window dots small; #5/#6/#12/#14 N/A (no paragraphs, no visible field bezel, no focus state in a still) |
| — native-tells audit | 3/10 | #1 lineage non-native; #3 selection = underline tabs not inset-rounded accent fill; #6 action is black not accent-bound; #10 faux monochrome window dots; #5/#9 density & toolbar-primary lean non-native. Passes: #2 content opaque/no glass (flat is legitimate), #7 one prominent action, #8 roughly concentric card/thumbnail radii |

**Verdict:** A genuinely well-composed content-forward gallery with a clear, defensible aesthetic thesis (colourless chrome) and disciplined action hierarchy — but it is **not trying to be AppKit-native**, and a single perspective marketing render is thin evidence. Value to the corpus is the *aesthetic pattern* (gallery-white content-forward), not any native token.
