# Evidence — where each rule came from

Every rule in this skill traces to a row below. The classes matter as much as
the citations, because a controlled test and a practitioner convention should
not carry the same authority even when they agree:

| Class | Meaning |
|---|---|
| **P** | Primary vendor documentation or a normative standard |
| **M** | A measurement: a study, a controlled test, or a large-sample census |
| **C** | Practitioner convention, with no measurement located |
| **X** | An anti-rule: something this skill deliberately refuses to enforce |

The corpus is four independent research reports totalling 182 cited sources,
exported to `docs/deep-research/email-digest-{openai,claude,gemini,perplexity}.md`
and argued through at <https://dossier.fledgeling.app/uniform>. Where the four
disagreed, the disagreement is recorded here rather than averaged away.

---

## The layout

| Rule | Class | Source |
|---|---|---|
| No item cap, asserted as a rule | **X / M** | MailerLite, 317,000 campaigns / 2.9bn emails: the 21+ unique-link bucket carries the highest click-to-open rate in the dataset at 6.72%. Campaign Monitor independently found click rate rising with link count to ~11 then plateauing. Scheibehenne, Greifeneder & Todd's meta-analysis (63 conditions, 50 experiments, N=5,036) pools choice overload to a mean effect size of virtually zero. |
| Three tiers: 2-4 featured, 5-9 compact, remainder one-line | **M** | Kong et al., ACM CSCW, 8-week field experiment, 117 completed records, 4,242 messages: top-news placement raised recognition 37%→49% and detail-reading 13%→22%. |
| Do not rank the long tail | **M** | Same experiment: message-order treatments below the top-news area produced no significant effect on interest, reading time or overall recognition. |
| The design target is rejection throughput | **M** | NN/g eyetracking, n=42, 117 newsletters: 51s mean time-after-open, 19% fully read, heatmaps concentrated on the first two words of headlines. Published 2006 and predates mobile; no modern equivalent was located by any backend. |
| Compact-tier icons are decorative, `alt=""` | **M** | NN/g 2017 (diary study n=9, usability testing n=28): full-width photos preferred, thumbnails rated less valuable and compelling, one previously-praised thumbnail newsletter re-classified as cluttered on re-test. |
| Primary links sit left | **M** | Kumar & Salo, *Journal of Marketing Communications* 24(5) 535-548: newsletter click-through follows a U-pattern with left-region links outperforming right, explicitly contrasted with the Z-pattern of web design. The one position finding measured in email rather than borrowed from the web. |

## The summary block

| Rule | Class | Source |
|---|---|---|
| No prose paragraph before the first item | **M** | NN/g: although introductions averaged three lines, 67% of users had zero fixations within them. |
| Exactly three highlights plus category counts | **C** | Convergent across all four backends despite disagreeing on why. NN/g's 6th-edition newsletter report recommends a brief contents block; that is usability guidance, not a reported effect size. |
| No internal anchor links | **M / P** | Mailchimp documents that recipients see the contents block but the links are not clickable; failure spans Apple Mail, Gmail, Outlook and Yahoo on iPhone and iPad. Litmus places Apple at 62.26% of opens. Anchor clicks also bypass ESP redirect tracking, so the variant is unmeasurable by construction. |

**The disagreement worth recording.** One backend argued a contents block
actively suppresses engagement through satisficing and completion bias, citing
survey-science literature. Another found no measured study in email either way.
The satisficing citation is about survey response, not email reading, so it does
not transfer as stated. All four nevertheless converge on the same
implementation, because the measured evidence (67% zero fixations) is about
*prose*, and a list of headline fragments is a different object — it is the
object the same heatmaps show readers actually fixating on.

**The gap.** No controlled study measures whether a top summary increases depth
of reading or satisfies the reader and reduces it. Instrument the block as its
own link set: if index links take meaningful share while below-index items
retain theirs, it amplifies; if index clicks cannibalise, it satisfies.

## Rendering

