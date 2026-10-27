"""8 stakan v4: one continuous screen-record pass where every scroll / marker / chip is cued to the exact
subtitle chunk (= his spoken words). Intro clip + CTA unchanged in look; CTA lines cued too.
usage: final2.py screen | cta | build out.mp4 [--nomusic]"""
import sys, subprocess
sys.argv_saved = list(sys.argv); sys.argv = ["x", "none"]
exec(open("/home/claude/r5/fin/final.py").read().replace('if __name__ == "__main__":', "if False:").replace('if __name__ == "__main__" and', "if False and"))
sys.argv = sys.argv_saved

G0 = A_DUR            # screen part starts (global seconds)
CTA0 = 51.45          # CTA starts (just before "Suv haqida yana")
K = "pmc"
yT, yN = y_of(K, P_T, 0.30), y_of(K, P_N, 0.40)
yR, yM = y_of(K, P_R, 0.40), y_of(K, P_M, 0.35)
yH, y1 = y_of(K, P_H, 0.07), y_of(K, P_1, 0.32)
KEYS = [(6.12, yT - 420, 1.0, 0), (6.70, yT, 1.0, 0),            # title
        (7.95, yT, 1.0, 0), (8.70, yN, 1.0, 0),                   # "jurnalida 26 davlatdan" -> sample sentence
        (15.70, yN, 1.0, 0), (16.90, yR - 250, 1.0, 0), (18.30, yR, 1.0, 0),   # "Bu maqola natijasini..." -> range sentence
        (21.55, yR, 1.0, 0), (22.30, yM, 1.0, 0),                 # "20 yoshli" -> example sentence
        (28.45, yM, 1.0, 0), (29.20, yH, 1.0, 0),                 # "Sportchilarda" -> athletes/humidity
        (38.10, yH, 1.0, 0), (38.95, y1, 1.0, 0)]                 # "Maqola xulosasi" -> conclusion
MARKS = [(P_T, 6.35, 1.3, MARK_SKY),
         (P_N, 9.66, 4.40, MARK_HOT),          # "5 600 dan ortiq kishi ... 96 yoshgacha"
         (P_R, 19.76, 1.90, MARK_SKY),         # "farqi 1 litrdan 6 litrgacha"
         (P_M, 23.42, 1.20, MARK_HOT),         # "yigitda taxminan 3,2"
         (P_F, 25.60, 1.40, MARK_HOT),         # "60 kilolik qizda ... 2,7"
         (P_A, 28.84, 2.80, MARK_SKY),         # "Sportchilarda ... 1 litr ko'proq"
         (P_H, 33.18, 3.80, MARK_SKY),         # "Havo namligi 50 foiz ... 0,3 litr"
         (P_1, 39.36, 2.30, MARK_SKY),         # "hammaga bir xil me'yor yo'q"
         (P_8, 47.04, 4.40, MARK_HOT)]         # "8 stakan tavsiyasi esa ... tasdiqlanmagan"
CHIPS = [("26 davlat", 8.30, 9.60, NAVY, None),
         ("5 600+ kishi", 9.66, 10.90, NAVY, None),
         ("8 kunlikdan 96 yoshgacha", 10.94, 15.50, NAVY, None),
         ("1 L dan 6 L gacha", 19.76, 21.65, NAVY, "odamdan odamga farq qiladi"),
         ("Yigit · 70 kg ≈ 3,2 L", 23.42, 26.95, NAVY, None),
         ("Yigit 3,2 L · Qiz 2,7 L", 26.98, 28.80, NAVY, None),
         ("Sportchilar: + ~1 L", 29.96, 33.10, NAVY, None),
         ("Namlik +50% → +0,3 L", 34.70, 38.25, NAVY, None),
         ("Hammaga bir xil me'yor yo'q", 39.36, 41.68, NAVY, None),
         ("Asosiy signal — chanqoq", 41.71, 47.00, (46, 150, 100), None),
         ("8 stakan — obyektiv dalil yo'q", 47.04, CTA0, WARN, "Science, 2022")]
TOUCH = [(6.12, 6.70), (7.95, 8.70), (16.0, 18.3), (21.55, 22.30), (28.45, 29.20), (38.10, 38.95)]

def screen_frame(G):
    fr, cam = view(K, KEYS, G, MARKS)
    for a0, a1 in TOUCH:                                         # finger dot while scrolling
        if a0 - 0.2 <= G <= a1 + 0.2:
            u = min(1, max(0, (G - a0) / (a1 - a0)))
            touch(fr, 820, 1500 - 650 * ease(u), min(1, (G - a0 + 0.2) / 0.2, (a1 + 0.2 - G) / 0.2))
    tag(fr, "Yamada et al., Science, 2022", ph(G, 6.3) * (1 - ph(G, 15.4, 0.3)) + ph(G, 38.3) * (1 - ph(G, 47.0, 0.3)))
    for s, t0, t1, col, sub in CHIPS:
        a = ph(G, t0, 0.25) * (1 - ph(G, t1 - 0.2, 0.2))
        if a > 0: chip(fr, s, a, col=col, sub=sub)
    return fr

