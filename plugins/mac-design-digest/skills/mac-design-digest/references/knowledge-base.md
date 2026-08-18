# Operationalising UI Design Quality — Knowledge Base

Deep-research synthesis (Gemini Deep Research, 2026-07) on what observably distinguishes excellent UI from mediocre UI, operationalised for screenshot analysis and mock generation. Formula images from the original export have been replaced with their textual values. Confidence qualifiers are the original researcher's.

**How to use this file:** the Screenshot Evaluation Rubric (§7) is the per-screenshot checklist. The Anti-Pattern Taxonomy (§6) names defects. The Convergence Table (§5) separates universal principles from platform conventions. §§1–4 are the evidence behind them — read when a rubric result needs explaining.

## Executive summary

- (High) **The 8-point spatial grid is universal.** All surveyed mature design systems (Material 3, Apple HIG, Fluent 2, Carbon, Polaris) rely on a base-8 or base-4 spatial grid for component dimensions, padding, and margins. Deviation from this scale is the primary operational identifier of mediocre, non-systematic UI.
- (High) **Typography follows strict mathematical ratios.** Excellent UI uses modular type scales (e.g., Major Third 1.250, Minor Third 1.200) rather than arbitrary pixel sizes. Line height is inversely proportional to font size: ~1.5× for body, 1.1–1.25× for headings.
- (High) **Hierarchy relies on de-emphasis, not amplification.** Professional interfaces push secondary elements back (weight reductions, gray-900 → gray-500 shifts) rather than making primary elements ever louder.
- (Medium) **Density must adapt to platform intent.** HIG and M3 favour breathable, touch-friendly density (44pt/48dp targets); enterprise systems (Carbon) intentionally deploy high-density, sharp-cornered (0px radius) elements.
- (High) **WCAG 2.2 contrast and focus appearance are mandatory quality thresholds.** 4.5:1 text, 3:1 non-text, and focus indicators with area ≥ a 2px perimeter of the component.
- (High) **Layouts are governed by 12-column grids** with fixed gutters (16–24px) and responsive margins.

## 1. Observable properties that distinguish excellent from mediocre UI

The distinction is fundamentally rooted in **mathematical consistency and the elimination of arbitrary visual decisions**. Expert interfaces are built from tightly constrained token sets; a static screenshot can be evaluated by reverse-engineering the underlying mathematics.

### Spacing and layout harmony
- Standard: 8-point grid, with 4-point sub-grid for high-density micro-adjustments. Every measurable dimension — padding, margin, gap, component height, icon size — is a multiple of 8 (or 4).
- Rationale: common resolutions divide cleanly by 8, avoiding half-pixel blur.
- Screenshot check: measure pixel distances between bounding boxes of adjacent elements; a systematic UI yields values mapping to the base-8 array. Mediocre UI reveals "magic numbers" (13px, 27px).
- Gestalt proximity: spacing *between* groups must be mathematically larger than spacing *within* a group.

### Typography and vertical rhythm
- Modular scale: sizes progress by a fixed ratio (Minor Third 1.200, Major Third 1.250). E.g., 16px base × 1.25 → 20, 25, 31, 39.
- Inverse line height: body 14–16px → ~1.5× (24px); display ≥36px → 1.1–1.2×.
- Screenshot check: extract text bounding-box heights; compute height-to-font-size ratios.

### Visual hierarchy and colour logic
- Hierarchy through **de-emphasis**: secondary metadata, timestamps, labels get lighter tokens (gray-900 → gray-500) and reduced weights, letting primary data anchor attention.
- Palette constraint: backgrounds/large surfaces use highly desaturated tints (HSL saturation <10%, lightness >95%); full saturation is reserved for interactive primaries (CTAs).
- Practitioner heuristic: design in grayscale first — hierarchy must survive without colour.

### Alignment and density
- Alignment maps to a 12-column grid: left/right edges of distinct blocks share exact X-coordinates dividing the container into clean fractions.
- Density is contextual but intentional: touch-first ≥44pt/48dp targets; enterprise (Carbon) compresses line-heights and paddings while still honouring the grid.

