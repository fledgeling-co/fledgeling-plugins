# hora Calendar — profile

- **Source:** macapp.supply (meta + cover + 6 marketing shots) · **Surfaces digested:** week view (main window), event context menu, menu-bar-extra popover, NLP quick-add popover, focus-drag pill, multi-window theming board · **Last updated:** 2026-07-19
- **One-sentence identity:** Notion Calendar's (Cron's) keyboard-driven week grid reskinned in a Tokyo-Night developer palette — a Google-Calendar client dressed as a code editor, with a Superhuman-grade NLP command bar bolted on.
- **Cluster:** unassigned (proposes a new "developer-dark productivity" cluster — sole member so far)
- **Lineage:** native (med confidence) — SwiftUI/AppKit reading. Decisive tell: the event context menu renders real SF Symbols with native ⌘X/⌘C/⌘D shortcut glyphs, a ⌫ delete symbol, submenu chevrons and grouped separators (see shot-2 crop); shot-1 shows a genuine macOS menu bar hosting the app's menu-bar-extra. Electron rarely reaches this menu fidelity. Residual doubt is only because the app is otherwise heavily custom-themed. Non-native *styling* choices (below) are signatures/defects, not lineage evidence.
- **Era (chrome):** big-sur → sequoia flat-native (pre-Liquid-Glass): opaque dark chrome, flat borderless toolbar symbols, no lensing edges, no scroll-edge glass observed. Heavily custom **dark-only** theming (ships Tokyo Night / Gruvbox / Osaka Jade code-editor schemes) sits on top of standard native window chrome.

## Tokens

All measurements from @2x marketing shots (2880×1800 → 1440×900 logical); pixel reads halved. Dark mode only — no light-mode app surface supplied.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window-canvas | ~#141417 near-black | (estimated)(confirmed) | week-grid canvas; every app shot is dark |
| bg/sidebar | ~#0D0D10, marginally darker than canvas | (estimated)(inferred) | left calendar list + right command rail |
| accent/brand | ~#F5333B electric red-coral | (estimated)(confirmed) | app-icon, marketing headlines, "NEVER MISS A THING" badges — **brand/chrome only** |
| accent/interactive | system blue ~#0A84FF (kit dark blue #0091FF) | (estimated)(confirmed) | OK / Accept / Join-Meet / "Today" pill / date badge — the in-app primary hue, kept distinct from brand red |
| event/identity-palette | 12-hue system-adjacent set (red, orange, yellow/olive, green, teal, cyan, blue, indigo, purple, pink) | (estimated)(confirmed) | per-calendar identity colours, translucent fill + solid left/edge stroke; matches macOS 12-hue logic |
| type/title | ~22pt Bold SF Pro ("June"), "2026" same size lighter | (estimated)(confirmed) | Title1-class; de-emphasis via colour not size |
| type/body | ~13pt SF Pro, event titles Semibold/Bold | (estimated)(confirmed) | matches kit Body 13pt |
| type/secondary | ~11pt SF Pro (event times, TZ, "W23") | (estimated)(confirmed) | Subheadline-class, ~50–55% label |
| type/caption | ~10pt (keycap chips, day-header dates) | (estimated)(inferred) | Caption-class |
| radius/event-block | ~6px | (estimated)(confirmed) | rounded event cards |
| radius/window | ~10–12px | (estimated)(inferred) | observed dark-window corner |
| radius/keycap-chip | ~4px | (estimated)(inferred) | shortcut key-caps in right rail |
| radius/pill-chip | capsule | (estimated)(confirmed) | Join pills, NLP token chips, marketing badges |
| chrome/toolbar-height | ~48–52pt | (estimated)(confirmed) | unified toolbar strip |
| control/segmented-height | ~28pt (Day/Week/Month capsule) | (estimated)(confirmed) | native-reading segmented control |
| sidebar/width (left) | ~230–256pt | (estimated)(confirmed) | calendar-visibility list |
| sidebar/row-height | ~30–32pt | (estimated)(confirmed) | checkbox + label rows |
| rail/width (right) | ~260–300pt | (estimated)(confirmed) | keyboard-command + pomodoro inspector |
| rail/section-header | tracked-UPPERCASE ~10pt secondary ("NAVIGATION"/"VIEWS"/"ACTIONS") | (estimated)(confirmed) | **DEFECT** vs native sentence-case semibold header grammar |
| now-indicator | red hairline + red time-pill ("9:17"/"19:39") | (estimated)(confirmed) | current-time line in week grid |
| gutter/dual-timezone | two stacked hour columns side-by-side (home TZ + secondary) | (estimated)(confirmed) | signature grid feature |
| marketing/headline-font | bold geometric grotesque (Satoshi/General-Sans class) | (estimated) | **brand only, not the app UI** (app UI is SF Pro) |
| marketing/wordmark | brush-script "Calendar" after rounded-square "h" icon | (estimated) | brand lockup |
| marketing/backdrop | near-black + faint blueprint grid + red(left)/blue(right)/green radial glows | (estimated) | composite backdrop, not app evidence |

## Layout skeletons

