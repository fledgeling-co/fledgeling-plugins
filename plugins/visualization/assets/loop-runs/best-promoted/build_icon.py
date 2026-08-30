#!/usr/bin/env python3
"""Engine A — the hand-authored layered SVG master for `visualization`.

Run it to regenerate `icon.svg` (the master) plus the two losing Engine A takes it is
judged against. Geometry and material live here as named constants, so a later fidelity
round or a targeted preference edit is a parameter change rather than path surgery.

    python3 build_icon.py            # writes icon.svg, icon-A2-fourbar.svg, icon-A3-edgebleed.svg
    python3 build_icon.py --export   # ... and rasterises icon.png / -256 / -128 / -16

DIRECTION: 2 Tahoe Gel-Glass, sub-register (a) — porcelain cushion tile carrying a coloured
gel object. Runner-up: 8 Instrument Emblem, which is the obvious pick for a chart skill and
was rejected for exactly that reason: it puts the product's artifact on the tile and says
"analytics app", not *this* skill. The gel-glass register lets the composition carry an
argument instead of a category.

THE GLYPH, subject-mined. The skill's central honesty rule is that a length-encoded bar
starts at zero. So the subject is not a bar chart; it is the thing a bar chart is measured
FROM. Three graphite bars of unequal height stand on one vermilion rule that runs the full
width of the glyph and glows.

SIGNATURE MOVE: the baseline is the hero and the bars are the context. Every reading of a
bar chart puts the light on the bars; this one puts it on the datum, because the datum is
what makes the bars mean anything. It is authored in the material as well as the layout —
`BOUNCE_*` warms the lower 168px of every bar with the rule's own light, so the bars are
visibly lit BY the baseline rather than merely standing near it, and the shared
`userSpaceOnUse` graphite field means one light governs the whole scene.

FAMILY FIT, and the deliberate difference from the near neighbour. `warrant` is five slate
bars of DECREASING WIDTH, laid horizontally as a descending sequence, with only the
narrowest lit and resting on the surface while the others float — the accent is a bar.
Here the bars are vertical, of unequal HEIGHT in no order, every one of them standing on
and touching a single rule, and the accent is the rule rather than any bar. Shared
porcelain ground and graphite gel keep them a family; opposite axis, opposite accent
target and opposite contact story keep them apart in a grid. `should-compact` is two
graphite masses held apart by a vertical lit seam — light in a gap; here the light is a
solid object that everything rests on. `trawl` owns the dark register outright and this
does not go near it.

VALUES SAMPLED FROM THE CORPUS, not assumed (`references/corpus/apple-2026/`, measured
2026-08-30 with Pillow rather than described):
  · apple-26 (Reminders) porcelain runs (255,255,255) at the top to (236,235,236) at the
    bottom — a vertical delta of 19, brightest at the TOP, so the key light is above.
  · apple-19 (Slack) and apple-28 (Photos) agree: 255 -> ~249 over the same strip.
  · the darkest in-tile pixel across apple-19/23/26/28 is a cool near-black at
    (26,29,32) / (31,33,37) / (26,29,31) / (25,28,31) — blue above red in every one, which
    is why GRAPHITE_LOW is (26,32,39) and not a neutral grey.
  · apple-26's dots each sit in a soft tinted halo well that bleeds onto the porcelain;
    that is the construction GLOW_* copies for the rule.
"""

from __future__ import annotations

import argparse
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
S = 1024

# ── geometry ────────────────────────────────────────────────────────────────────────────
# The focal is measured across the RULE, because the rule is the focal: 644px = 62.9% of
# the tile, inside the 55-65% band the composition constants call for.
BAR_W = 132.0          # wide enough that a bar is ~2.1px at 16, and a gap ~1.2px
BAR_GAP = 78.0         # the gaps are what die first at 16px, so they are sized for that
                       # and not for how the 1024 hero looks
