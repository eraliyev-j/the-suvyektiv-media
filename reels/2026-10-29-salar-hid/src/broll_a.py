"""Reel A 'Hid qayerdan?' (v3, 28.10) — B-roll clips, one per beat, 'case file' style (helpers from case.py).
No captions, no audio: Javohir's voice/A-roll is cut in later, subtitles go on top at y~1180.
All important content sits in y 230-1080 (above subtitle band and IG/Shorts UI).
Photos: see photos.txt (not stored in the public repo). PH env var = folder with them.
usage: python3 broll_a.py OUTDIR [still IDX T out.png]"""
import sys, os, math, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import case as C
from case import fn, ease, ph, back, card, stamp, text, marker, molecule, WHITE, SKY, SKYD, NAVY, WARN, INK2, SULF
from PIL import Image, ImageDraw

C.R = os.environ.get("PH", "/tmp/claude-0/sal") + "/"
W, H, FPS = 1080, 1920, 30
GREY = (150, 160, 170)
SHOW_SRC = False

def hud(d, k, t):
    g = min(1, (k + min(t / 4, 1)) / len(B))
    d.text((80, 120), "TERGOV · SALARDAGI HID", font=fn("Bold", 30), fill=NAVY + (235,))
    d.text((1000, 120), f"{k + 1:02d}/{len(B):02d}", font=fn("Bold", 30), fill=SKYD + (255,), anchor="ra")
    d.line([(80, 172), (1000, 172)], fill=(190, 205, 218, 255), width=4)
    d.line([(80, 172), (80 + 920 * g, 172)], fill=SKYD + (255,), width=4)
    d.ellipse([80 + 920 * g - 8, 164, 80 + 920 * g + 8, 180], fill=SKYD + (255,))

def deco(im, name, credit, t, rot=-3, w=820, cy=1500):
    """decorative evidence print below the subtitle band (y>1290): nothing essential here, IG UI may cover it"""
    card(im, name, 540, cy, w, rot, ph(t, 0.9, 0.6), t, credit, zoom=0.05)

def src(d, s, t, y=1010):
    if not SHOW_SRC and s.startswith("Manba"): return   # sources live in the caption (Javohir, 29.10)
    text(d, 80, y, s, fn("Medium", 24), INK2, ph(t, 1.2))

# ---------- beats ----------
def b01_hook(im, d, t):           # "Sergelidagi chirigan tuxum hidi qayerdan keladi?"
    text(d, 80, 236, "Sergeli, Toshkent", fn("Bold", 40), SKYD, ph(t, 0.1))
    f = fn("Black", 92)
    marker(d, 80, 300, "Chirigan tuxum", f, ph(t, 0.6, 0.5))
    text(d, 80, 300, "Chirigan tuxum", f, NAVY, ph(t, 0.2))
    text(d, 80, 405, "hidi qayerdan?", f, NAVY, ph(t, 0.4))
    card(im, "aerial", 540, 900, 920, -2.5, ph(t, 0.0, 0.6), t, "Kun.uz", zoom=0.08)
    stamp(im, "HID MANBASI?", 790, 660, 8, ph(t, 1.4, 0.35))

def b02_h2s(im, d, t):            # "Aybdor vodorod sulfid, H2S."
    text(d, 80, 250, "Aybdor:", fn("Black", 80), NAVY, ph(t, 0.1))
    f = fn("Black", 210)
    marker(d, 80, 350, "H₂S", f, ph(t, 0.7, 0.4), SULF)
    text(d, 80, 350, "H₂S", f, NAVY, ph(t, 0.3))
    molecule(im, 800, 470, 0.72 * (0.8 + 0.2 * back(min(1, t / 0.8))), ph(t, 0.2), t)
    text(d, 80, 650, "vodorod sulfid", fn("ExtraBold", 60), SKYD, ph(t, 0.9))
    text(d, 80, 730, "chirigan tuxum hidli gaz", fn("SemiBold", 40), INK2, ph(t, 1.2))
    src(d, "Manba: ATSDR / Hawaii DOH, H₂S ma'lumotnomasi", t)
    deco(im, "sludge", "Kun.uz", t, 3)

