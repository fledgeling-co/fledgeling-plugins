---
name: email-digest
description: Build a recurring multi-item digest or roundup email that survives contact with real inboxes - a tiered layout that absorbs volume instead of capping it, a table-based render that works in Outlook's Word engine and with images blocked, and a deterministic gate carrying every rule back to the evidence behind it. Use when someone wants to send a newsletter, changelog digest, product-announcement roundup, release notes email or "what shipped this week" to subscribers, when a digest has been called too long or unreadable, when an email needs checking before it goes out, or when a template needs auditing for accessibility, dark mode, Gmail clipping or Outlook rendering. Refuses the two fixes people reach for first, because the measured evidence goes the other way - it will not cap the item count and it will not gate on a text-to-image ratio. Not for transactional mail (receipts, password resets, alerts), cold outreach, or a single-announcement campaign, and not a sending pipeline; it produces and gates the message, and hands off to whatever already sends.
---

# email-digest

A digest that goes out with twenty-four items and comes back described as
unreadable has a real defect, and it is almost never the one people name.
Cutting the list is the intuitive fix and the evidence goes the other way:
MailerLite's 317,000 campaigns and 2.9 billion emails put the 21-or-more-links
bucket at the **highest** click-to-open rate in the dataset, and the
choice-overload meta-analysis pools to a mean effect size of virtually zero.

The defect is **undifferentiated scan cost per item**. Fifty-one seconds of
attention, every item costing the same fixation to evaluate, and nothing in the
visual field saying where to stop. Tiering fixes that. Truncation does not; it
just removes content somebody asked for.

So this skill does not cap the item count, and `scripts/lint_email.py` asserts
the absence of a cap as a rule, because that cap re-enters the code every time
somebody reasons from first principles instead of reading the evidence.

Full provenance for every rule: `references/evidence.md`. Read it when you need
to justify or change a rule, not on every run.

**Running as a Gemini model?** Read `gemini.md` in this directory first, then follow this file with the overrides it names. It gives every tier count, word bound and accent rule a readback command, converts the ux-craft / voice / design-craft routes into files the render depends on, and says why the gate reporting ok on zero tiers is not a pass. Other models skip it.

## What this produces

An HTML part, a plain-text part, and a gate report. It does not send. Whatever
already sends (an ESP, a cron route, a queue) keeps that job.

## Step 1 — Find the source and the brand

Discover rather than assume; a hard-coded map goes stale silently and only ever
fits one project.

- **The items.** A database collection, a JSON file, a changelog, a directory of
  markdown, an API. Ask if it is genuinely unclear; do not invent a schema.
- **The palette and marks.** Look for design tokens (`tokens.css`,
  `theme.ts`, a Tailwind config) and take the real values. Email clients do not
  resolve CSS custom properties, so tokens must be flattened to literals at
  build time.
- **Brand assets.** Note the format. **Gmail strips `<svg>` from the DOM
  entirely**, so a vector mark has to be rasterised before it can appear.
- **Where images are served from.** Every asset needs an absolute URL on a host
  the recipient can reach. A path that works on the site does not work in mail.

Where large imagery is wanted and only oversized source files exist, generate
email-sized derivatives with `scripts/email_assets.py`. A 3200px banner is not a
600px banner: the source assets in this marketplace average 663KB, and the
derivatives run 38 to 142KB. Serve them from somewhere the recipient can reach
before referencing them, and check the URL rather than assuming; a banner that
404s renders as a reserved gap with no error anywhere.

## Step 2 — Assign the tiers

**Route the tier decisions through `ux-craft` where it is installed.** An email
is a reading surface and `ux-craft` is the skill that owns those, emails
included by its own description. What it decides here that this skill does not:
the reading order, whether the summary block earns its position, and whether a
given item genuinely belongs in the featured tier or is only recent. Bring it
the item list and the constraints below rather than a finished template, because
by render time the decisions are already made.

Three tiers. The shape is not arbitrary: Kong et al.'s eight-week field
experiment is the only causal evidence in the corpus, and it found that
featuring relevant items raised their detail-reading from 13% to 22% while
**reordering everything below the featured block did nothing significant**.
Prominence earns the investment; ranking the tail does not.

| Tier | Count | Treatment |
|---|---|---|
| Featured | 2-4, default 2 | Full-column banner, headline, 25-55 words, one primary action and one subordinate |
| Spotlight | 2-5, default 3 | One row, three large icons side by side, title, one line |
| Also shipped | everything else | An icon, the title and a short tag, grouped under category headings |

