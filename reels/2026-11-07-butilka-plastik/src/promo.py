"""07.11 reel re-styled after the reference reel (app-promo motion graphics): saturated blue gradient with drifting
soft blobs, huge white headlines that blur-in, yellow tilted highlight words, white UI cards, stamps, polaroid
cards, starburst, magnifier, search-bar typing end card. Fast 2–4 s scenes, no bottom captions.
usage: promo.py render out.mp4 | still t out.png"""
import sys, math, random, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
R = "/home/claude/r8/"
W, H, FPS = 1080, 1920, 30
F = "/usr/share/fonts/opentype/inter/InterDisplay-{}.otf"
_fc = {}
def fn(w, s):
    k = (w, s)
    if k not in _fc: _fc[k] = ImageFont.truetype(F.format(w), s)
    return _fc[k]
WHITE, NAVY, YEL, RED, GRN = (255, 255, 255), (11, 31, 51), (255, 212, 59), (232, 72, 72), (46, 190, 120)
B1, B2, B3 = (40, 120, 240), (16, 72, 200), (120, 190, 255)
def cl(u): return max(0.0, min(1.0, u))
def eout(u): u = cl(u); return 1 - (1 - u) ** 3
def ein(u): u = cl(u); return u * u * (3 - 2 * u)
def back(u):
    u = cl(u); c = 1.7; return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2
def ph(t, t0, d=0.45): return eout((t - t0) / d)

# ---------- backgrounds ----------
def _blob(r, col):
    im = Image.new("RGBA", (4 * r, 4 * r), col + (0,)); ImageDraw.Draw(im).ellipse([r, r, 3 * r, 3 * r], fill=col + (255,))
    return im.filter(ImageFilter.GaussianBlur(r * 0.45))
BLOBS = {}
def bg(kind, T):
    if kind == "blue":   base, cols = (24, 96, 222), [(90, 170, 255), (10, 60, 190), (70, 140, 250)]
    elif kind == "navy": base, cols = (12, 30, 90), [(40, 90, 220), (80, 50, 170), (20, 60, 160)]
    else:                base, cols = (236, 243, 252), [(205, 225, 252), (255, 255, 255), (190, 215, 250)]
    im = Image.new("RGBA", (W, H), base + (255,))
    key = (kind,)
    if key not in BLOBS: BLOBS[key] = [_blob(520, c) for c in cols]
    for k, b in enumerate(BLOBS[key]):
        x = 540 + 380 * math.sin(T * 0.35 + k * 2.1) - 1040
        y = 960 + 600 * math.cos(T * 0.28 + k * 1.7) - 1040
        im.alpha_composite(b, (int(x), int(y)))
    return im

def starburst(T):
    im = Image.new("RGBA", (W, H), (255, 190, 20, 255)); d = ImageDraw.Draw(im)
    cx, cy = 540, 820; n = 28; rot = T * 0.25
    for k in range(n):
        if k % 2: continue
        a0 = rot + 2 * math.pi * k / n; a1 = rot + 2 * math.pi * (k + 1) / n
        d.polygon([(cx, cy), (cx + 2600 * math.cos(a0), cy + 2600 * math.sin(a0)), (cx + 2600 * math.cos(a1), cy + 2600 * math.sin(a1))], fill=(255, 226, 90, 255))
    g = Image.new("RGBA", (W, H)); ImageDraw.Draw(g).ellipse([cx - 420, cy - 420, cx + 420, cy + 420], fill=(255, 250, 220, 220))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(120)))
    return im

# ---------- text helpers ----------
def textlayer(s, f, col, shadow=True, stroke=0):
    d0 = ImageDraw.Draw(Image.new("RGBA", (1, 1))); bb = d0.textbbox((0, 0), s, font=f, stroke_width=stroke)
    w, h = bb[2] - bb[0] + 60, bb[3] - bb[1] + 60
    im = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(im)
    if shadow:
        sh = Image.new("RGBA", (w, h)); ImageDraw.Draw(sh).text((30 - bb[0], 38 - bb[1]), s, font=f, fill=(0, 20, 60, 110), stroke_width=stroke, stroke_fill=(0, 20, 60, 110))
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
    d.text((30 - bb[0], 30 - bb[1]), s, font=f, fill=col + (255,), stroke_width=stroke, stroke_fill=NAVY + (255,) if stroke else None)
    return im

