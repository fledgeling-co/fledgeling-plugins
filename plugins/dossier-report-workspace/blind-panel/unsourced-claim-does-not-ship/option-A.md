# Accessibility section — draft, with one line withheld

## The line I did not put on the page

You asked for this sentence:

> vestibular disorders affect around 35% of adults over 40, so reduced-motion support is essential

I have left it out, and I want to be direct about why rather than quietly dropping it.

This brief's own evidence file already flags this number by name. From the project design notes (Accessibility floor):

> One number to avoid: the claim that vestibular disorders affect ~35% of adults over 40 circulates widely without a traceable epidemiological citation. The mechanism is well sourced (W3C SCR40); the prevalence figure is not. Do not put it on a page.

And the project design notes records how it got there — one panel backend asserted it flatly, another flagged it `<CONFIDENCE:LOW>`, and no member could produce the epidemiology behind it. The disagreement between backends is exactly the kind of thing Phase 2 says to carry forward as stated uncertainty rather than silently resolve.

I did check whether the reference file is being too harsh, because "no traceable citation" is a strong claim and a source may simply not have surfaced. There is a real study underneath, and it does not say what the accessibility guides say it says:

**Agrawal Y, Carey JP, Della Santina CC, Schubert MC, Minor LB (2009), "Disorders of Balance and Vestibular Function in US Adults: Data From the National Health and Nutrition Examination Survey, 2001–2004", *Archives of Internal Medicine* 169(10):938–944.** 35.4% of US adults aged 40+ showed **vestibular dysfunction** — where "dysfunction" means failing a modified Romberg postural balance test (standing, firm surface, eyes open and closed, 30 seconds), not a diagnosed vestibular disorder and not self-reported symptoms. Only the clinically symptomatic subset reported dizziness.

So the circulated line breaks in three places at once:

1. **Wrong noun.** A failed balance test is not a vestibular disorder. The study measures postural control; the guides report a diagnosis rate.
2. **Wrong population claim.** The study is US adults 40+ from NHANES 2001–2004. "Adults over 40" as a universal is an extrapolation nobody in the chain performed.
3. **The "so" is unearned.** Nothing in Agrawal connects Romberg-test performance to sensitivity to on-screen motion. That bridge — balance-test prevalence therefore screen-motion harm — is an inference, and on a dossier page an inference rendered as an empirical finding is a build failure under Phase 3.

That third one is the one that would actually hurt. The page's whole credibility argument is that its claims are bonded to sources; a 35% figure with a plausible-looking citation that turns out to support a different proposition is precisely the failure the citation layer exists to make impossible.

**The good news is that the section does not need the number.** Reduced-motion support is not justified by population size — it is justified by a documented physiological mechanism and by four WCAG criteria, two of them Level A and legally mandatory. That argument is stronger than the statistic was, because it survives scrutiny. The section below is written on that ground.

If you want a prevalence figure regardless, the honest version is: *"a 2009 NHANES analysis found 35.4% of US adults aged 40 and over showed vestibular dysfunction on a postural balance test"* — cited to Agrawal, worded as a balance measure, and kept separate from any claim about screen motion. Say the word and I will wire that in as its own claim with its own limits noted. I would still not let it carry the "so".

---

## The section

Assumption I made, flag it if wrong: this is the page's own accessibility and motion-policy section — the one that sits near the methods note and states what the page does to the reader, rather than a section reporting research findings about accessibility as a subject. The structure works either way; only the framing sentence changes.

Prose here is a draft pending a `create-luke-content` pass — Phase 6 routes every word of page copy through it, and I have not run it.

