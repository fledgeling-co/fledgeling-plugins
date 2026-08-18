# Designing a surface that will be driven by data

A page whose content, theme and motion come from a database is not a page with variables in it.
It is a **vocabulary plus a renderer**, and the design decisions move accordingly: you are
choosing what can be expressed, not what one instance looks like.

This is now the normal shape for anything served to many tenants — one deployment, N brands. The
failure modes are specific and none of them are visible in a single instance.

## Design the vocabulary, then design one instance to prove it

Work in this order. The reverse order produces a system that can express exactly one page.

1. **Enumerate the section kinds.** Take them from a real surface you have already designed, not
   from imagination. Every kind is a named component with its own props.
2. **Enumerate the token set.** Colours, type, radii, elevation, motion, container measures. This
   is the entire vocabulary a brand gets — anything not in it cannot vary between tenants.
3. **Enumerate the motion presets.** Named, not authored. `reveal`, `parallax`, `countUp`,
   `lineDraw`, `railDrift`, a WebGL preset by name. A tenant selects; it does not supply code.
4. *Then* author one instance at full fidelity and prove the vocabulary carries it.

If step 4 needs something steps 1–3 do not have, the vocabulary is wrong — extend it deliberately
rather than special-casing the instance.

## The tokens most systems forget, and what they cost

**An on-dark accent.** A brand colour chosen against white will usually fail AA on a dark band.
Measured Aug 2026 on a real build: `#D72229` on `#2E2B2B` is **2.77:1** against a 4.5 floor, and it landed
on the hero headline, both hero CTAs, the running ticker and the footer's only signup button —
35 failing nodes on one page, the most-repeated failure on the site. A multi-tenant theme must
carry `primaryOnDark` as its own token, because you cannot compute it per tenant at render time
and you cannot ask each brand to have thought of it.

**An on-LIGHT accent, which is the same token and almost nobody writes it.** The dark-band
variant gets written because the failure is obvious. The light-ground one does not, because the
*first* tenant's accent usually clears AA on paper by luck and so the gap has no instance to
appear on. Measured Aug 2026 on tenant two, whose `#E65400` is its real, correctly-extracted brand orange:
**3.37:1** as a 13px eyebrow on its own sunken band, **3.72:1** as the current-page nav link on
white, and **3.72:1** again under white ink on the header button and the brand monogram. Four
serious violations, on a brand whose accent is right.

(`accessibility-audit.md` checklist 1 owns the role-split derivation and the two further incidents in this family — the token that existed and was ignored, and the `opacity` that moved a repaired colour back under the floor. This file carries the multi-tenant half.)

**The rule has to be role-aware or it rejects correct usage.** WCAG 1.4.3 asks 4.5:1 of body-size
text and 3:1 of large text (≥24px, or ≥18.66px bold) and non-text — so that orange is correct as
a fill, correct as a 72px display word, correct as a rule, and wrong as a 13px eyebrow. A blanket
4.5 floor over "the accent" is a rule that fires on the brand rather than on the defect. Carry
two derived variants and let the *role* pick: the raw accent for fills and display sizes, a
lifted one for anything at body size. Lift it against whichever ground the accent reads worst on,
because one token paints the same class on the surface and on the sunken band.

**And a stated token is not a waiver.** The same build derived `onPrimary` when a tenant left it
unset and honoured it when a tenant stated it — so a brand stating `#FFFFFF` shipped 3.72:1 ink.
A theme value is a statement about a colour, never a statement that it can be read on the thing
it sits on. Validate a stated token against its role's floor and replace it where it fails,
exactly as you would fill an absent one, and record the repair — a correction nobody logged looks
identical to a brand that got it right.

**Muted-on-dark alphas.** `rgba(255,255,255,.34)` reads as "subtle" and measures 2.98:1. `.55`
to `.62` is the honest range. Alpha is not a taste decision on a dark surface. `.44` on `#181717`
is 4.36:1 — still failing, and on one build it was carrying the *vendor's* own "Powered by …"
byline on every page of a customer's site: the dimmest text on the surface was the one mark that
should not look like an afterthought.

