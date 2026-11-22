"""Saturday Finale - 21 November 2026 front page.
Draws one 1024x1024 newspaper front page with Pillow.
Build-time only: the shipped program (main.py) is a stdlib copier.
Run: python3 build.py  -> writes entry.png next to this file.
"""
import os, json, math
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

# ------------------------------------------------------------------ art layers
# Every illustration is drawn on its own transparent RGBA layer sized exactly
# to its art box, in coordinates relative to that box (origin 0,0). The layer
# is then pasted onto the page at (x, y). Pillow clips anything drawn outside
# a layer's bounds, so no art can ever spill past its frame.
class Layer:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (max(1, R(w)), max(1, R(h))), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    def box(self, x0, y0, x1, y1, **kw):
        if "width" in kw:
            kw["width"] = max(1, R(kw["width"]))
        self.d.rectangle([R(x0), R(y0), R(x1), R(y1)], **kw)

    def poly(self, pts, **kw):
        if "width" in kw:
            kw["width"] = max(1, R(kw["width"]))
        self.d.polygon([(R(px), R(py)) for px, py in pts], **kw)

    def line(self, pts, fill, w):
        self.d.line([(R(px), R(py)) for px, py in pts], fill=fill, width=R(w), joint="curve")

    def ell(self, x0, y0, x1, y1, **kw):
        if "width" in kw:
            kw["width"] = max(1, R(kw["width"]))
        self.d.ellipse([R(x0), R(y0), R(x1), R(y1)], **kw)

    def T(self, x, y, s, f, fill=INK, anchor="la"):
        self.d.text((R(x), R(y)), s, font=f, fill=fill, anchor=anchor)

    def paste(self, x, y):
        img.paste(self.img, (R(x), R(y)), self.img)

# ------------------------------------------------------------------ art
# Each art function draws inside the box (x, y, w, h) in page points.

def art_tankers(x, y, w, h):
    L = Layer(w, h)
    L.box(0, 0, w, h, fill="#7FA8C9")
    # sea
    L.box(0, h * 0.62, w, h, fill="#2B5BA8")
    # wave lines
    for k in range(3):
        L.line([(12 + k * 60, h * 0.72), (44 + k * 60, h * 0.72)], "white", 1.5)
    # big tanker, left, with a flame rising from its stern
    L.poly([(18, h * 0.62), (30, h * 0.30), (120, h * 0.30), (132, h * 0.62)], fill="#3A3F47")
    L.box(52, h * 0.14, 66, h * 0.30, fill="#3A3F47")
    L.poly([(132, h * 0.34), (150, h * 0.06), (168, h * 0.34)], fill="#F08A24")
    L.poly([(142, h * 0.34), (150, h * 0.16), (158, h * 0.34)], fill="#FFD34D")
    # small tanker, right
    L.box(200, h * 0.62, 290, h * 0.72, fill="#22252B")
    L.box(218, h * 0.46, 228, h * 0.62, fill="#22252B")
    L.T(w - 10, 8, "2 HIT", HEAD(20), "white", "ra")
    L.paste(x, y)

def art_cop(x, y, w, h):
    L = Layer(w, h)
    L.box(0, 0, w, h, fill="#BFE0EE")
    # a true circle globe, centred left
    cx, cy = w * 0.42, h * 0.52
    r = h * 0.40
    L.ell(cx - r, cy - r, cx + r, cy + r, fill="#3E8A4F", outline="white", width=2)
    L.poly([(cx - r * 0.55, cy - r * 0.25), (cx - r * 0.10, cy - r * 0.55), (cx + r * 0.35, cy - r * 0.10),
            (cx - r * 0.05, cy + r * 0.15)], fill="#7BC47F")
    L.poly([(cx - r * 0.15, cy + r * 0.45), (cx + r * 0.45, cy + r * 0.30), (cx + r * 0.40, cy + r * 0.75),
            (cx - r * 0.35, cy + r * 0.65)], fill="#7BC47F")
    # two small clouds, right
    L.ell(w * 0.78, h * 0.16, w * 0.88, h * 0.28, fill="white")
    L.ell(w * 0.84, h * 0.22, w * 0.94, h * 0.34, fill="white")
    L.T(10, h - 26, "COP31", HEAD(22), INK, "la")
    L.paste(x, y)