| Principle | Observable evidence in a screenshot | Operational rule for generation | Source system(s) | Confidence |
|---|---|---|---|---|
| Base-8 spatial grid | Gaps between bounding boxes divide cleanly by 8 (or 4 for micro-spacing) | Select all padding/margin/gap values from [4, 8, 16, 24, 32, 48, 64, 96] | Fluent 2, M3, Carbon | High |
| Inverse line height | Text-block heights show line-height ratios that fall as font size rises | line-height 1.5 for sizes ≤16px; 1.1–1.2 for sizes ≥36px | M3, Refactoring UI | High |
| Hierarchy via de-emphasis | Labels/secondary metadata have lower contrast and thinner weight than primary values | Label text → gray-500 equivalent; value text → gray-900 at heavier weight | Refactoring UI | High |
| 12-column alignment | Left/right edges of distinct blocks share exact X-coordinates | Containers span integer multiples of a 12-column grid | Polaris, Carbon | High |
| Gestalt proximity spacing | Header-to-content gap is strictly smaller than section-to-section gap | Between-section margin ≥ 2× the largest within-section gap | Refactoring UI | High |

## 2. Cross-system convergence: universal principles vs. platform conventions

### Convergent (universal) principles
1. **Tokenization.** Every mature system has abandoned hard-coded values for a tiered token architecture: *primitive* (blue-500, spacing-16) → *semantic* (color-action-primary) → *component* (button-background-color-hover). Generated specs must emit semantic tokens; raw values can't adapt to dark mode or density preferences.
2. **Baseline accessibility as layout constraint.** WCAG 2.2 AA contrast (4.5:1 text, 3:1 large text/non-text) everywhere; components sized by padding rather than fixed heights so text can scale to 200% (WCAG 1.4.4) without breaking.
3. **Zero-default layout primitives.** Structural components (Stacks, Boxes, Grids — Polaris) ship with zero default spacing; all gaps are explicit tokens.

### Divergent (platform conventions)
- **Shape:** M3 uses an expressive 10-step radius scale (0–48dp + full pill); Fluent 2 defaults 4px (2px small); Carbon is the outlier at 0px sharp corners for enterprise density.
- **Elevation:** Apple HIG leans on depth via background blur (vibrancy/materials), translucency, and subtle physical shadows; M3 replaced heavy shadows with *tonal elevation* (surface lightness steps).

**Decision rule for generation:** treat the 8-point grid, semantic tokens, touch-target minimums, and WCAG contrast as immutable laws. Treat radius, shadows, and font families as configurable conventions. "macOS-style" → 44pt-equivalent targets, squircle-adjacent radii, SF Pro, vibrancy. "Enterprise" → 0–4px radii, high-density tables, muted tonal elevation.

## 3. Quantitative thresholds from perception & HCI research

### Fitts's Law (target acquisition)
Movement time is a function of distance D over target width W: MT = a + b·log₂(2D/W). Operational floors:
- Apple HIG: 44×44pt minimum hit region (60×60pt visionOS). Material: 48×48dp with 8dp clearance. WCAG 2.2 SC 2.5.8 absolute floor: 24×24 CSS px non-overlapping.
- Generation rule: min-height and min-width ≥44px on primary interactive elements regardless of glyph size.

### Hick's Law (choice & line length)
Decision time grows logarithmically with choices. Most rigid typographic application: **45–75 characters per line** for comprehension.
- Generation rule: max-width ~65ch (~600px) on text containers.

### Aesthetic-Usability Effect
Users perceive aesthetically coherent interfaces as more usable; "aesthetics" here is quantifiable contrast and structural hygiene, not subjective art.
- Text contrast ≥4.5:1; non-text ≥3:1.
- WCAG 2.2 SC 2.4.13 Focus Appearance: focus indicator area ≥ a 2px-thick perimeter of the component, with ≥3:1 contrast shift vs. unfocused state and adjacent colours.
- Generation rule: `outline: 2px solid <high-contrast-token>; outline-offset: 2px` on :focus-visible.

### Gestalt grouping (proximity & common region)
- Proximity ratio: sibling gap < parent-container gap, stepping ~2× per level. Example ladder: icon↔label 8px → list-item↔list-item ≥16px → group↔group ≥32px.
- Common region: enclosure (border or background tint) makes elements read as one unit — the anatomical basis of cards.

