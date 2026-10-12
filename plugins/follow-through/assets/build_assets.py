#!/usr/bin/env python3
"""Render the bundled squircle and loop/check metaphor. Requires Pillow."""
import math
from pathlib import Path
import re
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent


def squircle():
    commands = re.findall(r"([MCZ])([^MCZ]*)", (ROOT / "squircle-path.txt").read_text())
    points = []
    current = (0, 0)
    for command, body in commands:
        values = [float(v) for v in re.findall(r"-?\d+(?:\.\d+)?", body)]
        if command == "M":
            current = tuple(values[:2]); points.append(current)
        elif command == "C":
            for start in range(0, len(values), 6):
                p1, p2, p3 = [tuple(values[start + i:start + i + 2]) for i in (0, 2, 4)]
                for step in range(1, 13):
                    t = step / 12; u = 1 - t
                    points.append(tuple(u**3 * current[i] + 3*u*u*t*p1[i] + 3*u*t*t*p2[i] + t**3*p3[i] for i in (0, 1)))
                current = p3
    return points


def build():
    icon = Image.new("RGBA", (1024, 1024))
    draw = ImageDraw.Draw(icon)
    draw.polygon(squircle(), fill="#182e3d")
    draw.arc((226, 226, 798, 798), 42, 318, fill="#dce8e7", width=72)
    draw.polygon([(815, 322), (690, 354), (753, 457)], fill="#dce8e7")
    draw.line([(389, 523), (479, 617), (677, 400)], fill="#edaa67", width=70, joint="curve")
    for name, size in [("icon.png", 1024), ("icon-256.png", 256), ("icon-128.png", 128)]:
        icon.resize((size, size), Image.Resampling.LANCZOS).save(ROOT / name)
    banner = Image.new("RGB", (1600, 520), "#182e3d")
    banner.paste(icon.resize((360, 360), Image.Resampling.LANCZOS), (95, 80), icon.resize((360, 360), Image.Resampling.LANCZOS))
    draw = ImageDraw.Draw(banner)
    font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
    title = ImageFont.truetype(font_path, 90)
    body = ImageFont.truetype(font_path, 30)
    draw.text((510, 177), "Follow through", font=title, fill="#f1f4ef")
    draw.text((515, 300), "Evidence. Next action. Verified outcome.", font=body, fill="#dce8e7")
    banner.save(ROOT / "banner.png")


if __name__ == "__main__":
    build()
