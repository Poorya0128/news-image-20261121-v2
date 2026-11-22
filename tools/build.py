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

REGIONS = {
    "EU": ("Europe", "#2f5aa8"),
    "ME": ("Middle East", "#b3122e"),
    "AM": ("Americas", "#cf5a17"),
    "AP": ("Asia-Pacific", "#0f7c86"),
    "AF": ("Africa", "#8a5a12"),
    "GL": ("Global", "#5b3a8c"),
}

# ---------------------------------------------------------------- 3 illustrated leads
LEADS = [
    dict(k="baltic", r="EU", kick="Baltic Sea · Ukraine war", src="AFP · REUTERS · FINNISH MoD", lon=26.9, lat=60.1,
         art=art.baltic(), h="Drones set Russian cargo ship ablaze off Finland",
         p="The US-sanctioned Sparta II burned west of Suursaari island. Finland says the attack was likely Ukrainian; all 16 crew were evacuated as the ship drifted into Finnish waters."),
    dict(k="hormuz", r="ME", kick="Middle East · Iran war", src="AP · UKMTO · AL JAZEERA", lon=56.3, lat=26.6,
         art=art.hormuz(), h="Three tankers hit in the Strait of Hormuz",
         p="Apparent Iranian strikes on shipping, as Tehran unveils a dual-missile launcher underground and hosts Qatari mediators."),
    dict(k="sinaloa", r="AM", kick="Mexico · cartels", src="AP · REUTERS · CBS", lon=-108.4, lat=25.6,
         art=art.sinaloa(), h="“El Chapo Isidro” captured as 11 die in Sinaloa",
         p="Fausto Isidro Meza Flores, on the FBI’s Ten Most Wanted list, was seized in Guasave. Four soldiers and seven gunmen were killed."),
]

# ---------------------------------------------------------------- 8 drawn cards
CARDS = [
    dict(k="kryvyi", r="EU", kick="Ukraine war", src="AP · UKR AIR FORCE", lon=33.4, lat=47.9, art=art.kryvyi(),
         h="Missiles kill 2 in Zelensky’s home city", p="A boy of 7 and a medic die in Kryvyi Rih."),
    dict(k="cop", r="GL", kick="Climate · Antalya", src="REUTERS · GUARDIAN", lon=30.7, lat=36.9, art=art.cop31(),
         h="COP31 deadlocked over fossil fuels", p="Talks halted for the night, a day over time."),
    dict(k="robots", r="GL", kick="UN · Geneva", src="REUTERS · AP · NPR", lon=6.1, lat=46.2, art=art.robots(),
         h="“Killer robot” talks end without treaty", p="128 states agree only to “elaborate” rules."),
    dict(k="bepi", r="GL", kick="Space · Mercury", src="ESA · AP · NATURE", lon=None, lat=None, art=art.bepi(),
         h="BepiColombo enters orbit around Mercury", p="37-minute burn ends an eight-year cruise."),
    dict(k="quake", r="AP", kick="Banda Sea · Indonesia", src="USGS · GFZ", lon=127.5, lat=-7.7, art=art.quake(),
         h="Deep M6.8 quake felt in Timor and Darwin", p="USGS green alert; no tsunami threat."),
    dict(k="france", r="EU", kick="France · protests", src="REUTERS · BLOOMBERG", lon=2.35, lat=48.9, art=art.france(),
         h="Sixth weekend of cost-of-living marches", p="Turnout dips after wage and school pledges."),
    dict(k="gaza", r="ME", kick="Gaza City", src="REUTERS · GAZA MoH", lon=34.45, lat=31.5, art=art.gaza(),
         h="Strike on food-aid vehicle kills three", p="WCK says the truck was not its own."),
    dict(k="eu", r="EU", kick="EU · Brussels", src="AFP · POLITICO", lon=4.35, lat=50.85, art=art.eubudget(),
         h="Costa cuts €204bn from EU budget plan", p="Adds a Big Tech tax; Merz says still too high."),
]

