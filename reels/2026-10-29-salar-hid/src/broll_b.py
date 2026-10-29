"""Reel B '9,5 milliard ishladimi?' (v3, 29.10) — B-roll, one clip per beat, 'oldin / keyin' style:
light sky board, 2021 | 2026 | YECHIM tabs, before/after split photos, clean schematic diagrams.
Different from Reel A ('case file'): no paper, no tape, no stamps.
No subtitles, no audio: Javohir's voice/A-roll goes in later, subtitles on top at y~1180.
Everything essential sits in y 230-1080 and x 80-850 (IG/Shorts UI). Below y 1290 = decoration only.
Photos (not in the public repo): see photos_b.txt; PH env var = folder with them.
usage: python3 broll_b.py OUTDIR            -> b01..b09 .mp4 + ov01..ov08 .mov (alpha screen cards)
       python3 broll_b.py still IDX T out.png"""
import sys, os, math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

PH = os.environ.get("PH", "/tmp/claude-0/salB/ph") + "/"
W, H, FPS = 1080, 1920, 30
F = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
_fc = {}
def fn(w, s):
    if (w, s) not in _fc: _fc[(w, s)] = ImageFont.truetype(F.format(w), s)
    return _fc[(w, s)]
WHITE, SKY, SKYD, NAVY, NAVY2, WARN = (255, 255, 255), (132, 210, 253), (31, 111, 178), (11, 31, 51), (31, 58, 128), (226, 88, 62)
BG, BG2, INK2, LINE = (237, 248, 255), (214, 238, 252), (70, 88, 108), (190, 214, 232)
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def ph(t, t0, d=0.5): return ease((t - t0) / d)
def back(u): u = max(0, min(1, u)); c = 1.7; return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2
def rgba(c, a): return c + (int(255 * max(0, min(1, a))),)

def text(d, x, y, s, f, col, a=1.0, anchor="la"):
    if a <= 0: return
    d.text((x, y + (1 - a) * 22), s, font=f, fill=rgba(col, a), anchor=anchor)

def marker(d, x, y, s, f, a, col=SKY):
    if a <= 0: return
    w = d.textlength(s, font=f); bb = d.textbbox((x, y), s, font=f)
    d.rectangle([x - 10, bb[1] + (bb[3] - bb[1]) * 0.3, x - 10 + (w + 20) * a, bb[3] + 8], fill=col + (210,))

_ph = {}
def photo(name):
    if name not in _ph: _ph[name] = Image.open(PH + f"{name}.jpg").convert("RGB")
    return _ph[name]

def fit(p, w, h, z=1.0, fx=0.5, fy=0.5):
    """cover-crop photo p into w x h with zoom z around focus (fx, fy)"""
    pw, phh = p.size; s = max(w / pw, h / phh) * z
    cw, ch = w / s, h / s
    x0 = min(max(fx * pw - cw / 2, 0), pw - cw); y0 = min(max(fy * phh - ch / 2, 0), phh - ch)
    return p.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w, h), Image.BILINEAR)

def rmask(w, h, r):
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255); return m

def pane(im, img, x, y, a, credit="", r=28):
    """rounded photo pane with soft shadow and a credit pill; img already sized"""
    if a <= 0: return
    w, h = img.size; m = rmask(w, h, r)
    sh = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([40, 52, 40 + w, 52 + h], r, fill=(11, 31, 51, int(60 * a)))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    yy = int(y + (1 - a) * 30)
    im.alpha_composite(sh, (int(x) - 40, yy - 40))
    t = img.convert("RGBA"); t.putalpha(m.point(lambda v: int(v * a)))
    im.alpha_composite(t, (int(x), yy))
    if credit:
        d = ImageDraw.Draw(im); f = fn("SemiBold", 22); s = "Foto: " + credit
        tw = d.textlength(s, font=f)
        d.rounded_rectangle([x + 18, yy + h - 52, x + 42 + tw, yy + h - 16], 18, fill=(11, 31, 51, int(170 * a)))
        d.text((x + 30, yy + h - 47), s, font=f, fill=rgba(WHITE, a))

