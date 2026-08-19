# UI Observation Aggregate — Mac Design Archivist synthesis

Aggregated from **134 apps** / **209 surfaces** (`observations/*-ui.json`). Machine-readable twin: `_aggregate-ui.json`.

Canon gate: a rule is canon only with >=3 independent **native-lineage** apps and no contradiction. Native lineage here = `native` (+ `swiftui-native` if present). `web-electron` / `catalyst` / `ios-on-mac` feed the tells-and-corrections record, never macOS canon.

## Lineage distribution

| lineage | apps | share | confidence (high/med/low) |
|---|---|---|---|
| native | 66 | 49% | 18/38/10 |
| unknown | 46 | 34% | 0/0/46 |
| web-electron | 19 | 14% | 9/0/10 |
| catalyst | 2 | 1% | 0/2/0 |
| ios-on-mac | 1 | 1% | 0/1/0 |

**Native-lineage apps: 66 of 134 (49%)** — the canon-eligible pool.

## Era distribution

| era | apps |
|---|---|
| unknown | 43 |
| custom | 43 |
| big-sur | 24 |
| liquid-glass | 24 |

## Rubric & native-audit score distributions

- **Rubric (14-pt), scorable surfaces only (n=158)**: min 4, median 12.0, mean 11.26, max 13.
- **Native-audit (10-pt), n=142**: min 1, median 7.0, mean 6.16, max 10.

Rubric histogram (score: count): 4:2, 5:1, 6:2, 7:4, 8:3, 9:7, 10:10, 11:32, 12:74, 13:23

Native-audit histogram (score: count): 1:10, 2:8, 3:11, 4:7, 5:10, 6:12, 7:33, 8:29, 9:17, 10:5

Rubric mean by lineage (scorable surfaces): catalyst 12.14 (n=7), ios-on-mac 12 (n=1), native 11.73 (n=102), unknown 9.63 (n=27), web-electron 10.76 (n=21)

## Evidence class — real UI vs marketing/brand-only

- **Real-UI evidence (>=1 scorable surface): 109 apps.**
- **Marketing/brand-only (no scorable UI surface): 25 apps** — brand-evidence-only, treat tokens as brand/icon evidence, never UI canon:
  agentpeek, backdrop, cleanmymac, cleanshot-x, codex, coreviz-studio, cursor, dia, framer, glaze, hipixel, leafy-vocabulary-builder-for-mac, macwall, minarah, obsidian, orchard, pieoneer, pokey, slapmac, sweeper, toplify, unfumble, uninstally, voiceos, waterlemon

## Mode & surface-type coverage

Mode (per surface): dark 123, light 84, custom 2

Surface types: marketing-composite 101, other/main-window 56, menu-bar / notch popover 23, app-icon 13, settings 8, main-window (sidebar/split) 8

## Pattern frequency (apps evidencing)

| pattern | apps |
|---|---|
| other | 80 |
| toolbar | 50 |
| list | 44 |
| floating-panel | 40 |
| card-grid | 38 |
| menu-bar-extra | 29 |
| sidebar | 26 |
| empty-state | 18 |
| inspector | 18 |
| settings | 8 |
| table | 5 |
| menu | 4 |
| onboarding | 2 |

## Token frequency (top 30 by app coverage)

| token | apps |
|---|---|
| `text/secondary` | 28 |
| `text/primary` | 27 |
| `type/body` | 27 |
| `radius/card` | 24 |
| `accent/primary` | 22 |
| `type/section-header` | 21 |
| `chrome/traffic-lights` | 19 |
| `brand/backdrop` | 16 |
| `type/title` | 16 |
| `bg/sidebar` | 15 |
| `bg/window` | 15 |
| `radius/panel` | 15 |
| `bg/canvas` | 13 |
| `brand/wordmark` | 12 |
| `accent/brand` | 11 |
| `radius/window` | 11 |
| `icon/glyph` | 10 |
| `type/display` | 10 |
| `bg/panel` | 9 |
| `brand/headline` | 9 |
| `chrome/toolbar` | 9 |
| `radius/pill` | 9 |
| `bg/card` | 8 |
| `bg/content` | 7 |
| `brand/bg` | 7 |
| `brand/ink` | 7 |
| `text/tertiary` | 7 |
| `type/secondary` | 7 |
| `accent/system` | 6 |
| `bg/backdrop` | 6 |

