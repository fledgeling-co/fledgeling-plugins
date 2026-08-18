#!/usr/bin/env python3
"""
agent_voice_lint.py — deterministic guardrail for agent-authored text.

Two register classes, because the reader decides the failure mode:

  human-read  (reply, report, commit, review, doc)
      Fails on padding: closing summaries, self-congratulation, preamble openers.
      The reader is an expert mid-task; every deletable sentence is a cost.

  agent-read  (skill, brief)
      Fails on ambiguity: unmeasurable qualifiers, uncounted categorical scope,
      pressure language, verification scaffolding. A model can satisfy vague
      prose and still produce the wrong artifact, and that passes human review.

Config-driven through agent-voice-lint.json so one script serves every project.
Exit code is non-zero on any hard failure, so it can gate delivery. Everything
else is advisory and never fails the run.

Usage:
    python3 agent_voice_lint.py --format reply draft.md
    python3 agent_voice_lint.py --config agent-voice-lint.json --format skill SKILL.md
    python3 agent_voice_lint.py --format brief --target gemini brief.md
    cat draft.md | python3 agent_voice_lint.py --format report -
    python3 agent_voice_lint.py --extract-fingerprint corpus/*.md
    python3 agent_voice_lint.py --self-test
"""

import argparse
import json
import os
import re
import sys

# ------------------------------------------------------------------ registers

HUMAN_READ = {"reply", "report", "commit", "review", "doc"}
AGENT_READ = {"skill", "brief"}

BUILTIN_FORMATS = {
    "reply":  {"warn_lines": 15,
               "note": "a question gets an answer; past ~15 lines it is a report"},
    "report": {"warn_lines": 30,
               "note": "outcome, what changed, what is open"},
    "commit": {"max_subject_chars": 72,
               "note": "subject line under 72 chars, imperative, no full stop"},
    "review": {"warn_words": 220,
               "note": "one issue per comment, with its failure scenario"},
    "doc":    {"note": "every section load-bearing for a decision"},
    "skill":  {"warn_lines": 300,
               "note": "push depth to references; the runner pays for this on every call"},
    "brief":  {"note": "no brevity rule; an underspecified brief is the expensive failure"},
}

# --------------------------------------------------------- shared hard checks

# Closing flourish. A restatement of what was just said is the single most
# common way an answer doubles in length without gaining information.
CLOSING_SUMMARY = [
    "in summary", "in conclusion", "to summarise", "to summarize", "to sum up",
    "to recap", "in closing", "all in all", "to wrap up",
    "hope this helps", "i hope this helps", "hope that helps",
    "let me know if", "feel free to reach out", "feel free to ask",
    "please let me know", "happy to help", "anything else i can",
    "as a final note", "one last thing to note",
]

# Same words, but only where they open a sentence or a line.
CLOSING_SENTENCE_START = re.compile(
    r"(?im)(?:^|(?<=[.!?]\s)|(?<=[.!?]\s\s))\s*(?:[-*>]\s+)?"
    r"(overall|in short|in essence|net-net|bottom line)\s*[,:]"
)

# Emotional appeal, flattery, artificial pressure. Google measures these as
# actively harmful; Anthropic measures them as overtriggering.
PRESSURE = [
    "critical:", "critically important", "you must", "you absolutely must",
    "never ever", "extremely important", "extremely critical", "do not fail",
    "at all costs", "very bad things", "this is vital", "this is crucial",
    "under no circumstances", "i will be fired", "my job depends",
    "it is imperative that you", "failure is not an option", "no excuses",
]

# Assistant correspondence and unfilled slots pasted into a shipped artifact.
LEAKAGE = [
    "certainly!", "of course!", "as an ai", "as a large language model",
    "i cannot browse", "as of my last update", "based on available information",
    "[insert", "[your ", "[topic]", "[company]", "[name]", "[path]",
    "[todo]", "xxx-todo", "lorem ipsum", "<your project>", "<insert",
]

# ---------------------------------------------------- human-read hard checks

SELF_CONGRATULATION = [
    "successfully implemented", "successfully created", "successfully added",
    "successfully fixed", "successfully updated", "successfully completed",
    "successfully migrated", "successfully refactored", "successfully resolved",
    "robust solution", "comprehensive solution", "elegant solution",
    "clean solution", "robust implementation", "comprehensive implementation",
    "production-ready implementation", "battle-tested",
    "significantly improved", "greatly improved", "dramatically improved",
    "vastly improved", "massively improved", "substantially improved",
    "significantly faster", "much more maintainable", "far more maintainable",
    "considerably more maintainable", "rock-solid", "bulletproof",
]

