#!/usr/bin/env python3
"""Check a résumé's structure and voice against the defaults in resume-craft.

    python3 resume_lint.py resume.md                 # exit 0 clean, 1 on any error
    python3 resume_lint.py --allow-gaps draft.md     # a draft that still carries [gaps]
    python3 resume_lint.py --voice implied resume.md # the person chose no "I" in paragraphs
    python3 resume_lint.py --self-test               # run the bundled fixtures

It reads the Markdown subset that career-kit's build_resume.py renders:

    # Name / contact line / ## Section / ### Employer | dates /
    #### Title | Employer | dates / paragraphs / "- " bullets

What it checks is mechanical: section order and names, summary length, a count of years,
personal details, date format, role-line shape, bare present-tense openers, the generic
register, bullet counts, an empty education section, and [gap] markers. It cannot tell
whether a summary could sit on someone else's résumé, whether a skill is shown below, or
whether a verb is stronger than the person confirmed. Those are read by a person or a
reviewer; facts_lint.py in career-kit checks that each figure was confirmed.

ERROR lines fail the run. WARN lines are questions: read each one and decide.
"""
import argparse
import datetime
import os
import re
import sys

MONTHS = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
DATE_RANGE = re.compile(
    rf"\b(?:{MONTHS}) \d{{4}} [–-] (?:(?:{MONTHS}) \d{{4}}|Present|present)\b")
FULL_MONTH = re.compile(
    r"\b(January|February|March|April|June|July|August|September|October|November|December) \d{4}\b")

SECTION_ALIASES = {
    "summary": {"professional summary", "career summary", "summary", "profile",
                "professional profile"},
    "skills": {"key skills", "skills", "core capabilities", "core skills", "key capabilities"},
    "experience": {"professional experience", "experience", "career history",
                   "employment history", "work experience"},
    "education": {"education and certifications", "education & certifications", "education",
                  "qualifications", "qualifications and certifications",
                  "education and qualifications", "certifications"},
    "development": {"professional development", "training", "recent professional development"},
}
ORDER = ["summary", "skills", "experience", "education", "development"]
BANNED_SECTIONS = {"objective", "career objective", "personal details", "personal information",
                   "hobbies", "interests"}

# The register recruiters read as generic or machine-written. Sources: references/evidence.md.
CLICHES = [
    "results-driven", "results driven", "results-oriented", "results oriented",
    "proven track record", "passionate", "dynamic", "spearheaded", "spearhead",
    "leveraged", "leveraging", "leverage", "synergy", "synergies", "synergised",
    "seasoned", "visionary", "operational excellence", "fast-paced", "fast paced",
    "detail-oriented", "detail oriented", "team player", "self-starter", "self starter",
    "highly motivated", "thought leader", "best-in-class", "best in class", "world-class",
    "world class", "cutting-edge", "cutting edge", "strong communication skills",
    "excellent communication skills", "go-getter", "hard-working", "hardworking",
]
DUTY_OPENERS = re.compile(r"^(responsible for|duties includ|tasked with|in charge of)", re.I)

# Verbs that, opening a line in their bare form, read as a command or a misspelt past tense.
BARE_PRESENT = {
    "lead", "own", "manage", "drive", "deliver", "coordinate", "run", "build", "develop",
    "support", "oversee", "work", "write", "coach", "ensure", "partner", "collaborate",
    "prioritise", "prioritize", "create", "define", "maintain", "provide", "design", "plan",
    "prepare", "review", "report", "liaise", "facilitate", "implement", "identify", "analyse",
    "analyze", "monitor", "track", "mentor", "train", "negotiate", "present", "translate",
    "champion", "act", "serve", "take", "bring", "help", "handle", "execute", "engage",
    "shape", "set", "establish", "improve", "accept", "embed", "orchestrate", "administer",
}
IRREGULAR_PAST = {
    "led", "ran", "built", "cut", "took", "brought", "wrote", "won", "grew", "held", "set",
    "made", "gave", "got", "kept", "drove", "chose", "taught", "sold", "spoke", "began",
    "oversaw", "rebuilt", "put", "found", "saw", "met", "paid", "sent", "spent", "stood",
    "told", "withdrew", "rewrote", "undertook", "dealt", "drew", "rose", "split", "spread",
    "struck", "became", "came", "did", "went", "left", "lent", "lost", "read", "rethought",
    "shrank", "sought", "thought", "understood", "overcame", "underwent", "upheld", "hit",
    "let", "bid", "broke", "caught", "fought", "flew", "forecast", "heard", "knew", "laid",
    "learnt", "meant", "outgrew", "overhauled", "reset", "shut", "stuck", "swept", "wound",
    "was", "were", "had",
}

