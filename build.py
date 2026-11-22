"""Saturday Finale - 21 November 2026 front page.
Draws one 1024x1024 newspaper front page with Pillow.
Build-time only: the shipped program (main.py) is a stdlib copier.
Run: python3 build.py  -> writes entry.png next to this file.
"""
import os, json
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
S = 2                      # supersampling factor
W = H = 1024
img = Image.new("RGB", (W * S, H * S), "#F6F1E7")
d = ImageDraw.Draw(img)

def font(name, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", name + ".ttf"), int(round(size * S)))

HEAD = lambda s: font("Newsreader-SemiBold", s)
SERIF = lambda s: font("SourceSerif4-Regular", s)
SERIFB = lambda s: font("SourceSerif4-SemiBold", s)
SANS = lambda s: font("Inter-Regular", s)
SANSB = lambda s: font("Inter-SemiBold", s)
COND = lambda s: font("BarlowCondensed-SemiBold", s)

INK = "#1A1A1A"; GREY = "#555049"; RULE = "#CFC6B4"; PAPER = "#F6F1E7"; CARD = "#FFFDF8"
RED = "#B3261E"
REG = {"ME": ("Middle East", "#B3261E"), "EU": ("Europe", "#2B5BA8"), "AS": ("Asia", "#B7791F"),
       "AF": ("Africa", "#2F7D4F"), "NA": ("N. America", "#0E7C7B"), "LA": ("Lat. America", "#7B2F8E"),
       "OC": ("Oceania", "#1F4E79"), "GL": ("Global", "#333333")}
SHORTN = {"ME": "Middle East", "EU": "Europe", "AS": "Asia", "AF": "Africa", "NA": "N. America",
          "LA": "Lat. America", "OC": "Oceania", "GL": "Global"}
BADGE = {"CONFIRMED": "#2F7D4F", "OFFICIAL": "#2B5BA8", "CLAIM": "#B3261E", "REPORTED": "#6E6A62"}

def R(v):
    return int(round(v * S))

def box(x0, y0, x1, y1, **kw):
    if "width" in kw:
        kw["width"] = max(1, R(kw["width"]))
    d.rectangle([R(x0), R(y0), R(x1), R(y1)], **kw)

def poly(pts, **kw):
    if "width" in kw:
        kw["width"] = max(1, R(kw["width"]))
    d.polygon([(R(x), R(y)) for x, y in pts], **kw)

def line(pts, fill, w):
    d.line([(R(x), R(y)) for x, y in pts], fill=fill, width=R(w), joint="curve")

def ell(x0, y0, x1, y1, **kw):
    if "width" in kw:
        kw["width"] = max(1, R(kw["width"]))
    d.ellipse([R(x0), R(y0), R(x1), R(y1)], **kw)

def T(x, y, s, f, fill=INK, anchor="la"):
    d.text((R(x), R(y)), s, font=f, fill=fill, anchor=anchor)

def tw(s, f):
    return d.textlength(s, font=f) / S

def wrap(s, f, width):
    words = s.split()
    lines = []
    cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, f) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def fit(s, maker, size, width, maxlines, minsize):
    sz = size
    while sz > minsize:
        f = maker(sz)
        ls = wrap(s, f, width)
        if len(ls) <= maxlines:
            return f, ls, sz
        sz -= 0.5
    f = maker(minsize)
    return f, wrap(s, f, width), minsize

def para(x, y, lines, f, lh, fill=INK):
    for i, s in enumerate(lines):
        T(x, y + i * lh, s, f, fill)
    return y + len(lines) * lh

def badge(x, y, kind, size=8):
    f = SANSB(size)
    w = tw(kind, f) + 12
    box(x, y, x + w, y + size + 7, fill=BADGE[kind])
    T(x + 6, y + 1.5, kind, f, "white")
    return w

# ------------------------------------------------------------------ art
# Each art function draws inside the box (x, y, w, h) in page points.

