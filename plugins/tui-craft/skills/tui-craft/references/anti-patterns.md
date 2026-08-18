# Anti-patterns

Every entry was observed in a shipped terminal application in the reference
corpus — not imagined, not inferred from principle. That matters, because these
are the defects that survive review by competent people, which is what makes
them worth a checklist.

Each one names the app, the mechanism, and the gate that catches it (where a
gate can).

---

## 1. Hard truncation with no marker

**Observed:** Lazykiq cuts an error column at the panel edge —
`ImageProcessingJob::Unsupporte` — with nothing to indicate it was cut. noodle
drops the *head* of a path: `sers/carlosmontecinos/Projects/README.md`.

**Why it matters:** a reader cannot distinguish a truncated value from a short
one. `Unsupporte` looks like it might be the whole error. Worse for the head-cut
case, where the string reads as a valid relative path.

**Fix:** always mark the cut. `…` at the truncated end, and for paths prefer
middle-elision (`/Users/…/Projects/README.md`) which keeps both ends. The
MongoDB TUI and the football app both do this correctly.

**Gate:** `truncation-marker` catches clipping at the frame edge. A string the
app itself cut short is invisible to a gate — compare the cell against the
underlying data.

---

## 2. Footer overflow

**Observed:** Cronboard's thirteen-item key list runs off the edge mid-word:
`… Tab Change Ta ^p palette`.

**Why it matters:** the footer is the most-read text in a TUI, and it is the one
place a user looks when lost. A footer that breaks is a broken map.

**Fix:** budget it. Measure the rendered width at your minimum supported size,
and when the list outgrows it, demote to a `? help` overlay rather than letting
it wrap. Order by frequency, not by keyboard layout.

**Gate:** `overflow-wrap`, with a caveat this entry needs. The gate compares the
edges of each *content column*, found by splitting the row on its vertical rules,
and Cronboard's footer sits inside a bordered frame — the shape the predecessor
gate was structurally blind to, because it compared column 0 against column
`cols-1` and on a bordered app both hold `│`. It fires on bordered panels now, but
it tolerates only one pad column on each side. A panel padded by two or more hides
the wrap from it again, and a footer that wrapped *and* was then truncated shows
neither tell. Read the dump.

---

## 3. Modal with no containment

**Observed:** Cronboard's dialog covers the app behind a decorative dashed
border, with the underlying UI visible at the margins and no dismissal hint
anywhere inside it. ekphos's welcome modal floats over live content with no
dimming.

**Why it matters:** without a scrim the eye cannot tell what is modal and what is
underneath, and without a dismissal hint the user guesses between Esc, q, and
Enter.

**Fix:** size the modal to its content, centre it, dim or blank what is behind
it, and put its own keys in its own footer. The download manager's "Add
Download" does all four.

---

## 4. Block art below its legible size

**Observed:** Cronboard's figlet wordmark renders as disconnected fragments at
its shipped size.

**Why it matters:** a broken logo is worse than no logo — it reads as a rendering
bug in the app rather than as branding.

**Fix:** set a minimum cell budget for the block art and fall back to styled
plain text below it. Check it at 80×24, not only at your development size.

---

## 5. Focus colours with no stated meaning

**Observed:** the Jira TUI uses red, amber and blue accents on different fields
in the same view. celerator outlines focused panels in red, which reads as an
error state.

**Why it matters:** colour in a terminal is scarce and users learn it fast. Three
focus colours teach three different things and mean one.

**Fix:** one accent for focus, held everywhere. Semantic colours (red for error,
green for healthy) stay reserved for semantics. If focus needs more emphasis, add
the second signal — a title change, a mode pill — rather than a second colour.

**Gate:** `colour-inventory` reports the count; the meaning is yours to check.

---

## 6. Markdown flattened into a paragraph

**Observed:** moltbook renders a bulleted list as one run-on paragraph —
"Simple interface for the full Moltbook API Secure-by-design authentication
handling First-class support for posts, comments, voting…". Italics survived;
the list structure did not.

**Why it matters:** the structure was the content. Flattened, the text reads as
a wall and the items become unfindable.

**Fix:** if you render markdown, render its block structure — lists get a bullet
and an indent, headings get a per-level glyph (`◆ ■ ▸`, as ekphos does, since a
terminal cannot change type size). Test with a document that exercises every
block type.

---

## 7. Encoding and width failure

