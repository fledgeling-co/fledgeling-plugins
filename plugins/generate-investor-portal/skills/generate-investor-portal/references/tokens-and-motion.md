# Lifting a theme, and choosing motion

## The theme is a copy job, not a design job

A supplied DESIGN.md is **binding**. Take exact values. Do not round `#D72229` to `#D42229`
because it reads the same — it does not, and a near-miss is worse than an obvious substitution
because nobody catches it.

Map the DESIGN.md's names onto the contract's:

| DESIGN.md | contract |
|---|---|
| `primary`, `primary-hover`, `primary-pressed`, `primary-tint` | same |
| `ink`, `ink-body`, `ink-muted` | `ink`, `inkBody`, `inkMuted` |
| `canvas`, `surface`, `surface-sunken`, `surface-dark`, `surface-footer` | camelCase equivalents |
| `font-display`, `font-body`, `font-mono` | `fontDisplay`, `fontBody`, `fontMono` |
| `rounded.*` | `radius.*` |
| `elevation.*` | same |
| `motion.*` | same |
| container / gutter / prose | **do not copy.** The grid is not a tenant axis — the contract pins it to the platform's 1200 / 24 / 68 and refuses anything else as `measuredGrid`. A width measured off a brand's site and passed through is a style channel with a numeric keyboard, and it re-breaks parity per tenant. Every DESIGN.md measured so far states these exact three. |

## The one token you must compute: `primaryOnDark`

Almost no DESIGN.md carries it, and its absence is the most common accessibility failure in a
generated portal.

A brand accent chosen against white will usually fail AA on a charcoal band. Measured on a real
shipped portal: `#D72229` on `#2E2B2B` is **2.77:1** against a 4.5 floor. It landed on the hero
headline, both hero CTAs, the running ticker and the footer's only signup button — **35 failing
nodes on one page**, and the footer button repeated on eight of ten surfaces, making it the
most-repeated AA failure on the site.

Compute the lifted variant rather than guessing one:

```python
def srgb(c):
    c /= 255
    return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055) ** 2.4

def lum(hex_):
    h = hex_.lstrip('#')
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return 0.2126*srgb(r) + 0.7152*srgb(g) + 0.0722*srgb(b)

def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)
```

Lighten the accent along its own hue until `ratio(candidate, surfaceDark) >= 4.6`. Keep the hue —
a lifted red is still the brand; a pink is not.

**Check the muted-on-dark alphas too.** `rgba(255,255,255,.34)` reads as "subtle" and measures
2.98:1. The honest range is `.55`–`.62`. This is arithmetic, not taste.

**Then assert it.** Do not write the ratios into a comment and move on — a comment carrying six
eyeballed figures is worse than none, because the next reader trusts it. Compute, and put the
computed values in the record's provenance note if you record them at all.

**And check that something reads it.** Emitting the token is not applying it. On a real build
`primaryOnDark` was carried by the contract, set by every record, present in the rendered HTML,
and referenced by **no rule in the stylesheet** — so every accent word on every dark band was
still painted in raw `--primary`, and the house tier's 72px company name sat at **2.14:1**. It
passed every check anyone thought to run, because all of them looked for the token rather than
for the colour on the node.

Two things follow. Grep the stylesheet for `var(--primary-on-dark)` before believing the token
does anything. And when you add the rule, **put it last in the file**: `.thesis__n` and
`.hero h1 em` declare `color: var(--primary)` at equal specificity, so a rule placed earlier
loses to source order and fixes only the selectors that happened to be more specific. An
equal-specificity override that loses to source order is indistinguishable from a rule that was
never written.

## The other half nobody wrote: the accent as text on a LIGHT ground

`primaryOnDark` covers the dark bands. Nothing covers the light ones, and the reason the gap
survives is that the reference accent clears AA there **by luck** — `#D72229` on `#F7F6F5` is
5.03:1 — so there is no tenant to show it on until a brand arrives one luminance step warmer.

