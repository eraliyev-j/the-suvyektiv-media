"""Covers for the upcoming reels (24.10-07.11). Same SKY brand + mascot, but a DIFFERENT layout each,
so the grid does not look like nine copies of one card.
usage: python3 next_covers.py brand/mascot.png <out_dir> <photo_dir with big_<slug>.jpg>"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1080, 1920
F = "/usr/share/fonts/opentype/inter/InterDisplay-{}.otf"
fn = lambda w, s: ImageFont.truetype(F.format(w), s)
SKY, NAVY, WHITE, YEL = (132, 210, 253), (11, 31, 51), (255, 255, 255), (255, 212, 59)
MASCOT, OUT, PH = sys.argv[1], sys.argv[2], sys.argv[3]

def base():
    im = Image.new("RGBA", (W, H), SKY + (255,))
    g = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(g)
    d.ellipse([-300, -200, 700, 700], fill=(200, 236, 255, 160)); d.ellipse([500, 1100, 1500, 2100], fill=(90, 175, 245, 120))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(160))); return im

def shadow_paste(im, lay, x, y, k=.35, blur=18, off=(-12, 18)):
    sh = Image.new("RGBA", lay.size, (0, 40, 90, 0)); sh.putalpha(lay.getchannel("A").point(lambda v: int(v * k)))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)), (x + off[0], y + off[1])); im.alpha_composite(lay, (x, y))

def mascot(h, flip=False):
    m = Image.open(MASCOT).convert("RGBA")
    if flip: m = m.transpose(Image.FLIP_LEFT_RIGHT)
    s = h / m.height; return m.resize((int(m.width * s), int(m.height * s)), Image.LANCZOS)

def text(im, x, y, s, f, col, anchor="la", shadow=True):
    if shadow:
        sh = Image.new("RGBA", (W, H)); ImageDraw.Draw(sh).text((x + 4, y + 8), s, font=f, fill=(0, 40, 90, 90), anchor=anchor)
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(im).text((x, y), s, font=f, fill=col + (255,), anchor=anchor)

def fit(s, w, mx, weight="Black"):
    z = mx
    while fn(weight, z).getlength(s) > w and z > 50: z -= 4
    return fn(weight, z)

def tilt(im, s, x, y, size, angle=3, anchor_center=False):
    f = fit(s, 940, size, "BlackItalic")
    lay = Image.new("RGBA", (1060, 220)); ImageDraw.Draw(lay).text((20, 20), s, font=f, fill=YEL + (255,), stroke_width=6, stroke_fill=NAVY + (255,))
    lay = lay.crop(lay.getbbox()); pad = Image.new("RGBA", (lay.width + 20, lay.height + 20)); pad.alpha_composite(lay, (10, 10))
    lay = pad.rotate(angle, resample=Image.BICUBIC, expand=True)
    if anchor_center: x = int(x - lay.width / 2)
    im.alpha_composite(lay, (x, y)); return lay.height

def card(path, w, h, angle=-3, b=14):
    ph = Image.open(path).convert("RGB"); r = max(w / ph.width, h / ph.height)
    ph = ph.resize((int(ph.width * r) + 1, int(ph.height * r) + 1), Image.LANCZOS)
    ph = ph.crop(((ph.width - w) // 2, (ph.height - h) // 2, (ph.width - w) // 2 + w, (ph.height - h) // 2 + h))
    c = Image.new("RGBA", (w + 2 * b, h + 2 * b)); ImageDraw.Draw(c).rounded_rectangle([0, 0, c.width - 1, c.height - 1], 26, fill=WHITE + (255,))
    mk = Image.new("L", (w, h), 0); ImageDraw.Draw(mk).rounded_rectangle([0, 0, w - 1, h - 1], 16, fill=255); c.paste(ph, (b, b), mk)
    return c.rotate(angle, resample=Image.BICUBIC, expand=True)

def handle(im, x, y, anchor="la"):
    text(im, x, y, "Doktor H₂O · @suvyektiv", fn("Bold", 38), NAVY, anchor, shadow=False)


RED = (235, 72, 72)
def emote(im, kind, m, mx, my, dy=.45):
    """Mood next to the mascot's head: think (thought cloud + ?), wow (burst + ! + sparkles), huh (bubble + ?!)."""
    hx0, hx1, hy0, hy1 = mx + .34 * m.width, mx + .63 * m.width, my + .02 * m.height, my + .30 * m.height
    right = (hx0 + hx1) / 2 < W / 2            # mascot on the left -> mood goes to its right
    s = int(m.height * .26); lay = Image.new("RGBA", (int(s * 1.6), int(s * 1.5))); d = ImageDraw.Draw(lay)
    cx, cy = lay.width / 2, lay.height * .42
    if kind == "think":
        for dx, dy, r in [(-.32, .02, .30), (0, -.1, .36), (.32, .02, .30), (-.15, .16, .28), (.18, .16, .28)]:
            d.ellipse([cx + dx * s - r * s, cy + dy * s - r * s, cx + dx * s + r * s, cy + dy * s + r * s], fill=WHITE + (255,), outline=NAVY + (255,), width=6)
        for dx, dy, r in [(-.32, .02, .30), (0, -.1, .36), (.32, .02, .30), (-.15, .16, .28), (.18, .16, .28)]:
            d.ellipse([cx + dx * s - r * s + 6, cy + dy * s - r * s + 6, cx + dx * s + r * s - 6, cy + dy * s + r * s - 6], fill=WHITE + (255,))
        d.text((cx, cy + s * .02), "?", font=fn("Black", int(s * .5)), fill=NAVY + (255,), anchor="mm")
        tx = -1 if right else 1                # little trailing bubbles toward the head
        for k, r in enumerate([.09, .06]):
            x0 = cx - tx * s * (.42 + .16 * k); y0 = cy + s * (.5 + .14 * k)
            d.ellipse([x0 - r * s, y0 - r * s, x0 + r * s, y0 + r * s], fill=WHITE + (255,), outline=NAVY + (255,), width=5)
    elif kind == "wow":
        import math
        pts = [(cx + (s * (.55 if i % 2 == 0 else .36)) * math.cos(math.pi * i / 8), cy + (s * (.55 if i % 2 == 0 else .36)) * math.sin(math.pi * i / 8)) for i in range(16)]
        d.polygon(pts, fill=YEL + (255,), outline=NAVY + (255,), width=6)
        d.text((cx, cy), "!", font=fn("Black", int(s * .6)), fill=NAVY + (255,), anchor="mm")
        for dx, dy, r in [(.72, -.45, .09), (-.7, -.3, .07), (.6, .5, .06)]:
            x0, y0 = cx + dx * s, cy + dy * s
            d.polygon([(x0, y0 - r * s * 2), (x0 + r * s * .5, y0 - r * s * .5), (x0 + r * s * 2, y0), (x0 + r * s * .5, y0 + r * s * .5), (x0, y0 + r * s * 2), (x0 - r * s * .5, y0 + r * s * .5), (x0 - r * s * 2, y0), (x0 - r * s * .5, y0 - r * s * .5)], fill=WHITE + (255,))
    elif kind == "huh":
        tx = -1 if right else 1
        d.polygon([(cx - tx * s * .28, cy + s * .2), (cx - tx * s * .5, cy + s * .62), (cx - tx * s * .02, cy + s * .2)], fill=WHITE + (255,), outline=NAVY + (255,), width=6)
        d.rounded_rectangle([cx - s * .55, cy - s * .38, cx + s * .55, cy + s * .34], s * .2, fill=WHITE + (255,), outline=NAVY + (255,), width=6)
        d.polygon([(cx - tx * s * .27, cy + s * .3), (cx - tx * s * .04, cy + s * .3), (cx - tx * s * .2, cy + s * .4)], fill=WHITE + (255,))
        d.text((cx - s * .14, cy - s * .02), "?", font=fn("Black", int(s * .5)), fill=NAVY + (255,), anchor="mm")
        d.text((cx + s * .18, cy - s * .02), "!", font=fn("Black", int(s * .5)), fill=RED + (255,), anchor="mm")
    lay = lay.rotate(-8 if right else 8, resample=Image.BICUBIC, expand=True)
    x = int(hx1 - lay.width * .15) if right else int(hx0 - lay.width * .85)
    y = int(hy0 - lay.height * dy)
    shadow_paste(im, lay, x, y, k=.25, blur=12, off=(6, 12))

