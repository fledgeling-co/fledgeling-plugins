# iPhone Duo reference screens — witness findings

Reviewed with `be-my-witness:be-my-witness` on 2026-10-11. Source: 34 captures the owner supplied
(Apple's own apps on iPhone Duo: Safari, Settings, Mail, Reminders, Notes, Health, Music, Fitness,
App Store, Maps, Pages), from the Tech Talk videos and the Xcode 27.1 Device Hub.

A larger set followed on 2026-10-29: 313 captures of 38 apps on a real device, open and closed, in
`device-captures.md`. It has no book, tabletop, Split View or picture-in-picture frames, so the rows
below remain the only record of those poses. Where the two sets cover the same thing, the device set
adds measurements: flat, lists are a fixed column near 320pt (D01), and sheets centre on the fold at
653pt (D04).

## Verdict

```json
{
  "gate": "inconclusive",
  "comparedAgainst": [],
  "coverage": { "regionsInspected": 32, "regionsInReference": 34,
                "uninspected": ["#16 blank capture (2x4 px, prescan isEvidence=false)",
                                "#26 a Mac desktop, not an iPhone Duo surface"] },
  "conformance": { "basis": "none — reference evidence, not a candidate under test", "advisory": true }
}
```

No expected output and no mock: these screens are exemplars to learn from, not a build to grade, so
the gate is `inconclusive` by construction and every row below is an observation, not a defect.
Prescan: 33 of 34 are evidence; #2 (Safari tab search) failed `settled` because its background is
deliberately blurred, not loading. #27 duplicates #28 (the same Music frame in QuickTime). The six Mail
poses in #14 were cropped and read at 2x (`p1`–`p6`).

## Observations, by pose

| # | Pose | App | What the screen shows | Pattern |
|---|---|---|---|---|
| 14·p1, 15, 21, 29 | Closed, portrait | Mail, Music | Back, navigation and actions stand in one column on the right; status bar and camera sit at its top; content keeps a ~20pt leading margin | Vertical bar on the trailing edge; asymmetric insets |
| 14·p4 | Closed, landscape | Mail | Bar still on the right; camera now bottom-right; no status bar | Bar follows the hardware, not orientation |
| 17 | Closed | Mail | Diagram: leading area is the *layout margin*, trailing area is the *horizontal safe-area inset* | Margins and insets are separate and unequal |
| 19 | Closed | Mail list | `Select` (text-only) stays in a horizontal nav row next to the camera; back and ⋯ go vertical; filter button floats bottom-leading | Text-only items stay horizontal; symbol items go vertical |
| 18 | Closed | Fitness | Segmented pills stay horizontal at top; vertical tab bar floats over a horizontally scrolling carousel that runs under it | Full-bleed scrolling content may pass under the bar; wide controls stay in the nav row |
| 20 | Closed | App Store | Full-bleed artwork under the status column; close × in the vertical region | Background bleeds past the safe area, controls do not |
| 7 | Closed vs iPhone 18 | Mail | Bottom toolbar on iPhone becomes the lower group of the side bar; top bar becomes the upper group | Top items → top of the column, bottom items → bottom |
| 23, 22 | Closed vs open | Health, Music | Closed: one column + vertical tabs. Open: Health turns tabs into a sidebar; Music reflows to two columns (art + tracks) and the mini player becomes a full transport bar | Reveal one more level; information-dense apps take the sidebar |
| 8, 15, 21 | Open, landscape (flat) | Mail | List ~35–40% / detail ~60%; detail's actions in the side column (compose, reply, reply-all, forward, trash, folder); list's own controls stay above the list | Only the detail column goes vertical; controls stay near their pane |
| 14·p5 | Partly folded (book) | Mail | Same two panes, rebalanced to 50/50 at the fold; nothing tappable in the curve | Split views rebalance to an even split when folded |
| 9, 33, 34 | Open, landscape | Reminders, Settings | Sidebar column keeps horizontal controls (and bottom search); detail column carries the side bar; Settings content starts ~83pt below the top | Sidebar bars stay horizontal; top content still clears where a status bar would be |
| 24 | Open, landscape | Reminders | List Info sheet centred, horizontal bar (× and ✓) | Sheets on the inner display are centred with horizontal bars |
| 25 | Book | Reminders | The same sheet slides into the left half, clear of the fold; the list stays on the right | Sheets and popovers move off the fold by themselves |
| 32 | Open, landscape | Settings | Sign-in sheet centred over sidebar + detail; section index A–Z stays on the detail's trailing edge | Presentations sit over the split, not inside a pane |
| 14·p3, 14·p6 | Open, portrait / tabletop | Mail | Horizontal bars return: top (sidebar toggle, up/down, status) and bottom (trash, folder, reply … compose). Tabletop keeps the bottom bar on the flat half; the image runs across the fold | Only inner portrait has horizontal bars; tabletop = content up, controls down |
| 28, 29 | Closed landscape / sheet | Music | Now Playing sheet: art left, controls right, no vertical bar, grabber on top | Control-heavy full-screen sheets opt out of the vertical bar |
| 12 | Split View, right | Notes | App fills the right half; status column and its actions on the right edge | The bar sits on the outer edge |
| 13 | Split View, left | Notes | Same note in the left half; actions on the **left** edge; no status bar (it belongs to the right app) | Insets flip sides with the half; never mirror them |
| 5 | Open landscape, two apps | Notes + TV | Notes on the left with its bar on the left edge; video player on the right with its controls along the top | Each half's bar hugs its outer edge |
| 6 | Open portrait + PiP pinned | TV + Notes | Video pinned at the top; Notes below resizes vertically with horizontal bars | Height changes in real time; vertical flexibility is required |
| 10 | Open landscape + PiP | Pages | Alert centred; floating video controls over the document; tool column on the right | Alerts and PiP overlay the layout without moving it |
| 11 | Open landscape | Maps | Full-bleed map; floating controls on the right; place card bottom-leading | Immersive surfaces centre on the whole display with controls inset |
| 1–4 | Open landscape | Safari tab overview | Bars along the top, horizontal, status at top-right; menu drops from leading | Some system surfaces keep horizontal bars on purpose |

## What the screens add to the Tech Talks

1. **The first line of content clears ~60–85pt even with a zero top inset** (Settings, Mail detail).
   The safe area alone does not give a title room. Measured in the dAIolog build too.
2. **Lists keep their own controls; details hand theirs to the side bar.** Mail's list filter and ⋯ sit
   above the list in every open pose.
3. **Split ratios differ by pose:** about 35/65 flat, 50/50 folded. A layout that fixes the split at
   50/50 only when folded matches the system; one that always splits at the fold also holds.
4. **Split View left vs right is a mirror of the bar, not of the content.** The left app loses the
   status column and gains the bar on its left edge.
