#!/usr/bin/env python3
"""Engine A: the layered SVG master for mac-doctor.

Geometry and material live as named constants so a fidelity round is a
parameter edit rather than path surgery.

WHAT THIS BUILD CHANGED (round 6, the fidelity round)
-----------------------------------------------------
Two faults were open against take C:

  1. The ember did not sit cleanly in the ring's band. Geometrically it always
     shared the inner radius -- measured on the render, both boundaries sat at
     190 and 332 at every angle. What broke the read was that the RING carried
     an inner edge-catch stroke and the EMBER did not, so the band's inner
     boundary was a lit arc for 280 degrees and an unlit one for 40. The eye
     reads that as a broken circle. The fix is structural rather than
     cosmetic: `band()` below emits the whole nine-layer stack for any arc,
     and it is called twice -- once for graphite, once for ember. Every
     boundary, shoulder and bevel radius is therefore shared by construction
     and cannot drift apart in a later edit.

  2. The material was flat beside the raster. It was a single stroke with one
     linear ramp; C is a gel torus. Rebuilt as the bevelled-puck construction
     C actually uses (see the sampled numbers below).

Values sampled from the corpus and from take C rather than assumed
(create-mac-icon step 4; material-recipes.md "measure, never assume"):

  House porcelain, from armada-sync / dossier-report / create-mac-icon at 256:
      top    (253,253,252)   mid (245,238,231)   bottom (237,233,223)
  This is WARM. Apple's own porcelain is cool (254,255,255 -> 223,227,235);
  the family's is cream, and family consistency wins over the platform sample.

  Take C's ring body, sampled over 267k pixels:
      darkest (18,49,75) L 0.174 -- a deep cool navy, not a neutral graphite
      brightest (246,252,255) L 0.984 -- a near-white specular
      p5..p95 luminance spread 0.439
  The shipped master ran #5C6880 to #252B36, a spread of 0.24 with no
  specular at all. That one number is most of what "the raster looks richer"
  meant, and adding a real specular is the largest single move here.

  Take C's cross-section across the band, t=0 inner to t=1 outer:
      facing the key (225 deg): 0.28 rising monotonically to 0.84 at t=0.88
      level with the centre (180 deg): flat 0.28-0.30, lifting to 0.50 at t=0.91
      away from the key (45 deg): 0.29 falling to 0.20 mid, no outer lift
  So the cross-section is a shallow radial ramp with its minimum near the band
  centre, and the drama is ANGULAR: the specular exists only on the key side.
  Hence a radial gradient for the section and a separate key-axis-faded stroke
  for the specular, rather than one gradient trying to be both.

  Take C's cut ends: every terminus is a bevelled puck -- a dark wall around a
  paler inset face, the face lifting to L 0.36-0.53 against a body at 0.255,
  with a white hairline against the ground. Confirmed as era grammar in the
  corpus (apple-08's concentric ridges carry the same lit-shoulder / dark-
  terminator / bounced-inner-edge stack).

  Take C's ember: darkest (227,21,1) L 0.248 at saturation 0.996; brightest
  (254,226,193) L 0.900. The old master's dark end was #D8410F -- L 0.36 and
  visibly desaturated. A gel shadow that desaturates reads opaque
  (material-recipes, "The Cast" r06), so the dark end goes deep and stays
  saturated.

  Contact shadow, Safari, just under the object:
      local ground (233,234,235), shadow (205,215,232). About 12% darker and
  tinted toward the object's own hue, not a neutral grey. So the graphite
  ring casts cool and the ember casts warm, at identical offset and blur so
  the two read as one plane.

The composition is the capacity arc: a ring 280 degrees closed in graphite
over no track at all, with one ember segment sitting INLINE in the same band,
clear of the used arc on both sides. The gap is the message.
"""

import math
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
# assets -> mac-doctor -> plugins, then across to the canonical path
SQUIRCLE = (Path(__file__).resolve().parents[2] / "create-mac-icon" /
            "assets" / "squircle-path.txt")

# ---- geometry ---------------------------------------------------------------
S = 1024
CX = CY = 512
R = 280                 # ring centreline radius
W = 152                 # band width; heavier reads better at small sizes
GAP_MID = -55.0         # bisector of the gap, degrees, 0 = +x, y down
GAP_HALF = 40.0         # half-width of the hole: an 80 degree opening
EMBER_SPAN = 40.0       # the reclaimed segment, centred in the hole
SCALE = 0.93            # composition scale, keeps the band off the tile edge

