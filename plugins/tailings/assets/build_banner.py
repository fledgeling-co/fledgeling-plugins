#!/usr/bin/env python3
"""build_banner.py — the tailings banner, composed as SVG and rasterised by rsvg.

Not HTML, deliberately, and for the reason geminify's build_banner.py records: on
this machine the browser route cannot capture at 1600x520@2x, so an SVG composed
here and rasterised by rsvg-convert is the reproducible path.

rsvg resolves *installed* families and not webfonts, and it resolves an unknown
family silently to its fallback — which is how a banner ships in the default sans
while its source names something else. So this measures the inked width of the
wordmark under the chosen family and under a control, and refuses to write if they
match, because identical ink means the family never resolved.

That check earned its place twice here. Superclarendon was the first choice and
inks identically to Helvetica at 553px, so rsvg never resolves it on this machine
and the banner would have shipped in the fallback face. American Typewriter inks
615px against the control's 553px, and it suits the subject: this skill audits the
account a session gave of its work, and a typed-record face says so. Rockwell is
geminify's and stays there.

    python3 build_banner.py        # writes banner-src.svg + banner.png (3200x1040)

The artwork is the icon's own move at banner scale: material passing through a
screen, and the three grains it kept. The wordmark sits left, the screen right, and
the fall crosses the gap between them so the two halves are one picture.
"""
import pathlib
import re
import subprocess
import sys
import tempfile

W, H, SCALE = 1600, 520, 2
ASSETS = pathlib.Path(__file__).resolve().parent
FAMILY, CONTROL = "American Typewriter", "Helvetica"
WEIGHT = "700"

BG_TOP, BG_BOT = "#2B3138", "#171B20"
INK, INK_DIM = "#EDF1F5", "#8E9AA6"
FRAME, FRAME_LO = "#8E9AA6", "#5A6674"
MESH = "#7C8792"
SILT_HI, SILT_LO = "#96A3B0", "#3A434D"
GRAIN, GRAIN_CORE = "#E0A55C", "#FFD9A0"


def ink_width(family: str, text: str = "tailings") -> int:
    """Rendered ink width of the wordmark in one family, in px."""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="300">'
           f'<rect width="100%" height="100%" fill="#FFFFFF"/>'
           f'<text x="20" y="200" font-family="{family}" font-size="160" '
           f'font-weight="{WEIGHT}" fill="#000000">{text}</text></svg>')
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False) as fh:
        fh.write(svg)
        src = fh.name
    png = src.replace(".svg", ".png")
    subprocess.run(["rsvg-convert", "-w", "1600", src, "-o", png], check=True)
    # `-trim info:` reports the ORIGINAL page geometry with a trim offset, not the
    # inked box. Without +repage this measured 8px for a 160px wordmark, and the
    # family assertion fired on its own bad arithmetic rather than on a real
    # fallback — a check that fails for the wrong reason is not a check.
    out = subprocess.run(["convert", png, "-trim", "+repage", "info:"],
                         capture_output=True, text=True)
    m = re.search(r"\s(\d+)x(\d+)\s", out.stdout or "")
    return int(m.group(1)) if m else 0


def mesh(w, h, cols, rows):
    out = []
    for i in range(1, cols):
        x = -w / 2 + w * i / cols
        out.append(f'<line x1="{x:.1f}" y1="{-h/2:.1f}" x2="{x:.1f}" y2="{h/2:.1f}"/>')
    for j in range(1, rows):
        y = -h / 2 + h * j / rows
        out.append(f'<line x1="{-w/2:.1f}" y1="{y:.1f}" x2="{w/2:.1f}" y2="{y:.1f}"/>')
    return "\n        ".join(out)


def fall():
    out = []
    for dx, y, ln, op in [(-150, 300, 150, .70), (-96, 326, 178, .70), (-40, 306, 150, .62),
                          (14, 336, 172, .70), (70, 312, 158, .62), (124, 340, 150, .50),
                          (176, 314, 128, .40), (-198, 292, 112, .40), (216, 300, 104, .34)]:
        x = 1180 + dx
        out.append(f'<line x1="{x}" y1="{y}" x2="{x - 16}" y2="{y + ln}" stroke="url(#silt)" '
                   f'stroke-width="8" stroke-linecap="round" opacity="{op}"/>')
    return "\n    ".join(out)


def grains():
    return "\n        ".join(
        f'<g transform="translate({dx},{dy})">'
        f'<circle r="34" fill="url(#glow)" opacity="0.72"/>'
        f'<circle r="15" fill="{GRAIN}"/>'
        f'<circle r="7" cx="-3" cy="-3" fill="{GRAIN_CORE}"/></g>'
        for dx, dy in [(-92, -12), (14, 24), (104, -32)])


def svg() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0.4" y2="1">
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
    <radialGradient id="lift" cx="0.72" cy="0.3" r="0.7">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.09"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#lift)"/>

  {fall()}

  <g transform="translate(1180,232) rotate(-17)">
    <g stroke="{MESH}" stroke-width="5" opacity="0.42" stroke-linecap="round">
        {mesh(324, 176, 5, 3)}
    </g>
    <rect x="-176" y="-102" width="352" height="204" rx="20"
          fill="none" stroke="url(#frame)" stroke-width="17"/>
    <g>
        {grains()}
    </g>
  </g>

  <text x="104" y="268" font-family="{FAMILY}" font-size="132" font-weight="{WEIGHT}"
        fill="{INK}" letter-spacing="-2">tailings</text>
  <text x="108" y="330" font-family="{FAMILY}" font-size="34" font-weight="400"
        fill="{INK_DIM}">what the first pass left behind</text>
  <text x="108" y="382" font-family="{FAMILY}" font-size="26" font-weight="400"
        fill="{INK_DIM}" opacity="0.72">verify a finished session without re-doing its work</text>
</svg>
'''


if __name__ == "__main__":
    a, b = ink_width(FAMILY), ink_width(CONTROL)
    if a == 0:
        sys.exit("banner: the wordmark inked nothing — rsvg-convert or convert is missing")
    if a == b:
        sys.exit(f"banner: {FAMILY!r} and {CONTROL!r} ink identically at {a}px, so "
                 f"{FAMILY!r} never resolved and this would ship in the fallback face")
    src = ASSETS / "banner-src.svg"
    src.write_text(svg())
    out = ASSETS / "banner.png"
    subprocess.run(["rsvg-convert", "-w", str(W * SCALE), "-h", str(H * SCALE),
                    str(src), "-o", str(out)], check=True)
    dims = subprocess.run(["identify", "-format", "%wx%h", str(out)],
                          capture_output=True, text=True).stdout.strip()
    if dims != f"{W*SCALE}x{H*SCALE}":
        sys.exit(f"banner: rendered {dims}, expected {W*SCALE}x{H*SCALE}")
    print(f"wrote {out} at {dims} — {FAMILY} inked {a}px vs {CONTROL} {b}px")
