# What shipped wrong

The incidents behind the rules in SKILL.md §5 and §3, each with the tenant, the date and the
measurement. They are here rather than in the procedure because a reader looking for *how do I
choose a `band`* should not have to walk five incident reports to find it — but the incidents are
the reason the rules survive an argument, so they are kept whole rather than compressed into
verdicts.

Read this when a rule looks arbitrary, or when you are about to override one.

---

## The rule production broke five times out of five

**Measured on production 2026-08-08, all five generated tenants.** Every generated portal's hero
evidence panel opened with *"N dated documents held, each linking its published PDF"* — 245 for
Telstra, 388 for JB Hi-Fi, 46 for Temple & Webster, where it is **one of only two items**, so half
the hero's evidence was about the CMS.

The rule *"a crawler artefact is not a fact about the company"* was already written, in prose, at
the top of the same section. The phrasing gives the defect away: *held* is something the portal
does, not something the company does.

**A rule this file states and production breaks five times out of five is a rule that needs a
gate, not more prose.** That is now `naming:artefact` in `assets/record-gate.mjs`, as a regex over
every rendered string plus a literal ban:

```js
const ARTEFACT = /\b(documents?|pages?|links?|images?|photographs?|records?|files?)\s+(held|found|crawled|mirrored|indexed|captured)\b/i;
```

It is also the origin of this plugin's severity ladder. See `references/validate-and-prove.md`:
the bottom rung is *skill prose*, and what it costs is that **it lost 5-of-5**.

---

## The masthead that repeated the section under it

**Measured on the same five tenants.** The hero's eyebrow pill and its H1 were the **same string**,
the company's legal name, one above the other in two sizes — *"Telstra Group Limited"* over
*"Telstra Group Limited"*. The largest type on the page carried nothing the wordmark 300px above it
had not already said, and a screen-reader user heard the legal entity name three times before
reaching content.

The rule already existed one section down — *"drop the eyebrow whenever it would repeat the
heading"* — written for `unitList`. **It is not a `unitList` rule.** The gate now applies it to
every section on every page, with the `§NN · ` ordinal stripped first so the ordinal cannot
disguise a repeat.

---

## The H1 that was the name on the share register

**Five of six live portals** opened with `<h1>Telstra Group Limited</h1>`, `<h1>BHP Group
Limited</h1>`, `<h1>JB Hi-Fi Limited</h1>`.

The over-read: *"The H1 comes from the company's own website language"* (see Voice) is right, and it
had been read as *"the H1 is the legal entity name"*. The reference build opens with *"Design to
delivery, from the Hunter Valley to your site."* Both are the company's own language; only one of
them says anything.

The gate refuses an H1 equal to `identity.legalName`, and refuses one that is the legal name plus a
suffix — because a suffix was the first workaround anyone reached for.

---

## The gapped section index

**Measured on production 2026-08-08: four of six tenants** shipped a gapped index — `§01 §02 §03
§05 §06` on three of them, and `§01 §02 §03 §06` on Temple & Webster, which also had no governance
page. A reader counts that and concludes the portal is hiding section 04.

**The mechanism is worth knowing because it is a shape that recurs.** The renumbering pass was
written for the archetype that **reorders**, and lives inside its `if`. The gaps came from section
**omission**, which happens under every archetype — including the one whose layout table is `null`
and which therefore skipped the block entirely.

> **A repair coupled to the condition that first revealed the defect will miss every other
> condition that causes it.**

Renumber unconditionally, after every step that can drop a section, and assert the ordinals are
contiguous per page. The gate asserts it; the renumbering is the generator's job.

---

## The favicon that cannot be a file

Two tokens most records forget, both one line: a **favicon** — a branded investor portal showing
the generic page icon in the tab strip is the first thing anyone sees — and **`color-scheme`**
matching the record's own canvas, because a portal on `#0A0A0A` declaring `color-scheme: light`
gets light scrollbars, light form controls and a light pre-paint flash.

**The favicon cannot be a file in `public/`,** and reaching for one is the reflex to unlearn:
`public/` is not tenant-aware, and one deployment serves every company on the platform, so a file
there is *the last tenant to ship one*, wearing every other tenant's address. Resolve the tenant
from the hostname the way every other pixel on the page is resolved, and draw the record's own
monogram on its own accent.

