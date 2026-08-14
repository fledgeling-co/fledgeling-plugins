# The three readings — Primer, Brief, Technical

One report, three registers, one ledger. The reader chooses which one they get;
the evidence underneath does not change.

## What each reading is for

| Reading | Written for | What it does | What it may assume |
|---|---|---|---|
| **Primer** | someone meeting the subject for the first time, around an 11-year-old reading level | carries the finding as something concrete, with an analogy doing the work a definition would otherwise do | nothing. Every term it uses, it introduces |
| **Brief** | the informed non-specialist — the person who has to decide something | says what was found, what it means, and what should happen | general literacy in the domain's *consequences*, not its mechanisms |
| **Technical** | someone who will check the work | mechanism, numbers, method, limits, and the shape of the uncertainty | the field's vocabulary and that the reader wants the apparatus |

`brief` is the default. It is the reading that lands when a link is shared with
no fragment, the reading a search engine indexes, and the reading the PDF
exports as unless a different one is asked for.

The names describe the *document*, never the reader. "Primer" is a book that
starts at the beginning, which is a respectable thing for a document to be.
Nothing in the UI grades the person choosing.

## The rule that makes three readings honest

> A reading may change the words. It may never change what is claimed.

Simplifying is choosing shorter words for the same proposition. Dropping the
caveat that bounds a number is not simplification — it is a different and
stronger claim, and it is the one the Primer reading produces by default unless
this is enforced. The failure is quiet, because the simplified sentence reads
*better*: "the cache is why your bill is bigger" is cleaner prose than "cache
reads are 95.4% of tokens sent in this sample, which is not the same as 95.4% of
spend."

Four consequences, all checkable:

- **Confidence survives every reading.** A claim held at low confidence hedges
  in all three. The Primer hedges in Primer language — "we think, but we are not
  certain" — rather than dropping the hedge because it is hard to say simply.
- **An inference is marked as an inference in all three.** `data-kind` sits on
  the block, above the readings, so this holds structurally rather than by
  discipline.
- **Limits travel.** If the Technical reading says a figure covers one tenant
  over 28 days, the Primer says "we only looked at one customer, for a month."
  A number whose scope is dropped becomes a claim about everything.
- **A re-expressed number stays arithmetically the same number.** Primer may
  round and may change the unit — 95.4% becoming "about 19 in every 20" is a
  real translation and a good one. It may not drop the unit, invert the
  direction, or lose an order of magnitude. Record the re-expression in the
  ledger so it was authored once rather than improvised into the page.

## The ledger carries all three

`claims.json` gains a `readings` object per claim. The claim's `text` stays the
canonical statement; `readings` holds how each register says it.

```json
{
  "id": "c7",
  "text": "Cache reads were 95.4% of tokens sent across the 28-window sample.",
  "kind": "direct",
  "confidence": "high",
  "sources": ["s3"],
  "support": "logs/bench-2026-08-07.txt:1180-1204, summed per window",
  "limits": "One tenant, 28 consecutive days. Not a spend share — see c9.",
  "readings": {
    "primer": "Almost 19 out of every 20 words sent were ones the computer had already seen before.",
    "brief": "95.4% of the tokens we send are cache reads, so the headline rate is not the rate you pay.",
    "technical": "Cache-read share is 95.4% of 3.48B raw tokens, n=340 observations across 28 windows."
  }
}
```

**Omitting a claim from a reading is allowed and must be declared.** A
twelve-claim technical argument rendered whole for a first-time reader is not a
Primer, it is the same document with shorter words. Where a claim genuinely does
not belong in a register, say so:

```json
"omit": ["primer"],
"omitReason": "A per-window variance figure has no Primer form that is both true and useful; c7 carries the finding it supports."
```

Two claims may never be omitted from any reading: **the finding** and **the
ask**. A reader who gets a register without the conclusion has been given a
different document, not a simpler one.

## The markup

The root carries the active reading. Blocks are shared; only the prose swaps.

