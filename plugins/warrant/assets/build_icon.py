#!/usr/bin/env python3
"""build_icon.py — the warrant icon's layered SVG master, emitted from constants.

    python3 build_icon.py                  # writes icon.svg + the three PNG exports, prints measurements
    python3 build_icon.py --svg-only       # writes icon.svg only
    python3 build_icon.py --variant v1     # writes icon-A-v1.svg,   the flat first draft
    python3 build_icon.py --variant left   # writes icon-A-left.svg, the left-aligned alternative

The two variants are the audit sheet's losing takes, kept reproducible from this
one generator so the sheet can score them honestly rather than describe them.

Forked from `plugins/shipyard/assets/build_icon.py` — same light model, same
cushion ground, same squircle, same "geometry and material as named constants"
discipline, so a later round is a parameter edit rather than path surgery.

Direction: Tahoe gel-glass, porcelain sub-register (a) — lit objects on a
porcelain cushion tile with one bounded accent family spent on one element.

Device (subject-mined): the authority ladder. Five slabs, stacked, each narrower
than the one above it. Authority narrows as consequence rises, so the widest bar
is the scope nobody had to earn and the narrowest is the scope that was.

Signature move — "the ladder, settling": each slab's stand-off from the tile
decays as the slabs narrow. The widest floats 40px clear of the porcelain and
casts a wide, soft, offset shadow; the narrowest has landed and has a tight dark
contact line instead. The gaps between them close on the same schedule. So the
tile reads as authority *settling* into the smallest scope it has earned, rather
than as a stack of stripes — and the decaying stand-off is also what stops the
bar-chart and signal-meter readings, both of which invert the meaning ("more is
better" where this is "narrower is earned").

Corpus numbers this was authored against, sampled from
references/corpus/apple-2026/ (interior only, 10% inset):

  apple-26 Apple Reminders — the structural analogue: rows on a porcelain tile,
  one accent object per row, and the recipe for "emissive on porcelain"
    ground ramp           L 1.000 top-left -> 0.913 mid -> 0.831 bottom, neutral
    flat non-accent rules #C1C1C1 L 0.533 — clearly present, never competing
    accent dot core       #406CE8 L 0.176  }  the rim runs 2.3x the core's
    accent dot top rim    #7FACFF L 0.412  }  luminance — that is the emission
    halo well under dot   #B6D4F1 H209 S0.24 L0.634, dying to S0.02 within ~30px
                          at 468px, i.e. a LOW-saturation HIGH-value tint, tight

  apple-13 stacked sheets — the composition analogue, and the inversion trap:
    widest/top slab body  L 0.931, its top rim L 1.000, its own base L 0.614
    middle slab           L 0.359  S 0.30
    narrowest/bottom slab L 0.202  S 0.54 — nearly the ground colour
    i.e. the reference makes the WIDEST brightest and dissolves the narrowest.
    This tile has to invert that, and the stand-off decay is what earns the right.

  apple-12 Calculator — dark body plus exactly one bounded accent on porcelain:
    porcelain             #E0DFDE H30 S0.01 -> #BDBCB9 H45 S0.02 — warm-neutral
    accent key core       #FF9417 L 0.425, its top rim #FFB642 L 0.551
    every non-accent key  #D8D9D7 L 0.691 — the accent is the only saturated thing

  cool slate shadow face  rgb(29,32,35) H210 S0.17 (apple-26), rgb(29,34,39)
                          H210 S0.26 (apple-08) — deep shadow on a dark body in a
                          daylight porcelain scene reads blue-slate, not warm

Shelf numbers, sampled off the 38 sibling icon-256.png files in this repo:
  30 of 38 grounds run warm R>G>B; `trawl` is the one dark register. The ground
  constants below are lifted verbatim from shipyard rather than re-derived, which
  is what makes the two tiles read as one family.
"""
from __future__ import annotations

import argparse
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent

# The squircle is the family's shared silhouette and lives in one place. Resolve
# the canonical copy first so this generator is reproducible where it sits,
# rather than needing the path file copied in beside it.
_SQ_CANDIDATES = (
    HERE.parents[2] / "create-mac-icon" / "assets" / "squircle-path.txt",
    HERE / "squircle-path.txt",
    pathlib.Path.home() / ".claude/plugins/cache/fledgeling-plugins/create-mac-icon"
    / "1.4.0/skills/create-mac-icon/assets/squircle-path.txt",
)


def squircle() -> str:
    for p in _SQ_CANDIDATES:
        if p.exists():
            return p.read_text().strip()
    raise SystemExit("squircle-path.txt not found in any of:\n  "
                     + "\n  ".join(str(p) for p in _SQ_CANDIDATES))


SQ = squircle()
W = 1024

