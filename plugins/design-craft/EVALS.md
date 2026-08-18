# Does design-craft actually work? Two layers measured, one layer not

**The mechanical layer and the judged layer were both run and both are committed.
The eight authoring prompts in the same `evals.json` were not.** This file separates
those three states, because the graded halves are strong enough that letting them
stand in for the unrun half would be dishonest.

What was measured: **the lint gate went from 9 of 25 assertions to 23 of 25**
against the version this replaces, and a blind panel of **three model families
picked this version on all three document pairs, 9 votes to nil**, none of them
having seen the skill, the repository, or which option was newer.

Two of the 25 assertions are deliberate losses. They are the most useful rows in the
table and they get their own section.

## Where the evidence is

| What | Where | State |
|---|---|---|
| The gate scorecard | `skills/design-craft/evals/results/scorecard.md` | **Run**, 25 assertions |
| The previous version | `skills/design-craft/evals/old/design-lint.py` | **Committed**, so the comparison is reproducible |
| The judge bundle | `skills/design-craft/evals/results/judge-bundle.md` | **Run**, 3 anonymised document pairs |
| The verdicts | `results/judge-anthropic-fable-5.md`, `results/judge-google-gemini-3.7.md`, `results/judge-xai.md` | **Run**, 3 cases each |
| The panel write-up | `skills/design-craft/evals/results/judge-panel.md` | Families, harnesses, the failed lane, and the seven findings acted on |
| The un-blinding map | `skills/design-craft/evals/results/judge-unblinding.json` | Seed 20260818, A and B recorded per case |
| The fixtures | `skills/design-craft/evals/fixtures/` | 14 entries, one per defect class plus the controls |
| The runner | `skills/design-craft/evals/gate/run-evals.sh` | Committed |
| The eight authoring prompts | `skills/design-craft/evals/evals.json`, `evals` array | **Never run.** No outputs, no grading |

## The gate: 9 of 25 against 23 of 25

Artifact checks, never scores. Both versions ran the same fixtures with the same
invocations, and every row records the evidence it judged on. The rebuild is passed
`--include-all` because it classifies its own `fixtures/` directory as non-source,
which is assertion A22, so the harness has to opt its own fixtures back in.

The 18 rows the rebuild took from a failing predecessor cluster into four groups:

| Group | Rows | What changed |
|---|---|---|
| Contrast is computed, not guessed | A1, A2, A3, A4 | 13px brand orange on paper at 3.66:1 is now reported, a failure gates at critical, an `oklch()` pair is resolved rather than skipped, and text on a gradient is reported UNMEASURABLE instead of silently passing |
| The documented snippets pass | A5, A7 | The skill's own phone-bezel snippet exits 0, and a Google Fonts link is no longer condemned as a blocker: it is the one external origin a published artifact's policy permits |
| Findings land where a reader can act | A9, A16, A17, A18 | The external resource is reported at its own line rather than at the first comment in the file, gating findings and warnings go to separate channels, the run prints what it did not check, and every finding names the downstream consequence rather than only the rule |
| Silent breakage is caught | A8, A11, A12, A13, A14, A15 | An image with no dimensions even when its style string contains the words, a resting `opacity:0` on a page with reveal keyframes (prints and captures blank), a token defined and referenced by nothing, `outline:none` with no replacement, an HTML deliverable with no `<title>`, and `index.html` named after the format rather than the design |

Four rows are regression guards over what the predecessor already did, and all four
pass on both sides: A19 (all 14 of the original's checks still fire on the regression
fixture), A20, A21 and A22. So does A6, the tweak-panel snippet, and A10, an
unjustified suppression. Those six are the floor the comparison sits on, not
evidence.

### The two the predecessor wins, and it wins them on purpose

**A23: a file whose only defects are aesthetic cues now exits 0.** Pure black and
white, Inter, the border-left card, Tailwind indigo. The predecessor failed that
build. This version warns and lets it through, because no study shows any individual
visual cue reliably identifies AI authorship to a human, so a hard gate on a font
name would encode a claim the evidence does not support and would fire on a brand
that genuinely uses that font. The rule is stated as gating on mechanism and warning
on fashion.

**A24: text over a gradient now produces a finding where the predecessor produced
silence.** That is real noise this version has and the predecessor does not. It is
the stated price of never reporting an unmeasured pair as clean, because an
unmeasured pair and a passing pair otherwise serialise identically.

