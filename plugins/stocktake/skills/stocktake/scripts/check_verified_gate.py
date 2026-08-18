#!/usr/bin/env python3
"""The eight preconditions for promoting a card past Done into Verified.

Done is what an out-of-family verdict can grant. Verified is a person's
judgement, and stays one until every precondition below holds for the ONE
pre-registered low-risk class being promoted.

This script exists so the question gets asked rather than assumed. Its exit
code is the answer: 0 = all eight hold for this class, 1 = named ones missing.

Refusing is the feature. A skipped hard gate that leaves no trace reads
afterwards as a gate that passed.

  check_verified_gate.py <config.json> [--class NAME]
  check_verified_gate.py --template > verified-gate.json
"""
import argparse, json, os, sys

# Each: key, one-line question, why it is not ceremony.
PRECONDITIONS = [
    ("composite_reference_standard",
     "Is there a composite reference standard — multi-person adjudication plus known escapes?",
     "Without one there is nothing to be non-inferior TO. Evaluator agreement on review "
     "findings runs 5-65%, so a single reviewer is not a gold standard."),
    ("seeded_defect_bank",
     "Is there a seeded-defect bank of >=50 items across >=8 classes, blinded and rotating?",
     "A verifier that has never been shown a known defect has never been measured."),
    ("diagnosability_gate_blocking",
     "Does an inconclusive verdict BLOCK rather than round up to a pass?",
     "ISO/IEC 17025 treats inconclusive as valid output. FDA DEN180001 granted autonomy "
     "WITH a mandatory can't-tell path: 38 of 819 exams were forced to refer."),
    ("producer_verifier_isolation",
     "Is the verifier isolated from the producer, with signed attestation of test provenance?",
     "The evidence channel is authored by the party being judged. METR documents agents "
     "editing tests and monkey-patching evaluators."),
    ("verifier_control_chart",
     "Is there a control chart on verifier performance with a suspend rule?",
     "A reversioned model voids prior benchmarking (PCAOB AS 2201). Drift is invisible "
     "without a chart."),
    ("preregistered_ni_study",
     "Is there a pre-registered non-inferiority study on THIS class alone?",
     "No powered NI reader study has ever been run on code or UI review. Running one on "
     "one low-risk class is the smallest honest claim."),
    ("blinded_human_sample",
     "Has a blinded human sample of the existing queue been taken, with AI marks NOT shown first?",
     "Concurrent-read positioning cost specificity and detection across 429,345 reads "
     "(Fenton 2007). Second-read is the design that worked."),
    ("retention_for_readjudication",
     "Is retention long enough to re-adjudicate a promoted decision later?",
     "A promotion nobody can revisit is a promotion nobody can audit."),
]


def template():
    return {
        "class": "<the one pre-registered low-risk defect class this covers>",
        "preconditions": {k: {"holds": False, "evidence": ""} for k, _, _ in PRECONDITIONS},
    }


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("config", nargs="?")
    p.add_argument("--class", dest="klass")
    p.add_argument("--template", action="store_true")
    a = p.parse_args()

    if a.template:
        print(json.dumps(template(), indent=1))
        return 0

    if not a.config or not os.path.exists(a.config):
        print("REFUSED — no Verified-gate config exists.\n")
        print("Auto-promotion past Done is refused until all eight preconditions are")
        print("recorded as holding, with evidence, for one named low-risk class.\n")
        print("Start one:  check_verified_gate.py --template > verified-gate.json\n")
        for i, (_, q, why) in enumerate(PRECONDITIONS, 1):
            print(f"  {i}. {q}\n     {why}")
        return 1

    with open(a.config) as f:
        cfg = json.load(f)

    klass = a.klass or cfg.get("class") or ""
    missing = []
    unevidenced = []
    for key, q, why in PRECONDITIONS:
        entry = (cfg.get("preconditions") or {}).get(key) or {}
        if not entry.get("holds"):
            missing.append((key, q, why))
        elif not (entry.get("evidence") or "").strip():
            unevidenced.append((key, q))

    if not klass or klass.startswith("<"):
        print("REFUSED — no class named. Verified may be granted for ONE pre-registered")
        print("low-risk class, never for the board as a whole.")
        return 1

    if missing or unevidenced:
        print(f"REFUSED for class {klass!r} — {len(missing)} precondition(s) not met, "
              f"{len(unevidenced)} asserted without evidence.\n")
        for key, q, why in missing:
            print(f"  MISSING  {key}\n           {q}\n           {why}")
        for key, q in unevidenced:
            print(f"  NO-EVIDENCE  {key}\n               {q}")
        return 1

    print(f"All eight preconditions hold for class {klass!r}, each with evidence.")
    print("Auto-promotion to Verified is permitted FOR THIS CLASS ONLY.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
