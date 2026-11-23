# guide-craft Banner UX Review (`ux-craft:ux-craft`, Read mode)

## Reading hierarchy and scanability

- **Reader and context:** Developer or founder scanning `fledgeling-plugins` README on GitHub (rendered ~890–900px desktop, ~360–400px mobile). Target comprehension time: under 2 seconds.
- **Primary focal sequence:** (1) Icon silhouette + vermilion tab anchors left (`288px` at 1600w -> `72px` at 400w); (2) `guide-craft` wordmark reads cleanly even at 400px (`94px` -> `23.5px` effective height); (3) one-line essence (`26px` -> crisp at 900px, legible at 400px); (4) right-hand 3-surface folio diagram reinforces multi-surface output without competing with the title.

## Contrast, overflow and copy checks

- **Contrast (WCAG AA >= 4.5:1):** Wordmark `#25211E` on `#F3EFE7` (~13.7:1); essence body `#564D43` on `#F3EFE7` (~7.3:1); lifted vermilion label `#A63812` on `#FFFBF3` (~5.8:1); white text `#FFFDF9` on `#C44D1B` tab pill (~4.7:1).
- **Zero em dashes:** Copy uses commas and full stops only.
- **Zero clipping or overlap:** Fixed `1600x520` layout with explicit `overflow: hidden` and generous `60px+` outer margins on all four sides; right-hand diagram keeps at least `40px` horizontal clearance from the text column.
- **Honest restraint:** No invented metric claims or fake badges on the banner; the right-hand card labels (`WEB GUIDE`, `IOS APP`, `VOICE GUIDE`, `PROVENANCE`) name the actual surfaces the skill builds.
