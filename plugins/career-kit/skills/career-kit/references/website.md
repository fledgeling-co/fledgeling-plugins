# The personal website

A site that is obviously bespoke does a job a PDF cannot: it shows judgement. A site that looks
like a template does the opposite, so the design work is the point rather than decoration.

## References before layout

Consult shipped work rather than inventing a structure. Through the router:
`mobbin__search_screens`, `mobbin__search_sections`, `mobbin__search_flows` (harness prefix
`mcp__router__`, arguments `query`, `limit`, `platform`, `image_format`). Record which products
and which patterns you took — the source session used three, named in its notes, and that
record is what lets a later session stay consistent with the first.

Build through `design-craft:design-craft` and `ux-craft:ux-craft` together; they are a standing
pair rather than alternatives. `motion-craft:motion-craft` for a scroll story.

Imagery through `media-gen-pro__generate_image` (arguments `prompt`, `context`, `aspectRatio`,
`n`, `outputDir`, `basename`, optional `style`, `referenceImages`, `seed`). The server reports
which model served the request. Caption a generated image on the page as generated. Where the
choice between concepts is real, generate several, tile them into one contact sheet, and put
the sheet to a panel — then let the person choose, because this axis is theirs.

## GSAP and three.js where they earn their place

Use them for something the content needs: a timeline that assembles as you reach it, a figure
that responds to the pointer. Not for motion on every element.

Every effect needs a real path for someone without WebGL, with `prefers-reduced-motion`, or on
a touch device — a control that swaps the content, not a feature that silently is not there.
Both states need alt text and both need to be reachable by keyboard.

Pause rendering off-screen and cap `devicePixelRatio` at 2.

## Iterating on an effect

The source session's hero image went through six rounds in an afternoon: one image, a second
image revealed under the pointer, a trail, seven selectable effects, a water simulation the owner
said looked like jelly, and finally one image that grows slightly on hover. The end state was
simpler than the start.

- Show the idea cheaply first: a still, a short screen recording, or the effect on a local page.
  Build it into the site after the person has seen it.
- Keep the plain version working the whole time, so going back is one edit.
- After two iterations on one effect, offer the plain version again alongside the next attempt.
- A chooser between options is a review tool. Keep it in one removable block of markup, CSS and
  script, serve it locally, and take it out before any deploy.
- State after every iteration what a headless browser could not show: touch drag against page
  scroll, a real phone, Safari, a device without float textures.
- A caption saying what an image stands for is copy about the person. Ground it in the notes and
  check it against the picture; the first one drafted described the image wrongly. Whether a
  generated image carries a credit is the person's choice.

## Checking it

```bash
python3 -m http.server 8943 --bind 127.0.0.1 --directory site &
node scripts/shoot.mjs http://127.0.0.1:8943/ 1280 900 /tmp/site top=0 work=sel:#work
node scripts/shoot.mjs http://127.0.0.1:8943/ 390 844 /tmp/phone top=0 work=sel:#work
```

Chrome's own `--screenshot` captures scroll 0 and nothing else, so a scroll-driven page reports
as fine while everything below the fold is unverified. `shoot.mjs` eases to each position so
reveal animations fire, prints `scrollWidth` against `innerWidth` (the horizontal-overflow
check), and collects console errors.

Then read the PNGs. Run `design-review:design-review` on the served page for the contrast,
target-size and semantics gates.

Headless engines without 3D support report a console error on a WebGL page. That is the engine,
not the page — confirm by loading it in a real browser before changing anything.

Note what nobody looked at. The source session never saw its site on a real phone or in Safari,
and said so.

## Deploying

Only when the person says so. An unlisted address with a `noindex` header is still public: it
returns 200 to anyone who has the URL, and a page carrying figures the person restricted is a
breach whether or not it is linked. Check what a deployed page actually serves:

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://<the-site>/
curl -s https://<the-site>/ | grep -c "<a restricted figure>"
```

Check the visibility the person asked for before making the site easier to find. A domain made
of their own name is guessable, and a site meant to stay unlisted until a hiring process ends is
less hidden once it has one. Say so before attaching it. Keep private pages, such as interview
practice, off the public deployment.

## A custom domain

Registering a domain spends their money. Ask, and do not assume a stored balance is authority.
In the source session buying one took four turns because nothing was checked first. Before
offering to buy, check all of these and show them together:

1. The name is available, and its price.
2. The registrar balance covers it.
3. A complete registrant contact exists: name, postal address, phone, email. Ask once and record
   where it came from. The registrar tools may have no way to read the contact on another domain.
4. Whose name it will be registered in. The person it is about and the person helping are
   different legal owners; ask.
5. The email on the registration is one the owner reads. The registrar sends a verification link
   there, and an unverified domain is suspended after about two weeks.

Take a credential only from the secrets broker or with the owner's explicit say-so. When the
tools at hand cannot do a step, say which step and what would unblock it.

After buying: attach the apex and `www` to the host, replace the registrar's parking records with
the host's records without overwriting the zone, and report four separate states — attached, DNS
set, resolving, certificate issued. "Set" and "working" were several minutes apart; check with an
HTTPS request to the domain and do not report it as live before that returns 200. A local resolver
can keep serving the old parking record for the length of its TTL after the authoritative servers
are correct.

Put the verification email on the list of things waiting on the person.

## A generated video hero

When the person wants motion and a shader is more than the page needs, a short generated clip
works: muted, autoplaying, `playsinline`, no controls, played once and held on the last frame.

- Generate the still first and wait for the person's OK before any video call. Video is billed
  per clip and costs far more than an image.
- Image-to-video keeps objects consistent only from a first frame. To show things settling into
  an arrangement, generate the settled arrangement as the still, animate it coming apart, and
  reverse the clip with `ffmpeg -vf reverse`.
- Use a 16:9 source. A 3:1 source produced no file in the source session.
- A router or gateway can time out while the job carries on. Wait several minutes for the file
  before retrying, or the clip is billed twice.
- Set the first frame as the poster. Under `prefers-reduced-motion`, or when `play()` is
  refused, show the last frame as a still.
- Do not set `width` and `height` attributes that fight the CSS aspect ratio; on a phone they
  produced a tall, zoomed crop.
- Safari plays video only from a server that answers range requests. A local file and
  `python3 -m http.server` both fail; the deployed host does not.
- Ask what the picture might be taken to mean. A grid of objects sorted by size read to the
  person as "a banner for autism", which was not the association wanted on a profile page.

## The site address on the résumé

Printing the address on the résumé sends the résumé's readers to the site. Before that
happens, check every other path on the same domain. The source session had a private
interview-prep page at an unlinked path carrying the three figures the person kept off public
pages; the fix was to soften those figures at build time, with the build failing if one
remained.
