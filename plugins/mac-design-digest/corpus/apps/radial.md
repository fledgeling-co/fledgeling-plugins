# Radial — profile

- **Source:** macapp.supply (`radial.appverge.net`) · **Surfaces digested:** invoked radial menu / gesture HUD, root ring (1 surface, 1 state, from marketing cover) · **Last updated:** 2026-07-19
- **One-sentence identity:** A Fitts-optimal pie menu rendered in Apple's own Liquid-Glass material — Blender/Maya marking menus married to a Raycast-style launcher, summoned at the cursor by one gesture.
- **Cluster:** unassigned — opens a candidate "invoked-overlay / gesture-HUD utility" cluster (sole member; shares the chromeless-floating-panel premise with Alcove but uses native material, not iOS trade dress).
- **Lineage:** native (med-high) — a radial/pie menu is *not* a stock AppKit control, but every material choice here is Apple's own: genuine Liquid-Glass lensing (the disc bends and lightens the magenta backdrop at its edges, not a flat Gaussian blur), real monochrome SF Symbols as secondary-label glyphs (`sparkles`, `folder`, `globe`, the text-cursor `A`, a list-badge-plus), real superellipse macOS app tiles (Safari, Music, Stickies, Zed), and the chevron `›` = opens-a-further-view grammar. The bespoke *geometry* is a signature, not a lineage tell; the *grammar* reads native. So — unlike Alcove — its material/glyph discipline may feed canon; its polar geometry may not (nothing to promote from a sample of one).
- **Era (chrome):** liquid-glass (med) — frosted lensing disc with adaptive tint reads macOS-26+ Liquid Glass. Humility flag: from one still over a saturated backdrop, Regular Liquid Glass and plain `NSVisualEffectView` vibrancy are not reliably distinguishable; the edge-lensing (light bending, not just blurring) is the strongest tilt toward true Liquid Glass.

> **Evidence caveat:** the only app UI is the HUD *inside a marketing composite* (`cover.jpg`, 1920×1080) — a stylized product render, not a captured screenshot. There is **no chrome anchor** (no traffic lights, no menu bar) to calibrate retina scale, so every pixel figure below is `(estimated)` at an unknown scale; the reliable measurements are the **scale-free ratios** (hub-to-disc, ring radius). Everything outside the disc — the purple/magenta fanned wallpaper and the "ONE GESTURE. EVERYTHING." headline — is **brand evidence**, kept separate from app-UI tokens.

## Tokens

### App UI — the radial menu (all `(estimated)(inferred)` — single stylized render, unknown scale)
| Token | Value | Provenance | Notes |
|---|---|---|---|
| hud/material | frosted translucent glass, edge-lensing/adaptive tint over desktop | (estimated)(inferred) | Reads Liquid Glass; the entire HUD is the floating layer, so glass here is legitimate (no glass-in-content violation) |
| hud/shape | full circle (disc) | (estimated)(inferred) | Radius = diameter/2; the app's whole identity is the polar form |
| hud/diameter | ~490–520px in composite (scale unknown) | (estimated)(inferred) | No chrome anchor → cannot convert to pt honestly |
| hud/center-hub | bright white→lavender radial glow, ~0.42 × disc diameter | (estimated)(inferred) | Doubles as gesture deadzone AND breadcrumb: holds current ring's name ("Radial" = root) |
| hud/ring-radius | items centered at ~0.70 of disc radius | (estimated)(inferred) | Scale-free; the one high-confidence spatial fact |
| hud/item-count | ~9 items, ~evenly distributed (≈40° steps) | (estimated)(inferred) | Two visual classes (see below) |
| item/action-glyph | monochrome SF Symbol, near-black ~#2A2A2E (secondary-label register) + trailing chevron `›` | (estimated)(inferred) | `sparkles`, `folder`, `globe`, text-`A`, list-badge-plus — chevron = opens nested ring |
| item/launch-tile | full-color macOS app icon, superellipse, ~56–64px, NO chevron | (estimated)(inferred) | Safari, Music, Stickies, Zed — direct launch, identity colors (correct: app identity ≠ system accent) |
| item/chevron | `chevron.forward` ~12–16px, tertiary weight | (estimated)(inferred) | Native "…"/submenu grammar translated to radial |
| type/center-label | "Radial", ~15–17pt-class, muted pink-grey ~#C9A9C0 on near-white hub | (estimated)(inferred) | **Low contrast — likely <4.5:1** (see Defects) |
| chrome/traffic-lights | none | (estimated)(inferred) | Correct — a floating HUD/panel carries no traffic lights (HIG) |
| accent/system | not evidenced | (estimated)(inferred) | No blue selection/focus/hover fill visible; cursor rests on Safari with no highlight — selection grammar unseen |