def put(im, lay, cx, cy, a=1.0, sc=1.0, blur=0.0, rot=0.0):
    if a <= 0: return
    if rot: lay = lay.rotate(rot, resample=Image.BICUBIC, expand=True)
    if sc != 1: lay = lay.resize((max(1, int(lay.width * sc)), max(1, int(lay.height * sc))), Image.BILINEAR)
    if blur > 0.3: lay = lay.filter(ImageFilter.GaussianBlur(blur))
    if a < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
    im.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))

def headline(im, s, cx, cy, t, t0, size=170, col=WHITE, w="Black"):
    """blur-in + slight zoom-out entrance (reference's signature move)"""
    u = cl((t - t0) / 0.5)
    if u <= 0: return
    put(im, textlayer(s, fn(w, size), col), cx, cy, a=ein(u), sc=1.12 - 0.12 * eout(u), blur=18 * (1 - eout(u)))

def tilted(im, s, cx, cy, t, t0, size=96, rot=4, col=YEL):
    """yellow tilted italic highlight that pops in"""
    u = cl((t - t0) / 0.35)
    if u <= 0: return
    lay = textlayer(s, fn("BlackItalic", size), col, stroke=0)
    put(im, lay, cx, cy, a=min(1, u * 2), sc=back(u), rot=rot)