Three constraints ride with that, because it is the one place record data becomes **markup**:

1. **Escape the monogram.** A database row is not a trusted source of SVG.
2. **Validate the colours as hex** rather than interpolating them.
3. **A host that resolves to no tenant gets the *platform's* mark** — never the last one that
   resolved.

---

## The boilerplate that became content, and the filter that then ate the disclosures

A site crawl carries the company's privacy policy, terms, cookie notice and complaints procedure
under exactly the same heading levels as its service lines. Structure cannot tell them apart, so
subject matter must: one run rendered **"How Do We Collect Personal Information?"** and
**"Complaints Resolution"** under *"What the group actually does"*.

Then the same exclusion list, reused to decide which PDFs reach the document shelves, dropped four
**Modern Slavery Statements** filed under the Modern Slavery Act 2018 (Cth) — statutory
disclosures, published in the same folder as the annual report.

> **The tell that the split was already needed, visible without rendering anything.** The
> generator's own shelf map carried a `modern slavery` term in the rule that files a document under
> "Sustainability and ESG" — so there was a shelf named for a document class the filter guaranteed
> could never reach it. **A codebase that contains a category nothing can be assigned to is telling
> you a predicate is answering the wrong question.** Grep for that shape before trusting any
> exclusion list.

**Still open on this pipeline, recorded so it is not lost:** `whistle` sits in the same exclusion
list while `policy` is in the governance-title pattern, so a **Whistleblower Policy** — a core ASX
governance document, listed in the reference company's own footer — is dropped from every tenant's
governance page by the same mechanism. Nobody has fixed it. Guard any fix with a case that names
the documents and their hrefs: "4 documents mentioning slavery" passes on four copies of a policy
*about* the topic.

---

## The mandated page that was simply absent

**Measured on production 2026-08-08.** `temple-and-webster-group-ltd` had **no
`/corporate-governance` page and no `governanceSnapshot` section** — no route from the portal to any
governance material at all — while the other five portals carried, in the platform's own copy, the
sentence *"Listing Rule 4.10.3 lets the governance statement live at a URL, and that URL is lodged
with ASX under 4.7.4."*

The platform stated the obligation on five portals and shipped a sixth without it. The cause was an
evidence threshold applied to a levy: a correct mechanism for deciding whether a company gets a
`projectRail`, and the wrong one for deciding whether it gets a governance surface.

The research that followed sharpened this further, and the sharpening is a correction rather than a
confirmation. See `references/evidence.md`, E10: a visible `unavailable` is safer than a fabricated
value but **does not cure a legal omission**, so for a mandatory current governance statement
"not held" should be a publication block plus escalation rather than an honest surface — and one
undifferentiated `unavailable` cannot express the difference between "not required of this entity"
and "required and missing".

---

## The two tenants that were the same portal

**Measured on production 2026-08-08 across six live portals.** `metallium-ltd` and
`telstra-group-limited` — a junior explorer and Australia's largest telco — published the same
eight pages, with the same section kinds **in the same order on every one of them**, under the same
archetype. `jb-hi-fi-limited` matched Telstra on seven of eight *and* carried a byte-identical
WebGL vector, which the repo's own framebuffer probe scored at a still-distance of **1.169 against
a floor of 1.9**, decomposed as `shape 0.036 / ink 0.015 / churn 0.002` — **0.927 of the entire
distance is hue.** Strip the brand colour and they are indistinguishable.

Every per-tenant gate was green, and they could not be otherwise: **sameness is not a property of a
record, it is a property of a pair.**

Note *which* pair failed. The same-sector pair the design worried about — two retailers — scored
2.941 and was fine. It is the **cross-sector** pair that collapsed, because both sectors routed to
the house default preset.

And note the sampling frame. `portal-collision.mjs` reported **13 collisions over 53 published
pairs**, and four of those pairs were between tenants the six-portal review never opened, including
`ecargo-holdings-paid ↔ nh3-clean-energy-paid`, which collides on **all three axes at once** and is
worse than either pair the review named. A review that opens six of eleven tenants is a review with
a sampling frame; a pairwise gate has none.

---

## The emphasis rung that had never been won

