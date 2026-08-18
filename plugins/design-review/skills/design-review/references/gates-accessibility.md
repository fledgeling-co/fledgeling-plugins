# Gates — accessibility, semantics, dark patterns

Tier 1. Deterministic, blocking, low false-positive. Run these before spending any judgment: they are cheap and they are empirically where the failures are.

Contrast, alt text, labels, empty links, empty buttons and missing `lang` account for 96% of all detected accessibility errors across the top million home pages. Start there.

## 1. Contrast and colour

**Ratios (WCAG 2.2 AA):**
- Normal text: ≥ 4.5:1
- Large text (18pt / 24px, or 14pt / 18.66px bold): ≥ 3:1
- UI components, state indicators, graphical objects needed to understand content, focus indicators: ≥ 3:1 against adjacent colours

**Thresholds are inclusive with no rounding.** Exactly 4.5:1 passes; 4.499:1 fails. Rounding up is not a permitted mechanism.

Compute the actual ratio for every colour pair you can resolve — follow tokens back to their source value rather than guessing from a screenshot. Flag each failing pair with its measured ratio and the required minimum.

**Read the foreground from style, not from pixels.** WCAG's own guidance says to take foreground and background values from the user agent or the markup and styles rather than from anti-aliased glyph pixels, because anti-aliasing makes edge pixels lighter than the specified colour. So pixel sampling is the right tool for *the backdrop beneath text* and the wrong tool for the text itself.

**A gradient is a range of backdrops, and the gate scores its worst end.** W3C's ACT rule 09o5cg publishes worked examples of exactly this — a passing gradient spanning 12.6:1 to 7:1, a failing background image spanning 1.4:1 to 4.7:1. Note that the failing one reaches 4.7:1 at one end and still fails: the operative sentence is that text fails if *any* relevant portion falls below its threshold, and WebAIM tells practitioners the same thing — test where contrast is lowest.

`probeContrast` therefore recovers the gradient's colour stops and scores against the worst one, tagging the record `declared-gradient-stop` or `computed-gradient-stop`. Two consequences to carry into the finding:

- **It is a High, not a Blocker**, unless the text fails against *every* stop. The glyph may not sit over the worst end, and a conditional measurement sold as a certain one is how a real finding gets discounted.
- **The reading is contested and the skill picked a side.** ACT's own automatable formulation takes the *highest possible* contrast and then explicitly cautions that passing it does not mean the text has sufficient contrast. This skill takes the strict reading because a fabricated pass is worse here than a conditional finding. `references/evidence.md` carries both positions.

Where the stops cannot be recovered — an image URL, `color-mix()`, a blend mode, a cross-origin stylesheet — the record is `cantTell` and belongs in the unresolved population, which is neither a pass nor a failure. axe-core does the same and says so in the same words: *"The background color could not be determined due to a background image."*

**The failure this replaced.** The old guard tested `if (cs.backgroundImage && cs.backgroundImage !== 'none')`. An engine that does not implement the property returns `""`, which is falsy, so the guard never fired and the walk climbed past the gradient to the opaque white `body`. Measured 18 Aug 2026 on `evals/fixtures/landing.html`: white 72px display type over `#6366F1 → #A855F7 → #EC4899` reported at **1.0:1** — the worst possible ratio, on text that renders legibly — and five of seven reported failures on that page were scored against that non-existent white backdrop. One of the five was a wholly fabricated failure — the h1 clears its 3.0 floor at every stop, worst 3.53:1 — and the other four were real failures carrying ratios wrong by 1.9 to 2.5 points. The second group is the more insidious one, because the verdict looks right and nobody re-checks the number. Truthiness is not a capability check.

**Ancestor-walking cannot resolve a background that a sibling paints.** `probeContrast` finds the background by climbing the text node's ancestors until it hits a non-transparent `background-color`. That is wrong wherever the visible backdrop is an *absolutely-positioned sibling* — a scrim over a photograph, a colour band, a clipped shape, a `::before` overlay, a video poster. The probe skips straight past it to the section's own colour and reports white text on a near-white canvas at 1.08:1 when the rendered pixels are 17:1.

The tell is a cluster of impossible failures on exactly the elements sitting over imagery, all quoting the *same* background. Before reporting any of them, re-measure from pixels: crop each text node's box out of a render and take the **median** pixel as the backdrop — glyph ink is a minority of a line box, so the median is the background and the sort is robust to antialiasing.

```python
px = list(img.crop(box).getdata()); px.sort(key=luminance)
bg = px[len(px) // 2]                     # median = backdrop, not ink
```

