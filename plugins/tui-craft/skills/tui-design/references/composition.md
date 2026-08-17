# Composing a terminal screen

The spec is the easy half. This is the half that decides whether the screen is any
good, and most of it is decided before a single node is written.

## The medium gives you five channels and no type scale

A terminal has one font at one size. Every hierarchy problem the web solves with
`font-size: 24px` has to be solved here with something else, and the something
else is a short list:

**Weight** (bold, and dim as its opposite), **colour**, **position**, **spacing**,
and **the border**. That is the whole toolkit. Reverse video is a sixth, and
worth holding separately because it is the only one that survives every
degradation.

Two consequences follow immediately, and they are the difference between a screen
that reads and one that is merely correct:

- **Position is doing more work here than anywhere else.** A label at the top of a
  panel is a heading because of where it is, not because it is larger. So the
  layout carries the hierarchy, and a layout with everything at the same indent
  has no hierarchy regardless of how the colours are set.
- **You will run out of channels.** Five channels across focus, selection,
  category, severity, and emphasis means they collide. Deciding which channel
  belongs to which axis, once, at the start, is the single highest-leverage
  decision in a terminal design.

## Decide the role ladder before the layout

Write down every role and the one job it does, and make each rung genuinely
distinguishable from the next. Then check the ladder is a ladder: nothing meant to
be quieter than another is brighter than it.

This ordering is not a nicety. A palette assembled a token at a time, each one
looking fine on its own, is how `text-dim` ends up with more contrast than `text`.
Nothing looks broken; emphasis just quietly reads as recession, and the screen
feels wrong in a way nobody can point at. The `role-ladder` gate exists for that
one failure, and it caught it in this skill's own default theme: `border` was
chosen by eye at `#4C5464`, measured 2.44:1 against the dark surface, and was
below the floor an information-carrying line has to clear.

**Quiet ink is a real device, not a defect.** A dim timestamp beside a bright
message is doing hierarchy work the medium has almost no other way to do. So the
gate holds secondary roles to 3:1 rather than 4.5:1 and says so, instead of
deleting the only subtle channel a terminal has. What it will not accept is a role
carrying information below 3:1, which is decoration pretending to be text.

## The frame, and the size you are not designing for

Compile at the target size **and** at 80x24. A design that only works at 120x40 is
a design with an undisclosed requirement, and the compiler will tell you which
columns lose their content at the smaller one rather than leaving you to find out
from a user.

The reference corpus spans 640x376 to 2400x1600 and includes a near-square
640x600 and a 5.6:1 ribbon at 3000x540. Fixed-width layout assumptions do not
survive that range.

## Rails: per container, not per screen

Left-alignment discipline is the strongest compositional property in the corpus,
and it is **container-relative**. Each pane has its own left rail. Measuring first
ink across the whole screen conflates two panes into noise and reports a
two-column layout as sloppy for being two columns.

Within a container, few rails read as ordered and many read as scattered. In the
corpus, a typical screen has 86% of its content lines starting on one of three
rails. The compiler makes this a non-issue inside a table, because it solves the
columns; it stays your problem in free text, in nested indentation, and in
anything hand-built that you are comparing against.

A canvas app is the exception that proves it is a default and not a rule. A star
chart, a treemap or a plot has no rails by design and reads near zero. That is the
layout being spatial, not careless.

## The border is a shelf, not a fence

The strongest single move in the corpus. A panel border carries metadata at up to
three anchor points on the top rule and two more on the bottom:

- title on the left, state or sort in the centre, a count or version on the right
- a page indicator on the **bottom** rule, where a list's own footer would go

This buys a whole row of vertical space per panel and puts the metadata where the
eye already is, at the edge of the thing it describes. Observed in the corpus with
titles interrupting the rule and the rule resuming after, drawn far dimmer than
any text so the box recedes and the content does not.

One inconsistency to avoid, seen inside a single shipped app: two adjacent panels
where one title is centred and the other is left-aligned. Pick one and hold it
across every panel on the screen.

## Focus twice, selection so it survives

**Focus** gets at least two channels, because a terminal has no hover, no shadow
and no blur. Border and title; or border and a footer that changes to that pane's
keys. Every app in the corpus that reads clearly does this, and the ones that
signal once are the ones where you cannot tell which pane is live.

The best example in the corpus uses four channels at once for one state: the
column header turns accent, the selected item turns accent, the current value
takes an inverse fill, and a literal `>` sits beside it. Only the `>` survives
without colour, which is the point.

**Selection** needs a carrier that outlives colour. Colour is gone under
`NO_COLOR`, gone through a pipe, gone for a reader whose palette maps your index
somewhere unhelpful, and gone for anyone who cannot separate those two hues. The
carriers that work are a marker glyph in a gutter, reverse video, bold, or a
changed label. A background fill is not one: it is colour wearing different
clothes, and stripping colour removes it entirely.

