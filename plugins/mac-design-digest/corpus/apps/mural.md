# Mural — profile

- **Source:** macapp.supply (muralflow.com) · **Surfaces digested:** My Mural / Active Wall (frame-select + loop-range modes), Themes / Atmosphere coverflow (×3 rows), Lab / Grading inspector · **Last updated:** 2026-07-19
- **One-sentence identity:** a color-grading suite bolted onto a live-wallpaper manager — "iOS Photos' coverflow and a DaVinci-style grading panel wrapped in a Mac frame," moody lofi-media aesthetic, consumer not pro.
- **Cluster:** unassigned (candidate: *consumer-media-dark* / iOS-influenced creative utility)
- **Lineage:** catalyst / iOS-influenced SwiftUI (med confidence) — real Mac frame (genuine traffic lights, full-height source list) wrapping an iOS-density body. Non-native evidence below never feeds macOS canon.
- **Era (chrome):** custom flat-dark on a macOS 26/27-era frame — **not Liquid-Glass-committed**; the one translucent element is a floating filmstrip HUD over the video preview. Content surfaces are flat opaque.

## Lineage evidence (why catalyst, not AppKit-native)

Judge from the body, not the frame. Density is the discriminator and every reading points iOS-ward:
- Nav labels ~15–17pt (not 13pt macOS body); large titles ~40pt (kit LargeTitle is 26pt); section headers ~20–24pt.
- Primary action row is four ~66pt-tall rounded "cards" (Import / Done / Loop / Mixer) — iOS touch-density, not 24–28pt native push buttons.
- Themes browses via a 3D **coverflow carousel** (one focal card, perspective siblings, chevron paging) — an iOS/iTunes gesture, never a native macOS browse pattern.
- Inspector section headers set **tracked uppercase** (PRESETS, MANUAL CONTROL).
- Counter-evidence that keeps it "Mac frame, iOS body" rather than pure iOS-on-Mac: genuine traffic-light chrome, a real three-pane split (sidebar / canvas / inspector), and **native-looking linear sliders** (blue minimal fill + round knob) in the Lab panel.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/content | #323232 (measured)(confirmed) | | main canvas area, dark mode |
| bg/sidebar | #2B292B (measured)(confirmed) | | full-height source list, ~gray-43 |
| bg/inspector | #2B2B2B (measured)(inferred) | | Lab right panel — darker than content, base-vs-elevated split (rails dark, canvas lighter) |
| accent/primary | ~#0088–0091FF system blue (measured)(confirmed) | | selection text+glyph, slider fill (#177BE6), DYNAMIC badge |
| accent/confirm | ~#30D158 system green (measured)(confirmed) | | "Done" action check + selected-state border; a 2nd semantic accent |
| selection/fill | translucent blue ~#254D8E (measured)(inferred) | | nav pill fill; **blue-tinted fill + blue label**, not native gray-inset nor white-on-accent |
| label/secondary | #AAAAAA (measured)(confirmed) | | subtitles, uppercase section headers |
| traffic-lights | std #FF5F58 / #F2BB2F / #2DC241 (measured)(confirmed) | | genuine, inset ≈ (11, 7)pt → compact/no-toolbar archetype |
| type/large-title | ~40pt Bold SF Pro (estimated)(confirmed) | | "Active Wall" / "Atmosphere" — oversized vs 26pt kit |
| type/section-header | ~20–24pt Semibold + leading SF Symbol (estimated)(confirmed) | | "Lofi Focus", "Wild Quiet", "Film Scene" |
| type/nav-label | ~15–17pt (estimated)(confirmed) | | iOS-density, not 13pt |
| type/inspector-header | ~11pt tracked UPPERCASE, #AAAAAA (measured)(inferred) | | non-native — HIG wants sentence-case semibold |
| type/card-eyebrow | ~10–11pt tracked UPPERCASE white/gray (measured)(confirmed) | | "RAIN AGAINST THE GLASS", "LOFI BEATS" — editorial device on media cards |
| chrome/sidebar-width | ~220pt (measured)(inferred) | | full-height, transparent titlebar (lights float on sidebar top), no toolbar row |
| chrome/inspector-width | ~277pt (measured)(inferred) | | Lab only |
| radius/preview-card | ~16–20pt (estimated)(inferred) | | wallpaper preview + coverflow cards |
| radius/action-button | ~12pt (estimated)(inferred) | | the four bottom action cards |
| radius/preset-card | ~10pt (estimated)(inferred) | | Grading preset 2-col grid |
| slider/style | native linear: blue fill + light round knob on ~#2B track (measured)(inferred) | | the most native control in the app |

