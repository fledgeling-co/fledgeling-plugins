#!/usr/bin/env python3
"""Render a surface twice: neutralised for the judge, untouched for the human.

Tenant-authored text renders into the very capture a vision judge reads, which is
the transfer argument for image-borne prompt injection. So elements marked
`data-tenant-text` (and everything inside them) have their text replaced with
length-matched neutral filler before the judge sees the surface, while the
human-facing capture keeps the real words — a byte-identical copy of the input.

This is a mitigation rather than a fix. The transfer from oncology imaging to
product screenshots is an argument, not a measurement, and nothing here measures
it.

Length-matched means: same character count and same word count, per text node, so
layout does not shift between the two renders and the judge is not reading a
differently-sized page. Whitespace, punctuation, case and digit positions are all
preserved; letters become filler and digits become zeros. The match is checked
before either file is written, and a surface whose filler does not match exits 2
rather than producing a render the judge would read as different.

Parsing is stdlib `html.parser`. Text inside `<script>` and `<style>` is left
alone even within a tenant region — neutralising it would change how the page
renders rather than what the judge reads — and the count is reported.
"""

from __future__ import annotations

import argparse
import contextlib
import html
import html.parser
import io
import pathlib
import shutil
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import _cli                                                   # noqa: E402
import _state                                                 # noqa: E402

MARKER = "data-tenant-text"

# Attributes that reach a judge through the accessibility tree or a tooltip, so
# tenant text in one of them is on the same channel as tenant text in the body.
TEXT_ATTRS = ("title", "alt", "aria-label", "placeholder", "value", "content",
              "aria-description", "data-tooltip")

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}

RAW_TEXT = {"script", "style"}

FILLER_LETTERS = "neutralfiller"

# Whitespace-equivalent entities are separators rather than content: replacing one
# with a letter would change the word count.
SEPARATOR_ENTITIES = {"nbsp", "ensp", "emsp", "thinsp", "#160", "#32"}


def neutralise_text(text: str) -> str:
    """Replace letters with filler and digits with zeros, keeping everything else.

    Character-for-character, so the character count is unchanged; whitespace is
    untouched, so the word count is unchanged too.
    """
    out: list[str] = []
    letter = 0
    for ch in text:
        if ch.isdigit():
            out.append("0")
        elif ch.isalpha():
            fill = FILLER_LETTERS[letter % len(FILLER_LETTERS)]
            letter += 1
            out.append(fill.upper() if ch.isupper() else fill)
        else:
            out.append(ch)
    return "".join(out)


def words(text: str) -> int:
    return len(text.split())


def length_matched(original: str, filler: str) -> list[str]:
    """The invariant, as a list of violations. Empty means matched."""
    a, b = html.unescape(original), html.unescape(filler)
    problems: list[str] = []
    if len(a) != len(b):
        problems.append(f"character count {len(b)} != {len(a)} for {original[:40]!r}")
    if words(a) != words(b):
        problems.append(f"word count {words(b)} != {words(a)} for {original[:40]!r}")
    return problems


