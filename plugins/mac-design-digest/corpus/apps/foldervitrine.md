# FolderVitrine — profile

- **Source:** macapp.supply (cover.webp marketing composite embedding one live app surface) · **Surfaces digested:** folder preview panel (Quick Look-style), light mode · **Last updated:** 2026-07-19
- **One-sentence identity:** A macOS folder Quick Look reimagined as a literal glass display case — the honesty and restraint of a system info panel wearing a translucent Liquid-Glass skin, closest in spirit to Apple's own Quick Look "info" pane crossed with the photo-stack theatricality of a Gallery preview.
- **Cluster:** unassigned (first candidate for a "glass-utility / translucent single-panel" register — needs ≥2 more members before a cluster is honest)
- **Lineage:** native (high) — 13pt-class body, SF Pro throughout, borderless monochrome symbol buttons, capsule progress bar, system identity hues, a genuine floating translucent material. Non-native evidence: none; this reads AppKit/SwiftUI-native.
- **Era (chrome):** Liquid Glass native (macOS 26+ / Tahoe) — the whole panel is a floating refractive material that tints toward the desktop wallpaper behind it.

## Surface identity note

This is **not a standard document window** — there are no traffic lights, which is *correct*: the surface is a floating **folder preview panel** (Quick Look / "space-bar preview" archetype invoked on a folder in Finder). Chrome is honest for that archetype: a custom close (✕) and dismiss (⊘) pair top-left where Quick Look puts them, and a share/export symbol top-right. Judge it against popover/preview-panel grammar, not window grammar.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| chrome/panel-size | ~878 × 580 pt | (measured)(inferred) | edges scanned x≈203→1081, y≈131→711; composite reads ~1× logical, so px≈pt |
| chrome/panel-radius | ~20–24 pt | (estimated)(inferred) | soft corner; large, popover-class radius |
| chrome/panel-material | translucent Liquid Glass, wallpaper-tinting | (measured tint)(inferred) | body sampled #DFF3FF–#E9F4FF over a blue wallpaper — the panel is genuinely see-through, not an opaque near-white |
| chrome/close-dismiss | ~16–18 pt filled translucent-dark circles, top-left, ~16 pt inset | (estimated)(inferred) | ✕ close + ⊘ dismiss; Quick Look-mimic chrome |
| chrome/share | borderless up-from-tray symbol, top-right | (measured)(inferred) | monochrome, no bezel |
| type/section-header | ~17 pt SF Pro Bold, primary label | (estimated)(inferred) | "Types" / "Files" with a leading monochrome symbol; reads Title2-Bold |
| type/title | ~17 pt SF Pro Bold | (estimated)(inferred) | folder name "New Zealand 2016" |
| type/body | ~13 pt SF Pro Regular | (estimated)(inferred) | filenames; matches kit Body 13pt |
| type/metadata | ~12 pt SF Pro, secondary | (estimated)(inferred) | "278 items · 1.84 GB · 9 yr. ago" — middle-dot separated |
| type/group-subheader | ~10–11 pt SF Pro Semibold, tracked UPPERCASE, secondary | (estimated)(inferred) | "IMAGES" file-group header — Finder-style |
| type/timestamp | ~12 pt SF Pro, secondary | (estimated)(inferred) | right-aligned "9 yr. ago" per row |
| accent/type-images | #F48E3C orange | (measured)(inferred) | system-Orange-adjacent (kit light Orange #FF8D28), slightly warmer/muted |
| accent/type-videos | blue (kit-Blue class) | (estimated)(inferred) | film-strip icon + bar segment |
| accent/type-documents | green (kit-Green class) | (estimated)(inferred) | document icon + bar tip |
| viz/type-bar | full-width capsule, ~8 pt tall, 3 proportional segments | (measured)(inferred) | orange 90.6% / blue 7.9% / green 1.4% — maps exactly to 252/22/4 counts (honest data) |
| list/row-pitch | ~34 pt | (estimated)(inferred) | between kit Medium 32 and Large 40 sidebar rows |
| list/row-anatomy | ~18 pt tinted type-icon + 13 pt filename + trailing 12 pt secondary timestamp | (estimated)(inferred) | icon-left, value-left, meta-right |
| list/divider | ~1 pt inset hairline, ~#F2F8FF | (measured)(inferred) | starts after the icon; extremely low contrast on glass (see Defects) |
| layout/body-columns | 2 columns: left preview-stack ~40%, right data column ~55% | (measured)(inferred) | header spans full width above both |

## Layout skeletons

