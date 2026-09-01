#!/usr/bin/env python3
from pathlib import Path
import tempfile,importlib.util,json,hashlib
ROOT=Path(__file__).resolve().parents[4]
SCRIPT=ROOT/'plugins/test-campaign/skills/test-campaign/scripts/vacuity-check.py'
spec=importlib.util.spec_from_file_location('vacuity',SCRIPT);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
sha=lambda b:hashlib.sha256(b).hexdigest();out=[]
with tempfile.TemporaryDirectory(prefix='f65-primary-') as td:
 root=Path(td);src='func testInvalidBooleanScope() { write() }';f=root/'ExampleTests.swift';f.write_text(src);ref=root/'producer.swift';ref.write_text('producer contract')
 parsed=m.swift_body_spans(src)['blocks'][0];body=src[parsed['bodyStart']:parsed['end']];start=body.index('write(');assert start==1
 row={'file':'ExampleTests.swift','name':'testInvalidBooleanScope','bodySHA256':sha(body.encode()),'callOffset':True,'callSHA256':m.call_fingerprint(body,start,start+6),'mutator':'write','classification':'direct-output','rationale':'invalid bool offset must refuse','references':[{'path':'producer.swift','sha256':sha(ref.read_bytes())}]}
 path=root/'scopes.json';path.write_text(json.dumps({'version':True,'scopes':[row]}));rows,errors=m.load_blind_scopes(root,'scopes.json');result=m.pass_blind(root,('write',),('read',),rows)
 out.append({'case':'boolean-version-and-offset','source':src,'body':body,'actualOffset':start,'payload':json.loads(path.read_text()),'loadedRows':len(rows),'loadErrors':errors,'findings':result['findings'],'scopeFindings':result['scopeFindings'],'scopedCounts':result['scopedCounts'],'failOpen':len(rows)==1 and not errors and not result['findings'] and not result['scopeFindings']})
 for raw in [False,0,{},[]]:
  rows,errors=m.load_blind_scopes(root,raw);out.append({'case':'falsy-configured-path','raw':raw,'loadedRows':len(rows),'errors':errors,'failOpen':not rows and not errors})
 # Valid relative producer reference is retained as the control.
 valid=dict(row,callOffset=1);path.write_text(json.dumps({'version':1,'scopes':[valid]}));rows,errors=m.load_blind_scopes(root,'scopes.json');out.append({'case':'valid-relative-reference-control','loadedRows':len(rows),'errors':errors,'pass':len(rows)==1 and not errors})
receipt={'sourceSHA256':sha(SCRIPT.read_bytes()),'cases':out,'invalidBooleanSuppressesFinding':out[0]['failOpen'],'falsyConfiguredValuesIgnored':all(x['failOpen'] for x in out[1:5]),'validControlPasses':out[5]['pass']}
print(json.dumps(receipt,indent=2));raise SystemExit(0 if receipt['invalidBooleanSuppressesFinding'] and receipt['falsyConfiguredValuesIgnored'] and receipt['validControlPasses'] else 1)
