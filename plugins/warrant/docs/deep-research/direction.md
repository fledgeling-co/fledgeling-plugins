# Direction record — verifier-substitution page

## MOBBIN TRAWL (18 Aug 2026)

    q1  "long-form research article with inline citation markers and a numbered source list"
          → 6 results, opened 6 (OpenAI, Grammarly ×4, Harvest)
    q2  "comparison table of tiers with one row highlighted as recommended"
          → 5 results, opened 5 (Wix, Patreon, Vanta, Kit, Stripe)

    TOOK  Section label in a NARROW LEFT GUTTER, content in a wide right column,
          hairline rule between rows. OpenAI's references block does this for
          Footnotes / References / Authors / Acknowledgments, and Vanta and Stripe
          do the same for comparison rows. This is the mechanism for both the
          claim registry and the tier table — one device, two uses. (q1 OpenAI,
          q2 Vanta, q2 Stripe)

    TOOK  The recommended option is a RAISED, BOUNDED STRUCTURE, never a badge.
          Patreon lifts the recommended plan into a card that sits proud of its
          neighbours with a coloured header band running its full width; Wix puts
          a solid tab above the column and rules the column's sides. Kit uses a
          small pill badge and it is visibly the weakest of the three. Applies
          directly to the tier table, where exactly one tier is the
          recommendation. (q2)

    TOOK  Density. Every shipped comparison showed 9–11 rows above the fold
          (Wix 9, Vanta 11, Stripe 9). A generated layout would have shown four
          and called it calm. The claim registry and tier table should be dense
          enough to read as a reference, not as a marketing table. (q2)

    TOOK  An EYEBROW label above the heading, set small and quiet, to name a
          section without spending a heading level on it — Stripe's "Compare
          support plans", Harvest's italic "On ritual". Useful for marking which
          reading is active and for labelling a disagreement block. (q1 Harvest,
          q2 Stripe)

    TOOK  Zebra banding behind table body rows only, with the left label column
          left unbanded (Stripe). Keeps a dense table legible without drawing a
          vertical rule beside text, which the auditor measures.

    LEFT  Hand-drawn scribble marks flanking the pricing cards (Patreon). Pure
          identity, and it would read as whimsy on a page about audit evidence.

    LEFT  Tinted full-bleed collapsible section bar (Vanta). It is a real
          mechanism for collapsing, but the page has no collapsing to do and it
          would just be a grey band.

    LEFT  Centred narrow intro paragraph over a three-column link list
          (Grammarly). Generic marketing shape; the page's intro is a TLDR band
          with cited claims, which is a different object.

    NOTE  Four of six q1 results were Grammarly product UI rather than long-form
          article structure — the query pulled "citation" as a product feature.
          The one genuinely useful result was OpenAI's. Recording this so the
          hit rate is not overstated: 2 of 11 opened results carried a mechanism
          worth taking.

## Skeleton, derived from the claim graph rather than the brief

The brief had ten numbered subtopics. The section list below is written from
`claims.json` alone and then checked against that enumeration — it does not
match it, which is the point. Subtopics 3 and 5 do not get sections of their own
because the evidence did not support one; the panel's own failure does get a
section, and the brief never asked for it.

1.  The verdict, and what it costs to have it            (I1, C21, C11)
2.  What is already true here                            (C22, C23, C24)
3.  The jury is one reader                               (C2, C3, C4, I3)
4.  Nobody has measured the incumbent                    (C1, C5, C6)
5.  The aid makes the human worse                        (C7, C8, I5)
6.  The evidence channel belongs to the accused          (C14, C15, C16, C18, I6)
7.  What the signature has to be                         (C10, C11, C12, C13, I4)
8.  What is closable without a judge                     (C17, I7)
9.  What to do with the 194                              (I2, C19)
10. The panel that proved its own finding                (M1, M2, M3, M4)

Section 10 is the editorial tension and it is not omittable from any reading.

## FIXED (18 Aug 2026, with Luke)

    slug       deputy  →  ~/Dev/dossier/deputy/  →  deputy.fledgeling.app
    spine      Accountability, not accuracy. The blocker is not that the
               machines are insufficiently good; it is that a signature has to
               belong to somebody (C11), and a control that reversions silently
               cannot be the control of record (C12, C21).
    aesthetic  The warrant and its scope. Nested containment: everything inside
               the boundary the machine may decide, everything outside stays
               with a person, and the boundary tightens as consequence rises.
               Motion signature: the boundary contracting — one semantic move,
               not scroll decoration.
    icon       A bounded field with a smaller bounded field inside it, the
               inner one filled. Mined from the subject, settled at Phase 8.

    Slug and device are one metaphor family, which is load-bearing rather than
    tidy: a deputy is exactly a person who may act, within a written scope, on
    an authority that remains someone else's.

