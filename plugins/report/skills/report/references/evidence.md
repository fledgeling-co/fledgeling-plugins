# Evidence — what every rule traces to

This skill did not buy its own research. It is built on two corpora that
already existed in this portfolio, both read end to end before the skill
was written, plus the observed record of how these documents have
actually been asked for and criticised.

Recording the provenance honestly matters here more than usual, because
the skill's own central rule is that a claim should carry a locator.

## The corpora

**1. The scrollytelling panel** — `dossier-report`'s research, exported
in `plugins/dossier-report/docs/deep-research/`. Five backends, one
brief, all read end to end: Gemini ($7.00), OpenAI gpt-5.6 ($9.00),
Perplexity Sonar ($4.00), Claude Code ($0), Codex CLI ($0). **$20.00
total, 397,000 characters, 225 cited sources.** Citation verification:
Claude Code PASS (0 fabricated / 50); OpenAI 1 dead of 44, a 404 mirror
of a paper the same report cites by working DOI. Distilled in
`plugins/dossier-report/skills/dossier-report/references/evidence.md`.

**2. Typographic emphasis and editorial structure in long-form B2B
documents** — `create-diolog-guides`' research, at
`plugins/create-diolog-guides/skills/create-diolog-guides/references/research/typography-legibility-research.md`.
Tinker & Paterson through to Rello & Baeza-Yates and MIT AgeLab; the
print-side evidence this skill needs and the scrollytelling panel does
not cover.

**3. Anthropic's current prompting guidance**, read in full while
authoring: the migration guide, prompting best practices, and the Opus 5
page. This shaped how SKILL.md is *written* rather than what the report
should contain.

**4. The observed record.** 41 requests across this portfolio's session
transcripts asking for a report or summary with rich content, and the
feedback that followed. This is the weakest evidence type here — it is a
single user's stated preferences, not a measured result — and it is
labelled as such wherever it is load-bearing.

---

## What each rule rests on

### Lead with the conclusion

Chartbeat/Slate instrumentation: ~38% of arrivals leave immediately,
median scroll depth ~50% (Slate) to ~60% (web-wide), only 25% pass the
1,600th pixel of a 2,000-pixel article, and scroll depth correlates only
weakly with sharing.

→ The TLDR is the top of the full report, not only a separate file.

### The format buys attention, not comprehension

The single most repeated finding in the panel, agreed by all five
backends. Méndez & Such (CHI 2026, n=454): scrollytelling matched plain
text on comprehension accuracy and confidence, beat it on cognitive load
and engagement, trust differences inconclusive. McKenna et al. 2017
(n=240): animated transitions beat static on perceived engagement
(`p<.001`), no major comprehension difference. Kim et al. 2024: immersive
variants rated more interesting and **more persuasive**, no more
understandable or trustworthy.

→ The report never claims its format aids understanding, and never cites
dwell time as evidence of anything.

### Motion is semantic or cut

Supported: Heer & Robertson 2007 (n=24), animated transitions between two
states of one encoding reduced tracking error across all types
(`p<0.001`). Not supported: Tversky, Morrison & Bétrancourt 2002 —
apparent advantages were confounds, and after a week text-studying
participants improved while animation-studying participants declined.
More staging is not better: extreme staging worse than direct animation
for donut value changes (`p=0.024`).

→ The motion test, and the authored static frame.

### Never touch native scrolling

NN/g 2023: a majority experienced at least mild disorientation; on a
fully scrolljacked page **every** participant was disoriented. Murano
2026 (n=20): no speed benefit, significantly lower accuracy and
satisfaction.

→ `normalizeScroll()` prohibited; wheel, momentum, direction and history
left alone.

### Citations are built to be inspectable, not clicked

Piccardi et al. 2020, 96 million Wikipedia citation events over two
months: external-reference clicks in 0.29% of page views (0.56% desktop,
0.13% mobile); 93% of cited URLs received no click that month. Clicks
were *more* common on shorter, lower-quality pages.

Tse's rule caps the design: *"if you make a tooltip or rollover, assume
no one will ever see it."*

→ Three layers, redundant by design. The registry is the load-bearing
one; the popup is convenience.

`<INSUFFICIENT_EVIDENCE>` "Good citation UX makes readers verify" is
unsupported in either direction. What is supported: previews lower
exploration cost, and multiple co-present transparency signals raise
perceived credibility more than one does (n=1,183, small but significant
on 4 of 15 measures).

### Anchor, not button

Found by a blind judge on a page `dossier-report` produced: `<button
data-cite>` markers are inert with JavaScript disabled, breaking the
claim-to-source bond in exactly the no-JS case the document is told to
survive.

→ The markup contract. Carried over unchanged, because the reasoning
transfers exactly.

### Chart integrity is validated at generation

Pandey et al. CHI 2015 (n=330): deceptive charts produced interpretations
**58.5%–129.5% larger**; an inverted axis made **97.5%** respond
incorrectly. Okan et al. 2021, five studies: 83.5% showed a truncation
effect and **instruction did not eliminate it**; chart familiarity,
visual ability and education showed no protective correlation.

→ Reader sophistication is not a mitigation, so the check happens at
generation.

### Editorial titles

Borkin et al., 393 visualisations with eye-tracking on 33 participants:
titles and supporting text materially drove recognition and recall.

### Typography: size and space, not stacked styles

Williams & Spyridakis 1992 card-sorting: size (~20% between levels) and
spatial placement are far stronger hierarchy cues than weight or case.
MIT AgeLab: consistent alignment and predictable layout improve reading
speed by up to 22%.

