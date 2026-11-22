#!/usr/bin/env python3
"""Builds poster/index.html: the front page for Saturday 21 November 2026.

All story data lives here. Numbering, region and topic counts, map pins and the
headline total are computed from this data and asserted, so the page cannot
disagree with itself. Render with tools/render.sh afterwards.

Rules printed on the page:
  * Date: the story took place on Saturday 21 Nov 2026 between 00:00 and 24:00 UTC.
    Exception, marked REPORT: an earlier event first made public on Saturday.
  * Region: where it happened (UN M49; Western Asia incl. Turkey = Middle East).
    No single location (markets, online, space) = Global.  Sport is filed by venue.
  * CLAIM: one side's word (a party to a conflict, or an unverified accusation).
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
e = html.escape

REGIONS = {
    "EU": ("Europe", "#1f5fbf"),
    "ME": ("Middle East", "#c07400"),
    "AM": ("Americas", "#2e8b3d"),
    "AP": ("Asia-Pacific", "#b0306f"),
    "AF": ("Africa", "#6b4226"),
    "GL": ("Global & space", "#4b3c93"),
}
TOPICS = ["War", "Politics", "Economy", "Disaster", "Climate", "Science", "Health", "Society", "Crime", "Culture", "Sport"]

# ---------------------------------------------------------------- 3 illustrated leads
LEADS = [
    dict(k="baltic", r="EU", t="War", kick="Baltic Sea", src="AFP · REUTERS · FINNISH MoD", lon=26.9, lat=60.1,
         art=art.baltic(), h="Drones set Russian cargo ship ablaze off Finland",
         p="Finland says the drones that hit the US-sanctioned ship were likely Ukrainian; all 16 crew were evacuated."),
    dict(k="hormuz", r="ME", t="War", kick="Strait of Hormuz", src="REUTERS · UKMTO · AP", lon=56.3, lat=26.6,
         art=art.hormuz(), h="Two tankers hit by projectiles off Hormuz",
         p="UKMTO reports both near Oman’s Khasab; no casualties. Iran’s navy says a third hit a mine (unverified)."),
    dict(k="sinaloa", r="AM", t="Crime", kick="Sinaloa, Mexico", src="AP · REUTERS · CBS", lon=-108.4, lat=25.6,
         art=art.sinaloa(), h="“El Chapo Isidro” captured as 11 die in Sinaloa",
         p="Fausto Isidro Meza Flores, on the FBI’s Ten Most Wanted list, was seized in Guasave; 4 soldiers and 7 gunmen died."),
]

# ---------------------------------------------------------------- 8 drawn cards (each picture is specific to its story)
CARDS = [
    dict(k="kryvyi", r="EU", t="War", kick="Kryvyi Rih", src="AP · UKR AIR FORCE", lon=33.4, lat=47.9, art=art.kryvyi(),
         h="Russian missiles kill boy, 7, and medic, officials say", p="AP: 60 hurt. Kyiv: 117 drones downed.", claim=False),
    dict(k="cop", r="ME", t="Climate", kick="Antalya", src="REUTERS · GUARDIAN", lon=30.7, lat=36.9, art=art.cop31b(),
         h="COP31 deadlocked over the move away from fossil fuels", p="Halted for the night, a day over time."),
    dict(k="eu", r="EU", t="Economy", kick="Brussels", src="AFP · POLITICO", lon=4.35, lat=50.85, art=art.eubars(),
         h="Costa cuts €204bn from the EU’s 2028–34 budget plan", p="Adds a Big Tech tax; Merz: still too high."),
    dict(k="btc", r="GL", t="Economy", kick="Crypto", src="REUTERS · INVESTING", lon=None, lat=None, art=art.bitcoin(),
         h="Bitcoin hits a two-year low near $55,300, then rebounds", p="Back above $60,000 by 15:16 UTC."),
    dict(k="bepi", r="GL", t="Science", kick="Mercury", src="ESA · AP · NATURE", lon=None, lat=None, art=art.bepi(),
         h="BepiColombo enters orbit around Mercury after 8 years", p="37-minute burn from 18:24 UTC."),
    dict(k="riemann", r="GL", t="Science", kick="Maths & AI", src="GUARDIAN · SCI AM", lon=None, lat=None, art=art.riemann(),
         h="Lean community certifies Claude-aided Riemann proof", p="Lean FRO, Mathlib back Alpöge’s proof."),
    dict(k="quake", r="AP", t="Disaster", kick="Banda Sea", src="USGS · GFZ", lon=127.5, lat=-7.7, art=art.quakemap(),
         h="Deep M6.8 quake shakes Timor-Leste and Darwin", p="USGS green alert; no tsunami threat."),
    dict(k="gaza", r="ME", t="War", kick="Gaza City", src="REUTERS · GAZA MoH", lon=34.45, lat=31.5, art=art.gaza(),
         h="Israeli strike on a vehicle kills three in Gaza City", p="World Central Kitchen: not its vehicle."),
]

# ---------------------------------------------------------------- briefs, grouped by region
# (key, region, topic, place, text, source, flag, lon, lat)   flag: "claim" | "official" | "report" | ""
BRIEFS = [
    ("heli", "EU", "War", "Finland", "Russian heli breach suspected", "MoD", "official", 26.2, 60.4),
    ("blacksea", "EU", "War", "Black Sea", "Russia says it hit Ukraine ship", "SKY", "claim", 31.5, 44.0),
    ("front", "EU", "War", "Front line", "116 clashes in a day", "UA ARMY", "claim", 37.2, 48.3),
    ("kyiv", "EU", "Politics", "Kyiv", "UK’s Streeting calls Putin a “killer”", "ITV", "", 30.5, 50.4),
    ("geneva", "EU", "Politics", "Geneva", "UN killer-robot talks: no treaty", "REUTERS", "", 6.1, 46.2),
    ("france", "EU", "Society", "France", "6th weekend of living-cost marches", "REUTERS", "", 2.35, 48.9),
    ("mq9", "ME", "War", "Hormuz", "IRGC says it downed MQ-9", "TASNIM", "claim", 56.0, 27.2),
    ("aoun", "ME", "Politics", "Beirut", "Aoun demands Israeli exit", "ARAB NEWS", "", 35.5, 33.9),
    ("houthi", "ME", "War", "Yemen", "Houthis said to dig in on coast", "ISW", "claim", 43.4, 12.8),
    ("peru", "AM", "Disaster", "Peru", "M6.7 quake, 00:09 UTC; no damage", "USGS", "official", -76.0, -10.9),
    ("brazil", "AM", "Economy", "Brasília", "Lula: fiscal bill an “adjustment”", "RIO TIMES", "", -47.9, -15.8),
    ("fbi", "AM", "Crime", "Washington", "Trump plays down FBI hack", "AXIOS", "", -77.0, 38.9),
    ("iran", "AM", "Politics", "Washington", "Trump: “permanent” Iran deal", "CBS", "", -77.4, 39.4),
    ("halifax", "AM", "Politics", "Halifax", "Taiwan warns Carney on China", "AP", "", -63.6, 44.6),
    ("in", "AP", "Science", "Kharagpur", "Google gives IIT $5m for AI", "PTI", "", 87.3, 22.3),
    ("flu", "AP", "Health", "Tamil Nadu", "Bird-flu checks in Cuddalore", "PTI", "", 79.8, 11.7),
    ("bd", "AP", "Society", "Dhaka", "Troops sent to halt arson", "REUTERS", "", 90.4, 23.8),
    ("kr", "AP", "Politics", "Seoul", "Bid to impeach top judge on 3 Dec", "K. HERALD", "", 127.0, 37.5),
    ("nk", "AP", "Politics", "Pyongyang", "Kim tours school factories", "KCNA", "report", 125.8, 39.0),
    ("mama", "AP", "Culture", "Osaka", "BTS wins 5 MAMA awards", "K. HERALD", "", 135.5, 34.7),
    ("eg", "AF", "Politics", "Aswan", "Sisi urges global finance reform", "DNE", "", 32.9, 24.1),
    ("sudan", "AF", "War", "Sudan", "RSF accused of killing children", "AA", "claim", 33.6, 13.6),
    ("oyo", "AF", "Politics", "Oyo, Congo", "Ruto at four-way summit", "STATE HOUSE", "official", 15.9, -1.0),
    ("somalia", "AF", "War", "Mogadishu", "Turkish army chief visits", "GAROWE", "", 45.3, 2.0),
    ("ng", "AF", "Politics", "Ibadan", "Tinubu mutes rally after deaths", "PREM. TIMES", "", 3.9, 7.4),
]

# ---------------------------------------------------------------- sport (all finished before 24:00 UTC), filed by venue
SPORT = [
    ("eng", "EU", "Rugby · London", "England 37–12 NZ", "SKY", -0.34, 51.46),
    ("epl", "EU", "EPL · London", "Chelsea 1–4 Leeds", "ESPN", -0.19, 51.48),
    ("cric", "AP", "Test · Wellington", "India 486/4 v NZ", "AFP", 174.8, -41.3),
    ("t20", "AP", "T20 · Melbourne", "Australia beat England", "ESPN", 144.98, -37.82),
    ("cfb", "AM", "NCAA · Lincoln", "Nebraska 31–28 OSU", "NBC", -96.7, 40.8),
    ("ufc", "ME", "UFC · Doha", "Stirling KOs Procházka", "UFC", 51.5, 25.3),
]

TIMELINE = [
    ("00:09", "M6.7 quake, Peru", "peru"),
    ("by 04:00", "Geneva talks end", "geneva"),
    ("06:50", "Sparta II alert", "baltic"),
    ("09:42", "M6.8 Banda Sea", "quake"),
    ("10:34", "Heli over Loviisa", "heli"),
    ("15:16", "Bitcoin back at $60k", "btc"),
    ("18:24", "Mercury burn starts", "bepi"),
    ("20:00", "116 clashes logged", "front"),
]

NOT_COUNTED = ("<b>Before 00:00 UTC:</b> missiles in Poland · Brazil storm · UK–EU deal. "
               "<b>After 24:00:</b> Las Vegas GP · Sudamericana final. "
               "<b>Counted:</b> Peru quake at 00:09 UTC.")

SOURCE_KEY = ("AA Anadolu · DNE Daily News Egypt · ISW Inst. for the Study of War · KCNA N. Korean state media · "
              "MoD/MoH defence/health ministry · PTI Press Trust of India · SCI AM Scientific American · UKMTO UK Maritime Trade Ops")

# ---------------------------------------------------------------- numbering + checks
ORDER = ([("L", x["k"], x["r"], x["t"]) for x in LEADS] + [("C", x["k"], x["r"], x["t"]) for x in CARDS]
         + [("B", b[0], b[1], b[2]) for b in BRIEFS] + [("S", s[0], s[1], "Sport") for s in SPORT])
N = {k: i + 1 for i, (_, k, _, _) in enumerate(ORDER)}
assert len(N) == len(ORDER), "duplicate keys"
TOTAL = len(ORDER)
REG = {k: r for _, k, r, _ in ORDER}
COUNT = {r: sum(1 for _, _, rr, _ in ORDER if rr == r) for r in REGIONS}
TCOUNT = {t: sum(1 for *_, tt in ORDER if tt == t) for t in TOPICS}
assert sum(COUNT.values()) == TOTAL and sum(TCOUNT.values()) == TOTAL
DRAWN = len(LEADS) + len(CARDS)
# briefs must be grouped by region in REGIONS order
seq = [b[1] for b in BRIEFS]
assert seq == sorted(seq, key=list(REGIONS).index), "briefs not grouped by region"
for b in BRIEFS:
    assert len(b[3]) + len(b[4]) <= 52, (len(b[3]) + len(b[4]), b)
for _, _, k in TIMELINE:
    assert k in N
REPORTED = [b[0] for b in BRIEFS if b[6] == "report"]


SHORT = {"EU": "Europe", "ME": "Mid-East", "AM": "Americas", "AP": "Asia-Pacific", "AF": "Africa", "GL": "Global"}


def badge(n, color, size="b"):
    return f'<span class="bd {size}" style="background:{color}">{n}</span>'


def rc(r):
    return REGIONS[r][1]


# ---------------------------------------------------------------- html pieces
region_bar = "".join(f'<div style="flex:{COUNT[r]};background:{c}">{e(SHORT[r])} {COUNT[r]}</div>' for r, (name, c) in REGIONS.items())
region_key = "".join(f'<span><i style="background:{c}"></i>{e(name)} <b>{COUNT[r]}</b></span>' for r, (name, c) in REGIONS.items())
topic_key = " · ".join(f'{e(t)} <b>{TCOUNT[t]}</b>' for t in TOPICS if TCOUNT[t])

timeline = "".join(
    f'<div class="tl"><b>{badge(N[k], rc(REG[k]), "t")}{e(t)}{" UTC" if t[0].isdigit() else " UTC" if t.startswith("by") else ""}</b>{e(x)}</div>'
    for t, x, k in TIMELINE)


def meta(x, size):
    return (f'<div class="meta">{badge(N[x["k"]], rc(x["r"]), size)}<span class="kick" style="color:{rc(x["r"])}">'
            f'{e(x["t"])} · {e(x["kick"])}</span><span class="srcr">{e(x["src"])}</span></div>')


leads = "".join(f'<div class="lead"><div class="art">{x["art"]}</div>{meta(x, "b")}<h1>{e(x["h"])}</h1><p>{e(x["p"])}</p></div>' for x in LEADS)
cards = "".join(f'<div class="card"><div class="art2">{x["art"]}</div>{meta(x, "s")}<h2>{e(x["h"])}</h2><p>{e(x["p"])}</p></div>' for x in CARDS)

FLAG = {"claim": '<span class="claim">CLAIM</span>', "official": '<span class="off" title="official"></span>',
        "report": '<span class="rep">REPORT</span>', "": ""}


def brief_rows():
    rows, cur = [], None
    for k, r, t, place, text, src, flag, *_ in BRIEFS:
        if r != cur:
            cur = r
            n = sum(1 for b in BRIEFS if b[1] == r)
            rows.append(f'<div class="rh" style="color:{rc(r)};border-color:{rc(r)}">{e(REGIONS[r][0])} <span>{n}</span></div>')
        rows.append(f'<div class="br">{badge(N[k], rc(r), "s")}<div class="bt"><b>{e(place)}:</b> {e(text)} {FLAG[flag]}'
                    f'<span class="bs">{e(src)}</span></div></div>')
    return rows


rows = brief_rows()
half = (len(rows) + 1) // 2
# never leave a region header alone at the bottom of column 1
if rows[half - 1].startswith('<div class="rh"'):
    half -= 1
briefs_l, briefs_r = "".join(rows[:half]), "".join(rows[half:])

sport = "".join(f'<div class="sp">{badge(N[k], rc(r), "s")}<div><b>{e(c)} <span class="bs">· {e(src)}</span></b>{e(t)}</div></div>'
                for k, r, c, t, src, *_ in SPORT)

# ---------------------------------------------------------------- map pins
pins = []
for x in LEADS + CARDS:
    if x["lon"] is not None:
        pins.append(dict(n=N[x["k"]], lon=x["lon"], lat=x["lat"], c=rc(x["r"]), big=1))
for b in BRIEFS:
    pins.append(dict(n=N[b[0]], lon=b[7], lat=b[8], c=rc(b[1]), big=0))
for s_ in SPORT:
    pins.append(dict(n=N[s_[0]], lon=s_[5], lat=s_[6], c=rc(s_[1]), big=0))
OFFMAP = [N[x["k"]] for x in LEADS + CARDS if x["lon"] is None]

V1 = open(os.path.join(ROOT, "build", "index_v1.html"), encoding="utf-8").read()
LAND = re.search(r"const land = (\[.*?\]);\n  const water", V1, re.S).group(1)
WATER = re.search(r"const water = (\[.*?\]);\n  const poly", V1, re.S).group(1)

INSET = dict(lon0=-12, lon1=62, lat0=64, lat1=24)

MAPJS = f"""
(function () {{
  const land = {LAND};
  const water = {WATER};
  const pins = {json.dumps(pins)};
  const INSET = {json.dumps(INSET)};
  const inside = (x, y, poly) => {{ let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {{
      const [xi, yi] = poly[i], [xj, yj] = poly[j];
      if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) c = !c; }} return c; }};
  const inInset = p => p.lon >= INSET.lon0 && p.lon <= INSET.lon1 && p.lat <= INSET.lat0 && p.lat >= INSET.lat1;
  function draw(id, W, H, B, step, list, frame) {{
    const sx = W / (B.lon1 - B.lon0), sy = H / (B.lat0 - B.lat1);
    const P = (lon, lat) => [(lon - B.lon0) * sx, (B.lat0 - lat) * sy];
    let s = '<rect width="' + W + '" height="' + H + '" fill="#eef3f6"/>';
    for (let py = step / 2; py < H; py += step) for (let px = step / 2; px < W; px += step) {{
      const lon = B.lon0 + px / sx, lat = B.lat0 - py / sy;
      if (land.some(p => inside(lon, lat, p)) && !water.some(p => inside(lon, lat, p)))
        s += '<circle cx="' + px.toFixed(1) + '" cy="' + py.toFixed(1) + '" r="' + (step * 0.34).toFixed(2) + '" fill="#c3bba7"/>';
    }}
    if (frame) {{ const [x0, y0] = P(INSET.lon0, INSET.lat0), [x1, y1] = P(INSET.lon1, INSET.lat1);
      s += '<rect x="' + x0 + '" y="' + y0 + '" width="' + (x1 - x0) + '" height="' + (y1 - y0) + '" fill="none" stroke="#16181d" stroke-width="1" stroke-dasharray="3 2"/>' +
           '<text x="' + (x0 + 2) + '" y="' + (y0 - 2) + '" font-size="7.5" font-weight="800" fill="#16181d" font-family="Body">ZOOM BELOW</text>'; }}
    // deterministic label placement: biggest stories first, spiral out until no overlap
    const placed = [];
    const R = p => p.big ? 7.6 : 6.4;
    const order = list.slice().sort((a, b) => (b.big - a.big) || (a.n - b.n));
    const free = (x, y, r) => x > r && y > r && x < W - r && y < H - r && placed.every(q => Math.hypot(q.x - x, q.y - y) > q.r + r + 1);
    const marks = [];
    order.forEach(p => {{
      const [x, y] = P(p.lon, p.lat); const r = R(p); let bx = x, by = y;
      if (!free(x, y, r)) {{
        let done = false;
        for (let d = r * 2 + 2; d < 90 && !done; d += 4)
          for (let a = 0; a < 24 && !done; a++) {{ const t = -Math.PI / 2 + a * Math.PI / 12; const cx = x + d * Math.cos(t), cy = y + d * Math.sin(t);
            if (free(cx, cy, r)) {{ bx = cx; by = cy; done = true; }} }}
      }}
      placed.push({{x: bx, y: by, r: r}}); marks.push([p, x, y, bx, by, r]);
    }});
    marks.forEach(([p, x, y, bx, by, r]) => {{ if (bx !== x || by !== y)
      s += '<line x1="' + x.toFixed(1) + '" y1="' + y.toFixed(1) + '" x2="' + bx.toFixed(1) + '" y2="' + by.toFixed(1) + '" stroke="#16181d" stroke-width=".8"/><circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="1.8" fill="#16181d"/>'; }});
    marks.forEach(([p, x, y, bx, by, r]) => {{
      s += '<circle cx="' + bx.toFixed(1) + '" cy="' + by.toFixed(1) + '" r="' + r + '" fill="' + p.c + '" stroke="#fff" stroke-width="1"/>';
      s += '<text x="' + bx.toFixed(1) + '" y="' + (by + (p.big ? 3.2 : 2.8)).toFixed(1) + '" font-size="' + (p.big ? 9 : 7.6) + '" font-weight="800" fill="#fff" text-anchor="middle" font-family="Body">' + p.n + '</text>'; }});
    return s;
  }}
  let w = draw('world', 320, 102, {{lon0: -128, lon1: 180, lat0: 74, lat1: -46}}, 3.2, pins.filter(p => !inInset(p)), true);
  w += '<g transform="translate(118 78)"><rect width="104" height="22" rx="3" fill="#1a1236"/><text x="6" y="14.5" font-size="8.5" font-weight="800" fill="#fff" font-family="Body">OFF MAP: {", ".join(map(str, OFFMAP))}</text></g>';
  document.getElementById('world').innerHTML = w;
  document.getElementById('inset').innerHTML = draw('inset', 320, 94, INSET, 3.8, pins.filter(inInset), false);
}})();
"""

CHECKJS = """
(function () {
  const bad = [];
  document.querySelectorAll('.foot, .bt, .sp, .tl, .check, .lead, .card, .kick, .srcr, .meta, .acols > div, .bottom, .keys, .rk').forEach(el => {
    if (el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1) bad.push(el.className + '[' + (el.scrollWidth - el.clientWidth) + 'x' + (el.scrollHeight - el.clientHeight) + ']:' + (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 34));
  });
  const pg = document.querySelector('.page'); const last = document.querySelector('.foot').getBoundingClientRect();
  if (last.bottom > 1024) bad.push('PAGE-BOTTOM:' + last.bottom);
  document.body.setAttribute('data-overflow', bad.join(' | '));
})();
"""

CSS = open(os.path.join(ROOT, "tools", "style.css"), encoding="utf-8").read()

PAGE = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>The One-Day World · Saturday 21 November 2026</title><style>{CSS}</style></head>
<body><div class="page">
<header class="mast">
  <div class="dial">{art.daydial(66)}</div>
  <div class="mt">
    <div class="kick1">THE ONE-DAY WORLD &nbsp;·&nbsp; {TOTAL} STORIES · 6 REGIONS · {DRAWN} ILLUSTRATED · EVERY ITEM SOURCED</div>
    <div class="title">Saturday 21 November 2026</div>
    <div class="sub">Every story took place 00:00–24:00 UTC on Saturday 21 November 2026. One item marked REPORT: an earlier event first made public today.</div>
  </div>
  <div class="trust"><div class="th">HOW TO READ</div>
    <div><span class="bd s" style="background:#1f5fbf">1</span>story number, same on map</div>
    <div><span class="claim">CLAIM</span>one side’s word, attributed</div>
    <div><span class="off"></span>official statement or data</div>
    <div><span class="rep">REPORT</span>first reported today</div></div>
</header>
<div class="rbar">{region_bar}</div>
<div class="keys"><div class="tk"><b>TOPICS</b> &nbsp;{topic_key}</div><div class="tk2">Bar widths are true shares of the {TOTAL} stories</div></div>
<div class="tline"><div class="tlh">THE DAY<br>IN UTC</div>{timeline}</div>
<div class="leads">{leads}</div>
<div class="cards">{cards}</div>
<div class="bottom">
  <div class="mapbox"><div class="mh">WHERE IT HAPPENED <span>colour = region · number = story</span></div>
    <svg id="world" width="320" height="102" viewBox="0 0 320 102" xmlns="http://www.w3.org/2000/svg"></svg>
    <div class="mh2">EUROPE &amp; MIDDLE EAST, ZOOMED</div>
    <svg id="inset" width="320" height="94" viewBox="0 0 320 94" xmlns="http://www.w3.org/2000/svg"></svg></div>
  <div class="also"><div class="ah">ALSO ON SATURDAY, BY REGION</div>
    <div class="acols"><div>{briefs_l}</div><div>{briefs_r}</div></div></div>
</div>
<div class="sport"><div class="sb">{art.scoreboard()}<div>SPORT</div></div><div class="spg">{sport}</div></div>
<div class="check"><b class="ck">DATE CHECK</b> Not counted: {NOT_COUNTED}</div>
<footer class="foot"><b>Key:</b> {e(SOURCE_KEY)}</footer>
</div><script>{MAPJS}</script><script>{CHECKJS}</script></body></html>'''

open(os.path.join(ROOT, "poster", "index.html"), "w", encoding="utf-8").write(PAGE)
print("stories", TOTAL, "drawn", DRAWN, "regions", COUNT, "topics", {k: v for k, v in TCOUNT.items() if v})
