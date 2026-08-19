# Compresto — profile

- **Source:** macapp.supply (cover composite only; gallery empty) · **Surfaces digested:** main window (single-window utility, light mode) · **Last updated:** 2026-07-19
- **One-sentence identity:** Permute's drop-grid-plus-inspector converter layout dissolved into wallpaper-tinted Liquid Glass — a batch media compressor that wants to feel like light, with one candy-blue Compress button as its whole action layer.
- **Cluster:** unassigned (suggested: *warm-glass consumer utility*)
- **Lineage:** native — SwiftUI on macOS (med-high). Native double-chevron pop-up buttons, native `NSSwitch` toggles, real traffic lights + centered title + borderless SF Symbol toolbar, bordered push buttons, and SwiftUI `Form`-style grouped rounded sections. The inset-grouped rounded cards are SwiftUI's macOS form grammar, **not** a Catalyst/iOS tell.
- **Era (chrome):** Liquid Glass native (macOS 26/Tahoe era) (med). Capsule primary button, translucent unified titlebar, whole-window vibrancy. Caveat: era read leans on the glass material; the pop-up chevron squares don't clearly show accent tinting.

> **Evidence caveat (read first):** the only input is a marketing cover — the app window composited over a saturated flower-field wallpaper. The window's translucency is real (a genuine material choice), but its *intensity* here is exaggerated by the deliberately vibrant backdrop; over a neutral desktop the wallpaper-bleed would read milder. All window-background colour tokens are wallpaper-contaminated and marked accordingly. No dark-mode, no interaction/selection/focus states, no settings surface seen.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| chrome/window-material | translucent whole-window material, warm wallpaper-tinted; cool-light at top, warm amber at bottom | (estimated)(inferred) | Not opaque — content grid AND inspector sit on the same translucent sheet; see Defects (glass-in-content) |
| chrome/titlebar | unified translucent, ~33pt; centered bold title "Compresto"; 3 trailing borderless SF Symbols (pin / clipboard / gear), one group | (estimated)(inferred) | matches kit 33pt Default titlebar; traffic-light cluster measured |
| chrome/traffic-lights | 68×14pt cluster; red dot ⌀~12pt; red→green centers ~40pt | (measured)(inferred) | used as scale anchor → ~2.26 px/pt (≈@2x, slightly upscaled) |
| type/title | ~15–17pt, bold, centered | (estimated)(inferred) | Title3/Title2 emphasized class |
| type/row-label | ~13–14pt, regular, primary label (near-black) | (estimated)(inferred) | "Output folder", "Video quality" — cap-height 23px raw on "Input files (5)" |
| type/secondary | ~11–12pt, secondary label | (estimated)(inferred) | "~/Desktop/", "Target file size" — smaller + lighter |
| type/popup-value | ~13–14pt, primary weight (same as label) | (estimated)(inferred) | "Custom", "Same as input", "PNG" — value not de-emphasized vs its row label |
| action/primary | full-width capsule, ~265×42pt; fill `#0075F0`; label `#5FFCFF` cyan, bold | (measured)(inferred) | fill ≈ system Blue light `#0088FF`; cyan-on-blue label ≈ **3.5:1** — see Defects |
| control/pop-up | native pop-up button, double up/down chevron, ~24–28pt tall, ~6pt radius, neutral fill | (estimated)(inferred) | correct pop-up grammar (title shows current value) |
| control/switch | native `NSSwitch` capsule, off/white knob on gray track | (estimated)(inferred) | "Remove input files", "Remove audio" |
| control/bordered-button | gray Bordered push buttons ~24pt, ~6–8pt radius | (estimated)(inferred) | [Clear] [Change] — neutral, recessive |
| control/text-field | recessed gray field ("2"), ~24–28pt | (estimated)(inferred) | paired with a KB pop-up (unit) |
| radius/group-card | inspector grouped sections ~10–12pt | (estimated)(inferred) | SwiftUI Form section background |
| radius/thumb | media thumbnails ~12–16pt | (estimated)(inferred) | masonry grid |
| radius/pill | file badges + filename strips = capsule (glass pills) | (estimated)(inferred) | white translucent, dark text, over media |
| accent/primary | system blue ~`#0075F0` | (measured)(inferred) | bound only to the one CTA; possibly hard-coded rather than `controlAccentColor` |
| layout/split | two-column: left media grid (~2-col masonry, ~55% width) · right inspector panel (~40–42% width) | (estimated)(inferred) | classic converter layout |

## Layout skeletons

