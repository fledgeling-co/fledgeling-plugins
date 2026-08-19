# Satu — profile

- **Source:** macapp.supply · **Surfaces digested:** menu-bar popover (no-task + active-task), Options/Settings window (Review tab, default theme; Pro tab, cream theme), floating mini window (blue theme), full-screen blocking break view (blurred) · **Last updated:** 2026-07-19
- **One-sentence identity:** a lofi-mascot focus companion that lives in the menu bar — Structured/One Sec's consumer warmth stuffed into a single popover, personality carried by a rotating illustrated "vibe" card rather than by chrome.
- **Cluster:** unassigned (first candidate for a *cozy-consumer-utility* / *soft-playful-menubar* cluster — sole member so far)
- **Lineage:** native — likely custom-styled SwiftUI (med confidence) — genuine traffic-lit Settings window, native-style accent switches, and macOS-class 13pt density argue native; heavy custom grammar (tracked-uppercase accent headers, custom tab bar) is a *styling* choice, not proof of web/Electron. No Electron tells (no 16px web body, no kebab menus) but no cursor/DOM evidence either. Because the surface is heavily re-skinned, little here should feed macOS canon — record tells with corrections.
- **Era (chrome):** custom — a Big-Sur-rounded soft skin (opaque pastel fills, ~16px panel radius, pill controls); not Liquid-Glass (no lensing/scroll-edge on content), not legacy-native. The one translucent-material surface is the floating mini window.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/popover | ~`#F4F6FA` cool near-white (estimated)(confirmed) | | main menu-bar panel, light/default theme; soft, no visible border |
| bg/window-settings | ~`#FFFFFF` window with ~`#F0F1F4` grouped cards (estimated)(inferred) | | Options window, default theme |
| theme/cream | ~`#F4EEDD` warm cream ground + ~`#EDE6D2` cards (estimated)(inferred) | | swappable "Custom" theme; recolors whole panel |
| theme/blue | ~`#3B5BDB`→`#5C79E8` blue material (estimated)(inferred) | | floating mini window / blue theme; translucent |
| accent/primary | ~`#2E6BE6` blue (estimated)(confirmed) | | switches ON, selected tab fill, bar-chart bars, play-circle glyphs — system-blue-adjacent |
| accent/section-header | ~`#5C8DEF` lighter blue (estimated)(confirmed) | | tracked-uppercase headers — see Defects (non-native) |
| semantic/done | ~`#34C759` saturated green (estimated)(confirmed) | | "Done" button fill + check; deliberately off-accent = completion semantic |
| type/body | ~13–14px SF Pro Regular (estimated)(confirmed) | | macOS-class body, not iOS 17 |
| type/row-title | ~13–14px SF Pro Semibold (estimated)(confirmed) | | settings row titles, task title |
| type/row-subtitle | ~11–12px SF Pro, secondary grey (estimated)(confirmed) | | "Toggle visibility of the view" — very light, contrast risk |
| type/section-header | ~11px SF Pro Semibold, +tracking, UPPERCASE, accent-blue (estimated)(confirmed) | | FOCUS REVIEW / WEEKLY SESSIONS / PRO FEATURES + tab labels |
| radius/panel | ~16–18px (estimated)(confirmed) | | popover + settings window corners |
| radius/card | ~10–12px (estimated)(confirmed) | | task header card, grouped setting cards, art card |
| radius/pill | ~8–10px (estimated)(confirmed) | | Float / Done / Stop-chilling / segmented buttons |
| radius/switch | capsule (estimated)(confirmed) | | native-style accent switch |
| control/switch | ~40–44 × 24–26px, blue capsule (estimated)(confirmed) | | matches SwiftUI Toggle on macOS |
| control/segmented | LOFI\|AMBIENT + 4-tab bar, selected = light-blue fill (estimated)(confirmed) | | |
| row/settings-height | ~44–52px generous (estimated)(inferred) | | grouped rows w/ icon chip + title + subtitle + trailing switch |
| row/popover-height | ~30–32px (estimated)(inferred) | | disclosure list rows w/ trailing `>` chevron |
| icon-chip/settings | ~28px circle, blue-tinted fill, mono glyph (estimated)(inferred) | | iOS-Settings-style leading badge |
| chrome/popover-width | ~340–370px (estimated)(inferred) | | menu-bar-extra dropdown |
| chrome/traffic-lights | genuine; grey (disabled) minimize/zoom on Settings window (measured, semantic)(confirmed) | | correct macOS Settings-window behaviour |

## Layout skeletons

