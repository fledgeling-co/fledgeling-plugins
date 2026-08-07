"""Generate the radial roughField stops.

Rule, unchanged from round 10: each stop is the OLD field colour at the same
distance, scaled by target_L / current_L, so the correction is multiplicative and
every hue survives it untouched.  Only the coordinate the distance is measured in
changes -- u = (x+y)/sqrt2 becomes r = |(x,y) - (75,25)|, C2's own fitted source.
"""
import numpy as np

OLD = [(0, 'F1EADB'), (100, 'E7E0D1'), (180, 'D4CEBF'), (260, 'C5BFB0'), (340, 'B9B3A4'),
       (420, 'B0A99A'), (500, 'A59E8F'), (580, '9D9687'), (680, 'A19A88'), (800, 'A49C88'),
       (940, '9E957F')]
OLD_U = np.array([o[0] for o in OLD], float)
OLD_RGB = np.array([[int(h[i:i + 2], 16) for i in (0, 2, 4)] for _, h in OLD], float)
# the "target L" each old stop was authored to hit in the render (build_icon.py comments)
OLD_L = np.array([.888, .860, .791, .736, .677, .641, .601, .569, .571, .568])
OLD_LU = np.array([0, 100, 180, 260, 340, 420, 500, 580, 680, 800], float)

# C2's f(r) about (75,25), curl excluded, running-min monotonised (work/m8.py)
REF_R = np.array([0, 35, 65, 95, 125, 155, 185, 230, 290, 350, 410, 470, 530,
                  590, 650, 710, 770, 830, 890, 1500], float)
REF_L = np.array([.940, .9166, .8915, .8651, .8412, .8152, .7845, .7521, .7179, .6813,
                  .6523, .6500, .6250, .6016, .5778, .5655, .5655, .5643, .5483, .5483])

KNOTS = [0, 35, 95, 155, 230, 290, 350, 410, 470, 530, 590, 650, 710, 830, 1000]
GR = 1000.0

print('  <radialGradient id="roughField" cx="75" cy="25" r="%d" fx="75" fy="25"' % GR)
print('                  gradientUnits="userSpaceOnUse">')
for r in KNOTS:
    c_old = np.array([np.interp(r, OLD_U, OLD_RGB[:, k]) for k in range(3)])
    l_old = np.interp(r, OLD_LU, OLD_L)
    l_new = np.interp(r, REF_R, REF_L)
    c_new = np.clip(np.round(c_old * (l_new / l_old)), 0, 255).astype(int)
    print('    <stop offset="%.4f" stop-color="#%02X%02X%02X"/>  <!-- r %4d  target L %.3f -->'
          % (r / GR, c_new[0], c_new[1], c_new[2], r, l_new))
print('  </radialGradient>')
print()
print('# ratio applied per knot (new/old target L):')
print('  ' + '  '.join('%d:%.3f' % (r, np.interp(r, REF_R, REF_L) / np.interp(r, OLD_LU, OLD_L))
                       for r in KNOTS))