R_IN = R - W / 2        # 204 -- the band's inner boundary, shared by both arcs
R_OUT = R + W / 2       # 356 -- the band's outer boundary, shared by both arcs

# Bevel: the dark wall between the silhouette and the lit inset face. Measured
# off C at roughly 0.08 of the band width. It is what makes a gel puck read as
# moulded rather than printed, and it is applied identically to both arcs.
BEVEL = 10.0
# Angular inset for the face, so the CUT ENDS are bevelled too and not just the
# long sides. A stroke cannot inset its own caps, so the face arc is shortened
# by the same 12px expressed as an angle at the centreline radius.
BEVEL_DEG = math.degrees(BEVEL / R)

# Cross-section landmarks as fractions of the band width, from the C samples.
T_BOUNCE = 0.17         # inner shoulder, where ground bounce lands
T_DARK = 0.53           # the section minimum
T_SPEC = 0.82           # the lit shoulder carrying the specular
SPEC_W = 0.115 * W      # specular stroke width
BOUNCE_W = 0.095 * W    # inner-bounce stroke width
END_FADE = 96.0         # radius over which a cut end's pale face fades out

# The key light. One source, upper-left. Every angular gradient hangs on this
# ONE axis, expressed in USER SPACE (material-recipes: "one key, one axis").
# Object-bounding-box units were the first attempt and are wrong here: they
# rescale the axis to each shape, so a 40-degree ember got its own private
# light direction and broke rubric 5 on a mark whose whole point is that the
# two segments are one physical band.
# Measured off C rather than assumed: its specular runs along the TOP of the
# arc and wraps a little into the upper left, its darkest body sits at the
# bottom, and its left and right flanks at centre height read the same mid
# value. That is a near-vertical key tilted about 16 degrees left, not the
# 45-degree diagonal the first draft used. The diagonal put the ember at t=0.41
# on the axis, which is the neutral point, and the segment came out muddy while
# the ring around it was lit -- one object, two lighting stories.
KEY = (CX - 0.30 * R_OUT, CY - 1.06 * R_OUT,
       CX + 0.30 * R_OUT, CY + 1.06 * R_OUT)
# The vertical axis, for gravity-driven passes: the shade a form takes toward
# its base, and the bounce it picks up off the porcelain.
VERT_TOP, VERT_BOT = CY - R_OUT, CY + R_OUT

# ---- material ---------------------------------------------------------------
GROUND_TOP, GROUND_MID, GROUND_BOT = "#FDFDFC", "#F5EEE7", "#EDE9DF"

# Graphite gel. Slate-navy rather than neutral graphite: C's body measured
# (71,90,119) mean and the cool read is part of why it looked like material.
WALL_LIT, WALL_DARK = "#465272", "#132639"      # the bevel wall, key to far
FACE_IN = "#2E3951"     # inset face at the inner bevel line
FACE_BOUNCE = "#3A455E"  # inner shoulder, lifted by ground bounce
FACE_DARK = "#16283F"   # the section minimum, L 0.208 against C's 0.20
FACE_SHOULDER = "#505E7C"  # the lit outer shoulder
FACE_OUT = "#37455F"    # turning down again at the outer bevel line
SPEC = "#EEF3FB"        # near-white specular, against C's (246,252,255)
BOUNCE = "#A9B8D4"      # cool bounce off the porcelain into the inner wall
END_FACE = "#98A1B9"    # the cut cross-section, L 0.40 against C's 0.36-0.53

# The ember. Kin to the family accent #C4622D (hue 21 degrees): the mid holds
# that hue, the dark end deepens toward C's measured shadow without letting the
# saturation fall, and the specular matches C's brightest ember pixel almost
# exactly.
EM_WALL_LIT, EM_WALL_DARK = "#DE7433", "#B4441A"
EM_FACE_IN = "#DE4B0B"
EM_FACE_BOUNCE = "#E85512"
EM_FACE_DARK = "#C94208"     # L 0.275 at saturation 0.95, against C's 0.248/0.996
EM_FACE_SHOULDER = "#FA7F22"
EM_FACE_OUT = "#ED6114"      # the family accent itself
EM_SPEC = "#FFE0C4"          # against C's brightest (254,226,193)
EM_BOUNCE = "#F7B98E"
EM_END_FACE = "#F0A470"