# ---------------------------------------------------------------- palette
# One key light: top, tilted a little left — the same axis shipyard uses, so the
# two tiles are lit by the same lamp. One accent family (teal), one body family
# (slate). The ground is the shelf's warm porcelain, verbatim.
KEY = ((330.0, 236.0), (700.0, 726.0))

GROUND_HI = "#FDFCF9"        # lifted from shipyard/assets/build_icon.py
GROUND_MID = "#F6F4EF"
GROUND_LO = "#E5E0D6"
VIGNETTE = "#8B8070"

# r06: at #93A5BC/#6E8098 the lit top face measured 2.89:1 against the tile,
# under rubric #7's 3:1 floor — and a third of each slab's area was sitting
# below the figure-ground bar. Darkened ~12%, which also widens the accent's lit
# face against the slate ones from 1.51:1 to 1.7:1, so one edit pays twice.
SLAB_TOP_HI = "#8496AE"      # the lit top face, near the key
SLAB_TOP_LO = "#61738B"      # the lit top face, far from the key
SLAB_FACE_HI = "#586A80"     # front face, immediately under the fold
SLAB_FACE_MID = "#43536A"
SLAB_FACE_LO = "#2B3648"
SLAB_DEEP = "#1F2937"        # = corpus rgb(31,41,55), the measured cool shadow face
SLAB_LIP = "#C6D2E2"         # the top-edge rim light
SLAB_SEAM = "#222C3A"        # the fold between top face and front face
SLAB_BOUNCE = "#93A6BE"      # porcelain light coming back up under a floater

# The accent. Two named registers, both from the research page this plugin came
# out of: #186A73 is the light register and #63C3CC the lifted one. They are not
# interchangeable — per apple-26, an emissive object on porcelain is a DARK
# saturated core with a much brighter lit face and a tinted halo well, so the
# light register is the body and the lifted register is the face that catches
# the light. Reversing them makes it a pale sticker instead of a lit object.
TEAL_DEEP = "#0B3A41"        # stays saturated in shadow (the gel rule)
TEAL_CORE = "#186A73"        # <- the light register
TEAL_MID = "#1F7F89"
TEAL_HI = "#2E97A3"
TEAL_LIFT = "#63C3CC"        # <- the lifted register
TEAL_SUN = "#8FD9E0"         # the lifted register, caught square-on by the key
TEAL_LIP = "#C9F1F4"         # hot lip
TEAL_GLOW = "#3FB3BE"        # halo well and spill

SHADOW = "#2B333F"

# ---------------------------------------------------------------- geometry
DX = 0.0
DY = 0.0
SCALE = 1.0
OFFSET = (0.0, 0.0)          # measured off the render; see `python3 build_icon.py`

# Widths narrow on an ACCELERATING schedule (-15%, -19%, -27%, -40%), not an even
# one. Even steps are a chart's tick spacing; accelerating steps read as scope
# closing down as the consequence rises. The narrowest is 202px = 25.3px at
# 128px and 3.2px at 16px, so it still holds pixels where it has to.
BAR_W = (668.0, 568.0, 460.0, 336.0, 202.0)

# r02: 50+26 read as a stripe with a highlight on it. A slab needs enough front
# face to be a face, and enough top face to be a tread — 32 of 94 is a third of
# the object, which is what apple-13's slabs give their lit surface. This is also
# what stops five centred bars reading as a loading skeleton: a skeleton bar is
# thin and flat, a 94px slab with its own lit top is a physical thing.
BAR_H = 62.0                 # front-face height, constant — the slabs are one material
TOP_D = 32.0                 # visible top face: the camera tilt is constant, so this is too
RX = 25.0                    # gel corner radius on a 94px-tall slab

# The gaps close as the stack settles.
GAP = (62.0, 52.0, 42.0, 32.0)

# THE SIGNATURE MOVE. Stand-off in px above the tile surface. The decay
# decelerates (deltas 13, 11, 9, 7), so the last step is a landing rather than
# another equal drop.
LIFT = (40.0, 27.0, 16.0, 7.0, 0.0)

STACK_Y0 = 186.0             # top of the widest slab's top face

# Centred, not left-aligned, and this is a decision rather than a default. A
# stack of decreasing widths sharing one left edge IS a bar chart — the variant
# `left` builds exactly that so the sheet can show it losing. Centred, the same
# five widths read as a ziggurat narrowing toward a point, which is the shape the
# meaning wants.
LEFT_X = 178.0               # the widest slab's left edge, for the `left` variant

