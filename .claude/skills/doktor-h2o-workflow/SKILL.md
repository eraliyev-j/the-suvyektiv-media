---
name: doktor-h2o-workflow
description: Use whenever preparing a Doktor H2O (@suvyektiv) Uzbek reel, Short, carousel or caption. Applies the ig-* Instagram agent skills (hooks, beats, captions, humanizer) adapted to Uzbek and this repo's video pipeline.
---

# Doktor H₂O — reel / post ish tartibi

Ovoz va brend: `brand/voice.md` (avval o'qing). Uzoq muddatli maqsad va strategiya: `doktor-h2o-brand` skill (har reel shu maqsadga xizmat qilsin). Ichki skill paketi: `.claude/skills/ig-*`
(Jake Schincariol, "instagram-agent-skill", MIT — `LICENSE-instagram-agent-skill`).

## Qaysi skill qachon

| Ish | Skill |
|---|---|
| Reel skripti, hook, beat vaqtlari | `ig-reel` (hookscore.py, beats.py, hooks.json) |
| Trend / boshqa akkauntdan g'oya olish | `ig-viral` (swipe.py) |
| Caption + hashtag | `ig-caption` (caption.py) |
| Carousel post | `ig-carousel` |
| Matnni "AI hidi"dan tozalash | `ig-human` (humanize.py, detect.py) |
| Bitta reelni Short / carousel / storyga aylantirish | `ig-repurpose` |
| Haftalik reja (Se/Pa/Sh 16:00 KST) | `ig-plan` |
| Izohlarga javob, DM | `ig-reply`, `ig-comment`, `ig-dm` |
| Profil / akkaunt tahlili | `ig-profile`, `ig-audit` |
| Intro / talking-head videoga effekt | `effects` (fx.py, 42 effekt, Vibha Ramprakash, MIT) |

## Reel uzunligi va ilmiy chuqurlik (audit 2026-10-28)

Tomoshabin 8–12 s da ketadi, reel 34 s bo'ladimi yoki 77 s, farqi yo'q. 40 s dan keyingi qism
deyarli ko'rilmaydi. Shuning uchun:

- **Bitta reel = bitta ilmiy da'vo + 1 asosiy raqam + manba ekranda.** Maqsad 30–40 s, **maksimum 45 s**.
- Skript yozishdan oldin bitta gap bilan yoz: "Bu reel ___ ni isbotlaydi." Ikki gap chiqsa, bu ikki reel.
- Qolgan ilmiy tafsilot tashlab yuborilmaydi, boshqa joyga ko'chadi:
  1. **Caption**: tafsilot, ikkinchi darajali raqamlar, to'liq manba (DOI).
  2. **Hamroh karusel** (chorshanba sloti): bosqichlar, ro'yxatlar, jadval. Ketma-ketlik bo'lsa, karusel to'g'ri format.
  3. **Ikkinchi mustaqil reel**: boshqa da'vo, boshqa hook ("2-qism" emas, seriya yo'q).
  4. Keyinchalik YouTube uzun video (5–10 daq).
- Manba ekranda turishi ishonchni so'zsiz beradi: "Science, 2022" kartasi 1 s, uni o'qib berish 5 s.
- Ovoz ~2,5 so'z/s → 40 s ≈ 90–100 so'z. Skript 110 so'zdan oshsa, montajdan oldin qisqartir.
- Skript 45 s dan oshsa, Javohirga montajdan **oldin** ikki variant taklif qil: qisqartirish yoki bo'lish.

## Reel uchun majburiy qoidalar (ig-reel'dan)

1. Hook 3 ta variantda yoziladi, eng kuchlisi tanlanadi; hook birinchi 3 soniyada tugaydi.
   "Keling, …", "Bugun …", o'zini tanishtirish hookka kirmaydi. Maqom ("suv tadqiqotchisi") kerak bo'lsa, ekran kartasida.