YEARS_COUNT = [
    re.compile(r"\b\d{1,2}\s*\+\s*years?\b", re.I),
    re.compile(r"\b(?:\d{1,2}|ten|fifteen|twenty|twenty-five|thirty)\s+years?['’]?\s+(?:of\s+)?"
               r"(?:experience|service|tenure|expertise|in the|in banking|in financial|"
               r"with the|at the|leading|managing)", re.I),
    re.compile(r"\b(?:over|more than|nearly|almost)\s+(?:a|one|two|three|\d)\s+decades?\b", re.I),
    re.compile(r"\bdecades?\s+of\s+(?:experience|service)\b", re.I),
]
PERSONAL = [
    (re.compile(r"\b(date of birth|d\.?o\.?b\.?)\b", re.I), "date of birth"),
    (re.compile(r"\bborn\s+(?:on\s+|in\s+)?\d", re.I), "birth date"),
    (re.compile(r"\bmarital status\b|\b(married|single|divorced)\b\s*(\||$)", re.I),
     "marital status"),
    (re.compile(r"\bage\s*:\s*\d", re.I), "age"),
    (re.compile(r"\bnationality\s*:", re.I), "nationality"),
    (re.compile(r"\b(gender|religion)\s*:", re.I), "gender or religion"),
    (re.compile(r"!\[[^\]]*\]\("), "an image (a photo does not belong on the résumé)"),
]
CLEARED = re.compile(r"\b(security cleared|probity cleared|police check(ed)?|apra approved|"
                     r"eligible for (all )?(banking|background) checks)\b", re.I)
GAP = re.compile(r"\[[^\]\n]{2,}\](?!\()")


def words(text):
    return re.findall(r"[A-Za-z0-9$%][A-Za-z0-9$%'’.,/-]*", text)


class Report:
    def __init__(self):
        self.errors, self.warns, self.infos = [], [], []

    def error(self, code, msg):
        self.errors.append(f"ERROR {code}: {msg}")

    def warn(self, code, msg):
        self.warns.append(f"WARN  {code}: {msg}")

    def info(self, msg):
        self.infos.append(f"info  {msg}")

    def codes(self):
        return {ln.split()[1].rstrip(":") for ln in self.errors + self.warns}


def canonical(heading):
    h = heading.strip().lower()
    for key, names in SECTION_ALIASES.items():
        if h in names:
            return key
    return None


def parse(text):
    """Split the document into the name, the contact line and a list of sections."""
    lines = text.splitlines()
    doc = {"name": "", "contact": "", "sections": [], "lines": lines}
    cur = None
    seen_h1 = False
    for i, ln in enumerate(lines, 1):
        s = ln.rstrip()
        if s.startswith("# ") and not seen_h1:
            doc["name"], seen_h1 = s[2:].strip(), True
            continue
        if s.startswith("## "):
            cur = {"title": s[3:].strip(), "line": i, "body": []}
            doc["sections"].append(cur)
            continue
        if cur is None:
            if seen_h1 and s.strip() and not doc["contact"]:
                doc["contact"] = s.strip()
            continue
        cur["body"].append((i, s))
    return doc


def roles_of(section):
    """Group an experience section's body into employer headings and roles."""
    roles, cur, employer_intro = [], None, []
    in_employer = False
    for i, s in section["body"]:
        if s.startswith("#### "):
            cur = {"line": i, "head": s[5:].strip(), "paras": [], "bullets": []}
            roles.append(cur)
            in_employer = False
        elif s.startswith("### "):
            roles.append({"line": i, "head": s[4:].strip(), "employer": True,
                          "paras": [], "bullets": []})
            cur = roles[-1]
            in_employer = True
        elif cur is not None and s.startswith("- "):
            cur["bullets"].append((i, s[2:].strip()))
        elif cur is not None and s.strip():
            cur["paras"].append((i, s.strip()))
            if in_employer:
                employer_intro.append(s.strip())
    return roles


