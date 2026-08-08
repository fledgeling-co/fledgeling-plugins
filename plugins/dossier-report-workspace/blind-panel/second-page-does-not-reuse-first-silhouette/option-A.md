# Home battery economics (AU) — visual direction and page structure

Plan only. Nothing built. Every figure below is a **placeholder with an expected range**, marked for sourcing at build time — see [Numbers to verify](#numbers-to-verify-before-anything-is-built).

---

## 1. What's already on the shelf

Three pages exist. I read all three plus the DESIGN.md, because the thing to avoid is arriving at a fourth page that looks like a variation of one of them.

| | **cold-flu-evidence** | **dossier/undervolt** | **dossier/workflows** |
|---|---|---|---|
| Name it gives itself | "pharmacy pop" | "instrument panel" | "forensic listing" |
| Ground | Warm paper `#F2F1EC` | Graphite dark `#0E1013` | Cool bone `#EDEEF1` |
| Accents | Acid `#D6FF3D`, orange `#E8862A`, red | Rust `#C7472C` + teal `#3EBBAE` (before/after) | One ultramarine `#2438C8` |
| Type | Archivo Black + Archivo + Plex Mono | Plex Sans + Plex Mono | Bricolage Grotesque + JetBrains Mono |
| Signature device | Magnitude bars on inverted panels; icon array; hatch = uncertainty | A/B system switch; ladders; setting panels; before/after curves | Dot matrix where **loss = absence of fill**; path diagram; retry table |
| Silhouette in one line | Light page, huge black condensed headlines, acid bars | All-dark page, two-accent before/after | Light page, one blue, matrices |

**Shared across all three (the house kit):** the sticky Dossier/Margin colophon, numbered `.cite` buttons with `.citepop` popovers driven by a `const SRC = {...}` map, a rendered `<ol class="srcs">` Sources footer, mono eyebrows, a bordered mono status strip, `~1080–1120px` measure, a 4px spacing scale, `tabular-nums`, skip link, reduced-motion and print branches.

**The rule the codebase states out loud.** From `undervolt/index.html`:

> the sticky colophon is lifted verbatim … Everything below it is this page's own system and shares nothing with it.

and from `workflows/index.html`: `ported colophon (foreign object; its look stops at its border)`.

So: **port the chrome verbatim, invent everything else.** A fourth page that borrows undervolt's dark ground or workflows' single-blue-on-bone would read as a template, and the whole point of these pages is that each one is dressed by its own subject.

---

## 2. Direction: **Day Rate / Night Rate**

### The idea

A home battery makes no electricity. It is a **time machine for a kilowatt-hour** — it takes one that's worth 3c at 1pm and spends it at 6pm when it would have cost 45c. Everything about the economics is that one move, repeated. How wide the gap is, how many times you can make the trip, and whether you run out of trips before the warranty ends.

So the ground itself carries the mechanism: **the page has two grounds, day and night, and it changes ground at the seams where the argument crosses over.**

- **Day sections** — pale ledger green. Solar, exports, the feed-in collapse, rebates, who it suits. This is the paper the sums are done on.
- **Night sections** — midnight indigo. The evening peak, what the battery discharges into, what it costs, what it earns, whether it pays back. This is where the money is actually made.
- The changes are **hard seams, never gradients**, and each seam is occupied by a figure that crosses it.

That gives the page a silhouette no other page here has: scroll it fast with your eyes half-closed and you see broad alternating bands of pale green and deep indigo, with the same violet thread running through both. cold-flu is light with dark chart panels; undervolt is dark throughout; workflows is light throughout. This is the only one that **alternates as a structural argument**.

### The second idea: the figure is the headline

All three existing pages lead sections with big display type. This one doesn't. **Headings are modest; the numbers are the largest thing on screen.** Money sets its own type size. It's how a statement or a prospectus behaves, and it's the fastest way to make a page about money feel like it was actually calculated rather than written.

### Directions I rejected

- **Warm cream editorial with a serif and terracotta.** cold-flu's DESIGN.md already rejected this for itself, and here it would make a page about $12,000 feel like a weekend supplement.
- **Solar brochure — sky blue, sunburst gradients, a smiling roof.** Category costume. The page's argument is that the brochure numbers don't survive contact with a tariff, so it can't be dressed as one.
- **Green = eco.** The one thing this page must not do is imply the answer is yes because batteries are good. The ledger green is *accounting paper*, not environmentalism, and I'd say so in the DESIGN.md so nobody later "helpfully" pushes it toward eco-green.
- **Anything red-accented.** Red would be correct accounting semantics ("in the red"), but the chrome's proof-red `#C43A2B` sits in a sticky bar at the top of every screen. Half-matching the chrome reads as a mistake — the DESIGN.md says exactly this. Red is off the table for the content register; sign gets encoded by position and fill instead.

---

## 3. Tokens

House DESIGN.md frontmatter style, so it drops straight into a `DESIGN.md` at build time.

```yaml
name: Day Rate / Night Rate
description: >-
  Two grounds — ledger green for the day side, midnight indigo for the night
  side — because a battery's entire economics is moving a kilowatt-hour from
  one to the other. One violet accent means stored energy and nothing else.
colors:
  day:          "#E9EEE6"   # accounting analysis paper. NOT eco-green.
  day-raised:   "#DFE6DB"   # alternate table rows, inset notes
  day-rule:     "#C4CFBE"
  night:        "#101828"   # midnight indigo — blue cast, unlike undervolt's neutral graphite
  night-raised: "#182032"
  night-rule:   "rgba(232,236,242,.13)"
  ink:          "#15201A"   # near-black with a green cast, on day
  ink-2:        "#3C4A40"
  mute:         "#6E7A70"
  ink-night:    "#E8ECF2"
  ink-night-2:  "#A3ADBE"
  mute-night:   "#6E7889"
  volt:         "#4B2FBF"   # electric violet, dark tone — fills and text on day  (≈8:1)
  volt-lift:    "#9B7CFF"   # light tone — fills and text on night              (≈5.5:1)
  volt-tint:    "rgba(75,47,191,.12)"
typography:
  # Money is argued, so money is set in the serif.
  # Units are measured, so units are set in the mono.
  display:    { fontFamily: Newsreader, fontSize: 64px, fontWeight: 500, lineHeight: 1.06, letterSpacing: "-0.02em" }
  h2:         { fontFamily: Newsreader, fontSize: 30px, fontWeight: 500, lineHeight: 1.15 }
  h3:         { fontFamily: Newsreader, fontSize: 20px, fontWeight: 600, lineHeight: 1.25 }
  money-xl:   { fontFamily: Newsreader, fontSize: 88px, fontWeight: 500, lineHeight: 0.95, fontFeature: "'tnum' 1" }
  money-lg:   { fontFamily: Newsreader, fontSize: 44px, fontWeight: 500, fontFeature: "'tnum' 1" }
  body:       { fontFamily: Newsreader, fontSize: 18px, fontWeight: 400, lineHeight: 1.62 }
  standfirst: { fontFamily: Newsreader, fontSize: 22px, fontWeight: 400, lineHeight: 1.5 }
  unit:       { fontFamily: DM Mono, fontSize: 15px, fontWeight: 500, fontFeature: "'tnum' 1" }
  label-caps: { fontFamily: DM Mono, fontSize: 11px, fontWeight: 500, letterSpacing: "0.16em", textTransform: uppercase }
  micro:      { fontFamily: DM Mono, fontSize: 10px, fontWeight: 500, letterSpacing: "0.1em" }
  # chrome only, ported: Bricolage Grotesque + Space Mono
rounded:  { none: 0px, sm: 5px }   # 5px is the brand tiles' own radius, chrome only
spacing:  { xs: 4, sm: 8, md: 12, lg: 16, xl: 24, "2xl": 32, "3xl": 48, "4xl": 64, "5xl": 96, measure: 1080px }
```

**Font count:** 2 own (Newsreader, DM Mono) + 2 ported chrome (Bricolage Grotesque, Space Mono). Matches what undervolt and workflows each carry.

**No existing page uses a serif.** That one choice does most of the differentiating work at a glance, and it's defensible: prospectuses, annual reports and disclosure statements are serif documents, and this page is arguing like one.

### Encoding rules (the house "colour never alone" rule, applied)

| Meaning | Colour | Second signal | Third |
|---|---|---|---|
| Stored / moved by the battery | Solid violet | Above the datum line | Labelled |
| Bought from the grid | Ink | 45° hatch | Labelled |
| Exported to the grid | None | Outline only, no fill | Labelled |
| Your input (calculator) | Violet | Underlined field | — |

Fully legible in greyscale: solid / hatched / outline are three distinct textures.

### One device the other pages don't have: a provenance glyph

Every number on the page is one of two things, and the page says which:

- **Measured** — carries a numbered citation `[7]`, same `.cite` component as the other pages.
- **Modelled** — carries a `◇` and is derived from an assumption stated in the caption.

A payback figure is *always* modelled. Being upfront that the headline number is a model, while the spread and the rebate rates behind it are cited, is the most honest thing this page can do, and it's cheap. cold-flu encodes *certainty* with hatching; this page encodes *provenance* with a glyph. Different job, different device.

---

## 4. Collision check against the existing three

| Axis | cold-flu | undervolt | workflows | **this page** |
|---|---|---|---|---|
| Ground | one warm light | one dark | one cool light | **two, alternating by argument** |
| Body face | grotesk | grotesk | grotesk | **serif** |
| Accent count | 3 | 2 (paired) | 1 | 1 |
| Accent hue | acid/orange/red | rust/teal | ultramarine | **violet** — unclaimed |
| Headline scale | 124px display dominant | large display | 72px display | **modest headings, 88px money** |
| Signature figure | magnitude bars on inverted panels | before/after curve pairs | dot matrix, loss = void | **break-even crossing against a warranty rule** |
| Reading model | ranked comparison | pick-your-machine A/B | forensic narrative | **statement → verdict → your turn** |

No axis repeats. The violet is far enough from proof-red `#C43A2B` in both hue and value that the chrome still reads as a foreign object — worth an explicit eyeball at build time, since that's the one adjacency that could go wrong.

---

## 5. Page structure

Spine: **A battery is a financial instrument. Here's its return, here's what eats it, here's whether yours clears the bar.**

### Hero — day

```
┌────────────────────────────────────────────────────────────────────┐
│ ▣ DOSSIER  ▣ MARGIN   Field report · every figure cited     ← chrome│
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  HOME BATTERY STORAGE · AUSTRALIA · AUGUST 2026          ← DM Mono  │
│                                                                    │
│  You are not buying                                                │
│  electricity. You are buying                     ← Newsreader 64px  │
│  the gap between two prices.                       max 22ch         │
│                                                                    │
│  A battery never makes a kilowatt-hour. It moves one from the       │
│  hour it is worth 3c to the hour it costs 45c, and it can do        │
│  that a fixed number of times before the warranty runs out.         │
│  Everything else is detail.                                         │
│                                                                    │
│  Your tariff, your state and what time you cook decide the          │
│  answer. This page gives you the working, not the verdict.          │
│                                                                    │
│  ┌──────────────────────────────────────────────┐                  │
│  │ PRICES AS AT AUG 2026 · FEDERAL REBATE STEP  │  ← mono status    │
│  │ DECLINES EACH 1 JAN · ◇ = MODELLED           │     strip         │
│  └──────────────────────────────────────────────┘                  │
└────────────────────────────────────────────────────────────────────┘
```

### 1. The spread — day

The engine of the whole thing: `(import price − feed-in tariff)` is what one stored kilowatt-hour earns. Then the counterintuitive point that deserves its own callout: **the collapse of feed-in tariffs is what made batteries viable.** When export paid 12c the battery had little to beat; at 3c it has almost the full retail price to capture.

Component — **spread bars on a shared c/kWh ruler**:

```
THE SPREAD · what one stored kilowatt-hour earns          c/kWh
          0       10       20       30       40       50
          ├────────┼────────┼────────┼────────┼────────┤
NSW  Ausgrid    ▏░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▏          38.2  [1]
VIC  Citipower  ▏░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▏               32.7  [2]
SA   SAPN       ▏░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▏             35.1  [3]
QLD  Energex    ▏░░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▏                  28.4  [4]
WA   Synergy    ▏░░░░░▓▓▓▓▓▓▓▓▓▓▓▏                       21.6  [5]
                 └ paid to you        └ charged to you
                 ░ feed-in    ▓ THE SPREAD (violet)
```

Left tick = feed-in tariff. Right end = import price. The violet band between them is the money. One ruler, every row measured against it — that ruler idea recurs everywhere on the page.

### 2. Seam figure — the 24 hours (crosses day → night)

Full-bleed, sitting exactly on the ground change. The page's signature figure.

```
════════════ ledger green ends ════════════════════════════════
   00    03    06    09    12    15    18    21    24
    │     │     │     │     │     │     │     │     │
 price ─────────────╮                  ╭──────────╮
                    ╰──────────────────╯          ╰────  TOU c/kWh
 solar         ╭────────────────────╮
        ───────╯                    ╰───────
 load   ──╲___╱────────────────────╲_______╱▔▔▔╲______
                                     ▲ evening peak
 battery       ░░░░░CHARGE░░░░░         ▓▓▓DISCHARGE▓▓▓
               bought at ~0c            avoids 45c
════════════ midnight indigo begins ═══════════════════════════
```

### 3. What it costs — night

- Installed `$/kWh` before and after the federal discount.
- **How the Cheaper Home Batteries discount actually works** — delivered through the small-scale certificate mechanism, sized off usable capacity, with a VPP-capable requirement, and **it steps down every 1 January**. A reader needs to see that waiting a year is a real cost, without the page turning into a countdown gimmick.
- State layers stacked on top: NSW, VIC, WA, NT, ACT.

Component — **rebate decay ladder**, one row per year to 2030, showing `$/kWh` and the resulting net install for a reference 13.5 kWh system. Steps, not a curve; a step is what it actually is.

### 4. What it earns — night

The section that does the most work, because this is where installer quotes are optimistic.

Component — **the leak table.** Nameplate goes in the top, and each row takes a slice out. The violet fill visibly shrinks down the column:

```
WHAT YOU PAID FOR, AND WHAT ACTUALLY CYCLES      13.5 kWh nameplate

  Nameplate             13.5  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  100%
  Usable capacity       13.5  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  100%  [6]
  After round trip      12.2  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░   90%  [7]
  Filled, median day     9.8  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░   73%  ◇
  Emptied, median day    8.1  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░   60%  ◇
  ──────────────────────────────────────────────────────────────
  EARNING               8.1 kWh/day × 38.2c  =  $3.09/day
                                             =  $1,128/yr  ◇
        ▲ the only number that pays you. Not the one on the quote.
```

Then VPP participation as a separate line: what it adds per year, and what it costs you in cycles and in control over your own battery at 6pm.

### 5. Payback against warranty — night. The climax.

```
CUMULATIVE POSITION                     warranty ends ┃ yr 10
   +$4k ┤                                             ┃
        │                               ╱─────────────┃──── best fit
    $0 ─┼──────────────────────────╱────────────────  ┃  ← nominal zero
        │                     ╱   ╱                   ┃
        │  ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁┃▁▁ offset line
        │              ╱    ╱        ─ ─ ─ ─ ─ ─ ─ ─ ─┃ ─ ─ median ◇
   -$4k ┤        ╱   ╱      · · · · · · · · · · · · · ┃· ·  poor fit ◇
        │  ╱   ╱                                      ┃
   -$8k ┤╱ ╱                                          ┃
        └──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬───┃──
           1  2  3  4  5  6  7  8  9 10 11 12 13 14   ┃ 15   years

   The warranty rule is hard and vertical. A line that hasn't crossed
   before it is the answer, and no amount of prose changes that.
```

**The offset line is the page's best contribution.** The same money sitting in a mortgage offset compounds. The battery doesn't have to beat zero — it has to beat *that*, and almost no comparison you'll be shown makes it. Drawing it as a second, rising datum reframes the whole chart and costs one extra line.

### 6. Who it works for, who it doesn't — day

Ruled rows with a verdict, not decorative cards:

| Household | Verdict |
|---|---|
| Big evening load, time-of-use tariff, oversized solar | **Clears easily** |
| Average family, flat tariff | **Marginal** — flat tariffs gut the spread |
| Home all day, already self-consuming most of the solar | **Barely** — the battery has little left to capture |
| Holds a legacy premium feed-in tariff | **Usually not** — the battery cannibalises an export you're paid well for |
| Renting, or an apartment | **Not applicable** |

That fourth row is the one nobody tells people, and it's the sharpest thing the page can say.

### 7. What changes the answer — day

Two-way network tariffs and export charges; time-of-use versus flat; VPP terms and who controls discharge; the annual rebate step-down; the interest rate as the real hurdle.

### 8. What isn't settled — day

House pattern, borrowed from undervolt because it's the honest part: real degradation at Australian ambient temperatures versus datasheet; whether VPP payments hold as more batteries join; replacement cost in 2036; whether export charges spread.

### 9. The short version — night

Four or five blunt one-liners. Heading plus a sentence, nothing else.

### 10. Work out yours — night. The one interactive thing.

State, tariff type, daily consumption, evening share, system size, quoted price. Out: your spread, annual saving, payback year, and **whether it lands inside warranty** — a binary verdict, not a number to squint at. Reader inputs render in violet, which is where the accent's rule (*this is your number, not mine*) finally pays off.

No-JS fallback: three fully worked examples, printed. **This is the piece to cut first if scope needs cutting** — the page still works without it.

### 11. Sources — day, then closing chrome band

Same `<ol class="srcs">` rendered from `const SRC`, plus a short note on method and on where sources disagreed.

---

## 6. What's reused, what's new

**Ported verbatim:** colophon markup and CSS, `.cite` / `.citepop` mechanics and the `SRC` map, skip link, Sources footer, reduced-motion and print branches, the 4px spacing scale.

**New to this page:** the two-ground alternation, the serif register, money-in-serif / units-in-mono, the shared-ruler spread bars, the leak table, the break-even-versus-warranty chart with an offset-account datum, the `◇` provenance glyph, the calculator.

---

## 7. Numbers to verify before anything is built

Every figure above is illustrative. These are the ones the page stands on, in rough order of how badly a stale value would hurt:

1. **Federal Cheaper Home Batteries discount** — current `$/kWh`, the step-down schedule to 2030, eligibility window and the VPP-capable requirement. Volatile; steps annually.
2. **Retail import prices and feed-in tariffs per state/distributor** — the spread table is the page's engine. Volatile; changes at least yearly, and several jurisdictions have cut minimum feed-in tariffs recently.
3. **State schemes** — NSW, VIC, WA, NT, ACT. Volatile, and they stack with the federal discount differently.
4. **Installed cost per kWh** — before and after rebate, with a range rather than a point.
5. **Two-way / export tariffs** — which networks now charge for daytime export, and how much.
6. **Warranty terms** — years, cycles, retained capacity, for the two or three most-installed products.
7. **Round-trip efficiency and annual degradation** — datasheet versus measured.
8. **The prevailing mortgage rate** for the offset comparison.

Anything that survives only as an assumption gets the `◇` and a stated basis in the caption. Nothing modelled should ever carry a citation number — that's the one way this page could quietly mislead.

---

## 8. Open questions for you

1. **Audience.** Someone with solar deciding whether to add a battery, or someone deciding on both at once? I've written it for the first, which is the larger and better-served-by-honesty group. Changing it mostly changes sections 3 and 6.
2. **Calculator in or out?** It's the highest-value element and the biggest build. Happy to ship v1 with three worked examples and add it later.
3. **National, or lead with one state?** National with per-state rows is more useful but keeps every number in a range. A NSW-first page could be far sharper. I'd default to national.
4. **Verdict or working?** I've deliberately kept the page from concluding "yes" or "no", because the honest answer is "it depends, here's on what". If you'd rather it took a position, section 6 is where that would live.
