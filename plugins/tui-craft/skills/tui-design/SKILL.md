---
name: tui-design
description: Design and mock terminal user interfaces before the app exists, as a compiled cell grid rather than ASCII art in a code block. Use whenever someone asks to design, lay out, mock up, wireframe, sketch, propose or rethink a terminal UI — a dashboard, log viewer, installer, wizard, file browser, admin panel, data browser, or a CLI being turned into a full-screen app — and whenever they ask what a TUI screen should look like, how to lay out panels at 80x24, which colours or roles to use, how to signal focus or selection, or want two layout options compared before any code is written. Also use when handed a hand-drawn terminal mock to check, when a design needs to be proved to fit at a given size, or when someone asks whether a terminal layout is any good. Compiles a declarative spec into a real cell frame so the compiler does the width arithmetic, then runs design gates on it — role ladder, colour-independent state, focus channels — plus tui-craft's arithmetic gates. Hand the finished design to tui-craft to build and capture. Not for web or desktop GUI work.
---

# tui-design

You cannot capture a screen that does not exist yet, and that is the whole
problem this skill has that `tui-craft` does not. Its instrument reads a running
program. Before there is one, the only artifact is a proposal, and the usual way
of writing that proposal is a terminal layout drawn by hand in a fenced code
block.

That drawing is almost always wrong, for a mechanical reason rather than a
careless one. Drawing it means counting characters, and characters are not cells.
`len("🚀 Deploy")` is 8 and it occupies 9. One wide glyph puts every column after
it off by one, the border does not close, and the mock looks perfectly fine in
the message that produced it, because nothing in that message measured anything.
The same arithmetic fails the same way on CJK labels, on box-drawing runs, and on
any string a combining mark passes through.

So the mock stops being a drawing. You declare what the screen contains and how
it divides, a compiler does every piece of cell arithmetic, and what comes out is
a real frame in tui-craft's schema that its gates read directly.

## The line between this skill and tui-craft

The split is **author versus instrument**, not "does a program exist yet". Both
skills work on the same frame type and the distinction is what a frame may be
used to claim:

- A **composed** frame (`kind: "mock"`) supports claims about the *design*: what
  it occupies at this size, whether its roles form a ladder, whether its
  selection survives losing colour, whether its columns fit their content.
- It supports **no claim about a running program**. Not that the app draws this,
  not that a bug is fixed, not that a screen is ready. Those need a capture, and
  tui-craft owns them.

This does not put a hole in tui-craft's rule that a claim about a screen needs a
captured frame. It keeps it: a composed frame is evidence about a proposal, and a
proposal is not a screen.

`tui_gates.py` already prints an advisory when handed a mock. That advisory is
correct and should not be argued with.

## The loop

**1. Decide before you draw.** Two sizes at minimum: the one the app is for, and
80x24, which is the floor that still exists everywhere. A design that only works
at 120x40 is a design with an undisclosed requirement. Decide the six states you
will need too, because a layout that only holds the ideal state is the most common
way a TUI design fails late.

**2. Write the spec.** JSON (or YAML where `pyyaml` is installed; the schema is
identical). It contains no column numbers anywhere. Full node reference:
`references/spec-format.md`.

**3. Compile.**

```bash
python3 scripts/tui_mock.py spec.json -o frame.json --dump
```

The `--dump` is a character matrix with column rulers, and it is the artifact to
read rather than a rendered picture: misalignment that an image hides is obvious
against a ruler. `--ansi` paints it into the terminal when you want to see it in
colour. Anything that did not fit comes back as a **fit report** on stderr, and
the exit code is non-zero when there is one. Those are the findings a hand-drawn
mock cannot produce: a column narrower than its own content, a shelf label too
wide for its border, a panel whose fixed children want more room than it has.

**4. Gate the design.**

```bash
python3 scripts/tui_design_gates.py frame.json --strict
```

**5. Gate the arithmetic**, with tui-craft's own gates, on the same file:

```bash
python3 ../tui-craft/scripts/tui_gates.py frame.json
```

**6. Read the dump and fix.** Ask it *"what is wrong with this?"* rather than *"is
this done?"* — the same grid answers those two questions differently.

**7. Hand it over.** The frame and the spec go to whoever builds it, and from
that point tui-craft's loop applies: build, capture, gate, compare the capture
against this frame. The comparison is the payoff. Both sides were measured by the
same width function, so a difference between them is a difference in the build
rather than in the arithmetic.

Batch it: compile every state and size in one round, fix what the round surfaces,
confirm with one more round, stop.

## What the gates enforce, and what they only report

The split matters more than any single rule. **Enforced** checks can fail a
frame, and each one is a principle about how information has to be carried.
**Reported** measurements have no pass mark and are printed with their
denominators.