def art_tankers(x, y, w, h):
    box(x, y, x + w, y + h, fill="#7FA8C9")
    box(x, y + h * 0.62, x + w, y + h, fill="#2B5BA8")
    for k in range(3):
        line([(x + 12 + k * 60, y + h * 0.72), (x + 44 + k * 60, y + h * 0.72)], "white", 1.5)
    poly([(x + 18, y + h * 0.62), (x + 30, y + h * 0.30), (x + 120, y + h * 0.30),
          (x + 132, y + h * 0.62)], fill="#3A3F47")
    box(x + 52, y + h * 0.14, x + 66, y + h * 0.30, fill="#3A3F47")
    box(x + 150, y + h * 0.62, x + 240, y + h * 0.72, fill="#22252B")
    box(x + 168, y + h * 0.46, x + 178, y + h * 0.62, fill="#22252B")
    for (cx, cy, r, c) in [(200, y + h * 0.30, 16, "#F08A24"), (212, y + h * 0.22, 11, "#FFD34D"),
                           (190, y + h * 0.24, 8, "#FFD34D")]:
        ell(cx - r, cy - r, cx + r, cy + r, fill=c)
    T(x + w - 10, y + 8, "2 HIT", HEAD(20), "white", "ra")

def art_cop(x, y, w, h):
    box(x, y, x + w, y + h, fill="#BFE0EE")
    ell(x + w * 0.32, y + h * 0.10, x + w * 0.68, y + h * 0.90, fill="#3E8A4F", outline="white", width=2)
    poly([(x + w * 0.40, y + h * 0.30), (x + w * 0.52, y + h * 0.22), (x + w * 0.58, y + h * 0.42),
          (x + w * 0.44, y + h * 0.48)], fill="#7BC47F")
    poly([(x + w * 0.48, y + h * 0.62), (x + w * 0.62, y + h * 0.55), (x + w * 0.60, y + h * 0.78),
          (x + w * 0.46, y + h * 0.80)], fill="#7BC47F")
    T(x + 10, y + h - 26, "COP31", HEAD(22), INK, "la")

def art_mexico(x, y, w, h):
    box(x, y, x + w, y + h, fill="#1F2A44")
    cx, cy = x + w / 2, y + h / 2
    pts = []
    import math
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        r = 38 if k % 2 == 0 else 16
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    poly(pts, fill="#F2B705", outline="white", width=1.5)
    ell(cx - 11, cy - 11, cx + 11, cy + 11, fill="#1F2A44")
    T(cx, cy, "$", SANSB(16), "#F2B705", "mm")
    T(x + w - 8, y + 6, "SEIZED", SANSB(11), "white", "ra")

def art_quake(x, y, w, h):
    box(x, y, x + w, y + h, fill="#E8DCC4")
    poly([(x, y + h), (x + w * 0.25, y + h * 0.45), (x + w * 0.45, y + h * 0.62),
          (x + w * 0.65, y + h * 0.38), (x + w, y + h * 0.55), (x + w, y + h)], fill="#8A6D4B")
    line([(x + 8, y + h * 0.42), (x + 40, y + h * 0.34), (x + 70, y + h * 0.56),
          (x + 100, y + h * 0.28), (x + 140, y + h * 0.50), (x + 180, y + h * 0.36)],
         RED, 2.5)

def art_finland(x, y, w, h):
    box(x, y, x + w, y + h, fill="#9FC3D8")
    box(x, y + h * 0.66, x + w, y + h, fill="#2B5BA8")
    poly([(x + 22, y + h * 0.66), (x + 34, y + h * 0.36), (x + 150, y + h * 0.36),
          (x + 162, y + h * 0.66)], fill="#3A3F47")
    box(x + 60, y + h * 0.20, x + 74, y + h * 0.36, fill="#3A3F47")
    poly([(x + 108, y + h * 0.42), (x + 122, y + h * 0.08), (x + 136, y + h * 0.42)], fill="#F08A24")
    poly([(x + 116, y + h * 0.42), (x + 124, y + h * 0.20), (x + 132, y + h * 0.42)], fill="#FFD34D")
    T(x + 10, y + 6, "16 SAFE", SANSB(11), INK, "la")

