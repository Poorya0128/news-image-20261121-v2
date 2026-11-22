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
         p="Finland says the drones were likely Ukrainian. All 16 crew of the sanctioned ship were evacuated."),
    dict(k="hormuz", r="ME", t="War", kick="Strait of Hormuz", src="REUTERS · UKMTO · AP", lon=56.3, lat=26.6,
         art=art.hormuz(), h="Two tankers hit by projectiles off Hormuz",
         p="UKMTO: both near Oman’s Khasab, no casualties. Iran says a third hit a mine (unverified)."),
    dict(k="sinaloa", r="AM", t="Crime", kick="Sinaloa, Mexico", src="AP · REUTERS · CBS", lon=-108.4, lat=25.6,
         art=art.sinaloa(), h="“El Chapo Isidro” captured as 11 die in Sinaloa",
         p="FBI Ten Most Wanted fugitive Fausto Isidro Meza Flores seized; 4 soldiers, 7 gunmen killed."),
]

# ---------------------------------------------------------------- 8 drawn cards (each picture is specific to its story)
CARDS = [
    dict(k="kryvyi", r="EU", t="War", kick="Kryvyi Rih", src="AP · UKR AIR FORCE", lon=33.4, lat=47.9, art=art.kryvyi(),
         h="Russian missiles kill boy, 7, and medic, officials say", p="AP: 60 hurt. Kyiv: 117 drones downed.", claim=False),
    dict(k="cop", r="ME", t="Climate", kick="Antalya", src="REUTERS · GUARDIAN", lon=30.7, lat=36.9, art=art.cop31b(),
         h="COP31 deadlocked over the move away from fossil fuels", p="Halted for the night, a day over time."),
    dict(k="eu", r="EU", t="Economy", kick="Brussels", src="AFP · POLITICO", lon=4.35, lat=50.85, art=art.eubars(),
         h="Costa cuts €204bn from the EU’s 2028–34 budget plan", p="Plus a Big Tech tax; Merz objects."),
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
    ("heli", "EU", "War", "Finland", "Suspected heli incursion", "MoD", "official", 26.2, 60.4),
    ("blacksea", "EU", "War", "Black Sea", "Russia says ship hit", "SKY", "claim", 31.5, 44.0),
    ("front", "EU", "War", "Front", "116 clashes in a day", "UA ARMY", "claim", 37.2, 48.3),
    ("kyiv", "EU", "Politics", "Kyiv", "UK’s Streeting calls Putin a “killer”", "ITV", "", 30.5, 50.4),
    ("geneva", "EU", "Politics", "Geneva", "No killer-robot treaty", "REUTERS", "", 6.1, 46.2),
    ("france", "EU", "Society", "France", "6th weekend of protests", "REUTERS", "", 2.35, 48.9),
    ("aoun", "ME", "Politics", "Beirut", "Aoun demands Israeli exit", "ARAB NEWS", "", 35.5, 33.9),
    ("houthi", "ME", "War", "Yemen", "Houthis fortify coast", "ISW", "claim", 43.4, 12.8),
    ("peru", "AM", "Disaster", "Peru", "M6.7 quake, no damage", "USGS", "official", -76.0, -10.9),
    ("brazil", "AM", "Economy", "Brazil", "Lula defends fiscal bill", "RIO TIMES", "", -47.9, -15.8),
    ("fbi", "AM", "Crime", "US", "Trump plays down FBI hack", "AXIOS", "", -77.0, 38.9),
    ("iran", "AM", "Politics", "US", "Trump wants “permanent” Iran deal", "CBS", "", -77.4, 39.4),
    ("halifax", "AM", "Politics", "Halifax", "Taiwan warns Carney on China", "AP", "", -63.6, 44.6),
    ("in", "AP", "Science", "Kharagpur", "Google gives IIT $5m for AI", "PTI", "", 87.3, 22.3),
    ("bd", "AP", "Society", "Dhaka", "Troops sent to halt arson", "REUTERS", "", 90.4, 23.8),
    ("kr", "AP", "Politics", "Seoul", "Move to impeach top judge", "K. HERALD", "", 127.0, 37.5),
    ("nk", "AP", "Politics", "N. Korea", "Kim tours factories", "KCNA", "report", 125.8, 39.0),
    ("mama", "AP", "Culture", "Osaka", "BTS wins 5 MAMA awards", "K. HERALD", "", 135.5, 34.7),
    ("eg", "AF", "Politics", "Aswan", "Sisi urges finance reform", "DNE", "", 32.9, 24.1),
    ("sudan", "AF", "War", "Sudan", "RSF accused of killings", "AA", "claim", 33.6, 13.6),
    ("oyo", "AF", "Politics", "Congo", "Ruto at 4-way summit", "STATE HOUSE", "official", 15.9, -1.0),
    ("somalia", "AF", "War", "Somalia", "Turkish army chief visits", "GAROWE", "", 45.3, 2.0),
]