Full per-token value lists (every member) live in `_aggregate-ui.json` -> `token_frequency`.

## Defect frequency (anti-pattern -> apps)

| anti-pattern (name) | apps |
|---|---|
| Contrast Dilution | 72 |
| Focal Collision | 7 |
| Target Starvation | 7 |
| Evidence gap | 4 |
| Line Length Fatigue | 4 |
| Low UI contrast | 4 |
| No app UI supplied | 4 |
| Selection grammar deviation | 4 |
| Accent not system-bound | 3 |
| Contrast Dilution risk | 3 |
| Corpus-input gap | 3 |
| Evidence poverty | 3 |
| Glass-in-content | 3 |
| Non-system accent binding | 3 |
| Accent not bound to system | 2 |
| Faked chrome | 2 |
| No UI defects scorable | 2 |
| No app-UI defects recordable | 2 |
| No system-accent binding | 2 |
| No true design defect observable | 2 |
| Non-native density | 2 |
| Non-native section headers | 2 |
| Non-native selection grammar | 2 |
| Selection-grammar deviation | 2 |
| Template-default aesthetic | 2 |
| Tracked-uppercase section headers | 2 |
| UI Contrast | 2 |
| UI-contrast | 2 |
| 16px legibility failure | 1 |
| Accent binding absent | 1 |

## Aesthetic cluster-hint groups (normalised)

Raw `cluster_hint` strings are near-unique free text; grouped by keyword theme. `native` = members with native lineage (the canon-eligible subset of each cluster).

| normalised cluster | members | native | top adjectives |
|---|---|---|---|
| brand / non-native / marketing-register (do-not-seed-canon) | 44 | 1 | editorial, glossy, nocturnal, friendly, monochrome |
| unclustered / other | 17 | 11 | approachable, restrained, cinematic, rounded, brand-tinted |
| menu-bar utility | 12 | 11 | utilitarian, quiet, graphite, restrained, glanceable |
| warm-editorial / writing & reading | 11 | 9 | calm, warm, tactile, editorial, restrained |
| warm consumer utility | 10 | 4 | warm, confident, friendly, utilitarian, playful |
| notch / dynamic-island utility | 8 | 7 | glanceable, monochrome, playful-mascot, minimal, true-black |
| developer / terminal-dark tool | 8 | 5 | electric, nocturnal, instrument-like, instrument-panel, retro-terminal |
| gallery / content-forward | 7 | 4 | content-forward, cinematic, immersive, airy, chromeless |
| native-system-idiom utility | 7 | 5 | utilitarian, reassuring, orderly, self-effacing, orienting |
| glass / translucent utility | 6 | 6 | translucent, airy, confident, telemetric, glassy-blue |
| electric / accent-dark utility | 4 | 3 | dark, jewel-saturated, punchy, utilitarian, crisp |

### brand / non-native / marketing-register (do-not-seed-canon)  (44 members, 1 native)

- **Members:** ajar, backdrop, cleanmymac, cleanshot-x, codex, cooldock, coreviz-studio, craft, creavit-studio, cursor, dia, framer, glaze, heatscope-ai-ux-attention-heatmaps, hilium, hipixel, leafy-vocabulary-builder-for-mac, macrest, macwall, mailtwin, minarah, mjsfx, notion-calendar, nox, obsidian, onlook, orchard, pieoneer, pixelcasso, pokey, runey, screen-charm, sero, slapmac, slashit-app, super-shortcuts, superlist, sweeper, textsniper, toplify, uninstally, voiceos, zonedial, zush
- **Native (canon-eligible):** textsniper
- **Adjectives:** editorial(6), glossy(5), nocturnal(4), friendly(4), monochrome(4), warm(4), buoyant(3), playful(3)
- **Peer references:** Linear(3), Linear marketing(2), Raycast(2), apple.com product pages(1), Raycast / Vercel marketing minimalism(1), Apple mac product pages(1), Cindori house style (Sensei/Aquatic)(1), CleanShot X / Raycast marketing(1)

