# Notion Calendar — profile

- **Source:** macapp.supply (marketing cover only — no standalone shots) · **Surfaces digested:** main window, week view, light mode · **Last updated:** 2026-07-19
- **One-sentence identity:** Superhuman's keyboard-first command grammar applied to a calendar — Cron's crisp pastel scheduling grid, now wearing Notion's neutral-web restraint.
- **Cluster:** unassigned (candidate: "command-driven-web" / productivity-web-crisp — peers Superhuman, Linear, Notion; non-native cluster)
- **Lineage:** web-electron (high) — custom hollow-ring traffic lights (a HIG-named non-native mistake), inline keycap shortcut chips, product-web typographic feel. Contrast evidence only; **excluded from macOS canon.**
- **Era (chrome):** custom-drawn Electron chrome (not Liquid Glass, not legacy-native) — flat opaque surfaces, hairline dividers, no system materials.

> Evidence caveat: the only image is a marketing composite. The app *window* (bottom band) is the design evidence; the headline wordmark, "All your commitments…" line, and the floating cat/coffee/bike sticker-icons are brand evidence, analysed separately and never merged into UI tokens. The window is rendered **downscaled (~0.85× of 1:1)** and its bottom is cropped by the cover edge, so all pixel values are `(estimated)` with wide ranges; absolute pt sizes are inferred, not measured.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/canvas | near-white `#FFFFFF`–`#FDFDFC` | (estimated)(inferred) | center grid + right panel |
| bg/sidebar-rail | warm very-light grey `#F5F4F2`±3 | (estimated)(inferred) | left mini-calendar panel |
| type/family | neutral grotesque, reads as system stack (SF Pro / `-apple-system`) | (assumed)(inferred) | can't confirm SF vs Inter at render scale |
| type/month-title | ~20–22px, "January" heavy near-black + "2024" lighter grey | (estimated)(inferred) | two-weight de-emphasis in one title |
| type/panel-heading | ~13–14px Bold, label-primary `#1A1A1A`ish | (estimated)(inferred) | "No upcoming meeting", "Scheduling snippet" |
| type/day-header | ~12–13px Regular, secondary grey | (estimated)(inferred) | "Mon 15", "Su/Mo/Tu…" — de-emphasized |
| type/event-label | ~11–12px Medium, hue-matched saturated text | (estimated)(inferred) | colored text on same-hue pastel fill |
| accent/functional | RED `#E5484D`±, hardcoded | (estimated)(inferred) | today badge + urgent; NOT bound to system accent |
| selection/week | neutral grey rounded capsule (no accent tint) | (estimated)(inferred) | current-week band in mini-cal |
| today/marker | red rounded-square, white text (mini-cal + day header badge) | (estimated)(inferred) | ~6px radius solid fill |
| identity/hues | red · blue · purple-lavender · amber-yellow · salmon-coral | (estimated)(inferred) | softer pastels than the macOS 12-hue kit |
| event/fill | pastel tint ~12–18% sat body + ~3px saturated left rail | (estimated)(inferred) | the core chip recipe |
| radius/event-chip | ~4px | (estimated)(inferred) | |
| radius/toolbar-button | ~6–8px (Week / Today bordered pills) | (estimated)(inferred) | |
| radius/keycap | ~4–5px, fill-grey chip | (estimated)(inferred) | single-letter S / F |
| divider/hairline | ~8–12% black, very faint | (estimated)(inferred) | right-panel section separators — below native 29% |
| control/toolbar-h | ~28–30px | (estimated)(inferred) | Week pull-down, Today button |
| chrome/traffic-lights | hollow grey outline rings (custom, non-native) | (estimated)(confirmed) | zoomed — confirmed hollow, not system dots |
| chrome/titlebar | single combined title+toolbar strip, ~35–40px | (estimated)(inferred) | traffic lights + sidebar toggle left; avatar/Week/Today/‹›  right |

## Layout skeletons

