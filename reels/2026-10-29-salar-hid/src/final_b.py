"""Reel B '9,5 milliard' — final edit on Javohir's voice-over (Voice_261029_155606, 43.8 s of speech).
Format D: full-screen B-roll + data graphics (helpers/style from broll_b.py), subtitles 1:1 to the spoken words
(white Inter Bold 64, keywords #84D2FD, y~1180), own music bed (music_b.py).
usage: python3 final_b.py VOICE.wav MUSIC.wav OUT.mp4        |   python3 final_b.py still T out.png"""
import sys, os, re, math, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import broll_b as B
from broll_b import (fn, ph, ease, back, text, marker, pill, pane, kb, tick, factory, pond, rgba, board,
                     W, H, FPS, WHITE, SKY, SKYD, NAVY, NAVY2, WARN, INK2, LINE, BG2)
from PIL import Image, ImageDraw, ImageFilter

GREEN = (96, 160, 84)
TABS = ["HAVO", "SUV", "YECHIM"]
TCOL = [NAVY2, WARN, SKYD]
def tabs(d, act):
    f = fn("Bold", 28); x = 80
    for i, s in enumerate(TABS):
        s = tr(s); tw = d.textlength(s, font=f) + 44
        if i in act:
            d.rounded_rectangle([x, 112, x + tw, 166], 27, fill=TCOL[i] + (255,))
            d.text((x + 22, 139), s, font=f, fill=WHITE + (255,), anchor="lm")
        else:
            d.rounded_rectangle([x, 112, x + tw, 166], 27, outline=LINE + (255,), width=3)
            d.text((x + 22, 139), s, font=f, fill=(150, 170, 190, 255), anchor="lm")
        x += tw + 14
    d.text((1000, 139), "SALAR", font=fn("Black", 28), fill=NAVY + (200,), anchor="rm")

# ---------- English version (LinkedIn): same picture/voice, on-screen text + captions in English ----------
EN = "--en" in sys.argv
TR = {"HAVO": "AIR", "SUV": "WATER", "YECHIM": "SOLUTION",
 "Salardagi hidni yo'qotish uchun": "To remove the Salar smell", "mlrd so'm": "bn soums", "sarflangan": "spent",
 "Shu yil yozda": "This summer", "Hovuzlar": "Ponds", "germetik yopildi": "sealed airtight", "H₂S ichkarida qoladi": "H₂S stays inside",
 "Ichidagi havo": "The air inside", "filtrdan o'tkazildi": "is filtered", "gazni yutadi": "absorbs gas", "UB nur": "UV light",
 "parchalaydi": "breaks it down", "Ko'mir": "Carbon", "qolganini ushlaydi": "traps the rest", "toza havo ↓": "clean air ↓",
 "MUTASADDILAR AYTISHICHA": "OFFICIALS SAY", "vodorod sulfid miqdori": "hydrogen sulfide level",
 "Muammo hal bo'lmadi": "Problem not solved", "tozalanadi": "cleaned", "tozalanmaydi": "not cleaned",
 "Suv dalaga yaroqli bo'lishi uchun": "For water fit for farmland", "Har bir korxona": "Every company",
 "oqovasini tozalasin": "treats its wastewater", "korxona": "company", "o'z": "own", "tozalash": "treatment", "dala": "farm",
 "keyin Salarga, undan dalaga": "then to Salar, then to farms", "Har bir zavod uchun": "For every factory",
 "me'yor belgilangan": "limits are set", "ME'YOR": "LIMIT", "kimyoviy moddalar": "chemicals",
 "va ular shu me'yorga amal qilishi kerak": "and they must meet those limits",
 "Menimcha,": "In my view,", "mana shunda": "this is how", "muammo hal bo'ladi": "it gets solved",
 "FIKR · fakt emas": "OPINION · not a fact", "Javohir · suv va oqova suv tadqiqotchisi": "Javohir · water & wastewater researcher",
 "Suvni qadrlang!": "Value water!", "Suv haqida bilmoqchi bo'lganlaringizni": "What would you like to know about water?",
 "izohlarda yozib qoldiring ↓": "Tell us in the comments ↓", "Bizni kuzatishda davom eting,": "Keep following us,",
 "suv haqida suvyektiv": "let's think about water,", "fikrlaymiz!": "suvyektiv style!",
 "Toshkent sh. hokimligi / Gazeta.uz": "Tashkent city hall / Gazeta.uz", "Toshkent sh. hokimligi / Kun.uz": "Tashkent city hall / Kun.uz",
 "Daryo (illyustrativ)": "Daryo (illustrative)"}
