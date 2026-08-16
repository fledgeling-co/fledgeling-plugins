---
name: tui-craft
description: Design, build, and review terminal user interfaces (TUIs) against a captured cell grid rather than against source code. Use whenever someone builds, redesigns, reviews, or polishes anything that draws to a terminal — a dashboard, log viewer, file browser, installer, wizard, admin panel, data browser, or an interactive CLI being turned into a full-screen app — and whenever they name a TUI framework (Bubble Tea, Textual, Ratatui, Ink, Blessed, prompt_toolkit, crossterm, tview, urwid). Also use when a terminal UI "looks broken", has torn or missing borders, misaligned columns, text running off the edge, tofu boxes, colours that vanish when piped, or breaks on resize — and when someone asks whether a TUI is ready to ship. Captures the running app through a pty into a typed cell grid, runs mechanical gates on it (border integrity, cell-width arithmetic, overflow, truncation markers, glyph risk), then applies a pattern catalogue drawn from 48 shipped TUIs. Not for web or desktop GUI work.
---

# tui-craft

A terminal is a grid of cells, and almost every real TUI defect is arithmetic on
that grid going wrong. A string template does not tell you how many cells it
occupies. So reading the source tells you what the program *intends* to draw,
never what it draws — and the gap between those two is where the bugs live.

This skill closes that gap with an instrument. You capture the running app into
a typed cell grid, and every claim you make about how it looks refers to that
grid. Build and review are the same loop; they differ only in who wrote the app.

## The rule that makes the rest work

**A claim about a screen needs a captured frame.** Not the source, not a
description, not a mock you sketched in a fenced code block. If capture fails,
that failure is the result you report — `capture blocked`, with what you tried.
It is never a reason to fall back on reading the code and saying it looks right.

This is worth holding even when it feels pedantic, because the failure mode it
prevents is specific and common: the model reads its own string template, does
the column arithmetic in its head, gets `len("🚀 Deploy") == 8` instead of 9,
and declares a layout valid that renders with a torn border. Its predecessor
skill shipped 4,900 lines of sound design advice and had no way to see a single
pixel of what it produced.

Two frame kinds, and only one of them is evidence:

- `captured` — produced by `scripts/tui_capture.py` (or by a framework snapshot
  test piped through `scripts/frame_from_ansi.py`). Carries provenance: command,
  size, `TERM`, parser, a hash of the raw bytes.
- `mock` — anything you drew by hand. Useful for proposing a layout, and it may
  never support a finding. Label it, and say so when you show it.

## The loop

Same five steps whether you are building or reviewing.

**1. Decide the frame before you draw one.** Size, and whether the app takes the
alternate screen. A capture at 100×30 says nothing about 60×20, and the reference
corpus spans 640×376 to 2400×1600. Pick at least two sizes: the one it is
designed for, and 80×24, which is the floor that still exists everywhere.

**2. Capture.**

```bash
python3 scripts/tui_capture.py --cmd "./myapp" --cols 100 --rows 30 \
  --settle 1.2 --dump -o frame.json
```

`--keys "j,j,Enter,wait:0.5,/,f,o,o"` drives it to a state. Every state you
intend to claim anything about gets its own capture — the six states below are
six captures, not one screenshot and some optimism.

**3. Gate.** `python3 scripts/tui_gates.py frame.json` — mechanical checks that
return row and column coordinates. These are arithmetic, not taste, which is why
they run before you look: a torn border makes every judgement above it worthless.
Fix what they find first.

**4. Look at the ruler dump.** The dump is a character matrix with column
rulers, and it is the artifact to read — not a screenshot. Misalignment that is
invisible in a rendered image is obvious against a ruler. Ask it *"what is wrong
with this?"* rather than *"is this done?"* — the same grid answers those two
questions differently.

Raster capture earns its place for exactly one class of question the grid cannot
decide: whether a Nerd Font glyph renders as tofu, whether block-art is legible
at its shipped size, whether a braille chart reads. For those, render the frame
to HTML and open it with Obscura. Not as the default.

**5. Fix, and re-capture.** A fix you have not re-captured is a fix you have not
made.

Batch the loop: capture every state and size in one round, fix everything that
round surfaces, confirm with one more round, stop. Per-tweak re-capture is churn.

## What the gates decide, and what you decide

The gates own the arithmetic:

| Gate | Catches |
|---|---|
| `border-integrity` | A box that opens and does not close on the same column |
| `width-arithmetic` | A row pushed past its neighbours by a double-width glyph |
| `overflow-wrap` | Content that ran off the edge and continued mid-word |
| `truncation-marker` | Text cut at the edge with no ellipsis to say so |
| `shelf-containment` | An inset border label that crowded out its rule |
| `glyph-risk` | U+FFFD, and private-use glyphs that need a font the reader may lack |
| `colour-inventory` | Colour count, and a frame with no bold and no dim anywhere |

They are deliberately narrow. `truncation-marker` catches clipping at the frame
edge; a string the app itself cut at 53 characters looks like ordinary text to a
gate, and only you can catch that by comparing the cell against the data.

Everything above arithmetic routes out, and these are standing dependencies
rather than optional extras:

