#!/usr/bin/env python3
"""
build-icon.py — Engine A: the hand-authored layered SVG master for be-my-witness.

Geometry and material are named constants and the script emits the SVG, so a
fidelity round is a parameter edit rather than path surgery. That is the whole
reason this is a script and not a hand-written .svg file.

DEVICE  A jeweller's loupe over a wireframe grid. The cell under the lens resolves
        sharp while the grid outside stays soft; the rim is milled like a wax seal.
        One object, two readings: the instrument that looks close, and the mark of
        attestation. Which is what `be-my-witness` promises.

REGISTER  Tahoe gel-glass, values sampled from the corpus (apple-04, apple-01):
          vertical ground gradient light periwinkle -> violet, key light upper-left,
          a deep navy body against a near-white translucent face, soft contact
          shadow, two hue families and no third accent.

DECORATIVE, NOT PRODUCTION. This ships as a PNG in a marketplace README, so the
material lives in the file. Do NOT strip the gradients and shadows for Icon
Composer rules; nothing downstream would put them back.

USAGE   python3 build-icon.py > ../assets/icon-master.svg
"""
from __future__ import annotations

S = 1024                      # canvas
CX, CY = 512, 496             # optical centre, nudged up: the barrel carries weight low

# ── palette ───────────────────────────────────────────────────────────────────
GROUND_TOP    = "#AFC6F2"     # periwinkle, brightest under the key light
GROUND_MID    = "#9FA9EE"
GROUND_BOT    = "#8C7BE8"     # violet
GRID_LINE     = "#7E86D6"     # the soft lattice, low contrast against the ground
GRID_SHARP    = "#3B4478"     # the same lattice, resolved, under the lens

BODY_DARK     = "#141B33"     # barrel in shadow
BODY_MID      = "#26314F"
BODY_LIGHT    = "#3C4A70"     # barrel catching the key
RIM_LIGHT     = "#C9D2E4"     # milled metal, lit
RIM_DARK      = "#6E7races"   # placeholder replaced below
RIM_SHADE     = "#66708C"
GLASS_HI      = "#FFFFFF"
GLASS_LO      = "#DCE3F2"

R_OUTER = 300                 # rim outer radius
R_RIM   = 262                 # inner edge of the milled rim
R_LENS  = 244                 # the glass
NOTCHES = 88                  # milled teeth: FINE. At 36 with long teeth it read as a
                              # gear, which is a different object with a different meaning.


def notch_ring(cx, cy, r_in, r_out, n):
    """The milled edge. Trapezoids rather than rects so the teeth taper like real
    knurling; at 16px this collapses to a clean circle, which is the point."""
    import math
    out = []
    for i in range(n):
        a0 = (i + 0.28) * 2 * math.pi / n
        a1 = (i + 0.72) * 2 * math.pi / n
        p = []
        for r, a in ((r_in, a0), (r_out, a0 + 0.006), (r_out, a1 - 0.006), (r_in, a1)):
            p.append(f"{cx + r * math.cos(a):.2f},{cy + r * math.sin(a):.2f}")
        out.append(f'<polygon points="{" ".join(p)}" fill="url(#milled)" opacity=".92"/>')
    return "\n      ".join(out)


def grid(spacing, stroke, width, opacity, blur=None):
    """The lattice. Drawn full-bleed and clipped, so it reads as a plane the loupe
    sits on rather than a decal behind it."""
    lines = []
    for i in range(-2, int(S / spacing) + 3):
        v = i * spacing
        lines.append(f'<path d="M{v} -40 L{v - 150} {S + 40}"/>')      # sheared, so it
        lines.append(f'<path d="M-40 {v} L{S + 40} {v - 90}"/>')       # reads in perspective
    f = f' filter="url(#{blur})"' if blur else ""
    return (f'<g stroke="{stroke}" stroke-width="{width}" opacity="{opacity}" '
            f'fill="none"{f}>\n      ' + "\n      ".join(lines) + "\n    </g>")


SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}" viewBox="0 0 {S} {S}">
  <title>be-my-witness</title>
  <defs>
    <linearGradient id="ground" x1="0" y1="0" x2="0.25" y2="1">
      <stop offset="0" stop-color="{GROUND_TOP}"/>
      <stop offset=".52" stop-color="{GROUND_MID}"/>
      <stop offset="1" stop-color="{GROUND_BOT}"/>
    </linearGradient>

    <!-- Key light upper-left, sampled from the corpus rather than assumed. -->
    <radialGradient id="key" cx=".28" cy=".18" r=".85">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity=".38"/>
      <stop offset=".55" stop-color="#FFFFFF" stop-opacity=".06"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="barrel" x1=".18" y1="0" x2=".85" y2="1">
      <stop offset="0" stop-color="{BODY_LIGHT}"/>
      <stop offset=".45" stop-color="{BODY_MID}"/>
      <stop offset="1" stop-color="{BODY_DARK}"/>
    </linearGradient>

    <linearGradient id="milled" x1=".1" y1="0" x2=".9" y2="1">
      <stop offset="0" stop-color="{RIM_LIGHT}"/>
      <stop offset=".5" stop-color="{RIM_SHADE}"/>
      <stop offset="1" stop-color="{BODY_MID}"/>
    </linearGradient>

    <!-- The glass. Bright where the key hits, falling to a cool edge so it reads
         as a lens rather than a disc. -->
    <radialGradient id="glass" cx=".34" cy=".26" r=".92">
      <stop offset="0" stop-color="{GLASS_HI}" stop-opacity=".97"/>
      <stop offset=".58" stop-color="{GLASS_LO}" stop-opacity=".9"/>
      <stop offset="1" stop-color="#AEBAD6" stop-opacity=".82"/>
    </radialGradient>

    <linearGradient id="specular" x1=".2" y1="0" x2=".7" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity=".85"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
    <filter id="contact" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>

    <!-- The marketplace squircle, from create-mac-icon/assets/squircle-path.txt.
         One silhouette across the family; a bespoke radius reads as a mistake. -->
    <clipPath id="tile"><path d="M1024.00,512.00C1024.00,569.33 1023.85,646.20 1023.56,683.99C1023.27,721.78 1022.83,723.03 1022.24,738.75C1021.66,754.47 1020.92,766.39 1020.04,778.30C1019.16,790.20 1018.13,800.36 1016.95,810.17C1015.77,819.99 1014.44,828.75 1012.95,837.17C1011.47,845.58 1009.83,853.28 1008.04,860.66C1006.25,868.04 1004.30,874.89 1002.19,881.45C1000.08,888.01 997.81,894.14 995.37,900.02C992.94,905.90 990.34,911.43 987.56,916.73C984.79,922.03 981.85,927.02 978.72,931.81C975.59,936.59 972.29,941.11 968.79,945.43C965.29,949.75 961.62,953.83 957.72,957.72C953.83,961.62 949.75,965.29 945.43,968.79C941.11,972.29 936.59,975.59 931.81,978.72C927.02,981.85 922.03,984.79 916.73,987.56C911.43,990.34 905.90,992.94 900.02,995.37C894.14,997.81 888.01,1000.08 881.45,1002.19C874.89,1004.30 868.04,1006.25 860.66,1008.04C853.28,1009.83 845.58,1011.47 837.17,1012.95C828.75,1014.44 819.99,1015.77 810.17,1016.95C800.36,1018.13 790.20,1019.16 778.30,1020.04C766.39,1020.92 754.47,1021.66 738.75,1022.24C723.03,1022.83 721.78,1023.27 683.99,1023.56C646.20,1023.85 569.33,1024.00 512.00,1024.00C454.67,1024.00 377.80,1023.85 340.01,1023.56C302.22,1023.27 300.97,1022.83 285.25,1022.24C269.53,1021.66 257.61,1020.92 245.70,1020.04C233.80,1019.16 223.64,1018.13 213.83,1016.95C204.01,1015.77 195.25,1014.44 186.83,1012.95C178.42,1011.47 170.72,1009.83 163.34,1008.04C155.96,1006.25 149.11,1004.30 142.55,1002.19C135.99,1000.08 129.86,997.81 123.98,995.37C118.10,992.94 112.57,990.34 107.27,987.56C101.97,984.79 96.98,981.85 92.19,978.72C87.41,975.59 82.89,972.29 78.57,968.79C74.25,965.29 70.17,961.62 66.28,957.72C62.38,953.83 58.71,949.75 55.21,945.43C51.71,941.11 48.41,936.59 45.28,931.81C42.15,927.02 39.21,922.03 36.44,916.73C33.66,911.43 31.06,905.90 28.63,900.02C26.19,894.14 23.92,888.01 21.81,881.45C19.70,874.89 17.75,868.04 15.96,860.66C14.17,853.28 12.53,845.58 11.05,837.17C9.56,828.75 8.23,819.99 7.05,810.17C5.87,800.36 4.84,790.20 3.96,778.30C3.08,766.39 2.34,754.47 1.76,738.75C1.17,723.03 0.73,721.78 0.44,683.99C0.15,646.20 0.00,569.33 0.00,512.00C0.00,454.67 0.15,377.80 0.44,340.01C0.73,302.22 1.17,300.97 1.76,285.25C2.34,269.53 3.08,257.61 3.96,245.70C4.84,233.80 5.87,223.64 7.05,213.83C8.23,204.01 9.56,195.25 11.05,186.83C12.53,178.42 14.17,170.72 15.96,163.34C17.75,155.96 19.70,149.11 21.81,142.55C23.92,135.99 26.19,129.86 28.63,123.98C31.06,118.10 33.66,112.57 36.44,107.27C39.21,101.97 42.15,96.98 45.28,92.19C48.41,87.41 51.71,82.89 55.21,78.57C58.71,74.25 62.38,70.17 66.28,66.28C70.17,62.38 74.25,58.71 78.57,55.21C82.89,51.71 87.41,48.41 92.19,45.28C96.98,42.15 101.97,39.21 107.27,36.44C112.57,33.66 118.10,31.06 123.98,28.63C129.86,26.19 135.99,23.92 142.55,21.81C149.11,19.70 155.96,17.75 163.34,15.96C170.72,14.17 178.42,12.53 186.83,11.05C195.25,9.56 204.01,8.23 213.83,7.05C223.64,5.87 233.80,4.84 245.70,3.96C257.61,3.08 269.53,2.34 285.25,1.76C300.97,1.17 302.22,0.73 340.01,0.44C377.80,0.15 454.67,0.00 512.00,0.00C569.33,0.00 646.20,0.15 683.99,0.44C721.78,0.73 723.03,1.17 738.75,1.76C754.47,2.34 766.39,3.08 778.30,3.96C790.20,4.84 800.36,5.87 810.17,7.05C819.99,8.23 828.75,9.56 837.17,11.05C845.58,12.53 853.28,14.17 860.66,15.96C868.04,17.75 874.89,19.70 881.45,21.81C888.01,23.92 894.14,26.19 900.02,28.63C905.90,31.06 911.43,33.66 916.73,36.44C922.03,39.21 927.02,42.15 931.81,45.28C936.59,48.41 941.11,51.71 945.43,55.21C949.75,58.71 953.83,62.38 957.72,66.28C961.62,70.17 965.29,74.25 968.79,78.57C972.29,82.89 975.59,87.41 978.72,92.19C981.85,96.98 984.79,101.97 987.56,107.27C990.34,112.57 992.94,118.10 995.37,123.98C997.81,129.86 1000.08,135.99 1002.19,142.55C1004.30,149.11 1006.25,155.96 1008.04,163.34C1009.83,170.72 1011.47,178.42 1012.95,186.83C1014.44,195.25 1015.77,204.01 1016.95,213.83C1018.13,223.64 1019.16,233.80 1020.04,245.70C1020.92,257.61 1021.66,269.53 1022.24,285.25C1022.83,300.97 1023.27,302.22 1023.56,340.01C1023.85,377.80 1024.00,454.67 1024.00,512.00Z"/></clipPath>
    <clipPath id="lens"><circle cx="{CX}" cy="{CY}" r="{R_LENS}"/></clipPath>
  </defs>

  <g clip-path="url(#tile)">
    <!-- 1. ground -->
    <rect width="{S}" height="{S}" fill="url(#ground)"/>

    <!-- 2. the lattice, soft: this is the world before it is looked at -->
    {grid(118, GRID_LINE, 4.2, ".62", blur="soft")}

    <!-- 3. key light over the ground, before any object -->
    <rect width="{S}" height="{S}" fill="url(#key)"/>

    <!-- 4. contact shadow, cast down-right from the upper-left key -->
    <ellipse cx="{CX + 26}" cy="{CY + R_OUTER - 16}" rx="{R_OUTER - 40}" ry="64"
             fill="#0B1030" opacity=".34" filter="url(#contact)"/>

    <!-- 5. barrel: offset behind the rim, with a lit edge so the loupe reads as a
         solid object rather than a flat ring. -->
    <circle cx="{CX + 34}" cy="{CY + 40}" r="{R_OUTER - 8}" fill="url(#barrel)"/>
    <path d="M{CX - 196} {CY + 214} A {R_OUTER - 8} {R_OUTER - 8} 0 0 0 {CX + 258} {CY + 122}"
          fill="none" stroke="{BODY_LIGHT}" stroke-opacity=".55" stroke-width="7"/>

    <!-- 6. the milled rim: the instrument, and the seal -->
    <circle cx="{CX}" cy="{CY}" r="{R_OUTER}" fill="url(#milled)"/>
    <g>
      {notch_ring(CX, CY, R_OUTER - 16, R_OUTER + 5, NOTCHES)}
    </g>
    <circle cx="{CX}" cy="{CY}" r="{R_RIM}" fill="{BODY_DARK}" opacity=".92"/>

    <!-- 7. what the lens resolves: the same lattice, sharp and dark -->
    <g clip-path="url(#lens)">
      <circle cx="{CX}" cy="{CY}" r="{R_LENS}" fill="#EEF2FB"/>
      {grid(118, GRID_SHARP, 2.4, ".78")}
      {grid(19.7, GRID_SHARP, 0.9, ".52")}
      <circle cx="{CX}" cy="{CY}" r="{R_LENS}" fill="url(#glass)" opacity=".55"/>
    </g>

    <!-- 8. specular sweep across the glass -->
    <path d="M{CX - 190} {CY - 96} A 210 210 0 0 1 {CX + 44} {CY - 232}
             A {R_LENS} {R_LENS} 0 0 0 {CX - 190} {CY - 96} Z"
          fill="url(#specular)" opacity=".7"/>

    <!-- 9. rim light along the upper-left edge of the glass -->
    <circle cx="{CX}" cy="{CY}" r="{R_LENS - 3}" fill="none"
            stroke="#FFFFFF" stroke-opacity=".55" stroke-width="4"
            stroke-dasharray="470 900" transform="rotate(-152 {CX} {CY})"/>

    <!-- 10. tile edge, on the squircle -->
    <path d="M1024.00,512.00C1024.00,569.33 1023.85,646.20 1023.56,683.99C1023.27,721.78 1022.83,723.03 1022.24,738.75C1021.66,754.47 1020.92,766.39 1020.04,778.30C1019.16,790.20 1018.13,800.36 1016.95,810.17C1015.77,819.99 1014.44,828.75 1012.95,837.17C1011.47,845.58 1009.83,853.28 1008.04,860.66C1006.25,868.04 1004.30,874.89 1002.19,881.45C1000.08,888.01 997.81,894.14 995.37,900.02C992.94,905.90 990.34,911.43 987.56,916.73C984.79,922.03 981.85,927.02 978.72,931.81C975.59,936.59 972.29,941.11 968.79,945.43C965.29,949.75 961.62,953.83 957.72,957.72C953.83,961.62 949.75,965.29 945.43,968.79C941.11,972.29 936.59,975.59 931.81,978.72C927.02,981.85 922.03,984.79 916.73,987.56C911.43,990.34 905.90,992.94 900.02,995.37C894.14,997.81 888.01,1000.08 881.45,1002.19C874.89,1004.30 868.04,1006.25 860.66,1008.04C853.28,1009.83 845.58,1011.47 837.17,1012.95C828.75,1014.44 819.99,1015.77 810.17,1016.95C800.36,1018.13 790.20,1019.16 778.30,1020.04C766.39,1020.92 754.47,1021.66 738.75,1022.24C723.03,1022.83 721.78,1023.27 683.99,1023.56C646.20,1023.85 569.33,1024.00 512.00,1024.00C454.67,1024.00 377.80,1023.85 340.01,1023.56C302.22,1023.27 300.97,1022.83 285.25,1022.24C269.53,1021.66 257.61,1020.92 245.70,1020.04C233.80,1019.16 223.64,1018.13 213.83,1016.95C204.01,1015.77 195.25,1014.44 186.83,1012.95C178.42,1011.47 170.72,1009.83 163.34,1008.04C155.96,1006.25 149.11,1004.30 142.55,1002.19C135.99,1000.08 129.86,997.81 123.98,995.37C118.10,992.94 112.57,990.34 107.27,987.56C101.97,984.79 96.98,981.85 92.19,978.72C87.41,975.59 82.89,972.29 78.57,968.79C74.25,965.29 70.17,961.62 66.28,957.72C62.38,953.83 58.71,949.75 55.21,945.43C51.71,941.11 48.41,936.59 45.28,931.81C42.15,927.02 39.21,922.03 36.44,916.73C33.66,911.43 31.06,905.90 28.63,900.02C26.19,894.14 23.92,888.01 21.81,881.45C19.70,874.89 17.75,868.04 15.96,860.66C14.17,853.28 12.53,845.58 11.05,837.17C9.56,828.75 8.23,819.99 7.05,810.17C5.87,800.36 4.84,790.20 3.96,778.30C3.08,766.39 2.34,754.47 1.76,738.75C1.17,723.03 0.73,721.78 0.44,683.99C0.15,646.20 0.00,569.33 0.00,512.00C0.00,454.67 0.15,377.80 0.44,340.01C0.73,302.22 1.17,300.97 1.76,285.25C2.34,269.53 3.08,257.61 3.96,245.70C4.84,233.80 5.87,223.64 7.05,213.83C8.23,204.01 9.56,195.25 11.05,186.83C12.53,178.42 14.17,170.72 15.96,163.34C17.75,155.96 19.70,149.11 21.81,142.55C23.92,135.99 26.19,129.86 28.63,123.98C31.06,118.10 33.66,112.57 36.44,107.27C39.21,101.97 42.15,96.98 45.28,92.19C48.41,87.41 51.71,82.89 55.21,78.57C58.71,74.25 62.38,70.17 66.28,66.28C70.17,62.38 74.25,58.71 78.57,55.21C82.89,51.71 87.41,48.41 92.19,45.28C96.98,42.15 101.97,39.21 107.27,36.44C112.57,33.66 118.10,31.06 123.98,28.63C129.86,26.19 135.99,23.92 142.55,21.81C149.11,19.70 155.96,17.75 163.34,15.96C170.72,14.17 178.42,12.53 186.83,11.05C195.25,9.56 204.01,8.23 213.83,7.05C223.64,5.87 233.80,4.84 245.70,3.96C257.61,3.08 269.53,2.34 285.25,1.76C300.97,1.17 302.22,0.73 340.01,0.44C377.80,0.15 454.67,0.00 512.00,0.00C569.33,0.00 646.20,0.15 683.99,0.44C721.78,0.73 723.03,1.17 738.75,1.76C754.47,2.34 766.39,3.08 778.30,3.96C790.20,4.84 800.36,5.87 810.17,7.05C819.99,8.23 828.75,9.56 837.17,11.05C845.58,12.53 853.28,14.17 860.66,15.96C868.04,17.75 874.89,19.70 881.45,21.81C888.01,23.92 894.14,26.19 900.02,28.63C905.90,31.06 911.43,33.66 916.73,36.44C922.03,39.21 927.02,42.15 931.81,45.28C936.59,48.41 941.11,51.71 945.43,55.21C949.75,58.71 953.83,62.38 957.72,66.28C961.62,70.17 965.29,74.25 968.79,78.57C972.29,82.89 975.59,87.41 978.72,92.19C981.85,96.98 984.79,101.97 987.56,107.27C990.34,112.57 992.94,118.10 995.37,123.98C997.81,129.86 1000.08,135.99 1002.19,142.55C1004.30,149.11 1006.25,155.96 1008.04,163.34C1009.83,170.72 1011.47,178.42 1012.95,186.83C1014.44,195.25 1015.77,204.01 1016.95,213.83C1018.13,223.64 1019.16,233.80 1020.04,245.70C1020.92,257.61 1021.66,269.53 1022.24,285.25C1022.83,300.97 1023.27,302.22 1023.56,340.01C1023.85,377.80 1024.00,454.67 1024.00,512.00Z" fill="none"
          stroke="#FFFFFF" stroke-opacity=".22" stroke-width="2"/>
  </g>
</svg>
'''

if __name__ == "__main__":
    print(SVG)