Measured on a listed company's own brand orange, `#E65400`, correctly extracted from its own
DESIGN.md and correct as a colour:

| Role | Pairing | Ratio | Needs |
|---|---|---|---|
| `.over` §-eyebrow, 13px/700 | accent on the record's own sunken band | **3.37:1** | 4.5 |
| the current page in the nav | accent on white | **3.72:1** | 4.5 |
| the brand monogram | the record's **stated** white ink, on the accent | **3.72:1** | 4.5 |
| the header CTA | the same stated white ink | **3.72:1** | 4.5 |

Four serious axe nodes, on a tier that fronts 7,404 companies, from a generator that took the
accent straight into a text role without ever asking whether it could be read there.

**The ordering trap, and it is the whole of the fix.** WCAG 1.4.3 asks 4.5:1 of body-size text
and **3:1 of large text (≥24px, or ≥18.66px bold) and of non-text**. That orange is right as a
button fill, right as a 72px display word, right as a rule under a heading. A blanket 4.5 floor
over the accent rejects the brand colour in every place it belongs, and the brand colour is not
the defect. So the rule is **role-aware**: compute a lifted variant for the small-text roles —
the mirror of `primaryOnDark` — and leave the raw accent to the fills and the display sizes.

Lift it against whichever of the record's own light grounds the accent reads **worst** on. One
token paints the eyebrow on `surface` and on `surface-sunken` alike, and a variant that clears
the easier of the two fails on the other.

### "Worst ground" needs the grounds ENUMERATED, or it is advice

The rule above is right and it was still not enough, and the way that surfaced is worth keeping. A
blind reviewer, reading an answer written under this file, caught a lifted `primaryOnDark` that
cleared 4.5:1 against `surface-dark` and measured **3.78:1 against `surface-dark-raised`** — a token
the same record emitted, in the same table. Every token read as repaired.

Nothing was wrong with the rule. What was missing was the **list**: a record on a dark theme has at
least three dark grounds (`surface-dark`, `surface-dark-raised`, `surface-footer`) and two light ones
(`surface`, `surface-sunken`), and "worst" over an unenumerated set is whichever one the author
happened to think of. `assets/record-gate.mjs` now asks about all of them, and the judge's exact
figure — 3.78:1 — is the one it prints.

**An unenumerated ground is a ground nobody measures.** The same applies to any future surface token:
add it to the palette and it joins the pairs, or it is exempt by name in the case.

### `focus-ring = primary` is an identity that fails on a dark band

Adding the enumeration above immediately found something the reference build has always carried. The
derivation table in this file lists `--focus-ring = --primary` as an identity, and on a record with a
dark band that identity does not hold at the **3:1 non-text floor**:

| Ring | Ground | Ratio | Needs |
|---|---|---|---|
| the reference's own `#D72229` | its own `#2E2B2B` | **2.77:1** | 3.0 |
| a deep brand blue `#0B4F9E` | a `#1F2933` band | **1.85:1** | 3.0 |

2.77 is a number already in this file — it is the ratio recorded for `#D72229` as *text* on that same
ground. Nobody had applied it to the ring, because the ring is not text and the 4.5 conversation had
moved on. A keyboard user tabbing across a dark band gets a focus indicator they cannot see.

So: **the focus ring is a role, not an alias.** Derive it as the accent adjusted until it clears 3:1
on *every* ground it can appear over — which on a record with both a light canvas and a dark band is
usually a mid-tone of the accent's hue rather than the accent itself. It is the same shape as `link`
and `primary-on-dark`: an identity is only safe while nothing under it moves.

This one is worth dwelling on for a second, because of how it was found. It was not found by review,
and not by reading. It was found by **adding one pairing to a gate and watching the supposedly clean
fixture fail** — and the fixture had carried the defect since the day it was written. A new check is
the cheapest opportunity you will get to discover that your control was never clean.

