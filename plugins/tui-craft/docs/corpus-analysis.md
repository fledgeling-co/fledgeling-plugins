# TUI reference corpus — analysis

**Provenance.** 48 artifacts in `~/Downloads/tui`: 34 animated GIFs (640×376 → 2400×1600, 2–1381 frames)
and 14 PNG stills (796×406 → 3470×2270). Frames extracted with ffmpeg `mpdecimate` (near-duplicate
drop); GIFs that collapsed to a single frame were re-sampled at even intervals. 134 candidate frames
prescanned with `be-my-witness/scripts/prescan.py`; 14 rejected as `not-evidence` (blank / <2%
contentful cells, i.e. pre-roll frames). ~120 frames inspected, at native resolution where the long
edge was already under the 1568px downscale ceiling, tiled at 50% crops where it was not.

**Status of this analysis.** There is no expected output and no mock, so per be-my-witness this is an
*observation* pass, not a gate: no verdict, no conformance score. Text visible inside the captures is
treated as data. Nothing in the corpus attempted injection.

**Measured corpus facts** (from prescan, not impression):

- Mean luminance across every inspected frame: **0.01–0.29**. There is not one light-background app
  in 48 artifacts. Dark is the terminal default, and designing light-first is designing against the
  corpus.
- Contentful-cell density ranges **0.06 (habit tracker, wtf notes) → 0.96 (sampler)**. Both ends
  produce good design. Density is a decision, not a quality axis.
- Aspect ratios cluster at 16:9 and 3:2 but include 640×600 (near-square) and 3000×540 (a 5.6:1
  ribbon). Fixed-width layout assumptions do not survive this corpus.

---

## The apps, identified

| # | App | What it is | Why it's in here |
|---|---|---|---|
| g01 | euporie | Jupyter notebook in the terminal | In-terminal window chrome, menu bar with access keys, heat-tinted dataframe |
| g02 | Lazykiq | Sidekiq/job-queue monitor | Best-in-corpus chrome: KPI chips, border-shelf metadata, tag-shaped active tab |
| g03 | (star map) | Constellation plotter | Braille sub-cell plotting |
| g04 | (MongoDB TUI) | Mongo client | Autocomplete popup with inline docs; tree sidebar |
| g05 | Bagels 0.3.3 | Personal finance | Annotated bars, command palette, category tree, segmented control |
| g07 | (net monitor) | Packet/speed monitor | Mode-sensitive help line; focused-panel border colour |
| g08 | vtop | System monitor | Braille density plots; keycap footer |
| g09 | (SID player) | Chiptune player | ASCII banner + rules; VU meters; bottom-border metadata |
| g10 | (music player) | Audio player | Real album art (graphics protocol) + gradient spectrum |
| g11 | ekphos | Markdown research tool | 3-pane + welcome modal; heading glyph-per-level; breadcrumb status bar |
| g12 | sampler | Config-driven dashboard | Inline series legend inside plot; empty state that teaches |
| g13 | dolphie v4 | MySQL monitor | Panels by background fill, not borders; unit-coloured numerics |
| g14 | presenterm | Terminal slide deck | Slide progress bar; markdown chrome; inline images |
| g15 | (torrent search) | Search + downloads | Mnemonic letter marked on the panel title |
| g16 | (download manager) | Downloader | Chunk map; gradient progress; the model modal |
| g17 | moltbook TUI | Reddit-style client | Rank-scaled block wordmarks; bracketed-mnemonic filter chips |
| g18 | htop | Process viewer | The canonical meter and F-key bar |
| g20 | SOT v4.1 | System observation tool | Maximum density; nested stat boxes |
| g21 | Posting 1.0.2 | HTTP client (Textual) | Richest "premium" surface in the corpus |
| g22 | jolt v0.1.0 | Power/battery monitor | Footer that shows current setting *values* |
| g23 | Trippy v0.8.0 | Traceroute | Inverted header row; status-dot column; centred border title |
| g24 | Ducker | Docker TUI | Single-accent monochrome; chevron keycaps |
| g25 | mdfried | Markdown renderer | Headings rendered as scaled images |
| g26 | (Logstash TUI) | Logstash monitor | Per-row timeline heat strip + colour legend |
| g27 | (football scores) | Live scores | Alignment encodes team side; comparison bars |
| g28 | splashboard | Repo splash renderer | Chooser with inline descriptions; magazine two-column preview |
| g29 | (epub reader) | Book reader | TOC tree; chord bindings in brackets; % progress |
| g30 | (markdown editor) | Obsidian-flavoured editor | Source-block + rendered-output pairing; minimap rail; mode pill |
| g31 | Cronboard v0.6.2 | Cron manager | Modal done badly (see anti-patterns) |
| g32 | (agent CLI) | Coding agent | Inline progressive-disclosure hints; interrupt hint on the running item |
| g33 | (LLM cost dash) | Token/cost dashboard | Four-column faceted selector; totals above stacked bars |
| g34 | Gitwig v2.2.1 | Git TUI | Three metadata slots on one border line; mode-dependent footer |
| p01 | noodle | HTTP client | Ghost "add row"; dot-marked populated tabs |
| p02 | stormy | Weather | The whole app is one small well-set block |
| p03 | coderabbit | Code-review CLI | Gradient wordmark; inverted footer bar |
| p04 | celerator | Celery monitor | State column as coloured chips |
| p05 | (habit tracker) | Habit grid | Borderless layout, grouping by whitespace alone |
| p06 | kanha v0.1.2 | Security tool help | The canonical help/usage screen |
| p07 | wtf | Modular dashboard | Widget grid where each cell owns its layout |
| p08 | oxker | Docker TUI | Header row that is also the sort control; context menu |
| p09 | Jira TUI | Issue tracker | Densest form; mnemonic key on every field's own border |
| p10 | btui | Bluetooth manager | Inline (non-alt-screen) app that takes only the rows it needs |
| p11 | (disk usage) | Treemap/du tool | In-row bar column; real treemap |
| p12 | gh pr status | Styled CLI output | Same colour semantics without any TUI |
| p13 | croft | VS Code-shaped workspace | A GUI's IA carried into a terminal |
| p14 | WorkOS AuthKit installer | Installer/wizard | Vertical stepper with node glyphs |