def tr(s):
    if not EN: return s
    s = TR.get(s, s)
    return re.sub(r"(\d),(\d)", r"\1.\2", s)
_text, _marker, _pill, _pane = text, marker, pill, pane
def text(d, x, y, s, *a, **k): return _text(d, x, y, tr(s), *a, **k)
def marker(d, x, y, s, *a, **k): return _marker(d, x, y, tr(s), *a, **k)
def pill(d, x, y, s, *a, **k): return _pill(d, x, y, tr(s), *a, **k)
def pane(im, img, x, y, a, credit="", *r, **k): return _pane(im, img, x, y, a, tr(credit), *r, **k)
if EN: B.FOTO = "Photo: "

# ---------- scenes (local t) ----------
def s_hook(im, d, t):             # 0.00 "Salardagi hidni yo'qotish uchun jami 9,5 milliard so'm sarflanganligi aytilmoqda."
    text(d, 80, 232, "Salardagi hidni yo'qotish uchun", fn("Bold", 44), SKYD, ph(t, 0.0, 0.3))
    f = fn("Black", 170); v = 9.5 * ph(t, 1.6, 0.9)
    text(d, 80, 290, f"{v:.1f}".replace(".", ","), f, NAVY, ph(t, 0.1, 0.3))
    text(d, 80 + d.textlength("9,5", font=f) + 24, 370, "mlrd so'm", fn("Black", 64), SKYD, ph(t, 0.5))
    f2 = fn("Black", 80)
    marker(d, 80, 500, "sarflangan", f2, ph(t, 3.1, 0.45))
    text(d, 80, 500, "sarflangan", f2, NAVY, ph(t, 2.9, 0.35))
    pane(im, kb("filter", 920, 420, t, 1.0, 1.10, 0.5, 0.45), 80, 640, ph(t, 0.1, 0.6), "Toshkent sh. hokimligi / Gazeta.uz")

def s_yopildi(im, d, t):          # 4.78 "Shu yil yozda tozalash hovuzlari germetik yopildi"
    text(d, 80, 236, "Shu yil yozda", fn("Bold", 42), SKYD, ph(t, 0.05))
    f = fn("Black", 84)
    text(d, 80, 296, "Hovuzlar", f, NAVY, ph(t, 0.15))
    marker(d, 80, 392, "germetik yopildi", f, ph(t, 2.3, 0.4))
    text(d, 80, 392, "germetik yopildi", f, NAVY, ph(t, 1.9))
    pond(d, 80, 560, 920, 420, ph(t, 1.6, 1.1), t)
    text(d, 80, 1000, "H₂S ichkarida qoladi", fn("Bold", 38), INK2, ph(t, 2.4))
    pane(im, kb("plant26", 760, 420, t, 1.0, 1.08), 160, 1360, ph(t, 0.3, 0.6), "Toshkent sh. hokimligi / Kun.uz")