**Measured on production 2026-08-08 across four emphasis-aware tenants and eleven pages.** The
emphasis-3 rung had **never once been won by a bid**. All four awards were the hero, taken as the
off-budget `pageOpener` levy. The mechanism: the rung was offered to the top-ranked bid *only*, so
if that bid had no audited dark rendering the rung was burned, and a dark-capable section ranked #2
could never reach it. That is a bug, and it is fixed — the rung passes down the ranking, and only a
page where *nothing* can express it reports it unspent.

The review that found it proposed a second fix, and **that one was declined**. Emitting
`data-emphasis` on every `<section>` so a rendered-layer gate could read the budget would put a
database field into the markup so a gate could confirm the database, which is a gate measuring its
own input — and it would break a deliberate assertion, *nothing that renders a page reads
`emphasis`*, which is the entire proof that the feature cannot move the parity reference.

The measurement then sharpened what the real defect is. At level 2 the budget maps to
`band: 'surface'`, which measures **1.08:1 against the canvas**. So after all of it, the visible
difference between two tenants' home pages is which of two sections carries a band 8% off white.
**The defect is not that emphasis is invisible to a gate. It is that emphasis is nearly invisible
to a reader.** Gate what a section renders, never what a record ranked.

---

## The zero-image paid portals

**Measured on production 2026-08-08.** Two of six live paid tenants — Temple & Webster and Telstra
— shipped with **zero images on every page**: a type-on-charcoal hero and text-list business pages,
for a paying listed company.

Nothing was broken. Every image each record declared loaded, and each declared none. That is
invisible to every gate on the pipeline, because each one asks *does what the record names actually
render?* and the answer was yes.

Find-before-generate has a failure mode nobody wrote down: finding yields nothing, generating is
declined, and the portal goes out with no photograph of the company on it anywhere. **An outcome
nothing reports is an outcome nobody chose.**

---

## The images that were about the wrong thing

On one portal every one of seven business units carried an image about a different subject from its
own heading:

| Unit heading | `alt` on the image beside it |
|---|---|
| REVOLUTIONARY FLASH JOULE HEATING TECHNOLOGY | "Icon representing metal recovery and **recycling**" |
| MINERAL EXPLORATION | "Hand holding a small glass bottle filled with gold recovered from **e-waste**" |
| RECYCLING | "**Map of Quebec, Canada** showing the Pomme Project" |

Every row off by one or more, from index-order placement across two lists built independently. A
screen-reader user on the RECYCLING unit is told about a map.

This is the recurring failure of generated surfaces in its purest form — present, 200, well-formed,
and about the wrong thing — and good alt text is what makes it *provable* rather than what causes
it. It is also machine-checkable, because the alt text and the heading are both fields in the record
you are emitting, which is why the gate compares them for a shared subject word.

The same blindness in the other direction cost more than money: index-based pairing on one run put
an identifiable employee's portrait against an unrelated business unit — a real named individual, on
a public investor page, illustrating something they have nothing to do with. **A person's photograph
is bound to that person, not to a position in a list.**

---

## The chrome that was an empty object

`chrome: {}` **validates**, and produces a portal with no brand, no navigation and no footer. On one
generator that literal shipped to **every record it had ever produced** — nine of them — and the
consequence was invisible everywhere it was checked: the records validated, every route returned
200, and the content assertions passed. Measured on one tenant, five pages carried **zero internal
links** and **one tab stop**, the skip link. Two declared routes resolved 200 with nothing on the
site pointing at them.

Four literals then survived the obvious "grep for the company name" pass on a real build, and every
one was found by **opening a generated tenant's footer and reading it**:

| What rendered on the second tenant | Cause |
|---|---|
| `ABN ᴹ` — the word, a space, and a lone illustrative-value marker | `abn: ''` rendered unconditionally |
| a **Share registry** heading over an empty marker and a link to `""` | `registry` / `registryUrl` rendered unconditionally |
| `© 2026 Metallium Ltd. 0 sites across NSW and Queensland.` | the reference's two *states*, hard-coded, under a Western Australian company, over a count of nothing |
| "the document lodged with **ASX**" | a literal venue, on every NASDAQ and NYSE tenant |

`ABN ᴹ` is also the accessibility failure the research names independently: an unavailable state has
to be readable text, not a colour-only or glyph-only marker (`references/evidence.md`, E5).
