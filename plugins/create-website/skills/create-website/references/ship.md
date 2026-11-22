# Shipping: deploy, visibility and a custom domain

Nothing here runs until the person says so. Deploying, attaching a domain, buying one and
publishing are each their own say-so; approval for one is not approval for the next. Sources for
each rule are in `evidence.md` under "Deploy".

## Before the first deploy

1. `python3 scripts/site_audit.py site/ --deploy [--private .create-website/private.txt]` exits 0.
   `--deploy` fails on any review tool left in the build; `--private` fails on any listed string
   in the visible text, read from what a person sees rather than the page source, where a search
   once matched restricted figures inside font weights and pixel values.
2. Ask what visibility the person wants: public, unlisted, or private. Say plainly that unlisted
   is public.

## Unlisted is public

An address with a `noindex` header still answers 200 to anyone who has it. `noindex` asks
search engines not to list a page and stops nobody from reading it, and a crawler has to be
allowed to fetch the page to see the rule at all. Subdomains are not hidden either: every
certificate a public authority issues, including the Let's Encrypt certificates Vercel and
Netlify use, is published to Certificate Transparency logs, and scanners watch those logs. A
link pasted into a chat app is fetched at once by its preview bot.

A private site needs access control on the host, checked from outside:

| Host | What protects it | What does not |
|---|---|---|
| Vercel | Deployment Protection. Standard Protection covers preview and generated deployment URLs and leaves production domains open; "All Deployments" covers production too. Password protection is a paid option. | The automatic `noindex` on preview URLs |
| Netlify | Project visibility (private access through Netlify login) or password protection, set per team and context | The `noindex` on deploy previews; the latest deploy of a branch is not marked `noindex` at all |

Then verify as a stranger, with no cookies:

```bash
python3 scripts/deploy_check.py access https://<host>/ https://<host>/media/hero.mp4 --expect private
```

Every URL must answer 401 or 403, or redirect to a login on another host. Pass direct media and
image URLs, and the provider's own aliases (`*.vercel.app`, `*.netlify.app`): a protected page can
still serve its assets openly.

## Check every path before the address goes anywhere

```bash
python3 scripts/deploy_check.py paths https://<the-site>/ [--private .create-website/private.txt]
python3 scripts/deploy_check.py media https://<the-site>/media/hero.mp4 https://<the-site>/media/hero-phone.mp4
```

`paths` crawls robots.txt, the sitemap, every same-origin link and the paths people leave behind
(`/admin`, `/preview`, `/draft`, `/practice` and others), reports each status and whether it
sends `noindex`, and fails on a private string served anywhere. The source session had a private
page at an unlinked path carrying three figures the owner kept off public pages. Keep private
pages off the public deployment entirely. `media` requires 206 with a matching `Content-Range` for
each video, because Safari has refused to play video from servers that ignore range requests.

## Buying a domain

Registering a domain spends the person's money; a stored registrar balance is not authority. In
the source session buying one took four turns because nothing was checked first. Check all of
these and show them together before offering:

1. The name is available, and its price for the first year and on renewal.
2. The registrar balance covers it.
3. A complete registrant contact exists: name, postal address, phone, email. Ask once and record
   where it came from.
4. Whose name it is registered in. The person the site is about and the person helping are
   different legal owners.
5. The email on the registration is one the owner reads. The registrar sends a verification link
   there, and an unverified domain is suspended after about two weeks. Put that email on the list
   of things waiting on the person.

A domain made of someone's own name is guessable, so a site meant to stay quiet is less hidden
once it has one. Say so before attaching it.

## Attaching a domain: five states, reported separately

"Set" and "working" were several minutes apart in the source session. Report each state on its
own line and call the domain live only when the HTTPS request returns 200.

| State | How to read it |
|---|---|
| 0 Attached to the project | The host's dashboard or CLI; not visible from outside |
| 1 DNS set and resolving | `deploy_check.py domain <name> --expect-host <target>`: the apex A record and the `www` CNAME point where the host says. Use the project-specific records the host shows rather than remembered addresses |
| 2 HTTPS answers 200 | Same command |
| 3 Certificate issued | Same command: a certificate valid for the name, with its expiry. Issuance follows successful DNS verification |
| 4 Canonical redirect | `curl -sI https://<apex>/`: one hop to the canonical host, 301 or 308. The script does not check this one |

Replace the registrar's parking records with the host's records without overwriting the rest of
the zone. Three things stall a certificate, and `domain` lists the records behind the first two:
a stale AAAA record left from an old host (the authority tries IPv6 first and reaches the old
server), a CAA record that does not allow `letsencrypt.org`, and a proxy such as Cloudflare's
intercepting `/.well-known/acme-challenge/`. A wildcard needs DNS-01, which means delegating
nameservers to the host or adding the `_acme-challenge` TXT record. A local resolver can serve
the old parking record for its TTL after the authoritative servers are correct, so a failure
right after a change is not final; check again before reporting it.

When the tools at hand cannot do a step, say which step and what would unblock it.

## Writing to the person

The reply and any checklist the person receives speak in their terms: what is public, what is
protected, what it costs, what they need to decide. Keep script names, state numbers and file
paths from this skill's run in `.create-website/`, not in the person's checklist. In a test run a
blind judge marked a deploy checklist down for telling the owner to run internal scripts and for
talking about her in the third person.