**Main window (single window, no sidebar).**
- **Titlebar (unified, translucent):** traffic lights leading · centered "Compresto" title · trailing icon group of 3 (pin = always-on-top, clipboard = paste, gear = settings). One toolbar group, borderless monochrome symbols — HIG-correct.
- **Left column (~55%):** masonry/media grid of input files, ~2 columns of variable-height rounded thumbnails. Each tile: top-left glass **pill badge** (`JPG | 1.3 MB`, `MP4 | 275.1 MB`, `PDF | 6.4 MB`), bottom **filename capsule strip**; the video tile adds a pink circular play glyph + a red duration pill (`0908`). Tiles float on the warm translucent ground.
- **Right column (~40%) — inspector/settings panel:** vertical stack of SwiftUI-`Form` grouped rounded cards, each a run of label-left / control-right rows with hairline internal dividers:
  1. `Input files (5)` → [Clear] [Change]
  2. `Output folder` [Custom ▾] · `~/Desktop/` [Change] · `Remove input files` [switch]
  3. `Video quality` [File size ▾] · `Target file size` [2] [KB ▾] · `Video resolution` [Same as input ▾] · `Video format` [MP4 ▾] · `Remove audio` [switch]
  4. `Image quality` [Good ▾] · `Image size` [Same as input ▾] · `Image format` [PNG ▾]
  5. `PDF quality` [Balance ▾]
- **Panel footer:** full-width capsule **Compress** primary button pinned to the bottom of the inspector column.
- Alignment: clean two-column split; inspector rows share a right edge for controls and a left edge for labels; group cards inset with equal gutters.

## Signature moves

- **[GOLDEN-NUGGET] Wallpaper-tinted whole-window glass.** The app refuses an opaque content surface: the media grid and the settings inspector both sit on one translucent sheet that takes its warmth from the desktop behind it (cool at the sky, amber at the flowers). It's the entire personality in one material decision — "a compressor that feels like light." It is also the app's biggest native-grammar liability (glass-in-content, see Defects). Systematic across the whole window → recorded as a signature *and* a defect; the readability cost is real but the identity is unmistakable.
- **[GOLDEN-NUGGET] The candy-blue Compress bar.** One full-width capsule, saturated system blue, with a *cyan* label instead of white — a deliberately sweet, glowing CTA that is the sole saturated element in an otherwise warm-neutral field. Excellent Von Restorff / action-singularity behaviour (you cannot miss the one thing to do), undercut by a ~3.5:1 label contrast.
- **Glass pill metadata over media.** Format/size badges and filenames ride the thumbnails as translucent capsules rather than a caption bar — legible over any image, on-brand with the glass theme.

## Defects

- **Glass-in-content (native anti-pattern)** → the thumbnail grid and inspector form sit on translucent, wallpaper-tinted material; HIG reserves glass for the floating functional layer and keeps content opaque. → Canon: content stays opaque; put vibrancy only on toolbar/sidebar/floating chrome. *(Mitigation: intensity is amplified by the marketing wallpaper; treat as a real-but-softened concern until a neutral-desktop shot is seen.)*
- **Contrast Dilution / low-contrast prominent label** → cyan `#5FFCFF` on blue `#0075F0` ≈ 3.5:1. Clears the 3:1 large-text floor (the label is bold/large) but is **below the 4.5:1 the HIG explicitly requires on a prominent tint**. → Canon: white (or ≥4.5:1) label on the accent fill.
- **Faint UI contrast** → inter-row hairline dividers and group-card edges over the warm translucency read very light, likely <3:1 (rubric #10). → Canon: separators ≥3:1 (kit separator `#3C3C43` @29% on an opaque ground).
- **Flat label↔value hierarchy (minor)** → within pop-up rows the label ("Video format") and the current value ("MP4") share weight/darkness; native forms usually let the label recede. Low severity — the value is inside a control.
- **Hard-coded accent (possible)** → the CTA fill may be a hard blue rather than bound to `controlAccentColor`; HIG says tint the primary with the user's accent, not a brand hex. Can't confirm from one shot.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| main window (light) | 12/14 | #9 text contrast (Compress cyan-on-blue ~3.5:1, below 4.5:1) · #10 UI contrast (hairline dividers/card edges <3:1 over translucency). #14 focus not observable in a static cover (n/a, not counted). |

## Native-tells audit (10-point)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | AppKit-native / SwiftUI | PASS | native pop-ups, `NSSwitch`, bordered buttons, SwiftUI Form grouping |
| 2 | Glass only on floating chrome; content opaque | **FAIL** | whole-window translucency; grid + inspector on wallpaper-tinted glass |
| 3 | Selection grammar | n/a | no selected row visible |
| 4 | Sidebar headers | n/a | no sidebar |
| 5 | Density (13pt body, 20–28pt controls, desktop rows) | PASS | ~13–14pt labels, pop-ups ~24–28pt, rows ~28pt (Compress oversized) |
| 6 | Accent bound consistently | MARGINAL | one blue CTA; possibly hard-coded; low-contrast cyan label |
| 7 | One prominent action; button grammar | PASS (noted) | single Compress primary; but full-width + oversized vs "prominent not larger" |
| 8 | Concentric corners; child < parent | PASS (est) | cards/thumbs/pills step plausibly |
| 9 | Toolbar: borderless symbols, grouped, single primary | PASS | 3 trailing SF Symbols, one group; primary lives in content (ok) |
| 10 | Real chrome | PASS | genuine traffic lights, centered title, translucent unified bar |

Applicable passes ≈ 7/10 (1 fail #2, 1 marginal #6; #3/#4 n/a).
