#!/usr/bin/env python3
"""Icon generator for better-goal and better-loop.

One metaphor, shared device: a bearing needle on a porcelain dial.
  better-goal — the needle locked on a mark, held by a ratchet pawl.
  better-loop — the same needle circling a fixed watch-point, one tick per pass.

Family conventions (see ../../CLAUDE.md): squircle silhouette from
create-mac-icon/assets/squircle-path.txt, porcelain ground, slate metal,
one warm vermilion accent. Renders 1024 / 256 / 128 via rsvg-convert.

    python3 icon-gen.py goal   > icon-src.svg
    python3 icon-gen.py loop   > icon-src.svg
"""
import math
import sys
from pathlib import Path

SQUIRCLE = (Path(__file__).resolve().parents[2]
            / "create-mac-icon/assets/squircle-path.txt").read_text().strip()

CX = CY = 512.0
R_DIAL = 330.0        # porcelain dial
R_TICKS = 292.0       # tick ring
R_NEEDLE = 250.0      # needle reach


def polar(r, deg):
    a = math.radians(deg - 90.0)          # 0deg = 12 o'clock
    return CX + r * math.cos(a), CY + r * math.sin(a)


def ticks(major_every=6, n=36, r_out=R_TICKS, minor=16.0, major=30.0):
    out = []
    for i in range(n):
        deg = i * (360.0 / n)
        ln = major if i % major_every == 0 else minor
        w = 9.0 if i % major_every == 0 else 5.0
        x1, y1 = polar(r_out, deg)
        x2, y2 = polar(r_out - ln, deg)
        out.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="#9C8A6C" stroke-width="{w}" stroke-linecap="round" opacity="0.55"/>')
    return "\n    ".join(out)


def needle(deg):
    """Slate needle: a tapered blade from the hub out to the bearing."""
    tipx, tipy = polar(R_NEEDLE, deg)
    lx, ly = polar(52.0, deg - 96.0)
    rx, ry = polar(52.0, deg + 96.0)
    tailx, taily = polar(86.0, deg + 180.0)
    return (f'<path d="M{tipx:.1f},{tipy:.1f} L{rx:.1f},{ry:.1f} '
            f'L{tailx:.1f},{taily:.1f} L{lx:.1f},{ly:.1f} Z" fill="url(#blade)"/>')


def arc(r, a0, a1, sweep=1):
    x0, y0 = polar(r, a0)
    x1, y1 = polar(r, a1)
    large = 1 if abs(a1 - a0) > 180 else 0
    return f"M{x0:.1f},{y0:.1f} A{r},{r} 0 {large} {sweep} {x1:.1f},{y1:.1f}"


DEFS = f"""  <clipPath id="squircle"><path d="{SQUIRCLE}"/></clipPath>
  <radialGradient id="ground" cx="50%" cy="36%" r="78%">
    <stop offset="0%" stop-color="#FFFDFA"/>
    <stop offset="58%" stop-color="#F7F4EE"/>
    <stop offset="100%" stop-color="#EBE6DC"/>
  </radialGradient>
  <radialGradient id="vignette" cx="50%" cy="42%" r="76%">
    <stop offset="70%" stop-color="#8A7A5E" stop-opacity="0"/>
    <stop offset="100%" stop-color="#8A7A5E" stop-opacity="0.20"/>
  </radialGradient>
  <radialGradient id="dial" cx="50%" cy="34%" r="72%">
    <stop offset="0%" stop-color="#FFFFFF"/>
    <stop offset="62%" stop-color="#FBF8F1"/>
    <stop offset="100%" stop-color="#EDE7DA"/>
  </radialGradient>
  <linearGradient id="blade" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#4A525B"/>
    <stop offset="55%" stop-color="#333B44"/>
    <stop offset="100%" stop-color="#212730"/>
  </linearGradient>
  <linearGradient id="accent" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#FB8A5E"/>
    <stop offset="34%" stop-color="#F0603A"/>
    <stop offset="78%" stop-color="#D8431F"/>
    <stop offset="100%" stop-color="#A82C0C"/>
  </linearGradient>
  <linearGradient id="hub" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#5A626B"/>
    <stop offset="100%" stop-color="#262D35"/>
  </linearGradient>
  <filter id="soft" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="16"/>
  </filter>"""