def s_filtr(im, d, t):            # 7.74 "va ichidagi havo sorbent, ultrabinafsha nur va ko'mirdan o'tkazildi."
    text(d, 80, 236, "Ichidagi havo", fn("Bold", 42), SKYD, ph(t, 0.05))
    text(d, 80, 296, "filtrdan o'tkazildi", fn("Black", 84), NAVY, ph(t, 0.15))
    st = [("Sorbent", "gazni yutadi", 0.6), ("UB nur", "parchalaydi", 1.4), ("Ko'mir", "qolganini ushlaydi", 2.5)]
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
    for k in range(10):
        u = (t * 0.6 + k * 0.1) % 1.0
        yy = y0 - 30 + u * 520; xx = 760 + 30 * math.sin(u * 6 + k)
        col = (242, 196, 64) if u < 0.75 else SKY; r = 14 if u < 0.75 else 10
        d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=col + (int(220 * ph(t, 0.4)),))
    pill(d, 680, 1000, "toza havo ↓", fn("Bold", 34), NAVY, SKY, ph(t, 3.0))
    pane(im, kb("filter", 840, 420, t, 1.04, 1.12, 0.6, 0.45), 120, 1360, ph(t, 0.3, 0.6), "Toshkent sh. hokimligi / Gazeta.uz")

def s_nol(im, d, t):              # 11.50 "Mutasaddilarning aytishicha, vodorod sulfid miqdori nolga tushgan."
    pill(d, 80, 236, "MUTASADDILAR AYTISHICHA", fn("Bold", 30), WHITE, NAVY2, ph(t, 0.2))
    text(d, 80, 310, "vodorod sulfid miqdori", fn("Bold", 46), INK2, ph(t, 1.5))
    f = fn("Black", 180); v = max(0.0, 1 - ph(t, 1.6, 1.3))
    text(d, 80, 380, "H₂S", f, NAVY, ph(t, 1.5))
    text(d, 470, 380, "=", f, SKYD, ph(t, 1.7))
    text(d, 650, 380, "0" if v < 0.02 else f"{v * 9:.0f}", f, SKYD if v < 0.02 else WARN, ph(t, 1.7))
    cx, cy, R = 540, 960, 250; ga = ph(t, 0.3, 0.6)
    if ga > 0:
        d.pieslice([cx - R, cy - R, cx + R, cy + R], 180, 360, fill=rgba(WHITE, ga))
        for k in range(11):
            ang = math.pi + k * math.pi / 10; r1, r2 = R - 18, R - (46 if k % 5 == 0 else 32)
            d.line([(cx + r1 * math.cos(ang), cy + r1 * math.sin(ang)), (cx + r2 * math.cos(ang), cy + r2 * math.sin(ang))], fill=rgba(NAVY, ga), width=5)
        d.arc([cx - R + 8, cy - R + 8, cx + R - 8, cy + R - 8], 180, 240, fill=rgba(SKYD, ga), width=14)
        d.arc([cx - R + 8, cy - R + 8, cx + R - 8, cy + R - 8], 300, 360, fill=rgba(WARN, ga), width=14)
        ang = math.pi + (0.15 + 0.75 * v) * math.pi + 0.03 * math.sin(t * 9) * v
        d.line([(cx, cy), (cx + (R - 60) * math.cos(ang), cy + (R - 60) * math.sin(ang))], fill=rgba(NAVY, ga), width=10)
        d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=rgba(NAVY, ga))
        text(d, cx - R + 40, cy - 60, "0", fn("Black", 40), SKYD, ga)

def s_havo_suv(im, d, t):         # 15.30 "Lekin hali muammo hal bo'lmadi. Bu uskuna faqat havoni tozalaydi, suvni emas."
    text(d, 80, 236, "Muammo hal bo'lmadi", fn("Black", 70), NAVY, ph(t, 0.3))
    cols = [(80, "HAVO", True, "filter", "Toshkent sh. hokimligi / Gazeta.uz", 2.3, NAVY2), (580, "SUV", False, "dirty2", "Yuz.uz", 4.0, WARN)]
    for x, lab, ok, img, cr, t0, col in cols:
        a = ph(t, t0, 0.45)
        if a <= 0: continue
        pic = kb(img, 420, 420, t, 1.0, 1.08, 0.5, 0.45)
        if not ok: pic = Image.blend(pic, pic.convert("L").convert("RGB"), 0.35)
        pane(im, pic, x, 400, a, cr)
        f = fn("Black", 76); text(d, x, 860, lab, f, NAVY, a)
        tick(d, x + d.textlength(tr(lab), font=f) + 60, 905, 40, SKYD if ok else WARN, ph(t, t0 + 0.3, 0.3), ok)
        text(d, x, 955, "tozalanadi" if ok else "tozalanmaydi", fn("Bold", 38), col, ph(t, t0 + 0.35))
    a = ph(t, 4.3, 0.3)
    if a > 0:
        r = 52 * (0.8 + 0.2 * back(min(1, (t - 4.3) / 0.3)))
        d.ellipse([540 - r, 610 - r, 540 + r, 610 + r], fill=rgba(WHITE, a), outline=rgba(WARN, a), width=5)
        text(d, 540, 610, "≠", fn("Black", 70), WARN, a, "mm")

