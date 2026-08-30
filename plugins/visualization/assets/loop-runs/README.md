# Fidelity loop — visualization

Reference: `icon-engineC-22d450-2-masked.png` (Engine C, GPT Image 2, steered with
apple-26 / apple-31 / apple-19 / apple-23 from the create-mac-icon corpus).

Metric tier: **full (lpips)** in every round — torch and lpips were installed before
r00 rather than the loop running blind at 256 and 1024, where material lives.

| round | edit class | gate | net composite | kept? |
|---|---|---|---|---|
| r00 | baseline | — | — | reference established |
| r01 | the halo well | REJECT (128/32/16) | −0.0298 | kept; r02 found the cause |
| r02 | the overhang, one constant | **ACCEPT** | +0.0194 vs r00, +0.0194 vs r01 | yes |
| r03 | the edge catch | REJECT (32px self-contrast) | +0.0111 | resolved by splitting the file |
| r04 | the emission | **ACCEPT** | +0.0150 | yes — first round to lift 256 above the r00 baseline |
| r05 | the rule's face | **ACCEPT** | +0.0147 | yes — all five sizes improved |

Each round's `brief.md` carries the measurement it was built on. r04 and r05 are the
pair to read first, because together they are one lesson: r04 lit everything the rule
*touches* (the porcelain, the bar feet) and r05 lit the rule *itself*. Neither was
visible from the composite alone — the composite had barely moved across r01-r03 —
and both were found by isolating the object and sampling its own cross-section against
the reference's. r04's brief: the emission gap the user spotted turned out to be three separate faults,
the largest of which was a draw-order bug (the contact shadow drawn over the bloom,
eating 40 chroma), the second a contaminated measurement in r01, and the third a sign
error in the graphite ramp. It also records the trade the loop could NOT dissolve —
bar vibrancy against small-size legibility, near-linear with no knee — with the three
honest options rather than a promoted round that did not improve. r03's is the other
one worth reading: the gate rejected an edit the composite liked, four amplitudes and
three widths all returned identically 0.535, and the histogram showed why.

`best-promoted/` holds the shipped master, its small-size sibling and the build
script. `last-accepted/` is the gate's rollback point.

## Panel

`r03/panel/` holds the blind pairwise panel comparing the shipped master against
the r00 baseline. The generator's own family (`claude`) is recorded and excluded
from the majority per the skill's self-preference rule, and it **flipped on two of
four dimensions when the pair was swapped** — overall and material went to the
candidate in one order and the baseline in the other, which the protocol records as
a tie rather than a win. That is the position-bias correction doing its job, and it
is why a single-order verdict is not evidence.
