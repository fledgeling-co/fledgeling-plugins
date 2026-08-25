#!/usr/bin/env python3
"""Render a session transcript as a readable digest.

  slice.py <session.jsonl> [--from N] [--to N] [--full-text] [--tools] [--grep RE]

Every emitted block is prefixed with its source line number so a finding can cite
`<session>:<line>` and another reader can go and check it.
"""
import json, sys, re, argparse, os

ap=argparse.ArgumentParser()
ap.add_argument('path'); ap.add_argument('--from',dest='lo',type=int,default=0)
ap.add_argument('--to',dest='hi',type=int,default=10**9)
ap.add_argument('--grep',default=None)
ap.add_argument('--tools',action='store_true',help='include tool inputs')
ap.add_argument('--results',action='store_true',help='include tool results (truncated)')
ap.add_argument('--maxtext',type=int,default=2600)
ap.add_argument('--sidechain',action='store_true')
a=ap.parse_args()
rx=re.compile(a.grep,re.I) if a.grep else None
buf=[]
with open(a.path,errors='replace') as f:
    for ln,line in enumerate(f,1):
        if ln<a.lo or ln>a.hi: continue
        try: o=json.loads(line)
        except Exception: continue
        if o.get('isSidechain') and not a.sidechain: continue
        t=o.get('type'); msg=o.get('message') or {}; c=msg.get('content')
        blocks=c if isinstance(c,list) else ([{'type':'text','text':c}] if isinstance(c,str) else [])
        if t=='user':
            for b in blocks:
                if not isinstance(b,dict): continue
                if b.get('type')=='text':
                    tx=b.get('text','')
                    if tx.strip().startswith('<local-command') or '<system-reminder>' == tx.strip()[:17]: pass
                    buf.append(f"\n[{ln}] ===== HUMAN =====\n{tx[:a.maxtext*2]}")
                elif b.get('type')=='tool_result' and a.results:
                    r=b.get('content')
                    s=r if isinstance(r,str) else ' '.join(x.get('text','') for x in (r or []) if isinstance(x,dict))
                    tag='ERROR' if b.get('is_error') else 'result'
                    buf.append(f"[{ln}]   <{tag}> {' '.join(s.split())[:700]}")
        elif t=='assistant':
            mdl=msg.get('model','')
            for b in blocks:
                if not isinstance(b,dict): continue
                if b.get('type')=='text' and b.get('text','').strip():
                    buf.append(f"\n[{ln}] ----- {mdl} -----\n{b['text'][:a.maxtext]}")
                elif b.get('type')=='tool_use':
                    nm=b.get('name'); inp=b.get('input') or {}
                    if a.tools:
                        s=json.dumps(inp)[:900]
                    else:
                        s=(inp.get('command') or inp.get('file_path') or inp.get('skill')
                           or inp.get('pattern') or inp.get('prompt') or json.dumps(inp)[:200])
                        s=' '.join(str(s).split())[:300]
                    buf.append(f"[{ln}]   >> {nm}: {s}")
out='\n'.join(buf)
if rx:
    keep=[]; lines=out.split('\n')
    for i,l in enumerate(lines):
        if rx.search(l): keep += lines[max(0,i-6):i+10]
    out='\n'.join(dict.fromkeys(keep))
sys.stdout.write(out+'\n')
