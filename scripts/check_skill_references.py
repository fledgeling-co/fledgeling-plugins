#!/usr/bin/env python3
"""Check active skill references against manifests, without rewriting evidence.

This is a conservative source check, not proof that a runner loaded a skill.
External references remain unresolved unless an external marketplace is supplied.
"""

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote


HISTORY_DIRS = {"evals", "eval-runs", "runs", "old", "predecessor", "docs", "node_modules"}
HISTORY_FILES = {"CHANGELOG.md", "EVALS.md", "evidence.md", "gemini-corpus.md", "case-study-paired.md"}
RETIRED = {"create-test-suite": "test-campaign:test-campaign", "compaction-quality": "braindump:braindump"}
TOKEN = r"[a-z][a-z0-9-]*"
# Artifact marker namespaces and bundled CLI commands are not plugin referrals.
MARKERS = {"mac-craft:metrics", "mac-craft:quota", "ledger:inference", "ledger:kind", "ledger:limits", "ledger:readings", "ledger:sources", "ledger:unsourced"}
STANDALONE = {"verify", "skill-creator", "dataviz", "claude-api", "debug", "review", "update-config", "artifact-capabilities"}
# Frontmatter settings describe skills; they are not skill identifiers.
NON_SKILL_TERMS = {"disable-model-invocation"}
# Exact, reviewed source excerpts. Keep their original identifiers as evidence.
# A substring exemption applies to this one line, never the rest of the file.
HISTORICAL_EXCERPTS = {
    "plugins/geminify/skills/geminify/gemini.md": ["unloadable names: 1 (create-test-suite:create-test-suite)"],
    "plugins/geminify/skills/geminify/SKILL.md": ["failure later: `create-test-suite:create-test-suite` returned `Unknown skill`"],
    "plugins/tailings/skills/tailings/SKILL.md": ["A user named `/proctor` four times"],
    "plugins/tailings/skills/tailings/references/probes.md": ["`/proctor` asked for four times; `ToolSearch` returned no match"],
    "plugins/code-review/README.md": ["adapted from the built-in `code-review` skill in the Claude Code CLI"],
    "plugins/create-mac-icon/skills/create-mac-icon/references/corpus/SYNTHESIS.md": ["in the sibling `mac-design-studio` skill (diolog-plugins)"],
    "plugins/vouch/skills/vouch/gemini.md": ["*Route to `design-review` for the deterministic gates*, and `gates.md`:99 repeats it."],
    "plugins/better-loop/README.md": ["run `/code-review` every hour"],
    "plugins/better-goal/skills/better-goal/references/failure-modes.md": ["**Evidence:** `/workflow-resume` typed five times consecutively"],
    "plugins/shipyard/skills/design/gemini.md": ["*every design decision goes through `design-craft` with `ux-craft`'s lens*; **neither** was invoked"],
    "plugins/shipyard/skills/gap-fix/gemini.md": ["decision goes through `design-craft` with `ux-craft`'s lens* and **neither** skill was invoked"],
    "plugins/mac-doctor/skills/mac-doctor/SKILL.md": ["absorbed from the former `process-hygiene` skill"],
    "plugins/mac-doctor/skills/mac-doctor/references/processes.md": ["former `process-hygiene` skill"],
    "plugins/trawl/skills/trawl/SKILL.md": ["supersedes the original `adhd` skill"],
    "plugins/braindump/scripts/score_retention.py": ["verbatim keyed as `<command-message>goal-harness:goal-harness</command-message>`"],
    "plugins/visualization/skills/visualization/references/onboarding.md": [
        "e.g. a `brand-design` or `ui-kit` skill",  # User-supplied illustrative names.
        "Onboard diagram-design from my `acme-design` skill",
    ],
    "plugins/shipyard/skills/intake/gemini.md": ["On `COD Dossier`, a skill said *every design decision goes through `design-craft`"],
}
QUALIFIED = re.compile(rf"(?<![\w/:.-])({TOKEN}(?::{TOKEN}){{1,2}})(?![\w/.-])")
INLINE = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")
DIRECT_CALL = re.compile(r"\bSkill\s*\(\s*(?:\{\s*skill\s*:\s*)?[\"']([^\"'\n]*)[\"'](?!\s*\+)")
JSON_CALL = re.compile(r"[\"']skill[\"']\s*:\s*[\"']([^\"'\n]*)[\"'](?!\s*\+)")
ACTION = re.compile(r"\b(?:invoke|invoking|use|using|load|run|running|call|via|through|route to|hand off to|follow)\s+(?:the\s+)?$", re.I)