Report the two populations separately: ratios computed from resolved CSS, and ratios sampled from pixels. Never merge them into one count — the second is the only one that can speak for text over imagery, and the first is the only one that survives a re-render.

Report the computed figure, not a tidied one. A ratio quoted as 15.3:1 when the value is 15.518:1 changes no verdict, but it means the number in the report was typed rather than measured — and once one figure is approximate, no figure in the report can be trusted without recomputation. Three decimals costs nothing.

**Sweep the muted roles specifically.** Placeholder text, secondary and tertiary text, captions. Mid-grey tokens in the `#6b7380` neighbourhood fail 4.5:1 on light backgrounds most of the time, and muted-grey-on-tinted-near-white is the single most common contrast failure in generated design. "Muted" is a role, not a licence — secondary text still needs 4.5:1.

Grey text on a *coloured* background always looks washed out. Use a darker shade of the background's own hue, or the text colour at reduced opacity — never a neutral grey.

**An accent chosen against white needs a lifted variant for dark grounds, and a rule that actually reads it.** A brand colour picked for a light page will usually fail on a dark band: measured, `#D72229` on `#2E2B2B` is 2.77:1 against a 4.5 floor. Systems know this and carry an `on-dark` token for it. The failure worth checking for is the next one along — the token declared, emitted onto the page, and read by **no CSS rule**, so the accent text on every dark band is still painted in the raw accent. On one build the least readable text on the hero was the company's own name, 72px, at **2.14:1**, while `--primary-on-dark` sat in the DOM with a correct value.

`runAll().tokens.unconsumed` lists declared custom properties that no rule references (see `systematisation.md`). Its two honest limits — cross-origin sheets, and tokens read from JavaScript — are reported alongside the answer, so check the source before acting on an entry.

**Do not build contrast checks on APCA.** The WCAG 3.0 Editor's Draft of 8 April 2026 still marks visual contrast "Exploratory" and states the contrast algorithm for WCAG 3 is yet to be determined. APCA was flagged for removal in January 2023 and pulled in July 2023. Its own author has said nobody should drop WCAG 2 conformance over it. Use WCAG 2.2 ratios; if a design deviates, document the deviation rather than switching metric.

**Colour-only signalling.** Flag any state communicated by colour alone — green/red without an icon or text, a blue link with no underline, a chart with no legend or direct labels. Roughly 8% of men have a colour vision deficiency, and grayscale and high-contrast modes need a second signal regardless.

**Difficult combinations** to flag on sight: red+green; blue+yellow at similar lightness; light grey on white; coloured text on a coloured background of similar brightness.

**Pure `#FFFFFF` on `#000000`** is harsh and reads as unfinished. This is a craft recommendation, not a WCAG failure — file it as such.

## 2. Semantics and structure

- **Every page has a non-empty `<title>` describing it.** SC 2.4.2 Page Titled, **Level A** — the cheapest gate in this file and the most often skipped, because a title is invisible on the page it names. On a real run two whole route groups shipped with none: one exported no metadata at all, the other exported `metadata` carrying `robots` and no `title`. Four surfaces across every tenant showed the raw URL in the browser tab and in every share card. `runAll()` reports it as `semantics.title`; both runners flag `missingTitle`. A route group that exports metadata without a title is the shape to look for, not an absent metadata export.
- Exactly one `<h1>`. No skipped heading levels. Headings describe content, not visual size.
- Right element for the role: `<button>` not `<div onclick>`; `<a href>` not a styled div; `<label for>` bound to `<input id>`; real landmarks (`<nav>`, `<main>`, `<article>`, `<aside>`).
- Alt text on every meaningful image; `alt=""` on decorative ones. Meaningful alt describes what the image conveys, not what it is — `alt="Wireless headphones, side view"` beats `alt="product"`. Whether the alt is *contextually adequate* is a human judgment; note it as such.
- Every input has an associated `<label>`, or `aria-label` where visually labelless. Placeholder text alone is never a label — it disappears the moment the user types.
- Visual structure matches semantic structure: real lists, real tables, real headings.

**ARIA discipline.** Pages using ARIA average *more* accessibility errors than pages without, because deployment outpaces correctness. The decision order is strict:

1. Native HTML element with the right semantics
2. Native element restyled, if appearance was the reason for avoiding it
3. The ARIA APG pattern followed verbatim, if no native element fits
4. Closest APG pattern plus a documented deviation, as a last resort

Never invent ARIA. Flag any role/attribute combination that does not appear in the APG.

Note the specific generated-code failure: `role="button"` or `tabindex="0"` on a `<div>` binds no keyboard handlers. Check for the JavaScript, not the attribute.