# ---------------------------------------------------------------- briefs
# (key, region, place, text, source, flag, lon, lat)  flag: "claim" | "official" | ""
BRIEFS = [
    ("heli", "EU", "Finland", "Russian helicopter suspected over Loviisa", "DW", "", 26.2, 60.4),
    ("blacksea", "EU", "Black Sea", "Russia says it hit a Ukrainian cargo ship", "SKY", "claim", 31.5, 44.0),
    ("kyiv", "EU", "Kyiv", "UK’s Streeting: Putin a “cold-blooded killer”", "ITV", "", 30.5, 50.4),
    ("lisbon", "EU", "Lisbon", "Workers march in rain for pay, housing", "EURONEWS", "", -9.1, 38.7),
    ("ams", "EU", "Amsterdam", "UK PM Burnham meets Dutch PM Jetten", "GOV.UK", "official", 4.9, 52.4),
    ("tories", "EU", "London", "Tories, universities attack EU deal", "INDEPENDENT", "", -0.1, 51.5),
    ("pope", "EU", "Vatican", "Pope warns of “enormous” tech risks", "VATICAN", "official", 12.45, 41.9),
    ("icj", "EU", "Paris", "France seeks UN action on Myanmar ruling", "TOI", "", 2.35, 48.9),
    ("mq9", "ME", "Hormuz", "IRGC says it downed 58th US MQ-9", "TASNIM", "claim", 56.0, 27.2),
    ("aoun", "ME", "Beirut", "Aoun demands Israeli exit, rebukes Iran", "ARAB NEWS", "", 35.5, 33.9),
    ("unifil", "ME", "S. Lebanon", "UNIFIL starts handing posts to army", "ANADOLU", "", 35.3, 33.2),
    ("israel", "ME", "Israel", "Bennett backs unity rule under Eisenkot", "TOI", "", 34.8, 32.1),
    ("dar", "ME", "Islamabad", "Dar hopes for early US–Iran deal", "DAILY TIMES", "", 73.0, 33.7),
    ("houthi", "ME", "Yemen", "Houthis said to fortify Bab al-Mandeb", "ISW", "claim", 43.4, 12.8),
    ("fbi", "AM", "Washington", "Trump plays down FBI database hack", "UPI · AXIOS", "", -77.0, 38.9),
    ("iran", "AM", "Washington", "Trump wants “permanent” Iran deal", "CBS", "", -77.4, 39.4),
    ("taiwan_ca", "AM", "Halifax", "Taiwan warns Carney on China ties", "AP", "", -63.6, 44.6),
    ("ca_us", "AM", "Halifax", "Canada: “no change” in US military ties", "CP", "", -63.2, 45.0),
    ("bd", "AP", "Dhaka", "More troops sent to halt arson attacks", "REUTERS", "", 90.4, 23.8),
    ("kr", "AP", "Seoul", "DP eyes 3 Dec chief-justice impeachment", "KOREA HERALD", "", 127.0, 37.5),
    ("tw", "AP", "Taipei", "2 PLA aircraft, 7 ships, 4 balloons", "TAIWAN MND", "official", 121.5, 25.0),
    ("nk", "AP", "Pyongyang", "State media: Kim tours school factories", "AFP · KCNA", "", 125.8, 39.0),
    ("au", "AP", "Australia", "Thousands rally for midwife home births", "ABC", "", 151.0, -33.9),
    ("in", "AP", "Kharagpur", "Modi marks IIT’s 75th: “nation first”", "THE HINDU", "", 87.3, 22.3),
    ("eg", "AF", "Aswan", "Sisi urges overhaul of global finance", "DNE", "", 32.9, 24.1),
    ("sennar", "AF", "Sudan", "Sennar state imposes night curfew", "TAMAZUJ", "official", 33.6, 13.6),
    ("rsf", "AF", "Sudan", "RSF accused of killing 3 children", "ANADOLU", "claim", 28.5, 12.0),
    ("ng", "AF", "Ibadan", "Tinubu mutes rally after boat deaths", "PREMIUM TIMES", "", 3.9, 7.4),
    ("za", "AF", "S. Africa", "Tributes for Phumzile Mlambo-Ngcuka", "AFP", "", 28.0, -26.2),
]

