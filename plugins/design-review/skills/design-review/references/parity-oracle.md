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