def art_basra(x, y, w, h):
    box(x, y, x + w, y + h, fill="#E9C9A8")
    box(x + 30, y + h * 0.42, x + 130, y + h, fill="#5A4632")
    for k in range(3):
        box(x + 42 + k * 30, y + h * 0.52, x + 58 + k * 30, y + h * 0.66, fill="#FFD34D")
    box(x + 150, y + h * 0.30, x + 162, y + h, fill="#5A4632")
    poly([(x + 140, y + h * 0.34), (x + 156, y + h * 0.02), (x + 172, y + h * 0.34)], fill="#F08A24")
    poly([(x + 148, y + h * 0.34), (x + 156, y + h * 0.14), (x + 164, y + h * 0.34)], fill="#FFD34D")
    T(x + 10, y + 6, "4 DEAD", SANSB(11), RED, "la")

def art_trade(x, y, w, h):
    box(x, y, x + w, y + h, fill="#DCE8F5")
    box(x + 18, y + h * 0.18, x + 78, y + h * 0.62, fill="#2B5BA8")
    for k in range(6):
        import math
        ang = k * math.pi / 3
        ell(x + 48 + 14 * math.cos(ang) - 2, y + h * 0.40 + 12 * math.sin(ang) - 2,
            x + 48 + 14 * math.cos(ang) + 2, y + h * 0.40 + 12 * math.sin(ang) + 2, fill="#FFD34D")
    box(x + 108, y + h * 0.18, x + 168, y + h * 0.40, fill="#C8102E")
    box(x + 108, y + h * 0.40, x + 168, y + h * 0.62, fill="white")
    line([(x + 78, y + h * 0.40), (x + 108, y + h * 0.40)], "#1A1A1A", 2)

def art_drone(x, y, w, h):
    box(x, y, x + w, y + h, fill="#C9DCE6")
    cx, cy = x + w / 2, y + h * 0.52
    line([(cx - 34, cy - 14), (cx + 34, cy + 14)], "#333333", 2)
    line([(cx - 34, cy + 14), (cx + 34, cy - 14)], "#333333", 2)
    ell(cx - 26, cy - 26, cx + 26, cy + 26, fill="#3A3F47")
    ell(cx - 10, cy - 6, cx + 10, cy + 6, fill="#F08A24")
    for (rx, ry) in [(cx - 34, cy - 14), (cx + 34, cy - 14), (cx - 34, cy + 14), (cx + 34, cy + 14)]:
        ell(rx - 8, ry - 3, rx + 8, ry + 3, outline="#333333", width=1.5)
    T(x + 10, y + 6, "MQ-9", SANSB(12), INK, "la")

def art_riyadh(x, y, w, h):
    box(x, y, x + w, y + h, fill="#F5D9A8")
    for (bx, bw, bh) in [(14, 26, 52), (48, 20, 70), (76, 30, 44), (114, 22, 62), (144, 26, 38)]:
        box(x + bx, y + h - bh, x + bx + bw, y + h, fill="#5A4632")
    line([(x + 20, y + h * 0.55), (x + 90, y + h * 0.18), (x + 150, y + h * 0.42)], RED, 2)
    poly([(x + 84, y + h * 0.10), (x + 90, y + h * 0.20), (x + 96, y + h * 0.10)], fill="#FFD34D")
    T(x + 10, y + 6, "3 DOWN", SANSB(11), RED, "la")

def art_taiwan(x, y, w, h):
    box(x, y, x + w, y + h, fill="#FBEDEA")
    line([(x + 14, y + h * 0.20), (x + 14, y + h * 0.82)], INK, 1.5)
    line([(x + 14, y + h * 0.82), (x + w - 12, y + h * 0.82)], INK, 1.5)
    line([(x + 22, y + h * 0.30), (x + 60, y + h * 0.38), (x + 100, y + h * 0.55),
          (x + 140, y + h * 0.66), (x + 172, y + h * 0.76)], RED, 3)
    poly([(x + 172, y + h * 0.76), (x + 158, y + h * 0.70), (x + 162, y + h * 0.86)], fill=RED)
    T(x + w - 8, y + 6, "-17.5%", HEAD(19), RED, "ra")

