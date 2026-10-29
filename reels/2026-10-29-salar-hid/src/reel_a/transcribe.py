import json, sys
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
import numpy as np, wave
with wave.open(sys.argv[1]) as wf:
    audio = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768
segs, info = m.transcribe(audio, language="uz", word_timestamps=True, vad_filter=False, beam_size=5)
words = []
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text}")
    for w in s.words:
        words.append({"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)})
json.dump(words, open(sys.argv[2], "w"), ensure_ascii=False, indent=0)
