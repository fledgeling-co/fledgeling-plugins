# Accessibility section — dossier page

## Before the copy: the 35% line

I did not ship the line as written. The sentence you asked for was:

> vestibular disorders affect around 35% of adults over 40, so reduced-motion support is essential

The number is real but the sentence around it is not. Tracing it back:

- **Actual source:** Agrawal Y, Carey JP, Della Santina CC, Schubert MC, Minor LB. "Disorders of balance and vestibular function in US adults: data from the National Health and Nutrition Examination Survey, 2001–2004." *Arch Intern Med.* 2009;169(10):938–944. ([PubMed 19468085](https://pubmed.ncbi.nlm.nih.gov/19468085/))
- **What it actually found:** 35.4% of US adults aged 40+ (about 69 million people) showed **vestibular dysfunction** — measured by the modified Romberg Test of Standing Balance, a *standing-balance screening proxy*, across 5,086 NHANES respondents.

Three problems with restating that as the line above:

1. **"Vestibular disorders" ≠ what was measured.** The study screened balance performance (stand on foam, eyes closed, 20 seconds). It did not diagnose vestibular disorders. Reviewers of the method are explicit that it is a proposed indicator of vestibulospinal impairment, not a direct vestibular assessment. Notably, ~32% of the over-40s who failed reported *no dizziness at all*.
2. **US-only, not "adults".** It is a US national survey. The unqualified "adults over 40" reads as a global rate.
3. **The conclusion doesn't follow from that premise.** The study's outcome of interest is falls (up to a 12-fold increase in odds of falling among symptomatic participants), not screen-motion sensitivity. Using a balance-test prevalence to justify `prefers-reduced-motion` conflates two different things — and a reader who checks the citation will find that gap. The reduced-motion case doesn't need the inflation; it stands on WCAG and on the OS-level setting users have already set.

The copy below therefore makes the reduced-motion case on grounds that survive a click-through. If you want a headline prevalence number, use the Agrawal figure **stated accurately** (the optional variant is included), not the paraphrase.

---

## Section copy

### Motion and animation

Motion is opt-out at the operating-system level, and we honour that setting rather than overriding it. Every non-essential animation on this page is wrapped in a `prefers-reduced-motion: reduce` query: parallax, scroll-triggered reveals, autoplaying loops, and any transform that moves content a significant distance across the viewport are suppressed when a visitor has asked their device for reduced motion.

This matters because large-area or unexpected motion is a documented trigger for dizziness, nausea and disorientation in people with vestibular conditions, and for migraine and motion sensitivity more broadly. WCAG 2.3.3 (Animation from Interactions, Level AAA) requires that motion animation triggered by interaction can be disabled unless it is essential to the content. Respecting the system-level preference is the guideline's own recommended way of meeting that, and it costs the visitor nothing — they have already expressed the preference.

Reduced motion does not mean no motion. Small, local changes — a focus ring appearing, a button depressing, a colour crossfade — stay, because they carry meaning and do not move content through space. What goes is decorative movement: the kind that exists to look expensive.

We also hold two hard rules regardless of the preference setting. Nothing on the page flashes more than three times per second (WCAG 2.3.1), and any motion that starts on its own and runs longer than five seconds has a visible pause control (WCAG 2.2.2).

**Optional prevalence sentence, if you want a number in the copy:**

> A US national survey (NHANES 2001–2004) found that 35% of adults aged 40 and over showed measurable vestibular dysfunction on a standing-balance screening test — most of them without reporting any dizziness. Motion sensitivity is far more common than the people who mention it.

### Colour and contrast

Body text meets WCAG 2.1 AA contrast (4.5:1; 3:1 for large text and for the non-text parts of interface components). Colour is never the sole carrier of meaning — status, validity and category are always paired with text, shape or an icon, so the page survives being read in greyscale or by someone with colour vision deficiency. The palette is defined in both light and dark themes, and contrast is checked in each.

### Keyboard and focus

Every interactive element is reachable and operable by keyboard alone, in an order that matches the visual layout. Focus is always visible — we never remove the outline without replacing it with something at least as legible — and focus is never trapped. A skip link to the main content is the first thing in the tab order.

### Structure and semantics

The page is built from real landmarks and a single, unbroken heading hierarchy, so screen-reader users can navigate by structure rather than reading linearly. Images carry alt text that describes their purpose, or are marked decorative when they carry none. Charts and diagrams have a text equivalent nearby. Form controls have persistent, programmatically associated labels; error messages name the field and say how to fix it.

### Zoom and reflow

Content reflows to a single column at 320 CSS pixels wide with no horizontal scrolling, and remains usable at 200% zoom. Text spacing can be overridden by the visitor without content clipping or overlapping.

### What we have not solved yet

*(Keep or cut this subsection — but if you keep an accessibility section at all, a known-gaps line is what makes the rest of it credible.)*

- Third-party embeds are outside our control; where one fails a check, we note it at the point of use.
- We test with VoiceOver and NVDA; we do not currently test with JAWS or Dragon.
- Automated checks catch roughly a third of issues. The rest is manual, and manual means incomplete.

---

## Sources

- Agrawal Y et al., "Disorders of balance and vestibular function in US adults: NHANES 2001–2004," *Arch Intern Med.* 2009;169(10):938–944 — [PubMed](https://pubmed.ncbi.nlm.nih.gov/19468085/)
- Method caveat on the modified Romberg as a vestibular proxy — ["Measuring Vestibular Contributions to Age-Related Balance Impairment: A Review," *Front Neurol* 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7900546/)
- Age-related vestibular threshold change above 40 — [*Front Neurol* 2016](https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2016.00162/full)
- Vestibular disorder symptoms and triggers — [Vestibular Disorders Association (VeDA)](https://vestibular.org/article/what-is-vestibular/the-human-balance-system/vestibular-disorders-an-overview/)
- Why motion is a problem in digital content — [Equal Entry](https://equalentry.com/why-motion-on-websites-and-digital-content-is-a-problem/)
- `prefers-reduced-motion` implementation, and why "reduce" ≠ "remove all" — [CSS-Tricks](https://css-tricks.com/nuking-motion-with-prefers-reduced-motion/)
- User-side motion preferences — [MDN](https://developer.mozilla.org/en-US/docs/Web/Accessibility/Accessibility:_What_users_can_to_to_browse_safely)

**Note on a figure you may meet elsewhere:** the "70 million people" statistic that circulates in developer blogs is the same Agrawal study's US population estimate, re-quoted. It is not an independent corroboration of it, and it is not a count of people who need reduced motion on the web. Do not cite the two together as if they were two sources.
