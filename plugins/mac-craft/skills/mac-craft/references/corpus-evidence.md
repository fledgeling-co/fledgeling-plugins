# Corpus Evidence — what 135 shipping macOS apps actually do

The measured evidence layer. `design-directions.md` is the *buildable* catalogue — recipes,
identity tokens, signature moves, pattern routing. **This file is the evidence behind it**:
the canon with its member counts and its honest under-claims, the tells table, the readings
where native apps genuinely disagree, and the gaps in the sample.

**Why both files exist, stated so neither reads as filler.** The predecessor shipped these
as two renderings of the same nine clusters — 423 lines describing the same directions
twice, with neither file saying what the other prevented. Reading only the recipes gives a
runner a style with no idea how thin its evidence is (one cluster rests on three members,
one of them logged "competent but almost anonymous"). Reading only the evidence gives them
member counts and no way to build anything. So: **`design-directions.md` to choose and
build; this file to know how much weight the choice can bear.** The nine cluster sections
that were duplicated here are gone — the pointer table below is what replaced them.

> **Corpus level: Proficient.** 209 surfaces / 134 apps. Frozen **2026-07-19**; unchanged
> since, and it describes what apps *shipped*, never what the platform *specifies*. Where
> this file and `native-foundation.md` disagree, the platform wins — a corpus statistic is
> evidence about the field's habits, including its bad ones.

## Cluster → where to build from

| Cluster (evidence name) | Direction (buildable name) | Members | Weight it bears |
|---|---|---|---|
| Menu-bar Instrument | **1 · The Instrument** | 11 | Strong |
| Warm-Editorial / Paper | **2 · Warm Paper** | 9 | Strong, and an AI-default flag |
| Notch Native | **3 · The Notch** | 7 | Strong; deliberately non-native grammar |
| Liquid-Glass Translucent Utility | **4 · Liquid Glass** | 6 | Strong |
| System-Idiom Utility | **5 · System Native** | 5 | Adequate |
| Terminal-Dark Instrument | **6 · Terminal Dark** | 5 | Adequate, and an AI-default flag |
| Content-Forward Gallery | **7 · Quiet Gallery** | 4 | Thin |
| Warm Consumer Utility | **8 · Warm Consumer** | 4 | Thin |
| Electric Accent *(was "-Dark")* | **9 · Electric Accent** | 3 | **Provisional** — one member is light-mode, one geometry-only, one logged weak. Do not cite it for a dark-ground recipe; only `revone` evidences that. |

The rename in the last row is the reason this skill has a stable-option-identity rule: the
cluster was named on a dark ground that one of its three members has, the name was changed,
and every reference to it broke. An option keeps its name once it has one.

> The level claim rests on the **native subset**: 66 native-lineage apps (49%), all with ≥1 scorable UI surface. Stable canon + clusters with identities exist; full Expert is withheld because only **16 of 66** native apps carry ≥2 surfaces (most are single hero/marketing renders), and settings/onboarding/light-mode-pro evidence is thin (see Gaps).

**Evidence honesty.** 109 apps have ≥1 scorable UI surface; **25 are marketing/brand-only** (tokens = brand/icon evidence, never UI canon). **46 apps (34%) are unknown-lineage** — real UI but unverifiable framework, so excluded from canon. Only `native` evidence feeds the canon below; `web-electron` (19) / `catalyst` (2) / `ios-on-mac` (1) feed Tells & the Non-native shelf. Native-audit (10-pt) median **7.0**, mean 6.16; rubric (14-pt) median **12.0** — the corpus skews competent, with a long tail of Contrast Dilution.

---

## Canon — universal
*(promoted only from ≥3 independent native apps, no contradiction. Every row cites members.)*

> **Independence caveat (auditability).** The observation JSONs carry no developer/vendor field, so "independent (same developer counts once)" rests on **distinct app identities**, not confirmed-distinct developers — it is not auditable from the digestion artifacts. No same-developer duplicate is evident by name among cited members (e.g. only one `-4-breakfast` app is cited), so no violation is known; the guarantee is weaker than the rule's wording implies.

