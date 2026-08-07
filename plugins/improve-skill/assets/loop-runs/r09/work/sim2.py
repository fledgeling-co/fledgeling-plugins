"""Does the metric actually want the missing micro-relief?

The rough plane's band-pass sd runs 0.0026/0.0025/0.0027 against C2's 0.0210/0.0140/0.0116
at sigma 0.8/1.6/3.2 -- our surface has essentially no relief and C2's has a 1/f fall-off.
Adding it is materially right. Whether the numbers want it is a separate question and this
answers it: SSIM's cs term is a correlation, so uncorrelated relief of matched amplitude
drives cs DOWN even as edge_f1 recall goes UP. Simulate both and read the net.
"""
import math, sys, json, pathlib, numpy as np
from PIL import Image
sys.path.insert(0, 'loop-runs/r09/work')
sys.path.insert(0, '/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts')
import fidelity as F

def blur(g, s):
    rad = int(math.ceil(3*s))
    k = np.exp(-0.5*(np.arange(-rad, rad+1)/s)**2); k /= k.sum()
    p = np.pad(g, ((rad, rad), (0, 0)), mode='edge')
    out = sum(k[i]*p[i:i+g.shape[0]] for i in range(2*rad+1))
    p = np.pad(out, ((0, 0), (rad, rad)), mode='edge')
    return sum(k[i]*p[:, i:i+g.shape[1]] for i in range(2*rad+1))

SIGMAS = [0.8, 1.6, 3.2, 6.4, 12.8]
TARGET = {'rough': [0.0210, 0.0140, 0.0116, 0.0083, 0.0051],   # C2, measured in m5.py
          'block': [0.0125, 0.0076, 0.0067, 0.0067, 0.0078],
          'trued': [0.0042, 0.0019, 0.0015, 0.0015, 0.0019]}
HAVE   = {'rough': [0.0026, 0.0025, 0.0027, 0.0025, 0.0023],
          'block': [0.0035, 0.0038, 0.0047, 0.0038, 0.0043],
          'trued': [0.0018, 0.0013, 0.0013, 0.0012, 0.0021]}

B = 'loop-runs/r08/'
cand = Image.open(B+'candidate-1024.png').convert('RGBA')
a = np.asarray(cand).astype(np.float64)/255.0
rgb, alpha = a[..., :3].copy(), a[..., 3]
H, W = alpha.shape
Y, X = np.mgrid[0:H, 0:W]
ang = math.radians(33.0)
fline = Y - (604 - math.tan(ang)*(X-543))
blk = np.load('loop-runs/r09/work/blk_c.npy')
CURL = (X>=170)&(X<=500)&(Y>=40)&(Y<=420)
inside = alpha > 0.98
M = {'rough': inside & ~blk & ~CURL & (fline <= 0),
     'trued': inside & ~blk & ~CURL & (fline > 0),
     'block': blk}

rng = np.random.default_rng(9)
def relief(region, amp):
    """Band-limited noise whose per-octave sd fills the deficit target-have, times amp."""
    tot = np.zeros((H, W))
    for i, s in enumerate(SIGMAS):
        w = rng.standard_normal((H, W))
        b = blur(w, s) - blur(w, s*2)
        b /= max(b.std(), 1e-9)
        need = max(TARGET[region][i]**2 - HAVE[region][i]**2, 0.0)**0.5
        tot += b*need*amp
    return tot

base = json.loads(open(B+'score.json').read())['sizes']
def metrics(out):
    im = Image.fromarray((np.concatenate([np.clip(out,0,1), alpha[..., None]], axis=2)*255).astype(np.uint8), 'RGBA')
    res = {}
    for size in F.SIZES:
        ci = im.resize((size, size), Image.LANCZOS)
        ri = F.normalise_reference(pathlib.Path('icon-engineC-f5665d-2.png'), size)
        gc, gr = F.to_gray(ci), F.to_gray(ri)
        m = {'lum_delta': round(float(np.abs(gc-gr).mean()), 4), 'ssim': round(F.ssim(gc, gr), 4),
             'edge_f1': round(F.edge_f1(gc, gr), 4), 'mask_iou': round(F.mask_iou(ci, ri), 4),
             'self_contrast': round(float(np.percentile(gc, 90)-np.percentile(gc, 10)), 4)}
        m['composite'] = F.composite_for(size, m)
        res[size] = m
    return res

cal = metrics(rgb)
off = {s: {k: base[str(s)][k]-cal[s][k] for k in ('composite','self_contrast','ssim','edge_f1','lum_delta')} for s in F.SIZES}
FLOOR = {s: base[str(s)]['self_contrast']*0.94 for s in F.SIZES}

print('%-34s %8s   %s' % ('config', 'net', ' '.join('%8d' % s for s in F.SIZES)))
def run(name, regions, amp):
    out = rgb.copy()
    for r in regions:
        n = relief(r, amp)
        out = np.where(M[r][..., None], out*(1.0 + (n/np.maximum(out.mean(axis=2), 0.05))[..., None]), out)
    m = metrics(out)
    net = sum(m[s]['composite']+off[s]['composite']-base[str(s)]['composite'] for s in F.SIZES)
    cells = []
    for s in F.SIZES:
        c = m[s]['composite']+off[s]['composite']
        sc = m[s]['self_contrast']+off[s]['self_contrast']
        cells.append('%+.4f%s' % (c-base[str(s)]['composite'], '!' if sc < FLOOR[s] else ''))
    print('%-34s %+8.4f   %s' % (name, net, ' '.join('%8s' % c for c in cells)))
    print('%-34s          %s' % ('   ssim', ' '.join('%+8.4f' % (m[s]['ssim']+off[s]['ssim']-base[str(s)]['ssim']) for s in F.SIZES)))
    print('%-34s          %s' % ('   edge_f1', ' '.join('%+8.4f' % (m[s]['edge_f1']+off[s]['edge_f1']-base[str(s)]['edge_f1']) for s in F.SIZES)))
    return m

for amp in (0.35, 0.7, 1.0):
    run('rough only, amp %.2f' % amp, ['rough'], amp)
for amp in (0.35, 0.7, 1.0):
    run('rough+block+trued, amp %.2f' % amp, ['rough', 'block', 'trued'], amp)
