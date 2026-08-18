Ships, after a re-render forced by the icon rebuild.

The composition was already sound and did not need recolouring: its graphite (#2E343D through #434A55), vermilion (#D33C21, #EC5A33) and porcelain (#FAF8F2 through #E5E1D4) sit inside the ranges the new master's own constants define, because the new icon moved from a pale dial to a graphite rail with a vermilion shim and landed in the palette the banner already had. Only the artwork changed.

The right-hand seal rows bleed off the frame at `right: -60px` under `overflow: hidden`, and that is deliberate: the state reads as continuing past the window, which is what a watcher does. Two of the rows are lit and the rest are inert, so the accent still marks change rather than decorating the field. The wordmark's hyphen is a vermilion seal, which ties the mark to the icon's shim without spending the accent twice on anything semantic.

Known liabilities. The lit rows are the only place the accent appears at 400px, and at 200px they merge into a single warm smear, so the card-width read is carried by the icon alone. The icon's steel saddle, which its own audit sheet names as its weakest element at 2.92:1, is the first thing to disappear here too at the smaller widths. Rows 5, 6, 8, 9, 10 and 11 are one person's assessment rather than a panel's.

Two checker bugs were found by rendering this banner rather than by reasoning about it, and both are fixed rather than worked around.

`render_banner.py` refused the render, reporting that content ran past the frame and would be cropped. Every flagged node was an empty decorative div or span, and the assertion's own stated purpose is that no *text* is cropped. It now ignores elements with no text of their own, checking own text rather than descendants' so a wrapper does not inherit the blame for a child that fits. Proved still able to bite: a deliberately overflowing text node is caught and named.

`banner_sheet.py` reported an em dash in this banner's copy. It was inside a long HTML comment documenting this engine's rendering traps, so the checker was crying wolf about the author's own notes. It now strips comments before tags, and still fails on a real em dash in visible copy.
