# Design Directions — the aesthetic-direction catalogue

Nine **choosable directions** for a new macOS app, reframed from the corpus's verified style clusters (`design-corpus/TASTE.md`). Each is a committed identity you pick *before* laying pixels, then mine your subject inside. This file assumes the platform floor from `native-foundation.md` (control ladder, 13pt body, label tiers, chrome anatomy, the 10 native rules) and does **not** repeat it — a direction only records where it *departs from or specialises* that floor.

**How to use:** (1) start from the picker below by audience × subject and commit to ONE direction — catalogued, a hybrid of two, or a novel one the subject earns (a new direction must be declared with the same rigour: identity tokens, do/don'ts, differentiation from its nearest neighbours here); (2) inherit or author its identity tokens; (3) build the skeleton from the cited `patterns/` entries; (4) appropriate 2–3 signature moves, generalised to your subject, and name the design's own signature + one justified risk; (5) enforce the native floor before flourish. Every value here is corpus-measured or corpus-estimated — treat `~` ranges as ranges, not false precision.

> **Calibration, not a menu.** This catalogue records what *committed quality* looked like across 135 curated apps — it is the floor of taste, not the ceiling of invention. Two flags: **Warm Paper** and **Terminal Dark** are simultaneously corpus-proven *and* the two looks AI defaults to on any brief (cream + terracotta + serif; near-black + acid accent). Choose them only when the brief asks or the subject positively earns them (Caesura earned its paper from a musical rest; Ayron earned its acid-lime from its brand) — never as the free-axis default.

---

## Direction picker (audience × subject → candidates)

| Audience \ Subject | Glanceable status / telemetry | Writing / reading / notes | Files / media / conversion | Config / system control | Dashboard / data | Curation / browsing |
|---|---|---|---|---|---|---|
| **Pro / power** | Instrument · Terminal Dark | — | Liquid Glass · System Native | System Native · Terminal Dark | Terminal Dark · Electric Accent | — |
| **Developer** | Terminal Dark · Instrument | Warm Paper (dark) | — | System Native | Terminal Dark · Electric Accent | — |
| **Consumer** | The Notch · Instrument | Warm Paper | Liquid Glass · Warm Consumer | Warm Consumer · System Native | Warm Consumer | Quiet Gallery |
| **Creative** | The Notch | Warm Paper | Liquid Glass · Quiet Gallery | — | Electric Accent | Quiet Gallery |

Ties are deliberate: state the pick **and** the runner-up, then let the differentiation notes keep them apart. Cross-reference: *glanceable + tiny surface* almost always → Instrument or The Notch (a menu/popover/notch **is** the app); *content is the point* → Quiet Gallery; *impersonate the OS* → System Native.

---

## 1 · The Instrument — restraint as identity

**Essence:** a single `NSMenu`/popover *is* the whole app; it opens answering one question and vanishes. **Peers:** Bartender, Alfred, iStat Menus, Dato.

| | |
|---|---|
| **When to choose** | Pro/power or consumer utility whose value is a one-second glance (a metric, a countdown, a network, a quota). No document, no library — one question. |
| **Palette** | True-dark or graphite ground `#1A1A1C`–`#1E1E1E`; single accent (system blue default, or *withhold* to white); optional per-metric identity hues from the 12-hue palette (never as the accent). |
| **Type** | 13pt body; **tabular/mono hero figure at ~34–48pt** carries the surface. |
| **Density / radius / material** | Comfortable popover cadence (rows ~24 menu / ~40–52 rich); panel radius **16–20**; `NSVisualEffectView` menu material — never a hardcoded brand-colour surface. |
| **Layout** | `patterns/menu-bar-extra.md` (choose thin `NSMenu` vs rich window-popover) + `patterns/floating-panel.md` (no traffic lights, anchor to status item, up-caret). Hero readout on top, one saturated action at the XL-36 tier. |

**Appropriable signature moves** (generalise, don't copy): scale-as-hierarchy hero — promote the one datum to ~36pt so it answers pre-attentively · a mini sparkline/histogram that turns a one-shot readout into a glanceable daily dashboard · a live count/delta pill on every branch or metric · split personality — an austere dense menu-bar readout that opens into a roomier panel · zero-chrome commitment: no titlebar/toolbar the menu doesn't need.

**Do** — open answering one question; keep chrome invisible; bind the one action + selection to the system accent; seat critical secondary text at ≥55% white over glass. **Don't** — add a titlebar/toolbar; scatter a second saturated element; hardcode a brand-colour panel fill (the Open-Timer-navy tell); use iOS idioms (trailing circular checkmarks, per-row `>` chevrons, segmented-as-nav).

**Stay distinct from:** *Terminal Dark* (that direction is a full window with instrument density; The Instrument is a chromeless menu/popover) · *The Notch* (anchors to the notch/bezel, not the menu bar).

---

## 2 · Warm Paper — clinical utility recoloured as editorial calm

**Essence:** writing/reading surfaces in warm paper + one bookish accent, where hierarchy is weight + a single grey. **Peers:** Bear, iA Writer, Craft, Things.

| | |
|---|---|
| **When to choose** | Consumer/creative writing, notes, journaling, reading, or a calm break/habit utility — a subject that *earns* warmth (don't reach for it reflexively). |
| **Palette** | Warm off-white `#F8F7F5`/`#FDFAF5`/`#F3F3F0` **or** softened graphite dark (`#1E1E1E` ground, primary at ~85% white not pure `#FFF`); ONE muted accent (terracotta `#B35A3C`, lime for "done" only, steel-blue `#5E9DC0`) — deliberately *not* system blue. |
| **Type** | 13–16pt body (legibility over density); calm sentence-case or all-lowercase labels; a serif lives in *marketing*, rarely the UI. |
| **Density / radius / material** | Comfortable (rows ~44–51); card radius 10–20; opaque themed surfaces — glass is legitimately *absent* here. |
| **Layout** | `patterns/sidebar.md` (two-tone chrome, sentence-case headers) + `patterns/list-table.md` + `patterns/menu-bar-extra.md` for the utility variant. Single content column; the document is the interface. |

**Appropriable signature moves:** carry all secondary text on ONE warm-grey/taupe token so weight + that grey *is* the hierarchy · reserve the accent for a single status (done/next), never decoration · dimmed inline markdown syntax — the note shows its plain-text bones · make the subject's core noun the design system (a mark that is logo + selection glyph + status) · day/date/subject as the document title itself.

**Do** — carry hierarchy by weight + one grey; reserve the accent for one status; keep the reading surface chrome-free. **Don't** — use vivid system blue where a bookish muted hue fits; add editor chrome to a reading surface; let the calm palette dilute contrast (the recurring miss: active wayfinding text pushed to a 2.3:1 tertiary grey — keep live metadata at ~55% white / `#000`@50%).

**Stay distinct from:** *Warm Consumer* (that direction owns a *loud* brand hue quarantined to the icon and uses system blue for controls; Warm Paper owns a *muted* accent that replaces the system accent) · *Quiet Gallery* (withholds colour entirely; Warm Paper keeps one warm accent).

---

## 3 · The Notch — the bezel is the canvas

**Essence:** the MacBook notch / Dynamic-Island region is the entire surface; true-black fuses software to hardware. **Peers:** NotchNook, Boring Notch, Alcove, DynamicLake.

| | |
|---|---|
| **When to choose** | Consumer glanceable ambient status (now-playing, timers, live activities, drop-shelf) that wants to feel like a hardware feature, not a window. |
| **Palette** | **TRUE-BLACK opaque** `#000`–`#080808` (appearance-independent — the illusion needs it); monochrome + one status hue. |
| **Type** | Minimal — one glanceable count/countdown/glyph; body only in the expanded state. |
| **Density / radius / material** | Panel bottom-corner radius **28–34** (rounds into the bezel); **never translucent** here — glass breaks the merge. |
| **Layout** | `patterns/floating-panel.md` (notch sub-family: no chrome, transpose any sidebar into horizontal top-tabs) + `patterns/menu-bar-extra.md` notes. iOS Live-Activity mental model. |

**Appropriable signature moves:** commit to pure black so the app disappears into the hardware (Gestalt figure-ground closure) · one glanceable value only in the collapsed state · a concave shoulder-morph where island corners flare *outward* into the menu bar · a playful mascot/pixel theme for personality · the icon literally depicts the product (a lit bezel).

**Do** — commit to true black; one glanceable value; keep the collapsed state near-empty (reserve width for expansion). **Don't** — use a translucent/glass material (breaks the bezel illusion); port iOS control sizing wholesale into any window the app spawns; rely on the merge over a *light* desktop without testing it.

**Note:** this direction is **intentionally non-native** (custom UI in the menu-bar/notch zone, no system accent). It is a legitimate signature register but its grammar never counts as "mac taste" — keep any spawned settings/window fully native.

**Stay distinct from:** *The Instrument* (menu-bar-anchored, native chrome, system accent) · *Liquid Glass* (translucent — the exact opposite material choice).

---

## 4 · Liquid Glass — wallpaper-tinted translucent utility

**Essence:** whole-surface Liquid Glass that tints to the wallpaper; user content is the only saturation. **Peers:** iStat Menus, Yoink, Permute, CleanShot.

| | |
|---|---|
| **When to choose** | Consumer/pro file, drop-target, media, or conversion utility that wants to feel light and of-the-desktop. |
| **Palette** | Adaptive glass tinting to wallpaper (cool at top, warm at bottom); ONE saturated action bar; single-chroma discipline (only the source/status badge carries a second hue). |
| **Type** | 13–14pt body; labels defer to content. |
| **Density / radius / material** | Panel/thumb radius 12–20; `NSVisualEffectView` on the **floating layer only** — this is the cardinal rule and the direction's biggest liability. |
| **Layout** | `patterns/floating-panel.md` (glass islands, container morphing) + `patterns/toolbar.md` (float toolbar as glass islands, Scroll Edge Effect) + `patterns/card-grid.md` (masonry thumbnails, opaque with soft shadow). |

**Appropriable signature moves:** let user content be the only saturation; float 3–4 glass islands over edge-to-edge content · one candy-saturated action bar as the whole action layer · glass-pill metadata (format/size badges) riding thumbnails instead of a caption bar · group controls into one continuous glass container per cluster (container morphing) · a Quick-Look-disguise panel that reads as a native spacebar preview.

**Do** — content stays **opaque** (its own soft shadow), glass on chrome/islands only; one saturated action; verify secondary ≥4.5:1 and hairlines ≥3:1 against the *lightest* wallpaper it may float over. **Don't** — seat lists/text/cards on the glass (the glass-in-content defect); add a second accent; use a cyan-on-blue CTA label (~3.5:1) — white or ≥4.5:1 on the accent fill.

**Stay distinct from:** *Quiet Gallery* (also chromeless but withholds all colour and uses opaque/void grounds; Liquid Glass keeps one saturated action and translucent chrome) · *Warm Consumer* (opaque themed panels, brand hue; Liquid Glass is translucent, content-coloured).

---

## 5 · System Native — the OS as camouflage

**Essence:** near-exact macOS/System-Settings adoption (Jakob's Law) so the app's power feels sanctioned. **Peers:** System Settings, Ice, Hidden Bar, iStat Menus prefs.

| | |
|---|---|
| **When to choose** | Pro/consumer config-dense utility, especially one that rewrites OS behaviour (menu bar, windows, files) and needs to feel trustworthy and familiar. |
| **Palette** | Stock: window `#FFFFFF`/`#1E1E1E`, elevated cards one tonal step up (`~#26282C` dark), **system blue** bound to selection + switches + the one primary. |
| **Type** | 13pt body; **Title-Case Semibold** section headers (never tracked uppercase). |
| **Density / radius / material** | Regular-24 control ladder; grouped-form card radius 10–14; stock Liquid Glass where chrome calls for it. |
| **Layout** | `patterns/settings.md` (sidebar OR icon-over-label tab bar → grouped inset cards, label-left/control-right on shared axes) + `patterns/sidebar.md` (solid-accent selection r8) + `patterns/onboarding.md`. |

**Appropriable signature moves:** impersonate System Settings precisely, then earn distinctiveness through ONE purpose-built control mined from the job (a gradient editor, a live preview) · a hero header card per pane (icon tile + LargeTitle + one-line description) that titles each config "chapter" · reversibility written into copy ("moved to Trash") · risk-tiered filter pills with live counts · innovation lives in *content*, not chrome.

**Do** — impersonate the idiom exactly; earn distinction through one purpose-built control; grey out minimize/zoom on settings windows; disabled controls dim in place, never disappear. **Don't** — *fake* the chrome you're imitating (real traffic lights, real pop-up vs pull-down); break the idiom you borrowed for familiarity; let the one custom control drift off-accent.

**Stay distinct from:** *Warm Consumer* (that direction is spacious one-setting-per-card with a brand personality; System Native is dense many-rows-per-card stock fidelity) · *Terminal Dark* (custom instrument theme; System Native is stock).

---

## 6 · Terminal Dark — nocturnal instrument density

**Essence:** near-black developer/pro tools with instrument-panel density and a monospace metadata voice. **Peers:** Linear, Warp, iStat Menus, Screen Studio.

| | |
|---|---|
| **When to choose** | Developer/pro tool, dense dashboard, or telemetry board where figure-ground is tight and data is the point. |
| **Palette** | Near-black grounds `#0B0A0E`–`#1E1E1E` (keep figure-ground within a few %); inverted-depth tonal stacks (chrome > canvas > cards); per-datum colour from the 12-hue palette; **two-hue discipline** (brand owns marketing, system blue owns actions). |
| **Type** | 13pt body SF Pro; **monospace for instrument data only** (metadata, numerals, gauges); tracked-caps mono section labels are a *deliberate* instrument signature here (elsewhere a tell). |
| **Density / radius / material** | Compact — single-line ~28pt table rows; card radius 10–14, concentric; custom instrument theme, opaque content. |
| **Layout** | `patterns/list-table.md` (compact table density, ≥3:1 dividers) + `patterns/card-grid.md` (stat tiles: tinted glyph + big value + label) + `patterns/toolbar.md`. |

**Appropriable signature moves:** make the metaphor literal — a pixel/LCD display face + dial gauges if the subject is a "meter" · a dual-window card (a ring + a bar, each status-coloured to its own threshold) so the one at-risk item pops from a field of green · monospace metadata as a consistent instrument voice · per-event/per-metric colour on the system palette · a green/amber/red status ramp always paired with a value.

**Do** — keep figure-ground within a few %; reserve mono for instrument data; lift unfilled gauge tracks and dividers toward ≥3:1. **Don't** — let a fixed brand accent override every focus state (the over-bound-violet tell — bind selection to the system accent even in a themed surface); split status semantics so the same 42% reads green on one surface and orange on another; run tracked-caps at *heading* size (keep it tiny-eyebrow + tertiary).

**Stay distinct from:** *Electric Accent* (one hardcoded electric hue as the whole identity on a neutral ground; Terminal Dark is a multi-hue instrument system) · *The Instrument* (chromeless menu/popover; Terminal Dark is a full window).

---

## 7 · Quiet Gallery — content is the interface

**Essence:** chromeless browsers where furniture dissolves and the user's content is the entire surface. **Peers:** Eagle, Cosmos, Apple Photos, Paste.

| | |
|---|---|
| **When to choose** | Creative curation, moodboard, clipboard/asset library, wallpaper/media browser — anywhere the content must be the only figure. |
| **Palette** | **Zero-accent** — selection/emphasis in neutral white/graphite, not system blue; true-black `#000` or `#111` void grounds that turn thumbnails into lit objects; content is the only chroma. |
| **Type** | Personable centred window title ("HELLO, ATLAS" / "869 ITEMS"); minimal chrome typography. |
| **Density / radius / material** | Edge-to-edge content; thumbnail radius 6–8 opaque + soft shadow; chrome dissolved to floating glass islands. |
| **Layout** | `patterns/card-grid.md` (masonry/freeform canvas for heterogeneous content) + `patterns/toolbar.md` (four floating islands, segmented view-switcher) + `patterns/floating-panel.md`. |

**Appropriable signature moves:** dissolve all furniture into 3–4 floating glass islands over edge-to-edge imagery · withhold the system accent so every item is figure against silent chrome (Von Restorff by subtraction) · a neutral white/graphite selection reticle instead of accent · content-type-aware cards (a copied colour renders as a colour swatch, a URL as a screenshot) · a personable centred title that makes the schema warm.

**Do** — withhold the accent; keep every content item opaque with its own shadow (glass on islands only); a true-black/void ground to light the thumbnails. **Don't** — introduce app-owned colour that competes with content; let the near-white/void shell dilute the title/glyph contrast below the floors (push the count subtitle to `#000`@50%).

**Stay distinct from:** *Liquid Glass* (keeps one saturated action + wallpaper-tinted content ground; Quiet Gallery is zero-accent on a void) · *The Notch* (a hardware-fused overlay, not a content window).

---

## 8 · Warm Consumer — friendly brand warmth over correct bones

**Essence:** approachable Setapp-register tools with one loud brand hue quarantined to the icon and correct native bones underneath. **Peers:** One Sec, CleanShot X, Things, Klack.

| | |
|---|---|
| **When to choose** | Consumer utility that wants personality and reassurance (focus/wellbeing, keyboard sounds, small automations) without abandoning native correctness. |
| **Palette** | ONE loud brand hue (orange `#FF8C16`, teal) **quarantined to the icon + wordmark**; **system blue `#0A84FF` for actual controls**; optional whole-panel theming sets (default/cream/blue). |
| **Type** | 13pt body; rule-as-sentence subtitles ("Extension is .dmg · Move to Trash"); emotional de-escalation copy. |
| **Density / radius / material** | Comfortable, often spacious one-setting-per-card; radius 10–18; opaque themed panels or dark glass. |
| **Layout** | `patterns/settings.md` (spacious one-setting-per-card variant) + `patterns/menu-bar-extra.md` + `patterns/list-table.md` (status-toggle rows). |

**Appropriable signature moves:** quarantine the brand hue to the icon and bind every control to system blue (the textbook discipline) · status-toggle-as-traffic-light — a per-row green(on)/red(off) pill that doubles as the enable indicator · rule-as-sentence metadata that reads as plain English · signal the primary action by *luminance* on a tinted glass panel rather than a second accent · "Soon" status pills as a roadmap-in-the-menu (disabled-don't-remove). Two-material mood split — an immersive dark catalog to *choose*, a light panel to *use*.

**Do** — quarantine the brand hue, bind interaction to system blue; spend the warmth budget on copy and completion states, not everywhere. **Don't** — override every control with the brand colour (the orange-on-all-controls tell); use a coloured menu-bar glyph where a template symbol belongs; let one-setting-per-card spacing become iOS density (keep the Regular-24 ladder).

**Stay distinct from:** *Warm Paper* (owns a *muted* accent that replaces system blue; Warm Consumer keeps system blue and quarantines a *loud* hue) · *System Native* (dense stock fidelity; Warm Consumer is spacious and branded).

---

## 9 · Electric Accent — one hardcoded electric hue carries a neutral surface

**Essence:** a single deliberately-non-system accent (with genuine bloom) carrying an otherwise-monochrome utility. **Peers:** DaisyDisk, Permute, Linear, Raycast, Vercel.

| | |
|---|---|
| **When to choose** | Pro/creative dashboard or single-metric tool that wants one dramatic, ownable colour moment. *(Smallest, coherence-flagged cluster — provisional.)* |
| **Palette** | ONE hardcoded electric accent — the load-bearing token (indigo `#6155F5`, royal `#1B5BFF`) — deliberately not system blue; **ground luminance varies** (dark `#171717` *or* light `#FFFFFF` — do not assume dark); everything else a monochrome ramp. |
| **Type** | 13pt body; neo-grotesque restraint; a giant display numeral for the hero datum. |
| **Density / radius / material** | Dense-calm; card radius ~20 (popover-class); opaque content; neon with genuine outer glow/bloom. |
| **Layout** | `patterns/card-grid.md` + `patterns/list-table.md` + `patterns/floating-panel.md`. Fitts-optimal pie/radial layouts where a launcher (every item the same short distance from the invoke point). |

**Appropriable signature moves:** let one electric accent + a neon-bloom chart be the entire character on a neutral ground · one-accent discipline (the chart + a single green delta pill, nothing else saturated) · data-ink-minimal drama (no axes/gridlines) traded for a glanceable hero · a Fitts-optimal radial/pie menu.

**Do** — let a single electric accent carry the surface on a neutral ground (dark *or* light); keep everything else monochrome. **Don't** — ship the default AppKit table with only a blue swap (the "competent-but-almost-anonymous" trap — the distinctiveness must be in the execution, not the swap); assume this direction implies a dark ground (only one member evidences it); leave selection neutral-grey while the accent lives only on the chart — bind selection/focus to the accent too.

**Stay distinct from:** *Terminal Dark* (a multi-hue instrument system; Electric Accent is strictly one accent + monochrome) · this is the current *model-default dev-tool look* — its distinctiveness rests entirely on execution, so push the one accent moment hard or pick another direction.

---

## Commitment rules

1. **One direction, fully.** Pick a single direction per app and inherit its whole token set. Mixing two (warm-paper accent + electric neon chart + gallery void) reads as indecision, not richness. State the pick and the runner-up; do not blend them.
2. **Subject-mine *within* the direction.** Distinctiveness comes from mining the app's own subject through the chosen lens — the noun becomes the mark, the metaphor becomes the gauge, the job becomes the one purpose-built control. The direction is the grammar; the subject is the vocabulary. (Warm Paper is only *earned* when the subject wants calm — a break reminder, a journal — not applied reflexively.)
3. **Anti-sameness across a session.** When generating several apps in one session, vary the direction deliberately — do not let every mock converge on Terminal Dark or Electric Accent (the two model-default looks). If two briefs genuinely land on the same direction, differentiate on subject-mined signature moves and palette, and say how.
4. **Lookalike check.** If the result would pass as a specific digested app's screen (caesura, atlas, klack, hejour, bartender-6, revone), differentiate deliberately — appropriate the *move*, never the trade dress.
5. **Native floor is non-negotiable.** Enforce `native-foundation.md` before any flourish: 85/50/25 label tiers, one accent bound to interaction, card 10–14 / panel 16–20, 13pt body, real traffic lights, inset-rounded selection. The #1 defect to pre-empt is Contrast Dilution — secondary ≥4.5:1, dividers ≥3:1. A direction's *signature* may deviate (brand accent, tracked-caps eyebrow, true-black); a *defect* never gets that license.

---

## Non-native contrast shelf (when the user explicitly wants Electron density)

If — and only if — the user explicitly asks for a dense, information-maximal, Electron/web-style surface (a Notion/Linear/Superhuman register the native directions don't cover), treat it as a **contrast shelf**, not a tenth direction. It never seeds native canon.

- **What it looks like:** higher information density than the Regular-24 ladder allows, web-scale type (14–16px body), custom component systems, tracked-uppercase labels, kebab menus — the deliberate opposite of the native floor.
- **The lesson from the corpus's best Electron work** (1Password, Superlist, Notion Calendar, Craft): great non-native work *reproduces native selection grammar and de-emphasis by hand* — faithful macOS selection-duality, periwinkle field-labels, real hierarchy. Study the *result*; attribute nothing to native canon.
- **Say so explicitly.** When you deliver on the shelf, name it: "this is a deliberate non-native / web-density register, not macOS-native." Never let a shelf choice silently degrade a native-direction brief.
