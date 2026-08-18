# Evidence

Where the claims in this skill come from. Three independent bodies of evidence:
a first-hand corpus analysis, a three-backend deep-research panel on terminal
constraints, and a later two-backend panel on capture trust — plus a set of
measurements taken directly on this machine, which is where the load-bearing
rules about capture failure come from.

---

## Capture trust: what was measured here, 18 August 2026

The rules in `SKILL.md` step 3 are not inferred. They are the result of running
the instrument against eleven deliberately broken inputs and recording what came
back, and **the reason they exist is that the predecessor passed five of them.**

Every row below is a real invocation of `tui_capture.py` at 80×24, followed by
`tui_gates.py --strict`, on this machine:

| Input | Predecessor | Rebuild |
|---|---|---|
| Nonexistent binary | `captured`, exit 0, 0 high | `capture-blocked`, exit 127 recovered |
| Non-executable file (`/etc/passwd`) | `captured`, exit 0, 0 high | `capture-blocked`, exit 126 recovered |
| Python `ModuleNotFoundError` | `captured`, exit 0, 0 high | `capture-blocked`, error relayed |
| Shell syntax error | `captured`, exit 0, 0 high | `capture-blocked`, error relayed |
| `echo hello` | `captured`, exit 0, 0 high | `capture-blocked`, never addressed the grid |
| `head -30 /etc/hosts` | `captured`, exit 0, 0 high | `capture-blocked`, never addressed the grid |
| `true` / `exit 3` (silent) | `capture-blocked` | `capture-blocked` |
| `SIGSEGV` | `capture-blocked` | `capture-blocked`, signal named |
| `less` (real full-screen TUI) | `captured` | `captured` |
| `clear; echo hi` (inline, no alt-screen) | `captured` | `captured` |

**The root cause was one discarded value.** The predecessor's `capture()`
signalled the child unconditionally and then called
`os.waitpid(pid, os.WNOHANG)` *throwing the result away*, so the exit status was
never observed at all. Reaping before signalling recovers it: 127 for a missing
binary, 126 for a non-executable file, a negative code for a signal death, and —
the useful negative case — a real interactive TUI is the only class that has to
be killed, because it is still running when the settle window closes.

**The wait has to be bounded.** A blocking `waitpid` here hung the capture
indefinitely on a child that survives `SIGTERM`; measured, and the reason `_reap`
polls with a deadline in every branch rather than blocking once.

**Control sequences, measured across nine programs.** Counts from the raw byte
stream, same session:

| Program | CSI | Cursor moves | Erase | SGR | Alt-screen |
|---|---|---|---|---|---|
| `vi` | 40 | 13 | 3 | 4 | yes |
| `less` | 6 | 1 | 1 | 2 | yes |
| `clear; echo hi` | 3 | 1 | 2 | 0 | no |
| Python traceback | 10 | **0** | 0 | **10** | no |
| `echo hello` | 0 | 0 | 0 | 0 | no |
| `head` a file | 0 | 0 | 0 | 0 | no |
| `top -l 1` | 0 | 0 | 0 | 0 | no |
| Nonexistent binary | 0 | 0 | 0 | 0 | no |

Two conclusions the gate depends on. **SGR is not evidence of a UI** — a
colourised traceback emits ten SGR sequences and zero cursor moves, so a check
that counted "any escape sequence" would pass it. And **alt-screen cannot be
required**, because `clear; echo hi` is a legitimate inline screen that never
sets it; requiring 1049h would refuse the whole inline class the skill explicitly
supports.

**Held loosely, and it is a real disagreement with the research.** The panel is
explicit that the absence of cursor addressing *"cannot be treated as definitive
failure"* for non-curses TUIs, and that exit 127 is *"strong but not infallible"*
because POSIX does not reserve it — an application may return 127 while drawing
correctly. Both cautions are right, and they are why the "never addressed the
grid" branch refuses only in **conjunction** with the program having already
exited, rather than on the protocol signal alone. A long-running program that
paints with nothing but newlines will still be refused, and that is a known false
positive with a stated escape: the reason names the signal counts, so a reader can
overrule it in one line.

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

The one place a corpus number enters a gate is `render-proof`'s 6% ink line, and
it enters as a **`medium`, never a fail**, phrased as "unusual rather than wrong".
That is the density-is-a-decision rule holding under pressure: the temptation when
fixing a failure that had 3% ink is to set the floor at 5% and call it done, which
would fail the sparsest well-designed application in the corpus.

