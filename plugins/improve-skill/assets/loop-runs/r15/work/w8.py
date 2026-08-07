"""Fit each image's OWN block edges, then bin luminance by perpendicular distance.

Positionally determined detail (an arris, a shoulder trough, a contact shadow)
is the only kind this metric can reward, because both images put it in the same
place. Registration differs, so each image's edge is fitted on that image.
"""
import numpy as np
import common as C

c, r = C.cand(), C.ref()
Lc, Lr = C.lum(c), C.lum(r)
xs, ys = C.grid((1024, 1024))


def fit_line(L, p0, ang0, half=26, span=170, angs=None, offs=None):
    """Search inclination + offset for the line of greatest mean |luminance step|,
    measuring the step across a window `half` wide, over a segment of length `span`."""
    best = None
    for a in (angs if angs is not None else np.arange(ang0 - 12, ang0 + 12.01, 0.5)):
        th = np.radians(a)
        ux, uy = np.cos(th), -np.sin(th)      # along the line
        nx, ny = -uy, ux                      # across it
        for o in (offs if offs is not None else np.arange(-30, 30.01, 1.0)):
            t = np.linspace(-span / 2, span / 2, 140)
            px = p0[0] + ux * t + nx * o
            py = p0[1] + uy * t + ny * o
            hi = L[np.clip((py - ny * half / 2).astype(int), 0, 1023),
                   np.clip((px - nx * half / 2).astype(int), 0, 1023)]
            lo = L[np.clip((py + ny * half / 2).astype(int), 0, 1023),
                   np.clip((px + nx * half / 2).astype(int), 0, 1023)]
            step = abs(hi.mean() - lo.mean())
            if best is None or step > best[0]:
                best = (step, a, o)
    return best


def profile(L, p0, ang, off, span=170, dmin=-16, dmax=16):
    th = np.radians(ang)
    ux, uy = np.cos(th), -np.sin(th)
    nx, ny = -uy, ux
    t = np.linspace(-span / 2, span / 2, 220)
    out = []
    for d in np.arange(dmin, dmax + 0.001, 1.0):
        px = p0[0] + ux * t + nx * (off + d)
        py = p0[1] + uy * t + ny * (off + d)
        v = L[np.clip(py.astype(int), 0, 1023), np.clip(px.astype(int), 0, 1023)]
        out.append((d, v.mean()))
    return out


# ---- the block's BACK edge (top face against the un-planed ground), 3 stations
print("=== back edge (top face | un-planed ground) ===")
for tag, lxs in [("A", 180), ("B", 340), ("C", 500)]:
    p = C.to_top(lxs, C.BLADE_THICK)
    for name, L in (("cand", Lc), ("ref", Lr)):
        st, a, o = fit_line(L, p, np.degrees(np.arctan2(-(C.UY - C.K_RISE), C.UX)))
        pr = profile(L, p, a, o)
        plate_in = np.mean([v for d, v in pr if -14 <= d <= -8])    # face side
        plate_out = np.mean([v for d, v in pr if 8 <= d <= 14])     # ground side
        peak = max(v for d, v in pr if -6 <= d <= 6)
        peak_d = [d for d, v in pr if v == peak][0]
        print("  %s %-4s step %.3f ang %5.1f off %+5.1f | face %.3f  peak %.3f @d%+.0f  ground %.3f"
              % (tag, name, st, a, o, plate_in, peak, peak_d, plate_out))

# ---- the SHOULDER (top face | front face), 3 stations
print("\n=== shoulder (top face | front face) ===")
for tag, lxs in [("A", 180), ("B", 340), ("C", 500)]:
    p = C.to_top(lxs, 0.0)
    for name, L in (("cand", Lc), ("ref", Lr)):
        st, a, o = fit_line(L, p, np.degrees(np.arctan2(-(C.UY - C.K_RISE), C.UX)), half=20, span=150)
        pr = profile(L, p, a, o, span=150, dmin=-20, dmax=20)
        top = np.mean([v for d, v in pr if -18 <= d <= -12])
        front = np.mean([v for d, v in pr if 12 <= d <= 18])
        lo = min(v for d, v in pr if -8 <= d <= 8)
        lo_d = [d for d, v in pr if v == lo][0]
        print("  %s %-4s step %.3f ang %5.1f off %+5.1f | top %.3f  trough %.3f @d%+.0f (%+.1f%%)  front %.3f"
              % (tag, name, st, a, o, top, lo, lo_d, 100 * (lo / top - 1), front))
