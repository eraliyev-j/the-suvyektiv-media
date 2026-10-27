"""Bright 'explainer' bed (new for 8 stakan v4): 108 BPM, marimba-like plucked chords (C–G–Am–F), soft
kick + clap + shaker, round sub bass, airy pad; gentle build, drop at 'Maqola xulosasi'. Generated from scratch."""
import sys, numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
SR = 48000; DUR = 61.5; n = int(SR * DUR); b = 60 / 108
L = np.zeros(n); R = np.zeros(n); rng = np.random.default_rng(3)
f = lambda k: 440 * 2 ** ((k - 69) / 12)
def put(s, t, g, pan=0.0):
    i = int(t * SR)
    if i >= n or i < 0: return
    s = s[: n - i] * g; L[i:i + len(s)] += s * (1 - pan); R[i:i + len(s)] += s * (1 + pan)
def marimba(k, d=0.6):
    t = np.arange(int(SR * d)) / SR
    x = np.sin(2 * np.pi * f(k) * t) * np.exp(-t * 7) + 0.35 * np.sin(2 * np.pi * f(k) * 4 * t) * np.exp(-t * 28) + 0.15 * np.sin(2 * np.pi * f(k) * 10 * t) * np.exp(-t * 60)
    return x * np.minimum(1, t / 0.002)
def kick():
    t = np.arange(int(SR * 0.35)) / SR; return np.sin(2 * np.pi * np.cumsum(50 + 110 * np.exp(-t * 35)) / SR) * np.exp(-t * 9)
def clap():
    t = np.arange(int(SR * 0.18)) / SR; e = np.exp(-t * 30) * (1 + 0.6 * (np.sin(2 * np.pi * 90 * t) > 0))
    return sosfilt(butter(2, [900, 4000], 'bp', fs=SR, output='sos'), rng.standard_normal(len(t))) * e
def shaker():
    t = np.arange(int(SR * 0.06)) / SR; return sosfilt(butter(4, 6000, 'hp', fs=SR, output='sos'), rng.standard_normal(len(t))) * np.exp(-t * 70)
def sub(k, d):
    t = np.arange(int(SR * d)) / SR; return np.sin(2 * np.pi * f(k) * t) * np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.05)
def pad(ks, d):
    t = np.arange(int(SR * d)) / SR; e = np.minimum(1, t / 0.8) * np.minimum(1, (d - t) / 0.8)
    x = sum(np.sin(2 * np.pi * f(k) * (1 + dt) * t) for k in ks for dt in (-0.003, 0.003))
    return x * e / (2 * len(ks))
PROG = [([60, 64, 67], 48), ([59, 62, 67], 43), ([60, 64, 69], 45), ([60, 65, 69], 41)]   # C G/B Am F
PAT = [0, 2, 1, 2, 0, 2, 1, 2]
bar = 4 * b; DROP = 38.3; INTRO = 6.1
for bi in range(int(DUR / bar) + 1):
    t0 = bi * bar; ch, bs = PROG[bi % 4]
    lvl = 0.55 if t0 < INTRO else 1.0
    for q, k in enumerate(PAT):                                   # 8th-note marimba
        put(marimba(ch[k] + 12), t0 + q * b / 2, 0.16 * lvl, -0.25 if q % 2 else 0.25)
    if t0 >= 1.5 * bar: put(pad(ch, bar + 0.4), t0 - 0.1, 0.10)
    if t0 >= INTRO - 0.01:
        for q in range(4):
            if q in (0, 2): put(kick(), t0 + q * b, 0.55)
            else: put(clap(), t0 + q * b, 0.16, 0.1)
        for q in range(8): put(shaker(), t0 + q * b / 2 + b / 4, 0.05, -0.3)
        for q, d in ((0, 1.5), (1.5, 1.0), (2.5, 1.5)): put(sub(bs - 12, d * b), t0 + q * b, 0.30)
    if t0 >= DROP - 0.01:
        for q in range(8): put(marimba(ch[(q + 1) % 3] + 24, 0.3), t0 + q * b / 2 + b / 4, 0.06, 0.4)
rt = np.arange(int(SR * 2.0)) / SR
put(sosfilt(butter(2, [500, 7000], 'bp', fs=SR, output='sos'), rng.standard_normal(len(rt))) * (rt / 2.0) ** 3, DROP - 2.0, 0.10)
out = np.stack([L, R]); out = np.tanh(out * 1.4); t = np.arange(n) / SR
out *= np.clip(t / 0.5, 0, 1) * np.clip((DUR - t) / 2.0, 0, 1); out /= np.abs(out).max() * 1.1
wavfile.write(sys.argv[1], SR, (out.T * 32767).astype(np.int16)); print("ok")
