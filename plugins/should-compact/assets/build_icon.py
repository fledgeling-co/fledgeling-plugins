#!/usr/bin/env python3
"""Engine A — the hand-authored layered SVG master for `should-compact`.

Geometry and material live here as named constants so a fidelity round is a parameter edit
rather than path surgery. Run it to regenerate `icon.svg`.

DIRECTION: 2 Tahoe Gel-Glass, sub-register (a) — porcelain cushion tile carrying a coloured gel
object. Runner-up: (c) dark glass, rejected because the dark register is `trawl`'s alone in this
marketplace, and because the whole argument here is a bright gap, which needs a light ground to
read as *empty* rather than as another glowing thing on black.

THE GLYPH, subject-mined. The skill answers one question: is the work at a seam right now? So the
subject is not a verdict, a gauge or a hand. It is the seam. Two graphite masses sit side by side
and the gap between them is the brightest element in the icon — the composition performs the
argument, because what the skill is pointing at is the space, not the blocks either side of it.

SIGNATURE MOVE: the focal element is empty. Every other icon in this set puts light *on* an object;
this one puts it in the space an object is not. The right mass is also lifted 34px above the left,
so the pair reads as HELD mid-step rather than closed — a pause, not a full stop. That lift is the
difference between "now is a good moment" and "no".

FAMILY FIT, and the deliberate difference. `braindump` is one squat cylinder banded with horizontal
vermilion strata. Same porcelain ground, same graphite gel, same vermilion accent, so they read as
a pair; opposite shape language, so they never collide in a grid. Sibling: horizontal bands on one
mass. This: one vertical column of light between two masses.

VALUES SAMPLED FROM THE CORPUS, not assumed (apple-05, apple-06, apple-11 at
`references/corpus/apple-2026/`): ground runs #FFFFFF at the top to ~#E5E6E5 at the bottom, a
vertical delta of 19-26; the brightest point sits at the TOP, so the key light is above; the darkest
in-tile pixel is a cool near-black around (30,33,36) with blue above red; the accent runs 0.86-1.00
saturation at hue 6-35 degrees.
"""

from __future__ import annotations
import pathlib

S = 1024

# ── geometry ────────────────────────────────────────────────────────────────────────────────────
# Focal width is measured across BOTH masses plus the seam: 636px = 62.1% of the tile, inside the
# 55-65% band the composition constants call for.
SEAM_W      = 74      # the gap. It is the subject, so it is sized like one.
# Asymmetric on purpose. Two equal bars either side of a gap is a PAUSE glyph, which names the
# category ("stop/hold") instead of this subject ("is the work at a seam"). Unequal masses read as
# two pieces of work, and the seam between them stops being a symmetry axis.
BLOCK_W_L   = 330
BLOCK_W_R   = 246
BLOCK_H     = 392
BLOCK_H_R   = 330
GAP_CENTRE  = S // 2
LEFT_X      = GAP_CENTRE - SEAM_W / 2 - BLOCK_W_L
RIGHT_X     = GAP_CENTRE + SEAM_W / 2
LEFT_Y      = 330
RIGHT_LIFT  = 78      # the held beat. At 34 it read as a misalignment; it has to be unmistakably
                      # deliberate or it looks like a bug rather than a pause.
RIGHT_Y     = LEFT_Y - RIGHT_LIFT
R_SHOULDER  = 46      # generous rounding: gel is poured, not cut

# ── material ────────────────────────────────────────────────────────────────────────────────────
GROUND_TOP, GROUND_MID, GROUND_BOT = "#FFFFFF", "#F7F6F4", "#E5E4E1"
GRAPHITE = ["#4A535B", "#2E363D", "#1E242A", "#141A1F"]   # top-lit ramp, cool, per the corpus
SEAM_CORE, SEAM_MID, SEAM_EDGE = "#FFF1E2", "#FF7A2E", "#B8380C"
RIM = "#FFFFFF"


