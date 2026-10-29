# iPhone Duo device captures — witness findings

What 313 screenshots of shipping apps on a real iPhone Duo show, as 34 practices with the
measurements behind them. Read the section you need when deciding a split, where a control goes,
how wide a sheet or row runs, how the keyboard meets the layout, or what may cross the fold.
`apple-reference-screens.md` holds the earlier 34 captures of Apple's apps, including the poses
this set lacks.

## The set and how it was read

The owner captured 313 frames on 2026-10-29 (`IMG_0154` to `IMG_0468`; `0257` and `0359` do not
exist) across 38 apps, Apple's own and third-party ones such as Claude, ChatGPT, Gemini, Grok,
Slack, Bear, Things, Termius and Screens. 290 are open in landscape, 22 closed in portrait and 1
closed in landscape. The frames are not bundled, because they show personal data; the ids let the
owner find a frame.

Each of 39 runners on `claude-sonnet-5-5` read one app's run of 3 to 10 consecutive frames with
`be-my-witness:be-my-witness`. For every frame it ran the prescan and read 2x crops of the trailing
bar, the band around the fold and any sheet, menu or keyboard. It also read a diff mask between each
pair of consecutive frames, so a run of variations reads as one flow rather than as separate
screens. Two merge passes reduced 357 candidate practices to 34, dropping 6 with a reason.
Verifiers then opened each practice's cited frames plus at least 2 others: 5 practices stood as
written, 29 were amended (usually a measurement or a missing condition) and none was refuted. The
verified set, with every frame list, counter-example and flow, is
`../../docs/device-captures/2026-10-29-witness.json`.

```json
{
  "gate": "inconclusive",
  "comparedAgainst": [],
  "coverage": { "framesInspected": 313, "framesInSet": 313, "uninspected": [] },
  "conformance": { "basis": "none — exemplars to learn from, not a candidate under test", "advisory": true }
}
```

The gate is `inconclusive` by construction: there is no mock and no expected output, so every
entry is an observation of what shipping software does, mistakes included.

Captures are 3x, so 1 pt is 3 px. Open in landscape the window is 951×669 pt, the fold is at
x 475.5 and the trailing bar starts at x 867. Closed in portrait it is 466×678 pt and the bar starts
at x 382.

Practices are numbered D01 to D34 (D for device), and `patterns.md` and `evidence.md` cite them by
that number. **Kind** says who decides. A `system` behaviour happens in every app and needs no code; it tells you
what not to fight. An `app-choice` is a design decision some apps make and others do not.

## Panes and the fold

### D01 · Fix the list column near 320 pt

