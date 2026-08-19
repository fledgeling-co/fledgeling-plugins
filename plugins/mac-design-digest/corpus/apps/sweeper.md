# Sweeper — profile

- **Source:** macapp.supply · **Surfaces digested:** marketing cover (composite); app icon (context only) · **Last updated:** 2026-07-19
- **One-sentence identity:** An AppCleaner-class uninstaller sold with Apple.com's own marketing grammar — white ground, SF Pro heavy display, one burnt-sienna strike — but **no app window was ever provided**, so its actual UI is unstudied.
- **Cluster:** unassigned (no app-UI evidence to place it)
- **Lineage:** unknown (low) — the app's interface never appears in any supplied image; the marketing chrome is SF Pro / Apple-vernacular, which *hints* platform respect but is brand, not UI, evidence and feeds no macOS canon.
- **Era (chrome):** unknown for the UI. Icon render is legacy/realistic (Big-Sur-era skeuomorphism), not flat and not Liquid Glass.

> ⚠ **Evidence boundary.** Both inputs are non-UI: `cover.png` is a marketing composite (device-frame-free hero: icon + wordmark + headline + body copy on white) and `icon.png` is the app icon. There is no screenshot of the running application. Everything below is **brand evidence** from the cover plus **icon context** — none of it is macOS-UI evidence and none of it may promote to macOS UI canon. Workflow A (UI digest) has nothing native to score.

## Tokens

All tokens below are **marketing-brand** tokens measured from the cover composite (a graphic layout, not an app surface). They describe the promo page, not the product UI.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/bg | #FFFFFF (measured)(inferred) | | full-bleed white marketing ground |
| brand/text-primary | #1D1D1F (measured)(inferred) | | headline + wordmark; **exactly Apple.com's marketing near-black** — deliberate Apple-page mimicry |
| brand/text-secondary | #707070 (measured)(inferred) | | body/description; ~50% gray, de-emphasised |
| brand/accent | #B44B23 burnt sienna (measured)(inferred) | | the single accent; used only for the strikethrough rule, ~8px thick |
| brand/type-display | SF Pro, ~90–95px, Bold/Heavy, #1D1D1F (estimated)(inferred) | | headline "Apps don't leave quietly." |
| brand/type-wordmark | SF Pro, ~44px, Bold (estimated)(inferred) | | "Sweeper" |
| brand/type-body | SF Pro, ~26px, Regular, lh ~1.6 (estimated)(inferred) | | 3-line centred description, ~68 char measure |
| brand/layout | centred single-axis stack (measured)(inferred) | | icon → wordmark → headline → body, all mirror-centred |
| icon/silhouette | metallic-gray Trash bin, files spilling (measured)(inferred) | | realistic 3D render; reuses the macOS system-Trash form (see Icon context) |

## Layout skeletons

**Marketing cover (light).** Single vertical centred stack on pure-white full-bleed, mirror-symmetric about the horizontal centre axis. Top-to-bottom: app icon (~180px, ~90pt @2x) → wordmark "Sweeper" (~90px gap below icon) → headline "Apps don't leave quietly." (~120px gap; the largest, heaviest element, the burnt-sienna rule striking through "leave quietly") → 3-line body description in gray (~80px gap; wraps near ~68 characters). No buttons, no window chrome, no device frame. This is an Apple-product-page hero, not an app surface.

**App UI:** not provided — unknown.

## Signature moves
- **[GOLDEN-NUGGET] The editorial strikethrough as show-don't-tell.** The one accent moment in the whole composite is a single burnt-sienna rule (#B44B23) drawn through the words "leave quietly" — so the headline *enacts* its own claim ("apps don't ~~leave quietly~~"). It is a genuine typographic pun: the crossing-out is both the visual interest budget (Von Restorff — the one different thing) and the message's proof, resolved in one stroke. Systematic restraint everywhere else (mono-accent, mono-typeface, centred) makes the strike land. This is a brand/marketing signature, not a UI one.

## Defects
- None assessable at the UI level — no app surface was supplied. The only *finding* is the **evidence gap itself**: an uninstaller shipped to a design corpus with zero screenshots of the thing it uninstalls-with. Note also the icon leans on the **system-Trash silhouette** wholesale (clever concept mapping "uninstall → trash", but generic execution — it risks reading as the OS Trash can rather than an app), a brand-distinctiveness soft flag, not a rubric defect.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| marketing cover | n/a as UI — ~9/9 applicable checks pass **as a marketing graphic** (grid #1, alignment #2, proximity #3, scale #4, leading #5, measure #6, de-emphasis #7, text-contrast #9 all pass; #8/#10–#14 are n/a — no controls, chrome, inputs, or focus states) | Not a native UI surface; 14-point + 10-point native audits are inapplicable. Contributes 0 to macOS canon. |

## Icon context (Workflow A scope excludes a full icon digest — noted for the later synthesis pass)
Realistic metallic-gray Trash bin, front-lit with a soft specular sheen down the body and a graphite inner rim, app "cards" spilling from the top (a blue rounded-square dev-tool icon with a white bone/wrench glyph, a landscape photo, a document). Soft contact shadow. **Era: legacy/Big-Sur realistic skeuomorphism** — not flat, not Icon-Composer Liquid Glass layering. Concept is strong (uninstalling *is* trashing); execution borrows the OS Trash form closely. Rhymes with other realistic-object utility icons in the corpus (CleanMyMac-adjacent). If a later pass runs Workflow B, digest into `icons/sweeper.md`.
