def edit(p, rep):
    s = open(p).read()
    for a, b in rep:
        assert a in s, (p, a[:70]); s = s.replace(a, b)
    open(p, 'w').write(s)

edit('tools/build.py', [
 ('THE ONE-DAY WORLD &nbsp;·&nbsp; {TOTAL} STORIES · 6 REGIONS + SPACE · {DRAWN} DRAWN · ONE PAGE',
  'THE ONE-DAY WORLD &nbsp;·&nbsp; {TOTAL} STORIES · 5 REGIONS + GLOBAL · {DRAWN} DRAWINGS · ONE PAGE'),
 ('<div><span class="bd s" style="background:#2f5aa8">1</span> story no. = map pin</div>',
  '<div><span class="bd s" style="background:#2f5aa8">1</span> story number, also on map</div>'),
 ('<div class="mk">Markets closed: it’s Saturday</div>', '<div class="mk">Times in UTC · markets shut (Saturday)</div>'),
 ('("~04:00", "Geneva arms talks end"),\n    ("Overnight", "148 drones hit Ukraine"),',
  '("Overnight", "148 drones at Ukraine", "kryvyi"),\n    ("~04:00", "Geneva arms talks end", "robots"),'),
 ('("Morning", "Sparta II set ablaze")', '("Morning", "Sparta II set ablaze", "baltic")'),
 ('("09:42", "M6.8 Banda Sea quake")', '("09:42", "M6.8 Banda Sea quake", "quake")'),
 ('("10:34", "Heli breach suspected")', '("10:34", "Airspace breach suspected", "heli")'),
 ('("15:00", "EPL kick-offs")', '("15:00", "Chelsea v Leeds kicks off", "epl")'),
 ('("18:24", "Mercury orbit burn")', '("18:24", "Mercury orbit burn starts", "bepi")'),
 ('("Night", "COP31 halted, no deal")', '("Night", "COP31 halted, no deal", "cop")'),
 ('''timeline = "".join(f'<div class="tl"><b>{e(t)}{" UTC" if t[0].isdigit() or t[0] == "~" else ""}</b>{e(x)}</div>' for t, x in TIMELINE)''',
  '''REG = {k: r for _, k, r in ORDER}
timeline = "".join(f'<div class="tl"><b>{badge(N[k], rc(REG[k]), "t")}{e(t)}{" UTC" if t[0].isdigit() or t[0] == "~" else ""}</b>{e(x)}</div>' for t, x, k in TIMELINE)'''),
 ('kick="Ukraine war", src="AP · UKR AIR FORCE"', 'kick="Kryvyi Rih · Ukraine war", src="AP · UKR AIR FORCE"'),
 ('kick="Gaza City", src="REUTERS · GAZA MoH"', 'kick="Gaza City · aid", src="REUTERS · GAZA MoH"'),
 ('kick="Space · Mercury"', 'kick="Space · ESA–JAXA"'),
 ('h="Missiles kill 2 in Zelensky’s home city", p="A boy of 7 and a medic die in Kryvyi Rih."',
  'h="Missiles kill a boy, 7, and a medic in Zelensky’s home city", p="3 ballistic missiles, 148 drones overnight."'),
 ('h="COP31 deadlocked over fossil fuels", p="Talks halted for the night, a day over time."',
  'h="COP31 deadlocked over the move away from fossil fuels", p="Talks halted for the night, a day over time."'),
 ('h="“Killer robot” talks end without treaty", p="128 states agree only to “elaborate” rules."',
  'h="UN “killer robot” talks end without a treaty mandate", p="128 states agree only to “elaborate” rules."'),
 ('h="BepiColombo enters orbit around Mercury", p="37-minute burn ends an eight-year cruise."',
  'h="BepiColombo enters orbit around Mercury after 8 years", p="A 37-minute engine burn from 18:24 UTC."'),
 ('h="Deep M6.8 quake felt in Timor and Darwin", p="USGS green alert; no tsunami threat."',
  'h="Deep M6.8 quake shakes Timor-Leste and Darwin", p="USGS green alert; no tsunami threat."'),
 ('h="Sixth weekend of cost-of-living marches", p="Turnout dips after wage and school pledges."',
  'h="France marches for a sixth weekend over living costs", p="Turnout dips after wage and school pledges."'),
 ('h="Strike on food-aid vehicle kills three", p="WCK says the truck was not its own."',
  'h="Israeli strike on food-aid vehicle kills three", p="WCK says the truck was not its own."'),
 ('h="Costa cuts €204bn from EU budget plan", p="Adds a Big Tech tax; Merz says still too high."',
  'h="Costa cuts €204bn from the EU’s 2028–34 budget plan", p="Adds a Big Tech tax; Merz: still too high."'),
 ('p="Fausto Isidro Meza Flores, on the FBI’s Ten Most Wanted list, was seized in Guasave. Four soldiers and seven gunmen were killed."',
  'p="Fausto Isidro Meza Flores, one of the FBI’s Ten Most Wanted, was seized in Guasave; 4 soldiers and 7 gunmen died."'),
 ('const off = {{1: [-4, -13], 2: [16, -6], 3: [-2, 15], 4: [16, -2], 5: [-6, 16], 6: [-16, 8], 8: [12, 12], 9: [-16, -12], 10: [12, 14], 11: [-4, -16]}};',
  'const off = {{1: [-2, -11], 2: [16, -6], 3: [-2, 15], 4: [18, -6], 5: [-14, 12], 6: [-20, 14], 8: [12, 12], 9: [-24, -2], 10: [12, 14], 11: [-14, -14]}};'),
 ("""translate(4 112)"><rect width="74" height="34" rx="3" fill="#1a1236"/><circle cx="60" cy="17" r="10" fill="#9b948c"/>""",
  """translate(4 112)"><rect width="86" height="34" rx="3" fill="#1a1236"/><circle cx="72" cy="17" r="10" fill="#9b948c"/>"""),
 ("""<text x="24" y="14" font-size="7.5" font-weight="800" fill="#fff" font-family="Body">OFF MAP</text><text x="6" y="29" font-size="7.5" font-weight="800" fill="#f2c94c" font-family="Body">AT MERCURY</text>""",
  """<text x="23" y="14" font-size="8" font-weight="800" fill="#fff" font-family="Body">OFF MAP:</text><text x="6" y="28" font-size="8" font-weight="800" fill="#f2c94c" font-family="Body">AT MERCURY</text>"""),
 ('<div class="mn">Big pins: stories 1–11 · dots: briefs</div>', '<div class="mn">Numbered pins: stories 1–11 · small dots: briefs 12–40</div>'),
 ("PAGE = f'''", "assert N[BRIEFS[0][0]] == 12 and N[BRIEFS[-1][0]] == 40\nPAGE = f'''"),
])