## 3. Keyboard and focus

- Everything clickable is reachable by Tab. Hover-only menus, mouse-only dropdowns and modals that cannot be opened by keyboard all fail.
- Tab order follows reading order. Flag explicit `tabindex` values greater than 0 — they distort the natural order.
- Modals close on Escape. Dropdowns open with Enter/Space and navigate with arrows. Forms submit on Enter from a field.
- A modal that traps focus until dismissed is **correct behaviour**, not a keyboard-trap violation. The violation is a trap with no Escape or close path.
- Skip link as the first focusable element on pages with significant repeated navigation.
- In an SPA, a route change without a page load leaves focus stranded on the old page. Move focus to the new main region or its heading.

**`outline: none` without a replacement is a triple violation** — 1.4.11 Non-text Contrast, 2.4.7 Focus Visible, 2.4.13 Focus Appearance. It is not a style choice. The replacement needs ≥3:1 against the adjacent background; `:focus-visible` is preferred over `:focus` so the ring appears for keyboard navigation without firing on every mouse click.

Focus indicator geometry: 2 CSS px thick perimeter of the component, with ≥3:1 contrast between focused and unfocused states. Note that 2.4.13 Focus Appearance is **AAA**, not AA — cite it correctly. 2.4.11 Focus Not Obscured (Minimum) is AA and specifies no pixel value: the focused component must not be *entirely* hidden by author-created content, typically a sticky header or footer.

## 4. Target size

**24×24 CSS px is the AA floor.** SC 2.5.8 Target Size (Minimum), Level AA, verbatim: *"The size of the target for pointer inputs is at least 24 by 24 CSS pixels, except when:"* — followed by five exceptions.

**44×44 is the AAA bar** (SC 2.5.5 Target Size (Enhanced)) and matches the platform HIGs — iOS 44pt, Android 48dp. Note: the 44px figure is widely cited but was not confirmed against the criterion's own normative text during this skill's research, so treat it as the craft target it functions as rather than quoting it as spec.

Flag under 24×24 as a failure; under 44×44 as a craft recommendation on touch surfaces.

**The Spacing exception**, which is the one that matters in practice: *"Undersized targets (those less than 24 by 24 CSS pixels) are positioned so that if a 24 CSS pixel diameter circle is centered on the bounding box of each, the circles do not intersect another target or another undersized target's circle."*

Dense icon toolbars rely on this legitimately. It is not an excuse for an undersized primary action. The other four exceptions are Equivalent (the same function is available at adequate size elsewhere), Inline (the target is in a sentence), User Agent Control, and Essential.

Adjacent targets want ≥8px gaps on touch surfaces. Where the visible glyph is smaller than the hit area, extend the hit area with padding or a pseudo-element rather than growing the glyph.

## 5. The commonly-skipped AA criteria

These are rarely tested and frequently broken, which makes them high-yield.

| Criterion | Check |
|---|---|
| 1.4.4 Resize text | Text resizes to 200% without loss of content or function |
| 1.4.10 Reflow | Reflows to 320 CSS px wide without two-dimensional scrolling |
| 1.4.12 Text Spacing | Survives user-forced overrides — line-height 1.5×, paragraph spacing 2×, letter 0.12em, word 0.16em — without clipping. Fixed-height text containers fail this |
| 1.4.13 Content on Hover or Focus | Tooltips and previews are dismissible without moving the pointer, hoverable themselves, and persistent until dismissed |
| 2.5.2 Pointer Cancellation | No irreversible action fires on pointer-*down*. Commit on release so the user can slide off to cancel |
| 2.5.3 Label in Name | The accessible name contains the visible label text, or voice-control users cannot invoke the control |
| 2.5.7 Dragging Movements | Any drag-operated function has a single-pointer alternative |
| 1.3.4 Orientation | No lock to portrait or landscape unless the orientation is essential |
| 3.3.7 Redundant Entry | Information already provided is not asked for again. This is why email-confirm fields fail |
| 3.3.8 Accessible Authentication | No cognitive-function test in auth; paste is allowed |

Also: nothing flashes more than 3 times per second; auto-moving content is pausable; `prefers-reduced-motion` is respected; status messages are announced through live regions without stealing focus; modals restore focus on close and make the background inert.

## 6. RTL and bidi

Applies whenever the surface may render right-to-left or mixes scripts. Over 400 million people use RTL languages.

