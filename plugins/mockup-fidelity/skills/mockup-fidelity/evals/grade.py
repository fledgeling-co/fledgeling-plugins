#!/usr/bin/env python3
"""Grade two mockup-fidelity runs against the ten planted defects in the fixture.

Takes two run directories, each holding a `target.findings.json` written by
`assets/diff/capture.mjs --out <dir>`, and reports which planted defect each run
caught, declared inconclusive, or silently graded clean. A false pass is the
defect this whole skill exists to prevent, so it is counted separately.

    python3 grade.py <old-run-dir> <new-run-dir>
    python3 grade.py                       # defaults to out-old/ and out-new/

The paths used to be hardcoded relative to the working directory with no
argument interface and no check, so running this file as shipped raised a bare
FileNotFoundError from json.load several frames deep. Neither directory has ever
been committed, and they cannot be: a run directory is output. So the honest fix
is an interface plus a refusal that says what the inputs are and how to make
them, which is what an audit on 2026-08-19 asked for.
"""

import argparse
import json
import pathlib
import sys

# Answer key. `probe` = a predicate over the findings list that means "this planted defect was caught".
KEY = [
 ("D1","absent — whole 'Your watchlist' card removed",
   lambda F: any('watchlist' in (str(f.get('locator',''))+str(f.get('reference',''))+str(f.get('suggestedChange',''))).lower() for f in F)),
 ("D2","content — \"Editor's picks\" -> \"Movers today\"",
   lambda F: any("editor" in (str(f.get('reference',''))+str(f.get('locator',''))+str(f.get('suggestedChange',''))).lower()
                 or "movers today" in (str(f.get('target',''))+str(f.get('locator',''))).lower() for f in F)),
 ("D3","colour — muted text #9ca0ac -> #5e6a82",
   lambda F: any('5e6a82' in str(f.get('target','')).lower() or '9ca0ac' in str(f.get('reference','')).lower() for f in F)),
 ("D4","shadow — card box-shadow removed  [UNMEASURABLE HERE]",
   lambda F: any(f.get('class')=='shadow' or 'shadow' in str(f.get('property','')).lower() for f in F)),
 ("D5","spacing — card padding-top 16 -> 24",
   lambda F: any('pad' in str(f.get('property','')).lower() and str(f.get('target'))in('24','24px','24.0') for f in F)
             or any('pad-top' in str(f.get('property','')).lower() for f in F)),
 ("D6","layout — .row flex-direction row -> column",
   lambda F: any('flex-direction' in str(f.get('property','')).lower() for f in F)),
 ("D7","text-transform — uppercase removed, SAME source text  [UNMEASURABLE HERE]",
   lambda F: any('text-transform' in str(f.get('property','')).lower() for f in F)),
 ("D8","icon — trailing arrow <svg> removed from the CTA",
   lambda F: any('arrow' in str(f.get('property','')).lower() for f in F)),
 ("D9","radius — card border-radius 12 -> 4",
   lambda F: any('radius' in str(f.get('property','')).lower() for f in F)),
 ("D10","gradient — CSS linear-gradient -> flat colour  [UNMEASURABLE HERE]",
   lambda F: any(f.get('class')=='gradient' or 'bg-image' in str(f.get('property','')).lower()
                 or 'gradient' in str(f.get('property','')).lower() for f in F)),
]
# which capability silences which defect, for the inconclusive credit
SILENCES = {"D4":"shadow","D7":"textTransform","D10":"gradient","D8":"svgGlyphExtent"}

def load(p: pathlib.Path):
    d = json.loads(p.read_text())
    return d.get('findings', []), d.get('inconclusive', []), d.get('summary', {})


def resolve(arg: str, label: str) -> pathlib.Path:
    """A run directory, or the findings file inside one. Refuse with a sentence."""
    p = pathlib.Path(arg)
    candidate = p if p.suffix == '.json' else p / 'target.findings.json'
    if candidate.is_file():
        return candidate
    print(f"grade.py: no {label} findings at {candidate}", file=sys.stderr)
    print(f"  A run directory is output, never committed, so this file has to be produced first:",
          file=sys.stderr)
    print(f"  node ../assets/diff/capture.mjs --ref <mock> --target <build> --out {p}",
          file=sys.stderr)
    print(f"  Then: python3 grade.py <old-run-dir> <new-run-dir>", file=sys.stderr)
    raise SystemExit(2)


ap = argparse.ArgumentParser(description=__doc__.split(chr(10))[0])
ap.add_argument('old', nargs='?', default='out-old',
                help="the baseline run's directory (default: out-old)")
ap.add_argument('new', nargs='?', default='out-new',
                help="the run being graded (default: out-new)")
args = ap.parse_args()

rows=[]
oldF,oldI,oldS = load(resolve(args.old, 'baseline'))
newF,newI,newS = load(resolve(args.new, 'graded'))
newIkeys = {i['capability'] for i in newI}
oldIkeys = {i['capability'] for i in oldI}

print(f"OLD: {len(oldF)} findings, {len(oldI)} inconclusive declared, score {oldS.get('score')}, conclusive={oldS.get('conclusive')}")
print(f"NEW: {len(newF)} findings, {len(newI)} inconclusive declared, score {newS.get('score')}, conclusive={newS.get('conclusive')}")
print()
hdr=f"{'ID':<4} {'defect':<58} {'OLD':<22} {'NEW':<22}"
print(hdr); print('-'*len(hdr))
tally={'old_catch':0,'new_catch':0,'old_falsepass':0,'new_falsepass':0,'new_declared':0}
for cid,desc,probe in KEY:
    o = probe(oldF); n = probe(newF)
    cap = SILENCES.get(cid)
    o_decl = cap in oldIkeys if cap else False
    n_decl = cap in newIkeys if cap else False
    def verdict(caught, declared):
        if caught: return "CATCH"
        if declared: return "declared INCONCLUSIVE"
        return "** FALSE PASS **"
    ov, nv = verdict(o,o_decl), verdict(n,n_decl)
    if o: tally['old_catch']+=1
    if n: tally['new_catch']+=1
    if ov=="** FALSE PASS **": tally['old_falsepass']+=1
    if nv=="** FALSE PASS **": tally['new_falsepass']+=1
    if nv.startswith("declared"): tally['new_declared']+=1
    print(f"{cid:<4} {desc:<58} {ov:<22} {nv:<22}")
print('-'*len(hdr))
print(f"{'':<4} {'CAUGHT':<58} {str(tally['old_catch'])+'/10':<22} {str(tally['new_catch'])+'/10':<22}")
print(f"{'':<4} {'FALSE PASSES (silently graded clean)':<58} {str(tally['old_falsepass']):<22} {str(tally['new_falsepass']):<22}")
print(f"{'':<4} {'DECLARED INCONCLUSIVE (honest non-answer)':<58} {'0':<22} {str(tally['new_declared']):<22}")
print()
print("arrow findings NEW:", [ (f.get('property'), f.get('target'), f.get('reference')) for f in newF if 'arrow' in str(f.get('property','')).lower()])
print("arrow findings OLD:", [ (f.get('property'), f.get('target'), f.get('reference')) for f in oldF if 'arrow' in str(f.get('property','')).lower()])
print("icon findings NEW:", [ f.get('property') for f in newF if f.get('class')=='icon'])
