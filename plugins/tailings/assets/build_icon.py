#!/usr/bin/env python3
"""Master generator — tailings, direction "What the Screen Kept".

A sieve seen at a slight tilt. The bulk of the material has already gone through
and falls away below as cool, faint, parallel silt — that is the first pass, and
it did most of the work. Caught in the mesh, and only there, three grains sit lit
warm from inside.

That is the whole semantic and the reason the skill exists: you do not re-mine the
mountain. The value of a second pass is entirely in the small number of things the
first one left on the screen, and the picture is worth nothing without the silt
below to say how much already went through honestly.

Geometry and material are named constants; a fidelity round is a parameter edit
here, never path surgery in icon.svg.

    python3 build_icon.py [out.svg]

Emits 1024x1024 full-bleed layered artwork. The marketplace superellipse is a
CLIP, never a baked corner radius and never a baked drop shadow.
"""
import pathlib
import sys

S = 1024
ASSETS = pathlib.Path(__file__).resolve().parent
SQUIRCLE = (ASSETS / "squircle-path.txt").read_text().strip()

# ------------------------------------------------------------------- material
# Cool graphite ground so the one warm accent has somewhere to be the only warm
# thing. Slate rather than blue-black: the family reads as tools, not as night.
BG_TOP, BG_BOT = "#2B3138", "#171B20"
FRAME, FRAME_LO = "#8E9AA6", "#5A6674"
MESH = "#7C8792"
SILT_HI, SILT_LO = "#96A3B0", "#3A434D"
GRAIN, GRAIN_CORE = "#E0A martin", "#FFD9A0"   # placeholder, fixed below
GRAIN, GRAIN_CORE = "#E0A55C", "#FFD9A0"

# ------------------------------------------------------------------- geometry
TILT = -17                 # degrees; enough to read as a held screen, not a table
CX, CY = 512, 392          # the screen sits high — the silt needs the lower third
FW, FH = 486, 274          # frame; wider than tall so the mesh reads as a screen
FR = 26                    # frame corner radius
BAR = 26                   # frame bar thickness
COLS, ROWS = 5, 3          # mesh density: coarse enough to read at 32px
GRAINS = [(-126, -18), (18, 34), (142, -46)]   # three, in the mesh, not in a row


def mesh(w, h, cols, rows):
    out = []
    for i in range(1, cols):
        x = -w / 2 + w * i / cols
        out.append(f'<line x1="{x:.1f}" y1="{-h/2:.1f}" x2="{x:.1f}" y2="{h/2:.1f}"/>')
    for j in range(1, rows):
        y = -h / 2 + h * j / rows
        out.append(f'<line x1="{-w/2:.1f}" y1="{y:.1f}" x2="{w/2:.1f}" y2="{y:.1f}"/>')
    return "\n      ".join(out)


def silt():
    """What already went through.

    An earlier draft placed this as a detached band low in the frame, and the two
    halves read as a panel and some scratches rather than as one action. It now
    starts inside the mesh and continues past the frame, so the picture shows
    material passing through rather than two objects stacked.
    """
    out = []
    spec = [(-176, 470, 190), (-124, 506, 250), (-64, 486, 214), (-8, 522, 268),
            (52, 500, 232), (112, 530, 262), (168, 502, 198), (-212, 452, 150),
            (214, 476, 156), (24, 470, 300), (-96, 462, 176)]
    for dx, y, ln in spec:
        x = 512 + dx
        op = 0.72 if abs(dx) < 130 else 0.44
        out.append(f'<line x1="{x}" y1="{y}" x2="{x - 22}" y2="{y + ln}" '
                   f'stroke="url(#silt)" stroke-width="11" stroke-linecap="round" opacity="{op}"/>')
    return "\n    ".join(out)


def grains():
    out = []
    for dx, dy in GRAINS:
        out.append(
            f'<g transform="translate({dx},{dy})">'
            f'<circle r="46" fill="url(#glow)" opacity="0.72"/>'
            f'<circle r="21" fill="{GRAIN}"/>'
            f'<circle r="10" cx="-4" cy="-4" fill="{GRAIN_CORE}"/></g>')
    return "\n        ".join(out)


def svg():
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">
  <defs>
    <clipPath id="sq"><path d="{SQUIRCLE}"/></clipPath>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{BG_TOP}"/><stop offset="1" stop-color="{BG_BOT}"/>
    </linearGradient>
    <linearGradient id="silt" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{SILT_HI}"/><stop offset="1" stop-color="{SILT_LO}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="frame" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{FRAME}"/><stop offset="1" stop-color="{FRAME_LO}"/>
    </linearGradient>
    <radialGradient id="glow"><stop offset="0" stop-color="{GRAIN_CORE}"/>
      <stop offset="1" stop-color="{GRAIN}" stop-opacity="0"/></radialGradient>
    <radialGradient id="lift" cx="0.5" cy="0.34" r="0.72">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.10"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <g clip-path="url(#sq)">
    <rect width="{S}" height="{S}" fill="url(#bg)"/>
    <rect width="{S}" height="{S}" fill="url(#lift)"/>

    <!-- the first pass: the bulk, already gone through -->
    {silt()}

    <g transform="translate({CX},{CY}) rotate({TILT})">
      <!-- the screen it fell through -->
      <g stroke="{MESH}" stroke-width="7" opacity="0.42" stroke-linecap="round">
      {mesh(FW - BAR * 2, FH - BAR * 2, COLS, ROWS)}
      </g>
      <rect x="{-FW/2}" y="{-FH/2}" width="{FW}" height="{FH}" rx="{FR}"
            fill="none" stroke="url(#frame)" stroke-width="{BAR}"/>

      <!-- what it kept: the only warm thing in the picture -->
      <g>
        {grains()}
      </g>
    </g>
  </g>
</svg>
'''


if __name__ == "__main__":
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ASSETS / "icon.svg")
    out.write_text(svg())
    print(f"wrote {out}")
