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

# ---------------------------------------------------------------- 3 illustrated leads: the day's biggest stories
# status: ("CONFIRMED" | "CLAIM" | "REPORTED", sources)
LEADS = [
    dict(k="baltic", r="EU", t="Ukraine war", tag="BALTIC STRIKE", st=("CONFIRMED", "AFP · FINNISH MoD"), lon=26.9, lat=60.1,
         art=art.baltic(), h="Drones set Russian cargo ship ablaze off Finland",
         p="Finland says the drones were likely Ukrainian; all 16 crew of the sanctioned Sparta II were evacuated."),
    dict(k="btc", r="GL", t="Markets", tag="CRYPTO SLUMP", st=("CONFIRMED", "REUTERS · INVESTING.COM"), lon=None, lat=None,
         art=art2.bitcoin_lead(), h="Bitcoin hits a two-year low, then claws back",
         p="It fell to about $55,300 overnight, the lowest since September 2024, then rose to $60,192."),
    dict(k="riemann", r="GL", t="Maths & AI", tag="RIEMANN PROOF", st=("CONFIRMED", "GUARDIAN · SCI. AMERICAN"), lon=None, lat=None,
         art=art2.riemann_lead(), h="Experts certify a Claude-aided Riemann proof",
         p="The Lean and Mathlib communities say Levent Alpöge’s machine-checked proof of the 1859 problem is correct."),
]

# ---------------------------------------------------------------- 10 drawn cards, 5 per row
CARDS = [
    dict(k="sinaloa", r="AM", t="Cartels", tag="SINALOA", st=("CONFIRMED", "AP"), lon=-108.4, lat=25.6, art=art2.sinaloa_c(),
         h="“El Chapo Isidro” captured; 11 die", p="FBI Top Ten fugitive seized."),
    dict(k="hormuz", r="ME", t="Iran war", tag="HORMUZ", st=("CONFIRMED", "UKMTO"), lon=56.3, lat=26.6, art=art2.hormuz_c(),
         h="Two tankers hit by projectiles", p="Iran: a third hit a mine."),
    dict(k="kryvyi", r="EU", t="Ukraine war", tag="KRYVYI RIH", st=("CONFIRMED", "AP"), lon=33.4, lat=47.9, art=art2.kryvyi(),
         h="Missiles kill a boy, 7, and a medic", p="60 hurt, AP says."),
    dict(k="gaza", r="ME", t="Gaza", tag="GAZA CITY", st=("CONFIRMED", "REUTERS"), lon=34.45, lat=31.5, art=art2.gaza(),
         h="Israeli strike on a vehicle kills 3", p="WCK: it was not our vehicle."),
    dict(k="cop", r="ME", t="Climate", tag="COP31", st=("CONFIRMED", "REUTERS"), lon=30.7, lat=36.9, art=art2.cop31(),
         h="Climate talks stall a day past deadline", p="Fossil-fuel wording splits it."),
    dict(k="robots", r="EU", t="Diplomacy", tag="KILLER ROBOTS", st=("CONFIRMED", "REUTERS"), lon=6.1, lat=46.2, art=art2.robots(),
         h="UN arms talks end with no treaty", p="Talks go on until 2028."),
    dict(k="eu", r="EU", t="Economy", tag="EU BUDGET", st=("CONFIRMED", "AFP"), lon=4.35, lat=50.85, art=art2.eubudget(),
         h="Costa cuts €204bn from budget plan", p="Adds a Big Tech tax."),
    dict(k="bepi", r="GL", t="Space", tag="MERCURY", st=("CONFIRMED", "ESA"), lon=None, lat=None, art=art2.bepi(),
         h="BepiColombo enters orbit at Mercury", p="37-minute burn, 18:24 UTC."),
    dict(k="quake", r="AP", t="Quake", tag="BANDA SEA", st=("CONFIRMED", "USGS"), lon=127.5, lat=-7.7, art=art2.banda(),
         h="Deep M6.8 quake felt in Darwin", p="No tsunami, no damage."),
    dict(k="mama", r="AP", t="Music", tag="MAMA AWARDS", st=("CONFIRMED", "K. HERALD"), lon=135.5, lat=34.7, art=art2.mama(),
         h="BTS sweep five awards in Osaka", p="CORTIS take Song of the Year."),
]