# Opening words that delay the answer. Checked on the first non-empty line only.
PREAMBLE_OPENERS = [
    "here is", "here's", "here are", "based on my", "based on the analysis",
    "i've gone ahead", "i have gone ahead", "great question", "good question",
    "excellent question", "that's a great", "sure,", "sure!", "certainly,",
    "i'd be happy to", "i would be happy to", "let me ", "let's ",
    "i'll start by", "i will start by", "first, let me", "to answer your",
    "as requested", "as you requested", "per your request", "absolutely,",
    "you're right", "you are right", "you're absolutely right",
]

# --------------------------------------------------- agent-read hard checks

# Subjective or relative qualifiers that lack a concrete, measurable
# definition. Each one is a slot a model fills with its own priors.
UNMEASURABLE = [
    "robust", "comprehensive", "comprehensively", "thorough", "thoroughly",
    "appropriate", "appropriately", "properly", "adequate", "adequately",
    "sufficient", "sufficiently", "reasonable", "reasonably", "sensible",
    "high-quality", "high quality", "well-structured", "well structured",
    "best practice", "best practices", "best-practice", "state-of-the-art",
    "as needed", "where appropriate", "if necessary", "as necessary",
    "make sure it looks good", "looks good", "polished", "professional-looking",
]

# Weaker members of the same family: real words with legitimate uses, so they
# warn rather than fail. Promote via config "unmeasurable_extra" if a project
# wants them hard.
UNMEASURABLE_SOFT = [
    "clean", "cleanly", "nice", "elegant", "optimal", "efficiently",
    "carefully", "meaningful", "relevant", "significant", "substantial",
    "various", "several", "a few", "some of the", "etc.", "and so on",
]

# Verification the runner already performs. Removing these reduces wasted
# tokens with no loss in quality on current Claude models; the rule inverts
# for a Gemini runner, which needs the step named.
VERIFICATION_SCAFFOLD = [
    "double-check", "double check", "re-verify", "reverify",
    "verify your answer", "verify your work", "check your work",
    "check your answer", "use a subagent to verify",
    "spawn a subagent to verify", "add a final verification step",
    "include a final verification", "before responding, verify",
    "before you finish, verify", "verify before responding",
    "make sure to double", "triple-check", "review your own work",
]

# Uncounted categorical scope. One recorded run satisfied every categorically
# named requirement with a single instance.
#
# Group 2 is the head noun and group 3 an optional following word, because a
# single greedy two-word capture swallows the conjunction in "all screens and
# record ..." and then reads as singular. The plural test runs on whichever of
# the two is the real noun.
CATEGORICAL = re.compile(
    r"(?i)\b(all|every|each|any)\s+(?:the\s+|its\s+|their\s+)?"
    r"([a-z][a-z-]{2,})(?:\s+([a-z][a-z-]{2,}))?"
)
# A categorical in OBJECT position after a task verb is a scope instruction and
# hard-fails. The same words in SUBJECT position state a property of a class
# ("every finding carries its failure scenario") and only warn. A noisy hard
# check gets the lint switched off, so this one buys precision with recall.
TASK_VERB = re.compile(
    r"(?i)\b(capture|review|check|test|cover|handle|list|find|read|write|update"
    r"|fix|verify|ensure|include|add|remove|run|apply|document|report|return"
    r"|audit|scan|validate|implement|support|render|generate|enumerate|inspect"
    r"|measure|record|screenshot|iterate over|go through|walk through|process"
    r"|for)\s+(?:\w+\s+){0,3}$"
)

# Words that are never the noun a scope claim is about.
CATEGORICAL_STOP = {
    "and", "but", "for", "the", "that", "with", "from", "into", "then",
    "are", "was", "were", "has", "have", "had", "can", "will", "must",
    "should", "would", "may", "not", "you", "your", "our", "its", "their",
    "this", "these", "those", "when", "where", "which", "while", "also",
    "get", "gets", "run", "runs", "use", "uses", "set", "sets", "put",
}
# Idioms and closed references where "all/every/each" carries no scope.
CATEGORICAL_OK = {
    "all costs", "all of the above", "all right", "all times", "all three",
    "all four", "all five", "all cases", "all the way", "all of them",
    "any case", "any time", "any of the above", "any other", "any given",
    "any point", "each other", "every time", "every case", "every one",
    "all means", "all costs", "any means", "all odds", "any others",
    "each item", "every item", "every line", "every turn", "every rule",
    "any number", "all sorts", "any means", "every sentence",
}
# A line escapes the categorical check when it also names a count.
COUNT_NEARBY = re.compile(
    r"(?i)(\d+|\bone\b|\btwo\b|\bthree\b|\bfour\b|\bfive\b|\bsix\b|\bseven\b"
    r"|\beight\b|\bnine\b|\bten\b|\btwelve\b"
    r"|listed below|enumerated|the following|named below|exactly|per item"
    r"|as follows|below:|in the table)"
)