**Main window — week view (shot-2, shot-4, shot-6 center).** Three-pane split under a unified toolbar.
- Toolbar (l→r): sidebar-toggle · "+" new-event · moon theme/appearance toggle · [center] Day/Week/Month segmented capsule · [right of center] "‹ Today ›" date nav (Today in a pill) · [trailing] search · refresh · right-inspector toggle. Borderless monochrome SF Symbols; slightly >3 groups but calendar-reasonable.
- Left pane (~230–256pt): calendar-visibility list. Sentence-case section headers "Private" / "Other"; rows = per-calendar coloured checkbox + name (hora Planning purple-checked, Formula 1 red-checked, Holidays in Poland checked; Private/Family unchecked).
- Center: "June 2026" super-title (bold + light year) over dual-timezone hour gutter; day-column headers "Mon 1 … Fri 5" with today's date in a filled circle badge; all-day pill row; time-grid with translucent coloured event blocks (bold title / secondary time / video + recurrence glyphs); red now-line.
- Right pane (~260–300pt): the command rail — UPPERCASE groups NAVIGATION / VIEWS / ACTIONS each a list of `label ……… keycap-chip(s)`, then POMODORO TIMER with a large circular focus ring + play/reset + mode row.

**Event context menu (shot-2).** Native dark menu: Edit(↵) · Event color › · Move to Calendar › · Block on calendar › · │ Cut ⌘X · Copy ⌘C · Duplicate ⌘D · │ Delete ⌫. SF Symbol per row, right-aligned shortcut glyphs, submenu chevrons, group separators.

**Menu-bar-extra popover (shot-1).** Status item "ends in 42m" → popover "Upcoming ends in 42m": time-stamped event rows with ALL-DAY badges and coloured Join pills (blue Meet / purple / green), a "Tomorrow" section, and a bottom Focus 25:00 pomodoro strip with day counters + play.

**NLP quick-add popover (shot-5).** Centered dark rounded popover: calendar-plus glyph + echoed query "Lunch with Ania tomorrow 3pm at Jerry's"; parsed token row (person chip green "Ania" + dashed "+add", date chip blue "tomorrow 3pm", location chip amber "Jerry's"); action row "↵ Accept" (blue) · "⌘⇧↵ Edit details" (blue) · "esc" (dark).

**Focus-drag pill (shot-4).** Small translucent floating pill over the grid during drag: moon glyph + "10:00 – 18:00 · 3 days" + Cancel(leading) / OK(blue, trailing).

**Theming board (shot-6).** Same week view rendered across 3 stacked windows in different dark schemes — evidences a first-class theme system, not a single skin.

## Signature moves
- **[GOLDEN-NUGGET] The persistent right-hand keyboard-command rail.** A live shortcut cheat-sheet (NAVIGATION/VIEWS/ACTIONS, each row a label + physical keycap chips) with an embedded Pomodoro focus ring. It puts the app's entire "fast, keyboard-driven, made-for-work" thesis permanently on screen. It is simultaneously the app's clearest identity and its single biggest native-grammar deviation (a Superhuman/Linear transplant with tracked-uppercase headers).
- **Dual-timezone hour gutter** in the week grid — two time columns side-by-side (home + secondary TZ), a genuinely useful density choice for remote/global work.
- **Code-editor theming.** Tokyo Night / Gruvbox / Osaka Jade — the calendar borrows the developer-colourscheme world wholesale; per-event colours still come from the system 12-hue palette, so identity colour and theme chrome stay separate.
- **NLP quick-add with live parsed token chips** (person=green, date=blue, location=amber) — Superhuman-grade command entry, the "speed of thought" claim made concrete.
- **Menu-bar-extra "ends in Xm" countdown + one-click Join pills** — next-meeting-in-the-menu-bar, a real native menu-bar-extra done well.
- **Accent discipline across two hues:** brand electric-red owns the icon/marketing/chrome; system-blue owns every in-app interactive primary (OK/Accept/Join/Today). They never collide — a deliberate, well-held separation.

## Defects
- **Sidebar-header grammar (right rail):** tracked-UPPERCASE "NAVIGATION/VIEWS/ACTIONS" section headers violate the #1 macOS list-header authenticity rule (should be sentence-case, semibold, secondary colour). Systematic → house style, but a native-grammar miss.
- **Bespoke keycap command rail** is a cross-platform (Superhuman/Cron) pattern, not a macOS-native surface. Recorded as a lineage *tell*; excluded from any macOS canon. Deliberate and on-brand, so not a "fix", but it does not read as system-native.
- **Contrast Dilution risk:** secondary event metadata (e.g. "9:00 – 10:00" muted) on translucent dark-coloured event fills reads borderline <4.5:1 in the redder/greener blocks. Calendar convention, but flag for the fix (raise metadata alpha on saturated fills).
- **Focus appearance:** no visible keyboard focus ring evidenced in any still — cannot verify WCAG 2.4.13. Out of scope for static analysis; note as unverified.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| Week view (main window) | 12/14 | #9 event-metadata contrast borderline on saturated fills; #14 focus state not evidenced |
| Event context menu | 13/14 | #14 focus not evidenced (otherwise textbook native menu) |
| Menu-bar-extra popover | 12/14 | #9 some Join-pill/label contrast borderline; #14 not evidenced |
| NLP quick-add popover | 12/14 | #10 dashed "+add" chip border <3:1; #14 not evidenced |
| Theming board | 12/14 | inherits week-view #9/#14 |

### Native-tells audit (10-pt, macOS)
| Surface | Score | Fails |
|---|---|---|
| Week view | 8/10 | #4 tracked-uppercase rail headers; and the keycap command rail is a non-native pattern (counted against #4/general grammar) |
| Context menu | 10/10 | — clean native menu |
| Menu-bar-extra | 9/10 | minor: Join pills are colour+label (ok); otherwise native |
| NLP quick-add | 8/10 | floating translucent popover ok; token-chip surface is bespoke, not a standard macOS control |

**Averages (analysable UI surfaces):** ~12.2/14 rubric · ~8.75/10 native.
