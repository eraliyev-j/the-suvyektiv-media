"""8 stakan, English-subtitle version (LinkedIn). Same picture/voice as v4; captions, chips and CTA in English.
usage: final_en.py caps | screen | cta | build out.mp4"""
import sys, re, subprocess
_argv = list(sys.argv); sys.argv = ["x", "none"]
exec(open("/home/claude/r5/fin/final2.py").read().replace('if __name__ == "__main__":', "if False:"))
sys.argv = _argv
sys.path.insert(0, "/home/claude/r2"); import news

EN = {  # Uzbek sentence -> English
 INTRO[0][2]: "Everyone has heard you should drink 8 glasses of water a day.",
 INTRO[1][2]: "Then I came across a paper.",
 LINES[0][2]: "In 2022, a study in Science looked at over 5,600 people from 26 countries, aged 8 days to 96 years.",
 LINES[1][2]: "The result: daily water turnover ranged from 1 to 6 liters.",
 LINES[2][2]: "A 20-year-old man of 70 kg: about 3.2 liters. A 60 kg woman: 2.7 liters.",
 LINES[3][2]: "Athletes turn over about 1 liter more a day, because they move more.",
 LINES[4][2]: "If humidity rises by 50%, add another 0.3 liters.",
 LINES[5][2]: "The paper's conclusion: there is no one-size-fits-all amount.",
 LINES[6][2]: "The main signal is thirst.",
 LINES[7][2]: "Drinking when you are thirsty is the right way.",
 LINES[8][2]: "The 8-glasses rule is not backed by objective evidence.",
 LINES[9][2]: "What else would you like to know about water?",
 LINES[10][2]: "Tell us in the comments. Keep following us,",
 LINES[11][2]: "and let's think about water together, suvyektiv style!",
}

def en_events():
    ev = caps_events(); out = []; k = 0
    for t in [x[2] for x in INTRO] + [x[2] for x in LINES]:
        n = len(_chunks(t)); seg = ev[k:k + n]; k += n
        out.append((seg[0][0], seg[-1][1], EN[t]))
    assert k == len(ev), (k, len(ev))
    return out

CHIPS = [("26 countries", 8.30, 9.60, NAVY, None),
         ("5,600+ people", 9.66, 10.90, NAVY, None),
         ("8 days to 96 years", 10.94, 15.50, NAVY, None),
         ("1 L to 6 L", 19.76, 21.65, NAVY, "varies from person to person"),
         ("Man · 70 kg ≈ 3.2 L", 23.42, 26.95, NAVY, None),
         ("Man 3.2 L · Woman 2.7 L", 26.98, 28.80, NAVY, None),
         ("Athletes: + ~1 L", 29.96, 33.10, NAVY, None),
         ("Humidity +50% → +0.3 L", 34.70, 38.25, NAVY, None),
         ("No one-size-fits-all", 39.36, 41.68, NAVY, None),
         ("Main signal: thirst", 41.71, 47.00, (46, 150, 100), None),
         ("8 glasses: no solid evidence", 47.04, CTA0, WARN, "Science, 2022")]

def o_cta3(im, d, t):
    big(d, 540, 330, "What else would you like", fn("ExtraBold", 66), WHITE, ph(t, 0.1), "ma")
    big(d, 540, 420, "to know about water?", fn("Black", 84), SKY, ph(t, 1.0), "ma")
    a = ph(t, 2.3); s = "tell us in the comments ↓"
    w = d.textlength(s, font=fn("Bold", 46)) + 70
    d.rounded_rectangle([(W - w) / 2, 620, (W + w) / 2, 710], 45, fill=SKY + (int(255 * a),))
    d.text((W / 2, 665), s, font=fn("Bold", 46), fill=NAVY + (int(255 * a),), anchor="mm")
    big(d, 540, 790, "Keep following us", fn("Bold", 46), WHITE, ph(t, 3.4), "ma")
    big(d, 540, 870, "let's think about water", fn("ExtraBold", 56), WHITE, ph(t, 5.4), "ma")
    big(d, 540, 945, "together, suvyektiv!", fn("Black", 76), SKY, ph(t, 6.75), "ma")
    big(d, 540, 1060, "Doktor H₂O · @suvyektiv", fn("Bold", 40), SKY, ph(t, 7.4), "ma")

