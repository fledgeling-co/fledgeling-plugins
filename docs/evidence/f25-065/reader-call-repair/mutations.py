#!/usr/bin/env python3
"""Arm identifier-boundary and call-syntax guards in the actual scanner, then restore exactly."""
from pathlib import Path
import hashlib, json, os, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parents[4]
SOURCE=ROOT/'plugins/test-campaign/skills/test-campaign/scripts/vacuity-check.py'
original=SOURCE.read_text(); before=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
mutants=[
 ('drop-call-syntax',
  'r"\\w*\\s*(?:\\{|\\((?!\\s*(?:(?:_|[A-Za-z]\\w*)\\s*:\\s*)+\\)))"',
  'r"\\w*"'),
 ('allow-function-reference-placeholder',
  'r"\\w*\\s*(?:\\{|\\((?!\\s*(?:(?:_|[A-Za-z]\\w*)\\s*:\\s*)+\\)))"',
  'r"\\w*\\s*(?:\\(|\\{)"'),
 ('drop-invocation-context',
  'if any(reader_invocation_context(source, match.start())',
  'if any(True'),
]
rows=[]
try:
 for name,old,new in mutants:
  assert original.count(old)==1,(name,original.count(old))
  SOURCE.write_text(original.replace(old,new,1))
  with tempfile.TemporaryDirectory(prefix='f25-065-reader-pycache-') as cache:
   env=dict(os.environ,PYTHONPYCACHEPREFIX=cache)
   run=subprocess.run([sys.executable,ROOT/'plugins/test-campaign/tests/test_swift_bodies.py',
                       'SwiftBodies.test_attributed_helper_requires_an_executable_later_reader_call'],
                      cwd=ROOT,capture_output=True,text=True,timeout=60,env=env)
  rows.append({'name':name,'exit':run.returncode,'failedAsRequired':run.returncode!=0,
               'stdout':run.stdout,'stderr':run.stderr})
  SOURCE.write_text(original)
finally:
 SOURCE.write_text(original)
after=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
doc={'sourceSHA256':before,'restoredSHA256':after,'restored':before==after,
     'cacheIsolation':'unique temporary PYTHONPYCACHEPREFIX per mutant','mutants':rows,
     'allRejected':all(x['failedAsRequired'] for x in rows)}
print(json.dumps(doc,indent=2))
raise SystemExit(0 if doc['restored'] and doc['allRejected'] else 1)
