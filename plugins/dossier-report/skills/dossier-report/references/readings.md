# The three readings — Primer, Brief, Technical

One page, three registers, one claim graph. The reader chooses which one
they get; the evidence underneath does not change.

## What each reading is for

| Reading | Written for | What it does | What it may assume |
|---|---|---|---|
| **Primer** | someone meeting the subject for the first time, around an 11-year-old reading level | carries the finding as something concrete, with an analogy doing the work a definition would otherwise do | nothing. Every term it uses, it introduces |
| **Brief** | the informed non-specialist — the person the page is trying to change the mind of | says what was found, what it means, and what follows | literacy in the topic's *consequences*, not its mechanisms |
| **Technical** | someone who will check the work | mechanism, numbers, method, limits, and where the backends disagreed | the field's vocabulary and that the reader wants the apparatus |

`brief` is the default: the register a bare link lands on, the one the
`og:description` quotes, and the one a search engine indexes.

The names describe the *document*, never the reader. "Primer" is a book
that starts at the beginning, which is a respectable thing for a page to
be. Nothing in the UI grades the person choosing.

**This is the page's widest reach, and it is why it is worth the work.** A
dossier page is published to a public subdomain and shared as a link. One
register serves one audience; three serve the specialist who will check
it, the person who has to act on it, and the reader who would otherwise
have bounced at the first unexplained term — measured at ~38% of arrivals
leaving immediately.

## The rule that makes three readings honest

> A reading may change the words. It may never change what is claimed.

Simplifying is choosing shorter words for the same proposition. Dropping
the caveat that bounds a number is not simplification — it is a different
and stronger claim, and it is the one the Primer reading produces by
default unless this is enforced. The failure is quiet, because the
simplified sentence reads *better*.

On this skill's pages the risk is sharper than on an internal report,
because the page is published under a real name and its whole argument is
usually that somebody else overclaimed. Four consequences, all checkable:

- **Confidence survives every reading.** A claim held at low confidence
  hedges in all three, in that register's own language.
- **An inference is marked as an inference in all three.** `data-kind`
  sits on the block, above the readings, so this holds structurally.
- **Limits travel.** A figure whose scope is dropped becomes a claim about
  everything.
- **A disagreement between backends survives into every register.** Where
  the panel split, the Primer says so in Primer words — "the people who
  looked at this do not agree yet" — rather than picking the tidier side
  because the disagreement is hard to say simply. Silently resolving a
  split for a simpler register is exactly the overclaiming this skill
  exists to prevent, committed against your own corpus.
- **A re-expressed number stays the same number.** Primer may round and
  change the unit — 95.4% becoming "about 19 in every 20" is a real
  translation. It may not drop the unit, invert the direction, or lose an
  order of magnitude. Record the re-expression in the claim graph so it
  was authored once rather than improvised into the page.

## The claim graph carries all three

Every claim gains a `readings` object beside its existing fields. The
claim's canonical `text` does not move; `readings` holds how each register
says it.

```json
{
  "id": "c7",
  "text": "Cache reads were 95.4% of tokens sent across the 28-window sample.",
  "kind": "direct",
  "confidence": "high",
  "sources": ["s3", "s11"],
  "support": "Perplexity report §4, table 2; corroborated in the Gemini run §6",
  "limits": "One vendor, 28 days. Not a spend share.",
  "readings": {
    "primer": "Almost 19 out of every 20 words sent were ones the computer had already seen.",
    "brief": "95.4% of the tokens sent are cache reads, so the headline rate is not the rate paid.",
    "technical": "Cache-read share is 95.4% of 3.48B raw tokens, n=340 across 28 windows."
  }
}
```

**Omitting a claim from a reading is allowed and must be declared** —
`omit` with an `omitReason`. A twelve-claim argument rendered whole for a
first-time reader is not a Primer, it is the same page with shorter words.

Two things may never be omitted from any reading: **the finding** and
**the page's editorial tension** — the contested question at its centre. A
register that resolves the tension the other two leave open is a different
page, and a page with no tension anywhere reads as generated.

## The markup

The root carries the active reading. Blocks are shared; only the prose and
the figure treatment swap.

```html
<html lang="en" data-active-reading="brief">
  …
  <section class="ep" id="s3" data-claims="c7" data-kind="direct">
    <h2 data-reading="primer">Why the bill is bigger than the price</h2>
    <h2 data-reading="brief">Cache reads dominate the token bill</h2>
    <h2 data-reading="technical">Cache-read share across the 28-window sample</h2>

    <div class="say" data-reading="primer">
      <p>Almost 19 out of every 20…<a class="cite" href="#r3" data-cite="r3"
         data-n="3" aria-describedby="r3">3</a></p>
    </div>
    <div class="say" data-reading="brief">…</div>
    <div class="say" data-reading="technical">…</div>
  </section>
```

`data-reading` is space-separated, so a paragraph serving two registers
carries `data-reading="brief technical"` rather than being written twice.
Prefer that to duplication: two copies of a sentence drift on the first
edit.

**Every reading cites.** Markers live inside each register's own prose,
because the span a source supports is a different span in each wording.
The registry at the foot is shared and appears once.

## The toggle

Three requirements decide the design, and they are in tension:

1. It works with JavaScript off, because the citation contract already
   promises the page survives that.
2. It must not cost the reader their place. Registers differ in length, so
   a naive swap moves the text under the reader's eyes.
3. It has to be shareable — sending someone "the technical one" is most of
   why three readings exist on a published page.

**Radio inputs plus `:has()` carry the mechanism**, with no script:

