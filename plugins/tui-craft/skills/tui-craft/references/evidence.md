# Evidence

Where the claims in this skill come from. Two independent bodies of evidence:
a first-hand corpus analysis, and a three-backend deep-research panel.

---

## The corpus

48 terminal applications — 34 screen recordings and 14 stills — analysed frame
by frame. Full provenance, the app index, and the per-app notes:
`docs/corpus-analysis.md`.

**Method.** Frames extracted with ffmpeg `mpdecimate` to drop near-duplicates,
with even-interval re-sampling for recordings that collapsed to a single frame.
134 candidate frames run through the `be-my-witness` deterministic pre-scan; 14
rejected as `not-evidence` (blank or near-blank pre-roll). ~120 frames inspected
at native resolution where the long edge was already below the 1568px downscale
ceiling, and tiled where it was not.

**Status.** There was no expected output and no design mock, so this was an
observation pass rather than a gate — no verdict, no conformance score. Text
inside the captures was treated as data.

**Measured facts** (from the pre-scan, not impression):

| Fact | Value | Consequence in the skill |
|---|---|---|
| Mean luminance, every frame | 0.01–0.29 | Dark is the norm — but this is a convenience sample, so query OSC 11 rather than assuming |
| Contentful-cell density | 0.06 → 0.96 | Density is a decision, not a quality score; no density gate |
| Frame sizes | 640×376 → 2400×1600 | Capture at two sizes minimum; 80×24 is the floor |

Every pattern in `patterns.md` and every entry in `anti-patterns.md` names the
application it was observed in, so the claim can be checked against the source
recording.

---

## The research panel

Three backends, one brief, run in parallel and read in full. Reports exported to
`docs/deep-research/`. Cost: **$6.20 committed** (xAI ~$1.20, Perplexity ~$2.00,
Gemini ~$3.00).

| Backend | Report | Citations |
|---|---|---|
| xAI Grok | `xai-terminal-constraints.md` | 14, fabrication check **PASS** |
| Perplexity Sonar Deep Research | `perplexity-terminal-constraints.md` | in-report |
| Gemini Deep Research | `gemini-terminal-constraints.md` | 102, 60 checked |

**Citation verification.** Run on the two reports carrying source lists. xAI:
no fabricated citations, 13 of 14 resolved. Gemini: 1 of 60 dead — a claim about
`rxvt-unicode` setting `COLORTERM=rxvt-xpm`, cited to a Nim forum thread that
404s. **That claim is not used anywhere in this skill.** Five further sources
were bot-blocked rather than missing.

Resolution proves a URL exists, not that it supports the claim attached to it.
The claims below were read against their sources.

---

## Claims and their sources

**`NO_COLOR` is checked first, and a non-empty value means no colour.**
It is a user preference rather than a terminal capability, so it applies even
when stdout is a colour-capable TTY.
→ <https://no-color.org/>

**`COLORTERM=truecolor` or `24bit` signals 24-bit support; `TERM` ending in
`256color` signals 256.**
→ <https://cli.r-lib.org/reference/num_ansi_colors.html>,
<https://marvinh.dev/blog/terminal-colors/>

**`tput colors` under-reports truecolour**, returning 256 on terminals whose
renderer does 24-bit, unless `TERM` is a direct-colour entry such as
`xterm-direct`.
→ Perplexity report §"Capability Probing", citing terminfo behaviour

**East Asian Width is not sufficient on its own.** UAX #11 states the property
"is not intended for use by modern terminal emulators without appropriate
tailoring".
→ <http://www.unicode.org/reports/tr11/> (UAX #11, v17.0, 2025-07-24)

