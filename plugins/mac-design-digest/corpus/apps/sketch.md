# Sketch — profile

- **Source:** macapp.supply (cover composite only) · **Surfaces digested:** main window (light) — cropped, canvas-partial · **Last updated:** 2026-07-19
- **One-sentence identity:** Figma's canvas-first tool chrome rendered in AppKit — a native design editor that floats its toolbar as grouped white capsules over the canvas and codes its layer tree in two hues (indigo selection, magenta components).
- **Cluster:** unassigned (cluster_hint: canvas-creative-tool)
- **Lineage:** native (high) — genuine AppKit; real traffic lights, source-list sidebar, 13pt-class SF Pro, compact controls. Non-native evidence: none.
- **Era (chrome):** custom (Sketch house chrome) — opaque white floating capsule pills with soft shadows over the canvas; capsule bezels align with the macOS 26/27 capsule signature but the material reads opaque-white, not Liquid Glass lensing. Not clearly Liquid-Glass-era; recorded `(insufficient-evidence)` for glass classification.

> **Provenance caveat:** the only input is a marketing **cover composite** (2000×1000). Left ~55% is brand backdrop (pink→lavender gradient, black serif display headline "Designers, welcome home.", faceted-diamond logo) — analysed as *brand* evidence, never conflated with UI. Right ~45% is the actual app window, **cropped** (right edge and window bottom cut off; canvas only partially visible). Render appears ~1× logical (traffic-light dot ≈ 14–15px), so px≈pt; all UI metrics are `(estimated)` ranges.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/canvas | #F5F5F5 (measured)(inferred) | | design canvas, light mode |
| bg/sidebar | #FFFFFF (measured)(inferred) | | source list is pure white, not vibrancy-grey in this render |
| text/primary | #262626 ≈ 85% black (measured)(inferred) | | matches kit's softened primary (not pure #000) |
| accent/selection | #545CFD indigo/periwinkle (measured)(confirmed) | | binds selection + focused-doc text; NOT system blue #0088FF — brand-bound or user-Indigo-accent (see Defects) |
| sel/document-fill | #F0EFFF (measured)(inferred) | | selected document row: flat inset rounded fill, ~accent @ low alpha, indigo text — native-correct grammar |
| sel/layer-capsule | #545CFD fill, white text, **capsule** (measured)(inferred) | | selected layer/artboard: saturated full-bleed capsule — house style, deviates from native selection grammar (see Defects) |
| sel/page-row | #F2F2F2 light-gray inset fill (measured)(inferred) | | active page ("Designs") — neutral secondary selection |
| identity/component | #B620E1 magenta (measured)(inferred) | | symbol/component-instance glyphs in the layer tree; separate hue from accent — object-type coding |
| type/body | ~13pt SF Pro Regular (estimated)(inferred) | | layer-row + page-row labels |
| type/section-header | ~13–14pt SF Pro **Bold**, primary black (estimated)(inferred) | | "Documents"/"Pages" — sentence case but amplified bold-black, not secondary semibold (see Defects) |
| chrome/toolbar | floating opaque-white **capsule pills**, soft shadow, ~28–36pt tall, ≤4 function groups (estimated)(inferred) | | over-canvas, not a unified titlebar toolbar |
| chrome/sidebar-row-h | ~28–34pt layer rows; taller header rows (estimated)(inferred) | | insets ~4px, hierarchy via indented vertical guide lines |
| radius/toolbar-pill | capsule (infinite) (estimated)(inferred) | | |
| radius/selection | ~6–8pt document/page fills; capsule for layer selection (estimated)(inferred) | | |
| brand/gradient | #FAF1F4 pink → #F3E0FC lavender (measured)(inferred) | | marketing backdrop only — NOT app UI |
| brand/headline | high-contrast serif display, ~120px, warm near-black #1F2120 (measured)(inferred) | | editorial brand voice; app UI itself is SF Pro neo-grotesque |

