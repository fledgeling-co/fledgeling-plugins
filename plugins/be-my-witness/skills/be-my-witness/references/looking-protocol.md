# The looking protocol

A vision model reports what it can resolve. Hand it a 1440×900 screenshot whole and
it reports that the page looks fine, because at the scale it was given, it does: body
text is roughly 30 pixels of glyph height, a 2px spacing error is a fraction of a
pixel, and a wrong font weight is invisible. It is not lying. It is answering a
question about an image that does not contain the evidence.

So the protocol is about **sampling**, and the rule underneath it is simple: a defect
you could not have resolved is a defect you will clear.

## Capture first, or none of this works

No protocol recovers detail that was never sampled. Whatever produces the screenshot
must capture at **deviceScaleFactor 2 or higher**. A 1× capture upscaled afterwards
is interpolation, not information — it looks sharper and carries nothing new, which
is the worst combination available because it hides its own poverty.

If you are handed a 1× capture, say so in the verdict and lower your confidence. Do
not silently proceed as though the sample were adequate.

## The three passes

### Pass 1 — the whole frame, once, for structure only

Look at the full image at whatever scale it comes. Ask exactly three questions:

- What regions exist, and in what order?
- Does the skeleton match the reference's skeleton — same bands, same columns, same
  nesting?
- Is anything conspicuously absent or duplicated?

Then stop. Any finding about type, colour, spacing or alignment made at this scale is
a guess wearing a finding's clothes. Record structural observations; defer everything
else.

### Pass 2 — region by region, at ≥2× effective scale

This is where every real finding comes from.

```bash
python3 scripts/prescan.py shot.png --json > /tmp/ps.json
python3 scripts/crop.py shot.png --tiles-from /tmp/ps.json --scale 2 --out /tmp/tiles
```

Inspect, in this order:

1. **Every region the expected output names.** These are the gate. If the expectation
   says "the total row reads 38,000", the crop containing that row gets looked at,
   full stop.
2. **The tiles the pre-scan chose.** It ranks cells by how much real content they
   carry, so these are where a defect can actually be seen.
3. **Any region a Pass-1 structural observation pointed at.**

**Go to 3× when** the region contains text under ~13px, a hairline border, a focus
ring, an icon under 20px, or any judgement about letter-spacing or weight. Those live
below the resolving power of 2× on a dense surface.

### Pass 3 — paired crops, same rectangle from both

When a reference exists, never compare a crop of one against the whole of the other.
That is the framing error again, and it produces confident nonsense.

```bash
python3 scripts/crop.py shot.png --pair mock.png --region 0,0,480,300 --scale 2 --out /tmp/pair.png
```

The pair goes into one image with a divider, so what the model sees is like-for-like.
Where the two images have different dimensions, decide what "the same rectangle"
means before cropping — usually by normalising to a shared anchor (the top-left of
the content area, not of the viewport) and stating the normalisation in the verdict.

## How many tiles

Enough to cover the regions that carry meaning, and no more. Six is a sensible
default for a full page; a card-sized slice may need two. What matters is not the
count but that **you report it**: "6 of 7 regions inspected, footer not reached" is a
different result from "6 regions inspected", and they currently serialise the same.

An unstated denominator is how 904 passing assertions sat on top of a real defect in
a shipped parity oracle: the failing component was not among the landmarks, and the
oracle only ever loaded one route. Coverage that is not stated is coverage that is
assumed.

## What to record per crop

For each crop you actually looked at:

- the rectangle, in source pixels, and the scale it was viewed at
- what you were checking for
- what you saw, in terms specific enough to be wrong
- the file path, so a human can open the same image

"Header looks fine" is not a record. "Header crop (0,0,520,96) at 2×: the price pill
sits 8px from the bell, the mock shows ~14px; both carry the same three controls in
the same order" is.

## The failure this protocol exists to prevent

Rendering an image is not seeing one, and running a crop script is not looking at its
output. A contact sheet whose images fail to load renders as an empty page, and no
script and no summary will ever mention it. **Open what you made.** Read the crop.
Then ask it the productive question — not "is this done?" but **"what is wrong with
this?"** The same pixels answer those two questions differently, and only one of them
finds anything.