**Folder preview panel (light):**
- Full-width **header band**: top-left close/dismiss circle pair · top-right share symbol · below them a title row = blue folder glyph + bold folder name + secondary middle-dot metadata line (items · size · age).
- **Left column (~40%)**: a *preview-stack collage* — 3–4 real file previews (document, photos, a video) fanned with slight rotation, realistic soft drop shadows, the top one a video showing a play glyph and a 00:05 / 00:10 scrubber. This is decorative-but-real: it is the folder's actual contents, staged as a physical pile.
- **Right column (~55%)**, two stacked sections sharing a left alignment axis:
  - *Types*: bold header + leading bar-chart symbol → full-width proportional capsule bar → horizontal legend (tinted icon + label + secondary count, ×3).
  - *Files*: bold header + leading doc symbol, with two trailing borderless view toggles (grid / recent-clock) → tracked-uppercase group subheader ("IMAGES") → vertical file list, rows divided by inset hairlines.

## Signature moves

- **[GOLDEN-NUGGET] The vitrine itself — an all-translucent single panel.** The app's name (vitrine = glass display case) is executed literally: the entire preview is one floating refractive pane that tints to the wallpaper, with *content rendered directly on the glass* rather than on opaque cards. It is the source of the app's whole character and its whole risk (see Defects #1). Systematic across every region → signature, not accident.
- **[GOLDEN-NUGGET] The staged preview-stack collage.** Turning a mundane "folder contents" thumbnail into a fanned pile of real previews with depth, rotation, drop shadows, and a *playing* video (scrubber + timecodes) is the memorable element — it makes a folder feel like a stack of physical prints. This is where the boldness budget is spent; everything else stays quiet.
- **Honest proportional data-viz.** The Types capsule bar is measured, not decorative: segment widths equal the true 252/22/4 item split, and the three identity hues (orange/blue/green) are reused consistently across bar, legend, and row icons — a disciplined identity-color system, distinct from any app accent.

## Defects

- **Content-on-glass / Contrast Dilution risk** — the file list, dividers, and secondary text sit on the translucent glass, not on an opaque content surface. Liquid Glass grammar reserves glass for the floating layer and keeps *content* (lists/tables) opaque. Here the panel legitimately IS a floating preview, but the scrollable list within it is still content; over a busy wallpaper its legibility is wallpaper-dependent. → Canon would float the panel in glass but seat the list/type rows on an opaque (or high-opacity) content fill.
- **UI contrast failure on dividers** — row hairlines (~#F2F8FF) sit on ~#DFF3FF glass, far below the 3:1 non-text floor. → Darken dividers or use the kit Separator (#3C3C43 @29%) at content opacity.
- **Text contrast (secondary) over translucent glass** — timestamps and metadata in secondary gray over the lighter glass regions read below 4.5:1. → Raise secondary-label opacity or seat text on opaque fill.
- **Target Starvation (borderline)** — the ✕ / ⊘ close-dismiss circles read ~16–18 pt; standalone targets sit under the 24 px WCAG floor unless the hit area is padded (not confirmable from a static render). → Pad hit regions to ≥24–28 pt.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| folder preview panel (light) | 11/14 | #9 secondary text contrast on translucent glass; #10 divider ~1:1 on glass; #11 close/dismiss ~16–18 pt below 24 px floor (padding unconfirmable) |

## Native-tells audit

| Surface | Score | Notes |
|---|---|---|
| folder preview panel (light) | 7/10 (2 N/A) | Fail #2 glass-in-content (list/text on glass vs opaque). N/A #3 no selection state visible, #4 no sidebar. Pass: native lineage, 13pt density, consistent identity-hue binding, one restrained action, borderless grouped symbols, honest preview-panel chrome (correctly no traffic lights) |

## UX psychology

- **Aesthetic-Usability Effect** — the glass + staged photo-stack manufacture a strong ~50 ms first impression and a quality halo; a folder preview *feels* premium before any info is read. The halo buys forgiveness for the contrast costs on first contact — it does not repair them for daily use.
- **Von Restorff / signal-detection** — the fanned preview-stack is the one different thing on the surface, so the eye lands there first; deliberate use of a single focal object.
- **Jakob's Law** — mirrors Quick Look conventions (close top-left, share top-right, space-bar-preview archetype) so users arrive pre-trained. The translucency, though, undercuts the *processing fluency* users expect from a crisp system info panel — the same convention that earns trust also raises the legibility bar it then risks missing.
- **Hierarchy via de-emphasis** — metadata, counts, and timestamps are pushed to secondary gray so filenames and the folder title anchor; the count in "Images 252" whispers relative to the label, appropriate for a legend.

## Notes for synthesis

- Only **one** live app surface exists (the marketing cover embeds it); the gallery is empty. Single-surface app → all tokens `(inferred)`, none promotable. Ask the user for a dark-mode capture and a neutral-wallpaper capture — the glass tint (#DFF3FF here) is wallpaper-driven, so the "true" panel material is under-determined from this one blue-desktop render.
- A **Liquid Glass app icon** (icon.jpg: frosted-glass folder + photo, blue-on-white, soft squircle) also exists but was **not** icon-digested — this pass is Workflow A (UI) only. Flag for a Workflow B pass; it rhymes with the UI's glass-and-blue palette.
- Composite scale is uncertain but reads ~1× logical (panel ~878×580, matching kit example-window scale), so px≈pt was assumed; treat all sizes as estimated ranges.
