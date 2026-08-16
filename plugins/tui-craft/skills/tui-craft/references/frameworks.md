# Framework adapters

Four stacks, one job each: **how to get a frame out of it**, how to drive the six
states, and the handful of footguns that produce a visible cell defect.

Architecture is deliberately absent. The Elm loop, the widget tree and the
immediate-mode redraw are covered better by each framework's own documentation,
and restating them here would cost context without changing a cell on a captured
frame. What follows is only the part that does.

## Choosing

If a language is already in play, that decides it. If not:

| Job | Stack | Because |
|---|---|---|
| Single-binary ops tooling, ships to servers | **Bubble Tea** (Go) | One static binary, no runtime |
| Data-heavy dashboards, fastest to build | **Textual** (Python) | Richest widget set, CSS layout, best snapshot testing |
| Long-running monitors, tight resource budget | **Ratatui** (Rust) | No GC pauses, most control |
| Dev tooling in an existing JS project | **Ink** (TypeScript) | React model, npm ecosystem |

---

## Bubble Tea (Go)

**Frame out:** `github.com/charmbracelet/x/exp/teatest` drives the program and
gives you the output stream.

```go
tm := teatest.NewTestModel(t, model, teatest.WithInitialTermSize(100, 30))
tm.Send(tea.KeyMsg{Type: tea.KeyRunes, Runes: []rune("j")})
out, _ := io.ReadAll(tm.FinalOutput(t))
os.WriteFile("frame.ansi", out, 0644)
```

Then `python3 scripts/frame_from_ansi.py frame.ansi --cols 100 --rows 30 -o frame.json`.

**Footguns:**

1. **`len()` versus Lip Gloss width.** `lipgloss.Width(s)` measures cells;
   `len(s)` measures bytes and `utf8.RuneCountInString(s)` measures runes.
   Neither of the latter two is a width. Padding computed from them tears
   borders on any row containing CJK or emoji.
2. **Trailing newline in `View()`.** Bubble Tea joins views verbatim. A view
   ending in `\n` adds a blank row that shifts everything below it; one that
   omits a needed newline runs two sections together.
3. **`lipgloss.JoinHorizontal` with unequal heights** pads the shorter block to
   the taller one, which silently changes your layout's vertical rhythm. Set
   heights explicitly when the columns must align.
4. **Window size arrives as a message, not at init.** Rendering before the first
   `tea.WindowSizeMsg` uses whatever default you set. Guard the first paint.
5. **Styles are values, not pointers.** `s.Width(10)` returns a new style; a
   forgotten assignment silently keeps the old width.

---

## Textual (Python)

**Frame out:** Textual's own snapshot testing is the cleanest producer in any of
these frameworks.

```python
async def test_layout(snap_compare):
    assert snap_compare("myapp.py", terminal_size=(100, 30), press=["j", "enter"])
```

For a frame the gates can read, use `App.run_test()` and export:

```python
async with app.run_test(size=(100, 30)) as pilot:
    await pilot.press("j", "enter")
    open("frame.txt", "w").write(pilot.app.screen._compositor.__rich_console__ and "")
```

Simplest reliable route is to capture the process instead:
`python3 scripts/tui_capture.py --cmd "python3 myapp.py" --cols 100 --rows 30`.

**Footguns:**

1. **A scroll container clips rather than expands.** A widget taller than its
   container disappears below the fold with no warning; `overflow` and explicit
   heights decide this, and the default is not always what you want.
2. **CSS specificity.** Textual's CSS cascade follows web rules closely enough
   to surprise: an ID selector beats a class, and a later rule at equal
   specificity wins. A rule that looks correct and does nothing is usually this.
3. **`dock` removes the widget from normal flow**, and the remaining space is
   what siblings size against. Docking a footer after sizing the body means the
   body is one row too tall.
4. **Reactive attributes re-render on assignment**, including assignment of an
   equal value unless `always_update=False`. Cheap per widget, expensive in a
   list of 500.
5. **Rich markup in user data.** A value containing `[red]` is interpreted as
   markup. Escape anything that came from outside the app.

---

## Ratatui (Rust)

**Frame out:** `TestBackend` renders into an in-memory buffer.

```rust
let backend = TestBackend::new(100, 30);
let mut terminal = Terminal::new(backend)?;
terminal.draw(|f| ui(f, &app))?;
let buffer = terminal.backend().buffer().clone();
// write buffer content to a file, or assert on it directly
```

`Buffer` is already a typed cell grid, so assertions can be made directly against
it; `frame_from_ansi.py` is for when you want the same gates as everything else.

**Footguns:**

1. **`Constraint::Min` takes the remainder.** Two `Min` constraints in one layout
   split what is left in a way that is rarely what was intended; a `Min` beside a
   `Length` swallows every spare column. Prefer explicit `Length`/`Percentage`
   and one `Min` for the flexible region.
2. **Block borders consume the inner area.** A `Block` with borders leaves
   `inner()` two columns and two rows smaller. Computing children against the
   outer rect overdraws the border.
3. **Unicode width is yours to handle.** Ratatui does not measure your strings;
   use `unicode-width` and `unicode-segmentation`, and truncate on grapheme
   boundaries.
4. **Immediate mode redraws everything.** State that lives only in the draw
   closure is lost each frame — scroll offsets and selection belong in the app
   struct, and the stateful widgets (`StatefulWidget`) exist for exactly this.
5. **A zero-area rect panics some widgets.** At small terminal sizes a layout can
   compute a 0-width chunk. Guard the minimum size before drawing.

---

## Ink (TypeScript)

**Frame out:** `ink-testing-library` returns the rendered frames.

```ts
const {lastFrame, stdin} = render(<App />);
stdin.write('j');
fs.writeFileSync('frame.ansi', lastFrame() ?? '');
```

**Footguns:**

1. **Yoga flexbox, not CSS flexbox.** No `gap` on older versions, no `grid`, and
   `flexBasis` behaves differently. Layouts ported from web CSS drift.
2. **Text must be inside `<Text>`.** A bare string inside a `<Box>` throws at
   runtime rather than at build time.
3. **Wrapping is on by default.** A long string wraps and pushes everything below
   it down; set `wrap="truncate-end"` where a single row is required.
4. **Re-render is full-frame.** Ink diffs and repaints; a component re-rendering
   at 60fps will flicker over SSH. Throttle updates to what the data actually
   changes at.
5. **`process.stdout.columns` is undefined when not a TTY.** In CI that means
   `undefined` propagates into width maths and renders as `NaN` padding.

---

## What to test, whichever stack

The same six captures, every time:

| State | How to reach it |
|---|---|
| First run / empty | Run against empty fixture data |
| Loading | Capture with a short `--settle` before data lands |
| Ideal | The normal path, with realistic data volume |
| Partial | Half the fields populated; one column absent |
| Error | Point it at an unreachable dependency |
| Done / final | After the operation completes |

And the same three sizes: your design size, 80×24, and one wider than you expect.
Plus one `--no-color` capture, which is the cheapest possible test of whether
hierarchy rests on colour alone.