def art_bitcoin(x, y, w, h):
    box(x, y, x + w, y + h, fill="#FFF3D6")
    cx, cy = x + w / 2, y + h / 2
    ell(cx - 30, cy - 30, cx + 30, cy + 30, fill="#F7931A", outline="#C96A00", width=2)
    T(cx, cy, "B", SANSB(36), "white", "mm")
    line([(x + 12, y + h - 14), (x + 60, y + h - 26), (x + 110, y + h - 18), (x + w - 12, y + h - 30)],
         "#2F7D4F", 2.5)
    T(x + 10, y + 6, "$55,251", SANSB(12), INK, "la")

def art_rugby(x, y, w, h):
    box(x, y, x + w, y + h, fill="#3E8A4F")
    for k in range(4):
        line([(x + 12 + k * 48, y + h), (x + 30 + k * 44, y)], "#5BA36A", 1)
    line([(x + 24, y + 8), (x + 24, y + h - 6)], "white", 2.5)
    line([(x + 46, y + 8), (x + 46, y + h - 6)], "white", 2.5)
    ell(x + w - 60, y + h * 0.30, x + w - 20, y + h * 0.70, fill="#8A5A2B", outline="white", width=1.5)
    line([(x + w - 52, y + h * 0.50), (x + w - 28, y + h * 0.50)], "white", 1.5)
    T(x + 10, y + 6, "37-12", HEAD(18), "white", "la")

def art_cricket(x, y, w, h):
    box(x, y, x + w, y + h, fill="#CFE3C3")
    poly([(x + 20, y + h - 6), (x + 64, y + 10), (x + 72, y + 13), (x + 30, y + h - 2)], fill="#C9A066")
    line([(x + 88, y + 12), (x + 96, y + h - 18)], "#8A5A2B", 3)
    ell(x + 100, y + h - 26, x + 114, y + h - 12, fill=RED)
    T(x + w - 8, y + 8, "486-4", HEAD(19), INK, "ra")

ART = {"tankers": art_tankers, "cop": art_cop, "mexico": art_mexico, "quake": art_quake,
       "finland": art_finland, "basra": art_basra, "trade": art_trade, "drone": art_drone,
       "riyadh": art_riyadh, "taiwan": art_taiwan, "bitcoin": art_bitcoin, "rugby": art_rugby,
       "cricket": art_cricket}

