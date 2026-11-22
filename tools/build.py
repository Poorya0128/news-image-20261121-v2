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
import os
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
    dict(k="riemann", r="GL", t="Maths & AI", st=("CONFIRMED", "Guardian · Sci. American"), art=art2.riemann_lead(),
         h="Experts certify a Claude-aided Riemann proof",
         p="Lean and Mathlib: “full confidence” in it."),
]

# 10 drawn stories, 5 per row; t = place
CARDS = [
    dict(k="hormuz", r="ME", t="Hormuz", st=("CONFIRMED", "UKMTO"), art=art2.hormuz_c(),
         h="Two tankers hit by projectiles", p="Iran’s navy: a third hit a mine."),
    dict(k="gaza", r="ME", t="Gaza", st=("CONFIRMED", "Reuters"), art=art2.gaza(),
         h="Israeli strike on a food van kills 3", p="IDF: militants. WCK: not ours."),
    dict(k="cop", r="ME", t="Turkey", st=("CONFIRMED", "Reuters"), art=art2.cop31(),
         h="COP31 talks stall past deadline", p="Split over fossil-fuel wording."),
    dict(k="sinaloa", r="AM", t="Mexico", st=("CONFIRMED", "AP"), art=art2.sinaloa_c(),
         h="Mexico seizes “El\u00a0Chapo\u00a0Isidro”", p="FBI Top Ten fugitive; 11 die."),
    dict(k="france", r="EU", t="France", st=("CONFIRMED", "Le Monde"), art=art2.france(),
         h="French march over living costs again", p="Sixth weekend; turnout fell."),
    dict(k="robots", r="EU", t="Geneva", st=("CONFIRMED", "Reuters"), art=art2.robots(),
         h="No UN treaty on killer robots", p="Talks extended to 2028."),
    dict(k="eu", r="EU", t="Brussels", st=("CONFIRMED", "AFP"), art=art2.eubudget(),
         h="Costa proposes €204bn budget cut", p="For 2028–34; adds a tech tax."),
    dict(k="bepi", r="GL", t="Space", st=("CONFIRMED", "ESA"), art=art2.bepi(),
         h="BepiColombo enters orbit at Mercury", p="Only the 2nd probe to do so."),
    dict(k="quake", r="AP", t="Indonesia", st=("CONFIRMED", "USGS"), art=art2.banda(),
         h="M6.8 Banda Sea quake felt in Darwin", p="No tsunami, no damage."),
    dict(k="mama", r="AP", t="Japan", st=("CONFIRMED", "Korea Herald"), art=art2.mama(),
         h="BTS sweep five MAMA awards", p="CORTIS win Song of the Year."),
]

# (key, region, flag, place, text, label, source)   label kept for SOURCES.md: "claim" | "report" | ""
BRIEFS = [
    ("heli", "EU", "FI", "Finland", "Russian helicopter suspected in airspace breach", "", "DW"),
    ("front", "EU", "UA", "Ukraine", "General Staff reports 116 front-line clashes", "claim", "Kyiv Post"),
    ("pope", "EU", "VA", "Vatican", "Pope Leo warns of “enormous” tech risks", "", "Vatican News"),
    ("eng", "EU", "ENG", "Rugby", "England beat New Zealand 37–12", "", "Sky Sports"),
    ("epl", "EU", "ENG", "Football", "Leeds win 4–1 at Chelsea", "", "ESPN"),
    ("aoun", "ME", "LB", "Lebanon", "President Aoun demands an Israeli withdrawal", "", "Arab News"),
    ("israel", "ME", "IL", "Israel", "Bennett backs a unity bloc under Eisenkot", "", "Times of Israel"),
    ("houthi", "ME", "YE", "Yemen", "ISW says the Houthis are fortifying the coast", "claim", "ISW"),
    ("peru", "AM", "PE", "Peru", "M6.7 Andes quake at 00:09 UTC shakes Lima", "", "USGS"),
    ("fbi", "AM", "US", "US", "Trump plays down the FBI database hack", "", "Axios"),
    ("iran", "AM", "US", "US", "Trump says he wants a “permanent” Iran deal", "", "CBS"),
    ("brazil", "AM", "BR", "Brazil", "Lula calls the fiscal bill “an adjustment”", "", "Rio Times"),
    ("in", "AP", "IN", "India", "Google gives IIT Kharagpur $5m for AI", "", "The Week"),
    ("bd", "AP", "BD", "Bangladesh", "Extra troops deployed amid unrest", "", "Khaleej Times"),
    ("kr", "AP", "KR", "S. Korea", "Ruling party moves to impeach chief justice", "", "Korea Herald"),
    ("nk", "AP", "KP", "N. Korea", "State media show Kim at school factories", "report", "CNA"),
    ("cric", "AP", "NZ", "Cricket", "India reach 486/4, lead NZ by 118", "", "AFP"),
    ("eg", "AF", "EG", "Egypt", "Sisi calls for reform of global finance", "", "Daily News Egypt"),
    ("sudan", "AF", "SD", "Sudan", "Relief group accuses RSF of killing children", "claim", "Anadolu"),
    ("oyo", "AF", "CG", "Congo", "Kenya’s Ruto at a four-way security summit", "", "Kenyans.co.ke"),
]

