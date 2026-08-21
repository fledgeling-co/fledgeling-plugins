### Q1. Taxonomy of Remaining Work & Mechanical Gate

#### The Taxonomy
Your 5-class cut is structurally sound, but (c) and (d) need clearer fix-shapes, and spec contradictions must not collapse into generic test failures. The exact 5-bucket operational partition:

1. **`Unbuilt` (Named & Absent):** Brief exists; zero inventory/surface match; no test cases.  
   *Fix-shape:* Feature implementation pipeline.
2. **`Broken` (Proved Broken / Contradicted):** Campaign `fail`, registered `defect`, or requirement `evidence: contradicted`.  
   *Fix-shape:* Bugfix targeting specific case/oracle failures.
3. **`Unmeasured` (Epistemic Debt / Observability Deficit):** Case $\in \{\text{blocked, inconclusive, unoracled}\}$ OR requirement $\in \{\text{reported, unknown, vacuous}\}$.  
   *Fix-shape:* Test harness, fixture, auth bypass, mock disk, or CDP hook. **Never a feature brief.**
4. **`Untracked` (Dark Surface):** Surface/flow discovered in inventory that maps to zero briefs and zero explicit PRD requirements.  
   *Fix-shape:* Specification brief (retroactive spec or dead-code removal).
5. **`Retirable` (Stale / Completed Briefs):** Brief marked open, but requirement $\in \{\text{observed}\}$ with oracle $\ge \text{outcome}$ and status $\in \{\text{pass}\}$.  
   *Fix-shape:* Archive/delete triage file.

---

#### The Mechanical Conservation Gate
To guarantee unmeasured items never silently masquerade as done:

1. **Entity Conservation Law:** Let $U = \text{Briefs} \cup \text{PRD Requirements} \cup \text{Registry Cases} \cup \text{Inventory Surfaces}$. Every entity $e \in U$ must resolve to exactly one state in $\{\text{Unbuilt, Broken, Unmeasured, Untracked, Retirable, VerifiedDone}\}$.
2. **The Exit-Code Invariant:**
   * Compute `unmeasured_count`.
   * If any entity without `evidence: observed` or with status $\in \{\text{blocked, inconclusive}\}$ is mapped to `VerifiedDone`, **exit code 1 (Fatal Partition Violation)**.
   * If `unmeasured_count / total_inventory > threshold` (e.g., $>0.30$), **exit code 2 (Low Confidence / Epistemic Blockade)**.
   * On success: **exit code 0**.

---

#### The Denominator (Epistemic Horizon)
Never publish a single "Percent Complete" metric—it hides blind spots. Publish two separate metrics:

$$\text{Knowledge Horizon} = \frac{|\text{Requirements}_{\text{observed}}| + |\text{Cases}_{\text{pass}|\text{fail with oracle } \ge \text{outcome}}|}{|\text{Total Stated Requirements}| + |\text{Total Distinct Surfaces}|}$$

$$\text{Observed Completion} = \frac{|\text{VerifiedDone}|}{|\text{VerifiedDone}| + |\text{Unbuilt}| + |\text{Broken}|} \quad (\text{Evaluated strictly over the measured subset})$$

*Example output:* **`Observed Completion: 80% (OVER ONLY 29% OF SURFACE AREA; 71% UNMEASURED)`**.

---

### Q2. Output Shape Ranking

**Rank: Z > Y > X**

1. **Rank 1: (Z) Ledger JSON + Terse Markdown + Exit Code**
   * *Why:* AI executors parse JSON reliably. Markdown gives the human a 10-second summary in terminal output. Exit codes wire cleanly into CLI hooks and CI loops.
2. **Rank 2: (Y) Auto-generated Briefs in `docs/features-to-triage/`**
   * *Why:* Bridges directly to downstream execution. However, generated briefs should only be written for `Unmeasured` items (as `test-harness-*.md`) and `Untracked` items (as `spec-gap-*.md`). Do not rewrite existing feature briefs.
3. **Rank 3: (X) Self-contained HTML**
   * *Why:* High token/maintenance overhead for an agent-driven loop. Let `whats-left` handle UI rendering if a human wants a visual dashboard.

---

### Q3. Should the Skill Read Source Code?

**Recommendation: (x) Never.**

| Option | What it Buys | What it Costs |
| :--- | :--- | :--- |
| **(x) Never (Reconcile only)** | Sub-second runs, zero code-token cost, strict separation of concerns, zero hallucinated AST-parsing logic. | Relies entirely on the campaign registry's accuracy. |
| **(y) Always (Grep producers)** | Catches obviously stale registry entries. | High token cost; shallow regex/grep causes false confidence; duplicates `spec-validation`. |
| **(z) Conditionally (Disagreements only)** | Reconciles discrepancies without running whole-repo passes. | Introduces nondeterministic latency; invites scope creep into code evaluation. |

**Rationale:** The moment this skill greps source code, it becomes a poorly implemented `spec-validation`. Keep its contract pure: **Input is Documents + Campaign Registry; Output is the Remaining Ledger.** If an item is ambiguous or disputed, emit an explicit recommendation: `run spec-validation --target <id>`.

---

### Q4. Is the Framing Wrong?

**The framing is slightly wrong in one critical way: it treats unmeasured work as a backlog column instead of a blocking dependency graph.**

When $>50\%$ of a campaign is blocked, running feature executors produces compounding regression risk. You cannot fix what you cannot measure.

#### The Better Framing: A Two-Phase Unblocking DAG
Instead of a flat 5-bucket list, the skill should construct an **Unblocking DAG**:
1. **Tier 0: Blocker Breakers (Enabling Work):** Group unmeasured cases by root cause (e.g., "OAuth recovery hook", "Mock disk-quota injector").
2. **Tier 1: High-Confidence Product Work:** Features and bug fixes on surfaces that already have `oracle: effect-witness` and `evidence: observed`.
3. **Tier 2: Blind Product Work (Quarantined):** Unbuilt features on unmeasured surfaces, explicitly tagged `BLOCKED_BY_OBSERVABILITY`.

This prevents the AI executor from burning cycles implementing features on dark surfaces that immediately fail or stall during subsequent test campaigns.
