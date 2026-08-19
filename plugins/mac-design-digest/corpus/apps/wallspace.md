# Wallspace — profile

- **Source:** macapp.supply (`sources/wallspace/`) · **Surfaces digested:** 1 — main/browse window (dark), from a marketing **cover composite** (no raw screenshots supplied) · **Last updated:** 2026-07-19
- **One-sentence identity:** the App Store "Discover" storefront — cinematic full-bleed hero, glass-pill CTA, peeking card carousels — transplanted onto a Mac wallpaper utility; reads like Apple TV app / Unsplash, not like a native AppKit tool.
- **Cluster:** unassigned (proposed: *photographic-dark-storefront* — consumer media browsers)
- **Lineage:** web-electron (**low** confidence) — non-native evidence, **excluded from macOS canon**. Could equally be a stylized SwiftUI mock or an idealized marketing render; classification rests on styling idioms, not a raw screenshot (see Defects / Notes).
- **Era (chrome):** custom — glassy-dark, but does **not** obey Liquid Glass grammar (glass sits in content); not legacy-native either.

## Provenance caveat (read before trusting any number)

The only evidence is `cover.jpg` (1440×900, category: Utility, tagline "Live wallpaper for Mac"). The app window is rendered **tilted in 3-D perspective** inside a branded backdrop. Every pixel measurement below is therefore `(estimated)` with wide ranges — the perspective warp defeats clean bounding-box measurement, and the canvas scale (retina factor) is unknown. The left half of the cover (wordmark, laurel "2026 Wallpapers" badge, "The Ultimate Wallpaper App" headline, hex watermark) is **brand evidence**, kept separate from the app-window design evidence.

## Tokens

*(All `(estimated)`; perspective-warped marketing render. Brand tokens marked; none feed macOS canon.)*

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/chrome | dark translucent graphite, ~#33383E over content (estimated)(inferred) | | top bar reads as dark material over the hero photo |
| bg/content | full-bleed photographic (no opaque canvas) (estimated)(inferred) | | content *is* the imagery; chrome floats atop it |
| type/wordmark | ~18–22px bold, rounded geometric sans — **not** SF Pro (estimated)(inferred) | brand | in-app header wordmark; matches cover branding |
| type/hero-title | ~34–40px Bold white ("Sea Cliffs") (estimated)(inferred) | | tightly tracked; SF Pro Bold plausible but unconfirmed |
| type/eyebrow | ~10–12px UPPERCASE, tracked +~0.08em, secondary white ("FEATURED") (estimated)(inferred) | | tracked-uppercase eyebrow = web convention |
| type/metadata | ~13–15px secondary white, space-separated ("Mountains  3840×2160  85MB") (estimated)(inferred) | | asset spec sheet under the title |
| type/section-header | ~18–20px Bold white ("Wallspace's Pick") (estimated)(inferred) | | |
| type/subtitle | ~12–13px tertiary gray ("Curated selection…") (estimated)(inferred) | | good de-emphasis vs header |
| nav/segmented | capsule track ~36–42px tall; **white-filled** selected segment + dark text; thin vertical separators (estimated)(inferred) | | iOS/web UISegmentedControl idiom used as **primary nav** |
| button/primary | frosted-translucent **capsule** pill, ~38–44px tall, light fill + dark text + ↗ glyph ("View Wallpaper") (estimated)(inferred) | | glass fill sits **on** the photographic content |
| button/secondary | circular hairline-outline icon button (heart) ~36–40px (estimated)(inferred) | | low-contrast outline over photo |
| radius/card | ~14–18px on carousel thumbnails (estimated)(inferred) | | generous, uniform |
| radius/nav+cta | capsule (infinite) (estimated)(inferred) | | matches macOS 27 capsule bezel direction, if coincidentally |
| carousel | ~6 thumbnails visible, ~150–170px wide, one with a light selection ring; strip bleeds off right edge (estimated)(inferred) | | "peek" affordance inviting horizontal scroll |
| accent/system | **none evident** — selection & CTA are white/neutral, not a system-accent hue (estimated)(inferred) | | no `controlAccentColor` binding visible |
| traffic-lights | red + amber + **gray** third (not green) (estimated)(inferred) | | faked/custom chrome — focused window should show green |

## Layout skeletons

