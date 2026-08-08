"""r12 diagnostic 8: WHY did 16px cost 0.0078? Isolate the block's own mean per size.

Control = this exact SVG with the one filter attribute stripped, written to a scratch
file so the candidate is left alone. Anything that differs between the two at a given
size is the relief, and anything that differs BETWEEN SIZES is the relief failing to be
mean-neutral there.
"""
import sys, pathlib, tempfile, numpy as np
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
svg = (A / "icon.svg").read_text()
assert svg.count('filter="url(#ironGrit)"') == 1
ctl = pathlib.Path(tempfile.mkdtemp()) / "control.svg"
ctl.write_text(svg.replace('filter="url(#ironGrit)"', ""))

blockmask = np.load("d_topface.npy") | np.load("d_front.npy")
print("%5s | %-28s | %-28s | %s" % ("size", "block mean L  ctl -> grit", "whole-icon mean L", "lum_delta ctl -> grit"))
for size in (1024, 256, 128, 32, 16):
    gc = F.to_gray(F.render_candidate(ctl, size))
    gg = F.to_gray(F.render_candidate(A / "icon.svg", size))
    ref = F.to_gray(F.normalise_reference(A / "icon-engineC-f5665d-2.png", size))
    step = 1024 // size
    m = blockmask[::step, ::step][:size, :size]
    print("%5d | %.4f -> %.4f  (%+.4f) | %.4f -> %.4f  (%+.4f) | %.4f -> %.4f"
          % (size, gc[m].mean(), gg[m].mean(), gg[m].mean() - gc[m].mean(),
             gc.mean(), gg.mean(), gg.mean() - gc.mean(),
             np.abs(gc - ref).mean(), np.abs(gg - ref).mean()))
    if size <= 32:
        print("        block px sd  ctl %.4f -> grit %.4f" % (gc[m].std(), gg[m].std()))