| Enforced | The rule |
|---|---|
| `role-ladder` | Every role carrying information clears 3:1; roles the reader must read clear 4.5:1; and no role meant to be quieter than another out-contrasts it |
| `state-carrier` | A row distinguished from its siblings stays distinguished when colour is removed |
| `focus-channels` | A focused element differs on at least two channels |

| Reported | Why it is not a gate |
|---|---|
| role budget | Both ends of the corpus range are apps people like |
| rail discipline | A canvas app has no rails by design and should read low |
| panel fill | Dead space is usually a data-volume mismatch, not an error |
| chrome share | A border that carries titles and counts is earning its cells |

**Nothing measured from the reference corpus is a fail threshold.** That is a
correction rather than caution. The corpus is 48 shipped applications, and 27 of
its 34 colour-measurable frames carry at least one glyph role under 3:1. Its
median of 5.5 chromatic roles describes a habit. A habit turned into a gate fails
good screens for being unusual and passes bad ones for being typical, so the
numbers appear as context beside the result and the pass marks come from
principles instead. `references/evidence.md` carries the figures, how they were
measured, and the three places the measurement cannot reach.

Two of the enforced gates report `examined=0` on a captured frame, and say why.
That is honest rather than broken: a real capture carries ANSI names or
`default`, which resolve only in the reader's own palette, so a ladder is
genuinely unmeasurable from it. `examined=0` is never a pass.

`assets/example-failing.json` exists to be run. It fails all three enforced
gates on four planted defects, which is how you confirm the gates can fail before
trusting one that passes.

## Deciding the design, not just typing it

The spec is the easy half. `references/composition.md` is the method, and these
are the parts that most change a screen:

- **A terminal has one font at one size**, so the hierarchy toolkit is weight,
  colour, spacing, position and the border. There is no type scale to lean on.
  Anything that would be solved with 24px on the web is solved here with
  position and a rule.
- **Design the role ladder before the layout**, and give each role a job you can
  name. A palette assembled a token at a time is how `text-dim` ends up brighter
  than `text` and the hierarchy silently inverts.
- **Put metadata on the border.** A panel border carries a title on the left, a
  state in the centre, a count on the right, and a page indicator on the bottom
  rule. It buys a row of vertical space per panel and puts the metadata where the
  eye already is. `shelf_right` and `shelf_bottom_right` do this.
- **Signal focus twice**, because a terminal has no hover, no shadow and no blur.
  Border and title; or border and a footer that changes to that pane's keys.
- **Colour marks one axis, not everything.** In the corpus's clearest tables
  exactly one column carries category colour and the rest stay neutral.
- **Selection outranks category.** When a row is selected, its cells' semantic
  colours give way rather than fighting the selection.
- **Reach for `reverse` over a coloured fill** for selection. Reverse video is an
  attribute the terminal applies, so it survives `NO_COLOR`, a pipe, and a
  reader's unhelpful palette. A background fill is colour wearing different
  clothes.

`ux-craft` and `design-craft` are standing dependencies rather than optional
extras. **`ux-craft`** owns the flow, the six states, the trunk test, errors that
say how to fix, and destructive-action friction; load it before designing a flow.
**`design-craft`** owns hierarchy, restraint and the anti-slop pass; its visual
rules transfer and its typographic ones do not. Where either is unavailable, say
which substitution you made.

## Two limits worth knowing before they waste your time

Both were found by running this skill's output through tui-craft, and neither is
a defect in the design being reviewed:

- **`border-integrity` reports a false positive on stacked panels.** Two panels
  in one column separated by a gap row produce a border column with a hole in it,
  and the gate reads the hole as a box that does not close. Verified: the row
  above closes with `╰───╯` and the row below opens with `╭───╮`. Either accept
  the advisory or set `gap: 0`.
- **`tui_capture.py` reports `kind: "captured"` for a command that does not
  exist.** Capturing a missing binary yields a frame holding
  `/bin/sh: foo: command not found`, 28 ink cells, and exit 0. Check the ink
  count and the first row of any capture before gating it.

## Scope

Deliver what was asked, at the scope intended. A request for one screen is one
screen; the states and sizes are part of that screen, and a second unasked-for
feature is not. Make routine calls yourself and check in only where two readings
would produce materially different work.

Delegate to a subagent only for a genuinely large independent track, such as
specs for many screens of one app that do not share a layout. Compiling and
gating a spec is a script run, so do it directly.

Keep the reply short: the outcome, what the gates said with their denominators,
and what is open. Show the ruler dump when the layout is the point. Match a
written deliverable to what the task needs and stop.
