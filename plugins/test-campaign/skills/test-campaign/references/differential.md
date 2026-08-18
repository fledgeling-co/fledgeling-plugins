# The differential — measuring the build against the design of record

Testing the build can prove everything it does is correct and can never reveal
what it **lacks**. A control the design specifies and the build never rendered
has no selector, no route and no failing assertion. It is invisible to the entire
suite.

The differential is the only phase that can see it, and it is why
`project-comprehension.md` treats a mock as a first-class source rather than
decoration.

---

## What it is not

**Not a pixel diff.** Rendering noise — font rasterisation, anti-aliasing,
animation, dynamic content, sub-pixel layout — produces false positives at a rate
that buries the signal, and two independent research backends said the same
thing. A pixel comparison is a **tripwire**: useful to say "look here", never to
say "this is wrong". Where one is used, it starts from a deterministic fixture
and its verdict is a prompt for a structural read.

**And not a perceptual score either, which is the more tempting mistake.** The
natural upgrade from pixel equality is a similarity metric with a tolerance —
SSIM, LPIPS, DISTS. Measured: imperceptible perturbations raised **DISTS by up to
34.5%, LPIPS by 36.8%, VIF by 98.0% and HaarPSI by 22.6% while human opinion
scores stayed flat or fell**, and every metric tested could be pushed this way.
PSNR and SSIM were immune to those particular attacks, which makes them usable as
tripwires and still not as the verdict — SSIM separately penalises small
alignment errors no human notices, and is blind to localised texture and material
changes people see immediately.

Two consequences for how a tolerance is set:

- **A universal percentage tolerance across properties is indefensible.** There
  is no published tolerance that makes a `0.5px` difference in line-height,
  letter-spacing, width or height harmless, so a band is chosen per property with
  a stated reason, or not at all.
- **Widening a tolerance to absorb an unmeasurable read is a category error.** It
  converts "we do not know" into "we will ignore some differences" — a weaker
  claim wearing the same green tick. The honest move is `inconclusive`.

**Not eyeballing two screenshots.** That is the failure the whole measurement
discipline exists to prevent.

**Not the mock winning.** The mock is a second implementation of the same intent,
not the specification. Where the two disagree, **the model arbitrates** — the
requirement, the token source, the design system rule. A divergence resolves to
*build is wrong*, *mock is wrong*, or *both are legitimate for a stated reason*,
and the third outcome is common.

---

## The four vectors

Compare four things, on both sides, from the rendered result:

| Vector | Web | What only it catches |
|---|---|---|
| **Structure** | the role + accessible-name tree of the region | a missing control, a control that exists but is unnamed, a heading level that lies about hierarchy |
| **Resolved style** | `getComputedStyle`, **longhands only** | a colour, weight or radius that resolves outside the token scale |
| **Vocabulary** | the set of control names, headings, labels and empty-state sentences | the build offering an action the design does not, or naming it differently enough to teach a different mental model |
| **Quantised geometry** | `getBoundingClientRect`, snapped to a tolerance band | a structurally identical tree laid out wrongly — the case the first three vectors all pass |

Geometry is the fourth vector because structure-plus-style is genuinely
insufficient: two trees can carry identical nodes and identical computed values
and still place them differently. Quantise it — bands, not pixels — or it becomes
a pixel diff wearing a table.

**Read every computed value through its longhand.** Measured on one engine:
`padding` and `margin` return `0px` on an element whose CSS sets `16px` and
`40px`, while `paddingTop`, `paddingLeft`, `marginTop` and `marginLeft` are all
correct — and the layout itself is right. The shorthand resolves to zero silently
and passes a spacing assertion that should fail. Expand `border`, `borderRadius`,
`background`, `font`, `inset` and `gap` too.

And know your instrument's holes: on some engines an **empty** computed value
means *not implemented*, not *not set* — `boxShadow`, `backgroundImage`,
`textTransform`, `outline` and `flex` have all read empty on a page that clearly
had them. A comparison that treats empty as "absent on both sides" reports
agreement it did not measure.

---

## Subtract what is supposed to differ

A first naive run of this comparison produced **137 findings**. Almost none were
about design. Three subtractions, in this order, took it to a reviewable set —
each was necessary and none was sufficient:

**1. Subtract the shell.** The mock's content area against the build's content
area reported the build's navigation and release bar as forty-two findings across
six screens, none of them about a screen. Compute the shell as *what every screen
has*, on each side, and remove it.

Two traps inside that:

- **Compute it from screens that share a layout.** One route sat outside the
  console layout and carried neither nav nor bar, so intersecting all six found
  no shell at all. Intersect the ones that share the frame.