### Brand (marketing composite — NOT app-UI tokens, kept separate)
| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/backdrop | deep purple→magenta fanned "blade" render (~#2A0B3D → ~#E85CFF) | (estimated)(inferred) | Apple M-series-keynote register (the "Scary Fast"/product-launch abstract) |
| brand/headline | bold grotesk all-caps (Helvetica Now / SF Pro Display Bold class), two-tone: grey "ONE GESTURE." ~#8A8A8A + white "EVERYTHING." #FFFFFF | (estimated)(inferred) | Keynote-mimetic; grey-setup / white-payoff two-tone is the one typographic device |
| brand/icon | black superellipse tile, ring of 8 white capsule dashes (a stylized radial menu / spinner), soft inner light | (estimated)(inferred) | Icon depicts the product: the dashed ring = the radial menu itself. NOT digested as an icon here (Workflow A only) — noted for brand coherence |

## Layout skeletons

**Invoked radial menu (cover.jpg):** the user's desktop (here a magenta marketing wallpaper) fills the frame. A single translucent glass disc floats centered under the cursor. Three concentric zones: (1) a bright glowing **center hub** (~0.42 of disc dia) that is both the gesture deadzone and a breadcrumb label holding the current ring's name; (2) an **item ring** at ~0.70 radius carrying ~9 items evenly distributed around the circle; (3) the frosted glass annulus between them. Items divide into two classes on one ring — monochrome SF-Symbol *action wedges* with trailing chevrons (open nested rings) and full-color *app-launch tiles* without chevrons (direct launch). No window frame, no toolbar, no sidebar, no traffic lights — the disc is the entire visible app, drawn at the pointer.

## Signature moves
- **[GOLDEN-NUGGET] The whole app is one signature: a Fitts-optimal pie menu on the Mac.** macOS has no radial menu — its command surfaces are rectilinear (menu bar, dropdowns, context menus). Radial replaces angular-list scanning with a *polar* layout where every item sits the same short distance from the invoke point and each wedge is a large directional target. This is textbook Fitts (constant distance, large targets) plus spatial-recall: fixed angular positions let users learn a *gesture* ("flick up-right = folder"), which is exactly what the "ONE GESTURE. EVERYTHING." headline sells. Systematic, purposeful, accessible → signature, not defect.
- **[GOLDEN-NUGGET] Two item classes unified on one ring.** Monochrome SF-Symbol wedges that *expand* (chevron = nested ring) sit beside full-color app tiles that *launch directly* (no chevron). The disclosure chevron faithfully imports macOS's "…"/submenu grammar into polar space, and the monochrome-vs-full-color split (Von Restorff) tells the eye which items go deeper and which fire immediately — a legible taxonomy encoded purely in glyph treatment.
- **[GOLDEN-NUGGET] The center hub is a triple-duty object.** It is simultaneously the gesture deadzone (release here = cancel), the focal anchor (the one glowing element in a frosted field), and a breadcrumb (its label names the current ring, so a nested ring would read its own name). One element carrying navigation state, cancel affordance, and visual hierarchy.

## Defects
- **Contrast Dilution — center label.** "Radial" is set in a muted pink-grey on the bright near-white hub; the pairing reads well under ~4.5:1 (a legible-but-thin label). Low-stakes (a passive title on a deadzone, not an action), but a real contrast miss — canon would darken the label to a secondary-label tier that clears 4.5:1, or set it over the frosted annulus rather than the white glow.
- **Selection / hover grammar unseen.** The cursor rests on the Safari tile but no inset-rounded selection fill or accent-tinted highlight is shown. Native selection grammar (flat inset rounded fill, accent glyph) is therefore unverified — a gap, not proven wrong. Whether hover binds to the system accent is the single most important unanswered native question.
- **HUD-over-content contrast is backdrop-dependent (inherent risk, not proven here).** Monochrome glyphs on a translucent disc rely on the frost adding enough opacity to stabilize legibility over *any* desktop. Over this bright magenta wallpaper the top glyphs (`sparkles`, `folder`) read fine; over a busy or light-on-light desktop the same glyphs could thin out. The frost appears heavy enough to manage it, but robustness across desktops is untested from one composite.
- **Evidence poverty (not the app's fault):** one surface, one state, from a marketing render — real pt sizes, hover/selection state, nested-ring behavior, the settings/menu-bar-extra surface, and light-vs-dark-desktop behavior are all unseen. Scale is unknowable, so metrics are ratios and estimates at low confidence.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| invoked radial menu (root ring, over light composite) | 11/14 (several N/A — polar, text-sparse surface) | **Fail #9** center-label contrast <4.5:1 (pink-grey on white glow). **Partial #4** only one app type size shown (insufficient scale evidence). **N/A #5/#6** no paragraphs/line-length; **#12/#13** no inputs/form labels; **#14** no focus state captured. Passes: #1 even angular rhythm (radial "grid"), #2 constant-radius alignment, #3 clear hub/ring/item proximity tiers, #7 monochrome-vs-color de-emphasis, #8 no CTA collision (menu paradigm), #10 glyph contrast adequate here, **#11 Fitts — radial is the ideal case (constant distance, large wedges)** |
| — native-tells audit | 7/10 (radial geometry N/As several) | Passes: #1 native material/glyph grammar, #2 glass is on the floating layer only (no glass-in-content, no nested glass), #8 superellipse app tiles + concentric disc, #10 correctly chromeless (HUD has no traffic lights). Correct-idiom: #7 chevron = opens-further-view, #9 borderless monochrome symbols. **N/A/insufficient:** #3 selection grammar unseen (cursor on Safari, no highlight), #4 no sidebar, #5 custom overlay not standard-control density, #6 system-accent binding not evidenced |
