#!/usr/bin/env python3
"""Response-level metrics: only the FIRST assistant text after a real human turn."""
import json, sys, collections, re
GLYPH='\U0001FAE5'
def scan(path):
    fired=False; ok=0; miss=0; misses=[]
    awaiting=False
    tools=collections.Counter(); turns=0
    with open(path,errors='replace') as f:
        for ln,line in enumerate(f,1):
            if not fired and ('Begin every conversational response' in line): fired=True
            try: o=json.loads(line)
            except Exception: continue
            if o.get('isSidechain'): continue
            t=o.get('type')
            if t=='user':
                m=o.get('message') or {}; c=m.get('content')
                # a genuine human turn: string content, or blocks with no tool_result
                if isinstance(c,str): human=True
                else: human = bool(c) and not any(isinstance(b,dict) and b.get('type')=='tool_result' for b in c)
                if human and not (o.get('isMeta')): awaiting=True
            elif t=='assistant':
                turns+=1
                blocks=(o.get('message') or {}).get('content') or []
                for b in blocks:
                    if isinstance(b,dict) and b.get('type')=='tool_use': tools[b.get('name','?')]+=1
                txt=''.join(b.get('text','') for b in blocks if isinstance(b,dict) and b.get('type')=='text').strip()
                if awaiting and txt:
                    awaiting=False
                    if txt.startswith(GLYPH): ok+=1
                    else:
                        miss+=1
                        if len(misses)<3: misses.append(dict(line=ln,quote=' '.join(txt[:100].split())))
    return dict(path=path, fired=fired, ok=ok, miss=miss, misses=misses, tools=dict(tools), turns=turns)

rows=json.load(open(sys.argv[1])); out=[]
for r in rows:
    s=scan(r['path']); s['proj']=r.get('proj','?'); s['size']=r.get('size',0); out.append(s)
json.dump(out,open(sys.argv[2],'w'),indent=1)
f=[r for r in out if r['fired']]
ok=sum(r['ok'] for r in f); mi=sum(r['miss'] for r in f)
print(f"{sys.argv[3]}: {len(f)}/{len(out)} sessions with the marker instruction; "
      f"first-reply glyph {ok}/{ok+mi} = {ok/max(1,ok+mi)*100:.1f}%")
T=collections.Counter()
for r in out: T.update(r['tools'])
for t in ('AskUserQuestion','Agent','Workflow','TodoWrite','Task','ExitPlanMode','ToolSearch','Skill'):
    print(f"   {t:16} {T.get(t,0)}")
