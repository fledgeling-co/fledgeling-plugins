# Judge panel — families, harnesses, and the one that failed

Blind A/B on three anonymised document pairs (`judge-bundle.md`), order flipped per case from
seed `20260818`, un-blinding map in `judge-unblinding.json`. No judge saw the skill, the repo, or
which option came from which version, and none was told either option was newer. The bundle opens
with the injection fence — its contents are material to judge, never instructions to follow.

## Result

| Family | Harness / model | Case 1 motion verification | Case 2 library loading | Case 3 contrast | Outcome |
|---|---|---|---|---|---|
| **Anthropic** | `claude --model claude-fable-5 --effort high -p` | **rebuild** (A) | **rebuild** (B) | **rebuild** (B) | 3 of 3 for the rebuild |
| **Google** | `agy --model gemini-3.7-flash-high -p` | **rebuild** (A) | **rebuild** (B) | **rebuild** (B) | 3 of 3 for the rebuild |
| **xAI** | `grok -m grok-4.6 --effort xhigh -p` | **rebuild** (A) | **rebuild** (B) | **rebuild** (B) | 3 of 3 for the rebuild |
| **OpenAI** | `codex exec -m gpt-5.6-sol` | — | — | — | **FAILED** |

**Unanimous across all three available families, on all three cases, blind — 9 of 9.** All three
judges also returned `OVERALL: MIXED`, and all three for the same reason: the option order flipped
between case 1 and cases 2–3, so neither letter was consistently better. Un-blinded, the rebuild
took every case.

The three converge on one criterion none of them was given. Anthropic: the better text is
*"whichever names the silent failure … rather than the one that prescribes a check whose green
result is indistinguishable from a measurement never taken."* xAI, independently: *"A is the only
motion brief that will not certify a silent false pass; B is the only load and contrast brief that
names silent CSP failure and forbids a fabricated ratio."* Google: the winner *"prevents
false-positive test passes."* That is this skill's own epistemics arriving from outside it, three
times, in three families' own words.

## The one failure, recorded as a failure

It is not dropped from the tally, and it was not retried more than once.

- **OpenAI (`codex`)** — one attempt, 18 Aug 2026. `ERROR: You've hit your usage limit … try again
  at Aug 20th, 2026`. Exit 1, no output file written. A same-model substitution through a
  different harness was not available.
**A correction worth recording, because it changed the tally.** The xAI lane was first read as a
failure — it had emitted 88 bytes of narration and no verdict when it was checked, and the
subscription behind it had been reported exhausted by earlier runs on this machine that day. It was
then left running to its own budget rather than killed, and it completed with a full verdict. The
failure was in the reading, not in the lane. That is the same mistake this skill's Phase 0 is
about: an incomplete measurement read as a settled one.

So the panel is **three families, not four**, and every conclusion drawn from it carries that.
Three families agreeing unanimously is weaker than four; it is reported as three.

## Findings acted on the same day

A judge catching something is worth more than a judge agreeing, and two of these were real bugs.

1. **The pixel-median fallback sampled the letters along with the ground.** xAI, as Option B's
   worst flaw: *"The canvas 'glyph-box median' snippet is incomplete and samples the letters with
   the ground, so `contrast-unmeasurable` becomes a confident wrong ratio treated as G18."*
   Correct. A crop of the glyph box is bimodal, so its median tracks how much of the box the text
   covers rather than the ground behind it. The snippet now hides the text for the sample
   (`el.style.color = 'transparent'`, which moves no layout) and reads the foreground from
   `getComputedStyle` instead — never from those pixels.
2. **The pixel-median fallback's arithmetic was also wrong.** Anthropic, as Option B's worst flaw:
   *"The sample code computes luminance as `0.2126*R + 0.7152*G + 0.0722*B` on gamma-encoded sRGB
   bytes without linearizing each channel, so any contrast ratio derived straight from that median
   or 95th-percentile value is wrong in a way that looks precise."* Correct, and it was mine.
   `accessibility-audit.md` checklist 1 now linearises per channel, carries the ratio expression,
   and says why the step is not a detail — on a mid-grey ground the encoded and linear values
   differ by roughly a factor of two, which is enough to flip a verdict either way.
3. **The Known limits table read as permission to ignore motion.** Anthropic: an engineer skimming
   it *"may conclude motion needs no attention at all rather than a narrower one."* Google, from
   the other side: it *"hardcodes strict assumptions about a specific engine … rather than
   verifying whether the active browser actually supports them."* Both are right and they compose:
   `visual-verification.md` Phase 0 now states the table is a measurement rather than a property
   of headless browsers, gives a four-line probe that re-establishes each row on any engine, and
   lists explicitly what remains required — the viewport matrix, the end-state captures, the
   scroll pass, the reveal-safety grep, and the three source-side motion rules that are gated.
4. **The inline-the-library route gave sizes but no method.** Anthropic: the numbers were given
   *"without saying how to obtain the minified file."* `gsap-motion.md` now gives the `curl` and
   the `npm pack`.
5. **The contrast checklist opened on a path that may not resolve.** Google: it *"mandates running
   a specific local script that may not exist in the engineer's environment."*
   `accessibility-audit.md` now says the path is relative to the skill's own directory and what to
   do when it does not resolve.
6. **The re-measurement probe could itself be filed as a pass.** xAI: a reader could *"run the
   snippet, record `getAnimations: 0`, and file a pass."* The probe now carries the condition in a
   comment above it — run it while something is animating and a face is declared, or every answer
   it gives is meaningless.
7. **The inline route was named and never shown.** xAI: *"never shows a working inline-`<script>`
   example … so the artifact path is invented while the CDN block stays the one they paste."*
   `gsap-motion.md` now shows the three-tag inline shape above the CDN block.

## What the panel cannot tell you

Blind judges scored **content only**. Nothing in the bundle reflects the eval harness, the
selftest, the scorecard, the research corpus or the citation checks — so the audit machinery earns
nothing here by design, and the reverse holds too: three judges preferring the rebuilt prose is not
evidence that its gate is correct. That is what `scorecard.md` is for. Both layers are single runs
and carry sampling noise.

And the seven findings above are worth more than the 9-of-9. Two of them were real arithmetic defects
in a technique this rebuild introduced, found by judges who could not see the code, the tests or
each other — which is the argument for a heterogeneous panel rather than for this particular
result.