def lint(text, voice="first", summary_range=(60, 100), allow_gaps=False, year=None):
    r = Report()
    year = year or datetime.date.today().year
    doc = parse(text)
    body_text = "\n".join(doc["lines"])

    # --- name and contact line
    if not doc["name"]:
        r.error("no-name", "the first line should be '# Full Name'")
    if not doc["contact"]:
        r.error("no-contact-line", "no contact line under the name")
    elif re.search(r"\b\d{1,4}\s+[A-Z][a-z]+\s+(Street|St|Road|Rd|Avenue|Ave|Drive|Dr|Lane|"
                   r"Place|Crescent|Parade)\b", doc["contact"]):
        r.error("street-address", "the contact line carries a street address; city and state "
                                  "are enough")

    # --- sections: names and order
    found = []
    for sec in doc["sections"]:
        key = canonical(sec["title"])
        low = sec["title"].strip().lower()
        if low in BANNED_SECTIONS:
            r.error("section-not-wanted", f"line {sec['line']}: section '{sec['title']}' "
                                          "does not belong on the résumé")
        elif low in {"referees", "references"}:
            body = " ".join(s for _, s in sec["body"])
            if re.search(r"\b0\d[\d ]{7,}\b|@", body):
                r.error("referee-details", f"line {sec['line']}: referee contact details are "
                                           "supplied on request, not printed")
        elif key is None:
            r.warn("section-name", f"line {sec['line']}: '{sec['title']}' is not a standard "
                                   "heading a parser maps to a field")
        else:
            found.append((key, sec))
    keys = [k for k, _ in found]
    for need in ("summary", "skills", "experience"):
        if need not in keys:
            r.error("section-missing", f"no {need} section")
    ordered = [k for k in ORDER if k in keys]
    if keys != ordered:
        r.error("section-order", "sections should run summary, key skills, experience, "
                                 f"education; found {', '.join(keys)}")
    sec_of = dict(found)

    # --- summary
    if "summary" in sec_of:
        paras = [s for _, s in sec_of["summary"]["body"] if s.strip()]
        text_s = " ".join(paras)
        n = len(words(text_s))
        lo, hi = summary_range
        if n < lo - 20 or n > hi + 20:
            r.error("summary-length", f"summary is {n} words; the default is {lo} to {hi}")
        elif n < lo or n > hi:
            r.warn("summary-length", f"summary is {n} words; the default is {lo} to {hi}")
        if any(s.startswith("- ") for s in paras):
            r.warn("summary-bullets", "the summary is one paragraph of prose, not bullets")
        if voice == "first" and not re.search(r"\b(I|my|me)\b", text_s):
            r.warn("summary-person", "the summary has no 'I' or 'my'; paragraphs default to "
                                     "the first person (use --voice implied if the person "
                                     "chose otherwise)")
        r.info(f"summary: {n} words")

    # --- key skills
    if "skills" in sec_of:
        lines = [s for _, s in sec_of["skills"]["body"] if s.strip()]
        n = len(lines)
        if n < 2 or n > 5:
            r.warn("skills-lines", f"key skills has {n} line(s); the default is 2 to 4 "
                                   "labelled lines plus a tools line")
        unlabelled = [s for s in lines if not re.match(r"^(- )?[A-Z][A-Za-z ,&/-]{1,40}: ", s)]
        if unlabelled:
            r.warn("skills-label", f"{len(unlabelled)} skills line(s) have no 'Label: ' "
                                   "opening")
        if not any(re.match(r"^(- )?(Tools|Technology|Systems|Tools and systems)", s)
                   for s in lines):
            r.warn("skills-tools", "no Tools line; tools are a list and get their own line")
        if re.search(r"[█▓▒░●○★☆]|\b\d/5\b|\b\d{1,3}\s?%", " ".join(lines)):
            r.error("skills-ratings", "rating bars, stars or percentages in key skills")

    # --- experience
    all_bullets = []
    if "experience" in sec_of:
        roles = roles_of(sec_of["experience"])
        real_roles = [x for x in roles if not x.get("employer")]
        if not real_roles:
            r.error("no-roles", "no '#### Title | Employer | dates' role lines")
        for x in roles:
            head, line = x["head"], x["line"]
            parts = [p.strip() for p in head.split("|")]
            if not DATE_RANGE.search(head):
                if FULL_MONTH.search(head):
                    r.error("date-format", f"line {line}: write months as three letters, "
                                           "'Mon YYYY – Mon YYYY'")
                else:
                    r.error("date-format", f"line {line}: '{head}' needs dates as "
                                           "'Mon YYYY – Mon YYYY' or '– Present'")
            if not x.get("employer"):
                if len(parts) < 3:
                    r.warn("role-line", f"line {line}: role lines read 'Title | Employer | "
                                        "dates'; repeat the employer on each role")
                if re.search(r"\((promoted|promotion|secondment)[^)]*\)", head, re.I):
                    r.warn("role-line-note", f"line {line}: keep '(promoted)' out of the "
                                             "role line; say it in the employer sentences")
            all_bullets.extend(x["bullets"])
        for idx, x in enumerate(real_roles):
            nb = len(x["bullets"])
            if idx == 0:
                if nb and (nb < 3 or nb > 5):
                    r.warn("bullet-count", f"line {x['line']}: the current role has {nb} "
                                           "bullet(s); the default is 3 to 5")
                if not x["paras"]:
                    r.warn("no-scope", f"line {x['line']}: the current role has no scope "
                                       "paragraph before its bullets")
                scope = " ".join(p for _, p in x["paras"])
                if len(words(scope)) > 60:
                    r.warn("scope-length", f"line {x['line']}: the scope paragraph is "
                                           f"{len(words(scope))} words; the default is under "
                                           "about 50, with the detail in bullets")
            elif nb > 4:
                r.warn("bullet-count", f"line {x['line']}: an earlier role has {nb} bullets; "
                                       "the default is 1 to 4")
        dated = [x for x in real_roles if re.search(r"Present", x["head"])]
        if len(real_roles) == 1 and dated:
            m = re.search(r"(\d{4}) [–-] Present", real_roles[0]["head"])
            if m and year - int(m.group(1)) >= 8:
                r.warn("one-long-role", f"line {real_roles[0]['line']}: one role covering "
                                        f"{year - int(m.group(1))} years; date each role "
                                        "separately")

        # openers: bullets and paragraphs
        for i, b in all_bullets:
            first = re.sub(r"[^A-Za-z'-]", "", b.split()[0]) if b.split() else ""
            low = first.lower()
            if DUTY_OPENERS.match(b):
                r.warn("duty-opener", f"line {i}: '{' '.join(b.split()[:3])}…' describes a "
                                      "duty; a bullet is one thing that happened")
            elif low in BARE_PRESENT and low not in IRREGULAR_PAST - {"set", "cut", "put",
                                                                       "read", "split",
                                                                       "spread", "forecast",
                                                                       "reset", "shut",
                                                                       "hit", "let", "bid"}:
                r.error("bare-present", f"line {i}: bullet opens with the bare verb "
                                        f"'{first}', which reads as a command or a misspelt "
                                        "past tense")
            elif low == "i":
                r.warn("bullet-subject", f"line {i}: bullets open with a past-tense verb, "
                                         "without 'I'")
            elif not (low.endswith("ed") or low in IRREGULAR_PAST):
                r.warn("bullet-opener", f"line {i}: bullet opens with '{first}'; bullets "
                                        "open with a past-tense verb")
            if len(words(b)) > 75:
                r.warn("bullet-length", f"line {i}: bullet is {len(words(b))} words; one "
                                        "idea per bullet")
        for x in roles:
            for i, p in x["paras"]:
                first = re.sub(r"[^A-Za-z'-]", "", p.split()[0]).lower() if p.split() else ""
                if first in BARE_PRESENT and len(p.split()) > 3:
                    r.error("bare-present", f"line {i}: paragraph opens with the bare verb "
                                            f"'{p.split()[0]}'; write 'I {first}…' or recast")
    if "summary" in sec_of:
        for i, p in sec_of["summary"]["body"]:
            for sent in re.split(r"(?<=[.!?])\s+", p.strip()):
                if not sent:
                    continue
                first = re.sub(r"[^A-Za-z'-]", "", sent.split()[0]).lower()
                if first in BARE_PRESENT and len(sent.split()) > 3:
                    r.error("bare-present", f"line {i}: a summary sentence opens with the "
                                            f"bare verb '{sent.split()[0]}'")
                    break

    # --- the same story told in full twice
    if "summary" in sec_of and "experience" in sec_of:
        sw = [w.lower().strip(".,;:") for _, s_ in sec_of["summary"]["body"] for w in s_.split()]
        ex = " ".join(w.lower().strip(".,;:") for _, s_ in sec_of["experience"]["body"]
                      for w in s_.split())
        for k in range(len(sw) - 6):
            run = " ".join(sw[k:k + 7])
            if run in ex:
                r.warn("told-twice", f"the summary and the experience share the words '{run}'; "
                                     "name the proof in the summary and tell it once below")
                break

    # --- education
    if "education" in sec_of:
        lines = [(i, s) for i, s in sec_of["education"]["body"] if s.strip()]
        if not lines:
            r.error("education-empty", "the education section is empty; leave it out when "
                                       "there is nothing to list")
        for i, s in lines:
            if re.search(r"\b(Bachelor|Master|Diploma|Degree|BA|BSc|BCom|MBA|Graduate "
                         r"Certificate)\b", s):
                for y in re.findall(r"\b(19\d{2}|20\d{2})\b", s):
                    if year - int(y) > 10:
                        r.warn("graduation-year", f"line {i}: a graduation year of {y} is "
                                                  "an age signal; leave it off")

    # --- whole-document checks
    for i, ln in enumerate(doc["lines"], 1):
        for rx in YEARS_COUNT:
            m = rx.search(ln)
            if m:
                r.error("years-count", f"line {i}: '{m.group(0)}' counts years; the dates "
                                       "already show the tenure")
                break
        for rx, what in PERSONAL:
            if rx.search(ln):
                r.error("personal-detail", f"line {i}: {what} does not belong on the résumé")
        m = CLEARED.search(ln)
        if m:
            r.warn("cleared-claim", f"line {i}: '{m.group(0)}'; employers run their own "
                                    "checks, so this claims nothing")
        if re.match(r"^\s*\|.*\|\s*$", ln) and not ln.lstrip().startswith("#"):
            if re.search(r"\|\s*:?-{3,}", ln) or ln.count("|") >= 3 and i > 3:
                r.error("table", f"line {i}: a table; parsers lose text in tables")
        low = ln.lower()
        for c in CLICHES:
            if re.search(rf"(?<![a-z-]){re.escape(c)}(?![a-z-])", low):
                r.error("generic-register", f"line {i}: '{c}' reads as generic; say what "
                                            "happened instead")
                break
        if not ln.startswith("#") and FULL_MONTH.search(ln) and DATE_RANGE.search(ln) is None \
                and re.search(r"[–-]\s*(Present|\w+ \d{4})", ln):
            r.warn("date-format", f"line {i}: use three-letter months in date ranges")

    gaps = [(i, m.group(0)) for i, ln in enumerate(doc["lines"], 1) for m in GAP.finditer(ln)]
    if gaps:
        msg = f"{len(gaps)} gap marker(s), first at line {gaps[0][0]}: {gaps[0][1][:60]}"
        if allow_gaps:
            r.warn("gaps", msg + "; a document with gaps goes to the person, not an employer")
        else:
            r.error("gaps", msg + "; resolve them, or pass --allow-gaps for a draft")

    total = len(words(re.sub(r"^#+ ", "", body_text, flags=re.M)))
    r.info(f"{total} words, {len(all_bullets)} bullets")
    if total > 1100:
        r.warn("length", f"{total} words is more than two pages usually hold at 10.5pt")
    return r


