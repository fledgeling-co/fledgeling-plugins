# Campaign methodology

The campaign shape is in `SKILL.md`. This is the depth underneath four of its
stages: what the state matrix actually contains, what the accessibility rubric
measures and against what thresholds, how the fidelity ledger works, and what
the resulting report has to disclose about how it was produced.

---

## The state matrix

A state matrix is a coverage contract. Its value is not that you run every
cell — you will not — but that every cell you did not run is visible as a cell
you did not run, rather than absent from the document entirely.

### Content states

These are properties of the data the app is showing. They are the axis that
breaks layout, and they are the axis a developer is least likely to have seen,
because a developer's machine has one plausible amount of data in it.

| State | What it means | What it typically breaks |
|---|---|---|
| Empty | Zero items, first-class | Missing empty state; a table header with no body; a disabled action that should be hidden |
| One | Exactly one item | Pluralisation; a "select all" that makes no sense; a divider drawn after the last row |
| Few | A handful, no scrolling | Rarely breaks anything; this is the state everything was built in |
| Many | Enough to scroll | Scroll position on refresh; virtualised rows that never mount; a footer that scrolls away |
| Maximum | The documented or enforced ceiling | Counters that overflow their label; a "add" control that stays enabled at the limit |
| Overflowing | Content longer than its container — a 200-character name, a very long URL | Truncation with no tooltip; a label that pushes a control off-screen; a tree that stops being readable |
| Loading | Between request and response | A spinner that never clears; controls live during load; a settle that reports quiet mid-fetch |
| Stale | Data that is real but out of date | No indication it is stale; a refresh that silently does nothing |
| Error | The request failed | A raw error string; no retry; an error that replaces content rather than annotating it |
| Offline | No network at all | An error styled as an empty state; a retry that queues forever |
| Permission denied | The OS or the backend refused | A dead-end with no route to the setting that fixes it |
| First run | Nothing configured yet | Onboarding that assumes state it has not asked for; a window sized for content that is not there |
| Restored session | Relaunched into a saved state | State restored partially; a window restored to a display that is gone; selection restored to a deleted item |

Forcing them is the app's problem, not the server's. Most are reachable through
the app's own affordances — create items, delete them, disconnect the network,
revoke a grant, delete the preferences file for first run. Where a state is not
reachable, say so: an unforced state is an unrun cell.

### Environment states

These are properties of the machine, not the app. Nothing in the tool surface
sets them; they are changed in System Settings, with `defaults write`, or by
resizing and moving a window with `proctor_act`'s `resize` and `move` steps.
Change the setting, then re-read — the attachment survives a setting change, so
there is no need to re-attach and no reason to throw away the retained
references. A change that requires relaunching the app is the exception: after
a relaunch the handles are dead and you attach again.

| State | How it is set | What it typically breaks |
|---|---|---|
| Light / dark | System Settings > Appearance | Hard-coded colours; an image asset with a baked background; contrast that passes in one mode only |
| Increased text size | System Settings > Accessibility > Display | Clipped labels; a fixed-height row; a two-column layout that should reflow |
| Reduced motion | System Settings > Accessibility > Display | An animation that still runs; a transition that was the only feedback for a state change |
| Reduced transparency | Same panel | Illegible text over a now-opaque material; a divider that was doing the work of a border |
| Increased contrast | Same panel | Borders that appear and change layout; a focus ring that now collides with adjacent content |
| Narrow window | `proctor_act` `resize` | Overlapping controls; a toolbar that drops items with no overflow menu; a minimum size that is not enforced |
| Second display | Physical or a second monitor | A window restored off-screen; a sheet centred on the wrong display; backing-scale differences between displays |
| Non-English locale | System Settings > Language & Region, then relaunch | Layout built for English string lengths; a date or number format that breaks parsing; a title-matched selector that no longer matches |
| Right-to-left | An RTL locale, or `-AppleTextDirection YES` | Mirroring that did not happen; a chevron pointing the wrong way; focus order that follows the old visual order |

### Interaction states

Properties of a single control rather than the window. These are the cheapest
to cover and the most often skipped, because the happy path only ever shows
`default` and `pressed`.

