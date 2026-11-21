import json,glob,re,sys,collections,os
d=sys.argv[1]; key=json.load(open(d+"/unblind.json"))
res=collections.defaultdict(dict); imp=collections.defaultdict(list)
for f in sorted(glob.glob(d+"/*.md")):
    name,order,lane,_=os.path.basename(f).rsplit(".",3); t=open(f).read()
    a_is=key[f"{name}.{order}"]["A"]; other="without_skill" if a_is=="with_skill" else "with_skill"
    out={}
    for dim in ("ACCURACY","READS","SUITS","VERDICT"):
        m=re.findall(rf"{dim}:\s*\**\s*(A|B|TIE)\b",t); v=m[-1] if m else None
        out[dim]={"A":a_is,"B":other,"TIE":"tie",None:"MISSING"}[v]
    res[(name,lane)][order]=out
    for side in ("A","B"):
        m=re.search(rf"IMPROVE_{side}:\s*(.+)",t)
        if m: imp[(name, a_is if side=="A" else other)].append(f"[{lane}/{order}] {m.group(1).strip()[:330]}")
for (name,lane),o in sorted(res.items()):
    cells=[]
    for dim in ("ACCURACY","READS","SUITS","VERDICT"):
        a,b=o.get("fwd",{}).get(dim,"MISSING"),o.get("rev",{}).get(dim,"MISSING")
        cells.append(f"{dim[:4]}={a if a==b else 'flip('+a+'/'+b+')'}")
    print(f"{name:8s} {lane:12s} "+"  ".join(cells))
if "--improve" in sys.argv:
    for k in sorted(imp):
        if k[1]=="with_skill":
            print(f"\n## what would improve the WITH-SKILL {k[0]}"); print("\n".join(imp[k]))