**Audit the muted ramp, not the instance.** Those alphas are one authored ramp, so they fail
together and they fix together. One review measured seven muted classes across eight surfaces at
2.98:1, 4.22:1, 4.32:1, 4.34:1, 4.34:1, 4.36:1 and 4.41:1 — **five of them within 0.2 of
passing** — and a single pass over the ramp would have cleared most of the site's remaining
failures. Two consequences: file them as one finding, not seven; and note that the pass changes
the *reference* build's computed styles, so on a system with a parity oracle over the reference
it is a brand decision to raise, not a fix to slip into a review.

**A focus-ring colour that is not the accent.** The accent-coloured ring inherits the accent's
contrast problem exactly where a keyboard user needs it most.

## The stylesheet's defaults are one tenant's brand, not neutral values

This is the failure mode that only appears on tenant two, and it is worse than a missing token
because it produces something that looks deliberate.

Whatever the first tenant's values were became the stylesheet's fallbacks. So a second tenant
that omits a token does not get a neutral default — it gets **the first tenant's brand**.
Measured Aug 2026 on a live near-black portal against a light-themed reference: 12 of 25 colour tokens
unset, and the consequences were an alert band painted in the reference company's pale **pink**
with white text on it, a keyboard focus ring in the reference company's **red**, and a button
that turned red on press. Nothing errored, nothing warned, and every one of those is a plausible
enough colour that a reviewer reads it as a choice.

Three defences, in the order they should land:

- **Derive what is genuinely derivable** from what the tenant *did* state — and *measure*
  before you decide something is underivable. One review declared a link colour, a border
  colour and a footer surface "an invented relationship dressed as a recovered one"; measured
  against the reference stylesheet, every one of them is a fixed offset reproducing the
  reference's own hand-picked value to within a unit or two per channel. The test is
  mechanical: strip the token from tenant one's theme and check the derivation puts tenant
  one's value back. If it does, it is recovered. If it does not, you invented it.
- **Derive in the RENDERER, not only in the producer.** This is the one that repairs what is
  already stored. Fixing the generator corrects the next record; every partial record already
  in the database keeps painting tenant one until somebody reseeds, and nobody schedules that.
- **Then make the schema refuse a partial theme — and not before.** A record stating `canvas`
  and omitting the rest should fail validation *eventually*. Shipping that first takes
  production down: if the renderer re-validates on the way out of the store, and every stored
  themed record is partial (which is the finding), tightening the schema 404s all of them the
  moment it deploys. Order: derive in the renderer → reseed → tighten the schema.

Two traps inside the derivation itself:

**Do not gate it on "is this the dark case".** Every derivation in one build was written
`isDark ? … : undefined`, because the review that prompted it measured a near-black tenant and
a light tenant feels close enough to a light reference to be safe. Measured Aug 2026 on a warm-cream
`#F6F3EC` canvas: the sunken surface and the body ink unset, so its sunken bands painted the
reference's grey under a cream page. **A theme is not tenant one's because it is also light.**

**Derive at the root of the chain.** A derivation keyed on a token that is itself optional
repairs nothing when both are absent — a border-strong computed from `border`, a footer
computed from `surface-dark`. A tenant stating only a canvas and an accent still had thirteen
tokens on the reference's values after a fix that claimed to close this.

## A state pair is derived in one direction, not twice independently

Hover and pressed are a sequence, not two colours. Deriving each from the canvas separately
produced a real defect: a brand's *stated* darker hover beside a *derived* lighter pressed, so
the button got darker on hover and lighter on press. A tenant that states one of a pair decides
the direction of the other; the canvas only decides it when the tenant states neither. The same
holds for any ramp a tenant can partially supply — sizes, elevations, weights.

## A token nothing reads is not applied

The next failure along, and it is invisible to every check that looks for the token rather than
at the node. A multi-tenant contract carried `primaryOnDark`; every record set it; the injector
emitted it; the rendered HTML showed it. **No CSS rule referenced it.** Every accent word on
every dark band painted in the raw accent, and the largest text on the house-tier hero — the
company's own name, 72px — measured **2.14:1**.

Grep for `var(--the-token)` before believing a token does anything, and when you add the rule,
watch source order: an override at *equal* specificity placed earlier in the file loses silently,
and looks exactly like a rule that was never written.

## A variant class nothing selects is the same defect, one layer out