BAR_H = (300.0, 430.0, 206.0)
# Deliberately NOT monotonic. A descending run is `warrant`'s glyph and it reads as a
# ranking; medium-tall-short reads as measurement, which is this skill's subject.
FOUR_BAR_W = 104.0     # take A2's narrower bars — the 16px cost is the finding
FOUR_BAR_GAP = 62.0
FOUR_BAR_H = (268.0, 398.0, 190.0, 322.0)

RULE_H = 52.0          # the datum's thickness, chosen by measurement rather than eye. Swept
                       # 34/44/52/60/68 and read the peak chroma out of the 16px render:
                       # 95 / 126 / 152 / 172 / 189. 34 leaves the rule a 0.53px sliver that
                       # desaturates to (176,107,81) — the accent dies exactly where the
                       # non-negotiable 16px check lives. Above 52 the gain flattens (+20,
                       # then +17) while the rule visibly thickens into a plinth, which is a
                       # different object. 52 is the knee.
RULE_OVERHANG = 104.0  # how far the rule runs past the outermost bar on each side. This is
                       # the whole argument: the datum is wider than the data it carries, so
                       # it reads as something the bars were measured AGAINST rather than a
                       # plinth cut to fit them. 104 is the reference's own mean (r02): the
                       # corpus-steered raster take overhangs 98 left and 110 right, against
                       # the 46 first drafted, on a bar group within 3% of the same width.
RULE_RX = 12.0         # soft-cut ends. At RULE_H/2 it becomes a capsule, which reads as a
                       # pill-shaped object rather than a ruled line.
BAR_SINK = 4.0         # bars press this far into the rule, so no hairline seam survives
                       # rasterisation and the rule's bright core stays unbroken.
BAR_RX = 30.0          # generous top-corner rounding: gel is poured, not cut. Bottoms stay
                       # square, because a rounded foot cannot stand on anything.
CAP_H = 30.0           # the lit top face
AO_H = 16.0            # contact darkening on the rule at each bar's foot

RULE_TOP = 698.0       # solved for an optical centre of y=500: the figure runs from
                       # RULE_TOP - max(BAR_H) = 268 to RULE_TOP + RULE_H = 732.
BLOOM_RY = 118.0       # the halo well's vertical reach (r01). The reference's warm chroma
                       # on the porcelain is 197 at the rule and 0 by dy=110, so a well this
                       # tight is what the measurement says — not the 182 first drafted.
BLOOM_OVER = 26.0      # how far the well spreads past the rule's ends. The reference falls
                       # from 64 to 9 within 20px past the end, so the glow is bounded by
                       # the object rather than floating free of it.
BOUNCE_H = 120.0       # how far the rule's light climbs each bar. At 168 with the stops
                       # below at .40 the feet read as rust rather than as reflected light —
                       # the warm term stayed visible through the 32px downsample as a brown
                       # band, and a graphite bar that goes brown has changed material.

# ── material ────────────────────────────────────────────────────────────────────────────
GROUND_TOP, GROUND_MID, GROUND_BOT = "#FFFFFF", "#F7F6F3", "#E6E4E0"
VIGNETTE = "#1B1F24"

# Cool graphite, per the measured corpus darkest pixel: blue above red at every stop.
GRAPHITE_TOP = "#59636E"
GRAPHITE_UP = "#39424C"
GRAPHITE_MID = "#262E37"
GRAPHITE_LOW = "#1A2027"
EDGE_DARK = "#0E1319"   # the darkened core between the two edge catches
EDGE_CATCH = "#B9C6D6"  # the frosted catch on each turned edge. Cool, and lighter than
                        # GRAPHITE_TOP, so the catch reads as light passing through the
                        # body rather than as a rim drawn onto it. The far edge gets a
                        # narrower, weaker catch than the near one — one light, not two.

# Vermilion, kin to Fledgeling's #C4622D and deliberately redder than `should-compact`'s
# #FF7A2E so the two accents are not mistaken for one another at a glance.
RULE_DEEP = "#8C2E0F"
RULE_BODY = "#C43F16"
RULE_MID = "#E85F22"
RULE_HOT = "#FF9A4E"
RULE_LIP = "#FFE3C4"
GLOW = "#F26A28"