```html
<html lang="en" data-reading="brief">
  …
  <section class="block" id="b3" data-claims="c7" data-kind="direct">
    <h2 data-reading="primer">Why the bill is bigger than the price</h2>
    <h2 data-reading="brief">Cache reads dominate the token bill</h2>
    <h2 data-reading="technical">Cache-read share across the 28-window sample</h2>

    <div class="say" data-reading="primer">
      <p>Almost 19 out of every 20 words…<a class="cite" href="#r3" data-cite="r3"
         data-n="3" aria-describedby="r3">3</a></p>
    </div>
    <div class="say" data-reading="brief">…</div>
    <div class="say" data-reading="technical">…</div>
  </section>
```

`data-reading` is space-separated, so a paragraph serving two registers carries
`data-reading="brief technical"` rather than being written twice. Prefer that to
duplication: two copies of a sentence drift apart on the first edit.

The CSS that resolves it is in **The toggle** below — it is written as a
hide-the-others rule rather than a show-the-match rule, for reasons that are not
stylistic.

**Every reading cites.** The citation markers live inside each register's own
prose, because the span a source supports is a different span in each wording.
The registry at the foot is shared and appears once.

## The toggle

Three requirements decide the design, and they are in tension:

1. It has to work with JavaScript off, because the citation contract already
   promises the document survives that.
2. It must not cost the reader their place. Registers have different lengths,
   so a naive swap moves the text under the reader's eyes.
3. It has to be shareable — sending someone "the technical one" is most of why
   three readings exist.

**Radio inputs plus `:has()` carry the mechanism.** No script involved:

```html
<fieldset class="readings">
  <legend>Read this as</legend>
  <input type="radio" name="reading" id="rd-primer" value="primer">
  <label for="rd-primer">Primer<span>from scratch</span></label>
  <input type="radio" name="reading" id="rd-brief" value="brief" checked>
  <label for="rd-brief">Brief<span>what it means</span></label>
  <input type="radio" name="reading" id="rd-technical" value="technical">
  <label for="rd-technical">Technical<span>how we know</span></label>
</fieldset>
```

```css
html:has(#rd-primer:checked)    [data-reading]:not([data-reading~="primer"]),
html:has(#rd-brief:checked)     [data-reading]:not([data-reading~="brief"]),
html:has(#rd-technical:checked) [data-reading]:not([data-reading~="technical"]) { display: none; }
```

**Hide the inactive registers; never show the active one.** The obvious form of
this rule reads `[data-reading] { display: none }` plus a `display: revert` on
the match, and it is wrong twice over. It flattens a `<figure>`, an `<h2>` and a
`<div>` onto one display value, and — measured on Obscura, 14 Aug 2026 —
`display: revert` computes to `none` rather than to the UA default, so the whole
page renders blank on the engine that reviews it. `:has()` itself works there
and `CSS.supports('selector(:has(*))')` correctly returns true; `revert` is the
half that fails, which is precisely the kind of divergence a support query
cannot tell you about.

The inverted form also fails better. On an engine without `:has()`, nothing is
hidden and the reader gets all three registers stacked — redundant, but complete
and still fully cited. The other way round, the same engine hides everything and
serves a blank document.

The `<html data-reading>` attribute is then the script-side mirror of the same
state, kept in sync so print and deep-links have one thing to read.

The one-line description under each name is not decoration — a three-way control
whose options are single abstract nouns makes the reader click to find out what
they get, and most will not. Say what each one is.

**Keep the reader's place.** Before switching, record the id of the topmost
block intersecting the viewport; after switching, scroll that block back to the
same offset. Without this the reader lands somewhere arbitrary and reads the
switch as the page breaking.

**Deep-link both ways.** `?reading=technical` and `#technical` both set the
register; a block fragment (`#b7`) still resolves. Precedence: URL, then
`localStorage`, then `brief`. The URL wins so a shared link lands where the
sender meant rather than where the recipient last was.

**States.** The control is a real fieldset with real radios, so keyboard and
screen-reader behaviour comes free — do not rebuild it from `div`s. The current
option is distinct by more than colour (weight and a rule, not a tint alone),
`:focus-visible` shows a ring, hit targets clear 44px, and the transition runs
150–250ms and not at all under `prefers-reduced-motion: reduce`.

**Announce the change.** Switching register replaces most of the page's text
with no visible motion, which a screen-reader user has no way to notice. One
`aria-live="polite"` region saying "Technical reading" on change — and only on
change — covers it. This is the one place a live region is right; do not fire
one per block.