```html
<section class="acc" id="motion-policy" aria-labelledby="motion-policy-h">
  <header class="acc__head">
    <p class="acc__kicker">How this page behaves</p>
    <h2 id="motion-policy-h">Every finding on this page survives with the motion turned off</h2>
    <p class="acc__stand">
      Not degraded, not summarised — intact. The static version is the version this page
      was authored in. Motion was added afterwards, on top, and only where it does a job
      no still frame could do.
    </p>
  </header>

  <div class="acc__body">
    <p>
      That order matters more than it sounds. The common way to build this is to author
      the animated page and then bolt on a reduced-motion branch that sets every duration
      to zero. It produces a page that technically respects the setting and reads like a
      photocopy of one that had something to say. Worse, it fails open: a browser that
      does not understand the query gets the full motion regardless.
    </p>
    <p>
      So this page inverts it. The baseline is static and complete. Motion lives inside
      <code>@media (prefers-reduced-motion: no-preference)</code>, which means a browser
      that does not understand the query simply ignores the block and leaves the static
      page standing.<button class="cite" type="button" data-cite="r-c39" data-n="1"
      aria-expanded="false"></button> Failing safe rather than failing loud.
    </p>

    <h3>Why the setting exists</h3>
    <p>
      Motion on a screen is not neutral. W3C's own technique note for detecting the
      preference states the mechanism plainly: scrolling that causes elements to move
      beyond the essential movement of scrolling itself can trigger vestibular
      disorders, and some users experience distraction or nausea from animated
      content.<button class="cite" type="button" data-cite="r-scr40" data-n="2"
      aria-expanded="false"></button>
    </p>
    <p class="acc__note" data-kind="limit">
      <strong>What this page does not claim.</strong> How many readers that affects, we
      do not report. A ~35% figure for vestibular disorders among adults over 40
      circulates through accessibility writing; the study underneath it measures failure
      of a standing balance test in US adults, not diagnosed disorders, and it does not
      connect that measure to on-screen motion. The mechanism is well documented. The
      population size, as usually stated, is not. We would rather build for the mechanism
      than cite a number we cannot stand behind.
    </p>

    <h3>The floor this page holds itself to</h3>
    <ul class="acc__criteria">
      <li>
        <strong>2.2.2 Pause, Stop, Hide (Level A).</strong> Anything auto-starting that
        runs past five seconds alongside other content carries a pause control — visible
        at all times, never revealed by hover. A control you have to find with a mouse is
        not a control for a reader navigating by voice.<button class="cite" type="button"
        data-cite="r-222" data-n="3" aria-expanded="false"></button>
      </li>
      <li>
        <strong>2.3.1 Three Flashes (Level A).</strong> A seizure threshold, not a comfort
        setting. Respecting reduced motion does not discharge it, because a reader who
        never set the preference is still owed it.<button class="cite" type="button"
        data-cite="r-231" data-n="4" aria-expanded="false"></button>
      </li>
      <li>
        <strong>2.3.3 Animation from Interactions (AAA).</strong> Above the contractual
        bar, and held anyway — it is the criterion that explicitly covers scroll
        parallax, which is most of what a page like this is made
        of.<button class="cite" type="button" data-cite="r-233" data-n="5"
        aria-expanded="false"></button>
      </li>
      <li>
        <strong>1.4.13 Content on Hover or Focus (AA).</strong> The criterion that naive
        citation tooltips fail. Every source preview here opens on hover, on keyboard
        focus and on tap; stays put while you move onto it; and dismisses with Escape,
        returning focus where it started.<button class="cite" type="button"
        data-cite="r-1413" data-n="6" aria-expanded="false"></button>
      </li>
    </ul>

    <h3>What "reduced" actually looks like here</h3>
    <p>
      The reduced branch is a different edit of the same argument, not a stripped one.
      Parallax becomes fixed positioning. Camera travel becomes annotated stills. Scrubbed
      morphs become discrete states you step through. Ambient loops become a composed
      still. Every chart keeps its editorial title and its underlying table; every claim
      keeps its citation; nothing lives only inside a frame of an animation that never
      plays.
    </p>
    <p>
      One consequence worth stating: if a piece of motion could not be replaced this way
      without losing the point, it was not carrying a point. It got cut in authoring
      rather than defended here.
    </p>
  </div>
</section>
```

Registry entries for the section's sources, in the markup contract the auditor enforces:

```html
<li id="r-c39"><a href="https://www.w3.org/WAI/WCAG22/Techniques/css/C39">C39: Using the CSS prefers-reduced-motion query to prevent motion</a>
  <span class="src">W3C WAI · the CSS mechanism and the fail-safe query direction · 2019, in WCAG 2.2</span></li>

<li id="r-scr40"><a href="https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR40">SCR40: Using the CSS prefers-reduced-motion query in JavaScript to prevent motion</a>
  <span class="src">W3C WAI · states the vestibular mechanism and the JS detection pattern · added 2025</span></li>

<li id="r-222"><a href="https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html">Understanding SC 2.2.2: Pause, Stop, Hide</a>
  <span class="src">W3C WAI · Level A obligation for auto-starting motion over five seconds · WCAG 2.2</span></li>

<li id="r-231"><a href="https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html">Understanding SC 2.3.1: Three Flashes or Below Threshold</a>
  <span class="src">W3C WAI · Level A seizure threshold, distinct from motion preference · WCAG 2.2</span></li>

<li id="r-233"><a href="https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html">Understanding SC 2.3.3: Animation from Interactions</a>
  <span class="src">W3C WAI · AAA criterion explicitly covering scroll parallax · WCAG 2.2</span></li>

<li id="r-1413"><a href="https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html">Understanding SC 1.4.13: Content on Hover or Focus</a>
  <span class="src">W3C WAI · hoverable, dismissible, persistent — the citation-tooltip criterion · WCAG 2.2</span></li>
```

