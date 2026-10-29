"""Salar Reel A (29.10, final voice) — 'tergov / ish papkasi' style on light paper.
Full B-roll + Javohir's voice (no A-roll). Scenes follow the spoken sentences (timeline.py).
Subtitles: white bold Inter 64, keywords #84D2FD, static, centred at y~1180.
usage: render.py scenes OUT.mp4 | still SCENE T out.png | cover out.jpg"""
import sys, os, math, re, random, subprocess
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import timeline as TL

W, H, FPS = 1080, 1920, 30
PH = os.environ.get("PH", "/tmp/claude-0/sal") + "/"
F = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
WHITE, SKY, SKYD, NAVY, WARN = (255, 255, 255), (132, 210, 253), (31, 111, 178), (11, 31, 51), (226, 88, 62)
INK2, PAPER, SULF, NAVYB = (70, 88, 108), (241, 245, 248), (242, 196, 64), (31, 58, 128)
_fc = {}
def fn(w, s):
    if (w, s) not in _fc: _fc[(w, s)] = ImageFont.truetype(F.format(w), s)
    return _fc[(w, s)]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def ph(t, t0, d=0.45): return ease((t - t0) / d)
def back(u): u = max(0, min(1, u)); c = 1.7; return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2

# ---------- timeline ----------
SENT = TL.sentences()
VOICE_END = 59.36
END_HOLD = 3.0
TOTAL = VOICE_END + END_HOLD
ORDER = []
for a, b, s, sc in SENT:
    if not ORDER or ORDER[-1][0] != sc: ORDER.append([sc, a])
ORDER[0][1] = 0.0
SCENES = [(sc, a, (ORDER[i + 1][1] if i + 1 < len(ORDER) else TOTAL)) for i, (sc, a) in enumerate(ORDER)]
CH = TL.chunks()

# ---------- paper + helpers ----------
def make_paper():
    im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im)
    for x in range(0, W, 54): d.line([(x, 0), (x, H)], fill=(228, 235, 241), width=2)
    for y in range(0, H, 54): d.line([(0, y), (W, y)], fill=(228, 235, 241), width=2)
    rnd = random.Random(3)
    for _ in range(9000):
        x, y = rnd.randrange(W), rnd.randrange(H); c = rnd.randint(225, 248); d.point((x, y), fill=(c, c + 3, c + 6))
    return im.convert("RGBA")
PAPER_IM = make_paper()

_ph = {}
def photo(name):
    if name not in _ph:
        im = Image.open(PH + name + ".jpg").convert("RGB")
        if name == "dirty": im = im.crop((0, 0, int(im.width * 0.80), int(im.height * 0.86)))   # drop corner logo
        _ph[name] = im
    return _ph[name]

