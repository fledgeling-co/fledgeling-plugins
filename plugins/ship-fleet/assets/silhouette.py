#!/usr/bin/env python3
"""silhouette.py — rubric #3 check: is the glyph nameable as a filled solid?

Takes icon.svg, keeps the mid (berth structure) and fg (vessels) layers, flattens
every fill and stroke to black on a white tile, and drops shadows/filters so the
mass is the shape and nothing else.  Renders to silhouette.png.
"""
import pathlib, re, subprocess

src = pathlib.Path("icon.svg").read_text()
defs = re.search(r"<defs>.*?</defs>", src, re.S).group(0)


def layer(name):
    m = re.search(rf'<g id="{name}">(.*?)</g>\n', src, re.S)
    body = m.group(1)
    body = re.sub(r'\s*filter="url\(#(soft|tight|mist)\)"', "", body)
    body = re.sub(r'fill="(?!none)[^"]+"', 'fill="#000"', body)
    body = re.sub(r'stroke="(?!none)[^"]+"', 'stroke="#000"', body)
    body = re.sub(r'(fill|stroke)-opacity="[^"]+"', r'\1-opacity="1"', body)
    return body


out = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" '
       'width="1024" height="1024">' + defs +
       '<rect width="1024" height="1024" fill="#fff"/>'
       '<g clip-path="url(#sq)">' + layer("mid") + layer("fg") + "</g></svg>")
pathlib.Path("silhouette.svg").write_text(out)
subprocess.run(["rsvg-convert", "-w", "512", "-h", "512", "silhouette.svg",
                "-o", "silhouette.png"], check=True)
print("wrote silhouette.svg + silhouette.png")