```html
<fieldset class="readings">
  <legend class="sr">Read this as</legend>
  <span class="readings-label" aria-hidden="true">Read this as</span>
  <input type="radio" name="reading" id="rd-primer" value="primer">
  <label for="rd-primer"><b>Primer</b><span>from scratch</span></label>
  <input type="radio" name="reading" id="rd-brief" value="brief" checked>
  <label for="rd-brief"><b>Brief</b><span>what it means</span></label>
  <input type="radio" name="reading" id="rd-technical" value="technical">
  <label for="rd-technical"><b>Technical</b><span>how we know</span></label>
</fieldset>
```

```css
html:has(#rd-primer:checked)    [data-reading]:not([data-reading~="primer"]),
html:has(#rd-brief:checked)     [data-reading]:not([data-reading~="brief"]),
html:has(#rd-technical:checked) [data-reading]:not([data-reading~="technical"]) { display: none; }
```

**Hide the inactive registers; never show the active one.** The obvious
form — `[data-reading] { display: none }` plus `display: revert` on the
match — is wrong twice. It flattens a `<figure>`, an `<h2>` and a `<div>`
onto one display value, and, measured on Obscura 14 Aug 2026,
`display: revert` computes to `none`, so the page renders blank on the
engine that reviews it. `:has()` itself works there, and
`CSS.supports('selector(:has(*))')` correctly returns true — which is
exactly why a support query is no defence.

The inverted form also fails better: without `:has()` nothing is hidden
and the reader gets all three registers stacked — redundant, complete and
still fully cited. The other way round, the same engine serves a blank
page.

**Two construction rules that look like nitpicks and are not**, both
measured on the same engine:

- **Wrap every text run in an element.** A bare text node is not wrapped
  into an anonymous flex item, so `Primer<span>desc</span>` inside a
  column flex container puts the description *beside* the word and
  collapses the label to one line — while `display`, `flexDirection` and
  the span's own `display: block` all read correct. Use `<b>` and block
  stacking.
- **Carry the current state on border, background and weight, never on a
  `box-shadow`.** Obscura does not paint one, so a state signal riding on
  it is invisible in every review capture.

**Keep the reader's place.** Before switching, record the id of the
topmost episode intersecting the viewport; after switching, scroll it back
to the same offset. Without this the reader lands somewhere arbitrary and
reads the switch as the page breaking.

**Deep-link both ways.** `?reading=technical` and `#technical` both set
the register, and a block fragment still resolves. Precedence: URL, then
`localStorage`, then `brief` — the URL wins so a shared link lands where
the sender meant.

**Announce the change.** Switching replaces most of the page's text with
no visible motion, which a screen-reader user has no way to notice. One
`aria-live="polite"` region on change, and only on change.

**Reviewing a register means rendering it, not clicking it.** Setting
`.checked` from script does not re-evaluate `:has()` on Obscura, so a
scripted toggle measures the same register three times and reports three
passes. Serve three renders with a different radio `checked` in each.

## Reading and theme are independent

Two axes, two attributes, no interaction between them. Light is defined
unconditionally on bare `:root`; dark only ever overrides, written twice —
once under `prefers-color-scheme: dark` guarded as
`:root:not([data-theme="light"])`, and once under `:root[data-theme="dark"]`
so the control wins in both directions.

Never give a colour its only definition inside a media or `[data-theme]`
block, and give `body` an explicit token background. Both themes are
**measured**, not just authored: contrast, focus visibility and divider
gutters are checked in light *and* dark. A dark palette assembled by
inverting a light one passes by luck if it passes at all.

The theme control is script-created on purpose: with JavaScript off the
page already follows the OS preference, so a dead button would be worse
than none. The *reading* control is the opposite — it is content, and
works unaided. Three theme states, so "auto" stays reachable after a
manual choice.

## Visuals per reading

Same data, same claim, same scales wherever parallelism allows. What
changes is how much apparatus is on screen.

| Reading | The figure shows | Interaction is | Motion budget |
|---|---|---|---|
| **Primer** | one comparison, the finding only, direct labels, no legend | play — tap or drag to reveal, nothing to learn | largest: reveal and analogy carry a first-time reader |
| **Brief** | the comparison that carries the argument | filtering to the reader's own case | moderate |
| **Technical** | the distribution, the interval, the outliers, a table behind a disclosure | inspection — hover readout, brushing | smallest: little motion, much inspection |

Three rules hold across all three:

- **The scales agree.** Round the *labels* for Primer, never the geometry.
  A reader who switches and sees the data change has caught the page lying
  in one of the two.
- **Every register's figure renders from its own state**, and no claim
  exists only inside an animated intermediate frame. Readers skip faster
  than animations complete, in every register.
- **A figure omitted from a register follows its claim.**

## Writing the three

Route every word through `create-luke-content`, once per reading, giving
it the claim-graph rows rather than the finished prose of another
register. Three passes from the graph produce three registers of one
argument; one pass plus two rewrites produces one register and two
translations of it, and it reads that way.

The voice does not change across readings. Luke writing for an
eleven-year-old is still Luke — shorter sentences, concrete nouns, an
analogy carrying the weight — not a different author. A Primer that sounds
like a children's textbook has substituted a persona for a register.

## What the auditor enforces

`scripts/audit_page.py` checks the contract, and every check exists
because the honest version and the broken version look the same on screen:

- **Each reading, alone, is fully cited** — the page is sliced to shared
  content plus one register, and cite→source integrity runs on that slice.
  Three passes. A Primer that lost its markers during simplification fails
  here and nowhere else.
- **Every sourced claim carries a marker in each register that renders
  it**, somewhere on the page rather than in every block that mentions it.
- **The registry is shared and complete**, cited from at least one
  reading.
- **The default register renders without script** — one radio `checked` in
  the markup and `<html data-active-reading>` mirroring it.
- **Both themes are declared**, and no token is defined only in a dark
  block.