## Overlap check against the 30 published pages — TWO real hits

    quorum   `Where they all agreed, they were least useful` already argues
             that panel agreement is weak evidence, from a three-backend $20
             panel, and ships `All three said nobody does this. Somebody does`.
             CONSEQUENCE: the correlated-reader material (M1–M4, C2–C4) is a
             SECOND INSTANCE, not this page's discovery. It stays — the panel
             reproducing its own finding is still the editorial tension — but it
             cannot be the spine and it cannot be the h1.

    layout   The narrow-label-gutter skeleton is the HOUSE PATTERN, measured
             rather than assumed: quorum `11rem 1fr auto`, hearsay `110px/150px
             1fr`, register `118px/132px 1fr`, meter `74px 1fr`, dataless
             `220px 1fr 100px`. Five pages, one vertical divide.
             CONSEQUENCE: the Mobbin TOOK above is kept for the claim registry
             and the tier table only, where it is the right mechanism and was
             reference-verified. It is NOT the page's primary skeleton, or this
             is the sixth instance of the invariant the skill names as the one
             that reads as sameness.

    Free: `verified/` exists as an empty directory, no index.html, no collision.

## Section skeleton, re-derived under the fixed spine

Ordered as the warrant narrowing — widest permission first, then tightened
until what is left is what a machine can actually hold. This is not the brief's
enumeration and not the earlier draft's order; the spine moved, so the sequence
moved with it.

1.  The answer is a warrant, not a verdict            (I1, C21, C11)
2.  What is already inside the fence here             (C22, C23, C24)
3.  What a regulator has let a machine decide alone   (C9, C10)
4.  The signature is the part that will not delegate  (C11, C12, C13, I4)
5.  Inside the boundary, the panel is one reader      (C2, C3, C4, I3)
6.  Nobody measured the person being replaced         (C1, C5, C6)
7.  Hand the human the verdict and you shrink them    (C7, C8, I5)
8.  The evidence belongs to the party being judged    (C14, C15, C16, C18, I6)
9.  What genuinely fits inside a machine's warrant    (C17, I7)
10. What to do with the 194                           (I2, C19)
11. The panel wrote its own warrant too wide          (M1, M2, M3, M4)

Section 4 is the spine and section 11 is the editorial tension; neither is
omittable from any reading. Subtopics the brief enumerated that get no section:
the evidence did not support one.

## Build record (18 Aug 2026) — what was measured, and what could not be

Page: `~/Dev/dossier/deputy/index.html`, one self-contained file, GSAP inlined,
zero network requests. Served for review at `http://127.0.0.1:8781/`.

    MEASURED (Obscura, longhand computed styles only)
      contrast        19 element/ground pairs × light and dark = 38, zero failures
      overflow        scrollWidth − innerWidth = 0 at 1280
      frame nesting   5 distinct widths at rest: 1088 / 1022 / 954 / 888 / 822
      divider gutter  frame-to-ink gap ≥ 147px at every depth (floor 24px)
      registers       three separate renders, one radio `checked` in each;
                      page heights 27,899 / 30,570 / 31,940px prove the
                      registers are genuinely different content
      gates           audit_page.py 0 errors · design-lint 0 unadjudicated

    ADJUDICATED AGAINST THE RENDER, not suppressed
      design-lint reported four contrast CRITICALs at 1.20:1. Measured on the
      rendered CSS they are 15.03 / 15.03 / 15.03 / 5.24:1 — the lint resolved
      the page's light `--paper` as the ground for elements that sit on the dark
      publisher chrome and on the accent fill.
      design-lint's `external-resource` MAJORs are hyperlinks in the source
      registry, not subresource requests; the page issues none.

    NOT CHECKED ON THIS ENGINE — stated rather than assumed
      motion            no CSS animation and no GSAP timeline executes
      print             `setEmulatedMedia` is accepted and inert
      reduced motion    same reason
      type fidelity     web fonts never load (the page uses a system stack, so
                        this is narrower than usual, but it is still unchecked)
      chars per line    `Range.getClientRects()` returns one merged rect for
                        multi-line text here, so the measure was read off the
                        screenshots by counting characters instead

    TWO DEFECTS THE MEASUREMENT CAUGHT, both in the same mechanism
      1. `gsap.fromTo` wrote its start state immediately, so `--fi: 0px` sat on
         every frame and all five depths rendered at one width. The page's whole
         visual argument was absent at rest and no screenshot said so.
         Fixed with `immediateRender: false`.
      2. Once a trigger fired, a non-animating engine stranded the frame at the
         start state again — and the start state (full width) contradicts the
         device. Fixed by starting 44px wider than the end rather than at zero,
         so the nesting is legible in every frame of the motion.

## Review ledger (18 Aug 2026) — 16 findings raised, 16 closed