RIM = "#FFFFFF"
SHADOW = "#241F1C"      # warm-leaning, because the surface it falls on is warm-lit


ROUND_CATCH = """      <stop offset="0" stop-color="{EDGE_CATCH}" stop-opacity=".34"/>
      <stop offset=".022" stop-color="{EDGE_CATCH}" stop-opacity=".12"/>
      <stop offset=".057" stop-color="{EDGE_DARK}" stop-opacity=".34"/>
      <stop offset=".5" stop-color="{EDGE_DARK}" stop-opacity=".19"/>
      <stop offset=".943" stop-color="{EDGE_DARK}" stop-opacity=".29"/>
      <stop offset=".978" stop-color="{EDGE_CATCH}" stop-opacity=".07"/>
      <stop offset="1" stop-color="{EDGE_CATCH}" stop-opacity=".21"/>"""

# Below 96px: the plain roundness fall. No catch, maximum figure-ground.
ROUND_FLOOR = """      <stop offset="0" stop-color="{EDGE_DARK}" stop-opacity=".46"/>
      <stop offset=".18" stop-color="{EDGE_DARK}" stop-opacity=".05"/>
      <stop offset=".62" stop-color="{EDGE_DARK}" stop-opacity="0"/>
      <stop offset="1" stop-color="{EDGE_DARK}" stop-opacity=".30"/>"""


def squircle() -> str:
    return (HERE / "squircle-path.txt").read_text().strip()


def bar_path(x: float, y: float, w: float, h: float, rx: float) -> str:
    """A standing bar: rounded top corners, square feet.

    A capsule cannot stand on a line — the contact degenerates to a tangent point and the
    whole "every bar touches the datum" claim goes with it. So the radius is spent entirely
    on the top, where the poured-gel read lives.
    """
    r = min(rx, w / 2, h)
    return (f"M{x:.1f},{y + h:.1f} L{x:.1f},{y + r:.1f} "
            f"A{r:.1f},{r:.1f} 0 0 1 {x + r:.1f},{y:.1f} "
            f"L{x + w - r:.1f},{y:.1f} "
            f"A{r:.1f},{r:.1f} 0 0 1 {x + w:.1f},{y + r:.1f} "
            f"L{x + w:.1f},{y + h:.1f} Z")


def cap_path(x: float, y: float, w: float, rx: float, cap_h: float) -> str:
    """The bar's lit top face — the same rounded shoulders, cut flat at cap_h."""
    return bar_path(x, y, w, cap_h, rx)


def layout(widths_h, bar_w: float, gap: float):
    n = len(widths_h)
    span = n * bar_w + (n - 1) * gap
    x0 = (S - span) / 2
    xs = [x0 + i * (bar_w + gap) for i in range(n)]
    return xs, span