# ---------------------------------------------------------------- sport (all finished before 24:00 UTC), filed by venue
SPORT = [
    ("eng", "EU", "Rugby", "England 37–12 NZ", "SKY", -0.34, 51.46),
    ("epl", "EU", "Premier League", "Chelsea 1–4 Leeds", "ESPN", -0.19, 51.48),
    ("cric", "AP", "Test cricket", "India 486/4 v NZ", "AFP", 174.8, -41.3),
    ("t20", "AP", "T20 cricket", "Aus beat England", "ESPN", 144.98, -37.82),
    ("cfb", "AM", "NCAA · v Ohio St", "Nebraska 31–28", "NBC", -96.7, 40.8),
    ("ufc", "ME", "UFC Doha", "Stirling wins by KO", "UFC.COM", 51.5, 25.3),
]

TIMELINE = [
    ("00:09", "M6.7 quake, Peru", "peru"),
    ("by 04:00", "Geneva talks end", "geneva"),
    ("06:50", "Sparta II alert", "baltic"),
    ("09:42", "M6.8 Banda Sea", "quake"),
    ("10:34", "Heli incursion", "heli"),
    ("15:16", "Bitcoin at $60k", "btc"),
    ("18:24", "Mercury burn", "bepi"),
    ("20:00", "116 clashes", "front"),
]

DATECHECK = [
    ("ok", "Counted", "00:00–24:00 UTC, Sat 21 Nov"),
    ("edge", "Edge case", "Peru quake at 00:09 UTC, counted"),
    ("rep", "Exception", "Kim visit 20 Nov, told Sat"),
    ("out", "Too early", "Poland missiles · Brazil storm"),
    ("out", "Too late", "Las Vegas GP · Sudamericana"),
]
NOT_COUNTED = ("<b>Before 00:00 UTC:</b> missiles in Poland · Brazil storm · UK–EU deal. "
               "<b>After 24:00:</b> Las Vegas GP · Sudamericana final. "
               "<b>Counted:</b> Peru quake at 00:09 UTC.")