A `design-review` pass over the rendered page raised four HIGH, six MEDIUM and
six LOW. All are fixed. The four HIGH were invisible to my own checks because I
had measured one viewport.

    HIGH  closer band       `grid-template-columns:auto 1fr auto` gave the facts
                            list its 730px max-content and starved the prose
                            column to 176px, wrapping a 30px h2 to eight lines.
                            Fixed with an override — then re-fixed, because the
                            override was unscoped and beat the chrome's own
                            max-width:820px stacking, putting 321px of horizontal
                            scroll on a phone. Scoped to min-width:821px.
    HIGH  bar value labels  `white-space:nowrap` beside a 100%-wide fill escaped
                            the track, the figure card AND the scope frame, and
                            below 1280 it reached the document: 193px of page
                            scroll at 375 (WCAG 1.4.10). Now a three-column grid
                            with `.bar__t{display:contents}`.
    HIGH  skip link         z-index 60 under a z-index 150 opaque sticky bar, so
                            the first tab stop was invisible at every width.
    HIGH  sticky chrome     324px of a 812px viewport (39.9%), and `--masthead`
                            was a static 68px while the bar measured 212px, so
                            every one of 113 citation jumps landed up to 127px
                            above the visible area. `--mast-h` is now measured
                            beside `--colo-h`; the mobile bar is one row (61px);
                            and the generated `.tucked` state, which shipped with
                            a reduced-motion override and nothing ever adding the
                            class, is wired. Chrome is now 20.9% at 375.

    MEDIUM  every border and rule sat at 1.28–1.80:1 — including the containment
            device the whole design rests on. Component boundaries and the device
            are now ≥3:1 (`--rule-strong` lifted to #828A96); intra-card table and
            list rules are deliberately left quiet, which 1.4.11 does not cover.
    MEDIUM  the depth device was a 3% width step between sections never co-visible.
            `--scope-step` is now 4.2vw: 1088/980/872/766/658 at 1280, and
            1088/960/832/704/576 at 1600, where depth 4 does approach the measure.
            Figures are capped to their own scope so they cannot exceed the frame.
    MEDIUM  the position indicator drew five nested outlines whose inner two were
            an 11px and a 4px sliver. Redrawn as a narrowing stack of five bars,
            which is also truer: the frames only inset horizontally.
    MEDIUM  the citation preview sat under the publisher bar (z-index 50 vs 150),
            had no upper clamp when flipping, no blur handler, and `role="dialog"`
            on something never focused. All four fixed.
    MEDIUM  26 targets in the ledger's Src column measured 7.5×16px with no larger
            equivalent and no spacing exception. Now 24×25.
    MEDIUM  a reader who had chosen dark got a light first paint, because the theme
            was applied after 1,400 lines of body and two inlined GSAP blocks. A
            three-line script in `<head>` now sets it before content parses.

    LOW  heading order skipped h1→h3 · the TLDR rail was 15px narrower than every
         other rail · 14 type sizes with six pairs 0.5px apart, collapsed to eight ·
         16 numeric runs without tabular figures · two teals two units apart doing
         different jobs · `loading="lazy"` on four inline data URIs · claim C20 in
         the ledger and on no section, now argued in §1 · the frame tween computed
         its end pixel once with `once:true`, leaving every depth stale after a
         resize (now function-based with `invalidateOnRefresh`).

    MY OWN ERROR, recorded because it is the cheapest kind to repeat: the mobile
    media block was inserted above the rules it overrides, so `flex-wrap:nowrap`
    lost to source order at equal specificity and the masthead stayed at 212px
    while reporting as fixed. Moved to the end of the stylesheet.

    FINAL: 39 contrast checks × 2 themes × 2 viewports = 156, zero failures.
    Horizontal overflow 0 at 375 / 768 / 1024 / 1280 / 1600. audit_page.py 0
    errors. design-lint 0 unadjudicated critical or major.

## Aesthetic frame (superseded above — kept as the record of what was offered)

Subject matter as frame material: this is a page about **evidence that does not
survive being counted twice**. The visual device therefore has to be able to
show a thing that looks like N and is really ~2. Candidate devices, to be
narrowed with Luke:

- **Tally / ledger**: nine marks that collapse to two under a rule. Reads as
  audit, matches the claim-registry gutter, and the collapse is animatable as a
  single semantic motion rather than decoration.
- **Instrument calibration**: a dial with a declared uncertainty band, which is
  the ISO-17025 point made visual, and makes "inconclusive" a legible position
  rather than a gap.
- **Witness stand / attestation**: signature and seal language, which fits the
  admissibility half but risks legal-pastiche.

Taken by earlier pages in ~/Dev/dossier and therefore unavailable: hero
silhouettes, chart grammars and transition metaphors already used by `quorum`,
`hearsay`, `ledger`, `meter`, `register` and `dataless` — several of which sit
uncomfortably close to this subject and need checking before a direction is
fixed.