def base():
    return f"""  <rect width="1024" height="1024" fill="url(#ground)"/>
    <ellipse cx="512" cy="596" rx="352" ry="336" fill="#8A7A5E" opacity="0.16" filter="url(#soft)"/>
    <circle cx="{CX}" cy="{CY}" r="{R_DIAL}" fill="url(#dial)" stroke="#C7BCA4" stroke-width="7"/>
    {ticks()}"""


def goal_svg():
    """Needle held on the mark by a locking gate at the rim; it cannot fall back.

    The ratchet is abstracted to its function: two jaws closed around the bearing.
    A literal tooth ring was tried and is illegible below about 128px, where it
    reads as noise crowding the hub rather than as a mechanism.
    """
    mx, my = polar(R_TICKS - 4, 0)
    r_gate = 236.0
    jaw = 30.0                                   # gate half-width, degrees
    jaws = []
    for s in (-1, 1):
        d = s * jaw
        ix, iy = polar(r_gate - 34, d)
        ox, oy = polar(r_gate + 34, d)
        jaws.append(f'<line x1="{ix:.1f}" y1="{iy:.1f}" x2="{ox:.1f}" y2="{oy:.1f}" '
                    f'stroke="url(#accent)" stroke-width="26" stroke-linecap="round"/>')
    return f"""{base()}
    <!-- the gate the bearing is locked into -->
    <path d="{arc(r_gate, -jaw, jaw)}" fill="none" stroke="url(#accent)" stroke-width="26"
          stroke-linecap="round"/>
    {''.join(jaws)}
    <!-- the mark it is held on -->
    <circle cx="{mx:.1f}" cy="{my:.1f}" r="26" fill="url(#accent)"/>
    <circle cx="{mx:.1f}" cy="{my:.1f}" r="26" fill="none" stroke="#FFF6E4" stroke-width="6" opacity="0.85"/>
    {needle(0.0)}
    <circle cx="{CX}" cy="{CY}" r="112" fill="url(#hub)"/>
    <circle cx="{CX}" cy="{CY}" r="112" fill="none" stroke="#FFF8EA" stroke-width="8" opacity="0.30"/>
    <circle cx="{CX}" cy="{CY}" r="34" fill="#FFF8EA"/>"""


def loop_svg():
    """Same needle, circling a fixed watch-point; vermilion ticks accumulate per pass."""
    wx, wy = polar(R_TICKS - 4, 0)
    passes = []
    for i, deg in enumerate((0.0, 52.0, 104.0, 156.0)):
        x1, y1 = polar(R_TICKS + 22, deg)
        x2, y2 = polar(R_TICKS - 16, deg)
        passes.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                      f'stroke="url(#accent)" stroke-width="15" stroke-linecap="round" '
                      f'opacity="{1.0 - i * 0.21:.2f}"/>')
    return f"""{base()}
    <!-- the watch-point the loop keeps returning to -->
    <circle cx="{wx:.1f}" cy="{wy:.1f}" r="27" fill="url(#accent)"/>
    <circle cx="{wx:.1f}" cy="{wy:.1f}" r="27" fill="none" stroke="#FFF6E4" stroke-width="6" opacity="0.85"/>
    <!-- one tick per pass, fading behind -->
    {''.join(passes)}
    <!-- the sweep the needle has just made -->
    <path d="{arc(196.0, 196.0, 348.0)}" fill="none" stroke="#6E7A86" stroke-width="26"
          stroke-linecap="round" opacity="0.42"/>
    <path d="{arc(196.0, 300.0, 348.0)}" fill="none" stroke="url(#accent)" stroke-width="26"
          stroke-linecap="round"/>
    {needle(348.0)}
    <circle cx="{CX}" cy="{CY}" r="112" fill="url(#hub)"/>
    <circle cx="{CX}" cy="{CY}" r="112" fill="none" stroke="#FFF8EA" stroke-width="8" opacity="0.30"/>
    <circle cx="{CX}" cy="{CY}" r="34" fill="#FFF8EA"/>"""


def render(body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">
<defs>
{DEFS}
</defs>
<g clip-path="url(#squircle)">
{body}
    <rect width="1024" height="1024" fill="url(#vignette)"/>
</g>
</svg>
"""


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "goal"
    sys.stdout.write(render(goal_svg() if which == "goal" else loop_svg()))