**And a stated token is not a waiver.** `onPrimary` was computed when a record left it unset and
honoured when a record stated it — so a DESIGN.md stating `#FFFFFF` carried 3.72:1 ink all the
way to the header CTA and the brand monogram. A theme token is a statement about a colour, never
a statement that it can be read on the thing it sits on. **A stated value that fails its role's
floor is replaced exactly as an absent one is**, and the replacement goes in the record's
provenance, because a repair nobody recorded looks identical to a brand that got it right.

### The repair goes in a ROLE. It never goes in `primary`.

The other end of the same trap, and it destroys the brand rather than the contrast. Measured on
production 2026-08-08: `jb-hi-fi-limited`'s `theme.primary` is **`#807500`** — a dark khaki. JB
Hi-Fi's brand is a saturated yellow. That value is the *repaired* colour written back into the
brand slot, so it paints the monogram disc, the header CTA, the hero's accent word and every
stat chip. The raw brand colour appears nowhere on the portal, and the portal does not look like
JB Hi-Fi.

A near-miss on a brand colour is worse than an obvious substitution because nobody catches it —
that rule is already in this file for extraction, and it applies identically to repair.
`primary` stays exactly as the brand states it. The lifted value lives in `link`,
`primaryOnDark`, `onPrimary` and the small-text eyebrow role, each of them named, each of them
recorded. **If the repair has replaced the brand colour, the repair is the defect.**

### `onPrimary` passes and the reader still cannot read it: an alpha undoes an AA repair

A third site the two rules above still miss, and the first diagnosis of it — written here on
2026-08-08 from an axe report — was **wrong in a way that would have shipped the defect again**.
It is left visible rather than deleted, because the correction is the lesson.

The finding: `<span class="unit__fl">`, the 12px unit label on the accent stat chip, fails 4.5:1
on four of six live tenants (4.14 – 4.35). The first reading was "the ink was chosen by eye and
lands in the low fours — compute `onPrimary` against `primary` at the 4.5 floor, always."

**Measured in the browser instead of read off axe, that reading is false.** `.unit__fig` sets
`color: var(--on-primary)`, and the vars layer already *replaces* a stated `onPrimary` that
fails 4.5:1 on the accent. The token pair is compliant on every tenant:

| Tenant | ink (`--on-primary`) | accent | ratio | `opacity` | composited | ratio |
|---|---|---|---|---|---|---|
| alfabs | `#ffffff` | `#d72229` | 5.06 | `.9` | `rgb(251,233,234)` | **4.32** |
| metallium | `#1C1B1B` | `#E85A2A` | 4.85 | `.9` | `rgb(48,33,29)` | **4.34** |
| bhp | `#1C1B1B` | `#E65400` | 4.61 | `.9` | `rgb(48,33,24)` | **4.16** |
| jb-hi-fi | `#FFFFFF` | `#807500` | 4.71 | `.9` | `rgb(242,241,230)` | **4.15** |
| telstra | `#FFFFFF` | `#0D54FF` | 5.63 | `.9` | `rgb(231,238,255)` | 4.84 |

Every tenant passes on the colours it states, 4.61 to 5.63. A single `opacity: .9` on the label
composites that repaired ink back through the accent underneath it and takes four of five below
AA — including the hand-built reference build.

Three things follow, and the third is the general one:

- **A contract rule comparing `theme.onPrimary` to `theme.primary` would have caught none of
  them.** It is the rule the first reading asked for. It scores 4.61–5.63 and returns green.
- **`opacity` is the only property that moves a computed contrast without moving any colour
  token.** Every gate that reads a design system's resolved token map is structurally blind to
  it, and so is every audit that reasons from the tokens rather than from the render.
- **Muting text is a COLOUR, chosen and checked against its ground — never an alpha applied to a
  colour that was already chosen and checked.** If a label wants to sit back from the figure
  above it, give it its own token and measure that token.

And the method note, which is why the first reading was wrong: axe reports the **composited**
foreground (`#f2f1e6`), which looks like a stated token and is not one. `#f2f1e6` is
`0.9 × #FFFFFF + 0.1 × #807500`. When a measured foreground is not a value anywhere in the
theme, something between the token and the pixel is doing arithmetic — find it before writing
the rule.