def art_mexico(x, y, w, h):
    L = Layer(w, h)
    L.box(0, 0, w, h, fill="#1F2A44")
    cx, cy = w / 2, h / 2
    # gold seal ring behind the star
    L.ell(cx - 44, cy - 44, cx + 44, cy + 44, outline="#F2B705", width=1.5)
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        r = 38 if k % 2 == 0 else 16
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    L.poly(pts, fill="#F2B705", outline="white", width=1.5)
    L.ell(cx - 12, cy - 12, cx + 12, cy + 12, fill="#1F2A44")
    L.T(cx, cy, "$", SANSB(17), "#F2B705", "mm")
    L.T(w - 8, 6, "SEIZED", SANSB(11), "white", "ra")
    L.paste(x, y)

def art_quake(x, y, w, h):
    L = Layer(w, h)
    L.box(0, 0, w, h, fill="#E8DCC4")
    # cracked ground along the bottom
    L.poly([(0, h), (w * 0.22, h * 0.52), (w * 0.42, h * 0.68), (w * 0.62, h * 0.46),
            (w * 0.82, h * 0.62), (w, h * 0.55), (w, h)], fill="#8A6D4B")
    # small tilted building, left
    L.poly([(18, h * 0.55), (34, h * 0.55), (38, h), (14, h)], fill="#5A4632")
    L.box(22, h * 0.64, 28, h * 0.74, fill="#FFD34D")
    # seismograph zigzag across the upper half
    L.line([(8, h * 0.34), (40, h * 0.22), (70, h * 0.48), (100, h * 0.16),
            (130, h * 0.40), (160, h * 0.26), (186, h * 0.38)], RED, 2.5)
    L.paste(x, y)

def art_finland(x, y, w, h):
    L = Layer(w, h)
    L.box(0, 0, w, h, fill="#9FC3D8")
    L.box(0, h * 0.66, w, h, fill="#2B5BA8")
    # ship hull
    L.poly([(22, h * 0.66), (34, h * 0.36), (150, h * 0.36), (162, h * 0.66)], fill="#3A3F47")
    L.box(60, h * 0.20, 74, h * 0.36, fill="#3A3F47")
    # flame from the deck, clear of the funnel and the label
    L.poly([(108, h * 0.42), (122, h * 0.10), (136, h * 0.42)], fill="#F08A24")
    L.poly([(116, h * 0.42), (124, h * 0.22), (132, h * 0.42)], fill="#FFD34D")
    L.T(10, 6, "16 SAFE", SANSB(11), INK, "la")
    L.paste(x, y)

def art_basra(x, y, w, h):
    L = Layer(w, h)
    L.box(0, 0, w, h, fill="#E9C9A8")
    # plant building with lit windows
    L.box(30, h * 0.42, 130, h, fill="#5A4632")
    for k in range(3):
        L.box(42 + k * 30, h * 0.52, 58 + k * 30, h * 0.66, fill="#FFD34D")
    # chimney with flame, right
    L.box(150, h * 0.30, 162, h, fill="#5A4632")
    L.poly([(140, h * 0.34), (156, h * 0.08), (172, h * 0.34)], fill="#F08A24")
    L.poly([(148, h * 0.34), (156, h * 0.16), (164, h * 0.34)], fill="#FFD34D")
    L.T(10, 6, "4 DEAD", SANSB(11), RED, "la")
    L.paste(x, y)

def art_trade(x, y, w, h):
    L = Layer(w, h)
    L.box(0, 0, w, h, fill="#DCE8F5")
    # EU flag, stars kept inside the blue field
    L.box(18, h * 0.18, 78, h * 0.62, fill="#2B5BA8")
    for k in range(6):
        ang = k * math.pi / 3
        L.ell(48 + 11 * math.cos(ang) - 2, h * 0.40 + 8 * math.sin(ang) - 2,
              48 + 11 * math.cos(ang) + 2, h * 0.40 + 8 * math.sin(ang) + 2, fill="#FFD34D")
    # Indonesia flag
    L.box(108, h * 0.18, 168, h * 0.40, fill="#C8102E")
    L.box(108, h * 0.40, 168, h * 0.62, fill="white")
    # link between the flags, and a green check below it
    L.line([(78, h * 0.40), (108, h * 0.40)], "#1A1A1A", 2)
    L.line([(86, h * 0.72), (92, h * 0.80), (102, h * 0.66)], "#2F7D4F", 2)
    L.paste(x, y)

