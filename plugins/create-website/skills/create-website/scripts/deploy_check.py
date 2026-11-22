#!/usr/bin/env python3
"""Check what a deployed site actually serves, and the state of a custom domain.

    python3 deploy_check.py paths https://example.com [--private private.txt] [--max 200]
    python3 deploy_check.py domain example.com [--expect-host cname.vercel-dns.com]
    python3 deploy_check.py media  https://example.com/media/hero.mp4 [more URLs]
    python3 deploy_check.py access https://preview.example.com [asset URLs] --expect private

paths   list every path the host serves on that origin: the sitemap, robots.txt, every same-origin
        link reachable from the home page, and a handful of paths people leave behind (/admin,
        /preview, /draft, /test, /practice, /old). Report each status code, whether it sends
        noindex, and, with --private, any listed string in the visible text of a 200 page. An
        unlisted page with a noindex header still returns 200 to anyone with the address; the
        source session had a private practice page at an unlinked path on the same domain carrying
        three figures the owner kept off public pages. Run this before the site's address goes on
        anything. Exit 1 if a private string is served.
domain  report the four states separately, because "set" and "working" were several minutes apart:
        1 resolving (DNS answers, and points at --expect-host when given), 2 HTTPS answers 200,
        3 certificate valid for the name, with its expiry. "Attached to the project" is the host's
        own state: read it in the host's dashboard or CLI; this script cannot see it. A local
        resolver can serve an old parking record for its TTL after the authoritative servers are
        correct, so a failure right after a DNS change is not final. Exit 1 unless 1-3 all pass.
        Also lists AAAA and CAA records, the two that most often stall a certificate: a stale AAAA
        left from an old host is tried first by the certificate authority, and a CAA record that
        does not allow letsencrypt.org refuses the issue outright.
media   ask each video URL for its first 100 bytes and require 206 Partial Content with a matching
        Content-Range and 100 bytes back. Safari has refused to play video from servers that ignore
        range requests, python3 -m http.server among them; Accept-Ranges alone proves nothing.
        Exit 1 on any URL that answers otherwise.
access  request each URL with no cookies or credentials, as a stranger would. With --expect
        private, every URL must answer 401 or 403 or redirect to a login on another host; a 200 is
        a page anyone can read, and noindex does not change that. Pass the direct media and image
        URLs too: a protected page can still serve its assets openly. With --expect public, every
        URL must answer 200. Exit 1 on any mismatch.
"""
import argparse
import html
import re
import socket
import ssl
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

LEFTOVERS = ["/admin", "/preview", "/draft", "/test", "/practice", "/old", "/staging", "/private", "/index-old.html"]
UA = "create-website-deploy-check/1.0"


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers={"user-agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read(2_000_000).decode("utf-8", errors="replace")
            return r.status, dict(r.headers), body, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), "", url
    except Exception as e:  # network failure is a result, not a crash
        return None, {}, str(e), url


def visible_text(body):
    body = re.sub(r"<(script|style|noscript)\b.*?</\1>", " ", body, flags=re.S | re.I)
    return html.unescape(re.sub(r"<[^>]+>", " ", body))


def paths(base, private=(), limit=200):
    origin = "{0.scheme}://{0.netloc}".format(urlparse(base))
    seen, queue, rows, leaks = set(), [base], [], []
    status, _, robots, _ = fetch(urljoin(origin, "/robots.txt"))
    if status == 200:
        queue += [urljoin(origin, m) for m in re.findall(r"(?im)^(?:dis)?allow:\s*(\S+)", robots) if m != "/"]
    status, _, sm, _ = fetch(urljoin(origin, "/sitemap.xml"))
    if status == 200:
        queue += re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sm)
    queue += [urljoin(origin, p) for p in LEFTOVERS]
    while queue and len(seen) < limit:
        url = queue.pop(0).split("#")[0]
        if url in seen or urlparse(url).netloc != urlparse(origin).netloc:
            continue
        seen.add(url)
        status, headers, body, final = fetch(url)
        robots_hdr = {k.lower(): v for k, v in headers.items()}.get("x-robots-tag", "")
        noindex = "noindex" in robots_hdr.lower() or bool(re.search(r"<meta[^>]+noindex", body, re.I))
        rows.append((status, url, noindex))
        if status == 200 and "html" in {k.lower(): v for k, v in headers.items()}.get("content-type", "html"):
            text = visible_text(body)
            for s in private:
                if s and s in text:
                    leaks.append((url, s))
            for href in re.findall(r"""href=['"]([^'"]+)['"]""", body):
                nxt = urljoin(final, href)
                if urlparse(nxt).netloc == urlparse(origin).netloc and not re.search(r"\.(png|jpe?g|webp|avif|svg|mp4|webm|css|js|ico|woff2?)(\?|$)", nxt):
                    queue.append(nxt)
    return rows, leaks