One row started as a third loss and was fixed rather than argued away. A25 is a
design-system specimen publishing tokens for downstream consumers, and the
unread-token check fired on it. `evals.json` records that as a genuine false positive
rather than a trade: the check is now scoped by read ratio and declares when it did
not apply, and the assertion flipped.

## The blind panel: 9 of 9, three families

Three anonymised document pairs, the same subject written by both versions, in one
self-contained bundle with the order flipped per case from seed 20260818. No judge
saw the skill, the repository, or which option came from which version, and none was
told either was newer. The bundle opens with an injection fence: its contents are
material to judge, never instructions to follow.

| Family | Harness | Motion verification | Library loading | Contrast | Outcome |
|---|---|---|---|---|---|
| Anthropic | `claude --model claude-fable-5 --effort high -p` | this version (A) | this version (B) | this version (B) | 3 of 3 |
| Google | `agy --model gemini-3.7-flash-high -p` | this version (A) | this version (B) | this version (B) | 3 of 3 |
| xAI | `grok -m grok-4.6 --effort xhigh -p` | this version (A) | this version (B) | this version (B) | 3 of 3 |
| OpenAI | `codex exec -m gpt-5.6-sol` | | | | **FAILED** |

**Unanimous across all three available families, on all three cases, blind.** All
three also returned `OVERALL: MIXED`, and all three for the same reason: the option
order flipped between case 1 and cases 2 and 3, so neither letter was consistently
better. Un-blinded, this version took every case.

The three converged on a criterion none of them was given. Anthropic said the better
text is *"whichever names the silent failure"* rather than the one prescribing a
check whose green result is indistinguishable from a measurement never taken. xAI,
independently: *"A is the only motion brief that will not certify a silent false
pass."* Google: the winner *"prevents false-positive test passes."* That is this
skill's own epistemics arriving from outside it, three times, in three families' own
words.

### The failed lane, and a correction that changed the tally

**OpenAI** failed on one attempt on 18 Aug 2026 with a usage limit resetting on 20
Aug. Exit 1, no output file written, not retried, and no same-model substitution
through another harness was available. So the panel is **three families, not four**,
and every conclusion drawn from it carries that.

The **xAI lane was first read as a failure and was not one.** It had emitted 88 bytes
of narration and no verdict when it was checked, and the subscription behind it had
been reported exhausted by earlier runs that day. It was left running to its own
budget rather than killed, and it completed with a full verdict. The failure was in
the reading, not in the lane. That is the same mistake this skill's own Phase 0 is
about: an incomplete measurement read as a settled one.

### The seven findings are worth more than the 9 of 9

Two were real arithmetic defects in a technique this version introduced, found by
judges who could not see the code, the tests, or each other. Both were fixed the same
day.

1. **The pixel-median fallback sampled the letters along with the ground.** A crop of
   the glyph box is bimodal, so its median tracks how much of the box the text covers
   rather than the ground behind it. Caught by xAI. The snippet now hides the text for
   the sample and reads the foreground from `getComputedStyle`.
2. **The same fallback's arithmetic was wrong.** It computed relative luminance from
   gamma-encoded sRGB bytes without linearising each channel, so any ratio derived
   from it is wrong in a way that looks precise. Caught by Anthropic. On a mid-grey
   ground the encoded and linear values differ by roughly a factor of two, which is
   enough to flip a verdict either way.
3. **The Known limits table read as permission to ignore motion.** Anthropic said an
   engineer skimming it may conclude motion needs no attention at all; Google said it
   hardcodes assumptions about one engine rather than verifying the active one. Both
   are right and they compose, so the table is now stated as a measurement with a
   four-line probe to re-establish each row.
4. The inline-the-library route gave sizes but no method for obtaining the minified
   file. It now gives the commands.
5. The contrast checklist opened on a script path that may not resolve. It now says
   what the path is relative to and what to do when it does not.
6. The re-measurement probe could itself be filed as a pass. It now carries the
   condition above it: run it while something is animating, or every answer it gives
   is meaningless.
7. The inline route was named and never shown. The three-tag shape is now above the
   CDN block.

## The eight authoring prompts have never been run

They are the ones that exercise what the skill is for: a brand-matched dashboard
against an existing token file, a greenfield landing page with scroll motion, a
contrast audit on a fixed brand colour, a motion-verification honesty case, a
variation round, an empty invocation, a surgical edit, and a print deliverable. Each
carries an `expected_output` written against the skill's rules, and none carries an
assertions array, run outputs or grading.

