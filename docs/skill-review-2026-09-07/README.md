# Skill and reference review — 7 September 2026

Reviewed all 71 registered skill entry points across 55 plugins, their active
instruction/reference inventory and generated runner templates. Updated 54 plugins;
`should-compact:should-compact` was reviewed and needed no change. Each changed
plugin has a synchronized patch version in both manifests and its README badge
where present. This report records source review and validation; repository
publication and installed-runtime loading are separate evidence states.

The review combined catalogue-wide scans with detailed reads of affected workflows.
The inventories in [authoring.md](authoring.md), [craft.md](craft.md) and
[workflow.md](workflow.md) record each review track. Historical research, benchmark
outputs, source quotations and earlier changelog entries remain historical evidence.
The review did not execute every skill.

## Sources and interpretation

The supplied [migration index](https://platform.claude.com/docs/en/about-claude/models/migration-guide.md)
now links to model-specific migrations, so the review also used
[Migrating to Opus 5](https://platform.claude.com/docs/en/models/opus-5/migration-guide.md).
Prompt changes use the current [Claude prompting guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md)
and [Opus 5 guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5.md).
The trailing `$` in the supplied documentation-home URL was treated as punctuation;
the source was the [Claude documentation home](https://platform.claude.com/docs).
These sources were retrieved on 7 September 2026.

The supplied skill-naming incident report was a diagnostic lead. Its transcript
counts were not independently reproduced. [Claude Code's skill documentation](https://code.claude.com/docs/en/skills)
confirms the important distinction: plugin skills have namespaces, while personal,
project and bundled skills can have bare identifiers. The edits preserve that
distinction, along with real paths, CLI commands and schema values.

## Changes that affect execution

- **Exact references.** Prospective referrals now use actual plugin/skill IDs.
  Geminify's resolver no longer discards an invalid namespace and reports the
  remaining bare name as resolved. Source discovery is explicitly separate from
  successful loading in a running session. The site catalogue recognizes qualified
  referrals while linking to the correct plugin page.
- **Current model roles.** Opus 5 handles intake, triage and planning; Gemini 3.8
  implements after those artifacts; GPT-6 coordinates. These are the owner's
  preferences, with task-specific choices taking precedence. Runners discover exact
  supported selectors and parameter schemas instead of inventing model IDs.
- **Complete handoffs.** Packets carry source revisions, decisions, scope, writable
  paths, exact dependencies, deliverables, acceptance evidence and stop conditions.
  Independent work can run concurrently; dependent stages and shared writes remain
  sequenced. Fleet examples now respect zero capacity and consistent fallback caps.
- **Bounded checking.** Generic repeated self-checks and automatic extra review
  rounds were removed. Required tests, visual comparisons, independent acceptance
  and evidence tied to requirements remain. Same-family repetition cannot manufacture
  independence, and empty output cannot satisfy a gate.
- **Calibrated model guidance.** Older Gemini observations no longer establish
  Gemini 3.8 limitations or routing penalties. Opus guidance separates API migration
  settings from CLI prompts, scopes local environment incidents, and correctly
  describes tool permissions.
- **Product truth.** Launch Craft no longer injects a particular product's audience,
  pricing or platform support into every project. Its inventory helper and source
  checker now describe what they actually do; rendered acceptance remains required.
- **Bundled utilities.** Visualization diagnostics, imports and exports now enter
  through the actual installed skill and use its bundled files. Removed nonexistent
  predecessor commands and maintainer checks, preserved the existing profile
  storage format, and repaired the polar checker's default asset path.
- **Necessary questions.** Clarify lets routine authorized decisions proceed and
  uses a second opinion for material unresolved technical ambiguity. User preferences
  and missing authorization remain decisions for the user.

Independent review also found and repaired stale consumers of the new contracts:
child-plan path formatting, forced Claude fallbacks, fixed reviewer selectors,
extra adversarial-round requirements and the old eight-runner fallback.

The follow-up review before publication also reconciled the worker frontmatter's
fallback policy with its body, removed a residual Obscura-only referral, and
revised UX calibration interpretations that generalized from dated, small-sample
observations. The original measured results and source quotations remain intact.
These findings show the limits of automated reference checks: they do not certify
instruction consistency or the effectiveness of every skill.

## Reproduce the source checks

Run these from the repository root:

```bash
python3 scripts/check_skill_references.py
python3 -m unittest discover -s scripts -p test_skill_references.py
python3 -m unittest discover -s plugins/geminify/skills/geminify/scripts -p test_session_calibrate.py
node --test site/scripts/skill-identifiers.test.mjs
node site/scripts/build-catalogue.mjs
git diff --check
```

For external source resolution, add
`--external-marketplace /path/to/diolog-plugins` to the reference checker.
Its JSON output includes the scan inventory and unresolved external references;
external installation still requires runtime discovery. The checker is conservative
about natural-language references and does not certify every remote URL or tool API.

See [validation.json](validation.json) for final executed checks and
[source-audit.json](source-audit.json) for the final reference inventory.
[versions.json](versions.json) records the 54 version changes.

The final inventory covers 1,017 active files: zero source findings and zero
unresolved external names when checked against both source marketplaces. Nineteen
external references resolve in source; this does not prove installation. All 34
regression cases passed (21 reference-checker, six Geminify resolver and seven
catalogue-referral cases), along with the catalogue build, modified script syntax
and diff-format checks. Additional scoped craft checks and their limitations are
recorded in the detailed reports.

## What remains unmeasured

No comparative Opus 5, Gemini 3.8 or GPT-6 skill runs were executed. Existing
benchmarks do not establish the effectiveness of these prompt revisions. The
legacy Defer executable registry retains its calibrated Gemini 3.7/GPT-5.6 lanes;
the documented current-model path uses runtime discovery and native dispatch.
The icon loop runner remains Claude-specific. Remote tools and browser portability
were not validated in a live campaign. No plugin cache was reloaded or site
deployment verified as part of the review. Consult the repository history for
publication of these source changes; a pushed commit does not prove runtime loading.