In open landscape give the list or sidebar a fixed 292-403 pt column (320 typical) and let detail fill to 867 pt, so the fold falls inside detail. Fold-aligned dividers (Calendar Day, one Settings frame, Claude's effort/voice pane) are exceptions.

- **Kind:** app-choice, do; medium confidence; verifier: amended, wording above.
- **Measured:** Column widths: 320 pt in Claude, ChatGPT, Settings, Stocks, Journal, Files, Siri, Shortcuts, Weather; 335-340 in Passwords, Notes, Voice Memos; 360 Slack; 375 Messages; 380 Bear; 403 Mail; 292 Things. The fold sits 72-183 pt inside detail, which runs to 867 pt. Also 320 pt in Weather and Journal; Messages thread 375-867. Two-half pages split at the fold: Music 0-450 | 509-853, Podcasts 0-449 | 502-808, Books 52-449 | 501-877.
- **Seen:** 60 frames in 21 apps (Bear, ChatGPT, Claude, Files, Fitness, Games, Journal, Mail, Messages, Notes, Passwords, Screens, Settings, Shortcuts, Siri, Slack, Stocks, Termius, Things, Voice Memos, Weather). Start with IMG_0174, IMG_0226, IMG_0256, IMG_0240.
- **Exceptions:** IMG_0240 (Calendar): Day view and event detail divide at x 475.5 pt: left pane 0-475.5, right pane 476-867. IMG_0251 (Calendar): Same fold-divided split with a sheet in the left pane and 'No Event Selected' on the right. IMG_0232 (Settings): Sidebar widened to 475.5 pt for one frame; 0233 shows 320 pt again. Cause unknown, see Open questions.
- **Against this skill:** contradicts. SKILL.md step 4: "List and detail split at the fold, and on any pane at least 900pt wide." patterns.md 2 repeats it (fold, at least 800pt wide). Every app here except Calendar divides at 292-403 pt. The 35/65 flat ratio in apple-reference-screens.md stands; keep a fold split for book posture, which no frame shows.
- **In React Native:** Make DetailPaneLayout a fixed 320 pt list plus flex detail when flat and open, and keep the fold-aligned split only for book posture.

### D30 · Split two-half screens at the fold

Split a screen of two equal-weight halves (player and queue, show hero and episodes, Day and detail) at 475.5 pt, with a grabber or a 50 pt gutter on the fold. Music, Podcasts, Books and Calendar do; Settings keeps its 320 pt sidebar.

- **Kind:** app-choice, do; medium confidence; verifier: amended, wording above.
- **Measured:** Divider x 475.5; timeline x 0-473 (an event ends 2.5 pt from the divider); detail x 476-867 with cards x 516-846 (40 pt leading, 21 pt trailing); pinned actions x 557-846, y 598-644. Music hero and text in the left half, list from 528; Now Playing player 0-450, queue 509-853, grabber 447-507; Podcasts player ends 449, transcript 502-808, show-page text ends 392, episodes from 532; Books player 52-449, list 501-877, grabber on the fold.
- **Seen:** 10 frames in 4 apps (Books, Calendar, Music, Podcasts). Start with IMG_0306, IMG_0356, IMG_0397, IMG_0240.
- **Exceptions:** IMG_0410 (Fitness): Onboarding splits at 434 pt, 41 pt left of the fold; the fold cuts a notification icon. IMG_0321 (Shortcuts): The editor and library divide at 505 pt, 29 pt right of the fold.
- **Against this skill:** refines. patterns.md 3 "Two columns that meet at the fold" matches Apple for two-half screens (Music, Podcasts, Books, Calendar Day). patterns.md 2 treats a fold split as the rule for list and detail; those divide near 320-403 pt (D01), so the fold split belongs to two-half pages.
- **In React Native:** Use FoldColumns with a 50 pt gap for two-half screens such as a player and its queue, and keep DetailPaneLayout's fixed list column for list-and-detail.

### D07 · Let ordinary content cross the fold

Draw lists, text, charts and cards across x 475.5 pt without a gutter or inset; Apple's own apps do, and no frame shows a seam. Add fold logic only to a grid, picker or pane boundary you control.

- **Kind:** app-choice, do; medium confidence; verifier: confirmed as written.
- **Measured:** Crossing with no gutter: Settings rows 360-845 pt; Stocks chart and stats table; Journal cards 360-827; Files names 427-575; Podcasts result title 114-715; Wallet footnote 185-695; Apple TV separators 94-833. TV cards at 34, 299 and 565 pt (245 wide, 20 gap), card 2 over the fold; Wallet card stack 304-647 with the fold across every card.
- **Seen:** 20 frames in 9 apps (Files, Fitness, Journal, Mail, Podcasts, Settings, Stocks, TV, Wallet). Start with IMG_0226, IMG_0388, IMG_0451, IMG_0261.
- **Exceptions:** IMG_0240 (Calendar): The fold is the pane divider; nothing crosses it. IMG_0290 (Bear): Theme-card grid puts its 15 pt gutter on the fold, x 468-483 pt. IMG_0298 (Bear): The custom key grid puts its column gutter on the fold, x 469-482 pt.
- **Against this skill:** contradicts. SKILL.md opening: "so a phone column stretched across it puts a card over the hinge"; patterns.md 3: "Without it, a 3:2 row puts a card across the hinge." Apple's own apps do this in every frame cited. Caveat: no frame shows touch or crease behaviour, so keep FoldColumns optional rather than removing it.
- **In React Native:** Render a single pane as an ordinary full-width flex layout and reserve FoldColumns for grids you want a gutter on.

### D29 · Prefer gutters, not buttons, on the fold

Where you control a grid, picker or centred row, put its gap on x 475.5 pt rather than a button, icon or title. Treat it as a precaution: Apple's own apps break it and the frames show no seam or missed target.

- **Kind:** app-choice, avoid; low confidence; verifier: confirmed as written.
- **Measured:** On the fold: Shortcuts play 453-483, AI button 438-485, swipe Delete 414-489; Calendar Maybe button 418-585; Games Continue 276-675; Claude Opus pill 417-510; Voice Memos pause pill 357-511. Gutter on the fold: Bear Themes 164-468 and 483-787; Bear key grid 469-482; Stocks alert buttons end 472 and begin 481. Podcasts pause button and scrubber on the fold; Messages send arrow 462-499; Books fold 29 pt into cover column 3 (446-625); Games chip 402-497; Podcasts gutter 449-502 and Music grabber 447-507 on the fold.
- **Seen:** 48 frames in 19 apps (Bear, Calculator, Calendar, ChatGPT, Claude, Files, Games, Gemini, Grok, Journal, Messages, Podcasts, Screens, Settings, Shortcuts, Slack, Stocks, Termius, Translate). Start with IMG_0321, IMG_0290, IMG_0238, IMG_0390.
- **Exceptions:** IMG_0321 (Shortcuts): Apple's own app puts the Apple Intelligence button, x 438-485 pt, on the fold. IMG_0238 (Calendar): The fold passes through the left 58 pt of the Maybe button. IMG_0402 (Games): The Continue button is centred on x 475.5 in a 623 pt card.
- **Against this skill:** refines. patterns.md 3 ends the left column at foldX minus gap/2 so no card meets the hinge. Two apps (Bear) do it for grids; the rest ignore it with no visible harm, so make it optional.
- **In React Native:** For a grid you build, set columnGap so the gap lands on x 475.5; do not remove fold-aware code elsewhere on this evidence.

### D11 · Reflow on measured width, not device

Re-flow one screen by the width it has: Stocks goes from one news card to two when its sidebar hides, Fitness from one column closed to two open, Maps from a 400 pt leading panel to a bottom sheet. Key on pane width, not isTablet.

- **Kind:** app-choice, do; high confidence; verifier: confirmed as written.
- **Measured:** Stocks detail 467 pt: one news card x 360-827, range tabs overflow; 787 pt: two cards x 40-426 and 442-827, chart 787 pt wide, tabs fit. Fitness closed: one column x 24-358; open: x 20-343 and 385-839. Maps open: panel x 8.5-408; closed: sheet x 8.5-458. Gemini drawer 361 pt open, full width closed. Music pills 34-425 and 442-832, tiles about 188 wide at 16 pt gaps; Books covers 179 wide, 26 pt gaps; Games tiles 253 wide; Weather hourly pitch 58 pt, 9.5 columns in 567 pt.
- **Seen:** 24 frames in 11 apps (Books, Fitness, Games, Gemini, Maps, Music, Notes, Siri, Stocks, Voice Memos, Weather). Start with IMG_0380, IMG_0381, IMG_0415, IMG_0416.
- **Exceptions:** IMG_0325 (Calculator): Phone keypad stretched over 631 pt; the fold falls inside the 8-5-2-0 key column. IMG_0261 (TV): Search rows keep their phone layout across 740 pt, with the ellipsis 700 pt from the title.
- **Against this skill:** confirms. patterns.md 1 (useLayout from the width the screen has) and patterns.md 2 (width from the pane's own onLayout) already say this. These frames are worked examples with numbers.
- **In React Native:** Drive columns and chrome from useLayout() or onLayout width per pane, and re-run when a sidebar toggles.

### D22 · Selecting a sidebar row swaps detail in place

Selecting a row highlights it with a pill and replaces the detail in place, with no push, and the sidebar keeps its scroll offset. Settings holds identical sidebar scroll across consecutive selections.

- **Kind:** app-choice, do; high confidence; verifier: confirmed as written.
- **Measured:** Settings row pill x 20-300; sidebar scroll identical in 0229 and 0230 and in 0234 and 0235; detail replaced within x 340-866. Shortcuts: Automation row swaps the detail list in place. Journal sidebar 0-320 and detail 320-951 in all three frames.
- **Seen:** 22 frames in 7 apps (Claude, Journal, Passwords, Settings, Shortcuts, Slack, Stocks). Start with IMG_0229, IMG_0230, IMG_0315, IMG_0316.
- **Against this skill:** refines. patterns.md 2: "the right pane renders what the list would have pushed". Adds keeping the sidebar's scroll offset and selection pill across selections.
- **In React Native:** Hold the selected id and the sidebar list's scroll offset outside the detail navigator and render detail as a replaceable component.

### D24 · Fill an empty detail pane with a placeholder

When nothing is selected, select the first item or show a centred, labelled placeholder in the detail pane ('Select a conversation', 'No Event Selected', 'No Conversation Selected'), centred on the pane (Slack 613, Siri 635, Calendar about 680 pt), not on the fold.

- **Kind:** app-choice, do; high confidence; verifier: amended, wording above.
- **Measured:** Placeholder centres: Slack 613 (pane 360-866), Termius 595, Siri 635 (pane 320-951), Calendar 683 (pane 476-867). Stocks keeps the previous instrument in detail and centres its empty search state at x 160 in the 320 pt sidebar.
- **Seen:** 8 frames in 6 apps (Calendar, Settings, Siri, Slack, Stocks, Termius). Start with IMG_0266, IMG_0426, IMG_0251, IMG_0267.
- **Against this skill:** refines. SKILL.md step 4: "Select the first item by default, because an empty right half reads as broken"; patterns.md 2 repeats it. A labelled placeholder is used by four apps; add it as the alternative.
- **In React Native:** Render a centred empty-state component in the detail route when nothing is selected, sized from the pane's onLayout width.

### D26 · Slide a 280 pt sidebar over the list

In a three-column layout (sidebar, list, detail), open the sidebar on demand as a 280 pt full-height overlay with a scrim (Mail, Notes, Voice Memos; Gemini's drawer is 361 pt) rather than resizing panes. Two-column layouts keep a persistent 320 pt sidebar.

- **Kind:** app-choice, do; medium confidence; verifier: amended, wording above.
- **Measured:** Overlay x 0-280 pt, full height, blurred; detail stays at 340-867 (Mail 403-867) dimmed; Mail's bar buttons stay undimmed; Gemini drawer x 0-361 with a scrim over the main area.
- **Seen:** 4 frames in 4 apps (Gemini, Mail, Notes, Voice Memos). Start with IMG_0255, IMG_0161, IMG_0313, IMG_0173.
- **Exceptions:** IMG_0278 (Files): A persistent 320 pt sidebar with no overlay; the content pane takes the rest. IMG_0226 (Settings): A persistent 320 pt sidebar with the detail pane beside it. IMG_0461 (Messages): A third pane (inspector) removes the list column and re-lays thread and inspector at 547 pt instead of overlaying.
- **Against this skill:** new. The skill mentions only a persistent split.
- **In React Native:** Use a drawer navigator that overlays rather than reflows, with a fixed 280 pt width.

### D33 · Open a companion as a right-hand pane

Open content about the screen (contact inspector, lyrics, queue, transcript, chapters) as a right-hand pane beside the subject. Messages collapses its list to a toggle at x 20-68; Podcasts' player recentres on the full width when its pane closes.

- **Kind:** app-choice, do; medium confidence; verifier: amended, wording above.
- **Measured:** Messages: list 0-375 and thread 375-867 become thread 0-547 and inspector 547-951 (404 pt, 320 usable); toggle x 20-68, y 25-71; inspector close x 567-615, Edit 805-866. Music: player 0-450, queue or lyrics from 509. Podcasts: player to 449, transcript 502-808, chapters card 486-883; with the pane closed, artwork 343-608.
- **Seen:** 10 frames in 3 apps (Messages, Music, Podcasts). Start with IMG_0461, IMG_0460, IMG_0307, IMG_0357.
- **Against this skill:** confirms. patterns.md 5: "open it in the right pane instead while split: the subject stays readable beside it." Messages, Music and Podcasts do this for contact info, lyrics, queue, transcript and chapters. It does not cover sheets about a list item (see D13).
- **In React Native:** Render the companion in DetailPaneLayout's right pane when it opens, drop the list to a toggle if a third pane is needed, and let the subject take the full width when it closes.

### D23 · Keep each pane's own controls inside that pane

Controls live in their pane: sidebar toggle in the sidebar header (x 20-68 or 252-300; Claude uses the trailing bar), search pill at the sidebar foot (spans both panes while the keyboard is up), pinned actions at the pane foot. Pad list ends 70-90 pt.

- **Kind:** app-choice, do; high confidence; verifier: amended, wording above.
- **Measured:** Toggle x 252-296 (ChatGPT), 252-300 (Shortcuts), 192-300 with ellipsis (Weather), 20-68 when collapsed (Journal, Notes). Search pill x 20-300, y 598-645 (Settings). Pinned actions x 557-846, y 598-644 (Calendar). Pills overprint rows in Grok, Claude, ChatGPT, Settings, Voice Memos, Calendar and Fitness. Weather focused search x 152-739 plus cancel to 799 (587 pt) over a 320 pt sidebar; Messages search pill 20-295 and compose 308-355, y 598-644; Weather '...' 192-240 and toggle 252-300, y 24-71.
- **Seen:** 27 frames in 13 apps (Calendar, ChatGPT, Claude, Fitness, Grok, Journal, Messages, Notes, Settings, Stocks, Voice Memos, Wallet, Weather). Start with IMG_0198, IMG_0226, IMG_0240, IMG_0197.
- **Exceptions:** IMG_0197 (Claude): The sidebar toggle sits in the trailing bar at x 879-927, y 124-172, not in the sidebar header. IMG_0385 (Stocks): A search pill 588 pt wide rides the keyboard and spans the sidebar-detail boundary at 320 pt.
- **Against this skill:** refines. patterns.md 8: "Controls that act on one pane stay with that pane (Mail keeps the list's filter above the list)". Adds the sidebar toggle's and search pill's positions and the 70-90 pt list-end padding.
- **In React Native:** Put the sidebar toggle in the sidebar component's header row and give each pane's scroll content contentContainerStyle paddingBottom of about 90 pt where a pill floats.

### D16 · Do not stretch phone rows across 867 pt

Cap label-and-value and toggle rows at about 620-700 pt, centred or in a pane; full-width rows (about 850 pt) put label and value 600-800 pt apart. Multi-column tables, as in Files, may fill the width.

- **Kind:** app-choice, avoid; high confidence; verifier: amended, wording above.
- **Measured:** Stretched: ChatGPT label-to-value 700-800 pt, Apple TV rows 740 pt, Fitness+ search rows 833 pt, Screens rows 400+ pt apart, Stocks date row 600+. Capped: ChatGPT Plugins centred 710 pt, Scheduled cards 399 pt, sheet columns 621 pt (x 165-786), Files grid at 133 pt pitch. Weather sheet rows 621 pt, label from 185, switch 705-768, 340-400 pt apart; Games Add Friends row: name ends 428, Invite pill 680-759 (about 250 pt gap); Weather Continue and Not Now 400 pt wide, x 276-675.
- **Seen:** 21 frames in 9 apps (Calendar, ChatGPT, Claude, Fitness, Games, Screens, Stocks, TV, Weather). Start with IMG_0215, IMG_0261, IMG_0210, IMG_0423.
- **Exceptions:** IMG_0279 (Files): Name and Date Modified columns fill 631 pt as table columns, so the wide row reads as designed.
- **Against this skill:** new. The skill covers where panes split, not how wide a list or form may run.
- **In React Native:** Give settings screens a maxWidth near 620-700 pt with alignSelf 'center', or put the list in a left pane.

### D17 · Cap reading lines at 300 to 570 pt

In chat and reading panes, text runs 300-570 pt (about 30-70 characters): Claude 480, ChatGPT 437 (about 50 characters), Slack 427, Messages 381, Podcasts 306 at large type. Full-width screens run 85-105 characters, so this is a comfort choice.

- **Kind:** app-choice, do; medium confidence; verifier: amended, wording above.
- **Measured:** Claude transcript x 360-842 (480 pt) with composer x 360-851; ChatGPT assistant bubbles x 336-774 (437 pt, 38 characters); Slack x 424-851 (427 pt, 50-55); Messages bubble 381 pt (45); Fitness 381-440; Settings 485 pt (70); Siri 570 pt (63). Podcasts transcript x 502-808 (306 pt, 30 characters, large serif); Weather permission small print x 237-713 (90 characters); Fitness banner one line x 92-823 (about 100 characters).
- **Seen:** 13 frames in 8 apps (ChatGPT, Claude, Fitness, Games, Messages, Podcasts, Siri, Slack). Start with IMG_0356, IMG_0175, IMG_0225, IMG_0346.
- **Exceptions:** IMG_0454 (Safari): Web page paragraphs run about 105 characters over 825 pt across the fold. IMG_0212 (ChatGPT): A skill page runs 85-90 characters over 659 pt across the fold. IMG_0210 (ChatGPT): Description and footnote lines run 100-110 characters across the fold.
- **Against this skill:** new. No measure rule in SKILL.md or patterns.md.
- **In React Native:** Give Text containers inside a detail pane a maxWidth of 440-520 pt and message bubbles a width fraction of the pane's measured width.

### D14 · Centre elements on the area holding them

Sheets, search pills, sidebar-less screens (Wallet cards, Podcasts player, TV page dots, camera pills) and system permission alerts centre on the fold, 475.5 pt; in-app alerts and some empty states on 0-867, 433.5; detail content on its pane (~593; Messages inspector 707).

- **Kind:** app-choice, do; medium confidence; verifier: amended, wording above.
- **Measured:** Fold 475.5: sheets, Passwords search pill 150-795, Wallet pill, Safari URL field 295-655. Area 0-867 (433.5): ChatGPT search empty state, Gemini home 434, Shortcuts card 233-633. Pane 320-867 (593): ChatGPT orb and cards 394-793, Slack placeholder 613, Journal banner 367-820. Pane 320-951: Siri 635. Closed 0-382: Journal empty state 191. fold 475.5: Wallet cards 304-647, Podcasts artwork 343-608, TV page dots 401-547, scanner hint pill 345-606; pane: Podcasts empty queue 685 (pane 486-883), Messages avatar 707 (pane 547-867).
- **Seen:** 30 frames in 15 apps (ChatGPT, Document scanner, Gemini, Journal, Maps, Messages, Passwords, Podcasts, Safari, Shortcuts, Siri, Slack, Stocks, TV, Wallet). Start with IMG_0364, IMG_0357, IMG_0198, IMG_0390.
- **Exceptions:** IMG_0390 (Stocks): A permission alert is centred on the fold (x 317-637), not on the 433.5 pt area. IMG_0267 (Termius): The create-host form is centred in the pane, so its field and button straddle the fold.
- **Against this skill:** new. The skill never names which centre an element should use.
- **In React Native:** Centre inside the container that holds the element (onLayout width of the pane or of the inset-padded root), not with window width halved.

## The trailing bar

### D03 · Declare native bar items; the system places them

Declare actions and tabs as native bar items; the system places them as 44-48 pt glass circles and pills at x 879-927 pt: actions from y 125 open or 175 closed, tabs bottom-aligned, search a separate circle. Drawn buttons stay where drawn.

- **Kind:** system, do; high confidence; verifier: amended, wording above.
- **Measured:** Circles 47-48 pt at x 879-927 (centre about 903). Top group starts y 125 open, 175 closed, pitch about 60 pt (125-172, 184-232, 244-292, 304-351); related actions share a pill (y 125-223). Tab pill bottom-aligned: 5 icons y 384-644, 4 icons y 433-644, 3 icons y 484-644. Search circle y 598-645. Status stack y 21-107 open. Podcasts back y 125-171, filter-sort-more pill y 185-335, four-icon tab pill y 434-644; Books five-item tab pill y 383-645; Games avatar y 125-171; Wallet plus y 125-171, search y 598-645; Journal editor back, check, undo, text, more y 125-464 then a three-tool pill y 494-644.
- **Seen:** 61 frames in 23 apps (Bear, Books, Claude, Document scanner, Files, Fitness, Games, Gemini, Grok, Journal, Maps, Notes, Passwords, Podcasts, Shortcuts, Slack, Stocks, TV, Termius, Things, Translate, Voice Memos, Wallet). Start with IMG_0263, IMG_0267, IMG_0174, IMG_0395.
- **Exceptions:** IMG_0395 (Books): Profile avatar stays in the content header at x 803-843 pt instead of the bar. IMG_0347 (Weather): Sidebar toggle and ellipsis sit at the sidebar's top corner, x 192-300 pt; the bar holds no app buttons. IMG_0227 (Settings): Edit pill sits in the detail header, ending at the bar boundary, not in the bar.
- **Against this skill:** refines. SKILL.md step 4 ("Bars move to the side only as native bar items") and patterns.md 8 state the rule. This adds placement numbers and shows third-party apps get the bar the same way.
- **In React Native:** Use expo-router NativeTabs triggers and Stack.Toolbar items (SF Symbol plus label) so UIKit places them; a View-drawn header will not reach the bar.

### D06 · Top group for screen actions, bottom for tabs

Put screen actions (back, close, share, more, Done) in the bar's top group; tabs, creation and toolbar items in the bottom group. Reuse one top slot (x 879-927, y 124-172) across screens. The middle is usually clear; top groups reach y 350 or 500.

- **Kind:** app-choice, do; high confidence; verifier: amended, wording above.
- **Measured:** Fixed slot x 879-927, y 124-172: ChatGPT shows back, close, add and phone glyphs in it across 7 frames. Mail open: archive-move-reply pill y 426-576 plus compose y 590-637. Slack: tab pill y 373-585, Search y 598-645. Notes: tool pill y 434-584, compose y 598-645. Screens: top capsule y 125-276, bottom y 484-644. Messages round button y 125-171, capsule y 125-276; Music back y 125-171 above its share and '...' pill, tab pill y 384-647; a single contextual button joins the bar under the status stack in 0307.
- **Seen:** 31 frames in 12 apps (Calendar, ChatGPT, Mail, Messages, Music, Notes, Screens, Slack, Stocks, Termius, Things, Voice Memos). Start with IMG_0209, IMG_0210, IMG_0256, IMG_0263.
- **Exceptions:** IMG_0311 (Voice Memos): Seven actions fill the column from y 125 to 499, so the middle is not empty.
- **Against this skill:** refines. apple-reference-screens.md row 7 (top items to the top, bottom items to the bottom) and patterns.md 8 ("back -> prominent action -> other actions -> tabs") cover the order. This adds the reused fixed slot and the bottom group's contents.
- **In React Native:** Declare back, close and share as Stack.Toolbar items and tabs as NativeTabs triggers; keep the first toolbar item in the same position on every screen.

### D02 · End text and controls at the trailing inset

End text, rows, cards and controls at the bar's leading edge: x 867 pt open (usually 0-40 pt clear, mostly 12-25), about 382 pt closed (usually 15-45 clear). Sheets, menus and keyboard backing may run under the bar; Calculator and Siri do.

- **Kind:** app-choice, do; high confidence; verifier: amended, wording above.
- **Measured:** Open gap to 867 pt: 0-1 (ChatGPT cards, Settings 866), 12 (ChatGPT and Wallet 855), 15-16 (Grok 852, Fitness 851), 21 (Calendar, Shortcuts 846), 24-25 (Screens, Claude 842-843), 34-40 (Games, Podcasts, Stocks, Journal 827-833). Closed: content ends 346-383 pt of 382. Music content ends 832-835 (tightest 853), Books 846, Fitness 846, Journal 826; Podcasts transcript toggle at 770 and queue button at 848.
- **Seen:** 59 frames in 23 apps (Books, Calendar, ChatGPT, Claude, Fitness, Games, Gemini, Grok, Journal, Mail, Messages, Music, Passwords, Podcasts, Remote-desktop client, Screens, Settings, Shortcuts, Slack, Stocks, TV, Termius, Wallet). Start with IMG_0209, IMG_0156, IMG_0381, IMG_0244.
- **Exceptions:** IMG_0325 (Calculator): Keys run to 941 pt and the status cluster is absent; the app draws into the bar. IMG_0424 (Siri): Text runs to 920 pt; the status capsule sits over the first lines and cuts words. IMG_0456 (Safari): Second card of a two-column grid ends at 875 pt, 8 pt inside the bar's x range.
- **Against this skill:** refines. SKILL.md step 4 ("Pad each side for its own inset") and patterns.md 7 state the rule. This adds the measured clearance (0-40 pt, mostly 12-25) and the closed-portrait edge at 382 pt.
- **In React Native:** Pad each screen root by useSafeAreaInsets().right plus a 16-24 pt margin, and confirm on the Duo that the inset reports the bar before relying on it.

### D18 · Let backgrounds bleed under the bar, not controls

Let maps, artwork, separators and scroll indicators run under the trailing bar; keep text and controls out. Pad horizontal rows so the last item scrolls clear of the bar buttons, and fit fixed rows before the bar (x 867 pt open, 382 pt closed).

- **Kind:** app-choice, do; high confidence; verifier: amended, wording above.
- **Measured:** Under the bar: Maps tiles, Weather hourly cards to 919, Books cover art, Games carousels, Voice Memos waveform to 951, Files separators to 926, scroll indicator at x 946. Failures: Stocks 10Y at 828-852 past a rule ending 827, ChatGPT Pages tab 863-909, Fitness+ tab row cut at 859-867, Shortcuts chip behind the buttons. New failures: Fitness+ card from 849 under the tab capsule (x 880-926); Messages 'Documents' tab clipped at 951 behind the capsule at y 232; Safari close X under the status pill. New bleeds: Books shelf to 951 with the seventh cover clipped, Music gradient to 951, camera views to 951.
- **Seen:** 33 frames in 19 apps (Books, Calendar, ChatGPT, Document scanner, Files, Fitness, Games, Journal, Maps, Measure, Messages, Music, Settings, Shortcuts, Stocks, TV, Voice Memos, Weather, a banking app). Start with IMG_0162, IMG_0395, IMG_0321, IMG_0422.
- **Exceptions:** IMG_0166 (Maps): Closed, the status capsule covers a Recent card and hides part of its label. IMG_0347 (Weather): The hourly forecast card ends about 919 pt, 52 pt into the bar zone beside the status ring. IMG_0421 (Fitness): A carousel card begins at 849 pt and scrolls under the tab capsule, which covers its left part.
- **Against this skill:** confirms. apple-reference-screens.md rows 18 and 20: "Full-bleed scrolling content may pass under the bar; wide controls stay in the nav row" and "Background bleeds past the safe area, controls do not". These frames add 10 more apps and the failure cases.
- **In React Native:** Render backgrounds absolutely filling the window and inset only interactive overlays; give horizontal ScrollViews contentContainerStyle paddingRight equal to the right inset.

### D27 · Drawing into the bar changes the status cluster

The status cluster stays and never moves your content. Over content it sits on a blur capsule that cuts text beneath it (Siri x 833-925, y 26-68; Maps). Only full-bleed canvases (Calculator, remote desktop) lose it. Keep text out from under it.

- **Kind:** system, avoid; medium confidence; verifier: amended, wording above.
- **Measured:** Calculator keys to x 941, no status items; Remote-desktop canvas to x 950; Safari status inline at x 832-925, y 26-70; Siri text to x 920 with the cluster at x 833-925, y 26-68. camera views show no clock, battery or 5G, a green dot near x 927, y 26, and bar controls from y 24; Maps and Journal status capsule x 877-930 over the map; Safari status pill x 825-931, y 21-69.
- **Seen:** 13 frames in 9 apps (Calculator, Document scanner, Journal, Maps, Measure, Remote-desktop client, Safari, Siri, Translate). Start with IMG_0333, IMG_0282, IMG_0424, IMG_0454.
- **Exceptions:** IMG_0162 (Maps): The map runs under the bar and the status cluster stays intact; only passive art enters the column. IMG_0347 (Weather): Forecast cards run to 919 pt and the status cluster stays; only background content enters the bar.
- **Against this skill:** new. The skill does not say what the status cluster does when content enters the bar.
- **In React Native:** Keep scroll content inside the right inset; for an immersive canvas hide the status bar and keep controls inset.

### D28 · Bar buttons follow the status stack down

Never fix bar buttons at a constant y; they sit below the status stack. Closed, a mic dot pushes them down 22 pt; open, a low-battery banner pushes them 54 pt (status items 100 pt) but a mic dot does not. Use native items.

- **Kind:** system, do; medium confidence; verifier: amended, wording above.
- **Measured:** Open: stack y 21-107, first button y 125. Closed: stack y 72-160, first button y 175. Siri's mic dot moves a button from y 175-222 to y 197-244. Stocks banner x 535-937, y 16-111: status items drop about 100 pt and the Share capsule about 54 pt. Podcasts normal stack y 21-107, with a capsule y 24-190 (84 pt lower); Messages recording dot at x 925, y 26 with the capsule still at y 125-276.
- **Seen:** 9 frames in 4 apps (Calendar, Podcasts, Siri, Stocks). Start with IMG_0357, IMG_0388, IMG_0389, IMG_0430.
- **Against this skill:** new. The skill gives fixed positions only.
- **In React Native:** Do not hard-code a y offset for a bar control; declare it as a native toolbar item.

### D19 · Modal scrim dims bar buttons, not status items

A native modal's scrim dims bar buttons and the tab pill, never the status cluster. Centred sheets stop at x≈802, short of the bar; wide bottom sheets and closed-portrait sheets cover it below the status. Sidebars, menus and popovers do not dim it.

- **Kind:** system, do; high confidence; verifier: amended, wording above.
- **Measured:** Status cluster y 21-107 at full brightness; app buttons x 879-927 dimmed; sheet right edge 802-804 pt, 63-65 pt short of the bar.
- **Seen:** 60 frames in 16 apps (Bear, Books, Calendar, Claude, Fitness, Games, Grok, Journal, Maps, Notes, Screens, Shortcuts, Stocks, Translate, Wallet, a banking app). Start with IMG_0177, IMG_0287, IMG_0417, IMG_0255.
- **Exceptions:** IMG_0259 (Mail): Closed portrait: the Move bottom sheet spans x 7-457 pt and covers the bar column, dimming the bar buttons behind it. IMG_0255 (Mail): A sidebar overlay scrims the panes but leaves the bar's buttons undimmed; it is not a modal. IMG_0281 (Files): Sidebar edit mode leaves both bar pills active and undimmed.
- **Against this skill:** new. The skill does not describe scrim behaviour at the bar.
- **In React Native:** Use formSheet or pageSheet presentation (a native modal) instead of an in-tree overlay so the scrim covers the bar.

## Sheets, alerts and menus

### D04 · Present sheets natively: 653 pt on the fold

Open pose: modal sheets centre on the fold, usually 653 pt (x 149-802), top y 8 (partial-height y 82), 65 pt clear of the bar; small cards float from y 48-56. Exceptions: left-pane sheets (x 8-467), Bear's wide bottom sheet, full-window Now Playing.

- **Kind:** system, do; medium confidence; verifier: amended, wording above.
- **Measured:** Sheet x 149-802 pt; inner cards x 165-786 (621 pt, 16 pt inset); onboarding cards 623 pt (x 164-787); partial-height sheets start at y 82 (Weather, Safari, Siri). Smaller sheets stay centred on the fold: Notes 524 pt, Grok profile 581, Things 349-369, Bear password 400. Games Add Friends 600 pt (x 175-775), Challenges 625 (x 163-788); Weather, Journal, Fitness, Books, a banking app and Shortcuts sheets x 149-802. Now Playing in Music, Podcasts and Books spans x 0-951 from y 0, grabber at x 475.5.
- **Seen:** 83 frames in 24 apps (Bear, Books, Calendar, ChatGPT, Claude, Files, Fitness, Games, Grok, Journal, Notes, Passwords, Safari, Screens, Shortcuts, Siri, Slack, Stocks, Things, Translate, Voice Memos, Wallet, Weather, a banking app). Start with IMG_0306, IMG_0403, IMG_0177, IMG_0237.
- **Exceptions:** IMG_0243 (Calendar): The New Event sheet occupies only x 8-467 pt, 459 wide, with its right edge 8-9 pt before the fold. IMG_0186 (Claude): The Effort page sits in the left half, x 8-467 pt; the same page was fold-centred in 0185. IMG_0294 (Bear): A statistics bottom sheet spans x 12-939 pt from y 170, using the bar column below the status cluster.
- **Against this skill:** refines. apple-reference-screens.md rows 24 and 32 say sheets are centred and sit over the split. SKILL.md gives no sheet width; this adds 653 pt, top y 8, 65 pt clearance and the 623 pt card.
- **In React Native:** Use react-native-screens formSheet or pageSheet presentation (expo-router modal) and lay content out with flex; never give a Modal a width or a left offset.

### D13 · Present contextual sheets over both panes

Present item sheets fold-centred over both dimmed panes (653 pt, x 149-802). The same sheet can shrink to the left pane (Calendar New Event and Reminder, Claude Effort). Maps and Journal Places float an undimmed card; players and Messages open companions as a right pane.

- **Kind:** app-choice, do; medium confidence; verifier: amended, wording above.
- **Measured:** Sheet x 149-802 pt over list x 0-320 and detail x 320-867, scrim on both; Siri's Sources sheet starts y 82. Journal Places card x 531-940 with sidebar and map lit; Maps search panel x 8-408, top y 4; Messages inspector x 547-951; Podcasts transcript x 502-808.
- **Seen:** 14 frames in 10 apps (Calendar, ChatGPT, Claude, Fitness, Journal, Safari, Siri, Slack, Stocks, Weather). Start with IMG_0450, IMG_0427, IMG_0204, IMG_0164.
- **Exceptions:** IMG_0243 (Calendar): A New Event sheet sits in the left pane only, with the detail pane left visible beside it. IMG_0186 (Claude): The Effort page occupies the left half while the voice screen stays visible on the right. IMG_0450 (Journal): Entry card floats at x 531-940 inside the detail pane over a map; sidebar and map stay undimmed.
- **Against this skill:** refines. patterns.md 5: "open it in the right pane instead while split: the subject stays readable beside it." Holds for transcripts, lyrics, queue and contact info (Podcasts 0356, Music 0307, Messages 0461) and map cards (Journal 0450); sheets about a list item still open over both panes.
- **In React Native:** Present item sheets with formSheet over the split, and keep DetailPaneLayout's right pane for companions that sit beside the subject, such as a transcript or inspector.

### D20 · Sheet header: 48 pt close or back, left

In a form sheet (x 150-802), header y 24-72: 48 pt round close or back at x 165-213, title centred on 475.5, action at 738-786. Close can sit trailing (Bear, Books, Translate, ChatGPT). Narrow, wide or Games sheets move or left-align the title.

- **Kind:** app-choice, do; high confidence; verifier: amended, wording above.
- **Measured:** Header row y 24-72. Close or back x 165-213; trailing confirm, '...' or info x 738-786. Second sheet over the first keeps x 150-802 and starts y 290 with a grabber at y 295. Closed portrait: the same buttons move to the bar at y 175-283. Weather partial sheet (top y 82) back or close circle x 165-213, y 106-154; Books back leading and close trailing; a banking app close 165-213 and reset 738-786; Shortcuts close 165-213, confirm 740-787; Games back 179-227, check 723-771.
- **Seen:** 27 frames in 9 apps (Bear, Books, Calendar, Claude, Fitness, Shortcuts, Wallet, Weather, a banking app). Start with IMG_0348, IMG_0403, IMG_0288, IMG_0180.
- **Exceptions:** IMG_0294 (Bear): Close X sits at x 875-924 pt, inside the bar column, because the wide sheet starts below the status cluster. IMG_0373 (Wallet): Select mode swaps in text pills: Select All at the leading edge and Cancel at the trailing edge. IMG_0403 (Games): Add Friends: title at the leading edge (x 192), trailing check, no close or back button; nothing is centred on the fold.
- **Against this skill:** new. The skill has no sheet-header geometry.
- **In React Native:** Host a native stack navigator inside the formSheet route with headerLeft, headerRight and a centred headerTitle, and keep the sheet's detent fixed while it pushes.

### D31 · Sheets may sit in the left half

Some states show a sheet confined to the left half (x 8-467 pt, 459 wide, 8.5 pt short of the fold, top y 8) instead of fold-centred x 149-802. Inner content is 428 pt wide there, 621 centred; lay out for both.

- **Kind:** system, do; low confidence; verifier: amended, wording above.
- **Measured:** Left-half sheet x 8-467 pt, top y 8; fold-centred sheet x 149-802 pt in IMG_0242 and IMG_0185 of the same sessions.
- **Seen:** 5 frames in 3 apps (Calendar, Claude, Maps). Start with IMG_0242, IMG_0243, IMG_0185, IMG_0186.
- **Exceptions:** IMG_0242 (Calendar): The same New Event sheet is fold-centred, x 149-802 pt, in the frame before. IMG_0185 (Claude): The Effort page is fold-centred, x 149-802 pt, in the frame before. IMG_0346 (Weather): Permission sheet is fold-centred, x 149-802 pt, over a dimmed split view.
- **Against this skill:** refines. apple-reference-screens.md row 25 records a Reminders sheet sliding into the left half in book pose. Two more apps show it, but the capture cannot show whether the device was in book posture.
- **In React Native:** Lay sheet content out with flex so it works at 459 and 653 pt; do not assume either width.

### D32 · Wide sheets start below the status cluster

Bear's bottom sheets (Statistics, Table of Contents) span x 12-939 pt from top y 170, below the bar's first round button, and cover the bar column; close X (x 875-924) and tool pill sit there. Other apps' partial sheets (Claude Usage) stay 653 pt wide.

- **Kind:** app-choice, do; low confidence; verifier: amended, wording above.
- **Measured:** Bottom sheet x 12-939 pt, top y 170, bottom y 661; close X x 875-924, y 186-234; three-button tool pill y 452-613 inside the bar column, its active item with a filled highlight and a red icon.
- **Seen:** 2 frames in 1 apps (Bear). Start with IMG_0294, IMG_0295, IMG_0287.
- **Exceptions:** IMG_0287 (Bear): The same app's Settings sheet is 653 pt wide and stops 65 pt before the bar. IMG_0356 (Podcasts): Player fills the window from y 0; the status cluster sits on its surface at y 21-107. IMG_0397 (Books): Audiobook player fills x 0-951 from y 0 with the status cluster on its surface, not below it.
- **Against this skill:** new. The skill has no sheet that enters the bar column.
- **In React Native:** Use a bottom sheet with a top inset near 170 pt (snap point near 490 pt) and check its trailing controls clear the status stack.

### D15 · Use system alerts, centred left of the fold

Use the system alert: 319 pt wide, centred on the 0–867 pt area (x 274–593), buttons may straddle the fold. Permission prompts are 320 pt wide and centre on the fold (x 317–637). Cancel confirmations are 240 pt popovers anchored to the button, not alerts.

- **Kind:** system, do; medium confidence; verifier: amended, wording above.
- **Measured:** App alerts x 274-593, y 88-303 with the keyboard up (Maps, Voice Memos, Stocks) or y 165-471 for a rating prompt (Wallet); Save at x 437-578 crosses the fold. Permission alert x 317-637 (Stocks), buttons 333-472 and 481-621 with the fold between. Calendar discard alert 240 x 167 pt: x 70-310 and 21-261 open, x 202-442 closed.
- **Seen:** 7 frames in 5 apps (Calendar, Maps, Stocks, Voice Memos, Wallet). Start with IMG_0369, IMG_0390, IMG_0163, IMG_0384.
- **Exceptions:** IMG_0390 (Stocks): The calendar permission alert is x 317-637 pt, centred on the fold, unlike the four alerts at 274-593 pt.
- **Against this skill:** refines. apple-reference-screens.md row 10 ("Alerts and PiP overlay the layout without moving it") says nothing about centre or width. This adds 319 pt, centre 433.5 pt and the permission-prompt exception.
- **In React Native:** Use Alert.alert, Alert.prompt or the permission APIs unchanged; centre any custom dialog on the inset-padded root's width.

### D08 · Anchor menus to their button; use native menus

Anchor menus to the trigger, 250 pt wide by default (193-375 by content). Bar menus end near x 930, over the bar, starting at y 125 or 184. Left-pane menus stay left unless the trigger is near x 400-434; then they cross the fold.

- **Kind:** system, do; high confidence; verifier: amended, wording above.
- **Measured:** Bar triggers: x 677-929 pt, top y 124-125. Left-pane triggers: x 20-270 (Shortcuts), 52-302 (Stocks), 142-391 (Slack). Composer plus: x 333-611 and 386-635 straddle the fold. 319-320 wide: Voice Memos Options 611-930, Mail Move 610-930; View Options 375 pt; Bear menu height shrinks to y 327 above its accessory at 335. 249 wide: Podcasts bar menu 678-927, Wallet 678-926, Books 677-925 over the tab pill, Games 583-832, Journal 577-826 and its sidebar menu 20-270, Messages filter 32-281; Messages attach menu 320 wide, x 21-341. Podcasts and Books menus from a trigger at x 434: 309-558. Remote-desktop menu 657-904.
- **Seen:** 53 frames in 23 apps (Bear, Books, Calendar, ChatGPT, Claude, Files, Fitness, Games, Grok, Journal, Mail, Messages, Notes, Passwords, Podcasts, Remote-desktop client, Screens, Shortcuts, Slack, Stocks, Things, Voice Memos, Wallet). Start with IMG_0361, IMG_0175, IMG_0214, IMG_0332.
- **Exceptions:** IMG_0259 (Mail): Closed, the same Move menu becomes a bottom sheet 450 pt wide that covers the bar column. IMG_0245 (Calendar): Closed portrait calendar picker is x 101-351 pt, inside the content column and clear of the bar. IMG_0361 (Podcasts): A '...' trigger at x 434 opens a 249 pt menu at x 309-558, across the fold: left-pane menus do not always stay left.
- **Against this skill:** refines. apple-reference-screens.md row 25 says "Sheets and popovers move off the fold by themselves" (book pose). In the flat pose menus straddle the fold when the trigger is near it. SKILL.md mentions only Stack.Toolbar items.
- **In React Native:** Use a native menu library (zeego, @react-native-menu/menu or expo-ui) on a Stack.Toolbar item so UIKit anchors it, overlaps the bar and clamps height itself.

## The keyboard

### D05 · Expect the split keyboard around the fold

Open, the system keyboard is one 951 pt panel: key blocks at x 85-388 and 563-866, a 175 pt gap on x 475.5, 278 pt tall with a suggestion row and 241 pt without. Closed, one 466 pt piece, 304 or 265 pt tall.

- **Kind:** system, do; high confidence; verifier: confirmed as written.
- **Measured:** Open: panel x 0-951, top y 391 (278 pt, suggestion row) or 428 (241 pt, no suggestions or URL type); suggestions and autofill fill the right half only; keys x 85-388 and 563-866. Closed: panel x 0-466, keys x 7-460, top y 374 (304 pt, suggestions), 376 (302) or 413 (265, none). Music 0308 top row ends 361 and resumes 592 (231 pt gap) while g and v rows run 389-563 (174 pt); Games, Messages, Weather and Music panel top y 391-392, 277-278 tall; Maps and remote desktop without suggestions top y 429, 240 tall.
- **Seen:** 52 frames in 25 apps (Bear, Calendar, ChatGPT, Claude, Files, Games, Journal, Maps, Messages, Music, Notes, Passwords, Photos, Podcasts, Remote-desktop client, Screens, Shortcuts, Siri, Stocks, TV, Things, Translate, Voice Memos, Wallet, Weather). Start with IMG_0159, IMG_0254, IMG_0168, IMG_0200.
- **Against this skill:** new. Neither SKILL.md nor the references mention the keyboard.
- **In React Native:** Draw nothing; read the frame from Keyboard events rather than constants and design for 391 pt of visible height open and 374 pt closed.

### D09 · Lift the focused field above the keyboard

In open landscape the split keyboard tops out at y 391 pt (428 without suggestions; 374 in closed portrait). Lift the focused field or composer 8-20 pt above that edge. Keyboard overlays form sheets without resizing them, so make sheet content scroll.

- **Kind:** app-choice, do; high confidence; verifier: amended, wording above.
- **Measured:** Composer bottom 379-384 against keyboard top 391 (ChatGPT, Claude); ChatGPT composer y 288-378 with keyboard, 587-635 without; Shortcuts field y 324-374 with, 587-637 without; Messages composer 20 pt above a 428 keyboard top; TV search pinned at y 25-68; Passwords list header collapses 129 pt. Weather search pill y 336-383 above a keyboard top at 391 (8 pt); Messages field y 331-371 above a 392 top (21 pt); Music and Maps fields at y 24-70, 320-360 pt above; Maps list cut at 429 (240 pt keyboard).
- **Seen:** 22 frames in 15 apps (Calendar, ChatGPT, Claude, Journal, Maps, Messages, Music, Passwords, Photos, Screens, Shortcuts, Siri, TV, Translate, Weather). Start with IMG_0202, IMG_0242, IMG_0317, IMG_0318.
- **Exceptions:** IMG_0242 (Calendar): The New Event sheet's lower fields sit behind the keyboard; the sheet did not resize. IMG_0274 (Screens): The 'Learn how' link is under the translucent keyboard; Client Secret ends 9 pt above it. IMG_0448 (Journal): The second colour-swatch row is clipped at the keyboard's top edge.
- **Against this skill:** new. Keyboard avoidance is not in SKILL.md or patterns.md.
- **In React Native:** Drive KeyboardAvoidingView or react-native-keyboard-controller from the reported frame (check that RN's events report the split panel on the Duo) and make sheet content a ScrollView.

### D12 · Expect the keyboard to cover the lower bar

Split keyboard (top y 391 pt; 428 without suggestions) covers the lower bar. Bottom groups stay blurred beneath it (Music, Games, Podcasts, Photos, TV, Translate) or the app folds buttons into a top group (Calendar, Voice Memos, Journal). Keep typing controls in the top group.

- **Kind:** system, do; medium confidence; verifier: amended, wording above.
- **Measured:** Calendar: four circles end with '...' at y 358, 33 pt above the keyboard top; Voice Memos: share, favourite, folder and '...' end y 335 (seven actions to y 499 without keyboard); Journal: back, check and more end y 342; Notes: Done on top, tool pill removed. the five-icon tab pill (y 384-644) stays, blurred, behind the keyboard in Music (0308) and Games (0406); Games' avatar above it stays lit at y 125-171.
- **Seen:** 19 frames in 10 apps (Calendar, ChatGPT, Claude, Games, Journal, Music, Notes, Photos, TV, Voice Memos). Start with IMG_0308, IMG_0406, IMG_0239, IMG_0314.
- **Exceptions:** IMG_0251 (Calendar): The compact chip stack stays after the keyboard is gone; the reflow did not revert in this frame. IMG_0300 (Bear): App buttons stay visible above the 428 pt keyboard; they were already in the top group.
- **Against this skill:** new. No keyboard-and-bar interaction appears in the skill.
- **In React Native:** Do not put a control that typing needs in the bar's lower half; put it in the top group or in a keyboard accessory view.

### D25 · Float keyboard accessories 8 pt above the keys

Float a keyboard accessory (format toolbar, search pill) 8-12 pt above the keyboard top (y 391; 428 without a suggestion row), 44-48 pt tall, ending before the bar (x ≤866 open, ≤381 closed). A search pill with its X may centre on the fold.

- **Kind:** app-choice, do; high confidence; verifier: amended, wording above.
- **Measured:** Capsule y 335-383 against keyboard top 391 (Notes x 487-866, Bear x 12-855, Wallet pill, Journal pill y 336-383). Passwords search pill x 150-736 plus X to 795, 8 pt above. Closed: Notes toolbar x 20-382. Bear grid 10 by 4, x 86-865, gutter x 469-482. Weather pill y 336-383, x 152-739 plus cancel to 799; remote-desktop shortcut row x 23-928, y 371-427 above a 240 pt keyboard.
- **Seen:** 17 frames in 10 apps (Bear, Journal, Messages, Notes, Passwords, Photos, Podcasts, Stocks, Wallet, Weather). Start with IMG_0159, IMG_0297, IMG_0328, IMG_0366.
- **Exceptions:** IMG_0268 (Remote-desktop client): The special-keys row spans x 22-929 pt, reaching into the bar zone. IMG_0385 (Stocks): The search pill is 588 pt wide and covers the sidebar-detail boundary. IMG_0269 (Remote-desktop client): Shortcut row spans x 23-928 pt, y 371-427 pt, 62 pt into the bar column above a 240 pt keyboard.
- **Against this skill:** new. The skill has no keyboard-accessory rule.
- **In React Native:** Use InputAccessoryView or a keyboard-tracking view with right padding of the inset, and give a custom input view an even column count with a centre gutter.

## The top of the screen

### D21 · Start at the top; header row y 24-72

Open: top inset 0; add no status-bar padding. Header row 48 pt at y 24-72 (title centre y 48), first card near y 82, scroll content under a translucent header to y 0. Keep text left of the bar, x 867.

- **Kind:** app-choice, do; high confidence; verifier: amended, wording above.
- **Measured:** Grok first chat line y 22, toggle y 26; Things search pill y 29-68, large title y 69-95; ChatGPT title centre y 48, first card y 82; Settings inline title y 48, first card y 82; Claude header band y 0-82; sheets top y 8; leading inline title x 340. Fitness large title cap top y 38, Fitness+ title and pill row y 38 and 83; Journal title centre y 37, sidebar buttons y 25-71.
- **Seen:** 16 frames in 9 apps (ChatGPT, Claude, Files, Fitness, Gemini, Grok, Journal, Settings, Things). Start with IMG_0216, IMG_0228, IMG_0336, IMG_0156.
- **Exceptions:** IMG_0424 (Siri): Text starts at y 26 under the status capsule and runs to x 920, so words are cut. IMG_0259 (Mail): Closed portrait: the header starts at y 5 because the status items sit in the bar.
- **Against this skill:** refines. patterns.md 6: "59 + 8 (where it sits on every other iPhone) matched iOS Settings, which starts content ~83pt down". The first card at y 82 agrees; this adds the 24-72 header row, title centre y 48 and floating pills at y 22-29.
- **In React Native:** Use insets.top (0 open) rather than 47 or 59 pt constants, and set headerTransparent with a blur so lists scroll under the header.

## The closed display

### D10 · Closed portrait: one 382 pt column plus bar

Closed, content sits in one column ending x 382 pt; the 84 pt bar holds back, filter, Cancel and Confirm from y 175, under the status stack (y 75-160). Bottom sheets, Maps search and the keyboard span 466 pt and keep their own close X.

- **Kind:** app-choice, do; high confidence; verifier: amended, wording above.
- **Measured:** Bar x 382-466. Status stack y 72-160; first bar button y 175-222; bottom group ends y 645-656. Content ends 346-383 pt. One-piece keyboard x 0-466, 302-304 pt tall. Calendar sheet X and check at y 175-283 in the bar, form rows x 24-367.
- **Seen:** 20 frames in 7 apps (Calendar, Fitness, Gemini, Journal, Maps, Notes, Siri). Start with IMG_0244, IMG_0236, IMG_0171, IMG_0259.
- **Exceptions:** IMG_0165 (Maps): Bottom sheet spans x 8.5-458 pt, under the bar column. IMG_0259 (Mail): The Move bottom sheet spans x 7-457 pt and covers the bar column. IMG_0435 (Journal): Sheet fills x 8-458 pt; only its content is held to x 46-344.
- **Against this skill:** refines. SKILL.md facts table: "Closed (outer display) | 466×678 | One vertical bar, 84pt trailing; top inset 0". Adds the 382 pt column, status stack y 72-160, first action y 175, the 304 pt one-piece keyboard and sheet buttons moving into the bar.
- **In React Native:** Key the closed layout on useWindowDimensions width 466 and pad the root by the right inset; use native toolbar items so sheet buttons can move into the bar.

## Camera and immersive views

### D34 · Full-bleed camera views, controls in the bar

In a camera view, run the preview full-bleed to x 951 pt and hide the status bar: only the green camera dot (~x 924, y 26) remains. Put round controls in the bar from y 24, modes at its foot (capsule or stacked buttons), and any shutter in the bar or left of x 867.

- **Kind:** app-choice, do; medium confidence; verifier: amended, wording above.
- **Measured:** Measure: trash y 24-72, undo 85-132, shutter 149-189 in the bar, mode capsule y 535-647. Translate: gallery y 24-71, torch 84-132, mode capsule 484-645, shutter x 783-846 (centre y 334), language pill 340-527. Scanner: close y 24-72, three options y 477-644, shutter x 767-847, hint pill 345-606. Green dot near x 927, y 26.
- **Seen:** 4 frames in 3 apps (Document scanner, Measure, Translate). Start with IMG_0333, IMG_0377, IMG_0282, IMG_0376.
- **Against this skill:** new. The skill has no camera guidance; patterns.md 6 and 8 cover titles and bar items for list and detail screens only.
- **In React Native:** Draw the camera preview over the whole window, hide the status bar on that route, and declare the round controls as native bar items; keep the shutter left of x 867.


## Flows

Consecutive frames that perform one task, read through their diff masks. Frame ranges skip
numbers that belong to other runs.

| Flow | Frames | What it shows on the Duo | Practices |
|---|---|---|---|
| Messages: keyboard, edit, filter, inspector, attach, record, new message, search | 0458–0468 | The bar keeps one video-call button, then a three-icon capsule, unchanged by the keyboard. The 375 pt list gives way to a 404 pt inspector at 547-951 pt; menus open inside their own pane, and the send arrow sits on the fold. | D33, D01, D08, D05, D29 |
| Music: playlist, library, Now Playing, lyrics, search | 0304–0308 | Player and queue divide at the fold with a 50 pt gutter and a grabber on it. The keyboard covers the tab pill, which shows blurred behind it; content ends 32 pt before the bar. | D30, D33, D12, D02, D04 |
| Podcasts: show page, menus, search, transcript, chapters, output picker | 0351–0361 | Bar menus are 249 pt and sit right of the fold; the menu from a trigger at x 434 spans it (309-558). A black capsule pushes the status items down 84 pt; with the transcript closed the player centres on the fold. | D08, D30, D33, D28, D29 |
| Weather: edit cities, notification sheets, search with the keyboard | 0344–0350 | Weather's sheets sit on the fold at 653 pt, the partial ones from y 82. The sidebar header holds the toggle and '...', not the bar. The focused search field widens to 587 pt over both panes, 8 pt above a split keyboard. | D04, D23, D01, D16, D05 |
| Wallet: card stack, search, orders, rating alert, menu, notifications, select | 0364–0373 | Sheets stay on the fold at 653 pt with the bar dimmed beside them; the alert centres on x 434 and the menu opens right of the fold at 678-926 pt. The phone-width card stack puts the fold through every card. | D04, D08, D15, D25, D19 |
| Books: home, account sheet, owned books, audiobook player, library menus | 0394–0401 | Account and All Books keep one 653 pt sheet frame; the player fills the window and splits at the fold. Menus are 249 pt: 309-558 near the fold, 677-925 from the bar, overlapping the tab pill. | D04, D30, D08, D11, D18 |
| Games: onboarding cards, Friends sheets, search, library menu, Arcade | 0402–0409 | Sheets are 600 and 625 pt, centred on the fold, with the bar dimmed beside them. With the keyboard up the tab pill is blurred under it. Hero and carousels run under the bar while tiles stop at 832 pt. | D04, D19, D12, D18, D20 |
| Fitness: first run, Summary, Fitness+ sheet, Workout Buddy closed and open | 0410–0416 | Workout Buddy re-flows from 466 to 951 pt and keeps the back button and tab pill in the bar. Summary text ends at 846 pt; the Fitness+ sheet sits on the fold at 653 pt with the tab capsule dimmed. | D11, D04, D19, D02, D21 |
| Fitness: friends in a sheet, a full page, Fitness+ for you and search | 0417–0423 | A push stays inside one 653 pt sheet frame; the overflow menu opens right of the fold. As a page it runs x 16-851 pt in two columns, and the fold falls through the right column's activity icon. Search rows stretch to 833 pt. | D20, D08, D16, D18, D07 |
| Journal: compose with media, record, save, state of mind | 0441–0445 | Sheets sit on the fold, 653 pt from y 8 in 0444, and leave the bar's buttons visible and dimmed beside them. The add-media menu overlaps the bar; with the keyboard up the four bar buttons end at y 351, above its top at 391. | D04, D12, D25, D19, D08 |
| Journal: read view, new journal, entry menu, Places, Insights, sidebar menu | 0446–0453 | The 320 pt sidebar stays while the detail swaps in place. The floating entry card sits at x 531-940 with sidebar and map undimmed. The sidebar menu is 250 pt at x 20-270, wholly left of the fold. | D22, D01, D13, D08, D09 |
| Safari: article, bookmarks sheet, new tab, tab overview | 0454–0457 | Safari keeps its toolbar in content and shows the status items as a horizontal pill at x 825-931 pt. The bookmarks sheet is 653 pt on the fold; the tab grid runs to 935 pt, so a card's close X sits under the pill. | D27, D03, D04, D02, D18 |
| Translate: languages sheet, camera view, text with keyboard, favourites | 0374–0379 | Sheets share one 653 pt frame on the fold. In camera view the status cluster drops out: gallery and torch sit at y 24-132 in the bar, a mode capsule at y 484-645, and the shutter 21 pt left of the bar. | D34, D04, D03, D19 |
| Shortcuts: editor, icon picker sheet, filter popover, swipe delete | 0321–0324 | The sheet is 653 pt on the fold and dims the bar's four button groups while the status stack stays bright. Editor and library divide at 505 pt, 29 pt right of the fold, so the fold falls inside the editor. | D04, D19, D29, D08 |
| ChatGPT: projects, new chat with keyboard, Images, thread | 0221–0225 | The 320 pt sidebar never moves while the detail swaps. The keyboard runs the full 951 pt and covers the sidebar instead of resizing it; the image grid and carousel cross the fold untouched. | D22, D09, D01, D18, D23 |
| Apple TV: home shelves, search keyboard, episode page | 0260–0262 | Shelf cards start at 34 pt and cross the fold; page dots centre on it. Search rows run x 20-846 pt across the fold. Episode cards sit at 34, 299 and 565 pt, and a fourth starts at 831 pt and runs off the screen. | D07, D16, D14, D18, D03 |
| Claude: the Usage sheet rises, scrolls and expands | 0176–0179 | The 653 pt sheet is centred on the fold, so title, grabber and card centres land on it. It stops about 65 pt short of the bar, and the scrim dims the bar's app buttons but not its status items. | D04, D19, D20 |
| Calendar: sheets, split Day view, New Event with keyboard, left half | 0236–0243 | All sheets share x 149-802 pt on the fold except the last. In Day view the fold is the pane divider and the right pane pins its actions. The same New Event form is 653 pt wide in 0242 and 459 pt in 0243 with no change in window size. | D04, D30, D12, D31, D23 |
| Notes: attachments sheet, keyboard, handwriting sheet, folder overlay | 0157–0161 | The Attachments and Lines and Grids sheets cover both dimmed panes, the pane boundary at 340 pt and the fold. The keyboard overlays both panes from y 391. The 280 pt folder overlay draws over the 340 pt list, which keeps its width. | D04, D05, D06, D25, D26 |
| Stocks: hide the sidebar, actions menu, new watchlist with the keyboard | 0380–0386 | Detail content re-flows from 467 to 787 pt and crosses the fold. The '...' menu grows from the bar capsule with its right edge at 926 pt; the alert, scrim and keyboard span both columns, and the bar capsule vanishes with the keyboard up. | D11, D08, D15, D25, D23 |
| Claude: model and effort inside one sheet, then the left half | 0184–0187 | Navigation inside the sheet keeps its fold-centred frame. In 0186 the same Effort page sits in the left half, x 8-467 pt, with the voice screen beside it and the pane boundary on the fold. | D20, D31, D13, D04 |
| Bear: seven settings pages inside one 653 pt sheet | 0287–0293 | The sheet is 653 pt wide and stops 65 pt short of the bar. Centred titles and art lie on the crease; the Themes grid puts its 15 pt gutter on the fold, x 468-483. | D20, D04, D29 |
| Siri: fold closed, back to history, voice with the bar following the status stack | 0428–0431 | Closed, the persistent sidebar becomes navigation: actions move into the 84 pt bar, content reflows to 0-382 pt, and a mic dot pushes the bar button down 22 pt, from y 175 to 197. | D10, D28, D11 |
| Settings: persistent sidebar, then the page that widens it | 0226–0233 | Until 0232 the fold sits 155 pt inside the detail and cards cross it. One frame puts the pane boundary exactly on x 475.5, like the Music and Podcasts player pages; whether Settings widened on purpose is not shown. | D22, D01, D30 |

## Open questions

Claims the frames could not settle. Each needs a capture the set does not have.

- **A form sheet sits in the left half only (x 8-467 pt, 459 wide) in some states and is fold-centred (x 149-802 pt, 653 wide) in others.** Ten new modal sheets in seven apps are all fold-centred, 600-653 pt. Maps' non-modal panel sits left (x 8-408). No new left-half modal sheet appears, so the trigger for Calendar and Claude is still not in the pixels.
- **System alerts centre on the 0-867 pt content area (x 433.5) rather than on the fold (x 475.5).** No new frame shows a system alert or permission prompt. Weather's 'Allow Notifications' (IMG_0346) is a 653 pt in-app sheet on the fold. Nothing new for either position.
- **Content that crosses the fold at x 475.5 pt, including a button under the crease, has no effect on how it reads or how a touch lands.** Six more frames show content or a control crossing the fold with no seam, and three two-half pages keep a 50 pt gutter on it. Screenshots still cannot show the crease or touch response.
- **The Settings sidebar can widen to 475.5 pt (the fold) instead of its usual 320 pt.** No new frame shows a widened sidebar. Music, Podcasts and Books split full-window pages at the fold, which makes a deliberate fold split for Settings' Wallpaper page plausible; one frame cannot confirm it.
- **The closed display held in landscape shows the portrait layout turned 90 degrees, with no re-layout and no status cluster.** All 62 new frames are open landscape; none is closed landscape. The claim keeps its single frame.
- **Settled: The system, not the app, folds the bar's lower buttons into a '...' overflow when the keyboard opens.** Not a system rule. Music and Games keep their five-icon tab pill under the keyboard, blurred (0308, 0406), as Photos and TV do. Only toolbar buttons in Calendar, Voice Memos and Journal fold; who folds them stays unproven.

## What this set cannot show

- **The crease and touch.** A screenshot shows neither the crease nor where a tap lands, so the
  claims about content crossing the fold (D07, D29) rest on layout alone.
- **Posture.** Whether an open frame was flat or partly folded is not visible, so a left-half
  sheet (D31) cannot be tied to book posture from these frames.
- **Poses absent from the set:** open portrait, tabletop, both Split View halves and picture in
  picture. `apple-reference-screens.md` has Apple's apps in each of them.