All-caps: Tinker — 10–20% slower; Arbel & Toler 2020 — 13% longer to read
(94.7s vs 83.4s) and readers over 55 were **29% more likely to
misunderstand** all-caps contract terms. Italics: Tinker 1963 — ~10.4%
slower; Rello & Baeza-Yates 2016 (n=97, 48 with dyslexia) — fixation
0.27s vs 0.25s (`p=0.040`), 46% actively disliked italics.

→ The typography rules, and why they are compatible with a distinctive
look: distinctiveness lives in face choice, palette and composition, not
in decorating body text.

`<MISSING_DATA>` No empirical threshold exists for emphasis density —
"maximum % of bold words per page". Authorities rely on discretion. The
skill says "one or two key phrases per paragraph" as a convention, not a
measurement.

### Every page must look different

Goree et al. CHI '21: ~2M pairwise comparisons, 2003–2019. **Layout
similarity distance declined 44% from 2010 to 2019**, and the strongest
correlate was **shared use of a small number of frameworks and
libraries**.

Independently corroborated by Anthropic's own frontend-design guidance,
which names the convergence directly — Inter, Roboto, Arial, purple
gradients on white, and a documented tendency to converge on Space
Grotesk across generations.

→ The invariant is layout skeleton and motion signature, not palette.
Re-theming fixes nothing.

`<INSUFFICIENT_EVIDENCE>` There is no validated metric for "recognisably
templated" — all four backends returned this. The silhouette check is a
production heuristic, and is labelled as one.

One counterweight: Song et al. 2025/26 found cartoon styling and
hand-drawn fonts **reduced** perceived credibility, while embellishment
improved recognition in other work. Distinctive is not arbitrary.

### Disclosure does not cost credibility

Licenji & Hoxha, systematic review of **47 studies** on audience response
to news presented as machine-written: effects on perceived credibility
are predominantly null or conditional. No uniform penalty. Their usable
recommendation is that transparency works as part of an accountability
package — what the automation did, what review it received, who is
responsible.

→ The methods note is specific rather than a badge, and this is why it is
not treated as a cost to be minimised.

### Accessibility floor

WCAG 2.2.2 (A) auto-motion over 5s needs a persistently available control
— one that appears only on hover fails, because voice navigation may
never trigger it. 1.4.13 (AA) hover content hoverable, dismissible,
persistent — the criterion naive citation tooltips fail. 2.3.1 (A) three
flashes, distinct from reduced motion. 2.3.3 (AAA) explicitly covers
scroll parallax. PDF14 asks that running headers be marked as pagination
artifacts.

> **One number handled carefully.** "Vestibular disorders affect ~35% of
> adults over 40" is real — Agrawal et al. 2009, NHANES 2001–2004, n=5,086
> — but it measured **failure of a standing-balance screening test** among
> **US** adults 40+, with **falls** as the outcome. Not diagnosed
> disorders, not a global rate, and nothing about sensitivity to on-screen
> motion. This skill does not use it. The WCAG case has no soft spot and
> survives a click-through unaided.
>
> Recorded because it is the exact failure mode this skill's ledger
> exists to prevent: not a fabricated statistic, but a real one wearing a
> claim it does not support. The citation resolves, so only reading the
> source against the sentence catches it.

---

## The observed record

From this portfolio's transcripts. Weaker evidence than the above, and
load-bearing only for choices about *this user's* documents.

| Observation | Where | Consequence |
|---|---|---|
| "Look at how reva.skin does its citations with popups — I'd like the same" (asked twice, plus `sift-web` named as the reference implementation) | 2026-07-29, 2026-07-31 | The three-layer citation contract, matching `cold-flu-evidence/index.html`'s markup exactly |
| "Include the same banner as cold-flu-evidence… Aside from the top static banner, aesthetic/design should not be taken from that page" | 2026-07-30 | Reuse the infrastructure, never the look — the same boundary the panel reached independently |
| "Incorporate micro interactions / animations into the ui mocks that don't show when exporting as pdf" | 2026-07-09 | Motion never reaches the print output |
| "There's still many layout issues in the page, also it'd be great if there were proper, validated citations throughout" | 2026-07-29 | The auditor, and citation integrity checked both ways |
| "What's been generated so far looks more like a stylised document than a high fidelity, premium website" | 2026-07-31 | The authored review, and the anti-convergence rules |
| "Technical (comprehensive) and non technical (a tldr) summary in the same md file"; "a tldr aimed at a 14yo" | 2026-08-06, 2026-07-29 | The TLDR derived from the same ledger rather than written separately |
| 10+ HTML reports on disk, the largest inlining GSAP entirely into a single 750KB file | across `diolog-team-files`, `dAIolog`, `perch` | Self-containment as the default, with the webfont caveat stated |
| 26 projects carry a `DESIGN.md` | portfolio-wide | Resolution order puts the project's own system first |

---

## What this skill does not do, and why

Recorded rather than quietly dropped.

1. **No sameness detector.** Goree et al.'s method — greyscale blurred
   full-page screenshots scored pairwise against every previous report —
   would turn "every report must look different" from an unfalsifiable
   goal into a gate. The manual silhouette check is the cheap stand-in.
2. **No motion benchmark.** The one place the literature contradicts
   itself is whether GSAP ScrollTrigger materially harms INP, and every
   specific claim on both sides traces to vendor-adjacent blogs. The
   widely repeated "≤30 active triggers" figure has no traceable
   empirical basis. This skill does not tune against it.
3. **No measurement of whether reports get read.** The honest position
   is that this is unknown for this document class.
