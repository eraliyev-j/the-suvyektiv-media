import json, sys, html, pathlib, os
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
slides = json.loads((ROOT / sys.argv[1]).read_text(encoding="utf-8"))
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
F = ROOT / "node_modules/@fontsource"

def ff(family, path, weight):
    return f"@font-face{{font-family:'{family}';src:url('file://{path}') format('woff2');font-weight:{weight};}}"

fonts = "".join([
    ff("Manrope", F/"manrope/files/manrope-latin-800-normal.woff2", 800),
    ff("ManropeX", F/"manrope/files/manrope-latin-ext-800-normal.woff2", 800),
    ff("Inter", F/"inter/files/inter-latin-400-normal.woff2", 400),
    ff("Inter", F/"inter/files/inter-latin-600-normal.woff2", 600),
    ff("InterX", F/"inter/files/inter-latin-ext-400-normal.woff2", 400),
    ff("InterX", F/"inter/files/inter-latin-ext-600-normal.woff2", 600),
])

DROP = '<svg width="34" height="42" viewBox="0 0 34 42"><path d="M17 2C17 2 3 18 3 27a14 14 0 0 0 28 0C31 18 17 2 17 2Z" fill="none" stroke="currentColor" stroke-width="3"/></svg>'
RIPPLE = '<svg class="ripple" width="760" height="760" viewBox="0 0 760 760">' + "".join(
    f'<circle cx="380" cy="380" r="{r}" fill="none" stroke="currentColor" stroke-width="2" opacity="{o}"/>'
    for r, o in [(90, .55), (170, .4), (250, .28), (330, .18), (378, .1)]) + '</svg>'

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px}
body{font-family:Inter,InterX,sans-serif;-webkit-font-smoothing:antialiased}
.s{position:relative;width:1080px;height:1350px;padding:96px 104px;display:flex;flex-direction:column;overflow:hidden}
.light{background:#F7F8FA;color:#0B1F33}
.dark{background:#0B1F33;color:#FFFFFF}
.top{display:flex;justify-content:space-between;align-items:center;font-size:28px;font-weight:600;letter-spacing:.02em}
.brand{display:flex;align-items:center;gap:16px;color:#2F80ED}
.dark .brand{color:#6FA8F5}
.brand span{color:inherit}.brand .sep{opacity:.45;margin:0 2px}.brand .who{font-weight:600}
.brand sub{font-size:.7em;vertical-align:-.15em;line-height:0}
.count{opacity:.55;font-variant-numeric:tabular-nums}
.main{flex:1;display:flex;flex-direction:column;justify-content:center}
.kicker{font-size:30px;font-weight:600;text-transform:uppercase;letter-spacing:.12em;color:#2F80ED;margin-bottom:36px}
.dark .kicker{color:#6FA8F5}
h1{font-family:Manrope,ManropeX,sans-serif;font-weight:800;font-size:76px;line-height:1.08;letter-spacing:-.02em}
.hook h1{font-size:92px}
.accent{font-family:Manrope,ManropeX,sans-serif;font-weight:800;font-size:76px;line-height:1.1;letter-spacing:-.02em;color:#6FA8F5;margin-top:28px}
.rule{width:96px;height:6px;background:#2F80ED;border-radius:3px;margin:48px 0 44px}
.body p{font-size:42px;line-height:1.38;margin-bottom:30px;max-width:860px}
.body p:last-child{margin-bottom:0}
.steps{list-style:none;margin-top:4px}
.steps li{display:flex;align-items:center;gap:32px;font-size:42px;line-height:1.3;margin-bottom:34px}
.steps .n{flex:none;width:72px;height:72px;border-radius:50%;border:4px solid #2F80ED;color:#2F80ED;display:flex;align-items:center;justify-content:center;font-family:Manrope,ManropeX;font-weight:800;font-size:34px}
.note{margin-top:20px;padding:26px 32px;border-left:6px solid #2F80ED;background:#EAF2FD;font-size:34px;line-height:1.35}
.foot{display:flex;justify-content:space-between;align-items:center;font-size:26px;padding-top:32px;border-top:2px solid currentColor;opacity:.6}
.dark .foot{opacity:.55}
.ripple{position:absolute;right:-330px;bottom:-330px;color:#2F80ED;opacity:.7;pointer-events:none}.bg{position:absolute;inset:0;pointer-events:none}.top,.main,.foot{position:relative;z-index:1}
.handle{font-family:Manrope,ManropeX;font-weight:800;font-size:46px;color:#6FA8F5;margin-top:56px}
.swipe{margin-top:64px;font-size:30px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;opacity:.7}
"""


import math
def _wave(y0, amp, lam, ph, w=1080, step=12, tilt=0.0):
    pts=[]
    for x in range(-40, w+41, step):
        y=y0+amp*math.sin(2*math.pi*x/lam+ph)+0.35*amp*math.sin(2*math.pi*x/(lam*0.47)+ph*1.7)+tilt*x
        pts.append(f"{x},{y:.1f}")
    return "M"+" L".join(pts)
def _silk(n, y0, gap, amp, lam, ph0, dph, color, op0, op1, width=2, tilt=0.0):
    out=[]
    for j in range(n):
        t=j/max(n-1,1)
        op=op0+(op1-op0)*t
        out.append(f'<path d="{_wave(y0+j*gap, amp*(1+0.6*t), lam, ph0+j*dph, tilt=tilt)}" fill="none" stroke="{color}" stroke-width="{width}" opacity="{op:.3f}"/>')
    return "".join(out)
def _fill(y0, amp, lam, ph, color, op, tilt=0.0):
    return f'<path d="{_wave(y0, amp, lam, ph, tilt=tilt)} L1120,1400 L-40,1400 Z" fill="{color}" opacity="{op}"/>'
GRAIN = ('<filter id="g"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>'
         '<feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .55 0"/></filter>'
         '<rect width="1080" height="1350" filter="url(#g)" opacity=".06"/>')

import random
def _drops(theme, idx):
    rnd = random.Random(1000 + idx * 7)
    edge = "#1F3A80" if theme == "dark" else "#1F6FB2"
    defs = ('<defs>'
      f'<radialGradient id="db" cx="62%" cy="70%" r="65%"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".55"/>'
      f'<stop offset=".55" stop-color="#FFFFFF" stop-opacity=".10"/><stop offset=".85" stop-color="{edge}" stop-opacity=".18"/>'
      f'<stop offset="1" stop-color="{edge}" stop-opacity=".42"/></radialGradient>'
      '<filter id="ds" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>'
      '</defs>')
    zones = [  # (x0,x1,y0,y1,count,rmin,rmax)
      (640, 1070, 10, 235, 7, 10, 34),
      (990, 1075, 235, 1190, 8, 8, 26),
      (0, 85, 160, 1250, 5, 6, 20),
      (30, 1060, 1300, 1345, 6, 5, 14),
      (0, 1080, 0, 1350, 26, 2.5, 6),   # fine mist everywhere
    ]
    out = []
    placed = []
    for x0, x1, y0, y1, cnt, rmin, rmax in zones:
        tries = 0
        while cnt > 0 and tries < 400:
            tries += 1
            r = rmin + (rmax - rmin) * rnd.random() ** 1.8
            x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
            if any((x-a)**2 + (y-b)**2 < (r + c + 6)**2 for a, b, c in placed):
                continue
            if r > 6 and ((860 - r < x < 1080 and 30 - r < y < 160 + r) or (x < 600 + r and y < 150 + r)):
                continue  # keep the brand and slide counter clear
            placed.append((x, y, r)); cnt -= 1
            ry = r * (1.06 + 0.1 * rnd.random())
            sh_op = .22 if theme == "dark" else .14
            if r > 18 and rnd.random() < .45:   # sliding drop with a thin trail
                tl = r * rnd.uniform(2.5, 5)
                out.append(f'<path d="M{x:.1f},{y-ry:.1f} C{x-r*.25:.1f},{y-ry-tl*.5:.1f} {x+r*.2:.1f},{y-ry-tl*.8:.1f} {x:.1f},{y-ry-tl:.1f}" '
                           f'stroke="#FFFFFF" stroke-opacity=".35" stroke-width="{r*.28:.1f}" stroke-linecap="round" fill="none"/>')
            out.append(f'<ellipse cx="{x+r*.18:.1f}" cy="{y+r*.28:.1f}" rx="{r:.1f}" ry="{ry:.1f}" fill="{edge}" opacity="{sh_op}" filter="url(#ds)"/>')
            out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r:.1f}" ry="{ry:.1f}" fill="url(#db)"/>')
            out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r:.1f}" ry="{ry:.1f}" fill="none" stroke="{edge}" stroke-opacity=".22" stroke-width="{max(1,r*.06):.1f}"/>')
            out.append(f'<ellipse cx="{x-r*.35:.1f}" cy="{y-ry*.42:.1f}" rx="{r*.28:.1f}" ry="{r*.16:.1f}" fill="#FFFFFF" opacity=".9" transform="rotate(-35 {x-r*.35:.1f} {y-ry*.42:.1f})"/>')
            if r > 9:
                out.append(f'<ellipse cx="{x+r*.38:.1f}" cy="{y+ry*.5:.1f}" rx="{r*.12:.1f}" ry="{r*.07:.1f}" fill="#FFFFFF" opacity=".6"/>')
    return defs + "".join(out)

def premium_bg(theme, idx):
    ph = idx*0.9
    if theme == "dark":
        body = (
          '<defs><radialGradient id="gl" cx="18%" cy="8%" r="90%"><stop offset="0" stop-color="#C4ECFF"/>'
          '<stop offset=".45" stop-color="#84D2FD"/><stop offset="1" stop-color="#57B7F2"/></radialGradient>'
          '<linearGradient id="sh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".0"/>'
          '<stop offset="1" stop-color="#1F3A80" stop-opacity=".16"/></linearGradient></defs>'
          '<rect width="1080" height="1350" fill="url(#gl)"/>'
          + _silk(20, 820, 21, 50, 1500, ph, 0.13, "#FFFFFF", .15, .80, 2.4, tilt=-0.06)
          + _fill(1150, 34, 1300, ph+1.0, "#FFFFFF", .16, tilt=-0.05)
          + _fill(1215, 28, 900, ph+2.4, "#FFFFFF", .14)
          + '<rect y="900" width="1080" height="450" fill="url(#sh)"/>'
          + '<ellipse cx="900" cy="170" rx="420" ry="190" fill="#FFFFFF" opacity=".10" transform="rotate(-18 900 170)"/>'
        )
    else:
        body = (
          '<defs><linearGradient id="gl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F7FCFF"/>'
          '<stop offset="1" stop-color="#E1F3FE"/></linearGradient></defs>'
          '<rect width="1080" height="1350" fill="url(#gl)"/>'
          + _silk(18, -70, 17, 44, 1400, ph, 0.12, "#1F6FB2", .05, .20, 1.8, tilt=0.11)
          + _fill(1225, 22, 1200, ph+0.6, "#BFE6FD", .45, tilt=-0.03)
          + _fill(1262, 18, 800, ph+2.0, "#9ED7FA", .30)
        )
    return f'<svg class="bg" width="1080" height="1350" viewBox="0 0 1080 1350">{body}{_drops(theme, idx)}{GRAIN}</svg>'

e = html.escape
# Branding (2026-10-21: Instagram and YouTube share one look — Doktor H2O / @suvyektiv, sky theme).
BRAND = os.environ.get("BRAND", "Doktor H<sub>2</sub>O <span class=\"sep\">|</span> <span class=\"who\">Javohir Eraliyev</span>")  # 2026-11-11: name added  # raw HTML allowed
HANDLE = os.environ.get("HANDLE", "@suvyektiv")
TAGLINE = os.environ.get("TAGLINE", "Suv haqida, oddiy tilda.")
# THEME=sky: Doktor H2O palette, taken from the YouTube avatar (sky-blue #84D2FD bg, navy "Dr. H2O" text)
THEME_CSS = {"sky": """
.dark{background:#84D2FD;color:#0B1F33}
.dark .brand,.dark .kicker,.dark .handle,.accent{color:#1F3A80}
.ripple{color:#FFFFFF;opacity:.55}
.light{background:#EDF8FF;color:#0B1F33}
.light .brand,.light .kicker{color:#1F6FB2}
.rule{background:#1F6FB2}
.steps .n{border-color:#1F6FB2;color:#1F6FB2}
.note{border-left-color:#1F6FB2;background:#D6EFFE}
.dark .foot{opacity:.7}
"""}.get(os.environ.get("THEME", "sky"), "")
n = len(slides)
for i, s in enumerate(slides, 1):
    k = s["kind"]
    parts = []
    if s.get("kicker"): parts.append(f'<div class="kicker">{e(s["kicker"])}</div>')
    parts.append(f'<h1>{e(s["title"])}</h1>')
    if s.get("accent"): parts.append(f'<div class="accent">{e(s["accent"])}</div>')
    if k in ("body", "steps"): parts.append('<div class="rule"></div>')
    if k == "body":
        parts.append('<div class="body">' + "".join(f"<p>{e(p)}</p>" for p in s["body"]) + "</div>")
    if k == "steps":
        parts.append('<ol class="steps">' + "".join(f'<li><span class="n">{j}</span><span>{e(t)}</span></li>' for j, t in enumerate(s["steps"], 1)) + "</ol>")
        if s.get("note"): parts.append(f'<div class="note">{e(s["note"])}</div>')
    if k == "hook": parts.append(f'<div class="swipe">{e(os.environ.get("SWIPE", "Varaqlang →"))}</div>')
    if k == "cta": parts.append(f'<div class="handle">{e(HANDLE if "HANDLE" in os.environ else s["handle"])}</div>')
    # BG=premium (default since 2026-11-11): gradient + flowing silk-wave lines + grain; BG=ripple: old circles
    ripple = premium_bg(s["theme"], i) if os.environ.get("BG", "premium") == "premium" else (RIPPLE if s["theme"] == "dark" else "")
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>{fonts}{CSS}{THEME_CSS}</style></head>
<body><div class="s {s['theme']} {k}">{ripple}
<div class="top"><div class="brand">{DROP}<span>{BRAND}</span></div><div class="count">{i}/{n}</div></div>
<div class="main">{''.join(parts)}</div>
<div class="foot"><span>{e(HANDLE)}</span><span>{e(TAGLINE)}</span></div>
</div></body></html>"""
    p = ROOT / f"_slide{i}.html"; p.write_text(doc, encoding="utf-8")

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    for i in range(1, n + 1):
        pg.goto(f"file://{ROOT}/_slide{i}.html"); pg.wait_for_load_state("networkidle")
        pg.evaluate("document.fonts.ready")
        over = pg.evaluate("(() => {const m=document.querySelector('.main');return m.scrollHeight>m.clientHeight+2})()")
        pg.screenshot(path=str(out / f"{i:02d}.png"))
        print(i, "OVERFLOW" if over else "ok")
    b.close()
