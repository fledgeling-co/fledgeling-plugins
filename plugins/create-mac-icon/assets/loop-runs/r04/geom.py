#!/usr/bin/env python3
"""Print the geometry the round touches, so the leak is placed against real
coordinates rather than arithmetic."""
import re
import sys
import pathlib
import numpy as np

sys.argv = ["build_icon.py"]
src = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/build_icon.py").read_text()
src = src.replace('out.write_text(svg)', 'pass')
g = {"__name__": "probe", "__file__": "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/assets/build_icon.py"}
exec(compile(src, "build_icon.py", "exec"), g)

for name in ("mould_top", "cav_top", "tile_sil"):
    pts = np.array(g[name] if isinstance(g[name][0], (list, tuple)) else g[name])
    print(f"  {name:10s} x {pts[:,0].min():.0f}..{pts[:,0].max():.0f}   "
          f"y {pts[:,1].min():.0f}..{pts[:,1].max():.0f}")
ring = np.array(g["shift"](g["mould_top"], 0, g["MOULD_H"]))
print(f"  ring       x {ring[:,0].min():.0f}..{ring[:,0].max():.0f}   "
      f"y {ring[:,1].min():.0f}..{ring[:,1].max():.0f}")
lo = ring[np.argmin(ring[:, 0])]
print(f"  ring left tip  ({lo[0]:.0f},{lo[1]:.0f})    MOULD_H {g['MOULD_H']}")