def save(im, slug): im.convert("RGB").save(f"{OUT}/cover_{slug}.jpg", quality=94); print(slug)

# 1) 24.10 suv sarfi — BIG NUMBER, mascot bottom-LEFT, photo bottom-right
im = base()
text(im, 60, 280, "Suv sarfi bo'yicha", fn("Black", 96), NAVY)
text(im, 40, 380, "4-o'rin", fit("4-o'rin", 1000, 300), WHITE)
tilt(im, "O'zbekiston dunyoda", 50, 720, 96, angle=3)
c = card(f"{PH}/big_suv-sarfi.jpg", 500, 380, angle=4); shadow_paste(im, c, W - c.width - 20, 1120)
m = mascot(900); mx, my = -230, H - m.height + 60; shadow_paste(im, m, mx, my); emote(im, "wow", m, mx, my)
handle(im, W - 60, 1600, "ra"); save(im, "suv-sarfi")

# 2) 27.10 2050 — FULL-WIDTH photo band on top, text under it, mascot bottom-RIGHT
im = base()
c = card(f"{PH}/big_2050.jpg", 1000, 380, angle=0); shadow_paste(im, c, 26, 250)
text(im, 60, 700, "2050 yilga kelib", fn("Black", 96), NAVY)
text(im, 52, 805, "5 barobar", fit("5 barobar", 960, 210), WHITE)
tilt(im, "suv taqchilligi", 50, 1030, 100, angle=-3)
m = mascot(760); mx, my = W - m.width + 230, H - m.height + 40; shadow_paste(im, m, mx, my); emote(im, "huh", m, mx, my, dy=.05)
handle(im, 60, 1600); save(im, "2050")