edit('tools/art.py', [
 ('''<text x="110" y="24" font-size="22" font-weight="900" fill="#ffd36b" font-family="Head">M6.8</text>\'\'\'
    b += _tag(110, 34, "132 KM DEEP", "#fff", "#0f7c86", 10)
    b += _tag(188, 34, "09:42 UTC", "#111", "#fff", 9.5)''',
  '''<text x="106" y="26" font-size="24" font-weight="900" fill="#ffd36b" font-family="Head">M6.8</text>\'\'\'
    b += _tag(162, 10, "09:42 UTC", "#111", "#fff", 9.5)
    b += _tag(106, 36, "132 KM DEEP · NO TSUNAMI", "#fff", "#0f7c86", 9)'''),
 ('_tag(262, 54, "HELICOPTER", "#111", "#fff", 8.5)', '_tag(248, 54, "HELICOPTER 10:34", "#111", "#fff", 8.5)'),
])

edit('tools/style.css', [
 ('h1, h2, .title { font-family: "Head", sans-serif; }', 'h1, h2, .title { font-family: "Head", sans-serif; text-wrap: balance; }'),
 ('.srcr { margin-left: auto; font-size: 8.5px; font-weight: 700; color: #777;', '.srcr { margin-left: auto; font-size: 9px; font-weight: 700; color: #555;'),
 ('.card .srcr { font-size: 8px; }', '.card .srcr { font-size: 8.5px; }'),
 ('.lead p { font-size: 12px; line-height: 14.5px; padding: 3px 7px 0; }', '.lead p { font-size: 12px; line-height: 14.5px; padding: 3px 8px 6px; color: #222; }'),
 ('.lead h1 { font-size: 23px; line-height: 23px; font-weight: 900; padding: 3px 7px 0; }', '.lead h1 { font-size: 23px; line-height: 23.5px; font-weight: 900; padding: 3px 8px 0; }'),
 ('.bd.s { width: 16px; height: 16px; font-size: 9px; }', '.bd.s { width: 15px; height: 15px; font-size: 8.5px; }\n.bd.t { width: 13px; height: 13px; font-size: 7.5px; margin-right: 3px; }'),
 ('.br { display: flex; gap: 4px; align-items: center; height: 13.6px; min-width: 0;', '.br { display: flex; gap: 4px; align-items: center; height: 14.1px; min-width: 0;'),
 ('.bs { font-size: 7.5px; font-weight: 700; color: #888; letter-spacing: .05em; margin-left: 3px; }', '.bs { font-size: 8.5px; font-weight: 700; color: #666; letter-spacing: .04em; margin-left: 4px; }'),
 ('.lg { display: flex; flex-wrap: wrap; gap: 1px 8px; font-size: 10px; font-weight: 700; margin-top: 3px; }', '.lg { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px 6px; font-size: 10px; font-weight: 700; margin-top: 3px; }'),
 ('.tl b { display: block; color: #b3122e; font-size: 10px; letter-spacing: .04em; text-transform: uppercase; }', '.tl b { display: flex; align-items: center; color: #b3122e; font-size: 10px; letter-spacing: .04em; text-transform: uppercase; }'),
 ('.card h2 { font-size: 16px; line-height: 16.5px; font-weight: 800; padding: 2px 6px 0; }', '.card h2 { font-size: 15.5px; line-height: 16.5px; font-weight: 800; padding: 2px 7px 0; }'),
 ('.card p { font-size: 11.5px; line-height: 13.5px; padding: 1px 6px 0; color: #333; }', '.card p { font-size: 11.5px; line-height: 13.5px; padding: 1px 7px 0; color: #333; }'),
])
print("ok")