# ---------------------------------------------------------------- sport (all finished before 24:00 UTC)
SPORT = [
    ("eng", "EU", "Rugby", "England 37–12 NZ, a record"),
    ("ire", "EU", "Rugby", "Ireland 20–17 S. Africa"),
    ("sco", "EU", "Rugby", "Scotland 67–5 Japan"),
    ("wal", "EU", "Rugby", "Wales 26–29 Australia"),
    ("epl", "EU", "Premier League", "Chelsea 1–4 Leeds"),
    ("new", "EU", "Premier League", "Newcastle 2–2 Arsenal"),
    ("cric", "AP", "Cricket", "India 486/4 v NZ, day 3"),
    ("t20", "AP", "T20", "Australia beat England"),
    ("cfb", "AM", "College football", "Nebraska 31–28 Ohio St."),
    ("ufc", "ME", "UFC Doha", "Stirling KOs Procházka"),
]

TIMELINE = [
    ("~04:00", "Geneva arms talks end"),
    ("Overnight", "148 drones hit Ukraine"),
    ("Morning", "Sparta II set ablaze"),
    ("09:42", "M6.8 Banda Sea quake"),
    ("10:34", "Heli breach suspected"),
    ("15:00", "EPL kick-offs"),
    ("18:24", "Mercury orbit burn"),
    ("Night", "COP31 halted, no deal"),
]

NOT_COUNTED = ("<b>Friday 20 Nov:</b> missiles in Poland · Peru M6.7 quake · Brazil storm · UK–EU deal. "
               "<b>Ended after 00:00 UTC Sun:</b> Las Vegas GP · Sudamericana final.")

# ---------------------------------------------------------------- numbering + checks
ORDER = ([("L", x["k"], x["r"]) for x in LEADS] + [("C", x["k"], x["r"]) for x in CARDS]
         + [("B", b[0], b[1]) for b in BRIEFS] + [("S", s[0], s[1]) for s in SPORT])
N = {k: i + 1 for i, (_, k, _) in enumerate(ORDER)}
assert len(N) == len(ORDER), "duplicate keys"
TOTAL = len(ORDER)
COUNT = {r: sum(1 for *_, rr in ORDER if rr == r) for r in REGIONS}
assert sum(COUNT.values()) == TOTAL
DRAWN = len(LEADS) + len(CARDS) + 1  # + scoreboard
for b in BRIEFS:
    assert len(b[2]) + len(b[3]) <= 50, (len(b[2]) + len(b[3]), b)  # one line at 12px


def badge(n, color, size="b"):
    return f'<span class="bd {size}" style="background:{color}">{n}</span>'


def rc(r):
    return REGIONS[r][1]


# ---------------------------------------------------------------- html pieces
region_bar = "".join(
    f'<div style="flex:{COUNT[r] + 2};background:{c}">{e(name)} {COUNT[r]}</div>' for r, (name, c) in REGIONS.items())

timeline = "".join(f'<div class="tl"><b>{e(t)}{" UTC" if t[0].isdigit() or t[0] == "~" else ""}</b>{e(x)}</div>' for t, x in TIMELINE)

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

sport = "".join(f'<div class="sp">{badge(N[k], "#16181d", "s")}<div><b>{e(c)}</b>{e(t)}</div></div>' for k, r, c, t in SPORT)

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

