# AI Slop Check: Detect and Fix Generic AI Aesthetics

Review the current design for the visual tropes that signal "AI-generated template." Fix any found.

These patterns are rejected because they read as default, not intentional. A design that looks like a hundred other AI outputs is a design that fails to look like the user's design.

Each rule below is **positive-first**: lead with the default to reach for, then list the patterns to detect and replace. The order matters — at write-time you should be biased toward the default; at review-time, scan for the detection patterns.

## Phase 1: Identify the surface to review

Find what to review, in order: (1) the HTML/CSS file the user just edited or asked about; (2) files modified in the current session; (3) if unclear, ask which file or component. Read the file. Skim referenced CSS, tokens, and component files so you can resolve actual values.

## Phase 1b: Measure specification before you judge taste

The tell-list below is judgement, and judgement is where two reviewers disagree.
Six numbers are not, and they separated two artifacts built from **one prompt, one
source document and one shared `DESIGN.md`** — a pair that returned byte-identical
clean results from every deterministic gate then in place. **Measured Aug 2026, one
pair, on a Claude model; `n=1` — treat the numbers as one honest data point about
the direction of each metric, not as thresholds.** (`references/evidence.md` records
which numbers in this skill are measurements and which are standards.)

| Metric | designed | generic | how to read it |
|---|---|---|---|
| largest type size | 132px | 76px | no display tier means the top rung of the ramp is missing, and every level below it compresses |
| distinct type sizes | 19 | 13 | a real ramp has rungs; a short list means sizes were picked per-component |
| hue families (non-neutral) | 1 | 3 | count across the whole artifact — the second hue always arrives as a status chip |
| accent marks per surface, mean / max | 1.8 / 3 | 3.7 / 7 | count marks in the render, not selectors in the CSS |
| external resource requests | 0 | 3 | a self-contained artifact that isn't |
| surfaces built as an identical card row | 0 of 12 | 7 of 12 | module monotony, the strongest layout tell |

Run these first. They cost seconds, they do not vary between reviewers, and a
failure on any of them predicts a long list below. **Hue families must be
counted in the render, never from source**: a well-tokenised file writes
`color: var(--success)` and that hex appears once in `:root` whether the token is
used on forty chips or none, so a static count under-reports on exactly the code
most worth reviewing. `deck-craft/scripts/deck-preflight.js` reports `hueFamilies`
from computed styles; the same walk works on any page. **Count marks in the rendered
capture rather than in the stylesheet** — a filled bar, a rule, a progress track
and a dot each read as an accent object to the eye and as nothing to a selector
scan, so an automated count under-reports by exactly the amount that matters.

## Phase 2: Single-pass review for AI tropes

Walk through the design and apply each rule below. Single agent — these patterns are obvious enough that parallel dispatch is overkill.

Report every detection, including uncertain or low-severity ones, with a confidence and severity estimate. Your job at this stage is coverage — filtering happens when you fix (Phase 3) or when the findings are aggregated by `polish-pass`.

### 1. Gradients — flat or subtle, on-tone

**Default:** flat color from the design system, or a subtle on-tone gradient (two stops, low contrast, same hue family). Flat is almost always stronger.

**Detect & replace:** rainbow / 3+ color gradients (`linear-gradient(135deg, #FF00FF, #00FFFF, #FFFF00)` and similar); saturated purple-to-pink, orange-to-pink, or other "trendy" two-color blends on hero backgrounds, buttons, or large surfaces; gradient overlays on imagery that don't improve legibility or hierarchy.

### 2. Emoji — functional or brand-driven only

**Default:** no emoji. Reach for one only if the brand explicitly uses emoji in existing materials, the emoji is functional (a status indicator, a category marker tied to real meaning), or the user asked for them.

**Detect & remove:** emoji prepending headlines, button text, or list items where the brand doesn't use them (`🚀 Get Started`, `✅ Track progress`); repeated emoji as visual filler (`🎉🎉🎉`); emoji as bullet markers when they don't add meaning. If the layout relied on the emoji for visual weight, replace with a real icon from an established system (Feather, Material, Phosphor, Heroicons) or improve the typographic hierarchy.

### 3. Cards — separate with shadow, thin border, or background

**Default:** distinguish cards with a subtle shadow, a thin all-around border, or pure background separation. Reserve `border-left: 4px solid` for actual semantic emphasis (callouts, alerts, status indicators).

**Detect & replace** the exact pattern:

```css
.card { border-radius: 12px; border-left: 4px solid #...; }
```

…used as the *default* card or container style across the design. This combination is so overused it reads as "default SaaS template." Keep the left border only if it's purposeful (a callout, an alert, a status indicator) and used for that meaning specifically, or it's coming from an existing design system you're matching.

**Three more card tells, all bans as defaults:**

- **The ghost card** — `border: 1px solid` *plus* a soft wide shadow (blur ≥16px) on the same element as decoration. Pick **one elevation language per card** — border, *or* a defined shadow at ≤8px blur, *or* a background shift — stacking two or three of them on one element is the same failure at higher volume.
- **Over-rounding** — `border-radius` ≥24px on cards, sections, or inputs. Cards top out at 12–16px; full-pill is for tags and buttons only.
- **Nested cards** — a bordered/shadowed card inside another card is always wrong; flatten the inner one to plain content or a background tint. More broadly, cards are the lazy answer: reach for them only when they're genuinely the best affordance, not as the default way to group anything.

### 4. Imagery — real, licensed, or honest placeholder

**Default, in order of preference:** real photography (Unsplash, brand assets); professional illustration (icon library or commissioned); honest placeholder — striped background with monospace label like `product shot (1200×800)`. A placeholder is better than a bad illustration — it signals "asset needed" without pretending to be the real thing.

**Detect & replace:** custom SVG illustrations of people, scenes, abstract concepts not drawn by a skilled illustrator; "AI-style" character illustrations (giant heads, flat-color blobs, identical posing); decorative SVG that's clearly placeholder-quality but presented as final. Code-level tells for the "sketchy SVG" variant: class names like `*-sketch`, `doodle`, `wavy`; `feTurbulence`/`feDisplacementMap` "paper grain" filters; 5–30-path crude scenes depicting a tangible subject. If the scene can't be rendered with real assets, ship *no* illustration — never sketchy SVG as a fallback.

**This bans SVG imitating pictures; it never bans SVG doing geometry.** Crisp vector shape systems, diagrams with countable elements, drawn controls, animated linework, and shader-driven effects stay first-class media — that's what the medium gate in `generate-images.md` calls code territory. The line: geometry is what a session can specify exactly; a shaded, perspectived, or figure-bearing illustration is a *picture* even in line-art style, and pictures get generated or omitted.

**Imitation material is the sharpest tell in this family.** CSS bevels, embossing, stamped-metal, letterpress, or chalk effects standing in for a material the page never actually renders read as machine-made faster than any of the above. Either produce the material as a real asset or drop the material claim — a faked physical surface is worse than an honestly flat one.

### 5. Type — fonts chosen with intent

**Default:** pick a font with intent, matched to the brand's tone or the medium. With no brand to draw from, suggest 2–3 alternatives that match the design's tone (geometric, humanist, modern, classical) and let the user pick.

**Detect & question** bare use of Inter, Roboto, Arial, Fraunces, Space Grotesk, or bare system stacks (`-apple-system, sans-serif` with no actual font choice) used as silent defaults without a brand reason. Space Grotesk is the specific trap of *trying* to be distinctive — it's the face this model converges on when a brief asks for character, so its presence is evidence of gravity, not of choice. Keep them only if the brand specifies them, the user asked for them, or they're appropriate for the medium and the user has confirmed. Do not silently swap one generic for another.

**A system display face is a failure, not a fallback.** Impact, Arial Black, or the platform sans carrying the *display* voice of an own-world page means the face was never sourced. Self-host a face whose character matches the committed direction — the closest installed font is the wrong answer to a question about lettering. (Workhorse system stacks for *body and UI* on an Operate or Read surface are legitimate: see `visitor-modes.md`.)

**Two more reflexes in this family:** **monospace as a costume** for "technical" rather than for code, data, or measurement; and **unicode glyphs or emoji standing in for an icon system** — icons are drawn, from a real library or authored SVG, in one consistent stroke and weight.

**Serif discipline.** "Creative brief = serif" is itself an AI tell — reach for a serif only when the brand names one, or the aesthetic is genuinely editorial/luxury/publication and you can say why *this* serif fits *this* brand. Fraunces and Instrument Serif are banned as defaults (the two LLM-favorite display serifs). For in-headline emphasis, use italic or bold of the **same family** — never inject a lone serif word into a sans headline for "visual interest"; mixed-family emphasis reads amateur. When italic display text contains a descender (`y g j p q`), `line-height: 1` clips it — use ≥1.1 and reserve a few px below; audit every italic display word.