**Menu-bar popover (main window, shot-3/shot-5)** — single ~360px-wide rounded panel, floating below the menu bar. Top: a full-width rounded task-header *card* (grey fill) holding the task title (left) + a `count/total` pill (e.g. 24/44, right), and a second row inside it with a "Float" pill button (leading) and a green "Done" button (trailing). Below the card, a flush disclosure list — `Quick note >`, `Notify me  35m/5m >`, `Reminders  33/46 >`, `Lofi player v` — left-aligned labels, right-aligned secondary values in grey, per-row trailing chevron. When "Lofi player" is expanded: a large rounded album-art image card, then a control strip (leading cluster of 3 mono icon-buttons | trailing `LOFI|AMBIENT` segmented toggle + refresh), then optional playlist rows (blue play-circle + track title). Footer bar: `» Options` (leading) · `Quit ⏻` (trailing), both quiet grey. No-task state collapses the header to one grey full-width pill ("Stop chilling").

**Options/Settings window (shot-4)** — standard titled window ("Satu Options", genuine traffic lights). A custom 4-segment *tab bar* spans the content top: GENERAL / PRO / REVIEW / CUSTOM, each an icon over a tracked-uppercase label; selected segment gets a light-blue rounded fill. Below, tracked-uppercase accent-blue section header, then inset-grouped rounded cards of rows. *Review tab*: a 4-row stat card (Daily Goal + stepper, Today, Streak, This week) with leading mono glyph, left label, bold right value, hairline inset separators; below, a "Weekly Sessions" bar chart (grey past / blue current-week bars) with date range + prev/next chevrons. *Pro tab* (cream theme): grouped rows with 28px circular blue icon chips, title + subtitle, trailing accent switch.

**Floating mini window (shot-4 top-right)** — compact rounded (~14px) translucent blue bar mimicking a mini menu-bar: row of mono glyphs (play, AI sparkle, battery, list-toggle) + clock "Tue 7 Jul 09.55"; beneath, a lighter-blue pill row with current task + badge count + time.

**Blocking break view (shot-2)** — full-screen gradient-blue takeover, centered "Break Time – <task>" title + one-line body + a lone quiet "Quit" text button. (Heavily blurred in the marketing render — low evidence, structure only.)

## Signature moves
- **[GOLDEN-NUGGET] The lofi "vibe" art card as first-class content.** A large rounded image block inside the popover carries a rotating AI-illustrated mascot scene (studious black cat + duck, striped "FLOW" bunny, cherry-blossom car "automotive fact") with an inspirational caption. The entire warmth of the product lives in this one block; it's the reason to open the menu-bar item beyond utility. Systematic across every popover state → the app's soul.
- **Green as the one saturated action.** "Done" is the only fully-saturated control on any surface — a deliberate off-accent green reserved for task completion. Von Restorff by construction: the completion button is the single thing the eye is trained to find, and finishing a task lights it up. (Breaks strict accent-binding — see Defects — but systematic and purposeful, so it reads as signature, not slip.)
- **Whole-panel theming.** Default cool, "Custom" cream, and blue themes recolor the ground, cards, *and* the floating mini window as a set — a personalization surface unusual for a menu-bar utility.
- **Everything in one dropdown.** Task, timer, notify, Apple Reminders, quick note, music player, and weekly review stats all stack in a single ~360px popover — a maximal menu-bar-extra rather than a minimal one.

## Defects
- **Tracked-UPPERCASE accent-coloured section headers** (FOCUS REVIEW, WEEKLY SESSIONS, PRO FEATURES + the GENERAL/PRO/REVIEW/CUSTOM tab labels) → the #1 sidebar/section authenticity tell inverted: native headers are sentence-case, system-font, *secondary* colour, never tracked caps and never accent-tinted. Canon fix: `Weekly sessions` in secondary grey, no tracking.
- **Custom segmented "tab bar" for Settings navigation** → macOS Settings uses a real toolbar of tab items with normal-case labels; the icon-over-uppercase pill group is a non-native substitute ("a toolbar is not a tab bar").
- **Contrast Dilution** → task title reads grey-on-grey inside its header card; setting subtitles ("Toggle visibility of the view") are very light grey, on cream especially — likely below 4.5:1. Fix: primary label to ~85% ink, subtitles to the Secondary tier, not Tertiary.
- **Per-row `>` chevrons on popover rows** → iOS/Catalyst navigation affordance; native macOS disclosure lists lean on the disclosure triangle or plain rows.
- **Accent not fully bound** → blue (selection/switch/chart) is consistent, but section headers borrow the accent hue and the primary action is green; three colour jobs share no single system-accent binding.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| menu-bar popover (shot-3/5) | 12/14 | #9 task title grey-on-grey; #10 chevrons/icons ~<3:1 |
| Options — Review (shot-4 R) | 13/14 | #10 hairline separators very faint |
| Options — Pro, cream (shot-4 L) | 12/14 | #9 subtitle contrast on cream; #10 faint separators |

### Native-tells audit (10-point)
| Surface | Score | Fails / partials |
|---|---|---|
| menu-bar popover | 7/10 | #4 uppercase headers (n/a small here); #6 green primary off-accent; #3 no visible selection state |
| Options window | 6/10 | #4 tracked-uppercase accent headers; #6 accent-tinted headers; #9 custom tab bar not a real toolbar |
