#!/usr/bin/env python3
"""Find the days on which an account's feed holds nothing at all.

A feed-blind day is not a quiet day. On a real run two gaps of 38 and 44 days on the
primary business card were invisible until this was computed, and they contained
charges that belonged in the claim.

Usage:
    python3 find_blind_days.py feed.json --account "Amex Platinum" \
        --start 2025-08-07 --end 2026-06-30 [--min-run 3]

feed.json rows need {day|date, acct|account}.
"""
from __future__ import annotations
import argparse, datetime as dt, json, sys


def load_days(rows, account):
    out = set()
    for r in rows:
        acct = r.get('acct') or r.get('account') or r.get('transaction_account', {}).get('name')
        if account and acct != account:
            continue
        out.add((r.get('day') or r.get('date'))[:10])
    return out


def runs(sorted_days):
    """Collapse consecutive blind dates into (start, end, length) runs."""
    out, run = [], []
    for d in sorted_days:
        if run and (dt.date.fromisoformat(d) - dt.date.fromisoformat(run[-1])).days == 1:
            run.append(d)
        else:
            if run:
                out.append((run[0], run[-1], len(run)))
            run = [d]
    if run:
        out.append((run[0], run[-1], len(run)))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('feed')
    ap.add_argument('--account', required=True)
    ap.add_argument('--start', required=True)
    ap.add_argument('--end', required=True)
    ap.add_argument('--min-run', type=int, default=3,
                    help='only report runs at least this long')
    a = ap.parse_args()

    rows = json.load(open(a.feed))
    have = load_days(rows, a.account)
    start, end = dt.date.fromisoformat(a.start), dt.date.fromisoformat(a.end)
    period = [(start + dt.timedelta(days=i)).isoformat()
              for i in range((end - start).days + 1)]
    blind = [d for d in period if d not in have]
    reportable = [r for r in runs(blind) if r[2] >= a.min_run]

    print(f"[vouch-coverage] account={a.account!r} · period days={len(period)} · "
          f"days with data={len(period) - len(blind)} · blind={len(blind)} · "
          f"runs>={a.min_run}d={len(reportable)}")
    for s, e, n in reportable:
        print(f"    {s} .. {e}   ({n} days with no transaction at all)")
    if not reportable:
        print("    no run long enough to suggest a feed outage")
    print("\nBackfill each run from the card statement covering it "
          "(scripts/parse_statement.py), then re-run the sweep.")

    json.dump({'account': a.account, 'blind_days': blind,
               'runs': [{'start': s, 'end': e, 'days': n} for s, e, n in reportable]},
              open('blind_days.json', 'w'), indent=1)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