## Layout skeletons

**Main window (light, cropped):**
- **Chrome:** traffic lights top-left. No unified titlebar toolbar; instead a **standalone circular glass/white button** (component/isometric-cube glyph) pinned above the sidebar, and a row of **floating white capsule pill-clusters** over the canvas top: `[Sketch-diamond + ＋]` (insert group) · `[crop]` · `[align ↥ / distribute ↧ / frame ⧉]` (arrange group) · `[path/component ⬡]`. Borderless monochrome symbols except the colourful brand diamond.
- **Left panel (source list, ~256pt-class):** two zones. Top — **Documents** header (bold, +collapse/＋ affordances) → selected document "TV Dashboard" (indigo inset-rounded fill + file glyph). **Pages** header → Designs (active, gray fill) / Explorations / Symbols. Thin divider. Bottom — **layer tree**: selected artboard "TV Dashboard" in a saturated indigo capsule (white text), then indented layers (Menu ▸ Avatar / Home / Notifications ▸ Icon ▸ Shape ▸ Path / Path ▸ Dot) with per-row monochrome glyphs, magenta glyphs for symbol/component instances, dimmed rows for hidden layers, trailing `⨯`/link glyphs for boolean/mask markers. Indentation carried by faint vertical guide lines.
- **Canvas (right, partial):** light-gray artwork board titled "TV Dashboard" showing a TV app mock (LIVE/TV pill, crimson→red panel, avatar, left rail of circular nav icons, "Watching now" avatar stack +38).

## Signature moves
- **[GOLDEN-NUGGET] Floating capsule toolbar over the canvas.** Rather than a unified titlebar toolbar, Sketch floats grouped opaque-white capsule pills above the artwork, chunked ≤4 clusters by function, with a leading standalone circular tool button. Maximises canvas, keeps commands mobile/contextual — the app's chrome fingerprint. (Von Restorff: the single full-colour brand diamond among monochrome glyphs pulls the eye straight to "insert".)
- **[GOLDEN-NUGGET] Two-hue layer semantics.** The layer tree runs a disciplined two-colour system: **indigo = selection/accent** (selected doc, focused layer, doc-title text) and **magenta = component/symbol identity** (Avatar, Icon, Dot glyphs). Object-type is coded pre-attentively by hue, kept orthogonal to the selection accent — honours the native rule that identity colours stay separate from the system accent.

## Defects
- **Selection-grammar inconsistency (house style).** One source list carries two selection treatments: a native-correct flat inset lavender fill + indigo text for the selected *document*, but a **saturated full-bleed indigo capsule with white text** for the selected *layer/artboard*. The saturated capsule violates the native grammar (selection = flat inset accent-tinted fill, never a saturated capsule). Systematic and purposeful (document-scope vs object-focus emphasis), so borderline signature — but the white-on-saturated capsule is the one element that would not survive a native-tells audit. Canon would use the same flat inset fill at two emphasis levels.
- **Sidebar-header amplification.** "Documents"/"Pages" are sentence-case (✓) but rendered **bold primary-black** rather than the HIG secondary-colour semibold. A mild de-emphasis inversion — headers shout where native headers whisper.
- **Accent may be brand-bound, not system-bound (contested).** Selection accent is indigo/periwinkle #545CFD, not macOS system blue #0088FF. Either Sketch hardcodes its brand indigo (a deviation from "the accent is the user's") or the capturing user set the system accent to Indigo. Single surface can't disambiguate — recorded contested.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main window (light) | 12/14 | #7 section headers amplified bold-black not de-emphasised secondary; #10 sidebar divider <3:1 (native low-contrast separator, soft). #6/#12/#13/#14 N/A (no prose/inputs/forms/visible focus). |
| main window — native-tells | 8/10 | #3 layer selection is a saturated indigo capsule w/ white text (not flat inset accent-tinted); #4 headers bold-black not secondary semibold (soft). |
