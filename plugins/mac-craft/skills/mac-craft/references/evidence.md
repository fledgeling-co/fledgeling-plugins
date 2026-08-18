# Evidence — what is sourced, what is measured, and where the sources disagree

Every load-bearing number in this skill traces to a row here. The point of the file is
that a runner can tell **which tier a value sits in** before using it, because the
recorded failure mode in this skill's history is not disagreeing with a published value —
it is never reading one and then reporting conformance anyway.

## Tiers, and which beats which

| Tier | What it means | Rank |
|---|---|---|
| `kit` | Apple's macOS UI kit, deconstructed from its Sketch JSON. Exact geometry Apple ships but does not publish as prose. | 1 for geometry |
| `hig` | Apple's published Human Interface Guidelines / developer documentation / WWDC session. | 1 for policy, and it outranks `kit` wherever the two speak to the same thing |
| `research` | The August 2026 Dossier panel below. Four backends, 110 sources, 28 independent domains. | 2 |
| `corpus` | Measured from the 135-app macapp.supply digestion (`corpus-evidence.md`). Describes what shipping apps *do*, never what the platform *specifies*. | 3 |
| `direction` | A chosen aesthetic direction's identity tokens. Legitimate inside the native envelope, never over chrome geometry. | 4 |
| *(untagged)* | **A defect.** A cell you cannot tag is a value you invented. | — |

## The panel, August 2026

Four backends ran one brief; each read largely different material (11% source overlap),
so a claim only one backend made is **uncorroborated rather than agreed**.

| Backend | Model | Sources | Fabrication check | Weight given here |
|---|---|---|---|---|
| openai | `gpt-5.6-terra` | 85 | **PASS**, 85/85 resolved | Highest. Nearly all `developer.apple.com`. |
| perplexity | `sonar-deep-research` | 19 | **PASS**, 18/19 resolved | High. First-party HIG, independently confirms openai's type ramp. |
| xai | `grok-4.3` | 8 | not separately re-checked; all HIG/GitHub | Corroborating only. |
| gemini | `deep-research-preview-04-2026` | 38 | **ATTENTION — 2 malformed, 10 blocked** | Lowest, and see the conflict register. |

Reports and per-run source registries: `plugins/mac-craft/docs/deep-research/`
(plugin root, not this skill's directory — four full reports plus a `.sources.md`
registry each, so every claim above can be read back at its source).

## Values this skill takes as sourced

Corroboration is counted in **independent domains**, never in backends.