def b03_kislorod(im, d, t):       # "Kislorod yetmagan joyda bakteriyalar shu gazni chiqaradi."
    text(d, 80, 240, "Qanday paydo bo'ladi?", fn("Black", 70), NAVY, ph(t, 0.1))
    steps = [("Kislorod yetmaydi", "O₂ ≈ 0", 0.5), ("Bakteriyalar", "sulfat bilan «nafas oladi»", 1.3), ("Gaz chiqadi", "SO₄²⁻ → H₂S", 2.1)]
    for k, (a1, b1, t0) in enumerate(steps):
        a = ph(t, t0)
        if a <= 0: continue
        yy = 370 + k * 200 + (1 - a) * 20
        col = NAVY if k < 2 else WARN
        d.rounded_rectangle([80, yy, 1000, yy + 150], 24, fill=WHITE + (int(250 * a),), outline=col + (int(255 * a),), width=4)
        d.ellipse([110, yy + 35, 190, yy + 115], fill=(SKYD if k < 2 else WARN) + (int(255 * a),))
        text(d, 150, yy + 75, str(k + 1), fn("Black", 44), WHITE, a, "mm")
        text(d, 220, yy + 28, a1, fn("ExtraBold", 52), NAVY, a)
        text(d, 220, yy + 92, b1, fn("SemiBold", 34), INK2, a)
        if k < 2 and ph(t, steps[k + 1][1 + 1] - 0.3) > 0:
            d.polygon([(520, yy + 158), (560, yy + 158), (540, yy + 190)], fill=NAVY + (255,))
    src(d, "Manba: ATSDR (H₂S); oqova suv biologiyasi", t)
    deco(im, "fields", "Kun.uz", t, -3)

def b04_ppb(im, d, t):            # "Burnimiz uni milliard qismdan yarim qism bo'lsa ham sezadi."
    v = 0.5 * ph(t, 0.2, 1.0)
    text(d, 80, 220, f"{v:.1f}".replace(".", ","), fn("Black", 230), NAVY, ph(t, 0.05))
    text(d, 540, 300, "ppb", fn("Black", 110), SKYD, ph(t, 0.3))
    text(d, 80, 500, "milliard qismdan yarim qism", fn("ExtraBold", 52), NAVY, ph(t, 0.7))
    a = ph(t, 1.2)
    if a > 0:
        x0, y0, x1, y1 = 80, 600, 1000, 900
        d.rounded_rectangle([x0, y0, x1, y1], 26, fill=(196, 230, 250, int(255 * a)), outline=SKYD + (int(255 * a),), width=6)
        for k in range(1, 8): d.line([(x0 + k * 115, y0 + 10), (x0 + k * 115, y1 - 10)], fill=(255, 255, 255, int(160 * a)), width=4)
        text(d, 110, 620, "Olimpiya basseyni ≈ 2,5 mln litr", fn("Bold", 36), NAVY, a)
        b = ph(t, 2.0)
        if b > 0:
            cx, cy = 760, 800; r = 9
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WARN + (int(255 * b),))
            for k in range(3):
                rr = r + 14 + k * 22 + 10 * math.sin(t * 4 - k)
                d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=WARN + (int(140 * b / (k + 1)),), width=3)
            text(d, 80, 925, "ichida chorak choy qoshiq: shuncha nisbat", fn("Bold", 36), WARN, b)
    src(d, "Sezish chegarasi ≈ 0,5 ppb dan (odamga qarab 300 ppb gacha farq qiladi)", t, 1000)
    deco(im, "map", "Kun.uz", t, 2.5)

def b05_bakteriya(im, d, t):      # "Salarda oqova suvni foydali bakteriyalar tozalaydi."
    text(d, 80, 236, "Salarda suvni", fn("Black", 76), NAVY, ph(t, 0.1))
    f = fn("Black", 76); marker(d, 80, 324, "bakteriyalar tozalaydi", f, ph(t, 0.7, 0.5))
    text(d, 80, 324, "bakteriyalar tozalaydi", f, NAVY, ph(t, 0.3))
    card(im, "clar", 540, 760, 940, 1.8, ph(t, 0.0, 0.6), t, "UzA")
    a = ph(t, 1.0)                                             # friendly bacteria dots over the photo
    for k in range(9):
        x = 200 + (k * 97) % 680; y = 580 + (k * 61) % 320 + 8 * math.sin(t * 2 + k)
        d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=SKY + (int(230 * a),), outline=WHITE + (int(255 * a),), width=3)
    stamp(im, "BIOLOGIK TOZALASH", 700, 1050, -5, ph(t, 1.6, 0.35), col=SKYD, size=44)
    deco(im, "aerial", "Kun.uz", t, -2.5, 700, 1520)

