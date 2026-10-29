"""Own background music: calm 'investigation' bed — soft minor pad, low pulse, light clock tick. No samples, no third-party audio."""
import numpy as np, wave, sys
SR = 48000
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 63.0
t = np.arange(int(SR * DUR)) / SR
def note(m): return 440 * 2 ** ((m - 69) / 12)
BPM = 84; beat = 60 / BPM; bar = 4 * beat
chords = [[50, 57, 62, 65], [46, 53, 58, 62], [48, 55, 60, 64], [45, 52, 57, 61]]   # Dm  Bb  C  A
out = np.zeros_like(t)
for i in range(int(DUR / bar) + 1):
    t0 = i * bar; ch = chords[i % 4]
    m = (t >= t0) & (t < t0 + bar + 1.0); tt = t[m] - t0
    env = np.minimum(1, tt / 0.8) * np.exp(-np.maximum(0, tt - bar) * 3)
    for k, n in enumerate(ch):
        f = note(n + 12)
        out[m] += 0.05 * env * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2 * f * tt + 0.3) + 0.15 * np.sin(2 * np.pi * f * 1.003 * tt))
    for b in range(4):                     # low pulse on each beat
        tb = t0 + b * beat; mm = (t >= tb) & (t < tb + 0.5); u = t[mm] - tb
        out[mm] += 0.10 * np.exp(-u * 9) * np.sin(2 * np.pi * note(ch[0] - 12) * u)
    for b in range(8):                     # soft tick on eighths
        tb = t0 + b * beat / 2; mm = (t >= tb) & (t < tb + 0.03); u = t[mm] - tb
        out[mm] += (0.025 if b % 2 else 0.04) * np.exp(-u * 160) * np.random.default_rng(i * 8 + b).standard_normal(u.size)
fade = np.minimum(1, t / 1.5) * np.minimum(1, (DUR - t) / 2.0)
out *= fade
out = np.tanh(out * 2.2) / 2.2
out /= np.max(np.abs(out)) / 0.7
st = np.stack([out, np.roll(out, 240)], 1)
with wave.open("music.wav", "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
print("music", DUR)