SOURCE_KEY = ("AA Anadolu · DNE Daily News Egypt · ISW Inst. Study of War · KCNA N. Korean state media · "
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
    assert len(b[3]) + len(b[4]) <= 60, (len(b[3]) + len(b[4]), b)
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

CHECK = '<svg class="ok" viewBox="0 0 16 16" width="14" height="14"><circle cx="8" cy="8" r="8" fill="#1e8e3e"/><path d="M4.2 8.3 L7 11 L11.9 5.3" stroke="#fff" stroke-width="2.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
FLAG = {"claim": '<span class="claim">CLAIM</span>', "official": CHECK,
        "report": '<span class="rep">REPORT</span>', "": ""}


def brief_html(b):
    k, r, t, place, text, src, flag, *_ = b
    return (f'<div class="br">{badge(N[k], rc(r), "s")}<div class="bt"><b>{e(place)}:</b> {e(text)} {FLAG[flag]}'
            f'<span class="bs">{e(src)}</span></div></div>')


half = (len(BRIEFS) + 1) // 2
briefs_l = "".join(brief_html(b) for b in BRIEFS[:half])
briefs_r = "".join(brief_html(b) for b in BRIEFS[half:])

sport = "".join(f'<div class="sp">{badge(N[k], rc(r), "b")}<div><b>{e(c)} · {e(src)}</b>{e(t)}</div></div>'
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

MAPJS = f"""
(function () {{
  const land = {LAND};
  const water = {WATER};
  const pins = {json.dumps(pins)};
  const W = 330, H = 116, B = {{lon0: -128, lon1: 180, lat0: 74, lat1: -46}};
  const sx = W / (B.lon1 - B.lon0), sy = H / (B.lat0 - B.lat1);
  const P = (lon, lat) => [(lon - B.lon0) * sx, (B.lat0 - lat) * sy];
  const inside = (x, y, poly) => {{ let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {{
      const [xi, yi] = poly[i], [xj, yj] = poly[j];
      if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) c = !c; }} return c; }};
  let s = '<rect width="' + W + '" height="' + H + '" fill="#eef3f6"/>';
  const step = 3.4;
  for (let py = step / 2; py < H; py += step) for (let px = step / 2; px < W; px += step) {{
    const lon = B.lon0 + px / sx, lat = B.lat0 - py / sy;
    if (land.some(p => inside(lon, lat, p)) && !water.some(p => inside(lon, lat, p)))
      s += '<circle cx="' + px.toFixed(1) + '" cy="' + py.toFixed(1) + '" r="1.15" fill="#c3bba7"/>';
  }}
  pins.filter(p => !p.big).forEach(p => {{ const [x, y] = P(p.lon, p.lat);
    s += '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="3.4" fill="' + p.c + '" stroke="#fff" stroke-width="1"/>'; }});
  // numbered pins for the 11 illustrated stories; spiral outwards until no overlap (deterministic)
  const placed = [], R = 8.5, marks = [];
  const free = (x, y) => x > R && y > R && x < W - R && y < H - R && placed.every(q => Math.hypot(q[0] - x, q[1] - y) > 2 * R + 1);
  pins.filter(p => p.big).sort((a, b) => a.n - b.n).forEach(p => {{
    const [x, y] = P(p.lon, p.lat); let bx = x, by = y;
    if (!free(x, y)) {{ let done = false;
      for (let d = 2 * R + 2; d < 120 && !done; d += 3)
        for (let a = 0; a < 24 && !done; a++) {{ const t = -Math.PI / 2 + a * Math.PI / 12, cx = x + d * Math.cos(t), cy = y + d * Math.sin(t);
          if (free(cx, cy)) {{ bx = cx; by = cy; done = true; }} }} }}
    placed.push([bx, by]); marks.push([p, x, y, bx, by]); }});
  marks.forEach(([p, x, y, bx, by]) => {{ if (bx !== x || by !== y)
    s += '<line x1="' + x.toFixed(1) + '" y1="' + y.toFixed(1) + '" x2="' + bx.toFixed(1) + '" y2="' + by.toFixed(1) + '" stroke="#16181d" stroke-width="1"/>';
    s += '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="2" fill="#16181d"/>'; }});
  marks.forEach(([p, x, y, bx, by]) => {{
    s += '<circle cx="' + bx.toFixed(1) + '" cy="' + by.toFixed(1) + '" r="' + R + '" fill="' + p.c + '" stroke="#fff" stroke-width="1.4"/>';
    s += '<text x="' + bx.toFixed(1) + '" y="' + (by + 3.6).toFixed(1) + '" font-size="10.5" font-weight="800" fill="#fff" text-anchor="middle" font-family="Small">' + p.n + '</text>'; }});
  s += '<g transform="translate(6 92)"><rect width="118" height="19" rx="3" fill="#1a1236"/><text x="7" y="13.5" font-size="10" font-weight="700" fill="#fff" font-family="Small">Off map: {", ".join(map(str, OFFMAP))}</text></g>';
  document.getElementById('world').innerHTML = s;
}})();
"""

CHECKJS = """
(function () {
  const bad = [];
  document.querySelectorAll('.foot, .bt, .sp, .tl, .dcr, .dc, .mast, .mt, .trust, .title, .lead, .card, .kick, .srcr, .meta, .acols > div, .bottom, .keys, .rk').forEach(el => {
    if (el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1) bad.push(el.className + '[' + (el.scrollWidth - el.clientWidth) + 'x' + (el.scrollHeight - el.clientHeight) + ']:' + (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 34));
  });
  const pg = document.querySelector('.page'); const last = document.querySelector('.foot').getBoundingClientRect();
  if (last.bottom > 1024) bad.push('PAGE-BOTTOM:' + last.bottom);
  document.body.setAttribute('data-overflow', bad.join(' | '));
})();
"""

DC_ICON = {"ok": CHECK, "edge": '<span class="dci edge">!</span>', "rep": '<span class="rep">REPORT</span>', "out": '<span class="dci out">×</span>'}
datecheck = "".join(f'<div class="dcr">{DC_ICON[i]}<b>{e(h)}</b><span>{e(t)}</span></div>' for i, h, t in DATECHECK)

CSS = open(os.path.join(ROOT, "tools", "style.css"), encoding="utf-8").read()

PAGE = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>The One-Day World · Saturday 21 November 2026</title><style>{CSS}</style></head>
<body><div class="page">
<header class="mast">
  <div class="dial">{art.daydial(66)}</div>
  <div class="mt">
    <div class="kick1">THE ONE-DAY WORLD &nbsp;·&nbsp; {TOTAL} STORIES · {DRAWN} ILLUSTRATED · ALL SOURCED</div>
    <div class="title">Saturday 21 November 2026</div>
    <div class="sub">Every story took place 00:00–24:00 UTC on Saturday 21 November 2026 · stories 1–11 confirmed by 2+ sources</div>
  </div>
  <div class="trust"><div class="th">HOW TO READ</div>
    <div><span class="bd s" style="background:#1f5fbf">1</span>story no., same on map</div>
    <div><span class="claim">CLAIM</span>one side’s word, attributed</div>
    <div>{CHECK}official statement or data</div>
    <div><span class="rep">REPORT</span>first reported today</div>
    <div class="nb">1–11: no label, all confirmed</div></div>
</header>
<div class="rbar">{region_bar}</div>
<div class="tline"><div class="tlh">THE DAY<br>IN UTC</div>{timeline}</div>
<div class="leads">{leads}</div>
<div class="cards">{cards}</div>
<div class="bottom">
  <div class="mapbox"><div class="mh">WHERE IT HAPPENED <span>numbers: stories 1–11 · dots: briefs &amp; sport</span></div>
    <svg id="world" width="330" height="116" viewBox="0 0 330 116" xmlns="http://www.w3.org/2000/svg"></svg>
    <div class="dc"><div class="dch">DATE CHECK</div>{datecheck}</div></div>
  <div class="also"><div class="ah">ALSO ON SATURDAY <span>colour = region</span></div>
    <div class="acols"><div>{briefs_l}</div><div>{briefs_r}</div></div></div>
</div>
<div class="sport"><div class="sb">{art.scoreboard()}<div>SPORT</div></div><div class="spg">{sport}</div></div>
<footer class="foot"><b>Source key:</b> {e(SOURCE_KEY)}</footer>
</div><script>{MAPJS}</script><script>{CHECKJS}</script></body></html>'''

open(os.path.join(ROOT, "poster", "index.html"), "w", encoding="utf-8").write(PAGE)
print("stories", TOTAL, "drawn", DRAWN, "regions", COUNT, "topics", {k: v for k, v in TCOUNT.items() if v})
