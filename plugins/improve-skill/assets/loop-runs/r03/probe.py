"""Probe: measure a variant's curl percentiles against the reference's, then score it."""
import sys, subprocess, tempfile, pathlib
import numpy as np
from PIL import Image
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import variant as V

REF_TARGET = {'p1': 0.598, 'p10': 0.633, 'p50': 0.723, 'p90': 0.824,
              'mean': 0.729, 'ground': 0.793, 'ratio': 1.087}


def rend1024(p):
    t = pathlib.Path(tempfile.mktemp(suffix='.png'))
    subprocess.run(['rsvg-convert', '-w', '1024', '-h', '1024', str(p), '-o', str(t)], check=True)
    a = np.asarray(Image.open(t).convert('RGBA'), dtype=np.float64) / 255.
    t.unlink()
    return a[..., :3] * a[..., 3:4] + 0.501961 * (1 - a[..., 3:4])


def lum(c):
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


NO_CURL = pathlib.Path('loop-runs/r03/no-curl.svg')


def curl_stats(svg):
    la, lb = lum(rend1024(svg)), lum(rend1024(NO_CURL))
    m = np.abs(la - lb) > 0.02
    s = la[m]
    return {'p1': np.percentile(s, 1), 'p10': np.percentile(s, 10), 'p50': np.percentile(s, 50),
            'p90': np.percentile(s, 90), 'mean': s.mean(), 'ground': lb[m].mean(),
            'ratio': lb[m].mean() / s.mean(), 'range': np.percentile(s, 90) / np.percentile(s, 10)}


def report_curl(st):
    print('  curl vs reference target:')
    for k in ('p1', 'p10', 'p50', 'p90', 'mean'):
        print('    %-5s %.3f   (ref %.3f, %+.3f)' % (k, st[k], REF_TARGET[k], st[k] - REF_TARGET[k]))
    print('    ground:curl %.3f:1 (ref %.3f:1)   internal p90/p10 %.2f:1 (ref 1.30:1)'
          % (st['ratio'], REF_TARGET['ratio'], st['range']))