| Principle | Observable evidence | Operational rule | Source | Confidence |
|---|---|---|---|---|
| Fitts's targets | Interactive bounding boxes ≥44×44px | min-height/min-width 44px on buttons and icon targets | HIG, M3, WCAG | High |
| Hick's line length | Paragraphs ≤ ~65 characters wide | max-width: 65ch on text blocks | Refactoring UI | High |
| WCAG contrast | Luminance ratio ≥4.5:1 (text), ≥3:1 (non-text) | Sample fg/bg pairs; assert the ratio | WCAG 2.2 | High |
| Focus appearance | Focused elements show an outer ring ≥2px | 2px solid outline, 2px offset on :focus-visible | WCAG 2.2 | High |

## 4. Component anatomy specifications

### Cards
- Anatomy: container + internal padding + hierarchical content blocks. M3 variants: Elevated (shadow), Filled (tonal), Outlined (1px border).
- Specs: 16px uniform internal padding (24px desktop-large). Internal stack gaps consistent (8px title↔body, 16px before action footer). Radius by system: M3 12dp, Fluent 8px, Carbon 0px.

### Text fields & forms
- Anatomy: label, input container, placeholder/value, helper/error text.
- Specs: container 40–48px tall. Labels *above* the input, 4–8px gap (HIG, Polaris). M3: Filled or Outlined variants. Placeholder text is never a substitute for a visible label (recognition over recall).

### Data tables
- Carbon is the enterprise standard: row heights Tall 64px / Medium 48px / Short 32px / Compact 24px; 16px horizontal cell padding, vertically centred; zebra striping or subtle 1px bottom borders to guide horizontal tracking.

### Empty states
- Anatomy (Polaris): non-intrusive illustration/icon, concise headline, explanatory body, exactly one primary CTA.
- Specs: centre-aligned stack, max-width ~400px, generous vertical padding (64–96px).

### Navigation bars
- iOS tab bar: 49pt + safe-area inset; 28×28pt icons, 10pt labels 4pt below. M3 top app bars: 56dp small to expanded medium/large.

| Principle | Observable evidence | Operational rule | Source | Confidence |
|---|---|---|---|---|
| Card padding harmony | Border-to-content space uniform on all sides, on-grid | padding: 16px (or 24px) uniform in cards | M3, HIG, Carbon | High |
| Input height minimums | Inputs ≥40px tall | min-height 40px desktop / 48px mobile | Polaris, Carbon | High |
| Label proximity | Labels sit nearer their own field than the previous block | label margin-bottom 4px; form-group margin-bottom 24px | Refactoring UI | High |
| Empty-state anatomy | Visual + title + description + one CTA, centred | vertical centred stack, max-width 400px | Polaris | High |

## 5. Cross-system convergence table

| Dimension | Apple HIG | Material 3 | Fluent 2 | IBM Carbon | Verdict |
|---|---|---|---|---|---|
| Grid & spacing | 8pt increments | 8dp grid (space tokens) | 4px base (4× scale) | 8px base (4px sub-grid) | **Universal:** 8-point base with 4-point subdivisions |
| Typography | San Francisco (17pt iOS body; 13pt macOS body) | Roboto (16sp body) | Segoe UI (14px body) | IBM Plex (16px base) | **Convention:** fonts/baselines vary; modular scaling is universal |
| Touch targets | 44×44pt | 48×48dp | 40×40px | 40×40px | **Universal:** ≥40px floor for low-error interaction |
| Corner radius | Rounded, squircle physics | 10-step 0–48dp scale | Conservative 4px | Sharp 0px | **Convention:** radius = brand personality + density context |
| Colour & theming | Semantic system colours (.label, .systemBlue) | Tonal palettes, dynamic colour | Semantic alias tokens | Strict token tiers | **Universal:** tokenization; never raw hex in implementation |
| Elevation | Shadows + background blur (vibrancy) | Tonal surface colour (shadows deprecated) | Shadows, acrylic | Flat colour steps | **Convention:** depth simulation is OS-specific |

## 6. Anti-pattern taxonomy

