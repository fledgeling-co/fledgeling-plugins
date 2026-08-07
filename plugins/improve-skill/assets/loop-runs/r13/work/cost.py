"""Price the placement edit before authoring it: how many of the file's paths and
bytes belong to the grain, and what one extra polyline node costs.

Bytes bind on this fixture and paths do not - 1726/3000 paths but 323,357/350,000
bytes - so any placement change that adds vertices has to pay for them.
"""
import re, pathlib
s = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/icon.svg").read_text()
paths = re.findall(r'<path [^>]*>', s)
grain = [p for p in paths if "stroke-dasharray" in p]
print(f"paths total {len(paths)}   with dasharray (grain) {len(grain)}"
      f"   grain bytes {sum(len(p) for p in grain)}  file {len(s)}")
verts = sum(p.count(" L ") + 1 for p in grain)
coords = re.findall(r'-?\d+\.\d ', " ".join(g.split('d="')[1].split('"')[0] for g in grain))
print(f"grain vertices {verts}   mean bytes/path {sum(len(p) for p in grain)/len(grain):.0f}")
print(f"one extra vertex on every grain path costs about {verts and 14*len(grain)} bytes")
print(f"dropping coordinate precision from .1f to .0f saves about {2*2*verts} bytes")
print(f"headroom {350000 - len(s)} bytes, {3000 - len(paths)} paths")