a = sys.argv[1]
if a == "caps":
    news.KEY = re.compile(r"\d|%|liter|glass|science|thirst|suvyektiv|paper|evidence", re.I)
    ev = en_events()
    for x in ev: print(f"{x[0]:6.2f}-{x[1]:6.2f} {x[2]}")
    if "--dry" not in sys.argv: news.caps_render(ev, TOTAL, F_ + "en_caps.mov")
elif a == "screen":
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                          "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p", F_ + "en_screen.mp4"], stdin=subprocess.PIPE)
    for i in range(int(round((CTA0 - G0) * 30))): p.stdin.write(screen_frame(G0 + i / 30).tobytes())
    p.stdin.close(); p.wait(); print("screen done")
elif a == "still":
    screen_frame(float(sys.argv[2])).convert("RGB").save(sys.argv[3])
elif a == "cta":
    dur = TOTAL - CTA0; ov = F_ + "en_cta.mov"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", "30", "-i", "-", "-c:v", "qtrle", ov], stdin=subprocess.PIPE)
    for i in range(int(round(dur * 30))):
        im = Image.new("RGBA", (W, H)); o_cta3(im, ImageDraw.Draw(im), i / 30); p.stdin.write(im.tobytes())
    p.stdin.close(); p.wait()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "1", "-ss", "1.0", "-i", R + "px/95.mp4", "-i", ov, "-filter_complex",
                    f"[0:v]fps=30,trim=0:{dur:.3f},setpts=PTS-STARTPTS,scale=-2:1920,crop=1080:1920,eq=brightness=-0.10:saturation=0.9,gblur=sigma=1.5[b];"
                    f"[b][1:v]overlay=format=auto,format=yuv420p", "-t", f"{dur:.3f}", "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", F_ + "en_ctav.mp4"], check=True)
    print("cta done")
elif a == "build":
    out = sys.argv[2]
    inp = ["-i", F_ + "a.mp4", "-i", F_ + "en_screen.mp4", "-i", F_ + "en_ctav.mp4", "-i", F_ + "en_caps.mov", "-i", F_ + "voice_cut.wav", "-i", F_ + "music2.wav"]
    fc = ["[0:v]fps=30,scale=1080:1920,setsar=1,format=yuv420p[v0]", "[1:v]fps=30,setsar=1,format=yuv420p[v1]", "[2:v]fps=30,setsar=1,format=yuv420p[v2]",
          "[v0][v1][v2]concat=n=3:v=1:a=0[vc]",
          f"[vc][3:v]overlay=format=auto,fade=out:st={TOTAL - 0.5:.2f}:d=0.5,format=yuv420p[V]",
          f"[0:a]aresample=48000,aformat=channel_layouts=mono,atrim=0:{A_DUR:.3f}[ia]",
          "[4:a]aresample=48000,aformat=channel_layouts=mono[va]",
          f"[ia][va]concat=n=2:v=0:a=1,apad=pad_dur=4,highpass=f=80,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-16:TP=-1.5,atrim=0:{TOTAL:.3f}[voice]",
          f"[5:a]atrim=0:{TOTAL:.3f},volume=0.16,afade=t=in:d=1,afade=t=out:st={TOTAL - 1.5:.2f}:d=1.5[mus]",
          "[voice][mus]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95[A]"]
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + inp + ["-filter_complex", ";".join(fc), "-map", "[V]", "-map", "[A]", "-t", f"{TOTAL:.3f}",
                    "-c:v", "libx264", "-crf", "21", "-preset", "fast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    print("built", out)
