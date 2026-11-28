#!/usr/bin/env python3
"""changelog.py: create, check and timestamp a project's CHANGELOG.html.

Subcommands
  path   [--repo DIR]                     print where the page lives (the main checkout's root)
  init   [--repo DIR] [--project NAME]    create the page from the template if it is missing
  stamp                                   print the current Sydney time in the two forms an entry uses
  check  FILE [--allow-empty]             check the page's structure; exit 0 only when it holds
  self-test                               prove every check can fire, against the bundled example

Exit codes: 0 ok, 1 check failed, 2 usage or environment error.
Standard library only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
TEMPLATE = ASSETS / "changelog-template.html"
EXAMPLE = ASSETS / "example-changelog.html"
MARKER = "<!-- changelog:entries"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
FACETS = ["Task", "Achieved", "Remaining"]
NOTHING = "Nothing remaining."
MAX_BULLETS = 4
MAX_BULLET_WORDS = 14
PLACEHOLDERS = ["YYYY-MM-DD", "D Month YYYY", "D Mon YYYY", "PASTE THE EXPORTED SVG", "The outcome, in ten words or fewer", "{{PROJECT}}"]


# ---------------------------------------------------------------- a small DOM

class Node:
    __slots__ = ("tag", "attrs", "children", "parent", "line")

    def __init__(self, tag, attrs=None, parent=None, line=0):
        self.tag, self.attrs, self.children, self.parent, self.line = tag, dict(attrs or {}), [], parent, line

    def classes(self):
        return set((self.attrs.get("class") or "").split())

    def text(self):
        out = []
        for c in self.children:
            out.append(c if isinstance(c, str) else c.text())
        return "".join(out)

    def iter(self):
        for c in self.children:
            if isinstance(c, Node):
                yield c
                yield from c.iter()

    def find_all(self, tag=None, cls=None):
        return [n for n in self.iter() if (tag is None or n.tag == tag) and (cls is None or cls in n.classes())]

    def find(self, tag=None, cls=None):
        found = self.find_all(tag, cls)
        return found[0] if found else None

    def kids(self, tag=None, cls=None):
        return [c for c in self.children if isinstance(c, Node) and (tag is None or c.tag == tag) and (cls is None or cls in c.classes())]


class Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root")
        self.cur = self.root
        self.marker_seen = False
        self.marker_line = None

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.cur, self.getpos()[0])
        node.attrs["__after_marker"] = self.marker_seen
        self.cur.children.append(node)
        if tag not in VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        node = Node(tag, attrs, self.cur, self.getpos()[0])
        node.attrs["__after_marker"] = self.marker_seen
        self.cur.children.append(node)

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(data)

    def handle_comment(self, data):
        if data.strip().startswith("changelog:entries"):
            self.marker_seen = True
            self.marker_line = self.getpos()[0]


def parse(text):
    b = Builder()
    b.feed(text)
    b.close()
    return b


# ---------------------------------------------------------------- helpers

def squash(s):
    return re.sub(r"\s+", " ", s or "").strip()


def words(s):
    return [w for w in re.split(r"\s+", squash(s)) if re.search(r"\w", w)]


def sentences(s):
    s = squash(s)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", s)
    return [p for p in parts if p]


ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ISO_STAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?[+-]\d{2}:\d{2}$")
ENTRY_ID = re.compile(r"^(\d{4}-\d{2}-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*$")
JARGON = [
    (re.compile(r"\b[A-Z][A-Z0-9]{1,9}-\d{1,6}\b"), "a ticket number"),
    (re.compile(r"(?<![\w/])#\d{2,6}\b"), "a pull-request number"),
    (re.compile(r"\b[0-9a-f]{7,40}\b"), "a commit hash"),
    (re.compile(r"(?:^|\s)(?:\.{0,2}/)?[\w.-]+/[\w./-]*\.\w{1,5}\b"), "a file path"),
    (re.compile(r"(?:^|\s)--[a-z][\w-]+"), "a command-line flag"),
]


def main_checkout(repo: Path) -> Path:
    """The main checkout's root, even when called from inside a worktree."""
    try:
        common = subprocess.run(["git", "-C", str(repo), "rev-parse", "--path-format=absolute", "--git-common-dir"],
                                capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return repo.resolve()
    common_path = Path(common)
    if common_path.name == ".git":
        return common_path.parent.resolve()
    # A bare repository or an unusual layout: fall back to the working tree's own top level.
    top = subprocess.run(["git", "-C", str(repo), "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return Path(top.stdout.strip() or repo).resolve()


# ---------------------------------------------------------------- the checks

def check_text(text, allow_empty=False):
    """Return (errors, warnings, examined) for one page's source."""
    errors, warnings = [], []
    b = parse(text)
    root = b.root

    if MARKER not in text:
        errors.append("page: the `<!-- changelog:entries` marker is missing, so nobody can tell where a new entry goes")
    if not root.find("template"):
        errors.append("page: the `<template id=\"entry-template\">` block is missing; restore it from the skill's template")
    entries_box = next((n for n in root.iter() if n.tag == "div" and "entries" in n.classes()), None)
    if entries_box is None:
        errors.append("page: no `<div class=\"entries\">`; this is not a page built from the changelog template")
        return errors, warnings, 0

    articles = [a for a in root.find_all("article") if "entry" in a.classes() and not any(p.tag == "template" for p in ancestors(a))]
    if not articles and not allow_empty:
        errors.append("page: 0 entries examined. A page with no entries passes only with --allow-empty (straight after init)")

    seen_ids = {}
    dates = []
    for a in articles:
        where = f"entry {a.attrs.get('id') or '(no id)'} (line {a.line})"
        if a.parent is not entries_box:
            errors.append(f"{where}: sits outside `<div class=\"entries\">`, so the contents list and the view switch miss it")
        if not a.attrs.get("__after_marker"):
            errors.append(f"{where}: sits above the changelog:entries marker; new entries go directly below it")
        eid = a.attrs.get("id", "")
        m = ENTRY_ID.match(eid)
        if not m:
            errors.append(f"{where}: id must be YYYY-MM-DD-<slug> in lower case, got {eid!r}")
        if eid in seen_ids:
            errors.append(f"{where}: id duplicates the entry at line {seen_ids[eid]}")
        seen_ids[eid] = a.line
        id_date = m.group(1) if m else None
        if id_date:
            dates.append((id_date, eid))
        rem = a.attrs.get("data-remaining")
        if rem not in ("open", "none"):
            errors.append(f"{where}: data-remaining must be \"open\" or \"none\", got {rem!r}")

        head = a.find("header", "entry-head")
        if head is None:
            errors.append(f"{where}: no `<header class=\"entry-head\">`")
            continue
        date_p = head.find("p", "entry-date")
        date_t = date_p.find("time") if date_p else None
        if date_t is None or not ISO_DATE.match(date_t.attrs.get("datetime", "")):
            errors.append(f"{where}: the date line needs `<time datetime=\"YYYY-MM-DD\">`")
        elif id_date and date_t.attrs["datetime"] != id_date:
            errors.append(f"{where}: date line says {date_t.attrs['datetime']} but the id says {id_date}; both are the day the entry was first written")
        h2 = head.find("h2")
        if h2 is None:
            errors.append(f"{where}: no title `<h2>`")
        else:
            link = h2.find("a")
            if link is None or link.attrs.get("href") != f"#{eid}":
                errors.append(f"{where}: the title should link to its own entry, `<a href=\"#{eid}\">`")
            n = len(words(h2.text()))
            if n == 0:
                errors.append(f"{where}: the title is empty")
            elif n > 10:
                errors.append(f"{where}: the title runs {n} words; the limit is 10, one line")
        sub = head.find("p", "subtitle")
        if sub is None:
            errors.append(f"{where}: no `<p class=\"subtitle\">`")
        else:
            ss = sentences(sub.text())
            if len(ss) != 2:
                errors.append(f"{where}: the subtitle has {len(ss)} sentence(s); it takes exactly 2 (what was achieved, what it means)")
            for i, s in enumerate(ss, 1):
                if len(words(s)) > 25:
                    errors.append(f"{where}: subtitle sentence {i} runs {len(words(s))} words; the limit is 25")
        stamps = head.find("p", "stamps")
        times = stamps.find_all("time") if stamps else []
        if stamps is None or not squash(stamps.text()).startswith("Written"):
            errors.append(f"{where}: the timestamp line must start with \"Written\"")
        if not times:
            errors.append(f"{where}: the timestamp line has no `<time>` elements")
        bad = [t.attrs.get("datetime", "") for t in times if not ISO_STAMP.match(t.attrs.get("datetime", ""))]
        if bad:
            errors.append(f"{where}: timestamp datetime values need a time and a UTC offset (2026-11-27T14:05+11:00), got {bad}")
        if len(times) > 1:
            if "last updated" not in squash(stamps.text()):
                errors.append(f"{where}: an updated entry's timestamp line ends \"· last updated <time>\"")
            vals = [t.attrs.get("datetime", "") for t in times]
            try:
                parsed = [dt.datetime.fromisoformat(v) for v in vals]
                if parsed[-1] != max(parsed):
                    errors.append(f"{where}: \"last updated\" is not the latest time on the line")
                if parsed[0] != min(parsed):
                    errors.append(f"{where}: \"Written\" is not the earliest time on the line")
            except ValueError:
                pass

        box = a.kids("div", "facets")
        if len(box) != 1:
            errors.append(f"{where}: needs one `<div class=\"facets\">` holding Task, Achieved and Remaining, found {len(box)}")
        facets = box[0].kids("section", "facet") if box else []
        labels = [squash(f.find("h3").text()) if f.find("h3") else "" for f in facets]
        if labels != FACETS:
            errors.append(f"{where}: needs exactly three facets in order Task, Achieved, Remaining; found {labels}")
        for f, label in zip(facets, labels):
            for kind in ("plain", "technical"):
                divs = f.kids("div", kind)
                if len(divs) != 1:
                    errors.append(f"{where} {label}: needs one `<div class=\"{kind}\">`, found {len(divs)}")
                    continue
                body = squash(divs[0].text())
                if not body:
                    errors.append(f"{where} {label}: the {kind} version is empty")
                # Each version is a short bullet list, so the page reads at a glance.
                lists = divs[0].kids("ul")
                stray = [c for c in divs[0].kids() if c.tag != "ul"]
                loose = squash("".join(c for c in divs[0].children if isinstance(c, str)))
                if len(lists) != 1 or stray or loose:
                    errors.append(f"{where} {label}: the {kind} version must be one `<ul>` of short bullets and nothing else")
                else:
                    items = lists[0].kids("li")
                    if not 1 <= len(items) <= MAX_BULLETS:
                        errors.append(f"{where} {label}: the {kind} version has {len(items)} bullets; use 1 to {MAX_BULLETS}")
                    for n, li in enumerate(items, 1):
                        w = len(words(li.text()))
                        if w > MAX_BULLET_WORDS:
                            errors.append(f"{where} {label}: {kind} bullet {n} runs {w} words; the limit is {MAX_BULLET_WORDS}")
                if kind == "plain":
                    if divs[0].find("code") or divs[0].find("pre"):
                        errors.append(f"{where} {label}: the plain version contains code; that belongs in the technical version")
                    for rx, what in JARGON:
                        hit = rx.search(body)
                        if hit:
                            errors.append(f"{where} {label}: the plain version contains {what} ({hit.group(0).strip()!r}); keep it in the technical version")
                            break
            if label == "Remaining":
                texts = {k: squash(f.kids("div", k)[0].text()) for k in ("plain", "technical") if f.kids("div", k)}
                says_nothing = [k for k, v in texts.items() if v == NOTHING]
                if rem == "none" and len(says_nothing) != 2:
                    errors.append(f"{where}: data-remaining=\"none\" needs \"{NOTHING}\" in both versions of Remaining")
                if rem == "open" and says_nothing:
                    errors.append(f"{where}: data-remaining=\"open\" but Remaining says \"{NOTHING}\"; set data-remaining=\"none\" or list what is left")
        for fig in a.find_all("figure"):
            if fig.parent is not a:
                warnings.append(f"{where}: a figure sits inside a column; put it directly in the article, after the facets, so it spans the full width")
            if "visual" not in fig.classes():
                warnings.append(f"{where}: a `<figure>` without class=\"visual\" will not get the light plate in dark mode")
            svg = fig.find("svg")
            if svg is not None and svg.find("title") is None:
                warnings.append(f"{where}: an inline SVG has no `<title>`; re-export it from visualization:visualization")
        raw = a_source(text, a)
        for ph in PLACEHOLDERS:
            if ph in raw:
                errors.append(f"{where}: template placeholder text left in: {ph!r}")

    # Every id on the page must be unique: two inline SVGs sharing a marker or gradient id resolve to
    # one another's, and a repeated entry id breaks its link. Ids inside <template> are inert and skipped.
    seen = {}
    for n in root.iter():
        i = n.attrs.get("id")
        if not i or any(p.tag == "template" for p in ancestors(n)):
            continue
        if i in seen:
            errors.append(f"page: id {i!r} appears twice (lines {seen[i]} and {n.line}); "
                          "re-export a figure with the visualization skill's prefixed ids, or rename the entry")
        else:
            seen[i] = n.line

    ordered = [d for d, _ in dates]
    if ordered != sorted(ordered, reverse=True):
        errors.append("page: entries are not newest first by the day they were written: " + ", ".join(e for _, e in dates))
    for ph in ["{{PROJECT}}"]:
        if ph in text:
            errors.append("page: {{PROJECT}} was never replaced; run `changelog.py init --project NAME`")
    return errors, warnings, len(articles)


def ancestors(n):
    p = n.parent
    while p is not None:
        yield p
        p = p.parent


def a_source(text, article):
    """The article's source lines, for placeholder checks. Approximate but bounded to the entry."""
    lines = text.splitlines()
    start = article.line - 1
    end = start
    depth = 0
    for i in range(start, len(lines)):
        depth += lines[i].count("<article") - lines[i].count("</article>")
        end = i
        if depth <= 0 and i > start or (depth <= 0 and "</article>" in lines[i]):
            break
    return "\n".join(lines[start:end + 1])


# ---------------------------------------------------------------- commands

def cmd_path(args):
    print(main_checkout(Path(args.repo)) / "CHANGELOG.html")
    return 0


def cmd_init(args):
    root = main_checkout(Path(args.repo))
    target = root / "CHANGELOG.html"
    if target.exists():
        print(f"exists {target}")
        return 0
    project = args.project or root.name
    text = TEMPLATE.read_text(encoding="utf-8").replace("{{PROJECT}}", html.escape(project))
    target.write_text(text, encoding="utf-8")
    print(f"created {target}")
    return 0


def cmd_stamp(_args):
    try:
        from zoneinfo import ZoneInfo
        now = dt.datetime.now(ZoneInfo("Australia/Sydney"))
    except Exception as exc:  # zoneinfo data missing is an environment fault, not a reason to guess the offset
        print(f"cannot resolve Australia/Sydney: {exc}", file=sys.stderr)
        return 2
    off = now.strftime("%z")
    iso = now.strftime("%Y-%m-%dT%H:%M") + f"{off[:3]}:{off[3:]}"
    print(f"datetime   {iso}")
    print(f"date       {now.strftime('%Y-%m-%d')}")
    print(f"long date  {now.day} {now.strftime('%B %Y')}")
    print(f"written    {now.day} {now.strftime('%b %Y %H:%M')}")
    print(f"updated    {now.day} {now.strftime('%b %H:%M')}")
    return 0


def cmd_check(args):
    path = Path(args.file)
    if not path.is_file():
        print(f"no such file: {path}", file=sys.stderr)
        return 2
    errors, warnings, n = check_text(path.read_text(encoding="utf-8"), allow_empty=args.allow_empty)
    for e in errors:
        print(f"FAIL  {e}")
    for w in warnings:
        print(f"warn  {w}")
    print(f"changelog check: examined={n} entries · {len(errors)} failure(s) · {len(warnings)} warning(s)")
    print("not checked: whether the words are true, whether the plain version is plain beyond the patterns above, "
          "and whether the page renders; open it in Chrome to see it")
    return 1 if errors else 0


def cmd_self_test(_args):
    good = EXAMPLE.read_text(encoding="utf-8")
    errors, _, n = check_text(good)
    if errors or n == 0:
        print("self-test: the bundled example does not pass, so nothing below means anything:")
        for e in errors:
            print("  " + e)
        return 1
    first = good.index('<article class="entry"')
    mutations = [
        ("three-sentence subtitle", lambda t: t.replace("restarts; they wait in a queue and retry for up to a day.", "restarts. They wait in a queue. They retry for up to a day.", 1), "sentence(s)"),
        ("eleven-word title", lambda t: t.replace(">Failed deliveries now retry after a server restart<", ">Failed webhook deliveries now retry automatically after every single server restart<", 1), "the limit is 10"),
        ("code in the plain version", lambda t: t.replace("<li>Stop losing webhooks when the relay restarts</li>", "<li><code>x</code> Stop losing webhooks</li>", 1), "contains code"),
        ("ticket number in the plain version", lambda t: t.replace("<li>Stop losing webhooks when the relay restarts</li>", "<li>RELAY-212: stop losing webhooks</li>", 1), "ticket number"),
        ("open entry saying nothing remains", lambda t: t.replace("<ul><li>Prove it holds at peak traffic</li><li>Switch it on for customers: needs your go-ahead</li></ul>", "<ul><li>" + NOTHING + "</li></ul>", 1), "data-remaining=\"open\""),
        ("missing facet", lambda t: t.replace("<h3>Task</h3>", "<h3>Goal</h3>", 1), "Task, Achieved, Remaining"),
        ("oldest entry first", lambda t: t.replace('id="2026-11-24-signing-keys-rotate"', 'id="2026-11-29-signing-keys-rotate"', 1).replace('<time datetime="2026-11-24">', '<time datetime="2026-11-29">', 1).replace('href="#2026-11-24-signing-keys-rotate"', 'href="#2026-11-29-signing-keys-rotate"', 1), "newest first"),
        ("timestamp without an offset", lambda t: t.replace('datetime="2026-11-24T11:20+11:00"', 'datetime="2026-11-24T11:20"', 1), "UTC offset"),
        ("update without last updated", lambda t: t.replace(" · last updated <time", " · <time", 1), "last updated"),
        ("placeholder left in", lambda t: t.replace("Customers can now replace the secret", "D Month YYYY Customers can now replace the secret", 1), "placeholder"),
        ("duplicate SVG id", lambda t: t.replace('id="ex-retry-desc"', 'id="ex-retry-title"', 1), "appears twice"),
        ("entry above the marker", _move_marker_below_first, "above the changelog:entries marker"),
        ("bad id", lambda t: t.replace('id="2026-11-24-signing-keys-rotate"', 'id="Signing Keys"', 1), "id must be"),
        ("no entries", lambda t: _strip_entries(t), "0 entries examined"),
        ("a paragraph instead of bullets", lambda t: t.replace('<div class="plain"><ul><li>Stop losing webhooks when the relay restarts</li></ul></div>', '<div class="plain"><p>Stop losing webhooks when the relay restarts.</p></div>', 1), "one `<ul>` of short bullets"),
        ("a fifteen-word bullet", lambda t: t.replace("<li>Prove it holds at peak traffic</li>", "<li>Prove that it holds up properly at peak traffic on the busiest day of the whole year</li>", 1), "the limit is 14"),
        ("five bullets", lambda t: t.replace("<li>Any failure opens to show why</li>", "<li>a</li><li>b</li><li>c</li><li>d</li>", 1), "use 1 to 4"),
    ]
    failed = 0
    fresh = TEMPLATE.read_text(encoding="utf-8").replace("{{PROJECT}}", "self-test")
    e0, _, _ = check_text(fresh, allow_empty=True)
    if e0:
        print("  BROKEN   a freshly initialised page fails --allow-empty: " + "; ".join(e0))
        failed += 1
    else:
        print("  passes   a freshly initialised page, with --allow-empty")
    for name, mutate, expect in mutations:
        bad = mutate(good)
        if bad == good:
            print(f"  FIXTURE  {name}: the mutation changed nothing, so the check was never exercised")
            failed += 1
            continue
        errs, _, _ = check_text(bad)
        if any(expect in e for e in errs):
            print(f"  fires    {name}")
        else:
            print(f"  SILENT   {name}: expected a failure containing {expect!r}, got {errs or 'none'}")
            failed += 1
    print(f"self-test: {len(mutations) - failed} of {len(mutations)} checks fired; bundled example passes with {n} entries")
    return 1 if failed else 0


def _move_marker_below_first(t):
    i = t.index(MARKER)
    j = t.index("-->", i) + 3
    marker = t[i:j]
    t = t[:i] + t[j:]
    k = t.index("</article>") + len("</article>")
    return t[:k] + "\n" + marker + t[k:]


def _strip_entries(t):
    return re.sub(r"\s*<article class=\"entry\".*?</article>", "", t, flags=re.S)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("path"); s.add_argument("--repo", default="."); s.set_defaults(fn=cmd_path)
    s = sub.add_parser("init"); s.add_argument("--repo", default="."); s.add_argument("--project"); s.set_defaults(fn=cmd_init)
    s = sub.add_parser("stamp"); s.set_defaults(fn=cmd_stamp)
    s = sub.add_parser("check"); s.add_argument("file"); s.add_argument("--allow-empty", action="store_true"); s.set_defaults(fn=cmd_check)
    s = sub.add_parser("self-test"); s.set_defaults(fn=cmd_self_test)
    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
