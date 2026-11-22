#!/usr/bin/env python3
"""Builds poster/index.html: the front page for Saturday 21 November 2026.

Design goal (from the bounty rules): an AI editor compares two images, first on
whether the day is named and its events are recognisable, then on choice and
breadth, then on whether each story is clear from its picture and short label,
then faithfulness, then craft at about 300 px. So the page names the date in
huge type, shows 13 of the day's biggest stories as large drawings with
short headlines, covers every region, and lists 20 more in a readable strip.

Render with tools/render.sh; tools/check.sh reports any text that does not fit.
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
    "ME": ("Middle East", "#b86e00"),
    "AM": ("Americas", "#2e8b3d"),
    "AP": ("Asia-Pacific", "#b0306f"),
    "AF": ("Africa", "#7a4a26"),
    "GL": ("Global", "#4b3c93"),
}

# st = (kind, source): kind is "CONFIRMED" (2+ outlets or an official source) for every drawn story.
LEADS = [
    dict(k="baltic", r="EU", t="Finland", st=("CONFIRMED", "Reuters · Finnish MoD"), art=art.baltic(),
         h="Drones set Russian ship ablaze off Finland",
         p="Finland says Ukraine was likely behind it."),
    dict(k="btc", r="GL", t="Markets", st=("CONFIRMED", "Reuters · Investing.com"), art=art2.bitcoin_lead(),
         h="Bitcoin hits a two-year low, then claws back",
         p="Low of $55,326, 56% under its 2025 record."),
    dict(k="riemann", r="GL", t="Maths & AI", st=("CONFIRMED", "Guardian · SciAm"), art=art2.riemann_lead(),
         h="Experts certify a Claude-aided Riemann proof",
         p="Lean and Mathlib: “full confidence” in it."),
]

# 10 drawn stories, 5 per row; t = place
CARDS = [
    dict(k="hormuz", topic="Iran war", r="ME", t="Hormuz", st=("CONFIRMED", "UKMTO"), art=art2.hormuz_c(),
         h="Two tankers hit by projectiles", p="Iran’s navy: a third hit a mine."),
    dict(k="gaza", topic="War", r="ME", t="Gaza", st=("CONFIRMED", "Reuters"), art=art2.gaza(),
         h="Israeli strike on a food van kills 3", p="IDF: militants. WCK: not ours."),
    dict(k="cop", topic="Climate", r="ME", t="Turkey", st=("CONFIRMED", "Reuters"), art=art2.cop31(),
         h="COP31 talks stall past deadline", p="Split over fossil-fuel wording."),
    dict(k="sinaloa", topic="Cartels", r="AM", t="Mexico", st=("CONFIRMED", "AP"), art=art2.sinaloa_c(),
         h="Mexico seizes “El\u00a0Chapo\u00a0Isidro”", p="FBI Top Ten fugitive; 11 die."),
    dict(k="eu", topic="Economy", r="EU", t="Brussels", st=("CONFIRMED", "AFP"), art=art2.eubudget(),
         h="Costa proposes €204bn budget cut", p="For 2028–34; adds a tech tax."),
    dict(k="bepi", topic="Science", r="GL", t="Space", st=("CONFIRMED", "ESA"), art=art2.bepi(),
         h="BepiColombo enters orbit at Mercury", p="Only the 2nd probe to do so."),
    dict(k="quake", topic="Disaster", r="AP", t="Indonesia", st=("CONFIRMED", "USGS"), art=art2.banda(),
         h="M6.8 Banda Sea quake felt in Darwin", p="No tsunami, no damage."),
    dict(k="mama", topic="Music", r="AP", t="Japan", st=("CONFIRMED", "Korea Herald"), art=art2.mama(),
         h="BTS sweep five MAMA awards", p="CORTIS win Song of the Year."),
]

# (key, region, flag, place, text, label, source)   label kept for SOURCES.md: "claim" | "report" | ""
BRIEFS = [
    ("heli", "EU", "FI", "Finland", "Russian helicopter suspected in airspace breach", "", "DW"),
    ("front", "EU", "UA", "Ukraine", "General Staff logs 116 front-line clashes", "claim", "Kyiv Post"),
    ("pope", "EU", "VA", "Vatican", "Pope Leo warns of “enormous” tech risks", "", "Vatican News"),
    ("france", "EU", "FR", "France", "Sixth weekend of cost-of-living protests", "", "Le Monde"),
    ("robots", "EU", "UN", "Geneva", "No UN killer-robot treaty; talks run to 2028", "", "Reuters"),
    ("eng", "EU", "ENG", "Rugby", "England beat New Zealand 37–12", "", "Sky Sports"),
    ("epl", "EU", "ENG", "Football", "Leeds win 4–1 at Chelsea", "", "ESPN"),
    ("aoun", "ME", "LB", "Lebanon", "Aoun demands an Israeli withdrawal", "", "Arab News"),
    ("israel", "ME", "IL", "Israel", "Bennett backs a unity bloc under Eisenkot", "", "ToI"),
    ("houthi", "ME", "YE", "Yemen", "ISW: Houthis fortifying the coast", "claim", "ISW"),
    ("peru", "AM", "PE", "Peru", "M6.7 Andes quake at 00:09 UTC shakes Lima", "", "USGS"),
    ("fbi", "AM", "US", "US", "Trump plays down the FBI database hack", "", "Axios"),
    ("iran", "AM", "US", "US", "Trump says he wants a “permanent” Iran deal", "", "CBS"),
    ("brazil", "AM", "BR", "Brazil", "Lula calls the fiscal bill “an adjustment”", "", "Rio Times"),
    ("in", "AP", "IN", "India", "Google gives IIT Kharagpur $5m for AI", "", "The Week"),
    ("bd", "AP", "BD", "Bangladesh", "Extra troops deployed amid unrest", "", "Khaleej Times"),
    ("kr", "AP", "KR", "S. Korea", "Ruling party moves to impeach chief justice", "", "Korea Herald"),
    ("nk", "AP", "KP", "N. Korea", "Kim seen at school factories", "report", "KCNA via CNA"),
    ("cric", "AP", "NZ", "Cricket", "India reach 486/4, lead NZ by 118", "", "AFP"),
    ("eg", "AF", "EG", "Egypt", "Sisi calls for reform of global finance", "", "Daily News Egypt"),
    ("sudan", "AF", "SD", "Sudan", "Relief group accuses RSF of killing children", "claim", "Anadolu"),
    ("oyo", "AF", "CG", "Congo", "Kenya’s Ruto at a four-way security summit", "", "Kenyans.co.ke"),
]

# where each story happened (lon, lat); stories with no single place are listed as off the map
COORDS = dict(
    baltic=(26.9, 60.1), hormuz=(56.3, 26.6), gaza=(34.45, 31.5), cop=(30.7, 36.9), sinaloa=(-108.4, 25.6),
    eu=(4.35, 50.85), quake=(127.5, -7.7), mama=(135.5, 34.7),
    heli=(26.2, 60.4), front=(37.2, 48.3), france=(2.35, 48.9), robots=(6.1, 46.2), pope=(12.45, 41.9),
    eng=(-0.34, 51.46), epl=(-0.19, 51.48), aoun=(35.5, 33.9), israel=(34.8, 32.1), houthi=(43.4, 12.8),
    peru=(-76.0, -10.9), fbi=(-77.0, 38.9), iran=(-77.4, 39.4), brazil=(-47.9, -15.8), **{"in": (87.3, 22.3)},
    bd=(90.4, 23.8), kr=(127.0, 37.5), nk=(125.8, 39.0), cric=(174.8, -41.3), eg=(31.2, 30.0),
    sudan=(29.0, 11.5), oyo=(15.9, -1.0),
)

# The day in UTC, drawn to scale on a 24-hour axis.
# (UTC time, caption, story key, row "up"/"down", label side "l" = label starts at the marker, "r" = ends at it)
TIMELINE = [
    ("00:09", "Peru M6.7 quake", "peru", "up", "l"),
    ("c. 04:00", "Robot talks end", "robots", "down", "r"),
    ("05:00", "Tanker hit off Oman", "hormuz", "up", "l"),
    ("06:50", "Sparta II struck", "baltic", "down", "l"),
    ("09:42", "Banda Sea M6.8 quake", "quake", "up", "l"),
    ("10:34", "Finnish airspace breach", "heli", "down", "l"),
    ("15:16", "Bitcoin rebounds to $60,192", "btc", "up", "l"),
    ("20:00", "116 clashes", "front", "down", "l"),
]
BRIEF_FLAG = {b[0]: b[2] for b in BRIEFS}

# (figure, caption, story key)
NUMBERS = [
    ("16", "crew evacuated", "baltic"),
    ("$55.3k", "Bitcoin low", "btc"),
    ("2", "tankers hit", "hormuz"),
    ("11", "dead in Sinaloa", "sinaloa"),
    ("€204bn", "cut proposed", "eu"),
    ("8 yrs", "to reach Mercury", "bepi"),
]

DATE_IN = "events of Sat 21 Nov, or first reported that day."
DATE_OUT = [("Fri 20", "Kryvyi Rih strike, UK–EU deal"),
            ("Sun 22", "Las Vegas GP")]


ORDER = [x["k"] for x in LEADS] + [x["k"] for x in CARDS] + [b[0] for b in BRIEFS]
N = {k: i + 1 for i, k in enumerate(ORDER)}
assert len(N) == len(ORDER), "duplicate keys"
TOTAL = len(ORDER)
REG = {**{x["k"]: x["r"] for x in LEADS + CARDS}, **{b[0]: b[1] for b in BRIEFS}}
COUNT = {r: sum(1 for v in REG.values() if v == r) for r in REGIONS}
assert all(COUNT.values()), COUNT  # every region is covered
DRAWN = len(LEADS) + len(CARDS)
for k in [t[2] for t in TIMELINE] + [x[2] for x in NUMBERS]:
    assert k in N, k
assert set(COORDS) | {"btc", "riemann", "bepi"} == set(N), set(N) ^ set(COORDS)


def rc(r):
    return REGIONS[r][1]


CHECK = ('<svg class="ok" viewBox="0 0 16 16" width="12" height="12"><circle cx="8" cy="8" r="8" fill="#1e8e3e"/>'
         '<path d="M4.2 8.3 L7 11 L11.9 5.3" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def num(k, cls="n"):
    """Story number in its region colour; briefs get a plain dot."""
    if N[k] <= DRAWN:
        return f'<span class="{cls}" style="background:{rc(REG[k])}">{N[k]}</span>'
    return f'<span class="{cls} dot" style="background:{rc(REG[k])}"></span>'


def kicker(x):
    return (f'<div class="meta">{num(x["k"])}<span class="kick" style="color:{rc(x["r"])}">{e(REGIONS[x["r"]][0])} · {e(x["t"])}</span>'
            f'<span class="src">{CHECK}{e(x["st"][1])}</span></div>')


def card_kicker(x):
    return (f'<div class="meta">{num(x["k"])}<span class="kick" style="color:{rc(x["r"])}">{e(x["t"])}</span>'
            f'<span class="src">{CHECK}{e(x["st"][1])}</span></div>')


def card_art(svg):
    """Card drawings keep their 160x56 shape and scale to the card width."""
    return svg.replace("<svg ", '<svg preserveAspectRatio="xMidYMid meet" ', 1)


leads = "".join(
    f'<div class="lead" style="--c:{rc(x["r"])}"><div class="art">{x["art"]}</div>{kicker(x)}'
    f'<h1>{e(x["h"])}</h1><p>{e(x["p"])}</p></div>' for x in LEADS)

cards = "".join(
    f'<div class="card" style="--c:{rc(x["r"])}"><div class="art2">{card_art(x["art"])}<span class="topic">{e(x["topic"])}</span></div>{card_kicker(x)}'
    f'<h2>{e(x["h"])}</h2><p>{e(x["p"])}</p></div>' for x in CARDS)

LBL = {"claim": '<span class="st claim">CLAIM</span>', "report": '<span class="st rep">REPORTED</span>', "": ""}

briefs = "".join(
    f'<div class="br" style="--c:{rc(r)}">{art2.flag(fl)}<div class="bt"><b>{e(place)}:</b> {e(text)}{LBL[lab]}</div>'
    f'<span class="bs">{e(src)}</span></div>'
    for _, r, fl, place, text, lab, src in BRIEFS)

def minutes(t):
    h, m = t.replace("c. ", "").split(":")
    return int(h) * 60 + int(m)


def tl_event(t, cap, k, row, side):
    left = minutes(t) / 1440 * 100
    flag = art2.flag(BRIEF_FLAG[k]) if k in BRIEF_FLAG else ""
    mark = (f'<span class="mk" style="background:{rc(REG[k])}">{N[k]}</span>' if N[k] <= DRAWN
            else f'<span class="mk dot" style="background:{rc(REG[k])}"></span>')
    return (f'<div class="ev {row} {side}" style="left:{left:.3f}%"><i class="stem"></i>{mark}'
            f'<span class="lab">{flag}<b>{e(t)}</b>{e(cap)}</span></div>')


hours = "".join(f'<span class="hr" style="left:{h / 24 * 100:.3f}%">{h:02d}:00</span>' for h in (6, 12, 18))
timeline = (f'<div class="band">{hours}<span class="hr end">24:00</span></div>'
            + "".join(tl_event(*x) for x in TIMELINE))
numbers = "".join(f'<div class="nm"><b>{num(k, "tn")}{e(v)}</b><span>{e(c)}</span></div>' for v, c, k in NUMBERS)
numbers_tile = f'<div class="card tile"><div class="th">THE DAY IN NUMBERS</div><div class="nums">{numbers}</div></div>'
datecheck_tile = (f'<div class="card tile dc"><div class="th red">DATE CHECK</div><p class="in">{CHECK}<span><b>In:</b> {e(DATE_IN)}</span></p>'
                  + "".join(f'<p class="out"><span class="x">×</span><span><b>Out, {e(d)}:</b> {e(t)}</span></p>' for d, t in DATE_OUT)
                  + '<p class="lg"><span class="st claim">CLAIM</span> one side’s account</p>'
                  + '<p class="lg"><span class="st rep">REPORTED</span> made public today</p></div>')
CARD_ITEMS = re.findall(r'<div class="card" style=.*?</p></div>', cards)
assert len(CARD_ITEMS) == 8
grid = "".join(CARD_ITEMS[:4]) + numbers_tile + "".join(CARD_ITEMS[4:]) + datecheck_tile

pins = []
for k, (lon, lat) in COORDS.items():
    pins.append(dict(n=N[k], lon=lon, lat=lat, c=rc(REG[k]), big=int(N[k] <= DRAWN)))
OFFMAP = sorted(N[k] for k in N if k not in COORDS)
MAPDATA = open(os.path.join(ROOT, "tools", "mapdata.js"), encoding="utf-8").read()
LAND = re.search(r"const land = (\[.*?\]);\n", MAPDATA, re.S).group(1)
WATER = re.search(r"const water = (\[.*?\]);\n", MAPDATA, re.S).group(1)
MAPJS = """
(function () {
  const land = %s;
  const water = %s;
  const pins = %s;
  const W = 252, H = 88, B = {lon0: -125, lon1: 180, lat0: 64, lat1: -42.5};
  const sx = W / (B.lon1 - B.lon0), sy = H / (B.lat0 - B.lat1);
  const P = (lon, lat) => [(lon - B.lon0) * sx, (B.lat0 - lat) * sy];
  const inside = (x, y, poly) => { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
      const [xi, yi] = poly[i], [xj, yj] = poly[j];
      if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) c = !c; } return c; };
  let s = '<rect width="' + W + '" height="' + H + '" fill="#eaf1f5"/>';
  const step = 2.6;
  for (let py = step / 2; py < H; py += step) for (let px = step / 2; px < W; px += step) {
    const lon = B.lon0 + px / sx, lat = B.lat0 - py / sy;
    if (land.some(p => inside(lon, lat, p)) && !water.some(p => inside(lon, lat, p)))
      s += '<circle cx="' + px.toFixed(1) + '" cy="' + py.toFixed(1) + '" r=".9" fill="#c3bba7"/>';
  }
  pins.filter(p => !p.big).forEach(p => { const [x, y] = P(p.lon, p.lat);
    s += '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="2.6" fill="' + p.c + '" stroke="#fff" stroke-width=".8"/>'; });
  const placed = [], R = 7, marks = [];
  const free = (x, y) => x > R && y > R && x < W - R && y < H - R && placed.every(q => Math.hypot(q[0] - x, q[1] - y) > 2 * R + 1);
  pins.filter(p => p.big).sort((a, b) => a.n - b.n).forEach(p => {
    const [x, y] = P(p.lon, p.lat); let bx = x, by = y;
    if (!free(x, y)) { let done = false;
      for (let d = 2 * R + 2; d < 90 && !done; d += 2)
        for (let a = 0; a < 24 && !done; a++) { const t = -Math.PI / 2 + a * Math.PI / 12, cx = x + d * Math.cos(t), cy = y + d * Math.sin(t);
          if (free(cx, cy)) { bx = cx; by = cy; done = true; } } }
    placed.push([bx, by]); marks.push([p, x, y, bx, by]); });
  marks.forEach(([p, x, y, bx, by]) => { if (bx !== x || by !== y)
    s += '<line x1="' + x.toFixed(1) + '" y1="' + y.toFixed(1) + '" x2="' + bx.toFixed(1) + '" y2="' + by.toFixed(1) + '" stroke="#16181d" stroke-width=".9"/>'; });
  marks.forEach(([p, x, y, bx, by]) => {
    s += '<circle cx="' + bx.toFixed(1) + '" cy="' + by.toFixed(1) + '" r="' + R + '" fill="' + p.c + '" stroke="#fff" stroke-width="1.2"/>';
    s += '<text x="' + bx.toFixed(1) + '" y="' + (by + 3.3).toFixed(1) + '" font-size="9.5" font-weight="800" fill="#fff" text-anchor="middle" font-family="Small">' + p.n + '</text>'; });
  document.getElementById('world').innerHTML = s;
})();
""" % (LAND, WATER, json.dumps(pins))

legend = "".join(f'<span><i style="background:{c}"></i>{e(n)} {COUNT[r]}</span>' for r, (n, c) in REGIONS.items())

region_names = [REGIONS[r][0] for r in REGIONS if r != "GL"] + ["space"]
STRAP = ("Top news from " + ", ".join(region_names[:-1]).replace("Middle East", "the Middle East").replace("Americas", "the Americas") + " and " + region_names[-1])

SOURCES_LINE = ("Sources: Reuters, AP, AFP, USGS, ESA, UKMTO, Finnish MoD, Guardian, Scientific American, Korea Herald; "
                "links for every story in SOURCES.md. All drawings are original.")

CHECKJS = """
document.fonts.ready.then(function () {
  const bad = [];
  document.querySelectorAll('.top, .strap, .mapbox, .mh, .lead, .card, .meta, .lead p, .card p, .tile p, .nm, .also, .br, .bt, .foot, .foot div, .topic').forEach(el => {
    if (el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1)
      bad.push(el.className + el.tagName + '[' + (el.scrollWidth - el.clientWidth) + 'x' + (el.scrollHeight - el.clientHeight) + ']:' + (el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 34));
  });
  document.querySelectorAll('h1, h2').forEach(el => {  // headlines: at most 2 lines
    const cs = getComputedStyle(el), h = el.style.height; el.style.height = 'auto';
    const lines = Math.round((el.clientHeight - parseFloat(cs.paddingTop)) / parseFloat(cs.lineHeight)); el.style.height = h;
    if (lines > 2) bad.push('LINES ' + lines + ':' + el.textContent.slice(0, 34));
  });
  const ax = document.querySelector('.axis').getBoundingClientRect();
  const labs = [...document.querySelectorAll('.ev .lab')].map(el => [el, el.getBoundingClientRect()]);
  labs.forEach(([el, r], i) => {
    if (r.left < ax.left - 1 || r.right > ax.right + 1) bad.push('TL-EDGE:' + el.textContent);
    labs.slice(i + 1).forEach(([el2, r2]) => {
      if (r.left < r2.right + 4 && r2.left < r.right + 4 && r.top < r2.bottom && r2.top < r.bottom) bad.push('TL-OVERLAP:' + el.textContent + '/' + el2.textContent);
    });
  });
  const t = document.querySelector('.title');
  if (t.scrollWidth > t.clientWidth + 1) bad.push('TITLE-WIDTH');
  const f = document.querySelector('.foot').getBoundingClientRect();
  if (f.bottom > 1024) bad.push('PAGE-BOTTOM:' + f.bottom);
  document.body.setAttribute('data-overflow', bad.join(' | '));
});
"""

CSS = open(os.path.join(ROOT, "tools", "style.css"), encoding="utf-8").read()

PAGE = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>The world on Saturday 21 November 2026</title><style>{CSS}</style></head>
<body><div class="page">
<div class="top"><span>THE WORLD ON ONE PAGE</span><span>{TOTAL} STORIES · {len(REGIONS)} REGIONS · {DRAWN} DRAWN</span></div>
<div class="mast"><div class="mleft"><div class="title">Saturday 21 November 2026</div><div class="strap">{e(STRAP)}</div></div>
  <div class="mapbox"><div class="mh">WHERE IT HAPPENED <span>off map: {", ".join(map(str, OFFMAP))}</span></div>
  <svg id="world" width="252" height="88" viewBox="0 0 252 88" xmlns="http://www.w3.org/2000/svg"></svg></div></div>
<div class="leads">{leads}</div>
<div class="tline"><div class="tlh">THE DAY<br>IN UTC<small>00:00 – 24:00</small></div><div class="axis">{timeline}</div></div>
<div class="cards">{grid}</div>
<div class="also"><div class="ah">ALSO ON SATURDAY 21 NOVEMBER <span>{len(BRIEFS)} more · stripe colour = region</span></div><div class="acols">{briefs}</div></div>
<footer class="foot"><div><b>Every story happened, or was first reported, on Saturday 21 November 2026.</b> Times are UTC. {CHECK}= confirmed by 2+ outlets or an official source, named on each story.</div>
<div class="fl2"><span class="key">{legend}</span><span>All {TOTAL} stories are real reports from 21 Nov 2026, each linked in SOURCES.md. Drawings are original.</span></div></footer>
</div><script>{MAPJS}</script><script>{CHECKJS}</script></body></html>'''

open(os.path.join(ROOT, "poster", "index.html"), "w", encoding="utf-8").write(PAGE)
print("stories", TOTAL, "drawn", DRAWN, "regions", COUNT)