## Layout skeletons

**My Mural / Active Wall** — Full-height ~220pt source list (Mural logo+wordmark top; nav: My Mural / Themes / Lab; pinned bottom: Dynamic Lock Screen, hairline, Preferences). Content: oversized left-aligned title "Active Wall" + trailing "DYNAMIC" blue capsule badge; centered 16:9 wallpaper preview (~16pt radius) with a translucent floating filmstrip HUD (Close · Select Frame/Set Loop Range + frame thumbnails, yellow range handles in Loop mode); below the preview a row of four ~66pt action cards, exactly one carrying a green selected/confirm treatment.

**Themes / Atmosphere** — Same sidebar. Content: oversized title + one-line secondary subtitle; a labelled section row ("Lofi Focus" etc. with a leading SF Symbol); a **3D coverflow** of media cards — one centered focal card (title + tracked-uppercase eyebrow bottom-left), perspective-skewed neighbors, left/right chevrons; a down-chevron affordance signalling vertical paging between section rows.

**Lab / Grading** — Three panes. Sidebar; center canvas = live wallpaper preview with a top icon-tab strip (Grading / Widgets / Mantra / Ambience) and a corner "Mixer" overlay; right ~277pt inspector: title + subtitle, "PRESETS" tracked-uppercase header over a 2-col grid of preset chips (each a colored system-palette dot + name/descriptor, selected chip checkmarked), "MANUAL CONTROL" header over labelled native sliders (Temp/Saturation/Brightness/Contrast/Scanline/Grain with right-aligned numeric readouts), pinned Reset · Applied footer.

## Signature moves
- **[GOLDEN-NUGGET] The wallpaper-as-footage conceit.** Lab treats a desktop background like a video-grading timeline: cinematic LUT presets (Noir/Cinematic-Teal/Cyber-Neon/Warm-Gold) plus Scanline and Grain sliders, and the Active Wall view has per-frame selection + loop-range scrubbing. The entire product personality is "a VJ/color-grading rig for your desktop," and it's carried consistently across all three surfaces.
- **Coverflow theme browser.** The perspective carousel is the app's most memorable gesture and its clearest brand signature — also its biggest native-lineage liability (see Defects).
- **Content-mirrors-chrome palette.** The UI's moody purple/blue-black dark theme is chosen to disappear into the lofi/vaporwave imagery it manages — the app looks like its own wallpapers.

## Defects
- **Non-native density (systematic tell, not a defect per se):** ~40pt titles, ~66pt action cards, ~15–17pt nav — iOS sizing inside a Mac frame. Excluded from macOS canon.
- **Tracked-uppercase section headers** (PRESETS / MANUAL CONTROL) → HIG wants system-font, semibold, secondary-colour, sentence/title case. The #1 sidebar/inspector authenticity tell.
- **Coverflow for primary browsing** → Jakob's Law violation; native would be a grid or list. Also only the focal card is legible — discoverability cost for the flanking themes.
- **Selection grammar drift:** blue-translucent fill + blue label, rather than the native flat gray inset (or System Settings' white-on-solid-accent). Reads intentional but non-standard.
- **UI-contrast dilution (rubric #10):** unfilled slider tracks and preset-card borders sit near-invisible on the #2B inspector (<3:1); low-contrast chevrons on the coverflow.

## Rubric history
| Surface | Score | Failures | Native audit |
|---|---|---|---|
| Lab / Grading inspector (shot-6) | 12/14 | #10 UI contrast (unfilled tracks, card borders <3:1) | 7/10 — #1 lineage, #4 uppercase headers, #5 density |
| Themes / Atmosphere coverflow (shot-3/4/5) | 12/14 | #10 low-contrast chevrons | 7/10 — #1 lineage, #5 density, coverflow non-native browse |
| My Mural / Active Wall (shot-1/2) | 13/14 | #10 subtle action-card borders | 7/10 — #1 lineage, #5 density; good #7 action singularity (single green primary) |

## Notes
- Cover.png is a marketing composite (Creation-of-Adam parody, brush-script wordmark, "SCROLL TO ENTER") — brand evidence only; the embedded window is too small to measure and is superseded by the shots.
- The recurring "SILENCE / lofi girl" wallpaper and all card imagery are *content*, not UI — the serif "SILENCE" wordmark is inside the artwork, not an app type choice.
- All pixel values are @2x screenshot estimates (single app → `(inferred)`), tonal backgrounds `(measured)`. No light-mode surface, no Preferences/Settings window, no text-field or menu surface seen — bring those to promote tokens.