# ------------------------------------------------------------------ data
LEADS = [
    (1, "ME", "tankers", "MIDDLE EAST · IRAN WAR", "CONFIRMED",
     "Tankers hit off Oman; Iran claims Bahrain strike",
     "UKMTO: 2 tankers hit off Khasab, no casualties. Bahrain says a civilian site burned; Iran's Guards claim US radars.",
     "REUTERS · AL JAZEERA · UKMTO"),
    (2, "EU", "cop", "TÜRKIYE · CLIMATE", "CONFIRMED",
     "COP31 climate talks run into overtime",
     "Nations still split on fossil fuels; final plenary called for Sunday 06:00 GMT.",
     "REUTERS · AFP"),
    (3, "NA", "mexico", "N. AMERICA · MEXICO", "CONFIRMED",
     "Mexico seizes FBI-listed 'El Chapo Isidro'",
     "Fausto Isidro Meza Flores held in Guasave raid; officials say 11 died.",
     "AP · REUTERS"),
]
CARDS = [
    (4, "LA", "quake", "LATIN AMERICA · QUAKE", "OFFICIAL", "M6.7 quake in Peru: 1 dead, 16 hurt", "USGS · INDECI"),
    (5, "EU", "finland", "EUROPE · FINLAND", "CONFIRMED", "Drones set Russian ship ablaze off Finland", "REUTERS · AFP"),
    (6, "ME", "basra", "MIDDLE EAST · IRAQ", "CONFIRMED", "Fire at Basra power plant kills four", "REUTERS · AL JAZEERA"),
    (7, "AS", "trade", "ASIA · TRADE", "OFFICIAL", "Indonesia and EU sign trade pact", "EU COMMISSION"),
    (8, "ME", "drone", "MIDDLE EAST · HORMUZ", "CLAIM", "Iran says it downed a US MQ-9 drone", "AL JAZEERA"),
    (9, "ME", "riyadh", "MIDDLE EAST · SAUDI", "CLAIM", "Saudis say 3 Houthi missiles intercepted", "REUTERS · AFP"),
    (10, "AS", "taiwan", "ASIA · MARKETS", "OFFICIAL", "Taiwan curbs short-selling after rout", "FOCUS TAIWAN"),
    (11, "GL", "bitcoin", "GLOBAL · CRYPTO", "CONFIRMED", "Bitcoin hits 2-year low, then rebounds", "REUTERS · COINDESK"),
    (12, "EU", "rugby", "EUROPE · RUGBY", "CONFIRMED", "England rout the All Blacks 37-12", "BBC · AP"),
    (13, "OC", "cricket", "OCEANIA · CRICKET", "CONFIRMED", "Rahul's 136 puts India 118 ahead", "ESPNCRICINFO"),
]
LIST = [
    (14, "EU", "France:", "82,500 march over living costs"),
    (15, "ME", "Gaza:", "van strike kills 3; Israel says militants"),
    (16, "ME", "Lebanon:", "Aoun demands Israel withdraw"),
    (17, "ME", "Iran:", "navy says tanker hit a mine"),
    (18, "NA", "US:", "denies Iran hit an F-16"),
    (19, "GL", "UN:", "path to robot-arms pact by 2028"),
    (20, "EU", "EU:", "'good deal or no deal' at COP31"),
    (21, "EU", "NATO:", "will defend 'every inch' of Poland"),
    (22, "EU", "Zagreb:", "protest over a death in a clinic"),
    (23, "EU", "France:", "floods hit 850 homes in north"),
    (24, "AS", "India:", "Pakistan minister at SCO forum"),
    (25, "AS", "Manipur:", "toxic liquor kills 16"),
    (26, "AS", "Japan:", "snow cuts off a Fukushima village"),
    (27, "AS", "Pakistan:", "says 15 militants killed"),
    (28, "AF", "Ethiopia:", "polio drive for 11.3m children"),
    (29, "AF", "CAF:", "all 54 members back Infantino"),
    (30, "NA", "F1:", "Verstappen on Vegas pole"),
    (31, "EU", "Rugby:", "Ireland 20-17 South Africa"),
    (32, "EU", "Rugby:", "Australia 29-26 Wales"),
    (33, "EU", "EPL:", "Newcastle 2-2 Arsenal; Leeds win"),
    (34, "OC", "Cricket:", "Australia beat England in T20"),
    (35, "NA", "NBA:", "Harden's 26th 50-point game"),
]
PINS = {1: (56.2, 26.2), 2: (30.7, 36.9), 3: (-108.5, 25.6), 4: (-76.0, -11.0), 5: (26.5, 60.0),
        6: (47.8, 30.5), 7: (106.8, -6.2), 8: (57.0, 24.2), 9: (46.7, 24.7), 10: (121.5, 25.0),
        12: (-0.1, 51.5), 13: (174.8, -41.3)}
DOTS = {14: (2.3, 48.9), 15: (34.45, 31.5), 16: (35.5, 33.9), 17: (58.0, 25.0), 18: (-77.0, 38.9),
        19: (6.1, 46.2), 20: (4.4, 50.8), 21: (21.0, 52.2), 22: (16.0, 45.8), 23: (2.3, 50.5),
        24: (77.2, 28.6), 25: (93.9, 24.8), 26: (140.0, 37.7), 27: (66.8, 29.8), 28: (38.7, 9.0),
        29: (7.5, 9.1), 30: (-115.1, 36.2), 31: (-6.3, 53.3), 32: (-3.2, 51.5), 33: (-1.6, 55.0),
        34: (145.0, -37.8), 35: (-81.7, 41.5)}