def b06_korxona(im, d, t):        # "Lekin 2021 yilda 18 ta korxona oqovasini shu yerga tashlagani aniqlandi."
    v = int(18 * ph(t, 0.3, 1.0))
    text(d, 80, 210, f"{v}", fn("Black", 170), WARN, ph(t, 0.1))
    text(d, 330, 250, "ta korxona", fn("ExtraBold", 56), NAVY, ph(t, 0.5))
    text(d, 330, 320, "oqovasini Salarga tashlagan", fn("Bold", 36), INK2, ph(t, 0.7))
    card(im, "sample", 540, 720, 860, 2, ph(t, 0.2, 0.6), t, "Daryo (illyustrativ)")
    stamp(im, "TEKSHIRUV · 2021", 730, 1000, -6, ph(t, 1.6, 0.35))
    src(d, "Manba: Gazeta.uz (14.06.2021), Kun.uz (11.05.2021)", t, 1050)
    deco(im, "fields", "Kun.uz", t, 3, 700, 1520)

def b07_teri(im, d, t):           # "Jumladan, teri zavodlari."
    text(d, 80, 240, "Jumladan:", fn("Black", 80), NAVY, ph(t, 0.1))
    rows = [("5 ta", "teri zavodi", WARN, 0.4), ("6 ta", "to'qimachilik", NAVY, 0.9)]
    for k, (n, s, col, t0) in enumerate(rows):
        a = ph(t, t0); yy = 380 + k * 200
        if a <= 0: continue
        d.rounded_rectangle([80, yy, 80 + 920 * a, yy + 170], 24, fill=WHITE + (int(250 * a),), outline=col + (255,), width=5)
        text(d, 120, yy + 30, n, fn("Black", 100), col, a)
        text(d, 400, yy + 58, s, fn("ExtraBold", 56), NAVY, a)
    text(d, 80, 800, "18 ta xavfli korxona ro'yxatidan", fn("SemiBold", 38), INK2, ph(t, 1.4))
    src(d, "Manba: Gazeta.uz (14.06.2021)", t, 880)
    deco(im, "dirty", "Yuz.uz", t, 3)

def b08_nobud(im, d, t):          # "Kimyoviy moddalar foydali bakteriyalarni nobud qilgan."
    text(d, 80, 236, "Kimyoviy moddalar", fn("Black", 76), NAVY, ph(t, 0.1))
    f = fn("Black", 76); marker(d, 80, 324, "bakteriyalarni o'ldirgan", f, ph(t, 0.8, 0.5), (255, 190, 175))
    text(d, 80, 324, "bakteriyalarni o'ldirgan", f, NAVY, ph(t, 0.3))
    card(im, "dirty", 540, 740, 920, -1.5, ph(t, 0.0, 0.6), t, "Yuz.uz")
    a = ph(t, 0.6); u = ph(t, 1.6, 1.2)                         # sky dots turn grey and get crossed out
    for k in range(9):
        x = 200 + (k * 97) % 680; y = 580 + (k * 61) % 320
        col = tuple(int(SKY[i] + (GREY[i] - SKY[i]) * u) for i in range(3))
        d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=col + (int(230 * a),), outline=WHITE + (int(255 * a),), width=3)
        if u > 0.5:
            c = WARN + (int(255 * (u - 0.5) * 2),)
            d.line([(x - 15, y - 15), (x + 15, y + 15)], fill=c, width=5); d.line([(x - 15, y + 15), (x + 15, y - 15)], fill=c, width=5)
    src(d, "Manba: Kun.uz (24.06.2021, 16.05.2026)", t, 1050)
    deco(im, "sample", "Daryo (illyustrativ)", t, 3, 700, 1520)

