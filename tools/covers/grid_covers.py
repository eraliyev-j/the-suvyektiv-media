"""Uniform SKY grid covers for the older reels (2026-10-27 profile refresh).
usage: python3 grid_covers.py brand/mascot.png <out_dir> <photo_dir with big_<slug>.jpg (Pixabay)>"""
import sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1080, 1920
F = "/usr/share/fonts/opentype/inter/InterDisplay-{}.otf"
fn = lambda w, s: ImageFont.truetype(F.format(w), s)
SKY, NAVY, WHITE, YEL, BLUE = (132, 210, 253), (11, 31, 51), (255, 255, 255), (255, 212, 59), (37, 99, 235)
MASCOT, OUT, PHOTOS = sys.argv[1], sys.argv[2], sys.argv[3]
FLIP = set()

COVERS = [  # slug, chip, line1, line2, line3, cutout, icon, crop_bottom
    ("welcome", None, "Tanishing:", "Doktor H₂O", "suv haqida, ilm bilan", "w2", None, 0.50),
    ("suv-qanday", None, "Suv qanday", "tozalanadi?", "4 bosqichda", "s20", "steps", 120),
    ("fizik", "SUV TOZALASH · 1/4", "1-bosqich:", "Fizik usul", "panjara, qum, tindirish", "s8", "glass", 120),
    ("biologik", "SUV TOZALASH · 2/4", "Suvni kim tozalaydi?", "Bakteriyalar", "ha, foydalilari!", "s16", "bact", 120),
    ("kimyoviy", "SUV TOZALASH · 3/4", "Kran suvida", "xlor hidi", "nega kerak?", "s24", "flask", 120),
    ("membranali", "SUV TOZALASH · 4/4", "Filtr ichida", "membrana", "qanday ishlaydi?", "s12", "membrane", 120),
    ("qaynatilgan", None, "Qaynatilgan suv", "tozami?", "choynakdagi oq qatlam", "q2", "kettle", 0.62),
]

def shadow_text(im, x, y, s, f, col, anchor="la"):
    sh = Image.new("RGBA", (W, H)); ImageDraw.Draw(sh).text((x + 4, y + 8), s, font=f, fill=(0, 40, 90, 90), anchor=anchor)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    ImageDraw.Draw(im).text((x, y), s, font=f, fill=col + (255,), anchor=anchor)

def fit(s, w, maxsize, weight="Black"):
    sz = maxsize
    while fn(weight, sz).getlength(s) > w and sz > 60: sz -= 4
    return fn(weight, sz)

def photo_card(im, path, x, y, w=620, h=440, angle=-3):
    ph = Image.open(path).convert("RGB"); r = max(w / ph.width, h / ph.height)
    ph = ph.resize((int(ph.width * r) + 1, int(ph.height * r) + 1), Image.LANCZOS)
    ph = ph.crop(((ph.width - w) // 2, (ph.height - h) // 2, (ph.width - w) // 2 + w, (ph.height - h) // 2 + h))
    b = 14; card = Image.new("RGBA", (w + 2 * b, h + 2 * b + 46), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([0, 0, card.width - 1, card.height - 1], 26, fill=WHITE + (255,))
    mask = Image.new("L", (w, h), 0); ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], 16, fill=255)
    card.paste(ph, (b, b), mask)
    cd.text((b + 4, h + b + 23), "Foto: Pixabay", font=fn("Medium", 24), fill=(90, 110, 130, 255), anchor="lm")
    card = card.rotate(angle, resample=Image.BICUBIC, expand=True)
    sh = Image.new("RGBA", card.size, (0, 40, 90, 0)); sh.putalpha(card.getchannel("A").point(lambda v: int(v * .35)))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)), (x + 10, y + 20)); im.alpha_composite(card, (x, y))

