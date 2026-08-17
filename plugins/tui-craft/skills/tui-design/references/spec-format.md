# The spec format

One file describes one screen in one state. It contains no column numbers, no row
numbers and no padding counted by hand, because the moment a spec contains
arithmetic it can contain wrong arithmetic. Everything positional is derived.

JSON always works. YAML works where `pyyaml` is installed and the schema is
identical; the compiler says so plainly rather than half-parsing a YAML file it
cannot read.

## Top level

```json
{
  "schema": "tui-design/spec/1",
  "title": "queuectl — dashboard",
  "size": { "cols": 100, "rows": 30 },
  "theme": "dark",
  "roles": { "accent": { "fg": "#6FC3E8" } },
  "alt_screen": true,
  "root": { }
}
```

| Field | Meaning |
|---|---|
| `size` | The frame. Compile every design at its target size **and** at 80x24. |
| `theme` | `dark` or `light`. Both ship and both were run through the gates. |
| `roles` | Overrides merged onto the theme. Add roles here; do not rename the built-ins, because the gates read some by name. |
| `alt_screen` | Recorded in provenance. Inline apps that leave output in scrollback set it false. |
| `root` | The layout tree. |

## Layout: containers and sizing

A container splits its region along one axis. That is the only positioning
mechanism there is.

```json
{ "dir": "row", "gap": 1, "children": [
  { "flex": 3, "panel": { } },
  { "w": 25,   "panel": { } }
] }
```

- `dir` is `col` (children stacked vertically, the default) or `row` (side by side).
- `gap` is cells between children.
- A child takes a **fixed** size with `h` (inside a `col`) or `w` (inside a `row`),
  or a **share** of what is left with `flex`. `flex` defaults to 1.
- Fixed sizes are honoured first and the remainder is divided by weight. The
  rounding remainder goes to the last flexible child, so children always sum to
  exactly the parent. A layout whose children sum to one cell short of their
  parent is how an unexplained one-column gap appears down the middle of a screen.
- Children that overflow their parent are reported as `fixed-children-overflow`
  rather than quietly clipped.

Containers nest freely. Any child may itself be a container.

## Nodes

Every leaf carries exactly one node key, and optionally `id`, which names it in
the region report and in gate findings.

### `panel`

A bordered box whose border carries metadata. The border is a shelf, not a fence.

| Field | Default | Notes |
|---|---|---|
| `title` | — | Left slot of the top rule |
| `shelf_centre`, `shelf_right` | — | Top rule |
| `shelf_bottom_left`, `shelf_bottom_right` | — | Bottom rule. A page count belongs here. |
| `border` | `single` | `single`, `round`, `double`, `heavy`, `none` |
| `border_role`, `title_role`, `shelf_role` | derived | Override the roles |
| `focus` | `false` | Switches border and title to the focus role and registers the panel with the `focus-channels` gate |
| `focus_marker` | — | Drawn before the title when focused. Counts as a channel only because it draws. |
| `fill` | — | A role whose `bg` fills the panel. A fill instead of a border is a quieter container. |
| `pad` | `1` | Cells between border and content. `1` is the default because content flush against its own border is the defect design review measures on the web. |
| `child` | — | One node |

Slots are laid out left, then right, then centre in what remains, each padded
with a space so it reads as sitting in a gap in the rule. A slot too wide for its
border is dropped and reported, because overlapping shelf text is worse than a
missing version number.

### `table`

Column widths are solved, not declared.

```json
{ "table": {
  "selected": 2,
  "selected_marker": "▸",
  "columns": [
    { "name": "WHEN",  "w": 8 },
    { "name": "QUEUE", "w": 10, "role": "accent" },
    { "name": "JOB",   "flex": 2 },
    { "name": "TRIES", "w": 5, "align": "right" }
  ],
  "rows": [["10s", "critical", "NotificationJob", "1"]]
} }
```

| Field | Default | Notes |
|---|---|---|
| `columns[].w` / `.flex` | `flex: 1` | Fixed, or a share of the remainder |
| `columns[].align` | `left` | `left`, `right`, `centre`. Left unless it holds numbers: a ragged right edge on text costs less than a ragged left edge on figures. |
| `columns[].role` | `text` | Give category colour to one column, not to all of them |
| `selected` | — | Row index |
| `selected_role` | `selected` | Which is `reverse` by default, so selection survives losing colour. `selected-fill` is the coloured bar. |
| `selected_marker` | — | Reserves its own gutter and shifts every column, rather than overwriting the first one |
| `header`, `header_rule` | `true` | |
| `gap` | `2` | Cells between columns |