def card(im, name, cx, cy, w, rot, a, t, credit="", zoom=0.08, grey=0.0):
    if a <= 0: return
    p = photo(name)
    if grey > 0: p = Image.blend(p, ImageOps.grayscale(p).convert("RGB"), grey)
    pw, phh = p.size; h = int(w * phh / pw)
    z = 1 + zoom * min(1, t / 7)
    cw, ch = pw / z, phh / z
    sub = p.crop((int((pw - cw) / 2), int((phh - ch) / 2), int((pw + cw) / 2), int((phh + ch) / 2))).resize((w, h), Image.BILINEAR)
    b = 14; fr = Image.new("RGBA", (w + 2 * b, h + 2 * b + (34 if credit else 0)), WHITE + (255,))
    fr.paste(sub, (b, b))
    if credit: ImageDraw.Draw(fr).text((b, h + b + 7), "Foto: " + credit, font=fn("SemiBold", 22), fill=INK2 + (255,))
    td = ImageDraw.Draw(fr); tw = 150
    td.rectangle([(fr.width - tw) // 2, 0, (fr.width + tw) // 2, 22], fill=(200, 228, 246, 220))
    fr = fr.rotate(rot, resample=Image.BICUBIC, expand=True)
    s = 0.92 + 0.08 * a
    if s != 1: fr = fr.resize((int(fr.width * s), int(fr.height * s)), Image.BILINEAR)
    sh = Image.new("RGBA", fr.size, (0, 0, 0, 0)); sh.putalpha(fr.getchannel("A").point(lambda v: int(v * 0.26 * a)))
    sh = sh.filter(ImageFilter.GaussianBlur(12))
    if a < 1: fr.putalpha(fr.getchannel("A").point(lambda v: int(v * a)))
    x, y = int(cx - fr.width / 2), int(cy - fr.height / 2 + (1 - a) * 40)
    im.alpha_composite(sh, (x + 6, y + 14)); im.alpha_composite(fr, (x, y))

def stamp(im, s, cx, cy, rot, a, col=WARN, size=52):
    if a <= 0: return
    f = fn("Black", size); tw = int(ImageDraw.Draw(im).textlength(s, font=f)) + 60
    st = Image.new("RGBA", (tw, size + 50)); d = ImageDraw.Draw(st)
    d.rounded_rectangle([4, 4, tw - 4, size + 46], 12, outline=col + (255,), width=7)
    d.text((tw / 2, (size + 50) / 2), s, font=f, fill=col + (255,), anchor="mm")
    sc = 1 + 1.2 * (1 - ease(min(1, a)))
    st = st.rotate(rot, resample=Image.BICUBIC, expand=True)
    st = st.resize((int(st.width * sc), int(st.height * sc)), Image.BILINEAR)
    st.putalpha(st.getchannel("A").point(lambda v: int(v * min(1, a * 1.4) * 0.92)))
    im.alpha_composite(st, (int(cx - st.width / 2), int(cy - st.height / 2)))

def text(d, x, y, s, f, col, a=1.0, anchor="la"):
    if a <= 0: return
    d.text((x, y + (1 - a) * 24), s, font=f, fill=col + (int(255 * a),), anchor=anchor)

def marker(d, x, y, s, f, a, col=SKY):
    if a <= 0: return
    w = d.textlength(s, font=f); bb = d.textbbox((x, y), s, font=f)
    d.rectangle([x - 10, bb[1] + (bb[3] - bb[1]) * 0.25, x - 10 + (w + 20) * a, bb[3] + 8], fill=col + (200,))

def box(d, x0, y0, x1, y1, a, col=NAVY, fill=WHITE, r=24, w=5):
    if a <= 0: return
    d.rounded_rectangle([x0, y0 + (1 - a) * 20, x1, y1 + (1 - a) * 20], r, fill=fill + (int(250 * a),), outline=col + (int(255 * a),), width=w)

def molecule(im, cx, cy, sc, a, t):
    if a <= 0: return
    lay = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(lay)
    wob = 4 * math.sin(t * 2.2); rS, rH, L = 120 * sc, 66 * sc, 190 * sc
    hs = [(cx + L * math.sin(math.radians(46 + wob)), cy + L * math.cos(math.radians(46 + wob))),
          (cx - L * math.sin(math.radians(46 - wob)), cy + L * math.cos(math.radians(46 - wob)))]
    for hx, hy in hs: d.line([(cx, cy), (hx, hy)], fill=NAVY + (255,), width=int(16 * sc))
    for hx, hy in hs:
        d.ellipse([hx - rH, hy - rH, hx + rH, hy + rH], fill=WHITE + (255,), outline=NAVY + (255,), width=int(7 * sc))
        d.text((hx, hy), "H", font=fn("Black", int(66 * sc)), fill=NAVY + (255,), anchor="mm")
    d.ellipse([cx - rS, cy - rS, cx + rS, cy + rS], fill=SULF + (255,), outline=NAVY + (255,), width=int(8 * sc))
    d.text((cx, cy), "S", font=fn("Black", int(120 * sc)), fill=NAVY + (255,), anchor="mm")
    lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
    im.alpha_composite(lay)

def deco(im, name, credit, t, rot=-3, w=820, cy=1620):
    """decorative evidence print below the subtitle band: nothing essential here"""
    card(im, name, 540, cy, w, rot, ph(t, 0.5, 0.6), t, credit, zoom=0.05)

def hud(d, T):
    g = min(1, T / VOICE_END)
    d.text((80, 120), "TERGOV · SALARDAGI HID", font=fn("Bold", 30), fill=NAVY + (235,))
    d.text((1000, 120), "Doktor H₂O", font=fn("Bold", 30), fill=SKYD + (255,), anchor="ra")
    d.line([(80, 172), (1000, 172)], fill=(190, 205, 218, 255), width=4)
    d.line([(80, 172), (80 + 920 * g, 172)], fill=SKYD + (255,), width=4)
    d.ellipse([80 + 920 * g - 8, 164, 80 + 920 * g + 8, 180], fill=SKYD + (255,))

# ---------- scenes (t = seconds since scene start; comments = spoken line) ----------
def hook(im, d, t):   # "Sergelida Salar ... yaxshi bilishadi. Chirigan tuxum hidi. Qiziq, bu hid qayerdan keladi?"
    card(im, "aerial", 540, 830, 900, -2.5, ph(t, 0.0, 0.4), t, "Kun.uz", zoom=0.12)
    text(d, 80, 236, "Sergeli, Toshkent", fn("Bold", 40), SKYD, ph(t, 0.05, 0.3))
    f = fn("Black", 92)
    marker(d, 80, 296, "Chirigan tuxum", f, ph(t, 4.1, 0.5))
    text(d, 80, 296, "Chirigan tuxum", f, NAVY, ph(t, 0.0, 0.3))
    text(d, 80, 400, "hidi qayerdan?", f, NAVY, ph(t, 0.15, 0.3))
    a = ph(t, 1.0)
    if a > 0:                                  # pin on the plant
        x, y = 610, 800
        d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=WARN + (int(255 * a),), outline=WHITE + (int(255 * a),), width=4)
        w_ = d.textlength("Salar inshooti", font=fn("ExtraBold", 36)) + 40
        d.rounded_rectangle([x + 30, y - 32, x + 30 + w_, y + 32], 16, fill=NAVY + (int(235 * a),))
        text(d, x + 50, y - 22, "Salar inshooti", fn("ExtraBold", 36), WHITE, a)
    stamp(im, "HID MANBASI?", 800, 1010, 8, ph(t, 6.0, 0.35))

def h2s(im, d, t):    # "Bunga aybdor yagona vodorod sulfid gazi hisoblanadi."
    text(d, 80, 250, "Aybdor:", fn("Black", 80), NAVY, ph(t, 0.1))
    f = fn("Black", 210)
    marker(d, 80, 350, "H₂S", f, ph(t, 1.3, 0.4), SULF)
    text(d, 80, 350, "H₂S", f, NAVY, ph(t, 0.3))
    molecule(im, 800, 470, 0.72 * (0.8 + 0.2 * back(min(1, t / 0.8))), ph(t, 0.2), t)
    text(d, 80, 660, "vodorod sulfid gazi", fn("ExtraBold", 60), SKYD, ph(t, 1.2))
    text(d, 80, 740, "chirigan tuxum hidli gaz", fn("SemiBold", 40), INK2, ph(t, 1.8))
    deco(im, "sludge", "Kun.uz", t, 3)

def bakteriya(im, d, t):   # "Salarda oqova suvni bakteriyalar tozalaganligi uchun ularga doimiy kislorod kerak bo'ladi."
    text(d, 80, 236, "Salarda suvni", fn("Black", 76), NAVY, ph(t, 0.1))
    f = fn("Black", 76); marker(d, 80, 324, "bakteriyalar tozalaydi", f, ph(t, 1.0, 0.5))
    text(d, 80, 324, "bakteriyalar tozalaydi", f, NAVY, ph(t, 0.6))
    card(im, "clar", 540, 740, 920, 1.8, ph(t, 0.0, 0.5), t, "UzA", zoom=0.14)
    a = ph(t, 2.4)
    if a > 0:
        d.rounded_rectangle([300, 960, 780, 1060], 50, fill=SKYD + (int(245 * a),))
        text(d, 540, 1010, "O₂ doimo kerak", fn("Black", 52), WHITE, a, "mm")
    deco(im, "aerial", "Kun.uz", t, -2.5, 700, 1640)

def jarayon(im, d, t):     # "Kislorod yetmagan joyda boshqa bakteriyalar sulfat bilan nafas oladi va vodorod sulfid gazini chiqaradi."
    text(d, 80, 240, "Kislorod yetmasa:", fn("Black", 70), NAVY, ph(t, 0.1))
    steps = [("Kislorod yetmaydi", "O₂ ≈ 0", 0.3), ("Boshqa bakteriyalar", "sulfat bilan «nafas oladi»", 1.6), ("Gaz chiqadi", "SO₄²⁻  →  H₂S", 3.9)]
    for k, (a1, b1, t0) in enumerate(steps):
        a = ph(t, t0)
        if a <= 0: continue
        yy = 370 + k * 210
        col = NAVY if k < 2 else WARN
        box(d, 80, yy, 1000, yy + 160, a, col)
        yo = (1 - a) * 20
        d.ellipse([110, yy + 40 + yo, 190, yy + 120 + yo], fill=(SKYD if k < 2 else WARN) + (int(255 * a),))
        text(d, 150, yy + 80, str(k + 1), fn("Black", 44), WHITE, a, "mm")
        text(d, 220, yy + 30, a1, fn("ExtraBold", 52), NAVY, a)
        text(d, 220, yy + 96, b1, fn("SemiBold", 36), INK2, a)
        if k < 2 and ph(t, steps[k + 1][2] - 0.3) > 0:
            d.polygon([(520, yy + 168), (560, yy + 168), (540, yy + 200)], fill=NAVY + (255,))
    deco(im, "fields", "Kun.uz", t, -3)

def ppb(im, d, t):         # "Burnimiz uni hattoki milliard qismdan yarim qism bo'lsa ham sezadi."
    text(d, 80, 236, "Burnimiz sezadi:", fn("Black", 64), NAVY, ph(t, 0.1))
    v = 0.5 * ph(t, 0.9, 1.0)
    text(d, 80, 330, f"{v:.1f}".replace(".", ","), fn("Black", 230), NAVY, ph(t, 0.6))
    text(d, 540, 420, "ppb", fn("Black", 110), SKYD, ph(t, 0.9))
    text(d, 80, 610, "milliard qismdan", fn("ExtraBold", 58), NAVY, ph(t, 1.2))
    f = fn("ExtraBold", 58); marker(d, 80, 690, "yarim qism", f, ph(t, 2.0, 0.4), SULF)
    text(d, 80, 690, "yarim qism", f, NAVY, ph(t, 1.6))
    a = ph(t, 1.0)                          # 1 000 dots, one lit: "a tiny part"
    if a > 0:
        x0, y0 = 600, 640
        for i in range(10):
            for j in range(14):
                lit = (i, j) == (6, 9)
                c = WARN if lit and ph(t, 2.2) > 0 else (180, 205, 225)
                r = 9 if lit else 6
                cx, cy = x0 + j * 28, y0 + i * 32
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c + (int(255 * a),))
    deco(im, "map", "Kun.uz", t, 2.5)

