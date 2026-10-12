#!/usr/bin/env python3
"""Read-only validation and summary of a private follow-through ledger."""

import argparse
from datetime import datetime
import json
from pathlib import Path
import sys

DOMAINS = {"ops", "household", "decision", "commitment"}
STATES = {"unverified", "actionable", "waiting", "blocked", "completed", "dismissed"}
KINDS = {"current", "reported", "history"}


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("must be an ISO timestamp string")
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError("must include a timezone")
    return result


def validate(data):
    """Return errors; never infer source truth, consent or missing state."""
    errors = []
    if not isinstance(data, dict):
        return ["ledger must be an object"]

    def required(obj, field, label):
        value = obj.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{label}.{field}: nonempty string required")
            return None
        return value

    def time(value, label):
        try:
            return timestamp(value)
        except (ValueError, TypeError, OverflowError) as exc:
            errors.append(f"{label}: {exc}")
            return None

    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        errors.append("schema_version must be 1")
    required(data, "goal", "ledger")
    required(data, "stop_condition", "ledger")
    as_of = time(data.get("as_of"), "as_of")
    sources = data.get("sources")
    items = data.get("items")
    if not isinstance(sources, list) or not isinstance(items, list):
        return errors + ["sources and items must be arrays"]
    source_map = {}
    observed = {}
    for n, source in enumerate(sources):
        label = f"sources[{n}]"
        if not isinstance(source, dict):
            errors.append(f"{label}: object required")
            continue
        sid = required(source, "id", label)
        required(source, "scope", label)
        required(source, "locator", label)
        if sid in source_map:
            errors.append(f"{label}: duplicate source id {sid}")
        if not isinstance(source.get("kind"), str) or source["kind"] not in KINDS:
            errors.append(f"{label}: invalid kind")
        checked = time(source.get("observed_at"), f"{label}.observed_at")
        event = time(source["event_at"], f"{label}.event_at") if "event_at" in source else None
        if checked and as_of and checked > as_of:
            errors.append(f"{label}: observation is after as_of")
        if event and checked and event > checked:
            errors.append(f"{label}: event is after observation")
        if sid:
            source_map[sid] = source
            observed[sid] = checked
    ids = set()
    identities = set()
    for n, item in enumerate(items):
        label = f"items[{n}]"
        if not isinstance(item, dict):
            errors.append(f"{label}: object required")
            continue
        iid = required(item, "id", label)
        scope = required(item, "scope", label)
        identity = required(item, "identity", label)
        required(item, "summary", label)
        required(item, "owner", label)
        if iid in ids:
            errors.append(f"{label}: duplicate item id {iid}")
        ids.add(iid)
        domain = item.get("domain")
        if not isinstance(domain, str) or domain not in DOMAINS:
            errors.append(f"{label}: invalid domain")
            domain = None
        # Reject malformed values without hashing an untrusted list/dict.
        if isinstance(domain, str) and scope and identity:
            key = (domain, scope, identity)
            if key in identities:
                errors.append(f"{label}: duplicate identity {key}")
            identities.add(key)
        state = item.get("state")
        if not isinstance(state, str) or state not in STATES:
            errors.append(f"{label}: invalid state")
            state = None
        evidence = item.get("evidence")
        if not isinstance(evidence, list) or any(not isinstance(e, str) for e in evidence):
            errors.append(f"{label}.evidence: source-id array required")
            evidence = []
        if len(evidence) != len(set(evidence)):
            errors.append(f"{label}: duplicate evidence reference")
        for sid in evidence:
            if sid not in source_map:
                errors.append(f"{label}: unknown source {sid}")
            elif source_map[sid].get("scope") != scope:
                errors.append(f"{label}: source {sid} has different scope")
        if state not in {"unverified", "blocked"} and not evidence:
            errors.append(f"{label}: evidenced state has no evidence")
        if state != "completed":
            required(item, "next_action", label)
        if state == "dismissed":
            required(item, "reason", label)
        volatile = item.get("volatile", False)
        if not isinstance(volatile, bool):
            errors.append(f"{label}.volatile: boolean required")
        max_age = item.get("max_age_hours")
        if volatile and (type(max_age) not in {int, float} or not 0 < max_age < float("inf")):
            errors.append(f"{label}.max_age_hours: positive finite number required")
            max_age = None
        elif type(max_age) not in {int, float}:
            max_age = None
        fresh = set()
        for sid in evidence:
            if sid in source_map and source_map[sid].get("kind") == "current":
                checked = observed.get(sid)
                if checked and as_of and checked <= as_of:
                    age = (as_of - checked).total_seconds() / 3600
                    if not volatile or (max_age is not None and age <= max_age):
                        fresh.add(sid)
        if volatile and state in {"actionable", "waiting", "completed"} and not fresh:
            errors.append(f"{label}: volatile state needs fresh current evidence")
        if state == "completed":
            required(item, "outcome", label)
            completion = item.get("completion_evidence")
            if not isinstance(completion, list) or not completion or any(not isinstance(e, str) for e in completion):
                errors.append(f"{label}: completion_evidence must name current sources")
            else:
                if any(sid not in evidence or sid not in fresh for sid in completion):
                    errors.append(f"{label}: completion needs linked current evidence (fresh when volatile)")
    return errors


def summary(data):
    counts = {state: 0 for state in sorted(STATES)}
    rows = []
    for item in data["items"]:
        counts[item["state"]] += 1
        rows.append({key: item.get(key) for key in
                     ("id", "domain", "state", "summary", "owner", "next_action", "outcome")})
    return {"goal": data["goal"], "as_of": data["as_of"], "stop_condition": data["stop_condition"],
            "total": len(rows), "counts": counts, "items": rows}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "summary"])
    parser.add_argument("ledger", type=Path)
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.ledger.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}))
        return 1
    errors = validate(data)
    if errors:
        print(json.dumps({"ok": False, "errors": errors}, indent=2))
        return 1
    result = {"ok": True, "items": len(data["items"]), "sources": len(data["sources"])}
    print(json.dumps(result if args.command == "check" else summary(data), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