SHADOW_COOL = "#2A2F38"
SHADOW_WARM = "#C0430F"
RIM = "#FFFFFF"


# ---- helpers ----------------------------------------------------------------

def pt(deg, r):
    a = math.radians(deg)
    return CX + r * math.cos(a), CY + r * math.sin(a)


def arc(a0, a1, r):
    """Clockwise arc from a0 to a1 (a1 > a0) at radius r."""
    x0, y0 = pt(a0, r)
    x1, y1 = pt(a1, r)
    large = 1 if (a1 - a0) > 180 else 0
    return f"M {x0:.2f} {y0:.2f} A {r:.2f} {r:.2f} 0 {large} 1 {x1:.2f} {y1:.2f}"


def off(t):
    """Band fraction t (0 inner, 1 outer) as a radialGradient offset."""
    return (R_IN + t * W) / R_OUT


def section_gradient(gid, c_in, c_bounce, c_dark, c_shoulder, c_out):
    """The cross-section ramp, in user space so it is the same physical
    section on every arc that uses it."""
    return f'''  <radialGradient id="{gid}" gradientUnits="userSpaceOnUse"
                  cx="{CX}" cy="{CY}" r="{R_OUT:.2f}">
    <stop offset="{off(0.0):.4f}"      stop-color="{c_in}"/>
    <stop offset="{off(T_BOUNCE):.4f}" stop-color="{c_bounce}"/>
    <stop offset="{off(T_DARK):.4f}"   stop-color="{c_dark}"/>
    <stop offset="{off(T_SPEC):.4f}"   stop-color="{c_shoulder}"/>
    <stop offset="{off(1.0):.4f}"      stop-color="{c_out}"/>
  </radialGradient>'''


def key_gradient(gid, colour, peak, tail=0.0):
    """An opacity ramp along the single key axis: full at the lit corner,
    gone by the far one. Used for additive passes (specular, rim)."""
    x1, y1, x2, y2 = KEY
    return f'''  <linearGradient id="{gid}" gradientUnits="userSpaceOnUse"
                   x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}">
    <stop offset="0"    stop-color="{colour}" stop-opacity="{peak}"/>
    <stop offset="0.34" stop-color="{colour}" stop-opacity="{peak * 0.62:.3f}"/>
    <stop offset="0.68" stop-color="{colour}" stop-opacity="{peak * 0.14:.3f}"/>
    <stop offset="1"    stop-color="{colour}" stop-opacity="{tail}"/>
  </linearGradient>'''


def key_ramp(gid, lit, dark):
    """An OPAQUE colour ramp along the key axis, lit corner to far corner.

    The bevel wall's first draft used key_gradient for this, which ramps
    opacity rather than colour: the wall dissolved to nothing on the unlit
    side and the whole mark washed out. A wall is opaque everywhere; only its
    colour changes with the light.
    """
    x1, y1, x2, y2 = KEY
    return f'''  <linearGradient id="{gid}" gradientUnits="userSpaceOnUse"
                   x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}">
    <stop offset="0"    stop-color="{lit}"/>
    <stop offset="0.52" stop-color="{dark}"/>
    <stop offset="1"    stop-color="{dark}"/>
  </linearGradient>'''


def key_modelling(gid, lit, lit_op, dark, dark_op):
    """The face's own modelling: a lift toward the key, a fall away from it,
    on the same one axis."""
    x1, y1, x2, y2 = KEY
    return f'''  <linearGradient id="{gid}" gradientUnits="userSpaceOnUse"
                   x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}">
    <stop offset="0"    stop-color="{lit}" stop-opacity="{lit_op}"/>
    <stop offset="0.40" stop-color="{lit}" stop-opacity="0"/>
    <stop offset="0.60" stop-color="{dark}" stop-opacity="0"/>
    <stop offset="1"    stop-color="{dark}" stop-opacity="{dark_op}"/>
  </linearGradient>'''


