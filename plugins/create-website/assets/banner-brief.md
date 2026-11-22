# create-website banner brief

Written before `banner-src.html` existed, so the render has something to be measured against.
`design-craft:design-craft` owns the composition decisions below; `ux-craft:ux-craft` (Read mode)
owns the reading order and the cuts. Both ran in autonomous mode, so every question became a
stated assumption rather than a round of asking.

## Essence line

> Whole websites, section by section, with motion that still works when it can’t move.

Kept close to the supplied line. One sentence, no em dash, curly apostrophe. The bolded tail is
`still works when it can’t move`, because that clause is the only thing in the line a reader
could not have guessed from the plugin's name.

## What design-craft decided

**Visitor mode: Persuade.** A marketplace banner is read once, in a README column, by someone
deciding whether to keep reading. Nothing here is operated, so scanability outranks density and
the artifact leads.

**The composition is derived from `build_icon.py`, not from a sibling banner.** Each borrowed
fact and what it drives:

| Icon constant | Value | What it sets in the banner |
|---|---|---|
| `GROUND_HI/MID/LO` | `#FDFCF9` `#F3EFE7` `#E7E1D5` | the banner's ground ramp, same three stops at 0 / 55 / 100% |
| `ground` gradient geometry | `(330,0) → (620,1024)` | the ramp's angle: `atan(290/1024) = 15.8°` off vertical, so `164deg` |
| `VIGNETTE` | `#C4B899` at 0.22, centred `0.42 / 0.30`, inner edge 0.60 | the banner's corner vignette, same centre, same opacity |
| `LIGHT_DX, LIGHT_DY` | `-0.62, -0.78` | every shadow in the banner offsets along `(+0.62, +0.78)`: the icon plate at `(16, 20)` and `(5, 6)`, the plates in the right-hand device at `(2, 3)` |
| `SECTIONS[0]` hero ember | `#F7995F #EC6A31 #D14E1C`, seat `#6E2409` | the one accent, spent only on the arrival plate in each track and on the numerals |
| `SECTIONS[1]` middle stone | `#BCAA8C` wall, seat `#5E4F36` | rails, ghost plates, and the essence line's text colour |
| `SECTIONS[2]` base graphite | `#332C26` / `#201B18` | the wordmark at `#241F1B`, which sits between those two |
| `PITCH_HERO : PITCH_BASE` | `215 : 165` = 1.303 | the right-hand device's row pitch (56px) against its track inset (43px), same ratio |
| `CORNER_R`, `THICK` | `34`, `32` | the icon plate's shadow distance (32) and the text column's gap from it (64 = 2 × THICK) |

**Accent discipline.** The ember appears in exactly two roles: the arrival plate repeated four
times in the device, and the numeral in the caption. Raw `#EC6A31` is used as a fill only; at
mono body size the accent is the lifted `#A83A14`, which measures 5.6:1 on the ground where the
raw ember measures about 2.6:1.

**Type.** Instrument Sans for the wordmark and essence line, IBM Plex Mono for the measured
labels, both linked from Google Fonts. Instrument Sans is the plurality face across this
marketplace's banners and `brand-and-docs.md` asks for a set wordmark rather than a new one each
time, so this is the drift-reducing choice rather than a fresh reach. Nothing is set in a local
macOS face: the two banners that did that are unreproducible and are the reason check 3 exists.

**The right-hand device does not repeat the icon.** An exploded stack beside an exploded stack
is one idea drawn twice. The device instead draws what the icon cannot: four motion paths
(`full`, `reduced-motion`, `no webgl`, `touch`), each a rail whose left end differs and whose
right end is the same ember arrival plate. The shared right edge is the whole argument of the
essence line, made visible.

## What ux-craft decided (Read mode)

**Reading order, first to third.** First fixation is the icon, because it is the largest mass
and holds the only warm colour in the left half. First *read* is the wordmark, set at 86px and
sitting at the icon's optical centre line. Second is the essence line, one step down in size,
weight and colour, held to a 620px measure so it breaks to two lines rather than running the
width of the banner. Third is the device, deliberately quieter: 17px mono, stone grey, no
display weight anywhere in it. Nothing in the right third competes with the wordmark.

**What was cut.**

- A category pill beside the wordmark. It would say what the essence line already says, and a
  second element at display weight flattens the hierarchy the wordmark depends on.
- A second sentence under the essence line. One line is the format; two is a paragraph.
- Repeating "section by section" as a label under the device. A label that restates the sentence
  above it is a slot filled rather than a slot earned.
- A per-row count of sections. The number is not fixed by the skill, so it would be a claim the
  artifact cannot stand behind.

**What the labels may claim.** `full`, `reduced-motion`, `no webgl` and `touch` are the four
paths the skill actually builds for every section, so the device is evidence rather than
decoration. The caption states the count and nothing else.

## Accepted risks

- The mono labels are 17px, which stops being readable below about 700px of displayed width.
  That is inside the rubric, which asks for the wordmark at 400px and the wordmark plus the
  essence line at 900px, not for the device.
- The device's left-end differences (trail, fade, flat plate, tap ring) are small marks. If the
  render shows any of them reading as a smudge rather than a sign, the fix is to cut that mark
  and let the label carry the row, not to enlarge it.
