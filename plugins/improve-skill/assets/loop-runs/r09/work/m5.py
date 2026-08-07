"""Which spatial frequencies is each material missing?

SSIM's cs term is a local-variance ratio, so "sd_cand 0.0116 vs sd_ref 0.0310" only
says the amplitude is wrong somewhere. Band-pass both images with a difference of
Gaussians per octave and report the sd of each band inside a clean mask of each
material. That says WHICH scale is missing, which is the difference between turning
an amplitude up and authoring the right grain.
"""
import math, sys, numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, 'loop-runs/r09/work')
import nd
NEUTRAL = 128/255.0
def load(p):
    a = np.asarray(Image.open(p).convert('RGBA')).astype(np.float64)/255.0
    rgb, al = a[...,:3], a[...,3:4]
    rgb = rgb*al + NEUTRAL*(1-al)
    return 0.2126*rgb[...,0]+0.7152*rgb[...,1]+0.0722*rgb[...,2], a[...,3]
B='loop-runs/r08/'
gc, ac = load(B+'candidate-1024.png')
gr, ar = load(B+'reference-1024.png')
H, W = gc.shape
Y, X = np.mgrid[0:H, 0:W]
CURL_C = (X>=170)&(X<=500)&(Y>=40)&(Y<=420)
CURL_R = (X>=178)&(X<=492)&(Y>=50)&(Y<=414)
ang = math.radians(33.0)
f_ours = Y - (604 - math.tan(ang)*(X-543))
f_ref  = Y - (-0.8026*X + 991.2)
blk_c = np.load('loop-runs/r09/work/blk_c.npy'); blk_r = np.load('loop-runs/r09/work/blk_r.npy')
d_c = np.load('loop-runs/r09/work/dist_c.npy'); d_r = np.load('loop-runs/r09/work/dist_r.npy')

def blur(g, s):
    """Separable Gaussian in float; PIL's GaussianBlur refuses mode 'F' here."""
    rad = int(math.ceil(3*s))
    k = np.exp(-0.5*(np.arange(-rad, rad+1)/s)**2); k /= k.sum()
    p = np.pad(g, ((rad, rad), (0, 0)), mode='edge')
    out = sum(k[i]*p[i:i+g.shape[0]] for i in range(2*rad+1))
    p = np.pad(out, ((0, 0), (rad, rad)), mode='edge')
    return sum(k[i]*p[:, i:i+g.shape[1]] for i in range(2*rad+1))
SIGMAS = [0.8, 1.6, 3.2, 6.4, 12.8, 25.6]
_CACHE = {}
def bands(g, key):
    if key in _CACHE: return _CACHE[key]
    prev, out = g, []
    for s in SIGMAS:
        cur = blur(g, s)
        out.append(prev - cur); prev = cur
    _CACHE[key] = out
    return out

def report(title, masks_c, masks_r):
    print('\n=== %s ===' % title)
    hdr = '  %-22s' % 'band (sigma, px)' + ' '.join('%8.1f' % s for s in SIGMAS)
    print(hdr)
    for name in masks_c:
        mc, mr = masks_c[name], masks_r[name]
        bc, br = bands(gc, 'c'), bands(gr, 'r')
        print('  %-22s' % ('%s  cand sd' % name) + ' '.join('%8.4f' % b[mc].std() for b in bc))
        print('  %-22s' % ('%s  ref  sd' % name) + ' '.join('%8.4f' % b[mr].std() for b in br))
        print('  %-22s' % ('%s  ref/cand' % name) + ' '.join('%8.2f' % (b2[mr].std()/max(b1[mc].std(),1e-9))
                                                             for b1, b2 in zip(bc, br)))

# clean interior masks: no block (dilated), no curl, no tile rim, no plane boundary band
def clean(g, alpha, blk, dist, fline, curl, side):
    inner = nd.erode(alpha > 0.98, 9)
    for _ in range(6): inner = nd.erode(inner, 9)          # ~27px in from the squircle
    m = inner & (~curl) & (dist > 30) & (np.abs(fline) > 40)
    return m & ((fline <= 0) if side == 'rough' else (fline > 0))

masks_c = {'rough': clean(gc, ac, blk_c, d_c, f_ours, CURL_C, 'rough'),
           'trued': clean(gc, ac, blk_c, d_c, f_ours, CURL_C, 'trued'),
           'block': nd.erode(blk_c, 9) & ~nd.dilate(gc < 0.12, 9)}
masks_r = {'rough': clean(gr, ar, blk_r, d_r, f_ref, CURL_R, 'rough'),
           'trued': clean(gr, ar, blk_r, d_r, f_ref, CURL_R, 'trued'),
           'block': nd.erode(blk_r, 9) & ~nd.dilate(gr < 0.12, 9)}
for _ in range(5):
    masks_c['block'] = nd.erode(masks_c['block'], 9); masks_r['block'] = nd.erode(masks_r['block'], 9)
print('mask sizes  ' + '  '.join('%s c=%d r=%d' % (k, masks_c[k].sum(), masks_r[k].sum()) for k in masks_c))
report('band-pass sd by material (1024px)', masks_c, masks_r)

# grain direction: sd of the first difference along vs across the 33-degree cut
print('\ndirectionality of the fine bands (sd of gradient along vs across the cut, rough plane)')
gx = np.gradient(gc, axis=1); gy = np.gradient(gc, axis=0)
rx = np.gradient(gr, axis=1); ry = np.gradient(gr, axis=0)
u = (math.cos(ang), -math.sin(ang)); v = (math.sin(ang), math.cos(ang))
for nm, (ga, gb, m) in (('cand', (gx, gy, masks_c['rough'])), ('ref ', (rx, ry, masks_r['rough']))):
    al = (ga*u[0] + gb*u[1])[m].std(); ac_ = (ga*v[0] + gb*v[1])[m].std()
    print('  %s  along %.5f  across %.5f  anisotropy %.2f' % (nm, al, ac_, ac_/max(al,1e-9)))
