#!/usr/bin/env python3
"""
make_bundles.py — generate blind judging bundles with seeded random ordering.
"""

import json
import pathlib
import random
import re

BASE_DIR = pathlib.Path("/tmp/luke-evals")
EVALS_JSON = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-luke-content/evals/evals.json")
evals_data = json.load(open(EVALS_JSON))["evals"]

SEED = 20260827
rng = random.Random(SEED)

mapping = {}

def strip_meta(text: str) -> str:
    # Remove markers that might reveal the arm
    t = text.replace("🫥", "").strip()
    return t

for e in evals_data:
    eid = e["id"]
    c_file = BASE_DIR / "candidate" / f"{eid}.txt"
    p_file = BASE_DIR / "predecessor" / f"{eid}.txt"
    if not (c_file.exists() and p_file.exists()):
        print(f"Skipping {eid}: files missing")
        continue

    c_text = strip_meta(c_file.read_text())
    p_text = strip_meta(p_file.read_text())

    flip = rng.random() < 0.5
    opt_a, opt_b = (c_text, p_text) if flip else (p_text, c_text)
    mapping[eid] = {
        "A": "candidate" if flip else "predecessor",
        "B": "predecessor" if flip else "candidate"
    }

    bundle = f"""# Blind Judging Bundle — Eval {eid}: {e['name']}

You are an expert blind judge evaluating two candidate responses written as Luke Rhodes (CTO and co-founder of Diolog, an ASX fintech/IR SaaS). Both candidates were given the exact same prompt.

## Prompt given to both:
> {e['prompt']}

## Evaluation Criteria:
1. **Voice fidelity**: Does it sound like Luke (calm, direct, technically fluent without ego, understated dry wit, Australian spelling, contractions, no em dashes, no corporate buzzwords or AI tells)?
2. **Copywriting craft & credibility**: For marketing/business copy, does it demonstrate utility concretely with mechanisms, real numbers, and transparent boundaries, rather than relying on abstract benefits or hype adjectives?
3. **Factual grounding & integrity**: Does it adhere strictly to the supplied facts without fabricating numbers, testimonials, or conversational scaffolding?

---

### OPTION A:
```markdown
{opt_a}
```

---

### OPTION B:
```markdown
{opt_b}
```

---

### YOUR VERDICT:
Analyze both options across Voice, Craft, and Grounding.
State which option is better, or TIE.
Your final line MUST be exactly:
OVERALL: [A|B|TIE]
"""
    (BASE_DIR / "bundles" / f"{eid}.md").write_text(bundle)

(BASE_DIR / "unblinding-map.json").write_text(json.dumps({"seed": SEED, "map": mapping}, indent=2))
print(f"Generated bundles for {len(mapping)} evals. Unblinding map written to unblinding-map.json.")
