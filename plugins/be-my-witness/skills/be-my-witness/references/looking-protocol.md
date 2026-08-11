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

### Pass 2 — crop to the no-downscale ceiling, not to a multiplier

**A zoom factor is the wrong unit.** "2×" says nothing about whether the model will
downscale your crop back below legibility on receipt, and it usually will.

The unit that matters is the model's **no-resize ceiling** and the **text height that
survives it**:

- Crop so the region's **long edge lands at or under the ceiling** — 1568 px on the
  standard tier, 2576 px on Claude 4.7 and later. Images above it are downscaled,
  aspect preserved, before the model sees anything.
- Crop so **body text renders at ≥7 px** in the image the model receives. Accuracy
  falls off sharply below 7 px of text height; classical OCR shows a comparable ~6 px
  floor.
- Anything **under 200 px** on a side invites hallucination outright.

Worked, because the arithmetic is the whole argument. A 1280 px-wide page running to
4320 px tall is downscaled by 0.363× on the standard tier, so 14 px body text arrives
at **~5.1 px** — under the cliff, unreadable no matter how the prompt is worded. On
the high-resolution tier the factor is 0.596× and the same text lands at ~8.3 px,
barely over. Cut that page into **1280×720 tiles and nothing is downscaled at all**:
the text stays at 14 px, twice the cliff. Cost: about 952 visual tokens for the
unreadable whole page against about 1196 per readable tile.

That is the mechanical case for cropping. It is not a prompting preference.

**Crop size is not monotonic, and the optimum is model-dependent.** On ScreenSpot-Pro,
OS-Atlas-7B scored 25.1% at 512², 34.2% at 768², **40.2% at 1024²** and 40.1% at
1280², while UGround-7B peaked at 768². Too small loses context; too large exceeds
capacity. Around **1024²** is a reasonable default to start from and worth
re-measuring per model.

```bash
python3 scripts/prescan.py shot.png --json > /tmp/ps.json
python3 scripts/crop.py shot.png --tiles-from /tmp/ps.json --scale 2 --out /tmp/tiles
```

Inspect, in this order:

1. **Every region the expected output names.** These are the gate.
2. **The tiles the pre-scan chose**, which rank cells by real content.
3. **Any region a Pass-1 structural observation pointed at.**

**Keep one parent-context crop.** Cropping region by region can hide the defects
that only exist *between* regions: sibling misalignment, an overflow that starts in
one region and lands in another, and anything viewport-level. So alongside the tight
crops, retain one crop of the parent container at a lower zoom, and check alignment
across siblings there. A protocol made only of tight crops trades one blindness for
another.

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

## What the evidence does and does not say

The strongest public numbers for cropping are **GUI grounding** results, not defect
detection. On ScreenSpot-Pro, Qwen3-VL-8B scored 53.51% on the full image, 65.59% at
2x, and 71.79% at roughly 3.3x zoom (Spatially Stable GUI Grounding, 2026). A separate
adaptive-zoom preprint reports up to +13.4 points on the same benchmark, with larger
gains specifically on icon and text targets (UI-Zoomer, 2026).

Those measure whether a model can *locate* a target. This skill asks whether a
rendered surface is *wrong*, which is a different task, and a direct benchmark for it
does not appear to exist publicly. So read the protocol as: strongly supported by
adjacent evidence and by the mechanism (a defect below the resolving power of the
image cannot be reported), not as a measured claim about regression detection.

Cost moves the other way. Apple's FastVLM work is explicit that resolution buys
accuracy and spends compute and latency, and Microsoft's Phi-4-reasoning-vision
scored 9.2% at 2048 visual tokens against 17.5% at 3600 on the same benchmark. Crop
selectively rather than uniformly; that is what the tile ranking is for.

Provenance for all of the above: `docs/deep-research/`.

## The failure this protocol exists to prevent

Rendering an image is not seeing one, and running a crop script is not looking at its
output. A contact sheet whose images fail to load renders as an empty page, and no
script and no summary will ever mention it. **Open what you made.** Read the crop.
Then ask it the productive question — not "is this done?" but **"what is wrong with
this?"** The same pixels answer those two questions differently, and only one of them
finds anything.