**Reviewing a register means rendering it, not clicking it.** Measured on
Obscura, 14 Aug 2026: setting `.checked` from script does not re-evaluate the
`:has()` selector, so every register reads identically to a probe that toggles
and re-measures. The state set in the *served source* resolves correctly — all
three verified, including a `data-reading="brief technical"` element appearing
in exactly those two. So to review three registers, serve three renders with a
different radio `checked` in each, and capture each one. A single render plus
scripted clicks measures the same register three times and reports it as three
passes.

## Reading and theme are independent

Two axes, two attributes, no interaction between them:

```css
:root { /* the complete light palette lives here, unconditionally */ }
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { /* dark overrides */ }
}
:root[data-theme="dark"] { /* the same dark overrides, so the toggle wins */ }
@media print {
  :root, :root[data-theme="dark"] { /* light values again, unconditionally */ }
}
```

Never give a colour its only definition inside a media query or a `[data-theme]`
block. A token defined only in the dark branch is undefined in print, and the
failure renders as black-on-black in the one artifact nobody previews.

**Print is always light, and always one reading.** Ink is expensive and a dark
report on paper is a different document. The PDF stamps which register it is —
a line in the running header reading *Technical reading* — because a PDF with no
such mark is ambiguous the moment it is forwarded.

**Both themes are measured, not just authored.** Contrast, focus visibility and
divider gutters are checked in light *and* dark. A dark palette assembled by
inverting a light one passes by luck if it passes at all, and the theme nobody
measured is the theme that ships broken.

## Visuals per reading

Same data, same claim, same scales wherever parallelism allows — what changes is
how much of the apparatus is on screen.

| Reading | The figure shows | Interaction is | Labelling |
|---|---|---|---|
| **Primer** | one comparison, the finding only | play — tap or drag to reveal, no controls to learn | direct labels on the marks; no legend, no axis the reader must decode |
| **Brief** | the comparison that carries the decision | filtering to the reader's own case | direct labels, units named in words |
| **Technical** | the distribution, the uncertainty, the outliers | inspection — hover readouts, brushing, a table behind a disclosure | full axes, units, n, and the interval |

Three rules hold across all three, and they are the ones that make the set
trustworthy rather than three different arguments:

- **The scales agree.** If Primer rounds an axis and Technical does not, the two
  figures are making different claims and a reader who switches sees the data
  change. Round the *labels*, never the geometry.
- **Every reading's figure ships its static frame.** Print runs no animation and
  neither does a browser with script off. This is already the rule for animated
  blocks; three readings means three static frames, not one.
- **A figure omitted from a register follows its claim.** If the claim is
  omitted with a reason, its figure goes too. A chart with no accompanying claim
  is decoration that survived an edit.

## Writing the three

Route every word through `create-luke-content`, once per reading, and give it
the ledger rows rather than the finished prose of another register. Three passes
from the ledger produce three registers of the same argument; one pass plus two
rewrites produces one register and two translations of it, which read as
translations.

The voice does not change across readings. Luke writing for an eleven-year-old
is still Luke — shorter sentences, concrete nouns, an analogy carrying the
weight — not a different author. A Primer reading that sounds like a children's
textbook has substituted a persona for a register.

Where `create-luke-content` is not installed, say which substitution you made in
the methods note. A run that silently wrote its own prose and a run that had no
voice skill available look identical afterwards, and only one of them is fine.

## What the auditor enforces

`scripts/audit_report.py` checks the contract, and every check below exists
because the honest version and the broken version look the same on screen:

- **Each reading, alone, is fully cited.** The page is sliced to shared content
  plus one register's blocks, and cite→source and source→cite integrity run on
  that slice. Three passes. A Primer that lost its markers during simplification
  fails here and nowhere else.
- **The registry is shared and complete.** One `<li id="rN">` per source, cited
  from at least one reading.
- **Claim parity.** Every ledger claim reaches every reading, or carries `omit`
  with an `omitReason`. The finding and the ask may not be omitted at all.
- **Every claim has all three `readings` strings**, or an omission covering the
  missing one.
- **The default register renders without script.** `<html data-reading>` is
  present in the source and one register is `checked` in the markup.
- **Print resolves to exactly one reading**, and the print block defines every
  token it uses.