### unclustered / other  (17 members, 11 native)

- **Members:** 1password, bauhaus-clock, canary-mail, presentify, resurf, room-service, screen-studio, screenlex, sessionwatcher, sketch, soulver, subscription-day, tuple, unfold, viaduct, wallspace, zipic
- **Native (canon-eligible):** bauhaus-clock, canary-mail, presentify, resurf, room-service, screen-studio, screenlex, sketch, tuple, viaduct, zipic
- **Adjectives:** approachable(3), restrained(2), cinematic(2), rounded(2), brand-tinted(1), workmanlike(1), modernist(1), horological(1)
- **Peer references:** Notion(2), Linear(2), Raycast(2), CleanShot X(2), Slack(1), Front(1), Height (Electron brand-tinted cross-platform utilities)(1), Braun BN/ABW wall clocks (Dieter Rams / Dietrich Lubs)(1)

### menu-bar utility  (12 members, 11 native)

- **Members:** corner-time, finbar, klack, mac-4-breakfast, mux, open-timer, orbs, raycast, shake-it-on, tokens-4-breakfast, tono, usage
- **Native (canon-eligible):** corner-time, finbar, klack, mac-4-breakfast, mux, open-timer, orbs, raycast, shake-it-on, tono, usage
- **Adjectives:** utilitarian(3), quiet(2), graphite(2), restrained(2), glanceable(2), warm(2), rounded(2), native(1)
- **Peer references:** Bartender(3), One Thing(3), Alfred(3), macOS Spotlight(2), Raycast(2), iStat Menus(2), Alcove (settings)(1), Itsycal / Dato(1)

### warm-editorial / writing & reading  (11 members, 9 native)

- **Members:** caesura, forma, glance, glyph, grape, hejour, letterboxx, mymind, noticky, notion, vocal-notes
- **Native (canon-eligible):** caesura, forma, glance, glyph, grape, hejour, letterboxx, noticky, vocal-notes
- **Adjectives:** calm(4), warm(3), tactile(3), editorial(3), restrained(2), unadorned(2), literary(1), technical(1)
- **Peer references:** Bear(4), iA Writer(3), Craft(2), Apple Notes(2), Things (calm restraint)(1), Bear / iA Writer (paper warmth)(1), Opal / Oak (mindful-app warmth)(1), contrast-peers: Time Out, Stretchly, LookAway (clinical break apps it deliberately opposes)(1)

### warm consumer utility  (10 members, 4 native)

- **Members:** audio-notes-formerly-email-me, autoshelf, compressor, dropadoo, keeby, lookaway, satu, tellie, unfumble, waterlemon
- **Native (canon-eligible):** autoshelf, keeby, lookaway, satu
- **Adjectives:** warm(5), confident(3), friendly(2), utilitarian(2), playful(2), frictionless(1), orderly(1), warm-minimal(1)
- **Peer references:** One Sec(2), chat/quick-capture compose bars (Telegram/Spark send)(1), consumer note-capture utilities (Drafts-style quick capture)(1), CleanMyMac (brand-forward utility warmth)(1), Bartender / Dropover (dark brand-accented Mac utilities)(1), Things (dark) / Reeder (calm grouped-list rhythm)(1), CleanShot X(1), indie Setapp-register Mac utilities(1)

### notch / dynamic-island utility  (8 members, 7 native)

- **Members:** agentpeek, alcove, claude-notch-usage-companion, deskminder, droppy, dynamiclake, folder-hub, healthynotch
- **Native (canon-eligible):** alcove, claude-notch-usage-companion, deskminder, droppy, dynamiclake, folder-hub, healthynotch
- **Adjectives:** glanceable(3), monochrome(1), playful-mascot(1), minimal(1), true-black(1), iOS-mimetic(1), seamless(1), dark-utilitarian(1)
- **Peer references:** NotchNook(7), Boring Notch(6), Alcove(4), MediaMate(3), DynamicLake(2), NotchNook (concept peer — notch-dwelling utility)(1), Boring Notch (concept peer)(1), Ice / Dropover / Rectangle (icon-style peers — monochrome-mark Mac menu-bar utilities)(1)