def field(d, x, y, w, h, a):
    if a <= 0: return
    d.rounded_rectangle([x, y, x + w, y + h], 20, fill=rgba((214, 232, 196), a), outline=rgba(GREEN, a), width=5)
    for k in range(4):
        yy = y + 26 + k * (h - 40) / 4
        d.line([(x + 18, yy), (x + w - 18, yy)], fill=rgba(GREEN, a), width=5)
        for j in range(4):
            sx = x + 30 + j * (w - 60) / 3
            d.line([(sx, yy), (sx, yy - 14)], fill=rgba(GREEN, a), width=4)
            d.ellipse([sx - 8, yy - 22, sx, yy - 12], fill=rgba(GREEN, a))

def s_korxona(im, d, t):          # 20.35 "Suvni yaroqli holatda qishloq xo'jaligiga berishdan oldin har bir korxona chiqayotgan oqovasini tozalab, keyin bu yerga jo'natishi kerak."
    text(d, 80, 236, "Suv dalaga yaroqli bo'lishi uchun", fn("Bold", 40), GREEN, ph(t, 0.2))
    f = fn("Black", 80)
    text(d, 80, 296, "Har bir korxona", f, NAVY, ph(t, 3.7))
    marker(d, 80, 392, "oqovasini tozalasin", f, ph(t, 5.0, 0.4))
    text(d, 80, 392, "oqovasini tozalasin", f, NAVY, ph(t, 4.7))
    y = 660
    a0 = ph(t, 3.7)
    factory(d, 90, y - 50, 120, NAVY2, a0); text(d, 150, y + 100, "korxona", fn("Bold", 28), NAVY, a0, "ma")
    a1 = ph(t, 4.7, 0.4)
    if a1 > 0:
        sc = back(min(1, (t - 4.7) / 0.45)); cx = 355
        d.rounded_rectangle([cx - 95 * sc, y - 55, cx + 95 * sc, y + 75], 24, fill=rgba(WHITE, a1), outline=rgba(SKYD, a1), width=6)
        text(d, cx, y - 34, "o'z", fn("Black", 38), SKYD, a1, "ma"); text(d, cx, y + 10, "tozalash", fn("Black", 38), SKYD, a1, "ma")
        tick(d, cx + 92, y - 55, 28, SKYD, ph(t, 5.4, 0.3))
    a2 = ph(t, 6.3)
    if a2 > 0:
        d.ellipse([530, y - 70, 700, y + 100], fill=rgba(BG2, a2), outline=rgba(NAVY2, a2), width=6)
        text(d, 615, y + 15, "Salar", fn("Black", 36), NAVY, a2, "mm")
    field(d, 790, y - 60, 200, 150, ph(t, 1.2))
    text(d, 890, y + 100, "dala", fn("Bold", 28), GREEN, ph(t, 1.2), "ma")
    for k, (xa, xb, t0, dirty) in enumerate([(220, 255, 4.4, True), (455, 525, 6.1, False), (705, 785, 6.8, False)]):
        a = ph(t, t0, 0.3)
        if a <= 0: continue
        d.line([(xa, y + 15), (xa + (xb - xa) * a, y + 15)], fill=NAVY2 + (255,), width=6)
        for j in range(2):
            u = (t * 0.8 + j / 2) % 1; px = xa + (xb - xa) * u
            d.ellipse([px - 8, y + 7, px + 8, y + 23], fill=((242, 196, 64) if dirty else SKY) + (int(255 * a),))
    text(d, 80, 900, "keyin Salarga, undan dalaga", fn("Bold", 36), INK2, ph(t, 6.4))
    pane(im, kb("plant26", 760, 420, t, 1.0, 1.08), 160, 1360, ph(t, 0.3, 0.6), "Toshkent sh. hokimligi / Kun.uz")