def icon(im, kind, x, y, s):
    l = Image.new("RGBA", (s, s)); d = ImageDraw.Draw(l); lw = max(6, s // 40)
    water, wl = (70, 160, 245, 235), (200, 235, 255, 255)
    if kind == "glass":
        poly = [(s*.2, s*.08), (s*.8, s*.08), (s*.72, s*.92), (s*.28, s*.92)]
        d.polygon(poly, fill=(255, 255, 255, 150)); d.polygon([(s*.235, s*.4), (s*.765, s*.4), (s*.72, s*.92), (s*.28, s*.92)], fill=water)
        for i in range(14): xx, yy = s*(.32+.36*((i*37)%11)/11), s*(.5+.38*((i*53)%13)/13); d.ellipse([xx-6, yy-6, xx+6, yy+6], fill=(150, 110, 60, 220))
        d.line(poly + [poly[0]], fill=NAVY + (255,), width=lw, joint="curve")
    elif kind == "flask":
        d.polygon([(s*.4, s*.08), (s*.6, s*.08), (s*.6, s*.38), (s*.88, s*.9), (s*.12, s*.9), (s*.4, s*.38)], fill=(255, 255, 255, 150))
        d.polygon([(s*.27, s*.62), (s*.73, s*.62), (s*.88, s*.9), (s*.12, s*.9)], fill=(140, 110, 230, 235))
        d.line([(s*.4, s*.08), (s*.4, s*.38), (s*.12, s*.9), (s*.88, s*.9), (s*.6, s*.38), (s*.6, s*.08)], fill=NAVY + (255,), width=lw, joint="curve")
        d.line([(s*.34, s*.08), (s*.66, s*.08)], fill=NAVY + (255,), width=lw)
    elif kind == "bact":
        d.ellipse([s*.05, s*.05, s*.95, s*.95], fill=(255, 255, 255, 150), outline=NAVY + (255,), width=lw)
        for i, (cx, cy, a) in enumerate([(.38, .35, 30), (.62, .42, -40), (.45, .62, 70), (.66, .68, 10), (.3, .55, -20)]):
            b = Image.new("RGBA", (int(s*.3), int(s*.12))); ImageDraw.Draw(b).rounded_rectangle([0, 0, b.width-1, b.height-1], b.height//2, fill=(70, 190, 120, 255), outline=NAVY + (255,), width=max(3, lw//2))
            b = b.rotate(a, expand=True, resample=Image.BICUBIC); l.alpha_composite(b, (int(s*cx - b.width/2), int(s*cy - b.height/2)))
    elif kind == "membrane":
        d.rounded_rectangle([s*.05, s*.32, s*.8, s*.68], s*.18, fill=(240, 246, 252, 255), outline=NAVY + (255,), width=lw)
        d.ellipse([s*.68, s*.32, s*.92, s*.68], fill=water, outline=NAVY + (255,), width=lw)
        for i in range(4): d.ellipse([s*(.6+.09*i)+s*.36, s*.47, s*(.6+.09*i)+s*.36+s*.05, s*.53], fill=(70, 160, 245, 255))
    elif kind == "steps":
        for i in range(4):
            yy = s*(.1 + .22*i); d.rounded_rectangle([s*.05, yy, s*.95, yy + s*.16], s*.08, fill=(255, 255, 255, 220))
            d.ellipse([s*.09, yy + s*.025, s*.2, yy + s*.135], fill=BLUE + (255,))
            d.text((s*.145, yy + s*.08), str(i+1), font=fn("Black", int(s*.07)), fill=WHITE + (255,), anchor="mm")
            d.text((s*.26, yy + s*.08), ["Fizik", "Biologik", "Kimyoviy", "Membrana"][i], font=fn("Bold", int(s*.08)), fill=NAVY + (255,), anchor="lm")
    elif kind == "kettle":
        d.ellipse([s*.12, s*.25, s*.82, s*.92], fill=(255, 255, 255, 170), outline=NAVY + (255,), width=lw)
        d.chord([s*.12, s*.25, s*.82, s*.92], 20, 160, fill=(235, 230, 215, 255), outline=NAVY + (255,), width=lw)
        d.line([(s*.8, s*.55), (s*.97, s*.35)], fill=NAVY + (255,), width=lw*2)
    sh = Image.new("RGBA", l.size, (0, 40, 90, 0)); sh.putalpha(l.getchannel("A").point(lambda v: int(v * .25)))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)), (x + 8, y + 14)); im.alpha_composite(l, (x, y))

for slug, chip, l1, l2, l3, cut, ic, cb in COVERS:
    im = Image.new("RGBA", (W, H), SKY + (255,))
    g = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(g)
    d.ellipse([-300, -200, 700, 700], fill=(200, 236, 255, 160)); d.ellipse([500, 1100, 1500, 2100], fill=(90, 175, 245, 120))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(160)))
    # mascot (Doktor H2O logo character), bottom-right, same placement as the 8 stakan cover
    m = Image.open(MASCOT).convert("RGBA")
    if slug in FLIP: m = m.transpose(Image.FLIP_LEFT_RIGHT)
    sc = 1050 / m.height; m = m.resize((int(m.width * sc), int(m.height * sc)), Image.LANCZOS)
    mx, my = W - m.width + 250, H - m.height + 60
    sh = Image.new("RGBA", m.size, (0, 40, 90, 0)); sh.putalpha(m.getchannel("A").point(lambda v: int(v * .35)))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)), (mx - 14, my + 18)); im.alpha_composite(m, (mx, my))
    # text block (inside the 3:4 grid crop y 240..1680)
    y = 270
    if chip:
        f = fn("Bold", 38); w = f.getlength(chip) + 60
        ImageDraw.Draw(im).rounded_rectangle([60, y, 60 + w, y + 70], 35, fill=WHITE + (255,))
        ImageDraw.Draw(im).text((90, y + 35), chip, font=f, fill=NAVY + (255,), anchor="lm"); y += 100
    f1 = fit(l1, 960, 110); shadow_text(im, 66, y, l1, f1, NAVY); y += int(f1.size * 1.05)
    f2 = fit(l2, 960, 200); shadow_text(im, 58, y, l2, f2, WHITE); y += int(f2.size * 1.05)
    f3 = fit(l3, 900, 96, "BlackItalic")
    lay = Image.new("RGBA", (1000, 200)); ImageDraw.Draw(lay).text((20, 20), l3, font=f3, fill=YEL + (255,), stroke_width=6, stroke_fill=NAVY + (255,))
    lay = lay.rotate(3, resample=Image.BICUBIC, expand=True); im.alpha_composite(lay, (40, y - 10)); y += f3.size + 80
    photo_card(im, f"{PHOTOS}/big_{slug}.jpg", 30, max(y - 10, 840))
    im.alpha_composite(m, (mx, my))  # mascot stays in front of the photo
    ImageDraw.Draw(im).text((60, 1415), "Doktor H₂O · @suvyektiv", font=fn("Bold", 38), fill=NAVY + (255,))
    im.convert("RGB").save(f"{OUT}/cover_{slug}.jpg", quality=94)
    print(slug)