2. Har bir beat ≤ 4 s, bitta beat'da bitta raqam; ekrandagi bitta karta ≤ 6 so'z.
3. Bir xil da'vo ikki beat'da takrorlanmaydi (2050 skriptidagi xato).
4. Safe zone: matn y 230–1440, o'ngdan 230 px bo'sh (IG tugmalari). Subtitr y≈1180.
5. Oxiri hookka qaytadi (loop echo), keyin CTA.
6. **CTA: aytiladigan qismi ≤ 4 s, bitta so'rov** (mavzuga bog'langan savol, masalan "Siz kuniga necha stakan ichasiz? Izohda yozing."). To'liq brend gapi ("Suvni qadrlang! … suvyektiv fikrlaymiz!") ekranda yakuniy kartada turadi. Javohir boshqacha aytsa, uning so'zi.
7. Raqamlar faqat manbadan; manba ekranda.
8. `hookscore.py` o'zbek tilida ishonchsiz (eng yaxshi real hookni eng past baholagan). Hook tanlash: aniq raqam yoki tomoshabinning kundalik holati + savol, ≤ 12 so'z.

## Caption qoidalari (ig-caption'dan)

- Birinchi 125 belgi: asosiy fikr **raqam yoki nom bilan** (masalan "Londonda 130 tonnalik tiqin…"), "suv" so'zi shu qismda. Karusel bo'lsa, uning hooki birinchi qatorda.
- Bitta so'rov (CTA): izohda savol yozish.
- **Hashtag ≤ 5, o'zbekcha qidiruv so'zlari** (`#suv #suvtozalash #suvtejash #bilasizmi #uzbekistan`). `#subscribe`, `#water`, `#health` kabi inglizchasi yo'q. Captionda havola yo'q.
- Em-dash (—), "AI so'zlari" va ko'rinmas belgilarni olib tashlash (ig-human).
- **Shablon iboralar taqiqlangan** (audit 28.10, 6 captiondan 4 tasida takrorlangan): "Oʻylab qarasam, … bilmas ekanmiz", "Hammamiz …" bilan boshlash, "Qiziq tomoni". Har caption boshqacha ochiladi.
- Oxirida imzo: `Doktor H₂O · Javohir`.
- Tekshirish: `python3 .claude/skills/ig-caption/caption.py caption.txt --keywords suv` (hashtag, birinchi qator uzunligi). "ONE ASK" ogohlantirishiga e'tibor berma: o'zbekcha CTA'ni tanimaydi.

## O'zbek tiliga moslash

Paket skriptlari ingliz matni uchun yozilgan (`[A-Za-z]` regex, inglizcha slop ro'yxati).
O'zbek matnida ularning ballari ishonchsiz — shuning uchun qoidalar qo'lda qo'llanadi,
skriptlar faqat struktura tekshiruvi (uzunlik, beat vaqti, hashtag soni) uchun ishlatiladi.
Paket kodi o'zgartirilmagan.

## Pipeline

Video yig'ish: `reels/<sana>/src/*.py` (Pillow kadrlar → ffmpeg), faster-whisper small bilan
so'z vaqtlari, loudnorm oldidan `apad`. Har bir yangi reel — yangi vizual uslub.
Post: Buffer, faqat foydalanuvchi aytganda; cover — oxirgi 0.5 s kadr + thumbnailOffset.

## Video effektlar (`.claude/skills/effects`)

Javohir kadrda gapirgan klipga (ayniqsa intro, birinchi 3 s) qo'llanadi. Yuzni kuzatadi, matnni boshning orqasiga qo'yadi.
Brendga mos (yorug' fon, jiddiy uslub):
- Intro hook: `locked-on`, `lean-in` (bitta so'zda punch-in), `slow-push`, `backdrop-word` (color=84D2FD, o'zbekcha kalit so'z), `headline-box`, `split-headline`, `dot-reveal`.
- Yangilik / manba: `match-cut` (yangilik sahifalari, manba ekranda), `broll-split`.
- Raqamlar: `liquid-glass-graph` (faqat manbadagi real raqam), `countdown-flip`.
- Ro'yxat / layfhak: `apple-toggles`, `checklist`, `todo`.
Ishlatilmaydi: `spotlight`, `glitter-spotlight`, `led-sign`, `moody`, `timeline`, `red-collage` (qorong'i fon); `scribble`, `tier-list`, `uninstall`, `shortcut-rain` (bolabop / mavzuga mos emas); Instagram UI taqlidi (`comment-box`, `tap`, `reel-frame`).
Effekt oynasi 1,5-4 s; avval `--still` bilan tekshirish kadri, keyin render. Subtitr effektdan keyin ustidan qo'shiladi.