# How lift becomes a shadow, and this is the whole ballgame. r01 put the shadow
# DIRECTLY BELOW each slab and scaled its blur: every one of the five read as the
# same grey smear on the porcelain and nothing floated. Two fixes, both physical.
#
# First, the shadow is offset ALONG THE KEY, down-and-right, not straight down —
# so a floater's shadow sticks out past its own right end onto clear porcelain,
# where it is visible without needing a big vertical gap to live in. A displaced
# copy of the slab's own silhouette reads unmistakably as cast; a symmetric pool
# under it reads as dirt.
#
# Second, the vertical gap between a slab's base and its shadow now stays bright
# porcelain, because that sliver of untouched ground IS the stand-off. The landed
# slab gets no offset shadow at all — only a tight dark contact line welded to
# its base, which is the one thing a soft shadow cannot say.
# r03: at 0.62/0.44 the displacement was real but not READABLE as a gradient —
# bars 2 and 3 showed more shadow than bar 1, because the opacity decayed faster
# than the offset grew. With the key at roughly 45 degrees, a slab standing off
# by d throws its shadow about d sideways and d down, so these coefficients are
# now near 1 and the decay is gentle enough that the highest floater still has a
# shadow to displace.
# r04: 1.10/0.86 made the displacement readable and then cost the thing the
# direction is graded on — a 94px shadow offset 34px DOWN pokes below its own
# slab, and the countability probe read SIX bars at 128px. The offset is now
# almost entirely sideways, which is a higher key light and reads the same, so
# the shadow slides out onto clear porcelain instead of stacking under the slab.
SH_DX_GAIN = 1.34            # px of rightward offset per px of lift
SH_DY = 5.0                  # downward offset at zero lift
SH_DY_GAIN = 0.30
SH_SPREAD = 0.0009           # a soft distant light barely enlarges the shadow
SH_BLUR = 6.0
SH_BLUR_GAIN = 0.30
SH_OP = 0.30                 # a landed slab's shadow is small and dark …
SH_OP_DECAY = 0.0022         # … a high floater's is displaced and faint

# The accent's halo well. r01 used 150/330 and it read as a cyan cloud leaking
# out of the bottom of the tile. apple-26's well dies inside ~30px of a 468px
# tile — i.e. ~65px here — so tight is not a preference, it is the measurement.
# r03: still centred on the slab's BASE, so both wells pooled downward and the
# brightest softest thing in the tile sat in empty porcelain, pulling the eye off
# the object. Centred on the slab's middle they hug it on every side, which is
# what a well is.
#
# r07 raised the well's opacity for a reason that only showed up in the mono-tint
# check (rubric #10): flattened to grey, the accent slab was the PALEST mass in
# the tile, which is apple-13's inversion — narrowest reads as weakest, the exact
# reading this tile exists to refuse. The well is what fixes it, because a bright
# pool on the ground survives a hue flatten and says "this one is lit", where the
# object's own luminance can only say "this one is pale". apple-26 works the same
# way: its accent dot is DARKER than the grey rules and the well does the talking.
# r08: at 118/208 the tight well's radius barely exceeded the slab's own
# half-width of 101, so nearly all of it was painted and then covered by the slab
# — the measured well was 1.08:1 because there was almost no visible ring. Both
# wells are now proportioned off the slab (apple-26's well radius is ~1.9x its
# dot's) and squashed to an ellipse, because a circular pool around a 202x94 slab
# either misses the sides or floods above and below.
HALO_R_TIGHT = 186.0
HALO_R_WIDE = 300.0
HALO_SQUASH = 0.60           # y scale on both wells: the slab is wide and short
SPILL_R = 150.0              # falloff FROM the emitter, not a curtain over the tile

BAR_LABELS = ("tier 0 — advises only", "tier 1", "tier 2", "tier 3",
              "the earned scope")


# ---------------------------------------------------------------- helpers
def rrect(cx: float, y: float, w: float, h: float,
          r_top: float, r_bot: float) -> str:
    """Rounded rect centred on cx, with independent top/bottom corner radii.

    Independent radii are what let one slab be authored as two stacked faces —
    rounded top / square bottom for the top face, square top / rounded bottom
    for the front face — so the fold between them is a real seam the light can
    catch, instead of a gradient stop pretending to be an edge.
    """
    x0, x1 = cx - w / 2 + DX, cx + w / 2 + DX
    y0, y1 = y + DY, y + h + DY
    rt = min(r_top, w / 2, h)
    rb = min(r_bot, w / 2, h)
    return (f"M{x0 + rt:.1f},{y0:.1f} L{x1 - rt:.1f},{y0:.1f} "
            + (f"Q{x1:.1f},{y0:.1f} {x1:.1f},{y0 + rt:.1f} " if rt else "")
            + f"L{x1:.1f},{y1 - rb:.1f} "
            + (f"Q{x1:.1f},{y1:.1f} {x1 - rb:.1f},{y1:.1f} " if rb else "")
            + f"L{x0 + rb:.1f},{y1:.1f} "
            + (f"Q{x0:.1f},{y1:.1f} {x0:.1f},{y1 - rb:.1f} " if rb else "")
            + f"L{x0:.1f},{y0 + rt:.1f} "
            + (f"Q{x0:.1f},{y0:.1f} {x0 + rt:.1f},{y0:.1f} " if rt else "")
            + "Z")


