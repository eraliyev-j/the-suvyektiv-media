"""Reel B cover: real Salar filter photo + big hook text; text and photo inside the 3:4 grid crop (y 240-1680).
usage: python3 cover_b.py out.jpg"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from broll_b import fn, kb, pane, board, W, H, WHITE, SKY, SKYD, NAVY, NAVY2, WARN
from PIL import Image, ImageDraw
im = board(); d = ImageDraw.Draw(im)
pane(im, kb("filter", 960, 700, 0, 1.05, 1.05, 0.5, 0.45), 60, 900, 1, "Toshkent sh. hokimligi / Gazeta.uz")
d.text((70, 290), "Salar hidiga", font=fn("Black", 92), fill=NAVY + (255,))
f = fn("Black", 190)
d.text((60, 390), "9,5", font=f, fill=NAVY + (255,))
d.text((80 + d.textlength("9,5", font=f) + 10, 470), "mlrd so'm", font=fn("Black", 84), fill=SKYD + (255,))
f2 = fn("Black", 84); s = "Hid ketdi. Suv-chi?"
d.rounded_rectangle([56, 640, 64 + d.textlength(s, font=f2) + 30, 760], 24, fill=NAVY + (255,))
d.text((78, 654), s, font=f2, fill=WHITE + (255,))
d.rounded_rectangle([60, 1660, 640, 1740], 22, fill=NAVY + (240,))
d.text((86, 1676), "Doktor H₂O · @suvyektiv", font=fn("Bold", 38), fill=WHITE + (255,))
im.convert("RGB").save(sys.argv[1], quality=94)
