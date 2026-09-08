# Stage 9: the report

Two artifacts. A branded HTML page for the product owner, and the status page for the
portfolio.

## The page

Written through `create-luke-content:create-luke-content`, laid out with `design-craft` and
`ux-craft`, figures through `visualization:visualization`.

- **Figures over sentences.** The owner asked for this in those words. A count, a split, a
  before and after belong in a figure; the prose says what it means.
- **One column at one measure.** A page that starts at two thirds width and drops to half
  reads as broken. Set the wrapper to the measure plus its padding.
- **The reader does not read code.** No file paths, no identifiers, no gate names. "A check
  that could not fail" rather than "a vacuous assertion".
- **Final state, not a story.** No "I first tried X". The outcome and how it was reached.
- **Every claim is checkable.** Where a number moved, say from what. Where something is
  unproven, say so rather than rounding it up.

Gates, all three: `voice_lint.py` (an em dash is a hard fail), `design-lint.py` (0 critical),
and the visualization `self_check.py`. That last one hard-fails a document with no SVG; a
page whose figures are all CSS can refuse it deliberately, and that refusal belongs in the
report rather than being satisfied by adding an SVG nothing needs.

Open it when it is done: `open -a "Google Chrome" <path>`.

## What the owner actually wants to read

From one revision cycle, in their words: fewer words, more figures, no negative framing of
their work ("wrong" became "worth a decision"), and no em dashes because the voice skill
governs every written word.

Lead each claim with its outcome. A checklist of the claims the work makes, each marked
plainly, is the thing they read first.

## The status page

`status-update:status-update` writes `.status/project.json` and renders `STATUS.html` plus
the portfolio dashboard. Two lines back in chat: how it went and where the page is, then
anything that needs the owner. Both files are committed with the work they describe.

## Say what you could not measure

The most valuable line in a report is usually the one admitting a gap. A verdict measured
against the wrong code, a check nobody has watched fail, a flow that has never run: each is
worth more written down than smoothed over, because the alternative is a reader trusting a
number that cannot carry it.
