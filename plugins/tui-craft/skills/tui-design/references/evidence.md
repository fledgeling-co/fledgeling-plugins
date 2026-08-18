# Evidence

What was measured, how, and the places the measurement cannot reach. Read this
when you want to justify or tune a rule, not on every run.

The short version: three measurements survived scrutiny, three did not, and none
of them is a fail threshold in the gates. The gates fail on principles instead,
for a reason set out at the end.

## Provenance

The corpus, the extraction method, the `be-my-witness` observation-pass status,
and the research panels behind both skills are all recorded once in
`../../tui-craft/references/evidence.md` — restating them here would be a second
copy to keep true. What that file does not carry, and this one does, is what each
number below may be *used for*.

The sample, in one line: 48 artifacts, 34 animated GIFs (640x376 to 2400x1600) and
14 PNG stills (796x406 to 3470x2270), one settled frame extracted per artifact plus
a mid-recording frame where a GIF had enough of them — 47 frames in total, which is
the denominator every figure below is quoted against.

**The injection note in that file is about the wrong artifact, and it is worth
being precise about which.** The corpus was 48 files chosen by the author, and
nothing in it attempted injection. A frame a reader compiles from someone else's
spec, or captures from someone else's program, carries no such guarantee — which is
why the fence sentence in `SKILL.md` exists and why this paragraph is not a
reassurance.


## The instrument, and why it was checked first

A script measured each frame's ground, its colour roles, contrast, and left-rail
concentration. Before it was pointed at the corpus it was pointed at synthetic
fixtures with known answers: a frame authored with a `#1E1E1E` ground, an exact
8x17 cell lattice, one high-contrast role and one deliberately sub-floor role.

It recovered the lattice exactly, both role shares to within 0.003, and flagged
the sub-floor role at 2.24:1. A second fixture with three real roles and two
authored anti-aliasing blends confirmed the blends were rejected and the rails
read exactly 3 with full coverage.

That step is the reason the numbers below can be quoted at all, and it is also how
two of them were found to be worthless.

## What survived

| Measure | n | Result |
|---|---|---|
| Chromatic colour roles per frame | 34 | p25 3, **median 5.5**, p75 7, max 16 |
| Content lines starting on one of 3 rails, per frame | 38 | min 0.20, p25 0.75, **median 0.86**, max 1.00 |
| Frames with at least one glyph role under 3:1 | 34 | **27** |
| Dark ground | 34 | 33 |
| Distinct large surfaces (fills) per frame | 34 | median 4 |

Denominators differ on purpose. Colour figures are over the 34 frames that were
not palette-dithered; rails are colour-independent so all 38 frames with enough
text bands count.

## What did not survive, and the mechanisms

**Colour-role identity is not recoverable from a raster.** This is the sharpest
finding in the set and it is structural rather than a limit of effort. A dim grey
chosen deliberately as a secondary text role lies on the segment between the
ground and the primary text role, which is the identical locus of an anti-aliased
edge pixel. Verified on a fixture: ground `#1E1E1E`, text `#D4D4D4`, secondary
`#555555`. Since `0x55` is the exact midpoint of `0x1E` and `0xD4`, no threshold
separates the authored role from antialiasing, and the blend filter deletes the
authored one.

So a role count from pixels is a bracket, never a number: chromatic roles mostly
survive because a saturated colour rarely sits between two others, and grey levels
do not. It also means **`glyphRolesBelow45` is a lower bound on failures, never a
certificate** — the three frames that measured clean are clean *as measured*, and
the measurement is blind to exactly the class of colour most likely to be too dim.

This is the argument for the whole pipeline. Role identity is typed in the ANSI
stream and in a cell grid, and destroyed in the pixels. Reviewing a design from a
screenshot cannot see what reviewing it from a frame can.

**13 of 47 frames carry no usable colour at all.** GIF palette reduction dithers a
smooth dark ground into alternating near-pure primaries: roles at `#242400`,
`#000055`, `#484800`, saturation 1.00, holding 30% or more of the frame's ink.
Channels land on multiples of 36 and 85. Those are the encoder's decisions, not
the designer's, and the frames are excluded from every colour figure above.