def b09_xulosa(im, d, t):         # "Ya'ni hid faqat inshootdan emas, zavodlarning oqovasidan ham keladi."
    text(d, 80, 236, "Hid manbasi:", fn("Black", 80), NAVY, ph(t, 0.1))
    a = ph(t, 0.4); b = ph(t, 1.2); c = ph(t, 2.0)
    if a > 0:
        d.rounded_rectangle([80, 380, 500, 560], 24, fill=WHITE + (int(250 * a),), outline=NAVY + (255,), width=5)
        text(d, 290, 440, "Inshoot", fn("Black", 58), NAVY, a, "mm")
        text(d, 290, 505, "kislorod yetmasa", fn("SemiBold", 30), INK2, a, "mm")
    if b > 0:
        d.rounded_rectangle([580, 380, 1000, 560], 24, fill=WHITE + (int(250 * b),), outline=WARN + (255,), width=5)
        text(d, 790, 440, "Zavodlar", fn("Black", 58), WARN, b, "mm")
        text(d, 790, 505, "kimyoviy oqova", fn("SemiBold", 30), INK2, b, "mm")
        stamp(im, "HAM!", 930, 340, 10, b, size=40)
    if c > 0:
        for x0 in (290, 790):
            d.line([(x0, 575), (540, 700)], fill=NAVY + (int(255 * c),), width=6)
        d.polygon([(520, 690), (560, 690), (540, 720)], fill=NAVY + (int(255 * c),))
        d.rounded_rectangle([240, 730, 840, 900], 26, fill=NAVY + (int(245 * c),))
        text(d, 540, 815, "H₂S hidi", fn("Black", 80), SKY, c, "mm")
    text(d, 80, 960, "faqat inshootning aybi emas", fn("ExtraBold", 48), WARN, ph(t, 2.6))
    deco(im, "sludge", "Kun.uz", t, -3)

def b10_end(im, d, t):            # brand end card (spoken CTA: "Sizning hududingizda ham shunday hid bormi?")
    text(d, 80, 300, "Sizda ham shunday", fn("Black", 76), NAVY, ph(t, 0.0))
    text(d, 80, 390, "hid bormi?", fn("Black", 76), NAVY, ph(t, 0.2))
    a = ph(t, 0.6)
    w = d.textlength("izohda yozing ↓", font=fn("Bold", 46)) + 60
    d.rounded_rectangle([80, 500, 80 + w, 582], 41, fill=SKY + (int(255 * a),))
    text(d, 110, 515, "izohda yozing ↓", fn("Bold", 46), NAVY, a)
    text(d, 80, 680, "Suvni qadrlang!", fn("Black", 96), SKYD, ph(t, 1.2))
    text(d, 80, 810, "Bizni kuzatishda davom eting,", fn("SemiBold", 40), NAVY, ph(t, 1.6))
    text(d, 80, 862, "suv haqida suvyektiv fikrlaymiz!", fn("ExtraBold", 50), SKYD, ph(t, 1.9))
    text(d, 80, 960, "Doktor H₂O  ·  @suvyektiv", fn("Bold", 40), NAVY, ph(t, 2.3))
    deco(im, "clar", "UzA", t, 2.5, 760, 1520)

B = [(b01_hook, 4.0), (b02_h2s, 3.5), (b03_kislorod, 4.5), (b04_ppb, 5.0), (b05_bakteriya, 4.0),
     (b06_korxona, 5.5), (b07_teri, 3.5), (b08_nobud, 4.5), (b09_xulosa, 5.0), (b10_end, 5.0)]

def frame(k, t):
    im = C.PAPER_IM.copy().convert("RGBA"); d = ImageDraw.Draw(im)
    hud(d, k, t); B[k][0](im, d, t)
    return im

def render(k, out):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for f in range(int(round(B[k][1] * FPS))):
        p.stdin.write(frame(k, f / FPS).tobytes())
    p.stdin.close(); p.wait()

def lower_third(out, dur=4.0):
    """transparent overlay for beat 1 (Javohir on camera): name + status, above the subtitle band"""
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", out], stdin=subprocess.PIPE)
    for f in range(int(dur * FPS)):
        t = f / FPS; a = min(ph(t, 0.3, 0.4), 1 - ph(t, dur - 0.5, 0.4))
        im = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(im)
        if a > 0:
            d.rounded_rectangle([80, 920, 80 + 800 * a, 1040], 20, fill=NAVY + (int(235 * a),))
            text(d, 110, 934, "Javohir · suv tadqiqotchisi", fn("Bold", 42), WHITE, a)
            text(d, 110, 990, "Dong-A universiteti, Busan", fn("Medium", 28), SKY, a)
        p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    C.PAPER_IM = C.make_paper()
    if len(sys.argv) > 2 and sys.argv[2] == "still":
        frame(int(sys.argv[3]), float(sys.argv[4])).convert("RGB").save(sys.argv[5]); sys.exit()
    only = [int(x) for x in os.environ.get("ONLY", "").split(",") if x]
    for k, (fn_, dur) in enumerate(B):
        if only and k not in only: continue
        render(k, f"{out}/{fn_.__name__}.mp4"); print(fn_.__name__, dur)
    if not only: lower_third(f"{out}/b01_lower_third.mov")
