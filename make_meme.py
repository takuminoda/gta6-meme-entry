"""Render meme.png for the make.fun bounty "Post a GTA 6 meme on X".

The picture is the entry: a GTA VI launch-week joke with make.fun's ghost mascot
(assets/mark-1024.png) worked into a Vice City / Leonida sunset, with the make.fun
name drawn in the scene.  Run it with Python and PIL:

    python make_meme.py

It writes meme.png (1200x1200 PNG) next to this file.
"""
from __future__ import annotations

import math
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
MARK_PATH = os.path.join(ROOT, "assets", "mark-1024.png")
OUT_PATH = os.path.join(ROOT, "meme.png")

W, H = 1200, 1200

FONT_DIR = "C:/Windows/Fonts"
FONT_HEAD = os.path.join(FONT_DIR, "impact.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "segoeuib.ttf")

# Deep purple night -> magenta -> warm orange: a Leonida sunset.
SKY_STOPS = [
    (0.00, (22, 7, 50)),
    (0.28, (62, 17, 108)),
    (0.52, (176, 16, 116)),
    (0.72, (243, 76, 72)),
    (1.00, (255, 178, 72)),
]

MAGENTA = (255, 62, 165)
DARK = (18, 6, 38)
INK = (12, 6, 24)


def sky_color(t: float) -> tuple[int, int, int]:
    """Colour of the sunset gradient at height t (0 = top, 1 = bottom)."""
    t = min(1.0, max(0.0, t))
    for (t0, c0), (t1, c1) in zip(SKY_STOPS, SKY_STOPS[1:]):
        if t <= t1:
            f = 0.0 if t1 == t0 else (t - t0) / (t1 - t0)
            return tuple(int(round(c0[i] + (c1[i] - c0[i]) * f)) for i in range(3))
    return SKY_STOPS[-1][1]


def make_sky() -> Image.Image:
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        row = sky_color(y / (H - 1))
        for x in range(W):
            px[x, y] = row
    return img


def draw_sun(draw: ImageDraw.ImageDraw, cx: int, cy: int, r: int) -> None:
    """Synthwave sun: warm core to orange rim, with slits cut by the sky colour."""
    outer = (255, 138, 61)
    core = (255, 240, 196)
    step = 4
    for i in range(r, 0, -step):
        f = 1.0 - i / r
        col = tuple(int(round(outer[c] + (core[c] - outer[c]) * f)) for c in range(3))
        draw.ellipse([cx - i, cy - i, cx + i, cy + i], fill=col)
    # Slits: repaint the sky gradient over the lower half of the disc.
    y = cy + 12
    while y < cy + r:
        draw.rectangle([cx - r, y, cx + r, y + 9], fill=sky_color(y / (H - 1)))
        y += 24


def _qbez(p0, p1, p2, n: int = 14):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        pts.append((x, y))
    return pts


def _frond(draw, tx, ty, ang_deg, length, width, color) -> None:
    rad = math.radians(ang_deg)
    dx, dy = math.cos(rad), math.sin(rad)
    ex, ey = tx + dx * length, ty + dy * length
    cx, cy = tx + dx * length * 0.5, ty + dy * length * 0.5 - length * 0.22
    px, py = -dy, dx
    upper = _qbez((tx, ty), (cx, cy), (ex, ey))
    lower = _qbez((ex, ey), (cx + px * width, cy + py * width), (tx, ty))
    draw.polygon(upper + lower, fill=color)


def draw_palm(draw, x, base, height, lean, color) -> None:
    """Simple clean palm silhouette: a tapered curved trunk and a fan of fronds."""
    steps = 22
    ring = []
    for i in range(steps + 1):
        t = i / steps
        px = x + lean * (t ** 1.7)
        py = base - height * t
        half = height * 0.055 * (1.0 - 0.55 * t)
        ring.append((px, py, half))
    trunk = [(px - half, py) for px, py, half in ring]
    trunk += [(px + half, py) for px, py, half in reversed(ring)]
    draw.polygon(trunk, fill=color)
    tx, ty = ring[-1][0], ring[-1][1]
    for ang in (160, 190, 215, 240, 265, 290, 315, 340, 20):
        _frond(draw, tx, ty, ang, height * 0.46, height * 0.10, color)


def fit_font(path: str, text: str, start: int, max_w: int, min_size: int = 20) -> ImageFont.FreeTypeFont:
    size = start
    while size > min_size:
        f = ImageFont.truetype(path, size)
        if f.getbbox(text)[2] <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(path, min_size)


def text_center(draw, cx, y, s, font, fill, stroke=0, stroke_fill=INK, spacing=0, anchor="ma"):
    if spacing:
        widths = [draw.textlength(ch, font=font) for ch in s]
        total = sum(widths) + spacing * (len(s) - 1)
        x = cx - total / 2
        for ch, w in zip(s, widths):
            draw.text((x, y), ch, font=font, fill=fill, stroke_width=stroke,
                      stroke_fill=stroke_fill, anchor="la")
            x += w + spacing
        return total
    draw.text((cx, y), s, font=font, fill=fill, stroke_width=stroke,
              stroke_fill=stroke_fill, anchor="ma")
    return draw.textlength(s, font=font)


def mixed_center(draw, cx, y, parts, font, stroke=0, stroke_fill=INK):
    """parts: [(text, fill), ...] drawn as one centred line."""
    widths = [draw.textlength(t, font=font) for t, _ in parts]
    x = cx - sum(widths) / 2
    for (t, fill), w in zip(parts, widths):
        draw.text((x, y), t, font=font, fill=fill, stroke_width=stroke,
                  stroke_fill=stroke_fill, anchor="la")
        x += w


def sparkle(draw, x, y, r, color):
    draw.polygon([(x, y - r), (x + r * 0.28, y - r * 0.28), (x + r, y),
                  (x + r * 0.28, y + r * 0.28), (x, y + r), (x - r * 0.28, y + r * 0.28),
                  (x - r, y), (x - r * 0.28, y - r * 0.28)], fill=color)


def main() -> None:
    img = make_sky().convert("RGBA")
    draw = ImageDraw.Draw(img)

    draw_sun(draw, 600, 655, 215)

    # Palms on the horizon.
    for x, base, h, lean in ((110, 775, 300, -46), (1060, 780, 340, 40),
                             (265, 790, 200, -24), (905, 795, 175, 22)):
        draw_palm(draw, x, base, h, lean, (16, 6, 34))

    # Ground panel.
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle([0, 742, W, H], radius=48, fill=(18, 6, 38, 255))
    pd.rectangle([0, 742, W, 750], fill=(255, 62, 165, 255))
    img = Image.alpha_composite(img, panel)
    draw = ImageDraw.Draw(img)

    # Badge: make.fun's ghost on its magenta disc, worked into the scene.
    badge_size = 540
    bx, by = 30, 640
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([bx - 46, by - 46, bx + badge_size + 46, by + badge_size + 46],
               fill=(255, 62, 165, 95))
    glow = glow.filter(ImageFilter.GaussianBlur(55))
    img = Image.alpha_composite(img, glow)

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([bx + 40, by + badge_size - 18, bx + badge_size - 30, by + badge_size + 34],
               fill=(0, 0, 0, 120))
    shadow = shadow.filter(ImageFilter.GaussianBlur(20))
    img = Image.alpha_composite(img, shadow)

    badge = Image.open(MARK_PATH).convert("RGBA").resize((badge_size, badge_size),
                                                         Image.LANCZOS)
    img.alpha_composite(badge, (bx, by))
    draw = ImageDraw.Draw(img)

    # ---- Sky copy ----
    text_center(draw, 600, 52, "13 YEARS LATER...",
                fit_font(FONT_BOLD, "13 YEARS LATER...", 64, 860),
                (255, 255, 255), stroke=4, spacing=12)

    text_center(draw, 600, 118, "GTA 6",
                fit_font(FONT_HEAD, "GTA 6", 210, 900),
                (255, 255, 255), stroke=10, stroke_fill=INK)

    text_center(draw, 600, 330, "FINALLY DROPS",
                fit_font(FONT_HEAD, "FINALLY DROPS", 104, 940),
                (255, 214, 63), stroke=8, stroke_fill=INK, spacing=4)

    # Punchline on a dark plate so it reads over the sun.
    plate = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pld = ImageDraw.Draw(plate)
    pld.rounded_rectangle([140, 432, 1060, 628], radius=26, fill=(10, 4, 24, 238),
                          outline=(255, 62, 165, 255), width=4)
    img = Image.alpha_composite(img, plate)
    draw = ImageDraw.Draw(img)

    text_center(draw, 600, 452, "ME: calling in sick",
                fit_font(FONT_BOLD, "ME: calling in sick", 58, 860),
                (255, 255, 255), stroke=4)
    text_center(draw, 600, 522, "for a 150 GB download",
                fit_font(FONT_BOLD, "for a 150 GB download", 58, 860),
                (255, 255, 255), stroke=4)

    # ---- Bottom copy beside the ghost ----
    text_center(draw, 905, 688, "MY AGENT:",
                fit_font(FONT_BOLD, "MY AGENT:", 44, 520),
                (255, 138, 194), stroke=3, spacing=6)
    text_center(draw, 905, 750, "already got paid",
                fit_font(FONT_BOLD, "already got paid", 60, 540),
                (255, 255, 255), stroke=4)
    mixed_center(draw, 905, 828,
                 [("on ", (255, 255, 255)), ("make.fun", MAGENTA)],
                 fit_font(FONT_BOLD, "on make.fun", 84, 540), stroke=5)

    for sx, sy, sr in ((636, 690, 12), (1152, 880, 9), (660, 1090, 10)):
        sparkle(draw, sx, sy, sr, (255, 255, 255, 230))

    img.convert("RGB").save(OUT_PATH, "PNG", optimize=True)
    print(f"wrote {OUT_PATH} {img.size}")


if __name__ == "__main__":
    main()