- **An element whose label depends on a post-mount fetch is not constant across
  screens**, so the intersection cannot remove it, and it surfaces on whichever
  screens were read first. Exclude those **structurally** — locate the release
  bar as "the element whose next sibling is the nav" — rather than by matching
  text that changes.

**2. Subtract the data.** The mock ships a fictional issuer; the build renders a
real tenant. Template each side's own content out before diffing: replace each
side's headings with one placeholder and digit runs with another. Nine per-row
findings collapse into the one real one — *the mock writes "Open controls for X"
and the build writes "Open the controls for X"*.

**3. Subtract the deliberate.** A divergence already decided stays decided.

What is left is the design question.

---

## The decided baseline, ratcheted three ways

Findings that survive triage are recorded with a verdict and a reason. The
baseline then gates in **three** directions, and all three matter:

| Direction | What it catches |
|---|---|
| **Unrecorded** | a new divergence nobody has looked at — the normal regression case |
| **Stale** | a recorded divergence that no longer exists, so the baseline is describing a build that is gone |
| **Unreviewed** | an entry accepted without a reason, which is how a baseline becomes a list of everything |

A baseline that only ratchets on new findings grows monotonically and stops being
read. One that also fails on stale and unreviewed entries stays the size of the
real disagreement.

---

## Every frame is a surface

Mine the design of record for its **complete** frame inventory, not its happy
path. A caption qualified with `· empty`, `· dark`, `(drill-in)` or `Composer` is
its own surface with its own case, and *"minor sub-state of X"* is a banned reason
to drop one.

While you are there, pull the surface's **depth manifest** — sub-tab count and
what each shows, list or table row count, detail-pane sections, the modals and
sheets it can open, the spec's named sub-features, the drill-down levels the data
supports. "Match the density" is a vibe until it is a count. An agent told *here
is the bar* clears it; an agent told *go find the bar* under-builds under context
pressure.

---

## Across platforms, two contracts

A single cross-platform pixel baseline is unreliable by construction: native
controls, fonts, anti-aliasing, safe areas and interaction conventions
legitimately differ. Judge two things separately instead:

- **Semantic parity** — role, accessible name, enabled state, available action,
  data presented, state transitions. This *should* match across web, React Native
  and native, and a divergence here is a defect.
- **Platform fidelity** — typography, spacing, safe-area behaviour, control
  conventions, gesture affordances. Judged against a **platform-specific**
  baseline, where a divergence from the web is often correct.

Share the token source and the semantic component IDs; keep the rendered
references per platform.

And plan to the lane's ceiling. SwiftUI exposes no runtime style tree, so its
style vector is a triangulation — token conformance, element-scoped raster crops,
the platform audit's own contrast findings — not a read. `harness-lanes.md` has
the rest.

---

## A native desktop window against an HTML mock

This is the comparison a desktop campaign actually wants, and the first thing to
say about it is that **no product does it.** The commercial visual-testing tools
cover web and mobile; none covers a native Mac or Windows application. So this
comparison is hand-built or it is absent, and absent is a legitimate answer that
gets written into the not-covered section rather than filled with a screenshot
somebody looked at.

When it is hand-built, the four vectors survive but only two of them can be read
directly, because there is no `getComputedStyle` for a foreign native window:

| Vector | On a native lane |
|---|---|
| **Structure** | readable — the accessibility tree gives role, label, value, identifier |
| **Vocabulary** | readable — control names, headings, labels come off the same tree |
| **Geometry** | readable — accessibility frames, and assertable |
| **Resolved style** | **not readable.** Triangulate, or mark the vector `inconclusive` with that reason |

Geometry is where the temptation to reach for a similarity score returns, and the
answer is the same as everywhere else in this file: **quantise it, do not score
it.** Compare the bounding boxes of named regions — the header, the card grid, the
sidebar — snapped to a band chosen per lane, and report a region whose box moved
beyond the band. A band is a claim you can defend in a review; a similarity number
above a threshold is not, and it is the number an implementation can be tuned
toward without getting better.

Three things to fix before comparing at all, or the comparison measures the
capture rather than the build: the same nominal size and scale factor on both
sides, fonts loaded and settled, and animation stopped. On a native lane the last
one is the hard one — there is no equivalent of the browser's animation
disabling, and no OS-level virtual clock, so a frame captured mid-transition is a
real risk and a stated limit rather than something to average away.

---

## When there is no design of record

Say so, and change what the campaign claims rather than inventing a substitute.
The differential is `n/a` with that reason, and the **affordance** class of
requirement becomes unverifiable: nothing else can reveal a control the build
lacks. Native conformance rubrics substitute for platform correctness. Nothing
substitutes for the missing-control finding.