**Selection outranks category.** When a row is selected, its cells' semantic
colours give way. Keeping both makes the row unreadable and makes the category
colour mean two things at once.

## Colour marks one axis

In the corpus's clearest tables, exactly one column carries category colour and
every other column stays neutral. That is what makes the coloured column scannable
at all. A table where four columns each carry their own colour scheme has no
emphasis anywhere.

Alongside the colour, put the word. `[OK]`, `[WARN]`, a green `●` *next to* the
text "Serving": the glyph and the colour are redundant with a label that carries
the meaning on its own. That redundancy is what makes the screen work in a pipe,
in a log, and for a screen reader.

## The capability ladder, and a real trade-off in it

Terminals differ in what they can render, and the rungs are: plain text → ANSI 16
plus box drawing → 256 colour → truecolour → inline graphics protocols. Design
for the rung you can guarantee and treat everything above it as enhancement.

There is a genuine tension here worth deciding deliberately rather than by
default:

- **ANSI 16 travels.** Using the standard indices means the app adopts the
  reader's own theme and looks native everywhere. The cost is that **you cannot
  guarantee contrast**, because the index is mapped by their palette, not by you.
  A great deal of the low contrast measured in the corpus is exactly this: an app
  emits `bright_black` for secondary text and someone's theme renders it nearly
  invisible.
- **Truecolour lets you hold a ladder.** Naming hex values means the contrast you
  measured is the contrast the reader gets. The cost is that the app ignores their
  theme and may clash with it, and truecolour needs negotiating (`COLORTERM`).

Neither is correct in general. Pick by what the screen is for: a tool whose job is
to be readable at a glance under pressure wants the guaranteed ladder, and a tool
that should feel like part of someone's terminal wants the indices. Whichever you
pick, say so in the design, and ship the other as the fallback rather than
discovering it later.

`NO_COLOR` set to any non-empty value means no colour, and it is checked first,
before any of this.

## The six states, drawn as six specs

A TUI has the same six states as any interface, and a mock that only holds the
ideal one is the most common way a terminal design fails late. Each state is its
own spec file, because that is the only way to know it fits.

The corpus's good states teach rather than report:

- The **empty** state names the action that fills it (`<ENTER> to view options`)
  rather than saying "no data".
- The **add** affordance is often a dim ghost row at the end of a table, not a
  button.
- A **placeholder** shows the format (`http://mirror1.com, http://mirror2.com`),
  not just the field name.
- An empty *value* renders an explicit token (`N/A`) rather than a blank, so the
  reader can tell "nothing" from "not loaded".
- A collapsed result carries its own expand hint and a running item its own
  interrupt hint, **at the item** rather than in the footer.
- Sequential work gets a stepper: a vertical rule with `◇` done, `●` current,
  `◐` in progress.

`ux-craft` owns this properly, including the trunk test and errors that say how to
fix. Load it before designing a flow.

## Density is a decision

The corpus runs from 6% to 96% of cells carrying a glyph, and both extremes are
apps people admire. There is no correct density and no gate on it here.

What separates good density from bad is whether the role ladder stays constant
across panels. A dense screen where `accent` means one thing in the left pane and
another in the right is unreadable at any density; a sparse screen with three
consistent roles reads immediately.

The `panel fill` measurement exists for the related but different case: a panel
sized for one data volume and shown another, where eight rows of content sit in
twenty-eight rows of border. That is not an error and has no threshold, but it is
worth seeing.

## Quieter containers than a border

A border is not the only way to group. The corpus uses all of these, and the
quieter ones scale better on a dense screen:

- **A lifted background fill** with no border at all, for code blocks and inset
  panels. `{ "fill": "surface-lift", "border": "none" }`.
- **A thin left rule in the gutter** with the text indented past it, for
  blockquotes and nested content.
- **Whitespace alone.** One corpus app groups an entire habit grid with nothing
  but spacing and reads perfectly.
- **A thick left accent bar** of one cell marking the active item, which is a
  gutter marker doing container duty.

Reach for a border when the group needs a title or a count, because that is what
the shelf is for. Reach for a fill or a gap when it does not.

## Where this hands off

The design is done when it compiles clean at both sizes, the enforced gates pass,
and the ruler dump reads correctly to you. What it is *not* is verified: no
composed frame says anything about a running program.

Hand the specs and the frames to whoever builds it. The frames were measured by
the same width function tui-craft's capture uses, so once the app runs, a
difference between the capture and the mock is a difference in the build rather
than in the arithmetic. That comparison is why the mock was worth compiling.