def korxona(im, d, t):     # "2021 yilda 18 ta korxona oqova suvni mana shu tozalash inshootiga tashlaganligi aniqlandi."
    v = int(18 * ph(t, 0.8, 1.0))
    text(d, 80, 210, f"{v}", fn("Black", 170), WARN, ph(t, 0.5))
    text(d, 330, 250, "ta korxona", fn("ExtraBold", 56), NAVY, ph(t, 0.8))
    text(d, 330, 320, "oqovasini Salarga tashlagan", fn("Bold", 36), INK2, ph(t, 2.4))
    card(im, "sample", 540, 720, 860, 2, ph(t, 0.0, 0.5), t, "Daryo (illyustrativ)")
    stamp(im, "TEKSHIRUV · 2021", 720, 1010, -6, ph(t, 0.15, 0.35))
    deco(im, "fields", "Kun.uz", t, 3, 700, 1640)

def teri(im, d, t):        # "Teri va to'qimachilik zavodlari shular jumlasidandir."
    text(d, 80, 240, "Jumladan:", fn("Black", 80), NAVY, ph(t, 0.0))
    rows = [("Teri", "zavodlari", WARN, 0.1), ("To'qimachilik", "zavodlari", NAVY, 0.6)]
    for k, (n, s, col, t0) in enumerate(rows):
        a = ph(t, t0); yy = 380 + k * 200
        if a <= 0: continue
        d.rounded_rectangle([80, yy, 80 + 920 * a, yy + 170], 24, fill=WHITE + (int(250 * a),), outline=col + (255,), width=5)
        text(d, 120, yy + 40, n, fn("Black", 80), col, a)
        text(d, 120 + d.textlength(n + " ", font=fn("Black", 80)), yy + 66, s, fn("ExtraBold", 50), INK2, a)
    deco(im, "dirty", "Yuz.uz", t, 3)

