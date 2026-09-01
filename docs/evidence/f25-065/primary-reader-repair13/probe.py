#!/usr/bin/env python3
from __future__ import annotations
import hashlib, importlib.util, json, subprocess, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SCRIPT = ROOT / 'plugins/test-campaign/skills/test-campaign/scripts/vacuity-check.py'
spec = importlib.util.spec_from_file_location('f25065_primary13', SCRIPT)
scan = importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(scan)

def scope_for(source: str, helper_call: str = 'seed(') -> dict:
    blocks = scan.swift_body_spans(source)['blocks']
    helper, caller = blocks[0], blocks[1]
    hb = source[helper['bodyStart']:helper['end']]
    cb = source[caller['bodyStart']:caller['end']]
    target = hb.index('store('); call = cb.index(helper_call)
    return {'file':'ExampleTests.swift','name':helper['name'],
      'bodySHA256':hashlib.sha256(hb.encode()).hexdigest(),'testEntry':helper['testEntry'],
      'callOffset':target,'callSHA256':scan.call_fingerprint(hb,target,target+len('store(')),
      'mutator':'store','classification':'attributed-helper','rationale':'caller reads after helper',
      'references':[], 'callers':[{'file':'ExampleTests.swift','name':caller['name'],
        'bodySHA256':hashlib.sha256(cb.encode()).hexdigest(),'testEntry':caller['testEntry'],
        'callOffset':call,'callSHA256':scan.call_fingerprint(cb,call,call+len(helper_call))}]}

def cli(source: str, helper_call: str = 'seed(') -> dict:
    with tempfile.TemporaryDirectory(prefix='f25-065-primary13-') as td:
      root=Path(td); (root/'tests').mkdir(); (root/'tests/ExampleTests.swift').write_text(source)
      (root/'inventory.json').write_text(json.dumps({'requirement':[{'id':'REQ-001','title':'x','effect':'none'}]}))
      (root/'producer.swift').write_text('contract\n')
      row=scope_for(source, helper_call)
      row['references']=[{'path':'producer.swift','sha256':hashlib.sha256(b'contract\n').hexdigest()}]
      (root/'scopes.json').write_text(json.dumps({'version':1,'scopes':[row]}))
      (root/'campaign.json').write_text(json.dumps({'testRoot':'tests','blindScopeFile':'scopes.json',
        'blindVocabulary':{'only':True,'mutators':['store'],'readers':['read']}}))
      p=subprocess.run(['python3',str(SCRIPT),str(root),'--gate'],text=True,capture_output=True)
      return {'exit':p.returncode,'invalidScope':'INVALID SCOPE' in p.stdout,
              'scopeSummary':next((x.strip() for x in p.stdout.splitlines() if 'Swift scopes:' in x),''),
              'lastLine':p.stdout.strip().splitlines()[-1] if p.stdout.strip() else '',
              'stdout':p.stdout}

cases={
 'valid-direct':('private func seed() { store() }\nfunc testMeasure() { seed(); read() }','seed(',0),
 'valid-qualified':('private func seed() { store() }\nfunc testMeasure() { Fixtures.seed(); read() }','seed(',0),
 'valid-balanced-args-second-reader':('private func seed(_ x:Int) { store() }\nfunc testMeasure() { seed(read()); read() }','seed(',0),
 'valid-after-nested-return-block':('private func seed() { store() }\nfunc testMeasure() { if false { return }; seed(); read() }','seed(',0),
 'valid-semicolon-boundary':('private func seed() { store() }\nfunc testMeasure() { let value = 1; seed(); read(); _ = value }','seed(',0),
 'invalid-balanced-args-only-reader':('private func seed(_ x:Int) { store() }\nfunc testMeasure() { seed(read()) }','seed(',1),
 'invalid-nested-control':('private func seed() { store() }\nfunc testMeasure() { if true { seed() }; read() }','seed(',1),
 'invalid-prior-return-semicolon':('private func seed() { store() }\nfunc testMeasure() { return; seed(); read() }','seed(',1),
 'invalid-prior-throw-semicolon':('enum E:Error { case boom }\nprivate func seed() { store() }\nfunc testMeasure() throws { throw E.boom; seed(); read() }','seed(',1),
 'invalid-do-return-block':('private func seed() { store() }\nfunc testMeasure() { do { return }; seed(); read() }','seed(',1),
 'invalid-do-throw-block':('enum E:Error { case boom }\nprivate func seed() { store() }\nfunc testMeasure() throws { do { throw E.boom }; seed(); read() }','seed(',1),
 'invalid-repeat-return-block':('private func seed() { store() }\nfunc testMeasure() { repeat { return } while false; seed(); read() }','seed(',1),
 'invalid-return-single-line':('private func seed() -> Int { store(); return 1 }\nfunc testMeasure() -> Int { return seed(); read(); return 2 }','seed(',1),
 'invalid-throw-single-line':('enum E: Error { case boom }\nprivate func seed() -> E { store(); return .boom }\nfunc testMeasure() throws { throw seed(); read() }','seed(',1),
 'invalid-return-multiline':('private func seed() -> Int { store(); return 1 }\nfunc testMeasure() -> Int { return\n seed()\n read(); return 2 }','seed(',1),
 'invalid-throw-multiline':('enum E: Error { case boom }\nprivate func seed() -> E { store(); return .boom }\nfunc testMeasure() throws { throw\n seed()\n read() }','seed(',1),
 'invalid-return-comment-newline':('private func seed() -> Int { store(); return 1 }\nfunc testMeasure() -> Int { return /* terminal\n */ seed()\n read(); return 2 }','seed(',1),
 'invalid-throw-comment-newline':('enum E: Error { case boom }\nprivate func seed() -> E { store(); return .boom }\nfunc testMeasure() throws { throw /* terminal\n */ seed()\n read() }','seed(',1),
 'invalid-bare-trailing':('private func seed(_ f:()->Void) { store(); f() }\nfunc testMeasure() { seed { }; read() }','seed {',1),
 'invalid-parenthesized-trailing':('private func seed(_ f:()->Void = {}) { store(); f() }\nfunc testMeasure() { seed() { }; read() }','seed(',1),
 'invalid-comment-parenthesized-trailing':('private func seed(_ f:()->Void = {}) { store(); f() }\nfunc testMeasure() { seed() /* gap */ { }; read() }','seed(',1),
 'invalid-multiple-trailing':('private func seed(first:()->Void = {}, second:()->Void) { store() }\nfunc testMeasure() { seed() { } second: { }; read() }','seed(',1),
}

out={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'cases':{}}
for name,(source,call,expected) in cases.items():
  got=cli(source,call); got['expectedExit']=expected; got['matchesExpected']=got['exit']==expected
  out['cases'][name]=got
out['allExpected']=all(x['matchesExpected'] for x in out['cases'].values())
print(json.dumps(out,indent=2))