def kb(name, w, h, t, z0=1.0, z1=1.10, fx=0.5, fy=0.5, dur=5):
    return fit(photo(name), w, h, z0 + (z1 - z0) * min(1, t / dur), fx, fy)

def pill(d, x, y, s, f, fg, bg, a, pad=22, h=None, anchor="l"):
    if a <= 0: return 0
    tw = d.textlength(s, font=f); hh = h or f.size + 26
    if anchor == "r": x = x - tw - 2 * pad
    d.rounded_rectangle([x, y, x + tw + 2 * pad, y + hh], hh // 2, fill=rgba(bg, a))
    d.text((x + pad, y + hh / 2), s, font=f, fill=rgba(fg, a), anchor="lm")
    return tw + 2 * pad

def tick(d, cx, cy, r, col, a, ok=True):
    if a <= 0: return
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rgba(col, a))
    if ok: d.line([(cx - r * .45, cy + r * .02), (cx - r * .1, cy + r * .38), (cx + r * .5, cy - r * .35)], fill=rgba(WHITE, a), width=max(4, r // 5), joint="curve")
    else:
        k = r * .38
        d.line([(cx - k, cy - k), (cx + k, cy + k)], fill=rgba(WHITE, a), width=max(4, r // 5))
        d.line([(cx - k, cy + k), (cx + k, cy - k)], fill=rgba(WHITE, a), width=max(4, r // 5))

# ---------- board ----------
TABS = ["2021 · OLDIN", "2026 · KEYIN", "YECHIM"]
def board():
    im = Image.new("RGBA", (W, H), BG + (255,)); d = ImageDraw.Draw(im)
    for y in range(0, H, 6):                                   # faint vertical gradient toward the bottom
        k = y / H; c = tuple(int(BG[i] + (BG2[i] - BG[i]) * k) for i in range(3))
        d.rectangle([0, y, W, y + 6], fill=c + (255,))
    for x in range(80, W, 92): d.line([(x, 1300), (x, H)], fill=(225, 241, 251, 255), width=2)
    return im
BOARD = None

def tabs(d, act, t):
    """top bar: which period this beat talks about. act = set of active tab indices"""
    f = fn("Bold", 28); x = 80
    for i, s in enumerate(TABS):
        tw = d.textlength(s, font=f) + 44
        on = i in act
        if on:
            d.rounded_rectangle([x, 112, x + tw, 166], 27, fill=(WARN if i == 0 else NAVY2 if i == 1 else SKYD) + (255,))
            d.text((x + 22, 139), s, font=f, fill=WHITE + (255,), anchor="lm")
        else:
            d.rounded_rectangle([x, 112, x + tw, 166], 27, outline=LINE + (255,), width=3)
            d.text((x + 22, 139), s, font=f, fill=(150, 170, 190, 255), anchor="lm")
        x += tw + 14
    d.text((1000, 139), "SALAR", font=fn("Black", 28), fill=NAVY + (200,), anchor="rm")

# ---------- beats (voice line, screen card) ----------
def b01_hook(im, d, t):           # "Salar hidiga 9,5 milliard so'm sarflandi. Ishladimi?"   [9,5 mlrd so'm. Ishladimi?]
    v = 9.5 * ph(t, 0.15, 1.0)
    f = fn("Black", 170)
    s = f"{v:.1f}".replace(".", ",")
    text(d, 80, 220, s, f, NAVY, ph(t, 0.0, 0.3))
    text(d, 80 + d.textlength("9,5", font=f) + 24, 300, "mlrd so'm", fn("Black", 64), SKYD, ph(t, 0.4))
    f2 = fn("Black", 96)
    marker(d, 80, 425, "Ishladimi?", f2, ph(t, 1.3, 0.45))
    text(d, 80, 425, "Ishladimi?", f2, NAVY, ph(t, 1.0, 0.35))
    # before/after slider: 2021 (grey, dirty water) | 2026 (filter units)
    a = ph(t, 0.2, 0.6)
    if a > 0:
        w, h = 920, 470; x, y = 80, 590
        left = ImageOps.grayscale(kb("dirty2", w, h, t, 1.05, 1.12)).convert("RGB")
        left = Image.blend(left, Image.new("RGB", (w, h), (120, 130, 140)), 0.15)
        right = kb("filter", w, h, t, 1.0, 1.08, 0.5, 0.45)
        sx = int(w * (0.82 - 0.42 * ease((t - 0.8) / 1.6)) + 18 * math.sin(t * 1.3))
        comp = right.copy(); comp.paste(left.crop((0, 0, sx, h)), (0, 0))
        pane(im, comp, x, y, a)
        yy = int(y + (1 - a) * 30)
        d.line([(x + sx, yy), (x + sx, yy + h)], fill=WHITE + (255,), width=6)
        d.ellipse([x + sx - 26, yy + h / 2 - 26, x + sx + 26, yy + h / 2 + 26], fill=WHITE + (255,))
        d.polygon([(x + sx - 14, yy + h / 2), (x + sx - 4, yy + h / 2 - 10), (x + sx - 4, yy + h / 2 + 10)], fill=NAVY + (255,))
        d.polygon([(x + sx + 14, yy + h / 2), (x + sx + 4, yy + h / 2 - 10), (x + sx + 4, yy + h / 2 + 10)], fill=NAVY + (255,))
        pill(d, x + 20, yy + 20, "2021", fn("Black", 32), WHITE, WARN, a)
        pill(d, x + w - 20, yy + 20, "2026", fn("Black", 32), WHITE, NAVY2, a, anchor="r")
        f3 = fn("SemiBold", 22)
        d.text((x + 20, yy + h + 14), "Foto: Yuz.uz  |  Toshkent sh. hokimligi / Gazeta.uz", font=f3, fill=INK2 + (int(255 * a),))

def pond(d, x0, y0, w, h, lid, t, gas=1.0, clean=False):
    """schematic pond cross-section: earth, water, gas bubbles; lid 0..1 slides in from the right"""
    d.rounded_rectangle([x0, y0 + 60, x0 + w, y0 + h], 30, fill=(205, 222, 235, 255))
    d.rounded_rectangle([x0 + 30, y0 + 90, x0 + w - 30, y0 + h - 30], 24, fill=(122, 138, 120, 255))
    for k in range(5):                                       # surface ripples
        yy = y0 + 110 + k * 34
        d.line([(x0 + 60, yy), (x0 + w - 60, yy)], fill=(140, 156, 136, 255), width=3)
    lx = x0 + w - (w + 40) * ease(lid)
    for k in range(9):                                       # rising H2S
        ph0 = (t * 0.55 + k * 0.137) % 1.0
        bx = x0 + 90 + k * (w - 180) / 8 + 12 * math.sin(t * 2 + k)
        by = y0 + 210 - ph0 * 260
        if lid > 0.05 and by < y0 + 70 and bx > lx: continue          # trapped under the lid
        r = 10 + 6 * (k % 3); al = gas * (1 - ph0) * (0.25 if (lid > 0.9 and by < y0 + 70) else 1)
        if by < y0 + 70 and lid > 0.95: continue
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=(242, 196, 64, int(200 * al)), outline=(200, 150, 30, int(220 * al)), width=2)
    if lid > 0:
        d.rounded_rectangle([lx, y0 + 40, x0 + w + 20, y0 + 80], 14, fill=NAVY2 + (255,))
        for k in range(int((x0 + w + 20 - lx) // 70)):
            bx = lx + 30 + k * 70
            d.ellipse([bx - 5, y0 + 55, bx + 5, y0 + 65], fill=SKY + (255,))

def b02_yopildi(im, d, t):        # "2026 yil yozida hovuzlar germetik yopildi."   [Hovuzlar yopildi (2026)]
    text(d, 80, 236, "2026 yil yozi", fn("Bold", 42), SKYD, ph(t, 0.05))
    f = fn("Black", 84)
    text(d, 80, 296, "Hovuzlar", f, NAVY, ph(t, 0.15))
    marker(d, 80, 392, "yopildi", f, ph(t, 1.5, 0.4))
    text(d, 80, 392, "yopildi", f, NAVY, ph(t, 0.3))
    pond(d, 80, 540, 920, 420, ph(t, 0.7, 1.1), t)
    a = ph(t, 1.9, 0.35)
    if a > 0:
        pill(d, 700, 520, "GERMETIK", fn("Black", 34), WHITE, NAVY2, a)
    text(d, 80, 985, "H₂S ichkarida qoladi", fn("Bold", 38), INK2, ph(t, 2.1))
    pane(im, kb("plant26", 760, 420, t, 1.0, 1.08), 160, 1360, ph(t, 0.4, 0.6), "Toshkent sh. hokimligi / Kun.uz")

def b03_filtr(im, d, t):          # "Ichidagi havo sorbent, ultrabinafsha nur va ko'mirdan o'tkaziladi."   [Sorbent · UB · ko'mir]
    text(d, 80, 236, "Havo 3 bosqichda", fn("Bold", 42), SKYD, ph(t, 0.05))
    text(d, 80, 296, "tozalanadi", fn("Black", 84), NAVY, ph(t, 0.15))
    st = [("Sorbent", "gazni yutadi", 0.5), ("UB nur", "parchalaydi", 1.2), ("Ko'mir", "qolganini ushlaydi", 1.9)]
    x0, y0 = 80, 460
    for k, (n, s, t0) in enumerate(st):
        a = ph(t, t0, 0.4); yy = y0 + k * 150
        if a <= 0: continue
        sc = 0.9 + 0.1 * back(min(1, (t - t0) / 0.4))
        d.rounded_rectangle([x0, yy, x0 + 600 * sc, yy + 122], 26, fill=rgba(WHITE, a), outline=rgba(NAVY2, a), width=4)
        d.ellipse([x0 + 24, yy + 26, x0 + 94, yy + 96], fill=rgba(SKYD if k != 1 else (120, 90, 220), a))
        text(d, x0 + 59, yy + 61, str(k + 1), fn("Black", 40), WHITE, a, "mm")
        text(d, x0 + 120, yy + 20, n, fn("Black", 50), NAVY, a)
        text(d, x0 + 120, yy + 78, s, fn("SemiBold", 30), INK2, a)
        if k < 2 and ph(t, st[k + 1][2] - 0.2) > 0:
            d.polygon([(x0 + 280, yy + 128), (x0 + 320, yy + 128), (x0 + 300, yy + 146)], fill=NAVY2 + (255,))
    # air flow on the right: dirty (yellow) dots in, clean (sky) out
    for k in range(10):
        u = (t * 0.6 + k * 0.1) % 1.0
        yy = y0 - 30 + u * 520; xx = 760 + 30 * math.sin(u * 6 + k)
        col = (242, 196, 64) if u < 0.75 else SKY
        r = 14 if u < 0.75 else 10
        d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=col + (int(220 * ph(t, 0.4)),))
    a = ph(t, 2.4)
    if a > 0:
        pill(d, 680, 1000, "toza havo ↓", fn("Bold", 34), NAVY, SKY, a)
    pane(im, kb("filter", 840, 420, t, 1.0, 1.08, 0.5, 0.45), 120, 1360, ph(t, 0.3, 0.6), "Toshkent sh. hokimligi / Gazeta.uz")

def b04_rasmiy(im, d, t):         # "Rasmiylar chiqayotgan havoda H₂S nolga tushdi, deyishmoqda."   [Rasmiy: H₂S = 0]
    a = ph(t, 0.05)
    pill(d, 80, 236, "RASMIY MA'LUMOT", fn("Bold", 30), WHITE, NAVY2, a)
    text(d, 80, 310, "Chiqayotgan havoda", fn("Bold", 46), INK2, ph(t, 0.2))
    f = fn("Black", 180)
    v = max(0.0, 1 - ph(t, 0.6, 1.4))
    text(d, 80, 380, "H₂S", f, NAVY, ph(t, 0.3))
    text(d, 470, 380, "=", f, SKYD, ph(t, 0.5))
    val = "0" if v < 0.02 else f"{v * 9:.0f}"
    text(d, 650, 380, val, f, SKYD if v < 0.02 else WARN, ph(t, 0.5))
    # gauge
    cx, cy, R = 540, 960, 250
    ga = ph(t, 0.3, 0.6)
    if ga > 0:
        d.pieslice([cx - R, cy - R, cx + R, cy + R], 180, 360, fill=rgba(WHITE, ga))
        for k in range(11):
            ang = math.pi + k * math.pi / 10
            r1, r2 = R - 18, R - (46 if k % 5 == 0 else 32)
            d.line([(cx + r1 * math.cos(ang), cy + r1 * math.sin(ang)), (cx + r2 * math.cos(ang), cy + r2 * math.sin(ang))], fill=rgba(NAVY, ga), width=5)
        d.arc([cx - R + 8, cy - R + 8, cx + R - 8, cy + R - 8], 180, 240, fill=rgba(SKYD, ga), width=14)
        d.arc([cx - R + 8, cy - R + 8, cx + R - 8, cy + R - 8], 300, 360, fill=rgba(WARN, ga), width=14)
        ang = math.pi + (0.15 + 0.75 * v) * math.pi + 0.03 * math.sin(t * 9) * v
        d.line([(cx, cy), (cx + (R - 60) * math.cos(ang), cy + (R - 60) * math.sin(ang))], fill=rgba(NAVY, ga), width=10)
        d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=rgba(NAVY, ga))
        text(d, cx - R + 40, cy - 60, "0", fn("Black", 40), SKYD, ga)
    text(d, 80, 1010, "texnologlar so'zi, 2026 yil sentyabr", fn("SemiBold", 32), INK2, ph(t, 1.8))

def b05_havo_suv(im, d, t):       # "Lekin bu havoni tozalaydi, suvni emas."   [Havo toza ≠ suv toza]
    text(d, 80, 236, "Lekin…", fn("Black", 84), NAVY, ph(t, 0.05))
    cols = [(80, "HAVO", True, "filter", "Toshkent sh. hokimligi / Gazeta.uz", 0.3, NAVY2), (580, "SUV", False, "dirty2", "Yuz.uz", 1.0, WARN)]
    for x, lab, ok, img, cr, t0, col in cols:
        a = ph(t, t0, 0.45)
        if a <= 0: continue
        pic = kb(img, 420, 420, t, 1.0, 1.08, 0.5, 0.45)
        if not ok: pic = Image.blend(pic, ImageOps.grayscale(pic).convert("RGB"), 0.35)
        pane(im, pic, x, 400, a, cr)
        f = fn("Black", 76); text(d, x, 860, lab, f, NAVY, a)
        tick(d, x + d.textlength(lab, font=f) + 60, 905, 40, SKYD if ok else WARN, ph(t, t0 + 0.35, 0.3), ok)
        text(d, x, 955, "filtrlanadi" if ok else "filtrlanmaydi", fn("Bold", 38), col, ph(t, t0 + 0.4))
    a = ph(t, 1.6, 0.3)
    if a > 0:
        r = 52 * (0.8 + 0.2 * back(min(1, (t - 1.6) / 0.3)))
        d.ellipse([540 - r, 610 - r, 540 + r, 610 + r], fill=rgba(WHITE, a), outline=rgba(WARN, a), width=5)
        text(d, 540, 610, "≠", fn("Black", 70), WARN, a, "mm")

FACT = [(k % 6, k // 6) for k in range(18)]
def factory(d, x, y, s, col, a):
    if a <= 0: return
    c = rgba(col, a)
    d.rectangle([x, y + 0.45 * s, x + s, y + s], fill=c)
    d.polygon([(x, y + 0.45 * s), (x + 0.33 * s, y + 0.2 * s), (x + 0.33 * s, y + 0.45 * s), (x + 0.66 * s, y + 0.2 * s), (x + 0.66 * s, y + 0.45 * s)], fill=c)
    d.rectangle([x + 0.75 * s, y, x + 0.9 * s, y + 0.45 * s], fill=c)

def b06_korxona(im, d, t):        # "2021 yilda hidning bir sababi 18 ta korxonaning oqovasi bo'lgan."   [18 ta korxona (2021)]
    n = int(round(18 * ph(t, 0.4, 1.6)))
    text(d, 80, 210, f"{n}", fn("Black", 170), WARN, ph(t, 0.05))
    text(d, 330, 250, "ta korxona", fn("Black", 60), NAVY, ph(t, 0.3))
    text(d, 330, 326, "oqovasini Salarga tashlagan", fn("Bold", 34), INK2, ph(t, 0.5))
    for k, (cx, cy) in enumerate(FACT):
        a = ph(t, 0.4 + k * 0.085, 0.25)
        factory(d, 90 + cx * 120, 470 + cy * 120, 84, WARN if k < 5 else NAVY2, a)
    a = ph(t, 2.1)
    if a > 0:
        d.rounded_rectangle([80, 850, 80 + 34, 884], 8, fill=rgba(WARN, a)); text(d, 128, 848, "teri zavodlari", fn("Bold", 32), NAVY, a)
        d.rounded_rectangle([450, 850, 450 + 34, 884], 8, fill=rgba(NAVY2, a)); text(d, 498, 848, "va boshqalar", fn("Bold", 32), NAVY, a)
    text(d, 80, 930, "Gazeta.uz tekshiruvi, 2021 yil iyun", fn("SemiBold", 30), INK2, ph(t, 2.4))
    pane(im, kb("sample", 760, 420, t, 1.0, 1.08), 160, 1360, ph(t, 0.3, 0.6), "Daryo (illyustrativ)")

def b07_fikr(im, d, t):           # "Mening fikrimcha, asosiy yechim boshqa:"   [Mening fikrim:]
    a = ph(t, 0.05, 0.35)
    text(d, 60, 170, "“", fn("Black", 300), SKY, a)
    text(d, 80, 420, "Mening", fn("Black", 110), NAVY, ph(t, 0.15))
    f = fn("Black", 110)
    marker(d, 80, 545, "fikrim:", f, ph(t, 0.6, 0.4))
    text(d, 80, 545, "fikrim:", f, NAVY, ph(t, 0.3))
    pill(d, 80, 740, "FIKR · fakt emas", fn("Bold", 34), WHITE, SKYD, ph(t, 0.9, 0.3))
    text(d, 80, 840, "Javohir · suv va oqova suv tadqiqotchisi", fn("SemiBold", 32), INK2, ph(t, 1.1))

def b08_yechim(im, d, t):         # "korxonalar oqovasini kanalizatsiyaga tashlashdan oldin o'zi tozalashi."   [Korxona o'zi tozalasin]
    text(d, 80, 236, "Asosiy yechim:", fn("Bold", 42), SKYD, ph(t, 0.05))
    text(d, 80, 296, "Korxona", fn("Black", 84), NAVY, ph(t, 0.15))
    f = fn("Black", 84)
    marker(d, 80, 392, "o'zi tozalasin", f, ph(t, 1.6, 0.4))
    text(d, 80, 392, "o'zi tozalasin", f, NAVY, ph(t, 0.3))
    # chain: factory -> [own treatment] -> sewer -> Salar
    y = 640; xs = [80, 330, 600, 830]
    a0 = ph(t, 0.4)
    factory(d, xs[0] + 10, y - 40, 120, NAVY2, a0)
    text(d, xs[0] + 70, y + 110, "korxona", fn("Bold", 30), NAVY, a0, "ma")
    a1 = ph(t, 1.0, 0.4)
    if a1 > 0:
        sc = back(min(1, (t - 1.0) / 0.45))
        bx0, bx1 = xs[1] - 30 * sc + 30, xs[1] + 190 * sc
        d.rounded_rectangle([bx0, y - 50, bx1, y + 90], 24, fill=rgba(WHITE, a1), outline=rgba(SKYD, a1), width=6)
        text(d, (bx0 + bx1) / 2, y - 25, "o'z", fn("Black", 40), SKYD, a1, "ma")
        text(d, (bx0 + bx1) / 2, y + 22, "tozalash", fn("Black", 40), SKYD, a1, "ma")
        tick(d, bx1 - 6, y - 50, 30, SKYD, ph(t, 1.6, 0.3))
        text(d, xs[1] + 80, y + 110, "zavod ichida", fn("Bold", 30), SKYD, a1, "ma")
    a2 = ph(t, 1.4)
    if a2 > 0:
        d.rounded_rectangle([xs[2], y - 10, xs[2] + 170, y + 50], 30, outline=rgba(NAVY2, a2), width=6)
        text(d, xs[2] + 85, y + 110, "kanalizatsiya", fn("Bold", 30), NAVY, a2, "ma")
        d.ellipse([xs[3] + 10, y - 50, xs[3] + 170, y + 90], fill=rgba(BG2, a2), outline=rgba(NAVY2, a2), width=6)
        text(d, xs[3] + 90, y + 20, "Salar", fn("Black", 36), NAVY, a2, "mm")
    for k, (xa, xb, t0) in enumerate([(xs[0] + 135, xs[1] - 5, 0.8), (xs[1] + 225, xs[2] - 5, 1.4), (xs[2] + 175, xs[3] + 5, 1.6)]):
        a = ph(t, t0, 0.3)
        if a <= 0: continue
        d.line([(xa, y + 20), (xa + (xb - xa) * a, y + 20)], fill=NAVY2 + (255,), width=6)
        for j in range(3):                                      # flowing water dots (yellow before treatment, sky after)
            u = (t * 0.8 + j / 3) % 1
            px = xa + (xb - xa) * u
            col = (242, 196, 64) if k == 0 else SKY
            d.ellipse([px - 9, y + 11, px + 9, y + 29], fill=col + (int(255 * a),))
    text(d, 80, 900, "Kimyoviy modda inshootga yetib bormaydi", fn("Bold", 36), INK2, ph(t, 2.2))
    a = ph(t, 0.3, 0.6)
    pane(im, kb("plant26", 760, 420, t, 1.0, 1.08), 160, 1360, a, "Toshkent sh. hokimligi / Kun.uz")

def b09_end(im, d, t):            # "Sizningcha, 9,5 milliard to'g'ri sarflandimi? Izohda yozing."   [end card]
    text(d, 80, 236, "Sizningcha,", fn("Black", 76), NAVY, ph(t, 0.0))
    f = fn("Black", 76)
    marker(d, 80, 326, "9,5 milliard", f, ph(t, 0.5, 0.4))
    text(d, 80, 326, "9,5 milliard", f, NAVY, ph(t, 0.1))
    text(d, 80, 416, "to'g'ri sarflandimi?", f, NAVY, ph(t, 0.25))
    a = ph(t, 0.7)
    w = d.textlength("izohda yozing ↓", font=fn("Bold", 46)) + 60
    d.rounded_rectangle([80, 540, 80 + w, 622], 41, fill=rgba(SKY, a))
    text(d, 110, 555, "izohda yozing ↓", fn("Bold", 46), NAVY, a)
    text(d, 80, 700, "Suvni qadrlang!", fn("Black", 96), SKYD, ph(t, 1.2))
    text(d, 80, 830, "Bizni kuzatishda davom eting,", fn("SemiBold", 40), NAVY, ph(t, 1.6))
    text(d, 80, 882, "suv haqida suvyektiv fikrlaymiz!", fn("ExtraBold", 50), SKYD, ph(t, 1.9))
    text(d, 80, 980, "Doktor H₂O  ·  @suvyektiv", fn("Bold", 40), NAVY, ph(t, 2.3))

# (fn, dur s, active tabs, screen card for the alpha overlay)
B = [(b01_hook, 4.0, {0, 1}, "9,5 mlrd so'm. Ishladimi?"),
     (b02_yopildi, 3.5, {1}, "Hovuzlar yopildi (2026)"),
     (b03_filtr, 4.5, {1}, "Sorbent · UB · ko'mir"),
     (b04_rasmiy, 4.0, {1}, "Rasmiy: H₂S = 0"),
     (b05_havo_suv, 3.5, {1}, "Havo toza ≠ suv toza"),
     (b06_korxona, 5.0, {0}, "18 ta korxona (2021)"),
     (b07_fikr, 3.0, {2}, "Mening fikrim:"),
     (b08_yechim, 4.5, {2}, "Korxona o'zi tozalasin"),
     (b09_end, 5.0, set(), None)]

def frame(k, t):
    global BOARD
    if BOARD is None: BOARD = board()
    im = BOARD.copy(); d = ImageDraw.Draw(im)
    tabs(d, B[k][2], t); B[k][0](im, d, t)
    return im.convert("RGB")

def enc(out, alpha=False):
    v = ["-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le"] if alpha else \
        ["-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p"]
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba" if alpha else "rgb24",
                             "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", *v, out], stdin=subprocess.PIPE)

def render(k, out):
    p = enc(out)
    for f in range(int(round(B[k][1] * FPS))): p.stdin.write(frame(k, f / FPS).tobytes())
    p.stdin.close(); p.wait()

def overlay(k, out, dur=None):
    """transparent screen card for beats where Javohir is on camera: white panel at y 230-, fades in/out"""
    s = B[k][3]; dur = dur or B[k][1]
    p = enc(out, True); f = fn("Black", 72)
    tw = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength(s, font=f)
    while tw > 840: f = fn("Black", f.size - 4); tw = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength(s, font=f)
    for i in range(int(round(dur * FPS))):
        t = i / FPS; a = min(ph(t, 0.1, 0.35), 1 - ph(t, dur - 0.4, 0.35))
        im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
        if a > 0:
            x1 = 80 + (tw + 70) * ease(min(1, (t - 0.1) / 0.35))
            d.rounded_rectangle([80, 250, x1, 250 + f.size + 70], 26, fill=rgba(WHITE, 0.94 * a))
            d.rectangle([80, 250, 92, 250 + f.size + 70], fill=rgba(SKYD, a))
            text(d, 120, 280, s, f, NAVY, a)
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()

if __name__ == "__main__":
    if sys.argv[1] == "still":
        frame(int(sys.argv[2]), float(sys.argv[3])).save(sys.argv[4]); sys.exit()
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    only = [int(x) for x in sys.argv[2:]] or range(len(B))
    for k in only:
        name = B[k][0].__name__
        render(k, f"{out}/{name}.mp4")
        if B[k][3] and k in (0, 4, 6, 7): overlay(k, f"{out}/ov{k + 1:02d}_{name[4:]}.mov")   # Javohir-on-camera beats
        print("ok", name, flush=True)