def nobud(im, d, t):       # "Kimyoviy moddalar suvni tozalaydigan bakteriyalarni batamom nobud qilgan"
    text(d, 80, 236, "Kimyoviy moddalar", fn("Black", 76), NAVY, ph(t, 0.1))
    f = fn("Black", 76); marker(d, 80, 324, "bakteriyalarni o'ldirgan", f, ph(t, 2.9, 0.5), (255, 190, 175))
    text(d, 80, 324, "bakteriyalarni o'ldirgan", f, NAVY, ph(t, 1.8))
    card(im, "dirty", 540, 740, 920, -1.5, ph(t, 0.0, 0.5), t, "Yuz.uz", zoom=0.10, grey=0.85 * ph(t, 2.4, 1.2))
    stamp(im, "BIOLOGIYA TO'XTADI", 640, 1030, -5, ph(t, 3.2, 0.35), size=46)

def chirish(im, d, t):     # "va tozalovchi bakteriyalar kamayganligi uchun oqova suv chirib, hidni kuchaytirgan."
    text(d, 80, 236, "Natija:", fn("Black", 76), NAVY, ph(t, 0.0))
    steps = [("Tozalovchi bakteriya", "kamaydi", NAVY, 0.3), ("Oqova suv", "chiridi", NAVY, 2.4), ("Hid", "kuchaydi", WARN, 3.3)]
    for k, (a1, b1, col, t0) in enumerate(steps):
        a = ph(t, t0); yy = 360 + k * 210
        if a <= 0: continue
        box(d, 80, yy, 1000, yy + 160, a, col)
        text(d, 120, yy + 26, a1, fn("ExtraBold", 50), NAVY, a)
        text(d, 120, yy + 88, b1, fn("Black", 52), col, a)
        text(d, 960, yy + 80, "↓" if k < 2 else "↑", fn("Black", 80), col, a, "rm")
    deco(im, "sludge", "Kun.uz", t, -3)