**Observed:** the football app's header renders as mojibake:
`EHrOñy¥CWOVï±hZ5ea§GèkOOoÞçAcE`.

**Why it matters:** this is the terminal's characteristic failure. It usually
means bytes were decoded with the wrong codec, or a width calculation walked into
the middle of a multi-byte sequence.

**Fix:** decode explicitly as UTF-8 and slice on grapheme clusters rather than
bytes or code points. Add a fixture with CJK, an emoji ZWJ sequence and a
combining mark, and assert the rendered cell grid.

**Gate:** `glyph-risk` flags U+FFFD.

---

## 8. Unproofed footer copy

**Observed:** Bagels ships `→ Shfit front`.

**Why it matters:** it is on screen constantly, and it is the cheapest possible
signal that nobody read the finished product.

**Fix:** read the footer out loud once before shipping. It takes ten seconds and
it is the highest-visibility text in the application.

---

## 9. Inconsistent title anchoring

**Observed:** the download manager anchors some panel titles top-left and others
top-right in the same view.

**Why it matters:** the eye learns where to look for a panel's name. Moving it
costs a scan on every panel.

**Fix:** pick an anchor and hold it. Use the other anchors for a different *kind*
of information — state, counts, version — so position itself carries meaning.

---

## 10. Colour as the only signal

**Observed:** several corpus dashboards encode status purely as a coloured cell
with no glyph or label.

**Why it matters:** it fails for colour-blind readers, in monochrome terminals,
under `NO_COLOR`, and in any piped or logged output.

**Fix:** pair colour with a glyph or a word. oxker's `√ running` / `‖ paused` /
`✗ exited` survives every one of those conditions. Where colour genuinely is the
encoding — a heat grid, a swimlane — ship a legend, as Logstash does.

**Gate:** `colour-inventory` flags a frame with no bold and no dim anywhere,
which is the strongest signal that hierarchy rests on colour alone.

---

## 11. Reading the source instead of the render

**Not observed in an app — observed in the tooling around them**, and it is the
reason this skill exists.

The predecessor skill to `tui-craft` carried 4,900 lines of sound design advice
and no way to see a single frame of output. Its review workflow was "evaluate
visual design quality against principles above", performed against source code.

**Why it matters:** a string template does not tell you how many cells it
occupies. `len("🚀 Deploy")` is 8 in Python and 9 cells on screen, and that
one-cell difference tears the border on every row below it.

**Fix:** capture the frame. It is the whole loop in `SKILL.md`.

---

## Generated tells

Everything above was observed in a shipped application. This section is the one
exception and is marked as such: these are the tells that a terminal screen was
*generated* rather than designed. They are not drawn from the corpus, because the
corpus is 48 applications people chose to ship — they are the moves a model
reaches for when it is decorating rather than deciding, and each one is greppable
in a diff.

`design-craft` owns the general anti-slop pass and cannot see a cell grid, so the
terminal-specific list has to live here.

**1. A truecolour gradient across a header row.** The one effect that degrades to
*nothing* rather than to less: it vanishes under `NO_COLOR`, through a pipe, and on
a 16-colour terminal, taking the header's only hierarchy with it. Gradients also
need a colour per cell, which is the opposite of a role.

**2. Emoji as panel titles.** Two cells wide, font-dependent, and the arithmetic
breaks the border of the panel being titled — the `len("🚀 Deploy")` failure
applied to chrome, where it tears every row below.
**Gate:** `width-arithmetic` catches the tear, `glyph-risk` the font dependency.

**3. A figlet or block-art wordmark on a screen that is not the splash.** Four to
six rows of an 80×24 budget spent saying the name the user just typed.
**Gate:** `glyph-risk` where it uses private-use glyphs; the budget question is
yours.

**4. Three border weights on one screen**, or `╔═╗` double-lines everywhere. A
border weight that means nothing is decoration on the one channel a terminal
cannot spare — and rounded on some panels with square on others, in the same
frame, with no rule behind which is which.

**5. A spinner on an operation that completes inside one frame.** It flashes once
and reads as a glitch. A spinner is a promise that waiting is happening.

**6. Four or more chip hues with no legend.** Colour marks one axis; past that it
has stopped encoding and started decorating.
**Gate:** `colour-inventory` counts distinct foreground colours and flags above
six.

**7. A `│` gutter down the middle of a screen with nothing either side of it
that differs.** A rule that separates two things of the same kind is a rule that
is only there to look structural.