def s_meyor(im, d, t):            # 28.40 "Har bir zavod uchun suvdagi kimyoviy moddalarni oqova chiqarishda me'yor belgilangan. Va ular mana shu me'yorga amal qilishlari kerak bo'ladi."
    text(d, 80, 236, "Har bir zavod uchun", fn("Bold", 42), SKYD, ph(t, 0.2))
    f = fn("Black", 80)
    marker(d, 80, 296, "me'yor belgilangan", f, ph(t, 4.8, 0.4))
    text(d, 80, 296, "me'yor belgilangan", f, NAVY, ph(t, 4.5))
    base, top = 960, 470; NORM = 690
    drop = ph(t, 7.8, 1.0)
    for k, lvl in enumerate([0.88, 0.72, 0.95]):
        a = ph(t, 1.4 + 0.25 * k, 0.4)
        if a <= 0: continue
        x = 110 + k * 250; w = 150
        hi = lvl * (base - top) * a; lo = 0.38 * (base - top)
        hgt = hi + (lo - hi) * drop
        d.rounded_rectangle([x, top - 10, x + w, base], 18, outline=rgba(LINE, a), width=4, fill=rgba(WHITE, a))
        over = base - hgt < NORM
        if hgt > 30: d.rounded_rectangle([x + 10, base - hgt, x + w - 10, base - 8], 12, fill=rgba(WARN if over else SKYD, a))
        factory(d, x + 35, base + 20, 80, NAVY2, a)
        if drop > 0.95: tick(d, x + w - 6, top + 34, 26, SKYD, ph(t, 8.6, 0.3))
    a = ph(t, 4.5, 0.5)
    if a > 0:
        for xx in range(90, 830, 34): d.line([(xx, NORM), (min(xx + 20, 830), NORM)], fill=rgba(NAVY, a), width=6)
        pill(d, 840, NORM - 28, "ME'YOR", fn("Black", 28), WHITE, NAVY, a)
    text(d, 80, 410, "kimyoviy moddalar", fn("Bold", 36), INK2, ph(t, 1.6))
    text(d, 80, 1075, "va ular shu me'yorga amal qilishi kerak", fn("Bold", 34), NAVY, ph(t, 6.6))
    pane(im, kb("sample", 760, 420, t, 1.0, 1.08), 160, 1360, ph(t, 0.3, 0.6), "Daryo (illyustrativ)")

def s_fikr(im, d, t):             # 37.56 "Menimcha, mana shunda muammoni hal qilsa bo'ladi."
    text(d, 60, 170, "“", fn("Black", 300), SKY, ph(t, 0.0, 0.3))
    text(d, 80, 420, "Menimcha,", fn("Black", 110), NAVY, ph(t, 0.1))
    f = fn("Black", 76)
    marker(d, 80, 560, "mana shunda", f, ph(t, 0.9, 0.4))
    text(d, 80, 560, "mana shunda", f, NAVY, ph(t, 0.6))
    text(d, 80, 650, "muammo hal bo'ladi", f, NAVY, ph(t, 1.4))
    pill(d, 80, 790, "FIKR · fakt emas", fn("Bold", 34), WHITE, SKYD, ph(t, 0.5, 0.3))
    text(d, 80, 890, "Javohir · suv va oqova suv tadqiqotchisi", fn("SemiBold", 32), INK2, ph(t, 0.7))

