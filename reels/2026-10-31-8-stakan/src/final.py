"""8 stakan FINAL: intro = Javohir's short clip as-is (with its own audio), then his voice from the 2nd clip
(pauses removed) over the screen-record scenes, re-timed to his speech; subtitles = his own text, anchored to
his sentence timings. usage: final.py audio | segs | caps | build out.mp4"""
import sys, re, json, subprocess
sys.path.insert(0, "/home/claude/r2")
src = open("/home/claude/r5/screen.py").read().split('if __name__')[0]
exec(src)                                         # view(), s_science, s_results, ..., fn, colours, ph, big
F_ = "/home/claude/r5/fin/"
A_DUR = 6.122

# ---- 1. cut pauses in clip B (silence >0.3 s @ -38 dB, keep 0.1 s each side)
def keep_segments():
    out = subprocess.run(["ffmpeg", "-i", F_ + "b.mp4", "-af", "silencedetect=noise=-38dB:d=0.3", "-f", "null", "-"], capture_output=True, text=True).stderr
    ev = re.findall(r"silence_(start|end): ([0-9.]+)", out); sil = []; s0 = None
    for k, v in ev:
        v = float(v)
        if k == "start": s0 = v
        elif s0 is not None: sil.append((s0, v)); s0 = None
    dur = 61.6; segs = []; cur = 0.0
    for a, b in sil:
        if a < 0.1: cur = b - 0.1; continue
        segs.append((cur, a + 0.1)); cur = b - 0.1
    if s0 is not None and s0 > cur: segs.append((cur, s0 + 0.25))
    elif cur < dur: segs.append((cur, dur))
    return [(max(0, a), b) for a, b in segs if b - a > 0.05]
SEGS = keep_segments()
def remap(t):
    """original clip-B time -> cut time"""
    acc = 0.0
    for a, b in SEGS:
        if t <= a: return acc
        if t <= b: return acc + (t - a)
        acc += b - a
    return acc
B_DUR = sum(b - a for a, b in SEGS)

# ---- 2. his text, anchored to sentence timings in clip B (orig seconds)
LINES = [  # (orig start, orig end, text, scene)
 (1.2, 10.1, "2022-yilda Science jurnalida 26 davlatdan 5 600 dan ortiq kishi, yoshlari farqi 8 kunlikdan 96 yoshgachalar orasida tadqiqot o'tkazilgan.", "science"),
 (10.6, 16.5, "Bu maqola natijasini ko'radigan bo'lsak: kunlik suv almashinuvi farqi 1 litrdan 6 litrgacha.", "results"),
 (17.0, 24.3, "20 yoshli, 70 kilolik yigitda taxminan 3,2 litr, 60 kilolik qizda esa 2,7 litrni tashkil qilgan.", None),
 (24.9, 29.1, "Sportchilarda kuniga taxminan 1 litr ko'proq, chunki ular ko'p harakat qilishadi.", "factors"),
 (29.1, 34.4, "Havo namligi 50 foiz oshsa — yana 0,3 litr qo'shiladi.", None),
 (35.3, 38.5, "Maqola xulosasi shuni ko'rsatdiki: hammaga bir xil me'yor yo'q.", "verdict"),
 (38.9, 40.5, "Asosiy signal bu — chanqoq.", None),
 (40.9, 44.5, "Chanqaganingizda suv ichsangiz, bu eng to'g'ri yo'l hisoblanadi.", None),
 (44.8, 49.2, "8 stakan tavsiyasi esa obyektiv dalil bilan tasdiqlanmagan.", None),
 (50.1, 52.2, "Suv haqida yana nimalarni bilmoqchisiz?", "cta"),
 (52.9, 56.1, "Izohlarda yozib qoldiring. Bizni kuzatishda davom eting,", None),
 (56.1, 59.6, "suv haqida birgalikda suvyektiv fikrlaymiz!", None)]
INTRO = [(0.0, 3.7, "Kuniga 8 stakan suv ichish kerak degan tavsiyani hamma eshitgan."),
         (3.7, 6.0, "Men bir maqola o'qib qoldim.")]

# scene spans in cut time (B part starts at 0)
SC = []
starts = [(i, remap(l[0] - 0.15)) for i, l in enumerate(LINES) if l[3]]
for j, (i, st) in enumerate(starts):
    en = starts[j + 1][1] if j + 1 < len(starts) else B_DUR + 0.6
    SC.append((LINES[i][3], 0.0 if j == 0 else st, en))
ORIG = {"science": 8.0, "results": 9.5, "factors": 7.0, "verdict": 8.0}   # durations the animations were designed for

def s_verdict2(t):
    fr = s_verdict(min(t, 8.0) if t < 8.0 else t)
    return fr