| Value | Tier | Corroboration | Note |
|---|---|---|---|
| Body text **13 pt / 16 pt line height** | `hig` | openai + perplexity, both `developer.apple.com/design/human-interface-guidelines/typography` | Also the kit value. The loudest native-vs-web discriminator. |
| **Minimum text size 10 pt** | `hig` | openai + perplexity | New floor; the predecessor had none. |
| Type ramp: LargeTitle 26/32 · Title1 22/26 · Title2 17/22 · Title3 15/20 · Headline 13 Bold/16 · Body 13/16 · Callout 12/15 · Subheadline 11/14 · Footnote 10/13 · Caption1 10/13 | `hig` | openai + perplexity, independently, both matching the bundled `kit` table exactly | Three-way agreement. See the conflict register for the iOS ramp that gets imported instead. |
| Avoid Ultralight / Thin / Light weights; prefer Regular, Medium, Semibold, Bold | `hig` | perplexity | Single-sourced but first-party. |
| **Target size: 28×28 pt default, 20×20 pt hard minimum** (macOS) versus 44×44 / 28×28 (iOS) | `hig` | openai, `.../accessibility` | See the reconciliation note below — this does *not* contradict the 24 pt kit control height. |
| Every toolbar command must also exist in the menu bar | `hig` | openai + perplexity + xai, `.../toolbars` | Three backends, one page. One source, thrice found. |
| Window title: useful, content-bearing, **under ~15 characters**, never the app name | `hig` | openai + perplexity + xai | |
| Toolbar items carry **no bezel**; group by function and frequency; **max ~3 groups** | `hig` | perplexity + xai | Confirms the bundled grammar rule exactly. |
| Sidebar hierarchy: **no more than two levels**; deeper needs a middle list pane | `hig` | openai, `.../sidebars` (page updated 2026-06-08) | |
| Liquid Glass belongs on the **functional layer** (controls, navigation, overlays), never the content layer — "unnecessary complexity and a confusing visual hierarchy" | `hig` | openai + perplexity + xai, `.../materials` | Confirms the bundled glass-discipline rule. |
| Liquid Glass has **regular** and **clear** variants; regular blurs and adjusts luminosity for text-heavy surfaces, clear is for media backgrounds | `hig` | perplexity + xai | Not in the predecessor at all. |
| A clear-variant component over **bright** content needs a dimming layer — **dark at 35% opacity** | `hig` | perplexity, `.../materials` | Single-sourced, first-party, and the only concrete opacity number the panel produced. |
| Standard materials `ultraThin` / `thin` / `regular` / `thick`, thickness matched to how much the overlay obscures | `hig` | perplexity | |
| Focused list selection = accent fill with white text; unfocused = grey fill with standard text | `hig` | openai, `.../focus-and-selection` | Confirms the bundled selection-duality canon. |
| Concentric corners are a **named platform relationship** with an API (`concentricCornerRadii(in:)`): child radius = container radius − distance from child corner to container corner | `hig` | openai | Upgrades "child = parent − padding" from folklore to a cited formula. |
| One scroll-edge effect per scrollable pane; two stacked in one pane is wrong | `hig` | openai, WWDC25 356 | |
| Reduce Transparency → make backgrounds **opaque** (explicit direction, not a preference) | `hig` | openai + perplexity | |
| Increase Contrast on macOS **also forces Reduce Transparency**, and the two cannot be separated | community | perplexity, Apple Support Communities | Community-sourced. Actionable anyway: an increased-contrast pass must assume solid surfaces. |
| WCAG 2.2: **4.5:1** normal text, **3:1** large text, and **ratios must not be rounded up** | `hig`(W3C) | openai, `w3.org/WAI/WCAG22` | `scripts/mock_check.py` uses raw floats for exactly this reason. |
| APCA is a candidate method for future WCAG work and **not a conformance basis today** | `research` | openai, Myndex's own docs | So WCAG 2.2 stays the hard gate and APCA is not implemented. |
| **No automated tool alone determines conformance** | `hig`(W3C) | openai, `w3.org/WAI/test-evaluate` | This is why the gate's verdict is evidence and the human's is the verdict. |
| axe-core's `color-contrast` rule **does not work in JSDOM**; axe detects "on average 57% of WCAG issues" (vendor's own figure) | `research` | openai, Deque's own repo | The reason this skill ships a bespoke static gate rather than wrapping axe. |
| Pa11y and Lighthouse both require Headless Chrome | `research` | openai + xai + perplexity | So neither is available under this house's browser policy. |
| macOS **27 "Golden Gate" is beta** as of 2026-08-18 | `hig` | openai, `developer.apple.com/documentation/macos-release-notes` | The predecessor described "macOS 27" as though shipped. Hence the two profiles in SKILL.md step 0. |
| macOS 27 refines Liquid Glass: better diffusion, brighter highlights and darker edges, a **user-facing clarity/tint slider**, edge-extending sidebars, semi-bold sidebar selection, tighter window corners, interactive glass, a `showBorders` environment value | `hig` | openai, WWDC26 112 + 289 | Substance corroborated first-party. The *numbers* are not — see below. |

### The reconciliation that matters: 24 pt or 28 pt?

The bundled kit table says the Regular control tier is **24 pt tall**. Apple's published
accessibility guidance says the macOS default target is **28×28 pt** with a hard minimum
of **20×20 pt**. Both are correct and they measure different things: 24 pt is the drawn
control, 28 pt is the *target* it should answer to. So the rule is a pair, not a choice —
**draw the control on the kit ladder and pad its hit area to 28 pt**, and never go below
20 pt for anything interactive. A 44 pt control is the iOS number and is the tell.

This is the sort of apparent contradiction that gets resolved by picking one and
silently dropping the other. Both are cited; neither is dropped.

## Conflict register — where the panel disagreed

**1. The type ramp. Resolved against gemini.**
gemini gives Large Title **34 pt** and Title 1 **28 pt**, sourced to a GitHub gist its own
evidence table marks *"Unverified"*. Those are the **iOS** values. openai and perplexity
independently give 26/32 and 22/26 from `developer.apple.com/.../typography`, matching the
bundled kit table. Two first-party sources plus the kit beat one unverified gist, and the
direction of the error is itself the finding: **the iOS ramp is what gets imported by
mistake, and a 34 pt "Large Title" on a Mac surface is the tell.**

