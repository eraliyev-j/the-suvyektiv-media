# Montaj uslubim — Guidance Book (Doktor H₂O · @suvyektiv)

> Bu qoidalar 05.11 "5 ta suv tejash layfhagi" reel'idan olingan. Namuna: `reels/2026-11-05-layfhak/` (script.md, src/hack.py, reel.mp4). Biror qoida yetishmasa, Claude standart qiymatni ishlatadi va qaysilarini ishlatganini aytadi.

## 0. Umumiy
- Platforma: Instagram Reels (asosiy), YouTube Shorts, LinkedIn — bitta video uchalasiga
- Format: 9:16, 1080x1920 · FPS: 30
- Davomiylik: 55–70 soniya
- Til: o'zbekcha (lotin)
- Tasdiqlash: render qilishdan oldin rejani ko'rsat (sahnalar, vaqtlar, matn)
- Mavzu: suv — tejash, tozalash, sifat, faktlar; har raqam manbasi bilan (US EPA, BMT, FAO, stat.uz)

## 1. Hook (birinchi 1–3 soniya)
- 0–0.5 s: cover rasmi to'liq ekranda (`cover.jpg`, 1080x1920), keyin videoga o'tadi
- Keyin katta matn: asosiy raqam yoki va'da ("5 ta layfhak", "26 000 litr")
- Ovoz savol yoki va'da bilan boshlanadi: "Bilasizmi? ...", "Videoni oxirida ... hayratda qoldiradi"
- Taqiqlangan: salomlashish, "bugun men sizga..." kabi uzun kirish

## 2. Kesish va sahnalar
- Har bir fikr = bitta sahna = bitta real video (Pixabay va h.k.)
- Sahna chegaralari ovozdagi pauzalarga moslanadi (silencedetect, -30 dB, 0.3 s+); ovoz kesilmaydi
- Sahna uzunligi: 6–12 s; matn tezligi 18 belgi/soniyadan oshmasin
- Kamera: har kadrda sekin zoom-in (+4% video, +6% rasm)
- O'tishlar: ro'yxat bandlari orasida slideleft 0.3 s; oxirgi sahnalarda fade 0.3 s
- Boshida fade-in 0.3 s, oxirida fade-out 0.6 s
- Klip qisqa bo'lsa: muzlatma emas, sekinlashtir (25% gacha)

## 3. Subtitr
- Subtitr: ha, kuydirilgan (burned-in), ovoz matni bilan bir xil
- Shrift: Inter Bold · O'lcham: 64
- Rang: oq, kontur: qora 3 px + yumshoq soya
- Urg'u so'z rangi: moviy #84D2FD — raqamlar, %, litr va mavzuning kalit so'zlari
- Joylashuv: markazdan biroz pastda (y ≈ 1180 / 1920)
- Bir bo'lakda: 24 belgigacha, jumla bo'yicha bo'linadi
- Katta harf: oddiy (HAMMASI KATTA emas)

## 4. Grafika va ranglar
- Brend ranglari: navy #0B1F33, moviy #84D2FD, to'q moviy #1F6FB2, oq; ogohlantirish #FF785F, ijobiy #5ADC96
- Sarlavhalar: Inter Black / ExtraBold; raqam belgisi "#1"…"#5" katta, moviy
- Panellar: yarim shaffof navy, yumaloq burchak
- Raqamli mavzuda: doimiy hisoblagich (masalan "TEJALDI · yiliga") va to'lib boruvchi indikator
- Video ranglari: tabiiy, to'yinganlik 0.95, kontrast 1.04
- Matn o'qilishi uchun tepada va pastda qorong'i gradient
- Manba satri: kichik, Inter Medium 26, "Manba: ... · hisob: Doktor H₂O"

## 5. Musiqa va ovoz
- Ovoz: o'z ovozim (`voice.m4a`); highpass 80 Hz, kompressor 3:1
- Yakuniy balandlik: -14 LUFS, true peak -1.5 dB
- Fon musiqasi: o'zimiz generatsiya qilamiz (`music.py`, sample'siz)
- Musiqa darajasi: ovozdan ~18 dB past, gapirganda yana pasayadi (sidechain ducking)
- Oxirida: musiqa 1.5 soniyada so'nadi
- Effekt tovushlar: kerak bo'lsa yengil "whoosh"/"pop", har sahnada emas

## 6. Yakun
- Oxirgi sahna (CTA): "Suvni qadrlang!" + "izohlarda yozib qoldiring ↓" + "suv haqida suvyektiv fikrlaymiz!" + "Doktor H₂O · @suvyektiv"
- Fayl nomi: YYYY-MM-DD-mavzu_vN.mp4 (har qayta renderda N oshadi, eski versiya o'chirilmaydi)
- Cover: alohida `..._cover.jpg` + videoga thumbnail sifatida joylanadi
- Saqlash joyi: exports/; repoga `reels/YYYY-MM-DD-mavzu/reel.mp4` + `cover.jpg`
- Buffer: Instagram (Reel), YouTube (Short), LinkedIn — avval draft, keyin men tasdiqlayman

## 7. Qo'shimcha qoidalarim
- Raqamlarni manbadan tekshir; o'zimiz hisoblaganini "hisob: Doktor H₂O" deb belgila
- Manba video va ovoz fayllarini hech qachon o'zgartirma yoki o'chirma
- Hech narsani o'zim tasdiqlamagunimcha e'lon qilma yoki rejalashtirma
