# Native Foundation — the platform floor every design stands on

Distilled from Apple's macOS 27 UI kit (deconstructed from its Sketch JSON — values marked `(specified)` are exact kit data) and the macosify-derived native grammar. Use these values directly when building; deeper detail lives in the macosify plugin's `reference/hig/` and `reference/DESIGN.md`.

**Provenance, and why the `(specified)` tier exists.** Two independent research backends
searched for a complete public Apple table of control heights, bar heights, radii, blur
radii and glass opacities in August 2026 and **both returned it as missing** — Apple
publishes semantic APIs, control-size *names* and the type ramp, not a universal geometry
table. The deconstructed kit is therefore the only route to the numbers below, which is
what makes this file load-bearing rather than a restatement of the HIG. Where the HIG
speaks to the same thing, **the HIG wins**; those rows are tagged `(hig)`.
Sourcing, corroboration counts and the conflict register: `evidence.md`.

**Which macOS.** macOS 26 "Tahoe" is shipping; macOS **27 "Golden Gate" was still beta on
2026-08-18** `(hig)`. The values here are the Tahoe-era floor. The 27-era deltas are at the
end of this file, separated deliberately, because a beta refinement applied as though
shipped is a defect a reviewer cannot distinguish from a choice.

## Control metrics `(specified)`

One height ladder for all control families:

| Tier | Height | Use |
|---|---|---|
| Mini | 16 | dense inspectors |
| Small | 20 | compact panels |
| **Regular** | **24** | default everywhere |
| Large | 28 | emphasized contexts |
| **XL** | **36** | toolbars |

**Height is not target `(hig)`.** Apple's published accessibility guidance gives macOS a
default target of **28×28pt** and a hard minimum of **20×20pt** — against iOS's 44×44 and
28×28. The ladder above is the *drawn control*; 28pt is the *target it should answer to*.
So the rule is a pair rather than a choice: **draw on the ladder, pad the hit area to
28pt**, and never take an interactive element below 20pt. A 44pt control is the iOS number,
and on a Mac surface it is the tell. Neither value supersedes the other and neither is
dropped.

- Push button: label inset 16px per side; bezel reads capsule in the Liquid Glass era. Styles: Bordered / Bordered Default (the one accent-filled) / Bordered Tinted / Bordered Destructive / Borderless / Toggle.
- Fields: default 120w; text inset 6px (Rg); bezel radius ladder ~2.5 (Mn) → 6.5 (XL); focus ring radius 4/5/6/7/9 by tier. Search fields are capsules.
- Switches 44×20 (Sm) – 80×36 (XL), capsule; checkboxes/radios 14–18pt (Mn/Sm) and by-meaning: checkbox = independent setting, radio = exclusive set, switch = emphasized group toggle only.
- Scrollbar 12pt gutter, capsule thumb. Steppers pair with an editable field, always.

## Type `(specified)` — SF Pro (`-apple-system` stack; never bundle fonts)

| Role | Size | LH | Emphasized |
|---|---|---|---|
| LargeTitle | 26 | 32 | Bold |
| Title1 / Title2 / Title3 | 22 / 17 / 15 | 26 / 22 / 20 | Bold / Bold / Semibold |
| Headline | 13 (Bold) | 16 | Heavy |
| **Body** | **13** | **16** | Semibold |
| Callout / Subheadline | 12 / 11 | 15 / 14 | Semibold |
| Footnote / Caption | 10 | 13 | Semibold |

Loose leading = +2pt, tight = −2pt. Emphasis via Semibold, not Bold. 13pt body is the loudest native-vs-iOS/web discriminator — 17pt or 16px body means it isn't a mac app.

**Corroborated `(hig)`, and one addition.** Two independent research backends returned this
exact ramp from `developer.apple.com/design/human-interface-guidelines/typography` in
August 2026, matching the kit table row for row — so this is the rare table with three-way
agreement. The addition: **10pt is a published hard minimum for meaningful text**, and
Apple names the weights to avoid — Ultralight, Thin and Light — preferring Regular, Medium,
Semibold, Bold, "especially when text is small."

**The ramp that gets imported by mistake** is iOS's, where Large Title is **34pt** and
Title 1 is **28pt**. One research backend returned those as macOS values from an unverified
source. A 34pt "Large Title" on a Mac surface is a diagnostic, not a taste call.

## Colour `(specified)`

