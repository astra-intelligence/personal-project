#!/usr/bin/env python3
"""Render the 1200x630 Open Graph / social preview image for the site.

Reproducible from source: run `python scripts/render-og-image.py` to regenerate
`public/og-image.png` whenever the copy or brand changes.
"""
from __future__ import annotations

import math

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1200, 630
BG = (10, 11, 13)  # #0a0b0d
ACCENT = (99, 102, 241)  # indigo-500
ACCENT2 = (124, 58, 237)  # violet-600
TEXT = (238, 240, 244)  # #eef0f4
MUTED = (148, 163, 184)  # slate-400

FONT_NAME = "/home/paperclip/.fonts/Montserrat-ExtraBold.ttf"
FONT_TAG = "/usr/share/fonts/truetype/lato/Lato-Regular.ttf"
LOGO = "public/logo.png"
OUT = "public/og-image.png"


def draw_grid(draw: ImageDraw.ImageDraw) -> None:
    step = 60
    for x in range(0, W, step):
        draw.line([(x, 0), (x, H)], fill=(255, 255, 255, 6), width=1)
    for y in range(0, H, step):
        draw.line([(0, y), (W, y)], fill=(255, 255, 255, 6), width=1)


def radial_glow(size: tuple[int, int], center: tuple[int, int], radius: int) -> Image.Image:
    glow = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(glow)
    for i in range(radius, 0, -8):
        alpha = int(28 * (1 - i / radius))
        d.ellipse(
            [center[0] - i, center[1] - i, center[0] + i, center[1] + i],
            fill=(ACCENT[0], ACCENT[1], ACCENT[2], alpha),
        )
    return glow.filter(ImageFilter.GaussianBlur(40))


def main() -> None:
    img = Image.new("RGBA", (W, H), BG + (255,))
    draw_grid(ImageDraw.Draw(img))
    img.alpha_composite(radial_glow((W, H), (W - 200, 120), 420))
    img.alpha_composite(radial_glow((W, H), (120, H - 80), 360))

    # Monogram badge, top-left.
    logo = Image.open(LOGO).convert("RGBA").resize((120, 120), Image.LANCZOS)
    img.alpha_composite(logo, (72, 64))

    draw = ImageDraw.Draw(img)
    name_font = ImageFont.truetype(FONT_NAME, 76)
    tag_font = ImageFont.truetype(FONT_TAG, 34)

    draw.text((72, 300), "Pedro Minuça Santos", font=name_font, fill=TEXT + (255,))
    draw.text((72, 400), "Front-End Engineer  ·  Portfolio", font=tag_font, fill=MUTED + (255,))

    # Small accent bar under the name.
    draw.rounded_rectangle([72, 380, 200, 388], radius=4, fill=ACCENT + (255,))

    img.convert("RGB").save(OUT, "PNG")
    print(f"wrote {OUT} {img.size}")


if __name__ == "__main__":
    main()
