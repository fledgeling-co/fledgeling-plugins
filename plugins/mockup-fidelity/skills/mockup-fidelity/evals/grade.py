import json, sys, re

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

def load(p):
    d=json.load(open(p)); return d.get('findings',[]), d.get('inconclusive',[]), d.get('summary',{})

rows=[]
oldF,oldI,oldS = load('out-old/target.findings.json')
newF,newI,newS = load('out-new/target.findings.json')
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