### The LEADING family is the claim; everything after it is a fallback

`lib/portal-contract.ts` refuses a stack that names a face nothing serves. That question —
*does this face exist anywhere?* — is the wrong one for the **head** of the stack. Measured on
production, and it passed every gate:

```
jb-hi-fi-limited   declares "Roboto, Helvetica, Arial"   →   renders Helvetica
```

Roboto ships on Android and ChromeOS, and on neither Windows nor macOS. Mid-stack that is a
perfectly good fallback — the reference tenant's own stack carries Roboto and Segoe UI behind
Figtree, and that is what a fallback chain is for. **As the head it is a claim that only the
Android share of readers can honour.**

The contract now refuses `roboto` and `segoe ui` in position 0 unless the record actually serves
them (`NON_LEADING_WEB_SAFE`). When you extract a stack from a DESIGN.md, read the head first:
if it is not a face this origin serves and not a face every desktop platform supplies, either
add it to `TENANT_WEBFONTS` with its licence recorded and list it in `webfonts`, or lead with
the face the stack will actually render.

## Motion is a preset, not code

Pick per section from the enumerated set:

| preset | for |
|---|---|
| `reveal` | the default. Fade-and-rise on scroll |
| `lineMask` | a display headline arriving a line at a time |
| `parallax` | a background photograph drifting as its section leaves |
| `countUp` | numerals whose final value is already in the HTML — and **never over a stated figure.** The contract refuses it (`lodgedFigureMotion`) on any section carrying a `SourcedValue` or rendering a lodged document: ramping a disclosed number from zero makes it emphasis, and over a resource or reserve figure it detaches the number from the competent-person statement it is only valid alongside |
| `lineDraw` | an SVG path drawing itself once |
| `clipUncover` | a photograph uncovering on entry |
| `railDrift` | a horizontal rail drifting against the scroll |
| `magnetic` | pointer-following pull on a primary control |
| `marquee` | a continuous tape |
| `webgl` | a three.js layer, named by preset |

### The WebGL preset comes from the company's own world

| preset | suits |
|---|---|
| `spaceFrame` | a drifting Warren truss — fabrication, construction, engineering |
| `strata` | slow-drifting bands — resources, energy, mining |
| `globe` | a wireframe globe with arcs — logistics, shipping, multi-market |
| `pointField` | a displaced point field — the house default when nothing fits |

Set `opacity` low (the shipped reference uses **0.26**) and give it a `mask` so it occupies a
band rather than the whole hero. The first version of that reference ran the frame across the
full hero at 0.55 and it read as scribble through the copy — a mask confining it to a band low
in the frame is what turned it into structure.

**Four presets do not cover the ASX, and the collision is invisible from inside one tenant.**
`pointField` is the house default *and* the answer for anything that is not resources, not
logistics and not fabrication — which is most listed companies. Measured on production
2026-08-08, a consumer-electronics retailer and a telco both landed on it, and because the four
tuning axes are each derived from a DESIGN.md sentence, both derived the same four
(`planar` / `solid` / `standard` / density 1). The result is a byte-identical seven-value
vector, and the framebuffer probe scores the pair at a still-distance of **1.169** where the
gate's floor is 1.9 — with `shape 0.036`, `ink 0.015` and `churn 0.002`. The two heroes are the
same picture at the same density with the same movement; **0.927 of the entire distance is
hue.** Strip the brand colour and they are indistinguishable.

Note which pair failed. The *same-sector* pair the design worried about — two retailers — scores
2.941 and is fine. It is the **cross-sector** pair that collapsed, because both sectors route to
the same default. So:

- Before emitting the layer, compare the full vector against every published paid tenant.
- On a collision, take the corpus's **runner-up** preset and record the choice, the margin and
  the tenant it avoided in `generation.motion`.
