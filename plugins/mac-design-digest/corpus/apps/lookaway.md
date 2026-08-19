# LookAway — profile

- **Source:** macapp.supply (`lookaway.com`) · **Surfaces digested:** pre-break reminder HUD (1 surface, 1 state, from marketing cover) · **Last updated:** 2026-07-19
- **One-sentence identity:** A break-reminder nag re-imagined as a warm, wallpaper-adaptive glass card with a sleepy-eyes mascot — Time Out / One Sec's screen-break job in a calming consumer register, not a pro tool's neutral chrome.
- **Cluster:** unassigned — opens a candidate "warm wellness / calm-nudge utility" cluster (sole member; likely to share members with break/screen-time timers).
- **Lineage:** native (med) — the *runtime* is almost certainly a native menu-bar break utility (this category is native-Swift-dominated; a wallpaper-tinting always-on-top overlay is not an Electron idiom), and the panel exhibits **genuine macOS material behavior** (translucent, warm-adaptive to the desktop = Liquid-Glass lensing, not a flat scrim). BUT the visible surface is **fully custom — no native chrome (no traffic lights, menu bar, sidebar) to confirm lineage from**, and it does not bind `controlAccentColor`. Lineage is inferred, not proven; its accent-free grammar is recorded as a tell + correction and does not feed macOS accent canon.
- **Era (chrome):** Liquid-Glass-era — the HUD is a translucent card that takes the warm hue of the wallpaper behind it (the desktop's diagonal light bands read *through* the panel), with capsule-bezel controls. Current-era material and control vocabulary, custom-composed.

> **Evidence caveat:** the only app UI is the panel *inside a marketing composite* (`cover.png`, 2400×1260) — a stylized product render, not a captured screenshot. Scale is only semi-knowable, so all panel metrics are ~@2x ratio estimates at medium-low confidence. Everything outside the panel (the near-black warm-olive backdrop, the "Smart breaks…" headline, the sleepy-eyes app icon) is **brand evidence**, kept separate from app-UI tokens. The app icon was intentionally not digested (Workflow A only).

## Tokens

### App UI — the pre-break reminder HUD (all `(estimated)(inferred)` — single stylized render)
| Token | Value | Provenance | Notes |
|---|---|---|---|
| panel/material | translucent dark scrim over wallpaper → reads maroon ~#5A1E12, see-through | (estimated)(inferred) | Liquid-Glass adaptive tinting — the card takes the warm hue of the desktop; wallpaper gradient visible through it |
| panel/radius | ~24–32pt (generous rounded-rect) | (estimated)(inferred) | Large card radius |
| panel/width | ~520–560pt | (estimated)(inferred) | Wide glanceable overlay (~1100px in the 2400px asset, halved) |
| type/countdown | ~28–34pt Bold, #FFFFFF, tabular figures (`00:40`) | (estimated)(inferred) | The primary value; anchors the card |
| type/subtitle | ~18–20pt, warm amber-cream ~#EEC79E | (estimated)(inferred) | De-emphasized by **hue + contrast**, not size — "Almost time. Your eyes will appreciate this." |
| type/family | rounded-terminal geometric sans, Bold — reads SF Pro Rounded (or SF Pro Display Bold) | (estimated)(inferred) | Soft terminals; consistent HUD ↔ marketing headline; the app's warmth lives here |
| btn/primary-fill | frosted white ~#FFFFFF @ 15–20% → pale-warm on the maroon glass | (estimated)(inferred) | "Start break now" — promoted by **luminance, not accent hue** |
| btn/primary-text | cream-white ~#FFF6EE | (estimated)(inferred) | |
| btn/secondary-stroke | translucent cream ~#FFFFFF @ ~22%, ~1pt | (estimated)(inferred) | Outlined snooze pills; low-contrast border (see Defects #10) |
| btn/shape | capsule (height/2) | (estimated)(inferred) | All buttons fully-rounded — macOS-27 capsule-bezel vocabulary |
| btn/height | ~38–42pt | (estimated)(inferred) | Generous Fitts targets for a click-from-anywhere overlay |
| btn/gap | ~10–14pt between pills | (estimated)(inferred) | |
| icon/timer-glyph | pink→magenta→purple squircle (~#F58FD8 → #C24FC8 → #9B50D0), white tick-dial + vertical hand | (estimated)(inferred) | In-HUD timer icon, ~56–60pt squircle |

### Brand (marketing composite — NOT app-UI tokens, kept separate)
| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/app-icon | near-black squircle ~#111111, warm top rim-light ~#C9A24A; blob gradient magenta-pink→peach (~#F06FD0 → #F5B98A) with two black "sleepy-eyes" arcs | (estimated)(inferred) | The resting/calm face — the app's entire wellness thesis in one mark; warm rim-light reads as a Liquid-Glass specular edge |
| brand/headline | Bold rounded sans, #FFFFFF — "Smart breaks for healthy eyes and a focused mind" | (estimated)(inferred) | Marketing typography; same rounded family as the HUD |
| brand/backdrop | near-black with a warm olive/amber gradient wash, top-left | (estimated)(inferred) | Composite backdrop, not the app surface |

## Layout skeletons

**Pre-break reminder HUD (cover.png):** the live desktop wallpaper (warm-orange macOS Ventura default — the *user's* desktop, not app chrome) fills the frame. A single wide translucent glass card floats over it, radius ~24–32pt, warm-tinting to the wallpaper. Interior, two rows:
- **Header row:** leading timer-icon squircle (~56–60pt), then a two-line text block — large white countdown `00:40` (primary) stacked over the amber reassurance subtitle (secondary). Icon-to-text gap tight; title-to-subtitle gap tighter than the gap down to the action row (Gestalt proximity holds).
- **Action row:** a left-aligned prominent capsule ("Start break now", brighter frosted fill) followed by three quiet outlined capsule pills ("+1m", "+5m", "+15m") on one shared baseline. No traffic lights, no toolbar, no window frame — correct for a borderless overlay (like a sheet/alert).

## Signature moves
- **[GOLDEN-NUGGET] Primary action signaled by luminance, not the system accent.** Because the whole panel is a wallpaper-tinted *warm* glass, binding to the user's `controlAccentColor` (typically blue) would clash — so LookAway promotes "Start break now" with a **brighter frosted fill** and lets the snooze options recede to translucent outlined pills. It achieves textbook action singularity (Von Restorff) through brightness alone. A deliberate, coherent adaptation to a tinted surface — but it means the app opts out of native accent binding (see Defects).
- **[GOLDEN-NUGGET] The aesthetic *is* the compliance strategy.** A break nag is inherently unwelcome; disabling it is one click away. LookAway de-escalates the interruption with warmth — soft rounded-terminal type, a calm sleepy-eyes mascot, warm amber copy that *reassures* rather than commands ("Your eyes will appreciate this"), and a glass that adapts to the desktop so it feels part of the environment rather than an alien alert. The polish is a retention lever (aesthetic-usability effect), not decoration.
- **Graduated snooze ladder** (+1m / +5m / +15m) beside the primary — structured, low-friction deferral instead of a binary dismiss; agency over the interruption while keeping the choice count at 4 (Hick's).

## Defects
- **UI Contrast Dilution (#10, borderline).** The three outlined snooze pills use a thin translucent-cream stroke on dark maroon that likely falls under the 3:1 non-text floor — the borders barely register. Canon fix: raise stroke contrast or give the recessive pills a faint translucent fill so the edge reads without shouting.
- **Accent binding absent (signature, not anti-pattern).** No `controlAccentColor`; primary is luminance-only. Per defect-vs-signature (persona §2.3) this is *systematic + purposeful + accessible* on a warm-tinted HUD → recorded as a signature move, but it is the one place a strict native reading diverges, so the surface is **excluded from macOS accent canon** (lineage gate).
- **Evidence poverty (not the app's fault).** One surface, one state, from a marketing render over a single warm wallpaper. Unseen: the menu-bar extra (near-certain), settings, onboarding, the full-screen break overlay, and glass-tint robustness on a cool/dark desktop. All metrics are ratio estimates.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| pre-break reminder HUD (dark glass over warm desktop) | 8/14 (5 N/A on a glanceable HUD) | Pass: #1 grid (regular spacing), #2 alignment (icon/text/buttons share axes), #3 proximity, #4 modular scale (3 sizes), #7 de-emphasis (amber subtitle), #8 action singularity (one luminance primary), #9 text contrast (white 00:40 >7:1), #11 Fitts (~40pt targets). **Borderline-fail #10** UI contrast (outlined-pill strokes < 3:1). N/A: #5 line-height, #6 measure, #12 input height, #13 label proximity, #14 focus (no multi-line text / inputs / static focus). |
| — native-tells audit | 4/10 (3 N/A) | Pass: #2 glass on floating chrome only, buttons are translucent fills not nested glass · #7 one prominent action + correct button grammar · #8 capsule bezels + concentric card · #10 no faked chrome (borderless overlay, legitimately no traffic lights). Deviations: #1 lineage unconfirmable from surface · #5 not literal native density (justified — glanceable HUD) · #6 no accent binding (signature). N/A: #3 selection, #4 sidebar headers, #9 toolbar (none present). |