def o_cta3(im, d, t):
    big(d, 540, 330, "Suv haqida yana", fn("ExtraBold", 72), WHITE, ph(t, 0.1), "ma")
    big(d, 540, 420, "nimalarni bilmoqchisiz?", fn("Black", 84), SKY, ph(t, 1.0), "ma")
    a = ph(t, 2.3)
    w = d.textlength("izohlarda yozib qoldiring ↓", font=fn("Bold", 46)) + 70
    d.rounded_rectangle([(W - w) / 2, 620, (W + w) / 2, 710], 45, fill=SKY + (int(255 * a),))
    d.text((W / 2, 665), "izohlarda yozib qoldiring ↓", font=fn("Bold", 46), fill=NAVY + (int(255 * a),), anchor="mm")
    big(d, 540, 790, "Bizni kuzatishda davom eting", fn("Bold", 46), WHITE, ph(t, 3.4), "ma")
    big(d, 540, 870, "suv haqida birgalikda", fn("ExtraBold", 56), WHITE, ph(t, 5.4), "ma")
    big(d, 540, 945, "suvyektiv fikrlaymiz!", fn("Black", 76), SKY, ph(t, 6.75), "ma")
    big(d, 540, 1060, "Doktor H₂O · @suvyektiv", fn("Bold", 40), SKY, ph(t, 7.4), "ma")

TOTAL = A_DUR + B_DUR + 0.6
if __name__ == "__main__":
    a = sys.argv[1]
    if a == "screen":
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                              "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p", F_ + "v4_screen.mp4"], stdin=subprocess.PIPE)
        for i in range(int(round((CTA0 - G0) * 30))): p.stdin.write(screen_frame(G0 + i / 30).tobytes())
        p.stdin.close(); p.wait(); print("screen done")
    elif a == "still":
        screen_frame(float(sys.argv[2])).convert("RGB").save(sys.argv[3])
    elif a == "cta":
        dur = TOTAL - CTA0; ov = F_ + "cta3.mov"
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-c:v", "qtrle", ov], stdin=subprocess.PIPE)
        for i in range(int(round(dur * 30))):
            im = Image.new("RGBA", (W, H)); o_cta3(im, ImageDraw.Draw(im), i / 30); p.stdin.write(im.tobytes())
        p.stdin.close(); p.wait()
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "1", "-ss", "1.0", "-i", R + "px/95.mp4", "-i", ov, "-filter_complex",
                        f"[0:v]fps=30,trim=0:{dur:.3f},setpts=PTS-STARTPTS,scale=-2:1920,crop=1080:1920,eq=brightness=-0.10:saturation=0.9,gblur=sigma=1.5[b];"
                        f"[b][1:v]overlay=format=auto,format=yuv420p", "-t", f"{dur:.3f}", "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", F_ + "v4_cta.mp4"], check=True)
        print("cta done")
    elif a == "build":
        out = sys.argv[2]; mus = 0.0 if "--nomusic" in sys.argv else 0.16
        inp = ["-i", F_ + "a.mp4", "-i", F_ + "v4_screen.mp4", "-i", F_ + "v4_cta.mp4", "-i", F_ + "caps.mov", "-i", F_ + "voice_cut.wav", "-i", F_ + "music2.wav"]
        fc = ["[0:v]fps=30,scale=1080:1920,setsar=1,format=yuv420p[v0]", "[1:v]fps=30,setsar=1,format=yuv420p[v1]", "[2:v]fps=30,setsar=1,format=yuv420p[v2]",
              "[v0][v1][v2]concat=n=3:v=1:a=0[vc]",
              f"[vc][3:v]overlay=format=auto,fade=out:st={TOTAL - 0.5:.2f}:d=0.5,format=yuv420p[V]",
              f"[0:a]aresample=48000,aformat=channel_layouts=mono,atrim=0:{A_DUR:.3f}[ia]",
              "[4:a]aresample=48000,aformat=channel_layouts=mono[va]",
              f"[ia][va]concat=n=2:v=0:a=1,apad=pad_dur=4,highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-16:TP=-1.5,atrim=0:{TOTAL:.3f}[voice]",
              f"[5:a]atrim=0:{TOTAL:.3f},volume={mus},afade=t=in:d=1,afade=t=out:st={TOTAL - 1.5:.2f}:d=1.5[mus]",
              "[voice][mus]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95[A]"]
        subprocess.run(["ffmpeg", "-v", "error", "-y"] + inp + ["-filter_complex", ";".join(fc), "-map", "[V]", "-map", "[A]", "-t", f"{TOTAL:.3f}",
                        "-c:v", "libx264", "-crf", "21", "-preset", "fast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
        print("total", round(TOTAL, 2))
