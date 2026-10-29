"""Trim pauses: every silence longer than 0.35 s is shortened to ~0.28 s. Writes keep.json (intervals) and voice_cut.wav."""
import json, subprocess, sys
SRC = sys.argv[1]
DUR = 66.303
SIL = [(0.0, 0.665), (6.307, 7.025), (8.558, 9.492), (12.565, 13.341), (21.852, 22.251), (28.119, 29.544),
       (35.139, 35.557), (38.329, 39.329), (47.681, 48.401), (53.015, 54.243), (56.124, 56.711),
       (61.309, 62.029), (63.344, 63.859), (65.640, 66.303)]
PRE, POST = 0.12, 0.16           # keep this much of each silence after speech / before speech
keep, t = [], 0.0
for a, b in SIL:
    s0 = t; e0 = a + PRE if a > 0 else 0
    if e0 > s0: keep.append((round(s0, 3), round(min(e0, b), 3)))
    t = max(b - POST, a)
keep = [k for k in keep if k[1] - k[0] > 0.05]
keep[0] = (max(0, keep[0][0]), keep[0][1])
json.dump(keep, open("keep.json", "w"))
sel = "+".join(f"between(t,{a},{b})" for a, b in keep)
total = sum(b - a for a, b in keep)
# light cleanup: highpass, gentle de-ess via EQ, compressor; loudnorm with apad then atrim so the tail is not cut
af = (f"aselect='{sel}',asetpts=N/SR/TB,highpass=f=80,equalizer=f=6500:t=q:w=2:g=-3,"
      f"acompressor=threshold=-20dB:ratio=3:attack=5:release=80,apad=pad_dur=1,"
      f"loudnorm=I=-15:TP=-1.5:LRA=9,atrim=0:{total + 0.25:.3f}")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-af", af, "-ar", "48000", "-ac", "1", "voice_cut.wav"], check=True)
print(len(keep), "parts, total", round(total, 2), "s")