---

## The capture-trust panel

Two backends, one brief, run in parallel and read end to end. Reports exported to
`docs/deep-research/`. Reservation committed: **$5.00** worst case
(Gemini ~$3.00, Perplexity ~$2.00).

The plan named a four-member panel at $9.70. Eight research runs were already in
flight on this machine and the panel needed four slots at once, so it was
hand-assembled from the two members whose distinctive strengths the question
actually called for — breadth across four subtopics, and a date-windowed index.
**That is a two-member panel and is reported as one**, not as the four the plan
priced.

| Backend | Report | Citations | Fabrication check |
|---|---|---|---|
| Perplexity Sonar Deep Research | `perplexity-capture-trust.md` | 20 | 1 malformed of 20, 90% resolved |
| Gemini Deep Research | `gemini-capture-trust.md` | 37 | **2 of 37 do not exist**, 78% resolved |

**Two dead citations in the Gemini report carried load-bearing claims, and both
were replaced with a primary source rather than kept with a caveat:**

- The WCAG contrast thresholds (4.5:1 normal, 3:1 large, 7:1 AAA) were cited to a
  university brand page that does not resolve. Replaced by reading W3C's own
  Understanding SC 1.4.3 page directly on this machine, which states *"a contrast
  ratio of at least 4.5:1"* and *"Large-scale text … at least 3:1"*, with 7:1
  attributed to SC 1.4.6. The numbers held; the citation did not.
- A claim that `zutty` runs `vttest` headlessly and hashes the video output was
  cited to a 404. **It is not used anywhere in this skill.**

**The spotlighting figures were verified at source.** "Reduces the attack success
rate from greater than 50% to below 2%" is quoted verbatim from the abstract of
Hines et al., *Defending Against Indirect Prompt Injection Attacks With
Spotlighting*, arXiv 2403.14720 (March 2024), read on this machine — and the
abstract attributes it to GPT-family models, which the skill says. The three
technique names (delimiting, datamarking, encoding) are reported by the panel from
the full paper and were **not** verified against the abstract, which does not name
them. The counter-figure — above 30% end-to-end compromise under adaptive attacks,
attributed to the LLMail-Inject challenge and to Nasr et al. — comes from the panel
and its primary sources were not read here, so it is stated as a bound on the
fence's usefulness rather than as a measurement of this skill.

**Where the two reports disagree, and the disagreement is kept:**

- **Screen readers and the alternate screen.** Perplexity marked this
  `<MISSING_DATA>` and said explicitly that no official documentation on how
  NVDA, JAWS or VoiceOver handle an alternate-screen curses app was found. Gemini
  found sources at medium confidence (an AppleVis forum thread, a college
  accessibility guide) saying such apps read as an unreadable static grid unless
  the user engages Screen Review or Object Navigation manually. Neither is a
  vendor statement. The skill therefore still rests its screen-reader advice on
  `gh a11y`, a shipped implementation, rather than on either report.
- **Truecolour as an accessibility remedy.** Gemini recommends mandating 24-bit
  sequences for anything that must be legible, since they bypass the user's theme
  and make a contrast ratio knowable. That is exactly why `composition.md` argues
  it is a cost: the app is then ignoring a preference the user set deliberately,
  including a light theme. Both are right about the mechanism and they disagree
  about which side to fall on. Unresolved on purpose.
- **`--settle` is a hardcoded sleep, which both reports call an anti-pattern.**
  They recommend polling for semantic readiness instead. `tui_capture.py` still
  takes a fixed `--settle`, and the cheap check is in the frame already: capture
  twice and compare `raw_sha256`, since two identical streams mean it had settled.
  Named here rather than fixed, because a readiness predicate that works across
  every framework is a larger change than this rebuild took on.

**What this panel does not establish.** Nothing in either report measures whether
any of the design patterns in `patterns.md` improves task completion. The line
length figure both reports offer (50–75 characters, 66 as a target) rests on
secondary UX research, and one report marked its own version an inference — so it
is **not** a gate and is not stated as a rule anywhere in this skill.

Resolution proves a URL exists, not that it supports the claim attached to it.

---

## The terminal-constraints panel

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

**Web visual-regression tooling is structurally useless for TUIs** (it depends on
a DOM, CSS injection, or a browser engine); the working approach captures the
raw ANSI stream and replays it through a headless terminal model.
→ Gemini report §"Golden File Testing Pipelines for TUIs"