| Rule | Class | Source |
|---|---|---|
| Nested tables, inline styles, explicit widths | **P** | Microsoft documents classic Outlook's Word-based HTML processing. Rémi Parmentier's analysis of the CSS model: properties split into CORE, COREEXTENDED and FULL, with FULL available only on table elements. Consequences: `max-width` and `border-radius` ignored, CSS `background-image` needs VML, padding unreliable on `div` and `p`, `margin:0 auto` does not centre, media queries ignored. |
| No flex, grid, `position`, `transform`, `transition`, `animation` outside an mso guard | **P** | Google publishes Gmail's supported-CSS allowlist. It excludes all of these and states unsupported properties may be ignored. Gmail supports `var()` but not the custom-property declaration, so every `var()` resolves to its fallback — which makes design tokens useless in email and is why they must be flattened at build time. |
| No `<svg>` | **P** | Gmail strips the tag from the DOM entirely. A vector mark does not degrade, it vanishes. |
| Font stacks end web-safe; `mso-font-alt` on any `@font-face` | **M** | Outlook falls back to Times New Roman rather than to the next font in the stack. |
| HTML budget 90KB, warn at 80KB | **M** | Gmail clips near 102KB of HTML. Corroborated independently by Mailchimp, Litmus and Klaviyo; **documented by Google nowhere**. Applies to markup only — images, attachments and fonts do not count. Truncation lands at an arbitrary byte, so tables can be left unclosed, and it can hide both the ESP open pixel and the unsubscribe footer. |
| No base64 image data | **M** | Remote images do not count against the clip threshold and embedded ones do. |
| Subject varies per issue | **M** | Gmail threads same-subject messages and evaluates the thread's combined size against the clip. A recurring digest with a stable subject clips as a thread even when each issue is individually small. |
| Near-black and near-white, not `#000000`/`#FFFFFF` | **C** | Outlook.com's partial inversion targets those two values specifically rather than reacting to lightness. A heuristic against an undocumented detection rule, not a guarantee. |
| Colour-scheme meta tags only alongside a dark block | **M** | Apple Mail leaves markup untouched when the tags are absent and *partially inverts* when they are present without accompanying dark styles. One of the few deterministic dark-mode rules. |
| Left-aligned body text | **M** | Centred running text degrades readability, most sharply for dyslexic readers, by giving every line an unpredictable starting point. Added after a render here came out centred throughout: the outer `align="center"` that centres the card cascades `text-align` into every descendant. |

**Stale reference data, flagged.** Can I Email's test dates for the two features
most relevant to a modern layout are 2 November 2021 (`display:flex`) and
25 February 2020 (CSS custom properties). Treat those scores as lower bounds
with unknown drift. Classic Outlook is separately reported as reaching end of
life in October 2026, which would materially relax this section, but that date
was sourced only to a secondary compatibility guide and is not confirmed against
Microsoft's lifecycle documentation.

## Images

| Rule | Class | Source |
|---|---|---|
| **No text-to-image ratio gate** | **X / M** | Email on Acid tested against 23 popular spam filters: at 500+ characters, content-to-image ratio does not affect deliverability. Badsender files it under "Myths and Legends of Deliverability". The quoted figure varies between 60/40 and 80/20 by source, which is itself the tell. One backend proposed enforcing it as a hard gate; three rejected it. |
| Gate image-*only* communication instead | **M** | Outlook desktop blocks images by default, shows alt text only behind a security warning, and **will not allow it to be styled at all**; several clients reject alt text exceeding the image width; alt renders when images are turned off but not when an image is genuinely broken. Every failure mode lands on the same element. |
| Headline as a text node beside the image, never inside it | **M** | The banner's failure modes destroy the headline and the AI-generated inbox summary simultaneously. |
| 0-3 banner images | **C** | Bounded by the size budget rather than by a measurement. |

**The largest gap in the corpus.** No published test of banner imagery against
text-only for a developer audience exists. The general-audience UX evidence
(NN/g) favours large imagery; the developer-newsletter convention is close to
imageless and is demonstrated at scale by three publishers at 180,000, 216,000
and 1.6 million subscribers. These are not reconcilable by picking one, because
one is measured and the other is unmeasured but demonstrated. The resolution
here is asymmetric: large imagery only in the featured tier, where the measured
finding applies and the count is small.

## Accessibility and deliverability

| Rule | Class | Source |
|---|---|---|
| `role="presentation"` on every layout table, including nested | **M** | Email Markup Consortium, 443,585 HTML emails collected May 2024 to May 2025: 99.89% carried serious or critical automated issues and 21 passed cleanly. Missing table roles in 86.24%. The role is not inherited. |
| `alt` on every image, `alt=""` for decorative | **M** | Same corpus: missing alt text in 51.42%. |
| Descriptive link text | **M** | Same corpus: links without discernible text in 72.04%. Screen readers can list every link in isolation, where "Read more" is useless. |
| Real headings, one `h1`, no skipped levels | **M** | WebAIM Screen Reader User Survey #10: 71.6% navigate long pages by headings, 78% among advanced users, 88.8% rate heading levels useful. Web data, but the mechanism transfers: heading navigation is the screen-reader equivalent of visual tiering, and a tier built from styled `div`s gives sighted readers the benefit and screen-reader users nothing. |
| Contrast 4.5:1 normal, 3:1 large | **P** | W3C WCAG 2.2 SC 1.4.3. Same corpus: insufficient contrast in 59.37%. Not machine-checked here, because a client can undo it unilaterally by inverting. |
| Visible unsubscribe link plus RFC 8058 one-click headers | **P** | Google's sender guidelines, effective 1 February 2024 for senders above 5,000 messages/day, enforcement increased from November 2025: SPF, DKIM, DMARC, From-header alignment, one-click unsubscribe with both headers, **plus** a visible link in the body. Spam rate below 0.30%, guidance below 0.10%. |
| Plain-text MIME part | **C** | Required for accessibility and for clients that select it. |

