# Terminal truths

The constraints that actually break terminal interfaces, with sources. These are
the rules worth stating precisely, because getting them approximately right
produces defects that look like something else.

Sources are in `references/evidence.md`; the full research reports are in
`docs/deep-research/`.

**Contents**
1. [Cell width](#1-cell-width)
2. [Colour negotiation](#2-colour-negotiation)
3. [Light and dark](#3-light-and-dark)
4. [Fonts and glyphs](#4-fonts-and-glyphs)
5. [Alt-screen versus inline](#5-alt-screen-versus-inline)
6. [Size and resize](#6-size-and-resize)
7. [Frame tearing](#7-frame-tearing)
8. [Accessibility](#8-accessibility)
9. [Graphics protocols](#9-graphics-protocols)
10. [Testing](#10-testing)

---

## 1. Cell width

**A character is not a cell.** East Asian characters and most emoji occupy two
cells; combining marks, zero-width joiners and variation selectors occupy none.
`len()` on a string is not its rendered width in any language.

The failure is worse than a cosmetic misalignment, and the mechanism is worth
holding in mind: **if the application computes a width the terminal disagrees
with, every subsequent cell write on that row is offset, and the borders, chrome
and scroll regions below never recover.** That is why a single CJK string in one
table cell tears the panel border, which is exactly what the corpus shows.

**Unicode's East Asian Width property is not sufficient on its own.** UAX #11
says so directly: the property "is not intended for use by modern terminal
emulators without appropriate tailoring". It resolves Wide and Fullwidth to two
cells and everything else to one, which is right for CJK and wrong for emoji
sequences, flags, skin-tone modifiers and presentation selectors.

Ambiguous-width characters are one cell in a Western locale and two in a CJK
one — a genuine fork with no universally correct answer.

**What to do:**

- Use a maintained grapheme-segmentation library (UAX #29) rather than writing
  your own. Go's `uniseg`, Rust's `unicode-segmentation`, Python's `wcwidth`
  with grapheme handling. Writing a segmenter by hand in 2026 is explicitly
  discouraged by every source consulted.
- Slice strings on grapheme cluster boundaries, never on bytes or code points.
- Where the terminal supports it, ask it: the Kitty text-sizing protocol lets an
  application query the rendered width of a string, delegating the problem to the
  terminal's own font shaper. Where it does not, libraries like `ucs-detect`
  build a per-session correction table by probing edge cases at startup.
- Test with a fixture containing CJK, a ZWJ emoji sequence, a combining mark and
  a flag, and assert against the captured cell grid.

`scripts/tui_capture.py` implements the pragmatic default (UAX #11 plus
zero-width categories plus the emoji blocks) and its golden fixtures cover CJK,
combining marks and ZWJ. It is good enough to catch the defects; it is not a
substitute for a real segmenter in the application itself.

---

## 2. Colour negotiation

Colour depth is negotiated. The chain, in the order to check it:

1. **`NO_COLOR`** — if set to any non-empty value, emit no colour. This comes
   first, before any capability check, and it is a user preference rather than a
   terminal property: it applies even when stdout is a TTY that supports 24-bit
   colour. Command-line software that adds colour by default is expected to
   honour it.
2. **`COLORTERM`** — `truecolor` or `24bit` means 24-bit colour is safe.
3. **`TERM`** — a value ending in `256color` implies a 256-colour palette.
4. **Fall back conservatively** to 16 colours, then to none.

**`tput colors` under-reports.** It consults terminfo, and most terminals ship a
terminfo entry advertising 256 colours even when the renderer does 24-bit —
`tput colors` returns 256 unless `TERM` is set to a direct-colour entry such as
`xterm-direct`. Treat it as a floor, not an answer.

**macOS Terminal.app caps at 256 colours**, and it is still the default terminal
on every Mac. A truecolour gradient does not degrade gracefully there; it hits a
hard ceiling. If your design leans on 24-bit colour, a large share of your users
are not seeing it, and `--no-color` is not the only degraded path worth
capturing.

Multiplexers complicate this further: tmux and screen need explicit
`terminal-overrides` carrying `Tc` or `RGB` for truecolour to reach the
application inside them.

**Design consequence:** every gradient degrades. Design the 16-colour rendering
first and treat truecolour as an enhancement, or capture with `--no-color` and
look at what is left. If the screen is unreadable without colour, hierarchy was
resting on colour alone.

---

## 3. Light and dark

Every one of the 48 applications in the reference corpus is dark-background
(measured mean luminance 0.01–0.29). That is a convenience sample of what people
record and share, not a licence to assume it.

**Do not paint a full-screen dark canvas.** An application that hard-codes a near
-black background inverts into unreadable on a light profile, and it overrides a
choice the user already made.

**Ask the terminal instead.** An OSC 11 query (`OSC 11 ; ? BEL`) asks the
terminal to report its background colour; compute the luminance of the reply and
choose accordingly. xterm implements it, and VTE — which backs GNOME Terminal,
Terminator, Guake and others — has since 0.35.2.

`COLORFGBG` exists and encodes foreground and background as palette indices, but
support is partial and values go stale. Use it as a hint, never as the answer.

The safest default remains: use the terminal's default background (emit no
background colour at all) and let the user's theme show through.

---

## 4. Fonts and glyphs

**Nerd Font glyphs are a dependency, and they are width-ambiguous.** Private-use
-area code points render as tofu boxes for anyone without the font installed, and
several corpus apps (croft, Gitwig, the MongoDB TUI, SOT, the epub reader) depend
on them for file-type icons and branch markers.

The width problem is subtler than the missing-glyph one and worth checking
yourself:

```python
>>> import unicodedata
>>> unicodedata.east_asian_width('')   # a common powerline separator
'A'
```

`A` is **Ambiguous**, not Neutral. Ambiguous resolves to one cell in a Western
locale and two in a CJK one, so the same icon can occupy a different number of
cells for two different users of the same build, and the layout only breaks for
one of them. That is a bug report you cannot reproduce.

`scripts/tui_capture.py` resolves Ambiguous to one cell, which matches what
mainstream terminals do by default. It will therefore agree with a Western-locale
terminal and disagree with a CJK-locale one, so a capture is evidence about the
first and not the second.

Box-drawing characters and braille are far safer — they are in standard Unicode
blocks and covered by most monospace fonts — but braille density plots depend on
the font having genuinely proportional braille cells, and some do not.

**What to do:** treat icon glyphs as an enhancement with a text fallback, default
them off rather than trying to detect a font (you cannot), and let the user turn
them on. State the font requirement in the README rather than assuming it.

`glyph-risk` in the gates reports private-use code points so the dependency is at
least visible.

---

## 5. Alt-screen versus inline

A real design decision, and both are correct in different places.

**Alt-screen** (`CSI ?1049h`): the app takes the whole terminal and the previous
contents are restored on exit. Right for anything long-running or navigable —
dashboards, editors, browsers. The cost is that nothing survives: a user cannot
scroll back to what your app showed, or paste it.

**Inline**: the app draws in the normal buffer, takes only the rows it needs, and
leaves its output in scrollback. Right for anything whose result the user may
want to keep, quote or pipe — status output, installers, one-shot queries. `btui`
and `gh pr status` in the corpus both do this.

A useful hybrid: run interactively in the alt screen, and on exit print a compact
summary inline so the session leaves a trace.

---

## 6. Size and resize

The reference corpus spans 640×376 to 2400×1600 pixels; in cells, that is
roughly 80×24 to 200×60. Assume neither end.

- **80×24 is the floor that still exists everywhere.** Capture at it.
- Handle `SIGWINCH` and re-layout, rather than assuming the size at startup.
- Below your minimum usable size, say so explicitly rather than rendering a
  broken layout: a centred "needs at least 60×20" is a designed state.
- Resize during a redraw is a real race. Debounce it.

---

## 7. Frame tearing

A frame painted cell by cell over a slow link (SSH, tmux control mode) is
visible in intermediate states — borders appear and disappear, the layout jumps.

**DEC private mode 2026 (synchronised output)** fixes this. Wrap each logical
frame:

```
CSI ? 2026 h        begin synchronised update
  … all cell writes for this frame …
CSI ? 2026 l        end synchronised update
```

The terminal buffers and paints atomically, so no partial frame is ever seen.
Most modern terminals support it and the ones that do not ignore it harmlessly,
which makes it close to free.

---

## 8. Accessibility

**A TUI is structurally hostile to a screen reader.** The application draws a
two-dimensional grid addressed by coordinates; a screen reader consumes a
one-dimensional stream. There is no accessibility tree to expose, and the
terminal cannot infer one.

The shipped answer is not to make the grid accessible but to offer an
alternative mode. **GitHub CLI's `gh a11y` is the blueprint:**

- Braille spinners and stylised chrome are disabled, replaced with linear
  text-based progress a reader can parse in order.
- Prompts are linearised — a static text question and linear input, instead of a
  2D grid of interactive options the reader has to traverse.
- High-contrast profiles are enforced, and **no state is conveyed by colour
  alone**; a textual marker always accompanies it.

Regulatory pressure is real and increasing (WCAG 2.2 AA, the European
Accessibility Act), so budget for the fallback mode rather than treating it as
optional polish.

The floor that applies even without a dedicated mode: body text contrast ≥ 4.5:1
against the actual background, never colour as the only signal, every action
reachable by keyboard, and focus always visible.

---

## 9. Graphics protocols

Real images in a terminal are possible and three protocols compete.

| Protocol | Support | Notes |
|---|---|---|
| **Sixel** | Broad — xterm, foot, konsole, wezterm, mintty, mlterm, tmux (built with `--enable-sixel`) | The portable choice. Kitty deliberately does not implement it. |
| **Kitty graphics** | Kitty, and a small number of others | Richest: PNG/RGBA, compression, file or direct transmission. |
| **iTerm2 inline images** | iTerm2, WezTerm | Simplest to emit. |

**Detection is by query, not by environment variable.** Send the protocol's
query sequence followed by a primary device-attributes request; a reply carrying
only the DA response means no support. Inside tmux, passthrough must be enabled
or the sequence never reaches the terminal.

Worth it for genuine content — album art, figures in a document, a chart that
cannot survive braille. Not worth it for decoration, and always with a
character-cell fallback.

---

## 10. Testing

Web visual-regression tooling (Percy, Applitools, BackstopJS) is structurally
useless here: it depends on a DOM, CSS injection or a browser engine.

**The workflow that works** is the one this skill implements: capture the raw
ANSI byte stream from the application, replay it through a headless terminal
model into a deterministic cell grid, and assert against that. The frameworks
mostly ship their own producer of that stream — `teatest` for Bubble Tea,
`TestBackend` for Ratatui, snapshot testing for Textual, `ink-testing-library`
for Ink — and `scripts/frame_from_ansi.py` converts any of them into the same
frame schema the gates read.

Determinism requires pinning what varies: terminal size, `TERM`, locale, colour
depth, and any animation or clock in the app itself. A capture of a screen with a
live clock in it will never match twice; freeze it or exclude that region.
