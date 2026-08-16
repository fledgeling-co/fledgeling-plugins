# tui-craft

Design, build and review terminal interfaces against what the terminal actually
drew, not against the code that meant to draw it.

The gap between those two is where terminal bugs live. `len("🚀 Deploy")` is 8 in
Python and 9 cells on screen, and that one cell tears the panel border on every
row below it. You cannot see that by reading the source; you can only see it by
looking at the grid.

So this skill starts with an instrument.

## What it does

**Captures the running app.** `tui_capture.py` drives your TUI under a pty at a
fixed size, replays its byte stream through a terminal model, and emits a typed
cell grid with provenance attached: the command, the size, `TERM`, which parser
ran, and a hash of the raw bytes.

```bash
python3 scripts/tui_capture.py --cmd "./myapp" --cols 100 --rows 30 \
  --settle 1.2 --keys "j,j,Enter,/,f,o,o" --dump -o frame.json
```

**Runs the arithmetic.** `tui_gates.py` reads that frame and checks the things
nobody eyeballs correctly:

| Gate | What it catches |
|---|---|
| `border-integrity` | A box that opens and never closes on the same column |
| `width-arithmetic` | A row shoved past its neighbours by a double-width glyph |
| `overflow-wrap` | Content that ran off the edge and continued mid-word |
| `truncation-marker` | Text cut with no ellipsis to say it was cut |
| `shelf-containment` | An inset border label that crowded out its own rule |
| `glyph-risk` | Replacement characters, and Nerd Font glyphs that need a font your reader may not have |
| `colour-inventory` | The colour count, and a frame with no bold and no dim anywhere |

Every finding comes back with a row and a column, so you can go and look at it.

**Then you look.** The capture prints a character matrix with column rulers, and
that's the artifact to read. Misalignment that's invisible in a screenshot is
obvious against a ruler:

```
     000000000011111111112222222222333333333344444444445555555555
     012345678901234567890123456789012345678901234567890123456789
     ------------------------------------------------------------
  0 |┌ Pipelines ───────────────────────────────────────────────┐
  1 |│ deploy   prod-east-1                Active               │
  2 |│ build    日本語ビルド                     Running
  3 |│ test     staging-eu-west-2-canary   Failed               │
  4 |└──────────────────────────────────────────────────────────┘
```

Row 2 is missing its right border. The CJK string measured 6 characters and
drew 12 cells.

## The rule

A claim about a screen needs a captured frame. Not the source, not a description,
not a mock in a fenced code block.

If capture fails, that's the result you get: `capture blocked`, with what was
tried. It's never a reason to fall back on reading the code and saying it looks
about right. That failure mode is the reason this exists; its predecessor carried
4,900 lines of sound design advice and no way to see a single frame of output.

Hand-drawn frames are still useful for proposing a layout. They're labelled
`mock`, and they can't support a finding.

## Two producers, one schema

If you own the source, your framework already knows how to render itself for
testing. `frame_from_ansi.py` turns that output into the same frame, so
`teatest`, Ratatui's `TestBackend`, Textual's `run_test` and
`ink-testing-library` all feed the same gates.

```bash
python3 scripts/frame_from_ansi.py frame.ansi --cols 100 --rows 30 -o frame.json
```

Snapshot tests skip the host negotiation though (real colour depth, real font,
the terminal's own width handling), so run one pty capture before you ship.

## What it knows

**A pattern catalogue** built from 48 shipped TUIs, analysed frame by frame.
Every pattern names the app it came from, so you can check it. The border used
as a metadata shelf rather than a fence. Mnemonics marked on the thing they
operate, including the one form I haven't seen documented anywhere else: the Jira
TUI puts each field's jump key on that field's own border. Focus signalled twice,
because a terminal has no hover and no shadow. Six ways to draw a chart at one
character of resolution.

**An anti-pattern list** where every entry shipped in a real application.
Truncation with no marker. A footer that wraps mid-word. A modal with no scrim
and no way out. Block art below its legible size. `→ Shfit front`, which is in a
finance TUI right now.

**Terminal constraints, cited rather than asserted.** `NO_COLOR` before any
capability check. Why UAX #11 isn't sufficient on its own, in the standard's own
words. OSC 11 to ask the terminal whether it's light or dark instead of assuming
it's dark. DEC mode 2026 against frame tearing. `gh a11y` as the shipped blueprint
for an accessible mode, since a 2D grid and a screen reader's 1D stream don't
otherwise meet.

Sources are in `references/evidence.md` and the full research is in
`docs/deep-research/`.

## What it doesn't do

It doesn't own design judgement. Hierarchy and restraint route to `design-craft`;
flow, the six states and the trunk test route to `ux-craft`; comparing two
rendered images routes to `be-my-witness`. This skill owns the medium, the
instrument, and the corpus.

It's also not for web or desktop GUI work.

## Installing

```
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install tui-craft
```

`pyte` is optional. Install it (`pip install pyte`, pure Python, no compiler) and
the capture uses it; without it the bundled parser runs instead, gated by 16
golden fixtures covering CJK, combining marks and ZWJ emoji. Run
`python3 scripts/tui_capture.py --self-test` and it tells you which one you're
getting. If the fixtures fail it refuses to report a captured frame at all,
because a parser that quietly mis-parses makes every gate downstream lie with
confidence.

## Evals

Measured against no skill at all, which is the honest comparison. Results and
what they show, including where the baseline held its own, are in
[EVALS.md](EVALS.md).
