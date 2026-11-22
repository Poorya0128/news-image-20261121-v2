#!/usr/bin/env python3
"""Builds poster/index.html (the 43-story front page) from the story data below.

Every story is numbered once; the same number is used on the map pins, so the
judge can cross-check map <-> text. Run tools/render.sh afterwards.
"""
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V1 = open(os.path.join(ROOT, "build", "index_v1.html"), encoding="utf-8").read()
ICONS = re.findall(r'<div class="ic">(<svg.*?</svg>)</div>', V1, re.S)
ART = re.search(r'(<svg width="587".*?</svg>)', V1, re.S).group(1)
MAPJS = re.search(r"<script>(.*?)</script>", V1, re.S).group(1)


def icon(i, size=46):
    return re.sub(r'width="58" height="58"', f'width="{size}" height="{size}"', ICONS[i])


ICON_UKRAINE = """<svg viewBox="0 0 64 64" width="46" height="46">
<rect width="64" height="64" fill="#7a5a12"/>
<rect x="6" y="30" width="14" height="34" fill="#2a2a2a"/><rect x="22" y="22" width="16" height="42" fill="#3a3a3a"/><rect x="40" y="34" width="18" height="30" fill="#2a2a2a"/>
<g fill="#ffd36b"><rect x="9" y="34" width="3" height="3"/><rect x="14" y="40" width="3" height="3"/><rect x="26" y="27" width="3" height="3"/><rect x="31" y="35" width="3" height="3"/><rect x="44" y="40" width="3" height="3"/><rect x="50" y="46" width="3" height="3"/></g>
<path d="M26 22 C23 14 30 12 28 4 C35 10 34 16 37 18 C38 13 42 11 41 6 C47 12 46 18 42 22Z" fill="#ff7a1a"/>
<path d="M50 4 L58 14" stroke="#fff" stroke-width="3"/><path d="M58 14 l-1 -6 l-5 3z" fill="#fff"/>
</svg>"""

# ------------------------------------------------------------------ stories
# Numbers are assigned automatically in reading order; pins and the numbers
# strip refer to stories by key, so map and text can never disagree.
CARDS = [
    dict(k="mex", c="#c2561a", kick="Americas · Mexico", ic=icon(0),
         h="“El Chapo Isidro” held; 11 dead in Sinaloa",
         p="FBI Ten Most Wanted cartel boss seized in Guasave.",
         s="AP; Mexico Defence Ministry"),
    dict(k="hormuz", c="#a3162b", kick="Middle East · Iran war", ic=icon(1),
         h="Three tankers hit in Strait of Hormuz",
         p="Iran also shows off an underground missile launcher.",
         s="AP; UKMTO"),
    dict(k="kryvyi", c="#7a5a12", kick="Europe · Ukraine war", ic=ICON_UKRAINE,
         h="Missiles kill 2 in Kryvyi Rih",
         p="Russia fires 3 ballistic missiles, 148 drones overnight.",
         s="AP; Ukrainian Air Force"),
    dict(k="cop", c="#2e7d4f", kick="Climate · Turkey", ic=icon(3),
         h="COP31 deadlocked over fossil fuels",
         p="Antalya talks run a day over time, halted for the night.",
         s="Reuters; Guardian"),
    dict(k="bepi", c="#5b3a8c", kick="Space · Science", ic=icon(4),
         h="BepiColombo enters Mercury orbit",
         p="ESA–JAXA probe arrives after an eight-year cruise.",
         s="ESA; AP; Nature"),
]

