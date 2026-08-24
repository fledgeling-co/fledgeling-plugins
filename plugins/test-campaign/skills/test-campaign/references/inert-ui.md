# The application that renders and does nothing

A campaign can report 8 of 8 surfaces drawn, 19 of 19 requirements cited, 8 of 8
external effects witnessed and 32 of 32 passing cases watched to fail — over an
application whose six menu items open one screen and whose every button runs an
empty handler. This file is the measured case, the three shapes it comes in, and
what the registry now counts so it cannot pass again.

## The measurement

24 August 2026, a monorepo shipping a Next.js web studio, a NestJS API, a native
macOS app and a native iOS app. The campaign's own verdict, pasted from the run:

```
Cases:      32 pass · 0 fail · 0 skip · 0 open  (of 32)
Observed:   32/32 cases produced a measurement · 0 could not be measured
Requirements: 19 inventoried, 0 with no case
Surfaces:   8 enumerated, 0 with no case
External effects: examined=8 witnessed=8 vacuous=0 unwitnessed=0
Armed:      32/32 passing cases have been watched to fail
Scope:      FULL — every case in the campaign was run
```

`reckon` over the same registry: 140 rows, 0 unmeasured, 0 unjoined, 0 broken, 0
unbuilt, `check` and `ratchet` both exit 0. The repository gate passed 19 of 19
tasks. 2,925 API tests, 156 Playwright specs, 264 TUI tests, 89 XCTest cases, all
green.

The owner opened the signed macOS build and reported three things in nine
minutes:

1. *"Every menu item on the left shows the same screen."* Six sidebar
   destinations, one placeholder detail view.
2. *"None of the buttons work — like Open Mock Folder, Pull Proof."* Every
   control was `Button("…") {}`, an empty closure.
3. *"I opened a folder and nothing happened other than a snackbar showing."* The
   panel opened, the banner said it had worked, and no folder was read.

Nothing in the campaign was false. `strict-check.py` was the only instrument that
said anything at all, and what it said was buried under a green verdict:

```
CHECKED   22 of 32 cases (69%)
UNCHECKED 10  — and unchecked is failed
    10  only proves something rendered
```

## Why each gate passed

Recorded per instrument, because "the tests were bad" is not a finding anybody
can act on:

| Gate | What it measured | Why the defect survived it |
|---|---|---|
| API and compiler suites (2,925 tests) | HTML/JSX lowered to SwiftUI AST, compiled with `swiftc -typecheck` | It proved the compiler emits valid navigation code. It never mounted that code in the shell app. |
| The campaign's native cases | `ProctorReflector`'s socket server, `CALayer` introspection, loopback accept logs | Three cases, all telemetry. None enumerated the sidebar, none clicked between destinations, none read a state a click was supposed to change. |
| Playwright (156 specs) | The web studio at `localhost:3170`, where the same screen matrix was wired and worked | The browser lane cannot reach a SwiftUI binary. Its green said nothing about the native target and read as if it did. |
| `mock_check.py`, `design-lint.py` | The HTML design of record: 3,630 contrast checks, 422 typography rules, 33 ARIA roles | The mock was compliant. Linting the reference proves nothing about the build. |
| `reckon` | The partition over cases, requirements, surfaces and briefs | It reconciles claims against evidence. It cannot tell a shallow assertion from a deep one; that is `strict-check.py`'s axis and it was not read. |
| The repository gate | `turbo run lint typecheck build` over the TypeScript packages | The macOS app builds through `xcodebuild`. An empty closure is valid Swift and compiles without a warning. |

The pattern across the row is one thing said six ways: **each instrument
correctly measured the thing it was pointed at, and none of them was pointed at
the shipped application's own controls.**

## The three shapes

### 1 · Destination collapse

A navigation shell offers N destinations and renders one view under every label.
It survives a surface census because the shell is enumerated as one surface and
its destinations are not enumerated at all, so the denominator reads `1/1`
instead of `1/6`. This is the skill's first failure mode — covering a subset and
reporting it as the whole — arriving through the navigation model rather than
through a route table.

**Detect it by identity, not by appearance.** Select each destination in turn and
read back something that must differ: the root view's type name or accessibility
identifier, the detail region's accessible name, the window's document title. Six
selections that return one identifier is the defect, stated as a count.

**A capture is the cheap version and it is exact.** Photograph each destination
and compare the bytes. Between two destinations of one menu, identical bytes are
never a legitimate share — that is what `campaign.py`'s `destinationOf` gate
reads, and it is the one place the duplicate-image rule refuses a declared share.

### 2 · The inert control

```swift
Button("Open Mock Folder…") {}
Button("Pull Proof") {}
```

This compiles clean, renders at the right size, carries `role=button` and its
accessible name, passes a contrast gate, appears in the accessibility tree, and
accepts a click without raising anything. Every check at `presence` and
`structural` passes on it. So does a screenshot comparison, because it looks
correct.

