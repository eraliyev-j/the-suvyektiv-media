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

## Reel uchun majburiy qoidalar (ig-reel'dan)

1. Hook 3 ta variantda yoziladi, eng kuchlisi tanlanadi; hook birinchi 3 soniyada tugaydi.
2. Har bir beat ≤ 4 s; ekrandagi bitta karta ≤ 6 so'z.
3. Safe zone: matn y 230–1440, o'ngdan 230 px bo'sh (IG tugmalari). Subtitr y≈1180.
4. Oxiri hookka qaytadi (loop echo), keyin brend CTA.
5. Raqamlar faqat manbadan; manba ekranda.

## Caption qoidalari (ig-caption'dan)

- Birinchi 125 belgi — asosiy fikr (ko'rinadigan qism), qidiruv so'zlari matn ichida.
- Bitta so'rov (CTA) — bizda: izohda savol yozish.
- **Hashtag ≤ 5** (Instagram 2025-12-18 dan cheklagan). Captionda havola yo'q.
- Em-dash (—), "AI so'zlari" va ko'rinmas belgilarni olib tashlash (ig-human).

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