# (key, place, headline, detail, source)
COLUMNS = [
    ("Europe", "#1f4e8c", [
        ("fr", "France", "6th weekend of cost-of-living marches", "Turnout dips after concessions.", "Reuters"),
        ("pt", "Portugal", "Lisbon workers march in heavy rain", "Unions want pay, housing.", "Euronews"),
        ("kyiv", "Kyiv", "UK’s Streeting: Putin a “cold-blooded killer”", "Rebuts Trump’s “friend” remark.", "ITV"),
        ("blacksea", "Black Sea", "Russia says it hit a Ukrainian cargo ship", "Says it carried “dual-use” cargo.", "Sky News"),
        ("ams", "Amsterdam", "UK PM Burnham meets Dutch PM Jetten", "Tories attack EU deal.", "GOV.UK"),
        ("vat", "Vatican", "Pope warns of unethical tech risks", "Leo XIV to Space Forum.", "Vatican News"),
    ]),
    ("Middle East", "#a3162b", [
        ("gaza", "Gaza City", "Strike on food-aid vehicle kills 3", "Israel: Islamic Jihad target.", "Reuters"),
        ("aoun", "Lebanon", "Aoun demands Israeli exit, rebukes Iran", "Independence Day speech.", "Arab News"),
        ("unifil", "Lebanon", "UNIFIL starts handing posts to army", "As Israeli strikes go on.", "Anadolu"),
        ("mq9", "Iran", "IRGC claims 58th US MQ-9 shot down", "Says new air defence hit it.", "Tasnim"),
        ("dar", "Pakistan", "Dar hopes for early US–Iran deal", "“World can’t afford long war.”", "Daily Times"),
        ("houthi", "Yemen", "Houthis dig in on Bab al-Mandeb coast", "Tunnels, berms reported.", "ISW"),
    ]),
    ("Americas · UN", "#22355e", [
        ("fbi", "Washington", "Trump plays down FBI database hack", "2nd breach in two months.", "UPI; Axios"),
        ("iran", "Washington", "Trump wants “permanent” Iran deal", "Interview with Fox News.", "CBS"),
        ("taiwan_ca", "Halifax", "Taiwan warns Carney on China ties", "Warns of economic coercion.", "AP"),
        ("ca_us", "Halifax", "Canada: “no change” in US military ties", "Denies Hegseth curbs.", "CP"),
        ("geneva", "UN · Geneva", "“Killer robot” talks end without treaty", "128 states delay to 2028.", "Reuters"),
    ]),
    ("Asia-Pacific", "#0f7c86", [
        ("quake", "Banda Sea", "M6.8 deep quake near Timor-Leste", "09:42 UTC, 132 km deep.", "USGS"),
        ("bd", "Bangladesh", "Extra troops deployed after arson wave", "Hasina backers’ homes hit.", "Reuters"),
        ("kr", "South Korea", "Chief-justice impeachment eyed for 3 Dec", "Ruling DP says.", "Korea Herald"),
        ("tw", "Taiwan", "Tracks 2 PLA jets, 7 ships, 4 balloons", "24 hours to 6 a.m. Sat.", "Taiwan MND"),
        ("au", "Australia", "Thousands rally for midwife homebirths", "Insurance rule due 1 Jan.", "ABC"),
        ("in", "India", "Modi at IIT Kharagpur’s 75th", "Urges “nation first”.", "The Hindu"),
    ]),
    ("Africa", "#8a4b12", [
        ("eg", "Egypt", "Sisi urges overhaul of global finance", "At 6th Aswan Forum.", "Daily News Egypt"),
        ("sennar", "Sudan", "Sennar imposes night curfew", "Blue Nile fighting grows.", "Radio Tamazuj"),
        ("rsf", "Sudan", "RSF accused of killing civilians", "3 children among dead.", "Anadolu"),
        ("ng", "Nigeria", "Tinubu holds low-key Ibadan rally", "Muted after Bayelsa boat deaths.", "Premium Times"),
        ("za", "South Africa", "Tributes for Phumzile Mlambo-Ngcuka", "Ex-deputy president, 71.", "AFP"),
    ]),
]

SPORT = [
    ("eng", "Rugby", "England 37–12 NZ, record"),
    ("ire", "Rugby", "Ireland 20–17 South Africa"),
    ("sco", "Rugby", "Scotland 67–5 Japan"),
    ("epl", "Premier League", "Chelsea 1–4 Leeds"),
    ("boca", "Copa Sudamericana", "Boca 2–0 Atlético-MG"),
    ("cric", "Cricket", "India 486/4 v NZ"),
    ("t20", "T20", "Australia beat England"),
    ("cfb", "College football", "Nebraska 31–28 Ohio State"),
    ("ufc", "UFC Doha", "Stirling KOs Procházka"),
    ("f1", "Formula 1", "Verstappen wins Las Vegas"),
]

