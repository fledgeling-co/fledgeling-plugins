# Icon: Maestri

- **Era:** Liquid Glass (baked/quoted — effects hand-rendered, not Icon-Composer-applied) · **Rubric:** 9/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (webp, 1024×1024, squircle-masked with transparent corners — a web render, not a verifiable full-bleed layer set) · **App:** "Orchestration canvas for AI agents" (category AI)

| Dimension | Reading |
|---|---|
| Background | Glass-layers over a grid **canvas**: near-white `#FFFFFF` field with faint gray graph-paper grid `~#EBEBEB` (tints lavender `~#D1B9F6` under the card glow). Two receding translucent window cards: violet ramp `#9F5FFB→#814CFB`, electric blue `#1836F9`. |
| Glyph | **Mascot / emoticon** built from terminal punctuation — a winking face: `>` chevron (left eye), `‿` smile, `|` cursor bar (right eye). Rounded stroke caps, lavender-white `#E3E2F4→#BCBAE1`. Sits on a navy-black terminal screen inset `#0C0E14→#0F1641` (edges `~#050522`), roughly optically centred in the front window. |
| Overlay device | Framed-window motif — a glossy white front window (titlebar `#D9DBDD`) frames the dark terminal screen; real macOS traffic lights (red `#ED6968` · yellow `#F2CA46` · green `#65C469`) and a "maestri" wordmark `#C8CCE8` quoted literally in the titlebar. |
| Light model | Environmental glass, glow-driven: radial outer halos on the violet/blue cards + a top specular sheen on the white window + an inner vignette glow behind the glyph. No single hard directional source; all effects **baked in** (contra HIG "let the system apply specular/shadow"). |
| Layer stack | (back→front) 1) grid canvas → 2) violet window card `#9F5FFB→#814CFB` + 3 control dots → 3) blue window card `#1836F9` + 3 control dots → 4) glossy white front window + RYG traffic lights + "maestri" wordmark → 5) navy terminal screen inset → 6) lavender-white winking-face glyph. |
| Palette economy | Core is a disciplined **violet→blue analogous ramp** (one family) + navy screen + lavender-white glyph; but literal RYG traffic dots inject three semantic hues and the wordmark a fourth tint. Accent = electric blue/violet `#1836F9`. |

## Signature devices
- **[GOLDEN-NUGGET] Terminal prompt as a winking face** — the `>_` prompt plus a cursor `|` are re-read as an emoticon (`>` eye + `‿` smile + `|` wink-eye). This is the whole personality: a *friendly* agent shell. Textbook subject-mining for "orchestration canvas for AI agents."
- **Receding stacked windows** — three offset translucent cards imply many agents / many sessions coalescing onto one surface (the product's "one canvas" pitch made literal).
- **Graph-paper canvas ground** — a faint grid behind the stack nods directly to the "canvas" metaphor; rare, and it commits.
- **Literal window-chrome quotation** — real traffic lights + a wordmark rendered *inside* the icon (a Big-Sur-era "icon-of-a-window" habit, here at odds with modern HIG).

## Failures
- **#4 16px squint (critical):** three small-offset cards + a dark screen holding a 3-stroke face + RYG dots + wordmark all collapse; at menu-bar/Spotlight size this becomes a dark rectangle with a colored fringe — subject unreadable.
- **#10 Variant robustness:** the concept is keyed to a light canvas + white front window + RYG dots + navy screen; dark / clear / tinted / mono renders lose the layer separation and the glyph (which is defined only by the dark screen behind it).
- **#12 No-text:** "maestri" wordmark baked into the titlebar — text that smears first at small sizes.

### Soft passes (flagged, counted as passes)
- **#3 Silhouette:** solid-black it reads as "three stacked rounded rectangles" — generic *stacked windows*; the winking-terminal subject lives in interior detail, not the outline.
- **#5 Single light:** broadly environmental-glass, but top sheen (directional) + radial card glows + inner screen vignette are three logics, all baked.
- **#6 Palette economy:** RYG traffic dots + wordmark push past the ≤2-hue-family floor, though the brand ramp itself is clean.
- **#9 Era coherence:** Liquid-Glass vocabulary, but effects are hand-baked (HIG says let the system apply them) and mixed with a literal chrome quotation + wordmark — a *quoted* glass, not composed glass.

## Rhymes with
- Developer-tool terminal icons (Ghostty, iTerm, Warp, kitty) — but softened with rounded caps and a face instead of a bare prompt.
- Glowing violet→blue "glass card stack" AI-tool icons — the current AI-category default palette (electric indigo/blue on a light or dark glass plane).
- Framed-window / "icon-of-a-window" motifs (Big-Sur-era TextEdit/Preview lineage) crossed with a mascot-face twist.
