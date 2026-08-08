# Aesthetic direction — why every page must look different, and how

## The measured problem

"Every page should look different" sounds like taste. It is not.

Goree et al. (CHI '21) measured web-design homogenisation across
2003–2019 using ~2M pairwise image comparisons plus interviews with 11
designers of 15+ years' experience. Design became *less* homogeneous
2003–2007, then dramatically more so. **Layout similarity distance
declined 44% from 2010 to 2019**, in both colour and spatial layout.

The strongest correlate was **shared use of a small number of frameworks
and libraries**. Their forward-looking warning is the relevant one: this
may constrain the perceived repertoire of legitimate designs available to
future designers.

The consequence for a producer of many pages is exact:

> The invariant that reads as sameness is **layout skeleton and motion
> signature**, not palette.

A generator that reuses one motion library, one step-height rule and one
sticky-graphic layout converges on one look **regardless of theming**.
Re-colouring the previous page fixes nothing.

There is no validated metric for "recognisably templated" — all four
backends returned `INSUFFICIENT_EVIDENCE` on it. What follows are
production heuristics with the reasoning attached, not thresholds.

## The system boundary

Three backends stated this independently and identically:

> **Standardise the hidden infrastructure. Derive the visible rhetoric
> from the subject.**

| Reuse freely | Never reuse |
|---|---|
| The chrome script and its two blocks | Hero composition |
| Citation component behaviour and markup contract | Section silhouette |
| The auditor and its gates | Chart grammar |
| Focus styles, keyboard handling | Illustration system |
| The accessibility harness | Transition metaphor |
| The claim-graph shape | Typography |
| Grid utilities, spacing scale | Palette and material |

Precedent worth copying: the Financial Times built reusable story
patterns around **specific reader questions** rather than generic
layouts, and introduced each only after it had already worked on a
prominent story. The pattern earned its reuse by working once.

## Running `/trawl` on the aesthetic

Give trawl the *subject matter* as frame material, not "design a page".
The frames should be occupational and constraint-shaped — someone who
lives with the topic's consequences, an extreme operating constraint, an
adversary, a cross-domain mechanism, and the wild seat.

What comes back should be **directions**, each stating:

- the **register** (what kind of document this pretends to be — a
  technical manual, a field notebook, a broadsheet, a specimen sheet, a
  control panel, a court exhibit)
- the **one visual device** the page is built around, drawn from the
  subject
- the **palette logic** and what in the subject justifies it
- the **type pairing** and why it belongs to this material
- the **motion signature** — what moves, and what perceptual job it does
- what it would look like if it went **wrong**

Then run the shortlist past the user via `/clarify` in words, before
building anything.

## The theme-proof test

Apply before building. Every major visual choice must map to a **named
concept in the topic corpus**. Random palettes, generic particle fields
and interchangeable dark "cinematic" heroes fail — not because they are
ugly, but because they would fit any subject, which means they express
none.

## The authored review

Run against the built page, with the previously published pages open
beside it. The page **fails** if:

- its section silhouette matches a previous report once colour and copy
  are stripped
- changing the subject noun leaves the visual metaphor intact
- motion is primarily repeated fade / slide / reveal recipes
- typography, texture and illustration are unrelated to the source
  material
- the hero is more specific than the evidence beneath it
- the same chart grammar appears regardless of data type
- there is no explicit editorial tension, uncertainty or counterargument
  anywhere on it

That last one is not a visual test, and it belongs on this list anyway. A
page that resolves everything reads as generated because a human author
with real sources almost always has something they are unsure about.

**The cheap version of the silhouette check**: screenshot the new page
and each previous one full-length, convert to greyscale, blur heavily,
and compare the block structure. If the bands land in the same places,
the skeleton was reused. This is a production heuristic, not a validated
perceptual threshold — treat a match as a prompt to look, not a verdict.

## Distinctive is not arbitrary

One counterweight worth holding. Song et al. (2025/26) found cartoon
styling and hand-drawn fonts **reduced perceived credibility**, while
other work found embellishment improved recognition and memorability.

These are not in conflict: recognisable, subject-derived imagery helps,
and arbitrary decoration costs trust. The page is evidence-dense and
published under a real name. Distinctiveness comes from committing hard
to a subject-native visual argument, never from novelty for its own sake.
