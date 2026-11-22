def ed(p, pairs):
    s=open(p).read()
    for a,b in pairs:
        assert a in s, (p, a[:80]); s=s.replace(a,b)
    open(p,'w').write(s)
ed('tools/build.py',[
 ('<div class="sub">Every story took place 00:00–24:00 UTC on Saturday 21 November 2026 · illustrated stories 1–11 are each confirmed by two or more independent sources</div>',
  '<div class="sub">Every story took place 00:00–24:00 UTC on Saturday 21 November 2026 · stories 1–11 confirmed by 2+ sources</div>'),
 ('<div><span class="bd s" style="background:#1f5fbf">1</span>story number, same on map</div>','<div><span class="bd s" style="background:#1f5fbf">1</span>story no., same on map</div>'),
 ('<div class="nb">1–11 carry no label: all confirmed</div>','<div class="nb">1–11: no label, all confirmed</div>'),
 ('("15:16", "Bitcoin back at $60k", "btc")','("15:16", "Bitcoin at $60k", "btc")'),
 ('("18:24", "Mercury burn starts", "bepi")','("18:24", "Mercury burn", "bepi")'),
 ('("20:00", "116 clashes logged", "front")','("20:00", "116 clashes", "front")'),
 ('("10:34", "Heli over Loviisa", "heli")','("10:34", "Heli incursion", "heli")'),
 ('p="UKMTO reports both near Oman’s Khasab; no casualties. Iran’s navy says a third hit a mine (unverified)."',
  'p="UKMTO: both near Oman’s Khasab, no casualties. Iran says a third hit a mine (unverified)."'),
 ('p="Fausto Isidro Meza Flores, on the FBI’s Ten Most Wanted list, was seized in Guasave; 4 soldiers and 7 gunmen died."',
  'p="FBI Ten Most Wanted fugitive Fausto Isidro Meza Flores seized; 4 soldiers, 7 gunmen killed."'),
 ('p="Finland says the drones that hit the US-sanctioned ship were likely Ukrainian; all 16 crew were evacuated."',
  'p="Finland says the drones were likely Ukrainian. All 16 crew of the US-sanctioned ship got off."'),
 ('("ok", "Counted", "00:00–24:00 UTC, Saturday 21 November")','("ok", "Counted", "00:00–24:00 UTC, Sat 21 Nov")'),
 ('("edge", "Edge, counted", "Peru M6.7 quake at 00:09 UTC (19:09 Fri in Lima)")','("edge", "Edge case", "Peru quake 00:09 UTC: in")'),
 ('("rep", "Exception", "KCNA report of a 20 Nov visit, marked REPORT")','("rep", "Exception", "Kim visit 20 Nov, told Sat")'),
 ('("out", "Before, left out", "Missiles in Poland · Brazil storm · UK–EU deal")','("out", "Too early", "Poland missiles · Brazil storm")'),
 ('("out", "After, left out", "Las Vegas GP · Sudamericana final")','("out", "Too late", "Las Vegas GP · Sudamericana")'),
 ('const W = 330, H = 136,','const W = 330, H = 124,'),
 ('<svg id="world" width="330" height="136" viewBox="0 0 330 136"','<svg id="world" width="330" height="124" viewBox="0 0 330 124"'),
 ("'<g transform=\"translate(6 112)\">","'<g transform=\"translate(6 100)\">"),
 ('("eng", "EU", "Rugby · London", "England 37–12 NZ", "SKY"','("eng", "EU", "Rugby", "England 37–12 NZ", "SKY"'),
 ('("epl", "EU", "EPL · London", "Chelsea 1–4 Leeds", "ESPN"','("epl", "EU", "Premier League", "Chelsea 1–4 Leeds", "ESPN"'),
 ('("cric", "AP", "Test · Wellington", "India 486/4 v NZ", "AFP"','("cric", "AP", "Test cricket", "India 486/4 v NZ", "AFP"'),
 ('("t20", "AP", "T20 · Melbourne", "Aus beat England", "ESPN"','("t20", "AP", "T20 cricket", "Aus beat England", "ESPN"'),
 ('("cfb", "AM", "NCAA · Lincoln", "Nebraska 31–28 OSU", "NBC"','("cfb", "AM", "NCAA", "Nebraska 31–28 OSU", "NBC"'),
 ('("ufc", "ME", "UFC · Doha", "Stirling wins by KO", "UFC"','("ufc", "ME", "UFC Doha", "Stirling wins by KO", "UFC.COM"'),
])
ed('tools/style.css',[
 ('.trust { width: 226px; flex: none; border-left: 1px solid #3a4a6a; padding-left: 10px; font-family: "Small"; font-size: 10.5px; line-height: 14px;','.trust { width: 212px; flex: none; border-left: 1px solid #3a4a6a; padding-left: 10px; font-family: "Small"; font-size: 10.5px; line-height: 13.6px;'),
 ('.trust .th { font-weight: 800; letter-spacing: .12em; color: #f2c94c; font-size: 10px; }','.trust .th { font-weight: 800; letter-spacing: .12em; color: #f2c94c; font-size: 9.5px; line-height: 12px; }'),
 ('.trust .bd.s', '.trust .bd.s') if False else ('.trust .nb {','.trust .bd.s { width: 14px; height: 14px; font-size: 8.5px; }\n.trust .claim, .trust .rep { font-size: 8px; line-height: 11px; }\n.trust .nb {'),
 ('.dcr b { width: 96px; flex: none; color: #3a2c00; font-weight: 700; }','.dcr b { width: 74px; flex: none; color: #3a2c00; font-weight: 700; }'),
 ('.sb { display: flex; align-items: center; gap: 6px; width: 122px; flex: none; font-family: "Head"; font-weight: 900; font-size: 17px; line-height: 16px; }','.sb { display: flex; align-items: center; gap: 6px; width: 126px; flex: none; font-family: "Head"; font-weight: 900; font-size: 16px; line-height: 16px; }'),
 ('.sb svg { width: 74px; height: 33px; }','.sb svg { width: 62px; height: 28px; }'),
])
print('pass3 ok')