def xulosa(im, d, t):      # "Ya'ni hid faqatgina inshootdan emas, balki zavodlarning oqovasidan ham kelgan."
    text(d, 80, 236, "Hid manbasi:", fn("Black", 80), NAVY, ph(t, 0.1))
    a = ph(t, 0.9); b = ph(t, 2.3); c = ph(t, 3.4)
    if a > 0:
        d.rounded_rectangle([80, 380, 500, 560], 24, fill=WHITE + (int(250 * a),), outline=NAVY + (255,), width=5)
        text(d, 290, 440, "Inshoot", fn("Black", 58), NAVY, a, "mm")
        text(d, 290, 505, "kislorod yetmasa", fn("SemiBold", 30), INK2, a, "mm")
    if b > 0:
        d.rounded_rectangle([580, 380, 1000, 560], 24, fill=WHITE + (int(250 * b),), outline=WARN + (255,), width=5)
        text(d, 790, 440, "Zavodlar", fn("Black", 58), WARN, b, "mm")
        text(d, 790, 505, "kimyoviy oqova", fn("SemiBold", 30), INK2, b, "mm")
        stamp(im, "HAM!", 930, 345, 10, b, size=40)
    if c > 0:
        for x0 in (290, 790): d.line([(x0, 575), (540, 700)], fill=NAVY + (int(255 * c),), width=6)
        d.polygon([(520, 690), (560, 690), (540, 720)], fill=NAVY + (int(255 * c),))
        d.rounded_rectangle([240, 730, 840, 900], 26, fill=NAVY + (int(245 * c),))
        text(d, 540, 815, "H₂S hidi", fn("Black", 80), SKY, c, "mm")
    deco(im, "fields", "Kun.uz", t, 2.5)