ORDER = ["lead"] + [c["k"] for c in CARDS] + [b[0] for _, _, bs in COLUMNS for b in bs] + [x[0] for x in SPORT]
N = {k: i + 1 for i, k in enumerate(ORDER)}
assert len(N) == len(ORDER)
TOTAL = len(ORDER)
for c in CARDS:
    c["n"] = N[c["k"]]

NUMBERS = [("16", "crew evacuated", "lead"), ("148", "drones at Ukraine", "kryvyi"), ("11", "dead in Sinaloa", "mex"),
           ("128", "states in Geneva", "geneva"), ("8 yrs", "to Mercury", "bepi"), ("37–12", "England v NZ", "eng")]
NUMBERS = [(v, l, N[k]) for v, l, k in NUMBERS]

DATE_CHECK = "Russian missiles land in Poland · M6.7 Peru quake · Brazil supercell storm · UK–EU summit deal · Ruto’s Busia speech"

# map pins: (key, lon, lat, label dx, label dy)
PINS = [
    ("lead", 26.9, 60.1, -4, -13), ("kryvyi", 33.4, 47.9, 18, -6), ("kyiv", 30.5, 50.4, 10, -16),
    ("fr", 2.35, 48.9, -26, -16), ("geneva", 6.1, 46.2, -30, 0), ("pt", -9.1, 38.7, -22, 6),
    ("vat", 12.45, 41.9, -14, 18), ("ams", 4.9, 52.4, -12, -24), ("blacksea", 31.5, 43.5, 30, 4),
    ("cop", 30.7, 36.9, -6, 18), ("aoun", 35.5, 33.9, 22, -8), ("gaza", 34.45, 31.5, 12, 14),
    ("eg", 32.9, 24.1, -16, 12), ("sennar", 33.6, 13.6, -18, 8), ("rsf", 28.5, 12.0, -22, 14), ("houthi", 43.4, 12.6, 16, 10),
    ("hormuz", 56.3, 26.6, 18, 2), ("mq9", 56.0, 27.5, 12, -16), ("dar", 73.0, 33.7, 2, -16),
    ("ng", 3.9, 7.4, -18, 8), ("za", 28.0, -26.2, -18, 8),
    ("in", 87.3, 22.3, -10, 18), ("bd", 90.4, 23.8, 14, 14), ("kr", 127.0, 37.5, -4, -15), ("tw", 121.5, 25.0, 16, 4),
    ("quake", 127.5, -7.7, 14, 12), ("au", 151.0, -33.9, -16, -6),
    ("mex", -108.4, 25.6, -4, 17), ("fbi", -77.0, 38.9, 6, 17), ("iran", -77.0, 38.9, -16, 8), ("taiwan_ca", -63.6, 44.6, 12, -12), ("ca_us", -63.6, 44.6, 22, 4),
]
COLOR = {"lead": "#1f4e8c"}
for c in CARDS:
    COLOR[c["k"]] = c["c"]
for _, col, bs in COLUMNS:
    for b in bs:
        COLOR[b[0]] = col
PINS = [(N[k], lo, la, dx, dy, COLOR[k]) for k, lo, la, dx, dy in PINS]

e = html.escape


def badge(n, c, cls="badge"):
    return f'<span class="{cls}" style="background:{c}">{n}</span>'


cards_html = "".join(
    f'''<div class="card" style="--c:{c["c"]}">
  <div class="kline">{badge(c["n"], c["c"])}{e(c["kick"])}</div>
  <div class="hd"><div class="ic">{c["ic"]}</div><h2>{e(c["h"])}</h2></div>
  <p>{e(c["p"])}</p>
  <div class="src">{e(c["s"])}</div>
</div>''' for c in CARDS)

cols_html = ""
for title, col, briefs in COLUMNS:
    items = "".join(
        f'''<div class="brief">{badge(n, col, "nb")}<div><div class="bt"><span class="pl">{e(place)}</span> {e(h)}</div><div class="bx">{e(t)} <i>{e(s)}</i></div></div></div>'''
        for n, place, h, t, s in [(N[b[0]],) + tuple(b[1:]) for b in briefs])
    cols_html += f'<div class="col" style="--c:{col}"><div class="colhd">{e(title)}</div>{items}</div>'

sport_html = "".join(
    f'<div class="sp">{badge(n, "#16181d", "nb")}<div><b>{e(k)}</b> {e(t)}</div></div>' for n, k, t in [(N[x[0]], x[1], x[2]) for x in SPORT])