- **Label tiers (light):** primary `#000` @85% · secondary @50% · tertiary @25% · quaternary @10%. (Dark: `#FFF` @100/55/25/10%.) Primary is never pure black.

> **The light secondary tier fails the contrast floor this skill enforces, and that is
> where Contrast Dilution comes from.** Measured 2026-08-18 with the sRGB formula
> `scripts/mock_check.py` uses: black @50% on `#FFFFFF` is **3.98:1** — under the 4.5:1 AA
> floor for body text — while white @50% on `#1E1E1E` is 5.12:1 and passes. The *same tier
> name* passes in dark and fails in light, which is exactly why the failure is invisible to
> a reviewer who checked one appearance. Tertiary @25% is **1.83:1** light and 2.28:1 dark
> and can never carry text at all.
>
> So the usable rule, which supersedes the raw kit tier for any text that carries meaning:
> **light secondary at ≥55% (4.76:1), 60% for comfort; tertiary and quaternary are divider
> and disabled tiers only.** Keep the kit percentages for genuinely non-essential text —
> that is what the platform uses them for — and never report a 50% label as compliant.
> Contrast Dilution appears in **72 of 135** corpus apps, and this table is its origin.

- **Fills (bezels/tracks):** black/white @10/8/5/3/2%.
- **System hues (light / dark):** Red `#FF383C/#FF4245` · Orange `#FF8D28/#FF9230` · Yellow `#FFCC00/#FFD600` · Green `#34C759/#30D158` · Mint `#00C8B3/#00DAC3` · Teal `#00C3D0/#00D2E0` · Cyan `#00C0E8/#3CD3FE` · Blue `#0088FF/#0091FF` · Indigo `#6155F5/#6D7CFF` · Purple `#CB30E0/#DB34F2` · Pink `#FF2D55/#FF375F` · Brown `#AC7F5E/#B78A66`.

> **A system hue is not automatically a legible fill.** White 13pt on kit Blue `#0088FF` is
> **3.52:1** — Apple's own Bordered Default button sits below AA for body text. Keep the kit
> hue for rings, selection and graphics where no text sits on it, and carry a second token
> for text-bearing accent fills: `#0071E3` is 4.70:1 and reads as the same blue. The gate
> reports a system-hue failure with a different message from an ordinary one, because
> "the platform does it" is a real fact with a different fix, and treating it as an
> exemption is how dilution spreads.