def s_end(im, d, t):              # 40.30 "Bizni kuzatishda davom eting, suv haqida suvyektiv fikrlaymiz!"
    text(d, 80, 280, "Suvni qadrlang!", fn("Black", 96), SKYD, ph(t, 0.0))
    text(d, 80, 410, "Suv haqida bilmoqchi bo'lganlaringizni", fn("SemiBold", 40), NAVY, ph(t, 0.2))
    text(d, 80, 462, "izohlarda yozib qoldiring ↓", fn("Bold", 40), NAVY, ph(t, 0.3))
    text(d, 80, 580, "Bizni kuzatishda davom eting,", fn("Black", 56), NAVY, ph(t, 0.1))
    f = fn("Black", 56)
    marker(d, 80, 650, "suv haqida suvyektiv", f, ph(t, 1.9, 0.5))
    text(d, 80, 650, "suv haqida suvyektiv", f, NAVY, ph(t, 1.6))
    text(d, 80, 720, "fikrlaymiz!", f, NAVY, ph(t, 2.4))
    text(d, 80, 860, "Doktor H₂O  ·  @suvyektiv", fn("Bold", 44), NAVY, ph(t, 0.8))

# (start s, scene, active tabs)
SC = [(0.0, s_hook, {0}), (4.78, s_yopildi, {0}), (7.74, s_filtr, {0}), (11.50, s_nol, {0}), (15.30, s_havo_suv, {0, 1}),
      (20.35, s_korxona, {1, 2}), (28.40, s_meyor, {2}), (37.56, s_fikr, {2}), (40.30, s_end, set())]
TOTAL = 45.3

# ---------- subtitles: 1:1 to the spoken words (times from faster-whisper word stamps) ----------
CAPS = [(0.000, 1.720, "Salardagi hidni yo'qotish uchun"), (1.720, 3.080, "jami 9,5 milliard so'm"), (3.080, 4.780, "sarflanganligi aytilmoqda."),
        (4.780, 5.780, "Shu yil yozda"), (5.780, 7.740, "tozalash hovuzlari germetik yopildi"), (7.740, 9.140, "va ichidagi havo sorbent,"),
        (9.140, 11.220, "ultrabinafsha nur va ko'mirdan o'tkazildi."), (11.820, 13.040, "Mutasaddilarning aytishicha,"),
        (13.040, 14.980, "vodorod sulfid miqdori nolga tushgan."), (15.540, 17.300, "Lekin hali muammo hal bo'lmadi."),
        (17.300, 19.540, "Bu uskuna faqat havoni tozalaydi,"), (19.540, 20.100, "suvni emas."), (20.580, 21.560, "Suvni yaroqli holatda"),
        (21.560, 24.060, "qishloq xo'jaligiga berishdan oldin"), (24.060, 25.040, "har bir korxona"), (25.040, 26.520, "chiqayotgan oqovasini tozalab,"),
        (26.520, 28.120, "keyin bu yerga jo'natishi kerak."), (28.620, 29.800, "Har bir zavod uchun"), (29.800, 32.000, "suvdagi kimyoviy moddalarni"),
        (32.000, 34.260, "oqova chiqarishda me'yor belgilangan."), (34.900, 36.200, "Va ular mana shu me'yorga"),
        (36.200, 37.680, "amal qilishlari kerak bo'ladi."), (37.680, 38.900, "Menimcha, mana shunda"), (38.900, 40.380, "muammoni hal qilsa bo'ladi."),
        (40.380, 41.940, "Bizni kuzatishda davom eting,"), (41.940, 43.760, "suv haqida suvyektiv fikrlaymiz!")]
if EN:
    CAPS = [(0.00, 4.78, "About 9.5 billion soums were reportedly spent to remove the smell at Salar."),
            (4.78, 11.22, "This summer the treatment ponds were sealed, and the air inside was passed through sorbent, UV light and carbon."),
            (11.82, 14.98, "Officials say hydrogen sulfide levels dropped to zero."),
            (15.54, 17.30, "But the problem isn't solved yet."),
            (17.30, 20.10, "This unit only cleans the air, not the water."),
            (20.58, 28.12, "Before the water can safely go to farms, every company must treat its own wastewater and only then send it here."),
            (28.62, 34.26, "Every factory has limits for chemicals in its wastewater discharge."),
            (34.90, 37.68, "And they have to meet those limits."),
            (37.68, 40.38, "In my view, that's how the problem can be solved."),
            (40.38, 43.76, "Keep following us, and let's think about water, suvyektiv style!")]