- If there is no runner-up above the floor, say so and stop. Inventing a fifth axis to break the
  tie is the distinctiveness-loop failure this skill already refuses: every option must be
  traceable to a sentence in the brand's own documents.

### Two rules that are not stylistic

- **Never put content behind motion.** Every layer is an optional CDN load behind SRI; a section
  whose motion never arrives must still render complete.
- **`marquee` requires an operable pause control** — WCAG 2.2.2, Level A. `prefers-reduced-motion`
  is honoured but a media query is not a mechanism, and hover-to-pause does not exist on touch.


## The surface set, on a dark theme

`primaryOnDark` is the token everyone knows to compute. The surfaces are the ones that
get missed, and they fail more visibly.

A stylesheet's defaults are not neutral — they were authored for one theme. A DESIGN.md
that states a dark canvas but omits `surface-sunken` therefore inherits a **light**
default for it, and every rule keyed to that token paints a light band on a dark page.
On a real run this was `.facts tbody tr:nth-child(even)`: white bars with invisible text
straight across a dark company's facts table, on a page that had already passed a token
check and a 200.

So derive, rather than inherit — and note that **both branches are real**. Writing the light
branch as `undefined` is how the same defect survived on light brands for a whole review cycle:

```js
const isDark = luminance(canvas) < 0.5;
surface:       stated ?? (isDark ? shift(canvas, +10) : '#FFFFFF')
surfaceSunken: stated ?? shift(canvas, isDark ? +18 : -8)   // NOT `: undefined`
border:        stated ?? shift(canvas, isDark ? +28 : -20)
ink:           stated ?? (isDark ? '#F5F5F5' : '#1C1B1B')
inkBody:       stated ?? shift(ink, isDark ? -30 : +30)
```

The rule generalises past colour: **the token a brand forgets is the token that breaks.**
Compute it from what the brand did state, and a partial DESIGN.md produces a coherent
portal rather than a half-inverted one.

## Every token, not only the surfaces — an unset token is another company's brand

The derivation above covers the tokens that fail *visibly*. The ones that fail *quietly* are the
rest of the palette, and they fail worse, because the stylesheet's defaults are not neutral
values — they are one specific company's brand, the one the reference build was authored for.

Measured on a live generated portal with a `#0A0A0A` canvas: **12 of 25 colour tokens unset.**

| Token | Fell back to | What it painted |
|---|---|---|
| `--primary-tint` | the reference's pale **pink** | an alert band with white text on pale pink — three lines unreadable |
| `--link` | the reference's red | a facts-table link at 3.28:1 on near-black |
| `--focus-ring` | the reference's red | this company's keyboard focus ring is another company's brand colour |
| `--primary-pressed` | the reference's dark red | pressing this company's orange button turns it the other company's red |
| `--border-strong` | a light grey | near-white hairlines and arrow strokes on a black page |
| `--on-primary` | `#FFFFFF` | every secondary button failing AA **on hover** |

So: **a themed record emits a complete palette.** Two mechanisms, and you want both:

1. **Derive what is genuinely derivable, from relationships you can verify against the
   reference** — never from invented ones. *Measure before declaring a relationship
   uninventable.* An earlier version of this file said `--link`, `--border-strong` and
   `--surface-footer` were not derivable and a rule for them "would be an invented
   relationship dressed as a recovered one". They were then measured against the reference
   stylesheet and every one of them is **recovered**, to within a unit or two per channel:

   ```
   --border-strong        #E2DFDD → #C4C0BE     −30 / −31 / −31   (border, stepped)
   --surface-dark-raised  #2E2B2B → #3C3939     +14 / +14 / +14
   --surface-footer       #2E2B2B → #181717     −21 / −20 / −20
   --on-dark-muted        #FDFCFC → #B7B2B1     −72 per channel, floored at AA
   --surface-sunken       #F7F6F5 → #EFEDEC      −8 /  −9 /  −9   (canvas, stepped away)
   --ink-body             #1C1B1B → #3A3A3A     +30 / +31 / +31
   --focus-ring           = --primary                identity
   --on-dark              = --surface                identity
   ```

   `--link`, `--primary-hover` and `--primary-pressed` are not fixed offsets: they are the
   accent adjusted **until it is readable**, which is the relationship those numbers encode,
   so compute that. The test for "recovered, not invented" is mechanical — strip the token
   from the reference theme and check the derivation puts the reference's own value back.
   If it does not, you invented it. Assert that reproduction; do not write the offsets into a
   comment and trust them.

   **Do not gate the derivation on `isDark`.** Every derivation in the first version was
   written `isDark ? … : undefined`, because the review that prompted them measured a
   near-black tenant and a light brand feels close enough to a light reference to be safe. It
   is not. Measured on a brand with a `#F6F3EC` warm-cream canvas: `--surface-sunken` and
   `--ink-body` unset, so its sunken bands painted the reference's grey `#EFEDEC` under a
   cream page and its body copy was the reference's ink. **A theme is not the reference's
   because it is also light.**

   And **derive at the root of the chain, not off another optional token.** A derivation
   keyed on a token that is itself optional repairs nothing when both are absent:
   `--border-strong` computed from `border`, `--surface-footer` from `surfaceDark`, and
   `--on-dark` from either — so a record stating only `canvas` and `primary` still left
   thirteen tokens on the reference's values.

2. **Derive in the RENDERER, not only in the generator.** This is the mechanism that repairs
   what is already in the database. A generator fix corrects the next record; the partial
   records already stored keep painting another company until somebody reseeds them, and
   nobody schedules that. One live tenant went from 13 emitted colour tokens to 25 by a
   change in the renderer's variable mapping and nothing the generator did.

   **The schema-refusal version comes last, not first.** An earlier version of this file
   called "make the schema refuse a partial record" the only version that cannot regress. It
   is the version that takes production down: the renderer re-validates every record on the
   way *out* of the database, every stored themed record is partial (that is the finding),
   and tightening the schema 404s all of them the moment it deploys — before any reseed. On a
   platform where the contract file is vendored into the renderer and hash-gated by the build,
   it is also a two-repo change that fails the build on one side until the other lands. The
   order is: derive in the renderer → reseed every stored record → *then* make the schema
   refuse a partial palette, in both repos, in one change.

## A state pair is derived in ONE direction

`hover` and `pressed` are a sequence, not two independent colours. The reference walks
`#D72229 → #B91D23 → #9E1318` — the accent darkened, then darkened again — and on a dark
canvas the same gesture has to go the other way or "pressed" reads as "disabled".

Deriving each of them from the canvas independently produced a real defect: a brand's own
*stated* `#D14A1E` hover (darker) beside a *derived* `#FF7E4E` pressed (lighter), so the
button got darker on hover and lighter on press. **A brand that states one of the pair
decides the direction of the other.** Read the direction off whichever the record gives you;
fall back to the canvas only when it gives you neither.

## `colorScheme` is DERIVED from the canvas, not added as a twenty-sixth token

`color-scheme: light` hard-coded in the stylesheet is one line and it is wrong on every dark
record. The browser-painted surfaces — scrollbars, form controls, the pre-paint canvas — stay
light on a near-black portal.

It is tempting to add it to the contract. Don't: it is not a colour the record chooses, it is a
*consequence* of the canvas the record already states, and a twenty-sixth token is a token
nobody remembers to set. Compute it from the canvas's relative luminance in the same place the
rest of the palette is derived.

> **And then check that something reads it, the same way you would a colour.** The first
> version emitted `color-scheme: var(--scheme)` *inside* the `:root` block — where a
> token-consumed gate that reads consumption from the rules **after** `:root` cannot see it,
> and reported `--scheme is declared but nothing, directly or indirectly, reads it`. It has to
> be a rule (`html{color-scheme:var(--scheme)}`). A token read only by the block that declares
> it is the unread-token defect wearing a disguise.
