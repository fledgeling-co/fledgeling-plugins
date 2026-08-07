"""SSIM carries 0.40 of the composite at 128/256/1024 -- more than luminance. |g_c - g_r|
says nothing about where SSIM is lost, so map the SSIM field itself and break it down by
region, at the sizes where it is weighted most.
"""
import math, sys, pathlib, numpy as np
from PIL import Image
sys.path.insert(0, '/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts')
import fidelity as F

def ssim_map(a, b):
    w = max(3, min(11, a.shape[0]//4) | 1)
    c1, c2 = 0.01**2, 0.03**2
    mu_a, mu_b = F.box_mean(a, w), F.box_mean(b, w)
    va = F.box_mean(a*a, w) - mu_a**2
    vb = F.box_mean(b*b, w) - mu_b**2
    cov = F.box_mean(a*b, w) - mu_a*mu_b
    lum  = (2*mu_a*mu_b + c1)/(mu_a**2 + mu_b**2 + c1)
    cs   = (2*cov + c2)/(va + vb + c2)
    return np.clip(lum*cs, -1, 1), lum, cs, va, vb

for size in (1024, 256, 128):
    ci = F.render_candidate(pathlib.Path('icon.svg'), size)
    ri = F.normalise_reference(pathlib.Path('icon-engineC-f5665d-2.png'), size)
    gc, gr = F.to_gray(ci), F.to_gray(ri)
    S, L, CS, va, vb = ssim_map(gc, gr)
    H = size; Y, X = np.mgrid[0:H, 0:H]
    s = H/1024.0
    ang = math.radians(33.0)
    fl = Y - (604*s - math.tan(ang)*(X-543*s))
    CURL = (X>=170*s)&(X<=500*s)&(Y>=40*s)&(Y<=420*s)
    blk = (gc < 0.45) | (gr < 0.45)
    al = np.asarray(ci)[...,3]/255.0 > 0.98
    regs = [('curl', CURL & al & ~blk), ('block', blk & ~CURL),
            ('trued', al & ~blk & ~CURL & (fl>0)), ('rough', al & ~blk & ~CURL & (fl<=0)),
            ('rim/out', ~al)]
    print('\n=== %dpx ===  ssim %.4f   (weight %.2f)' % (size, S.mean(), 0.40 if size>=128 else 0.35))
    print('  %-8s %6s %8s %9s %8s %8s %10s %10s' % ('region','frac','ssim','deficit%','lum-term','cs-term','sd_cand','sd_ref'))
    for k, m in regs:
        if m.sum() < 50: continue
        print('  %-8s %6.3f %8.4f %8.1f%% %8.4f %8.4f %10.4f %10.4f' % (
            k, m.mean(), S[m].mean(), 100*((1-S[m]).sum()/(1-S).sum()),
            L[m].mean(), CS[m].mean(), np.sqrt(np.maximum(va[m],0)).mean(), np.sqrt(np.maximum(vb[m],0)).mean()))