TIMES = [("00:09", "Peru quake hits", "LA"), ("03:00", "Basra plant fire", "ME"),
         ("05:00", "Tankers hit off Oman", "ME"), ("13:30", "Bitcoin rebounds", "GL"),
         ("19:20", "Bahrain site burns", "ME")]
NUMS = [("6.7", "Peru quake (USGS)", "LA"), ("2", "tankers hit off Oman", "ME"),
        ("11", "dead in Sinaloa raid", "NA"), ("82,500", "marched in France", "EU"),
        ("-17.5%", "Taiwan stocks, week", "AS"), ("37-12", "England v New Zealand", "EU")]
DC = [("Kryvyi Rih strike", "Fri 20 Nov"), ("Missiles fall in Poland", "Fri 20 Nov"),
      ("Palisades Fire verdict", "Fri 20 Nov"), ("Denmark expels attaché", "Fri 20 Nov")]

M = 12
# ------------------------------------------------------------------ masthead
kick = [("SATURDAY 21 NOVEMBER 2026", RED),
        ("  ·  THE DAY IN WORLD NEWS  ·  35 STORIES  ·  8 REGIONS  ·  ALL FROM THIS SATURDAY", GREY)]
fk = SANSB(13)
kw = sum(tw(a, fk) for a, _ in kick)
kx = W / 2 - kw / 2
for a, c in kick:
    T(kx, 6, a, fk, c)
    kx += tw(a, fk)
T(W / 2, 58, "SATURDAY FINALE", HEAD(56), INK, "mm")
box(M, 94, W - M, 95.2, fill=INK)

def rowlabel(y, l1, l2):
    T(M, y, l1, SANSB(12), RED)
    T(M, y + 15, l2, SANSB(12), RED)

LBLW = 92
# ------------------------------------------------------------------ world in time
ty = 98
rowlabel(ty + 5, "WORLD IN", "TIME (UTC)")
cw = (W - M - (M + LBLW)) / len(TIMES)
for i, (tm, what, rg) in enumerate(TIMES):
    cx = M + LBLW + cw * i + cw / 2
    if i:
        box(M + LBLW + cw * i, ty + 4, M + LBLW + cw * i + 0.8, ty + 42, fill=RULE)
    T(cx, ty + 12, tm, HEAD(21), REG[rg][1], "mm")
    f, ls, _ = fit(what, SERIFB, 17, cw - 8, 1, 13)
    T(cx, ty + 34, ls[0], f, INK, "mm")
box(M, ty + 48, W - M, ty + 48.8, fill=RULE)
# ------------------------------------------------------------------ world in numbers
ny = ty + 52
rowlabel(ny + 7, "WORLD IN", "NUMBERS")
cw = (W - M - (M + LBLW)) / len(NUMS)
for i, (num, cap, rg) in enumerate(NUMS):
    cx = M + LBLW + cw * i + cw / 2
    if i:
        box(M + LBLW + cw * i, ny + 4, M + LBLW + cw * i + 0.8, ny + 46, fill=RULE)
    T(cx, ny + 15, num, HEAD(31), REG[rg][1], "mm")
    f, ls, _ = fit(cap, SANSB, 14, cw - 6, 1, 10)
    T(cx, ny + 39, ls[0], f, GREY, "mm")
box(M, ny + 52, W - M, ny + 53.2, fill=INK)

