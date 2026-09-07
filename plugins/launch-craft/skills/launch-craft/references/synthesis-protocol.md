# Synthesis protocol: OVERVIEW.md and PRD.md

The output describes the repository's actual product and separates implemented behavior from plans and mocks. The orchestrator reads the source material or supplies it to a runner; the bundled inventory helper alone does not perform synthesis.

## Input contract

Discover the repository's actual directories, using these conventions as starting points:

| Input | What it can establish |
| --- | --- |
| `docs/features-to-triage/*.md` | Requested behavior, rationale, scope and acceptance intent |
| `docs/plans/*.md`, `docs/specs/*.md` | Approved design or implementation intent |
| `design/mocks/html/*.html`, `mocks/*.html` | Designed screens and states |
| Source, manifests, tests and captured execution | Architecture, dependencies and observed implementation |
| Positioning and commercial decisions | Audience, category, approved prices and entitlements |

Record the complete in-scope source list before drafting. Give every brief an explicit requirement row or a reason it is outside scope. The scan helper counts conventional files and prints their paths; it does not classify status.

## Runner brief

Use the selected runtime's supported runner interface. Pass a prompt file when supported; do not construct a shell command by interpolating source text. A runner must have access to every path named in its brief. Replace all template fields before dispatch.

```text
<context>
Project root: [absolute path]
Accepted decisions: [paths and relevant decisions]
In-scope inventory: [complete file list]
Existing documents to preserve: [paths]
Output paths: [OVERVIEW.md, PRD.md, feature-trace.md]
</context>

<task>
Read the listed material. Produce OVERVIEW.md describing product purpose,
architecture, actual dependencies, modules and key workflows. Produce PRD.md
with audience, feature requirements, acceptance criteria and status. Produce
feature-trace.md mapping every in-scope brief to a requirement ID and source.

Separate Built, In Progress, Planned, Triaged and Backlog. Use Built only where
implementation evidence supports it; record the evidence locator and any
execution limitation. A mock or plan alone does not establish shipped behavior.

Use only approved audience, pricing, platform and entitlement facts. Mark
unknown facts as unresolved instead of filling them from an example product.

Write only the named outputs. Return their paths, the count of briefs covered,
any excluded briefs with reasons, and unresolved factual conflicts. Keep the
return concise; the documents carry the full substance.
</task>
```

## Acceptance

Check coverage against the original inventory, read representative source-linked claims and resolve conflicting statuses before site implementation. Document length follows the product's complexity; do not pad each heading to a fixed length. Include an architecture diagram where it clarifies relationships, and validate its names against the source.
