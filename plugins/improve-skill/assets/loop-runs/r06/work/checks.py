"""r06: pixel-level checks the whole-tile view cannot settle.

(a) The block's back edge. pitRelief is applied to the face path directly, and
    feComposite arithmetic multiplies ALPHA by k1 = 1/sin(50 deg) = 1.305 as well as
    colour, so antialiased edge pixels come out more opaque than drawn. Harmless if it
    is a fraction of a pixel, a visible artefact if it is not - so it gets looked at.
(b) The cut, at 3x, before and after: the step in texture across it is the round's
    whole claim and it should read as a material boundary, not as a seam.
(c) The face, before and after, for any colour shift the modulation should not cause.
"""
import pathlib

from PIL import Image

W = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r06/work')
pre, post = Image.open(W / 'state-now.png'), Image.open(W / 'v2.png')
ref = Image.open(W.parent.parent / 'r04/reference-1024.png').convert('RGB')

PANES = [('back edge x3', (700, 240, 830, 370), 3),
         ('cut x3', (150, 700, 400, 830), 3),
         ('face x2', (330, 380, 600, 520), 2)]

rows = []
for name, box, z in PANES:
    w, h = (box[2] - box[0]) * z, (box[3] - box[1]) * z
    strip = Image.new('RGB', (w * 2 + 12, h), (20, 20, 20))
    strip.paste(pre.convert('RGB').crop(box).resize((w, h), Image.NEAREST), (0, 0))
    strip.paste(post.convert('RGB').crop(box).resize((w, h), Image.NEAREST), (w + 12, 0))
    rows.append((name, strip))

tw = max(s.width for _, s in rows)
th = sum(s.height + 26 for _, s in rows)
sheet = Image.new('RGB', (tw, th), (20, 20, 20))
yy = 0
for name, s in rows:
    sheet.paste(s, (0, yy + 26))
    yy += s.height + 26
sheet.save(W / 'checks.png')
print(f'wrote {W}/checks.png  (left = before relief, right = after, per row)')
print('rows top to bottom: ' + ', '.join(n for n, _ in PANES))
