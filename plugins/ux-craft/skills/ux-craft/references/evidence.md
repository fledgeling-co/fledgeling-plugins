# Evidence — where every number, law and measured claim here comes from

This skill's own rule, from `psychology-laws.md`: *if you can't trace a claim to research, label it practitioner judgment; never fabricate a citation.* This file is that rule turned on the skill itself. It exists because the predecessor version held its citations to a higher standard than its own measurements — seven specific, checkable numbers appeared with no date, no run and no instrument named.

## The correction that arrived with the fourth panel member — added 2026-08-21

The account these rules were first written from was mechanically wrong in one place, and the fourth
research member caught it.

| Claim | Source | Tier | Limit |
|---|---|---|---|
| A denied tool's definition is removed from the request, so the model never sees it and cannot attempt it | [Agent SDK permissions](https://code.claude.com/docs/en/agent-sdk/permissions) | Vendor documentation | Documents a bare-name deny; an allowlist-plus-discovery path is not covered explicitly |
| Diagnosis time fell **60.7%**, 10.37 +/- 2.18 minutes against 25.72 +/- 3.75, with proactively-added error logs, at 1.4% runtime overhead | [ErrLog, OSDI'12](https://www.eecg.utoronto.ca/~yuan/papers/osdi12-errlog.pdf) | Measured, controlled, 20 programmers | Conventional software, not agent runs |
| Automation bias occurs in naive and expert participants alike and cannot be prevented by training or instructions; failure-exposure training helped omission errors but not commission errors | [Human Factors](https://journals.sagepub.com/doi/10.1177/0018720810376055) | Measured, review | Not agent supervision |
| A truncated generation ends with a 200 OK and a stop reason in the body, so nothing in the stack raises | Vendor stop-reason documentation | Vendor documentation | Describes one provider's API |

**What it changes.** Surfacing refused calls was written as the first fix and is now a partial one: where
a capability is withheld from the agent's context there is no refusal event, so the manifest is the only
surface an absence appears on and a preflight is the only check that fires when nothing was attempted.
**What it does not change:** the channel-placement conclusion, which the 60.7% figure strengthens
considerably.

**Verified against the code rather than the docs.** The pipeline in question used an allowlist plus a
matching discovery list rather than a bare-name deny, and its own comment records that excluding a tool
from the allowlist *alone* was measured insufficient once, with a call executing before a later denial.
So refusals were possible in an earlier configuration and not in the one that failed. Settling it
completely needs a run trace showing whether any attempt was ever recorded; that was not available, and
the limit is stated where the rules live.

## The evidence tiers

Three tiers, and the weaker ones are named as weaker. Declaring which tier is stronger is the point; a flat list of "sources" hides the difference.

| Tier | What it is | How far it carries |
|---|---|---|
| **`[normative]`** | The text of a published standard, quoted from the standards body's own document | Strongest. A conformance claim may rest on this and on nothing else |
| **`[docs]`** | A vendor's or platform's published guidance, read at source | Strong for that platform's craft expectations. Never a conformance claim |
| **`[measured]`** | An observation from a recorded run or a live surface, with the run named and dated where it was recorded | One data point. Named so you can weigh it, never generalised into a law |
| **`[judgment]`** | Practitioner consensus with no study behind it | Usable, and says so. Never dressed as research |

A claim with no tag in this skill is `[judgment]` by default. That default is deliberate: it costs nothing to be honest and it stops the strongest reading being the free one.

## Accessibility numbers

**Verified at source, 2026-08-18**, from `w3.org`:

| Claim | Source | Level | Status |
|---|---|---|---|
| Target size minimum **24 × 24 CSS px** | WCAG 2.2 SC 2.5.8 Target Size (Minimum) | **AA** | `[normative]` — the only target-size number a WCAG failure may cite |
| Its five exceptions: Spacing (a 24 px-diameter circle centred on the target overlapping no other target's circle), Equivalent, Inline, User Agent Control, Essential | WCAG 2.2 SC 2.5.8 | AA | `[normative]` — part of the criterion, not loopholes |
| Target size enhanced **44 × 44 CSS px** | WCAG 2.2 SC 2.5.5 Target Size (Enhanced) | **AAA** | `[normative]` — a miss is an AAA gap, never an AA failure |
| CSS pixel = "the visual angle of about 0.0213 degrees" | WCAG 2.2 glossary | — | `[normative]` — this is why a CSS px is not a device pixel |
| Focus indicator area ≥ a 2 CSS px thick perimeter, ≥ 3:1 focused-vs-unfocused | WCAG 2.2 SC 2.4.13 Focus Appearance | AAA | `[normative]` |
| Focus not obscured by author content | WCAG 2.2 SC 2.4.11 | AA | `[normative]` |
| Redundant entry — previously entered information is auto-populated or selectable | WCAG 2.2 SC 3.3.7 | **A** | `[normative]` — a billing address with no "same as shipping" bypass is the canonical failure |
| Accessible authentication — no cognitive function test in any authentication step | WCAG 2.2 SC 3.3.8 (Minimum) / 3.3.9 (Enhanced) | **AA** / **AAA** | `[normative]` — blocking paste into a password field, or blocking a password manager, is the canonical violation; 3.3.9 additionally removes object recognition and personal-content identification as acceptable alternatives |
| Dragging movements have a single-pointer alternative | WCAG 2.2 SC 2.5.7 | **AA** | `[normative]` |
| Body text ≥ 4.5:1, large text ≥ 3:1, UI components and focus indicators ≥ 3:1 | WCAG 2.1/2.2 SC 1.4.3, 1.4.11 | AA | `[normative]` |

**Not verified at source in this session**, and flagged rather than smoothed over:

| Claim | Standing |
|---|---|
| Apple HIG minimum tap target **44 × 44 pt** | `[docs, unverified 2026-08-18]` — `developer.apple.com/design/human-interface-guidelines/layout` returned **zero bytes** through Obscura and title-only through WebFetch; both are client-rendered. The figure is long-standing and widely reported, the unit is points, and neither could be read off the page today. Treat it as a craft target and never as a conformance claim |
| Android / Material minimum touch target **48 × 48 dp** | `[docs, unverified 2026-08-18]` — `m3.material.io` likewise returned zero bytes through Obscura. Same handling |

That the two vendor numbers could not be read at source while both WCAG numbers could is itself the argument for the resolution in NN7: the conformance claim rests on the tier that was verifiable.

## The behavioural claims, and how strong each actually is

The predecessor's best single quality was a section arguing against its own citations. This extends it. Where the popular framing overstates the research, Advise mode is required to say so.

| Claim as usually cited | Status | What survives |
|---|---|---|
| **Nudges produce large behaviour change** (Thaler & Sunstein) | **Substantially weaker than popular framing.** Meta-analytic correction for publication bias puts average effects near zero (Maier et al. 2022 re-analysis of the nudge literature) | The *structural* claims: defaults matter, framing matters, there is no neutral presentation. Do not promise conversion lifts from re-ordering options |
| **Choice overload — more options reduce action** (Iyengar & Lepper 1999, the jam study) | **Context-dependent, not universal.** Across many conditions the effect is near zero (Scheibehenne, Greifeneder & Todd 2010 meta-analysis) | Reduce options at *decision points* — purchases, one-time commitments, unfamiliar choices. Never thin an expert tool palette or a browse surface; density is a feature there |
| **Aesthetic-usability effect** (Kurosu & Kashimura 1995; Tractinsky) | **Real but bounded.** Erodes with repeated use and does not survive a severe usability failure | It buys forgiveness on first contact, not a pass. It is also why polish on a manipulative flow makes the flow worse |
| **Miller's 7±2** | **Superseded, and misapplied twice over.** Miller measured *immediate recall* of a rehearsed string; Cowan 2001/2010 revises un-rehearsed working-memory capacity to ~4±1 | Use 3–5 where the user must *hold* something: a verification code, a set of steps, ≤4–7 visible fields per step. **Not as an item cap on a persistent surface** — a nav bar or dashboard stays on screen, so the user is recognising rather than recalling, and the cost there is visual search, governed by grouping and labelling. "≤7 top-nav items" was a rule in the predecessor version and it was wrong |
| **One thing per page** (GDS) | `[docs]` — a government design-system position validated across large transaction volumes, published as guidance rather than as a paper | Strong for public-service and checkout flows; bendable for expert tools and editing contexts, never for checkout or registration |
| **50 ms first impression** (Lindgaard et al. 2006) | **Robust for visual-appeal judgment**, stable on re-test | The first viewport is a thesis statement. It does not license claims about comprehension or trust forming that fast |
| **Hick's Law** (Hick 1952) | **Largely fails to transfer to a structured graphical interface.** Robust in its original paradigm — abstract stimulus-response, unfamiliar mappings — but a CHI 2020 review (Liu et al.) finds that in GUI navigation visual search, categorical grouping and familiarity govern the time, and choice-reaction time can stay flat as options rise | Cut visible choices at *decision points* and justify it as reduced deciding. Never compute a time from the formula, and never cite Hick to thin a well-grouped workspace. **Citation caveat:** this finding reached us cited to a video rather than to the paper; the direction is consistent with the rest of the literature and the specific attribution is unconfirmed |
| **Fitts's Law** (Fitts 1954) | **Robust, including on touch** in its general form, but the absolute floor differs: a fingertip is 16–20 mm wide against a cursor's single pixel | Big, close primary actions; generous hit areas. The law transfers; the minimum sizes do not |
| **Jakob's Law** (Nielsen) | `[judgment]` — a practitioner formulation, not a study | Users arrive with expectations trained elsewhere. Be conventional about the interface, innovative about the product |
| **Doherty threshold ~400 ms** | `[judgment]` originating in a 1982 IBM productivity observation, widely repeated as a law — but it now has a measurable descendant | Keep the loop under ~0.4 s or show progress; ~100 ms feels instant. Where you need a number you can actually measure, use Interaction to Next Paint under 200 ms at the 75th percentile |
| **Peak–end rule** (Kahneman) | **Robust, and confirmed in an interface setting.** A NASA-TLX study found a high-friction task placed at the *end* of a sequence worsened the retrospective workload rating for the whole session against the same task in the middle | Invest in the success moment and the exit. Never put the hardest step last for implementation convenience |
| **Serial-position effect** (Ebbinghaus) | **Context-dependent in interfaces.** Item familiarity and brand recognition override position, so a recognisable item mid-grid performs like one at an edge | Use it to order *unfamiliar* sets — a new nav, an email's sections. Do not use it to argue about placing something the user already knows by name |
| **Loss aversion ~2×** (Kahneman & Tversky 1979) | **Robust in the original framing**, with the magnitude contested and context-dependent | Loss framing works *only when the loss is real*. A countdown that resets on refresh is fraud, not framing |
| **Inline validation improves completion** (Wroblewski / Etre 2009) | **Single small practitioner study, and a search for replications found none.** Treat the completion claim as `[judgment]` | Validate on blur, re-validate on change after a first error. What survives independently is the failure it identified: telling a user they are wrong mid-word |
| **Single-column forms convert better** (Penzo 2006 eye-tracking; Baymard) | **No controlled experiment establishes an effect size.** The same is true of one-page vs wizard and guest vs account-required checkout — practitioner consensus with vendor case studies, no peer-reviewed number | Single column by default, argued as a clearer scan path and a shorter label-to-field distance. Never quote a percentage |
| **Autofill raises completion** | **Vendor observational dataset, not a trial**: 71% completion with autofill against 59% manual, a 12-point absolute gap, with keystroke effort down as much as 80%. Direction is credible, the decimals are not | Set `autocomplete` tokens. **And know the other half: in ~10% of forms in that dataset autofill *lowered* completion**, because the cached value's shape failed the field's own validation and the user could not resolve it. Token, input type and server validation must agree, and the form must be tested by autofilling rather than typing |
| **Type-to-confirm reduces destructive-action errors** | `[judgment]` — universally adopted, **never measured**. No published study compares its error rates against a plain dialog or against undo | Argue it as a deliberate shift from an automatic click to a conscious act of typing. Where the two conflict, prefer undo: a recoverable mistake beats a well-gated irrecoverable one |
| **A live region announces what you put in it** | **False in a way that breaks a pattern this skill recommends.** A region injected already containing its text usually does not announce at all, and an interactive element inside a live region is flattened to plain text with its role stripped | Render the region empty and permanently, then write text into it. Keep the undo control *outside* the live region and keyboard-reachable — a time-limited undo only mouse users can reach is a countdown, not an undo |
| **Automated scanners establish accessibility** | **False.** Scanners read the static DOM, and the gap against manual assistive-technology testing is widest exactly at the dynamic state changes an SPA is made of | The gate script and a probe narrow the unverified set. They never empty it, and no run of either supports a conformance claim |
| **The research base is WEIRD** | **Robust as a methodological critique of the field** | The architecture is expected to be universal; the calibration is cultural. Validate trust and first-impression choices with target-market users |

Where two sources conflict, the conflict stays visible here rather than being resolved silently. The two live ones: whether inline validation's completion benefit replicates outside the original study, and whether the nudge literature's structural claims survive at a magnitude worth designing for.

## Measured claims in this skill, and their provenance

`[measured]` claims are single observations. Named runs are weighable; unnamed ones are flagged rather than deleted, because the observation is real and specific and deleting it would lose a genuine finding to tidiness.

**Run `Egress Gemini`, 2026-08-17, n=1.** One recorded run of this skill plus `design-craft` on a rich brief for a two-platform CI-runner app, producing `~/Dev/egress/design/mocks/html/index.html`; a comparable run on a near-identical brief produced `interaction-mock.html` beside it, and both were probed with the same scripts. Everything below is from that run:

- One state of six delivered across five surfaces; no `data-state` or state attribute of any kind. (SKILL.md Build step 4, NN3)
- `:focus-visible` 0, `:focus` 0, `:active` 0, `:disabled` 0, six `:hover` rules; `aria-*` 0, `role=` 0, `tabindex` 0, `prefers-reduced-motion` 0, and 12 `<div onclick>` carrying the whole navigation of both apps. (NN3, NN7, and the reason `ux-lint.py` exists)
- Contrast: every primary button 3.65:1, every selected sidebar row 3.65:1, a section header 3.37:1, one `+` glyph at **1.00:1** — invisible against its own background — beside a self-authored review claiming "100% pass rate". (NN7, NN12)
- `Cancel All Runners` (red, destructive) beside `Set Max Concurrency` (blue, primary) at equal weight, destructive first in reading order. (NN1)
- Every destructive action fired a 3-second toast and nothing else, while `Stop` on an idle runner was styled destructive-red. (NN6)
- A 4-step onboarding rail highlighting step 2 while its body showed step 1, over a sidebar advertising a fully configured cluster. (NN2, Build step 3)
- A `DESIGN.md` review matrix reading "Verified & Tested" on every row including a contrast row the artifact fails. (NN12)
- A `DESIGN-REVIEW.md` with five surfaces, five rows, all PASS, from a named browser engine that failed on all four attempts and never ran. (The probe-honesty rule)
- Five prominent controls spilling their own fixed-height boxes, one with its arrow glyph clipped by the button's bottom border. (`ux-lint.py --probe`)

**Live-surface observations, run and date not recorded.** Each is specific and checkable; none carries an instrument or a build. Any new measured claim added to this skill must carry its run and date, and these stand as the reason that rule exists:

- A 156 px reserve against a 76 px dock leaving 2 px of clearance. (NN11)
- `Constant ratio 1.1765%` printed beside a legitimate axis note on three slides of one investor deck. (NN12)
- A contact form on which three empty fields submitted reached "Not sent — your text is still in the field above". (`flows-and-forms.md`, the `novalidate` rule)
- A 327 px drawer at `left: -8` clipping the first glyph of every label on one tenant of six. (`flows-and-forms.md`, navigation)
- 387 items in one section: 83,703 px of document, 93 viewport-heights, 6,429 DOM nodes, zero controls. (`flows-and-forms.md`, lists)
- An empty `<nav aria-label="Investor portal">` shipped across 7,404 generated pages. (`flows-and-forms.md`, chrome)
- Five live sites whose hero eyebrow and H1 were the same string, and whose per-instance copy was character-identical after the substituted name. (`ux-writing.md`)
- Two pages from one corpus: the weaker carried one hedge-free statement of a limit in 3,700 words, the stronger twenty-six. (`ux-writing.md`, uncertainty as content)
- One generated investor deck whose every headline figure traced cleanly while the prose around them added a facility's dimensions, a second operating region, a competitive claim and a derived ratio set in a chip. (`data-provenance.md`)

**Engine limits, measured on this machine, 2026-08-13 and 2026-08-18.** The Obscura table in `review-playbook.md`. Each entry is a measurement of the tool rather than of a design, and each has already produced a false finding — which is why they are rules and not notes.

## Diagnostic quality and automation bias — added 2026-08-21

Four external findings, added after a three-week root-cause hunt in an AI-agent pipeline ended at a
failure reason that existed in a datastore and reached no channel a person read. They back
non-negotiable 4 and the supervision section of `ai-product-ux.md`, which previously carried no
effect size and no automation-bias material at all.

| Claim | Source | Tier | Limit to state |
|---|---|---|---|
| Explicit, pinpointing diagnostics diagnosed **3–13×** faster than ambiguous messages and **1.2–14.5×** faster than none | [Controlled diagnosis study of configuration problems](https://citeseerx.ist.psu.edu/document?doi=7fb221c90643acdf146e56fe04632c13829bff82&repid=rep1&type=pdf) | Measured, controlled | Conventional software, not agent runs; the ranges are wide |
| Redesigning a diagnostic alone cut mean correction time 225.90 → 194.18 s and raised success 77.1% → 84.9% | [Empirical Software Engineering, 2025](https://link.springer.com/article/10.1007/s10664-025-10695-1) | Measured, controlled | One task domain (SQL); a modest absolute effect |
| Monitoring accuracy **59% with an automated aid against 97% without**; **3.92 commission errors in six opportunities** with correct contradictory instruments available | [Does automation bias decision-making?](https://www.researchgate.net/publication/222507469_Does_automation_bias_decision-making) | Measured, simulator | Flight-deck fault monitoring, not progress watching; 1998; small task set |
| Risk ratio **1.26, 95% CI 1.11–1.44** for following erroneous automated advice | [Automation bias: systematic review and meta-analysis](https://pmc.ncbi.nlm.nih.gov/articles/PMC3240751/) | Measured, meta-analysis | Mostly clinical decision support, where the aid issues an explicit recommendation |
| The out-of-the-loop performance problem: disengaged operators are slower to detect, understand and respond to failures | [Endsley and Kiris, *Human Factors*](https://journals.sagepub.com/doi/10.1518/001872095779064555) | Established, foundational | 1995, aviation and process control, before agent harnesses existed |

**What the set supports, and what it does not.** Together they support one conclusion: the
intervention is *where the signal is placed*, not how hard the operator looks. None of them has
been reproduced on an agent pipeline, so any claim about MTTD or MTTR for capability manifests or
refusal surfacing specifically is **not measured** — the skill says so where it recommends them.

## The canon map

Where each author's load-bearing ideas are operationalised. This is a routing table, not a bibliography: it tells you whose lens to apply, and where the file that applies it lives.

| Source | Load-bearing ideas | Lives in |
|---|---|---|
| Krug, *Don't Make Me Think* | Self-evidence, scanning not reading, trunk test, omit needless words, mindless choices | review-playbook, ux-writing |
| Norman, *Design of Everyday Things* | Affordances, signifiers, feedback, conceptual models, mapping, constraints, error = design failure | psychology-laws, review-playbook |
| Garrett, *Elements of UX* | Five planes (strategy → scope → structure → skeleton → surface); lower planes constrain upper | review-playbook (review altitudes) |
| Cooper, *About Face* | Goal-directed design, personas as goal proxies, posture, eliminating excise | flows-and-forms |
| Yablonski, *Laws of UX* | Hick, Fitts, Jakob, Miller/Cowan, aesthetic-usability, peak-end, von Restorff, Tesler, Doherty, goal-gradient | psychology-laws (with the status table above) |
| Weinschenk, *100 Things* | How people see, read, remember, decide; attention and error patterns | psychology-laws |
| Eyal, *Hooked* | Trigger → action → variable reward → investment, with the ethics gate applied | psychology-laws (§ engagement), email-ux (lifecycle) |
| Wathan & Schoger, *Refactoring UI* | Hierarchy via weight/colour before size; de-emphasize instead of emphasize; labels last resort; design states not screens | flows-and-forms, plus design-craft for the visual system |
| Tidwell, *Designing Interfaces* | Pattern vocabulary for navigation, data entry, search, lists | flows-and-forms, mobile-ux |
| Lidwell et al., *Universal Principles* | Progressive disclosure, forgiveness, performance load | psychology-laws |
| Wroblewski, *Mobile First* / *Web Form Design* | Mobile constraints force clarity; one-thumb reach; forms as conversation; validation timing | mobile-ux, flows-and-forms |
| Allen & Chudley, *Smashing UX* | Right technique per situation; checklists as scaffolding | review-playbook, checklists |
| Gothelf, *Lean UX* | Mock to learn, not to specify; hypothesis over requirements; smallest testable thing | SKILL.md Build mode |
| Buley, *Team of One* | Lightweight, high-leverage methods when you are the only UX voice | the whole skill's default posture |
| Portigal / Torres | Research and continuous discovery | **out of scope** — route to `intent-layer` or `discovery-sentinel` |

## Deep research corpus, and how good its citations are

`docs/deep-research/` in this plugin carries the full report behind the status table above, exported so every claim here stays auditable from inside the repo rather than from a link:

- `gemini-forms-flows-replication-wcag22.md` — Google Gemini Deep Research, fast tier, academic archetype, 2026-08-18, ~$3.00, 26 cited sources. Question: the primary-source evidence base for forms, flows and error recovery; the replication status of the behavioural claims this skill cites; WCAG 2.2 target size from the normative sources; and what assistive-technology behaviour cannot be judged from a static render.

**Its citation quality, measured rather than assumed.** The fabrication check passed: 26 citations, **0 fabricated, 0 dead links, 0 malformed URLs**. Reachability is weaker — 15 of 26 opened directly and 11 returned 403, which is a paywall or a bot wall and says nothing about whether the source is real. Two specific weaknesses matter more than the count, and they are why the rows above carry caveats rather than clean verdicts:

- **Four load-bearing meta-analyses carry no usable URL.** Scheibehenne et al. 2010 (choice overload), Maier et al. 2022 (nudge effect sizes after publication-bias correction), Cowan 2001 (working-memory capacity) and Lindgaard et al. 2006 (the 50 ms judgment) were each reported with the citation marked unverifiable by the report itself. That is honest behaviour — it declared the gap instead of inventing a link — and it means those four claims currently rest on the model's own knowledge rather than on a fetched primary source. They agree with what this skill already held, which is corroboration of a sort and not verification.
- **One peer-reviewed claim is cited to a video.** The CHI 2020 review on Hick's Law failing to transfer to GUI navigation is attributed to a YouTube URL. The direction is consistent with the rest of the literature; the specific attribution is unconfirmed and is flagged in the row itself.

**Panel composition, and what did not run.** The plan assembled four backends. Only one started: **Google Gemini Deep Research** ran and completed. The other three did not, and the reason is recorded rather than dropped — the concurrency ceiling was saturated by other work at dispatch time, so **Perplexity Sonar Deep Research, OpenAI gpt-5.6 and xAI Grok are recorded as failed to start, not as omitted.** A single-backend result is a single reading of the literature; where this file says a claim is robust or weaker than its framing, that verdict has one research backend behind it plus the primary standards documents read directly, and not a panel that agreed.

Two disagreements are held open rather than resolved: whether inline validation's completion benefit replicates outside the original study, and whether the nudge literature's structural claims survive at a magnitude worth designing for. Where a report and this file conflict, this file records the conflict rather than picking a side.
