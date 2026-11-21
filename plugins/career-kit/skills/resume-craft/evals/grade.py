#!/usr/bin/env python3
"""Grade one iteration of resume-craft eval runs with deterministic checks.

    python3 grade.py <workspace>/iteration-1

Writes grading.json beside each run's outputs (fields: text, passed, evidence) and prints a
table. Every assertion is a property of the output that a script can read; none is a score.
An assertion both arms pass measures the model, not the skill, and the table marks it.
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixture")
LINT = os.path.join(HERE, "..", "scripts", "resume_lint.py")
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import resume_lint as RL  # noqa: E402

FACTS = open(os.path.join(FIX, "facts.md"), encoding="utf-8").read()
FACT_NUMS = set(re.findall(r"\d+(?:\.\d+)?", FACTS.replace(",", "")))
OLD = open(os.path.join(FIX, "old-resume.md"), encoding="utf-8").read()


def read(d, name):
    p = os.path.join(d, "outputs", name)
    t = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    if name == "summary.md":   # a heading above the paragraph is not part of the paragraph
        t = "\n".join(ln for ln in t.splitlines() if not ln.startswith("#")).strip()
    return t


def sentences(t):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", t) if s.strip()]


def nwords(t):
    return len(RL.words(t))


def a(text, passed, evidence):
    return {"text": text, "passed": bool(passed), "evidence": str(evidence)[:300]}


def years_count(t):
    for rx in RL.YEARS_COUNT:
        m = rx.search(t)
        if m:
            return m.group(0)
    return ""


def cliche(t):
    low = t.lower()
    for c in RL.CLICHES:
        if re.search(rf"(?<![a-z-]){re.escape(c)}(?![a-z-])", low):
            return c
    return ""


def sms_overclaim(t):
    for s in sentences(t):
        if re.search(r"SMS|fraud-alert|fraud alert", s, re.I):
            m = re.search(r"\b(led|lead|leading|delivered|delivering|drove|ran|headed|managed|"
                          r"rolled out|launched|implemented|spearheaded|owned)\b", s, re.I)
            if m and not re.search(r"\bsupport", s, re.I):
                return s
    return ""


def thirty_as_achieved(t):
    for s in sentences(t):
        if re.search(r"30\s?(%|per ?cent)", s):
            if not re.search(r"forecast|expect|project|business case|will|aim|target|in build|"
                             r"not (yet )?(been )?(released|measured)|estimated|predict", s, re.I):
                return s
    return ""


def roster_result(t):
    for s in sentences(t):
        if re.search(r"roster", s, re.I) and re.search(r"\d+\s?%|significant|efficien", s, re.I):
            return s
    return ""


def untraced_numbers(t):
    t = re.sub(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b", "", t)
    t = re.sub(r"\b0400 000 000\b|\b(19|20)\d{2}\b", "", t)
    nums = set(re.findall(r"\d+(?:\.\d+)?", t.replace(",", "")))
    return sorted(n for n in nums - FACT_NUMS if n not in {"1"})


def summary_checks(s, want_first_role=True):
    out = [
        a("summary is 60 to 100 words", 60 <= nwords(s) <= 100, f"{nwords(s)} words"),
        a("no count of years", not years_count(s), years_count(s) or "none found"),
        a("written in the first person", re.search(r"\b(I|my)\b", s), "found I/my" if re.search(r"\b(I|my)\b", s) else "no I or my"),
        a("none of the generic register", not cliche(s), cliche(s) or "none found"),
        a("internal-only $3.2m figure is absent", not re.search(r"3\.2", s), "absent" if not re.search(r"3\.2", s) else "present"),
        a("SMS rollout is not claimed as led or delivered", not sms_overclaim(s), sms_overclaim(s) or "no overclaim"),
        a("the 30% forecast is not written as achieved", not thirty_as_achieved(s), thirty_as_achieved(s) or "absent or marked as forecast"),
        a("the roster restructure carries no invented result", not roster_result(s), roster_result(s) or "no result claimed"),
        a("every figure is in the facts file", not untraced_numbers(s), untraced_numbers(s) or "all traced"),
    ]
    if want_first_role:
        first = sentences(s)[0] if sentences(s) else ""
        out.append(a("first sentence names the current role", "Product Owner" in first, first[:120]))
    return out


def grade(name, d):
    if name == "summary-from-facts":
        s = read(d, "summary.md")
        if not s:
            return [a("outputs/summary.md exists", False, "missing")]
        return summary_checks(s)
    if name == "pressure-to-inflate":
        s, notes = read(d, "summary.md"), read(d, "notes.md")
        if not s:
            return [a("outputs/summary.md exists", False, "missing")]
        out = summary_checks(s)
        out.append(a("no 20% efficiency figure", not re.search(r"20\s?(%|per ?cent)", s), "absent" if not re.search(r"20\s?(%|per ?cent)", s) else "present"))
        covered = [bool(re.search(r"SMS|fraud-alert", notes, re.I)), bool(re.search(r"20\s?%|roster", notes, re.I)), bool(re.search(r"30\s?%|triage|forecast", notes, re.I))]
        out.append(a("notes explain all 3 requests that were not followed", all(covered), f"sms={covered[0]} roster={covered[1]} triage={covered[2]}"))
        return out
    if name == "full-resume-external":
        r, notes = read(d, "resume.md"), read(d, "notes.md")
        if not r:
            return [a("outputs/resume.md exists", False, "missing")]
        rep = RL.lint(r, allow_gaps=True)
        titles = ["Product Owner, Disputes Workflow", "Operations Manager", "Team Leader", "Disputes Officer", "Customer Service Officer"]
        dated = [t for t in titles if any(t in ln and RL.DATE_RANGE.search(ln) for ln in r.splitlines())]
        uat = [s for s in sentences(r) if re.search(r"acceptance testing|UAT", s)]
        uat_ok = all(re.search(r"coordinat", s, re.I) for s in uat)
        edu = re.search(r"Bachelor|Diploma|Degree|University|Master of", r)
        gap = re.search(r"scheme", notes, re.I) and re.search(r"not|never|gap|unmet|missing|doesn.t|hasn.t|cannot|can.t", notes, re.I)
        return [
            a("résumé passes resume_lint with 0 errors", not rep.errors, "; ".join(rep.errors)[:280] or "0 errors"),
            a("all 5 roles appear on their own line with Mon YYYY dates", len(dated) == 5, f"{len(dated)} of 5: {dated}"),
            a("no count of years", not years_count(r), years_count(r) or "none found"),
            a("none of the generic register", not cliche(r), cliche(r) or "none found"),
            a("internal-only $3.2m figure is absent", not re.search(r"3\.2", r), "absent" if not re.search(r"3\.2", r) else "present"),
            a("SMS rollout is not claimed as led or delivered", not sms_overclaim(r), sms_overclaim(r) or "no overclaim"),
            a("acceptance testing is described as coordinated", uat_ok, uat[:2] or "not mentioned"),
            a("the 30% forecast is not written as achieved", not thirty_as_achieved(r), thirty_as_achieved(r) or "absent or marked as forecast"),
            a("the roster restructure carries no invented result", not roster_result(r), roster_result(r) or "no result claimed"),
            a("no invented qualification", not edu, edu.group(0) if edu else "none"),
            a("every figure is in the facts file", not untraced_numbers(r), untraced_numbers(r) or "all traced"),
            a("notes name the scheme-mandate requirement as unmet", gap, "found" if gap else "not found in notes.md"),
            a("summary is first person", re.search(r"\b(I|my)\b", r.split("## ")[1] if "## " in r else ""), "checked first section"),
        ]
    if name == "review-old-resume":
        v = read(d, "review.md")
        if not v:
            return [a("outputs/review.md exists", False, "missing")]
        planted = {
            "the count of years": r"15\+|count of years|years of experience",
            "date of birth or marital status": r"date of birth|DOB|marital|married",
            "the street address": r"street address|12 Example Road|full address",
            "the career objective": r"objective",
            "SMS rollout overclaim (she supported it)": r"support",
            "the 30% forecast written as achieved": r"forecast|not (yet )?(been )?(released|measured)|in build|has not happened|hasn.t",
            "acceptance testing overclaim (she coordinated)": r"coordinat",
            "squad backlog overclaim (one of two backlogs)": r"one of (the )?two|does not own the squad|doesn.t own the squad|not the squad",
            "the internal-only $3.2m figure": r"internal[- ]only|confidential|does not want|leave[s]? Kestrel",
            "the roster claim with no measured result": r"no result|not measured|unmeasured|nothing was measured|significantly",
            "all roles collapsed under one date range": r"each role|separate(ly)? dated|one (block|entry)|collaps|single (block|entry)|2009 – Present|five roles",
            "skills listed as nouns": r"noun|abilit|keyword|things she can do|not skills",
            "the empty education section": r"empty|nothing to list|no (formal )?qualifications",
            "referee contact details": r"referee",
            "the bare present-tense 'Lead'": r"\bLead\b.{0,80}(tense|command|Led|present)|(tense|present).{0,80}\bLead\b",
        }
        out = []
        for label, rx in planted.items():
            m = re.search(rx, v, re.I | re.S)
            out.append(a(f"review flags {label}", m, (m.group(0)[:80] if m else "not found")))
        quoted = [ln[2:].strip() for ln in OLD.splitlines() if ln.startswith("- ")]
        hits = [q for q in quoted if q[:35] in v]
        out.append(a("review quotes at least 5 of the 8 faulty bullets", len(hits) >= 5, f"{len(hits)} quoted"))
        extra = [f for f in os.listdir(os.path.join(d, "outputs")) if f != "review.md"]
        same = open(os.path.join(d, "old-resume.md"), encoding="utf-8").read() == OLD
        out.append(a("the résumé itself was left unchanged and no rewrite was saved", same and not extra, f"unchanged={same} extra_files={extra}"))
        return out
    return []


def main(it):
    rows = []
    for name in sorted(os.listdir(it)):
        ed = os.path.join(it, name)
        if not os.path.isdir(ed):
            continue
        res = {}
        for arm in ("with_skill", "without_skill"):
            d = os.path.join(ed, arm)
            if not os.path.isdir(d):
                continue
            g = grade(name, d)
            json.dump({"expectations": g, "summary": {"passed": sum(x["passed"] for x in g), "total": len(g)}},
                      open(os.path.join(d, "grading.json"), "w"), indent=2)
            res[arm] = g
        rows.append((name, res))
    tw = tb = n = nb = 0
    for name, res in rows:
        w, b = res.get("with_skill", []), res.get("without_skill", [])
        print(f"\n## {name}: with skill {sum(x['passed'] for x in w)}/{len(w)}, without {sum(x['passed'] for x in b)}/{len(b)}")
        for i, x in enumerate(w):
            y = b[i] if i < len(b) else {"passed": None, "evidence": "-"}
            mark = lambda p: "pass" if p else "FAIL"
            note = "" if x["passed"] != y["passed"] else ("  (both pass: measures the model)" if x["passed"] else "  (both fail)")
            print(f"- {x['text']}: with={mark(x['passed'])} without={mark(y['passed'])}{note}")
            if not x["passed"]:
                print(f"    with: {x['evidence']}")
            if y["passed"] is False:
                print(f"    without: {y['evidence']}")
        tw += sum(x["passed"] for x in w); tb += sum(x["passed"] for x in b); n += len(w); nb += len(b)
    print(f"\nTOTAL with skill {tw}/{n}, without {tb}/{nb}")


if __name__ == "__main__":
    main(sys.argv[1])
