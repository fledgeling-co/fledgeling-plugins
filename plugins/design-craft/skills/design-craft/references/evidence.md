# Evidence — where these numbers come from, and where they disagree

Every rule in this skill that carries a number is either **measured on this machine**, **derived
from a published standard**, or **taken from research read at source**. This file records which,
so a later maintainer changing `4.5` in `scripts/design-lint.py` knows whether they are adjusting
a taste value or breaking a standards floor. It also records where the evidence contradicts
itself, because a skill that silently resolves a conflict has decided something on the reader's
behalf without saying so.

The research corpus is committed under `docs/deep-research/` — four independent backends
(OpenAI gpt-5.6-terra, Google deep-research, Perplexity sonar-deep-research, xAI grok-4.3),
**161 citations across the four**, run 18 Aug 2026. Fabrication check: **0 fabricated citations
of 161 checked.** OpenAI 48/48 resolved; gemini 63 checked, 0 fabricated, 9 bot-walled;
xai 13 checked, 1 bot-walled; perplexity reported 16 "404s" which are a **markdown artifact** —
its evidence table appends the footnote marker inside the href (`…/million/[14`), and every one
of those URLs resolves when the marker is stripped. Two load-bearing sources were then opened
by hand and confirmed at source; both are quoted below.

---

## 1. The contrast gate

**WCAG 2.x is the gate, and it is a standard rather than a preference.** 4.5:1 for normal text,
3:1 for large text (≥24px, or ≥18.66px bold) and non-text, inclusive with no rounding —
4.499:1 fails. All four backends agree, citing
[W3C Understanding 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum). This is
the one check in `design-lint.py` that fails at `critical`.

**Why contrast, of everything, earned the hard gate.** WebAIM's 2026 Million report — one million
home pages, read at source 18 Aug 2026 — found **low-contrast text on 83.9% of them, up from
79.1% the year before, and the most commonly detected accessibility issue by a wide margin**;
56.1 detected errors per page; **95.9% of pages with detected WCAG 2 failures**, an uptick that
undoes several years of gains. Those are only the *automatically detectable* failures, so the real
rate is higher. A skill that produces web surfaces and does not compute contrast is reproducing
the single most common defect on the web.

**APCA is deliberately not used.** It is perceptually better — polarity-sensitive, asymmetric,
and a better predictor of real readability, especially in dark mode — and it is not a standard.
gemini reports it was **removed from the WCAG 3.0 working draft in mid-2023** for lack of Working
Group consensus; openai reports the March 2026 WCAG 3 Working Draft still records its contrast
algorithm as **"yet to be determined"**, with APCA not named as adopted. Both conclude the same
thing and so does perplexity: WCAG 2.x is the deterministic gate, APCA is an advisory lens at
most. Gating on APCA would gate on a non-standard.

**Contrast is tri-state, and this is the finding that changed the design.** Three backends
independently describe the same failure mode. axe-core's own rule documentation accounts for
background *opacity* but names foreground opacity, CSS gradients, pseudo-element backgrounds,
borders-as-backgrounds, overlapping elements and off-viewport elements as difficult, and does
**not** report text over a `background-image`, text obscured by another element, or images of
text. To hold its zero-false-positive line it classifies those as **"Needs Review" / incomplete**
rather than as violations. gemini states the operational consequence bluntly: *an agent
programmed to halt only on definitive `violations` will silently ship inaccessible gradients and
translucent overlays, because the linter categorises those failures as warnings.* perplexity
arrives at the same three-state model from the other direction (violation / no violation /
measurement unavailable), and notes axe treats a 1:1 result as incomplete for exactly this
reason. So `design-lint.py` emits `contrast-unmeasurable` rather than skipping — **an unmeasured
pair and a passing pair otherwise serialise identically**, which is this skill's own epistemics
rule (`visual-verification.md` Phase 0 rule 4) arriving from outside.

**The pixel-median fallback ships with the gate, not instead of it.** WCAG's own sufficient
technique **G18** asks for a measurement at the letter/background boundary where the background
varies, and WebAIM's guidance is to test the region where contrast is *lowest* — a worst-case
sample, not a token comparison. That is why `accessibility-audit.md` checklist 1 carries the
median/95th-percentile pixel probe as a named technique rather than as a gesture: it resolves an
unmeasurable, and it adjudicates a *reported* failure that the cascade produced. A fabricated
failure costs as much as a fabricated pass.

