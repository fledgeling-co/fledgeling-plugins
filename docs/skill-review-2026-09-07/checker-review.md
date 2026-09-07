# Independent source-checker and catalogue referral review

Reviewed `scripts/check_skill_references.py`, `scripts/test_skill_references.py`, `site/scripts/skill-identifiers.mjs`, `site/scripts/skill-identifiers.test.mjs`, and their integration in `site/scripts/build-catalogue.mjs`. Changed the first four only; the catalogue integration already correctly delegates display-link owner extraction and preserves the original boundary text.

## Corrections

- Check explicit unknown bare Skill arguments instead of silently dropping them; distinguish literal arguments from runtime variables and templates. Reject malformed literal identifiers (leading slash, uppercase, embedded arguments) rather than normalizing them into valid calls.
- Preserve unknown qualified slash references, their locations, and source-resolution status. A missing subskill in a supplied external plugin source is an error; an unavailable external source remains explicitly unresolved.
- Parse declared skill names only from initial YAML frontmatter, accepting simple quoted names and trailing YAML comments. Body `name:` examples cannot change declared identity.
- Include generated `.tmpl` instructions in the active scan.
- Mask reviewed historical excerpts and built-in command descriptions only at their exact spans, so an active call later on the same line stays visible. Narrowed one overly broad historical synthesis exemption; kept deliberate illustrative placeholder and historical identifiers unchanged.
- Exclude XML closing tags and the Windows `tscon /dest:console` option in their actual non-skill contexts, without suppressing unknown plugin references generally.
- Add regression coverage for CLI exit codes: findings fail; clean source references pass; unresolved external sources are visible with explicit source-only limits.
- Catalogue referral extraction now handles slash commands inside backticks and coordinated alternatives, maps subskills to the owning plugin page, and avoids partial triple namespaces, paths, invented prefixes and hyphenated English false positives. Repeated calls do not leak regex state.

## Validation

- `python3 -m unittest discover -s scripts -p test_skill_references.py`: 21 tests passed.
- `node --test site/scripts/skill-identifiers.test.mjs`: 7 tests passed.
- Actual source audit with `/Users/lukerhodes/Dev/diolog-plugins` as external marketplace exited 0: 55 plugins, 71 skills, 1,017 active files, zero findings, zero unresolved external references, 19 distinct external references resolved from supplied source.
- Exact audit output: `/tmp/skill-review-independent-root-audit.json`.
- Parent reports final full catalogue validation passed. No catalogue build or runtime-model execution was repeated by this independent review after the final parser-only corrections.

## Evidence boundary

The checker remains a conservative source gate, not a full Markdown/program parser and not runtime proof. Historical records and tests are intentionally excluded; unformatted ambiguous prose is not exhaustively interpreted as calls. A source-resolved external dependency does not prove installation, successful Skill invocation, runtime selector availability, model identity, or behavioural quality. Each runner still needs the concrete runtime receipt required by the revised skill contracts.