# ------------------------------------------------------------------ lead cards
gy = ny + 59
gap = 8
lw = (W - 2 * M - 2 * gap) / 3
ah = 96
LH = 236
LSZ = min(fit(L_[5], HEAD, 30, lw - 18, 2, 22)[2] for L_ in LEADS)
for i, (n, rg, art, kk, bd, head, sub, src) in enumerate(LEADS):
    x = M + i * (lw + gap)
    box(x, gy, x + lw, gy + LH, fill=CARD, outline=RULE, width=0.8)
    box(x, gy, x + lw, gy + 4, fill=REG[rg][1])
    ART[art](x, gy + 4, lw, ah)
    cy = gy + ah + 10
    ell(x + 8, cy, x + 24, cy + 16, fill=REG[rg][1])
    T(x + 16, cy + 8, str(n), SANSB(10), "white", "mm")
    T(x + 30, cy + 2, kk, SANSB(11.5), REG[rg][1])
    f, ls, sz = fit(head, HEAD, LSZ, lw - 18, 2, 22)
    yy = para(x + 9, cy + 18, ls, f, sz * 1.02)
    fs, lss, szs = fit(sub, SANS, 13, lw - 18, 2, 10.5)
    para(x + 9, yy + 4, lss, fs, szs * 1.25, GREY)
    badge(x + 9, gy + LH - 18, bd, 9)
    fsr, lsr, _ = fit(src, SANSB, 10.5, lw - 110, 1, 8)
    T(x + lw - 9, gy + LH - 7, lsr[0], fsr, REG[rg][1], "rd")

# ------------------------------------------------------------------ small cards
sy0 = gy + LH + 8
sg = 7
sw = (W - 2 * M - 4 * sg) / 5
sh = 136
sah = 44
CSZ = min(fit(c[5], HEAD, 19, sw - 12, 3, 15)[2] for c in CARDS)
for k, (n, rg, art, kk, bd, head, src) in enumerate(CARDS):
    r_, c_ = divmod(k, 5)
    x, y = M + c_ * (sw + sg), sy0 + r_ * (sh + sg)
    box(x, y, x + sw, y + sh, fill=CARD, outline=RULE, width=0.8)
    box(x, y, x + sw, y + 3, fill=REG[rg][1])
    ART[art](x, y + 3, sw, sah)
    cy = y + sah + 7
    ell(x + 6, cy, x + 19, cy + 13, fill=REG[rg][1])
    T(x + 12.5, cy + 6.5, str(n), SANSB(8.5), "white", "mm")
    f0, l0, _ = fit(kk, SANSB, 10, sw - 30, 1, 8)
    T(x + 23, cy + 1.5, l0[0], f0, REG[rg][1])
    f, ls, sz = fit(head, HEAD, CSZ, sw - 12, 3, 15)
    para(x + 7, cy + 15, ls, f, sz * 1.0)
    bw_ = badge(x + 7, y + sh - 15, bd, 7.5)
    fsrc, lsrc, _ = fit(src, SANSB, 9, sw - 20 - bw_, 1, 7)
    T(x + sw - 6, y + sh - 5, lsrc[0], fsrc, REG[rg][1], "rd")

# ------------------------------------------------------------------ map + date check (left)
by0 = sy0 + 2 * sh + sg + 6
mx0, my0, mw, mh = M, by0 + 17, 300, 112
box(mx0, my0, mx0 + mw, my0 + mh, fill="#C9DCE6")
LAT0, LAT1 = 72, -50
def proj(lon, lat):
    return (mx0 + (lon + 180) / 360 * mw, my0 + (LAT0 - lat) / (LAT0 - LAT1) * mh)
land = json.load(open(os.path.join(HERE, "data", "land.json")))
for ring in land:
    pts = [proj(lo, max(min(la, LAT0 + 5), LAT1 - 5)) for lo, la in ring]
    if len(pts) > 2:
        poly(pts, fill="#EFE6D2", outline="#A89878")
T(M, by0 + 2, "WHERE IT HAPPENED", SANSB(12), RED)
for n, (lo, la) in DOTS.items():
    rg = next(r for (m, r, *_) in LIST if m == n)
    px, py = proj(lo, la)
    ell(px - 2.4, py - 2.4, px + 2.4, py + 2.4, fill=REG[rg][1], outline="white")