def keyingi(im, d, t):     # "Keyingi videoda bu hidni yo'qotish uchun qilingan chora-tadbirlar haqida batafsil ma'lumot berib o'tiladi."
    text(d, 80, 236, "Keyingi videoda:", fn("Black", 76), NAVY, ph(t, 0.1))
    f = fn("Black", 70)
    marker(d, 80, 330, "hidni yo'qotish", f, ph(t, 2.2, 0.5))
    text(d, 80, 330, "hidni yo'qotish", f, NAVY, ph(t, 1.6))
    text(d, 80, 420, "chora-tadbirlari", f, NAVY, ph(t, 3.0))
    card(im, "clar", 540, 780, 860, -2, ph(t, 0.0, 0.5), t, "UzA", zoom=0.10)
    stamp(im, "DAVOMI BOR", 740, 1020, -6, ph(t, 4.6, 0.35), col=SKYD)

def cta(im, d, t):         # "Bizni kuzatishda davom eting, suv haqida suvyektiv fikrlaymiz." + brand end card
    text(d, 80, 300, "Suvni qadrlang!", fn("Black", 110), SKYD, ph(t, 0.0))
    text(d, 80, 450, "Suv haqida bilmoqchi bo'lganlaringizni", fn("Bold", 40), NAVY, ph(t, 0.4))
    a = ph(t, 0.7)
    w_ = d.textlength("izohlarda yozib qoldiring ↓", font=fn("Bold", 44)) + 60
    d.rounded_rectangle([80, 512, 80 + w_, 592], 40, fill=SKY + (int(255 * a),))
    text(d, 110, 527, "izohlarda yozib qoldiring ↓", fn("Bold", 44), NAVY, a)
    text(d, 80, 680, "Bizni kuzatishda davom eting,", fn("SemiBold", 42), NAVY, ph(t, 1.0))
    text(d, 80, 736, "suv haqida suvyektiv fikrlaymiz!", fn("ExtraBold", 52), SKYD, ph(t, 1.6))
    a = ph(t, 2.2)
    if a > 0:
        d.rounded_rectangle([80, 860, 720, 950], 24, fill=NAVY + (int(245 * a),))
        text(d, 110, 878, "Doktor H₂O  ·  @suvyektiv", fn("Bold", 42), WHITE, a)
    deco(im, "aerial", "Kun.uz", t, 2.5, 760, 1620)

FUN = {k: globals()[k] for k in ["hook", "h2s", "bakteriya", "jarayon", "ppb", "korxona", "teri", "nobud", "chirish", "xulosa", "keyingi", "cta"]}

