"""Sample real pixel values out of the candidate and reference 1024 renders.

Point lists come in as JSON on argv (no eval; these are data, not code).
"""
import json
import sys
import numpy as np
from PIL import Image

R = 'loop-runs/r01/reference-1024.png'
C = 'loop-runs/r01/candidate-1024.png'


def load(p):
    a = np.asarray(Image.open(p).convert('RGBA'), dtype=np.float64) / 255.
    rgb, al = a[..., :3], a[..., 3:4]
    return rgb * al + 0.501961 * (1 - al)


def L(c):
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def show(tag, img, x, y, r=6):
    p = img[y - r:y + r, x - r:x + r]
    l = L(p)
    m = p.reshape(-1, 3).mean(0)
    print('  %-26s (%4d,%4d) L %.3f  rgb %.3f %.3f %.3f  sd %.4f'
          % (tag, x, y, l.mean(), m[0], m[1], m[2], l.std()))


if __name__ == '__main__':
    c, r = load(C), load(R)
    print('CANDIDATE')
    for tag, x, y in json.loads(sys.argv[1]):
        show(tag, c, x, y)
    print('REFERENCE')
    for tag, x, y in json.loads(sys.argv[2]):
        show(tag, r, x, y)