for n, (lo, la) in PINS.items():
    rg = next(r for (m, r, *_) in LEADS + CARDS if m == n)
    px, py = proj(lo, la)
    off = {1: (6, -6), 8: (6, 7), 9: (-7, 4), 6: (-2, -8), 2: (-6, -6), 12: (-5, -5), 5: (0, -6)}.get(n, (0, 0))
    px += off[0]
    py += off[1]
    ell(px - 6.5, py - 6.5, px + 6.5, py + 6.5, fill=REG[rg][1], outline="white", width=0.8)
    T(px, py, str(n), SANSB(7.5), "white", "mm")
counts = {}
for n, rg, *_ in LEADS + CARDS + LIST:
    counts[rg] = counts.get(rg, 0) + 1
order = ["EU", "ME", "AS", "NA", "AF", "LA", "OC", "GL"]
lx, lgy = mx0, my0 + mh + 3
for j, rg in enumerate(order):
    if j == 4:
        lx, lgy = mx0, lgy + 14
    s_ = f"{SHORTN[rg]} {counts[rg]}"
    f_ = SANSB(10.5)
    ell(lx, lgy + 3, lx + 8, lgy + 11, fill=REG[rg][1])
    T(lx + 11, lgy + 1, s_, f_, INK)
    lx += tw(s_, f_) + 22
dy = lgy + 18
dh = H - 16 - dy
box(mx0, dy, mx0 + mw, dy + dh, fill="#FBEDEA", outline=RED, width=1.2)
box(mx0, dy, mx0 + mw, dy + 20, fill=RED)
T(mx0 + 7, dy + 3, "DATE CHECK · LEFT OUT AS OLDER NEWS", SANSB(11.5), "white")
yy = dy + 26
for a, b in DC:
    T(mx0 + 7, yy, a, SANS(12.5), INK)
    T(mx0 + mw - 7, yy, b, SANSB(12.5), RED, "ra")
    yy += 15
T(mx0 + 7, yy, "Not yet: COP31 final plenary", SANS(12.5), INK)
T(mx0 + mw - 7, yy, "Sun 22 Nov", SANSB(12.5), "#2B5BA8", "ra")

# ------------------------------------------------------------------ list (right)
lx0 = mx0 + mw + 14
colw = (W - M - lx0 - 14) / 2
heads = [("MORE FROM SATURDAY · 14-24", 0), ("MORE FROM SATURDAY · 25-35", 1)]
for h_, c_ in heads:
    x = lx0 + c_ * (colw + 14)
    T(x, by0 + 2, h_, SANSB(12), RED)
rowh = (dy + dh - (by0 + 20)) / 11
for i, (n, rg, place, what) in enumerate(LIST):
    c_, r_ = divmod(i, 11)
    x, y = lx0 + c_ * (colw + 14), by0 + 20 + r_ * rowh
    fn = SANSB(15)
    T(x, y + 1, str(n), fn, REG[rg][1])
    nx = x + tw(str(n), fn) + 6
    fp = SANSB(15)
    T(nx, y + 1, place, fp, INK)
    px = nx + tw(place, fp) + 4
    sz = 15
    while tw(what, SANS(sz)) > x + colw - px and sz > 11:
        sz -= 0.25
    T(px, y + 1 + (15 - sz) * 0.8, what, SANS(sz), INK)
    if r_ < 10:
        box(x, y + rowh - 2.5, x + colw, y + rowh - 2, fill="#DDD5C4")

# ------------------------------------------------------------------ footer
T(M, H - 5, "Saturday 21 November 2026, UTC times. CONFIRMED = 2+ outlets · OFFICIAL = on the record · "
  "CLAIM = one side's account. Original drawings, not photos. Sources: Reuters, AP, AFP, BBC, Al Jazeera, USGS, UKMTO.",
  SANS(8.6), GREY, "ls")

# ------------------------------------------------------------------ output
out = img.resize((W, H), Image.LANCZOS)
out = out.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
path = "/output/entry.png" if os.path.isdir("/output") else os.path.join(HERE, "entry.png")
out.save(path, format="PNG", optimize=True)
print("wrote", path)
