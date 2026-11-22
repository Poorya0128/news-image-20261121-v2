def ed(p, pairs):
    s=open(p).read()
    for a,b in pairs:
        assert a in s, (p, a[:80]); s=s.replace(a,b)
    open(p,'w').write(s)
ed('tools/build.py',[
 # numbers: short captions
 ('("16", "crew evacuated off Finland", "baltic")','("16", "crew evacuated", "baltic")'),
 ('("$55.3k", "Bitcoin low, since Sept 2024", "btc")','("$55.3k", "Bitcoin low", "btc")'),
 ('("1859", "year Riemann posed it", "riemann")','("1859", "Riemann’s year", "riemann")'),
 ('("11", "killed in Sinaloa", "sinaloa")','("11", "dead in Sinaloa", "sinaloa")'),
 ('("148", "drones fired at Ukraine", "kryvyi")','("148", "drones at Ukraine", "kryvyi")'),
 ('("128", "states at Geneva talks", "robots")','("128", "states in Geneva", "robots")'),
 ('("€204bn", "cut from EU plan", "eu")','("€204bn", "EU budget cut", "eu")'),
 ('("20:00", "116 clashes logged", "front")','("20:00", "116 clashes", "front")'),
 ('("15:16", "Bitcoin at $60,192", "btc")','("15:16", "Bitcoin $60,192", "btc")'),
 # card decks <= 30 chars, single source in the band
 ('st=("CONFIRMED", "AP · REUTERS"), lon=-108.4','st=("CONFIRMED", "AP"), lon=-108.4'),
 ('p="FBI Ten Most Wanted cartel boss seized."','p="FBI Top Ten fugitive seized."'),
 ('st=("CONFIRMED", "REUTERS · UKMTO"), lon=56.3','st=("CONFIRMED", "UKMTO"), lon=56.3'),
 ('p="Iran says a third hit a mine (unverified)."','p="Iran: a third hit a mine."'),
 ('p="148 drones and 3 missiles overnight."','p="60 hurt, AP says."'),
 ('p="WCK: not its vehicle; Israel cites Jihad."','p="Accounts differ on the cargo."'),
 ('p="Fossil-fuel wording splits Antalya."','p="Fossil-fuel wording splits it."'),
 ('st=("CONFIRMED", "REUTERS · AP"), lon=6.1','st=("CONFIRMED", "REUTERS"), lon=6.1'),
 ('p="128 states agree to talk until 2028."','p="Talks go on until 2028."'),
 ('p="Adds a Big Tech tax; Merz objects."','p="Adds a Big Tech tax."'),
 ('st=("CONFIRMED", "ESA · AP"), lon=None','st=("CONFIRMED", "ESA"), lon=None'),
 ('p="37-minute burn from 18:24 UTC."','p="37-minute burn, 18:24 UTC."'),
 ('p="USGS green alert; no tsunami."','p="No tsunami, no damage."'),
 ('st=("CONFIRMED", "KOREA HERALD"), lon=135.5','st=("CONFIRMED", "K. HERALD"), lon=135.5'),
 ('p="CORTIS win Song of the Year."','p="CORTIS take Song of the Year."'),
 # briefs that overflowed
 ('"Black Sea", "Russia says it hit a Ukrainian ship"','"Black Sea", "Russia says it hit a cargo ship"'),
 ('"Ukraine", "Army logs 116 front-line clashes"','"Ukraine", "Army logs 116 clashes"'),
 ('"France", "Sixth weekend of cost-of-living marches"','"France", "Sixth weekend of cost-of-living protests"'),
 ('"Rugby", "England beat New Zealand 37–12, a record"','"Rugby", "England 37–12 New Zealand"'),
 # card markup: header band (number + label + status) replaces the meta row
 ('''    f'<div class="card" style="--c:{rc(x["r"])}"><div class="art2">{x["art"]}{banner(x)}</div>'
    f'<div class="meta">{kicker(x)}<span class="right">{status(x["st"])}</span></div><h2>{e(x["h"])}</h2>'
    f'<p>{e(x["p"])}</p></div>' for x in CARDS)''',
  '''    f'<div class="card" style="--c:{rc(x["r"])}"><div class="band" style="background:{rc(x["r"])}"><span class="n">{N[x["k"]]}</span>{e(x["tag"])}'
    f'<span class="bs2">{CHECK if x["st"][0] == "CONFIRMED" else ""}{e(x["st"][1])}</span></div>'
    f'<div class="art2">{x["art"]}</div><h2>{e(x["h"])}</h2><p>{e(x["p"])}</p></div>' for x in CARDS)'''),
 ('<span>stories 1–13 · dots: briefs · off map: {", ".join(map(str, OFFMAP))}</span>','<span>dots = briefs · off map: {", ".join(map(str, OFFMAP))}</span>'),
 ("document.querySelectorAll('.lead, .card, .meta,","document.querySelectorAll('.band, .lead, .card, .meta,"),
])
ed('tools/art2.py',[
 ('    b += tag(150, 104, "LOW ~$55,300 · LOWEST SINCE SEPT 2024", "#fff", "#111", 9.5)','    b += tag(172, 98, "LOW ~$55,300", "#fff", "#111", 9.5)\n    b += tag(20, 96, "LOWEST SINCE SEPT 2024", "#f7931a", "#111", 9)'),
 ('<text x="156" y="62" font-size="10" font-weight="700" fill="#5b3a8c">EVERY NON-TRIVIAL ZERO ON THE LINE</text>','<text x="156" y="62" font-size="10" font-weight="700" fill="#5b3a8c">ALL ZEROS ON THE LINE</text>'),
 ('tag(156, 72, "LEAN + MATHLIB: PROOF CORRECT", "#2a1a4a", "#fff", 9.5)','tag(156, 72, "LEAN + MATHLIB: CORRECT", "#2a1a4a", "#fff", 9.5)'),
 ('tag(156, 92, "CLAUDE-AIDED · LEVENT ALPÖGE", "#fff", "#2a1a4a", 9.5)','tag(156, 92, "CLAUDE-AIDED PROOF", "#fff", "#2a1a4a", 9.5)'),
])
ed('tools/style.css',[
 ('.title { font-size: 58px; line-height: 60px;','.title { font-size: 54px; line-height: 56px;'),
 ('.card { background: #fbf8f1; box-shadow: 0 0 0 1px #d8cfbd; border-top: 4px solid var(--c); overflow: hidden; }','.card { background: #fbf8f1; box-shadow: 0 0 0 1px #d8cfbd; overflow: hidden; }\n.band { display: flex; align-items: center; gap: 5px; height: 20px; padding: 0 6px 0 3px; color: #fff; font-family: "Small"; font-size: 10.5px; font-weight: 800; letter-spacing: .05em; white-space: nowrap; overflow: hidden; }\n.band .n { background: #fff; color: #16181d; border-radius: 50%; width: 15px; height: 15px; display: inline-flex; align-items: center; justify-content: center; font-size: 9px; flex: none; }\n.band .bs2 { margin-left: auto; display: inline-flex; align-items: center; font-size: 9.5px; font-weight: 700; letter-spacing: .02em; background: rgba(255,255,255,.92); color: #1e5f30; padding: 0 4px; border-radius: 2px; }'),
 ('.card h2 { font-size: 16px; line-height: 17px; font-weight: 800; padding: 2px 7px 0; }','.card h2 { font-size: 16px; line-height: 17px; font-weight: 800; padding: 4px 7px 0; }'),
 ('gap: 7px 9px; margin-top: 7px; height: 290px; }','gap: 7px 9px; margin-top: 7px; height: 288px; }'),
 ('.leads { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 6px; height: 244px; }','.leads { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 6px; height: 240px; }'),
 ('.nums { height: 42px; }','.nums { height: 40px; }'),
 ('.nm b { display: block; font-family: "Head"; font-size: 21px; line-height: 22px;','.nm b { display: block; font-family: "Head"; font-size: 20px; line-height: 21px;'),
 ('.row { display: flex; margin-top: 4px; border: 1px solid #c8bea8; background: #fbf8f1; height: 38px; }','.row { display: flex; margin-top: 4px; border: 1px solid #c8bea8; background: #fbf8f1; height: 37px; }'),
])
s=open('tools/style.css').read(); s=s.replace('.art2 .ban { font-size: 10px; left: 4px; top: 4px; }\n.art2 .ban span { width: 15px; height: 15px; font-size: 9px; }\n',''); open('tools/style.css','w').write(s)
print('ok')