def domain(name, expect_host=None):
    states = {}
    try:
        addrs = sorted({a[4][0] for a in socket.getaddrinfo(name, 443)})
        states["1 resolving"] = (True, ", ".join(addrs))
        if expect_host:
            out = subprocess.run(["dig", "+short", "CNAME", name], capture_output=True, text=True).stdout.strip()
            target_ips = sorted({a[4][0] for a in socket.getaddrinfo(expect_host, 443)}) if out == "" else []
            ok = expect_host.rstrip(".") in out or (target_ips and set(target_ips) & set(addrs))
            states["1 resolving"] = (bool(ok), f"{', '.join(addrs)} (CNAME: {out or 'none'}; expected {expect_host})")
    except socket.gaierror as e:
        states["1 resolving"] = (False, str(e))
    status, _, body, final = fetch(f"https://{name}/")
    states["2 https 200"] = (status == 200, f"status {status} at {final}" if status else body[:160])
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((name, 443), timeout=15) as sock, ctx.wrap_socket(sock, server_hostname=name) as s:
            cert = s.getpeercert()
        exp = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        states["3 certificate"] = (True, f"valid for {name}, expires {exp.date().isoformat()}")
    except Exception as e:
        states["3 certificate"] = (False, str(e)[:200])
    states["0 attached to the host project"] = (None, "read it in the host's dashboard or CLI; not visible from outside")
    aaaa, caa = records(name, "AAAA"), records(name, "CAA")
    if aaaa is not None:
        states["4 AAAA records"] = (None, ", ".join(aaaa) or "none")
    if caa is not None:
        allows = not caa or any("letsencrypt.org" in r for r in caa)
        states["5 CAA records"] = (None if allows else False, (", ".join(caa) or "none (any authority may issue)")
                                   + ("" if allows else "; letsencrypt.org is not allowed, so the host cannot issue"))
    return states


def records(name, kind):
    try:
        out = subprocess.run(["dig", "+short", kind, name], capture_output=True, text=True, timeout=15).stdout
    except (OSError, subprocess.TimeoutExpired):
        return None
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def media(url):
    req = urllib.request.Request(url, headers={"user-agent": UA, "range": "bytes=0-99"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read(200)
            cr = r.headers.get("content-range", "")
            ok = r.status == 206 and cr.startswith("bytes 0-99/") and len(body) == 100
            return ok, f"status {r.status}, Content-Range '{cr or 'none'}', {len(body)} bytes"
    except urllib.error.HTTPError as e:
        return False, f"status {e.code}"
    except Exception as e:
        return False, str(e)[:160]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def access(url, expect):
    opener = urllib.request.build_opener(NoRedirect)
    try:
        r = opener.open(urllib.request.Request(url, headers={"user-agent": UA}), timeout=20)
        status, loc = r.status, ""
    except urllib.error.HTTPError as e:
        status, loc = e.code, (e.headers or {}).get("location", "")
    except Exception as e:
        return False, str(e)[:160]
    if expect == "public":
        return status == 200, f"status {status}"
    to_login = 300 <= status < 400 and urlparse(urljoin(url, loc)).netloc != urlparse(url).netloc
    return status in (401, 403) or to_login, f"status {status}" + (f" -> {loc}" if loc else "")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("paths"); p.add_argument("url"); p.add_argument("--private"); p.add_argument("--max", type=int, default=200)
    d = sub.add_parser("domain"); d.add_argument("name"); d.add_argument("--expect-host")
    m = sub.add_parser("media"); m.add_argument("urls", nargs="+")
    c = sub.add_parser("access"); c.add_argument("urls", nargs="+")
    c.add_argument("--expect", choices=["private", "public"], required=True)
    a = ap.parse_args()
    if a.cmd in ("media", "access"):
        bad = 0
        for u in a.urls:
            ok, detail = media(u) if a.cmd == "media" else access(u, a.expect)
            bad += not ok
            print(f"{'PASS' if ok else 'FAIL'}  {u}: {detail}")
        what = "answer range requests with 206" if a.cmd == "media" else f"behave as {a.expect}"
        print(f"RESULT: {len(a.urls) - bad} of {len(a.urls)} URL(s) {what}")
        return 1 if bad else 0
    if a.cmd == "paths":
        private = [ln.strip() for ln in open(a.private, encoding="utf-8") if ln.strip()] if a.private else []
        rows, leaks = paths(a.url, private, a.max)
        for status, url, noindex in rows:
            print(f"{status or 'ERR':>4}  {'noindex ' if noindex else '        '}{url}")
        for url, s in leaks:
            print(f"FAIL  private string '{s}' served at {url}")
        live = [u for st, u, _ in rows if st == 200]
        print(f"RESULT: {len(rows)} path(s) checked, {len(live)} answer 200, {len(leaks)} private leak(s). Every 200 is public to anyone with its address, noindex or not.")
        return 1 if leaks else 0
    states = domain(a.name, a.expect_host)
    for k in sorted(states):
        ok, detail = states[k]
        print(f"{'PASS' if ok else 'n/a ' if ok is None else 'FAIL'}  {k}: {detail}")
    return 0 if all(v[0] for k, v in states.items() if v[0] is not None) else 1


if __name__ == "__main__":
    sys.exit(main())
