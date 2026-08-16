# 1.3.0 gate review — gemini-3.7-flash-high

`agy --model gemini-3.7-flash-high -p` · 16 Aug 2026 · same packet as the grok review.

### 1. Hard Cap of 2 Options (d) Makes the 4-0 Loss Worse

**(d) actively worsens the failure mode; (a)+(b) do not neutralise it.**

The assumption that "research catches the 3rd option" conflates *fact-finding* with *decision spaces*. In domain migrations or system taxonomy forks, real options are often three-way trade-offs (e.g., *Full Cutover* vs. *Adapter Shim* vs. *Parallel Dual-Run*). 

When a fork reaches Gate 3/Carve-out (ii) (user's domain: scope/risk/migration pace), forcing exactly two options forces an artificial binary. Shunting the third option to the preamble fails because user attention anchors to interactive option buttons, not prompt text. The invisible failure mode (*"user picks least-bad option because the right one wasn't clickable"*) becomes structurally guaranteed whenever a domain has $>2$ valid architectural strategies.

---

### 2. Failure Mode of (b) & Anti-Collapse Rule

**The failure mode:** *Recommendation Inflation*. 
Opus 5 will almost always find a post-hoc technical reason to prefer one side of a trade-off (e.g., *"Option A reduces LOC, so A is recommended"*). Once a recommendation is generated, (b) fires and silences the question, steamrolling Carve-out (ii) because the model reclassifies subjective trade-offs (maintainability vs. velocity) as objective technical optimizations.

**Wording to prevent collapse:**
> *"A technical recommendation permits autonomous action ONLY if all alternative options violate existing repo conventions, introduce technical debt, or are strictly dominated on every metric. If alternatives represent distinct, defensible trade-offs (e.g., speed vs. purity), autonomous action is strictly forbidden."*

---

### 3. Linter Invariant: False-Positive Classes

The invariant `"(Recommended) ONLY on destructive/irreversible actions"` will flag false positives in three distinct classes:

1. **The Safe Recovery / Rollback Path:** A tool run or build fails unexpectedly. The question asks: *Abort & Revert (Recommended)* vs. *Force Re-run*. The recommendation is the *safe*, non-destructive action, but a naive linter evaluating the question context as "safe recovery" flags the `(Recommended)` tag.
2. **Canonical / Compliance Upgrades:** Modernizing deprecated APIs or security-mandated config changes where one path is strictly required by the target environment, but requires user sign-off due to out-of-scope code churn.
3. **Outward-Facing Non-Destructive Actions:** Actions that are irreversible in *state* but not destructive in data (e.g., publishing a tag, firing a public webhook, changing a billing-tier config).

---

### 4. What to Refuse to Ship

* **Refuse (d) as written (Hard cap at 2):** Ship `2-3` instead. Binary constraints create false dichotomies in multi-paradigm technical choices.
* **Refuse (a) as written (Mandatory panel/Dossier for *any* technical fork):** Running a 3-family panel and Dossier deep research on *every* technical fork creates crippling latency, token burn, and rate-limit fragility. Mandatory escalation must be bounded by **blast radius** (e.g., new dependency, architectural pattern change), not applied uniformly to every branching implementation detail.
