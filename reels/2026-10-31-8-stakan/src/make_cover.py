from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1080, 1920
F = "/usr/share/fonts/opentype/inter/InterDisplay-{}.otf"
fn = lambda w, s: ImageFont.truetype(F.format(w), s)
SKY, NAVY, WHITE, YEL, BLUE = (132, 210, 253), (11, 31, 51), (255, 255, 255), (255, 212, 59), (37, 99, 235)

im = Image.new("RGBA", (W, H), SKY + (255,))
# soft light blobs (like the reference style) + faint water ripples
g = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(g)
d.ellipse([-300, -200, 700, 700], fill=(200, 236, 255, 160)); d.ellipse([500, 1100, 1500, 2100], fill=(90, 175, 245, 120))
im.alpha_composite(g.filter(ImageFilter.GaussianBlur(160)))

def text(x, y, s, f, col, anchor="la", shadow=True, stroke=0):
    lay = Image.new("RGBA", (W, H)); ld = ImageDraw.Draw(lay)
    if shadow:
        sh = Image.new("RGBA", (W, H)); ImageDraw.Draw(sh).text((x + 4, y + 8), s, font=f, fill=(0, 40, 90, 90), anchor=anchor)
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    ld.text((x, y), s, font=f, fill=col + (255,), anchor=anchor, stroke_width=stroke, stroke_fill=WHITE + (255,))
    im.alpha_composite(lay)

# --- hook (inside the 3:4 grid crop: y 240..1680)
text(70, 270, "Kuniga", fn("Black", 120), NAVY)
text(62, 390, "8 stakan", fn("Black", 210), WHITE, stroke=0)
lay = Image.new("RGBA", (900, 200)); ImageDraw.Draw(lay).text((20, 20), "ichish shartmi?", font=fn("BlackItalic", 104), fill=YEL + (255,), stroke_width=6, stroke_fill=NAVY + (255,))
lay = lay.rotate(4, resample=Image.BICUBIC, expand=True); im.alpha_composite(lay, (40, 590))

# --- 8 glasses (two rows), the person "drinking through" them: 1-6 empty, 7 half, 8 full
def glass(x, y, w, h, level, n):
    l = Image.new("RGBA", (w + 40, h + 60)); ld = ImageDraw.Draw(l)
    top, bot, ins = 20, h + 20, int(w * 0.12)
    poly = [(20, top), (20 + w, top), (20 + w - ins, bot), (20 + ins, bot)]
    ld.polygon(poly, fill=(255, 255, 255, 150))
    if level > 0:
        wy = bot - (bot - top - 14) * level
        fx = lambda yy: ins * (yy - top) / (bot - top)
        ld.polygon([(20 + fx(wy), wy), (20 + w - fx(wy), wy), (20 + w - ins, bot), (20 + ins, bot)], fill=(70, 160, 245, 235))
        ld.line([(24 + fx(wy), wy), (16 + w - fx(wy), wy)], fill=(200, 235, 255, 255), width=5)
    ld.line(poly + [poly[0]], fill=NAVY + (255,), width=6, joint="curve")
    ld.line([(32, top + 14), (32 + ins * 0.6, bot - 18)], fill=(255, 255, 255, 220), width=6)
    ld.text((20 + w / 2, bot + 30), str(n), font=fn("Black", 34), fill=NAVY + (255,), anchor="mm")
    im.alpha_composite(l, (x, y))
levels = [0, 0, 0, 0, 0, 0, 0.5, 1.0]
gw, gh = 92, 130
for i, lv in enumerate(levels):
    r, c = divmod(i, 4)
    glass(50 + c * 105, 850 + r * 210, 84, 120, lv, i + 1)

# --- mascot (logo), big, bottom-right
m = Image.open("mascot.png").convert("RGBA")
s = 1050 / m.height; m = m.resize((int(m.width * s), int(m.height * s)), Image.LANCZOS)
sh = Image.new("RGBA", m.size, (0, 40, 90, 0)); sh.putalpha(m.getchannel("A").point(lambda v: int(v * 0.35)))
mx, my = W - m.width + 250, H - m.height + 60
im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)), (mx - 14, my + 18)); im.alpha_composite(m, (mx, my))

# --- source badge
f = fn("Bold", 40); s_ = "✓ Science 2022 tekshirdi"; s_ = "Science 2022 tekshirdi"
w = ImageDraw.Draw(im).textlength(s_, font=f) + 120
b = Image.new("RGBA", (int(w), 90)); bd = ImageDraw.Draw(b)
bd.rounded_rectangle([0, 0, w - 1, 89], 45, fill=WHITE + (255,))
bd.ellipse([24, 22, 70, 68], fill=BLUE + (255,)); bd.line([(36, 45), (45, 55), (60, 36)], fill=WHITE + (255,), width=6)
bd.text((88, 45), s_, font=f, fill=NAVY + (255,), anchor="lm")
im.alpha_composite(b, (50, 1300))
text(60, 1415, "Doktor H₂O · @suvyektiv", fn("Bold", 38), NAVY, shadow=False)

im.convert("RGB").save("cover_8stakan.jpg", quality=94)
im.convert("RGB").crop((0, 240, 1080, 1680)).resize((360, 480)).save("cover_grid.jpg")
print("ok")