### 6. Color — subtly toned whites and blacks

**Default:** whites and blacks subtly toned to match the palette. Warm: `#FFFAF0` bg / `#2D2118` text. Cool: `#F5F7FA` bg / `#1F2937` text. Neutral: `#FAFAFA` bg / `#1A1A1A` text.

**Detect & replace:** exact `#FFFFFF` background paired with exact `#000000` text. The combination is harsh, cold, and reads as unfinished.

**Two readability tells in the same family:** muted-gray body or placeholder text on a tinted near-white background — the single most common AI readability failure; secondary text still needs 4.5:1, "muted" is a role, not a license. And gray text sitting on a *colored* background always looks washed out — use a darker shade of the background's own hue, or the text color at reduced opacity, never a neutral gray.

### 7. Color values — trace to a token or harmonious palette

**Default:** every color value should trace to a design token, brand variable, or `oklch()`-derived harmonious palette. If creating a palette from scratch, use `oklch()` to keep lightness and chroma consistent across hues.

**Detect & consolidate:** color values that don't trace anywhere. Five different blues across the file (`#0066CC`, `#0077DD`, `#3498DB`, `#3B82F6`, `#5B8DEF`) is a smell — colors were invented inline. More than ~12 raw hex values outside `:root` means tokens weren't honoured — consolidate into custom properties. **Weight near-misses as *more* severe than far-misses:** a value within ~5% of an existing token (a blue 3% off the brand blue, a gray almost matching the system neutral) is worse than a clearly different color — perception is non-linear (Bujack et al. 2022) and "almost right" registers as *more* wrong than "obviously different." Snap near-misses to the token; only clearly-different values get to argue they're deliberate. And treat the default Tailwind indigo family as an automatic fail when used as the accent: `#6366F1`, `#4F46E5`, `#4338CA`, `#3730A3`, `#8B5CF6`, `#7C3AED`, `#A855F7`. Indigo is the textbook AI tell; replace with the committed accent.

### 8. Spacing — snap to a 4px or 8px scale

**Default:** define spacing tokens (`--space-xs: 4px` through `--space-2xl: 64px`) and use them. Multiples of 4 or 8 feel intentional.

**Detect & replace:** off-scale values like `padding: 7px 15px`, `margin: 18px`, `gap: 13px`. They feel chaotic.

**This rule governs values *you* authored. It never applies to a matched system.** When the design is rooted in an existing codebase, brand or UI kit (SKILL.md §4), that system's resolved values are *data*: `padding: 18px 22px` lifted from `packages/ui` is correct at 18 and 22, and rounding it to 16/24 breaks the match while reporting the break as a fix. Follow tokens through to their resolved values and leave them exactly as they are — the same carve-out `redesign.md` grants colour ("a brand that is already purple stays purple") applies to spacing, radii, control heights and type sizes. Flag an off-scale value only when you cannot trace it to the incumbent system.

### 9. The editorial-warm house style — deliberate or absent

**Default:** an aesthetic direction chosen for the brief (see `frontend-aesthetic-direction.md`). The warm-editorial look is legitimate for editorial, hospitality, and portfolio work — when it traces to a brand or an explicitly committed direction.

**Detect & question** the combination, absent a brand reason: cream / warm off-white page backgrounds in the `#F4F1EA` family; serif display faces as silent defaults (Georgia, Playfair Display, Fraunces); italic word-accents in headlines; terracotta / amber accent palette.

