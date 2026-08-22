#!/usr/bin/env python3
"""flagship icon — "Pennant on the halyard".

Geometry and material as named constants so a later fidelity round is a parameter edit
rather than path surgery. Family register lifted from ship-armada/assets/icon-notes.md:
Tahoe gel-glass sub-register (a) — porcelain ground carrying one coloured gel object.

Subject: a flagship carries the commander and the SIGNALS; it does not command the other
ships' masters. So the glyph is the signal, not the fleet — which also keeps it clearly
distinct from ship-armada's plan-view hulls.

Traps pre-empted, each from ship-armada's own render loop:
  * a solid taper, bright tip over dark base, reads as a FLAME -> ramp flattened and
    weighted dark, brightest value held at the hoist rather than the fly.
  * axis-aligned symmetric points read as ORDNANCE -> the pennant sits on a real diagonal
    and the swallowtail breaks the symmetry.
  * an objectBoundingBox gradient on a zero-width path renders as NOTHING -> every
    gradient here is userSpaceOnUse.
"""
from pathlib import Path

S = 1024

# --- palette: two hue families only, graphite is a neutral rather than a third hue ---
PLATE_HI, PLATE_MID, PLATE_LO = "#FEFCF7", "#F8F1E4", "#EBE1CE"
VIGNETTE = "#7A6244"
GEL_1, GEL_2, GEL_3, GEL_4 = "#F2683A", "#E54824", "#D63A20", "#B92E1D"
GEL_DEEP_A, GEL_DEEP_B = "#B0261C", "#7F1721"
INK = "#6E7A86"

# --- geometry ---
MAST_X      = 232.0          # halyard, left of centre so the fly has room to stream
MAST_TOP    = 138.0
MAST_BOT    = 872.0
MAST_W      = 19.0
TRUCK_R     = 30.0           # the ball at the masthead
HOIST_Y     = 250.0          # where the pennant bends on
HOIST_H     = 306.0          # luff depth at the mast
FLY_X       = 884.0          # tip of the fly
FLY_Y       = 470.0          # dropped below hoist -> real diagonal, not axis-aligned
TAIL_BITE   = 168.0           # swallowtail depth
GRATICULE_STEP = 128.0
GRAT_OPACITY   = 0.10
GRAT_THROUGH   = 0.19        # the authored overlap: chart redrawn clipped to the gel


def pennant():
    """Luff at the mast, two edges sweeping to a swallowtail fly."""
    top_y, bot_y = HOIST_Y, HOIST_Y + HOIST_H
    notch_x, notch_y = FLY_X - TAIL_BITE, FLY_Y + 6.0
    return (
        f"M{MAST_X:.1f},{top_y:.1f} "
        f"C{MAST_X+150:.1f},{top_y+8:.1f} {FLY_X-210:.1f},{FLY_Y-96:.1f} {FLY_X:.1f},{FLY_Y-30:.1f} "
        f"L{notch_x:.1f},{notch_y:.1f} L{FLY_X:.1f},{FLY_Y+46:.1f} "
        f"C{FLY_X-200:.1f},{FLY_Y+128:.1f} {MAST_X+156:.1f},{bot_y+30:.1f} {MAST_X:.1f},{bot_y:.1f} Z"
    )


def graticule():
    out = []
    n = 1
    while n * GRATICULE_STEP < S:
        v = n * GRATICULE_STEP
        out.append(f'<line x1="{v}" y1="0" x2="{v}" y2="{S}"/>')
        out.append(f'<line x1="0" y1="{v}" x2="{S}" y2="{v}"/>')
        n += 1
    return "\n      ".join(out)