---

## Patterns worth stealing

### 1. The border is a shelf, not a fence

The strongest single move in the corpus. A panel border carries metadata at up to three anchor
points on the same line, and on the bottom border too.

- Lazykiq: title `Jobs in batch` (left, red) + `SIZE: 9.8K · PAGE: 1/391` (right) on the top border.
- Gitwig: `Gitwig` (left) + `Sort: Custom` (centre) + `v2.2.1` (right) — three slots, one line.
- Jira TUI: `Page 1 of 1 (total: 25)` on the **bottom** border of the list.
- SID player: `Total time: 03:37:12` on the bottom border of the queue.
- oxker: the live value in the title — `cpu 03.82%`, `memory 184.42 MB`.
- noodle: `200 OK` inset top-right of the Response panel, in green.
- Posting: the collection name inset in the bottom border of the sidebar.

This buys a whole row of vertical space per panel and puts the metadata where the eye already is.

### 2. Mnemonics live on the thing they operate

Four escalating treatments, all observed:

1. **Letter brightened inside the word** — Trippy's `help settings quit`, torrent search's panel
   titles `s̲earch` / `r̲esults`, croft's `ᵐenu` / `ᵖreset`.
2. **Bracketed inside the label** — moltbook's `[N]ew`, `[T]op`, `[D]iscussed`, `[R]andom`.
3. **Keycap chip beside the label** — vtop's `dd Kill process`, Lazykiq's `s switch queue`,
   moltbook's `[1] Feed`, Gitwig's `Navigate [↑↓]`.
4. **Key inset on the field's own border** — Jira TUI puts `(p)`, `(t)`, `(s)`, `(a)`, `(j)`, `(x)`,
   `(z)` in the bottom-right of each input's frame. Every field advertises its own jump key.

(4) is the best form-navigation affordance in the corpus and I have not seen it documented anywhere.

### 3. Focus is signalled redundantly, or it isn't signalled

Terminals have no cursor blur, no shadow, no hover. Every app that reads clearly signals focus at
least twice:

- ekphos: border brightens **and** title brightens.
- Net monitor: focused panel's border turns amber **and** the top help line changes to that mode's keys.
- Jira TUI: focused field's border **and** its label take the accent.
- Gitwig: the status-bar mode chip changes (`NORMAL` → `DETAIL`) **and** the listed actions change.
- Bagels: header row highlighted **and** current row highlighted — two levels of selection at once.

The corpus's own counter-example: MongoDB TUI's form fields are solid blue blocks with no border,
and the focused one is only slightly lighter. It is genuinely hard to tell where you are.

### 4. The footer is a live surface, not a legend

