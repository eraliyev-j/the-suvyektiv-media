"""Reel B voice clean-up (29.10): rumble HPF 75 Hz, LPF 15 kHz; door noise at 3.25-4.30 s (squeak 2379/4758 Hz tones +
low thump) -> HPF 120 Hz + notches inside that window; then ffmpeg arnndn (RNNoise cb.rnnn, mix 0.85) + afftdn nr=8.
usage: python3 denoise_b.py in48.wav pre.wav ; ffmpeg -i pre.wav -af "arnndn=m=cb.rnnn:mix=0.85,afftdn=nr=8:nf=-55" clean.wav"""
import sys, numpy as np, scipy.io.wavfile as wf
from scipy.signal import butter, sosfiltfilt, iirnotch, filtfilt
sr, a = wf.read(sys.argv[1]); a = a.astype(np.float64) / 32768
x = sosfiltfilt(butter(4, 75, 'hp', fs=sr, output='sos'), a)
x = sosfiltfilt(butter(6, 15000, 'lp', fs=sr, output='sos'), x)
y = sosfiltfilt(butter(4, 120, 'hp', fs=sr, output='sos'), x)
for f0 in (2379, 4758, 7137):
    for df in (-12, 0, 12):
        b, c = iirnotch(f0 + df, 30, fs=sr); y = filtfilt(b, c, y)
t = np.arange(len(x)) / sr
w = np.clip((t - 3.25) / 0.08, 0, 1) * np.clip((4.30 - t) / 0.08, 0, 1)
wf.write(sys.argv[2], sr, ((x * (1 - w) + y * w) * 32767).astype(np.int16))