KEY = re.compile(r"\d|billion|sealed|sorbent|UV|carbon|hydrogen|sulfide|zero|air|water|farms|treat|limits|chemicals|milliard|germetik|sorbent|ultrabinafsha|ko'mir|vodorod|sulfid|nolga|havoni|suvni|qishloq|xo'jaligi|korxona|tozala|me'yor|kimyoviy|suvyektiv", re.I)
CF = fn("Bold", 64)
EV = []
for a, b, s in CAPS:                                   # split long lines (> 24 chars) proportionally, as in earlier reels
    words = s.split(" "); chunks = []; cur = []
    for w in words:
        if cur and len(" ".join(cur + [w])) > 24: chunks.append(cur); cur = []
        cur.append(w)
    chunks.append(cur); tot = sum(len(" ".join(c)) for c in chunks); t = a
    for c in chunks:
        dd = (b - a) * len(" ".join(c)) / tot; EV.append((t, t + dd, c)); t += dd

def caption(im, t, y=1180):
    cur = [e for e in EV if e[0] <= t < e[1]]
    if not cur: return
    t0, t1, ws = cur[0]; al = max(0, min(1, (t - t0) / 0.08, (t1 - t) / 0.06))
    lay = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(lay)
    widths = [d.textlength(w, font=CF) for w in ws]; sp = d.textlength(" ", font=CF)
    x = (W - sum(widths) - sp * (len(ws) - 1)) / 2
    for w, wd in zip(ws, widths):
        d.text((x, y), w, font=CF, fill=(SKY if KEY.search(w) else WHITE) + (255,), stroke_width=3, stroke_fill=(0, 0, 0, 160))
        x += wd + sp
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(lay.getchannel("A").point(lambda v: int(v * 0.6)))
    sh = sh.filter(ImageFilter.GaussianBlur(10))
    if al < 1:
        for L in (sh, lay): L.putalpha(L.getchannel("A").point(lambda v: int(v * al)))
    im.alpha_composite(sh, (0, 5)); im.alpha_composite(lay)

BOARD = None
def frame(T):
    global BOARD
    if BOARD is None: BOARD = board()
    k = max(i for i, s in enumerate(SC) if s[0] <= T)
    t0, fnc, act = SC[k]; t = T - t0
    im = BOARD.copy(); d = ImageDraw.Draw(im); tabs(d, act); fnc(im, d, t)
    if t < 0.18 and k > 0:                              # quick cross-fade from the previous scene
        p0, pf, pa = SC[k - 1]; prev = BOARD.copy(); pd = ImageDraw.Draw(prev); tabs(pd, pa); pf(prev, pd, T - p0)
        im = Image.blend(prev, im, ease(t / 0.18))
    caption(im, T)
    return im.convert("RGB")

def build(voice, music, out):
    v = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", voice, "-i", music, "-filter_complex",
                          f"[1:a]apad,atrim=0:{TOTAL},loudnorm=I=-15:TP=-1.5:LRA=9,aresample=48000,asplit[vo][vk];"
                          f"[2:a]atrim=0:{TOTAL},volume=0.16,afade=t=out:st={TOTAL - 1.5}:d=1.5[mu];"
                          "[mu][vk]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=300[duck];"
                          "[duck][vo]amix=inputs=2:normalize=0[a]",
                          "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", str(TOTAL), out], stdin=subprocess.PIPE)
    for f in range(int(round(TOTAL * FPS))): v.stdin.write(frame(f / FPS).tobytes())
    v.stdin.close(); v.wait()

if __name__ == "__main__":
    argv = [x for x in sys.argv if x != "--en"]
    if argv[1] == "still": frame(float(argv[2])).save(argv[3])
    else: build(*argv[1:4])