The stylesheet form of the unread token, and this one arrives with a comment vouching for it.
`.idx--undated` existed in a real portal's CSS with a note explaining exactly the case it was
for — an index row whose documents carry no date — and no code path ever applied it. So all
thirteen rows of that page rendered the dated variant with nothing to put in the date cell: an
`<time dateTime="">` (invalid, and empty) inside a track that computed to `0px`, with the dotted
leader stranded as a 24px stub in front of it. Every variant class gets grepped backwards to the
selector that applies it, the same way a token gets grepped back to the rule that reads it — and
a variant with no producer is either wired up or deleted, because a stylesheet that documents a
state the renderer cannot reach is worse than one that never claimed to.

The build-side half: **when a field is absent, emit no element rather than an empty one.** An
empty `<time>`, an empty `<nav>` and an empty list item all reserve layout and all announce
themselves to a screen reader as something that is there.

And the version of that which survives the obvious pass: **a labelled block renders only where
the tenant holds something to put in it.** After a footer's hard-coded proper nouns were all
found and removed, four literals were still rendering on tenant two — `ABN ᴹ` (the word, a
space, and a lone footnote marker), a **Share registry** heading over a link to `""`, and
`0 sites across NSW and Queensland` under a company in a different state. A heading over an
empty value is worse than the absence, because it asserts the field exists and that *this*
tenant has nothing for it; a derived `0` is not a fact, it is a template that did not get its
data. None of it greps: there is no company name in any of those four strings. They were found
by opening tenant two's footer and reading it.

## What must NOT be a token

**Anything a tenant could set that breaks the layout.** Container width, base font size and
spacing scale look like natural tokens and are the ones that turn a coherent grid into a
per-tenant regression surface. Ship them fixed until a real tenant needs otherwise.

**Free-text CSS.** A `styleOverrides` blob is how a design system dies: it is unreviewable,
untestable and it is where every tenant-specific hack accumulates.

## Sections switch off; they do not empty

A tenant with no video does not get an empty video band — the section is absent. This has a
design consequence people miss: **every section must look right as the first thing after the
hero and as the last thing before the footer**, because with sections toggling you cannot know
its neighbours. Band alternation, first-child spacing and divider logic all have to be derived
from position at render time rather than baked per section.

Corollary: design the *empty* tier too. A tenant you hold nothing for still gets a page. It
should place **fewer** sections rather than the same sections with nothing in them — an empty
share-price block reads as broken where its absence reads as honest.

Measured, on a tier built for a company almost nothing was held for: four bands to convey three
facts, at 36% / 48% / 61% ink fill against the reference build's own 49–62% rhythm, with 184px,
205px and 229px of ink-to-ink dead gap between them. The payload was Legal name, Ticker,
Exchange — **all three already stated in the page's own badge and H1**. A 1150px-wide table
restating the headline is what "the same sections, thinner" produces. The honest version of that
page is one band.

The measurement that catches it is **ink fill per band** — the union bbox of what a band actually
paints, over the band's own box height. A box-based check reports every one of those bands as
healthy, because their boxes are the right size; it is the content that is missing. `design-review`
carries the probe (`probeColumnVoids`).

## The chrome is part of the vocabulary

Header, navigation and footer are the parts nobody enumerates, because on tenant one they were
just there. Then a generator emits an empty `chrome` object, the layout renders
`{header && …}`, and the tenant ships with **no brand, no navigation and no footer** — five
pages measuring zero internal links and a single tab stop, with two routes resolving 200 that
nothing on the site pointed at. Every content check passed.

Two rules follow. **The nav is derived from the pages the tenant declares**, so a one-page tenant
renders no `<nav>` at all rather than an empty labelled landmark and an empty drawer list — an
empty landmark announces itself to a screen reader and holds nothing. And **no tenant-specific
literal survives in a shared component**: a footer hard-coding one company's monogram, listing
code and policy PDFs publishes that company's constitution under every other tenant's address the
day chrome starts rendering.

## The renderer must fail loudly

Map section kind → component, and **throw on an unknown kind**. A silently dropped section is
indistinguishable from one the tenant disabled, and no diff can tell you which happened. This is
a design constraint, not an engineering one: it is what makes the vocabulary enforceable.

## Prove it with two instances, not one

A vocabulary validated against a single brand is a vocabulary shaped like that brand. Build the
second one — ideally one with a different accent, a different type family and a different motion
preset — before believing the system generalises. Most of what is actually hard-coded only
becomes visible on the second tenant.
