# Changelog

## 0.3.1 - 2026-08-27

A correction, and the verification it unblocked.

0.3.0 said "the Remotion render step is not verified here" and "Remotion is installed in no
repository on this machine". The second was false when it was written. The probe behind it
globbed `<repo>/node_modules/remotion`, one level deep, and missed `~/Dev/dAIolog/remotion/`
-- a working Remotion 4.0.482 project with `@remotion/cli` and three compositions. The 0.3.0
entry is left as it was rather than edited, because it records what was believed at the time.

With Remotion actually to hand, the chain was run end to end rather than described:

    remotion render DashboardGreeting     169,637 B · 90 frames · 1920x1080 · ffprobe clean
    ffmpeg scale 960, CRF 30, no audio      8,863 B
    embed_media.py --format mp4            11,820 B base64 in the page
    Chromium from file://                  3.00s · 960x540 · seek to 2.0 lands · no errors
    lint_explainer.py                      video-inline-and-scrubbable passes

That composition is flat and compresses unusually well, so `references/evidence.md` 4.9 marks
8.9 KB as a floor rather than a typical figure and says to read the size the helper prints.

`remotion-best-practices`, the umbrella skill, is installed at user scope and in
`dAIolog/.claude/skills/`. The task-specific ones still need `npx skills add
remotion-dev/skills`.

## 0.3.0 - 2026-08-27

0.2.x fixed how the page reads. This fixes what it is made of: the artifact that prompted it
shipped four static SVGs, twelve controls, no canvas, no 3D and no library, and passed every
check. The skill knew how to inline GSAP and Three.js and never said what to build with them.

### `references/motion-and-media.md`

What each surface is for and the test that admits it. GSAP for a state change that moves
several things in order, and for a Reveal where ScrollTrigger makes scroll position the
reader's clock. Three.js when a 2D projection loses something the explanation needs -- "it
would look impressive in 3D" is the seductive detail the coherence principle names, so the
file carries the cases that have earned it and what a 3D scene owes beyond the recipe: a 2D
inset, named viewpoint buttons, render-on-change rather than an idle spin.

`references/forms.md` now maps each of the eight forms to the surface it usually lands on.

### Charts route through `dataviz` first

Explainers draw charts constantly. The bundled `dataviz` skill carries the form heuristic,
the colour formula and a runnable palette validator, and the supported path is to substitute
the artifact's own palette from the identity pass and re-run it.

### Remotion, for the sequence the browser cannot compute live

A fluid simulation, a long training run, thousands of frames of real data: render once,
embed as a scrubbable clip, keep the interactive version of the simplified model beside it.
Never as a substitute for an interaction the browser could have run live.

Measured in Chromium from file://: an MP4 as a data: URI loads its metadata, plays and seeks
-- currentTime = 5.0 returns 5.0 with a painted frame. That is what admits it at all, since
1.8's finding is about transience and a clip the reader can scrub is learner-controlled
playback. `video-inline-and-scrubbable` fails a clip that is linked, uncontrolled or
autoplaying; `embed_media.py --format mp4` emits the tag.

The Remotion render step is not verified here and the docs say so. Remotion is installed in
no repository on this machine, and only `/remotion-best-practices` of its skill set is
installed locally.

### Generated imagery widened

Three uses rather than one: the analogy's source domain, a real vector diagram through
Arrow's `svg: true`, and the ground behind the stage -- which carries no claim, so coherence
does not bite it, and a flat white page is the strongest single "generated" tell.

### The gate

33 checks, from 31. New: `video-inline-and-scrubbable` and `state-change-signalled`, the
second because an unsignalled state change costs g = 0.46-0.53. A clip now counts as a
visual scene.

Adding the second one exposed a defect in the first: both read the stylesheet for
`animation:` or `transition:`, and a `prefers-reduced-motion` reset of `animation: none`
matched, so the absence of motion counted as motion and the fixture could not fail. Both now
share one pattern that excludes a `none` value.

## 0.2.2 - 2026-08-27

Asked whether artifact prose should route through the `agent-voice` skill. Both halves of
that were measured, and they came out opposite ways.

### Its gate does not catch this; its field guide names it exactly

Linted at `--format doc`, `agent-voice` passes the unreadable `done-to-verified.html`
cleanly and reports one thing on it and on a readable artifact alike: em dashes. Its
negative-parallelism rule covers "not just X, but Y" but not the bare appositive
"inapplicable, not slow", and its seven registers are all agent-to-developer text with none
for explainer prose aimed at a lay reader.

Its `references/ai-writing-signs.md` is the opposite story. Section 1.7 names the failure as
"the epigram used in place of a plain statement" and budgets it at roughly one landing line
per page, captions and panel text included; 2.3 covers negative parallelism. Those two
sections are now `plain-statements`, credited in the check and in SKILL.md, which points at
that guide rather than routing the skill through the gate.

