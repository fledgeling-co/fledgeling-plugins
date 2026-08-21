#!/usr/bin/env python3
"""Generate the recover-claude-code icon: two links threaded together, one ember weld.

Geometry and material are named constants so a later change is a constant edit rather
than path surgery.

The metaphor is reattachment. Not "fix a broken thing" — that is mac-doctor's ring with a
missing arc — but joining two things that were each whole and had come apart: a session
and the agent context that belongs to it. Two links threaded through each other say that,
and a chain of two still reads as a chain at 16px.

Two composition rules, both bought by a failed first attempt. Mirrored tilt makes the pair
symmetric and it stops reading as two objects: the first build put both stadiums at ±30
degrees and rendered a heart. And the links have to overlap *only at their ends*, because
an overlap through the middle merges the silhouettes. So: two horizontal links, side by
side, meeting in a narrow interlock, with one bar passing over and the other under.

Palette, light model and ground are lifted verbatim from plugins/mac-doctor/assets so this
sits in the family: porcelain ground, one charcoal-navy object, one warm ember accent, key
light upper-left. The squircle is the shared path every icon in the set uses.
"""
from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parent
SQUIRCLE = (Path(__file__).resolve().parents[2] / "create-mac-icon" /
            "assets" / "squircle-path.txt")

# ---------------------------------------------------------------- geometry
S = 1024
CX = CY = 512

L_HALF = 258            # outer half-length of a link
H_HALF = 152            # outer half-height
BAND = 88               # tube thickness; holds its shading down to 32px
OFFSET = 202            # centre of each link from the tile centre
                        # overlap = 2*(L_HALF - OFFSET) = 112, a narrow interlock
LEAN = -8.0             # a few degrees off horizontal, so it is drawn not diagrammed
SCALE = 0.94

WELD_RX, WELD_RY = 74, 104   # the bloom, taller than wide to sit in the interlock
WELD_CORE = 26

# ---------------------------------------------------------------- material
GROUND_TOP, GROUND_MID, GROUND_BOT = "#FDFDFC", "#F5EEE7", "#EDE9DF"

WALL_LIT = "#465272"
FACE_BOUNCE = "#3A455E"
FACE_DARK = "#16283F"
FACE_SHOULDER = "#505E7C"
FACE_OUT = "#37455F"
SPEC = "#EEF3FB"
BOUNCE = "#A9B8D4"

EM_FACE_DARK = "#DF2700"
EM_FACE_SHOULDER = "#FF4E18"
EM_SPEC = "#FFE0C4"

BEVEL = 8.0
SHADOW_A = 0.30


def stadium(cx: float, cy: float, hw: float, hh: float) -> str:
    """A rounded rectangle whose radius is its short half-axis, drawn clockwise."""
    r = min(hw, hh)
    return (f"M{cx - hw + r:.2f},{cy - hh:.2f}"
            f"L{cx + hw - r:.2f},{cy - hh:.2f}"
            f"A{r:.2f},{r:.2f} 0 0 1 {cx + hw - r:.2f},{cy + hh:.2f}"
            f"L{cx - hw + r:.2f},{cy + hh:.2f}"
            f"A{r:.2f},{r:.2f} 0 0 1 {cx - hw + r:.2f},{cy - hh:.2f}Z")


def ring(cx: float, cy: float, hw: float, hh: float, band: float) -> str:
    """A link body: outer stadium with the inner one subtracted, filled even-odd."""
    return stadium(cx, cy, hw, hh) + " " + stadium(cx, cy, hw - band, hh - band)


def link(gid: str, cx: float, lean: float) -> str:
    """One link: face ramp across the tube, bevel walls, ground bounce, one specular.

    The specular is an explicit arc on the upper-left shoulder rather than a dashed
    outline, because a dash pattern on a stadium puts highlights wherever the path
    happens to start and the light stops being one source.
    """
    hw, hh = L_HALF, H_HALF
    r_in = min(hw - BAND, hh - BAND)
    return f"""
    <g transform="rotate({lean:.2f} {cx:.2f} {CY})">
      <path d="{ring(cx, CY, hw, hh, BAND)}" fill="url(#face{gid})" fill-rule="evenodd" />
      <path d="{stadium(cx, CY, hw - BEVEL / 2, hh - BEVEL / 2)}" fill="none"
            stroke="{WALL_LIT}" stroke-width="{BEVEL:.2f}" opacity="0.80" />
      <path d="{stadium(cx, CY, hw - BAND + BEVEL / 2, hh - BAND + BEVEL / 2)}"
            fill="none" stroke="{BOUNCE}" stroke-width="{BEVEL * 0.9:.2f}" opacity="0.40" />
      <path d="M{cx - hw + BAND * 0.5:.2f},{CY - hh + BAND * 0.42:.2f}
               L{cx + hw * 0.05:.2f},{CY - hh + BAND * 0.42:.2f}"
            fill="none" stroke="{SPEC}" stroke-width="{BAND * 0.13:.2f}"
            stroke-linecap="round" opacity="0.38" />
    </g>"""