**Main window — week view (three-zone, left→right):**
- **Left rail (~160–170px render):** warm-grey panel. Month nav chevrons (up/down, top-right). Su–Sa column headers (secondary grey). 6×7 date grid; out-of-month days dimmed; **today = red rounded-square (white numeral)**; **current week = neutral grey rounded capsule** spanning the row.
- **Center (fluid):** week grid. Header row = timezone labels (**EST / PST dual zone**) + day columns "Mon 15 … Fri 19"; **today "Wed 17" set black-bold with a red date badge**, other days secondary grey. Below headers: full-width **all-day event band** (e.g. lavender "Augusto OOO" spanning the week). Time gutter shows **dual-timezone times stacked** (12 PM / 9 AM). Timed-event area of colored chips. **"Now" line = solid black rule + dot at 10:10 AM** (black, not red).
- **Right panel (~205–215px render):** white. Search field (magnifier + placeholder) at top. "No upcoming meeting" heading → hairline divider → "Scheduling snippet" heading + **"Share availability"** full-width quiet-fill button with an **"S" keycap** trailing → divider → "Quick meeting" + **"Meet with…"** person-icon field with an **"F" keycap** trailing.
- **Toolbar strip (top, over center+right):** circular avatar · **"Week ⌄"** pull-down · **"Today"** push button · **‹ ›** nav chevrons. No unified NSToolbar — controls float in the custom title strip.

## Signature moves
- **[GOLDEN-NUGGET] Status-as-edge-treatment event chips.** One chip vocabulary encodes meeting state without status icons: solid pastel fill = confirmed; **diagonal-hatched left rail = tentative**; **dashed outline, no fill = proposed/draft** ("Liam / Stephanie wee"); **strikethrough label = declined** ("Tools weekly sync", "Operations Research"); neutral grey = holiday/neutral all-day. Every chip also carries a ~3px saturated left rail + hue-matched label + optional emoji prefix. Five states, one system — this is the app's entire scheduling literacy in one component.
- **[GOLDEN-NUGGET] Keyboard-first keycap chips.** Inline single-letter shortcut caps (S, F) sit beside actions, declaring the Superhuman-lineage command-driven identity — the interface teaches its own shortcuts in place.
- **Dual-timezone gutter.** EST/PST rendered side-by-side in both the time gutter and the header — a power-scheduler feature promoted into the layout skeleton, not buried in settings.
- **Two-weight month title.** "January" heavy near-black + "2024" lighter grey — de-emphasis inside a single title string.
- **Red-as-today.** The one functional accent (today, urgency) is hardcoded red per the calendar-page metaphor, deliberately *not* the user's system accent; selection stays neutral grey so red always means "now".

## Defects
(Recorded as tells+corrections, not canon — lineage is web-electron.)
- **Custom traffic-light dots** (hollow grey rings) → HIG-named non-native mistake; native fix = real `NSWindow` traffic lights that fill on focus.
- **Accent not bound to system** → today/urgency hardcoded red; native fix = bind today/selection to `controlAccentColor`, keep identity hues separate.
- **Contrast Dilution risk on event labels** → hue-matched saturated text on same-hue pastel fill; amber/yellow labels ("Santiago work trip!") most at risk of dipping under 4.5:1.
- **Faint hairline dividers** (~8–12% black) → below the 3:1 UI-contrast floor and below the native ~29% separator; fix = firmer separator token.
- Inline keycaps + custom chrome are web conventions — signatures in the web cluster, native tells for macOS.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main window (week view, light) | 12/14 | #9 colored event-label text on same-hue pastel likely <4.5:1 (amber worst); #10 hairline dividers ~<3:1. #14 focus state not shown → unverifiable. |
| — native-tells audit | 6/10 | #1 web-electron not AppKit; #3 today/selection grammar custom (red square + grey capsule, not inset-rounded accent fill); #6 accent hardcoded red not `controlAccentColor`; #10 custom hollow traffic lights. |