def hline(cx: float, y: float, w: float, inset: float) -> str:
    x0, x1 = cx - w / 2 + inset + DX, cx + w / 2 - inset + DX
    return f"M{x0:.1f},{y + DY:.1f} L{x1:.1f},{y + DY:.1f}"


def g(tags) -> str:
    return "\n    ".join(tags)


# ---------------------------------------------------------------- derived
def layout(bar_w=BAR_W, gap=GAP, y0=STACK_Y0, align="centre"):
    """Per-bar (cx, top_y, fold_y, base_y, w). One pass, so a gap edit moves everything."""
    out, y = [], y0
    for i, w in enumerate(bar_w):
        cx = 512.0 if align == "centre" else LEFT_X + w / 2
        out.append((cx, y, y + TOP_D, y + TOP_D + BAR_H, w))
        if i < len(gap):
            y += TOP_D + BAR_H + gap[i]
    return out


# ---------------------------------------------------------------- svg
def build(variant: str = "ship") -> str:
    """Emit the master.

    variant "v1" is the first draft, kept reproducible so the audit sheet can
    score it honestly: flat slabs, no top face, no stand-off decay, one shared
    shadow. It is the take that proved the direction needs depth — see
    icon-notes.md.
    """
    v1 = variant == "v1"
    bars = layout(align="left" if variant == "left" else "centre")
    (kx1, ky1), (kx2, ky2) = KEY
    tf = (f'transform="translate({512 + OFFSET[0]},{512 + OFFSET[1]}) '
          f'scale({SCALE}) translate(-512,-512)"')

    lifts = tuple(0.0 for _ in LIFT) if v1 else LIFT
    accent = bars[-1]
    ACC_CY = accent[1] + (TOP_D + BAR_H) / 2

    # per-bar top-face gradients along the one key axis, so a slab lower in the
    # tile is lit slightly less — the same lamp, honestly applied
    top_grads = []
    for i, (cx, ty, fy, by, w) in enumerate(bars):
        top_grads.append(
            f'<linearGradient id="top{i}" gradientUnits="userSpaceOnUse" '
            f'x1="{cx - w / 2:.0f}" y1="{ty:.0f}" x2="{cx + w / 2:.0f}" y2="{fy:.0f}">'
            f'<stop offset="0" stop-color="{SLAB_TOP_HI}"/>'
            f'<stop offset="1" stop-color="{SLAB_TOP_LO}"/></linearGradient>')
        top_grads.append(
            f'<linearGradient id="face{i}" gradientUnits="userSpaceOnUse" '
            f'x1="0" y1="{fy:.0f}" x2="0" y2="{by:.0f}">'
            f'<stop offset="0"    stop-color="{SLAB_FACE_HI}"/>'
            f'<stop offset="0.46" stop-color="{SLAB_FACE_MID}"/>'
            f'<stop offset="0.88" stop-color="{SLAB_FACE_LO}"/>'
            f'<stop offset="1"    stop-color="{SLAB_DEEP}"/></linearGradient>')
        # r03: the fold was a 2.4px hairline and it disappeared at 1024, so the
        # lighter top face read as a painted stripe on a flat bar rather than as
        # a surface at an angle to it. A slab's top face casts onto its own front
        # face; that short AO band under the overhang is what makes the fold an
        # edge, and it is the cheapest depth cue in the tile.
        top_grads.append(
            f'<linearGradient id="fold{i}" gradientUnits="userSpaceOnUse" '
            f'x1="0" y1="{fy:.0f}" x2="0" y2="{fy + 14:.0f}">'
            f'<stop offset="0"   stop-color="#131A26" stop-opacity="0.52"/>'
            f'<stop offset="0.5" stop-color="#131A26" stop-opacity="0.20"/>'
            f'<stop offset="1"   stop-color="#131A26" stop-opacity="0"/></linearGradient>')
        # the rim light falls off away from the key rather than running at one
        # opacity end to end, which is the difference between light on an edge
        # and a line drawn along it
        top_grads.append(
            f'<linearGradient id="lip{i}" gradientUnits="userSpaceOnUse" '
            f'x1="{cx - w / 2:.0f}" y1="0" x2="{cx + w / 2:.0f}" y2="0">'
            f'<stop offset="0"    stop-color="{SLAB_LIP}" stop-opacity="0.30"/>'
            f'<stop offset="0.24" stop-color="{SLAB_LIP}" stop-opacity="0.72"/>'
            f'<stop offset="1"    stop-color="{SLAB_LIP}" stop-opacity="0.22"/>'
            f'</linearGradient>')

    defs = f"""
  <defs>
    <!-- the tile is a cushion: bright near the key, vignetted at the rim.
         Values lifted verbatim from shipyard so the shelf reads as one set. -->
    <radialGradient id="cushion" cx="0.36" cy="0.20" r="0.98">
      <stop offset="0"    stop-color="{GROUND_HI}"/>
      <stop offset="0.50" stop-color="{GROUND_MID}"/>
      <stop offset="1"    stop-color="{GROUND_LO}"/>
    </radialGradient>
    <radialGradient id="vignette" cx="0.5" cy="0.48" r="0.74">
      <stop offset="0.58" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="1"    stop-color="{VIGNETTE}" stop-opacity="0.17"/>
    </radialGradient>

    {g(top_grads)}

    <!-- porcelain light coming back up under a slab that has not landed -->
    <linearGradient id="bounceup" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{SLAB_BOUNCE}" stop-opacity="0"/>
      <stop offset="1" stop-color="{SLAB_BOUNCE}" stop-opacity="0.42"/>
    </linearGradient>

    <!-- the accent. Dark saturated body, much brighter lit face, per apple-26.
         r02: the top face now stays at the LIFTED register for most of its run
         rather than ramping down through it. At r01 the accent's lit face and the
         slate slabs' lit faces measured 1.02:1 — identical luminance, adjacent
         hue — so the accent read as "the teal one" rather than as the lit one,
         which is the whole point of the tile. -->
    <!-- r05: the accent measured 3.43:1 across its own fold where every slate
         slab measures 2.23:1, so its pale top read as a mint cap stuck onto a
         dark body rather than as one lit object. The body now starts BRIGHT
         immediately under the fold and deepens from there — apple-06's
         emissive-from-within tell — which closes the fold and keeps the lit face
         chromatic instead of near-white. -->
    <linearGradient id="accface" gradientUnits="userSpaceOnUse"
        x1="0" y1="{accent[2]:.0f}" x2="0" y2="{accent[3]:.0f}">
      <stop offset="0"    stop-color="{TEAL_HI}"/>
      <stop offset="0.24" stop-color="{TEAL_MID}"/>
      <stop offset="0.52" stop-color="{TEAL_CORE}"/>
      <stop offset="0.86" stop-color="{TEAL_DEEP}"/>
      <stop offset="1"    stop-color="{TEAL_CORE}"/>
    </linearGradient>
    <linearGradient id="acctop" gradientUnits="userSpaceOnUse"
        x1="{accent[0] - accent[4] / 2:.0f}" y1="{accent[1]:.0f}"
        x2="{accent[0] + accent[4] / 2:.0f}" y2="{accent[2]:.0f}">
      <stop offset="0"    stop-color="{TEAL_LIFT}"/>
      <stop offset="0.48" stop-color="{TEAL_LIFT}"/>
      <stop offset="1"    stop-color="{TEAL_HI}"/>
    </linearGradient>
    <!-- emissive from within: the body glows just under its own lit fold -->
    <linearGradient id="accinner" gradientUnits="userSpaceOnUse"
        x1="0" y1="{accent[2]:.0f}" x2="0" y2="{accent[2] + 26:.0f}">
      <stop offset="0" stop-color="{TEAL_LIFT}" stop-opacity="0.26"/>
      <stop offset="1" stop-color="{TEAL_LIFT}" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="wellTight" gradientUnits="userSpaceOnUse"
        cx="{accent[0] + DX:.0f}" cy="{ACC_CY:.0f}" r="{HALO_R_TIGHT:.0f}"
        gradientTransform="translate(0,{ACC_CY * (1 - HALO_SQUASH):.1f}) scale(1,{HALO_SQUASH})">
      <stop offset="0"    stop-color="{TEAL_GLOW}" stop-opacity="0.42"/>
      <stop offset="0.50" stop-color="{TEAL_GLOW}" stop-opacity="0.18"/>
      <stop offset="1"    stop-color="{TEAL_GLOW}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="wellWide" gradientUnits="userSpaceOnUse"
        cx="{accent[0] + DX:.0f}" cy="{ACC_CY:.0f}" r="{HALO_R_WIDE:.0f}"
        gradientTransform="translate(0,{ACC_CY * (1 - HALO_SQUASH):.1f}) scale(1,{HALO_SQUASH})">
      <stop offset="0"    stop-color="{TEAL_GLOW}" stop-opacity="0.13"/>
      <stop offset="0.56" stop-color="{TEAL_GLOW}" stop-opacity="0.05"/>
      <stop offset="1"    stop-color="{TEAL_GLOW}" stop-opacity="0"/>
    </radialGradient>
    <!-- the spill is a falloff from the emitter, so it warms only the slab the
         accent actually faces. A gradient clipped to every slab would spend the
         accent on decoration; shipyard learned that at r02. -->
    <radialGradient id="spill" gradientUnits="userSpaceOnUse"
        cx="{accent[0] + DX:.0f}" cy="{accent[1] - 6:.0f}" r="{SPILL_R:.0f}">
      <stop offset="0"    stop-color="{TEAL_GLOW}" stop-opacity="0.34"/>
      <stop offset="0.42" stop-color="{TEAL_GLOW}" stop-opacity="0.11"/>
      <stop offset="1"    stop-color="{TEAL_GLOW}" stop-opacity="0"/>
    </radialGradient>

    <filter id="blurS" x="-60%" y="-160%" width="220%" height="420%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
    <filter id="blurM" x="-60%" y="-160%" width="220%" height="420%">
      <feGaussianBlur stdDeviation="13"/>
    </filter>
    <filter id="blurL" x="-70%" y="-200%" width="240%" height="500%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>

    <clipPath id="clipFace3">
      <path d="{rrect(bars[3][0], bars[3][2], bars[3][4], BAR_H, 0, RX)}"/>
    </clipPath>
  </defs>"""

    # ---- bg: the cushion tile, and the accent's widest halo
    bg = f"""
  <g id="bg">
    <rect width="1024" height="1024" fill="url(#cushion)"/>
    <rect width="1024" height="1024" fill="url(#vignette)"/>
    {'' if v1 else '<rect width="1024" height="1024" fill="url(#wellWide)"/>'}
  </g>"""

    # ---- mid: the cast shadows. This layer IS the stand-off record — a slab
    #      that floats casts wide, soft and faint; a slab that has landed casts
    #      tight and dark. Nothing else in the tile carries the height.
    sh = []
    if v1:
        cx, ty, _, by, w = bars[0]
        sh.append(f'<rect x="{cx - w / 2:.0f}" y="{bars[-1][3] + 10:.0f}" '
                  f'width="{w:.0f}" height="26" rx="13" fill="{SHADOW}" '
                  f'opacity="0.18" filter="url(#blurM)"/>')
    else:
        for i, ((cx, ty, fy, by, w), lift) in enumerate(zip(bars, lifts)):
            if lift <= 0:
                continue                     # the landed slab casts contact, not a shadow
            sw = w * (1 + lift * SH_SPREAD)
            sx = cx + lift * SH_DX_GAIN
            sy = ty + SH_DY + lift * SH_DY_GAIN
            op = SH_OP - lift * SH_OP_DECAY
            blur = "blurS" if lift < 12 else ("blurM" if lift < 32 else "blurL")
            # a displaced copy of the slab's own silhouette: cast, not smeared
            sh.append(f'<path d="{rrect(sx, sy, sw, TOP_D + BAR_H, RX, RX)}" '
                      f'fill="{SHADOW}" opacity="{op:.3f}" filter="url(#{blur})"/>')
        # the landed slab: a tight dark line welded to its base, no gap, barely
        # blurred. The difference between this and a displaced soft copy is the
        # only place the stand-off is recorded, so it has to be unmistakable.
        cx, _, _, by, w = accent
        sh.append(f'<path d="{rrect(cx, by - 6, w + 14, 16, 8, 8)}" fill="#0C2A2F" '
                  f'opacity="0.46" filter="url(#blurS)"/>')

    mid = f"""
  <g id="mid" {tf}>
    {g(sh)}
  </g>"""

    # ---- fg: the four slate slabs. One material, no value ramp down the stack —
    #      a ramp would say "more is better", which is the reading this tile
    #      exists to refuse. Only width and stand-off vary.
    slabs = []
    for i, ((cx, ty, fy, by, w), lift) in enumerate(zip(bars[:-1], lifts[:-1])):
        h = TOP_D + BAR_H
        slabs.append(f'<path d="{rrect(cx, ty, w, h, RX, RX)}" fill="url(#face{i})"/>')
        if not v1:
            slabs.append(f'<path d="{rrect(cx, ty, w, TOP_D, RX, 0)}" '
                         f'fill="url(#top{i})"/>')
            slabs.append(f'<path d="{rrect(cx, fy, w, 14, 0, 0)}" '
                         f'fill="url(#fold{i})"/>')
            slabs.append(f'<path d="{hline(cx, fy, w, 2)}" stroke="{SLAB_SEAM}" '
                         f'stroke-width="2" stroke-opacity="0.62" fill="none"/>')
        # the rim light on the top edge — the one crisp line per slab
        lip = f'url(#lip{i})' if not v1 else SLAB_LIP
        lip_op = '' if not v1 else ' stroke-opacity="0.34"'
        slabs.append(f'<path d="{hline(cx, ty + 3, w, RX * 0.72)}" '
                     f'stroke="{lip}" stroke-width="4" stroke-linecap="round"'
                     f'{lip_op} fill="none"/>')
        if not v1:
            # bounce is strongest on the slab CLOSEST to the porcelain, which is
            # the one furthest down the settle. Another honest reading of height.
            # r02: r01 ran this to 0.67 on the lowest floater and it read as a
            # painted stripe rather than as an underside catching light.
            b = 0.10 + 0.30 * (1 - lift / max(lifts[0], 1e-6))
            slabs.append(f'<path d="{hline(cx, by - 3.2, w, RX * 1.15)}" '
                         f'stroke="{SLAB_BOUNCE}" stroke-width="2.6" '
                         f'stroke-linecap="round" stroke-opacity="{b:.2f}" fill="none"/>')

    fg = f"""
  <g id="fg" {tf}>
    {g(slabs)}
  </g>"""

    # ---- highlight: the accent slab, and only what its light actually touches
    cx, ty, fy, by, w = accent
    h = TOP_D + BAR_H
    if v1:
        hl_inner = (f'<path d="{rrect(cx, ty, w, h, RX, RX)}" fill="{TEAL_CORE}"/>'
                    f'<path d="{hline(cx, ty + 2.6, w, RX * 0.72)}" stroke="{TEAL_LIFT}" '
                    f'stroke-width="4" stroke-linecap="round" stroke-opacity="0.7" fill="none"/>')
    else:
        hl_inner = f"""
    <!-- The spill, before the accent itself, because it belongs to the slab
         above. r01 washed the whole of slab 4's face and it read two-tone, like
         a rendering fault; r02 keeps the radial tight and adds the crisp part —
         one teal rim on slab 4's UNDERSIDE, which is the edge the emitter
         actually faces. Slab 3 gets nothing: an emitter's spill is a falloff
         from the emitter, not a curtain over everything it might touch. -->
    <g clip-path="url(#clipFace3)">
      <rect x="0" y="0" width="1024" height="1024" fill="url(#spill)"/>
    </g>
    <path d="{hline(bars[3][0], bars[3][3] - 3.2, bars[3][4], RX * 1.15)}"
          stroke="{TEAL_LIFT}" stroke-width="3" stroke-linecap="round"
          stroke-opacity="0.42" fill="none"/>

    <rect width="1024" height="1024" fill="url(#wellTight)"/>

    <path d="{rrect(cx, ty, w, h, RX, RX)}" fill="url(#accface)"/>
    <path d="{rrect(cx, ty, w, TOP_D, RX, 0)}" fill="url(#acctop)"/>
    <path d="{rrect(cx, fy, w, 30, 0, 0)}" fill="url(#accinner)"/>
    <path d="{hline(cx, fy, w, 2)}" stroke="{TEAL_LIP}" stroke-width="2"
          stroke-opacity="0.24" fill="none"/>
    <path d="{hline(cx, ty + 3, w, RX * 0.72)}" stroke="{TEAL_SUN}"
          stroke-width="4.4" stroke-linecap="round" stroke-opacity="0.92" fill="none"/>
    <path d="{hline(cx, ty + 3, w, RX * 1.6)}" stroke="{TEAL_LIP}"
          stroke-width="2" stroke-linecap="round" stroke-opacity="0.60" fill="none"/>
    <path d="{rrect(cx, ty, w, h, RX, RX)}" fill="none" stroke="{TEAL_LIFT}"
          stroke-width="2" stroke-opacity="0.34"/>"""

    hl = f"""
  <g id="highlight">
   <g {tf}>
    {hl_inner}
   </g>
    <path d="{SQ}" fill="none" stroke="#FFFFFF" stroke-opacity="0.55" stroke-width="5"
          transform="translate(3.07,3.07) scale(0.994)"/>
  </g>"""

    title = {"ship": "warrant — the authority ladder, settling into the scope it has earned",
             "v1": "warrant — first draft: flat ladder, no stand-off",
             "left": "warrant — left-aligned alternative: the same ladder as a bar chart",
             }[variant]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{W}" '
            f'viewBox="0 0 {W} {W}">\n'
            f'  <title>{title}</title>'
            f'{defs}{bg}{mid}{fg}{hl}\n</svg>\n')