### developer / terminal-dark tool  (8 members, 5 native)

- **Members:** ayron-time-tracker, code-meter, fello-ai, hora-calendar, inkline-text-editor, macusb, mole, open-screen-shot
- **Native (canon-eligible):** code-meter, hora-calendar, inkline-text-editor, macusb, mole
- **Adjectives:** electric(1), nocturnal(1), instrument-like(1), instrument-panel(1), retro-terminal(1), vigilant(1), dark(1), glossy(1)
- **Peer references:** Linear(2), iStat Menus(2), Vercel / Geist(1), Raycast(1), Warp (terminal)(1), Railway(1), Stats (menu-bar monitor)(1), TripMode(1)

### gallery / content-forward  (7 members, 4 native)

- **Members:** atlas, creos, gatheros, mural, prostir-zvuku, supaste, walltune
- **Native (canon-eligible):** atlas, prostir-zvuku, supaste, walltune
- **Adjectives:** content-forward(4), cinematic(3), immersive(2), airy(1), chromeless(1), curated(1), colourless-chrome(1), gallery-crisp(1)
- **Peer references:** Eagle(2), Cosmos(2), Pinterest(2), Apple Photos(1), Pixave(1), mymind(1), Raycast (dark surface)(1), Cosmos (cosmos.so)(1)

### native-system-idiom utility  (7 members, 5 native)

- **Members:** bartender-6, codeshot, fantastical, hoolo, looq-preview-files-for-mac, maestri, purge
- **Native (canon-eligible):** bartender-6, codeshot, fantastical, maestri, purge
- **Adjectives:** utilitarian(2), reassuring(2), orderly(1), self-effacing(1), orienting(1), neutral(1), unadorned(1), dense(1)
- **Peer references:** macOS System Settings(1), Ice(1), Hidden Bar(1), One Switch(1), iStat Menus preferences(1), Carbon.now.sh(1), ray.so(1), CodeSnap(1)

### glass / translucent utility  (6 members, 6 native)

- **Members:** cachesweep, compresto, dropzone, foldervitrine, liqoria, spacepeek
- **Native (canon-eligible):** cachesweep, compresto, dropzone, foldervitrine, liqoria, spacepeek
- **Adjectives:** translucent(5), airy(2), confident(1), telemetric(1), glassy-blue(1), warm(1), utilitarian(1), glossy-legacy(1)
- **Peer references:** iStat Menus(1), Ice(1), One Thing(1), CleanMyMac menu widget(1), DevUtils(1), Permute (drop-grid + right settings converter layout)(1), CleanMyMac (friendly consumer-utility warmth)(1), Yoink(1)

### electric / accent-dark utility  (4 members, 3 native)

- **Members:** drivemosaic, picmal, radial, revone
- **Native (canon-eligible):** picmal, radial, revone
- **Adjectives:** dark(1), jewel-saturated(1), punchy(1), utilitarian(1), crisp(1), brand-bright(1), translucent(1), gestural(1)
- **Peer references:** DaisyDisk(1), GrandPerspective(1), Linear/Vercel (web-hero language)(1), Permute(1), Handbrake(1), ImageOptim(1), Raycast (launcher)(1), Blender/Maya marking menus (pie menu)(1)

## Psychology-law frequency

| law / heuristic | apps |
|---|---|
| Von Restorff effect (isolation/salience) | 132 |
| Jakob's Law (familiarity) | 111 |
| Aesthetic-usability effect | 108 |
| Hick's Law (choice cost) | 60 |
| Fitts's Law (target size/distance) | 27 |
| Miller/Cowan chunking (working memory) | 25 |
| Recognition over recall | 19 |
| Processing fluency | 17 |
| Serial-position / Peak-end | 16 |
| Hierarchy via de-emphasis (Refactoring UI) | 15 |
| Zeigarnik / Goal-gradient | 15 |
| Demonstrate-don't-describe / description-experience gap | 11 |
| Doherty threshold (responsiveness) | 8 |
| Fogg behaviour model (B=MAP) | 7 |
| Gestalt principles (proximity/figure-ground) | 6 |
| First-impression / 50ms appeal | 5 |
| Loss aversion / emotional framing | 5 |
| Pre-attentive / peripheral-vision capture | 5 |
| Forgiveness / reversibility | 4 |
| Information scent | 4 |
| Social proof / Cialdini persuasion | 4 |
| Tesler's Law (conservation of complexity) | 4 |
| Colour-never-alone (redundant coding) | 3 |
| Progressive disclosure | 3 |
| Choice-overload calibration | 2 |

