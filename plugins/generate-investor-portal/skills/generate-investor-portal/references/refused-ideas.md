# Ideas that look good and are not

These are not style preferences. Each one is an idea a capable author re-derives from the same brand
documents you are reading, so each is written with the mechanism that defeats it rather than a
verdict — **a rule with no reason attached loses to the first person with an argument, and the
argument for all six is good.**

A documented decision *not* to build something is rarer and more useful than another check, so the
refusals are kept whole, including the one that was proposed by a review and declined.

---

## Three the contract refuses outright

You will meet these as a validation error rather than as advice. The reason is in
`PlatformProhibitionSchema` in `libs/shared/src/investor-portal/portal-contract.ts`.

### `announcementExcerpt` — an excerpt of a lodged announcement

Quoting one sentence of a price-sensitive release is **selective emphasis**, and it changes what the
release says even when every word is verbatim: the reader gets the fragment the portal chose in place
of the document the company lodged.

Bound three ways, because one is not enough: the lodged-document field set is closed so an excerpt
has nowhere to live; no string may be a fragment of a lodged title; and no string may be a lodged
title with its case changed. Render the title whole and link to the PDF.

A US district court has noted the same mechanism in AI-assisted summarisation — selective quotation
obscures the holding (`references/evidence.md`, E11). That is corroboration of the mechanism, not of
this specific rule.

### `lodgedFigureMotion` — `countUp` over a stated figure

Ramping a numeral from zero turns a disclosure into emphasis. Over a mineral-resource or ore-reserve
figure it detaches the number from the **competent-person statement** it is only ever valid
alongside; over any other figure it detaches it from its as-at date and its source.

`countUp` is still available over a number that is not a stated figure.

### `measuredGrid` — a measured grid value in the theme

`container` / `gutter` / `prose` read off a brand's site and passed through is a free-text style
channel with a numeric keyboard: unbounded, cited to nothing, different on every tenant, and it
re-breaks the parity oracle per tenant. Every DESIGN.md measured so far states the same
**1200 / 24 / 68**.

If a brand genuinely differs, add the rung to `PLATFORM_GRID` **with the sentence that justifies
it** — the same standard `WebglFigureSchema` holds its three values to.

**The general form:** a new tenant style axis is an **enum or a bucketed value, never a pass-through
number.** A raw measured number is a free-text channel expressed numerically — it ends the bounded
vocabulary the same way a `styleOverrides` blob would, and it does it without looking like one.

---

## Three that are design decisions, so they cannot be a schema rule

### Composing the page from engagement telemetry

Ordering or promoting sections by what readers click is self-echoing: the telemetry measures the
layout that produced it, so the loop converges on whatever the first layout happened to surface.

Worse on this surface specifically — it demotes exactly the content nobody clicks *and that is
mandated anyway*: governance documents, the registry block, disclaimers, the illustrative-value
ledger. Section order comes from what the record holds, which is the same input for every reader.
**Engagement evidence is not brand evidence.**

### Reader-density rungs with a HUD toggle

A "summary / standard / full" switch varies what **one** reader sees; it does nothing about what
distinguishes **two companies**, which is the problem the structural vocabulary exists for. And it
multiplies the surface every computed-style oracle has to cover by the number of render states, on a
platform whose gates are already the thing holding the tenant count up.

If a portal is too dense, the record is placing too many bands. Cut sections, not pixels.

### A distinctiveness loop with no hard abort

"Keep differentiating until the two tenants are far enough apart" runs out of honest input: once the
second-ranked evidence in the DESIGN.md is used, the loop has nothing left and starts choosing by
taste or by noise. That is variety from randomness, and it fails the derivability floor every axis on
this platform is held to — **every option must be traceable to a sentence in the brand's own
documents and must cite it.**

A loop that cannot cite its next move must stop, and report that the brand's material supports N
axes rather than inventing the N+1th.

---

## And one a review proposed, argued for, and did not get

The emphasis review found a real bug (see `references/what-shipped-wrong.md`, "The emphasis rung that
had never been won") and proposed two fixes. The first was taken. The second was **emit
`data-emphasis` on every `<section>` so a rendered-layer gate can read the budget**, and it was
declined.

The argument for it is good: the budget is currently unmeasurable from the rendered layer, and this
skill's own ladder says an unmeasurable rule is a weak rule.

The reason it is still wrong:

- Emphasis is not a device. It is a **ranking step** whose output is `band` and `divider`, and those
  are already in the DOM and already gateable. Emitting the rank itself would put a database field
  into the markup **so a gate could confirm the database — a gate measuring its own input.**
- It would break a deliberate assertion — *nothing that renders a page reads `emphasis`* — which is
  the entire proof that the feature cannot move the parity reference.

And the measurement sharpened what the real defect is. At level 2 the budget maps to
`band: 'surface'`, which measures **1.08:1 against the canvas**. So after all of it, the visible
difference between two tenants' home pages is which of two sections carries a band 8% off white.

> **The defect is not that emphasis is invisible to a gate. It is that emphasis is nearly invisible
> to a reader.**

The fix for that is a wider set of audited dark-capable kinds and a louder level-2 treatment — not an
attribute. **Gate what a section *renders*, never what a record *ranked*.**

One external rule belongs beside this, because it is the same subject with a legal edge: ASX expects
a cautionary statement accompanying an estimate or target to carry **equal prominence — same font
type, size and colour, on the same page** (`references/evidence.md`, E4). An emphasis budget that can
quieten a caution is a compliance defect, not a design choice.
