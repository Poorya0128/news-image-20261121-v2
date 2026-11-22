#!/usr/bin/env python3
"""Builds poster/index.html: the 50-story front page for Saturday 21 November 2026.

All story data lives here. Numbers, region counts, map pins and the headline
count are computed from this data and checked, so the page can never disagree
with itself. Render with tools/render.sh afterwards.
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

# Region = WHERE the event happened (UN M49 grouping; Western Asia incl. Turkey = "Middle East").
REGIONS = {
    "EU": ("Europe", "#2f5aa8"),
    "ME": ("Middle East", "#b3122e"),
    "AM": ("Americas", "#cf5a17"),
    "AP": ("Asia-Pacific", "#0f7c86"),
    "AF": ("Africa", "#8a5a12"),
    "SP": ("Space", "#5b3a8c"),
}

# ---------------------------------------------------------------- 3 illustrated leads
LEADS = [
    dict(k="baltic", r="EU", kick="Baltic Sea · Ukraine war", src="AFP · REUTERS · FINNISH MoD", lon=26.9, lat=60.1,
         art=art.baltic(), h="Drones set Russian cargo ship ablaze off Finland",
         p="The US-sanctioned Sparta II burned west of Suursaari island. Finland says the attack was likely Ukrainian; all 16 crew were evacuated as the ship drifted into Finnish waters."),
    dict(k="hormuz", r="ME", kick="Middle East · Iran war", src="REUTERS · UKMTO · AP", lon=56.3, lat=26.6,
         art=art.hormuz(), h="Two tankers hit by projectiles off Hormuz",
         p="UKMTO reports both near Oman’s Khasab; no casualties. Iran’s navy says a third hit a mine (unverified)."),
    dict(k="sinaloa", r="AM", kick="Mexico · cartels", src="AP · REUTERS · CBS", lon=-108.4, lat=25.6,
         art=art.sinaloa(), h="“El Chapo Isidro” captured as 11 die in Sinaloa",
         p="Fausto Isidro Meza Flores, on the FBI’s Ten Most Wanted list, was seized in Guasave; 4 soldiers and 7 gunmen died."),
]

# ---------------------------------------------------------------- 8 drawn cards
CARDS = [
    dict(k="kryvyi", r="EU", kick="Ukraine war", src="AP · UKR AIR FORCE", lon=33.4, lat=47.9, art=art.kryvyi(),
         h="Missiles kill boy, 7, and medic in Kryvyi Rih", p="AP: 60 hurt. Kyiv: 117 of 148 drones downed."),
    dict(k="cop", r="ME", kick="Climate · Antalya", src="REUTERS · GUARDIAN", lon=30.7, lat=36.9, art=art.cop31(),
         h="COP31 deadlocked over the move away from fossil fuels", p="Talks halted for the night, a day over time."),
    dict(k="robots", r="EU", kick="UN talks · Geneva", src="REUTERS · AP · NPR", lon=6.1, lat=46.2, art=art.robots(),
         h="UN “killer robot” talks end without a treaty mandate", p="128 states agree only to “elaborate” rules."),
    dict(k="bepi", r="SP", kick="Space · ESA–JAXA", src="ESA · AP · NATURE", lon=None, lat=None, art=art.bepi(),
         h="BepiColombo enters orbit around Mercury after 8 years", p="A 37-minute engine burn from 18:24 UTC."),
    dict(k="quake", r="AP", kick="Banda Sea · Indonesia", src="USGS · GFZ", lon=127.5, lat=-7.7, art=art.quake(),
         h="Deep M6.8 quake shakes Timor-Leste and Darwin", p="USGS green alert; no tsunami threat."),
    dict(k="france", r="EU", kick="France · protests", src="REUTERS · BLOOMBERG", lon=2.35, lat=48.9, art=art.france(),
         h="France marches for a sixth weekend over living costs", p="Turnout dips after wage and school pledges."),
    dict(k="gaza", r="ME", kick="Gaza City", src="REUTERS · GAZA MoH", lon=34.45, lat=31.5, art=art.gaza(),
         h="Israeli strike on a vehicle kills three in Gaza City", p="World Central Kitchen: not its vehicle."),
    dict(k="eu", r="EU", kick="EU · Brussels", src="AFP · POLITICO", lon=4.35, lat=50.85, art=art.eubudget(),
         h="Costa cuts €204bn from the EU’s 2028–34 budget plan", p="Adds a Big Tech tax; Merz: still too high."),
]

# ---------------------------------------------------------------- briefs
# (key, region, place, text, source, flag, lon, lat)  flag: "claim" | "official" | ""
BRIEFS = [
    ("heli", "EU", "Finland", "Russian helicopter suspected over Loviisa", "DW", "", 26.2, 60.4),
    ("blacksea", "EU", "Black Sea", "Russia says it hit a Ukrainian cargo ship", "SKY", "claim", 31.5, 44.0),
    ("kyiv", "EU", "Kyiv", "UK’s Streeting: Putin a “cold-blooded killer”", "ITV", "", 30.5, 50.4),
    ("lisbon", "EU", "Lisbon", "Workers march in rain for pay, housing", "EURONEWS", "", -9.1, 38.7),
    ("ams", "EU", "Amsterdam", "Burnham meets Dutch PM Jetten", "GOV.UK", "official", 4.9, 52.4),
    ("tories", "EU", "London", "Tories, universities attack EU deal", "INDEPENDENT", "", -0.1, 51.5),
    ("pope", "EU", "Vatican", "Pope warns of “enormous” tech risks", "VATICAN", "official", 12.45, 41.9),
    ("icj", "EU", "Paris", "France seeks UN action on Myanmar ruling", "TOI", "", 2.35, 48.9),
    ("mq9", "ME", "Hormuz", "IRGC says it downed 58th US MQ-9", "TASNIM", "claim", 56.0, 27.2),
    ("aoun", "ME", "Beirut", "Aoun demands Israeli exit, rebukes Iran", "ARAB NEWS", "", 35.5, 33.9),
    ("unifil", "ME", "S. Lebanon", "UNIFIL starts handing posts to army", "ANADOLU", "", 35.3, 33.2),
    ("israel", "ME", "Israel", "Bennett backs unity rule under Eisenkot", "TOI", "", 34.8, 32.1),
    ("houthi", "ME", "Yemen", "Houthis said to fortify Bab al-Mandeb", "ISW", "claim", 43.4, 12.8),
    ("peru", "AM", "Peru", "M6.7 quake at 00:09 UTC; no damage", "USGS · AP", "official", -76.0, -10.9),
    ("fbi", "AM", "Washington", "Trump plays down FBI database hack", "UPI · AXIOS", "", -77.0, 38.9),
    ("iran", "AM", "Washington", "Trump wants “permanent” Iran deal", "CBS", "", -77.4, 39.4),
    ("halifax", "AM", "Halifax", "Taiwan warns Carney; Ottawa: US ties intact", "AP · CP", "", -63.6, 44.6),
    ("dar", "AP", "Islamabad", "Dar hopes for early US–Iran deal", "DAILY TIMES", "", 73.0, 33.7),
    ("bd", "AP", "Dhaka", "More troops sent to halt arson attacks", "REUTERS", "", 90.4, 23.8),
    ("kr", "AP", "Seoul", "DP eyes 3 Dec chief-justice impeachment", "KOREA HERALD", "", 127.0, 37.5),
    ("tw", "AP", "Taipei", "2 PLA aircraft, 7 ships, 4 balloons", "TAIWAN MND", "official", 121.5, 25.0),
    ("nk", "AP", "Pyongyang", "State media: Kim tours school factories", "AFP · KCNA", "", 125.8, 39.0),
    ("au", "AP", "Australia", "Thousands rally for midwife home births", "ABC", "", 151.0, -33.9),
    ("in", "AP", "Kharagpur", "Modi marks IIT’s 75th: “nation first”", "THE HINDU", "", 87.3, 22.3),
    ("eg", "AF", "Aswan", "Sisi urges overhaul of global finance", "DNE", "", 32.9, 24.1),
    ("sudan", "AF", "Sudan", "Sennar curfew; RSF accused of killings", "TAMAZUJ", "claim", 33.6, 13.6),
    ("ng", "AF", "Ibadan", "Tinubu mutes rally after boat deaths", "PREMIUM TIMES", "", 3.9, 7.4),
    ("za", "AF", "S. Africa", "Tributes for Phumzile Mlambo-Ngcuka", "AFP", "", 28.0, -26.2),
]

# ---------------------------------------------------------------- sport (all finished before 24:00 UTC)
# (key, region by venue, competition, result, source)
SPORT = [
    ("eng", "EU", "Rugby · Twickenham", "England 37–12 NZ, a record", "SKY"),
    ("ire", "EU", "Rugby · Dublin", "Ireland 20–17 S. Africa", "AP"),
    ("sco", "EU", "Rugby · Murrayfield", "Scotland 67–5 Japan", "AP"),
    ("wal", "EU", "Rugby · Cardiff", "Wales 26–29 Australia", "SKY"),
    ("epl", "EU", "Premier League", "Chelsea 1–4 Leeds", "ESPN"),
    ("new", "EU", "Premier League", "Newcastle 2–2 Arsenal", "ESPN"),
    ("cric", "AP", "Test · Wellington", "India 486/4 v NZ, day 3", "AFP"),
    ("t20", "AP", "T20 · Melbourne", "Australia beat England", "ESPN"),
    ("cfb", "AM", "College football", "Nebraska 31–28 Ohio St.", "NBC"),
    ("ufc", "ME", "UFC · Doha", "Stirling KOs Procházka", "UFC"),
]

TIMELINE = [
    ("00:09", "M6.7 quake, Peru", "peru"),
    ("~04:00", "Geneva arms talks end", "robots"),
    ("Morning", "Sparta II set ablaze", "baltic"),
    ("09:42", "M6.8 Banda Sea quake", "quake"),
    ("10:34", "Suspected heli breach", "heli"),
    ("15:00", "Chelsea–Leeds kick-off", "epl"),
    ("18:24", "Mercury orbit burn", "bepi"),
    ("Night", "COP31 halted, no deal", "cop"),
]

NOT_COUNTED = ("<b>Before 00:00 UTC Sat:</b> missiles in Poland · Brazil storm · UK–EU deal. "
               "<b>After 24:00 UTC Sat:</b> Las Vegas GP · Sudamericana final. "
               "<b>Counted:</b> Peru quake, 00:09 UTC Sat (19:09 Fri local).")

# ---------------------------------------------------------------- numbering + checks
ORDER = ([("L", x["k"], x["r"]) for x in LEADS] + [("C", x["k"], x["r"]) for x in CARDS]
         + [("B", b[0], b[1]) for b in BRIEFS] + [("S", s[0], s[1]) for s in SPORT])
N = {k: i + 1 for i, (_, k, _) in enumerate(ORDER)}
assert len(N) == len(ORDER), "duplicate keys"
TOTAL = len(ORDER)
COUNT = {r: sum(1 for *_, rr in ORDER if rr == r) for r in REGIONS}
assert sum(COUNT.values()) == TOTAL
DRAWN = len(LEADS) + len(CARDS)  # illustrated stories (scoreboard not counted)
for b in BRIEFS:
    assert len(b[2]) + len(b[3]) <= 52, (len(b[2]) + len(b[3]), b)  # one line at 12px


def badge(n, color, size="b"):
    return f'<span class="bd {size}" style="background:{color}">{n}</span>'


def rc(r):
    return REGIONS[r][1]


# ---------------------------------------------------------------- html pieces
region_bar = "".join(
    f'<div style="flex:{COUNT[r] + 2};background:{c}">{e(name)} {COUNT[r]}</div>' for r, (name, c) in REGIONS.items())

REG = {k: r for _, k, r in ORDER}
timeline = "".join(f'<div class="tl"><b>{badge(N[k], rc(REG[k]), "t")}{e(t)}{" UTC" if t[0].isdigit() or t[0] == "~" else ""}</b>{e(x)}</div>' for t, x, k in TIMELINE)

leads = "".join(f'''<div class="lead">
  <div class="art">{x["art"]}</div>
  <div class="meta">{badge(N[x["k"]], rc(x["r"]))}<span class="kick" style="color:{rc(x["r"])}">{e(x["kick"])}</span><span class="srcr">{e(x["src"])}</span></div>
  <h1>{e(x["h"])}</h1><p>{e(x["p"])}</p></div>''' for x in LEADS)

cards = "".join(f'''<div class="card">
  <div class="art2">{x["art"]}</div>
  <div class="meta">{badge(N[x["k"]], rc(x["r"]), "s")}<span class="kick" style="color:{rc(x["r"])}">{e(x["kick"])}</span><span class="srcr">{e(x["src"])}</span></div>
  <h2>{e(x["h"])}</h2><p>{e(x["p"])}</p></div>''' for x in CARDS)


def brief_html(b):
    k, r, place, text, src, flag, *_ = b
    tag = '<span class="claim">CLAIM</span>' if flag == "claim" else ('<span class="off"></span>' if flag == "official" else "")
    return (f'<div class="br">{badge(N[k], rc(r), "s")}<div class="bt"><b style="color:{rc(r)}">{e(place)}:</b> {e(text)} '
            f'{tag}<span class="bs">{e(src)}</span></div></div>')


half = (len(BRIEFS) + 1) // 2
briefs_l = "".join(brief_html(b) for b in BRIEFS[:half])
briefs_r = "".join(brief_html(b) for b in BRIEFS[half:])

sport = "".join(f'<div class="sp">{badge(N[k], rc(r), "s")}<div><b>{e(c)}</b>{e(t)} <span class="bs">{e(src)}</span></div></div>' for k, r, c, t, src in SPORT)

pins = []
for x in LEADS + CARDS:
    if x["lon"] is not None:
        pins.append(dict(n=N[x["k"]], lon=x["lon"], lat=x["lat"], c=rc(x["r"]), big=True))
for b in BRIEFS:
    pins.append(dict(n=N[b[0]], lon=b[6], lat=b[7], c=rc(b[1]), big=False))

legend = "".join(f'<span><i style="background:{c}"></i>{e(n)}</span>' for n, c in REGIONS.values())

V1 = open(os.path.join(ROOT, "build", "index_v1.html"), encoding="utf-8").read()
LAND = re.search(r"const land = (\[.*?\]);\n  const water", V1, re.S).group(1)
WATER = re.search(r"const water = (\[.*?\]);\n  const poly", V1, re.S).group(1)

# absolute callout positions (map px) so clustered pins never overlap
CALL = {N[k]: xy for k, xy in {"france": (116, 24), "eu": (136, 10), "robots": (124, 52), "baltic": (162, 9),
        "kryvyi": (206, 30), "cop": (162, 72), "gaza": (192, 78), "hormuz": (230, 54), "sinaloa": (22, 88),
        "quake": (302, 124)}.items()}
assert set(CALL) == {N[x["k"]] for x in LEADS + CARDS if x["lon"] is not None}

MAPJS = f"""
(function () {{
  const W = 320, H = 160, LON0 = -128, LON1 = 158, LAT0 = 74, LAT1 = -46;
  const sx = W / (LON1 - LON0), sy = H / (LAT0 - LAT1);
  const P = (lon, lat) => [(lon - LON0) * sx, (LAT0 - lat) * sy];
  const land = {LAND};
  const water = {WATER};
  const inside = (x, y, poly) => {{ let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {{
      const [xi, yi] = poly[i], [xj, yj] = poly[j];
      if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) c = !c; }} return c; }};
  let s = '<rect width="' + W + '" height="' + H + '" fill="#eef3f6"/>';
  const step = 3.6;
  for (let py = step / 2; py < H; py += step) for (let px = step / 2; px < W; px += step) {{
    const lon = LON0 + px / sx, lat = LAT0 - py / sy;
    if (land.some(p => inside(lon, lat, p)) && !water.some(p => inside(lon, lat, p)))
      s += '<circle cx="' + px.toFixed(1) + '" cy="' + py.toFixed(1) + '" r="1.25" fill="#b9b2a0"/>';
  }}
  const pins = {json.dumps(pins)};
  pins.filter(p => !p.big).forEach(p => {{ const [x, y] = P(p.lon, p.lat);
    s += '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="2.6" fill="' + p.c + '" stroke="#fff" stroke-width=".8"/>'; }});
  const call = {json.dumps(CALL)};
  pins.filter(p => p.big).forEach(p => {{ const [x, y] = P(p.lon, p.lat); const d = call[p.n];
    const bx = d[0], by = d[1];
    s += '<line x1="' + x + '" y1="' + y + '" x2="' + bx + '" y2="' + by + '" stroke="#16181d" stroke-width=".9"/>';
    s += '<circle cx="' + x + '" cy="' + y + '" r="2.2" fill="#16181d"/>';
    s += '<circle cx="' + bx + '" cy="' + by + '" r="7.2" fill="' + p.c + '" stroke="#fff" stroke-width="1.2"/>';
    s += '<text x="' + bx + '" y="' + (by + 3.4) + '" font-size="' + (p.n > 9 ? 8.5 : 9.5) + '" font-weight="800" fill="#fff" text-anchor="middle" font-family="Body">' + p.n + '</text>'; }});
  s += '<g transform="translate(4 124)"><rect width="86" height="34" rx="3" fill="#1a1236"/><circle cx="72" cy="17" r="10" fill="#9b948c"/>' +
       '<circle cx="12" cy="11" r="7.2" fill="{REGIONS["SP"][1]}" stroke="#fff" stroke-width="1.2"/><text x="12" y="14.4" font-size="9.5" font-weight="800" fill="#fff" text-anchor="middle" font-family="Body">{N["bepi"]}</text>' +
       '<text x="23" y="14" font-size="8" font-weight="800" fill="#fff" font-family="Body">OFF MAP:</text><text x="6" y="28" font-size="8" font-weight="800" fill="#f2c94c" font-family="Body">AT MERCURY</text></g>';
  document.getElementById('map').innerHTML = s;
}})();
"""

CSS = open(os.path.join(ROOT, "tools", "style.css"), encoding="utf-8").read()

FIRST_B, LAST_B = N[BRIEFS[0][0]], N[BRIEFS[-1][0]]
PAGE = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>The One-Day World · Saturday 21 November 2026</title><style>{CSS}</style></head>
<body><div class="page">
<header class="mast">
  <div class="dial">{art.daydial(66)}<div class="doy">DAY 325 · 40 LEFT</div></div>
  <div class="mt">
    <div class="kick1">THE ONE-DAY WORLD &nbsp;·&nbsp; {TOTAL} STORIES · 5 REGIONS + SPACE · {DRAWN} ILLUSTRATED · ONE PAGE</div>
    <div class="title">Saturday 21 November 2026</div>
    <div class="sub">Everything on this page happened, or was first reported, on Saturday 21 November 2026 (UTC). Every item names its source.</div>
  </div>
  <div class="trust"><div class="th">HOW TO READ</div>
    <div><span class="bd s" style="background:#2f5aa8">1</span> story number, also on map</div>
    <div><span class="claim">CLAIM</span> one side’s word, attributed</div>
    <div><span class="off"></span> official data or statement</div>
    <div class="mk">Region = where it happened · times UTC</div></div>
</header>
<div class="rbar">{region_bar}</div>
<div class="tline"><div class="tlh">THE DAY<br>IN UTC</div>{timeline}</div>
<div class="leads">{leads}</div>
<div class="cards">{cards}</div>
<div class="bottom">
  <div class="mapbox"><div class="mh">WHERE IT HAPPENED</div>
    <svg id="map" width="320" height="160" viewBox="0 0 320 160" xmlns="http://www.w3.org/2000/svg"></svg>
    <div class="lg">{legend}</div>
    <div class="mn">Numbered pins: stories 1–11 · small dots: briefs {FIRST_B}–{LAST_B}</div></div>
  <div class="also"><div class="ah">ALSO ON SATURDAY 21 NOVEMBER</div>
    <div class="acols"><div>{briefs_l}</div><div>{briefs_r}</div></div></div>
</div>
<div class="sport"><div class="sb">{art.scoreboard()}<div>SPORT<br><small>FULL TIME</small></div></div><div class="spg">{sport}</div></div>
<div class="check"><b class="ck">DATE CHECK</b> Not counted: {NOT_COUNTED}</div>
<footer class="foot"><div><b>Reads at three sizes:</b> date and 3 leads at thumbnail size · {DRAWN} illustrated stories at half size · all {TOTAL} stories at full size</div>
<div>Sources: AP · Reuters · AFP · USGS · ESA · GOV.UK · Vatican · Taiwan MND · ISW · and outlets named per item</div></footer>
</div><script>{MAPJS}</script></body></html>'''

open(os.path.join(ROOT, "poster", "index.html"), "w", encoding="utf-8").write(PAGE)
print("stories", TOTAL, "drawn", DRAWN, "regions", COUNT)