(single-app laws omitted here; full list in JSON.)

## Signature moves (app -> move)

398 recorded signature moves across the corpus; full list in `_aggregate-ui.json` -> `signature_moves`. A sample:

- **1password** — Periwinkle-violet lowercase field-label system (~#8A80E0) across all detail fields — brand-owned, non-native, and the single most recognizable 1Password desi...
- **1password** — Faithful macOS selection-duality in Electron: soft inset source-list fill in the sidebar vs solid-accent white-text focused-table fill in the content list, h...
- **1password** — Brand-warm consumer chrome over a security tool: coloured per-item favicons, yellow-star favorite glyph, friendly account-switcher — approachability engineer...
- **agentpeek** — Mac-notch-as-face: one black glyph reads simultaneously as the physical notch and a peeking creature with cartoon eyes — the whole product thesis in a single...
- **agentpeek** — System typeface (SF Pro Display) used straight as the wordmark — deliberate native-affiliation move, inherits the platform's crafted first-impression prior.
- **ajar** — Semantic tonal descent: headline set in three measured lightness steps (#040404 -> #3F3F3F -> #808080) so the type literally dims line by line, enacting the ...
- **ajar** — Apple-marketing mimicry: pure-white ground + SF Pro + exact apple.com #1D1D1F pill + oversized restrained display type = deliberate 'looks like Apple shipped...
- **ajar** — Big Sur-era icon: indigo gradient squircle with an apex-lit lavender cone lifted off a soft contact shadow
- **alcove** — The entire app is the signature: import the iPhone Dynamic Island onto the MacBook notch, using a TRUE-BLACK opaque material so software fuses with the physi...
- **alcove** — Icon = the product literally: a thick black display-bezel squircle glowing purple->magenta->pink from within (the island's content aura); the aura hue is reu...
- **atlas** — Chromeless content-first shell — all UI dissolved into 4 floating Liquid Glass islands over edge-to-edge imagery; sidebar collapsed; the collection IS the in...
- **atlas** — Zero-accent UI — chrome contributes ~no colour; selection/emphasis neutral white-on-graphite not system blue; every thumbnail becomes figure against a silent...
- **atlas** — Floating dark-glass view-mode switcher (Grid/Canvas/Infinity) — spatial browsing modes as core identity; Infinity freeform canvas is the hero mode.
- **atlas** — Personable centered title ('HELLO, ATLAS' / '869 ITEMS') — Photos-schema window title made warm; the only chrome typography.
- **audio-notes-formerly-email-me** — Single warm goldenrod hue as the entire brand system, threaded icon background -> menu-bar glyph tint -> the one CTA (committed colour strategy on a near-whi...
- **audio-notes-formerly-email-me** — Reduction to exactly one field + one send button (frictionless quick-capture), paper-plane 'send' metaphor as connective tissue
- **autoshelf** — Single-hue brand commitment: one orange-red (~#E5401C) carries the entire identity — solid saturated sidebar-selection fill (not translucent), the file-with-...
- **autoshelf** — Status-toggle-as-traffic-light: a custom green(on)/red(off) pill per rule row doubles as an at-a-glance enabled/disabled indicator — the one place saturated ...
- **autoshelf** — Rule-as-sentence subtitle: each row's metadata reads as plain English (condition . action . destination — 'Extension is .dmg . Move to Trash . Downloads'), s...
- **ayron-time-tracker** — Monospace as the metadata voice: uppercase-tracked mono eyebrows + tabular mono time values against a grotesque display sans — tracked time reads as instrume...
