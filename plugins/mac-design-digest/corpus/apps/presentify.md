# Presentify — profile

- **Source:** macapp.supply (cover marketing composite only; no standalone shots supplied) · **Surfaces digested:** floating annotation toolbar, Preferences window (Cursor tab), Spotlight/Zoom lens (feature output) · **Last updated:** 2026-07-19
- **One-sentence identity:** A screen-annotation overlay utility whose entire "app" is a dark floating tool-capsule plus a spotlight lens designed to disappear over any other app's content — Epic Pen / ZoomIt's job, dressed in a playful purple consumer-indie brand.
- **Cluster:** unassigned (candidate: `consumer-utility-overlay` / menu-bar-utility — sole member so far)
- **Lineage:** native (high) — real macOS traffic lights + centred titlebar, a classic AppKit Preferences `NSToolbar` icon-over-label tab bar, 13pt-class desktop density, native `NSSlider` rows, borderless floating `NSPanel` for the tool bar. Non-native evidence: none observed.
- **Era (chrome):** big-sur / legacy-native — flat opaque black tool panel (no Liquid Glass lensing, no scroll-edge effect, no capsule-glass container morphing); Preferences uses a modern System-Settings-adjacent stacked-label form but a pre-Tahoe icon-tab toolbar. No macOS 26+ glass evidence.

> **Provenance caveat (applies to every measured token below):** the only input is a 1200×630 JPEG marketing composite. The app windows sit small and rotated-flat inside it at an unknown scale, so absolute pixel/point values are unrecoverable — readings are recorded as ratios, structure, and colour, all `(estimated)` with wide bands. No standalone @1×/@2× app screenshot exists to promote these to `(measured)`. Request real capture of the toolbar + Preferences to firm these up.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/purple | ~#7C3AED→#A855F7 gradient (estimated)(confirmed) | | icon squircle, cover backdrop, and Preferences slider fill all share it — the through-line identity |
| chrome/annotation-bar-bg | near-black opaque ~#0B0B0E (estimated)(inferred) | | always dark regardless of desktop; not glass, not translucent — an opaque float-over-anything panel |
| chrome/annotation-bar-radius | ~8–10px continuous, capsule-ish ends (estimated)(inferred) | | |
| palette/annotation-inks | 5 swatches: cyan/blue, red, green, yellow, purple (estimated)(inferred) | | leading control group; reads as system-hue-adjacent but cyan runs brighter than kit Blue `#0088FF` |
| glyph/tools | monochrome white SF-Symbol-class: pen/line, freehand, rectangle, ellipse, text (T), highlighter + shuffle (estimated)(inferred) | | one icon size, borderless, grouped by thin dividers |
| type/settings-label | ~13px SF Pro, primary/dark (estimated)(inferred) | | row title tier |
| type/settings-desc | ~11px SF Pro, secondary gray (estimated)(inferred) | | one-sentence helper under each label — recognition-over-recall |
| accent/controls | purple slider fill (estimated)(inferred) | | either brand-purple hardcoded over `controlAccentColor`, or user accent set purple for the shot — cannot disambiguate from one still |
| bg/settings-canvas | white / ~#F5F5F7 light (estimated)(inferred) | | Preferences is light mode; tool bar is dark mode — two fixed appearances, not one theme |
| chrome/prefs-toolbar | icon-over-label tabs ×5: General · Annotate · Cursor · Shortcuts · About (estimated)(confirmed) | | classic AppKit preferences pattern; Cursor tab selected |
| annotation/callout | rounded-rect, coloured 1–2px border + matching coloured text ("This is Presentify!") (estimated)(inferred) | | output styling of the text tool; border colour = ink colour |

## Layout skeletons

**Floating annotation toolbar** (Presentify's primary UI, over other apps' content): a single horizontal dark capsule. L→R: drag handle (‖) · five circular colour-ink swatches · divider · shuffle/randomise glyph · divider · draw-tool cluster (line/pen, freehand, rectangle, ellipse, text T) · divider · highlighter. Monochrome glyphs, colour reserved entirely for the ink swatches. No visible tool-selection state in this still.

**Preferences — Cursor tab** (light): 33pt-class titlebar (traffic lights left, centred title "Cursor") → borderless icon+label toolbar of 5 tabs → scrollable content of grouped form rows. Each row = left stack of [primary label / secondary one-sentence description] + right-aligned control (mostly sliders). Section header "Spotlight" in secondary colour separating groups. A rounded "Zoom" popover/callout floats over the content demonstrating a control ("Zoom Level — The magnification level (2.0× zoom)"). Controls right-edge-aligned to a shared axis.

**Spotlight/Zoom lens** (feature output, not chrome): a bright circular magnifier following the cursor, surroundings dimmed — the app's on-screen effect, shown over a presentation slide.

## Signature moves
- **Colour-swatch-first toolbar.** The five annotation inks lead the bar, before any tool — colour is the fastest, most-frequent choice for a live annotator, so it's promoted to the primary position and given the only saturation on an otherwise monochrome bar (Von Restorff: the colour *is* the differentiated element).
- **Chrome engineered to float over the whole OS.** The product is almost entirely a borderless dark panel + a spotlight lens; the "app" is designed to be invisible except its tools, sitting on top of Xcode, Keynote, a browser — whatever is being presented. Opaque-dark (not glass) is the deliberate legibility choice for "readable over any background."
- **Two-tier self-teaching settings rows.** Every Preferences control pairs a bold label with a full explanatory sentence ("The size of the spotlight area…"), trading density for onboarding-free recognition — appropriate for a consumer utility whose users configure once.

## Defects
- **Provenance ceiling, not a design defect:** accessibility floors (4.5:1 text, focus appearance #14, ≥24px hit targets on the small tool glyphs) are unverifiable from the composite — record as unknown, not pass/fail.
- **Possible accent-binding tell (contested):** purple slider fill may indicate brand purple hardcoded over the user's system `controlAccentColor` — a native-feel tell if so (accent should be the *user's*). Cannot distinguish a hardcoded tint from a user accent set to purple in one still; leave `(contested)` pending a capture with a known-non-purple system accent.
- **No visible selection grammar on the tool bar:** which draw tool / ink is active isn't legible here — likely present but unconfirmed.

## Rubric history
| Surface | Score | Failures / notes (marketing-composite, all estimated) |
|---|---|---|
| Annotation toolbar | ~11/14 | many checks n/a (no body text: #5,#6,#9); #14 focus unverifiable; #11 hit-target size on ~14–16px glyphs unconfirmed |
| Preferences (Cursor) | ~12/14 | #14 focus appearance not visible; #11 fine under macOS pointer calibration; strong on #7 de-emphasis (label/description two-tier) |
| Native-tells audit | ~9/10 (both surfaces) | #6 accent binding contested (purple); #3 selection grammar unconfirmed on toolbar; #2 glass legitimately absent (opaque overlay + light forms), not a miss |

## Brand evidence (not a UI digest)
- **App icon** (Workflow A run — icon NOT formally digested; noted as brand context only): Big-Sur-era layered-material squircle, purple gradient ground, a light lavender/white presentation easel-on-tripod glyph with soft dimensional depth and a purple board. Rhymes with the Keynote-lectern family of "presentation" icons but uses a flip-chart easel. Reinforces the purple identity carried through backdrop and slider accent. A full 12-point icon digest (Workflow B) is deferred.
- **Marketing composite (brand, not app):** drenched purple gradient, SF-Pro-class white headline with a bold-weight emphasis span, three faux laurel-wreath "award" badges — consumer-approachable, committed single-hue colour strategy. Analysed as brand, never conflated with the app chrome (which is restrained and monochrome).