**Main / browse window (dark, single surface).** Vertical scroll of a media storefront:
- **Top bar (floating, translucent-dark):** leading = app icon + "Wallspace" wordmark; trailing-right = 3-segment capsule nav `Home | Explore | Library` (Home selected). No native toolbar anatomy (no leading sidebar toggle, no centered title, no trailing primary-action + search).
- **Hero (full-bleed photo, ~45–50% of window height):** bottom-left text stack — eyebrow "FEATURED" → title "Sea Cliffs" → metadata line → action row (frosted capsule CTA + heart icon). All left-aligned to a shared left margin (~24–32px inset).
- **Carousel strip:** horizontal row of rounded thumbnails, one ring-selected, bleeding off the right edge.
- **Sectioned grid:** "Wallspace's Pick" header + subtitle, then a card grid beginning at the cut-off bottom edge.
- **Alignment:** hero text stack, section header, and left content margin appear to share one vertical axis — the layout's strongest native-adjacent discipline.

## Signature moves

- **Storefront-hero transplant** `[GOLDEN-NUGGET]`: the entire identity is a cinematic full-bleed featured image + glass CTA + peeking carousels — App Store Discover / Apple TV grammar. It's *systematic and purposeful* (a wallpaper app's value literally IS the imagery, so content-as-hero is the right bet), but it's a **borrowed template identity**, not a bespoke one — competent-generic rather than distinctive to Wallspace.
- **Spec sheet under a cinematic title** (the one genuinely app-specific choice): "Mountains  3840×2160  85MB" sits directly under the glossy "Sea Cliffs" headline — utility honesty (resolution + file size, the things a wallpaper buyer actually needs) poking through the glossy shell. Small, but it's the app's own.

## Defects

- **Glass-in-content (Liquid Glass golden-rule violation)** → the frosted "View Wallpaper" capsule and the translucent top bar are rendered as glass sitting *on* photographic content; native glass belongs only to the floating functional layer, with content opaque. Canon: opaque controls over content, or a solid scrim, reserving glass for true chrome.
- **Segmented control as primary navigation** → `Home | Explore | Library` is a filled-segment pill doing main-window view switching. HIG explicitly lists this as a non-native mistake ("use a tab view; keep segmented controls to toolbars/inspectors"; "a toolbar is not a tab bar"). Canon: a source-list sidebar or a real tab view.
- **Faked / custom chrome** → the third traffic light is **gray, not green**, on an apparently focused window; the top bar is a hand-drawn branded header, not `NSToolbar` anatomy. HIG: use the real traffic lights, never hand-draw a toolbar over fake chrome.
- **Tracked-UPPERCASE eyebrow** ("FEATURED") → web/marketing convention; native section/eyebrow labels are sentence-case system font.
- **Contrast Dilution over imagery** (#9/#10) → secondary-white metadata/eyebrow and the hairline frosted CTA + heart outline + carousel ring risk falling below 4.5:1 (text) / 3:1 (non-text) where they overlap mid-tone regions of the photo, with no guaranteed scrim. Canon: a legibility gradient behind overlaid text, solid enough control edges.

## Rubric history

| Surface | Score | Native audit | Failures |
|---|---|---|---|
| main/browse window (dark, marketing composite) | 11/14 | 2/10 | 14-pt: #1 grid unverifiable (perspective warp), #9 text-over-imagery contrast risk, #10 frosted UI/outlines <3:1 over photo. Native: #1 lineage non-native, #2 glass-in-content, #3 white-filled (non-accent) selection grammar, #5 consumer/web density & oversized controls, #6 no accent binding, #9 header-is-not-a-toolbar, #10 faked traffic lights. Passes: #7 one prominent action; hierarchy/de-emphasis (#7 14-pt) & alignment (#2/#3 14-pt) are the surface's real strengths. |

## Notes for synthesis

- **Do not promote anything from Wallspace toward macOS canon** — non-native lineage + marketing-composite provenance + single surface. It is at best *contrast evidence* for "what a consumer media-storefront look does on Mac."
- Icon (`icon.png`, 512²: dark rounded-square, white 4-point sparkle) was supplied but **not digested** — this task is Workflow A only. Flag for a future Workflow B pass.
- If a *real* screenshot surfaces later, re-digest: lineage may resolve toward SwiftUI, and true measurements would replace every `(estimated)` token here.