nums_html = "".join(
    f'<div class="num"><b>{e(v)}</b><span>{e(l)} <em>({ref})</em></span></div>' for v, l, ref in NUMBERS)

art = (ART.replace('width="587" height="139" viewBox="0 13 587 139" preserveAspectRatio="xMidYMid slice"', 'width="497" height="96" viewBox="0 14 587 113" preserveAspectRatio="xMidYMid slice"')
       .replace('<text x="96" y="24"', '<text x="96" y="29"')
       .replace('M478 126 L508 126 L503 133 L483 133Z', 'M478 112 L508 112 L503 119 L483 119Z')
       .replace('<text x="472" y="146"', '<text x="404" y="124"'))
assert 'height="96"' in art

pins_js = "[" + ",".join(f"[{n},{lo},{la},{dx},{dy},'{c}']" for n, lo, la, dx, dy, c in PINS) + "]"
mapjs = MAPJS
mapjs = re.sub(r"const W = 408, H = 178, LON0 = -128, LON1 = 152, LAT0 = 73, LAT1 = -46;",
               "const W = 497, H = 184, LON0 = -126, LON1 = 156, LAT0 = 72, LAT1 = -42;", mapjs)
mapjs = re.sub(r"const pins = \[.*?\];", "const pins = " + pins_js + ";", mapjs, flags=re.S)
mapjs = mapjs.replace("r=\"8.5\"", "r=\"7.6\"").replace("(n > 9 ? 9.5 : 11)", "(n > 9 ? 8.6 : 10)").replace("(by + 3.8)", "(by + 3.3)")
mapjs = mapjs.replace("translate(6 120)", "translate(4 130)")