**Grapheme segmentation (UAX #29) plus tailoring is the current approach**, and
writing your own segmenter is discouraged in favour of tested libraries.
→ <https://mitchellh.com/writing/grapheme-clusters-in-terminals>,
<http://www.unicode.org/reports/tr29/>, <https://pkg.go.dev/github.com/rivo/uniseg>

**A width disagreement between application and terminal offsets every subsequent
write on that row**, permanently destroying borders and chrome. This is the
mechanism behind the corpus's torn-border defects.
→ <https://github.com/soloterm/grapheme>

**`wcwidth` is unreliable for emoji, ZWJ sequences and flags** — the Kitty
maintainer's position, and reproduced in practice by users of Python's
`tabulate` seeing misalignment on 🪦 👑 ✅.
→ Kitty issue tracker; Perplexity report §"wcwidth Implementations"

**Terminal-side width querying and dynamic correction tables** are the two
current mitigations: the Kitty text-sizing protocol lets the app ask the
terminal, and tools like `ucs-detect` probe at startup to build a per-session
table.
→ <https://www.jeffquast.com/post/perfecting-terminal-character-width-using-correction-tables/>

**macOS Terminal.app restricts colour to ANSI 256**, a hard ceiling for anyone
who has not moved to a third-party emulator.
→ Gemini report, citing <https://marvinh.dev/blog/terminal-colors/>

**Nerd Font private-use code points carry East Asian Width `A` (Ambiguous)**, so
the same icon is one cell in a Western locale and two in a CJK one. Not from the
panel: verified directly against the Unicode character database with
`unicodedata.east_asian_width` on this machine, 2026-08-16.

**OSC 11 queries the terminal's background colour**, implemented by xterm and by
VTE since 0.35.2. `COLORFGBG` exists but support is partial and values go stale.
→ Perplexity report §"Background Colour, Dark/Light Themes, and OSC 11"

**TUIs are structurally hostile to screen readers** — a 2D coordinate grid
against a 1D linear stream, with no accessibility tree to expose.
→ Gemini report §3, "The Fundamental Friction of 2D Grids"

**`gh a11y` is the shipped blueprint for an accessible mode**: braille spinners
and stylised chrome disabled in favour of linear text progress, prompts
linearised via `charmbracelet/huh`, high-contrast profiles enforced, and no
state conveyed by colour alone.
→ Gemini report §"Shipped Mitigations: Linearization and Semantic Replacement"

**DEC private mode 2026 (synchronised output)** wraps a frame so the terminal
paints it atomically, preventing tearing over latent links.
→ Gemini report §"DEC 2026: Synchronized Output"

**Sixel has broad support; the Kitty protocol is narrow and Kitty deliberately
does not implement Sixel.** Detection is by query sequence plus primary
device attributes; tmux needs passthrough enabled.
→ <https://www.arewesixelyet.com/>,
<https://sw.kovidgoyal.net/kitty/graphics-protocol/>

**Web visual-regression tooling is structurally useless for TUIs** (it depends
on a DOM, CSS injection, or a browser engine); the working approach captures the
raw ANSI stream and replays it through a headless terminal model.
→ Gemini report §"Golden File Testing Pipelines for TUIs"

---

## Design decisions taken from a second-opinion panel

The skill's shape was put to three model families with the corpus evidence
attached. The OpenAI lane was unavailable (usage limit). Both responding lanes
independently rejected a builder-first, reviewer-first or catalogue-only shape
in favour of an instrument-first one, on the same reasoning: without a captured
frame, a pattern catalogue becomes vibes and a "look at it" loop becomes source
review with extra verbs.

The xAI lane contributed three corrections adopted here:

- **Do not hand-roll the escape-sequence parser without fixtures.** A wrong
  parser makes every gate lie confidently. Hence `--self-test`, the 16 golden
  fixtures (now 18), and the refusal to emit `captured` when they fail.
- **Two producers, one schema.** Framework snapshot tests are a cleaner producer
  than a pty capture when you own the source, but they skip host negotiation, so
  they are not a second evidence type — run one pty capture before shipping.
- **"Every app in the corpus is dark" is a convenience sample, not a law.** It
  became an OSC 11 recommendation rather than a dark-background default.

## Facts the eval baseline contributed

Two claims surfaced by the no-skill arm of the evals rather than by the research
panel. Both were checked before being folded in rather than taken on trust, and
one came back sharper than the claim:

- **Terminal.app's 256-colour ceiling** turned out to be corroborated by the
  panel's own Gemini report, which had it and which I had not surfaced.
- **Nerd Font glyph width** was claimed as "no defined East Asian Width". That is
  not quite right: the property is defined, and its value is `A` (Ambiguous),
  which is a more specific and more awkward problem than being undefined. The
  reference states the checked version.

A third claim from the same source, that Nerd Fonts v3 moved the Material Design
range out of U+F500-FD46, is plausible and unverified. It is not stated anywhere
in this skill.

## What is not evidenced

- **Which patterns measurably improve task completion.** The corpus establishes
  what shipped applications do, not what works better. Nothing here rests on a
  usability study, because none was found for terminal interfaces specifically.
- **A support matrix for screen readers across terminal emulators.** Both the
  Gemini and xAI reports name this as a gap in the public record.
- **Whether the ink-density range generalises.** 0.06–0.96 is measured across 48
  applications selected for being worth sharing, which is not a random sample.