**A banner is a wide crop, so it needs a wide column.** The featured tier has
one; a three-across row does not, and a banner at 168px is a strip of colour
with an illegible wordmark inside it. So the spotlight row leads with a **large
icon** instead, at around 112px, because an icon is drawn to survive being
small. The tail rows carry the same icon at 24px.

This is not the shape NN/g measured badly. That finding is about a **thumbnail
beside a paragraph** competing with the text it sits next to; an icon leading a
column, at four times a thumbnail's size, with a title under it rather than
beside it, is a different object. If you put a small square next to a line of
body copy, you have built the thing that tested badly.

**Point the tail at a small derivative.** Eighteen rows aimed at 256px card
icons cost the recipient most of a megabyte to render a 24px square.
`email_assets.py --icon <src> --size 24` writes the 48px file; roughly 3KB each.

The row is a real table with pixel column widths, collapsing to full width under
620px. Outlook has no flex and no grid but lays a table out correctly, and the
clients that ignore the media query are the desktop ones with the room anyway.

**Where banners do share a row, conform them to one ratio first.** Sources drift
off whatever house ratio a project has, and at full width nobody notices; in a
row they align at the top and finish at different heights, which reads as a
broken layout rather than as a mismatched asset. `email_assets.py --aspect
1000:325` pads the short ones with their own edge colour rather than cropping
the artwork.

### A fourth block, where the digest has long-form behind it

Some of the items exist because a piece of research said they should, and that
research is a different class of thing from the items: longer, older than the
week, and read for a different reason. It gets its own block rather than a tier,
two tiles across at 260px, set on their own ground so the reader can see at a
glance that they have left the list.

Two tiles, not three. Each carries a headline and a sentence of what was found,
and at the three-across width of 168px that sentence sets to four or five words
a line. One tile reads as an orphan rather than a section.

**The ground colour goes on the cell, never on the image.** A tile whose dark
field arrives as artwork becomes light text on the email's paper the moment
images are blocked, which is a client default rather than an error state.
Everything textual stays live text for the same reason, and `research:ground`
fails the render that gets this wrong.

Give it `research.palette` matching wherever the research is actually published.
A tile that does not resemble the page it leads to is a worse tile than a plain
one. The block sits between the middle tier and the tail: the reader has been
through the items chosen for them, the long list is still ahead, and Kong et al.
found ordering that tail changes nothing, so this is the last position in the
email where placement is worth anything.

Two rules that are easy to get wrong:

- **Featured items are chosen for relevance, not recency.** The Kong effect is
  conditional on the featured item mattering to that reader. Position is a weak
  proxy. If the source knows better (engagement, category, an editor's pick),
  pass an explicit `tier` per item and say what the ranking was.
- **Every banner is decorative and carries `alt=""`.** The headline lives beside
  it as a text node in both banner tiers, because the banner's failure modes
  (blocked, broken, alt clipped to the image width, alt unstylable in Outlook)
  all land on the same element and take the AI-generated inbox summary with
  them. Every tier has to read completely with images stripped.

## Step 3 — Write the copy

**Every word of it goes through the project's voice skill.** Not the subject
only, and not the featured paragraphs only: the subject, the preheader, the
heading, the three summary lines, both featured headlines and bodies, and every
one-line tag in both lower tiers. A digest whose featured copy was written
properly and whose eighteen tail lines were not reads as two different people,
and the tail is where most of the words are.

Pick the skill by who the mail is from. A named person or brand signs it, so
`create-luke-content` for Luke, `create-diolog-content` for Diolog, or whatever
persona owns that byline; `agent-voice` only where nobody's name is on it. This
skill owns structure, not voice.

Two things that go wrong when the routing is skipped:

- **Item copy drifts technical**, because the source it is drawn from is a
  README or a spec written for somebody already inside the problem. "Picks the
  release lane from the fingerprint, not from intent" and "Works out whether a
  release needs the App Store or not" describe the same skill, and only one of
  them survives contact with a reader who has not used it.
- **The lines start rhyming.** Twenty-three tags written in one pass converge on
  one sentence shape. `create-luke-content`'s `voice_lint.py` flags a repeated
  rhetorical phrase for exactly this reason; run it over the whole set at once
  rather than per item, which is the only way it can see the repetition.

Four things the structure needs from the copy:

- **A subject that names something specific**, with any count secondary.
  `24 new skills` fails the gate. A bare number sets a scope expectation without
  a relevance one, and the only causal evidence available is that naming a
  relevant item raises that item's detail-reading.
- **A subject that varies per issue.** Gmail threads same-subject messages and
  evaluates the thread's *combined* size against its clip threshold, so a
  recurring digest with a stable subject eventually clips no matter how small
  each issue is. A count varies for free.
- **No prose paragraph before the first item.** NN/g measured **67% of readers
  with zero fixations** on three-line intros. The summary block replaces it.
- **A summary of exactly three highlights plus category counts**, every link
  pointing outward to its destination. Not a contents list, which recreates the
  flat list above the flat list.
- **Set it as a summary, not as a to-do list.** Three bulleted lines read as
  three items to work through; the same three set as statements on a tinted
  ground, with the linked name carrying the weight, read as one block the reader
  takes in and moves past. What it must not become is a prose paragraph: the
  NN/g result below indicts prose specifically, and separate short lines are the
  object the same heatmaps show people reading.
- **Say what the items were used on, where you can source it.** A highlight that
  names the work ("three projects closed out behind this one") answers the
  question a list of titles does not, and it is the relevance signal the Kong
  result turns on. A highlight may be composed of `parts`, so one line can name
  the project in plain text and still link each skill to its own page. Measure
  it rather than asserting it: repository history, ticket references and build
  logs all carry the join, and an invented one is worse than none.

Length guidance for subjects is a truncation constraint, not a performance
lever: three large datasets give three different optima and an academic study
across 455 million users found no direct relation at all. The gate warns and
never fails on it.

## Step 4 — Render

**Route the visual treatment through `design-craft` where it is installed**, with
`ux-craft`'s lens still on it: they are a pair rather than alternatives.
`design-craft` decides the palette (taken from the project's own tokens and
flattened to literals, since Gmail supports `var()` but not the declaration),
the type scale, and how much visual weight actually separates the three tiers.
The renderer below ships a default palette so it runs standalone; that default is
a starting point, not a design.

Two things `design-craft` will decide differently from the default, and both
are worth stating because they are easy to get backwards:

- **Take the fonts from the project, and let each stack end web-safe.** A linked
  web font loads in Apple Mail and iOS Mail, which is 62.26% of opens; Gmail
  ignores the link entirely. So the fallback is not a formality, it is what most
  Gmail readers actually see, and it should be a face somebody chose. Hide the
  `<link>` from Outlook with a downlevel-revealed comment. Pass the stacks
  through `brand.fonts`.
- **One primary action per card, and the accent appears once.** Two calls to
  action stacked as separate rows read as a list of two similar choices. Put
  them on one row as a two-cell table, give the primary the filled accent, and
  demote the secondary to the muted foreground with an underline: an
  accent-coloured link beside an accent-filled button is two claims on the same
  emphasis. In a digest the primary is the item's own page, because the reader
  is deciding whether this is worth their attention rather than deciding to
  install.

```bash
python3 scripts/render_digest.py payload.json --out-html mail.html --out-text mail.txt
python3 scripts/render_digest.py --example        # the payload shape
```

The renderer compiles to nested tables with inline styles, because Outlook for
Windows renders through the Microsoft Word engine and Gmail publishes a CSS
allowlist that excludes `position`, every flex child property, every grid
property, `transform`, `transition` and `animation`. Modern CSS is a
progressive enhancement on a layout that already works without it.

Use it, or write your own template against the same rules. If you write your
own, the gate is what makes the two equivalent.

## Step 5 — Gate

```bash
python3 scripts/lint_email.py mail.html --text mail.txt --subject "<subject>"
```

Exit 0 clean, 1 on any error. **Read the exit code, not the output** — piping
through `grep` or `tail` reports the pipe's status and has already turned a
failure into a pass once during this skill's own development.

Nineteen checks. The ones that catch real defects most often:

- **`tiers`** — no tier markers means every tier rule below is measuring
  nothing while still printing a verdict. This failed silently on the first
  render here.
- **`prose-intro`** — a paragraph over 180 characters before the first item.
- **`research:ground`** — a research tile with no background on the cell. The
  tile is dark against a light email, so with images blocked it inverts into
  unreadable light-on-paper rather than degrading.
- **`summary:anchors`** — any `href="#"`. Anchors do not act in Apple Mail,
  Gmail, Outlook or Yahoo on iPhone and iPad, Apple is 62.26% of opens, and
  anchor clicks bypass ESP redirect tracking so the block cannot even be
  measured where it works.
- **`a11y:table-role`** — `role="presentation"` on every layout table,
  including nested ones, because the role is not inherited. 86.24% of a
  443,585-email corpus fails this.
- **`a11y:alignment`** — the outer `align="center"` that centres the card
  cascades `text-align` into every descendant, so an email can be centred
  throughout without anyone writing `text-align:center` once. That is how it
  reached a render here.
- **`css:svg`** — Gmail strips the tag; the mark vanishes rather than degrading.
- **`dark:commitment`** — the colour-scheme meta tags are a promise. Apple Mail
  leaves markup alone without them and *partially inverts* with them and no
  dark styles, so declaring support you have not built is worse than declaring
  none.
- **`size:budget`** — 90KB against Gmail's ~102KB clip, leaving headroom for the
  ESP's tracking rewrite, which lands after this runs. Clipping truncates
  mid-markup and can take the unsubscribe link with it.
- **`images-off`** — strips every image and asserts the content survives.

### What this gate does not cover, and who does

`lint_email.py` is the email-specific half. The general reading-surface half is
`ux-craft`'s `ux-lint.py`, and running both is the intended shape:

```bash
python3 <ux-craft>/scripts/ux-lint.py --static mail.html
```

| Concern | Gated by | Why there |
|---|---|---|
| Clipping, Word-engine CSS, SVG stripping, dark-mode inversion, image blocking, anchor failure, tier shape, prose intro, layout-table roles | `lint_email.py` | Email-medium rules with no web equivalent. Layout-table roles land here because only email forces tables in the first place. |
| Colour contrast, touch-target size, vague link labels, alt coverage | `ux-lint.py` | General reading-surface rules it already gates properly. `lint_email.py` checks alt and link text too; treat the overlap as belt and braces rather than duplicating it further, and do not add contrast here. |

Two of `ux-lint.py`'s checks do not transfer to email, and the run should say so
rather than either fixing or ignoring them. **`no-focus-visible`**: Gmail's
published CSS allowlist has no pseudo-class support, so a `:focus-visible`
treatment cannot render in the medium at all. **`state-coverage`**: an email has
no states to cover. Everything else it reports is real, and it caught dead CSS
here that this gate did not.

Two things `lint_email.py` deliberately does not do:

- **It does not cap items.** See the top of this file.
- **It does not gate a text-to-image ratio.** Email on Acid tested against 23
  spam filters and found that at 500+ characters the ratio does not affect
  deliverability; Badsender files the rule under deliverability myths. Gate
  against image-*only* communication instead, which `images-off` does.

## Step 6 — Look at it

Serve the HTML and open it. The gate proves the email renders and is reachable;
only reading it proves it is worth reading. Check with images blocked as well as
loaded, because that is the state a meaningful share of Outlook recipients see
and it is the state the gate can only partly simulate.

Then hand off to whatever sends.

## What this skill will not do

- **Send.** It produces and gates a message.
- **Choose a metric for you, beyond refusing a broken one.** Open rate cannot
  select a winner: Apple's Mail Privacy Protection downloads remote content
  regardless of engagement and Apple is 62.26% of opens, which breaks open rate
  and takes click-to-open with it, since CTOR divides by the same number. Use
  bot-filtered unique clickers per delivered email.
- **Promise the tiering works.** No published study compares a tiered
  multi-item email against a flat list of the same items. Four independent
  research backends searched for one and none found it. The design is an
  inference from four measured results, and the honest way to settle it is a
  randomised split in your own programme measuring read time and per-tier click
  penetration.

## Routes to

| Skill | For |
|---|---|
| `ux-craft` | Tier decisions, reading order, and the general reading-surface gate |
| `design-craft` | Palette from the project's tokens, type scale, tier weighting |
| `create-luke-content` / `create-diolog-content` / a named persona | Every word of prose, where a person or brand signs the mail |
| `agent-voice` | Every word of prose, where nobody's name is on it |

Where one is not installed, say which substitution you made rather than
implying the pass happened.

## References

`references/evidence.md` — every rule, its class of evidence, and the eight
widely-repeated figures that could not be traced to any primary source.
`references/payload.md` — the payload schema and per-item fields.
