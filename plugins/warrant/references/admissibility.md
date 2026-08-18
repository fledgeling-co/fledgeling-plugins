# Admissibility — what the standards demand of a warrant

Read this before writing or renewing a warrant. It is the reason the pipeline keeps one human
signature rather than none, and it is where the wording of `warrant.toml` comes from.

Nothing here is legal advice, and the corpus behind it cannot supply one. Whether any of these
instruments reaches an internal software release control at a given company is a legal
classification that a lawyer makes on the facts. What the corpus can supply is the shape of the
constraint, which is enough to design against.

## The four instruments

### 21 CFR Part 11 — a signature belongs to a person

An electronic signature must be unique to one individual and must not be reused by or reassigned to
anyone else (`C11`). A model identifier fails that on its face: it is not an individual, it is
shared across every invocation, and it is reassigned every time the vendor ships a new version.

**What the warrant does about it.** `owner.name` and `owner.email` are required and validation
rejects a file without them. The signature is on the policy, once, rather than on each item — and
that is a different act from a per-item attestation, which is why it survives the rule that kills
the per-item version.

A role with no current holder is a warrant with no signature. If the named owner leaves, the warrant
is invalid until a person is named, and `charter_validate.py` treats that as a hard failure rather
than a warning.

### PCAOB Auditing Standard 2201 — the control must not have changed

An auditor may lean on a previous period's testing of an entirely automated control only where they
verify the control has not changed since (`C12`). Two lanes reach that clause; the inference that a
silently reversioned model fails the predicate is ours, and it is the single most load-bearing
inference in the plugin.

**What the warrant does about it.** Every lane pins a model id and a model version in `lanes.toml`,
and an unpinned lane fails validation. `warrant:ratchet` compares the pinned version against the one
recorded at the class's last regression run, and a difference revokes the class to tier 0 without
asking. That is the predicate mechanised: the control changed, so the benchmark no longer holds.

This is also why the warrant is a committed file rather than a database row. An auditor reading
`git log` can see when the control changed and who signed the change.

### ISO/IEC 17025 — an inconclusive result is a result

The laboratory-competence standard requires measurement uncertainty to be declared, and treats an
inconclusive outcome as a valid one rather than a failure to produce an outcome (`C13`). The text is
paywalled; existence is confirmed and contents are unread, so this row carries medium confidence.

**What the warrant does about it.** `inconclusive` is a terminal verdict state that routes to a
person, not a retry. This matters more than it sounds: the target product's own screenshot-judging
pass already returns `inconclusive` on all 50 surfaces that have both captures and expectations
present, and the instinct is to read that as a broken pipeline. Under this standard it is the
correct output, and forcing it to binary would manufacture certainty the pipeline does not have.

### DO-330 — a tool whose output nobody checks needs qualifying

Criterion 2 covers exactly the tool class this plugin builds: one that could fail to detect an error
where its output is not otherwise verified. It requires Tool Operational Requirements, a
qualification plan, and re-qualification whenever the tool changes (`C10`). The standard is paywalled
and the clause detail here is industry restatement.

**What the warrant does about it.** The warrant *is* the Tool Operational Requirements document: it
names what the tool may decide, on which classes, at which tier, under what escalation. The
regression corpus is the qualification evidence, and the model-version revocation trigger is the
re-qualification rule.

The structural problem DO-330 exposes is worth stating plainly rather than designing around: the
standard presumes specifiable, deterministic tool behaviour, and a model judge has neither. That is
why the deterministic plane exists and why it runs first — the part of the pipeline that can be
specified in the DO-330 sense is the part that does not call a model.

## What no instrument in the corpus permits

An all-machine verification step accepted as the control of record. Four independent readers searched
for one and none found it — no regulated software vendor, no enforcement action or qualified opinion
where the defence was that the automated checks passed (`C21`). That is a search absence rather than
a proof, and auditors' acceptance decisions are frequently private, so treat it as the state of the
public record rather than as a law.

The design consequence is the whole shape of this plugin: authority is delegated by a standing scope
that a person owns, and the per-item act inside that scope is a measurement rather than an
attestation. No standard in the corpus requires an individual to sign a measurement.

## What would change this

A published regulated-industry precedent where an automated verification step became the control of
record, or a legal classification finding that Part 11 does not reach an internal release gate. Both
are outside what this corpus can settle. If either lands, the residual signature becomes a choice
rather than a constraint, and `warrant:charter` is the one place that would change.
