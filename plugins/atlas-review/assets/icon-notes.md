# atlas-review icon: what was built and why

## The concept that ships

**The stroke you broke to prove it.** The capital A of the Atlas script wordmark,
re-poured in the sibling's material, with one clean fracture cut square across its
descending stem and vermilion filling the void.

`atlas-publish` and `atlas-review` are one letterform doing opposite things. The sibling
stands a vermilion gate where the next stroke would begin and leaves the porcelain past
it bare: a stroke stopped, because publishing reaches phones and going live is a person's
move. This one takes the same stroke and cuts it, because the skill's claim is that a
check which cannot fail is not a check, and the only way to find out whether a test can
fail is to break the thing it covers and watch.

The break is not damage. The break is the evidence. So the cut has two flat parallel
faces, the letterform continues cleanly on both sides, and the mark holds.

## The one liberty, and the one thing that is genuinely new

Every material constant in `build_icon.py` is the sibling's, lifted rather than
re-derived: the porcelain ground, the warm-lit graphite ramp, the vermilion, the
three-part cast shadow, the rim-and-bounce pair. The two icons have to sit on a page
together, and a value that drifts by a few percent reads as a mistake rather than as a
family.

What is new is the groove. The cut opens two boundaries the letterform did not have, and
neither the rim mask nor the bounce mask can see them: both are keyed on the whole glyph's
silhouette, so an edge that only exists because of the cut goes completely unlit. Left
that way the void reads as a painted stripe. Two hand-placed bands fix it, one dark on the
face above the void and one light on the face below, plus a floor that is occluded at the
top edge and brightens toward the bottom. That construction is the addition this
commission makes to the family, and it is written up in the build script rather than left
in the SVG.

## Measured, not eyeballed

The cut's position and angle come from rasterising the glyph and scanning it. Down rows
490 to 565 the descending stem is the only ink on its scanline, with open porcelain on
both sides, so the two faces have nothing to touch and cannot read as an overlap. Its
centreline runs at dx/dy of -0.4254 and its perpendicular thickness holds at 40 units, so
the cut sits at 23.04 degrees and crosses at right angles to the stroke's own direction.

## What was tried and dropped

- **A cut reaching 130 units.** The band ran on past the stem and clipped the bowl's upper
  arch as well. Two voids read as damage. One reads as a measurement.
- **Cutting the bowl's left flank instead.** It splits the letter's enclosure, and a broken
  enclosure says the mark did not survive. Severing the stem leaves the bowl whole.
- **A gap of 78 tile px.** The stem reads severed rather than cut, and the claim is that
  the mark holds. 52 closes up too far at 24px. 66 ships.
- **An open void, built and scored as take A2.** The cut goes clean through to porcelain
  with the accent surviving only as a hair on the rim. It is the more restrained object at
  1024 and the more honest one conceptually, and it loses the only test that mattered: by
  32px the void has closed to a pale nick and in grayscale it is gone entirely.
- **A bright cream lip on the lower face at 0.52 opacity.** It stopped being a lit edge and
  became a gloss streak down the stroke, which is the failure the sibling's own notes warn
  about for cream on a warm-lit body. A cut face is narrow and hard, never polished.

## What the engines were for

Engine B did not run: Arrow refused on a gateway key over its budget. Engine A was widened
to two genuinely different hand-authored takes in its place, which is the sanctioned
substitution and is recorded here because a missing engine is a deviation rather than a
default.

Engine C is worth its cost twice over. It arrived independently at this composition from
the brief alone, which is the useful result: the concept survives a reader who was not in
the room. It also drew the cut as a hairline, which vanishes by 32px, and it baked a
rounded-rect corner instead of the family superellipse. Its one real win is the body,
which carries a rounder and deeper under-edge than the master did, and `EXTRUDE` went from
the sibling's 11 to 15 on the strength of it. At 19 the shelf detaches and reads as a
second object under the letter.

## Known liabilities

1. **Identity rests on 0.54% accent coverage.** A Tinted variant that recolours the accent
   returns this icon to the sibling's silhouette, and the pair stops being
   distinguishable. This is the sharpest open question here.
2. **At 16px the cut is roughly one warm pixel.** What survives the squint is the
   letterform and its mass rather than the device, which is the same bargain the sibling
   makes with its gate.
3. **The groove's faces are lit by hand-placed bands.** A renderer that treats those blurs
   differently will change the cut's depth before it changes anything else in the icon.
4. **Rendering was verified in librsvg only.** The rim, glow and cast-shadow filters want a
   spot-check in Safari.

## Files

| File | What it is |
|---|---|
| `icon.svg` | the layered master that ships, emitted by `build_icon.py` |
| `build_icon.py` | geometry and material as named constants; every round is a parameter edit here |
| `icon.png`, `icon-256.png`, `icon-128.png` | the marketplace exports |
| `icon-email-48.png` | the digest-row derivative |
| `glyph-path.txt`, `squircle-path.txt` | the brand letterform and the family silhouette |
| `icon-engineA2-open-3f19c4.*` | the open-void alternate, built to lose the size test |
| `icon-engineC-fracture-*.png` | the two raster takes |
| `audit.html`, `audit-renders/` | the contact sheet and its renders |
| `banner-src.html`, `banner.png` | the README banner and its source |