class Neutraliser(html.parser.HTMLParser):
    """Rewrites the document, and records every (original, filler) text pair."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.out: list[str] = []
        self.pairs: list[tuple[str, str]] = []
        self.stack: list[tuple[str, bool]] = []
        self.depth = 0
        self.raw_depth = 0
        self.tenant_elements = 0
        self.attributes_neutralised = 0
        self.raw_skipped = 0

    # ── regions ──
    def _marked(self, attrs: list[tuple[str, str | None]]) -> bool:
        return any(name.lower() == MARKER for name, _ in attrs)

    def _emit_tag(self, tag: str, attrs: list[tuple[str, str | None]],
                  self_closing: bool) -> None:
        """Rebuild a tag only when an attribute had to change; otherwise emit the
        original text verbatim, so quoting and entities survive untouched."""
        inside = self.depth > 0 or self._marked(attrs)
        changed = False
        rebuilt: list[str] = []
        for name, value in attrs:
            if value is None:
                rebuilt.append(name)
                continue
            if inside and name.lower() in TEXT_ATTRS and value.strip():
                filler = neutralise_text(value)
                self.pairs.append((value, filler))
                self.attributes_neutralised += 1
                changed = True
                value = filler
            rebuilt.append(f'{name}="{html.escape(value, quote=True)}"')
        if not changed:
            self.out.append(self.get_starttag_text() or f"<{tag}>")
            return
        tail = " /" if self_closing else ""
        self.out.append(f"<{tag}" + ("" if not rebuilt else " " + " ".join(rebuilt))
                        + tail + ">")

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        marked = self._marked(attrs)
        self._emit_tag(tag, attrs, self_closing=False)
        if marked:
            self.tenant_elements += 1
        if tag in VOID:
            return
        self.stack.append((tag, marked))
        if marked:
            self.depth += 1
        if tag in RAW_TEXT:
            self.raw_depth += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self._marked(attrs):
            self.tenant_elements += 1
        self._emit_tag(tag, attrs, self_closing=True)

    def handle_endtag(self, tag: str) -> None:
        self.out.append(f"</{tag}>")
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                for _, marked in self.stack[i:]:
                    if marked:
                        self.depth -= 1
                del self.stack[i:]
                if tag in RAW_TEXT and self.raw_depth:
                    self.raw_depth -= 1
                return
        # An unmatched close tag says nothing about the region; leave the stack.

    # ── content ──
    def handle_data(self, data: str) -> None:
        if self.depth > 0 and self.raw_depth == 0 and data.strip():
            filler = neutralise_text(data)
            self.pairs.append((data, filler))
            self.out.append(filler)
            return
        if self.depth > 0 and self.raw_depth and data.strip():
            self.raw_skipped += 1
        self.out.append(data)

    def handle_entityref(self, name: str) -> None:
        source = f"&{name};"
        if self.depth > 0 and self.raw_depth == 0 and name.lower() not in SEPARATOR_ENTITIES:
            filler = neutralise_text(html.unescape(source)) or "n"
            self.pairs.append((source, filler))
            self.out.append(filler)
            return
        self.out.append(source)

    def handle_charref(self, name: str) -> None:
        source = f"&#{name};"
        if self.depth > 0 and self.raw_depth == 0 and f"#{name}".lower() not in SEPARATOR_ENTITIES:
            filler = neutralise_text(html.unescape(source)) or "n"
            self.pairs.append((source, filler))
            self.out.append(filler)
            return
        self.out.append(source)

    # ── everything else passes through ──
    def handle_comment(self, data: str) -> None:
        self.out.append(f"<!--{data}-->")

    def handle_decl(self, decl: str) -> None:
        self.out.append(f"<!{decl}>")

    def handle_pi(self, data: str) -> None:
        self.out.append(f"<?{data}>")

    def unknown_decl(self, data: str) -> None:
        self.out.append(f"<![{data}]>")


def neutralise_document(source: str) -> tuple[str, Neutraliser]:
    parser = Neutraliser()
    parser.feed(source)
    parser.close()
    return "".join(parser.out), parser


# ── main ─────────────────────────────────────────────────────────────────────

def extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--html", required=False, metavar="PATH",
                   help="the surface to render (required outside --selftest)")
    p.add_argument("--out-judge", default=None, metavar="PATH",
                   help="default: <root>/.warrant/renders/<stem>.judge.html")
    p.add_argument("--out-human", default=None, metavar="PATH",
                   help="default: <root>/.warrant/renders/<stem>.human.html")
    p.add_argument("--require-tenant-text", action="store_true",
                   help=f"exit 2 when nothing carries {MARKER}")


def main(args: argparse.Namespace) -> int:
    root = pathlib.Path(args.root).expanduser().resolve()
    if not args.html:
        _cli.say(args, "--html is required")
        _cli.emit(args, {"ok": False, "reason": "no-input"})
        return _cli.ERROR
    src = pathlib.Path(args.html).expanduser().resolve()
    if not src.is_file():
        raise _state.Absent(str(src))

    renders = _state.state_dir(root, create=True) / "renders"
    judge_path = pathlib.Path(args.out_judge).expanduser().resolve() if args.out_judge \
        else renders / f"{src.stem}.judge.html"
    human_path = pathlib.Path(args.out_human).expanduser().resolve() if args.out_human \
        else renders / f"{src.stem}.human.html"

    source = src.read_text(errors="replace")
    judge_text, parser = neutralise_document(source)

    problems: list[str] = []
    for original, filler in parser.pairs:
        problems.extend(length_matched(original, filler))
    # Checked against the filler itself rather than the whole document: a tenant
    # word that also appears in the page's own chrome is not a survivor.
    filler_blob = "".join(f for _, f in parser.pairs)
    survivors = [w for original, _ in parser.pairs
                 for w in html.unescape(original).split()
                 if len(w) > 3 and w in filler_blob]
    if survivors:
        problems.append(f"{len(survivors)} tenant word(s) survive in the judge render, "
                        f"first {survivors[0]!r}")

    if problems:
        _cli.say(args, f"NOT written: the judge render is not length-matched "
                       f"({len(problems)} problem(s))")
        for problem in problems[:10]:
            _cli.say(args, f"  {problem}")
        _cli.emit(args, {"ok": False, "reason": "not-length-matched",
                         "problems": problems, "judge": None, "human": None})
        return _cli.FAILED

    if parser.tenant_elements == 0:
        note = (f"nothing on this surface carries {MARKER}, so the judge render is "
                "identical to the human one; a surface with unmarked tenant text is "
                "indistinguishable here from a surface with none")
        if args.require_tenant_text:
            _cli.say(args, f"NOT written: {note}")
            _cli.emit(args, {"ok": False, "reason": "no-tenant-text", "note": note,
                             "judge": None, "human": None})
            return _cli.FAILED
        _cli.say(args, f"note: {note}")

    judge_path.parent.mkdir(parents=True, exist_ok=True)
    human_path.parent.mkdir(parents=True, exist_ok=True)
    judge_path.write_text(judge_text)
    # Byte-identical, rather than re-serialised: the human capture must be the
    # surface as authored, not the surface as this parser understood it.
    shutil.copyfile(src, human_path)

    after: list[str] = []
    if human_path.read_bytes() != src.read_bytes():
        after.append("the human render is not byte-identical to the input")

    chars = sum(len(html.unescape(o)) for o, _ in parser.pairs)
    word_total = sum(words(html.unescape(o)) for o, _ in parser.pairs)
    _cli.say(args, f"judge  {judge_path}")
    _cli.say(args, f"human  {human_path}")
    _cli.say(args, f"  {parser.tenant_elements} element(s) marked {MARKER}, "
                   f"{len(parser.pairs)} text node(s) neutralised, "
                   f"{parser.attributes_neutralised} attribute(s), "
                   f"{chars} char(s) / {word_total} word(s) matched exactly")
    if parser.raw_skipped:
        _cli.say(args, f"  {parser.raw_skipped} script/style block(s) inside a tenant "
                       "region left untouched, so the render is unchanged")
    for problem in after:
        _cli.say(args, f"  problem after writing: {problem}")

    _cli.emit(args, {
        "ok": not after,
        "judge": str(judge_path),
        "human": str(human_path),
        "tenant_elements": parser.tenant_elements,
        "text_nodes": len(parser.pairs),
        "attributes_neutralised": parser.attributes_neutralised,
        "characters_matched": chars,
        "words_matched": word_total,
        "raw_blocks_skipped": parser.raw_skipped,
        "problems": after,
    })
    return _cli.OK


# ── selftest ─────────────────────────────────────────────────────────────────

def _call(*argv: str) -> tuple[int, str, str]:
    p = _cli.parser("selftest")
    extra(p)
    parsed = p.parse_args(list(argv))
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = _cli.run(main, None, parsed)
    return code, out.getvalue(), err.getvalue()


FIXTURE = (pathlib.Path(__file__).resolve().parent.parent
           / "evals" / "fixtures" / "charter-panel-lot" / "surface.tenant.html")


def selftest() -> list[tuple[str, bool]]:
    cases: list[tuple[str, bool]] = []
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="warrant-neutralise-"))
    try:
        root = tmp / "repo"
        root.mkdir()
        src = root / "surface.html"
        shutil.copy(FIXTURE, src)

        code, out, _ = _call("--root", str(root), "--html", str(src))
        cases.append(("renders both versions", code == _cli.OK))
        judge = (_state.state_dir(root) / "renders" / "surface.judge.html").read_text()
        human = (_state.state_dir(root) / "renders" / "surface.human.html").read_bytes()
        cases.append(("the human render is byte-identical to the input",
                      human == src.read_bytes()))
        cases.append(("the judge render differs from the input",
                      judge != src.read_text()))

        original = src.read_text()
        _, parser = neutralise_document(original)
        cases.append(("every text node is length-matched",
                      all(not length_matched(o, f) for o, f in parser.pairs)))
        cases.append(("the whole judge render keeps the input's length",
                      len(judge) == len(original)))
        cases.append(("the judge render keeps the input's word count",
                      words(judge) == words(original)))

        cases.append(("the injection attempt does not survive",
                      "INSTRUCTIONS" not in judge and "verdict" not in judge.lower()))
        cases.append(("tenant prose does not survive",
                      "Roaring Twenties" not in judge))
        cases.append(("a tenant figure becomes zeros",
                      "12.4" not in judge and "00.0" in judge))
        cases.append(("tenant text in title= is neutralised",
                      "Tenant tooltip" not in judge))
        cases.append(("non-tenant chrome survives untouched",
                      "Quarterly report" in judge and "Diolog" in judge))
        cases.append(("markup survives", judge.count("<p") == original.count("<p")))
        cases.append(("the marker attribute survives", MARKER in judge))
        cases.append(("script inside a tenant region is untouched",
                      "tenantScriptMarker" in judge))
        cases.append(("the untouched script is reported", "script/style" in out))
        cases.append(("a comment survives", "<!-- chrome comment -->" in judge))
        cases.append(("the doctype survives", judge.lower().startswith("<!doctype html>")))
        cases.append(("a non-breaking space is preserved as a separator",
                      "&nbsp;" in judge))

        # Nesting: the region ends where its element closes.
        nested = root / "nested.html"
        nested.write_text('<div data-tenant-text><span><b>Secret words</b></span>'
                          '</div><p>After the region</p>')
        code, _, _ = _call("--root", str(root), "--html", str(nested))
        text = (_state.state_dir(root) / "renders" / "nested.judge.html").read_text()
        cases.append(("nesting inside a region is neutralised",
                      code == _cli.OK and "Secret" not in text))
        cases.append(("text after the region survives", "After the region" in text))

        # A surface with nothing marked.
        plain = root / "plain.html"
        plain.write_text("<p>Chrome only, nothing tenant-authored.</p>")
        code, out_plain, _ = _call("--root", str(root), "--html", str(plain))
        cases.append(("a surface with no marked text is reported and written",
                      code == _cli.OK and f"nothing on this surface carries {MARKER}"
                      in out_plain))
        code, out_req, _ = _call("--root", str(root), "--html", str(plain),
                                 "--require-tenant-text")
        cases.append(("--require-tenant-text turns that into a failure",
                      code == _cli.FAILED))

        # The length-match rule, observed failing: a filler that drops characters
        # must stop the render being written at all.
        global neutralise_text
        good = neutralise_text
        judge_path = _state.state_dir(root) / "renders" / "surface.judge.html"
        before = judge_path.read_text()
        try:
            neutralise_text = lambda text: text.replace("e", "")   # noqa: E731
            code, out_bad, _ = _call("--root", str(root), "--html", str(src))
            cases.append(("a filler that is not length-matched exits 2",
                          code == _cli.FAILED))
            cases.append(("the failure names the count mismatch",
                          "character count" in out_bad))
            cases.append(("nothing is written on that failure",
                          judge_path.read_text() == before))
            neutralise_text = lambda text: text                    # noqa: E731
            code, out_id, _ = _call("--root", str(root), "--html", str(src))
            cases.append(("a filler that changes nothing is caught as a survivor",
                          code == _cli.FAILED and "survive" in out_id))
        finally:
            neutralise_text = good

        cases.append(("length_matched passes a matched pair",
                      length_matched("Hello there", "Neutr utaal") == []))
        cases.append(("length_matched fires on a word-count change",
                      any("word count" in p for p in length_matched("a b", "ab c d"))))
        cases.append(("length_matched fires on a character-count change",
                      any("character count" in p for p in length_matched("abc", "ab"))))
        cases.append(("digits become zeros", neutralise_text("12.4%") == "00.0%"))
        cases.append(("case and punctuation are preserved",
                      neutralise_text("Ab, c!") == "Ne, u!"))

        code, _, _ = _call("--root", str(root), "--html", str(root / "absent.html"))
        cases.append(("a surface that does not exist exits 3", code == _cli.MISSING))
        code, _, _ = _call("--root", str(root))
        cases.append(("no --html exits 1", code == _cli.ERROR))
        code, o, e = _call("--root", str(root), "--html", str(src), "--json")
        cases.append(("--json puts only JSON on stdout",
                      o.lstrip().startswith("{") and "judge" in o and "judge" in e))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return cases


if __name__ == "__main__":
    raise SystemExit(_cli.entry(__doc__ or "", main, selftest, extra))