def catalogue(root):
    manifest = root / ".claude-plugin/marketplace.json"
    entries = json.loads(manifest.read_text())["plugins"]
    skills, plugins, roots = {}, set(), []
    for entry in entries:
        directory = (root / entry["source"]).resolve()
        plugin = json.loads((directory / ".claude-plugin/plugin.json").read_text())
        if plugin["name"] != entry["name"]:
            raise ValueError(f"manifest name mismatch: {directory}")
        plugins.add(plugin["name"])
        paths = sorted(directory.glob("skills/*/SKILL.md"))
        if not paths and (directory / "SKILL.md").exists():
            paths = [directory / "SKILL.md"]
        if not paths:
            raise ValueError(f"no skills in registered plugin: {directory}")
        for path in paths:
            name = path.parent.name if path.parent != directory else plugin["name"]
            # Body examples can contain their own `name:` lines. Only metadata
            # inside the first frontmatter block declares the skill's name.
            source = path.read_text()
            frontmatter = re.match(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", source, re.S)
            declared = re.search(r"^name:[ \t]*(.+)$", frontmatter.group(1), re.M) if frontmatter else None
            if declared:
                scalar = re.fullmatch(r"(?:\"([^\"]+)\"|'([^']+)'|([^\s#]+))[ \t]*(?:#.*)?", declared.group(1).strip())
                declared_name = next((value for value in scalar.groups() if value is not None), None) if scalar else None
                if declared_name != name:
                    raise ValueError(f"skill name differs from directory: {path}")
            skills[f"{plugin['name']}:{name}"] = path
        roots.append(directory)
    return skills, plugins, roots


def active_files(roots):
    files = set()
    for root in roots:
        for path in root.rglob("*"):
            relative = path.relative_to(root)
            if not path.is_file() or path.suffix not in {".md", ".py", ".sh", ".mjs", ".js", ".ts", ".tmpl"}:
                continue
            if set(relative.parts) & HISTORY_DIRS or path.name in HISTORY_FILES:
                continue
            # Only installable instructions, executable prompts and the usage README.
            if relative.parts[0] not in {"skills", "references", "scripts", "agents", "commands", "templates"} and len(relative.parts) != 1:
                continue
            if path.name.startswith(("test_", "selftest")) or path.name.endswith(".test.mjs"):
                continue
            files.add(path)
    return sorted(files)


def references(text, names, historical_excerpts=()):
    """Yield (line, identifier, must_resolve) for explicit calls and prose cues.

    Ignore paths, frontmatter names, product headings and historical quotations.
    Unformatted prose is intentionally not exhaustively interpreted as tool calls.
    """
    seen = set()
    for number, line in enumerate(text.splitlines(), 1):
        if re.match(r"^name:", line):
            continue
        for excerpt in historical_excerpts:
            # Mask just the reviewed excerpt. An active call appended to the
            # same line must still be checked.
            line = line.replace(excerpt, " " * len(excerpt))
        # Mask only the exact names described as harness built-ins. Another
        # plugin invocation later on this line still requires qualification.
        line = re.sub(
            r"\b(?:bundled|built-in)\s+(?:`?/verify`?\s+and\s+)?`?/?(?:code-review|design)`?(?:\s+command)?(?![\w:-])",
            lambda match: " " * len(match.group(0)), line,
        )
        # Literal tool arguments must be exact IDs, including casing and the
        # absence of a leading slash. Do not infer runtime template values.
        candidates = [(m.group(1), True) for pattern in (DIRECT_CALL, JSON_CALL) for m in pattern.finditer(line)
                      if not any(char in m.group(1) for char in "<>{}$")]
        for match in QUALIFIED.finditer(line):
            identifier = match.group(1)
            # Namespaced skills contain hyphens or a known skill component;
            # omit ordinary key:value text and literal template placeholders.
            parts = identifier.split(":")
            skill_shaped = any(part in names for part in parts) or (len(parts) == 2 and parts[0] == parts[1] and "-" in parts[0])
            if identifier not in MARKERS | {"plugin:skill"} and skill_shaped:
                candidates.append((identifier, False))
        for match in INLINE.finditer(line):
            value = match.group(1)
            name = value.lstrip("/").split(" ")[0]
            before = re.sub(r"[*_]", "", line[:match.start()])
            after = line[match.end():]
            explicit_skill = re.match(r"(?:['’]s)?\s+skill\b", after)
            if name in STANDALONE | NON_SKILL_TERMS:
                continue
            # A quoted unknown skill explicitly labelled as a skill or used as
            # a namespaced action is still an identifier, even when no source
            # catalogue has ever contained it.
            shaped = re.fullmatch(rf"{TOKEN}(?::{TOKEN})*", name)
            if name in names and (value.startswith("/") or ACTION.search(before) or explicit_skill):
                candidates.append((name, True))
            elif shaped and (explicit_skill or (":" in name and ACTION.search(before))):
                candidates.append((name, True))
        # Unquoted /plugin-skill in runnable examples, not filesystem paths.
        for match in re.finditer(rf"(?<![\w./:<])\/({TOKEN}(?::{TOKEN})*)(?![\w/:.*-])", line):
            # XML closing tags and the Windows tscon /dest option are data,
            # not slash-command referrals. Other qualified slash calls remain.
            if match.group(1) == "dest:console" and re.search(r"\btscon\s[^`\n]*$", line[:match.start()]):
                continue
            if (":" in match.group(1) or match.group(1) in names) and match.group(1) not in STANDALONE:
                candidates.append((match.group(1), True))
        for identifier, explicit in candidates:
            key = (number, identifier)
            if key not in seen and (explicit or ":" in identifier or identifier in names) and identifier not in STANDALONE | NON_SKILL_TERMS:
                seen.add(key)
                yield number, identifier, explicit


def audit(root, external_roots=()):
    root = root.resolve()
    local, plugins, roots = catalogue(root)
    known = dict(local)
    source_plugins = set(plugins)
    for external in external_roots:
        found, external_plugins, _ = catalogue(external)
        known.update(found)
        source_plugins.update(external_plugins)
    bare = {}
    for identifier in known:
        bare.setdefault(identifier.split(":")[-1], []).append(identifier)
    names = set(bare) | set(RETIRED)
    files = active_files(roots)
    findings, externals, external_locations = [], set(), {}
    for path in files:
        relative = str(path.relative_to(root))
        body = path.read_text(errors="replace")
        for line, identifier, explicit in references(body, names, HISTORICAL_EXCERPTS.get(relative, ())):
            code = None
            if not re.fullmatch(rf"{TOKEN}(?::{TOKEN})*", identifier):
                findings.append({"file": relative, "line": line, "identifier": identifier, "code": "invalid-skill-identifier", "detail": "pass the exact skill identifier to Skill; slash syntax is only for chat commands"})
                continue
            if identifier in known:
                if identifier not in local:
                    externals.add(identifier)
                    external_locations.setdefault(identifier, []).append({"file": relative, "line": line})
                continue
            parts = identifier.split(":")
            if parts[-1] in RETIRED:
                code, detail = "retired-skill", f"use {RETIRED[parts[-1]]} after checking the intended task"
            elif len(parts) == 1 and explicit:
                if identifier in bare:
                    code, detail = "bare-plugin-skill", "resolve to " + " or ".join(sorted(bare[identifier]))
                else:
                    code, detail = "unknown-skill", "no matching source skill; resolve the exact installed identifier"
            elif len(parts) > 2 or parts[0] in {"plugin", "fledgeling-plugins"}:
                code, detail = "invented-namespace", "use the owning plugin and skill directory names"
            elif len(parts) == 2 and parts[0] in source_plugins:
                code = "missing-local-skill" if parts[0] in plugins else "missing-external-skill"
                detail = "no such skill exists in this registered source plugin"
            elif len(parts) == 2:
                externals.add(identifier)
                external_locations.setdefault(identifier, []).append({"file": relative, "line": line})
            if code:
                findings.append({"file": str(path.relative_to(root)), "line": line, "identifier": identifier, "code": code, "detail": detail})
        if path.suffix == ".md":
            for number, line in enumerate(body.splitlines(), 1):
                for target in re.findall(r"\]\(([^)]+)\)", line):
                    target = target.split("#")[0].strip("<>")
                    if not target or re.match(r"\w+:|/|~|\$|\{", target) or any(c in target for c in "<>* "):
                        continue  # URLs, absolute/runtime paths and template placeholders.
                    if not (path.parent / unquote(target)).exists():
                        findings.append({"file": relative, "line": number, "identifier": target, "code": "broken-local-link", "detail": "relative Markdown target does not exist"})
    return {
        "plugins": len(plugins), "skills": len(local), "files_scanned": len(files),
        "inventory": [str(p.relative_to(root)) for p in files],
        "findings": findings,
        "external_references": [{"identifier": n, "source_resolved": n in known, "locations": external_locations.get(n, [])} for n in sorted(externals)],
        "limits": "Source resolution only; runtime installation and successful Skill tool results must be checked by the runner. Historical records, test fixtures and unformatted ambiguous prose are excluded.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--external-marketplace", type=Path, action="append", default=[])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = audit(args.root.resolve(), [p.resolve() for p in args.external_marketplace])
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for item in result["findings"]:
            print(f"{item['file']}:{item['line']}: {item['code']}: {item['identifier']}: {item['detail']}")
        unresolved = sum(not x["source_resolved"] for x in result["external_references"])
        print(f"Skill references: {result['skills']} skills, {result['files_scanned']} active files, {len(result['findings'])} errors; {unresolved} external references need runtime discovery.")
    return bool(result["findings"])


if __name__ == "__main__":
    raise SystemExit(main())