- Logical properties only: `margin-inline-start`, `padding-inline-end`, `inset-inline-start`, `text-align: start`. Physical `left`/`right` is the failure.
- Pair `dir` with `lang` — `<html dir="rtl" lang="ar">`. `dir` alone misses font-stack and locale behaviour.
- Wrap intrinsically-LTR values (phone numbers, IBANs) in `<bdi dir="ltr">` inside RTL paragraphs. A bare `<bdi>` misdetects weak-character runs.
- Never letter-space Arabic — it breaks cursive joining. No italics on Arabic or Hebrew; neither script has an italic tradition.

**Icon mirroring:**

| Category | Action | Why |
|---|---|---|
| Directional movement (back, forward, pagination) | Mirror | Movement relative to reading direction |
| Text alignment, chat bubbles | Mirror | Text flow changes the visual shape |
| Clock, play, rewind, media controls | Do not mirror | Represents time or physical tape direction, universally LTR |
| Magnifying glass | Do not mirror | Handle convention follows right-handed majority |
| Checkmarks, slashes, currency, chart axes | Do not mirror | Universal or mathematical, loses meaning mirrored |

## 7. Dark patterns — legal gates, not ethics

These are enforceable obligations in several jurisdictions, so they belong in the gate tier rather than the opinion tier.

**Click symmetry.** Count the steps required for opt-out versus opt-in, cancel versus subscribe, unsubscribe versus sign-up. More than 2× the clicks is a hard fail; 1–2× is a warning. CCPA requires symmetry in choice — the path to the more privacy-protective option cannot be longer, more difficult, or more time-consuming — and states that agreements obtained through dark patterns **do not constitute consent**.

**Scope note.** The EU framework is fragmented, and saying so is more accurate than asserting one rule. DSA Article 25(1) prohibits interfaces that materially distort or impair autonomous, informed choice, but explicitly excludes practices already covered by the Unfair Commercial Practices Directive and GDPR — so a GDPR-violating consent pattern is assessed under GDPR, not DSA. CCPA's definition is effect-based but scoped to privacy interfaces. EDPB Guidelines 03/2022 (deceptive design in social media) and 05/2020 (consent) name the specific patterns.

**Checkable patterns:**
- Pre-checked consent of any kind (illegal under GDPR, not merely rude)
- Opt-out buried in long text or behind more steps than opt-in
- Default sharing on
- Urgency or emotional language deployed to push consent
- Confirmshaming — a decline option worded to induce guilt
- Disguised ads; fabricated social proof

**The falsifiability triad** for any urgency, scarcity or social-proof claim. An honest claim is:

1. **Falsifiable** — the user could catch it lying
2. **Specific** — a verifiable referent ("3 rooms left in this rate class, updated 2:14 PM"; "access ends Tue 6 May")
3. **User-controllable** — a mechanism they can check

Zero or one of three is a manipulation finding regardless of how reasonable the copy sounds. "Registration closes Friday 6 June" qualifies; "Spots filling fast!" does not. A countdown that resets on refresh is fraud, not urgency.

Note the interaction with polish: a fluent, well-crafted surface raises the trust a dishonest mechanic then spends. Flag high-polish plus low-honesty as a priority finding, not as partial credit.

## 8. What this gate set cannot tell you

State these in "Needs verification" every time:

- Screen reader output and flow
- Whether focus order makes sense for the task
- Whether alt text is contextually adequate
- Dynamic ARIA state transitions
- Cognitive accessibility
- Real assistive-technology behaviour on real devices

Automated tooling detects roughly a fifth to under two-thirds of what an expert manual audit finds, and 2.49% of keyboard failures. A clean gate run means no known defect is present. It does not mean accessible.

## 9. Run these on a settled page, and say that you did

Every number in this file is a function of the moment it was sampled. Colour especially: a compositing element's rendered colour during a fade is not its colour, and nothing in the output distinguishes the two.

The failure in full, from a real run. An axe pass fired 400ms after a scroll sweep, into a 700ms reveal with an 80ms per-element stagger. It read a `#E85A2A` accent as `#6a2d18` and a body grey as `#414141`, and reported one surface going from 13 contrast failures to **28** *after* a fix that provably removed them. Every number was precise, internally consistent, and wrong — and the natural reading of it was "the fix made things worse", which is the expensive part.

So: scroll the document, drain `document.getAnimations()`, and **record how many were still running at the moment of measurement**. Draining without recording is not the fix; the recorded count is what lets a reader distinguish a clean gate from an unusable one. `runAll().settled` carries it, and both runners surface it as `animationsRunningAtMeasure`.

One consequence for before/after tables: **never quote two harnesses' numbers in the same column.** If you fixed the harness mid-review, the before figure came from the broken one. Re-measure the before, or exclude that gate from the table and say why.
