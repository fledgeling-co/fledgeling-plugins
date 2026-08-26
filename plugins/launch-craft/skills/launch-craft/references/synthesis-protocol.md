# Synthesis Protocol: OVERVIEW.md & PRD.md

This protocol defines the exact extraction, aggregation, and synthesis standards for turning scattered project files into authoritative product documentation using Gemini 3.7 Flash High.

---

## 1. Input Corpus Aggregation

The synthesis engine scans and indexes:
1. **Feature Briefs (`docs/features-to-triage/*.md`)**:
   - Extracts: Feature name, core rationale, target audience, technical scope, and platform implications.
2. **Implementation Plans & Specs (`docs/plans/*.md`, `docs/specs/*.md`)**:
   - Extracts: Component architecture, data models, state machines, API endpoints.
3. **Mock UIs (`design/mocks/html/*.html`, `mocks/*.html`)**:
   - Extracts: Screen hierarchies, interactive states, UI component taxonomy.
4. **Application Codebase (`src/`, `apps/`, `packages/`, config files)**:
   - Extracts: Runtime frameworks, database adapters, IPC/networking protocols, active routes.

---

## 2. Gemini Invocation Standard

Run the aggregation prompt through `agy`:
```bash
perl -e 'alarm shift @ARGV; exec @ARGV' 900 agy --new-project --model gemini-3.7-flash-high -p "<aggregation_prompt>" > /tmp/synthesis.md 2>/tmp/synthesis.log
```

### Prompt Construction Template:
```
You are an expert Principal Software Architect and Product Lead.
Examine the provided project codebase files, mock HTML, implementation plans, and feature briefs in docs/features-to-triage/.

Generate two authoritative documents:

PART 1: OVERVIEW.md
- Project Identity & Mission Statement
- System Architecture Diagram (Mermaid)
- Core Technology Stack & Module Map
- Runtime Infrastructure & Deployment Target
- Key Workflows & Data Flows

PART 2: PRD.md
- Product Vision & Goals
- User Personas (Primary: Home Network Admins, Secondary: Gamers/Power Users)
- Complete Feature Requirement Traceability Matrix:
  * ID / Name
  * Status (Built / In Progress / Triaged / Backlog)
  * User Story & Acceptance Criteria
  * Target Platforms (Windows, Mac, iPad, iPhone, Linux)
  * Originating Brief / Source File
- Non-Functional Requirements (Latency, Privacy, Memory Footprint, Offline Resilience)
- Security & BYOK Architecture
```

---

## 3. Output Schema & Invariants

### Invariants for `OVERVIEW.md`:
- Must include a clean Mermaid architecture diagram.
- Must list actual dependencies and runtimes discovered from repository package manifests.
- Must avoid speculative filler text.

### Invariants for `PRD.md`:
- Every file in `docs/features-to-triage/` MUST map to at least one numbered requirement row in the PRD matrix.
- Must explicitly state the dual pricing and deployment posture ($9.99 BYOK/self-hosted vs $4.99/mo hosted).
- Must explicitly enumerate platform support across all 5 target operating systems.
