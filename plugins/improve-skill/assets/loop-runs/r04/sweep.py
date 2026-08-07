"""r04 sweep driver: build variants of build_icon.py, render, score with the harness.

Every variant is a coarse-structure re-registration onto values measured off the
reference; the sweep exists to choose among them, not to hunt constants.
"""
import json
import pathlib
import re
import shutil
import subprocess
import sys

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
R4 = A / "loop-runs/r04"
SRC = (R4 / "_before/build_icon.py").read_text()
FID = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts/fidelity.py"
REF = A / "icon-engineC-f5665d-2.png"

VARIANTS = {
    "v1_angle":       dict(ANGLE=38.9),
    "v2_angle_thick": dict(ANGLE=38.9, BLADE_THICK=192.0),
    "v3_full":        dict(ANGLE=38.9, BLADE_THICK=192.0, BLADE_LEN=560.0),
    "v4_full_centre": dict(ANGLE=38.9, BLADE_THICK=192.0, BLADE_LEN=560.0, EDGE_MID=(571.0, 596.0)),
    "v5_thick_only":  dict(BLADE_THICK=192.0),
    "t204": dict(BLADE_THICK=204.0),
    "t172": dict(BLADE_THICK=172.0),
    "t182": dict(BLADE_THICK=182.0),
    "t202": dict(BLADE_THICK=202.0),
    "t212": dict(BLADE_THICK=212.0),
    "t232": dict(BLADE_THICK=232.0),
    "t192_len560": dict(BLADE_THICK=192.0, BLADE_LEN=560.0),
    "t192_len600": dict(BLADE_THICK=192.0, BLADE_LEN=600.0),
}


def patch(src, ov):
    for k, v in ov.items():
        if k == "EDGE_MID":
            src = re.sub(r"^EDGE_MID = \([^)]*\)",
                         f"EDGE_MID = ({v[0]}, {v[1]})", src, flags=re.M)
        elif k == "ANGLE":
            src = re.sub(r"^ANGLE = math\.radians\([0-9.]+\)",
                         f"ANGLE = math.radians({v})", src, flags=re.M)
        else:
            src = re.sub(rf"^{k} = [0-9.]+", f"{k} = {v}", src, flags=re.M)
    return src


only = sys.argv[1:] or list(VARIANTS)
for name in only:
    ov = VARIANTS[name]
    (A / "build_icon.py").write_text(patch(SRC, ov))
    out = subprocess.run([sys.executable, "build_icon.py"], cwd=A, capture_output=True, text=True)
    print(f"--- {name} {ov}")
    print(out.stdout.strip() or out.stderr.strip())
    probe = R4 / f"{name}.svg"
    shutil.copy(A / "icon.svg", probe)
    od = R4 / f"scratch-{name}"
    subprocess.run([sys.executable, FID, "score", "--candidate", str(probe),
                    "--reference", str(REF), "--outdir", str(od), "--label", name],
                   capture_output=True, text=True)
    s = json.loads((od / "score.json").read_text())["sizes"]
    print("    " + "  ".join(f"{k}:{s[k]['composite']:.4f}" for k in ("1024", "256", "128", "32", "16")))
    base = json.loads((A / "loop-runs/r01/score.json").read_text())["sizes"]
    net = sum(s[k]["composite"] - base[k]["composite"] for k in s)
    print(f"    net {net:+.4f}   lum {s['1024']['lum_delta']:.4f} ssim {s['1024']['ssim']:.4f} "
          f"edge {s['1024']['edge_f1']:.4f}  |  sc32 {s['32']['self_contrast']:.4f} "
          f"(base {base['32']['self_contrast']:.4f})  sc16 {s['16']['self_contrast']:.4f} "
          f"(base {base['16']['self_contrast']:.4f})")

(A / "build_icon.py").write_text(SRC)
subprocess.run([sys.executable, "build_icon.py"], cwd=A, capture_output=True)
print("\nrestored baseline build_icon.py + icon.svg")