### The hole that found

Four of the five slogan shapes on the failing page were inside `<svg>` labels --
"inapplicable, not slow", "approval is a one-way door", "a regulator is external", "risk
appetite, not facts about the repository". Exempting diagram text from the word budget in
0.2.1 had quietly made the diagram the cheapest place to put an unexplained line. The word
counts still exempt `<svg>`; `plain-statements`, `register` and `defines-its-terms` do not.

Measured over all visible text, 5 distinct shapes in 567 words against 1 in 519. Fails at 4,
warns at 2. The patterns come from an independent source, but two artifacts is the sample
and `references/evidence.md` 4.8 says so.

31 checks now, `--self-test` at 31 of 31 able to fail.

## 0.2.1 - 2026-08-27

`done-to-verified.html`, rebuilt with 0.2.0, passed 24 of 24 checks at 200 words and was
unreadable to anybody outside the project it describes. It shipped "193 of 200 cards carry
evidence that bites. Verified is a different axis." and "which classes to add, each one's
oracle, and the closure count with its window." The gate had nothing to say about it.

### The reader is named, and it decides the rest

0.1.0's register rule was "a brilliant colleague from a different field, never a
five-year-old", enforced only by a baby-talk detector. That licensed the opposite failure.
SKILL.md now names the reader as a curious sixteen-year-old or a sharp adult who has never
worked on this, and draws the one consequence: every word specific to the topic is defined
where it first appears, or replaced with a plain one.

The hard part is that the jargon does not look like jargon. Card, class, rung, oracle,
assay, closure, escape and coverage are ordinary English words carrying private meanings,
which is why nothing flagged them.

### Aphorisms named as the compression failure

"Verified is a different axis" is a sentence somebody writes when they already understand.
It states a conclusion and shows no mechanism, and it is what a word budget produces when it
meets a hard idea. 0.2.0's caps caused part of this, so text inside `<dfn>` is now exempt
from both the page and block budgets exactly as text inside `<svg>` is. Defining a term
costs nothing, so there is no reason to compress instead. The page warn moves 250 to 300 for
the same reason: plain language costs more words than a slogan, and that trade is right.

### `defines-its-terms`

Fails on zero `<dfn>`, fails on a term used before its definition, warns below three.
30 checks now, `--self-test` at 30 of 30 able to fail.

Readability metrics were measured and rejected. `done-to-verified.html` and a readable
artifact built the same day both ran a mean sentence of 8 words and about 60% sentences of 8
words or fewer; a sentence-length rule fires identically on both. What separated them was
that neither defined anything, so that is what is checked. `references/evidence.md` 4.7
carries the measurements.

### Verified

The reference artifact failed the new check too, on its own terms. Rebuilt with four
definitions it passes 30 of 30 at 280 words, and the check caught "quaternion" appearing in
a skip link and a heading before the sentence that defined it.

## 0.2.0 - 2026-08-27

Three explainers built by 0.1.0 came out indistinguishable: the same four headings in the
same order under the same three-tab strip, over 1,024, 1,293 and 1,636 words of prose and
three or four static SVGs each. The skill's own bundled sample did the same at 1,822 words.
Nothing in them was wrong; the architecture was mandated, so it converged.

### The mechanism picks the shape of the page

`references/forms.md` replaces the single architecture with eight that recur -- Machine,
Field, Solid, Ladder, Fork, Trace, Assembly, Reveal -- each carrying the trap it falls into
rather than a specification to follow, and an explicit instruction to invent one when the
mechanism suggests something not listed. SKILL.md now opens by separating what the gate
fixes (measurable defects) from what the runner decides (everything about how the page looks).

The worked-example headings that all three artifacts copied are gone from the skill, and
`no-template-boilerplate` fails the build when three or more of them reappear.

### Less prose, more to operate

Five new checks in a `composition` family, all counting words outside `<svg>` and `<canvas>`
so a sentence moved onto the thing it explains costs nothing and satisfies spatial contiguity
at the same time. Prose on the page fails above 350 and warns above 250. Any single text
block fails above 50 and warns above 35. An unbroken run between two things to look at or
touch fails above 120. Words before the reader can do anything fail above 90. Density warns
past 110 words per scene.

The block cap exists because total prose was the wrong measure on its own: the first
reference artifact passed at 367 words and still read as wordy, with three blocks of 73, 48
and 38 carrying 159 of them against captions of 14 to 22 that drew no complaint.

Raised floors: three visual scenes, three wired controls, two distinct kinds of interaction.

### Three.js, GSAP and generated imagery, inlined