def end_gradient(gid, deg, colour, peak):
    """A pale cut-face that fades away from one terminus."""
    x, y = pt(deg, R)
    return f'''  <radialGradient id="{gid}" gradientUnits="userSpaceOnUse"
                  cx="{x:.2f}" cy="{y:.2f}" r="{END_FADE}">
    <stop offset="0"    stop-color="{colour}" stop-opacity="{peak}"/>
    <stop offset="0.45" stop-color="{colour}" stop-opacity="{peak * 0.55:.3f}"/>
    <stop offset="1"    stop-color="{colour}" stop-opacity="0"/>
  </radialGradient>'''


def band(a0, a1, keyname, opts):
    """Emit the full material stack for one segment of the band.

    Called once for the graphite arc and once for the ember. Both get the same
    radii, the same bevel, the same shoulder positions and the same cut-end
    construction, so the band's inner and outer boundaries are continuous arcs
    by construction rather than by a matched pair of edits.
    """
    fa0, fa1 = a0 + BEVEL_DEG, a1 - BEVEL_DEG   # face arc, inset at both ends
    face_w = W - 2 * BEVEL
    shell = arc(a0, a1, R)
    face = arc(fa0, fa1, R)
    spec = arc(fa0, fa1, R_IN + T_SPEC * W)
    bounce = arc(fa0, fa1, R_IN + T_BOUNCE * W)
    return f'''  <g id="{keyname}">
    <!-- glass edge: ONE hairline, drawn under the mass so the lit lip spills
         onto the ground rather than ringing it, and modulated by the key so
         it is a catch on the lit side rather than a uniform outline. A second
         wide halo was tried and removed: at any opacity that showed, it read
         as a sticker cut line. -->
    <path d="{shell}" fill="none" stroke="url(#{opts['rim']})"
          stroke-width="{W + 7}" stroke-linecap="butt" filter="url(#hairline)"/>
    <!-- the bevel wall: the dark moulded rim the inset face sits inside -->
    <path d="{shell}" fill="none" stroke="url(#{opts['wall']})"
          stroke-width="{W}" stroke-linecap="butt"/>
    <!-- the inset face, carrying the cross-section ramp -->
    <path d="{face}" fill="none" stroke="url(#{opts['section']})"
          stroke-width="{face_w}" stroke-linecap="butt"/>
    <!-- the single key light, modelling the whole segment along one axis.
         Applied to the SHELL, not the face: lighting only the inset face left
         the bevel wall unlit, which reads as an inked outline. -->
    <path d="{shell}" fill="none" stroke="url(#{opts['key']})"
          stroke-width="{W}" stroke-linecap="butt"/>
    <path d="{shell}" fill="none" stroke="url(#{opts['shade']})"
          stroke-width="{W}" stroke-linecap="butt"/>
    <!-- the lit shoulder: a soft specular that exists only on the key side -->
    <path d="{spec}" fill="none" stroke="url(#{opts['spec']})"
          stroke-width="{SPEC_W:.1f}" stroke-linecap="round" filter="url(#specular)"/>
    <!-- bounce off the porcelain into the inner wall, strongest at the bottom -->
    <path d="{bounce}" fill="none" stroke="url(#{opts['bounce']})"
          stroke-width="{BOUNCE_W:.1f}" stroke-linecap="round" filter="url(#soften)"/>
    <!-- the two cut cross-sections, paler than the body and fading inward -->
    <path d="{face}" fill="none" stroke="url(#{opts['end0']})"
          stroke-width="{face_w}" stroke-linecap="butt"/>
    <path d="{face}" fill="none" stroke="url(#{opts['end1']})"
          stroke-width="{face_w}" stroke-linecap="butt"/>
  </g>'''


