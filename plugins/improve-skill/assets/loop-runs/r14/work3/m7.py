"""Attribute the curl's dark pixels to a shading branch by painting the branches.

OUT_* -> red, IN_* -> blue, TRANSMIT -> green. Whatever colour the dark limb
comes out is the branch that owns it.
"""
import subprocess, pathlib, re, numpy as np
from PIL import Image

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
OUT = pathlib.Path(__file__).resolve().parent

src = (A / 'build_icon.py').read_text()
for name, col in (('OUT_LIT', '(255,  0,  0)'), ('OUT_DARK', '(255,  0,  0)'),
                  ('IN_LIT', '(  0,  0,255)'), ('IN_DARK', '(  0,  0,255)'),
                  ('TRANSMIT', '(  0,255,  0)')):
    src = re.sub(rf'^{name}\s*=\s*\([^)]*\)', f'{name} = {col}', src, count=1, flags=re.M)
tmp = A / '_dbg_build.py'
tmp.write_text(src)
subprocess.run(['python3', str(tmp)], cwd=str(A), check=True, stdout=subprocess.DEVNULL)
dbg = OUT / 'branch-map.svg'
dbg.write_bytes((A / 'icon.svg').read_bytes())
tmp.unlink()

png = OUT / 'branch-map.png'
subprocess.run(['rsvg-convert', '-w', '1024', '-h', '1024', str(dbg), '-o', str(png)], check=True)
a = np.asarray(Image.open(png).convert('RGB'), dtype=np.float64)
Image.open(png).convert('RGB').crop((120, 60, 640, 500)).save(OUT / 'branch-map-crop.png')

# report the branch mix over the cells the dark map flagged
print('cell map over the curl box: R=outer  B=inner  (mean channel per 20px cell)')
for y in range(160, 420, 20):
    row = []
    for x in range(150, 430, 20):
        c = a[y:y + 20, x:x + 20].mean(axis=(0, 1))
        tag = 'R' if c[0] > c[2] + 12 else ('B' if c[2] > c[0] + 12 else '.')
        row.append(tag)
    print(f'  y={y:4d} ' + ' '.join(row))
