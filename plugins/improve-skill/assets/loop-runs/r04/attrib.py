"""r04: disentangle two writers on one fixture.

Something outside this track edited build_icon.py's curl constants mid-round. This builds
each source in its own scratch directory (build_icon.py writes icon.svg beside itself) so
nothing on the shared fixture is touched, hashes them against the shipped icon.svg, and
scores this round's edit on its own.
"""
import hashlib
import pathlib
import re
import shutil
import subprocess
import sys

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
R4 = A / "loop-runs/r04"
SCRATCH = R4 / "scratch-attrib"
FID = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts/fidelity.py"


def md5(p):
    return hashlib.md5(pathlib.Path(p).read_bytes()).hexdigest()[:12]


def build(name, src):
    d = SCRATCH / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "build_icon.py").write_text(src)
    for extra in ("squircle-path.txt",):
        if (A / extra).exists():
            shutil.copy(A / extra, d / extra)
    r = subprocess.run([sys.executable, "build_icon.py"], cwd=d, capture_output=True, text=True)
    if not (d / "icon.svg").exists():
        print(f"  {name}: BUILD FAILED\n{r.stderr[-800:]}")
        return None
    return d / "icon.svg"


base = (R4 / "_before/build_icon.py").read_text()
mine = base.replace("BLADE_THICK = 152.0", "BLADE_THICK = 204.0")
mine = re.sub(r"^CURL_BASE_L = \(289\.0, 130\.0\)",
              "CURL_BASE_L = (289.0, BLADE_THICK - 22.0)", mine, flags=re.M)
assert "BLADE_THICK = 204.0" in mine and "BLADE_THICK - 22.0" in mine, "patch did not apply"

print(f"shipped icon.svg          md5 {md5(A / 'icon.svg')}")
for name, src in (("current", (A / "build_icon.py").read_text()),
                  ("mine", mine),
                  ("baseline", base)):
    svg = build(name, src)
    if svg:
        print(f"{name:24s}  md5 {md5(svg)}")

svg = SCRATCH / "mine/icon.svg"
if svg.exists():
    subprocess.run([sys.executable, FID, "score", "--candidate", str(svg),
                    "--reference", str(A / "icon-engineC-f5665d-2.png"),
                    "--outdir", str(R4 / "mine-only"), "--label", "r04 coarse structure (this track only)"],
                   check=True)