def svg() -> str:
    sq = (pathlib.Path(__file__).parent / "squircle-path.txt").read_text().strip()

    def block(x: float, y: float, w: float, h: float, tag: str) -> str:
        """One graphite mass: body ramp, a soft top-edge highlight, and a seam-facing warm bounce.

        The warm bounce is the one non-obvious part. The seam is emissive, so the faces looking
        into it must pick its light up; without that the blocks read as two objects that happen to
        be near a glowing line rather than two objects lit BY it.
        """
        return f"""
    <g id="{tag}">
      <rect x="{x:.1f}" y="{y:.1f}" width="{w:.0f}" height="{h:.0f}"
            rx="{R_SHOULDER}" fill="url(#graphite)"/>
      <rect x="{x:.1f}" y="{y:.1f}" width="{w:.0f}" height="{h:.0f}"
            rx="{R_SHOULDER}" fill="url(#topEdge)"/>
      <rect x="{x:.1f}" y="{y:.1f}" width="{w:.0f}" height="{h:.0f}"
            rx="{R_SHOULDER}" fill="none" stroke="{RIM}" stroke-opacity=".16" stroke-width="2"/>
    </g>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">
  <title>should-compact</title>
  <defs>
    <clipPath id="tile"><path d="{sq}"/></clipPath>

    <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{GROUND_TOP}"/>
      <stop offset=".55" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_BOT}"/>
    </linearGradient>

    <linearGradient id="graphite" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{GRAPHITE[0]}"/>
      <stop offset=".34" stop-color="{GRAPHITE[1]}"/>
      <stop offset=".76" stop-color="{GRAPHITE[2]}"/>
      <stop offset="1" stop-color="{GRAPHITE[3]}"/>
    </linearGradient>

    <!-- one soft top light; no hard speculars anywhere in this file -->
    <linearGradient id="topEdge" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{RIM}" stop-opacity=".30"/>
      <stop offset=".13" stop-color="{RIM}" stop-opacity=".05"/>
      <stop offset="1" stop-color="{RIM}" stop-opacity="0"/>
    </linearGradient>

    <!-- the sanctioned second source: an emissive interior, here with no interior to sit in -->
    <linearGradient id="seam" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{SEAM_EDGE}"/>
      <stop offset=".18" stop-color="{SEAM_MID}"/>
      <stop offset=".46" stop-color="{SEAM_CORE}"/>
      <stop offset=".74" stop-color="{SEAM_MID}"/>
      <stop offset="1" stop-color="{SEAM_EDGE}"/>
    </linearGradient>

    <linearGradient id="seamSoft" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{SEAM_MID}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{SEAM_MID}" stop-opacity=".55"/>
      <stop offset="1" stop-color="{SEAM_MID}" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="bloom" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="{SEAM_MID}" stop-opacity=".78"/>
      <stop offset=".45" stop-color="{SEAM_MID}" stop-opacity=".22"/>
      <stop offset="1" stop-color="{SEAM_MID}" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="contact" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="#1E242A" stop-opacity=".34"/>
      <stop offset=".62" stop-color="#1E242A" stop-opacity=".10"/>
      <stop offset="1" stop-color="#1E242A" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="vignette" cx=".5" cy=".46" r=".72">
      <stop offset=".62" stop-color="#000000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000000" stop-opacity=".07"/>
    </radialGradient>

    <linearGradient id="innerRim" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{RIM}" stop-opacity=".9"/>
      <stop offset=".5" stop-color="{RIM}" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#tile)">
    <!-- #bg — the cushion. A dead-flat ground is instantly previous-era. -->
    <rect width="{S}" height="{S}" fill="url(#ground)"/>
    <rect width="{S}" height="{S}" fill="url(#vignette)"/>
    <path d="{sq}" fill="none" stroke="url(#innerRim)" stroke-width="3" stroke-opacity=".55"/>

    <!-- #mid — the seam's light reaching the porcelain, and the contact shadow it sits in -->
    <ellipse cx="{GAP_CENTRE}" cy="{LEFT_Y + BLOCK_H - 6}" rx="330" ry="120" fill="url(#bloom)"/>
    <ellipse cx="{GAP_CENTRE}" cy="{LEFT_Y + BLOCK_H + 26}" rx="352" ry="62" fill="url(#contact)"/>

    <!-- #fg — the two masses, and between them the subject -->
    <!-- #mid — the seam, drawn BEHIND the masses and overrun at both ends. Light in a gap has no
         outline of its own: it is bounded by the things either side of it. Drawn on top with
         rounded caps it became a glowing capsule sitting between two blocks, which is an object,
         and the whole point is that the focal element is empty. Overrunning the ends by 90px means
         the blocks clip it, so its extent is set by them rather than by a rectangle of its own. -->
    <rect x="{GAP_CENTRE - SEAM_W*0.9:.1f}" y="{RIGHT_Y - 34}" width="{SEAM_W*1.8:.1f}"
          height="{BLOCK_H + RIGHT_LIFT + 68}" fill="url(#seamSoft)"/>
    <rect x="{GAP_CENTRE - SEAM_W/2:.1f}" y="{RIGHT_Y - 34}" width="{SEAM_W}"
          height="{BLOCK_H + RIGHT_LIFT + 68}" fill="url(#seam)"/>
    <rect x="{GAP_CENTRE - 13:.1f}" y="{RIGHT_Y - 34}" width="26"
          height="{BLOCK_H + RIGHT_LIFT + 68}" fill="{SEAM_CORE}" opacity=".95"/>

    <!-- #fg — the two masses. They bound the light; they are not the subject. -->
    {block(LEFT_X, LEFT_Y, BLOCK_W_L, BLOCK_H, "mass-left")}
    {block(RIGHT_X, RIGHT_Y, BLOCK_W_R, BLOCK_H_R, "mass-right")}

  </g>
</svg>
"""


if __name__ == "__main__":
    out = pathlib.Path(__file__).parent / "icon.svg"
    out.write_text(svg())
    print(f"wrote {out} · focal {BLOCK_W_L + BLOCK_W_R + SEAM_W}px = {(BLOCK_W_L + BLOCK_W_R + SEAM_W)/S:.1%} of tile")