# All-caps tokens that are not jargon needing a definition.
ACRONYM = re.compile(r"\b([A-Z][A-Z0-9]{1,7})\b")
ACRONYM_OK = {
    "AI", "API", "APIS", "CLI", "CSS", "HTML", "HTTP", "HTTPS", "JSON", "JS",
    "TS", "SQL", "URL", "URI", "UUID", "XML", "YAML", "MD", "PR", "PRS", "UI",
    "UX", "ID", "IDS", "OK", "TODO", "NOTE", "FAIL", "PASS", "WARN", "INFO",
    "RESULT", "LLM", "LLMS", "MCP", "SDK", "OS", "CPU", "GPU", "RAM", "IO",
    "CI", "CD", "DOM", "SVG", "PNG", "JPG", "PDF", "CSV", "REST", "RPC",
    "TTL", "LRU", "JWT", "TLS", "SSL", "SSH", "DNS", "IP", "TCP", "UDP",
    "A", "I", "AND", "OR", "NOT", "IF", "THE", "USE", "ONE", "TWO", "XHIGH",
    "GB", "MB", "KB", "MS", "PP", "US", "AU", "UK", "EU", "SKILL", "EVALS",
    "README", "CLAUDE", "AGENTS", "XHTML", "ARIA", "WCAG", "AA", "AAA",
    "GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "CRUD", "ORM", "NAN",
    "OOM", "P99", "P95", "P50", "SLA", "SLO", "QA", "E2E", "TDD", "DRY",
}

# ------------------------------------------------------------ soft AI tells

DEFAULT_CLICHES = [
    "dynamic landscape", "let's dive in", "lets dive in", "let's break it down",
    "in today's fast-paced", "fast-paced world", "game-changer", "game changer",
    "unlock the power", "unlock the potential", "delve into", "delving into",
    "ever-evolving", "navigate the complexities", "at the end of the day",
    "move the needle", "leverage the power", "it's no secret that",
    "buckle up", "the bottom line is", "paradigm shift", "best-in-class",
    "low-hanging fruit", "supercharge", "rich tapestry", "stands as a testament",
    "serves as a testament", "is a testament to", "marking a pivotal",
    "a pivotal moment", "underscores the importance", "underscores its",
    "highlights the importance", "highlighting the importance",
    "evolving landscape", "indelible mark", "deeply rooted", "valuable insights",
    "key takeaway", "in an era of", "in an era where", "it's important to note",
    "it is important to note", "worth noting that", "it should be noted",
]

AI_VOCAB = [
    "delve", "tapestry", "testament", "underscore", "underscores", "pivotal",
    "crucial", "intricate", "intricacies", "meticulous", "meticulously",
    "boasts", "showcase", "showcases", "showcasing", "garner", "garnered",
    "fostering", "bolster", "bolstered", "interplay", "vibrant", "enduring",
    "groundbreaking", "seamless", "seamlessly", "cutting-edge", "world-class",
    "renowned", "multifaceted", "holistic", "leverage", "utilise", "utilize",
]

NEG_PARALLEL = re.compile(
    r"(?i)\b(it'?s not just|isn'?t just|not only .{3,60} but also"
    r"|it'?s not (?:a |an |about )?\w+[,;] it'?s"
    r"|not (?:the|a|an) \w+, but (?:the|a|an) \w+"
    r"|here'?s the kicker|that'?s only half the story"
    r"|and that'?s where it gets interesting)"
)
PARTICIPLE_TAIL = re.compile(
    r"(?i),\s(?:highlighting|underscoring|emphasi[sz]ing|showcasing|reflecting"
    r"|demonstrating|ensuring|fostering|cementing|solidifying|signaling"
    r"|signalling|reinforcing|paving the way)\s[^.]{5,}\.\s*$"
)
BOLD_HEADER_BULLET = re.compile(r"^\s*[-*•]\s+\*\*[^*]+:?\*\*")
MARKDOWN_HEADING = re.compile(r"^#{1,6}\s")
XML_TAG = re.compile(r"^\s*</?[a-z][a-z0-9_]{2,}>\s*$")
BULLET = re.compile(r"^\s*(?:[-*•]|\d+\.)\s+\S")
EM_DASHES = ["—", "―"]
EN_DASH = "–"

NOMINALIZATION = re.compile(
    r"\b\w{4,}(?:tion|tions|sion|sions|ment|ments|ness|ance|ence|ities|ity)\b", re.I)
CONTRACTION = re.compile(r"\b\w+['’](?:t|s|re|ve|ll|d|m)\b", re.I)