- jolt shows current *values*: `t theme (Default)`, `a appearance (auto)`, `refresh: 1.0s`.
- Gitwig and the markdown editor lead with a mode pill (`NORMAL`, `DETAIL`).
- noodle shows the environment as a coloured dot: `● staging`.
- Gitwig and croft show live `mem: 10.0mb  cpu: 18.8%` right-aligned.
- Net monitor swaps the whole line by mode: `Press q to exit, e to start editing, dd to delete rule.`
  → `Press Esc to stop editing, Enter to record the rule.`
- Separator conventions split three ways: middot (`•`) for metadata, pipe (`|`) for peers, chevron
  (`›`) for hierarchy. The apps that pick one and hold it read better than the ones that mix.

### 5. Charts that work at one-character resolution

Ranked by information per cell, all observed:

- **Braille** (`⠁⠂⠄`) — 2×4 sub-cell dots. sampler, vtop, jolt, Trippy, Logstash. The only way to get
  a real line chart in a terminal.
- **Block runs** (`█▉▊▋`) — 8ths of a cell horizontally, so a bar is smooth to 1/8 cell. htop, Bagels.
- **Bracket meters** (`[|||||   37.5%]`) — htop's per-core meters; the bracket is the track, the fill
  is gradient-coloured by load, and the percentage sits *inside* the bracket, right-aligned.
- **Chunk/heat grids** — download manager's chunk map (hundreds of discrete units as coloured cells);
  Logstash's per-row timeline strip; the habit tracker's dot matrix.
