# Changelog

## 0.7.0 - 2026-09-01

Adds a Gemini-calibrated `gemini.md`, so the conditional pointer already in `SKILL.md` now resolves to a real file instead of a missing one. Written by the `geminify` Mode A procedure and gated by `verify_quotes.py`.

## 0.6.1 - 2026-08-30

Every skill name written in a prompt or a cross-reference now carries its full
`plugin:skill` form. A bare name is not resolvable by the Skill tool, so a runner told to
invoke one gets `Unknown skill` and carries on without it.

Measured across 51,763 session transcripts over 21 days: 53 of 77 Skill invocations failed,
a 68% failure rate. Bare names were 27 of those. Four more came from agents that knew a
prefix was needed and invented one (`plugin:`, or the marketplace name).

## 0.6.0 - 2026-08-27

The vendoring step shipped requiring a path to a local `.js`, and the docs pointed at
`~/Dev/perch/site/vendor/gsap.min.js` and an `investorlink` `node_modules` copy. Both are
incidental to one machine, so the step was broken for anyone who installed the plugin.

### Libraries fetch themselves, once

`vendor_lib.py` now takes no path. It fetches from a pinned, checksummed URL into
`~/.cache/eli5-vendor` and reuses it; a mismatch refuses rather than inlining an unexpected
file. GSAP 3.13.0 at 72,435 B and Three.js r169 at 687,458 B came back byte-identical to the
local copies they replace.

Nothing is redistributed in this repository and nothing is fetched when the page renders. A
CDN `<script src>` inside the artifact would be quicker to write and fails *silently* in a
sandboxed runtime, which is the whole reason for section 1.10.

GSAP's licence was read rather than assumed: commercial use is free, the prohibited case is a
no-code visual animation builder competing with Webflow, and removing its notices is
forbidden. A code-generating skill is not the prohibited case, and `vendor_lib.py` refuses a
GSAP file whose `@license` header has been stripped. Three.js is MIT.

### `scripts/new_explainer.py`

A starting file with the mechanical scaffolding already wired: theme tokens, the
reduced-motion path, the four `data-*` markers, pointer capture, an animation frame that
cancels itself, and any library inlined.

    python3 scripts/new_explainer.py out.html --with gsap,scrolltrigger --title "..."
    python3 scripts/new_explainer.py out.html --with three --canvas --title "..."

It emits no sections, no layout and no copy. A page template is what produced three
indistinguishable artifacts in the first place, so this removes the typing that repeats and
nothing else. A bare scaffold fails `visual-scenes`, `interactive-controls`,
`defines-its-terms` and `title-names-its-subject`, so it cannot be shipped as written -- it is
a starting point, not a draft. Both variants load clean in Chromium with `gsap`,
`ScrollTrigger` and `THREE` present and no page errors.

## 0.5.0 - 2026-08-27

`checks-fail-quietly.html` passed every register check while opening on the title "Sabotage
it and it still says all clear" and the sentence "Something runs, looks at what came back,
and reports." Neither is baby-talk, neither is a slogan by 4.8's patterns, and neither names
anything a reader can hold.

### `names-things` and `title-names-its-subject`

The first fails four or more distinct placeholder nouns -- something, someone, stuff, the
thing, things, what came back, one of those -- and warns at two. The second fails an `<h1>`
anchored by nothing: no word of four characters or more, outside a stopword list, that the
visible text uses three times or more. A title whose subject is a bare pronoun is a riddle
the body has to decode.

Measured: 9 placeholders and an unanchored title on `checks-fail-quietly.html`, 6 and
anchored on `why-done-isnt-trusted.html`, 4 and anchored on `done-to-verified.html`, 1 and
anchored on the reference build.

### One metric measured and rejected

Vague subjects -- sentences beginning on a bare pronoun or indefinite -- do not separate the
cases: 19% on the unreadable artifact, 7% and 17% on two readable ones. The readable
reference scores as badly as the bad one, because its pronouns carry antecedents in the same
sentence. The gate does not carry that rule, and `references/evidence.md` 4.12 says why.

### The honest limit, written down

This is the third round of lexical register rules. Baby-talk, then undefined jargon, then
slogans, now placeholders -- each new artifact found a phrasing the previous round did not
cover, because a lexicon catches the shape it was fitted to. SKILL.md now carries a worked
before-and-after of both quoted lines, since a nuanced tone is steered better by an example
than by a description, and 4.12 records the gate as the backstop rather than the mechanism.

36 checks, `--self-test` at 36 of 36 able to fail.

## 0.4.0 - 2026-08-27

Four artifacts in a row drew with SVG and CSS alone -- no canvas, no library, no clip -- and
passed every check. The cause was in the wording: `vendor-inlined` skips when no library is
present, and every rule about reaching for one was phrased as a disqualifier. "Is not the
test." "Usually stays on plain SVG." "Never as a substitute for." A model reading those
correctly concluded not to.

### `surface-reach`

Fails an artifact that draws only with SVG and CSS, unless a `<!-- surface: ... -->` comment
records the choice on purpose. An explainer may still be SVG-only; it has to say so. Measured
after the change: the four SVG-only artifacts fail, the two that reach beyond pass.

### GSAP is the default way to signal

Not an alternative to CSS transitions. An unmarked state change costs g = 0.46-0.53, and one
`transition:` declaration across nine controls is signalling in name only -- the shape
measured on a real artifact. At 72 KB the orchestrated, reversible, reduced-motion-aware
version is the default rather than the upgrade.

### Three.js gains the second-lens case

Previously one test: the invariant is spatial. Now two, and the new one is the case most
often missed. Section 1.2 asks for a structurally different view when a topic has more than
one mechanism, and a field drawn flat as a heatmap and again as a 3D surface where height
carries the same quantity is exactly that -- same data, two projections, every mark still
encoding a real variable.

`why-done-isnt-trusted.html` is where this came from, and its library choice was right: a
FORM comment justifies canvas at 8,014 cells against the ~500 where DOM nodes drop frames,
and its invariant is not spatial, so three.js would have been decoration. Its real gap is
that it carries no second lens -- which is a legitimate three.js case it passed over. Forcing
a library into a page that does not want one is the coherence failure, not the fix.

What stays out is unchanged: an idle spin, a 3D chart of two variables, depth encoding
nothing. "It would look impressive" is not a reason; "the reader cannot answer this question
from the flat view" is.

### Remotion skills

The full set is installed now rather than the router alone, so the docs route to
`/remotion-create`, `/remotion-markup`, `/remotion-render` and `/remotion-docs` by name.

34 checks, `--self-test` at 34 of 34 able to fail.

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
