#!/usr/bin/env python3
"""Builds poster/index.html: the front page for Saturday 21 November 2026.

All story data lives here. Numbering, counts, the timeline, map pins and every
total on the page are computed from this data and asserted. Render with
tools/render.sh; tools/check.sh reports any text that does not fit its box.

Rules (printed on the page):
  * Date: the story took place on Saturday 21 Nov 2026, 00:00-24:00 UTC.
    REPORT = an earlier event first made public on Saturday.
  * Region: where it happened (UN M49; Western Asia incl. Turkey = Middle East).
    No single location (markets, an online proof check, a spacecraft) = Global.
  * CONFIRMED = two or more independent outlets, or an official source.
    CLAIM = one side's account (a party to a conflict, or an unverified accusation).
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art  # noqa: E402  (lead drawings, 328x132)
import art2  # noqa: E402  (card drawings 160x56 and flags)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = html.escape

REGIONS = {
    "EU": ("Europe", "#1f5fbf"),
    "ME": ("Middle East", "#c07400"),
    "AM": ("Americas", "#2e8b3d"),
    "AP": ("Asia-Pacific", "#b0306f"),
    "AF": ("Africa", "#6b4226"),
    "GL": ("Global", "#4b3c93"),
}

# ---------------------------------------------------------------- 3 illustrated leads
# status: ("CONFIRMED" | "CLAIM" | "REPORTED", sources)
LEADS = [
    dict(k="baltic", r="EU", t="Ukraine war", st=("CONFIRMED", "AFP · FINNISH MoD"), lon=26.9, lat=60.1,
         art=art.baltic(), h="Drones set Russian cargo ship ablaze off Finland",
         p="Finland says the drones were likely Ukrainian. All 16 crew of the sanctioned Sparta II were evacuated."),
    dict(k="hormuz", r="ME", t="Iran war", st=("CONFIRMED", "REUTERS · UKMTO"), lon=56.3, lat=26.6,
         art=art.hormuz(), h="Two tankers hit by projectiles off Hormuz",
         p="UKMTO: both near Oman’s Khasab, no casualties. Iran says a third hit a mine, which is unverified."),
    dict(k="sinaloa", r="AM", t="Cartels", st=("CONFIRMED", "AP · REUTERS"), lon=-108.4, lat=25.6,
         art=art.sinaloa(), h="“El Chapo Isidro” captured as 11 die in Sinaloa",
         p="Fausto Isidro Meza Flores was seized in Guasave; 4 soldiers and 7 gunmen died."),
]

# ---------------------------------------------------------------- 12 drawn cards
CARDS = [
    dict(k="kryvyi", r="EU", t="Ukraine war", st=("CONFIRMED", "AP"), lon=33.4, lat=47.9, art=art2.kryvyi(),
         h="Russian strike kills boy and medic in Kryvyi Rih"),
    dict(k="france", r="EU", t="Protest", st=("CONFIRMED", "REUTERS"), lon=2.35, lat=48.9, art=art2.france(),
         h="France marches for a sixth weekend"),
    dict(k="eu", r="EU", t="Economy", st=("CONFIRMED", "AFP"), lon=4.35, lat=50.85, art=art2.eubudget(),
         h="Costa cuts €204bn from EU budget plan"),
    dict(k="robots", r="EU", t="Diplomacy", st=("CONFIRMED", "REUTERS"), lon=6.1, lat=46.2, art=art2.robots(),
         h="UN “killer robot” talks end with no treaty"),
    dict(k="cop", r="ME", t="Climate", st=("CONFIRMED", "REUTERS"), lon=30.7, lat=36.9, art=art2.cop31(),
         h="COP31 stalls on fossil fuels, a day late"),
    dict(k="gaza", r="ME", t="Gaza", st=("CONFIRMED", "REUTERS"), lon=34.45, lat=31.5, art=art2.gaza(),
         h="Israeli strike on a vehicle kills 3 in Gaza"),
    dict(k="peru", r="AM", t="Quake", st=("CONFIRMED", "USGS"), lon=-76.0, lat=-10.9, art=art2.peru(),
         h="M6.7 quake shakes Peru’s Andes"),
    dict(k="quake", r="AP", t="Quake", st=("CONFIRMED", "USGS"), lon=127.5, lat=-7.7, art=art2.banda(),
         h="Deep M6.8 quake felt in Timor and Darwin"),
    dict(k="mama", r="AP", t="Music", st=("CONFIRMED", "KOREA HERALD"), lon=135.5, lat=34.7, art=art2.mama(),
         h="BTS sweep five MAMA awards in Osaka"),
    dict(k="btc", r="GL", t="Markets", st=("CONFIRMED", "REUTERS"), lon=None, lat=None, art=art2.bitcoin(),
         h="Bitcoin hits two-year low, then rebounds"),
    dict(k="bepi", r="GL", t="Space", st=("CONFIRMED", "ESA · AP"), lon=None, lat=None, art=art2.bepi(),
         h="BepiColombo enters orbit around Mercury"),
    dict(k="riemann", r="GL", t="Maths & AI", st=("CONFIRMED", "GUARDIAN"), lon=None, lat=None, art=art2.riemann(),
         h="Experts certify AI-aided Riemann proof"),
]

# ---------------------------------------------------------------- one-line briefs (flag, colour and number)
# (key, region, flag, place, text, label, lon, lat)   label: "claim" | "report" | ""
BRIEFS = [
    ("heli", "EU", "FI", "Finland", "Russian helicopter breach suspected", "", 26.2, 60.4),
    ("blacksea", "EU", "RU", "Black Sea", "Russia hits a Ukraine ship", "claim", 31.5, 44.0),
    ("front", "EU", "UA", "Ukraine", "Army logs 116 clashes", "claim", 37.2, 48.3),
    ("kyiv", "EU", "GB", "Kyiv", "UK’s Streeting calls Putin a “killer”", "", 30.5, 50.4),
    ("ams", "EU", "NL", "Amsterdam", "UK PM meets Dutch PM Jetten", "", 4.9, 52.4),
    ("lisbon", "EU", "PT", "Lisbon", "Workers march for pay and housing", "", -9.1, 38.7),
    ("pope", "EU", "VA", "Vatican", "Pope warns of “enormous” tech risks", "", 12.45, 41.9),
    ("icj", "EU", "FR", "Paris", "France seeks UN action on Myanmar", "", 2.35, 48.9),
    ("eng", "EU", "ENG", "Rugby", "England 37–12 New Zealand, a record", "", -0.34, 51.46),
    ("ire", "EU", "IE", "Rugby", "Ireland 20–17 South Africa", "", -6.23, 53.33),
    ("epl", "EU", "ENG", "Football", "Leeds win 4–1 at Chelsea", "", -0.19, 51.48),
    ("aoun", "ME", "LB", "Beirut", "Aoun demands Israeli withdrawal", "", 35.5, 33.9),
    ("unifil", "ME", "UN", "S. Lebanon", "UNIFIL hands posts to army", "", 35.3, 33.2),
    ("israel", "ME", "IL", "Israel", "Bennett backs Eisenkot-led unity bid", "", 34.8, 32.1),
    ("houthi", "ME", "YE", "Yemen", "Houthis said to fortify coast", "claim", 43.4, 12.8),
    ("ufc", "ME", "QA", "UFC Doha", "Stirling knocks out Procházka", "", 51.5, 25.3),
    ("fbi", "AM", "US", "US", "Trump plays down FBI database hack", "", -77.0, 38.9),
    ("iran", "AM", "US", "US", "Trump wants a “permanent” Iran deal", "", -77.4, 39.4),
    ("halifax", "AM", "CA", "Halifax", "Taiwan warns Carney on China", "", -63.6, 44.6),
    ("brazil", "AM", "BR", "Brazil", "Lula calls fiscal bill “an adjustment”", "", -47.9, -15.8),
    ("cfb", "AM", "US", "US college", "Nebraska 31–28 Ohio State", "", -96.7, 40.8),
    ("dar", "AP", "PK", "Islamabad", "Dar hopes for early US–Iran deal", "", 73.0, 33.7),
    ("in", "AP", "IN", "Kharagpur", "Google gives IIT $5m for AI", "", 87.3, 22.3),
    ("flu", "AP", "IN", "Tamil Nadu", "Bird-flu checks in Cuddalore", "", 79.8, 11.7),
    ("bd", "AP", "BD", "Dhaka", "More troops sent to stop arson", "", 90.4, 23.8),
    ("kr", "AP", "KR", "Seoul", "Ruling party eyes judge impeachment", "", 127.0, 37.5),
    ("nk", "AP", "KP", "N. Korea", "Kim visits factories", "report", 125.8, 39.0),
    ("tw", "AP", "TW", "Taipei", "2 PLA aircraft, 7 ships, 4 balloons", "", 121.5, 25.0),
    ("cric", "AP", "NZ", "Cricket", "India 486/4 v NZ in Wellington", "", 174.8, -41.3),
    ("t20", "AP", "AU", "T20", "Australia beat England by 3 wickets", "", 144.98, -37.82),
    ("eg", "AF", "EG", "Aswan", "Sisi urges global finance reform", "", 32.9, 24.1),
    ("sudan", "AF", "SD", "Sudan", "RSF accused of killing children", "claim", 33.6, 13.6),
    ("oyo", "AF", "CG", "Congo", "Ruto at four-way security summit", "", 15.9, -1.0),
    ("somalia", "AF", "SO", "Mogadishu", "Turkish army chief visits", "", 45.3, 2.0),
    ("ng", "AF", "NG", "Ibadan", "Tinubu mutes rally after deaths", "", 3.9, 7.4),
]

# (time in UTC hours, label, story key, above?)
TIMELINE = [
    (0.15, "00:09 Peru quake", "peru", 1),
    (3.9, "~04:00 Geneva talks end", "robots", 0),
    (6.83, "06:50 Sparta II hit", "baltic", 1),
    (9.7, "09:42 Banda Sea quake", "quake", 0),
    (10.57, "10:34 heli breach", "heli", 1),
    (15.0, "15:00 Chelsea–Leeds", "epl", 0),
    (15.27, "15:16 BTC $60k", "btc", 1),
    (18.4, "18:24 Mercury burn", "bepi", 0),
    (20.0, "20:00 116 clashes", "front", 1),
]

LEFT_OUT = [
    ("Russian missiles land in Poland", "Fri 20 Nov"),
    ("Brazil supercell storm", "Fri 20 Nov"),
    ("UK–EU summit deal", "Fri 20 Nov"),
    ("Mlambo-Ngcuka dies", "Fri 20 Nov"),
    ("Las Vegas GP", "Sun 22 Nov UTC"),
    ("Sudamericana final", "ends Sun UTC"),
]

SOURCES_LINE = "Reuters, AP, AFP, USGS, ESA, UKMTO, Finnish MoD, Korea Herald, Anadolu, ISW, KCNA; all links in SOURCES.md"

# ---------------------------------------------------------------- numbering + checks
ORDER = ([("L", x["k"], x["r"]) for x in LEADS] + [("C", x["k"], x["r"]) for x in CARDS]
         + [("B", b[0], b[1]) for b in BRIEFS])
N = {k: i + 1 for i, (_, k, _) in enumerate(ORDER)}
assert len(N) == len(ORDER), "duplicate keys"
TOTAL = len(ORDER)
REG = {k: r for _, k, r in ORDER}
COUNT = {r: sum(1 for _, _, rr in ORDER if rr == r) for r in REGIONS}
assert sum(COUNT.values()) == TOTAL
DRAWN = len(LEADS) + len(CARDS)
for _, _, k, _ in TIMELINE:
    assert k in N, k
assert [t for t, *_ in TIMELINE] == sorted(t for t, *_ in TIMELINE)


def badge(n, color, size="b"):
    return f'<span class="bd {size}" style="background:{color}">{n}</span>'


def rc(r):
    return REGIONS[r][1]


CHECK = ('<svg class="ok" viewBox="0 0 16 16" width="12" height="12"><circle cx="8" cy="8" r="8" fill="#1e8e3e"/>'
         '<path d="M4.2 8.3 L7 11 L11.9 5.3" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def status(st):
    kind, src = st
    if kind == "CONFIRMED":
        return f'<span class="st conf">{CHECK}{e(src)}</span>'
    if kind == "CLAIM":
        return f'<span class="st claim">CLAIM</span><span class="ss">{e(src)}</span>'
    return f'<span class="st rep">REPORTED</span><span class="ss">{e(src)}</span>'


def kicker(x):
    return f'{badge(N[x["k"]], rc(x["r"]))}<span class="kick" style="color:{rc(x["r"])}">{e(REGIONS[x["r"]][0])} · {e(x["t"])}</span>'


leads = "".join(
    f'<div class="lead" style="--c:{rc(x["r"])}"><div class="art">{x["art"]}</div>'
    f'<div class="meta">{kicker(x)}<span class="right">{status(x["st"])}</span></div>'
    f'<h1>{e(x["h"])}</h1><p>{e(x["p"])}</p></div>' for x in LEADS)

cards = "".join(
    f'<div class="card" style="--c:{rc(x["r"])}"><div class="art2">{x["art"]}</div>'
    f'<div class="meta">{kicker(x)}</div><h2>{e(x["h"])}</h2>'
    f'<div class="stl">{status(x["st"])}</div></div>' for x in CARDS)

LBL = {"claim": '<span class="st claim">CLAIM</span>', "report": '<span class="st rep">REPORTED</span>', "": ""}


def brief_html(b):
    k, r, fl, place, text, label, *_ = b
    return (f'<div class="br">{badge(N[k], rc(r), "s")}{art2.flag(fl)}<div class="bt"><b>{e(place)}:</b> {e(text)} {LBL[label]}</div></div>')


half = (len(BRIEFS) + 1) // 2
briefs_l = "".join(brief_html(b) for b in BRIEFS[:half])
briefs_r = "".join(brief_html(b) for b in BRIEFS[half:])

# proportional UTC timeline
TL_W = 920
tl = ['<svg class="tlsvg" width="920" height="40" viewBox="0 0 920 40">',
      '<line x1="10" y1="20" x2="910" y2="20" stroke="#16181d" stroke-width="1.6"/>']
for hr in range(0, 25, 3):
    x = 10 + hr / 24 * 900
    tl.append(f'<line x1="{x:.1f}" y1="17" x2="{x:.1f}" y2="23" stroke="#16181d" stroke-width="1"/>')
tl.append('<text x="10" y="35" font-size="9.5" fill="#555" font-family="Small">00:00</text>'
          '<text x="910" y="35" font-size="9.5" fill="#555" text-anchor="end" font-family="Small">24:00</text>')
for t, label, k, up in TIMELINE:
    x = 10 + t / 24 * 900
    c = rc(REG[k])
    y = 12 if up else 34
    anchor = 'start' if x < 60 else ('end' if x > 860 else 'middle')
    tl.append(f'<line x1="{x:.1f}" y1="20" x2="{x:.1f}" y2="{14 if up else 26}" stroke="{c}" stroke-width="1.4"/>'
              f'<circle cx="{x:.1f}" cy="20" r="4" fill="{c}" stroke="#fff" stroke-width="1"/>'
              f'<text x="{x:.1f}" y="{y}" font-size="11" font-weight="700" fill="#16181d" text-anchor="{anchor}" font-family="Small">'
              f'<tspan fill="{c}" font-weight="800">{N[k]}</tspan> {e(label)}</text>')
tl.append('</svg>')
timeline = "".join(tl)

left_out = "".join(f'<div class="lo"><span>{e(a)}</span><b>{e(d)}</b></div>' for a, d in LEFT_OUT)
legend = "".join(f'<span><i style="background:{c}"></i>{e(n)} {COUNT[r]}</span>' for r, (n, c) in REGIONS.items())

# ---------------------------------------------------------------- map pins
pins = []
for x in LEADS + CARDS:
    if x["lon"] is not None:
        pins.append(dict(n=N[x["k"]], lon=x["lon"], lat=x["lat"], c=rc(x["r"]), big=1))
for b in BRIEFS:
    pins.append(dict(n=N[b[0]], lon=b[6], lat=b[7], c=rc(b[1]), big=0))
OFFMAP = [N[x["k"]] for x in LEADS + CARDS if x["lon"] is None]

V1 = open(os.path.join(ROOT, "build", "index_v1.html"), encoding="utf-8").read()
LAND = re.search(r"const land = (\[.*?\]);\n  const water", V1, re.S).group(1)
WATER = re.search(r"const water = (\[.*?\]);\n  const poly", V1, re.S).group(1)

MAPJS = f"""
(function () {{
  const land = {LAND};
  const water = {WATER};
  const pins = {json.dumps(pins)};
  const W = 322, H = 108, B = {{lon0: -128, lon1: 180, lat0: 74, lat1: -46}};
  const sx = W / (B.lon1 - B.lon0), sy = H / (B.lat0 - B.lat1);
  const P = (lon, lat) => [(lon - B.lon0) * sx, (B.lat0 - lat) * sy];
  const inside = (x, y, poly) => {{ let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {{
      const [xi, yi] = poly[i], [xj, yj] = poly[j];
      if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) c = !c; }} return c; }};
  let s = '<rect width="' + W + '" height="' + H + '" fill="#eaf1f5"/>';
  const step = 3.3;
  for (let py = step / 2; py < H; py += step) for (let px = step / 2; px < W; px += step) {{
    const lon = B.lon0 + px / sx, lat = B.lat0 - py / sy;
    if (land.some(p => inside(lon, lat, p)) && !water.some(p => inside(lon, lat, p)))
      s += '<circle cx="' + px.toFixed(1) + '" cy="' + py.toFixed(1) + '" r="1.1" fill="#c3bba7"/>';
  }}
  pins.filter(p => !p.big).forEach(p => {{ const [x, y] = P(p.lon, p.lat);
    s += '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="3" fill="' + p.c + '" stroke="#fff" stroke-width=".9"/>'; }});
  const placed = [], R = 8, marks = [];
  const free = (x, y) => x > R && y > R && x < W - R && y < H - R && placed.every(q => Math.hypot(q[0] - x, q[1] - y) > 2 * R + 1);
  pins.filter(p => p.big).sort((a, b) => a.n - b.n).forEach(p => {{
    const [x, y] = P(p.lon, p.lat); let bx = x, by = y;
    if (!free(x, y)) {{ let done = false;
      for (let d = 2 * R + 2; d < 120 && !done; d += 3)
        for (let a = 0; a < 24 && !done; a++) {{ const t = -Math.PI / 2 + a * Math.PI / 12, cx = x + d * Math.cos(t), cy = y + d * Math.sin(t);
          if (free(cx, cy)) {{ bx = cx; by = cy; done = true; }} }} }}
    placed.push([bx, by]); marks.push([p, x, y, bx, by]); }});
  marks.forEach(([p, x, y, bx, by]) => {{ if (bx !== x || by !== y)
    s += '<line x1="' + x.toFixed(1) + '" y1="' + y.toFixed(1) + '" x2="' + bx.toFixed(1) + '" y2="' + by.toFixed(1) + '" stroke="#16181d" stroke-width="1"/>'; }});
  marks.forEach(([p, x, y, bx, by]) => {{
    s += '<circle cx="' + bx.toFixed(1) + '" cy="' + by.toFixed(1) + '" r="' + R + '" fill="' + p.c + '" stroke="#fff" stroke-width="1.3"/>';
    s += '<text x="' + bx.toFixed(1) + '" y="' + (by + 3.5).toFixed(1) + '" font-size="10" font-weight="800" fill="#fff" text-anchor="middle" font-family="Small">' + p.n + '</text>'; }});
  document.getElementById('world').innerHTML = s;
}})();
"""

CHECKJS = """
(function () {
  const bad = [];
  document.querySelectorAll('.lead, .card, .meta, .bt, .br, .lo, .foot, .top, .tlbox, .mapbox, .also, .acols > div, .bottom, .lead h1, .lead p, .card h2, .stl').forEach(el => {
    if (el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1)
      bad.push(el.className + '[' + (el.scrollWidth - el.clientWidth) + 'x' + (el.scrollHeight - el.clientHeight) + ']:' + (el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 34));
  });
  const f = document.querySelector('.foot').getBoundingClientRect();
  if (f.bottom > 1024) bad.push('PAGE-BOTTOM:' + f.bottom);
  document.body.setAttribute('data-overflow', bad.join(' | '));
})();
"""

CSS = open(os.path.join(ROOT, "tools", "style.css"), encoding="utf-8").read()

PAGE = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>The One-Day World · Saturday 21 November 2026</title><style>{CSS}</style></head>
<body><div class="page">
<div class="top"><span class="tk">THE WORLD IN ONE DAY</span><span class="tc">{TOTAL} STORIES · {len(REGIONS)} REGIONS · {DRAWN} DRAWN · ALL FROM THIS SATURDAY (UTC)</span></div>
<div class="title">Saturday 21 November 2026</div>
<div class="tlbox"><div class="tlh">THE DAY<br>IN UTC</div>{timeline}</div>
<div class="leads">{leads}</div>
<div class="cards">{cards}</div>
<div class="bottom">
  <div class="mapbox"><div class="mh">WHERE IT HAPPENED <span>off map: {", ".join(map(str, OFFMAP))}</span></div>
    <svg id="world" width="322" height="108" viewBox="0 0 322 108" xmlns="http://www.w3.org/2000/svg"></svg>
    <div class="lg">{legend}</div>
    <div class="dc"><div class="dch">DATE CHECK · LEFT OUT, NOT SATURDAY UTC</div>{left_out}
      <div class="dcn"><b>Counted:</b> Peru quake at 00:09 UTC Sat (19:09 Fri, Lima)</div></div></div>
  <div class="also"><div class="ah">ALSO ON SATURDAY 21 NOVEMBER <span>{TOTAL - DRAWN} briefs · colour = region</span></div>
    <div class="acols"><div>{briefs_l}</div><div>{briefs_r}</div></div></div>
</div>
<footer class="foot"><div><b>Every story took place on Sat 21 Nov 2026 (UTC).</b> {CHECK}= confirmed by 2+ outlets or an official source · <span class="st claim">CLAIM</span> one side’s account · <span class="st rep">REPORTED</span> earlier event made public today</div>
<div>Sources: {e(SOURCES_LINE)} · drawings made in code</div></footer>
</div><script>{MAPJS}</script><script>{CHECKJS}</script></body></html>'''

open(os.path.join(ROOT, "poster", "index.html"), "w", encoding="utf-8").write(PAGE)
print("stories", TOTAL, "drawn", DRAWN, "regions", COUNT)