def defs(fig_top: float, rule_top: float, rule_h: float, small: bool = False) -> str:
    """One light field for the whole scene.

    The graphite ramp is `userSpaceOnUse` across the figure's full height rather than
    per-bar `objectBoundingBox`, so a short bar samples only the lower, darker part of the
    same field a tall bar samples all of. Per-object ramps would give three separately-lit
    objects, which is the single-light-model rubric check failing quietly.
    """
    round_stops = (ROUND_FLOOR if small else ROUND_CATCH).format(
        EDGE_CATCH=EDGE_CATCH, EDGE_DARK=EDGE_DARK)
    return f"""
    <clipPath id="tile"><path d="{squircle()}"/></clipPath>

    <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{GROUND_TOP}"/>
      <stop offset=".54" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_BOT}"/>
    </linearGradient>

    <radialGradient id="vignette" cx=".5" cy=".44" r=".74">
      <stop offset=".60" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="1" stop-color="{VIGNETTE}" stop-opacity=".075"/>
    </radialGradient>

    <linearGradient id="innerRim" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{RIM}" stop-opacity=".92"/>
      <stop offset=".5" stop-color="{RIM}" stop-opacity="0"/>
    </linearGradient>

    <!-- the scene's one light, shared by every bar -->
    <linearGradient id="graphite" gradientUnits="userSpaceOnUse"
                    x1="0" y1="{fig_top:.1f}" x2="0" y2="{rule_top:.1f}">
      <stop offset="0" stop-color="{GRAPHITE_TOP}"/>
      <stop offset=".30" stop-color="{GRAPHITE_UP}"/>
      <stop offset=".70" stop-color="{GRAPHITE_MID}"/>
      <stop offset="1" stop-color="{GRAPHITE_LOW}"/>
    </linearGradient>

    <!-- The edge catch (r03), and the one relationship on this icon that was authored
         backwards before it was measured. Across the reference's tall bar the luminance
         runs 128 / 108 / 91 / 94 / 92 / 100 / 135 from edge to edge: BRIGHT at both
         edges, darkest through the middle. That is a translucent body catching light on
         its turned edges. The first draft was a roundness fall — dark edges, bright core
         — which is an opaque cylinder, and it read as one.

         Floored below 96px (`small=True`), and that is a resolution fact rather than a
         taste call. At 32px a 132px bar is 4.1 pixels wide, and two lit edges plus a
         darker core is three values in four pixels when antialiasing has already spent
         two of them on the silhouette. Measured: the catch lifts the render's 10th
         percentile from 0.392 to 0.476 and drops self-contrast at 32px from 0.600 to
         0.535, past the gate's 6% floor — identically at every amplitude from 0.20 to
         0.40 and at every catch width from 2.2% to 5.5%, because the catch is not
         brightening the dark pixels, it is deleting them. Not an amplitude to tune. -->
    <linearGradient id="round" x1="0" y1="0" x2="1" y2="0">
{round_stops}
    </linearGradient>

    <linearGradient id="cap" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{RIM}" stop-opacity=".34"/>
      <stop offset=".22" stop-color="{RIM}" stop-opacity=".07"/>
      <stop offset="1" stop-color="{RIM}" stop-opacity="0"/>
    </linearGradient>

    <!-- THE SIGNATURE, in material: the rule's light climbing every bar. -->
    <linearGradient id="bounce" gradientUnits="userSpaceOnUse"
                    x1="0" y1="{rule_top - BOUNCE_H:.1f}" x2="0" y2="{rule_top:.1f}">
      <stop offset="0" stop-color="{GLOW}" stop-opacity="0"/>
      <stop offset=".55" stop-color="{GLOW}" stop-opacity=".06"/>
      <stop offset="1" stop-color="{RULE_HOT}" stop-opacity=".26"/>
    </linearGradient>

    <!-- the datum, in cross-section: lip at the lit top edge, hot core just under it,
         body, then a deep shaded underside where it meets the porcelain -->
    <linearGradient id="rule" gradientUnits="userSpaceOnUse"
                    x1="0" y1="{rule_top:.1f}" x2="0" y2="{rule_top + rule_h:.1f}">
      <stop offset="0" stop-color="{RULE_LIP}"/>
      <stop offset=".16" stop-color="{RULE_HOT}"/>
      <stop offset=".42" stop-color="{RULE_MID}"/>
      <stop offset=".78" stop-color="{RULE_BODY}"/>
      <stop offset="1" stop-color="{RULE_DEEP}"/>
    </linearGradient>

    <!-- the ends fall off, so the rule reads as one lit length rather than a painted bar -->
    <linearGradient id="ruleEnds" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{RULE_DEEP}" stop-opacity=".55"/>
      <stop offset=".07" stop-color="{RULE_DEEP}" stop-opacity="0"/>
      <stop offset=".93" stop-color="{RULE_DEEP}" stop-opacity="0"/>
      <stop offset="1" stop-color="{RULE_DEEP}" stop-opacity=".55"/>
    </linearGradient>

    <!-- the halo well (r01). Fitted to the reference rather than eyeballed: chroma on
         the porcelain beside the rule falls 197 / 153 / 77 / 34 / 13 / 0 at dy =
         0 / 20 / 40 / 60 / 80 / 110, so the stops below are that curve and BLOOM_RY is
         that reach. The first draft had a faint 182px veil peaking at chroma 19 against
         the reference's 198 — a coloured bar rather than an emitter. -->
    <radialGradient id="bloom" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="{RULE_HOT}" stop-opacity=".82"/>
      <stop offset=".18" stop-color="{GLOW}" stop-opacity=".60"/>
      <stop offset=".37" stop-color="{GLOW}" stop-opacity=".28"/>
      <stop offset=".62" stop-color="{GLOW}" stop-opacity=".09"/>
      <stop offset="1" stop-color="{GLOW}" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="contact" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="{SHADOW}" stop-opacity=".30"/>
      <stop offset=".58" stop-color="{SHADOW}" stop-opacity=".09"/>
      <stop offset="1" stop-color="{SHADOW}" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="ao" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#3B1206" stop-opacity=".30"/>
      <stop offset="1" stop-color="#3B1206" stop-opacity="0"/>
    </linearGradient>"""