def chip_extra(fr, t, dur):
    # 'chanqoq' chip during his thirst sentence (relative times inside verdict scene)
    a0 = remap(38.9) - [s for s in SC if s[0] == "verdict"][0][1]
    a1 = remap(44.5) - [s for s in SC if s[0] == "verdict"][0][1]
    a = ph(t, a0) * (1 - ph(t, a1, 0.25))
    chip(fr, "Asosiy signal — chanqoq", a, y=1460, col=OK if "OK" in globals() else SKYD)

def o_cta2(im, d, t):
    big(d, 540, 330, "Suv haqida yana", fn("ExtraBold", 72), WHITE, ph(t, 0.0), "ma")
    big(d, 540, 420, "nimalarni bilmoqchisiz?", fn("Black", 84), SKY, ph(t, 0.3), "ma")
    a = ph(t, 1.6)
    w = d.textlength("izohlarda yozib qoldiring ↓", font=fn("Bold", 46)) + 70
    d.rounded_rectangle([(W - w) / 2, 620, (W + w) / 2, 710], 45, fill=SKY + (int(255 * a),))
    d.text((W / 2, 665), "izohlarda yozib qoldiring ↓", font=fn("Bold", 46), fill=NAVY + (int(255 * a),), anchor="mm")
    big(d, 540, 790, "Bizni kuzatishda davom eting", fn("Bold", 46), WHITE, ph(t, 2.6), "ma")
    big(d, 540, 870, "suv haqida birgalikda", fn("ExtraBold", 56), WHITE, ph(t, 4.4), "ma")
    big(d, 540, 945, "suvyektiv fikrlaymiz!", fn("Black", 76), SKY, ph(t, 4.6), "ma")
    big(d, 540, 1060, "Doktor H₂O · @suvyektiv", fn("Bold", 40), SKY, ph(t, 5.4), "ma")

def render_scr(name, dur, out):
    f = {"science": s_science, "results": s_results, "factors": s_factors, "verdict": s_verdict}[name]
    k = {"verdict": 0.62}.get(name, ORIG[name] / dur if dur < ORIG[name] else 1.0)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                          "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(int(round(dur * 30))):
        t = i / 30; fr = f(t * k)
        if name == "verdict": chip_extra(fr, t, dur)
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()

def render_cta(dur, out):
    ov = F_ + "cta_ov.mov"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-c:v", "qtrle", ov], stdin=subprocess.PIPE)
    for i in range(int(round(dur * 30))):
        im = Image.new("RGBA", (W, H)); o_cta2(im, ImageDraw.Draw(im), i / 30); p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "1", "-ss", "1.0", "-i", R + "px/95.mp4", "-i", ov, "-filter_complex",
                    f"[0:v]fps=30,trim=0:{dur:.3f},setpts=PTS-STARTPTS,scale=-2:1920,crop=1080:1920,eq=brightness=-0.10:saturation=0.9,gblur=sigma=1.5[b];"
                    f"[b][1:v]overlay=format=auto,format=yuv420p", "-t", f"{dur:.3f}", "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", out], check=True)