# ------------------------------------------------------------------- helpers

def read_text(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def default_config():
    return {
        "em_dash": "advisory",
        "banned_phrases": list(DEFAULT_CLICHES),
        "advisory_phrases": [],
        "ai_vocab_extra": [],
        "unmeasurable_extra": [],
        "acronym_allowlist": [],
        "repeat_allowlist": [],
        "categorical": "fail",
        "formats": {},
        "fingerprint": {},
    }


def load_config(path):
    cfg = default_config()
    if not path:
        return cfg
    with open(path, "r", encoding="utf-8") as f:
        user = json.load(f)
    for key, val in user.items():
        if key == "banned_phrases":
            cfg["banned_phrases"] = sorted(set(DEFAULT_CLICHES) | {p.lower() for p in val})
        elif key == "formats":
            cfg["formats"].update(val)
        else:
            cfg[key] = val
    return cfg


def blank_mentions(text):
    """Blank out quoted and italicised spans, preserving line count and offsets.

    A rule file names the form it bans by quoting or italicising it ("never
    write 'CRITICAL: you MUST'", *In summary*), and those quotes wrap across
    lines in real prose. A phrase check that cannot tell a mention from a use
    flags exactly the file that gets the rule right, so mentions are blanked
    before the phrase bans run. Newlines inside a span are kept so reported line
    numbers still point at the right line.

    The trade: a draft that italicises its own closing summary escapes the
    check. Quoting your own padding is not something that happens by accident,
    while quoting a banned form to ban it is what a rule file does on every
    page.
    """
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))

    # Quoted spans, straight and curly, spanning lines where prose wraps them.
    text = re.sub(r"\"[^\"]{0,900}?\"", blank, text)
    text = re.sub(r"\u201c[^\u201d]{0,900}?\u201d", blank, text)
    text = re.sub(r"(?<![A-Za-z])'[^'\n]{0,160}?'(?![A-Za-z])", blank, text)
    # Single-asterisk and underscore emphasis, the other mention convention.
    text = re.sub(r"(?<!\*)\*(?!\*)[^*\n]{1,300}?\*(?!\*)", blank, text)
    text = re.sub(r"(?<![\w_])_[^_\n]{1,160}?_(?![\w_])", blank, text)
    return text