**The cell lattice is not recoverable by autocorrelation.** An early estimator
returned cells wider than they were tall (`18x8`, `4x8`), which no monospace font
produces; it was locking onto glyph stroke period and harmonics. Dropped rather
than tuned. What it was wanted for was alignment, and alignment is measured
directly from where ink runs begin.

**Chromatic ink share is not reportable.** It read a median of 0.685 even on the
undithered subset, which is implausible as a design fact, and the ink mask counts
panel fills and syntax highlighting alongside text. Not used.

## Three limits on the sample itself

- **These are hero frames.** Almost every artifact is a README recording or a
  launch screenshot, so the corpus over-represents the ideal state and
  under-represents empty, error, loading and 80x24. Nothing here is evidence about
  how these apps behave in the states that matter most for robustness.
- **48 dark grounds out of 48 is a convenience sample.** Terminal recordings are
  made on dark themes. It is a sound default and a bad law, which is why the
  advice is to query the terminal (OSC 11) and match the host rather than to paint
  a dark canvas.
- **Rail concentration was measured screen-globally**, so it conflates panes in a
  multi-pane layout and understates per-container discipline. The gate measures
  per container; the 0.86 median does not.

## The looking pass

Measurement decided which frames to open. Six were inspected at native resolution
with the long edge under the downscale ceiling, chosen to span the measured range:
the most rail-disciplined, the most colour-dense, the most colour-sparse, a
minimal one-accent design, and a spatial canvas.

That is **6 of 47 frames looked at**, with all 47 measured. Stating the
denominator matters: the compositional observations in `composition.md` come from
those six plus the earlier pattern census, and they are observations rather than
frequencies.

What they showed, in brief: panel titles interrupting the border rule with the
rule resuming after; borders drawn far dimmer than any text; focus signalled on
four channels at once with only the marker glyph surviving monochrome; semantic
colour confined to the one column carrying a category; selection overriding
category colour rather than fighting it; a two-rail label/value block with dim
labels and bright values; code blocks as a lifted fill with no border;
blockquotes as a gutter rule; an explicit `N/A` token where a value was absent;
and, inside one app, two adjacent panels disagreeing about whether the title is
centred or left-aligned.

## Why none of this is a gate

Every number above describes what 48 applications did. Turning that into a
threshold fails good screens for being unusual and passes bad ones for being
typical, and the corpus is emphatically not a contrast authority: 27 of its 34
colour-measurable frames carry at least one glyph role below 3:1.

So the gates enforce principles that can be argued from first premises about the
medium, and print the corpus figures beside the result as context:

- A role carrying information must be legible, and a ladder must not invert.
  Argued from the fact that colour and weight are the only hierarchy channels
  available.
- A state must have a carrier that survives losing colour. Argued from `NO_COLOR`,
  pipes, reader palettes, and colour vision.
- Focus needs two channels. Argued from the absence of hover, shadow and blur.

## Cross-family review

The design of this skill was put to three model families before it was built:
whether it should be a separate plugin or a second skill in one, and what the mock
format should be. Both forks were sent with the options in swapped order to
control for first-position bias.

The record, including the lanes that failed: an OpenAI lane hit a usage limit, and
the recommendations came from Google and xAI lanes plus a second Claude. All three
independently rejected drawing mocks by hand and endorsed a compiler owning the
arithmetic. The **one plugin, two skills** structure came from the Claude lane's
argument that the design phase must compute display width with the same function
the gates use and must be able to run those gates on its own output, neither of
which resolves across separately installed plugins. That was verified before
adopting: an earlier draft did carry its own copy of `char_width`, cross-checked
by a path glob that only resolved because the two plugins sat side by side in
development.

Three corrections from those lanes are in the shipped design: rails are
container-relative rather than screen-global; a role ladder replaces flat WCAG on
every glyph, because quiet secondary ink is deliberate; and no corpus median is a
fail threshold.