def build():
    squircle = SQUIRCLE.read_text().strip()

    ring_a0 = GAP_MID + GAP_HALF                # -15
    ring_a1 = GAP_MID - GAP_HALF + 360          # 265
    em_a0 = GAP_MID - EMBER_SPAN / 2            # -75
    em_a1 = GAP_MID + EMBER_SPAN / 2            # -35

    ring_shell = arc(ring_a0, ring_a1, R)
    em_shell = arc(em_a0, em_a1, R)
    em_cx, em_cy = pt(GAP_MID, R)

    defs = "\n".join([
        section_gradient("sectionRing", FACE_IN, FACE_BOUNCE, FACE_DARK,
                         FACE_SHOULDER, FACE_OUT),
        section_gradient("sectionEmber", EM_FACE_IN, EM_FACE_BOUNCE,
                         EM_FACE_DARK, EM_FACE_SHOULDER, EM_FACE_OUT),
        key_ramp("wallRing", WALL_LIT, WALL_DARK),
        key_ramp("wallEmber", EM_WALL_LIT, EM_WALL_DARK),
        key_modelling("keyRing", "#FFFFFF", 0.13, "#06162B", 0.30),
        key_modelling("keyEmber", "#FFF0E2", 0.22, "#5E1A03", 0.16),
        key_gradient("specRing", SPEC, 0.95),
        key_gradient("specEmber", EM_SPEC, 0.88),
        key_gradient("rimRing", RIM, 0.72, tail=0.10),
        key_gradient("rimEmber", RIM, 0.66, tail=0.10),
        end_gradient("end0Ring", ring_a0, END_FACE, 0.85),
        end_gradient("end1Ring", ring_a1, END_FACE, 0.72),
        end_gradient("end0Ember", em_a0, EM_END_FACE, 0.55),
        end_gradient("end1Ember", em_a1, EM_END_FACE, 0.42),
    ])

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">
<defs>
  <!-- PLANE 1: ground. A cushion, not a print: vertical ramp, edge vignette,
       and a faint inner rim light around the perimeter. -->
  <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0"    stop-color="{GROUND_TOP}"/>
    <stop offset="0.52" stop-color="{GROUND_MID}"/>
    <stop offset="1"    stop-color="{GROUND_BOT}"/>
  </linearGradient>
  <radialGradient id="vignette" cx="0.30" cy="0.26" r="0.92">
    <stop offset="0"    stop-color="#FFFFFF" stop-opacity="0.55"/>
    <stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0"/>
    <stop offset="1"    stop-color="#8C8577" stop-opacity="0.16"/>
  </radialGradient>
  <!-- the ember is a light source, not just a saturated fill: it spills onto
       the porcelain it sits on. Vibrancy is emission, not saturation. -->
  <radialGradient id="emberSpill" gradientUnits="userSpaceOnUse"
                  cx="{em_cx:.1f}" cy="{em_cy:.1f}" r="330">
    <stop offset="0"    stop-color="#F07A2A" stop-opacity="0.16"/>
    <stop offset="0.45" stop-color="#F07A2A" stop-opacity="0.06"/>
    <stop offset="1"    stop-color="#F07A2A" stop-opacity="0"/>
  </radialGradient>

{defs}

  <!-- The two shading passes that are NOT on the key axis: a vertical shade
       under the whole face, and the ground bounce, which comes from below. -->
  <linearGradient id="shadeRing" gradientUnits="userSpaceOnUse" x1="0" y1="{VERT_TOP}" x2="0" y2="{VERT_BOT}">
    <stop offset="0"    stop-color="#08172C" stop-opacity="0"/>
    <stop offset="0.55" stop-color="#08172C" stop-opacity="0.07"/>
    <stop offset="1"    stop-color="#08172C" stop-opacity="0.28"/>
  </linearGradient>
  <linearGradient id="shadeEmber" gradientUnits="userSpaceOnUse" x1="0" y1="{VERT_TOP}" x2="0" y2="{VERT_BOT}">
    <stop offset="0"    stop-color="#6B1A02" stop-opacity="0"/>
    <stop offset="0.55" stop-color="#6B1A02" stop-opacity="0.03"/>
    <stop offset="1"    stop-color="#6B1A02" stop-opacity="0.14"/>
  </linearGradient>
  <linearGradient id="bounceRing" gradientUnits="userSpaceOnUse" x1="0" y1="{VERT_BOT}" x2="0" y2="{VERT_TOP}">
    <stop offset="0"    stop-color="{BOUNCE}" stop-opacity="0.62"/>
    <stop offset="0.42" stop-color="{BOUNCE}" stop-opacity="0.24"/>
    <stop offset="1"    stop-color="{BOUNCE}" stop-opacity="0.04"/>
  </linearGradient>
  <linearGradient id="bounceEmber" gradientUnits="userSpaceOnUse" x1="0" y1="{VERT_BOT}" x2="0" y2="{VERT_TOP}">
    <stop offset="0"    stop-color="{EM_BOUNCE}" stop-opacity="0.58"/>
    <stop offset="0.42" stop-color="{EM_BOUNCE}" stop-opacity="0.22"/>
    <stop offset="1"    stop-color="{EM_BOUNCE}" stop-opacity="0.04"/>
  </linearGradient>

  <filter id="soften" x="-25%" y="-25%" width="150%" height="150%">
    <feGaussianBlur stdDeviation="5"/>
  </filter>
  <filter id="hairline" x="-25%" y="-25%" width="150%" height="150%">
    <feGaussianBlur stdDeviation="1.6"/>
  </filter>
  <!-- The specular gets its own, tighter blur. Sharing the 5px soften made it
       a pale wash rather than a catch; a specular is the one pass whose
       sharpness carries how hard the surface reads. -->
  <filter id="specular" x="-25%" y="-25%" width="150%" height="150%">
    <feGaussianBlur stdDeviation="2.8"/>
  </filter>
  <!-- Contact shadows, tinted toward each object's own hue but at identical
       offset and blur, so the ring and the ember read as one plane. -->
  <filter id="castCool" x="-40%" y="-40%" width="180%" height="190%">
    <feGaussianBlur stdDeviation="19"/>
  </filter>
  <filter id="castTight" x="-40%" y="-40%" width="180%" height="190%">
    <feGaussianBlur stdDeviation="6"/>
  </filter>

  <clipPath id="sq"><path d="{squircle}"/></clipPath>