if __name__ == "__main__":
    a = sys.argv[1]
    if a == "info":
        print("B cut dur", round(B_DUR, 2), "segments", len(SEGS))
        for s in SC: print(s, round(s[2] - s[1], 2))
    elif a == "audio":
        f = ";".join(f"[0:a]atrim={x:.3f}:{y:.3f},asetpts=PTS-STARTPTS[a{i}]" for i, (x, y) in enumerate(SEGS))
        f += ";" + "".join(f"[a{i}]" for i in range(len(SEGS))) + f"concat=n={len(SEGS)}:v=0:a=1[o]"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", F_ + "b.mp4", "-filter_complex", f, "-map", "[o]", "-ar", "48000", "-ac", "1", F_ + "voice_cut.wav"], check=True)
    elif a == "segs":
        only = sys.argv[2:]
        for j, (name, st, en) in enumerate(SC):
            if only and name not in only: continue
            out = F_ + f"s{j}_{name}.mp4"
            if name == "cta": render_cta(en - st, out)
            else: render_scr(name, en - st, out)
            print("done", name)
    elif a == "caps":
        import news
        news.KEY = re.compile(r"\d|%|litr|stakan|science|chanqoq|suvyektiv|maqola", re.I)
        ev = [(s + 0.05, e, t) for s, e, t in INTRO]
        ev += [(A_DUR + remap(s) - 0.05, A_DUR + remap(e) + 0.1, t) for s, e, t, _ in LINES]
        news.caps_render(ev, A_DUR + B_DUR + 0.6, F_ + "caps.mov")
    elif a == "build":
        out = sys.argv[2]; total = A_DUR + B_DUR + 0.6
        inp = ["-i", F_ + "a.mp4"]
        for j, (name, st, en) in enumerate(SC): inp += ["-i", F_ + f"s{j}_{name}.mp4"]
        n = len(SC)
        inp += ["-i", F_ + "caps.mov", "-i", F_ + "voice_cut.wav", "-i", F_ + "music.wav"]
        fc = ["[0:v]fps=30,scale=1080:1920,setsar=1,format=yuv420p[v0]"]
        fc += [f"[{j + 1}:v]fps=30,setsar=1,format=yuv420p[v{j + 1}]" for j in range(n)]
        fc.append("".join(f"[v{j}]" for j in range(n + 1)) + f"concat=n={n + 1}:v=1:a=0[vc]")
        fc.append(f"[vc][{n + 1}:v]overlay=format=auto,fade=out:st={total - 0.5:.2f}:d=0.5,format=yuv420p[V]")
        # audio: intro clip audio, then cut voice; music bed under everything, ducked
        fc.append(f"[0:a]aresample=48000,aformat=channel_layouts=mono,atrim=0:{A_DUR:.3f}[ia]")
        fc.append(f"[{n + 2}:a]aresample=48000,aformat=channel_layouts=mono[va]")
        fc.append(f"[ia][va]concat=n=2:v=0:a=1,apad=pad_dur=4,highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-16:TP=-1.5,atrim=0:{total:.3f}[voice]")
        fc.append(f"[{n + 3}:a]atrim=0:{total:.3f},volume={0.0 if "--nomusic" in sys.argv else 0.16},afade=t=in:d=1,afade=t=out:st={total - 1.5:.2f}:d=1.5[mus]")
        fc.append("[voice][mus]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95[A]")
        subprocess.run(["ffmpeg", "-v", "error", "-y"] + inp + ["-filter_complex", ";".join(fc), "-map", "[V]", "-map", "[A]", "-t", f"{total:.3f}",
                        "-c:v", "libx264", "-crf", "21", "-preset", "fast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
        print("total", round(total, 2))

# ---- word-anchored captions (v2): each ≤24-char chunk is timed from whisper word boundaries
def _chunks(s):
    s = re.sub(r"(\d) (\d)", "\\1\u00a0\\2", s); out = []; cur = []
    for w in s.split(" "):
        if cur and len(" ".join(cur + [w])) > 24: out.append(" ".join(cur)); cur = []
        cur.append(w)
    out.append(" ".join(cur)); return out

def _timeline(words, a, b):
    """whisper words inside [a,b] -> list of (t_start, t_end, cum_char_start, cum_char_end)"""
    ws = [w for w in words if w[1] > a - 0.05 and w[0] < b + 0.05]
    tl = []; c = 0
    for s, e, t in ws:
        n = max(1, len(t.strip())); tl.append((max(s, a), min(e, b), c, c + n)); c += n
    return tl, c

def _time_at(tl, total, frac):
    x = frac * total
    for s, e, c0, c1 in tl:
        if x <= c1: return s + (e - s) * (x - c0) / max(1, c1 - c0)
    return tl[-1][1]

def caps_events():
    A = [tuple(w) for seg in json.load(open(F_ + "a.json")) for w in seg["w"]]
    B = [tuple(w) for seg in json.load(open(F_ + "b.json")) for w in seg["w"]]
    ev = []
    for words, lines, mapf in ((A, [(s, e, t) for s, e, t in INTRO], lambda x: x),
                               (B, [(s, e, t) for s, e, t, _ in LINES], lambda x: A_DUR + remap(x))):
        for s, e, t in lines:
            tl, tot = _timeline(words, s, e)
            ch = _chunks(t); L = sum(len(c) for c in ch) + len(ch) - 1; pos = 0
            for c in ch:
                f0, f1 = pos / L, min(1, (pos + len(c)) / L); pos += len(c) + 1
                t0, t1 = (_time_at(tl, tot, f0), _time_at(tl, tot, f1)) if tl else (s + (e - s) * f0, s + (e - s) * f1)
                ev.append([mapf(t0) - 0.06, mapf(t1) + 0.12, c])
    for i in range(len(ev) - 1):                       # no overlaps; close tiny gaps inside a sentence
        if ev[i][1] > ev[i + 1][0]: ev[i][1] = ev[i + 1][0]
        elif ev[i + 1][0] - ev[i][1] < 0.25: ev[i][1] = ev[i + 1][0]
    for i in range(len(ev)):                           # every chunk readable for at least 0.4 s
        if ev[i][1] - ev[i][0] < 0.4:
            ev[i][1] = ev[i][0] + 0.4
            if i + 1 < len(ev) and ev[i + 1][0] < ev[i][1]:
                ev[i + 1][0] = ev[i][1]
    return [tuple(x) for x in ev]

if __name__ == "__main__" and sys.argv[1] == "caps2":
    import news
    news.KEY = re.compile(r"\d|%|litr|stakan|science|chanqoq|suvyektiv|maqola", re.I)
    ev = caps_events()
    for x in ev: print(f"{x[0]:6.2f}-{x[1]:6.2f} {x[2]}")
    if "--dry" not in sys.argv: news.caps_render(ev, A_DUR + B_DUR + 0.6, F_ + "caps.mov")
