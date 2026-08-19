# MacRest — profile

- **Source:** macapp.supply (cover.webp only; no gallery shots) · **Surfaces digested:** 1 — marketing cover composite containing one notification/permission panel · **Last updated:** 2026-07-19
- **One-sentence identity:** A Mac sleep-control utility dressed in boutique fashion-editorial marketing — high-contrast Didone serif on warm-black, one rose-pink identity accent — where the only "UI" shown is a brand-styled render of a system notification alert (Amphetamine/Lungo's job, wearing Aesop's clothes).
- **Cluster:** unassigned (single app; brand-marketing evidence only, no captured native surface)
- **Lineage:** unknown (low) — the panel is a **marketing render**, not a captured native window; its anatomy references a macOS Notification Center banner but its styling (oversized glowing buttons, brand-pink accent, ✓/✕ glyphs) is non-native. No AppKit/SwiftUI surface was provided to classify. Non-native evidence never feeds macOS canon.
- **Era (chrome):** custom (brand-styled). The composite's context wallpaper is the **Ventura (macOS 13) default**, not a Tahoe/Liquid-Glass surface — the reference era is pre-Tahoe, and the panel material is a marketing "dark vibrancy" look, not audited system glass.

> **Provenance warning.** This entire profile rests on a single 1280×720 marketing composite. There is **no screenshot of the shipping app** (the real MacRest is almost certainly a menu-bar extra with a small popover/settings pane — unseen). Treat the notification panel as **brand evidence with weak UI inference**, not as a design system. All pixel values are composite-scale `(estimated)`.

## Tokens

Two layers must not be conflated: **brand layer** (backdrop, serif headline, icon accent — marketing) and **panel layer** (the notification render — the nearest thing to app UI).

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/backdrop | `#1D1218`–`#1E1417` warm-black (plum/brown, not pure #000) | (estimated)(inferred) | brand hero ground, top zone |
| type/headline | high-contrast Didone/luxury serif (Canela/Didot-class), ~48–56px, cream `#EDE4DC` | (estimated)(inferred) | **brand** marketing headline — NOT app UI type |
| accent/identity | rose-pink `#FE87A9` (CTA fill) / deeper rose `#B14160` (icon moon) | (estimated)(confirmed) | carried icon → CTA → glow; the app's own accent, overriding the system accent |
| panel/card-fill | dark translucent material, center `#391C18` bleeding to `#AF301F` at edges | (estimated)(inferred) | translucency proven by orange wallpaper reading through — a floating-alert material |
| panel/card-radius | ~24px | (estimated)(inferred) | composite scale |
| panel/title | ~19–20px, "Slack" **bold** + "wants to stay awake" regular, cream `#EADED7` | (estimated)(inferred) | native-notification title anatomy |
| panel/subtitle | ~16px, warm gray `#7C6E6C` | (estimated)(inferred) | de-emphasised body line |
| panel/timestamp | ~15px, very muted `#4A342E` "now", trailing | (estimated)(inferred) | quietest tier — good de-emphasis |
| panel/app-icon | ~40px square, ~9px radius (Slack) | (estimated)(inferred) | leading, header row |
| btn/primary (Allow) | ~56–60px tall, ~15–16px radius, pink `#FE87A9` fill, dark label + ✓, pink outer glow | (estimated)(inferred) | oversized vs native 24–28pt; touch-scaled marketing button |
| btn/secondary (Block) | same geometry, dark translucent fill, white label + ✕ | (estimated)(inferred) | near-equal footprint to primary |
| btn/gap | ~16px between the two buttons | (estimated)(inferred) | |
| context/wallpaper | Ventura orange `#F6A13A` | (measured) | dates the composite's reference to macOS 13 |

## Layout skeletons

**Notification/permission panel (the sole surface).** Floating rounded card (~860×220 composite px) centred on a desktop wallpaper with a soft drop shadow. Two rows + an action row: (1) header — leading 40px app icon, then bold-name + regular-predicate on one baseline, trailing muted "now"; (2) body — one secondary-gray predicate line left-aligned under the title (icon column not indented into); (3) actions — two near-equal-width buttons side by side, **Allow (pink, leading) / Block (dark, trailing)**, each with a glyph + label. Everything shares a single left edge at the icon; buttons split the width into two columns with a ~16px gutter.

**Brand hero band (above the panel).** Left: dark squircle app icon (crescent moon + gear, rose-pink on graphite). Right: two-line serif display headline, cream on warm-black, left-aligned, generous leading. This is marketing composition, not an app window.

## Signature moves
- **[GOLDEN-NUGGET] Nocturnal rose as a throughline.** A single rose-pink identity color travels icon (moon) → primary CTA fill → CTA glow, against an all-warm palette (plum-black ground, cream type, Ventura-orange wallpaper). The utility category almost never commits to an identity color this hard; it's the app's entire personality in one hue.
- **[GOLDEN-NUGGET] Editorial-luxe register on a plumbing utility.** High-contrast Didone serif + warm-black + one saturated pop is a *fashion/luxury* aesthetic family (Aesop, Canela-class editorial) borrowed to sell sleep-management. Deliberate genre transposition — memorable, and rare for a Utility.

## Defects
- **Marketing render, not shipping UI** → the panel's oversized glowing buttons and brand-pink actions are not how macOS renders a real notification; the shipping surface is unseen. Biggest caveat, not a craft defect per se.
- **Accent overrides the system accent** → native macOS binds selection/primary-action to the *user's* chosen accent; MacRest hard-codes rose-pink. A brand choice, but a native tell — excluded from macOS canon.
- **Reversed alert button order** → native grammar puts the default/confirm action *trailing* (right), Cancel/dismiss *leading* (left). Here the prominent "Allow" sits leading, "Block" trailing — inverted.
- **Iso-scale competing actions (mild)** → Allow and Block occupy near-equal footprints; the pink-vs-dark fill still differentiates the primary, so it lands short of a hard hierarchy failure but reads as two co-equal choices.
- **Von Restorff pointed at the anti-goal** → a *sleep*-protecting utility makes "Allow [Slack to stay awake]" the single brightest element, pulling the eye to the action that defeats the app's purpose; "Block" (the on-brand outcome) is the muted one. Possibly intentional demonstration, but the visual emphasis fights the product story.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| notification panel (marketing render) | 11/14 · native 3/10 | 14-pt: #1 grid unverifiable on a glow/composite render `(estimated)`; #10 Block button border/fill ~<3:1 against the translucent card. (#12/#13/#14 N/A — no inputs/labels/focusable state.) Native-tells: #1 non-native render, #5 density (~58px buttons, not 20–28pt), #6 app accent not system accent, #7 reversed button order. Passes: glass placement (floating alert), roughly concentric corners, no faked traffic lights. |