# 3) 29.10 Salar — mascot LEFT big, text RIGHT-aligned, photo tilted under text
im = base()
text(im, W - 60, 280, "Sergelidagi hid uchun", fn("Black", 84), NAVY, "ra")
f = fit("9,5 mlrd so'm", 980, 190); text(im, W - 50, 390, "9,5 mlrd so'm", f, WHITE, "ra")
f3 = fit("Nega?", 900, 100, "BlackItalic")
l = Image.new("RGBA", (1000, 200)); ImageDraw.Draw(l).text((20, 20), "Nega?", font=f3, fill=YEL + (255,), stroke_width=6, stroke_fill=NAVY + (255,))
l = l.crop(l.getbbox()).rotate(-3, resample=Image.BICUBIC, expand=True); im.alpha_composite(l, (W - 50 - l.width, 610))
c = card(f"{PH}/big_salar.jpg", 560, 400, angle=4); shadow_paste(im, c, W - c.width - 30, 820)
m = mascot(1000, flip=False); mx, my = -250, H - m.height + 60; shadow_paste(im, m, mx, my); emote(im, "think", m, mx, my)
handle(im, W - 60, 1600, "ra"); save(im, "salar")

# 4) 03.11 kran suvi — CENTRED text, round photo in the middle, small mascot bottom-centre
im = base()
text(im, W // 2, 300, "Kran suvi", fit("Kran suvi", 980, 200), WHITE, "ma")
text(im, W // 2, 520, "qayerdan keladi?", fn("Black", 96), NAVY, "ma")
d = 480; ph = Image.open(f"{PH}/big_kran.jpg").convert("RGB"); r = max(d / ph.width, d / ph.height)
ph = ph.resize((int(ph.width * r) + 1, int(ph.height * r) + 1), Image.LANCZOS); ph = ph.crop(((ph.width - d) // 2, (ph.height - d) // 2, (ph.width - d) // 2 + d, (ph.height - d) // 2 + d))
circ = Image.new("RGBA", (d + 28, d + 28)); ImageDraw.Draw(circ).ellipse([0, 0, d + 27, d + 27], fill=WHITE + (255,))
mk = Image.new("L", (d, d), 0); ImageDraw.Draw(mk).ellipse([0, 0, d - 1, d - 1], fill=255); circ.paste(ph, (14, 14), mk)
tilt(im, "Chorvoqdan krangacha", W // 2, 640, 84, angle=-2, anchor_center=True)
shadow_paste(im, circ, 60, 840, off=(0, 18))
m = mascot(760); mx, my = W - m.width + 230, H - m.height + 40; shadow_paste(im, m, mx, my); emote(im, "think", m, mx, my)
handle(im, 60, 1600); save(im, "kran")

# 5) 05.11 layfhak — photo LEFT tall card, big counter on the right, mascot bottom-right small
im = base()
text(im, 60, 270, "5 ta odat bilan", fn("Black", 96), NAVY)
text(im, 52, 380, "26 000 litr", fit("26 000 litr", 980, 190), WHITE)
tilt(im, "yiliga tejaysiz", 50, 590, 100, angle=3)
c = card(f"{PH}/big_layfhak.jpg", 420, 560, angle=-4); shadow_paste(im, c, 40, 800)
m = mascot(900); mx, my = W - m.width + 260, H - m.height + 60; shadow_paste(im, m, mx, my); emote(im, "wow", m, mx, my, dy=.15)
handle(im, 60, 1600); save(im, "layfhak")

# 6) 07.11 butilka — photo band TOP, number HUGE centre, mascot bottom-LEFT (flipped)
im = base()
c = card(f"{PH}/big_butilka.jpg", 1000, 380, angle=0); shadow_paste(im, c, 26, 250)
text(im, W - 60, 700, "1 litr butilka suvida", fn("Black", 80), NAVY, "ra")
text(im, W - 50, 800, "240 000", fit("240 000", 980, 230), WHITE, "ra")
f3 = fit("plastik zarra", 900, 104, "BlackItalic")
l = Image.new("RGBA", (1000, 200)); ImageDraw.Draw(l).text((20, 20), "plastik zarra", font=f3, fill=YEL + (255,), stroke_width=6, stroke_fill=NAVY + (255,))
l = l.crop(l.getbbox()).rotate(3, resample=Image.BICUBIC, expand=True); im.alpha_composite(l, (W - 50 - l.width, 1060))
m = mascot(860, flip=False); mx, my = -200, H - m.height + 50; shadow_paste(im, m, mx, my); emote(im, "huh", m, mx, my, dy=-.05)
handle(im, W - 60, 1600, "ra"); save(im, "butilka")