## Metrics

| Rule | Class | Source |
|---|---|---|
| Open rate cannot select a winner | **P / M** | Apple documents that protected Mail clients download remote content in the background regardless of engagement. Litmus places Apple at 62.26% of opens, states MPP opens are not reliable, and estimates MPP touches 55-60% of all opens. Click-to-open is not a substitute: it divides by the same polluted denominator. Pixel-derived read time is likewise unavailable — Litmus writes `-1` into `read_seconds` for that audience. |
| Use bot-filtered unique clickers per delivered email | **M** | Security and privacy scanners click links, reportedly inflating raw click rates 10-35% on B2B lists. |
| Subject length warns, never fails | **M** | Three large datasets give three optima (~30, ~45, >70 characters). An academic study of 5,765 emails across 455 million users in 73 countries found no direct relation between subject length and attention. A hard gate would encode a disagreement as a fact. |
| Reject count-only subjects | **M** | Kong et al.: featuring a relevant item in the subject raised that item's read-in-detail rate from 15% to 24% with no significant overall open-rate difference. |
| The preheader is no longer a controlled surface | **M** | Apple Intelligence pre-open summaries are on by default and replace preview text with a two-line summary generated from the message HTML. The first real body text becomes the actual input, and reported quality is worst for image-heavy mail. |

---

## What this skill does not gate, because another one already does

`lint_email.py` covers the email medium. `ux-craft`'s `ux-lint.py` covers the
reading surface, and the two are meant to run together rather than one standing
in for the other.

Contrast and touch-target size are the clearest case. Both are in the table
above with primary sources (WCAG 2.2 SC 1.4.3 and SC 2.5.8), and neither is
implemented here, because `ux-lint.py` already resolves colour pairs statically
and probes a rendered page. Adding a second contrast implementation would mean
two gates disagreeing about the same standard, which is worse than one gate.

Run on this skill's own 24-item fixture, `ux-lint.py` found dead CSS that
`lint_email.py` missed: an `outline:none` left on the featured banner after the
element stopped being a link. That is the argument for running both, made
concretely rather than asserted.

Two of its checks do not transfer to email, and the reason is medium rather than
disagreement:

- **`no-focus-visible`** — Gmail's published CSS allowlist has no pseudo-class
  support, so a `:focus-visible` treatment cannot render in email at all. The
  finding is correct about the file and inapplicable to the artifact.
- **`state-coverage`** — an email has no states. There is no loading, error or
  partial state to cover.

Report both as not-applicable with the reason rather than suppressing them.
A check whose pass and whose cannot-run look identical is the failure mode this
whole corpus keeps running into.

---

## Figures that could not be traced, and must not be quoted

Two backends independently ran traceability checks. These eight circulate widely
and have no locatable primary source:

- 57% of a subscriber's viewing time is spent above the fold
- 70% of clicks recorded in the top 25% of a newsletter
- 43% of users view email with images off — traced to a 2013 Litmus figure
  specific to Gmail *before* it switched images on by default, with Litmus
  itself cautioning against extrapolating from it
- The 60/40 text-to-image ratio
- Optimised preview text increases open rate up to 45%
- 14-22% higher open rates from optimised preheaders
- Plain-text emails get nine times the engagement
- Plain text boosts open rates by 42%

**The instructive case is the fold.** The article most cited for email fold
statistics takes every figure from NN/g *web page* usability research covering
2010-2018. There is no email-specific scroll-depth measurement in it, Litmus
flags its own post as aged, and its conclusion is "it depends". Scroll depth has
no native event model in email at all, which is why publishers report click
distribution by template position instead. Any email fold statistic, traced back
far enough, arrives at web data.

## What remains unmeasured

Four of the seven questions in the original brief have no published study behind
them, and three of those are instrumentation-blocked rather than merely
unstudied:

1. **Tiered versus flat**, the central design claim. Unmeasured.
2. **A top summary block's effect on depth of reading.** Unmeasured.
3. **Banner imagery for a developer audience.** Unmeasured.
4. **Email-native scroll depth.** Structurally unmeasurable — HTML mail cannot
   execute the instrumentation the web uses.

Image-blocking prevalence is likewise unmeasurable in principle, because open
detection depends on an image loading, so a reader with images blocked is
invisible to the instrument. Anchor-link engagement is untrackable because
anchors bypass the ESP redirect.

A skill built on inference should say so, which is why the SKILL.md does.