# ---------- subtitles ----------
KEY = re.compile(r"\d|H₂S|^hid|vodorod|sulfid|kislorod|bakteriya|sulfat|korxona|^teri|to'qimachilik|zavod|milliard|^salar|chirigan|tuxum|suvyektiv|nobud|chirib|yarim", re.I)
def subs(im, T):
    cur = [c for c in CH if c[0] <= T < c[1]]
    if not cur: return
    s = cur[0][2]; f = fn("Bold", 64)
    lay = Image.new("RGBA", (W, 200)); d = ImageDraw.Draw(lay)
    words = s.split(); sp = d.textlength(" ", font=f)
    widths = [d.textlength(w, font=f) for w in words]
    x = (W - (sum(widths) + sp * (len(words) - 1))) / 2
    for w, ww in zip(words, widths):
        col = SKY if KEY.search(w.strip(",.?:!«»")) else WHITE
        d.text((x, 100), w, font=f, fill=col + (255,), anchor="lm", stroke_width=7, stroke_fill=NAVY + (255,))
        x += ww + sp
    shadow = lay.getchannel("A").filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.35))
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0)); sh.putalpha(shadow)
    im.alpha_composite(sh, (0, 1080 + 6)); im.alpha_composite(lay, (0, 1080))

# ---------- render ----------
def frame(T, with_subs=True):
    k = max(i for i, s in enumerate(SCENES) if s[1] <= T)
    sc, a, b = SCENES[k]; t = T - a
    im = PAPER_IM.copy(); d = ImageDraw.Draw(im)
    hud(d, T); FUN[sc](im, d, t)
    if t < 5 / FPS and k > 0:                      # quick paper-flash cut
        im = Image.blend(im, PAPER_IM, 1 - t * FPS / 5)
    if with_subs: subs(im, T)
    return im

def part(args):
    i0, i1, out = args
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for f in range(i0, i1): p.stdin.write(frame(f / FPS).tobytes())
    p.stdin.close(); p.wait(); return out

def render(out, nproc=8):
    n = int(round(TOTAL * FPS)); step = math.ceil(n / nproc)
    jobs = [(i, min(n, i + step), f"/home/claude/salarA/part{j:02d}.mp4") for j, i in enumerate(range(0, n, step))]
    with Pool(nproc) as pool: parts = pool.map(part, jobs)
    open("/home/claude/salarA/parts.txt", "w").write("".join(f"file '{p}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "/home/claude/salarA/parts.txt", "-c", "copy", out], check=True)

def cover(out):
    """cover: real Salar photo + big hook text; text and key image inside the 3:4 grid crop (y 240-1680)"""
    im = Image.new("RGBA", (W, H), SKY + (255,)); d = ImageDraw.Draw(im)
    for y in range(H):                                  # sky -> light gradient
        u = y / H; c = tuple(int(SKY[i] * (1 - u) + (237, 248, 255)[i] * u) for i in range(3)); d.line([(0, y), (W, y)], fill=c + (255,))
    card(im, "aerial", 540, 1250, 960, -2.5, 1, 7, "Kun.uz", zoom=0.12)
    f1, f2 = fn("Black", 112), fn("Black", 128)
    text(d, 70, 300, "Sergelidagi", fn("Black", 84), NAVY)
    d.rounded_rectangle([56, 410, 64 + d.textlength("chirigan tuxum", font=f1) + 24, 545], 22, fill=NAVY + (255,))
    text(d, 76, 418, "chirigan tuxum", f1, WHITE)
    text(d, 70, 560, "hidi", f2, NAVY)
    text(d, 70 + d.textlength("hidi ", font=f2), 560, "qayerdan?", f2, SKYD)
    stamp(im, "TERGOV", 860, 860, 8, 1, size=50)
    d.rounded_rectangle([70, 1700, 640, 1780], 22, fill=NAVY + (240,))
    text(d, 96, 1716, "Doktor H₂O · @suvyektiv", fn("Bold", 38), WHITE)
    im.convert("RGB").save(out, quality=94)

if __name__ == "__main__":
    a = sys.argv[1]
    if a == "scenes": render(sys.argv[2])
    elif a == "still": frame(float(sys.argv[2])).convert("RGB").save(sys.argv[3])
    elif a == "cover": cover(sys.argv[2])
    elif a == "info":
        for s in SCENES: print(s)
        print("total", TOTAL)