- Window backgrounds: `#FFFFFF` light / `#1E1E1E` dark; dark chrome is graphite (~`#2C2C2E`–`#3A3A3C` surfaces), never pure black; author dark independently, never invert.
- Bind selection/focus/primary-action to ONE accent (the user's, conceptually); per-item identity colours come from the 12-hue palette and are separate; status colour always pairs with a glyph/label.
- **Selection duality `(hig)`:** a focused list's selected row is an accent fill with white text; an *unfocused* window's selected row is a grey fill with standard text. Two states, not one dimmed. Hover styling is never reused as selection.
- **Increased contrast must be authored per appearance.** One scheme-agnostic override is the trap: a single `prefers-contrast` block that darkens the secondary label paints black on graphite in dark mode — an increased-contrast mode that *reduces* contrast, invisible in any light-mode review. Found by the gate on this skill's own fixture.

## Chrome anatomy `(specified)`

| Element | Value |
|---|---|
| Titlebar | 33pt; traffic-light cluster 68×14 at (9, 9.5); inset scales with bar height (concentric ratio) |
| Unified toolbar | 52pt (8 + 36 XL controls + 8) · compact 40pt (Rg controls) · expanded 77pt |
| Sidebar | 256pt wide; rows 24/32/40 (S/M/L); selection = inset rounded fill, radius 8, 4px side insets |
| Menus | items 19/22/24 (Mini/Small/Regular); selection radius 8; inner padding 12–14 |
| Popover radius | 20 · Alert buttons 228×28 stacked · Tooltip min 98×19 |
| Scroll edge effect | content slides under glass chrome with a translucent fade — include it wherever content meets a floating toolbar |

Concentric corners: child radius = parent − padding; capsule = height/2. Window radius is era-fragmented — pick one and keep every nested radius concentric to it.

**Concentric is a named platform relationship, not a rule of thumb `(hig)`.** Apple ships
`concentricCornerRadii(in:)`, which computes a child's radius as *the container's radius
minus the distance from the child's corner to the container's corner* — the same arithmetic,
now with a citation and an API a SwiftUI implementer can call. macOS 27 adds AppKit support.
So do not prescribe a universal `12px`; state the **relationship** (`containerConcentric` or
`independent`) and let the implementer resolve it. And the window radius itself stays
unresolved: one research backend claims macOS 27 standardises it at 20pt down from Tahoe's
26pt, and both of its sources fail to resolve, while the first-party corroboration confirms
only "tighter corners" with no number. Pick one and be concentric to it.

## Materials `(hig)`

Liquid Glass is **adaptive**, which is why a fixed CSS blur is a poor specification and a
semantic material role is a good one.

- **Two variants.** *Regular* blurs and adjusts the luminosity of what is behind it to keep
  text legible, and is what most components use — alerts, sidebars, popovers, anything
  text-heavy. *Clear* is more translucent, for components floating over photos and video
  where seeing through matters more than maximum contrast.
- **A clear-variant component over bright content needs a dimming layer: dark at 35%
  opacity.** Not needed when the content behind is already dark, or when the system's own
  media controls supply their own. This is the only concrete opacity figure the research
  produced, and it is first-party.
- **Standard materials** — `ultraThin`, `thin`, `regular`, `thick` — carry the content
  layer; thickness is chosen by how much the overlay should obscure, and `thick` is the one
  for a dark colour scheme.
- **Glass never goes in the content layer.** Apple's own words: including it there creates
  "unnecessary complexity and a confusing visual hierarchy." Three research backends, one
  page. This is grammar rule 3 below, now cited.
- **Vibrancy**: macOS provides vibrant variants of every system colour so foreground content
  holds up against a changing background. Over any translucent surface, use the vibrant
  treatment rather than a flat grey.
- **One scroll-edge effect per scrollable pane.** In a split view each pane may have one, at
  consistent heights; two stacked in one pane is wrong.
- **Reduce Transparency means opaque, as a direction rather than a preference.** And on
  macOS, turning on Increase Contrast *also* forces Reduce Transparency — the two cannot be
  separated (community-sourced) — so an increased-contrast pass must assume solid surfaces.
- One tension worth holding rather than resolving: Apple's Materials guidance says to
  *prefer translucency to opaque colours in windows*, while the corpus shows flat opaque
  windows shipping widely and legitimately. Apple states a preference; real apps exercise
  the exception. Do not read the preference as licence to put glass on everything — that
  collides with the rule three bullets up.

## The native grammar (10 rules to design by)

Each rule carries **the symptom you would see if you broke it**, because a rule whose
violation is invisible needs a gate rather than a sentence — and the ones that are
greppable say which gate check catches them.

1. **Selection** = flat inset rounded fill + accent text/glyph — never full-bleed bars or glossy capsules. *Symptom:* the selected row reads as a coloured banner rather than a seat; and the unfocused-window state looks identical to the focused one, because only one was drawn.
2. **Sidebar / section headers**: system font, semibold, secondary colour. **Never tracked uppercase at heading size.** *Symptom:* the header competes with the content it labels instead of receding under it — and it is the single most reliable web tell a Mac user names first. `mock_check.py [casing]` fails this above 13px. On casing generally, see the note under the audits below: title case for menu-bar items is sourced, blanket sentence case is not.
3. **Liquid Glass only on floating chrome** (toolbar/sidebar/menus/popovers/sheets); content opaque; no glass-on-glass; a flat opaque window is legitimately native. *Symptom:* body text sits on a surface that shifts as the wallpaper changes, so legibility is a property of the user's desktop picture rather than of your design. Apple's own words for it: "unnecessary complexity and a confusing visual hierarchy."
4. **One prominent (accent-filled) action per view**, trailing; Cancel leading; destructive never default; "…" = opens a further view; **disabled dims, never disappears**. *Symptom:* two saturated buttons means neither is the answer to the surface's question; and a control that vanishes when unavailable makes the layout jump and teaches the user the feature does not exist.
5. **Density**: 13pt body, 24pt controls padded to a 28pt target, 24–28pt rows; hierarchy via label tiers and weight, not size inflation. *Symptom:* the window holds a third of the information a Mac user expects at that size, which reads as a port rather than a design.
6. **Pop-up (double chevron, shows a value) ≠ pull-down (single chevron, static title).** Control by meaning (checkbox / radio / switch / segmented rules above); segmented controls switch views in-place — never main navigation. *Symptom:* the user cannot tell what the control currently *is* from looking at it, only what it does.
7. **Toolbar**: borderless monochrome SF Symbols, ≤3 groups, one trailing primary; window title useful and content-bearing, **under ~15 characters, never the app name** `(hig)`. **Every toolbar command also exists in the menu bar** `(hig)` — people hide and customise toolbars, so a toolbar-only command is a command that can disappear. *Symptom:* bezelled toolbar buttons read as in-content buttons; a title of the app's own name tells the user nothing about which of their four windows this is.
8. **Forms**: right-aligned colon labels + left-aligned controls on a shared edge, flat on one surface — no stacked labels, no iOS grouped cards. *Symptom:* the eye cannot scan a column of values because each label pushes its control to a different x.
9. **Real chrome**: genuine traffic-light geometry, **arrow cursor**, focus states; menu bar is the complete command surface (note it in the spec even if unrendered). Sidebars go **no more than two hierarchy levels** deep; deeper needs a middle list pane `(hig)`. *Symptom:* a hand cursor over a button, which is the loudest tell in the set and the one `mock_check.py [cursor]` fails outright.
10. **Motion** (when specified): transform/opacity only, ~150/250/400ms, honour Reduce Motion. *Symptom:* none you can see in a mock — **this is the rule with no visible symptom, and this house's browser executes no CSS animation at all**, so it is asserted in the motion spec and verified nowhere. Say so rather than claiming it.

## Delivery audits

**Native-tells audit (10 checks — all pass unless a named deliberate deviation):** lineage reads native · glass discipline · selection grammar · header casing · density · accent binding · action singularity · concentric corners · toolbar grammar · real chrome.

**Quality rubric (14 checks, from the digest skill's knowledge base):** 8pt grid adherence · 12-col/edge alignment · proximity grouping (between-group > within-group) · ≤6 font sizes on a modular scale · line-height inverse to size · ~65ch measure · de-emphasis hierarchy · one saturated primary per region · 4.5:1 text contrast · 3:1 UI contrast · target minimums (**20pt hard floor, 28pt default target**; 44pt only for touch-adjacent) · input heights ≥ Rg tier · label proximity · focus appearance (2px ring, 3:1 shift).

**Neither audit is self-reportable.** Six of these twenty-four points are computed by
`scripts/mock_check.py` and the rest are read by a person looking at a render. A score
written without either is the failure this skill was rebuilt around: one recorded run
reported all seven of its prose audits as PASS while a glyph sat at 1.00:1 against its own
background. Report the gate's counters verbatim, and mark every point the gate cannot see
as read-by-eye rather than folding both into one number.

**On casing, honestly.** Apple's HIG specifies **title-style capitalization with articles
removed for menu-bar items** (two independent first-party sources). Body copy, field
labels, placeholders and helper text are sentence case (same sources). **Buttons are
genuinely contested** — the corpus ships both and the third-party claim for title case
everywhere rests on sources that do not resolve. So pick one per surface and hold it,
because the citable rule is consistency within an element type. Tracked ALL-CAPS at
heading size is a tell under every reading.

## macOS 27 "Golden Gate" deltas — beta as of 2026-08-18

Kept separate on purpose. A beta refinement applied as though shipped is indistinguishable
from a mistake, so tag any of these `research` rather than `kit` and name it in the
delivery. Sourced first-party from WWDC26 sessions 112 and 289 unless noted.

- **Sidebars extend to the window edges** rather than floating inset, with content still
  flowing behind them. This reverses the most visible Tahoe-era choice.
- **Sidebar selection adds semi-bold text** as emphasis, alongside the fill.
- **Toolbar scroll-edge** resolves to a *hard* edge automatically when free-floating title
  text is present; bordered toolbar items over a sidebar take Liquid Glass.
- **Window corners are tighter.** No number is available from a source that resolves — see
  the concentric-corners note above.
- **A user-facing clarity/tint slider** for Liquid Glass, plus better diffusion of complex
  content, brighter highlights and darker edges. The consequence for design is the
  important part: **translucency is now a user preference, so it cannot carry hierarchy.**
  Anything a design needs the user to perceive must survive the material going flat.
- **Optional interactive glass response** on controls, and **AppKit concentric-corner
  support**.
- **A `showBorders` environment value**, for adding clear boundaries to custom controls
  when the system asks for them.

Report both scores honestly with every delivered design; fix or disclose misses.