| Rule | Values | Native members (count) | Since |
|---|---|---|---|
| **De-emphasis hierarchy survives grayscale** — 2–3 ink tiers do the work; colour is the last 10%. | primary ~**85%** ink · secondary ~**50–55%** · tertiary ~**25%** (matches kit Labels) | sketch, spacepeek, shake-it-on, hejour, bartender-6, purge, klack, grape, resurf, code-meter, raycast, caesura, fantastical, letterboxx, forma, claude-notch (16) | 2026-07 |
| **Single-accent economy** — exactly one saturated moment per view (one CTA / one selection / one datum); everything else neutral. | 1 accent budget per surface | compresto, open-timer, caesura, autoshelf, liqoria, mac-4-breakfast, satu, revone, room-service, tono, noticky, hejour, orbs, walltune, sketch (15) | 2026-07 |
| **Accent bound to interactive state** — the one accent lives on selection / focus / primary action, not scattered decoration; brand hue quarantined to icon+marketing. | selection+focus+primary share one hex | zipic, spacepeek, satu, letterboxx, glance, cachesweep, macusb, bartender-6, vocal-notes, compresto, keeby, screenlex, hora-calendar, resurf (14) | 2026-07 |
| **Card / container radius 10–14pt** | ~10–14pt (concentric: inner ≈ outer − 4) | spacepeek(12–14), viaduct(12), bartender-6(10–12), satu(10–12), resurf(12), forma(10–12), usage(10–12), room-service(10–12), code-meter(12–14), letterboxx(13) — 10 in-band; **macusb(14–16) sits mostly ABOVE the band, does not evidence the headline range** (11 cited) | 2026-07 |
| **Floating panel / popover radius 16–20pt** | ~16–20pt (aligns kit popover **20**) | cachesweep(16), open-timer(20), folder-hub(16–20), satu(16–18), purge(18–20), droppy(16–20), mac-4-breakfast(16–20), dropzone(16–20), tono(20–24) — 9 carry the band; **klack(14–18) and usage(12–16) fall BELOW the 16 lower bound**, do not evidence the headline range (11 cited) | 2026-07 |
| **Body type = 13pt SF Pro** (matches kit Body) | 13pt SF Pro Regular, lh ~16 | noticky, codeshot, sketch, finbar, shake-it-on, satu, mac-4-breakfast, resurf, hora-calendar, grape, fantastical, room-service, foldervitrine, code-meter, hejour (15) | 2026-07 |
| **Genuine native window chrome** — real traffic-light cluster (~68×14), colours on focus, mutes when inactive. *(Conclusion sound; "never faked dots" is the pattern, not proven-clean on every member — see note.)* | 68×14 cluster, ~12pt dots | clean screenshots: atlas, inkline, vocal-notes, glyph, canary-mail, autoshelf. **Traffic lights observed inside MARKETING COMPOSITES** (render, not clean capture): compresto, corner-time, room-service, hejour, macusb, satu (12) | 2026-07 |
| **Selection = inset rounded-rect fill** — the *geometry* (inset-rounded row/sidebar selection, kit sidebar/menu spec) is canon; the **neutral-flat grammar + radius-8 value** is only *(recurring)* — 2 clean apps. | geometry: inset-rounded ✓ · radius **8** = vocal-notes/grape only (caesura ~10, autoshelf ~10–12) | vocal-notes, grape *(clean neutral inset, r≈8)*; autoshelf, caesura *(inset-rounded geometry but **solid brand-hue fill** overriding the system accent — flagged native#3/#6 in their own obs)*; canary-mail *(**sidebar** conforms neutral #2C3235; message-list = saturated indigo card #2558C9, native#3)* (5) | 2026-07 |

Near-canon, **not** promoted (honest under-claim): **8/4pt spacing rhythm.** Native-audit spacing checks pass broadly, but explicit spacing tokens exist for only 5 native apps under 5 different names (noticky 16/8, deskminder 8, usage 15–16, tono 10–12, raycast). Treat base-8 as the *(assumed)* default per HIG/knowledge-base, not a corpus-measured canon.

**Corrections this pass (2026-07-19 audit).**
- **Rule 8 (selection fill):** `cachesweep` **removed** — its own observation logs a *trailing circular checkbox ~18–20pt* and failure `native#3 selection is trailing circular checkmark, not macOS inset-rounded accent fill`. It is a **counter-example**, not evidence (cited count 6→5). Of the survivors, only vocal-notes + grape cleanly evidence the *neutral flat, radius-8* grammar; autoshelf/caesura/canary-mail show the inset-rounded geometry but with brand-saturated fills that override the system accent — so the radius-8/neutral-flat specificity is now *(recurring)*, geometry stays canon.
- **Rule 4 / Rule 5:** two members each sit outside the headline band (see rows) — annotated in place, rules survive on their in-range members.


---

## Canon — macOS conventions
Ground truth: `kit/macos-27.md` `(specified)`. Corpus confirms/contests these:

- **Control ladder** Mn16 / Sm20 / **Rg24** / Lg28 / **XL36 (toolbars)**; push-button padding 16px. Native apps honour Rg-24 defaults; the frequent tell is *iOS density* (45pt buttons, 26pt checkboxes, ~40pt titles) in catalyst/ios-on-mac and 2 native apps — always logged as non-native.
- **Type** SF Pro, **13pt Body / 16 lh**; light primary **#000 @85%** (not pure black — kit avoids Contrast Dilution). 15/17/22/26pt title ramp. Reading-cluster apps deviate body **up** to 15–16pt on purpose (glance, viaduct item names) — density traded for legibility.
- **Chrome** titlebar 33pt; unified toolbar 52 (compact 40 / expanded 77); sidebar 256pt, rows 24/32/40, selection radius 8; menu rows 24, selection radius 8; popover radius 20; menu-bar-item selection 13 (capsule). Traffic-lights 68×14 at (9, 9.5).
- **Selection fill radius 8** confirmed by native selection grammar (above). **Separators** ~29% black — apps that drop below (8–15% hairlines) fail the 3:1 UI-contrast floor (the corpus's #1 defect).
- **Era (Liquid Glass)** capsule bezels; over-glass vibrant tiers; Scroll Edge Effect under floating toolbars; Active/Inactive states. Corpus glass exemplars: cachesweep, compresto, foldervitrine, liqoria, atlas, maestri. Watch **Glass-in-content** (3 apps) — glass belongs on chrome/floating layers, content stays opaque.


---

## Signature move bank
*(the raw material of distinctiveness — slug → move)*

| Slug | Move |
|---|---|
| caesura | The name *is* the system: a `//` caesura mark = logo + selection + status; one terracotta #B35A3C everywhere |
| autoshelf | Status-toggle-as-traffic-light: per-row green(on)/red(off) pill doubles as enable indicator |
| autoshelf | Rule-as-sentence subtitle: metadata reads as plain English ("Extension is .dmg · Move to Trash") |
| atlas | Chromeless shell — UI dissolved into 4 floating Liquid Glass islands over edge-to-edge imagery |
| atlas | Personable centred window title ("HELLO, ATLAS" / "869 ITEMS") — Photos schema made warm |
| cachesweep | Scale-as-hierarchy hero: ~36pt "120.3 MB" reclaimable figure answers the one question pre-attentively |
| spacepeek | Quick Look disguise — presents as a native spacebar-invoked Finder panel; ⚡ throughput proof pill |
| fantastical | Brand-red as typographic jewelry (the YEAR, TODAY cap, now-line) never as a fill |
| fantastical | Agenda/DayTicker pane *replaces* the list-of-calendars source list |
| finbar | Quantified menu tree: live count pill on every branch ("File 38", "Edit 16") |
| finbar | App-icon-as-search-context: target app's icon in the field's leading slot instead of a magnifier |
| klack | Two-material mood split: dark immersive catalog to choose vs light control panel to use |
| klack | Audition-before-commit rows: every row pairs a leading "+" with a trailing "▶" preview |
| open-timer | Session sparkline — a 7-bar histogram turns a one-shot timer into a glanceable daily dashboard |
| mux | Entire product surface is a single native NSMenu — zero custom chrome; restraint as character |
| orbs | Wheel-as-spatial-memory launcher: fixed wedges + hold-flick-release; number badges as expert path |
| radial | Fitts-optimal pie menu — every item the same short distance from the invoke point |
| hejour | Day-as-document title: the date *is* the page title; monochrome-plus-one-lime for "done" only |
| hejour | Dimmed inline markdown syntax — `##` persists in tertiary grey while the heading renders bold |
| noticky | Monochrome ink controls on coloured paper — checkboxes drawn as black ink, colour = filing identity |
| glyph | Heading-level gutter badges (grey "H1"/"H3" tags in the left margin) |
| forma | Monospace-everything on graph paper — full drafting-table commitment; hand-drawn bezier connectors |
| letterboxx | Data-viz as the sole boldness budget over disciplined system-default chrome; unread = weight + dot |
| keeby | Brand hue quarantined to the icon; selection/focus/primary all bind to system blue #0A84FF |
| lookaway | Signals the primary action by **luminance**, not accent hue, on a wallpaper-tinted warm glass panel |
| mac-4-breakfast | Telemetry-as-identity: raw 14.5 W / 8575 mAh / 32.6 °C promoted to primary hero type |
| code-meter | The meter *is* the metaphor: pixel/bitmap display face + dial gauges; dual-window ring+bar per row |
| compresto | Wallpaper-tinted whole-window glass; one candy-blue Compress bar with a cyan (not white) label |
| dropzone | Drag-target tile-grid *is* the product (Launchpad/Stacks metaphor as file destinations) |
| vocal-notes | Correct two-level selection: solid accent-blue knockout-white in focused list WHILE sidebar stays inset-gray |
| usage | Fixed per-metric identity palette (indigo=disk, blue=cpu) instead of the system accent; split menu-bar/window personality |
| sketch | Floating capsule toolbar — grouped opaque-white pill clusters (≤4 by function) over the canvas |
| bartender-6 | Hero header card per settings pane (icon tile + LargeTitle + one-line description) titles each config chapter |
| supaste | Content-type-aware clip cards on a true-black gallery backdrop; counted collections as capsule tabs |
| purge | Risk-tiered taxonomy (Safe/Check-First/All) + "710 photos or 355 songs" tangible-equivalent chips |
| maestri | Infinite canvas of *live* PTY/agent sessions as first-class nodes; colour-coded pipeline swimlanes |
| dynamiclake | Concave shoulder morph — island top corners flare OUTWARD into the menu bar (inverse radius) |


---

## Tells & corrections
*(most frequent non-native tells → the native fix. Contrast Dilution alone appears in **72 apps** — the corpus's dominant defect, across all lineages.)*

| Tell | Native correction |
|---|---|
| **Contrast Dilution** — secondary text <4.5:1, dividers/borders 8–15% (<3:1) | 85/50/25 label tiers; separators to ~29%; dividers from Fills tiers to ≥3:1 |
| **Faked / custom traffic lights** — grey dot rings on a card that isn't a window | Real NSWindow cluster (68×14) that colours on focus, mutes when inactive |
| **iOS density** — 40pt titles, 66pt action cards, 45pt buttons, 26pt checkboxes | Rg-24 control ladder, 13pt body, 16px push-button padding |
| **Gradient-as-accent** — pink→violet→blue decorative fill standing in for the accent | Single flat `controlAccentColor`; brand gradient only in icon/marketing |
| **Accent not system-bound** — hardcoded brand green/red on every control | Bind selection/focus/primary to system accent; quarantine brand hue to the icon |
| **Tracked-uppercase section headers** at heading size | SF Pro Semibold sentence/title case (tracked tiny-caps *eyebrow* only — see Contested) |
| **In-window hamburger** instead of the menu bar | Real menu-bar commands; window chrome stays native |
| **Selection-grammar drift** — blue-translucent fill + blue label | Flat gray inset (unfocused) OR solid-accent knockout-white (focused), radius 8 |
| **Glass-in-content** — Liquid Glass material behind body text | Glass on chrome/floating layers only; content surfaces opaque |
| **Non-native modality** — centred floating modal | Top-anchored native sheet |

---

## Contested
*(native apps genuinely disagree — both readings recorded; splits track cluster lines.)*

| Question | Reading A | Reading B | Verdict |
|---|---|---|---|
| **Section-header grammar** | Tracked-UPPERCASE eyebrow (10–11px, tertiary): caesura, satu, autoshelf, room-service, mole, cachesweep, fantastical | Sentence/Title-case Semibold 13pt: sketch, klack, foldervitrine, dropzone, letterboxx, finbar, bartender-6, grape, mux | Both native. Tracked-caps is native **only** at tiny eyebrow size + tertiary colour; at heading size it becomes a web tell. |
| **Accent source** | System blue is the accent (majority default): zipic, spacepeek, satu, cachesweep, macusb, vocal-notes, keeby, fantastical | One owned hue OR accent-withheld: caesura(terracotta), revone(indigo), room-service(orange), picmal(royal), atlas/grape/orbs/walltune/prostir/tono (neutral white) | Tracks cluster lines: **Content-Forward Gallery** withholds accent; **Warm** clusters own one hue; utilities default to system blue. All keep the *single-accent* canon — only the source differs. |
| **Section elevation** | Borders-as-elevation, no shadow (room-service, canary tonal steps) | Tonal fill-step elevation (grape, inkline inverted stack) | Both valid; shadow-free is the majority. |

---

## Knowledge gaps
- **Settings surfaces: only 8 in the whole corpus.** Empty-state 18, **onboarding just 2**, table 5. The corpus can specify a hero window far better than a preferences pane, an empty state, or a first-run flow. Bring settings + onboarding surfaces for the dense-pro clusters.
- **Single-surface bias:** only 16 of 66 native apps have ≥2 scorable surfaces — most tokens are `(inferred)` from one hero/marketing render, which over-indexes on hero styling. Multi-surface digests would promote many `(inferred)` → `(confirmed)`.
- **Marketing-composite contamination:** 101 of 209 surfaces are marketing composites; 25 apps are brand-only. Their tokens are brand/icon evidence, not UI canon — flagged per-app.
- **Mode imbalance:** dark 123 vs light 84 — the corpus is **dark-heavy**. Light-mode dense-pro evidence (the hardest to get right) is the thinnest slice.
- **Unknown lineage 34% (46 apps):** real UI, unverifiable framework — held out of canon entirely. Framework-tell captures would recover some.
- **Window corner radius still `(unknown)`** from the kit (layer-style masked); few clean screenshot measurements exist.
- **Out of scope:** motion, hover, transitions, responsiveness — static evidence only.

