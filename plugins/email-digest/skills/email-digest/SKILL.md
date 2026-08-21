---
name: email-digest
description: Build a recurring multi-item digest or roundup email that survives contact with real inboxes - a tiered layout that absorbs volume instead of capping it, a table-based render that works in Outlook's Word engine and with images blocked, and a deterministic gate carrying every rule back to the evidence behind it. Use when someone wants to send a newsletter, changelog digest, product-announcement roundup, release notes email or "what shipped this week" to subscribers, when a digest has been called too long or unreadable, when an email needs checking before it goes out, or when a template needs auditing for accessibility, dark mode, Gmail clipping or Outlook rendering. Refuses the two fixes people reach for first, because the measured evidence goes the other way - it will not cap the item count and it will not gate on a text-to-image ratio. Not for transactional mail (receipts, password resets, alerts), cold outreach, or a single-announcement campaign, and not a sending pipeline: it produces and gates the message, and hands off to whatever already sends.
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
600px banner.

## Step 2 — Assign the tiers

Three tiers. The shape is not arbitrary: Kong et al.'s eight-week field
experiment is the only causal evidence in the corpus, and it found that
featuring relevant items raised their detail-reading from 13% to 22% while
**reordering everything below the featured block did nothing significant**.
Prominence earns the investment; ranking the tail does not.

| Tier | Count | Treatment |
|---|---|---|
| Featured | 2-4, default 3 | Optional banner, headline, 25-55 words, install line, one text CTA |
| Compact | 5-9 | Decorative icon, title, one line. Text-forward |
| One-line | everything else | Title plus a short tag, grouped under category headings |

Two rules that are easy to get wrong:

- **Featured items are chosen for relevance, not recency.** The Kong effect is
  conditional on the featured item mattering to that reader. Position is a weak
  proxy. If the source knows better (engagement, category, an editor's pick),
  pass an explicit `tier` per item and say what the ranking was.
- **The compact tier's icons are decorative and carry `alt=""`.** NN/g measured
  thumbnails as rated *less* valuable than full-width imagery and re-classified
  a thumbnail newsletter as cluttered on re-test. The row has to read completely
  with every image stripped.

## Step 3 — Write the copy

Route prose to the project's own voice skill where one exists
(`create-luke-content`, `agent-voice`, or a named persona). This skill owns
structure, not voice.

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

Length guidance for subjects is a truncation constraint, not a performance
lever: three large datasets give three different optima and an academic study
across 455 million users found no direct relation at all. The gate warns and
never fails on it.

## Step 4 — Render

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

Sixteen checks. The ones that catch real defects most often:

- **`tiers`** — no tier markers means every tier rule below is measuring
  nothing while still printing a verdict. This failed silently on the first
  render here.
- **`prose-intro`** — a paragraph over 180 characters before the first item.
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

Two things the gate deliberately does not do:

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

## References

`references/evidence.md` — every rule, its class of evidence, and the eight
widely-repeated figures that could not be traced to any primary source.
`references/payload.md` — the payload schema and per-item fields.
