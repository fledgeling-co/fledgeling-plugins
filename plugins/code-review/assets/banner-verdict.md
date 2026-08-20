This banner ships.

It is 3200x1040 from a 1600x520 layout at deviceScaleFactor 2, sets its wordmark
in Instrument Sans linked from Google Fonts rather than in a local face, and
displays the plugin's own icon.png inlined as a data URI rather than a redrawn
imitation of it. Every colour in the source is a constant lifted out of
build_icon.py: the porcelain ramp, the graphite ramp, the four-stop accent, the
seat edge, and the key light at 34% across and 26% down.

The device is the icon's move restated at banner width. A ledger's rows run up
to a column that has been cut clean out, and carry on past the gap. The rows on
the right side are the whole point of the composition and the one thing that
separates it from atlas-publish's banner, whose rails also end against a
vermilion vertical: a queue held at a gate stops, whereas a table with a column
removed continues, and continuing is what makes the gap read as an omission
rather than as a terminus.

Known liabilities. First, the essence line runs 60 characters and its bold half
is doing the semantic work, so at the 200px thumbnail only the wordmark
survives, which is the family norm but is worth knowing. Second, the device sits
in the upper band with the through-light glow alone occupying the lower right,
so the right half is deliberately unbalanced against the vertically centred
lockup; measured headroom between the lowest rail and the tagline's line box is
five pixels after the nudge, which is enough but is not much, and any future
lengthening of the tagline will collide before it overflows. The first draft did
collide, and render_banner.py reported no overflow while it did, because nothing
had left the frame.

## Alpha fringe, found after sign-off and fixed

Reported on the shipped banner: a dark hairline tracing the icon's squircle, with two short dashes
breaking the top edge at the shoulders. It was not a stroke and not a shadow. `icon.png` stored RGB
(0,0,0) in all 50,873 of its fully transparent pixels, which is invisible at 1:1 and harmless under
PIL, but the render engine downsamples 1024 to 576 device pixels in straight rather than
premultiplied alpha, so that black averaged into the silhouette's edge.

Measured on the banner itself, in the porcelain shoulder band above the graphite slab: 25 pixels
below luminance 200, minimum 191.2, before. Zero pixels below 200, minimum 231.6, after.

The fix floods the edge colour outward into the transparent region and never touches alpha, so the
icon is bit-identical everywhere it is actually visible; the script asserts both of those before it
writes. `icon-256.png` and `icon-128.png` carried the same defect (360 and 148 offending pixels) and
were fixed with it.

**This defect passed every check anyone made of it,** including `audit_sheet.py` and the first pass
of `banner_sheet.py`, because the icon file is correct at full size and the artifact only exists
after a downscale that nothing measured. It was found by a person looking at the banner.