# ---------------------------------------------------------------- one-line briefs (flag, colour and number)
# (key, region, flag, place, text, label, lon, lat)   label: "claim" | "report" | ""
BRIEFS = [
    ("heli", "EU", "FI", "Finland", "Russian helicopter breach suspected", "", 26.2, 60.4),
    ("blacksea", "EU", "RU", "Black Sea", "Russia says it hit cargo ship", "claim", 31.5, 44.0),
    ("front", "EU", "UA", "Ukraine", "Army logs 116 clashes", "claim", 37.2, 48.3),
    ("france", "EU", "FR", "France", "Sixth weekend of cost-of-living protests", "", 2.35, 48.9),
    ("pope", "EU", "VA", "Vatican", "Pope warns of “enormous” tech risks", "", 12.45, 41.9),
    ("eng", "EU", "ENG", "Rugby", "England 37–12 New Zealand", "", -0.34, 51.46),
    ("epl", "EU", "ENG", "Football", "Leeds win 4–1 at Chelsea", "", -0.19, 51.48),
    ("aoun", "ME", "LB", "Lebanon", "Aoun demands an Israeli withdrawal", "", 35.5, 33.9),
    ("israel", "ME", "IL", "Israel", "Bennett backs an Eisenkot-led coalition", "", 34.8, 32.1),
    ("houthi", "ME", "YE", "Yemen", "Houthis said to fortify the coast", "claim", 43.4, 12.8),
    ("peru", "AM", "PE", "Peru", "M6.7 quake at 00:09 UTC; Lima shakes", "", -76.0, -10.9),
    ("fbi", "AM", "US", "US", "Trump plays down FBI database hack", "", -77.0, 38.9),
    ("iran", "AM", "US", "US", "Trump wants a “permanent” Iran deal", "", -77.4, 39.4),
    ("brazil", "AM", "BR", "Brazil", "Lula calls fiscal bill “an adjustment”", "", -47.9, -15.8),
    ("in", "AP", "IN", "India", "Google gives IIT Kharagpur $5m for AI", "", 87.3, 22.3),
    ("bd", "AP", "BD", "Bangladesh", "More troops sent to stop arson", "", 90.4, 23.8),
    ("kr", "AP", "KR", "S. Korea", "Ruling party targets top judge", "", 127.0, 37.5),
    ("nk", "AP", "KP", "N. Korea", "Kim visits school factories", "report", 125.8, 39.0),
    ("cric", "AP", "NZ", "Cricket", "India 486/4 v NZ in Wellington", "", 174.8, -41.3),
    ("eg", "AF", "EG", "Egypt", "Sisi urges global finance reform", "", 32.9, 24.1),
    ("sudan", "AF", "SD", "Sudan", "RSF accused of killing children", "claim", 33.6, 13.6),
    ("oyo", "AF", "CG", "Congo", "Ruto at four-way security summit", "", 15.9, -1.0),
]

# (time label, text, story key)
TIMELINE = [
    ("00:09", "Peru M6.7 quake", "peru"),
    ("~04:00", "Geneva talks end", "robots"),
    ("06:50", "Sparta II hit", "baltic"),
    ("09:42", "Banda Sea M6.8", "quake"),
    ("10:34", "Heli breach", "heli"),
    ("15:16", "Bitcoin $60,192", "btc"),
    ("18:24", "Mercury burn", "bepi"),
    ("20:00", "116 clashes", "front"),
]

# (figure, caption, story key)
NUMBERS = [
    ("16", "crew evacuated", "baltic"),
    ("$55.3k", "Bitcoin low", "btc"),
    ("1859", "Riemann’s year", "riemann"),
    ("11", "dead in Sinaloa", "sinaloa"),
    ("148", "drones at Ukraine", "kryvyi"),
    ("128", "states in Geneva", "robots"),
    ("€204bn", "EU budget cut", "eu"),
    ("8 yrs", "to reach Mercury", "bepi"),
]

SUMMARY = "Drones set a Russian ship ablaze off Finland · Bitcoin hits a two-year low · Experts certify an AI-aided Riemann proof · Mexico seizes “El Chapo Isidro”"

LEFT_OUT = ("Left out as earlier news (Fri 20 Nov): Russian missiles landing in Poland, the Brazil supercell storm, the UK–EU deal, "
            "Mlambo-Ngcuka’s death. Not yet: the Las Vegas GP (Sun 22 Nov UTC), the Sudamericana final (ends after 00:00 UTC), "
            "COP31’s next draft (Sun 22), Mercury orbiters separate (9–10 Dec). Counted: Peru quake, 00:09 UTC.")

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


def banner(x):
    return (f'<div class="ban" style="background:{rc(x["r"])}"><span>{N[x["k"]]}</span>{e(x["tag"])}</div>')


def kicker(x):
    return f'<span class="kick" style="color:{rc(x["r"])}">{e(REGIONS[x["r"]][0])} · {e(x["t"])}</span>'


leads = "".join(
    f'<div class="lead" style="--c:{rc(x["r"])}"><div class="art">{x["art"]}{banner(x)}</div>'
    f'<div class="meta">{kicker(x)}<span class="right">{status(x["st"])}</span></div>'
    f'<h1>{e(x["h"])}</h1><p>{e(x["p"])}</p></div>' for x in LEADS)

def card_art(svg):
    """Fill the card width; trims about 1 px off the top and bottom of the drawing."""
    return svg.replace("<svg ", '<svg preserveAspectRatio="xMidYMid slice" ', 1)


cards = "".join(
    f'<div class="card" style="--c:{rc(x["r"])}"><div class="band" style="background:{rc(x["r"])}"><span class="n">{N[x["k"]]}</span>{e(x["tag"])}'
    f'<span class="bs2">{CHECK if x["st"][0] == "CONFIRMED" else ""}{e(x["st"][1])}</span></div>'
    f'<div class="art2">{card_art(x["art"])}</div><h2>{e(x["h"])}</h2><p>{e(x["p"])}</p></div>' for x in CARDS)