# ---------------------------------------------------------------- exports
EXPORTS = [("icon.png", 1024), ("icon-256.png", 256), ("icon-128.png", 128)]


def _mask(size: int):
    from PIL import Image
    svg, png = HERE / "_mask.svg", HERE / "_mask.png"
    svg.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1024" '
                   f'height="1024" viewBox="0 0 1024 1024"><path d="{SQ}" fill="#fff"/></svg>')
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size),
                    str(svg), "-o", str(png)], check=True)
    a = Image.open(png).convert("RGBA").split()[3]
    svg.unlink(missing_ok=True)
    png.unlink(missing_ok=True)
    return a


def _lum(p):
    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(p[0]) + 0.7152 * f(p[1]) + 0.0722 * f(p[2])


def _ratio(a, b):
    la, lb = _lum(a), _lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def render_and_measure():
    """Export the shipped PNGs, then measure the things the notes quote.

    Marketplace tiles are decorative PNGs rather than Icon Composer input, so the
    squircle mask has to be baked into the file.
    """
    from PIL import Image
    full = HERE / "_full.png"
    subprocess.run(["rsvg-convert", "-w", "1024", "-h", "1024",
                    str(HERE / "icon.svg"), "-o", str(full)], check=True)
    base = Image.open(full).convert("RGBA")
    for name, size in EXPORTS:
        im = base.resize((size, size), Image.LANCZOS)
        im.putalpha(_mask(size))
        im.save(HERE / name)
        print(f"  {name}  {size}x{size}")

    rgb = base.convert("RGB")
    bars = layout()

    # Rubric #2 is judged on the INK bbox, not on an area-weighted centroid — a
    # top-heavy stack legitimately carries its area high while its outline sits
    # centred, and reading the centroid as the centring instrument sent r03 and
    # r04 looking for a composition fault that was not there.
    por = [_lum(rgb.getpixel(p)) for p in
           ((40, 40), (984, 40), (40, 984), (984, 984), (60, 512), (964, 512))]
    thr = min(por) - 0.10
    xs, ys = [], []
    for x in range(0, 1024, 2):
        for y in range(0, 1024, 2):
            if _lum(rgb.getpixel((x, y))) < thr:
                xs.append(x)
                ys.append(y)
    print(f"\n  porcelain L range                {min(por):.3f}..{max(por):.3f}")
    print(f"  ink bbox                         ({min(xs)},{min(ys)})-({max(xs)},{max(ys)})"
          f"  {max(xs) - min(xs)}x{max(ys) - min(ys)}")
    print(f"  ink bbox centre                  {(min(xs) + max(xs)) / 2:.0f}, "
          f"{(min(ys) + max(ys)) / 2:.0f}   target 512, 512")
    print(f"  object fills                     "
          f"{(max(xs) - min(xs)) / 1024:.0%} x {(max(ys) - min(ys)) / 1024:.0%} of the tile")

    ground = rgb.getpixel((96, 210))
    ground_lo = rgb.getpixel((900, 880))
    slab_face = rgb.getpixel((512, int(bars[0][2] + BAR_H * 0.5)))
    slab_top = rgb.getpixel((512, int(bars[0][1] + TOP_D * 0.5)))
    acc_face = rgb.getpixel((512, int(bars[4][2] + BAR_H * 0.5)))
    acc_top = rgb.getpixel((512, int(bars[4][1] + TOP_D * 0.5)))
    # r04/r07: the well hugs the slab now, so a probe 26px BELOW the base — and
    # then one 34px to its right — both landed outside a well that is plainly
    # there and reported it at 1.00-1.11:1. Probe just off the slab's edge.
    well = rgb.getpixel((int(bars[4][0] + bars[4][4] / 2 + 40),
                         int(bars[4][1] + (TOP_D + BAR_H) / 2)))

    print("\nfigure-ground, measured on the shipped 1024 render")
    print(f"  slate front face vs tile   {_ratio(slab_face, ground):.2f}:1")
    print(f"  slate top face vs tile     {_ratio(slab_top, ground):.2f}:1")
    print(f"  accent front face vs tile  {_ratio(acc_face, ground):.2f}:1")
    print(f"  accent top vs accent face  {_ratio(acc_top, acc_face):.2f}:1")
    print(f"  accent top vs slate top    {_ratio(acc_top, slab_top):.2f}:1")
    print(f"  halo well vs tile          {_ratio(well, ground_lo):.2f}:1")
    print(f"  accent top  {acc_top}   accent face {acc_face}   well {well}")

    for s in (32, 16):
        grey = rgb.convert("L").resize((s, s), Image.LANCZOS)
        px = list(grey.getdata())
        print(f"  {s}px luminance spread      {(max(px) - min(px)) / 255:.3f}")

    # The one check the direction lives or dies on: are five bars still countable?
    # Read the centre column of the real 128px export and count dark runs.
    for s in (128, 64, 48, 32):
        im = base.resize((s, s), Image.LANCZOS).convert("L")
        col = [im.getpixel((s // 2, y)) for y in range(s)]
        hi, lo = max(col), min(col)
        thr = lo + (hi - lo) * 0.55
        runs, prev, lens = 0, False, []
        for v in col:
            dark = v < thr
            if dark and not prev:
                runs += 1
                lens.append(0)
            if dark:
                lens[-1] += 1
            prev = dark
        flag = "" if runs == 5 else "   <-- FAIL"
        print(f"  {s}px countable bars        {runs}  (want 5)  runs={lens}{flag}")

    full.unlink(missing_ok=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="ship", choices=("ship", "v1", "left"))
    ap.add_argument("--svg-only", action="store_true")
    a = ap.parse_args()
    out = HERE / ("icon.svg" if a.variant == "ship" else f"icon-A-{a.variant}.svg")
    out.write_text(build(a.variant))
    print(f"wrote {out.name}  ({out.stat().st_size / 1024:.1f} KB)")
    if a.variant == "ship" and not a.svg_only:
        render_and_measure()