**2. Text casing. Genuinely conflicted, and the predecessor was wrong.**
`mac-essence.md` conviction 5 asserted **"sentence case everywhere (headers, labels,
buttons)"**. Apple's HIG Menus page specifies **title-style capitalization with articles
removed** for menu items — cited by openai *and* perplexity, independently, first-party.
gemini goes further and claims title case for all buttons and headers too, but sources it
to a 2012 StackExchange thread and a 2019 Facebook post, both of which are 403-blocked.

Settled position, stated with the uncertainty intact: **title case for menu-bar items
(sourced); sentence case for body copy, field labels, placeholders and helper text
(sourced); buttons are contested — the corpus shows both and Apple's own apps ship both,
so pick one per surface and hold it, because the citable rule is consistency within an
element type.** What no reading disputes: **tracked ALL-CAPS at heading size is a web
tell in every source.** That part of conviction 5 survives; the blanket claim does not.

**3. macOS 27's numbers. Single-sourced and unverifiable; not adopted.**
gemini asserts a system-wide window radius of exactly **20 pt** in macOS 27, down from
**26 pt** in Tahoe. Its sources are a MacRumors forum thread (403) and a 9to5Mac article
that **does not resolve at all** — and the citation checker reports nothing else in that
report supports the claim. openai independently confirms the *substance* ("standardizes
tighter window corners") from WWDC26 first-party, with **no number**. So: the direction of
travel is sourced, the value is not. The bundled reference's existing position — window
radius is era-fragmented, pick one and keep every nested radius concentric to it — is
still the honest one, and it is now paired with a cited formula rather than a guess.

**4. Whether a flat opaque window is native. Both, and the tension is real.**
Apple's Materials guidance says to **prefer translucency to opaque colors in windows**,
because opacity "can block people's view" (perplexity, first-party). The corpus says a
flat opaque window is legitimately native and ships widely (`corpus-evidence.md`). Both
hold: Apple states a preference, shipping apps exercise the exception. Recorded rather
than averaged. Do not read the HIG preference as a requirement to put glass on everything —
that collides directly with the glass-discipline rule two rows above it.

**5. DOM-free text-fit measurement. Resolved against gemini.**
gemini recommends a library it says computes exact text geometry with no DOM in
0.00052 ms, sourced to one blog post, and describes it as using canvas font metrics —
which requires a canvas. openai independently returns `MISSING_DATA` for DOM-free text
layout and states plainly that exact verification needs either a restricted layout grammar
or a real engine with the deployment font stack. **`mock_check.py` therefore does not
attempt text-fit or overflow measurement, and says so** rather than shipping a check whose
passes mean nothing.

**6. "A false pass is worse than a false fail."** gemini's substance is right and its
citation is an electrical-safety-testing vendor page (403), which is not evidence about
software audits. The same principle is available first-party from W3C, which states that
no tool alone determines conformance and that tools can produce misleading results. Cite
W3C.

## What the panel could not answer

- **No complete public Apple table of control heights, bar heights, radii, blur radii or
  glass opacities exists.** openai and xai independently report this as missing. That is
  the finding, and it is what justifies keeping the `kit` tier at all: the deconstructed
  Sketch JSON is the *only* route to those numbers, so `native-foundation.md` is load-
  bearing rather than redundant with the HIG.
- **No controlled study shows which single affordance failure makes a reviewer call an app
  "not a real Mac app."** openai marks its own diagnostic list as inference from Apple's
  stated expectations, not a measured causal result. So the native-tells audit is a list
  of documented platform expectations, and this skill should not claim it is a
  perception study.
- **Apple's Liquid Glass compositing is proprietary**, so no static reading can compute
  true contrast through glass. `mock_check.py` reports such pairs as unresolved and
  refuses to score them.

## Measured on this machine, 2026-08-18

Not from the panel. Computed with the same sRGB luminance formula the gate uses:

| Pair | Ratio | Consequence |
|---|---|---|
| Kit secondary label, black @50% on `#FFFFFF` | **3.98:1** | **Fails the 4.5:1 floor.** The kit's own light secondary tier is below AA for body text. |
| Black @55% on `#FFFFFF` | 4.76:1 | The lowest light secondary that clears it. |
| Black @60% on `#FFFFFF` | 5.74:1 | Comfortable. |
| Kit tertiary, black @25% on `#FFFFFF` | **1.83:1** | Cannot carry text at all. Dividers and disabled only. |
| Kit secondary, white @55% on `#1E1E1E` | 5.91:1 | Passes. |
| White @50% on `#1E1E1E` | 5.12:1 | Passes — so the *same tier name* passes in dark and fails in light. |
| White 13 pt on kit system Blue `#0088FF` | **3.52:1** | The platform's own accent-filled button is below AA for body text. |
| White 13 pt on `#0071E3` | 4.70:1 | Clears it and reads as the same blue. |

The first and last rows are the origin of the defect the corpus calls its dominant one.
**Contrast Dilution appears in 72 of 135 corpus apps, and the tier table the predecessor
told a runner to apply directly is where it comes from.** Corrected in
`native-foundation.md`; enforced by `scripts/mock_check.py`, which reports a
system-hue failure differently from an ordinary one because the two have different fixes.

## Two defects in this skill's own gate, and why they are worth writing down

Both were found by `scripts/gate_tests.sh` on the day the gate was written, and both are
bug *classes* rather than one-off slips. The presenting symptom in each case was **the
instrument accusing the material** — the suite reported fourteen broken fixtures when the
fixtures were correct and the gate was wrong twice. That is the exact failure this whole
rebuild is aimed at, arriving from the other direction: a checker confidently wrong is worse
than a checker absent, because its output looks like evidence.

**1. Exit 2 masked exit 1.** The first revision returned `2` (unmeasurable) whenever any
check could not be performed, checked *before* the failure count. So a mock carrying a
1.00:1 invisible glyph **and** one gradient background it could not resolve exited `2`. The
failures still printed — but the code a caller branches on said "could not measure", and a
runner reading it goes and chases the indeterminate check while the invisible glyph ships.

The general rule, which applies to any runner with more than one verdict class: **a proven
failure outranks an indeterminate one.** If you can demonstrate the thing is broken,
"broken" is the verdict; indeterminate only wins when nothing failed, because that is the
case it is actually about — no failures found *and* no confidence that none exist. Report
both counts on the summary line so the softer signal is not lost. Any multi-check gate will
meet this; the ordering is not obvious until it bites.

**2. The cascade walk skipped colour inheritance.** `color` is an inherited CSS property,
and the first revision read it only from *matched* rules. A `<div>` holding text inside a
`body { color: … }` therefore declared no colour of its own, so the pair was skipped
entirely — and the skip was invisible, because `examined` simply came out lower and nothing
said which elements had been dropped. Fixing it took the passing fixture from **76 measured
pairs to 116**, a 53% undercount, and corrected the font sizes the 4.5-versus-3.0 threshold
depends on (a row inheriting 15px was being scored at the 13px default).

This is the macOS-mockup twin of a defect the sibling `design-review` rebuild recorded from
its own domain: a backdrop the checker resolved wrongly, producing a contrast blocker that
did not exist. Same shape both times — **a cascade approximation that silently resolves the
wrong layer produces a number, and a number is believed.** The defence is not a better
approximation; it is that the gate must be able to say *which* pairs it measured and refuse
the ones it could not, which is why `unresolved` is a separate counter from `failures` and
why neither is ever folded into `examined`.

### And the caveat that survives the code

Adding the ancestor walk did **not** retire the reason a reader needs to distrust it. The
walk finds the nearest ancestor that *declares* a background; it does not know whether that
ancestor actually paints behind the text, because positioning, stacking order, transforms
and overlapping siblings all decide that and none of them are in the declarations. Sibling
combinators (`+`, `~`) are additionally treated as descendant, which over-matches on
purpose — over-matching a background is safer than reporting a resolvable pair as
unresolved, but it is still a wrong answer some of the time.

So the fallback stays a documented step rather than being replaced by the check: **when a
contrast verdict looks wrong, open the render and sample the pixel under that text.** A
measured pixel beats a resolved declaration, and it is the move that identifies a probe
artifact *as* a probe artifact instead of scoping around it. A prose caveat and a code gate
are not substitutes for each other; the gate makes the common case cheap, and the caveat is
what a reader does when the gate and their eyes disagree. Teardown P1 says make it code. It
does not say delete the reasoning.