**Exit status 127 means the command was not found; 126 means found but not
executable; 128+N means killed by signal N.** No POSIX text reserves these, so
they are strong evidence rather than proof — an application may return 127 for its
own reasons while drawing correctly, which is why `render-proof` never rests on the
exit code alone.
→ <https://unix.stackexchange.com/questions/242111/using-reserved-codes-for-exit-status-of-shell-scripts>;
corroborated by direct measurement on this machine (table above)

**stdout and stderr are merged under a pty and cannot be separated after the
fact.** The kernel attaches both descriptors to the same terminal device, so
"assert stderr is empty" is not available to a pty harness. The documented case is
Paramiko, where `get_pty=True` silently combines the two streams.
→ <https://docs.python.org/3/library/pty.html>,
<https://github.com/paramiko/paramiko/issues/1142>

**`ESC[?1049h` enters the alternate screen buffer**, which terminfo calls `smcup`.
Its presence is strong evidence of a full-screen application; **its absence is
not evidence of failure**, because inline TUIs legitimately never set it.
→ <https://jameshfisher.com/2017/12/04/how-less-works/>; measured here on `vi`,
`less` and `clear; echo hi`

**Ink density fails as a sole capture-trust signal.** Every established TUI test
harness compares a full framebuffer rather than an aggregate metric — Textual via
`pytest-textual-snapshot`, Ratatui via `TestBackend` plus `insta`, tmux via
`capture-pane`. A legitimately sparse screen and an error screen have the same
density.
→ <https://textual.textualize.io/guide/testing/>,
<https://ratatui.rs/recipes/testing/snapshots/>,
<https://drmaciver.com/2015/05/using-tmux-to-test-your-console-applications/>

**`pilot.pause()` drains Textual's message queue before an assertion.** A
hardcoded sleep races the layout engine; both reports call fixed sleeps an
anti-pattern in terminal testing.
→ <https://textual.textualize.io/guide/testing/>

**Snapshot flakiness in terminal tests comes from four named sources**: unfixed
terminal size, an unpinned `TERM`, locale differences in grapheme rendering, and
trailing-whitespace diffs. The mitigations are to fix the geometry explicitly, to
export a known `TERM`, and to trim trailing whitespace before diffing.
→ <https://textual.textualize.io/guide/testing/>,
<https://ratatui.rs/recipes/testing/snapshots/>

**`tmux capture-pane -e` strips RGB attributes unless the session has the `Tc`
capability override**, so a colour assertion taken through tmux without it reads
as monochrome.
→ Gemini report §"Multiplexer and External PTY Emulation" (single-sourced;
not independently verified here)

**WCAG requires 4.5:1 for normal text and 3:1 for large text at Level AA, and
7:1 at AAA.** Read directly at source on this machine, 18 Aug 2026: *"a contrast
ratio of at least 4.5:1"* and *"Large-scale text and images of large-scale text
have a contrast ratio of at least 3:1"*, with 7:1 attributed to SC 1.4.6. The page
also states the threshold does not round — 4.499:1 does not meet 4.5:1.
→ <https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html>

**The 16-colour ANSI palette has no defined RGB mapping.** The values are whatever
the reader's terminal theme sets, so an application naming `red` cannot know its
own contrast ratio. This is the reason a role ladder is measurable only from hex
values, and the reason `examined=0` is the honest answer on a captured frame.
→ <https://jvns.ca/blog/2024/10/01/terminal-colours/>

**Red/green is the pairing to avoid; blue-orange, blue-red and purple-green
survive the common colour-vision deficiencies.** Colour-blind readers also
re-map their terminal palette, which is a second reason hue cannot be the only
carrier.
→ <https://news.ycombinator.com/item?id=46810904> (community discussion, not a
standard — held loosely)

**Fencing untrusted content in explicit delimiters cuts naive prompt-injection
success from above 50% to below 2%**, measured on GPT-family models, and degrades
under adaptive attack.
→ <https://arxiv.org/abs/2403.14720> (Hines et al., March 2024; the figure was
read verbatim from the abstract on this machine). The three named instantiations —
delimiting, datamarking, encoding — are reported by the panel from the full paper
and were not verified against the abstract.

**Treating captured output as data rather than instructions is the documented
control**, alongside structured separation of instructions from data.
→ <https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html>


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