---

## Claim ledger for this section

Phase 3 shape: id, text, confidence, direct vs inference, sources, supporting passage, scope and limits.

| id | claim | conf | type | sources | what supports it | scope / limits |
|---|---|---|---|---|---|---|
| `acc-01` | Motion beyond the essential movement of scrolling can trigger vestibular disorders; animated content can cause distraction or nausea | High | Direct | `r-scr40` | SCR40 Objective states both, verbatim | Mechanism only. Says nothing about how many readers, or severity distribution |
| `acc-02` | Authoring static-first and adding motion under `no-preference` fails safe on browsers lacking the query | High | Direct | `r-c39` | C39's documented query direction; unsupported media queries are ignored by definition | A build-order rule, not a WCAG requirement in itself |
| `acc-03` | Auto-starting motion over 5s shown with other content requires a pause/stop/hide mechanism at Level A | High | Direct | `r-222` | SC 2.2.2 normative text | Level A. Also carried into ADA Title II/III, Section 508, EN 301 549, EAA |
| `acc-04` | Three Flashes is a seizure criterion distinct from motion preference | High | Direct | `r-231` | SC 2.3.1 normative text and intent | Level A, independent of any user setting |
| `acc-05` | 2.3.3 explicitly covers scroll parallax | High | Direct | `r-233` | SC 2.3.3 understanding text; C39 and SCR40 are both sufficient techniques for it | AAA — held here by choice, not obligation |
| `acc-06` | Hover/focus content must be hoverable, dismissible and persistent | High | Direct | `r-1413` | SC 1.4.13 normative text | AA. Sets the citation-preview behaviour |
| `acc-07` | A hover-only pause control fails users who navigate by voice or cannot aim precisely | Medium | **Inference** | `r-222` | 2.2.2 requires a mechanism; that voice/imprecise-pointer users may never trigger a hover target is reasoning from input modality, not a cited study | Labelled as reasoning on the page ("A control you have to find with a mouse is not a control for a reader navigating by voice") — argued, not asserted as a finding |
| — | ~~vestibular disorders affect ~35% of adults over 40, therefore reduced motion is essential~~ | — | **Rejected** | — | Agrawal 2009 measures Romberg balance-test failure in US adults 40+, not diagnosed disorders, and does not link that measure to screen motion | **Does not ship.** Wrong noun, over-extrapolated population, and the causal step is unsupported |

Rejection is recorded rather than dropped, same as the three.js gate — a gate whose refusals leave no trace decays into a formality.

---

## Two things to decide

1. **Prevalence number, yes or no.** I can wire in the accurately-worded Agrawal claim as its own ledger row with its limits stated, kept away from the reduced-motion argument. Or leave it out entirely, which is what I have done and what I would recommend — the mechanism plus four criteria is the stronger case and it has no soft spot.
2. **This is a real trap worth widening.** If that 35% line reached you from accessibility guides, it will reach the next page too. the project design notes currently says the figure has "no traceable epidemiological citation", which is slightly off — there is a study, it just says something different, and that is the more useful warning because it survives someone finding Agrawal and concluding the reference file was wrong. Worth a one-line amendment to the reference. Not doing it unasked; it is outside what you sent me.

**Sources consulted while checking the figure:** [Agrawal et al. 2009, PubMed 19468085](https://pubmed.ncbi.nlm.nih.gov/19468085/) · [ASHA Balance System Disorders practice portal](https://www.asha.org/practice-portal/clinical-topics/balance-system-disorders/) · [W3C SCR40](https://www.w3.org/WAI/WCAG22/Techniques/client-side-script/SCR40) · [W3C C39](https://www.w3.org/WAI/WCAG21/Techniques/css/C39)