def run_self_test():
    here = os.path.dirname(os.path.abspath(__file__))
    tests = os.path.join(here, "..", "tests")
    good = open(os.path.join(tests, "good.md"), encoding="utf-8").read()
    bad = open(os.path.join(tests, "bad.md"), encoding="utf-8").read()
    ok = True
    rg = lint(good, year=2026)
    if rg.errors:
        ok = False
        print("FAIL good.md should have no errors:")
        print("\n".join(rg.errors))
    else:
        print(f"ok   good.md: 0 errors, {len(rg.warns)} warning(s)")
    rb = lint(bad, year=2026)
    expected = {"years-count", "personal-detail", "bare-present", "generic-register",
                "date-format", "section-not-wanted", "education-empty", "gaps",
                "summary-length", "section-order", "referee-details", "duty-opener",
                "role-line", "skills-ratings", "table", "street-address"}
    missing = expected - rb.codes()
    if missing:
        ok = False
        print("FAIL bad.md did not raise: " + ", ".join(sorted(missing)))
    else:
        print(f"ok   bad.md: all {len(expected)} expected checks fired "
              f"({len(rb.errors)} errors, {len(rb.warns)} warnings)")
    r3 = lint(good.replace("I am the", "Am the", 1) + "\n", voice="implied", year=2026)
    print("ok   --voice implied accepted" if "summary-person" not in r3.codes()
          else "FAIL --voice implied still warns")
    ok = ok and "summary-person" not in r3.codes()
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--voice", choices=["first", "implied"], default="first",
                    help="person used in paragraphs (default: first)")
    ap.add_argument("--summary-words", default="60-100",
                    help="accepted summary length as min-max (default 60-100)")
    ap.add_argument("--allow-gaps", action="store_true",
                    help="report [gap] markers as warnings, for a draft going to the person")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        sys.exit(run_self_test())
    if not a.files:
        ap.error("give a résumé file, or --self-test")
    lo, hi = (int(x) for x in a.summary_words.split("-"))
    status = 0
    for path in a.files:
        text = open(path, encoding="utf-8").read()
        r = lint(text, voice=a.voice, summary_range=(lo, hi), allow_gaps=a.allow_gaps)
        print(f"== {path}")
        for ln in r.errors + r.warns + r.infos:
            print(ln)
        print(f"RESULT: {len(r.errors)} error(s), {len(r.warns)} warning(s)")
        if r.errors:
            status = 1
    sys.exit(status)


if __name__ == "__main__":
    main()
