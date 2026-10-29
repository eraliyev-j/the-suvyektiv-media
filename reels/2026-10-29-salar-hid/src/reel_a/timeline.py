"""Spoken text (1:1 with the voice) on the original timeline -> cut timeline; subtitle chunks."""
import json, re
KEEP = json.load(open("/home/claude/salarA/keep.json"))

def remap(t):
    acc = 0.0
    for a, b in KEEP:
        if t < a: return acc
        if t <= b: return acc + t - a
        acc += b - a
    return acc

# (orig start, orig end, spoken text, scene)
SENT = [
    (0.60, 4.70, "Sergelida Salar oqova tozalash inshooti yaqinida yashovchilar bu hidni yaxshi bilishadi.", "hook"),
    (4.70, 6.30, "Chirigan tuxum hidi.", "hook"),
    (7.00, 8.55, "Qiziq, bu hid qayerdan keladi?", "hook"),
    (9.45, 12.56, "Bunga aybdor yagona vodorod sulfid gazi hisoblanadi.", "h2s"),
    (13.33, 17.70, "Salarda oqova suvni bakteriyalar tozalaganligi uchun ularga doimiy kislorod kerak bo'ladi.", "bakteriya"),
    (17.84, 23.80, "Kislorod yetmagan joyda boshqa bakteriyalar sulfat bilan nafas oladi va vodorod sulfid gazini chiqaradi.", "jarayon"),
    (24.32, 28.10, "Burnimiz uni hattoki milliard qismdan yarim qism bo'lsa ham sezadi.", "ppb"),
    (29.50, 35.13, "2021 yilda 18 ta korxona oqova suvni mana shu tozalash inshootiga tashlaganligi aniqlandi.", "korxona"),
    (35.55, 38.32, "Teri va to'qimachilik zavodlari shular jumlasidandir.", "teri"),
    (39.30, 43.16, "Kimyoviy moddalar suvni tozalaydigan bakteriyalarni batamom nobud qilgan", "nobud"),
    (43.16, 47.65, "va tozalovchi bakteriyalar kamayganligi uchun oqova suv chirib, hidni kuchaytirgan.", "chirish"),
    (48.40, 53.00, "Ya'ni hid faqatgina inshootdan emas, balki zavodlarning oqovasidan ham kelgan.", "xulosa"),
    (54.20, 61.30, "Keyingi videoda bu hidni yo'qotish uchun qilingan chora-tadbirlar haqida batafsil ma'lumot berib o'tiladi.", "keyingi"),
    (62.00, 65.62, "Bizni kuzatishda davom eting, suv haqida suvyektiv fikrlaymiz.", "cta"),
]

def sentences():
    return [(round(remap(a), 3), round(remap(b), 3), s, sc) for a, b, s, sc in SENT]

def chunks(maxc=24, maxw=4):
    """subtitle chunks: words of a sentence timed proportionally to character length, grouped <= maxc chars"""
    out = []
    for a, b, s, _ in sentences():
        words = s.split()
        L = sum(len(w) + 1 for w in words); t = a; groups, cur = [], []
        for w in words:
            if cur and (len(" ".join(cur + [w])) > maxc or len(cur) >= maxw or cur[-1][-1] in ",:"):
                groups.append(cur); cur = []
            cur.append(w)
        groups.append(cur)
        for g in groups:
            dur = (b - a) * sum(len(w) + 1 for w in g) / L
            out.append([round(t, 3), round(t + dur, 3), " ".join(g)]); t += dur
    # snap chunk starts to the nearest real word onset from whisper (orig timeline -> cut timeline)
    ws = [remap(w["s"]) for w in json.load(open("/home/claude/salarA/words.json"))]
    sent_starts = {x[0] for x in sentences()}
    for c in out:
        if c[0] in sent_starts: continue
        near = min(ws, key=lambda v: abs(v - c[0]))
        if abs(near - c[0]) < 0.35: c[0] = round(near, 3)
    for i in range(len(out) - 1): out[i][1] = max(out[i][1], out[i][0] + 0.3)
    for i in range(len(out) - 1):                  # hold each chunk until the next one if the gap is short
        if out[i + 1][0] - out[i][1] < 0.6: out[i][1] = out[i + 1][0]
    return out

if __name__ == "__main__":
    for x in sentences(): print(x)
    print(len(chunks()), "chunks")
    for c in chunks()[:12]: print(c)
