# Shake it On — profile

- **Source:** macapp.supply · **Surfaces digested:** Settings window (dark) · 4 marketing/brand composites (context only) · **Last updated:** 2026-07-19
- **One-sentence identity:** A keep-awake menu-bar utility whose native SwiftUI settings form is competent-anonymous, redeemed by one committed choice — every active control wears a warm brand orange instead of the system accent, threading the icon's wooden-maraca warmth into the UI. Functional peers: Amphetamine, KeepingYouAwake, Lungo. UI peer: System Settings' grouped `Form`.
- **Cluster:** unassigned (candidate: warm-indie / menu-bar-utility)
- **Lineage:** native (high) — SwiftUI grouped `Form`: rounded inset row-groups, native `Toggle`/radio controls, real "Settings" window chrome. Only native evidence feeds canon; the brand-orange accent override is logged as a native-tell, not learned as mac taste.
- **Era (chrome):** big-sur (modern flat native, post-Big-Sur grouped-settings idiom) — no Liquid Glass evidence present, which is legitimate for a flat opaque settings window; not legacy (rounded tonal groups, capsule switches).

## Evidence quality caveat
All five supplied images are 4:5 / 1.9:1 **marketing renders**, not raw app captures. Only **shot-4** contains app UI — a "Shake It On Settings" window composited on a blue backdrop under a "Smart conditions" headline, at a slight perspective tilt. Colours sampled from the render are reliable `(measured)`; all geometry (window width, row heights, control sizes) is `(estimated)` from a scaled/tilted render and cannot be resolved to true points. Cover, shot-1, shot-2, shot-3, shot-5 are brand/explainer slides — analysed as brand evidence, never conflated with app-UI evidence.

## Tokens

### App UI (shot-4, dark settings — native evidence)
| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window | #1B1B1B (measured)(inferred) | | window body + titlebar, near-uniform. Kit dark window bg is #1E1E1E — within render tolerance |
| surface/group | #222222 (measured)(inferred) | | inset row-group container; ~+7L tonal-elevation step above window — dark-mode-correct (no pure black) |
| accent/brand-orange | #F78523 / rgb(247,133,35) (measured)(confirmed) | | on radio fill AND switch-ON tracks. NOT system accent; system orange (dark) is #FF9230. Hardcoded brand hue — see Signature & Defects |
| control/switch-knob-on | #FFEDE0 (measured)(inferred) | | warm off-white knob, faintly cream (not pure #FFF) |
| control/switch-off-track | ~#373737 (measured)(inferred) | | native dark OFF track; knob ~#E1E1E1 seated left |
| text/primary | #FFFFFF (~85%) (estimated)(confirmed) | | row labels, title, section headers |
| text/section-header | white, bold, Title Case (estimated)(confirmed) | | "Activation" / "Only Shake If" / "Paused When" — Headline-role weight, sentence/title case (passes the uppercase-header tell) |
| text/tertiary | mid-grey ~#7D7D7D–#8E8E8E (estimated)(inferred) | | group caption "…at least one must be true to shake." — contrast ~4:1, marginal in dark |
| type/body | ~13–14pt SF Pro Regular (estimated)(inferred) | | row labels; single-line rows |
| type/caption | ~11–12pt SF Pro Regular (estimated)(inferred) | | tertiary helper line |
| radius/group | rounded inset card (estimated)(inferred) | | concentric with capsule switches; exact px unrecoverable from tilted render |
| control/switch | native capsule `Toggle` (measured)(confirmed) | | ~1.8:1 track ratio; ON=orange, OFF=dark |
| separators | hairline ~#2E2E2E on #222 group (estimated)(inferred) | | inter-row dividers; low-contrast (native convention) |

