# Evidence

Every rule in this skill traces to one of three places: a measured result with a
citation, a mechanism that cannot be argued with, or a failure that actually
happened. This file says which, so a rule can be challenged on its own terms.

**Four reports back it**, three of them a panel run on one brief across independent
backends. Full text and source registries: `docs/deep-research/`. Where they disagree,
the disagreement is recorded rather than averaged — that is the point of a panel.

| Report | Backend | Sources | Citations checked |
|---|---|---|---|
| `panel-claude` | Claude Code CLI | 46 | — |
| `panel-gemini` | Gemini Deep Research (max) | 63 | 61 live, 0 fabricated, 2 blocked |
| `panel-codex` | Codex CLI | 35 | — |
| `codex-single-run` | Codex CLI (earlier, fast) | 30 | 28 live, 1 dead, 1 blocked |

---

## The adjudication

The panel was asked to confirm, quantify or overturn each design decision. All five
survived. Three were in the wrong units.

| Decision | Verdict | What replaced the guess |
|---|---|---|
| Test expectation is the oracle, mock advisory | **Confirmed** | Rated High Confidence independently by two backends |
| Deterministic pre-scan before any model looks | **Confirmed, narrowed** | Pixel diff scores **100.00% change-accuracy and 0.00% no-change-accuracy**; with a 0.1 threshold and anti-aliasing tolerance, 97.93% / 6.72%. A near-perfect *detector* and a worthless *discriminator*: use it to prove "not blank, not identical", never to adjudicate |
| Crop to 2–3× | **Confirmed, re-united** | Crop to the **no-downscale ceiling** (1568 px long edge standard, 2576 px Claude 4.7+) and to **≥7 px rendered text height**; optimum crop size ~**1024²**, non-monotonic and model-dependent |
| Both orders, flips inconclusive | **Confirmed, strengthened to a gate** | **43.0%** average order-flip rate across 36 models; **64.3%** first-shown pick rate; **15.7 pp** first-position lift |
| Five difference classes | **Confirmed** | Independently re-derived by two backends; maps onto a 37-rule taxonomy built at Cohen's κ = 0.722 |
| Image text untrusted | **Confirmed, escalated** | Typographic injection **5% → 77%**; **82.50%** average ASR across six open-source LVLMs |

Two rules the panel added by warning against things the skill had not done:

- **No chain-of-thought on the judging call.** Three-step CoT degraded every metric:
  GPT-4V scoring **0.557 → 0.299**, pairwise 0.806 → 0.728. It cut hallucination and
  bought accuracy with it.
- **Never drop the reference, even when advisory.** Self-preference roughly *doubles*
  without one to anchor on (GPT-4o 0.55 → 1.08).

---

## The mechanical case for cropping

The strongest single finding, because it is arithmetic rather than preference.

Models downscale above a documented long-edge ceiling, aspect preserved, before
inference. Text accuracy falls off sharply below **7 px** of rendered glyph height,
and images under 200 px a side invite hallucination outright.

So: a 1280 px-wide page running to 4320 px tall is downscaled **0.363×** on the
standard tier, delivering 14 px body text at **~5.1 px** — under the cliff,
unreadable however the prompt is worded. High-resolution tier: 0.596×, ~8.3 px,
barely over. Cut into 1280×720 tiles: **no downscale at all**, text at 14 px, twice
the cliff. Roughly 952 visual tokens for the unreadable whole page against 1196 per
readable tile.

Crop size is non-monotonic. On ScreenSpot-Pro, OS-Atlas-7B: 25.1% at 512², 34.2% at
768², **40.2% at 1024²**, 40.1% at 1280² — while UGround-7B peaked at 768². Too small
loses context, too large exceeds capacity.

**And run two passes at two sizes.** On ASCII art, *lower* resolution helped GPT-4o,
apparently by blurring detail and emphasising structure. Global judgements read better
downscaled; local ones need full resolution. One image size cannot serve both.

---

## Where the reports disagree

Recorded, not resolved. A merged number would be fiction.

**Prompt-injection attack success: 15.8% to 98%.** The spread is real and mostly
methodological. One backend cited visual goal hijacking at **15.8%** against GPT-4V
(2024) and a steganographic variant at **24.3% ± 3.2%** (2025). Another cited
typographic injection at **64%** peak against GPT-4V, Claude 3 and Gemini, an
**89–91%** best-of-suite ensemble against undefended open models, and a physical-world
variant at **98%**. A third cited FigStep at **5% → 77%** and Anthropic's own browser
measurement at **23.6% unmitigated → 11.2% mitigated**, with browser-specific vectors
at **35.7% → 0%**.
*Read it as:* single-attack rates against defended frontier models sit in the tens of
percent; best-of-suite ensembles against undefended models approach ninety. Mitigation
demonstrably works (35.7% → 0% on a named vector). The skill's controls are justified
at any point in that range.

**Position bias magnitude.** One backend reported Claude-3.5-Sonnet position
consistency at 0.82 / 0.76; another a "~5% persistent distortion"; another a **43.0%**
average flip rate across 36 models, with MT-Bench-era figures as extreme as Claude-v1
at 23.8% consistency and 75% first-position preference. These measure different things
on different tasks and eras. **No source reports swap consistency above ~80% for
pairwise judging.** That floor is the load-bearing fact, and it is enough.