def pill(im, s, cx, cy, a, fill=(255, 255, 255), fg=NAVY, size=40, alpha=60, icon=None):
    if a <= 0: return
    d0 = ImageDraw.Draw(im); f = fn("Bold", size); tw = d0.textlength(s, font=f) + (60 if icon else 0)
    w, h = tw + 64, size + 40
    l = Image.new("RGBA", (int(w), int(h))); d = ImageDraw.Draw(l)
    d.rounded_rectangle([0, 0, w - 1, h - 1], h // 2, fill=fill + (int(255 * alpha / 100),))
    x = 32
    if icon == "check":
        d.ellipse([28, h / 2 - 20, 68, h / 2 + 20], fill=(37, 99, 235, 255)); d.line([(38, h / 2), (46, h / 2 + 9), (60, h / 2 - 9)], fill=WHITE + (255,), width=5); x = 84
    d.text((x, h / 2), s, font=f, fill=fg + (255,), anchor="lm")
    put(im, l, cx, cy + (1 - a) * 20, a=a)

def card(w, h, r=34, fill=WHITE):
    l = Image.new("RGBA", (w + 80, h + 80)); sh = Image.new("RGBA", l.size)
    ImageDraw.Draw(sh).rounded_rectangle([40, 56, 40 + w, 56 + h], r, fill=(0, 30, 90, 90))
    l.alpha_composite(sh.filter(ImageFilter.GaussianBlur(20)))
    ImageDraw.Draw(l).rounded_rectangle([40, 40, 40 + w, 40 + h], r, fill=fill + (255,))
    return l, ImageDraw.Draw(l)

def polaroid(name, w, label, rot):
    p = Image.open(R + f"pp/{name}.jpg").convert("RGB"); h = int(w * 1.0)
    s = max(w / p.width, h / p.height); p = p.resize((int(p.width * s), int(p.height * s)))
    p = p.crop(((p.width - w) // 2, (p.height - h) // 2, (p.width - w) // 2 + w, (p.height - h) // 2 + h))
    l, d = card(w + 36, h + 110, 18)
    l.paste(p, (58, 58)); d.text((40 + (w + 36) / 2, 58 + h + 46), label, font=fn("Bold", 34), fill=NAVY + (255,), anchor="mm")
    return l.rotate(rot, resample=Image.BICUBIC, expand=True)

def stamp(s, col=RED, size=58):
    f = fn("Black", size); tw = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength(s, font=f)
    l = Image.new("RGBA", (int(tw + 70), size + 60)); d = ImageDraw.Draw(l)
    d.rounded_rectangle([5, 5, l.width - 6, l.height - 6], 16, outline=col + (255,), width=8)
    d.text((l.width / 2, l.height / 2), s, font=f, fill=col + (255,), anchor="mm")
    return l

def drop_icon(sz):
    l = Image.new("RGBA", (sz, sz)); d = ImageDraw.Draw(l)
    d.rounded_rectangle([0, 0, sz - 1, sz - 1], int(sz * 0.26), fill=WHITE + (255,))
    cx, cy, r = sz / 2, sz * 0.58, sz * 0.24
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(37, 99, 235, 255))
    d.polygon([(cx - r * 0.93, cy - r * 0.35), (cx, sz * 0.14), (cx + r * 0.93, cy - r * 0.35)], fill=(37, 99, 235, 255))
    d.ellipse([cx - r * 0.45, cy - r * 0.2, cx - r * 0.05, cy + r * 0.2], fill=(170, 210, 255, 255))
    return l

# ---------- scenes: (name, dur, fn) ----------
def sc_hook(t, T):
    im = bg("blue", T)
    headline(im, "Butilka", 540, 300, t, 0.0, 190)
    headline(im, "suvi", 540, 480, t, 0.25, 190)
    u = ph(t, 1.1)
    if u > 0:
        put(im, textlayer("toza deb o'ylaysizmi?", fn("Bold", 64), (210, 230, 255), shadow=False), 540, 640, a=u)
    tilted(im, "Unda bunga qarang", 540, 820, t, 1.9, 84, 3)
    return im

def sc_lab(t, T):
    im = bg("blue", T)
    headline(im, "1 litrda", 540, 280, t, 0.0, 160)
    l, d = card(860, 520)
    d.text((90, 90), "Laboratoriya natijasi", font=fn("Bold", 40), fill=NAVY + (255,))
    d.text((800, 96), "PNAS · 2024", font=fn("SemiBold", 30), fill=(150, 160, 180, 255), anchor="ra")
    rows = [("Namuna", "butilka suvi, 1 L", NAVY), ("Brendlar", "3 ta mashhur", NAVY), ("Usul", "lazer mikroskop", NAVY)]
    for k, (a_, b_, c_) in enumerate(rows):
        y = 180 + k * 70
        d.text((90, y), a_, font=fn("Medium", 36), fill=(110, 120, 140, 255)); d.text((810, y), b_, font=fn("Bold", 36), fill=c_ + (255,), anchor="ra")
    d.line([(90, 400), (810, 400)], fill=(225, 230, 240, 255), width=3)
    v = int(240000 * eout((t - 1.2) / 1.6))
    d.text((90, 440), "Plastik zarralari", font=fn("Bold", 40), fill=NAVY + (255,))
    d.text((810, 430), f"{v:,}".replace(",", " "), font=fn("Black", 60), fill=RED + (255,), anchor="ra")
    if t > 2.0: d.rectangle([60, 410, 840, 520], fill=None)
    put(im, l, 540, 760, a=ph(t, 0.3), sc=0.94 + 0.06 * ph(t, 0.3))
    u = cl((t - 2.9) / 0.3)
    if u > 0: put(im, stamp("PLASTIK!"), 760, 1010, a=min(1, u * 1.5), sc=1.8 - 0.8 * eout(u), rot=-12)
    return im

def sc_hidden(t, T):
    im = bg("navy", T)
    headline(im, "Ular ko'zga", 540, 520, t, 0.0, 120)
    tilted(im, "ko'rinmaydi!", 540, 690, t, 0.9, 140, 4)
    return im

def sc_scale(t, T):
    im = bg("blue", T)
    pill(im, "Hajmini solishtiring", 540, 300, ph(t, 0.0), alpha=25, fg=WHITE)
    put(im, polaroid("hair", 380, "Soch tolasi · 70 µm", -7), 330, 820, a=ph(t, 0.3), sc=0.9 + 0.1 * back(cl((t - 0.3) / 0.5)))
    put(im, polaroid("nano", 380, "Nanoplastik · <1 µm", 6), 750, 900, a=ph(t, 1.0), sc=0.9 + 0.1 * back(cl((t - 1.0) / 0.5)))
    tilted(im, "70 baravar ingichka", 540, 1340, t, 2.0, 84, -3)
    return im

def sc_90(t, T):
    im = starburst(T)
    headline(im, "90%", 540, 760, t, 0.0, 330, NAVY)
    u = ph(t, 0.8)
    if u > 0: pill(im, "zarralar — nanoplastik", 540, 1020, u, fill=NAVY, fg=WHITE, size=54, alpha=100)
    return im

def sc_paper(t, T):
    im = bg("light", T)
    pill(im, "Haqiqiy tadqiqot · PNAS 2024", 540, 260, ph(t, 0.0), fill=WHITE, fg=(37, 99, 235), size=38, alpha=100, icon="check")
    l, d = card(900, 330, fill=(37, 99, 235))
    d.text((90, 90), "Kolumbiya universiteti", font=fn("Bold", 38), fill=(200, 225, 255, 255))
    d.text((90, 150), "Eski hisoblardan", font=fn("Bold", 46), fill=WHITE + (255,))
    d.text((90, 210), "10–100×", font=fn("Black", 110), fill=YEL + (255,))
    d.text((560, 245), "ko'p", font=fn("Black", 64), fill=WHITE + (255,))
    put(im, l, 540, 520, a=ph(t, 0.2), sc=0.95 + 0.05 * ph(t, 0.2))
    # mini 'paper' sheet with magnifier
    p, pd = card(880, 520, 20)
    pd.text((90, 80), "Rapid single-particle chemical imaging", font=fn("Bold", 32), fill=NAVY + (255,))
    pd.text((90, 122), "of nanoplastics by SRS microscopy", font=fn("Bold", 32), fill=NAVY + (255,))
    rnd = random.Random(2)
    for i in range(7):
        y = 190 + i * 44; w = rnd.randint(520, 760); pd.rounded_rectangle([90, y, 90 + w, y + 16], 8, fill=(222, 228, 238, 255))
    pd.rounded_rectangle([90, 410, 560, 470], 10, fill=(255, 240, 180, 255))
    pd.text((110, 418), "≈ 240 000 particles / L", font=fn("Bold", 34), fill=NAVY + (255,))
    put(im, p, 540, 1130, a=ph(t, 0.9), sc=0.96 + 0.04 * ph(t, 0.9))
    u = ein((t - 1.8) / 1.0)
    if t > 1.6:
        mx, my = 360 + 120 * u, 1270 - 20 * u; r = 110
        m = Image.new("RGBA", (W, H)); md = ImageDraw.Draw(m)
        md.line([(mx + r * 0.7, my + r * 0.7), (mx + r * 1.6, my + r * 1.6)], fill=NAVY + (255,), width=26)
        md.ellipse([mx - r, my - r, mx + r, my + r], outline=YEL + (255,), width=16, fill=(255, 255, 255, 50))
        im.alpha_composite(m)
    return im

def sc_risk(t, T):
    im = Image.new("RGBA", (W, H), (70, 70, 74, 255))
    rnd = random.Random(4); d = ImageDraw.Draw(im)
    for i in range(3):   # scattered grey documents
        x, y = 160 + i * 300, 600 + (i % 2) * 300
        d.rectangle([x, y, x + 420, y + 560], fill=(110, 110, 114, 255))
        for j in range(12): d.line([(x + 30, y + 40 + j * 40), (x + 30 + rnd.randint(200, 360), y + 40 + j * 40)], fill=(85, 85, 90, 255), width=6)
    im = im.filter(ImageFilter.GaussianBlur(3)).convert("RGBA")
    headline(im, "Xavflimi?", 540, 420, t, 0.0, 170)
    u = cl((t - 1.0) / 0.4)
    if u > 0:
        ban = Image.new("RGBA", (1300, 300)); bd = ImageDraw.Draw(ban); bd.rectangle([0, 0, 1300, 300], fill=YEL + (255,))
        bd.text((650, 95), "Sog'liqqa ta'siri", font=fn("Bold", 56), fill=NAVY + (255,), anchor="mm")
        bd.text((650, 190), "hali isbotlanmagan", font=fn("Black", 88), fill=NAVY + (255,), anchor="mm")
        put(im, ban, 540 + (1 - eout(u)) * 900, 960, a=1, rot=4)
    return im

def sc_takeaway(t, T):
    im = bg("light", T)
    headline(im, "Xulosa", 540, 380, t, 0.0, 130, NAVY)
    l, d = card(860, 300)
    d.text((470, 120), "\"Butilka\"", font=fn("Black", 72), fill=NAVY + (255,), anchor="mm")
    d.text((470, 230), "≠ \"plastiksiz\"", font=fn("Black", 72), fill=(37, 99, 235, 255), anchor="mm")
    put(im, l, 540, 720, a=ph(t, 0.5), sc=0.94 + 0.06 * back(cl((t - 0.5) / 0.5)))
    pill(im, "Manba: Qian et al., PNAS 2024", 540, 1000, ph(t, 1.2), fill=WHITE, fg=(90, 100, 120), size=32, alpha=100)
    return im

def sc_end(t, T):
    im = bg("blue", T)
    put(im, drop_icon(220), 540, 330, a=ph(t, 0.0), sc=back(cl(t / 0.5)))
    headline(im, "Doktor H₂O", 540, 560, t, 0.2, 130, YEL)
    headline(im, "Suvni qadrlang!", 540, 700, t, 0.5, 96)
    # search bar typing @suvyektiv
    sb, sd = card(860, 130, 65)
    s = "@suvyektiv"; n = int(cl((t - 1.2) / 1.2) * len(s)); typed = s[:n]
    sd.text((100, 105), typed + ("|" if int(t * 3) % 2 == 0 else ""), font=fn("Bold", 56), fill=NAVY + (255,), anchor="lm")
    sd.ellipse([800, 65, 880, 145], fill=(37, 99, 235, 255)); sd.ellipse([822, 86, 852, 116], outline=WHITE + (255,), width=6); sd.line([(850, 114), (864, 128)], fill=WHITE + (255,), width=6)
    put(im, sb, 540, 920, a=ph(t, 0.9))
    if t > 2.6:
        b = 6 * math.sin(t * 8); d = ImageDraw.Draw(im); d.polygon([(540, 1030 + b), (510, 1070 + b), (570, 1070 + b)], fill=YEL + (255,))
    pill(im, "Savollaringizni izohlarda yozing", 540, 1130, ph(t, 2.6), fill=WHITE, fg=NAVY, size=38, alpha=100, icon="check")
    pill(im, "Suv haqida suvyektiv fikrlaymiz!", 540, 1230, ph(t, 3.0), fill=WHITE, fg=NAVY, size=38, alpha=100, icon="check")
    return im

SC = [("hook", 3.6, sc_hook), ("lab", 4.4, sc_lab), ("hidden", 2.6, sc_hidden), ("scale", 4.2, sc_scale), ("90", 2.8, sc_90),
      ("paper", 4.4, sc_paper), ("risk", 3.4, sc_risk), ("take", 3.2, sc_takeaway), ("end", 5.0, sc_end)]
STARTS = [sum(s[1] for s in SC[:i]) for i in range(len(SC))]
TOTAL = sum(s[1] for s in SC)
XF = 0.22

def frame(T):
    i = max(k for k in range(len(SC)) if STARTS[k] <= T); t = T - STARTS[i]
    im = SC[i][2](t, T)
    if i > 0 and t < XF:                                   # quick blur-dissolve from previous scene
        prev = SC[i - 1][2](SC[i - 1][1] + t, T); u = t / XF
        im = Image.blend(prev.filter(ImageFilter.GaussianBlur(12 * u)), im, ein(u))
    return im

def render(out):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", R + "ov/music_promo.wav", "-map", "0:v", "-map", "1:a", "-shortest",
                          "-c:v", "libx264", "-crf", "19", "-preset", "fast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                          "-af", f"afade=t=out:st={TOTAL - 1.2:.2f}:d=1.2,loudnorm=I=-15:TP=-1.5", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for f in range(int(TOTAL * FPS)): p.stdin.write(frame(f / FPS).convert("RGBA").tobytes())
    p.stdin.close(); p.wait()

if __name__ == "__main__":
    if sys.argv[1] == "still": frame(float(sys.argv[2])).convert("RGB").save(sys.argv[3])
    elif sys.argv[1] == "render": render(sys.argv[2])