`default`, `hover`, `focused`, `pressed`, `disabled`, `selected`, `dragging`,
`keyboard-only`.

Three of these need the synthetic-event plane and so need the app in the
foreground: `hover` (there is no accessibility action for "the pointer is over
this"), `dragging` (a `dragPath`), and the pointer half of `pressed`. `focused`
and `keyboard-only` are reachable process-directed, by writing `AXFocused` or
by a `key` step with `tab`. `disabled` and `selected` are read, not driven —
they are the `enabled` and `selected` fields on the node.

`keyboard-only` deserves its own pass rather than being treated as a variant of
`focused`: it asks whether every action in the window can be reached without a
pointer at all, which is a question about the whole window and not about one
control.

### Which crossings are worth it

Crossing all three axes gives 13 × 9 × 8 cells and would be theatre. Cross two
states when they contend for the same resource, and treat them as independent
otherwise. There are three resources worth thinking about.

**Space.** Cross content states that produce a lot of content with environment
states that reduce the room for it. Overflowing × increased text size,
many × narrow window, maximum × increased text size, overflowing × non-English
locale. These are where the real layout defects live, because each axis alone
leaves enough slack to hide the problem and together they do not.

**Colour.** Cross states that introduce a distinct colour treatment with the
appearance settings. Error × dark, disabled × increased contrast, selected ×
increased contrast, permission-denied × dark. An error state is where hard-coded
colour survives longest, because it is the screen nobody opens in dark mode.

**Timing.** Cross states with a duration against the motion settings.
Loading × reduced motion, and loading × any state you can interrupt. Reduced
motion is where a transition that was the only feedback for a change turns into
no feedback at all.

Everything else is one axis at a time. Empty × dark mode is a cheap cell and
worth running once, but empty × dark × increased text size is not a third
finding — it is the same background colour checked three times.

Record the matrix as cells run and cells not run, with the reason for each
omission. A matrix that implies it was fully run is worse than no matrix,
because it converts an unknown into a false assurance.

---

## The accessibility rubric for macOS

Four of the assertion kinds — `hasLabel`, `contrast`, `minHitSize`,
`focusOrder` — line up with the categories Apple's own audit checks
(`XCUIAccessibilityAuditType`: `.sufficientElementDescription`, `.contrast`,
`.hitRegion`, and the element-detection and trait categories around them). That
alignment is deliberate: a finding phrased in Apple's own audit vocabulary is a
finding a developer can act on without translation.

### What a well-behaved control exposes

An AppKit or SwiftUI control that has adopted accessibility properly presents,
through `proctor_snapshot` or `proctor_find`:

- A **role** that describes what it is (`AXButton`, `AXCheckBox`, `AXTextField`,
  `AXSlider`), and a **subrole** where the role is ambiguous.
- A **title** or a **label** (AXDescription) that names it in human words. A
  control whose visible text is its name carries a title; a control that is
  icon-only carries a label, because there is no visible text to serve.
- A **value** where it has one, and a **roleDescription** where the standard
  role name would mislead.
- Live **state**: `enabled`, `focused`, `selected`.
- **Actions** it can perform — at minimum `AXPress` on anything pressable.
- **Writable attributes** where a value can be set rather than typed.
- An **identifier** (AXIdentifier), where the developer set one.

Two things about that list are worth stating plainly. First, `actions` is the
field that separates a control from a picture of a control. A node with the
right role and no actions cannot be operated by anything on the accessibility
plane, which includes both this server and every assistive technology.

Second, a custom `NSView` that draws itself and adopts nothing appears as a flat
`AXGroup` or `AXUnknown` with no children, no actions and no label — under a
region that clearly contains several controls. That flatness is the signature,
and it is both a finding to report and a hard limit on what the rest of the
campaign can test in that region.

### AXIdentifier is a selector, not a name

`accessibilityIdentifier` exists to let a test address an element without
depending on its wording. It is not surfaced to users and is excluded from
localisation, which is exactly what makes it durable: it survives a copy change,
a translation and a design pass.

The anti-pattern Apple names directly is putting a machine string
(`QUOTE_TEXTVIEW`) in the *label* so that a test can find it — which makes
VoiceOver read out a symbol name and couples the accessibility surface to the
test suite. When a campaign finds a label that reads like an identifier, the
finding is "move this string to the identifier", not "rename the label".

An app with no identifiers anywhere is not a defect, but it is a constraint
worth reporting, because every selector the campaign wrote is then a title match
and the whole suite is one wording change from failing.

### What an unlabelled `AXButton` costs

A VoiceOver user reaches an unlabelled button and hears "button". Not what it
does, not what it affects — the role and nothing else. The only way forward is
to activate it and find out, which for a destructive control is not a
reasonable thing to ask of anyone. Where several unlabelled buttons sit in a
row, they are mutually indistinguishable and the user is navigating by counting.

It costs the campaign too: an unlabelled node has no title, no label and
usually no identifier, so there is no stable way to address it, and any flow
that touches it has to select it by position — which is the least durable
selector there is.

`hasLabel` treats a node as labelled when it carries a title, a label, or a
value that serves as its name. Run it with a `find` predicate scoped to
interactive roles rather than across the whole tree; a decorative group has no
obligation to be named, and reporting it as a failure buries the three buttons
that matter.

### Contrast thresholds

Apple does not define its own contrast formula; it points at the W3C ratio and
recommends a minimum of 4.5:1 between foreground text and its background, which
is also the App Store Connect "Sufficient Contrast" bar for text, buttons and
controls in common tasks. The two thresholds to assert:

| Content | Ratio | Basis |
|---|---|---|
| Body text | 4.5:1 | WCAG 1.4.3 Contrast (Minimum), AA — the level Apple's guidance cites |
| Large text (roughly 18pt, or 14pt bold and up) | 3:1 | Same criterion, large-text allowance |
| Non-text UI — a control boundary, a checked/unchecked distinction, a focus ring | 3:1 | Non-text contrast; the state distinction is the thing being measured |

Logotypes, incidental text and inactive controls are exempt. Assert contrast in
both appearances and, where the app is being audited seriously, with increased
contrast on as well — meeting 4.5:1 in light mode and missing it in dark is the
common shape, because dark mode is where grey-on-black gets chosen for its
looks.

`contrast` reads pixels, so its measurement is of what reached the display,
after compositing and the display profile. That is the right thing to measure
for this question — a user reads pixels, not declared colours — but it means a
value very near the threshold is near the threshold *on this display*, and
should be reported with its measured number rather than as a pass.

### Hit-target minimums

WCAG 2.2 SC 2.5.8 sets 24 × 24 CSS pixels as the AA floor, with an exception
where undersized targets are spaced so that 24-unit circles centred on each do
not intersect; SC 2.5.5 sets 44 × 44 as the enhanced bar. On a pointer-driven
platform the 24-unit floor is the defensible assertion and 44 is the aspiration,
so `minHitSize` with `expected: 24` is the gate and anything under 44 is worth
a note rather than a failure.

Measure the *hit region*, not the drawn glyph. A 16pt icon inside a 28pt button
passes; a 16pt icon that is its own hit region does not. The node's `frame` is
what `minHitSize` compares, which is why a control drawn small inside a
generous parent needs the parent to be the accessible node — and when it is not,
`agree` reports it as `hitTargetMismatch`.

### Focus order against visual order

Focus order should follow the reading order of the content: in a left-to-right
locale, left to right and top to bottom; in a right-to-left locale, mirrored. A
focus order that jumps — a sidebar, then a footer, then back to the toolbar —
is disorienting for a keyboard user and unusable for someone who cannot see the
jump happen.

`focusOrder` compares the tab traversal against the node frames, so it is
measuring the relationship the criterion actually names rather than checking a
declared order. Two cases produce a legitimate-looking failure worth reading
carefully: a modal sheet, where focus should be trapped and the order inside it
is the only order that matters, and a toolbar that is deliberately reachable
only through a keyboard group. Both are worth checking against intent before
reporting.

Run this pass in an RTL locale too where the app claims RTL support. A window
that mirrored its layout and did not mirror its focus order is a specific,
common defect that neither pass finds alone.

---

## The fidelity ledger

Adapted from `mockup-fidelity`, and what is taken is its central discipline:
**breadth before depth, with the burden of proof inverted** — every element of
the reference gets a row marked present, divergent or absent before any property
is measured, and a difference stays a defect until an external citation proves
it intentional.

### The ledger

One row per element of the reference, per surface. Three states:

- **Present** — the build has it, and it matches. Earned by measuring the
  element, never inferred from purpose. A control that does the same job under a
  different label, or a bordered button rendered as a bare text link, is
  divergent rather than present.
- **Divergent** — present, but wrong in place, size, style or content. Recorded
  with both measured numbers.
- **Absent** — the reference has it, the build does not.

The fourth category the reference cannot generate is **extra**: something the
build renders that the reference does not. Enumerate those per region by reading
the build's children against the reference's, element for element. They are
divergences too — especially when an extra element displaces a real one.

### Divergences carry numbers, not adjectives

"The button is a bit small" is not a ledger row. `28 × 22 pt against 32 × 28 pt
in the reference` is. The reason is that a measured divergence is actionable
without a second conversation and can be re-checked mechanically after a fix,
where an adjective needs the same person to look again and agree with
themselves.

Where the build embeds `ProctorReflector`, the numbers come from
`proctor_inspect` and are resolved values — the colour the code produced, the
corner radius the layer holds, the font actually in use. Where it does not,
geometry comes from the accessibility tree's frames and appearance comes from
pixels, and a style row says which. A colour read from a PNG is a colour after
compositing and the display profile; report it as a measurement of the render,
which is what it is.

### The burden of proof

A difference is a defect until a citation proves otherwise, and a citation is
**external and pre-existing**: a ticket, a spec line, a code comment that
predates the audit and matches reality, a recorded product decision, or a
platform rule the reference violates. A reason you composed during the audit to
explain why a difference is acceptable is not a citation — it is the
rationalisation the inverted burden exists to catch.

Native chrome is the one standing exemption on macOS, and it is narrow. A real
native window's traffic lights, its title bar, a system sheet, a standard
toolbar and the menu bar are correct as the platform draws them, and a mock's
hand-drawn versions of those are not a target. Everything inside the content
area is in scope, and a header the app draws is content.

---

## Native conformance

The fidelity ledger answers *does the build match its design*. A different
question sits next to it — *is the build a correct, native Mac app* — and it
needs no mockup, because the platform is the reference. This is the pass that
covers "ui/ux design tests" for an app that was never given a design of record,
and it is where a build that renders cleanly and passes every accessibility
assertion can still be quietly wrong for macOS.

The rubric is `mac-design-studio`'s `references/native-foundation.md`, and the
numbers behind it are the macOS 27 UI kit and the HIG in `macosify`'s
`reference/`. Do not restate them here; read them there and measure against
them. What Proctor contributes is the measurement: the rendered accessibility
tree carries roles, frames and font attributes, and the captures carry pixels,
and both can be checked against the ladder rather than eyeballed.

The conformance defects worth naming, each measurable from the tree or a
capture:

- **Off the control ladder.** A control whose height is not a kit tier — a
  27pt push button where the ramp says 21 or 32 — reads as almost-native, which
  is worse than obviously custom because nobody notices to fix it.
- **Off the type ramp.** Body text that is not 13pt, a title that lands between
  two roles. Read the font size from the node where the reflector is present,
  or measure cap height from a capture where it is not.
- **The 8pt grid, broken.** Padding and gaps that are not multiples of the grid
  unit, caught by differencing sibling frames.
- **Liquid Glass without discipline.** A floating panel or toolbar with no
  scroll-edge treatment where content meets chrome, or the material used on a
  surface that is not floating chrome at all.
- **Non-native tells.** Tracked-uppercase section labels, a full-width busy
  gradient, a card grid with iOS-sized corner radii — the tropes
  `mac-design-studio`'s ten-point audit and `design-craft`'s `ai-slop-check`
  enumerate. Each is a finding phrased in the platform's own vocabulary, which
  is what makes it actionable.

The judged half of the question — whether the result is *good*, not merely
conformant — is `design-review`'s, with the captures attached. Conformance is
measured here; craft is judged there; and an app can pass one while failing the
other, which is exactly why they are two passes and not one.

---

## Disclosure requirements

Four things go in the report's methods note. Each exists because a reader who
does not know it will over-read the result.

**Whether `AXManualAccessibility` was applied, and to what.** Read it from the
attachment's `provenance.manualAccessibilityApplied`. Chromium and Electron
build no full accessibility tree until a client asks for one, and the flag that
asks is detectable by the app: Electron surfaces assistive-technology presence
to application code, and the equivalent flag on AppKit windows is documented to
change window-management behaviour. So the app under test was observed in a
configuration real users do not run, with a different code path and a different
performance profile. A finding measured under that observer effect is still a
finding — a missing label is missing either way — but a timing finding, a
smoothness finding, or anything about responsiveness is a finding about the
instrumented app, and saying so is the difference between a methods note and a
misattribution.

**Which settle signals were available.** Read them from each step's
`settle.signals` and `settle.reason`. There is no native equivalent of the
browser's virtual-time control on macOS: Core Animation timing runs in an
out-of-process render server on the system clock, with no supported hook to
slave it to a test clock. Determinism here is engineered from settle signals and
per-step hashing, not enforced by the platform, so a settle is a conjunction of
heuristics and its strength varies by what was available. A campaign where every
step settled on `captureQuietOnly` is a campaign with one observer, and a reader
comparing it against one where the app's own idle endpoint answered should be
able to see that difference without asking.

**Which captures came back untrustworthy.** Read it from
`CaptureResult.trustworthy` and `caveat`. A stale frame is pixel-identical to a
fresh one, which means the freshness metadata is the only thing separating them
and a reader looking at the PNG cannot recover it. Listing the untrustworthy
captures, and saying what you did instead — raised the window and re-captured,
or dropped the claim — lets a reader tell a visual claim resting on a verified
frame from one resting on a frame that arrived when the compositor felt like
sending one.

**Whether a reflector was embedded.** Read it from
`DoctorReport.attachedApps[].reflectorConnected`. There is no cross-process
computed-style API on macOS — every richer mechanism requires code injection
into the target, which hardened runtime and Library Validation block on
notarised apps. For an app without an embedded reflector, style claims rest on
pixels and geometry claims rest on accessibility frames, and neither is the
declared value. Stating this stops a colour in the report from being read as a
value someone can grep the source for.

---

## What a campaign cannot establish

**Anything below the accessibility layer in an app that never adopted it.** A
custom view that draws its own controls and exposes nothing presents as a flat
node with no children and no actions. The campaign can report that it is
unexposed, and can capture pixels of it, and `agree` can report a control-shaped
region with no node behind it. It cannot read the control's state, drive it
process-directed, or say whether it is correct. There is no route around this
for an app you do not own: the mechanisms that would reach it require injecting
code into the target, and that is exactly what the platform blocks.

**Timing behaviour under real load.** Every timing number the campaign produces
was measured on an instrumented app, usually with the accessibility tree forced
on, on a machine doing nothing else, with settle waits between steps that a user
does not take. `elapsedMs` is useful for comparing one run against another under
the same conditions, and for spotting a step that got dramatically slower. It is
not a latency measurement and should not be reported as one.

**Anything that needs a second physical machine.** Cross-machine sync, handoff,
a licence check that behaves differently on a second install, a document open in
two places. Apple silicon caps concurrent macOS guests at two per host in the
kernel, and lifting it requires disabling SIP, so a VM fleet does not
substitute. Parallelism within one session comes from driving many windows
process-directed, which does not contend for focus — real parallelism past that
is a hardware purchase.

**Rendering that both observers agree on and that is nonetheless wrong.** The
tri-observer check finds disagreement. When the tree says "Submit", the layer
says the button is where the tree says it is, and the pixels show a button
reading "Submit" — and the label should have said "Pay £40.00" — every observer
agrees and every one of them is wrong. The same holds for a correct-looking
chart plotting the wrong series, a date formatted correctly in the wrong
timezone, and a total that renders beautifully and does not add up. These are
correctness questions about content, and they are answered by the acceptance
criteria the flows assert against, not by any amount of observation. Where a
criterion did not exist, the campaign did not test it, and the honest place for
that is the report's "not covered" section.
