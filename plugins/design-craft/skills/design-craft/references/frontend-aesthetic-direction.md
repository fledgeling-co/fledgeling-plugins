# Frontend Aesthetic Direction: Commit to a Look When No Brand Exists

Establish an aesthetic direction (typography, color, density, mood, component style) when the user is designing without an existing brand or design system. Use this **before** drawing hi-fi work in a greenfield context.

**Mocking a hi-fi design from scratch without committing to an aesthetic is the fastest path to AI-template aesthetics.** Without a deliberate direction, you default to safe, generic, indistinct designs. Pick a direction first, then design within it.

## Phase 1: Confirm there's truly no existing context

Before committing to a new direction, double-check that no existing context applies:

- No brand guide
- No existing app or product to match
- No reference site the user explicitly wants to mimic
- No partial design system in the codebase

If any of these exist, **stop and use them** instead. Aesthetic direction is for true greenfield. If the user has a brand and forgot to attach it, ask for it before proceeding.

Also check for a **local design-system library** (on this user's machine: `~/Dev/open-design/design-systems/` — 150+ portable `DESIGN.md` systems). Two uses here: a brief that names or clearly evokes a brand ("something like Linear", "Stripe-quality") gets the actual system as context rather than your memory of it; and when proposing the 4 directions below, a well-authored library system (atelier-zero, kami, a strong product system) can *be* one of the candidates, tokens and all. Skim before trusting — entries with generic default palettes are boilerplate, not direction.

## Phase 2: Discover the intent

Ask the user (or confirm if they've stated):

- **Three adjectives** that describe the desired feel. ("Editorial / serious / spacious" vs "Playful / bold / loud" vs "Minimal / quiet / utilitarian.")
- **Audience.** B2B engineers respond to different aesthetics than consumer or editorial audiences.
- **Industry context.** SaaS, consumer, editorial, fintech, healthcare, government — each has its own reasonable defaults.
- **Reference designs they admire.** Specific brands, sites, or apps. Ask what specifically they admire — the type, the spacing, the color, the tone, the density?
- **Off-limits.** What aesthetics or tropes does the user explicitly want to avoid?

**Mine the subject before consulting the map.** Pin down one concrete subject, its audience, and the surface's single job (state your choice if the brief leaves it open). The subject's own world — its materials, instruments, artifacts, and vernacular — is where non-template choices come from: a coffee brand suggests crema tones and kraft textures; a synth plugin suggests panel silkscreen type and patch-cable color; a climbing gym suggests chalk, rope weaves, topo lines. Subject-mining tells you *which* family to pick and how to remix it; the range map alone produces family-generic output. Anything you remember about this user's prior designs or preferences counts as context too.

**Widen the world, then trawl shipped UI.** On a free aesthetic axis, run `references/aesthetic-ideation.md` first — it invokes `trawl:trawl` so the seven candidates are not one model sampling itself. Then trawl real shipped UI (`references/mobbin-trawl.md`). Subject-mining and ideation supply the *world*; Mobbin supplies the *mechanics* — how dense a real screen of this type is, what surfaces exist that a spec never lists, which parts shipped products leave deliberately plain. Two or three Mobbin searches, images opened, a took/left ledger that includes the ideation lines. A direction built on only one of those sources is half-derived: a beautiful world at the wrong density, or a competent screen that could belong to anyone.

**Candidate sources.** The range map below remains the in-file list. `references/aesthetic-worlds.md` is the wider anchored catalogue (24 worlds in five groups, plus premium-consumer palette rotations). After a shortlist exists, load at most two files from `references/aesthetic-worlds/`. `references/current-moves.md` is the dated 2026 permission list; read a row's strength and status before treating it as current. Pull candidates from at least two groups of the worlds table, not from one row of the range map three times. Consecutive greenfield commissions, including across sessions via `references/diversity-ledger.md`, may not share a winning family, display face, topology, signature, or palette family unless product truth or an explicit request overrides it.

### Name the rut, then derive past it

Two things are ruled out before you generate a single candidate: **the page this category always ships**, and **its predictable opposite**. Write both down. "Fintech → navy and gold" is the first; "fintech, but not navy → terminal dark" is the second, and it is exactly as reflexive. Neither goes on the candidate list. If the brief paints its own picture — a product name, a titled artifact, a governing metaphor — its literal reading joins the rut: spend at most one candidate on it and derive the rest from elsewhere in the audience's world.

Then list **seven concrete visual systems, artifacts, places, or rituals the audience knows by heart**, each with one line on why it resonates and can carry the product's mechanism. Two rules keep the list honest:

- **The audience's world includes its graphic and screen traditions, not only its physical objects** — the notation, publications, identity programs, data graphics, and interfaces it reads daily. A nameable abstract system (a school of poster design, a documentation standard, a scoring notation) is as concrete a candidate as any object. Ask both: what would this thing look like as a physical object, and what did its world look like before the web?
- **Span at least three material families.** Near-duplicates count once. When more than three of the seven share one material family, the derivation stopped at the subject's most obvious artifact — dig further before proceeding.

**Ask for the seven as a distribution, not as a best answer.** The measured form of this step is *verbalized sampling*: rather than asking yourself for the strongest candidate, enumerate the candidates **with a rough probability on each** — how likely is this the answer any run on this brief would give — and then choose from the low-probability tail. Measured at **1.6–2.1× the diversity of direct prompting** (ICML 2026), with one report putting it at recovering up to 66.8% of a model's latent range; a raised temperature does not substitute, and neither does asking to "be creative". Writing the probabilities down is what makes the tail visible: the candidate you would have led with is the one carrying the highest number.

**Then don't build your top-ranked candidate by default.** This one is *this skill's house rule rather than a published finding* — the reviewed literature supports critique-and-revise and deliberate divergence, and has nothing directly on discard-the-top-pick (`references/evidence.md` §4). It stays because its mechanism is nameable: rank the seven by resonance, and treat the top one with suspicion: it is what *every* run on this brief would produce, which is the definition of the outcome this whole procedure exists to avoid. Build a lower-ranked candidate unless the top one is genuinely forced by product truth or an explicit brief constraint — and say in the direction block which rank you took and why. Taste is never grounds for climbing back to the top of the list; a factual failure (the candidate can't carry the mechanism, the assets don't exist, the claim isn't true) is.

Set five dials (1–10) from the brief and say them out loud — they calibrate everything downstream. Three already lived here; two more, from garden-skills' calibration file, catch the cases those three miss:

| Dial | What it changes | Quiet | Loud |
|---|---|---|---|
| **VARIANCE** | How far layout departs from category convention | Stable grid, familiar nav | Off-grid moments, multiple layout families |
| **MOTION** | How much meaning is carried through time | State feedback only | Pin, scrub, spatial storytelling |
| **DENSITY** | Useful information per viewport, not clutter | One idea, gallery pauses | Cockpit; needs grouping and disclosure |
| **ASSET DEPENDENCE** | Whether the page fails without real imagery or identity assets | Type and structure can carry it | Inventory assets before layout; no CSS stand-in |
| **BRAND FIDELITY** | How strictly an incumbent identity must survive | Exploratory | Extension-level; new work looks native |

A Linear-style dev tool reads about 5 / 3 / 5 / 6 / 6. A public-sector portal 3 / 2 / 6 / 3 / 9. A festival site 9 / 8 / 4 / 8 / 4. Changing a dial has to change the plan; a score with no consequence is decoration, drop it.

If the brief reads as an established design system (Material, Fluent, Carbon, Polaris, Primer, GOV.UK, USWDS, Atlassian, Bootstrap, Radix Themes, shadcn), **install the official package rather than hand-faking its CSS** — one system per project. shadcn is owned source: customise radii, colour, type before shipping, never the default kit. Aesthetics like glassmorphism or brutalism have no official package, so build them honestly and label approximations. Apple Liquid Glass is Apple-platform only; a `backdrop-filter` web version is an approximation and is labelled as one.

### Presenting the round

If the user is unsure, present **one direction fully committed** — its world, first viewport, visitor path, signature moment, and honest risk — alongside 2–3 named alternates from different rows of the range map. **Each alternate gets a real case and its main tradeoff**, in a sentence that a reader could act on: a set where only your favourite has an argument behind it is a rigged vote wearing a choice's clothes, and the user can feel it. Lead with the commitment rather than a flat lineup: a neutral menu of your own ranked candidates invites the safest card, which is the failure mode this procedure is built against. The alternates must not share a palette family (four takes on warm-cream is one direction, not four), and at least one must be deliberately off-distribution.

**Always include the standing exit: the category standard, played straight.** One quiet, permanent option — the conventional answer executed at full fidelity. It is the user's door, never your recommendation: never argue for it, never weigh it against the committed direction, never let it soften the alternates. When the user takes it (through the option, through a request for something safer, or in plain words asking for the familiar or competitor-like path), convention *becomes* the commitment: ask once for two or three products this should sit alongside, make their craft level the bar, and execute the canon at full fidelity — no irony, no smuggled quirk.

Ship each direction as a complete drop-in `:root` block (5–6 color tokens + font stacks) plus 4–6 "posture" bullets (border weight, radius, accent budget, motion mode, what to avoid) — once chosen, that block is binding. (The `AskUserQuestion` tool's `preview` field is ideal here — show each direction as a small swatch/type sample so the user compares them side by side.)

### The range map — named aesthetic families

Real variety is picked from a map, not hoped for. Each family names its tokens so a direction is buildable, not a vibe. **Never converge on the same family across consecutive projects or variation rounds** — repetition across generations is how a house style calcifies into a template.

| Family | Type | Color & surface | Signature moves |
|---|---|---|---|
| **Swiss / International** | One grotesk (Helvetica Now, Suisse), tight scale | Near-white, near-black, ONE red or blue | Hard grid, exposed structure, no radius, no shadow |
| **Editorial / literary** | Modern serif display + humanist sans | Toned paper, ink, one warm accent | Drop caps, pull quotes, column rhythm, generous leading |
| **Brutalist / raw** | Mono or grotesk, oversized | Unmixed primaries or b/w, visible borders | Default-looking controls, hard shadows (4px offset, no blur), marquees |
| **Neo-grotesque product** (Linear/Vercel) | Inter-class sans but tracked and weighted deliberately | Dark or light neutral ramp, one electric accent | Subtle borders, glass panels, glow accents, dense-calm layouts |
| **Luxury / fashion** | High-contrast serif (Canela, Didot-class), airy caps | Cream/black or monochrome + metallic restraint | Huge whitespace, small centered nav, full-bleed photography |
| **Playful / toy** | Rounded sans (Nunito-class), chunky weights | Saturated pastels, 2–3 hues | Pill everything, springy motion, sticker shadows |
| **Terminal / hacker** | Mono everywhere | Black/green or black/amber, scanline grain | Box-drawing chars, blinking cursor, log aesthetics |
| **Retro-futurist / Y2K** | Extended/condensed pairings, chrome effects | Gradients earned: chrome, iridescent mesh | Outlines, starbursts, pixel dither, marquee energy |
| **Organic / soft** | Low-contrast humanist faces | Earth tones, blurred mesh backgrounds | Blob masks, grain, hand-feel spacing irregularity |
| **Industrial / utilitarian** | DIN/Univers-class, all-caps labels | Concrete neutrals, safety-orange accent | Rulers, specs, stencils, exposed metadata (ISO-style) |

These are starting points to remix, not costumes: pull one family's type with another's surface treatment when the brief supports it. For named anchors and a spread across material families, read `references/aesthetic-worlds.md` — load the matching group, not the whole table. Match implementation complexity to the vision — maximalism needs elaborate effects executed fully; minimalism needs restraint and precision. Half-committed is the only wrong dose.

Two rows carry a warning: **Neo-grotesque product (dark neutral + one electric/acid accent)** and **Editorial/literary** are the looks current models reach for unprompted on dev-tool and creative briefs respectively — choosing them requires the same stated reason the warm-editorial combination does (see `ai-slop-check.md` §9's three-look family).

## Phase 3: Commit to the system — make it concrete

Vocalize your decisions as a comment block at the top of the file the user can see. **Be specific.** Vague aesthetic statements ("modern and clean") produce generic designs.

Commit on each axis:

### Typography

Pick **specific** fonts (not "a sans-serif"):

- **Headline font** — name, weight, size scale
- **Body font** — name (often the same family), weight, size scale
- **Mono font** (if needed for code) — name
- **Utility face** (optional) — for captions, data tables, and metadata on data-heavy surfaces; often the mono doing double duty

Avoid the overused defaults — Inter, Roboto, Arial, bare system stacks, and the silent serif-display defaults (Fraunces, Playfair Display, Georgia-as-display). Add **Space Grotesk** to that list: it is the face this model reaches for unprompted when told to "pick something distinctive", which makes it the opposite of distinctive. The tell for any of them is that you arrived at the name before you had a reason — a font chosen because the direction called for it can be defended in one sentence ("a typewriter mono, because the product is a log reader"); a font chosen by gravity can't. Pick something with intent: a humanist sans (Söhne, Suisse), a modern serif (Tiempos, GT Sectra), an editorial classic (Tiempos Headline, Canela), a typewriter mono (JetBrains Mono, IBM Plex Mono), a geometric sans (Visby), depending on the mood.

If the user might not have access to a paid foundry, suggest the closest free alternative (e.g. "Inter is overused, but Söhne is paid — try Söhne for production, or Albert Sans / Geist as free alternatives").

Commit to a type scale (sizes, weights, line heights). 1–2 families maximum. **When pairing two faces, pair on a contrast axis** — serif + sans, geometric + humanist, display + text — or use one family in multiple weights. Never pair similar-but-not-identical faces (two geometric sans, two humanist sans): the near-match reads as a mistake, not a choice.

### Color

**First pick a strategy — the commitment axis** (how much of the surface color carries):

- **Restrained** — tinted neutrals + one accent ≤10% of pixels. The product-UI default, and the floor whenever the visitor came to *operate* or *read*.
- **Committed** — one saturated color carries 30–60% of the surface. Identity-driven pages.
- **Full palette** — 3–4 named color roles, each used deliberately. Campaigns, data-viz.
- **Drenched** — the surface *is* the color. Heroes and campaign pages.

Persuade and Experience surfaces have permission for the bolder strategies; take it when the brief allows. Choosing Restrained is fine; *defaulting* to it unexamined is how timid, evenly-distributed palettes happen. Colour commits at page scale — fields that own whole regions, not accents scattered over a neutral ground. State the strategy in the direction block.

**Theme (dark vs light) is never a default.** Not dark "because tools look cool dark," not light "to be safe." Before choosing, write one sentence of physical scene: who uses this, where, under what ambient light, in what mood. If the sentence doesn't force the answer, it isn't concrete enough — add detail until it does.

Then pick a tone:

- **Warm** — cream, beige, gold, terracotta, rust
- **Cool** — gray, slate, ice, blue
- **Neutral** — concrete, charcoal, off-white

**The warm-editorial combination (cream background + serif display + terracotta/amber accent) is the current default-model look.** Choose it only when the brief is genuinely editorial, hospitality, or portfolio — and say so explicitly in the direction block. If the direction drifts there without a stated reason, pick again. Its successor default is already visible: **beige/cream + brass/clay/oxblood + espresso** appears unprompted on every cookware/wellness/artisan brief. When a brief pulls that way, deliberately rotate: cold luxury (silver/chrome/smoke), deep forest + bone + amber, black-and-tan, cobalt + cream, terracotta + slate, or monochrome + one saturated pop.

**The rendition self-check — run it after committing, before writing a line of CSS.** Reread your own OWN-WORLD block. If it says cream, paper, parchment, ivory, sand, or lamplight for a Persuade surface the brief did not pin, the *rendition* failed even though the direction may be sound: rework it from the world's saturated materials first. This is the specific prior that reasserts itself on warm, bookish, family, and child-facing subjects, and a warm subject is never a licence for it — book cloth, thread, jackets, endpapers, and shelf ephemera span the whole saturated spectrum, and cream paper is the smallest corner of that world. Treat the first palette that arrives on those briefs as already spent.

Then pick:

- **Primary brand color** (with light and dark variants)
- **One accent** (optional — a single accent color is often enough)
- **Semantic colors** (success / warning / error / info)
- **Neutral scale** (5–10 steps from near-white to near-black, on the chosen tone)

Use `oklch()` to keep harmony if the palette is from scratch:

```css
--brand-primary: oklch(55% 0.18 250);
--brand-accent:  oklch(70% 0.15 30);
```

**Subtly tone whites and blacks.** Pure `#FFFFFF` and `#000000` is harsh. Match the chosen tone (e.g. `#FAFAFA` warm-neutral, `#1A1A1A` near-black).

**Write the accent budget as enforceable rules, not adjectives.** "Use sparingly" is unenforceable; a frequency, a role ban, and a forbidden value are checkable at review. The pattern (from magazine-grade systems):

- *Frequency:* "one accent moment per viewport-and-a-half — if two CTAs are accent-filled, the section markers drop to muted ink."
- *Role bans:* "the secondary accent is never a CTA — it is jewelry (a single ★, a highlighted stat ring, one annotation dot)."
- *Forbidden values:* "pure white only as inverse text inside the dark panel, never on the paper ground; nothing darker than the committed ink."

Two or three rules of this shape make the direction self-policing — a reviewer (or the swap test) can catch violations mechanically.

### Density

Pick a spacing scale (4px or 8px base) and commit to a density:

- **Tight** — compact dashboards, dense data UIs (smaller padding)
- **Normal** — typical product UI (comfortable padding)
- **Loose** — editorial, marketing, premium feel (generous padding, lots of whitespace)

The density choice is felt as much as seen — it's a major part of the aesthetic.

### Border radius and shadow

- **Sharp** (radius 0–2px) — utilitarian, brutalist, editorial
- **Soft** (radius 4–8px) — typical modern product
- **Pill / fully-rounded** (radius 9999px on buttons; 12–16px on cards) — playful, friendly, consumer

Shadows similarly: sharp / soft / none. Commit to one elevation system, not a mix.

### Component style

- **Filled** — solid backgrounds, primary actions saturated
- **Ghost** — no fill, only border or just text
- **Outlined** — bordered, transparent fill
- **Elevated** — cards float on shadow

Pick a default, with secondary styles for hierarchy.

### Imagery and iconography

- **Photography** — real photos (Unsplash, brand commission, stock)
- **Illustration** — professional library or commission
- **Icons** — Feather, Material, Phosphor, Heroicons, or a paid set
- **Honest placeholders** when assets aren't available

Avoid hand-drawn SVG illustrations.

### Motion

- **Quiet** — minimal motion, transitions only on state changes (200ms ease)
- **Expressive** — entrance animations, scroll-driven reveals, view transitions
- **Playful** — overshoots, springs, micro-interactions on hover

Commit to one mode; mixed motion modes feel unintentional. Whatever the mode, spend the budget in one place: **a single well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions.** Implement per `motion-design.md` (tokens, easing curves, choreography).

### Depth and texture

- **Flat** — borders and background contrast only
- **Elevated** — a tokenized shadow/elevation system
- **Textured** — grain, mesh gradients, glass, image treatments
- **Dimensional** — CSS 3D moments or a WebGL centerpiece

Commit alongside the motion mode; implement per `depth-and-3d.md` (the technique ladder, budgets, and fallbacks). Texture is the cheapest "designed, not generated" signal — and the easiest to overdose.

### Signature

Name **the single element this design will be remembered by** — the one place the boldness budget is spent, derived from the subject (Phase 2), while everything around it stays quiet and disciplined. A signature is concrete ("the hero's headline set in the subject's stencil lettering, drawn on scroll"), not a vibe ("memorable typography"). This is the plan-time version of the 80/20 soul rule in `ai-slop-check.md` — commit to the memorable element before writing code rather than hoping one emerges and checking at review.

## Phase 3.5: The swap test — a genericness gate

Before documenting, run the counterfactual: imagine a neighboring brief — a different product in the same category — and ask whether your committed direction would fit it unchanged. Any axis that transfers untouched is a default, not a choice: revise that axis and say what you changed and why. (The anti-convergence rule above only works across sessions; the swap test works inside this one.)

Then run it **one tier deeper**: could someone guess your chosen family from the category *plus your anti-references* alone? "Fintech, but not navy-and-gold → terminal dark" and "AI workflow tool, but not SaaS-cream → editorial-typographic" are second-order reflexes — the predictable alternative is still a reflex. Rework until neither the first-order nor the second-order guess lands.

## Phase 4: Write the direction contract into the file

The chosen direction goes into the artifact as a visible block — a comment at the top of the source **and** a "design system summary" section in the rendered output. Like a junior designer showing their thinking to their manager.

Write it as a **contract in five named blocks**, ≤150 words total, placed where it survives the build (an HTML comment in the emitted markup, as the first child of `<body>` in the root layout — not only in templating frontmatter, and never inside a slotted child component, since some compilers strip a slot's leading comment). After the first production build, grep the built output for it: a contract the build erased is a contract nobody can audit.

- **THESIS** — the one idea this surface owns, and the category-default arrangement it refuses.
- **OWN-WORLD** — the palette and component language, specific enough to be recognizable with all content removed. This is where the token block lives.
- **STORY** — what the visitor understands, believes, and does.
- **FIRST VIEWPORT** — the exact composition: what is where, at what scale, and where the primary action sits.
- **FORM** — the candidate you took, its rank on your seven-item list, and why you took that one.

**Once written, the direction is settled, and a settled decision stays settled.** Do not re-open the aesthetic on a later turn, do not re-offer the alternates, and do not re-ask a question this round answered — a second direction round on a brief the user already decided reads as not having listened, and it costs the build every unit already drafted against the first answer. The contract is the record: read it rather than re-litigating it. (The exception is a genuine signal change — the user's own feedback pointing somewhere else — which `discovery-questions.md` Phase 7 handles, and which is a *correction*, never a re-ask.)

Close with a sixth line — **FINISH** — naming the run's exit condition, verbatim: *"unreviewed is unfinished; this build ends with the review, the verdict, and the open items declared."* The contract tops the artifact you reopen on every edit, and it is the one reminder that survives a long build: a page that looks complete with FINISH undischarged is not done, it's abandoned at the finish line.

**If a block reads like a mood, the direction isn't decided yet.** "Warm and confident" is not an OWN-WORLD; `#2B1B12` ground, ochre plate, 1px hairlines, no radius above 4px, and a stencil display face is. The critique gate audits the render against these blocks promise by promise (`unit-critique-gate.md`), so a block that can't be checked is a block that won't be.

```
/* Direction contract
 * THESIS: A field notebook for climbers — refuses the hero-photo-plus-gradient
 *   outdoor-brand page and the terminal-dark "tech" alternative.
 * OWN-WORLD: Topo-map ground #1C2119, chalk #EDE8DC, one route-marker orange
 *   #D2521E. Tiempos Headline + JetBrains Mono for grades and metadata.
 *   Hairline 1px rules, radius 2px, no shadow. Contour linework as the motif.
 * STORY: A climber sees their own logbook, believes the grades are honest,
 *   and books a session.
 * FIRST VIEWPORT: Full-bleed contour field, headline knocked out of it at 5rem,
 *   grade ladder running the left gutter, one filled CTA at lower-left.
 * FORM: Candidate 4 of 7 (topo survey sheet) — candidate 1 was the
 *   climbing-photo page every run ships.
 * FINISH: unreviewed is unfinished; this build ends with the review, the
 *   verdict, and the open items declared.
 */
```

## Phase 4.5: Comp before build (when an image backend exists)

When image generation is available (`generate-images.md` resolves the backend), **visualize the committed direction before building it.** This step produces the most compositional and ambitious work, and skipping it is how a strong direction becomes a flat page with the right colours.

- **Three comps, not one.** One comp invites rubber-stamping; the spread between three is what surfaces the composition worth building. Render three high-fidelity north-star comps of the requested surface at its own viewport (portrait at device size for a mobile-first surface, desktop landscape otherwise) and save them where they survive the session.
- **A comp is a designed surface, not a picture of the subject.** Lead the prompt with the surface's own structure — the regions this design actually has, named in order with their scale relationships — then the world's atmosphere. A prompt that leads with atmosphere returns a vignette: the model paints the fish market instead of the fish market's website. Self-check every render: if it could hang as a poster, regenerate with the layout scaffold stated more literally.
- **The comps test composition, not identity.** The world is already committed — keep palette, type direction, material language, and motion grammar fixed and vary only what an image can resolve: topology, sequence, density, hierarchy, focal composition.
- **One approval point.** Show all three, ask what carries forward and what feels false, then stop and wait. Don't start code until the user approves or explicitly delegates the choice; a delegated pick is recorded exactly as an approval is, and disclosed in your first reply rather than your last.
- **Then inventory the approved comp in writing** before building: its component grammar, corner language, line weights, elevation treatment, type ramp, navigation items, headline levels and their scale relationships, signature geometry, and each section's arrangement and density — plus an implementation medium per region (`generate-images.md`, "The medium gate"). Everything the comp doesn't show gets built from this record; without it the fallback is the stock kit of square boxes, 1px grids, and bento cells. An element never written down is the element the build silently drops, and the 150-word contract can't carry this list.

**Building against an approved comp runs in two phases.** Phase one is *reproduction*: rebuild the comp at its own breakpoint until a screenshot at the comp's dimensions overlaps it near-exactly — materials, components, elevation, assets, and implied design language included. Three concessions exist and no others: fonts (the closest obtainable face), icons (exact match unless the user chose a library), and genuine defects in the comp. Set the screenshot beside the freshly reopened comp image at identical dimensions after every region, never beside your memory of it — models systematically believe their HTML/CSS/SVG recreation succeeded when it didn't. When a region keeps losing that comparison, stop recreating it in code and produce it as a rendered asset. Only when reproduction holds does phase two begin: motion, interactivity, then responsiveness.

**The comp outranks every written record of it.** When your inventory or brief committed to less than the comp shows — a softer texture, a sparser field, a sculpted plate reduced to flat CSS — correct the record *upward* to the comp. Qualifiers like "subtle", "restrained", and "low-contrast", and counts rounded down to a comfortable fraction, are how approved materials die between approval and build.

## Phase 5: Apply, then test

Build a small surface (a hero, a card, a button group) using the direction. Show it to the user early. Ask: "Does this read as [the three adjectives you committed to]?" If no — or if the user pushes back on a specific axis — revise the direction before going broader. A direction that works at small scale holds up across a full design; one that doesn't will get worse, not better.

## Phase 6: Use the direction consistently

Every subsequent design should reference the direction's tokens, not invent new values. If a new design needs a value the direction doesn't define, **add it to the direction first**, then use it. Don't introduce one-off values inline. Eventually the direction is mature enough to extract into a tokens file — that's when `design-system-extract` becomes useful.

## Phase 7: Summarize

Report: the three adjectives; the committed type, color, density, radius, component, imagery, and motion choices; any axes the user should review before you go broader; the first surface built using the direction (link to the file).