def face_gradient(gid: str) -> str:
    """Across-the-tube ramp: bounce-lifted inner shoulder, section minimum past the
    middle, turning down again at the far wall. Stops are mac-doctor's, which were
    sampled off the macOS 26 corpus rather than guessed."""
    return f"""
    <linearGradient id="face{gid}" x1="0.20" y1="0.02" x2="0.80" y2="1.00">
      <stop offset="0.00" stop-color="{FACE_BOUNCE}" />
      <stop offset="0.17" stop-color="{FACE_SHOULDER}" />
      <stop offset="0.53" stop-color="{FACE_DARK}" />
      <stop offset="0.82" stop-color="{FACE_SHOULDER}" />
      <stop offset="1.00" stop-color="{FACE_OUT}" />
    </linearGradient>"""


def build() -> str:
    squircle = SQUIRCLE.read_text().strip()
    lx, rx = CX - OFFSET, CX + OFFSET
    ov = L_HALF - OFFSET            # half-width of the interlock zone

    left = link("L", lx, LEAN)
    right = link("R", rx, LEAN)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}"
     viewBox="0 0 {S} {S}">
  <defs>
    <linearGradient id="ground" x1="0.30" y1="0" x2="0.62" y2="1">
      <stop offset="0" stop-color="{GROUND_TOP}" />
      <stop offset="0.55" stop-color="{GROUND_MID}" />
      <stop offset="1" stop-color="{GROUND_BOT}" />
    </linearGradient>
    {face_gradient("L")}
    {face_gradient("R")}
    <radialGradient id="weld" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0.00" stop-color="#FFF3E6" stop-opacity="0.97" />
      <stop offset="0.24" stop-color="{EM_SPEC}" stop-opacity="0.88" />
      <stop offset="0.52" stop-color="{EM_FACE_SHOULDER}" stop-opacity="0.80" />
      <stop offset="0.78" stop-color="{EM_FACE_DARK}" stop-opacity="0.26" />
      <stop offset="1.00" stop-color="{EM_FACE_DARK}" stop-opacity="0" />
    </radialGradient>
    <radialGradient id="contact" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#6B5B4A" stop-opacity="{SHADOW_A}" />
      <stop offset="0.62" stop-color="#6B5B4A" stop-opacity="{SHADOW_A * 0.34:.3f}" />
      <stop offset="1" stop-color="#6B5B4A" stop-opacity="0" />
    </radialGradient>
    <clipPath id="tile"><path d="{squircle}" /></clipPath>
    <!-- the interlock's upper half: where the left link is drawn again, over the right -->
    <clipPath id="weave">
      <rect x="{CX - ov - BAND:.0f}" y="0" width="{2 * ov + 2 * BAND:.0f}" height="{CY}" />
    </clipPath>
  </defs>

  <g clip-path="url(#tile)">
    <rect width="{S}" height="{S}" fill="url(#ground)" />
    <ellipse cx="{CX + 14}" cy="{CY + H_HALF * 1.42:.0f}" rx="{L_HALF * 1.42:.0f}"
             ry="{H_HALF * 0.42:.0f}" fill="url(#contact)" />

    <g transform="translate({CX} {CY}) scale({SCALE}) translate({-CX} {-CY})">
      <!-- left link, then right over it, then the left link's top bar back on top:
           one bar over and one under is what makes them threaded rather than stacked -->
      {left}
      {right}
      <g clip-path="url(#weave)">{left}</g>

      <!-- the weld: the one warm thing in the tile, sitting in the interlock -->
      <ellipse cx="{CX:.0f}" cy="{CY:.0f}" rx="{WELD_RX}" ry="{WELD_RY}"
               fill="url(#weld)" />
      <circle cx="{CX:.0f}" cy="{CY:.0f}" r="{WELD_CORE}" fill="#FFF6EC" opacity="0.95" />
      <circle cx="{CX:.0f}" cy="{CY:.0f}" r="{WELD_CORE * 0.5:.0f}" fill="#FFFFFF" />
    </g>
  </g>
</svg>
"""


if __name__ == "__main__":
    svg = build()
    (OUT / "icon-src.svg").write_text(svg)
    (OUT / "icon.svg").write_text(svg)
    print(f"wrote {OUT / 'icon.svg'} ({len(svg)} bytes)")