MAPJS = f"""
(function () {{
  const W = 300, H = 150, LON0 = -128, LON1 = 158, LAT0 = 74, LAT1 = -46;
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
  const off = {{1: [-4, -13], 2: [16, -6], 3: [-2, 15], 4: [16, -2], 5: [-6, 16], 6: [-16, 8], 8: [12, 12], 9: [-16, -12], 10: [12, 14], 11: [-4, -16]}};
  pins.filter(p => p.big).forEach(p => {{ const [x, y] = P(p.lon, p.lat); const d = off[p.n] || [12, -10];
    const bx = x + d[0], by = y + d[1];
    s += '<line x1="' + x + '" y1="' + y + '" x2="' + bx + '" y2="' + by + '" stroke="#16181d" stroke-width=".9"/>';
    s += '<circle cx="' + x + '" cy="' + y + '" r="2.2" fill="#16181d"/>';
    s += '<circle cx="' + bx + '" cy="' + by + '" r="7.2" fill="' + p.c + '" stroke="#fff" stroke-width="1.2"/>';
    s += '<text x="' + bx + '" y="' + (by + 3.4) + '" font-size="' + (p.n > 9 ? 8.5 : 9.5) + '" font-weight="800" fill="#fff" text-anchor="middle" font-family="Body">' + p.n + '</text>'; }});
  s += '<g transform="translate(4 112)"><rect width="74" height="34" rx="3" fill="#1a1236"/><circle cx="60" cy="17" r="10" fill="#9b948c"/>' +
       '<circle cx="12" cy="11" r="7.2" fill="{REGIONS["GL"][1]}" stroke="#fff" stroke-width="1.2"/><text x="12" y="14.4" font-size="9.5" font-weight="800" fill="#fff" text-anchor="middle" font-family="Body">{N["bepi"]}</text>' +
       '<text x="24" y="14" font-size="7.5" font-weight="800" fill="#fff" font-family="Body">OFF MAP</text><text x="6" y="29" font-size="7.5" font-weight="800" fill="#f2c94c" font-family="Body">AT MERCURY</text></g>';
  document.getElementById('map').innerHTML = s;
}})();
"""

CSS = open(os.path.join(ROOT, "tools", "style.css"), encoding="utf-8").read()

PAGE = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>The One-Day World · Saturday 21 November 2026</title><style>{CSS}</style></head>
<body><div class="page">
<header class="mast">
  <div class="dial">{art.daydial(66)}<div class="doy">DAY 325 · 40 LEFT</div></div>
  <div class="mt">
    <div class="kick1">THE ONE-DAY WORLD &nbsp;·&nbsp; {TOTAL} STORIES · 6 REGIONS + SPACE · {DRAWN} DRAWN · ONE PAGE</div>
    <div class="title">Saturday 21 November 2026</div>
    <div class="sub">Everything on this page happened, or was first reported, on Saturday 21 November 2026 (UTC). Every item names its source.</div>
  </div>
  <div class="trust"><div class="th">HOW TO READ</div>
    <div><span class="bd s" style="background:#2f5aa8">1</span> story no. = map pin</div>
    <div><span class="claim">CLAIM</span> one side’s word, attributed</div>
    <div><span class="off"></span> official data or statement</div>
    <div class="mk">Markets closed: it’s Saturday</div></div>
</header>
<div class="rbar">{region_bar}</div>
<div class="tline"><div class="tlh">THE DAY<br>IN UTC</div>{timeline}</div>
<div class="leads">{leads}</div>
<div class="cards">{cards}</div>
<div class="bottom">
  <div class="mapbox"><div class="mh">WHERE IT HAPPENED</div>
    <svg id="map" width="300" height="150" viewBox="0 0 300 150" xmlns="http://www.w3.org/2000/svg"></svg>
    <div class="lg">{legend}</div>
    <div class="mn">Big pins: stories 1–11 · dots: briefs</div></div>
  <div class="also"><div class="ah">ALSO ON SATURDAY 21 NOVEMBER</div>
    <div class="acols"><div>{briefs_l}</div><div>{briefs_r}</div></div></div>
</div>
<div class="sport"><div class="sb">{art.scoreboard()}<div>SPORT<br><small>FULL TIME</small></div></div><div class="spg">{sport}</div></div>
<div class="check"><b class="ck">DATE CHECK</b> Not counted: {NOT_COUNTED}</div>
<footer class="foot"><div><b>Reads at three sizes:</b> date and 3 leads at thumbnail size · {DRAWN} pictures at half size · all {TOTAL} stories at full size</div>
<div>Sources: AP · Reuters · AFP · USGS · ESA · GOV.UK · Vatican · Taiwan MND · ISW · and outlets named per item</div></footer>
</div><script>{MAPJS}</script></body></html>'''

open(os.path.join(ROOT, "poster", "index.html"), "w", encoding="utf-8").write(PAGE)
print("stories", TOTAL, "drawn", DRAWN, "regions", COUNT)