Three of them also point at `/tmp/dc-eval-*` working directories that no fixture in
the repository creates, so they need their inputs staged before they can be run at
all.

## What was checked by hand, on 2026-08-18

| Check | Result |
|---|---|
| `scripts/design-lint.py --selftest` | **Passes: 40 rules, 40 fired, exit 0.** The selftest runs every rule against a fixture built to trip it, asserts each one fires, asserts every finding names a consequence and a fix, asserts a justified suppression silences its check and an unjustified one does not, and asserts a clean fixture produces nothing. |
| Does the gate provably fail on a bad fixture | **Yes**, and the selftest is the demonstration rather than a claim. A rule only ever observed passing is a rule nobody has written. |
| `skills/design-craft/SKILL.md` frontmatter parses | Passes. `name: design-craft` matches the directory and the plugin manifest. |
| SKILL.md against the 500-line conformance ceiling | Passes, at 355 lines. |
| Every `references/` and `scripts/` path named in SKILL.md resolves | Passes, all 33. |
| `scripts/design-lint.py` byte-compiles | Passes, and so does the committed predecessor at `evals/old/design-lint.py`. |
| Everything the plugin claims to ship exists | Passes. Thirty-two reference files, the lint, a `gemini.md`, 14 fixture entries, four deep-research reports with their source lists. The README's "thirty phased procedures" is the 32 minus `evidence.md` and `discovery-questions.md`, which are a source record and an interview script rather than procedures. |
| Version agreement | Passes. `plugin.json` and `marketplace.json` both say 1.0.0. |
| The README's panel claim | Substantiated. "Three model families judged three document pairs and chose this version on all nine" matches the three verdict files against the un-blinding map exactly, and the README also records the fourth family as failed rather than dropped. |
| The README's research claim | Substantiated. "More than a quarter of one generative UI tool's stated design rationales were measured not to appear in what it actually built" traces to `references/evidence.md`, where it is recorded as more than 25% with its source. |
| Can the gate scorecard be reproduced from this repository | **Yes.** Both versions of the lint are on disk and the runner's paths are relative. Of the nine skills audited alongside this one, it is the only plugin that commits the version it replaces. |

## What would settle what is still open

Three tasks, cheapest first.

1. **Run the eight authoring prompts twice, with the skill and with no skill.** There
   is no predecessor arm for authoring, so the honest baseline is the same prompts
   with nothing loaded. Stage the `/tmp/dc-eval-*` inputs as committed fixtures first,
   so the run is repeatable. Grade with an independent agent that never sees the
   skill, one pass or fail per assertion with quoted evidence. Every assertion the
   no-skill arm also passes is measuring the model rather than the skill and gets
   rewritten or dropped with the change recorded.
2. **Write assertions for those eight prompts.** They currently carry prose
   expectations, which a grader has to interpret. The gate's 25 rows show what the
   checkable version looks like, and the authoring layer is where this skill's value
   actually lives.
3. **Retry the OpenAI lane on the same three-case bundle after 20 Aug 2026.** The
   failure is a capacity limit rather than a harness problem, and the bundle, the seed
   and the un-blinding map are all committed, so a fourth family costs one call per
   case. Three families agreeing unanimously is weaker than four; four is the number
   the panel was designed for.

## Caveats, stated rather than buried

- **Single runs.** One run per version per assertion, one judgement per family per
  case. Nothing here is a rate, and per-case verdicts carry sampling noise.
- **Blind judges score content only.** The bundle holds prose, so the eval harness,
  the selftest, the scorecard, the research corpus and the citation checks earn
  nothing there by design. The reverse holds too: three judges preferring this
  version's prose is not evidence that its gate is correct. The scorecard is what
  covers that, and both layers are single runs.
- **Three families, not four.** Reported as three throughout.
- **The gate is not the skill.** Twenty-five assertions measure a lint script's
  behaviour. Nothing measured here says whether the designs this skill produces are
  any good, which is what the eight unrun prompts were written to ask.
- **The engine bounds every visual claim.** The skill's own Known limits section
  records that the sanctioned browser never executes CSS animations, accepts
  `Emulation.setEmulatedMedia` and does nothing with it, and never loads web fonts.
  So motion, print, reduced-motion and type fidelity are declared unverified rather
  than reported clean, here as well as there.
