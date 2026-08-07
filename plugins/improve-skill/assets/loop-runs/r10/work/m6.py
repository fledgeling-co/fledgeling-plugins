"""Attribution probe: which authored layer owns the master's excess mid-scale energy?

Builds ablated variants of the CURRENT icon.svg by deleting one layer's elements
by their distinctive fill/stroke colour, renders each, and reports the full
five-size composite the gate would see, plus the rough-ground patch sd at 1024
and after an 8x box average (the 128px read).
"""
import sys, re, pathlib, json, numpy as np
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
Wd = A / "loop-runs/r10/work"
SVG = (A / "icon.svg").read_text()
REF = A / "icon-engineC-f5665d-2.png"

ABL = {
    "base":            [],
    "-rough grain":    [r'<path d="[^"]*" stroke="#6A5F4C"[^/]*/>'],
    "-trued grain":    [r'<path d="[^"]*" stroke="#8A7C64"[^/]*/>',
                        r'<path d="M [-\d.]+ -8 L [-\d.]+ [-\d.]+" stroke="#FFFFFF"[^/]*/>'],
    "-rough mottle":   [r'<ellipse [^/]*fill="#8C7A5E"[^/]*/>', r'<ellipse [^/]*fill="#FFF6E4"[^/]*/>'],
    "-trued mottle":   [r'<ellipse [^/]*fill="#9C8A6C"[^/]*/>',
                        r'<ellipse cx="[-\d]+" cy="[-\d]+" rx="\d+" ry="\d+" fill="#FFFFFF"[^/]*/>'],
    "-stone blotch":   [r'<ellipse [^/]*fill="#9A968C"[^/]*/>', r'<ellipse [^/]*fill="#191714"[^/]*/>'],
}


def score(svg_text, tag):
    p = Wd / f"probe-{tag}.svg"
    p.write_text(svg_text)
    out = {}
    for size in (1024, 256, 128, 32, 16):
        ca = F.render_candidate(p, size)
        rb = F.normalise_reference(REF, size)
        g, h = F.to_gray(ca), F.to_gray(rb)
        m = {"lum_delta": float(np.abs(g.mean() - h.mean()) + np.abs(g - h).mean() * 0),
             "ssim": F.ssim(g, h), "edge_f1": F.edge_f1(g, h)}
        # fidelity's own lum_delta definition
        m["lum_delta"] = float(np.abs(g - h).mean())
        mi = F.mask_iou(ca, rb)
        if mi is not None:
            m["mask_iou"] = mi
        m["composite"] = F.composite_for(size, m)
        out[size] = m
    return out


base = None
for tag, pats in ABL.items():
    s = SVG
    n = 0
    for pat in pats:
        s, k = re.subn(pat, "", s)
        n += k
    r = score(s, tag.replace(" ", "_"))
    tot = sum(r[k]["composite"] for k in r)
    if base is None:
        base = r
    line = "  ".join(f"{k}:{r[k]['composite']:.4f}" for k in (1024, 256, 128, 32, 16))
    d = "  ".join(f"{r[k]['composite']-base[k]['composite']:+.4f}" for k in (1024, 256, 128, 32, 16))
    print(f"{tag:16s} removed={n:4d}  {line}   net {tot - sum(base[k]['composite'] for k in base):+.4f}")
    print(f"{'':16s}   delta         {d}")
    print(f"{'':16s}   ssim1024 {r[1024]['ssim']:.4f} ef1024 {r[1024]['edge_f1']:.4f} "
          f"ssim128 {r[128]['ssim']:.4f} ef128 {r[128]['edge_f1']:.4f} lum1024 {r[1024]['lum_delta']:.4f}")
