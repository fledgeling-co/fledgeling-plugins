#!/usr/bin/env python3
"""Verify installed CLI snapshots and cache content; never modify an installation."""
import argparse
import hashlib
import json
from pathlib import Path
import sys


def installed_rows(data, provider):
    if provider == 'claude':
        rows = data if isinstance(data, list) else None
    elif provider == 'codex':
        rows = data.get('installed') if isinstance(data, dict) else None
    else:
        raise ValueError('only observed Claude and Codex snapshot schemas are supported')
    if not isinstance(rows, list) or not rows or not all(isinstance(r, dict) for r in rows):
        raise ValueError('missing, empty or malformed installed snapshot; cannot establish adoption')
    key = 'id' if provider == 'claude' else 'pluginId'
    if any(not isinstance(r.get(key), str) or not r[key] for r in rows):
        raise ValueError('installed snapshot has unidentified entries')
    identities = [(r[key], r.get('scope', '')) for r in rows]
    if len(identities) != len(set(identities)):
        raise ValueError('duplicate installed identity/scope; reconcile before verifying')
    return rows


def verify(before, after, provider, target, version, source_skill, cached_skill):
    old, new = installed_rows(before, provider), installed_rows(after, provider)
    key = 'id' if provider == 'claude' else 'pluginId'
    targets = [r for r in new if r[key] == target]
    if len(targets) != 1:
        raise ValueError('expected exactly one installed target; missing or ambiguous scope')
    row = targets[0]
    if row.get('version') != version or row.get('enabled') is not True:
        raise ValueError('target version/enabled state does not match requested adoption')
    if provider == 'codex' and row.get('installed') is not True:
        raise ValueError('target is not installed')
    if not any(r[key] == target for r in old):
        raise ValueError('update verification requires an already-installed target')
    def others(rows):
        return sorted((r[key], r.get('scope', ''), r.get('enabled'), r.get('installed', True),
                       r.get('version')) for r in rows if r[key] != target)
    if others(old) != others(new):
        raise ValueError('unrelated installation identity/version/enabled state changed')
    source, cached = Path(source_skill).read_bytes(), Path(cached_skill).read_bytes()
    if not source or not cached or source != cached:
        raise ValueError('source and installed skill contents are empty or differ')
    return {'status': 'installed_content_verified', 'provider': provider, 'target': target,
            'version': version, 'installed_count': len(new), 'other_count': len(new)-1,
            'skill_sha256': hashlib.sha256(source).hexdigest(),
            'active_session_loaded': 'not established by installation evidence'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ['before', 'after', 'provider', 'target', 'version', 'source-skill', 'cached-skill']:
        p.add_argument('--'+name, required=True)
    a = p.parse_args()
    try:
        r = verify(json.loads(Path(a.before).read_text()), json.loads(Path(a.after).read_text()),
                   a.provider, a.target, a.version, a.source_skill, a.cached_skill)
        print(json.dumps(r, indent=2))
        return 0
    except (OSError, ValueError, KeyError) as e:
        print(json.dumps({'status': 'refused', 'reason': str(e)}))
        return 2

if __name__ == '__main__':
    sys.exit(main())
