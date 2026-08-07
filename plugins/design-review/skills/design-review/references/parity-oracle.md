# Parity as an acceptance oracle

When a surface is being **re-implemented** — ported to a new stack, split into components, driven
from data instead of hard-coded, rebuilt on a new framework — "does it still look right?" is the
wrong question, because you cannot answer it by looking. The eye cannot see a 2px letter-spacing
drift across forty landmarks, and it certainly cannot see one on a page it has stared at all day.

Replace the judgement with a measurement.

## What to compare

Three populations, reported separately. Merging them hides which layer moved.

**1. Design tokens.** Read the custom properties off `:root` on both surfaces. This is the
cheapest check and it localises a whole class of failure instantly: if `--primary` differs, no
amount of component-level diffing tells you anything you did not already know.

**2. The band skeleton.** The ordered list of top-level section class-chains.

```js
[...document.querySelectorAll('main > section, .hero, .band, .tape')]
  .map(el => `${el.tagName.toLowerCase()}.${el.className.trim().replace(/\s+/g, ' ')}`)
```

This catches structure, which is where a re-implementation actually goes wrong: a duplicated
element, a section split in two, a wrapper that changed nesting depth. Both of the real defects
found on the run this reference comes from were skeleton diffs and neither was visible in source.

**3. Computed styles on named landmarks.** Not every node — a fixed list of ~40 selectors
covering the chrome, each section's heading, its body copy, its primary control and its data
surfaces. For each, a fixed property list:

```
fontFamily fontSize fontWeight lineHeight letterSpacing color backgroundColor
padding{Top,Bottom,Left,Right} margin{Top,Bottom} borderRadius boxShadow
display gridTemplateColumns maxWidth textTransform borderBottom{Width,Color}
```

Forty landmarks × twenty properties is eight hundred assertions, which is enough to be
load-bearing and few enough to read when it fails.

## The landmark set is per PAGE, not per site

The single most expensive lesson from running this oracle in anger: **a parity script that
loads one route certifies one route and implies all of them.**

A real one reported `checks=904 diffs=0` continuously while every index row of every tenant
carried a spurious second grid track — `grid-template-rows: 27.5px 16px` — dropping the row's
trailing arrow onto its own line and costing ~450px of dead height on one page. It was
invisible to the oracle twice over: `.idx` was not among the 40 named landmarks, and the
oracle only ever loaded `/`, where no `.idx` exists. Nine hundred green assertions sat over it
indefinitely.

So:

- **Enumerate the routes, not just the selectors.** Every page the record, router or sitemap
  declares gets a row, and its landmark set is the components *that page* actually renders.
- **Print which pages were compared**, next to the check count. `checks=904` over one route
  and `checks=904` over eight are different results and currently serialise identically.
- **When a component appears on page B and not page A, its landmarks belong to page B.** The
  temptation is one shared list applied everywhere; the selectors that do not match simply
  contribute nothing, and a missing landmark is silent.

The general form is the denominator rule below, applied to surfaces rather than to nodes.

## What NOT to compare

**Text.** If the port carries the same strings by construction — and it should — a text diff is
self-confirming. It will pass on a completely broken layout.

**Screenshots, as the primary instrument.** A pixel diff tells you *that* something moved, never
*what*. Use captures to look at what the numbers flagged; do not use them to find it.

## Making the comparison honest

**Neutralise scroll-triggered state on both sides identically.** A reveal system leaves most of a
long page at `opacity: 0` in a full-page capture. Strip the arming class and clear inline styles
on both surfaces before probing, or you are comparing two differently-hidden pages.

**Prove the probe can fail.** Run it once against a deliberately broken build. A parity script
that reports zero diffs because its selector list is empty, or because it read a field the probe
never sets, looks exactly like success. Print the denominator — `checks=904` is a result;
`diffs=0` alone is not.

**Port faithfully first, fix second.** If the reference has known defects, reproduce them. Fixing
during the port makes the diff unreadable, and the diff is the only instrument proving the port
faithful. Land parity, then fix in the new codebase where the change is visible as a change.

## Proving the data path, not just the render

When the point of the port is that content now comes from somewhere new — a database, an API, a
CMS — parity alone does not prove it. A fallback path can render the same thing from the old
source and pass every check.

**Run the negative test.** Break the new source and confirm the surface *fails*:

```
API at a dead port, fallback disabled  →  404      ← would be 200 if it were the fallback
API up                                 →  200      ← and now parity
```

And carry the provenance in the resolution itself (`source: 'api' | 'seed' | 'none'`), so "it
renders" can never be mistaken for "it renders from the new source". This is the same discipline
as reporting gates and looked-at surfaces separately: an unfalsifiable check is not evidence.

## Assert the chrome and the graph, not only the content

A generated-instance suite drifts towards asserting what is *interesting* — the copy, the
figures, the names — and away from what is *structural*. The structural things are the ones
nobody writes a case for, because no one has ever seen them missing.

A real suite of 43 cases and 524 assertions across 13 tenants never asked whether a generated
portal had a **header**. Every record the generator had ever produced carried `chrome: {}`,
and the layout rendered `{header && …}`, so every generated tenant shipped with no brand, no
navigation and no footer. Five pages measured **one tab stop** — the skip link — and **zero
internal links**; two routes resolved 200 with nothing on the site pointing at them. The suite
was green throughout, on assertions like *"people includes `Stephen Hall :: Chief Executive
Officer`"*.

Three assertions worth adding to any suite over generated surfaces:

- **Chrome exists.** Header, navigation, footer — present, and populated from *this* record.
- **The page graph is connected.** Every page the record declares is reachable by a link from
  at least one other, and its keyboard tab-stop count is above the floor a bare document has.
- **No orphan resolves 200.** A route that renders but that nothing links to is a page nobody
  will ever see, and it is indistinguishable from a working one in every per-page check.
