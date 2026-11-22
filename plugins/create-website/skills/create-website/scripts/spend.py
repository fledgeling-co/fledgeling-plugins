#!/usr/bin/env python3
"""Keep the running cost of billed generation for one site, so the person sees it before and after.

    python3 spend.py quote  --ledger .create-website/spend.json --what "hero clip 1" --model veo-3.1 --unit second --price 0.40 --units 8
    python3 spend.py add    --ledger .create-website/spend.json --what "hero clip 1" --model veo-3.1 --unit second --price 0.40 --units 8
    python3 spend.py total  --ledger .create-website/spend.json [--cap 20]

quote  print what a call will cost and what the total becomes, and record the quote apart from
       spend. Say this to the person before the first billed clip or image set.
add    record a call that ran, and print the new running total. Say the total after each call.
total  print the running total; with --cap, exit 1 when the total has reached the cap the person
       set, so the next billed call waits for them.
Prices are what the provider states for the model at the time; record the source in --what when
it is not obvious. The ledger records spend; it does not authorise it.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone


def load(path):
    if os.path.exists(path):
        return json.load(open(path, encoding="utf-8"))
    return {"currency": "USD", "entries": []}


def total(led):
    return round(sum(e["cost"] for e in led["entries"]), 2)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("quote", "add"):
        p = sub.add_parser(name)
        p.add_argument("--ledger", required=True)
        p.add_argument("--what", required=True)
        p.add_argument("--model", required=True)
        p.add_argument("--unit", required=True, help="second, image, or call")
        p.add_argument("--price", type=float, required=True, help="price per unit")
        p.add_argument("--units", type=float, required=True)
    t = sub.add_parser("total")
    t.add_argument("--ledger", required=True)
    t.add_argument("--cap", type=float)
    a = ap.parse_args()
    led = load(a.ledger)
    if a.cmd in ("quote", "add"):
        cost = round(a.price * a.units, 2)
        if a.cmd == "add":
            led["entries"].append({"at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "what": a.what,
                                   "model": a.model, "unit": a.unit, "price": a.price, "units": a.units, "cost": cost})
            os.makedirs(os.path.dirname(os.path.abspath(a.ledger)), exist_ok=True)
            json.dump(led, open(a.ledger, "w"), indent=2)
            print(f"recorded {a.what}: {a.units:g} {a.unit}(s) of {a.model} at ${a.price:.2f} = ${cost:.2f}. Running total ${total(led):.2f}")
        else:
            # A quote is recorded apart from spend, so the ledger shows the price was stated first.
            led.setdefault("quotes", []).append({"at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                                                 "what": a.what, "model": a.model, "unit": a.unit, "price": a.price,
                                                 "units": a.units, "cost": cost})
            os.makedirs(os.path.dirname(os.path.abspath(a.ledger)), exist_ok=True)
            json.dump(led, open(a.ledger, "w"), indent=2)
            print(f"quoted {a.what}: {a.units:g} {a.unit}(s) of {a.model} at ${a.price:.2f} = ${cost:.2f}. Total would become ${total(led) + cost:.2f}")
        return 0
    tot = total(led)
    print(f"{len(led['entries'])} billed call(s), running total ${tot:.2f}" + (f" of a ${a.cap:.2f} cap" if a.cap else ""))
    return 1 if a.cap is not None and tot >= a.cap else 0


if __name__ == "__main__":
    sys.exit(main())