**Detect cream by value and by name, not just by hex family.** The whole warm-neutral band — OKLCH lightness 0.84–0.97, chroma <0.06, hue 40–100 — reads as cream/sand/paper regardless of what it's called, and the token names are tells in themselves: `--paper`, `--cream`, `--sand`, `--bone`, `--linen`, `--parchment`, `--ivory`, `--wheat`. "Warm, traditional, editorial" in a brief does **not** translate to a warm-tinted near-white body background — that's the reflex. Warmth is carried by the accent, the typography, and the imagery; the body background is either a true off-white (chroma ~0, or tinted 0.005–0.015 toward the *brand's own hue*), a saturated brand color, or a darker mid-tone that's clearly the brand's.

Any one of these can be a deliberate choice. All of them together — especially on a dashboard, dev tool, fintech, healthcare, or enterprise surface — is the default-template look, today's equivalent of the purple gradient. Replace with the committed direction, or flag for the user if no direction exists.

**Its successor default: the premium-consumer palette.** For premium-consumer briefs (cookware, wellness, artisan goods, DTC home) the model now defaults to warm beige/cream backgrounds + brass/clay/oxblood accents + espresso near-black text. That palette on every premium brief makes the brand invisible. Acceptable only when the brief names those colors or the identity is genuinely vintage-craft. Otherwise rotate to a different family: **Cold Luxury** (silver-grey + chrome + smoke), **Forest** (deep green + bone + amber), **Black-and-Tan** (true off-black + warm tan, no beige), **Cobalt + Cream**, **Terracotta + Slate**, or **monochrome + one saturated pop**. Never ship the beige+brass family twice in a row.

**The other two AI-default looks — detect them the same way.** Current AI output clusters around three looks, and warm-editorial is only the first: **(2) near-black background with a single acid-green or vermilion accent** — the default for every dev-tool/startup/AI brief (the range map's "neo-grotesque product" family used without a stated reason); and **(3) the broadsheet** — hairline rules, zero border-radius, dense newspaper columns, oversized serif masthead. All three are legitimate *for some briefs*; all three are defaults rather than choices when they appear regardless of subject. **The brief's own words always win** — including when it explicitly asks for one of these looks; the rule is only: don't spend a *free* axis on a default.

**The second-order reflex check.** Avoiding the first default and landing on the *predictable alternative* is the same trap one tier deeper: "fintech but not navy → terminal-dark", "AI tool but not SaaS-cream → editorial-typographic". If someone could guess the chosen family from the category *plus* the anti-references alone, it's still a reflex — rework until neither the first-order nor the second-order guess is obvious.

### 10. Hero — one moment, max 4 text elements

**Default:** the hero is a **thesis** — open with the most characteristic thing in the subject's world, in whatever form fits it: a headline, an image, an animation, a live demo, an interactive moment. Structurally: eyebrow *or* brand strip (or neither), headline (max 2 lines desktop), subtext (≤20 words), CTAs (1 primary + at most 1 secondary). Top padding ≤6rem — more and the content floats mid-viewport and reads as a bug. A 4-line hero headline is always a font-size error, never a copy-length problem.

**Detect the template hero:** a big number with a small label, a supporting-stats row, and a gradient accent is the stock AI answer for SaaS heroes — keep it only if a metric genuinely *is* the product's thesis.

**Detect & remove** extra hero tenants: tiny taglines below CTAs, trust micro-strips, pricing teasers, feature bullet lists, social-proof avatar rows — all move to their own sections below. Logo walls live under the hero, never inside it — built from real SVG marks, logos only: no category labels under each mark (`Stripe · payments` tells the user nothing they don't know), and legible in both themes. **Where the marks come from depends on the delivery surface**: a CDN endpoint such as `https://cdn.simpleicons.org/{slug}/{hex}` works on a served page and is **blocked with no error inside a published Artifact**, where the wall ships as a row of broken images — inline the SVG paths there instead (`delivery-surfaces.md`). Styled text wordmarks in a row read as placeholder either way; a simple inline-SVG monogram is the honest answer for an invented brand.

### 11. Layout rhythm — vary the section families

**The measurable form of this trope is module monotony**, and it is invisible while
you build because each surface's grid was a reasonable local choice. Measured Aug 2026: seven
of twelve slides in one deck were the same 3-or-4-across bordered card row; the
comparison deck used stat tiles, an editorial photo split, a data table, a progress
matrix, a milestone grid, a shared-scale bar pair and a full-bleed photograph across
the same twelve. Before reaching for a card row, name what the content *is* — a
comparison, a sequence, a matrix, a single figure, a quotation — and let that choose
the module. If two consecutive surfaces would take the same module, one of them is
wrong or they are one surface.

**Default:** a page of 8 sections uses at least 4 different layout families; density alternates (one tight section, one breathing one).

**Detect & fix:** the same layout family (3-column cards, split text-image, full-width quote) appearing more than once per page; more than 2 consecutive zigzag (image-left/image-right alternating) sections — break the third with a full-width or vertical-stack section; **eyebrows over every section header** — ration to max 1 eyebrow per 3 sections (hero counts), and when in doubt drop it: the headline alone is enough; bento grids with filler — a bento has exactly as many cells as you have content for (3 items → 3 cells; an empty tile means the grid shape is wrong, reshape it); and the all-text bento — every cell white-on-white typography — reads as the boring default even when the rest of the page is good: give 2–3 cells real visual variation (an image, a tinted background, a pattern).

### 12. CTAs and nav — one label per intent

**Detect & fix:** two CTAs with the same intent under different labels ("Get in touch" + "Contact us" + "Let's talk" are all *contact*) — pick one label and reuse it everywhere on the page; CTA text that wraps at desktop (shorten to ≤3 words or widen the button — a wrapped CTA is broken, full stop); nav taller than 80px or wrapping to two lines at desktop (64–72px is the healthy default).

### 13. Content tells — decoration that screams AI

**The governing principle: structure is information.** Structural devices — numbering, eyebrows, dividers, labels, dots — must encode something true about the content, never decorate it. Numbered markers (01/02/03) are right only when the content genuinely is a sequence whose order the reader needs; a divider is right only where two things genuinely part. Test every structural device against this before consulting the ban list — the list is instances, the principle catches what the list misses.

**Detect & remove**, all banned as defaults: fake product UI built from `<div>` rectangles (fake dashboards, task lists, terminals — use a real screenshot, a generated image, or nothing); version labels as hero eyebrows (`V0.6`, `BETA`, `EARLY ACCESS`) and version footers on marketing pages (`v1.4.2 · last sync 4s ago`); section-number eyebrows (`001 · Capabilities`, `00 / INDEX`) — eyebrows name topics, they don't enumerate; decorative colored status dots on nav items, list rows, and badges (a dot only when it conveys real live state, max one per section); locale/time/weather strips ("Lisbon 14:23 · 18°C") unless the brief is genuinely about place; scroll cues ("Scroll to explore", animated mouse icons — the user knows what scrolling is); photo-credit-style captions as decoration (`Plate 03 · House archive`) — credit only real photographers; poetic section labels ("Field notes", "On our desks") — use plain functional labels or none; generic step labels ("Step 1 / Step 2 / Phase 01") — the verb is the label ("Install", "Configure", "Ship"); the middle-dot rationed to max 1 per metadata line, never the universal separator.

**Decorative-CSS tells, same treatment:** **gradient text** (`background-clip: text` over a gradient) — decorative, never meaningful; use a solid color and emphasize with weight or size. **Glow-for-emphasis** (neon box-shadows, colored outer glows on buttons/cards/headings) — shadows exist for elevation, never for attention; emphasis borrowed from a glow is emphasis the hierarchy failed to earn, so fix the hierarchy. **Zero-offset coloured halos** — a shadow needs an offset and a soft blur to read as depth; without them it's paint. **Hard offset block shadows** (`box-shadow: 4px 4px 0`) outside a world that genuinely *is* neobrutalist — the zero-blur shadow is a costume, and a direction that didn't choose it never earns it as a default. **Decorative grid-line backgrounds** (two-axis `linear-gradient(... 1px, transparent 1px)` + `background-size` overlays) — legitimate only when the surface genuinely is a canvas, map, blueprint, or measurement tool. **`repeating-linear-gradient` stripe backgrounds** on `body::before` or sections — pure generated decoration. **Image zoom-on-hover** (`transform: scale/rotate` on an `<img>` via `:hover` or a parent `group-hover`) — the image isn't the action target and the motion adds no information; if a card needs hover feedback, animate its background, border, or shadow, never the image. **The reflex modal** — a dialog for a task that needs neither interruption nor protected focus, reached for before inline or progressive disclosure was tried.

### 14. Sample data — kill the Jane Doe effect

**Default:** believable, specific, slightly messy data. Locale-appropriate realistic names (never "John Doe" / "Sarah Chan"), photo-style avatars (never the SVG egg or a user icon), organic numbers (`47.2%`, `+1 (312) 847-1928` — never `99.99%`, `50%`, `1234567`), contextual brand names that sound real (never Acme, Nexus, SmartFlow, Cloudly), concrete verbs (never Elevate, Seamless, Unleash, Revolutionize, Next-Gen). Testimonial quotes are ≤3 lines — a landing-page quote is a snippet, not the review — with real attribution: name + role (+ company), never "— Sarah".

### 15. Theme lock — one theme per page

**Default:** pick light, dark, or `prefers-color-scheme` at the page level and lock it. Background tints within the theme family are fine; a light warm-paper section sandwiched mid-scroll into a dark page reads as walking into a different website. One deliberate full theme-switch device is allowed only when the brief calls for it. If the page supports both modes, **test both before shipping** — half-themed dark mode is worse than none. And a dark theme is *designed*, not inverted: desaturated/lighter tonal variants of the palette, softer text contrast (near-white on near-black, never pure-on-pure), shadows rethought as borders or glows, and font weight eased slightly (light-on-dark renders optically heavier — a 400 body may want ~350, or letting the system's antialiasing decide) — with contrast checked separately from light mode.

### 16. Browser surfaces — themed, not defaulted

**Default:** the parts you didn't draw carry the design too. `::selection`, `caret-color`, custom scrollbars, focus rings, `text-underline-offset` / `text-decoration-thickness` on links, and `font-variant-numeric` on data all ship with browser defaults belonging to no design system.

**Detect:** a committed palette everywhere except the selection highlight (still system blue), the caret (still black), and the link underline (still the browser's default offset and thickness). This is the cheapest signal that a page was *built* rather than assembled, and the one most reliably skipped — its absence is a finding even when nothing else on the page is wrong.

### 17. Structure — the outline is the deepest tell

**Default:** the section list is written from the material, then checked against the brief — never the other way round. Sections land in an order the brief never proposed, at least one of the brief's topics is absent because the material did not support a section on it, and at least one section exists that nobody asked for. Headings are claims a reader could disagree with, not noun-phrase filing labels.

**The governing principle: a page's section list is a design decision, and it is the one nobody audits.** Every check above operates on a surface; this one operates on the skeleton underneath it, which is why it survives a complete visual pass. A page can have a committed palette, intentional type, real data and zero slop tells, and still be a template — because its sections came from the request rather than from the material.

**Detect & fix:** lay the section headings beside the brief that commissioned the page. If they are the brief's own list in the brief's own order, the structure was inherited — a six-part request that becomes six sections named after its six parts is the signature, and it looks like thoroughness. Measured Aug 2026 on two builds from one body of material, two blind judges in opposite orderings both named this as the first thing separating them, ahead of every visual difference. Same family: headings that are all noun phrases (`Process topology`, `Deployment model`, `Security posture`) — a noun phrase tells a scanner what a section is *about* but never what it *says*. A page whose headings could be reordered without anyone noticing does not have a spine.

### 18. Explainer vocabulary — the technical page's stock costume

**Default:** find the one distinction the subject actually turns on, build a component for *that*, and use it everywhere. The device should be re-drawable from the subject alone — if a reader who understood the topic could sketch it, it belongs to the topic.

**Detect & fix:** every genre has a default kit, and for technical explainers, docs sites and research write-ups it is specific enough to name — **a trio of cards each with an icon in a rounded square**, **coloured status pills** (green *Supported* / red *Blocked* / amber *Partial*), a **feature-comparison matrix**, a **numbered pipeline strip**, and a dark background with one saturated accent, usually blue. None of these is wrong; they are the default because they work. The tell is reaching for them *first*, so the page is assembled from the genre's kit rather than from its own subject. Apply the swap test to components rather than to the whole page: change the subject to something unrelated, and if the same card trio, pills and matrix would serve a database, a payments API or a CI tool with only the strings edited, the vocabulary expresses the genre and not the material. A page built on one subject-derived device repeated across every figure reads as authored; the same page built from the stock kit reads as competent and anonymous, and the difference shows up in blind comparison even when the stock version is the more polished of the two.

## Phase 3: Fix and summarize

Apply fixes directly. For decisions where multiple options are reasonable (e.g. which non-Inter font to use), pick the most defensible default and note the choice in your summary so the user can override.

**Copy self-audit before ship.** Re-read every visible string — headlines, eyebrows, buttons, captions, alt text, footer. Flag and rewrite anything grammatically broken, with unclear referents, or that reads like an LLM trying to sound thoughtful (forced metaphors, mock-poetic micro-meta, fake-craftsman humility, dash-heavy sentence rhythm — the typesetting rules govern which dash character to use, not how often to reach for one). If unsure whether a string makes sense, replace it with a plain functional sentence — AI-cute copy is worse than boring copy.

**The 80/20 soul rule.** Slop removal isn't the same as soul. Aim for ~80% proven patterns + ~20% distinctive choice: one bold visual move, voice in the microcopy ("Start tracking" beats "Get started"), one memorable micro-interaction, one detail only someone who used the product would add. The screenshot test: if someone outside the project can look at a screenshot and say which product it is, the design has soul; if not, you shipped a template.

When done, summarize: tropes found by category; fixes applied; open questions for the user (font choice, asset replacement, etc.).
