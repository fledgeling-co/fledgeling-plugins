# Pattern catalogue

Every pattern here was observed in a shipped terminal application. The app is
named so the claim is checkable, and each entry shows the shape rather than
describing it — a rendering is worth more than a paragraph when the medium is
a character grid.

Source corpus: 48 applications (34 recordings, 14 stills), analysed frame by
frame. `docs/corpus-analysis.md` has the full provenance and the app index.

**Contents**
1. [Chrome and structure](#1-chrome-and-structure)
2. [Navigation](#2-navigation)
3. [Focus and selection](#3-focus-and-selection)
4. [Keys and mnemonics](#4-keys-and-mnemonics)
5. [Tables and lists](#5-tables-and-lists)
6. [Forms](#6-forms)
7. [Charts at one-character resolution](#7-charts-at-one-character-resolution)
8. [Status, footers and modes](#8-status-footers-and-modes)
9. [Overlays](#9-overlays)
10. [Identity](#10-identity)

---

## 1. Chrome and structure

### The border as a metadata shelf

The strongest single move in the corpus. A panel's border is a rule you are
already drawing; hang information on it and you save a row of vertical space per
panel while putting the metadata where the eye already is.

Up to three anchors on the top rule, and the bottom rule takes them too.

```
┌─Gitwig──────────────── Sort: Custom ──────────────────────── v2.2.1─┐
│                                                                     │
│  demo                                                               │
│  main                                              ● 1+  1!  1?     │
│                                                                     │
└─────────────────────────────────────────────── Page 1 of 1 (25) ────┘
```

Observed: Gitwig (title / sort state / version on one rule), Lazykiq
(`Jobs in batch` left, `SIZE: 9.8K · PAGE: 1/391` right), Jira TUI (`Page 1 of 1
(total: 25)` on the bottom rule), the SID player (`Total time: 03:37:12` on the
bottom rule), oxker (the live value in the title: `cpu 03.82%`), noodle
(`200 OK` inset top-right, in green), Posting (collection name on the bottom
rule of the sidebar).

Keep the anchor consistent across panels. The download manager in the corpus
anchors some titles left and others right in the same view, and it reads as a
mistake rather than a rhythm.

### Panels without borders

Borders are not the only way to group, and two of the best-composed screens in
the corpus use none.

`dolphie` builds cards from a background one step lighter than the page:

```
    ╭ Host Information ──╮   ← what most tools do
    │ Version  MySQL 8.0 │
    ╰────────────────────╯

       Host Information         ← what dolphie does: a fill, no rule
       Version   MySQL 8.0
       Uptime    3 days
```

The habit tracker uses nothing at all — six cards on an implicit 3×2 grid,
grouped by whitespace, each a dim label over a dot matrix. It is the most
confident layout in the corpus and it has zero box-drawing characters in it.

Reach for a border when you need to *contain* something (a scroll region, a
table with its own header). Reach for spacing when you only need to *group*.

### Widget grid

`wtf` composes a dashboard from independent modules, each a bordered box with an
emoji-and-name title, each owning its own internal layout, unified only by that
convention. Cells differ in height; the grid is column-based. It scales to
sixteen widgets without a redesign.

---

## 2. Navigation

### Numbered tabs

The number is the shortcut, and putting it in the label removes a legend.

```
 1 Dashboard   2 Busy   3 Queues   4 Retries   5 Scheduled   6 Dead
```

Lazykiq renders the number in an inverted keycap and the active tab as a
tag/arrow shape in amber. moltbook uses `[1] Feed  [2] Leaderboard` with the
active one as a filled chip. Gitwig uses `| W [1] | F [2] | G [3] |`.

### Underlined active tab

Where there is no number, an accent underline is the clearest active marker,
because a terminal cannot change size or weight much.

```
 Headers•   Body•   Parameters   Auth   Settings
 ────────
```

Posting and noodle both do this, and both add the pattern worth stealing: a
**dot suffix marks a tab that has content in it**. One character, and the user
stops opening empty tabs.

### Segmented control

```
 Spending Trajectory  │  Spending  │  Balance
 ═══════════════════
```

Bagels puts one under a chart to switch the series. Active in bold accent,
inactive dim. The download manager uses bordered pills instead, with counts
baked in: `Queued (0)` `Active (1)` `Done (0)`.

### Tree sidebar

```
 ▼ sample_analytics
     accounts
     transactions
     customers
 ▼ sample_mflix
     movies
```

Disclosure triangles `▼ ▸`, one indent level per depth, and the leaf that is
selected takes the fill. Posting adds colour-coded method badges (`GET` green,
`POST` amber, `DEL` red) as a left column — the badge does the work an icon
would do in a GUI.

---

## 3. Focus and selection

A terminal has no hover, no shadow, no blur. **Signal focus at least twice**, or
users will not find it.

| App | Signal one | Signal two |
|---|---|---|
| ekphos | border brightens | panel title brightens |
| net monitor | border turns amber | help line swaps to that mode's keys |
| Jira TUI | field border takes accent | field label takes accent |
| Gitwig | panel border | footer mode pill `NORMAL` → `DETAIL` |
| Bagels | header row highlighted | current row highlighted (two levels at once) |

The counter-example is instructive: the MongoDB TUI renders form fields as solid
blue blocks with no border, and marks focus with a slightly lighter blue. It is
genuinely hard to tell where you are.

Selection itself is usually a full-width fill:

```
  9755  DataSyncJob   "stripe", "local_db"
▌ 9754  DataSyncJob   "salesforce", "local_db"   ← full-row fill, text stays legible
  9753  ReportGenJob  "activity", "8/2024"
```

Keep the text readable against the fill. Several corpus apps invert to a
saturated background and leave the foreground unchanged, which drops contrast
below usable.

---

## 4. Keys and mnemonics

Four treatments, escalating in specificity. Pick one and hold it.

**1. Brightened letter in the word** — cheapest, works inside prose.

```
 help  settings  quit          ← h, s and q rendered bright, rest dim
```
Trippy; the torrent search app applies it to panel titles (`search`, `results`).

**2. Bracketed letter in the label** — unmissable, costs two cells.

```
 [N]ew   [T]op   [D]iscussed   [R]andom   [s]huffle
```
moltbook, with the active filter as an inverted chip.

**3. Keycap chip beside the label** — the footer default.

```
 dd Kill process   j Down   k Up   g Jump to top   c Sort by CPU
```
vtop, htop's F-key bar, Lazykiq's `s switch queue`.

**4. The key inset on the field's own border** — the best form affordance in the
corpus, and rare enough to be worth naming.

```
 ┌─Status──────────────────┐  ┌─Assignee────────────────┐
 │ Select a status       ▼ │  │ Select a user         ▼ │
 └──────────────────(s)────┘  └──────────────────(a)────┘
```

Jira TUI puts `(p)`, `(t)`, `(s)`, `(a)`, `(j)`, `(x)`, `(z)` in the bottom-right
of each input's frame. Every field advertises its own jump key, on itself, with
no legend anywhere.

---

## 5. Tables and lists

### Header row as the sort control

oxker makes the header a full-width inverted bar that is simultaneously the
column labels, the sort state, and the help affordance:

```
 name    state    status      ▼ cpu   memory/limit   ↓ rx   ↑ tx   ( h ) show help
```

The arrow marks the sorted column and its direction. htop does the same with
`CPU%▽`, jolt with `Impact ▼`.

### Status as a glyph column

Trippy renders hop status as a coloured circle in its own narrow column — no
legend needed because the colours are conventional and the column is consistent.
oxker uses `√ running`, `‖ paused`, `✗ exited`, which survives a monochrome
terminal in a way a bare colour does not.

### State chips

```
 RECEIVED    STARTED    SUCCESS    FAILURE
 ────────    ───────    ───────    ───────
   amber       cyan      green      magenta      ← each on an inverted fill
```

celerator. Effective, but it is also the corpus's warning about chip-colour
inflation: four saturated hues, no legend, and a fifth colour for selection.

### Metadata line under the title

```
 Moltdocs transforms documentation into living knowledge
   m/headlines • u/Moltdocs • 17h ago • 985,622 pts • 2,838 comments
```

moltbook, the download manager (`↓ Downloading • 42% • 20.54 MB/s • 449 MB /
1.1 GB`), the football app. A middot-separated dim line under a bright title
carries a surprising amount without a table.

Hold one separator convention: middot for metadata, pipe for peers, chevron for
hierarchy. The apps that mix them read as noisier than they are.

### In-row bars

A bar column inside a table, all bars sharing a baseline, with the number
right-aligned beside it:

```
 libanimestan_bridge.a   ████████████████████     1.0   126.5 MiB
 libicrate-a353c45f.rlib ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁     0.7    90.7 MiB
```

The disk-usage tool. The selected row tints its bar too, which is a nice touch.

---

## 6. Forms

The Jira TUI is the reference implementation and worth reading in full
(`docs/corpus-analysis.md`, entry p09). What transfers:

- Label inset in the field's own top-left border; jump key in its bottom-right.
- Placeholder text dim and showing the *format*, not restating the label.
- Read-only fields rendered dim with no border accent — they look unfocusable
  because they are.
- **Exactly one saturated fill on the screen**, on the primary action. It is the
  only green thing in a blue-and-amber view and it reads instantly.
- A required/unsaved marker `(*)` inset on the field's border.

The download manager's "Add Download" is the model modal form:

```
 ┌─Add Download───────────────────────────────────────────────┐
 │  URL:      https://sin-speed.hetzner.com/1GB.bin           │
 │  Mirrors:  http://mirror1.com, http://mirror2.com          │  ← dim, an example
 │  Path:     /home/meet/Downloads              [Tab] Browse  │  ← affordance on its row
 │  Filename: (auto-detect)                                   │
 │                                                            │
 │  tab browse/next · enter confirm/next · esc cancel         │  ← its own keys
 └────────────────────────────────────────────────────────────┘
```

Sized to its content, not the screen. Its own key hints in its own footer, so
leaving is never a guess.

---

## 7. Charts at one-character resolution

Ranked by information per cell.

| Technique | Resolution | Seen in |
|---|---|---|
| Braille `⠁⠂⠄⡀` | 2×4 sub-cell dots | sampler, vtop, jolt, Trippy, Logstash |
| Block runs `█▉▊▋▌▍▎▏` | 8ths of a cell horizontally | htop, Bagels |
| Bracket meter | fill + value inside the track | htop |
| Chunk / heat grid | one cell per discrete unit | download manager, Logstash |
| Treemap | nested coloured rectangles | disk-usage tool |
| Graphics protocol | real pixels | music player, epub reader, mdfried |

The bracket meter is the most copied idea in terminal software and deserves its
reputation — the bracket is the track, the fill is gradient-coloured by load, and
the value sits right-aligned *inside* the track:

```
 0[||||||||             37.5%]   4[|||||                25.0%]
 2[||||||||||||||||||||100.0%]   6[|||                  12.5%]
```

Annotation conventions that recur:

- Value labelled at the end of the bar, or above it (the LLM cost dashboard puts
  the daily total above each stacked bar).
- A floating bordered stat box *inside* the plot area, one per series, carrying
  `cur / dlt / max / min` — sampler and Logstash both do this and it is far more
  readable than a legend below the axes.
- The axis maximum pinned to the plot's top-left corner (oxker).
- Time flowing right-to-left into the past: `now  −30s  −60s` (jolt).
- When colour encodes state, ship a legend. Logstash puts
  `■ NEW  ■ RUNNABLE  ■ BLOCKED  ■ WAITING  ■ TIMED_WAITING` under its swimlanes.

### Annotated bars

Bagels puts callouts above and below a segmented bar, with a connector pointing
at the boundary:

```
 ┌ Spent: 1165.42                          Remaining: 1334.58 ┐
 ███████████████████░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
                    └ Save: 1000.0
```

### Comparison bars

The football app splits a bar proportionally between two sides, value left and
right, which encodes a comparison in one row:

```
        Possession
  70% ▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░ 30%
        Total Shots
   14 ▓▓▓▓▓▓▓▓▓░░░░░░░░░ 11
```

It also uses **alignment to encode team side** — home events flush right, away
events flush left, either side of a centre line. No labels needed.

---

## 8. Status, footers and modes

The footer is the most-read text in a TUI. Treat it as a live surface.

**Show current values, not just keys.** jolt's footer reads
`t theme (Default)   a appearance (auto)   refresh: 1.0s`, so the footer answers
"what is it set to" as well as "how do I change it".

**Lead with a mode pill.** Gitwig (`NORMAL` / `DETAIL`), the markdown editor
(`NORMAL` in a rounded chip beside the filetype). The pill changes with focus,
and so does the list of actions beside it.

**Show environment state.** noodle puts `● staging` bottom-left with a coloured
dot. Getting this wrong is expensive in a way a colour alone will not prevent.

**Right-align the ambient stuff** — live `mem: 10.0mb  cpu: 18.8%` (Gitwig,
croft), version strings, `^p palette`.

**Budget the footer.** Cronboard's thirteen-item key list runs off the edge
mid-word. When the list outgrows the width, demote to `? help` rather than
letting it wrap — and proof it, because Bagels ships `→ Shfit front`.

---

## 9. Overlays

### Command palette

Bagels: a full-width overlay from the top, a search input with a block cursor,
then two-line entries — the command bold with matched characters underlined, and
its description beneath. The selected row fills across both lines.

```
 ┌──────────────────────────────────────────────────────────┐
 │ the▌                                                     │
 └──────────────────────────────────────────────────────────┘
   theme: cobalt
   Set the theme to cobalt
 ▌ theme: dark
 ▌ Set the theme to dark
   theme: galaxy
   Set the theme to galaxy
```

Underlining the matched characters is what makes fuzzy matching feel intentional
rather than magic.

### Modal

Size it to its content, centre it, inset its title, and **put its own dismissal
key inside it**. `Press Enter or Space to continue` (ekphos), `Press '8' or Esc
to close` (moltbook), `esc cancel` (download manager).

Cronboard's modal is the one to avoid: it covers the whole app behind a
decorative dashed border, the underlying UI peeks through the margins, and
nothing in it says how to leave.

### Context menu

oxker floats a small action list beside the row it acts on, with `▶` marking the
cursor:

```
                                          ┌──────────┐
  postgres   √ running   Up 8 minutes     │  pause   │
  rabbitmq   ‖ paused    Up 34 minutes    │  restart │
  redis      ✗ exited    Exited (0)       │▶ stop    │
                                          │  delete  │
                                          └──────────┘
```

### Autocomplete with inline documentation

The MongoDB TUI shows the completion name highlighted with an italic description
beside it, so the list teaches while it completes:

```
 $regex             Selects documents where values match a regular expression.
 $regexWithOptions  Selects documents where values match a regular expression
 $rand              Selects a random document from the collection.
```

---

## 10. Identity

### Block-art wordmark

Common, and worth doing when there is room. coderabbit ramps colour across the
letters with a drop shadow; moltbook scales leaderboard names by rank so first
place is physically larger than fourth.

The constraint is real: Cronboard's wordmark renders as broken fragments at its
shipped size. Block art needs a minimum cell budget and a plain-text fallback
below it.

### Splash and help

The canonical help screen (kanha):

```
 ┌────────────────────────────────────────────────────────┐
 │  ██  ██  ▄▀█ █▄ █ █ █ ▄▀█   v0.1.2                     │
 │      Hacking in a nutshell                             │
 │                                                        │
 │  Usage:  kanha <COMMAND>                               │
 │  ──────                                                │
 │  Commands:                                             │
 │  ────────                                              │
 │    status     Just return the HTTP response code       │
 │    fuzz       Fuzz urls and return the response codes  │
 │                                                        │
 │  kanha ⑂                                        main   │
 └────────────────────────────────────────────────────────┘
```

Underlined section headings, a two-column command ladder with the command in
bold accent, version inline with the wordmark, tagline in italic.

### Stepper

The WorkOS installer, and the cleanest sequential-progress pattern in the corpus:

```
 ◇  Starting authentication...
 │
 ●  Open this URL in your browser:
 │    https://signin.workos.com/device
 │    Enter code: RGXX-CXVJ
 │
 ●  Browser opened automatically
 │
 ◐  Waiting for authentication...
```

A vertical rule with node glyphs: `◇` done, `●` sub-step, `◐` in progress
(a spinner shape). Free-form content indents between the nodes.
