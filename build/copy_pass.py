def ed(p, pairs):
    s=open(p).read()
    for a,b in pairs:
        assert a in s, (p, a[:80]); s=s.replace(a,b)
    open(p,'w').write(s)
ed('tools/build.py',[
 ('"Finland", "Russian heli breach suspected"','"Finland", "Suspected heli incursion"'),
 ('"Black Sea", "Russia says it hit Ukraine ship"','"Black Sea", "Russia: hit Ukraine ship"'),
 ('"Front line", "116 clashes in a day"','"Front", "116 clashes in a day"'),
 ('"Geneva", "UN killer-robot talks: no treaty"','"Geneva", "No killer-robot treaty"'),
 ('"France", "6th weekend of living-cost marches"','"France", "6th weekend of protests"'),
 ('"Yemen", "Houthis said to dig in on coast"','"Yemen", "Houthis fortify coast"'),
 ('"Peru", "M6.7 quake, 00:09 UTC; no damage"','"Peru", "M6.7 quake, no damage"'),
 ('"Brasília", "Lula: fiscal bill an “adjustment”"','"Brazil", "Lula defends fiscal bill"'),
 ('"Washington", "Trump plays down FBI hack"','"US", "Trump plays down FBI hack"'),
 ('"Washington", "Trump: “permanent” Iran deal"','"US", "Trump wants “permanent” Iran deal"'),
 ('"Seoul", "Bid to impeach top judge on 3 Dec"','"Seoul", "Move to impeach top judge"'),
 ('"Pyongyang", "Kim tours school factories"','"N. Korea", "Kim tours factories"'),
 ('"Aswan", "Sisi urges global finance reform"','"Aswan", "Sisi urges finance reform"'),
 ('"Sudan", "RSF accused of killing children"','"Sudan", "RSF accused of killings"'),
 ('"Oyo, Congo", "Ruto at four-way summit"','"Congo", "Ruto at four-way summit"'),
 ('"Mogadishu", "Turkish army chief visits"','"Somalia", "Turkish army chief visits"'),
 ('"Australia beat England", "ESPN"','"Aus beat England", "ESPN"'),
 ('"Stirling KOs Procházka", "UFC"','"Stirling wins by KO", "UFC"'),
 ('p="Adds a Big Tech tax; Merz: still too high."','p="Plus a Big Tech tax; Merz objects."'),
 ('THE ONE-DAY WORLD &nbsp;·&nbsp; {TOTAL} STORIES · 6 REGIONS · {DRAWN} ILLUSTRATED · EVERY ITEM SOURCED','THE ONE-DAY WORLD &nbsp;·&nbsp; {TOTAL} STORIES · {DRAWN} ILLUSTRATED · ALL SOURCED'),
 ('<div class="nb">No label on 1–11: each confirmed by 2+ sources</div>','<div class="nb">1–11 carry no label: all confirmed</div>'),
 ('ISW Inst. for the Study of War','ISW Inst. Study of War'),
 ('const W = 330, H = 170,','const W = 330, H = 136,'),
 ('<svg id="world" width="330" height="170" viewBox="0 0 330 170"','<svg id="world" width="330" height="136" viewBox="0 0 330 136"'),
 ("'<g transform=\"translate(6 146)\">","'<g transform=\"translate(6 112)\">"),
])
ed('tools/style.css',[
 ('.bottom { display: flex; gap: 14px; margin-top: 6px; height: 250px; }','.bottom { display: flex; gap: 14px; margin-top: 6px; height: 244px; }'),
 ('.br { display: flex; gap: 6px; align-items: center; height: 20.8px;','.br { display: flex; gap: 6px; align-items: center; height: 20.2px;'),
 ('.dcr { display: flex; align-items: center; gap: 6px; font-family: "Small"; font-size: 11px; line-height: 15px;','.dcr { display: flex; align-items: center; gap: 6px; font-family: "Small"; font-size: 11px; line-height: 15.5px;'),
 ('.lead p { font-size: 13px; line-height: 15.5px;','.lead p { font-size: 13px; line-height: 15px;'),
 ('.sb { display: flex; align-items: center; gap: 6px; width: 132px;','.sb { display: flex; align-items: center; gap: 6px; width: 122px;'),
 ('.sp { display: flex; gap: 6px; font-size: 13.5px;','.sp { display: flex; gap: 6px; font-size: 13px;'),
])
print('copy ok')
