#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,os,subprocess,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[4]
source=root/'plugins/test-campaign/skills/test-campaign/scripts/vacuity-check.py'
test=root/'plugins/test-campaign/tests/test_swift_bodies.py'
original=source.read_text(); original_hash=hashlib.sha256(original.encode()).hexdigest()

def replace_once(text, old, new):
 assert text.count(old)==1,(old,text.count(old)); return text.replace(old,new,1)

def simple(old,new): return lambda s:replace_once(s,old,new)
mutants=[
 ('drop-call-syntax',simple('+ r"\\w*\\s*\\((?!\\s*', '+ r"\\w*\\s*(?!\\s*')),
 ('allow-function-reference-placeholder',simple(
  '                   + r"\\w*\\s*\\((?!\\s*(?:(?:`[^`\\r\\n]+`|[^():,\\s]+)\\s*:\\s*)+\\))"',
  '                   + r"\\w*\\s*\\("')),
 ('allow-reader-trailing-closure',simple(
  '    return False\n\n# ── what a provider has to resolve to ──',
  '    return bool(re.search(r"\\bread\\s*\\{", source))\n\n# ── what a provider has to resolve to ──')),
 ('allow-nested-reader',simple(
  'if any(reader_invocation_context(source, match.start())\n               for match in re.finditer(pattern, source)):',
  'if any(True for match in re.finditer(pattern, source)):')),
 ('allow-conditional-reader',simple(
  '    if conditional_depth:\n        return False',
  '    if False and conditional_depth:\n        return False')),
 ('skip-helper-execution-context',simple(
  '                        not helper_invocation_context(masked_caller, context_start)):',
  '                        False):')),
 ('allow-return-position-helper',simple(
  '    if re.match(r"(?:return|throw)\\b", statement):',
  '    if False and re.match(r"(?:return|throw)\\b", statement):')),
 ('split-helper-terminal-at-newline',simple(
  'statement = re.split(r"[;{}]", source[:start])[-1].strip()',
  'statement = re.split(r"[;\\n{}]", source[:start])[-1].strip()')),
 ('allow-parenthesized-trailing-helper',simple(
  '                if masked_caller[reader_tail:].lstrip().startswith("{"):',
  '                if False and masked_caller[reader_tail:].lstrip().startswith("{"):')),
 ('scan-helper-arguments-as-later-readers',simple(
  '                if not has_reader_call(masked_caller[reader_tail:], readers):',
  '                if not has_reader_call(masked_caller[offset + match.end():], readers):')),
 ('allow-top-level-terminator-reader',simple(
  '        if depths[terminal.start()] == minimum_depth and prefix[terminal.end():].strip():',
  '        if False and depths[terminal.start()] == minimum_depth and prefix[terminal.end():].strip():')),
 ('drop-invocation-context',simple(
  'if any(reader_invocation_context(source, match.start())\n               for match in re.finditer(pattern, source)):',
  'if any(True for match in re.finditer(pattern, source)):')),
]
results=[]
try:
 for i,(name,mutate) in enumerate(mutants):
  changed=mutate(original); assert changed!=original
  source.write_text(changed)
  with tempfile.TemporaryDirectory(prefix=f'f25-065-primary13-mut-{i}-') as cache:
   env=dict(os.environ,PYTHONPYCACHEPREFIX=cache)
   p=subprocess.run(['python3',str(test),'-k','test_attributed_helper_requires_an_executable_later_reader_call'],cwd=root,text=True,capture_output=True,env=env)
  results.append({'name':name,'exit':p.returncode,'rejected':p.returncode!=0,
    'tail':'\n'.join((p.stdout+p.stderr).strip().splitlines()[-8:])})
  source.write_text(original)
finally:
 source.write_text(original)
restored=hashlib.sha256(source.read_bytes()).hexdigest()
print(json.dumps({'sourceSHA256':original_hash,'restoredSHA256':restored,'restored':original_hash==restored,
 'mutants':results,'allRejected':all(x['rejected'] for x in results)},indent=2))