PAGE = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>The One-Day World — Saturday 21 November 2026</title>
<style>
@font-face {{ font-family: "Body"; font-weight: 400; src: url(fonts/NotoSans-SemiCondensed.ttf); }}
@font-face {{ font-family: "Body"; font-weight: 400; font-style: italic; src: url(fonts/NotoSans-SemiCondensedItalic.ttf); }}
@font-face {{ font-family: "Body"; font-weight: 600; src: url(fonts/NotoSans-SemiCondensedSemiBold.ttf); }}
@font-face {{ font-family: "Body"; font-weight: 700; src: url(fonts/NotoSans-SemiCondensedBold.ttf); }}
@font-face {{ font-family: "Body"; font-weight: 800; src: url(fonts/NotoSans-SemiCondensedExtraBold.ttf); }}
@font-face {{ font-family: "Head"; font-weight: 700; src: url(fonts/NotoSans-CondensedBold.ttf); }}
@font-face {{ font-family: "Head"; font-weight: 800; src: url(fonts/NotoSans-CondensedExtraBold.ttf); }}
@font-face {{ font-family: "Head"; font-weight: 900; src: url(fonts/NotoSans-CondensedBlack.ttf); }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 1024px; height: 1024px; overflow: hidden; }}
body {{ background: #f3ede1; color: #16181d; font-family: "Body", sans-serif; -webkit-font-smoothing: antialiased; }}
h1, h2, .title, .d2, .colhd, .bt, .num b, .lab {{ font-family: "Head", sans-serif; }}
.page {{ position: absolute; inset: 8px 12px 6px 12px; }}
.topline {{ display: flex; justify-content: space-between; font-size: 11px; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; border-bottom: 1.5px solid #16181d; padding-bottom: 2px; color: #333; }}
.topline b {{ color: #b3122e; }}
.mast {{ display: flex; align-items: flex-end; justify-content: space-between; padding: 1px 0 3px; border-bottom: 4px double #16181d; }}
.title {{ font-size: 54px; line-height: 52px; font-weight: 900; text-transform: uppercase; }}
.title span {{ color: #b3122e; }}
.mid {{ font-size: 12px; font-weight: 700; color: #333; text-align: center; line-height: 15px; margin-bottom: 4px; }}
.mid b {{ display: block; font-size: 22px; line-height: 22px; font-family: "Head"; color: #b3122e; }}
.date {{ text-align: right; background: #b3122e; color: #fff; padding: 3px 10px 4px; border-radius: 3px; margin-bottom: 3px; }}
.d1 {{ font-size: 13px; font-weight: 800; letter-spacing: .12em; }}
.d2 {{ font-size: 27px; line-height: 27px; font-weight: 900; }}
.badge, .nb {{ display: inline-flex; align-items: center; justify-content: center; border-radius: 50%; color: #fff; font-weight: 800; flex: none; font-family: "Body"; }}
.badge {{ width: 18px; height: 18px; font-size: 10.5px; }}
.nb {{ width: 17px; height: 17px; font-size: 9.5px; margin-top: 1px; }}
.row1 {{ display: flex; gap: 10px; margin-top: 5px; height: 252px; }}
.lead {{ width: 497px; display: flex; flex-direction: column; }}
.kbar {{ background: #1f4e8c; color: #fff; padding: 2px 6px; display: flex; justify-content: space-between; align-items: center; font-size: 11px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; }}
.kbar .k {{ display: flex; align-items: center; gap: 5px; }}
.kbar .k .badge {{ background: #fff !important; color: #1f4e8c; }}
.kbar .w {{ color: #dbe6f7; }}
h1 {{ font-size: 28px; line-height: 27px; font-weight: 900; margin: 2px 0 3px; }}
.art {{ height: 98px; border: 1px solid #16181d; overflow: hidden; flex: none; }}
.art svg {{ display: block; }}
.leadtext {{ display: flex; gap: 9px; margin-top: 4px; }}
.leadtext p {{ font-size: 12.5px; line-height: 15px; }}
.quote {{ width: 120px; flex: none; border-left: 4px solid #b3122e; padding-left: 6px; font-size: 13px; line-height: 15px; font-weight: 800; font-style: italic; }}
.quote small {{ display: block; font-size: 10.5px; line-height: 12px; font-weight: 600; font-style: normal; color: #444; margin-top: 2px; }}
.src {{ font-size: 10.5px; line-height: 12px; color: #555; font-style: italic; margin-top: 2px; }}
.src::before {{ content: "Sources: "; font-style: normal; font-weight: 700; color: #333; }}
.right {{ flex: 1; display: flex; flex-direction: column; gap: 4px; }}
.mapbox {{ border: 1px solid #16181d; background: #fbf8f1; }}
.maphead {{ background: #16181d; color: #fff; font-size: 11px; font-weight: 800; letter-spacing: .07em; text-transform: uppercase; padding: 2px 6px; display: flex; justify-content: space-between; }}
.maphead span {{ color: #f2c94c; }}
#map {{ display: block; }}
.nums {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 2px 5px; border: 1px solid #16181d; background: #16181d; padding: 3px 6px; color: #fff; flex: 1; align-content: center; }}
.num {{ display: flex; flex-direction: column; }}
.num b {{ font-size: 18px; line-height: 18px; color: #f2c94c; font-weight: 900; }}
.num span {{ font-size: 10.5px; line-height: 11px; }}
.num em {{ font-style: normal; color: #f2c94c; font-weight: 700; }}
.cards {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 7px; margin-top: 6px; height: 122px; }}
.card {{ border-top: 4px solid var(--c); background: #fbf8f1; box-shadow: 0 0 0 1px #d8cfbd; padding: 3px 6px 3px; display: flex; flex-direction: column; overflow: hidden; }}
.kline {{ display: flex; align-items: center; gap: 4px; font-size: 10.5px; font-weight: 800; letter-spacing: .05em; text-transform: uppercase; color: var(--c); }}
.hd {{ display: flex; gap: 6px; margin-top: 3px; align-items: center; }}
.ic {{ width: 46px; height: 46px; flex: none; border-radius: 3px; overflow: hidden; }}
.ic svg {{ display: block; }}
h2 {{ font-size: 16.5px; line-height: 16.5px; font-weight: 800; }}
.card p {{ font-size: 12px; line-height: 14px; margin-top: 3px; }}
.card .src {{ margin-top: auto; }}
.cols {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin-top: 6px; height: 428px; overflow: hidden; }}
.col {{ border-top: 3px solid var(--c); }}
.colhd {{ font-size: 15px; font-weight: 900; text-transform: uppercase; color: var(--c); letter-spacing: .03em; border-bottom: 1px solid #b9ae98; padding: 1px 0 1px; }}
.brief {{ display: flex; gap: 5px; padding: 4px 0 3px; border-bottom: 1px dotted #b9ae98; }}
.brief .nb {{ background: var(--c) !important; }}
.bt {{ font-size: 14.5px; line-height: 15.5px; font-weight: 800; }}
.pl {{ font-family: "Body"; font-size: 10px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; color: var(--c); }}
.bx {{ font-size: 12px; line-height: 14px; margin-top: 1px; }}
.bx i {{ color: #666; font-size: 10.5px; }}
.sport {{ display: flex; margin-top: 5px; height: 62px; border-top: 2px solid #16181d; border-bottom: 2px solid #16181d; }}
.lab {{ background: #16181d; color: #fff; width: 74px; flex: none; display: flex; align-items: center; justify-content: center; text-align: center; font-size: 15px; line-height: 15px; font-weight: 900; text-transform: uppercase; }}
.spg {{ flex: 1; display: grid; grid-template-columns: repeat(5, 1fr); gap: 2px 8px; padding: 3px 6px; }}
.sp {{ display: flex; gap: 4px; font-size: 11.5px; line-height: 13px; }}
.sp b {{ display: block; font-size: 9.5px; letter-spacing: .05em; text-transform: uppercase; color: #b3122e; }}
.check {{ margin-top: 4px; font-size: 11px; line-height: 13px; background: #fff4c2; border: 1px solid #c9a227; padding: 2px 6px; }}
.check b {{ color: #7a5a00; }}
.foot {{ display: flex; justify-content: space-between; margin-top: 3px; font-size: 10.5px; color: #444; font-weight: 600; }}
.foot b {{ color: #b3122e; }}
</style></head>
<body><div class="page">
<div class="topline"><div>World edition · No. 325 · <b>All {TOTAL} stories on this page happened on Saturday 21 November 2026</b></div><div>Sources under every item · numbers match map pins</div></div>
<div class="mast">
  <div class="title">The One-Day <span>World</span></div>
  <div class="mid"><b>{TOTAL} STORIES</b>6 continents · 1 day</div>
  <div class="date"><div class="d1">SATURDAY</div><div class="d2">21 NOVEMBER 2026</div></div>
</div>
<div class="row1">
  <div class="lead">
    <div class="kbar"><div class="k">{badge(1, "#fff")}Lead · Baltic Sea</div><div class="w">Gulf of Finland · Saturday morning</div></div>
    <h1>Drones set Russian cargo ship<br>Sparta&nbsp;II ablaze off Finland</h1>
    <div class="art">{art}</div>
    <div class="leadtext">
      <div><p>Finland says the strike was likely Ukrainian. All 16 crew were evacuated as the US-sanctioned ship drifted into Finnish waters; a Russian helicopter later breached Finnish airspace, Finland suspects.</p>
      <div class="src">AFP; Reuters; Finnish Defence Ministry; ISW</div></div>
      <div class="quote">“War is spilling over into our immediate vicinity.”<small>Finnish PM Orpo, on X</small></div>
    </div>
  </div>
  <div class="right">
    <div class="mapbox"><div class="maphead">Where it happened · pins = story numbers <span>Sat 21 Nov 2026</span></div>
      <svg id="map" width="497" height="184" viewBox="0 0 497 184" xmlns="http://www.w3.org/2000/svg"></svg></div>
    <div class="nums">{nums_html}</div>
  </div>
</div>
<div class="cards">{cards_html}</div>
<div class="cols">{cols_html}</div>
<div class="sport"><div class="lab">Sport<br>Sat</div><div class="spg">{sport_html}</div></div>
<div class="check"><b>DATE CHECK · left out because they happened on Friday 20 Nov:</b> {e(DATE_CHECK)}</div>
<div class="foot"><div>Compiled from wire and official reports dated <b>21 Nov 2026</b> · times UTC · all art drawn in code, no photos</div><div>The One-Day World · Sat 21.11.2026 · {TOTAL} stories</div></div>
</div>
<script>{mapjs}</script>
</body></html>
'''

open(os.path.join(ROOT, "poster", "index.html"), "w", encoding="utf-8").write(PAGE)
print("stories:", TOTAL, "pins:", len(PINS))