def svg():
    p = pennant()
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">
  <defs>
    <clipPath id="squircle"><path d="{Path("squircle-path.txt").read_text().strip()}"/></clipPath>
    <linearGradient id="plate" x1="0" y1="0" x2="0" y2="{S}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{PLATE_HI}"/><stop offset="0.55" stop-color="{PLATE_MID}"/>
      <stop offset="1" stop-color="{PLATE_LO}"/>
    </linearGradient>
    <radialGradient id="vig" cx="{S/2}" cy="{S*0.42}" r="{S*0.78}" gradientUnits="userSpaceOnUse">
      <stop offset="0.55" stop-color="{VIGNETTE}" stop-opacity="0"/>
      <stop offset="1" stop-color="{VIGNETTE}" stop-opacity="0.16"/>
    </radialGradient>
    <!-- flattened and weighted dark: brightest at the hoist, never a bright tip -->
    <linearGradient id="gel" x1="{MAST_X}" y1="{HOIST_Y}" x2="{FLY_X}" y2="{FLY_Y+60}"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{GEL_1}"/><stop offset="0.34" stop-color="{GEL_2}"/>
      <stop offset="0.68" stop-color="{GEL_3}"/><stop offset="1" stop-color="{GEL_4}"/>
    </linearGradient>
    <linearGradient id="gelshade" x1="{MAST_X}" y1="{HOIST_Y+HOIST_H}" x2="{FLY_X}" y2="{FLY_Y}"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{GEL_DEEP_B}" stop-opacity="0.42"/>
      <stop offset="1" stop-color="{GEL_DEEP_A}" stop-opacity="0.06"/>
    </linearGradient>
    <linearGradient id="rim" x1="{MAST_X}" y1="{HOIST_Y}" x2="{FLY_X*0.8}" y2="{HOIST_Y+40}"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.50"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.04"/>
    </linearGradient>
    <linearGradient id="fold" x1="{MAST_X}" y1="{HOIST_Y+HOIST_H-90}" x2="{MAST_X}" y2="{HOIST_Y+HOIST_H+40}"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{GEL_DEEP_B}" stop-opacity="0"/>
      <stop offset="1" stop-color="{GEL_DEEP_B}" stop-opacity="0.55"/>
    </linearGradient>
    <linearGradient id="sheen" x1="{MAST_X}" y1="{HOIST_Y+70}" x2="{FLY_X*0.72}" y2="{HOIST_Y+210}"
                    gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.26"/>
      <stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0.09"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="pennantClip"><path d="{p}"/></clipPath>
  </defs>

  <g clip-path="url(#squircle)">
    <g id="bg">
      <rect width="{S}" height="{S}" fill="url(#plate)"/>
      <g stroke="{INK}" stroke-width="2.5" opacity="{GRAT_OPACITY}">
      {graticule()}
      </g>
      <rect width="{S}" height="{S}" fill="url(#vig)"/>
    </g>

    <g id="mid">
      <!-- halyard: chart ink, drawn behind the gel so the pennant bends on in front -->
      <rect x="{MAST_X - MAST_W/2:.1f}" y="{MAST_TOP}" width="{MAST_W}" height="{MAST_BOT-MAST_TOP}"
            rx="{MAST_W/2:.1f}" fill="{INK}" opacity="0.62"/>
      <circle cx="{MAST_X}" cy="{MAST_TOP}" r="{TRUCK_R}" fill="{INK}" opacity="0.62"/>
      <ellipse cx="{MAST_X+14:.1f}" cy="{MAST_BOT+16:.1f}" rx="86" ry="15"
               fill="{VIGNETTE}" opacity="0.13"/>
    </g>

    <g id="fg">
      <path d="{p}" fill="url(#gel)"/>
      <path d="{p}" fill="url(#gelshade)"/>
      <g clip-path="url(#pennantClip)"><rect x="0" y="{HOIST_Y+HOIST_H-90:.0f}" width="{S}" height="140" fill="url(#fold)"/></g>
      <g clip-path="url(#pennantClip)"><rect width="{S}" height="{S}" fill="url(#sheen)"/></g>
      <!-- authored overlap: the chart reads THROUGH the gel -->
      <g clip-path="url(#pennantClip)" stroke="#FFE2CF" stroke-width="2.5" opacity="{GRAT_THROUGH}">
      {graticule()}
      </g>
    </g>

    <g id="highlight">
      <path d="M{MAST_X:.1f},{HOIST_Y:.1f} C{MAST_X+150:.1f},{HOIST_Y+8:.1f} {FLY_X-210:.1f},{FLY_Y-96:.1f} {FLY_X:.1f},{FLY_Y-30:.1f}"
            fill="none" stroke="url(#rim)" stroke-width="7" stroke-linecap="round"/>
      <path d="{p}" fill="none" stroke="{GEL_DEEP_B}" stroke-width="1.5" opacity="0.20"/>
    </g>
  </g>
</svg>
'''


if __name__ == "__main__":
    Path("icon.svg").write_text(svg())
    print("wrote icon.svg")