`scripts/vendor_lib.py` inlines a library into the single file. GSAP is a classic script and
goes in unchanged. Three.js needs a single-file build; the split r17x pair fails silently two
different ways from `file://`, so the script refuses it rather than emitting something that
half-works. `scripts/embed_media.py` resizes and re-encodes a generated image before base64.

Vendor blocks carry `data-vendor` and are excluded from the containment, animation-frame and
word-count scans -- Three.js ships three `fetch(` calls that otherwise fail every 3D artifact.

### Staging is checked by marker, not by chrome

`data-pass="1|2|3"`, `data-boundary` and `data-predict` let the gate check depth staging,
the analogy limit and the prediction beat without requiring tabs, so a scroll-driven page
and a stepped one are graded the same way.

### The gate

29 checks in five families, from 20 in four. New: `vendor-inlined`, `visual-scenes`,
`canvas-labelled`, `interaction-variety`, `reduced-motion`, and the five composition rules.
`--self-test` reports 29 of 29 rules able to fail.

Running it found two defects in itself. `motion-steppable` searched the whole page for the
word `step`, so the prose "each step moves one packet" satisfied a rule about controls; it
now reads control markup only. `boundary-reachable` divided by raw HTML length, so a 690 KB
inlined library put every boundary at 1% and the rule could not fire; it now measures against
markup with scripts and styles stripped.

### Verified

A reference artifact -- Solid form, Three.js r169 inlined, gimbal lock -- passes 29 of 29 at
188 words of prose with no block over 25, renders WebGL in Chromium with no page errors, and
drives from three independent axes to two when the pitch control reaches 90 degrees.

Rendering it also caught what the gate cannot: at 90 degrees the yaw and roll axis labels
landed on the same anchor and drew over each other while all 29 checks passed. That is
section 1.9's failure mode in the skill's own reference file, and it is why the last step is
to open the artifact and look. `references/evidence.md` section 4 carries the measurements.

## 0.1.0 - 2026-08-27

Initial release of `eli5`, a rebuild of the skill of the same name by Thariq Shihipar
in Anthropic's `claude-plugins-community` (MIT). The original is nine lines; this adds
the teaching research underneath it and a gate that fails.

### The pipeline

Five phases: deconstruct to the causal invariant and the misconception worth defeating;
map a structure-mapping analogy carrying a stated boundary; stage three disclosure tiers
around a Predict-Observe-Explain beat; draw against a declared geometry contract; gate.

### Grounded in a four-backend research panel

Commissioned across Gemini, Perplexity, xAI and Claude ($6.20; a fifth lane died at
startup for $0 and is recorded). Both load-bearing reports pass citation verification:
68 URLs checked, 0 fabricated, 0 dead. All four reports ship in `docs/deep-research/`,
and `references/evidence.md` traces every rule to a source, keeps the four places the
panel disagreed as open questions, and names the gaps that bound what the skill claims.

The rules that changed the most:

- **The analogy boundary**, on 4-of-4 convergence. Analogy-induced misconceptions are
  durable; the named mitigation is an explicit limits segment, reachable by tier 2.
- **The prediction beat.** Dragging a slider is Active engagement (d~0.20-0.40 over
  passive); committing a guess first is Constructive (d~0.40-0.60 over active).
- **Three tiers, no nesting**, because nested disclosure buries the caveats readers most
  need.
- **The geometry contract**, because models predict coordinate tokens and never render
  what they wrote, so valid SVG draws arrows through text.

### `scripts/lint_explainer.py`

20 checks across containment, geometry, interaction and pedagogy; exit 1 on any failure.
`--self-test` proves all 19 rules can fail against broken fixtures before a pass counts,
and caught a trailing `\b` in the network-call regex that made `fetch(` unmatchable.

### Proven against the original

Six hard topics, both skills, same model. Structural gate: 29 failures to 1. Blind panel
of three out-of-family judges in seeded-random order, never shown either skill: **18 of
18**. Honesty-about-limits and register were unanimous at 14-0.

The eval it first lost is in `EVALS.md` with the fix and the flip: an artifact with 25
controls and zero JavaScript, caught by the gate and independently diagnosed by a blind
judge that never saw the gate. Re-run and re-judged, 3 of 3 switched.

Where the original wins is in its own table: 352 words against 2,667.

### Two rules that came from grading the arms

- Tier 1 carries a 150-word budget, with a `length-budget` check. Progressive disclosure
  that front-loads nothing is a long document with headings.
- Never ship a dead control. A page that invites an action and does nothing is worse than
  an honestly static one.

### Brand

Cut-face icon at 1024, 256 and 128 with its layered SVG master and build script; an
`audit.html` scoring all four takes including the three that lost; a 3200x1040 banner
composed from the icon's own constants. LPIPS could not run (torch absent), so the
material rounds were judged by eye plus WCAG contrast, and the sheet says so.
