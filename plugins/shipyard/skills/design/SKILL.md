---
name: design
description: >-
  Produce interactive design mocks for a triaged feature covering every surface, user flow,
  state, action, and menu — the design stage between triage and work, runnable in parallel with
  planning. Routes iPhone/iPad/Mac (and optional Windows) mocks through mac-design-studio with
  web mirroring the mac layout, consults the Mobbin MCP during ideation, judges open direction
  forks with a cross-family panel, then gates the mocks through design-review and be-my-witness
  and actions their findings before handing off. Use when a feature needs its UI designed
  ("design the mocks for DIO-0001", "run the design stage"), when the conductor reaches a
  user-facing feature, or when triage marked surfaces that don't exist yet. Produces a mock
  index + state matrix the planner's test strategy and the verifier consume. Skip only for
  features with no user-facing surface — and record that decision.
---

# Pipeline Design — mocks for every surface, state, and flow

Design the feature's UI before it is built, as interactive HTML mocks plus a **state matrix** —
the enumeration of surfaces × states that later becomes the worker's checklist and the test
suite's coverage bar. A feature whose UI is only half-represented here is a feature that ships
half-built later; the mock set is the contract, not an illustration.

Runs after triage (`To Do`), in parallel with `plan` when triage already named the surfaces.
Skip only when the feature has no user-facing surface, and write "design: not applicable
(<reason>)" into the spec/ticket so the skip is a decision, not an omission.

**Running as a Gemini model?** Read `gemini.md` in this directory first, then follow this file with the overrides it names. It routes the mock build and the aesthetic judgement to defer's lane picker before you start, turns the surface x state x platform matrix into a table filled before the first mock, and gives the Obscura capture, the HIG/Fluent metric table and the design-craft/ux-craft passes a denominator, a source tier and a file each phase reads. Other models skip it.

## Inputs

- A triaged id. Read the brief/spec/ticket and the whole thread per
  `${CLAUDE_PLUGIN_ROOT}/references/tracker-adapter.md` — triage's assumptions and any human
  answers are binding design constraints.
- The repo's design authority where one exists (DESIGN md, design system, tokens, existing mock
  index) — new mocks extend it; they never fork it.

## Procedure

1. **Inventory the surfaces.** From the brief + triage: every screen, panel, menu, overlay, and
   reusable part the feature touches, on every platform the brief names (**iPhone, iPad, Mac,
   Web always for app work; Windows when the brief includes it**). Then the state matrix per
   `${CLAUDE_PLUGIN_ROOT}/references/test-strategy.md` §state-matrix: each surface × default /
   loading / empty / error / success, plus permission and responsive variants where they apply.
   This inventory is the stage's coverage bar — a surface missing from it is invisible to every
   later stage.

2. **Ideate with references.** Consult the **Mobbin MCP** (`search_screens` / `search_flows`,
   platform-appropriate) for how shipped products handle each surface and flow — cite the
   screens that informed a direction. Run `design-craft` and `ux-craft` as the authoring pair.

3. **Settle the direction.** Where the direction is genuinely open (two structurally different
   layouts, a navigation model fork), build 2–3 **structurally different** candidates of the key
   surface (different layout and hierarchy, not colourways — three tweaked card grids is
   wallpaper, not a choice) and judge with a cross-family panel per
   `${CLAUDE_PLUGIN_ROOT}/references/second-opinion-lanes.md` §Panels. Record the verdict and the
   dissent as a design assumption. In an attended session the human outranks the panel — offer
   the candidates with the panel's recommendation marked.

4. **Build the mocks.**
   - **iPhone / iPad / Mac**: through the `mac-design-studio:mac-design-studio` skill — it owns native-correct
     idiom, the corpus, and the HIG routing. One mock set per platform; shared vocabulary,
     platform-correct chrome.
   - **Windows** (when in scope): start from the mac set's structure, then apply a Windows 11
     aesthetic (Fluent: Segoe UI Variable, mica/acrylic surfaces, Windows title-bar and control
     placement) as its own pass — never ship the mac chrome on Windows.
   - **Web**: mirrors the mac app's layout — same information architecture and hierarchy,
     web-native controls.
   - Mocks are interactive where the flow is the point (tabs, walkthrough states, menu open/
     close), and every cell of the state matrix renders — a mock that type-checks but renders
     blank has represented nothing. Verify by opening the rendered surfaces (Obscura), not by
     reading the source.

5. **Gate the mocks — and act on the findings.** Run `design-review` (deterministic gates +
   craft passes) and `be-my-witness` on the rendered set. Action every Critical/High finding and
   the Mediums that are cheap, then **one** re-review of the changed surfaces — a bounded loop,
   not review-until-quiet. be-my-witness is calibrated before trusting: it over-flags without
   tuning, so scope it to the surfaces and states in the matrix rather than every pixel it can
   reach. Record the review outcome (findings by severity, actioned/deferred) in the design
   section — an unactioned Critical does not hand off.

6. **Hand off.** Write the mock index (`design/mocks/<id>/INDEX.md` or the repo's own
   convention): every mock path, the state matrix with each cell's mock reference, the panel
   verdicts and design assumptions, the review outcome. Reference it from the spec/ticket
   (path + committed sha, per the tracker adapter). The planner reads the matrix into the test
   strategy; the worker builds to the mocks; the verifier measures against them.

## Rules

- **The matrix is the bar.** Every surface × state cell is mocked, or explicitly waived with a
  reason in the index. An unwaived empty cell blocks handoff.
- **Decisions defer like everywhere else**: taste that survives the second-opinion gate goes to
  the human (attended) or becomes a marked assumption with the panel's verdict (unattended);
  everything else is settled by evidence, the design system, or the panel.
- **Executor lanes never do design** (`references/executor-lanes.md`) — design leaf work runs on
  mid-tier Claude subagents; direction stays on the strongest model.
- **Design tokens and shared base elements are read-only** from this stage — a feature mock that
  edits the design system breaks every sibling; propose token changes as their own item.
- Keep the index to rows and paths — it is a resumable state file, not an essay.