### Brand / marketing (context only — NOT native canon)
| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/blue | #4AAFE8 (measured) | | backdrops, "worst" highlight, numbered circles, card left-borders — the primary brand hue |
| brand/blue-hero-gradient | ~#3DA1D9 → #5CBBEF (measured) | | cover/shot-1 hero backdrop |
| brand/blue-tint-surface | #E8F4FD (measured) | | explainer-slide + card backgrounds |
| brand/coral | #E8734A (measured) | | bullet markers (shot-2) — a coral, distinct from the UI's purer orange #F78523: two warm accents in the system |
| brand/display | high-contrast serif **italic** (Playfair/Didone-class) (estimated) | | "Your Mac sleeps at the worst times", "How it works", "Smart conditions" — editorial voice |
| brand/wordmark | bold rounded geometric grotesk (estimated) | | "Shake It On" lockup — SF Rounded / Poppins-class |
| brand/icon | emoji-composite: 🪇 maracas + shaking hand + arrow cursor, blue rounded-square, soft top-light (measured) | | playful, literal; ties the orange-wood accent to the UI |

## Layout skeletons

**Settings window (shot-4, dark) — SwiftUI grouped `Form`:**
- **Titlebar** (~33pt-class): traffic lights leading — red (close) / yellow (minimize) / **grey (zoom disabled)**, the settings-window dimming HIG expects; title "Shake It On Settings" left-aligned immediately after the lights (not centered), primary-label weight.
- **Content:** single column, symmetric left/right gutter, sections stacked top-to-bottom.
- **Section unit:** bold Title-Case header (flush left, generous space above) → one rounded inset group (#222) of full-width rows with hairline separators → optional tertiary caption trailing the group.
- **Row grammar:** label left on a shared X-axis; control trailing on a shared right axis. Row types seen: (a) *Mode* — a two-option radio pair "Always active" (selected, orange) / "Only when idle"; (b) condition rows — single trailing `Toggle`.
- **Sections:** `Activation` (Mode radio) · `Only Shake If` (6 condition switches: Audio playing, App matching, Wi-Fi, External display, CPU threshold, External disk — all OFF; caption "When any of these are checked, at least one must be true to shake.") · `Paused When` (Display off/locked ON, Screensaver running ON, Focus/DND cut off).

## Signature moves
- **[GOLDEN-NUGGET] Brand-orange accent override.** Every *active* control — the selected radio and both ON switches — renders in a warm brand orange (#F78523), not the system accent. It is systematic (no active control escapes it), purposeful (carries the icon's wooden-maraca / warm-hand palette into an otherwise default-dark settings pane), and accessible (orange-on-dark clears contrast). Per the defect-vs-signature rule this is a **signature** — but it doubles as a native-tell deviation (see Defects). In a category of blue-by-default keep-awake utilities, the orange is the app's entire visual identity inside the UI.
- **Declarative "smart conditions" model.** The when-to-jiggle logic is exposed as two plain-language toggle groups (`Only Shake If` = OR-gate, `Paused When` = veto) with a one-line caption spelling out the boolean ("at least one must be true"). Recognition over recall; Tesler's Law honoured — the app absorbs the scheduling complexity into declarative switches instead of a rule editor.

## Defects
- **Accent not bound to the system (native-tell #6).** Controls hardcode brand orange rather than `controlAccentColor`; a user whose system accent is blue/pink/graphite still sees orange. Canon-native behaviour: bind selection/active-control tint to the system accent, reserve brand hue for illustration/onboarding. Recorded as a deliberate brand trade-off, not sloppiness — but it is why this UI would never read as "system-default."
- **Marginal tertiary contrast (soft, rubric #9).** The group caption (~#7D7D7D on #1B1B1B) sits near ~4:1 — legible but under the 4.5:1 body floor for its size class.
- **Low-contrast OFF-switch tracks & separators (soft, rubric #10).** OFF track (~#373737) vs group (#222) is ~1.3:1 and hairline separators are barely present — native convention, flagged for completeness, not a fault.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| Settings window (dark) | 12/14 | #9 tertiary caption ~4:1 (marginal); #10 OFF-switch track ~1.3:1 / faint separators (native convention). #12/#14 N/A (no text fields; no focus state in still). |
| — native-tells audit | 8/10 | #6 accent hardcoded orange, not system-bound (the headline miss). #3 selection-grammar N/A (no list), #9 toolbar N/A (none). |
```