A column narrower than its own widest cell is reported as `column-too-narrow`
with what it wanted and what it had. A selected row's cells take the selection
style, so category colour gives way rather than fighting it.

### `pairs`

Label and value on two rails, with the value rail computed from the widest label
so the values align by construction.

```json
{ "pairs": { "items": [["host", "wrk-01"], ["threads", "16"]] } }
```

`label_role` defaults to `text-dim` and `value_role` to `text-strong`. That way
round, not the other: the label is the part the reader already knows.
`value_rail` overrides the computed rail; `gap` (default 2) sets the space after
the widest label.

### `text`

```json
{ "text": { "lines": ["No queues yet.", "", "Press <ENTER> to add one."],
            "role": "text-dim", "align": "centre", "wrap": true } }
```

`wrap` measures in cells, because wrapping on character count is the same bug one
layer up: a line of CJK wrapped at 60 characters is 120 cells wide.

### `list`

`items`, `selected`, `marker` (default `▸`), `role`, `selected_role`, and `fill`
to give the selected row a background. The marker occupies a gutter that every
row shares.

### `chips`

A row of stat chips, each a label and a value in one container.

```json
{ "chips": { "style": "fill", "items": [
  { "label": "PROCESSED", "value": "1.4M", "role": "accent" },
  { "label": "FAILED", "value": "51.7K", "role": "danger" }
] } }
```

`style` is `fill` (one row, inverse-filled) or `border` (three rows, bordered).
Inside a chip the label is quiet and the value is not, which is what makes a row
of them scannable: the eye lands on four numbers rather than four words each
followed by a number.

### `keybar`

```json
{ "keybar": { "style": "bracket", "items": [["j/k", "move"], ["?", "help"]] } }
```

`style` is `chip` (`j/k move`) or `bracket` (`[j/k] move`). The key takes
`key_role` and the label `label_role`, always different, because a footer where
both are the same colour reads as prose. `fill` gives the bar a background.
Items that do not fit are dropped and reported with how many of how many were
shown, rather than running off the edge.

### `gauge`

```json
{ "gauge": { "label": "cpu", "value": 62, "readout": "62%", "role": "accent" } }
```

The bar is drawn **and** the number is written. A bar alone encodes its value in
length only, which a screen reader cannot linearise and a reader cannot read off
precisely. `max` defaults to 100; `glyph` and `track` set the filled and empty
characters.

### `blank`

A spacer. `{ "blank": {} }`, or `{ "blank": { "role": "surface-lift" } }` to fill
the region with that role's background.

## The built-in roles

Both themes define these, and the gates read several by name.

| Role | Job |
|---|---|
| `surface`, `surface-lift` | The ground, and a lifted plane for code blocks and inset panels |
| `text` | Body |
| `text-strong` | Emphasis. Bold. |
| `text-dim` | Secondary. Allowed the 3:1 floor rather than 4.5:1. |
| `border`, `border-focus` | Rules, and the focused variant |
| `accent` | The one colour that means "this" |
| `ok`, `warn`, `danger` | Semantic state |
| `selected` | `reverse`, so it survives colour loss |
| `selected-fill` | The coloured selection bar, when you want it and have a marker too |

Any role name containing `dim`, `muted`, `subtle`, `faint`, `ghost`, `border`,
`rule` or `track` is treated as quiet by the `role-ladder` gate and held to 3:1
instead of 4.5:1. Naming a role `label` does not make it quiet, which is why the
failing fixture's `label` role fails at 1.82:1.

## The fit report

Anything that did not fit comes back on stderr, and a non-zero exit follows. Each
finding names where and what it wanted:

```
{"kind": "column-too-narrow", "column": "JOB", "wanted": 22, "had": 14}
{"kind": "shelf-too-wide", "row": 2, "where": "right", "wanted": 30, "had": 24}
{"kind": "truncated", "row": 7, "col": 12, "where": "table:cell", "wanted": 31, "had": 18}
```

`zwj-width-ambiguous` is the one that cannot be fixed by resizing. A ZWJ sequence
is one double-width glyph in a terminal that composes it and its separate parts
in one that does not, a four-cell difference on a family emoji, and no width
function can say which the reader will get. Reserve the uncomposed width or use a
single-code-point glyph.