</defs>

<g clip-path="url(#sq)">
  <g id="ground-plane">
    <rect width="{S}" height="{S}" fill="url(#ground)"/>
    <rect width="{S}" height="{S}" fill="url(#vignette)"/>
    <path d="{squircle}" fill="none" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="3"/>
  </g>

  <g transform="translate({CX},{CY}) scale({SCALE}) translate({-CX},{-CY})">
    <rect width="{S}" height="{S}" fill="url(#emberSpill)"/>

    <!-- PLANE 2: the shadow the whole band casts. One offset, one blur, two
         hues, so a warm segment and a cool arc still sit on the same table. -->
    <g id="cast-shadow">
      <g transform="translate(0,17)" filter="url(#castCool)">
        <path d="{ring_shell}" fill="none" stroke="{SHADOW_COOL}" stroke-opacity="0.30"
              stroke-width="{W}" stroke-linecap="butt"/>
        <path d="{em_shell}" fill="none" stroke="{SHADOW_WARM}" stroke-opacity="0.34"
              stroke-width="{W}" stroke-linecap="butt"/>
      </g>
      <g transform="translate(0,5)" filter="url(#castTight)">
        <path d="{ring_shell}" fill="none" stroke="{SHADOW_COOL}" stroke-opacity="0.22"
              stroke-width="{W}" stroke-linecap="butt"/>
        <path d="{em_shell}" fill="none" stroke="{SHADOW_WARM}" stroke-opacity="0.24"
              stroke-width="{W}" stroke-linecap="butt"/>
      </g>
    </g>

    <!-- PLANE 3: the band itself. No track behind it — a visible pale track
         makes the hole read as a filled lighter segment rather than as free
         space, which is the read the whole mark depends on. -->
{band(ring_a0, ring_a1, "used-arc", dict(
        wall="wallRing", section="sectionRing", key="keyRing", shade="shadeRing",
        spec="specRing", bounce="bounceRing", end0="end0Ring", end1="end1Ring",
        rim="rimRing"))}
{band(em_a0, em_a1, "reclaimed-segment", dict(
        wall="wallEmber", section="sectionEmber", key="keyEmber", shade="shadeEmber",
        spec="specEmber", bounce="bounceEmber", end0="end0Ember", end1="end1Ember",
        rim="rimEmber"))}
  </g>
</g>
</svg>
'''


def main():
    svg = build()
    master = OUT / "icon.svg"
    master.write_text(svg)
    for size, name in ((1024, "icon.png"), (256, "icon-256.png"),
                       (128, "icon-128.png"), (64, "icon-64.png"),
                       (32, "icon-32.png"), (16, "icon-16.png")):
        subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size),
                        str(master), "-o", str(OUT / name)], check=True)
    print(f"wrote {master} and 6 rasters")


if __name__ == "__main__":
    sys.exit(main())