### `<CONFLICTING_EVIDENCE>` What proportion of accessibility defects automation misses

Four numbers, three methodologies, no shared corpus. They are not reconcilable and the report
that says so is the one to follow.

| Figure | Source | What it actually measured | Found by |
|---|---|---|---|
| **57.38%** of all issues found automatically; for WCAG 1.4.3, **73,733 of 88,714** found automatically → **16.89% manual share** | [Deque's automated-coverage report](https://www.deque.com/automated-accessibility-coverage-report/), 13,000+ page-states, ~300,000 issues | issue *shares in Deque's own audit dataset* | openai (with the counts), perplexity, xai (as "57%") |
| axe-core **27%**, Pa11y **20%**, both together **35%** → a 65–80% false-negative rate | UK Department for Work and Pensions benchmark, via a11yflow / testparty | detection against a corpus of *known* issues | gemini |
| ~**57%** automatically, ~**80%** with Intelligent Guided Tests | axe-core maintainer, GitHub | tool capability statement | perplexity, xai |
| ">40% of real contrast defects in complex UIs" | xai's own inference | estimate; xai flags it `INSUFFICIENT_EVIDENCE` itself | xai |
| 9 tools over 121 pages: **every tool found issues the others missed**; 4% of tool-page runs failed outright | Pool, *Accessibility Metatesting*, ACM W4A 2023 (peer-reviewed) | complementarity, not recall | openai |

**Take openai's stance: there is no universal percentage, so name the classes instead.** Its
report says the defensible figure is the dataset-specific 16.89% manual share for 1.4.3, "not a
general law", and every backend converges on the same uncoverable classes: text over a gradient
or image where the lowest-contrast region is not sampled; a colour that changes in a state the
test never entered; effective contrast altered by alpha and stacking; and colours that depend on
user or platform settings the test environment does not reproduce. Those four classes are what
the lint's own "not checked" line names, and they are why it prints one.

## 2. The lint's substrate, and its severity model

**Parse over regex — unanimous, and only partly taken.** All four backends recommend an AST
(PostCSS/Stylelint for CSS, an HTML5 parser for markup) over text heuristics, and the reasons are
concrete: regex cannot distinguish a declaration from a comment, a Markdown fence, a string, a
custom syntax or a fixture; the HTML Standard specifies error recovery a string search cannot
reproduce. Two documented false-positive classes make the point on real tools rather than in
principle — stylelint's `no-descending-specificity` misfiring on nested selectors
([#8567](https://github.com/stylelint/stylelint/issues/8567)) and typescript-eslint's `no-shadow`
misfiring on static methods whose type parameters shadow the class's
([#2592](https://github.com/typescript-eslint/typescript-eslint/issues/2592)) — both of which are
*AST-aware rules* still getting it wrong, which is the honest ceiling.

**What was taken:** the markup half now runs through Python's stdlib `html.parser`, so `<img>`,
`<svg>`, `<div onclick>`, `<title>` and applied class names come from a real parse. **What was
not:** CSS, because there is no stdlib CSS parser and this script's constraint is zero
dependencies anywhere the skill is seeded, including a headless sandbox with no npm. The
mitigations are named in the file's own docstring rather than left implicit, and the checks that
would need the cascade or real specificity are **not written** — they are in the "deliberately NOT
checked" block instead, because a rule that cannot answer honestly is worse than an absent one.

**Path classification before checking, not more exact patterns.** openai:
*"a source-classification phase removes the dominant 'gate fires on its own documentation'
failure mode more reliably than adding ever-more-exact regex exclusions."* gemini names the same
failure as the "self-blocking loop" and the same remedy (`.stylelintignore`, `overrides`).
`design-lint.py` skips `docs/`, `references/`, `fixtures/`, `examples/`, `dist/`, `vendor/` and
all `.md` unless `--include-all` is passed — which the eval harness must pass for its own
fixtures, and that is assertion **A22**.

**Severity: a rule gates when it names a mechanism; it warns when it names a fashion.** This is
the organising principle the corpus produced, and it changed the gate. openai's tiering
(`BLOCKER` / `ERROR` / `WARNING` / `ADVISORY`) puts standards violations and runtime breakage at
the top and "typeface-family concentration, likely default aesthetic" at the bottom — explicitly
`ADVISORY` for "do not use Inter", with the reason: *"No direct evidence supports treating it as
an AI-authorship signal."* gemini's guidance is the same shape ("stylistic drift to `warning`,
structural failures to `error`, so the agent does not loop debugging its own read-only
documentation"), and perplexity recommends Biome's three tiers plus structured suppression.
So `pure-bw`, `gradient-stops`, `default-card`, `default-font`, `tailwind-indigo`,
`cream-token-name` and `decorative-emoji` **warn**; contrast, a removed focus ring,
`div onclick`, an unread token, a resting `opacity: 0`, a blocked resource and a missing title
**gate**. `untracked-caps` and `over-tight-tracking` stay gating on a different ground: they name
a legibility mechanism (counters collide; letters touch), which is typographic practice rather
than a claim about authorship.

**Suppression is not self-service.** perplexity is explicit that letting the agent add its own
suppression annotations risks a gate that gets trained to disable itself, and recommends
reserving suppression for human authors. This skill's compromise: a suppression is permitted, its
**reason is required** (a bare `lint-ok:` is ignored and reported), and both the script's
docstring and `unit-critique-gate.md` say a run that suppresses its way to zero has not passed.

## 3. "AI-generated" as a signature — the sharpest conflict in the corpus

`<CONFLICTING_EVIDENCE>` **Whether individual visual cues identify AI authorship to a human.**

- **gemini says yes and highly identifiable**: layout homogeneity, the ubiquitous three-column
  equal feature grid, generic split-hero sections, saturated purple/blue gradients, and
  *"repetitive typography pairings (e.g. Inter paired with Space Grotesk)"*. Its sources for the
  cue list are practitioner blogs (think.design, perfect-ui), not perceptual studies.
- **openai says the evidence does not support it**: *"there is insufficient direct perceptual
  evidence that any particular front-end cue reliably identifies AI-authored layouts to
  humans"*, and it files a `MISSING_DATA` for the controlled study that would settle it —
  blinded, preregistered, matched human/LLM briefs.
- **perplexity threads it**: the homogenisation is *measured*, the human-detection step is
  *inferred*, and it says so.

**Resolution taken, and it is a calibration rather than a pick.** The homogenisation is real and
measured; the authorship-detection claim is not. So the rules stay — including the named fonts,
because a face reached for by gravity rather than by reason is a *design* problem whatever a
stranger could infer from it — and the *tier* drops to advisory. What became mandatory instead is
the process, which is where the measured evidence actually is (§4). One small independent
corroboration worth recording: gemini names the Inter/Space Grotesk pairing unprompted, which is
the same pair `ai-slop-check.md` §5 names from this skill's own A/B. That is weak support for the
cue and no support at all for the detection claim.

**One number about usability, single-sourced, and bot-walled.** gemini reports an MDPI 2026 study
comparing human-designed, raw AI-generated and prompt-optimised AI-generated interfaces:
**63.10% task accuracy on the raw AI interfaces against 100% for both the human-designed and the
prompt-constrained AI ones**, and — the part that matters more — *pixel-level computational
visual metrics correlated only weakly with perceived usability*. The source
(mdpi.com/2079-9292/15/15/3458) returns 403 to an automated fetch, so it is plausible and
unconfirmed. It is not used as a threshold anywhere. It is recorded because it points the same
way as this skill's standing dependency on `ux-craft`: a visually dense, polished, unusable
surface is a real and measured outcome.

## 4. Anti-convergence, and the paper that anchors this skill's own doctrine

**"Design Theater" is the corpus's strongest single finding, and it was read at source.**
[arXiv:2607.22928](https://arxiv.org/abs/2607.22928) v2, accepted at AAAI/AIES — Imteyaz,
Imteyaz, Rajpal, Shaikh, Muller and Savage. **120 interfaces, five generative UI tools, 24 tasks**
spanning structural, styling and functional requirements. Confirmed verbatim at the abstract:

- **more than 25% of user-facing design rationales are not reflected in the generated
  interface, rising to 34% for functional requirements**;
- tools identified roughly **half** the UX principles embedded in the prompts (mean 0.54), and
  **four of the five implemented 6% or fewer functional principles**;
- cross-tool comparison shows **convergence in visual appearance and layout organisation, while
  colour choices varied more**.

Two of this skill's most distinctive rules are that paper's findings arriving from outside.
**"Your narration of what you fixed is not evidence"** (`unit-critique-gate.md` verdict pass) is
the Design Theater gap with a number on it. And the direction contract audited promise-by-promise
is a thinking-fidelity check by another name.

The third finding **sharpens** a rule rather than confirming it. `generate-variations.md` requires
each variation to commit to a different *primary* axis and warns that three shades of one colour
world is one variation. Design Theater measures that colour is precisely where generated designs
*already* diverge and layout is where they collapse — so varying colour buys the least, and the
structural axes (layout topology, structural decomposition, density, hierarchy) buy the most.
That ordering is now stated in the file.

**One correction to the record.** perplexity names the paper's three metrics as *Thinking Fidelity
Score*, *Principle Adherence Score* and *Design Homogeneity Index*. The abstract introduces
"three metrics" without naming them, so those names are **unconfirmed** — the findings above are
verbatim, the metric names are not, and this skill does not repeat them as the paper's own.

**Interventions, ranked by how well they are actually supported:**

| Intervention | Evidence | Status here |
|---|---|---|
| Critique-then-revise | Highest diversity among tested prompting methods in Ma et al. 2025 (4,000 GPT-4 design concepts, five topics), and the strongest lever in that study | Already the whole shape of `unit-critique-gate.md` |
| Explicit axis enumeration | Reasoned mechanism, not independently measured on front-end layouts | Mandatory (`generate-variations.md` Phase 3) |
| Verbalized Sampling — ask for a *distribution* with probabilities, then sample | ICML 2026: **1.6–2.1× diversity** over direct prompting; gemini adds "recovers up to 66.8% of the base model's latent diversity". Two backends, one lineage | Added to `frontend-aesthetic-direction.md` as the sourced form of the seven-candidate step |
| Forced material/family diversity | Sensible operationalisation, not benchmarked as an independent treatment | Mandatory (≥3 material families) |
| Temperature / top-p | Ma et al.: `t=1, top-p=1` was the most diverse *parameter* setting, but prompt structure mattered more. Everyone agrees temperature alone does not fix mode collapse | Not used; this skill has no sampling controls anyway |
| **Discard-your-top-pick** | openai: *"no corroborated direct evidence"*; "do not make it mandatory on the claim that it is empirically proven" | **Kept, and reframed.** It stays because it has a stated mechanism — the top-ranked candidate is what every run on this brief produces — and it is now presented as this skill's own house rule rather than as a finding |

**Held loosely, because it cuts against something this skill does.** aclanthology 2025
(findings-emnlp.836) reports that structured templates, role markers and formatting tokens
*constrain* an instruction-tuned model's output space and push it toward identical variants. The
direction contract is a structured template. The countervailing evidence is Google's own guidance
in `gemini.md` — that a categorical noun ships as one instance and an enumerated one ships whole —
and this skill's own measurement behind it. Both cannot be maximised: the contract's five blocks
are kept because the failure they prevent (an unaudited direction) is measured here, and the
diversity cost is noted rather than dismissed.

## 5. The capture engine, and why "verified" is rationed

Everything in SKILL.md's **Known limits** table and `visual-verification.md` Phase 0 is
**measured on this machine, 13 and 18 Aug 2026** — not sourced, not inferred. The corpus
corroborates the *class* of problem from three directions, which is why the table is framed as an
instrument's failure states rather than as a list of complaints:

- **The shorthand read is specified to be unreliable, not merely quirky.** CSSOM permits a
  shorthand serialisation to return an **empty string** when it cannot exactly represent all its
  longhands ([CSSOM-1](https://www.w3.org/TR/cssom-1/)). So "`getComputedStyle(el).background` is
  empty, therefore there is no background" is invalid *by specification*, on any engine. Read
  longhands.
- **`getComputedStyle(el, '::after')` is a supported API** per CSSOM and MDN — which makes
  Obscura's behaviour (ignoring the pseudo argument and returning the element's own style) a
  divergence from spec that answers confidently and wrongly. That is the worst shape a limitation
  can have, and it is why the table's framing is *"a capability whose absence returns a plausible
  value is worse than one that fails."*
- **Animation suppression is a documented default elsewhere too.** Playwright disables animations
  for screenshot assertions by default; finite animations are fast-forwarded and infinite ones
  cancelled. Chromium's headless mode has documented differences in screenshots, PDFs and
  GPU/WebGL. MDN notes `requestAnimationFrame` is paused in background tabs. None of that is
  Obscura, and all of it means the *general* practice — never conclude "motion is fine" from a
  default capture — is not a local workaround.
- **The three-state contract is the corpus's own recommendation.** openai's evidence schema
  requires `PASS | FAIL | UNAVAILABLE` plus engine, version, headless mode, viewport, DPR and
  states tested; perplexity requires "measurement not trustworthy" as a first-class outcome and
  Vitest's stable-screenshot detection as the model. `visual-verification.md`'s three-line report
  is the same contract in this skill's own vocabulary, and the "Not checked" line is the
  `UNAVAILABLE` channel.

## 6. CSP and the published-artifact surface

**The operative statement about the artifact platform is quoted, and one part of it is
technically imprecise.** Anthropic's own `shipyard:design` skill states the policy — "the iframe has no
network egress beyond its own origin, Google Fonts aside… `'unsafe-eval'` IS allowed" — and
`delivery-surfaces.md` quotes it because it is the authority on that platform's behaviour. But
`connect-src 'self'` governs **script-initiated** connections (`fetch`, XHR, WebSocket,
EventSource, Beacon), **not** `<script src>` loading, which `script-src` governs; fonts are
`font-src`; stylesheets are `style-src`. openai makes the distinction explicitly and warns
against exactly the inference the quote invites: *do not conclude a CDN script is allowed because
`connect-src` permits self.* The observable behaviour is unchanged — CDNs are blocked — so the
skill keeps the quote and adds the correction.

**`'unsafe-eval'` permits string-to-code execution and authorises nothing about origins.** Two
backends state this independently. It is the reason `make-a-prototype.md` now says the eval was
never the blocker and the load was — inlining Babel works because the script is *present* rather
than fetched.

`<CONFLICTING_EVIDENCE>` **Whether in-page transpilation should be allowed in a published
artifact at all.** openai says ban it outright (`CSP-004`: no `text/babel`, no Babel Standalone,
no eval-based loaders in published artifacts; transpile before publication). This skill says
pre-transpiling is preferred and inlining is a working fallback. Both are defensible: openai's
rule is right about the general case (a sandbox that forbids `unsafe-eval` breaks it, and most
do), and this skill's is right about *this* surface, where `'unsafe-eval'` is documented as
allowed. The disagreement is recorded rather than resolved, and the preference order in
`make-a-prototype.md` follows openai.

**The silent-failure signature, and its second-order failure.** All four backends describe the
first half: a blocked resource does not crash the page, it produces a console violation and a
degraded render — fallback typography, inert controls, an empty widget, a page that looks
plausible. gemini names the second half, which is the one worth carrying:

> Unless the verification script is instrumented to capture `Refused to load the script…` or
> `Refused to evaluate a string as JavaScript…`, the agent will assume the execution was clean.
> **The agent will then hallucinate that its core JavaScript logic is flawed, entering a loop of
> rewriting functional code**, rather than identifying the infrastructure-level block.

That is why `delivery-surfaces.md` treats reading the console as part of the check rather than as
debugging, and why "the console is part of the capture" is a rule in
`visual-verification.md` Phase 2 rather than advice.

## 7. This skill's own measurements

Everything below is `n=1` or `n=2` from a recorded run on this machine, and is dated at the point
of use in the file that carries it. It is the weakest evidence class here and the most specific:

- The **A/B pair** behind `ai-slop-check.md` Phase 1b (largest type 132px vs 76px, 19 vs 13
  distinct sizes, 1 vs 3 hue families, 1.8/3 vs 3.7/7 accent marks, 0 vs 3 external requests,
  0 of 12 vs 7 of 12 identical card rows). Aug 2026, one pair, one model. Directional, not a
  threshold — and now labelled as such in the file.
- The **Gemini calibration run** in `gemini.md` (`Egress Gemini`, 2026-08-17): every primary
  button at 3.65:1 while the artifact's own review claimed "100% pass rate on contrast"; 0
  `:focus-visible`, 0 `:active`, 0 `:disabled`, 12 `<div onclick>`; 45 raw hex against 11 tokens;
  4 images opened for 10 surfaces. That run is the single most direct argument for the contrast
  gate: the claim was fabricated and the arithmetic was available.
- The **multi-tenant incidents** in `data-driven-surfaces.md` and `accessibility-audit.md`
  (`#D72229` on `#2E2B2B` at 2.77:1 across 35 nodes; `#E65400` at 3.37/3.72:1 by role; a muted
  ramp at 2.98–4.41:1 with five of seven within 0.2 of passing; a `primaryOnDark` no rule read,
  leaving a 72px company name at 2.14:1).
- **The gate reproduces three of those four to two decimal places.** Verified 18 Aug 2026:
  `#D72229` on `#2E2B2B` → 2.773 (recorded 2.77); `#E65400` on white → 3.728 (recorded 3.72);
  `rgba(255,255,255,.44)` on `#181717` → 4.358 (recorded 4.36); `#767676` on white → 4.542
  (the WebAIM reference value). The fourth, `rgba(255,255,255,.34)` at a recorded 2.98:1,
  computes to **3.12** on `#181717` — the recorded figure does not name its ground, and the `.44`
  match to 2dp says the compositing is right, so the discrepancy is in the record rather than in
  the arithmetic. Left as-is and flagged here rather than quietly corrected.

## 8. Engine limits and render traps measured 21 Aug 2026

Three findings from one long-form build, all of which broke a layout while every source-level and
`matchMedia`-level check reported healthy. They are recorded here because each is the same class as
the ones already in this file: **a capability whose absence answers confidently.**

| Finding | How it presented | Where the rule lives |
|---|---|---|
| `ch` units inside `minmax()` do not resolve | `minmax(0,68ch) minmax(0,25ch)` collapsed both tracks to ~100px; the page set one word per line while the media query matched and the rule was present in source | SKILL.md § Known limits |
| `clip-path` is not applied | The `box-shadow: 0 0 0 100vmax` full-bleed idiom spread in every direction and painted over the last line of the section above | SKILL.md § Known limits |
| An unterminated `@media` block is silently dead | One dropped `}`; `matchMedia(...).matches` returned `true`, the rule was greppable, the node computed `display: block` | SKILL.md § 15, mechanic 7 |

**Tier: measured on this machine, n=1 build, Obscura 0.2.0.** Two of the three are engine-specific
and would behave correctly in a compliant engine; the third is a CSS authoring trap and is
engine-independent. The transferable rule in all three cases is the one § 15 already states — read
the computed value on the node, never the presence of the rule — which is why they were added as
evidence for an existing discipline rather than as new advice.

One motion finding from the same build, recorded against `gsap-motion.md`: an `opacity: 0` entrance
on the block carrying the page's conclusion left it as a void in every capture taken before the tween
resolved. **Tier: measured, n=1.** The rule derived from it (`gsap.from` so the authored markup is the
end state, and never animate the conclusion) is a restatement of the existing static-frame
requirement rather than a new constraint.

## What this file is not

None of the above makes a passing gate a verification. Every check in `design-lint.py` was
written after someone met the defect it catches, so the set is structurally blind to the defect
nobody has met yet — and the sourcing above raises confidence in the *thresholds*, not in the
*coverage*. That is why the script prints its own "not checked" line, why the report shape in
`visual-verification.md` Phase 4 separates what a machine asserts from what you assert, and why
this skill's Known limits section exists at all.