**Human agreement, and how bad it is.** One backend found model Krippendorff's α of
0.51–0.75 against expert humans at 0.29–0.78 (median 0.55) on an out-of-domain task.
Two others converged on something far more damning *for design specifically*: 20
professional designers reach **α = 0.25** on binary visual-preference, falling to
**α = 0.104 / κ = 0.114** on a four-way scale.
*Consequence for this skill:* a conformance score against a mock is inherently
low-signal, because the humans it would be imitating barely agree with each other.
This is the strongest available argument for the test being the oracle and the mock
being advisory, and it arrived independently of that design choice.

**Do perceptual metrics beat pixel diff on UIs?** One backend found SSIM and LPIPS at
SROCC 0.379 and 0.367 on web UIs and reported that *basic pixel-matching correlates
better with human judgement*. Another found pixel diff at 0.00% no-change accuracy.
Both are consistent once you separate the questions: pixel diff is a superb detector
and a hopeless discriminator, and the learned metrics are not better enough at
discrimination to be worth their complexity. Neither belongs on the gate.

---

## What the evidence adds — controls the skill did not have

**A capture provenance manifest.** Route, viewport, DPR, browser, fonts, locale,
theme, auth state, scroll position, fixture hash, readiness predicate, crop rectangle
— recorded *before* any model looks. A VLM cannot infer whether a changed date or
viewport is legitimate, and will answer anyway.

**Blind the judge.** Neutral `image_A` / `image_B`, never filenames, never the
generating model.

**No tools on the judging call.** No filesystem, shell, network or messaging access on
the call that sees the image. OCR text into a data field; never paste it back into the
controlling prompt. Abstain rather than merely report when an image carries
instructions.

**Scope decides the class, not magnitude.** A global intentional change (light to dark
theme) is meaningful; a single shadow tweak is local cosmetic noise. Taken verbatim
from the taxonomy's own boundary rule.

**Verbosity bias enters through the text, not the image.** Lengthening answers raised
scores 0.6 (GPT-4V) and 0.75 (Gemini) points. In this skill that arrives through the
*expected-output prose*: a verbose expectation pulls the verdict toward "match"
independent of the pixels. Fixed-length, atom-per-line expectations neutralise it;
free-form prose does not.

---

## Where the evidence runs out

- **No study measures UI defect detection as a function of crop factor** with
  everything else held constant. Every crop number here is grounding or parsing. The
  transfer argument is the shared bottleneck — too few post-downscale pixels on target
  — and this skill's targets are typically *smaller* than a clickable control. Read
  +29.2 points as an upper bound and directional support.
- **No UI-specific κ or α for VLM-versus-human on regression judgements.** Any figure
  has to be produced locally, and must be reported against human–human agreement or
  it flatters itself.
- **No verbosity-bias effect size on screenshots**, only on text.
- **No independent cross-vendor benchmark** of anti-aliasing or flake rates. Vendor
  documentation establishes behaviour, never efficacy.

---

## Industry defaults, for calibration

| Tool | Documented behaviour |
|---|---|
| Playwright | pixelmatch in **YIQ** (separates luma from chroma, so sub-pixel colour shifts are tolerated); `threshold` **0.2**; `maxDiffPixelRatio` typically **0.01–0.05**; captures until **two consecutive screenshots match** |
| Chromatic | Excludes anti-aliased pixels by default; `diffThreshold` **0.063** |
| Percy | Cloud rendering for OS/font parity; `diff-threshold` default **1%** |
| reg-suit | `matchingThreshold` **0**, `thresholdRate` ~**0.05** |
| Applitools | Match *regions* (Strict / Layout / Ignore / Floating / Dynamic) rather than one global threshold |

Playwright's two-consecutive-screenshots rule is this skill's settle check, reached
from the deterministic side.

---

## Failures this skill encodes directly

Not from the literature. These happened, and each became a rule:

1. A capture suite photographed a **loading skeleton** and scored design mocks against
   it for a whole run. → the settle check, and `state` as its own class.
2. A structural score reported four healthy surfaces as drifted because a 440×275 card
   was compared against a 1440×900 viewport. → the framing check, and framing never
   failing a run.
3. A parity oracle reported **904 green assertions** while a real defect sat under it,
   because the component was not among its landmarks and it only loaded one route. →
   the denominator rule.
4. The first threshold calibration called a populated dashboard "not evidence" and
   passed a skeleton, because cross-cell variance cannot separate them on a mostly
   white surface. → within-cell contrast, measured against real captures.

---

## Provenance and its limits

The `codex-single-run` report carries two warnings from its own tooling: it restates a
large fraction of the brief and delivers its body twice. Its citations were
dereferenced — 28 of 30 resolved, one 404 (RegionFocus/ICCV), one 403 (Applitools,
login-gated). The Gemini panel member passed a fabrication check outright: 63
citations, none fabricated, 61 live.

A resolving URL proves a page exists, never that it supports the claim attached to it.
Numbers reproduced across two or more independent backends are marked as such above;
the rest are single-sourced and should be treated that way.