def svg(bar_h=BAR_H, bar_w=BAR_W, gap=BAR_GAP, edge_bleed=False, small=False,
        title="visualization") -> str:
    xs, span = layout(bar_h, bar_w, gap)
    fig_top = RULE_TOP - max(bar_h)

    if edge_bleed:
        rule_x0, rule_w, rule_rx = -8.0, S + 16.0, 0.0
    else:
        rule_x0 = xs[0] - RULE_OVERHANG
        rule_w = span + 2 * RULE_OVERHANG
        rule_rx = RULE_RX
    rule_cx = rule_x0 + rule_w / 2

    bars, caps, bounces, aos = [], [], [], []
    for x, h in zip(xs, bar_h):
        d = bar_path(x, RULE_TOP - h, bar_w, h + BAR_SINK, BAR_RX)
        bars.append(
            f'      <path d="{d}" fill="url(#graphite)"/>\n'
            f'      <path d="{d}" fill="url(#round)"/>\n'
            f'      <path d="{d}" fill="none" stroke="{RIM}" stroke-opacity=".15" stroke-width="2"/>')
        caps.append(f'      <path d="{cap_path(x, RULE_TOP - h, bar_w, BAR_RX, CAP_H)}" fill="url(#cap)"/>')
        bounces.append(f'      <path d="{d}" fill="url(#bounce)"/>')
        aos.append(f'      <rect x="{x - 9:.1f}" y="{RULE_TOP + BAR_SINK:.1f}" '
                   f'width="{bar_w + 18:.1f}" height="{AO_H:.1f}" fill="url(#ao)"/>')

    nl = "\n"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">
  <title>{title}</title>
  <desc>Three graphite bars of unequal height standing on one glowing vermilion baseline,
        on a porcelain cushion tile. The baseline is the focal element.</desc>
  <defs>{defs(fig_top, RULE_TOP, RULE_H, small)}
  </defs>

  <g clip-path="url(#tile)">

    <g id="bg">
      <!-- the cushion. A dead-flat ground is instantly previous-era (grammar #1). -->
      <rect width="{S}" height="{S}" fill="url(#ground)"/>
      <rect width="{S}" height="{S}" fill="url(#vignette)"/>
      <path d="{squircle()}" fill="none" stroke="url(#innerRim)" stroke-width="3" stroke-opacity=".55"/>
    </g>

    <g id="mid">
      <!-- the datum's light reaching the porcelain, and the shadow it still casts. Drawn
           BELOW the bars so they occlude it: light spills around them, not over them. -->
      <ellipse cx="{rule_cx:.1f}" cy="{RULE_TOP + RULE_H / 2:.1f}"
               rx="{rule_w / 2 + BLOOM_OVER:.1f}" ry="{BLOOM_RY:.1f}" fill="url(#bloom)"/>
      <ellipse cx="{rule_cx:.1f}" cy="{RULE_TOP + RULE_H + 20:.1f}" rx="{rule_w * 0.54:.1f}" ry="46"
               fill="url(#contact)"/>
    </g>

    <g id="fg">
      <!-- THE DATUM. Drawn before the bars, unbroken end to end: it is what they stand on,
           so nothing may interrupt it. -->
      <rect x="{rule_x0:.1f}" y="{RULE_TOP:.1f}" width="{rule_w:.1f}" height="{RULE_H:.1f}"
            rx="{rule_rx:.1f}" fill="url(#rule)"/>
      <rect x="{rule_x0:.1f}" y="{RULE_TOP:.1f}" width="{rule_w:.1f}" height="{RULE_H:.1f}"
            rx="{rule_rx:.1f}" fill="url(#ruleEnds)"/>

      <!-- the bars: context, not subject. They sink {BAR_SINK:.0f}px into the rule so no
           hairline seam survives rasterisation. -->
{nl.join(bars)}
{nl.join(bounces)}
    </g>

    <g id="highlight">
      <!-- one soft top light; no hard specular anywhere in this file -->
{nl.join(caps)}
      <!-- contact darkening where each bar presses into the gel -->
{nl.join(aos)}
    </g>

  </g>
</svg>
"""


VARIANTS = {
    "icon.svg": dict(),
    "icon-small.svg": dict(small=True, title="visualization — 64px and below"),
    "icon-A2-fourbar.svg": dict(bar_h=FOUR_BAR_H, bar_w=FOUR_BAR_W, gap=FOUR_BAR_GAP,
                               title="visualization — four-bar take"),
    "icon-A3-edgebleed.svg": dict(edge_bleed=True, title="visualization — edge-bleed take"),
}
# Which file each shipped size comes from. The crossover is measured, not assumed:
# self-contrast (p90 - p10 of the composited grey) for master vs floor, by size —
#
#   48px  0.7216 / 0.7059   floor costs 0.016
#   40px  0.5737 / 0.5890   floor gains 0.015
#   32px  0.5216 / 0.6000   floor gains 0.078   <- the crossover, and the big one
#   24px  0.5137 / 0.5471   floor gains 0.033
#   16px  0.6451 / 0.6118   floor costs 0.033
#
# So the catch is worth having everywhere except the 24-40px band, where a bar is
# 3-5 pixels wide. 16px recovers on its own because by then the bar is 2 pixels and
# the catch has been averaged away entirely — it is 32 that has just enough room to
# be hurt. `audit_sheet.py`'s own SMALL_BELOW is 96, which is a different question
# (which file the SHEET renders small sizes from); the sheet is told this number
# explicitly via --small so the two cannot drift apart silently.
SMALL_BELOW = 48
EXPORTS = {"icon.png": 1024, "icon-256.png": 256, "icon-128.png": 128, "icon-16.png": 16}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--export", action="store_true", help="also rasterise the shipped PNG sizes")
    a = ap.parse_args()

    for name, kw in VARIANTS.items():
        (HERE / name).write_text(svg(**kw))
        print(f"wrote {name}")

    xs, span = layout(BAR_H, BAR_W, BAR_GAP)
    rule_w = span + 2 * RULE_OVERHANG
    fig_h = max(BAR_H) + RULE_H
    print(f"\nfocal (the rule) {rule_w:.0f}px = {rule_w / S:.1%} of tile")
    print(f"figure {rule_w:.0f} x {fig_h:.0f}, optical centre y="
          f"{(RULE_TOP - max(BAR_H) + RULE_TOP + RULE_H) / 2:.0f}")
    print(f"at 16px: bar {BAR_W / 64:.2f}px, gap {BAR_GAP / 64:.2f}px, rule {RULE_H / 64:.2f}px")

    if a.export:
        for name, size in EXPORTS.items():
            src = "icon.svg" if size >= SMALL_BELOW else "icon-small.svg"
            subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size),
                            str(HERE / src), "-o", str(HERE / name)], check=True)
            print(f"exported {name} ({size}px, from {src})")


if __name__ == "__main__":
    main()