The AppKit and accessibility-tree (AX) version of the same shape, measured on a
different application: a suite asserted that 13 sidebar identifiers resolved, and
all 13 did — but the element carrying `sidebar.spend` was an `AXStaticText` with
an **empty actions list**. The identifier sat on the row's label rather than on
the control that owns the tap. Every assistive client could find every
destination and activate none.

```applescript
-- not enough
value of attribute "AXIdentifier" of e

-- what closes the gap
name of every action of e   -- must contain "AXPress" for anything interactive
```

**Detect it by actuating and reading a state outside the control.** Sweep C in
`sweeps.md` carries the browser mechanics. The rule that generalises: the
observable you read afterwards must be something the handler was supposed to
change, read back through a different channel from the one that struck. A
handler's return value, and the driver's own report that the click landed, are
both the actuation side of the vacuous assertion — `detector-defects.md` §11.
A `.jsx` or `.tsx` source read is not that channel either: source text says what
a component declares, never what rendered.

### 3 · The acknowledgement-only effect

The sharpest of the three, because the control is wired, the handler runs, and a
check that watches for *any* state change passes.

```swift
func chooseFolder() {
    let panel = NSOpenPanel()
    panel.canChooseDirectories = true
    if panel.runModal() == .OK {
        banner = "Opened \(panel.url!.lastPathComponent)"   // and nothing else
    }
}
```

The panel opens. The banner changes. The DOM signature moves. Nothing reads the
folder, no list populates, no counter updates. An oracle asserting on the banner
text is asserting on **the product's own report that it succeeded**, which is the
one observable guaranteed to exist whether or not the work happened.

**Detect it by refusing the product's own success message as the observable.**
For each control, name the state its handler is supposed to change and read that
instead: rows in the list, files parsed, bytes on the pasteboard, the sheet
presented, the request fired. Where a control's only promised effect genuinely is
a message, the case stands at `structural` rather than `outcome`, and says so.

## What the registry counts

Three optional fields, and absent means NOT DECLARED rather than clean, because a
census over an undeclared population is the empty-denominator failure this skill
already carries three instances of.

```jsonc
// inventory.json — surfaces
{ "id": "SURF-006", "label": "Workspace",
  "controls": ["Open Mock Folder…", "Pull Proof", "Copy Swift", "Export File"] }

{ "id": "SURF-007", "label": "Storyboards", "destinationOf": "SURF-006",
  "shot": "shots/storyboards.png" }
```

```jsonc
// cases.json
{ "id": "CASE-0033", "surface": "SURF-006", "req": "REQ-0009",
  "lane": "macos-glass", "oracle": "outcome",
  "actuates": ["Open Mock Folder…", "Pull Proof"] }
```

`campaign.py check` then refuses to clear on four configurations:

- **A surface declaring controls that no passing effect-rung case actuates.** A
  case below `outcome` that names an actuation has measured the click and not the
  effect, so it does not move the census.
- **A case actuating a control its surface never declared.** Without that, the
  denominator can be raised by naming controls nobody enumerated.
- **Two destinations of one shell publishing one identical image**, declared
  share or not.
- **A destination of a shell that no case reaches.**

And it prints two denominators every run, on a green verdict as well as a red
one: `Controls: 11 of 18 declared control(s) actuated`, and a per-lane row
carrying that lane's case count, passes, effect-rung passes, armed count and
oracle mix. The lane row is what makes a lane that was only ever checked on paper
visible while the campaign-wide mix still reads healthy.

## The limit, stated rather than left implicit

**A short `controls` list passes every gate above.** Nothing mechanical can know
that a surface offers eleven controls when its registry entry names four. The
instrument that can is the differential in `differential.md`: it reads the design
of record, which is the only source for "the build is missing a control", and no
amount of testing the build reveals what the build lacks. Where a surface has a
mock, take its control list from the mock rather than from the build.

**A lane with no effect-rung pass is reported and not blocked**, and the reason
is a measurement rather than a softening. On the campaign above, the native lane
*did* carry an effect-witness case — a loopback socket recorder — so a rule of
the form "every lane owes one effect rung" would have cleared it and the app
would still have shipped with six dead destinations. The rule that catches this
defect is the control census; the lane row is there because a zero in that column
is worth a reader's attention either way.

## Sources

- The campaign, the owner's three reports, and the per-instrument table:
  recorded 22–24 August 2026 against a four-target monorepo. The verdict blocks
  and `strict-check` output above are pasted from that run.
- The `AXPress` finding and the empty-actions-list measurement: the
  `acceptance-e2e` plugin's own
  `skills/acceptance-e2e/references/macos-ax-acceptance.md` (a different
  marketplace, not a file in this plugin), from a separate application whose 13
  sidebar identifiers all resolved.
- The actuation-side twin of the vacuous assertion, and the two shapes above it:
  `detector-defects.md` §11, §15 and §16.