| Defect name | Visual signature in a screenshot | Principle violated | Corrective rule |
|---|---|---|---|
| **Magic Number Spacing** | Gaps measure odd values (11px, 21px, 27px) | 8-point grid | Snap all margin/padding/gap to nearest multiple of 4 or 8 |
| **Proximity Failure** | Equal spacing above and below a section heading | Gestalt proximity | Make the gap *above* a heading ≥2× the gap below it |
| **Contrast Dilution** | Everything is #000 on #FFF; metadata differs only by size | Hierarchy via de-emphasis | Primary → gray-900, secondary → gray-500, background → gray-50 |
| **Focal Collision** | Multiple fully saturated filled buttons in one card/modal | Hick's Law / action hierarchy | One filled primary per region; others outlined or text-only |
| **Line Length Fatigue** | Paragraphs span the full width of a 1440px window | Cognitive load / saccadic return | max-width 60–75 characters (~65ch) on body text |
| **Target Starvation** | Standalone icons (close ✕) occupy only their 16×16 glyph | Fitts's Law / WCAG 2.5.8 | Pad hit areas to ≥44×44px (invisible padding is fine) |

## 7. Screenshot Evaluation Rubric

Run this ordered 14-point checklist against any single screenshot. Score each pass/fail with a one-line evidence note.

**Grid and spacing (structural integrity)**
1. **Grid adherence:** do all paddings, margins, gaps divide evenly by 4 or 8? (0 deviation allowed.)
2. **Container alignment:** do left/right edges of distinct blocks align to shared vertical axes (12-column mapping)?
3. **Gestalt proximity:** is between-group spacing visibly larger than within-group spacing?

**Typography and readability**
4. **Modular scale:** fewer than 6 distinct font sizes, in geometric progression?
5. **Line-height proportion:** headings tight (~1.1–1.2×), body loose (~1.5×)?
6. **Measure constraint:** paragraphs capped near ~65 characters?

**Hierarchy and colour**
7. **De-emphasis check:** secondary metadata visually quieter (lighter colour and/or thinner weight)?
8. **Action singularity:** at most one saturated filled primary button per distinct region?
9. **Text contrast:** normal text ≥4.5:1 against its background?
10. **UI contrast:** borders and icons ≥3:1 against their background?

**Components and accessibility**
11. **Fitts's minimums:** interactive elements ≥44×44px bounding boxes (24×24 absolute floor)?
12. **Input height:** text inputs ≥40px (desktop) / 48px (mobile)?
13. **Label proximity:** labels nearer their own field than the preceding block?
14. **Focus appearance:** any visible focus state has a ≥2px ring with a 3:1 contrast shift?

**macOS calibration note (added for this skill):** macOS is a pointer-first platform. Native controls (menu items ~22pt, toolbar buttons ~28pt, standard buttons ~20pt tall) legitimately run smaller than the 44px touch floor — evaluate desktop surfaces against HIG macOS control metrics and the 24px WCAG floor, not the touch minimums. Checks 11–12 apply at full strength to touch-adjacent layouts (Catalyst-style, iPad-influenced) and to generated mocks intended for dual-platform use.

## 8. Evidence table

| Claim | Primary source | Date | Evidence type |
|---|---|---|---|
| 8-point grid governs spacing across modern systems | Industry practitioner guide | 2026 | Practitioner literature |
| Touch targets 44–48px minimise error (Fitts) | HCI summary literature | Current | Empirical HCI summary |
| 4.5:1 / 3:1 contrast minimums | W3C WCAG 2.2 | 2023–2026 | Technical specification |
| Focus appearance: 2px perimeter, 3:1 shift | W3C WCAG 2.2 | 2023–2026 | Technical specification |
| M3 10-step radius scale | Google Material Design | Current | Official documentation |
| Carbon 2×/8px grid, 0px radii | IBM Carbon | Current | Official documentation |
| Hierarchy by de-emphasising labels | Wathan & Schoger, *Refactoring UI* | Current | Expert critique / book |
| 45–75 char line length | Refactoring UI / typography guidelines | Current | Typography guidelines |
| 44×44pt minimum hit region | Apple HIG | Current | Official documentation |
| Polaris zero-default layout spacing | Shopify Polaris | Current | Official repository |

## 9. Known gaps in this knowledge base

- **Motion/animation metrics** — excluded by the research scope. Do not speculate on easing/timing from static images.
- **Font-specific kerning nuances** — SF Pro's dynamic tracking adjustments per point size are not detailed here; don't claim exact tracking values from screenshots.
- **Variable font axis mapping** — opsz/wdth formulas undocumented here.
- **macOS-specific control metrics** — this research is cross-platform; where it conflicts with measured native macOS control sizes or an official Apple UI kit, the kit/HIG value wins (see the skill's provenance ladder).