- **Treemap** — real nested rectangles, coloured (disk-usage tool).
- **In-row bars** — a bar column inside a table, all bars sharing a baseline (disk-usage tool).
- **Graphics protocols** — actual images via sixel/kitty/iTerm2 (music player album art, epub figures,
  mdfried's scaled headings, presenterm). Real, and worth using when the terminal supports it.

Annotation conventions that recur: value labelled at the end of the bar or above it; a floating
bordered stat box inside the plot area carrying `cur / dlt / max / min` per series (sampler,
Logstash); the axis maximum pinned to the plot's top-left corner (oxker); time axes reading
right-to-left into the past with `now  −30s  −60s` (jolt).

### 6. Density is a decision, and both ends are legitimate

- **0.06** — the habit tracker: no borders at all, six cards on an implicit 3×2 grid, grouped by
  whitespace, a dim label and a dot matrix each. Archived habits get a strikethrough. It is the most
  confident design in the corpus.
- **0.96** — sampler, SOT: every cell earning its keep, ten panels, five colours.

What separates good density from bad is whether the *colour roles* stay constant. SOT survives at
0.9 because green/amber/red mean the same thing in all eleven panels. Celerator struggles at 0.4
because it uses four saturated hues for four states with no legend and a fifth for selection.

### 7. States, observed

The corpus does actually ship the unglamorous states, and the good examples teach:

- **Empty that teaches the action** — sampler's `<ENTER> to view options`; Gitwig's `Select a file to
  view its diff`; torrent search's `No active downloads`.
- **Ghost row as the add affordance** — noodle's dim `[ ] Key / Value` row at the end of the header
  table; MongoDB's `Click to add new connection / or by pressing Ctrl+L, Ctrl+Right`.
- **Placeholder that shows format** — download manager's mirrors field pre-filled dim with
  `http://mirror1.com, http://mirror2.com`; `(auto-detect)` for the filename; Jira's
  `Type in a JQL expression to search issues...`.
- **Progressive disclosure hinted inline** — the agent CLI's `(ctrl+o to expand)` on each collapsed
  result and `(esc to interrupt)` on the *running* item, not in the footer.
- **A stepper for sequential work** — the WorkOS installer's vertical rule with `◇` done, `●` sub-step,
  `◐` in-progress. The cleanest progress pattern here.

### 8. The model modal

Download manager's "Add Download" is the one to copy: sized to its content (not the screen), centred,
inset title, dim placeholder examples, a right-aligned inline affordance on the row it belongs to
(`[Tab] Browse`), and — the part everyone forgets — **its own key hints inside its own footer**:
`tab browse/next · enter confirm/next · esc cancel`. The user never has to guess how to leave.

ekphos's welcome modal adds a keybinding table and `Press Enter or Space to continue`.
moltbook's About adds `Press '8' or Esc to close`.

---

## Anti-patterns — every one observed in a shipped app in this corpus

1. **Hard truncation with no marker.** Lazykiq cuts `ImageProcessingJob::Unsupporte` at the panel
   edge with nothing to say it was cut. noodle drops the head of a path: `sers/carlosmontecinos/…`.
   Compare MongoDB TUI and the football app, which both use `…`. A truncation the user can't see is
   a lie about the data.
2. **Footer overflow.** Cronboard's 13-item key list runs off the edge mid-word: `Tab Change Ta ^p
   palette`. The footer must be budgeted and demoted (or paged behind `?`) before it wraps.
3. **Modal with no scrim and no containment.** Cronboard's dialog covers the app with a decorative
   dashed border, the underlying UI peeking through the margins, and no dismissal hint inside it.
   ekphos's welcome modal also floats over live content with no dimming.
4. **Block-art wordmarks below their legible size.** Cronboard's figlet logo renders as broken
   fragments at its shipped size. Block art needs a minimum cell budget or a plain-text fallback.
5. **Focus colours with no stated meaning.** Jira TUI uses red, amber, and blue accents on different
   fields in one view. Celerator outlines panels in red (which reads as error) to mean focus.
6. **Markdown flattening.** moltbook renders a bulleted list as one run-on paragraph — "Simple
   interface for the full Moltbook API Secure-by-design authentication handling First-class
   support…". List structure lost, italics retained.
7. **Encoding/width failure.** The football app's header renders as mojibake
   (`EHrOñy¥CWOVï±hZ5ea§GèkOOoÞçAcE`). Width and encoding bugs are the terminal's characteristic
   failure and need a test, not a hope.
8. **Unproofed footers.** Bagels ships `→ Shfit front`. The footer is the most-read text in the app
   and the least proofed.
9. **Inconsistent title anchoring.** The download manager anchors panel titles top-left on some
   panels and top-right on others in the same view.

---

## Terminal-specific constraints the old skill never mentions

These are the ones that actually break TUIs, and none are in `tui-design-skill`:

- **Cell width is not character count.** CJK and most emoji are two cells wide; combining marks and
  ZWJ sequences are one grapheme over several code points. Column maths done in `len()` misaligns
  every table below it. moltbook renders `自主之路` correctly in a list whose alignment survives —
  that is a deliberate width-aware implementation, not luck.
- **Colour depth is negotiated, not assumed.** Truecolour, 256, 16, and none all exist; `NO_COLOR`
  and `TERM=dumb` are real. Every gradient in this corpus degrades to nothing on a 16-colour terminal.
- **Light terminals exist even though this corpus has none.** Hard-coded near-black backgrounds
  invert into unreadable on a light profile; the ANSI palette is the portable route.
- **Nerd fonts are a dependency.** croft, Gitwig, MongoDB TUI, SOT and the epub reader all use
  private-use-area glyphs. Without the font they render as tofu. That needs a fallback, not a README note.
- **Alt-screen vs inline is a design decision.** btui and gh pr status print in the normal buffer and
  leave their output in scrollback; splashboard, Lazykiq and the rest take the alt screen and vanish
  on exit. Scrollback-preserving output is the right call for anything the user may want to paste.
- **Resize is continuous, not an event you can ignore.** The corpus spans 640×376 to 2400×1600.
- **Screen readers.** A TUI drawn with box characters and absolute positioning is close to unusable
  with a screen reader; the mitigation is a non-interactive text mode, which no app here ships.

---

## What this means for the new skill

The existing `tui-design-skill` is a well-written essay about design in general, retargeted at
terminals. Its principles are not wrong — "start monochrome", "spacing is the most impactful choice",
the 4–5 colour palette — they are simply **ungrounded**: nothing in it is traceable to a real app, so
none of it tells you what a good TUI actually *looks like*. It carries no pattern with a rendering, no
anti-pattern anyone has actually shipped, no terminal-specific failure mode, and — the largest gap —
**no way to look at the thing you built**. design-craft's entire method is render → crop → ask "what
is wrong with this?", and a TUI is trivially capturable (VHS, asciinema, termshot, or a plain
`script`/`tmux capture-pane`). A TUI design skill without a looking loop is giving advice it never
checks.

The new skill should carry, at minimum:

1. A **pattern catalogue** where each entry is a rendered example, traced to the app it came from.
2. The **anti-pattern list above**, each one with the app that shipped it.
3. A **capture-and-look loop** — the design-craft method, in terminal form, with real tooling.
4. The **terminal constraint set**: cell width, colour depth, fonts, alt-screen, resize, NO_COLOR.
5. ux-craft's **non-negotiables translated to the terminal**: one primary action, the three questions,
   the six states, errors that say what to do, recognition over recall, destructive-action friction.
6. **Density as a stated decision** rather than an implied maximum.
