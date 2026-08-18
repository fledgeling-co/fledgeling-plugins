# Icon notes — `test-campaign`

Direction 2, sub-register (a): porcelain cushion + gel objects. Same register as
`whats-left` and `proctor`, which it sits beside in the marketplace.

## The idea

The coverage grid, honest about its holes. Eight captured frames in a
three-by-three arrangement; the centre one is vermilion, the thing the campaign
actually proved; the ninth is not there at all. In its place is an empty socket
pressed into the cushion, lit by the same top light as everything else, so the
gap is as visible as any pass. That is the plugin's whole argument in one shape,
and it is why the missing cell is drawn rather than simply omitted.

Device #20 from the bank (data-as-glyph abstraction, one accent datum) crossed
with #16 (the icon performs the verb). Differentiated from its neighbours by
glyph type: `whats-left` is a list that thins upward with one card standing
forward, `proctor` is a stack of windows with a dithered edge, this one is a
matrix whose subject is the cell with nothing in it.

## Palette, sampled rather than guessed

Read out of the two sibling PNGs before anything was authored, because reading
*about* a register is not the same as looking at one.

| | value | source |
|---|---|---|
| cushion | `#F8F5EE` → `#E4DDCB` | whats-left `#F6F3EA`→`#E0D9C8`, proctor `#F8F4EC`→`#E9E2D4` |
| inner rim | `#FFFDF8` | both siblings carry one; a flat ground is previous-era |
| quiet frames | `#8B7E6A` → `#665B49`, edge `#544A3B` | the gel register both siblings use |
| accent | `#F79A61` → `#E4652E` | whats-left max-chroma `#E06330`, proctor `#E65017` |
| shadow | `#4A3F2E` | shared with both |

Interior luminance of the siblings measured 139–250 (proctor) and 162–250
(whats-left); this icon sits inside that range.

## Three engines

| | take | outcome |
|---|---|---|
| **A** | `icon.svg` (+ `build_icon.py`) | **ships.** Hand-authored, four named layers. |
| **B** | `icon-engineB-arrow-7ad2c3.svg` | Arrow 1.1. Lost: it drew the ninth cell as a pale filled tile, which is the one thing the icon must not do. Nothing salvaged. |
| **C** | `icon-engineC-0ae063.png` (+ `-masked`) | GPT Image 2 with four reference images (two Tahoe porcelain corpus captures, both siblings). Won the material read; ported into A as parameter edits. |

`audit.html` carries the scored contact sheet with all three, verified by
`audit_sheet.py check` (18 image references, all resolve).

## What measurement caught that the eye did not

Three defects, each found by taking a reading rather than by looking:

1. **Near-white frames on a porcelain cushion measured 1.1:1.** They read as
   white on white at every size. Rubric #7 wants 3:1; the fix was to move the
   frames into the gel register the siblings already use, which now measures
   **4.55:1**.
2. **The accent measured 1.19:1 against its neighbours**, so in grayscale the
   one proven cell was indistinguishable from the other seven and the icon's
   whole reading was carried by hue alone. That is failure mode #3 and a hard
   #10 liability. Darkening the quiet frames took it to **1.87:1**, confirmed on
   a grayscale render.
3. **The first build had zero named layer groups** and `fidelity.py structure`
   failed it. Splitting the lighting out of the frame bodies into its own
   `highlight` plane is what makes #10 true rather than asserted.

The socket itself took three attempts, and the first two failed the same way: a
cell filled a shade lighter than the cushion read as a third kind of tile, and a
cell with a floor plus a rim catch on its lower lip read as a raised pale tile.
Any filled shape in that position is an object. It ships with no fill at all.

## Fidelity

Scored against take C at five sizes, numpy tier (no torch, so luminance + SSIM +
edges only):

```
                  1024      256      128       32       16
pre-layer       0.5992   0.6544   0.7220   0.9188   0.9360
layered         0.5994   0.6560   0.7215   0.9199   0.9366
```

The loop was stopped after one round deliberately. The remaining gap at 1024 is
material richness, and closing it by converging on C would have dragged in three
things C gets wrong: an irregular grid, a warmer palette than the family, and a
flat construction that fails #10 by definition. The skill's own rule applies here
— the rubric outranks the gate, and a gate ACCEPT is evidence rather than a
verdict.

## Known liabilities

- A grid of rounded squares is one move from a generic app-grid glyph. It is the
  drawn absence, not the grid, that makes this icon specific, and a viewer who
  meets it only at 16px may read it as the category.
- Measurably flatter than the raster at 1024. A later round could deepen the
  cushion volume without touching geometry.
- Accent-versus-neighbour separation of 1.87:1 is enough to see but not
  comfortable. A tinted-variant pass should be re-checked rather than assumed.

## Rendering notes

The icon renders through `rsvg-convert`. The banner does too, and that is a
divergence from the siblings worth knowing: they keep the banner artwork in
`banner-src.html` and screenshot it with a browser, but no HTML renderer here
lays that page out at the authored width. QuickLook clips the body at its own
viewport and cut the title off; the Obscura engine does not implement flex, so
`flex-direction` came back `column` against an unset property and `gap` came back
`normal` against an authored `18px`. Rather than tune the artwork against a
renderer that is wrong, the banner is `banner-src.svg`, rasterised by the same
tool that already renders the icon.

The same engine gap means `audit.html` itself has not been read in a browser that
lays it out correctly. Its images were verified to resolve, and the icons in it
were read directly from the PNG renders at 128 / 64 / 48 / 32 / 16 rather than
through the sheet, so the judgement behind the scores does not depend on it.

```bash
python3 build_icon.py > icon.svg
for s in 1024 256 128; do rsvg-convert -w $s -h $s icon.svg -o icon-$s.png; done
rsvg-convert -w 3200 -h 840 banner-src.svg -o banner.png
```