- **`ux-craft`** owns the flow, the six states, the trunk test ("where am I,
  what can I do, what happens next"), errors that say how to fix, recognition
  over recall, and destructive-action friction. Load it before designing a flow
  or reviewing one.
- **`design-craft`** owns hierarchy, restraint, and the anti-slop pass. Its
  visual rules mostly transfer; its typographic ones do not, because a terminal
  has one size and one family. Weight, colour, spacing and position are the
  whole toolkit.
- **`be-my-witness`** owns comparing two rendered images when you genuinely have
  a raster pair and a reference.

## Reviewing: find wide, then filter

Run the find pass with no severity filter at all. Asking for "only serious
issues" during the looking measurably lowers what gets found, because the
instruction is followed literally and quietly. Report everything you see,
including uncertain findings — then rank, merge and drop in a separate pass, and
let the ranked list be short if the surface is clean.

Every finding carries its row and column, what the cell holds, what it should
hold, and which capture it came from.

## The states, in a terminal

A TUI has the same six states as any interface — first-run/empty, loading,
ideal, partial, error, done — and the corpus shows the good ones teaching rather
than merely reporting:

- The empty state names the action that fills it (`<ENTER> to view options`),
  rather than saying "no data".
- The add affordance is often a dim ghost row at the end of a table, not a button.
- A placeholder shows the *format* (`http://mirror1.com, http://mirror2.com`),
  not just the field name.
- A collapsed result carries its own expand hint (`ctrl+o to expand`), and a
  running item carries its own interrupt hint (`esc to interrupt`) — at the item,
  not in the footer.
- Sequential work gets a stepper: a vertical rule with `◇` done, `●` step,
  `◐` in progress.

## Patterns

`references/patterns.md` is the catalogue — every entry traced to a shipped app
in the reference corpus, with a rendering. Read it before laying out a screen.
The ones that recur hardest:

- **The border is a shelf, not a fence.** A panel border carries a title left, a
  state centre, a version right, and a page count on the *bottom* rule. It buys
  a row of vertical space per panel and puts metadata where the eye already is.
- **Mnemonics live on the thing they operate** — brightened letter in the word,
  bracketed letter in the label, keycap chip beside it, or the key inset on each
  form field's own border.
- **Focus is signalled at least twice**, because a terminal has no hover, no
  shadow and no blur. Border *and* title; or border *and* a footer mode change.
- **The footer is a live surface**, showing current setting values and a mode
  pill, not a static legend.
- **Density is a decision, not a score.** The reference corpus runs from 6% to
  96% of cells carrying a glyph and both extremes are excellent. What separates
  good density from bad is whether colour roles stay constant across panels.

`references/anti-patterns.md` is the counterpart, and every entry in it was
observed in a real shipped application rather than imagined.

## Terminal truths

`references/terminal-truths.md` carries the constraints with their sources.
The ones that change what you write:

- **Cell width is not character count.** CJK and most emoji take two cells;
  combining marks and ZWJ sequences take zero. When the app computes a width the
  terminal disagrees with, every later write on that row is offset and the
  borders never recover.
- **Unicode's East Asian Width property is not sufficient on its own** — UAX #11
  says so explicitly. Grapheme segmentation (UAX #29) plus a tested library is
  the current approach; writing your own segmenter in 2026 is not advised.
- **Colour is negotiated, never assumed.** `NO_COLOR` set to any non-empty value
  means no colour, checked first. `COLORTERM=truecolor|24bit` means 24-bit.
  `tput colors` under-reports truecolour on most terminals.
- **Ask the terminal what colour it is** with an OSC 11 query, then compute
  luminance. Every app in the reference corpus is dark-background, but that is a
  convenience sample and not a licence to paint a dark canvas over a light theme.
- **Nerd Font glyphs are a dependency**, and render as tofu without the font.
- **Alt-screen versus inline is a design decision.** Inline leaves output in
  scrollback where it can be pasted; alt-screen vanishes on exit.
- **Screen readers linearise; a 2D grid resists that.** The shipped answer is a
  dedicated mode — `gh a11y` disables braille spinners and stylised chrome for
  linear text, linearises prompts, and never encodes state in colour alone.
- **Wrap each frame in DEC mode 2026** (`CSI ?2026 h` … `CSI ?2026 l`) so a
  partially-painted frame is never visible over a slow link.

## Frameworks

Pick by the language already in play; if none is, pick by the job.
`references/frameworks.md` carries one thin adapter each for Bubble Tea (Go),
Textual (Python), Ratatui (Rust) and Ink (TypeScript). Each covers only what
changes a cell on a captured frame: how to emit a frame from that stack's own
snapshot testing, how to drive the six states, and the three to five footguns
that produce visible defects. Architecture is not in there — the framework's own
documentation covers it better, and restating it costs context without changing
a cell.

## Scope

Deliver what was asked, at the scope intended. Make routine calls yourself and
check in only where two readings would produce materially different work.
Delegate to a subagent only for a genuinely large, independent track — a wide
audit across many screens — never to re-check a capture you just took.

Keep the reply short: lead with the outcome, then what changed, then what is
open. Match a written deliverable to what the task needs and stop.