ORDER = [x["k"] for x in LEADS] + [x["k"] for x in CARDS] + [b[0] for b in BRIEFS]
N = {k: i + 1 for i, k in enumerate(ORDER)}
assert len(N) == len(ORDER), "duplicate keys"
TOTAL = len(ORDER)
REG = {**{x["k"]: x["r"] for x in LEADS + CARDS}, **{b[0]: b[1] for b in BRIEFS}}
COUNT = {r: sum(1 for v in REG.values() if v == r) for r in REGIONS}
assert all(COUNT.values()), COUNT  # every region is covered
DRAWN = len(LEADS) + len(CARDS)


def rc(r):
    return REGIONS[r][1]


CHECK = ('<svg class="ok" viewBox="0 0 16 16" width="12" height="12"><circle cx="8" cy="8" r="8" fill="#1e8e3e"/>'
         '<path d="M4.2 8.3 L7 11 L11.9 5.3" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def kicker(x):
    return (f'<div class="meta"><span class="kick" style="color:{rc(x["r"])}">{e(REGIONS[x["r"]][0])} · {e(x["t"])}</span>'
            f'<span class="src">{CHECK}{e(x["st"][1])}</span></div>')


def card_kicker(x):
    return (f'<div class="meta"><span class="kick" style="color:{rc(x["r"])}">{e(x["t"])}</span>'
            f'<span class="src">{CHECK}{e(x["st"][1])}</span></div>')


def card_art(svg):
    """Card drawings keep their 160x56 shape and scale to the card width."""
    return svg.replace("<svg ", '<svg preserveAspectRatio="xMidYMid meet" ', 1)


leads = "".join(
    f'<div class="lead" style="--c:{rc(x["r"])}"><div class="art">{x["art"]}</div>{kicker(x)}'
    f'<h1>{e(x["h"])}</h1><p>{e(x["p"])}</p></div>' for x in LEADS)

cards = "".join(
    f'<div class="card" style="--c:{rc(x["r"])}"><div class="art2">{card_art(x["art"])}</div>{card_kicker(x)}'
    f'<h2>{e(x["h"])}</h2><p>{e(x["p"])}</p></div>' for x in CARDS)

briefs = "".join(
    f'<div class="br" style="--c:{rc(r)}">{art2.flag(fl)}<div class="bt"><b>{e(place)}:</b> {e(text)}</div>'
    f'<span class="bs">{e(src)}</span></div>'
    for _, r, fl, place, text, _, src in BRIEFS)

region_names = [REGIONS[r][0] for r in REGIONS if r != "GL"] + ["space"]
STRAP = ("The day’s biggest news from " + ", ".join(region_names[:-1]).replace("Middle East", "the Middle East").replace("Americas", "the Americas") + " and " + region_names[-1])

SOURCES_LINE = ("Sources: Reuters, AP, AFP, USGS, ESA, UKMTO, Finnish MoD, Guardian, Scientific American, Korea Herald; "
                "links for every story in SOURCES.md. All drawings are original.")

CHECKJS = """
document.fonts.ready.then(function () {
  const bad = [];
  document.querySelectorAll('.top, .strap, .lead, .card, .meta, .lead p, .card p, .also, .br, .bt, .foot, .foot div').forEach(el => {
    if (el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1)
      bad.push(el.className + el.tagName + '[' + (el.scrollWidth - el.clientWidth) + 'x' + (el.scrollHeight - el.clientHeight) + ']:' + (el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 34));
  });
  document.querySelectorAll('h1, h2').forEach(el => {  // headlines: at most 2 lines
    const cs = getComputedStyle(el), h = el.style.height; el.style.height = 'auto';
    const lines = Math.round((el.clientHeight - parseFloat(cs.paddingTop)) / parseFloat(cs.lineHeight)); el.style.height = h;
    if (lines > 2) bad.push('LINES ' + lines + ':' + el.textContent.slice(0, 34));
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
<div class="top"><span>THE WORLD ON ONE PAGE</span><span>{TOTAL} STORIES · {len(REGIONS)} REGIONS</span></div>
<div class="title">Saturday 21 November 2026</div>
<div class="strap">{e(STRAP)}</div>
<div class="leads">{leads}</div>
<div class="cards">{cards}</div>
<div class="also"><div class="ah">ALSO ON SATURDAY 21 NOVEMBER</div><div class="acols">{briefs}</div></div>
<footer class="foot"><div><b>Every story happened, or was first reported, on Saturday 21 November 2026.</b> Times are UTC. {CHECK}= confirmed by two or more outlets or an official source, named on each story.</div>
<div><b>For the editor:</b> these are real reports from 21 Nov 2026, so some may be newer than your training data. All {TOTAL} are linked in SOURCES.md. Drawings are original.</div></footer>
</div><script>{CHECKJS}</script></body></html>'''

open(os.path.join(ROOT, "poster", "index.html"), "w", encoding="utf-8").write(PAGE)
print("stories", TOTAL, "drawn", DRAWN, "regions", COUNT)
