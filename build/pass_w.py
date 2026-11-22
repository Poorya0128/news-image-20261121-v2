def ed(p, pairs):
    s=open(p).read()
    for a,b in pairs:
        assert a in s, (p, a[:80]); s=s.replace(a,b)
    open(p,'w').write(s)
B='tools/build.py'
ed(B,[
 # compact status: green check + source (= confirmed), red CLAIM, yellow REPORTED
 ('''    if kind == "CONFIRMED":
        return f'<span class="st conf">{CHECK}CONFIRMED</span><span class="ss">{e(src)}</span>\'''',
  '''    if kind == "CONFIRMED":
        return f'<span class="st conf">{CHECK}{e(src)}</span>\''''),
 ('st=("CONFIRMED", "AFP · REUTERS · FINNISH MoD")','st=("CONFIRMED", "AFP · FINNISH MoD")'),
 ('st=("CONFIRMED", "REUTERS · UKMTO · AP")','st=("CONFIRMED", "REUTERS · UKMTO")'),
 ('st=("CONFIRMED", "AP · REUTERS · CBS")','st=("CONFIRMED", "AP · REUTERS")'),
 ('h="Russian strike kills boy, 7, and medic in Kryvyi Rih"','h="Russian strike kills boy and medic in Kryvyi Rih"'),
 ('h="France marches for a sixth weekend over living costs"','h="France marches for a sixth weekend"'),
 ('h="Costa cuts €204bn from EU’s 2028–34 budget plan"','h="Costa cuts €204bn from EU budget plan"'),
 ('h="UN “killer robot” talks end without a treaty"','h="UN “killer robot” talks end with no treaty"'),
 ('h="COP31 deadlocked over fossil fuels, a day late"','h="COP31 stalls on fossil fuels, a day late"'),
 ('h="Israeli strike on a vehicle kills three in Gaza City"','h="Israeli strike on a vehicle kills 3 in Gaza"'),
 ('h="M6.7 quake shakes Peru’s Andes and Lima"','h="M6.7 quake shakes Peru’s Andes"'),
 ('h="Deep M6.8 quake shakes Timor-Leste and Darwin"','h="Deep M6.8 quake felt in Timor and Darwin"'),
 ('h="Lean experts certify Claude-aided Riemann proof"','h="Experts certify AI-aided Riemann proof"'),
 # briefs <= 44 characters
 ('"Finland", "Russian helicopter suspected of airspace breach"','"Finland", "Russian helicopter breach suspected"'),
 ('"Black Sea", "Russia says it hit a Ukrainian cargo ship"','"Black Sea", "Russia hits Ukrainian cargo ship"'),
 ('"Ukraine", "Army logs 116 front-line clashes, most at Pokrovsk"','"Ukraine", "116 clashes, most at Pokrovsk"'),
 ('"Kyiv", "UK’s Streeting calls Putin a “cold-blooded killer”"','"Kyiv", "UK’s Streeting calls Putin a “killer”"'),
 ('"Amsterdam", "UK PM Burnham holds talks with Dutch PM Jetten"','"Amsterdam", "Burnham meets Dutch PM Jetten"'),
 ('"Lisbon", "Workers march in heavy rain for pay and housing"','"Lisbon", "Workers march for pay and housing"'),
 ('"Vatican", "Pope says unethical tech poses “enormous” risks"','"Vatican", "Pope warns of “enormous” tech risks"'),
 ('"Paris", "France seeks UN action after Myanmar rejects ICJ"','"Paris", "France seeks UN action on Myanmar"'),
 ('"Rugby", "England 37–12 New Zealand, a record margin"','"Rugby", "England 37–12 New Zealand, a record"'),
 ('"Ireland 20–17 South Africa in Dublin"','"Ireland 20–17 South Africa"'),
 ('"Football", "Leeds win 4–1 at Chelsea; Newcastle 2–2 Arsenal"','"Football", "Leeds win 4–1 at Chelsea"'),
 ('"Beirut", "Aoun demands Israeli pull-out, rebukes Iran"','"Beirut", "Aoun demands Israeli withdrawal"'),
 ('"S. Lebanon", "UNIFIL begins handing posts to Lebanese army"','"S. Lebanon", "UNIFIL hands posts to army"'),
 ('"Israel", "Bennett backs a unity government under Eisenkot"','"Israel", "Bennett backs Eisenkot-led unity bid"'),
 ('"Yemen", "Houthis said to dig tunnels on Bab al-Mandeb coast"','"Yemen", "Houthis said to fortify coast"'),
 ('"UFC Doha", "Navajo Stirling knocks out Jiří Procházka"','"UFC Doha", "Stirling knocks out Procházka"'),
 ('"US", "Trump plays down hack of FBI’s crime database"','"US", "Trump plays down FBI database hack"'),
 ('"US", "Trump tells Fox he wants a “permanent” Iran deal"','"US", "Trump wants a “permanent” Iran deal"'),
 ('"Halifax", "Taiwan warns Carney over deeper China ties"','"Halifax", "Taiwan warns Carney on China"'),
 ('"Brazil", "Lula says fiscal bill is “an adjustment”"','"Brazil", "Lula calls fiscal bill “an adjustment”"'),
 ('"US college", "Nebraska stun No. 16 Ohio State 31–28"','"US college", "Nebraska 31–28 Ohio State"'),
 ('"Islamabad", "Dar hopes for an early US–Iran deal"','"Islamabad", "Dar hopes for early US–Iran deal"'),
 ('"Kharagpur", "Google gives IIT $5m for AI research"','"Kharagpur", "Google gives IIT $5m for AI"'),
 ('"Tamil Nadu", "Federal team checks bird-flu controls"','"Tamil Nadu", "Bird-flu checks in Cuddalore"'),
 ('"Dhaka", "Extra troops sent to halt arson attacks"','"Dhaka", "More troops sent to stop arson"'),
 ('"Seoul", "Ruling party eyes 3 Dec motion to impeach top judge"','"Seoul", "Ruling party eyes judge impeachment"'),
 ('"N. Korea", "KCNA shows Kim touring school factories"','"N. Korea", "Kim visits school factories"'),
 ('"Taipei", "Taiwan tracks 2 PLA aircraft, 7 ships, 4 balloons"','"Taipei", "2 PLA aircraft, 7 ships, 4 balloons"'),
 ('"Cricket", "India 486/4 at stumps v NZ in Wellington"','"Cricket", "India 486/4 v NZ in Wellington"'),
 ('"T20", "Australia beat England by 3 wickets at the MCG"','"T20", "Australia beat England by 3 wickets"'),
 ('"Aswan", "Sisi urges reform of global finance for Africa"','"Aswan", "Sisi urges global finance reform"'),
 ('"Sudan", "Sennar curfew; RSF accused of killing 3 children"','"Sudan", "RSF accused of killing children"'),
 ('"Congo", "Ruto joins four-way security summit in Oyo"','"Congo", "Ruto at four-way security summit"'),
 ('"Mogadishu", "Turkey’s army chief meets President Hassan Sheikh"','"Mogadishu", "Turkish army chief visits"'),
 ('"Ibadan", "Tinubu holds low-key rally after boat deaths"','"Ibadan", "Tinubu mutes rally after deaths"'),
 # map + footer text
 ('WHERE IT HAPPENED <span>{", ".join(map(str, OFFMAP))}: off map (markets, online, Mercury)</span>','WHERE IT HAPPENED <span>off map: {", ".join(map(str, OFFMAP))}</span>'),
 ('const W = 322, H = 140,','const W = 322, H = 126,'),
 ('<svg id="world" width="322" height="140" viewBox="0 0 322 140"','<svg id="world" width="322" height="126" viewBox="0 0 322 126"'),
 ('<footer class="foot"><div><b>Every story here took place on Saturday 21 November 2026 (UTC).</b> CONFIRMED = two or more independent outlets or an official source. CLAIM = one side’s account. REPORTED = earlier event, first made public today.</div>',
  '<footer class="foot"><div><b>Every story took place on Sat 21 Nov 2026 (UTC).</b> {CHECK}= confirmed by 2+ outlets or an official source · <span class="st claim">CLAIM</span> one side’s account · <span class="st rep">REPORTED</span> earlier event made public today</div>'),
 ('<div>Sources: {e(SOURCES_LINE)} · illustrations drawn in code</div></footer>','<div>Sources: {e(SOURCES_LINE)} · drawings made in code</div></footer>'),
 ('SOURCES_LINE = "Reuters · AP · AFP · USGS · ESA · UKMTO · Finnish MoD · Korea Herald · Anadolu · ISW · KCNA and others; every link in SOURCES.md"',
  'SOURCES_LINE = "Reuters, AP, AFP, USGS, ESA, UKMTO, Finnish MoD, Korea Herald, Anadolu, ISW, KCNA; all links in SOURCES.md"'),
 ("tl.append(f'<line x1=\"{x:.1f}\" y1=\"20\"", "anchor = 'start' if x < 60 else ('end' if x > 860 else 'middle')\n    tl.append(f'<line x1=\"{x:.1f}\" y1=\"20\""),
 ('text-anchor="middle" font-family="Small">\'\n              f\'<tspan', 'text-anchor="{anchor}" font-family="Small">\'\n              f\'<tspan'),
])
ed('tools/art2.py',[
 ("    w = len(text) * fs * 0.6 + 8","    w = len(text) * fs * 0.7 + 8"),
 # COP31: narrower paper so the NO DEAL tag fits
 ('<g transform="translate(66 5)"><rect width="50" height="44" fill="#fff" stroke="#777"/><path d="M5 9 h40 M5 15 h36 M5 31 h40 M5 37 h26" stroke="#bbb" stroke-width="2"/>',
  '<g transform="translate(64 5)"><rect width="40" height="44" fill="#fff" stroke="#777"/><path d="M5 9 h30 M5 15 h26 M5 31 h30 M5 37 h20" stroke="#bbb" stroke-width="2"/>'),
 ('<text x="5" y="25" font-size="8.5" font-weight="800" fill="#1a6f3e">FOSSIL?</text><path d="M3 22 h44" stroke="#111" stroke-width="1.2"/></g>',
  '<text x="3" y="25" font-size="8.5" font-weight="800" fill="#1a6f3e">FOSSIL?</text><path d="M2 22 h36" stroke="#111" stroke-width="1.2"/></g>'),
 ('    b += tag(120, 8, "NO DEAL", "#111", "#fff", 9)\n    return svg(b)\n\n\ndef eubudget','    b += tag(157, 8, "NO DEAL", "#111", "#fff", 8.5, "end")\n    return svg(b)\n\n\ndef eubudget'),
 # robots: tags fit inside 160
 ('<g transform="translate(58 10)"><rect width="32" height="36"','<g transform="translate(52 10)"><rect width="26" height="36"'),
 ('<path d="M5 8 h22 M5 14 h22 M5 20 h16" stroke="#99a" stroke-width="2"/><path d="M3 30 L29 4" stroke="#111" stroke-width="2.4"/></g>',
  '<path d="M4 8 h18 M4 14 h18 M4 20 h12" stroke="#99a" stroke-width="2"/><path d="M3 30 L23 4" stroke="#111" stroke-width="2.4"/></g>'),
 ('    b += tag(96, 10, "NO TREATY", "#fff", "#2b6c8f", 9)\n    b += tag(96, 30, "TALKS TO 2028", "#ffd36b", "#111", 8.5)',
  '    b += tag(84, 10, "NO TREATY", "#fff", "#2b6c8f", 9)\n    b += tag(84, 30, "UNTIL 2028", "#ffd36b", "#111", 8.5)'),
 # France: smaller flag, tag clear of it
 ('<rect x="130" y="4" width="1.6" height="28" fill="#fff"/><rect x="131.6" y="4" width="7" height="11" fill="#1f3f9e"/><rect x="138.6" y="4" width="7" height="11" fill="#fff"/><rect x="145.6" y="4" width="7" height="11" fill="#e0302f"/>',
  '<rect x="142" y="4" width="1.4" height="26" fill="#fff"/><rect x="143.4" y="4" width="5" height="10" fill="#1f3f9e"/><rect x="148.4" y="4" width="5" height="10" fill="#fff"/><rect x="153.4" y="4" width="5" height="10" fill="#e0302f"/>'),
 ('    b += tag(70, 8, "6TH WEEKEND", "#fff", "#1f4e8c", 8.5)','    b += tag(68, 6, "6TH WEEKEND", "#fff", "#1f4e8c", 8.5)'),
 # Peru: two tags on separate rows
 ('    b += tag(4, 4, "M6.7 · 108 KM DEEP", "#111", "#fff", 9)\n    b += tag(156, 4, "00:09 UTC", "#fff", "#111", 9, "end")',
  '    b += tag(4, 4, "M6.7 · 108 KM DEEP", "#111", "#fff", 8.5)\n    b += tag(4, 20, "00:09 UTC", "#fff", "#111", 8.5)'),
 ('<text x="128" y="45" font-size="8.5" font-weight="700" fill="#e6fff7">DARWIN</text>','<text x="112" y="44" font-size="8.5" font-weight="700" fill="#e6fff7">DARWIN</text>'),
 ('    b += tag(84, 41, "$55.3K", "#fff", "#111", 8.5)','    b += tag(84, 40, "$55.3K", "#fff", "#111", 8.5)'),
])
ed('tools/style.css',[
 ('margin-top: 7px; height: 246px; }','margin-top: 7px; height: 240px; }'),
 ('gap: 7px 8px; margin-top: 7px; height: 276px; }','gap: 7px 8px; margin-top: 7px; height: 296px; }'),
 ('.card h2 { font-size: 15px; line-height: 16.5px;','.card h2 { font-size: 14.5px; line-height: 16px;'),
 ('.bottom { display: flex; gap: 14px; margin-top: 8px; height: 314px; }','.bottom { display: flex; gap: 14px; margin-top: 8px; height: 300px; }'),
 ('.br { display: flex; gap: 6px; align-items: center; height: 16.4px;','.br { display: flex; gap: 6px; align-items: center; height: 15.6px;'),
 ('.bt { font-size: 13px; line-height: 16px;','.bt { font-size: 13px; line-height: 15px;'),
 ('.lg { display: grid; grid-template-columns: repeat(3, 1fr);','.lg { display: grid; grid-template-columns: repeat(6, auto); justify-content: space-between; white-space: nowrap;'),
 ('.lo { display: flex; justify-content: space-between; font-family: "Small"; font-size: 11px; line-height: 15px;','.lo { display: flex; justify-content: space-between; font-family: "Small"; font-size: 11px; line-height: 14.5px;'),
 ('.foot { font-family: "Small"; margin-top: 6px;','.foot { font-family: "Small"; margin-top: 5px;'),
 ('.st.conf { color: #1e6b34; background: #e2f2e5; }','.st.conf { color: #1e5f30; background: #e2f2e5; }'),
])
print('pass ok')