def art_drone(x, y, w, h):
    L = Layer(w, h)
    L.box(0, 0, w, h, fill="#C9DCE6")
    cx, cy = w / 2, h * 0.52
    # arms
    L.line([(cx - 32, cy - 11), (cx + 32, cy + 11)], "#333333", 2)
    L.line([(cx - 32, cy + 11), (cx + 32, cy - 11)], "#333333", 2)
    # solid rotor discs at the four arm ends
    for (rx, ry) in [(cx - 32, cy - 11), (cx + 32, cy - 11), (cx - 32, cy + 11), (cx + 32, cy + 11)]:
        L.ell(rx - 8, ry - 3, rx + 8, ry + 3, fill="#3A3F47")
    # body with a white rim, orange camera eye
    L.ell(cx - 16, cy - 13, cx + 16, cy + 13, fill="#3A3F47", outline="white", width=1)
    L.ell(cx - 6, cy - 4, cx + 6, cy + 4, fill="#F08A24")
    L.T(10, 6, "MQ-9", SANSB(12), INK, "la")
    L.paste(x, y)

def art_riyadh(x, y, w, h):
    L = Layer(w, h)
    L.box(0, 0, w, h, fill="#F5D9A8")
    # skyline, every tower short enough to stay inside the box
    for (bx, bw, bh) in [(14, 26, 22), (48, 20, 28), (76, 30, 18), (114, 22, 26), (144, 26, 16)]:
        L.box(bx, h - bh, bx + bw, h, fill="#5A4632")
    # intercept arc above the skyline, with a gold burst at its peak
    L.line([(20, h * 0.55), (90, h * 0.16), (150, h * 0.42)], RED, 2)
    L.poly([(90, h * 0.07), (92.5, h * 0.16), (97, h * 0.16), (93, h * 0.22), (95, h * 0.32),
            (90, h * 0.25), (85, h * 0.32), (87, h * 0.22), (83, h * 0.16), (87.5, h * 0.16)],
           fill="#FFD34D")
    L.paste(x, y)

def art_taiwan(x, y, w, h):
    L = Layer(w, h)
    L.box(0, 0, w, h, fill="#FBEDEA")
    # axes
    L.line([(14, h * 0.18), (14, h * 0.84)], INK, 1.5)
    L.line([(14, h * 0.84), (w - 12, h * 0.84)], INK, 1.5)
    # falling line with an arrowhead
    L.line([(22, h * 0.28), (60, h * 0.36), (100, h * 0.52), (140, h * 0.64), (168, h * 0.74)], RED, 3.5)
    L.poly([(168, h * 0.74), (154, h * 0.68), (158, h * 0.84)], fill=RED)
    L.T(w - 8, 6, "-17.5%", HEAD(19), RED, "ra")
    L.paste(x, y)

def art_bitcoin(x, y, w, h):
    L = Layer(w, h)
    L.box(0, 0, w, h, fill="#FFF3D6")
    # rebound line first, so the coin covers its middle
    L.line([(12, h - 12), (60, h - 24), (110, h - 18), (w - 12, h - 28)], "#2F7D4F", 2.5)
    # coin sized to fit the box with a margin
    cx, cy = w / 2, h / 2
    r = h * 0.42
    L.ell(cx - r, cy - r, cx + r, cy + r, fill="#F7931A", outline="#C96A00", width=2)
    L.T(cx, cy, "B", SANSB(24), "white", "mm")
    L.T(10, 6, "$55,251", SANSB(12), INK, "la")
    L.paste(x, y)

def art_rugby(x, y, w, h):
    L = Layer(w, h)
    L.box(0, 0, w, h, fill="#3E8A4F")
    # mowing stripes
    for k in range(4):
        L.line([(12 + k * 48, h), (30 + k * 44, 0)], "#5BA36A", 1)
    # touchline near the bottom
    L.line([(8, h * 0.78), (w - 8, h * 0.78)], "white", 1.5)
    # ball, right, with a seam
    L.ell(w - 62, h * 0.28, w - 20, h * 0.72, fill="#8A5A2B", outline="white", width=1.5)
    L.line([(w - 54, h * 0.50), (w - 28, h * 0.50)], "white", 1.5)
    L.T(10, 8, "37-12", HEAD(18), "white", "la")
    L.paste(x, y)

def art_cricket(x, y, w, h):
    L = Layer(w, h)
    L.box(0, 0, w, h, fill="#CFE3C3")
    # pitch, diagonal band
    L.poly([(20, h - 6), (64, 10), (72, 13), (30, h - 2)], fill="#C9A066")
    # bat and red ball
    L.line([(88, 12), (96, h - 18)], "#8A5A2B", 3)
    L.ell(100, h - 26, 114, h - 12, fill=RED)
    L.T(w - 8, 8, "486-4", HEAD(19), INK, "ra")
    L.paste(x, y)

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
