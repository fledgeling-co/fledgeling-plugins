# Ajar — profile

- **Source:** macapp.supply (parcse.com/ajar) · **Surfaces digested:** marketing cover composite (web) + app icon — **no native app UI provided** · **Last updated:** 2026-07-19
- **One-sentence identity:** An apple.com-homage marketing page (near-white ground, SF Pro display, `#1D1D1F` pill CTA) whose one real idea is a black→gray→light-gray headline fade that *performs* the app's "light dims as the lid closes" pitch — Linear/Raycast marketing minimalism with a single witty typographic trick.
- **Cluster:** unassigned (no native UI evidence to cluster on)
- **Lineage:** unknown (low) — the app itself is a menu-bar "Lid Angle Sync & Keep Awake" utility and is *plausibly* AppKit-native `NSMenuBarExtra`, but **not one pixel of app chrome is shown**; the only rendered surface is a web marketing composite. Nothing here feeds macOS canon.
- **Era (chrome):** unknown — no window chrome shown. Icon reads **Big Sur / modern gradient-squircle era** (single squircle, vertical gradient plane, one centered dimensional glyph, soft contact shadow); cannot distinguish Big Sur material from early Liquid Glass from a flat 256px render.

## What is (and isn't) in the inputs

Two images, zero app UI:
- **`cover.jpg` (2400×1260)** — a **web marketing composite**, not an app screenshot. Pure-white page, brand lockup top-left, three-line display headline, one CTA pill, a `parcse.com / ajar` URL bottom-right. This is *brand evidence*, analysed below; it is **not native macOS UI** and is excluded from macOS canon and clusters.
- **`icon.png` (256×256)** — the app icon, recorded as identity evidence (this is Workflow A, so no full 12-point icon digest; a proper icon digest belongs in `icons/ajar.md` under Workflow B).

The app's actual UI — a menu-bar-extra popover, near-certainly — was not supplied. **The corpus cannot yet say anything about how Ajar's UI looks or whether it reads native.**

## Tokens

Brand/marketing tokens (web surface — never promote to macOS canon):

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/bg | `#FFFFFF` pure white | (measured)(inferred) | marketing page ground |
| brand/ink-primary | `#040404`–`#090909` near-black | (measured)(inferred) | wordmark + headline line 1 |
| brand/ink-2 | `#3B3B3B`–`#3F3F3F` | (measured)(inferred) | tagline + headline line 2 |
| brand/ink-3 | `#808080` mid-gray | (measured)(inferred) | headline line 3; ~3.9:1 on white (passes 3:1 large-text only) |
| brand/ink-muted | `#7F7F81` | (measured)(inferred) | footer URL |
| brand/cta-fill | `#1D1D1F` | (measured)(inferred) | **Apple's signature off-black** (apple.com button colour), not #000 — an Apple-ecosystem tell |
| brand/type | SF Pro Display; Bold headlines/wordmark, Regular/Medium tagline | (estimated)(inferred) | grotesque; Apple pill + macOS context → SF Pro over Inter |
| brand/accent | indigo/periwinkle (from icon only) | (measured)(inferred) | the sole colour on the page is the icon; restrained strategy, accent <2% of pixels |
| icon/bg-gradient | `#8986FF` (top) → `#6B68FB` → `#5D58E7` → `#514ACF` (bottom) | (measured)(inferred) | vertical-ish plane, lit top / deep indigo base; sits by system **Indigo** (`#6155F5` light) |
| icon/glyph | lavender cone, apex `#E6E6FD` → mid `#CBC9F5` → base `#A09CE7` | (measured)(inferred) | apex-lit gradient (brightest at tip), soft base contact shadow — "light rising to a peak" / lid / mountain |
| icon/shape | rounded squircle tile, single centered glyph, no overlay device | (measured)(inferred) | Big Sur-era grammar |

## Layout skeletons

**cover.jpg — marketing composite (web), light, ~1.9× export.** One hard left alignment axis shared by icon, wordmark, tagline, all three headline lines, and the CTA; footer URL right-aligned to the opposite margin. Top zone: 1-unit squircle icon + "Ajar" Bold wordmark on a baseline, tagline in ink-2 directly beneath (tight within-group gap). Large vertical gap, then the display headline block — three stacked lines at one size, tight leading (~1.05–1.1), each line a step lighter (`#040404` → `#3F3F3F` → `#808080`). Large gap, then a black `#1D1D1F` fully-rounded CTA pill ("Try free for 7 days →") bottom-left; muted URL bottom-right. Generous whitespace throughout — loose density, Swiss-poster proportions.

**App UI:** none provided — skeleton unknown.

## Signature moves

- **[GOLDEN-NUGGET] Semantic tonal descent.** The headline "Open the lid. / Light rises with it. / Close it and the Mac is gone." is set in three measured lightness steps (`#040404` → `#3F3F3F` → `#808080`). The type *literally dims* line by line, enacting the product's behaviour (brightness follows the lid; close it and the screen goes dark) inside a static image. This is content-encoding typography — the demo *is* the type — and it is the entire memorable budget of the page, spent in one place. Systematic and purposeful → signature, not a Contrast Dilution defect (the faintest line is huge display type at ~3.9:1, clearing the 3:1 large-text floor).
- **Apple-marketing mimicry as brand posture.** Pure-white ground + SF Pro + the exact apple.com `#1D1D1F` pill + oversized restrained display type is a deliberate "looks like Apple shipped it" register — trades on Jakob's Law (borrowed platform familiarity → borrowed trust) for a solo utility.

## Defects

- **No true defects observable** — but note this is a *marketing* surface, not the product. The one thing that would be a Contrast Dilution defect in body copy (the `#808080` line) is a defensible large-display device here.
- **Corpus-level gap, not an app defect:** the submission ships a marketing composite where an app UI screenshot belongs. For a design corpus, this input is nearly all brand and almost no product.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| cover.jpg (marketing composite, web — NOT native UI) | 11/14 · #12/#13/#14 N/A | none among applicable checks; #9 passes only under the large-text lens (line-3 `#808080` ≈ 3.9:1) — a deliberate device |
| native app UI | — | not provided; cannot score |

**Native-tells audit:** N/A on every point — `cover.jpg` is a web marketing page with no toolbar, sidebar, traffic lights, selection grammar, or native controls to audit. The app's native fidelity is **unmeasured**.