LBL = {"claim": '<span class="st claim">CLAIM</span>', "report": '<span class="st rep">REPORTED</span>', "": ""}


def brief_html(b):
    k, r, fl, place, text, label, *_ = b
    return (f'<div class="br">{badge(N[k], rc(r), "s")}{art2.flag(fl)}<div class="bt"><b>{e(place)}:</b> {e(text)} {LBL[label]}</div></div>')


half = (len(BRIEFS) + 1) // 2
briefs_l = "".join(brief_html(b) for b in BRIEFS[:half])
briefs_r = "".join(brief_html(b) for b in BRIEFS[half:])

timeline = "".join(f'<div class="tl"><b>{e(t)}{" UTC" if t[0] in "0123456789~" else ""}</b>'
                   f'<span>{badge(N[k], rc(REG[k]), "t")}{e(x)}</span></div>' for t, x, k in TIMELINE)
numbers = "".join(f'<div class="nm"><b>{e(v)}</b><span>{badge(N[k], rc(REG[k]), "t")}{e(c)}</span></div>' for v, c, k in NUMBERS)
region_bar = "".join(f'<div style="flex:{COUNT[r]};background:{c}">{e(n)} {COUNT[r]}</div>' for r, (n, c) in REGIONS.items())
for _, _, k in TIMELINE + NUMBERS:
    assert k in N, k

legend = "".join(f'<span><i style="background:{c}"></i>{e(n)} {COUNT[r]}</span>' for r, (n, c) in REGIONS.items())

# ---------------------------------------------------------------- map pins
pins = []
for x in LEADS + CARDS:
    if x["lon"] is not None:
        pins.append(dict(n=N[x["k"]], lon=x["lon"], lat=x["lat"], c=rc(x["r"]), big=1))
for b in BRIEFS:
    pins.append(dict(n=N[b[0]], lon=b[6], lat=b[7], c=rc(b[1]), big=0))
OFFMAP = [N[x["k"]] for x in LEADS + CARDS if x["lon"] is None]

MAPDATA = open(os.path.join(ROOT, "tools", "mapdata.js"), encoding="utf-8").read()
LAND = re.search(r"const land = (\[.*?\]);\n", MAPDATA, re.S).group(1)
WATER = re.search(r"const water = (\[.*?\]);\n", MAPDATA, re.S).group(1)

MAPJS = f"""
(function () {{
  const land = {LAND};
  const water = {WATER};
  const pins = {json.dumps(pins)};
  const W = 300, H = 150, B = {{lon0: -128, lon1: 180, lat0: 74, lat1: -46}};
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
  document.querySelectorAll('.band, .lead, .card, .meta, .bt, .br, .foot, .top, .summary, .tl, .nm, .mapbox, .also, .acols > div, .bottom, .lead p, .card p, .dc, .rbar div').forEach(el => {
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
<div class="top"><span class="tk">THE WORLD IN ONE DAY</span><span class="tc">{TOTAL} STORIES · {len(REGIONS)} REGIONS · {DRAWN} DRAWN · ALL FROM SATURDAY 21 NOVEMBER 2026</span></div>
<div class="title">Saturday 21 November 2026</div>
<div class="summary">{e(SUMMARY)}</div>
<div class="row"><div class="rl">THE DAY<br>IN UTC</div>{timeline}</div>
<div class="row nums"><div class="rl">THE DAY<br>IN NUMBERS</div>{numbers}</div>
<div class="rbar">{region_bar}</div>
<div class="leads">{leads}</div>
<div class="cards">{cards}</div>
<div class="bottom">
  <div class="mapbox"><div class="mh">WHERE IT HAPPENED <span>dots = briefs · off map: {", ".join(map(str, OFFMAP))}</span></div>
    <svg id="world" width="300" height="150" viewBox="0 0 300 150" xmlns="http://www.w3.org/2000/svg"></svg></div>
  <div class="also"><div class="ah">ALSO ON SATURDAY 21 NOVEMBER <span>{len(BRIEFS)} more · colour = region</span></div>
    <div class="acols"><div>{briefs_l}</div><div>{briefs_r}</div></div></div>
</div>
<div class="dc"><b class="dch">DATE CHECK</b> {e(LEFT_OUT)}</div>
<footer class="foot"><div><b>Every story took place on Saturday 21 November 2026 (UTC).</b> {CHECK}= confirmed by 2+ outlets or an official source · <span class="st claim">CLAIM</span> one side’s account · <span class="st rep">REPORTED</span> earlier event made public today</div>
<div>Sources: {e(SOURCES_LINE)} · original drawings</div></footer>
</div><script>{MAPJS}</script><script>{CHECKJS}</script></body></html>'''

open(os.path.join(ROOT, "poster", "index.html"), "w", encoding="utf-8").write(PAGE)
print("stories", TOTAL, "drawn", DRAWN, "regions", COUNT)