def strip_noise(text):
    """Remove fenced code, inline code and link targets before prose checks.

    A phrase inside a code block or a backtick is a quoted artifact, not the
    author's prose, and flagging it produces the false positives that get a
    lint switched off.
    """
    text = re.sub(r"```.*?```", "\n", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", " ", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    return blank_mentions(text)


def prose_lines(text, drop_mentions=False):
    """(lineno, line) for lines that carry the author's own prose.

    drop_mentions blanks quoted and italicised spans first; see blank_mentions.
    Structural checks keep the raw line, because a bullet is a bullet whether or
    not it quotes something.
    """
    if drop_mentions:
        text = blank_mentions(text)
    out, fence = [], False
    for i, raw in enumerate(text.splitlines(), 1):
        if raw.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        out.append((i, re.sub(r"`[^`\n]*`", " ", raw)))
    return out


def phrase_hits(lines, phrases):
    hits = []
    for i, line in lines:
        low = line.lower()
        for p in phrases:
            if p in low:
                hits.append((i, p, line.strip()))
    return hits


def split_sentences(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"^#{1,6} .*$", " ", text, flags=re.M)
    text = re.sub(r"^\s*[-*•]\s+", "", text, flags=re.M)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'“(])", text)
    return [p.strip() for p in parts if len(re.findall(r"\b\w+\b", p)) >= 2]


def fingerprint(text):
    sents = split_sentences(text)
    if not sents:
        return None
    lens = [len(re.findall(r"\b\w+\b", s)) for s in sents]
    n_words = sum(lens) or 1
    mean = sum(lens) / len(lens)
    sd = (sum((x - mean) ** 2 for x in lens) / len(lens)) ** 0.5
    paras = [p for p in re.split(r"\n\s*\n", text) if split_sentences(p)]
    para_sents = [len(split_sentences(p)) for p in paras] or [1]
    return {
        "mean_sentence_words": round(mean, 1),
        "sd_sentence_words": round(sd, 1),
        "contraction_per_100w": round(100 * len(CONTRACTION.findall(text)) / n_words, 2),
        "comma_per_sentence": round(text.count(",") / len(sents), 2),
        "nominalization_per_1000w": round(1000 * len(NOMINALIZATION.findall(text)) / n_words, 1),
        "mean_paragraph_sentences": round(sum(para_sents) / len(para_sents), 1),
    }


def compare_fingerprint(draft, target):
    checks = [
        ("mean_sentence_words", 0.35, "average sentence length"),
        ("sd_sentence_words", 0.40,
         "sentence-length variance (uniform rhythm is an LLM tell)"),
        ("nominalization_per_1000w", 0.50,
         "nominalization rate (-tion/-ment/-ness abstractions)"),
    ]
    for key, tol, label in checks:
        want, got = target.get(key), draft.get(key)
        if not want or got is None:
            continue
        if abs(got - want) / want > tol:
            where = "above" if got > want else "below"
            yield f"{label}: draft {got} vs target {want} ({where} the +/-{int(tol*100)}% band)"


def repeated_phrases(text, allow=(), n=5, limit=6):
    body = strip_noise(text)
    words = re.findall(r"[a-z'’]+", body.lower())
    if len(words) < n * 3:
        return []
    shingles = [" ".join(words[i:i + n]) for i in range(len(words) - n + 1)]
    counts = {}
    for s in shingles:
        counts[s] = counts.get(s, 0) + 1
    allow_low = [a.lower() for a in allow]
    out = [(s, c) for s, c in counts.items()
           if c >= 2 and not any(a in s for a in allow_low)]
    return sorted(out, key=lambda x: -x[1])[:limit]


# --------------------------------------------------------------- the checks

class Report:
    def __init__(self):
        self.failures = 0
        self.lines = []

    def fail(self, msg):
        self.failures += 1
        self.lines.append(f"FAIL  {msg}")

    def warn(self, msg):
        self.lines.append(f"warn  {msg}")

    def info(self, msg):
        self.lines.append(f"info  {msg}")

    def ok(self, msg):
        self.lines.append(f"ok    {msg}")


def check(text, fmt, cfg, target):
    r = Report()
    lines = prose_lines(text)
    said = prose_lines(text, drop_mentions=True)  # see blank_mentions
    raw_lines = text.splitlines()
    body = strip_noise(text)
    is_human = fmt in HUMAN_READ
    is_agent = fmt in AGENT_READ

    # -- shared hard checks -------------------------------------------------
    hits = phrase_hits(said, CLOSING_SUMMARY)
    for i, line in said:
        m = CLOSING_SENTENCE_START.search(line)
        if m:
            hits.append((i, m.group(1).lower(), line.strip()))
    if hits:
        for i, p, line in hits:
            r.fail(f'closing flourish "{p}" (end on the last real point), line {i}: {line[:90]}')
    else:
        r.ok("no closing summary")

    hits = phrase_hits(said, PRESSURE)
    if hits:
        for i, p, line in hits:
            r.fail(f'pressure language "{p}" (measured to make performance worse, not better),'
                   f" line {i}: {line[:90]}")
    else:
        r.ok("no pressure language")

    hits = phrase_hits(said, LEAKAGE)
    if hits:
        for i, p, line in hits:
            r.fail(f'assistant leakage or placeholder "{p}", line {i}: {line[:90]}')
    else:
        r.ok("no leakage or placeholders")

    # -- human-read hard checks --------------------------------------------
    if is_human:
        hits = phrase_hits(said, SELF_CONGRATULATION)
        if hits:
            for i, p, line in hits:
                r.fail(f'self-congratulation "{p}" (state the observable instead),'
                       f" line {i}: {line[:90]}")
        else:
            r.ok("no self-congratulation")

        first = next((ln.strip() for _, ln in lines if ln.strip()), "")
        low = first.lower()
        opener = next((p for p in PREAMBLE_OPENERS if low.startswith(p)), None)
        if opener:
            r.fail(f'first line opens on a preamble ("{opener}"); lead with the answer: {first[:90]}')
        elif first:
            r.ok("first line leads with content")

    # -- agent-read hard checks --------------------------------------------
    if is_agent:
        unmeasurable = list(UNMEASURABLE) + [w.lower() for w in cfg.get("unmeasurable_extra", [])]
        found = []
        for i, line in said:
            low = line.lower()
            for w in unmeasurable:
                if re.search(r"\b" + re.escape(w) + r"\b", low):
                    found.append((i, w, line.strip()))
        if found:
            for i, w, line in found:
                r.fail(f'unmeasurable qualifier "{w}" (give an objective constraint instead),'
                       f" line {i}: {line[:90]}")
        else:
            r.ok("no unmeasurable qualifiers")

        soft = [(i, w, line.strip()) for i, line in said for w in UNMEASURABLE_SOFT
                if re.search(r"\b" + re.escape(w) + r"\b", line.lower())]
        for i, w, line in soft[:8]:
            r.warn(f'soft qualifier "{w}" (measurable where it matters?), line {i}: {line[:80]}')

        if target == "claude":
            hits = phrase_hits(said, VERIFICATION_SCAFFOLD)
            if hits:
                for i, p, line in hits:
                    r.fail(f'verification scaffolding "{p}" (this runner self-verifies; the'
                           f" instruction costs tokens and buys nothing), line {i}: {line[:80]}")
            else:
                r.ok("no verification scaffolding")
        else:
            hits = phrase_hits(lines, VERIFICATION_SCAFFOLD)
            if hits:
                r.info(f"{len(hits)} verification instruction(s); correct for a"
                       f" '{target}' runner, remove them for a Claude runner")
            else:
                r.warn(f"no verification step named; a '{target}' runner needs the check"
                       " stated explicitly (command, expected output, failure shape)")

        cat = []
        for i, line in said:
            if MARKDOWN_HEADING.match(line) or COUNT_NEARBY.search(line):
                continue
            for m in CATEGORICAL.finditer(line):
                det, first, second = m.group(1).lower(), m.group(2).lower(), m.group(3)
                second = second.lower() if second else None
                if f"{det} {first}" in CATEGORICAL_OK:
                    continue
                if second and f"{det} {first} {second}" in CATEGORICAL_OK:
                    continue
                noun = second if (second and second not in CATEGORICAL_STOP) else first
                if not noun.endswith("s") or noun.endswith("ss"):
                    continue  # singular reads as generic, not as a scope claim
                phrase = f"{m.group(1)} {first}" + (f" {second}" if noun is second else "")
                is_instruction = bool(TASK_VERB.search(line[:m.start()]))
                cat.append((i, phrase, line.strip(), is_instruction))
                break
        if cat:
            for i, p, line, is_instruction in cat:
                msg = (f'uncounted categorical scope "{p}" (a categorical requirement is'
                       f" satisfiable with one instance; write the number), line {i}: {line[:80]}")
                if is_instruction and cfg.get("categorical") == "fail":
                    r.fail(msg)
                else:
                    r.warn(msg)
            if not any(c[3] for c in cat):
                r.ok("no uncounted scope in an instruction")
        else:
            r.ok("categorical scopes are counted")

        allow = set(ACRONYM_OK) | {a.upper() for a in cfg.get("acronym_allowlist", [])}
        acr = sorted({m.group(1) for m in ACRONYM.finditer(body)} - allow)
        if acr:
            r.warn(f"undefined acronym(s): {', '.join(acr[:10])} — define on first use"
                   " or add to the config allowlist")

        heads = sum(1 for ln in raw_lines if MARKDOWN_HEADING.match(ln))
        tags = sum(1 for ln in raw_lines if XML_TAG.match(ln))
        if heads >= 2 and tags >= 2:
            r.warn(f"mixed delimiter families ({heads} markdown headings, {tags} XML tags);"
                   " choose one and keep it")

        if not re.search(r"(?i)(return|output|respond|report|emit|answer)\b[^.]{0,60}"
                         r"(format|shape|json|schema|form|structure|array|object|table"
                         r"|sentence|line|verdict)", body):
            r.warn("no output-format statement found; say what comes back and in what shape")

    # -- shared advisories -------------------------------------------------
    em = [(i, ln.strip()) for i, ln in lines if any(d in ln for d in EM_DASHES)]
    if em:
        if cfg.get("em_dash") == "forbid":
            for i, line in em:
                r.fail(f"em dash (use ; , . or parentheses, or restructure), line {i}: {line[:80]}")
        else:
            r.warn(f"{len(em)} line(s) with an em dash; watch density and the spaced punchy pattern")
    else:
        r.ok("no em dashes")

    for i, ln in lines:
        for m in re.finditer(re.escape(EN_DASH), ln):
            c = m.start()
            left = ln[c - 1] if c else " "
            right = ln[c + 1] if c + 1 < len(ln) else " "
            if not (left.isdigit() and right.isdigit()):
                r.warn(f"en dash outside a numeric range, line {i}: {ln.strip()[:80]}")
                break

    hits = phrase_hits(said, cfg["banned_phrases"])
    if hits:
        for i, p, line in hits:
            r.fail(f'AI cliche "{p}" (say it plainly), line {i}: {line[:90]}')
    else:
        r.ok("no AI cliches")

    for i, p, line in phrase_hits(said, [p.lower() for p in cfg["advisory_phrases"]]):
        r.warn(f'advisory phrase "{p}", line {i}: {line[:80]}')

    vocab = set(AI_VOCAB) | {w.lower() for w in cfg["ai_vocab_extra"]}
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", body.lower())
    found = sorted({w for w in words if w in vocab})
    if len(found) >= 3:
        r.warn(f"{len(found)} distinct AI-vocabulary words ({', '.join(found[:8])});"
               " one may be fine, this density is a tell")
    elif found:
        r.info(f"AI-vocabulary present: {', '.join(found)} (watch density)")

    for i, ln in lines:
        if NEG_PARALLEL.search(ln):
            r.warn(f'negative parallelism ("not just X, but Y"), line {i}: {ln.strip()[:80]}')
        if PARTICIPLE_TAIL.search(ln.rstrip()):
            r.warn(f"participle analysis tail, line {i}: {ln.strip()[:80]}")

    if is_human:
        bullets = sum(1 for _, ln in lines if BULLET.match(ln))
        content = sum(1 for _, ln in lines if ln.strip())
        if content >= 6 and bullets / content > 0.5:
            r.warn(f"{bullets} of {content} content lines are bullets; prose by default,"
                   " structure for comparisons, procedures and tabular data")
        bh = [(i, ln.strip()) for i, ln in lines if BOLD_HEADER_BULLET.match(ln)]
        if len(bh) >= 3:
            r.warn(f"{len(bh)} inline-header bullets (bullet + bold label + colon);"
                   " the signature AI list shape")
        heads = sum(1 for ln in raw_lines if MARKDOWN_HEADING.match(ln))
        if fmt in {"reply", "commit"} and heads:
            r.warn(f"{heads} markdown heading(s) in a '{fmt}' piece; this register has no sections")

    reps = repeated_phrases(text, allow=cfg.get("repeat_allowlist", []))
    if reps:
        r.warn("repeated 5-word runs (a natural term repeating is fine; a rhetorical phrase"
               " repeating is templating):")
        for p, c in reps:
            r.lines.append(f'        {c}x "{p}"')

    target_fp = cfg.get("fingerprint") or {}
    n_words = len(re.findall(r"\b\w+\b", body))
    if target_fp and n_words >= 120:
        fp = fingerprint(text)
        if fp:
            devs = list(compare_fingerprint(fp, target_fp))
            for d in devs:
                r.warn(f"fingerprint: {d}")
            if not devs:
                r.ok("stylometric fingerprint within target bands")

    # -- length ------------------------------------------------------------
    n_lines = len([ln for ln in raw_lines if ln.strip()])
    r.info(f"{n_words} words, {n_lines} non-empty lines")

    spec = {**BUILTIN_FORMATS.get(fmt, {}), **cfg["formats"].get(fmt, {})}
    note = spec.get("note", "")
    if spec.get("warn_lines") and n_lines > spec["warn_lines"]:
        r.warn(f"{n_lines} lines exceeds the {spec['warn_lines']}-line target for '{fmt}' ({note})")
    if spec.get("warn_words") and n_words > spec["warn_words"]:
        r.warn(f"{n_words} words is long for '{fmt}' ({note})")
    if spec.get("max_subject_chars"):
        subject = next((ln for ln in raw_lines if ln.strip()), "")
        if len(subject) > spec["max_subject_chars"]:
            r.warn(f"subject line is {len(subject)} chars, over"
                   f" {spec['max_subject_chars']}: {subject[:80]}")
        if subject.rstrip().endswith("."):
            r.warn("subject line ends with a full stop")

    return r


# ---------------------------------------------------------------- self-test

FIXTURES = [
    # (name, format, target, text, must_fail)
    ("clean reply", "reply", "claude",
     "Partly. The happy path is covered in `auth.test.ts`, but a malformed header\n"
     "throws at line 41 instead of returning 401.\n", False),
    ("preamble opener", "reply", "claude",
     "Here is the answer you asked for.\n\nThe tests pass.\n", True),
    ("closing flourish", "report", "claude",
     "Rate limiting is live on the public routes.\n\nIn summary, the work is done.\n", True),
    ("self-congratulation", "report", "claude",
     "I successfully implemented the cache and it is a robust solution.\n", True),
    ("clean skill rule", "skill", "claude",
     "Check each of the five states: default, hover, focus, disabled, and error.\n"
     "Return a JSON array with one object per state, in the format below.\n", False),
    ("unmeasurable qualifier", "skill", "claude",
     "Review the states thoroughly and make sure the design is robust.\n"
     "Return the results in JSON format.\n", True),
    ("uncounted categorical", "skill", "claude",
     "Capture all screens and record the contrast ratio.\n"
     "Return the output as a JSON array.\n", True),
    ("pressure language", "skill", "claude",
     "CRITICAL: you must capture the four states listed below.\n"
     "Return output in JSON format.\n", True),
    ("verification scaffolding", "brief", "claude",
     "Find the three connection sites named below and return a JSON array.\n"
     "Double-check your answer before responding.\n", True),
    ("verification kept for gemini", "brief", "gemini",
     "Find the three connection sites named below and return a JSON array.\n"
     "Verify your work by running `pnpm test db` and quoting the exit code.\n", False),
    ("placeholder", "doc", "claude",
     "The service reads from [insert table name] on startup.\n", True),
    # Regressions. Each of these was a live false positive during the build.
    ("quoted ban is a mention", "skill", "claude",
     'Calm triggers. Use "Use X when ..." rather than "CRITICAL: you MUST".\n'
     "Return the result in JSON format.\n", False),
    ("italicised ban is a mention", "doc", "claude",
     "End on the last real point. Sections opening *In summary* or *Overall,* are a tell.\n",
     False),
    ("quote wrapping across lines", "skill", "claude",
     'Anthropic is explicit: "If your prompt contains explicit verification\n'
     "instructions ('include a final verification step for any non-trivial task,'\n"
     "'use a subagent to verify'), remove them: instructions like these cause\n"
     'over-verification on this model and removing them costs nothing in quality."\n'
     "Return the findings in the JSON shape below.\n", False),
    ("categorical as subject only warns", "skill", "claude",
     "Every finding carries its own failure scenario, and each section states the\n"
     "decision it serves. Return the output in the format below.\n", False),
    ("categorical as object still fails", "skill", "claude",
     "Review all the error states and record the contrast ratio.\n"
     "Return the output in JSON format.\n", True),
    ("adverbial 'overall' is not a summary", "doc", "claude",
     "The skill arm came out 11.6% more expensive overall, with no quality difference.\n",
     False),
    ("sentence-initial 'Overall,' is", "doc", "claude",
     "The cache now evicts on a size cap. Overall, the change is a net win.\n", True),
]


def self_test():
    passed = failed = 0
    cfg = default_config()
    for name, fmt, target, text, must_fail in FIXTURES:
        rep = check(text, fmt, cfg, target)
        got_fail = rep.failures > 0
        if got_fail == must_fail:
            passed += 1
            print(f"ok    {name}: {'fails as expected' if must_fail else 'clean as expected'}")
        else:
            failed += 1
            print(f"FAIL  {name}: expected {'a hard failure' if must_fail else 'clean'}, "
                  f"got {rep.failures} failure(s)")
            for ln in rep.lines:
                if ln.startswith("FAIL"):
                    print(f"        {ln}")
    print(f"\nself-test: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


# --------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Lint agent-authored text.")
    ap.add_argument("path", nargs="*", help="File to lint, or - for stdin")
    ap.add_argument("--config", default=None, help="Path to agent-voice-lint.json")
    ap.add_argument("--format", dest="fmt", default=None,
                    help="reply | report | commit | review | doc | skill | brief")
    ap.add_argument("--target", default="claude",
                    help="Family that will read this: claude | gemini | openai | xai | mixed")
    ap.add_argument("--extract-fingerprint", action="store_true",
                    help="Print the stylometric fingerprint block for the given files")
    ap.add_argument("--self-test", action="store_true",
                    help="Run the built-in fixtures and exit")
    args = ap.parse_args()

    if args.self_test:
        sys.exit(self_test())

    if not args.path:
        ap.error("a file to lint is required (or --self-test)")

    if args.extract_fingerprint:
        corpus = "\n\n".join(read_text(p) for p in args.path)
        fp = fingerprint(corpus)
        if fp is None:
            print("no prose found")
            sys.exit(1)
        n = len(re.findall(r"\b\w+\b", corpus))
        print(json.dumps({"fingerprint": fp}, indent=2))
        note = ("stable" if n >= 2000 else
                "usable but below the ~2,000-word stability threshold" if n >= 800 else
                "thin; treat as rough")
        print(f"// corpus: {n} words ({note})")
        sys.exit(0)

    if len(args.path) > 1:
        print("lint takes one file at a time")
        sys.exit(2)

    fmt = args.fmt
    if not fmt:
        base = os.path.basename(args.path[0]).lower()
        fmt = ("skill" if base in {"skill.md", "claude.md", "agents.md"} else
               "commit" if "commit" in base else "doc")
        print(f"info  no --format given; inferred '{fmt}' from the filename")
    if fmt not in HUMAN_READ | AGENT_READ:
        print(f"unknown format '{fmt}'; expected one of "
              f"{', '.join(sorted(HUMAN_READ | AGENT_READ))}")
        sys.exit(2)

    cfg = load_config(args.config)
    rep = check(read_text(args.path[0]), fmt, cfg, args.target)

    print(f"      format={fmt} target={args.target}")
    for ln in rep.lines:
        print(ln)
    print()
    if rep.failures:
        print(f"RESULT: {rep.failures} hard issue(s) — fix before delivering.")
        sys.exit(1)
    print("RESULT: clean on the hard checks.")
    sys.exit(0)


if __name__ == "__main__":
    main()
