"""Hand-written SVG illustrations for the front page (all drawn in code)."""


def _cap(w, h, text, bg="#0f1a2e"):
    return (f'<rect x="0" y="{h-17}" width="{w}" height="17" fill="{bg}" opacity=".92"/>'
            f'<text x="{w/2}" y="{h-5}" font-size="10.5" font-weight="800" fill="#fff" text-anchor="middle" '
            f'letter-spacing="1.6" font-family="Body">{text}</text>')


def _tag(x, y, text, bg="#b3122e", fg="#fff", fs=10.5, pad=5, w=None):
    w = w or (len(text) * fs * 0.56 + pad * 2)
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{fs+6}" rx="2" fill="{bg}"/>'
            f'<text x="{x + w/2:.0f}" y="{y + fs + 1.6:.1f}" font-size="{fs}" font-weight="800" fill="{fg}" '
            f'text-anchor="middle" font-family="Body" letter-spacing=".5">{text}</text>')


def svg(w, h, body):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="Body">{body}</svg>')


# ------------------------------------------------------------------ leads 328x132
def baltic(w=328, h=132):
    b = '''<defs><linearGradient id="bs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22304f"/>
    <stop offset=".6" stop-color="#8a4b55"/><stop offset="1" stop-color="#e59a5c"/></linearGradient>
    <radialGradient id="bg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffd36b" stop-opacity=".95"/>
    <stop offset=".5" stop-color="#ff7a1a" stop-opacity=".5"/><stop offset="1" stop-color="#ff5a00" stop-opacity="0"/></radialGradient></defs>
    <rect width="328" height="132" fill="url(#bs)"/>
    <path d="M0 78 L30 74 L58 77 L80 72 L112 75 L130 73 L130 80 L0 80Z" fill="#3a3550"/>
    <text x="6" y="70" font-size="10" font-weight="800" fill="#f6e7d6" letter-spacing="1">FINLAND</text>
    <g fill="#2a2628" opacity=".92"><ellipse cx="196" cy="48" rx="20" ry="13"/><ellipse cx="214" cy="32" rx="26" ry="14"/>
    <ellipse cx="246" cy="20" rx="34" ry="13"/><ellipse cx="286" cy="11" rx="44" ry="12"/></g>
    <rect y="80" width="328" height="52" fill="#183048"/>
    <g stroke="#6f8fb0" stroke-width="1.2" opacity=".55" fill="none"><path d="M10 98 q8 -3 16 0 t16 0"/><path d="M60 108 q8 -3 16 0 t16 0"/><path d="M270 100 q8 -3 16 0 t16 0"/></g>
    <ellipse cx="200" cy="72" rx="52" ry="30" fill="url(#bg)"/>
    <path d="M140 84 L148 96 L270 96 L278 80 L140 80Z" fill="#7d1d1d"/><path d="M140 80 L278 80 L277 83 L141 83Z" fill="#111"/>
    <rect x="148" y="66" width="22" height="14" fill="#ddd6c8"/><rect x="152" y="58" width="14" height="8" fill="#ddd6c8"/><rect x="161" y="50" width="4" height="8" fill="#111"/>
    <rect x="174" y="70" width="17" height="10" fill="#2f5f8a"/><rect x="193" y="70" width="17" height="10" fill="#a8432a"/><rect x="212" y="70" width="17" height="10" fill="#3d7a4a"/>
    <rect x="231" y="70" width="17" height="10" fill="#2f5f8a"/><rect x="250" y="70" width="17" height="10" fill="#b7882b"/>
    <path d="M190 70 C187 60 195 57 193 47 C201 53 200 60 204 63 C205 55 211 51 209 43 C219 52 218 62 215 70Z" fill="#ff7a1a"/>
    <path d="M196 70 C195 63 201 60 199 54 C205 59 205 64 207 66 C209 60 212 57 212 52 C217 59 216 66 213 70Z" fill="#ffd36b"/>
    <text x="178" y="92" font-size="9" font-weight="900" fill="#f3e9d8" letter-spacing="1.4">SPARTA II</text>
    <g fill="#111"><path d="M60 26 l16 4 l-16 4 l3 -4z"/><path d="M66 30 l-4 -7 l3 0 l6 7z"/><path d="M66 30 l-4 7 l3 0 l6 -7z"/>
    <path d="M92 42 l16 4 l-16 4 l3 -4z"/><path d="M98 46 l-4 -7 l3 0 l6 7z"/><path d="M98 46 l-4 7 l3 0 l6 -7z"/></g>
    <path d="M78 30 Q140 36 186 60" stroke="#ffe1a8" stroke-width="1.4" stroke-dasharray="4 3" fill="none"/>
    <path d="M110 46 Q150 52 190 66" stroke="#ffe1a8" stroke-width="1.4" stroke-dasharray="4 3" fill="none"/>
    <g fill="#111" transform="translate(300 40) scale(.7)"><ellipse cx="0" cy="0" rx="13" ry="6"/><rect x="10" y="-2" width="20" height="3"/>
    <rect x="-22" y="-9" width="44" height="2"/><rect x="-12" y="9.5" width="24" height="1.6"/></g>
    <path d="M286 96 L306 96 L303 101 L289 101Z" fill="#f28c28"/>'''
    b += _tag(8, 6, "2 DRONES · LIKELY UKRAINIAN, SAYS FINLAND", "#111", "#ffe1a8", 9.5)
    b += _tag(262, 54, "HELICOPTER", "#111", "#fff", 8.5)
    b += _tag(8, 90, "16 CREW EVACUATED", "#f28c28", "#111", 9.5)
    b += _cap(w, h, "GULF OF FINLAND · WEST OF SUURSAARI")
    return svg(w, h, b)


def hormuz(w=328, h=132):
    b = '''<rect width="328" height="132" fill="#2c6e9e"/>
    <path d="M0 0 L328 0 L328 40 L290 46 L262 38 L236 44 L214 34 L190 40 L170 30 L140 28 L110 22 L80 26 L50 18 L20 22 L0 16Z" fill="#e2cf9f"/>
    <path d="M0 132 L0 84 L30 80 L60 88 L92 84 L120 92 L150 86 L170 70 L186 62 L196 70 L200 86 L232 96 L262 110 L300 112 L328 104 L328 132Z" fill="#e2cf9f"/>
    <path d="M186 62 L192 56 L198 64 L196 70Z" fill="#e2cf9f"/>
    <g fill="#8e7a4e" opacity=".35"><circle cx="40" cy="8" r="2"/><circle cx="120" cy="12" r="2"/><circle cx="250" cy="20" r="2"/><circle cx="60" cy="110" r="2"/><circle cx="280" cy="124" r="2"/></g>
    <text x="150" y="16" font-size="14" font-weight="900" fill="#5e4a1e" letter-spacing="4">IRAN</text>
    <text x="40" y="104" font-size="10" font-weight="800" fill="#5e4a1e" letter-spacing="2">UAE</text>
    <text x="268" y="106" font-size="10" font-weight="800" fill="#5e4a1e" letter-spacing="2">OMAN</text>
    <text x="40" y="70" font-size="9.5" font-weight="700" fill="#cfe4f2" letter-spacing="2" font-style="italic">THE GULF</text>
    
    <text x="128" y="80" font-size="8.5" font-weight="800" fill="#fff" letter-spacing="1">STRAIT OF HORMUZ</text>'''
    for x, y in ((118, 56), (160, 46), (212, 56)):
        b += (f'<g transform="translate({x} {y})"><path d="M-12 0 L12 0 L9 5 L-10 5Z" fill="#1d1d1d"/><rect x="5" y="-5" width="5" height="5" fill="#eee"/>'
              f'<path d="M-3 -1 l2 -9 l2 6 l3 -8 l1 9 l4 -4 l-2 6z" fill="#ffd36b"/><circle cx="0" cy="-3" r="9" fill="none" stroke="#ff5a2a" stroke-width="1.4" stroke-dasharray="2 2"/></g>')
    b += '''<g transform="translate(276 54)"><path d="M-14 0 L14 0 M0 -4 L0 4 M-6 -10 L6 10 M6 -10 L-6 10" stroke="#111" stroke-width="0"/>
    <path d="M-12 -2 L10 -2 L14 0 L10 2 L-12 2Z" fill="#333"/><path d="M-2 -2 L-8 -12 L-4 -12 L4 -2Z M-2 2 L-8 12 L-4 12 L4 2Z" fill="#333"/>
    <path d="M-9 -9 L9 9 M9 -9 L-9 9" stroke="#ff3b3b" stroke-width="2.4"/></g>'''
    b += _tag(240, 72, "MQ-9 · IRGC CLAIM", "#111", "#ffd36b", 8.5)
    b += _tag(8, 30, "3 TANKERS HIT", "#b3122e", "#fff", 10.5)
    b += _cap(w, h, "STRAIT OF HORMUZ · IRAN WAR")
    return svg(w, h, b)


def sinaloa(w=328, h=132):
    b = '''<defs><linearGradient id="ns" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c1630"/><stop offset="1" stop-color="#3a2a40"/></linearGradient></defs>
    <rect width="328" height="132" fill="url(#ns)"/>
    <g fill="#fff" opacity=".7"><circle cx="20" cy="12" r="1"/><circle cx="90" cy="20" r="1"/><circle cx="170" cy="8" r="1"/><circle cx="300" cy="18" r="1"/></g>
    <path d="M60 30 L20 110 L110 110Z" fill="#fff7c2" opacity=".18"/><path d="M220 24 L180 110 L270 110Z" fill="#fff7c2" opacity=".18"/>
    <g fill="#111"><g transform="translate(62 28)"><ellipse rx="14" ry="6"/><rect x="10" y="-2" width="22" height="3"/><rect x="29" y="-6" width="3" height="9"/><rect x="-24" y="-10" width="48" height="2"/><rect x="-1" y="-9" width="2" height="3"/><rect x="-12" y="8" width="24" height="1.6"/></g>
    <g transform="translate(222 22) scale(.85)"><ellipse rx="14" ry="6"/><rect x="10" y="-2" width="22" height="3"/><rect x="29" y="-6" width="3" height="9"/><rect x="-24" y="-10" width="48" height="2"/><rect x="-12" y="8" width="24" height="1.6"/></g></g>
    <path d="M0 98 L20 98 L20 86 L36 86 L36 92 L52 92 L52 80 L70 80 L70 92 L96 92 L96 84 L120 84 L120 98 L328 98 L328 132 L0 132Z" fill="#1a1420"/>
    <rect y="98" width="328" height="34" fill="#2a2228"/>'''
    for x in (130, 200):
        b += (f'<g transform="translate({x} 96)"><rect x="0" y="-12" width="30" height="12" fill="#151515"/><rect x="30" y="-8" width="12" height="8" fill="#151515"/>'
              f'<circle cx="8" cy="1" r="3.5" fill="#000"/><circle cx="34" cy="1" r="3.5" fill="#000"/>'
              f'<path d="M4 -12 C1 -24 9 -26 7 -36 C15 -30 14 -22 18 -19 C19 -27 25 -30 23 -40 C33 -31 32 -20 28 -12Z" fill="#ff7a1a"/>'
              f'<path d="M9 -12 C8 -19 14 -21 12 -27 C17 -22 17 -18 19 -16 C21 -21 24 -23 24 -28 C28 -21 27 -16 24 -12Z" fill="#ffd36b"/></g>')
    b += '''<g transform="translate(270 52)"><rect x="0" y="0" width="48" height="40" fill="#f3ede1"/><rect x="0" y="0" width="48" height="9" fill="#b3122e"/>
    <text x="24" y="7" font-size="6" font-weight="900" fill="#fff" text-anchor="middle">FBI · TOP 10</text>
    <circle cx="24" cy="20" r="6" fill="#555"/><rect x="15" y="26" width="18" height="8" rx="3" fill="#555"/>
    <text x="24" y="39" font-size="5.5" font-weight="900" fill="#111" text-anchor="middle">CAPTURED</text></g>'''
    b += _tag(8, 44, "11 KILLED", "#b3122e", "#fff", 10.5)
    b += _tag(8, 64, "$5M US BOUNTY", "#111", "#ffd36b", 9.5)
    b += _cap(w, h, "GUASAVE, SINALOA · OVERNIGHT RAID")
    return svg(w, h, b)


# ------------------------------------------------------------------ cards 238x62
def kryvyi(w=238, h=62):
    b = '''<rect width="238" height="62" fill="#14182a"/>
    <g fill="#2a2f45"><rect x="6" y="30" width="20" height="32"/><rect x="28" y="22" width="16" height="40"/><rect x="46" y="34" width="22" height="28"/><rect x="70" y="26" width="14" height="36"/><rect x="86" y="38" width="24" height="24"/></g>
    <g fill="#ffd36b" opacity=".8"><rect x="10" y="36" width="3" height="3"/><rect x="32" y="28" width="3" height="3"/><rect x="50" y="40" width="3" height="3"/><rect x="74" y="32" width="3" height="3"/><rect x="92" y="44" width="3" height="3"/></g>
    <path d="M36 22 C33 14 40 12 38 4 C45 10 44 16 47 18 C48 13 52 11 51 6 C57 12 56 18 52 22Z" fill="#ff7a1a"/>
    <g stroke="#ff9a4a" stroke-width="1.6" fill="none"><path d="M170 4 L110 30"/><path d="M190 6 L130 34"/><path d="M210 8 L150 36"/></g>'''
    b += _tag(150, 40, "148 DRONES", "#ffd36b", "#111", 10)
    b += _tag(150, 22, "3 BALLISTIC", "#b3122e", "#fff", 10)
    return svg(w, h, b)


def cop31(w=238, h=62):
    b = '''<rect width="238" height="62" fill="#e8dcc0"/>
    <circle cx="36" cy="32" r="22" fill="#5fa8d3"/><path d="M20 22 C28 20 30 28 36 26 C42 24 40 18 46 18 C49 26 52 32 46 38 C42 44 34 40 30 48 C24 50 18 42 15 38 C13 30 15 26 20 22Z" fill="#7cc36b"/>
    <rect x="64" y="8" width="8" height="40" rx="4" fill="#fff" stroke="#555"/><circle cx="68" cy="50" r="7" fill="#e0302f"/><rect x="66" y="20" width="4" height="30" fill="#e0302f"/>
    <g transform="translate(92 10)"><rect width="66" height="24" rx="4" fill="#fff" stroke="#2e7d4f" stroke-width="1.5"/><path d="M10 24 L6 32 L18 24Z" fill="#fff" stroke="#2e7d4f" stroke-width="1.5"/>
    <text x="33" y="16" font-size="11" font-weight="900" fill="#2e7d4f" text-anchor="middle">NO DEAL</text></g>
    <g transform="translate(166 10)"><circle cx="16" cy="16" r="15" fill="#fff" stroke="#111" stroke-width="2"/><path d="M16 16 L16 6 M16 16 L24 20" stroke="#111" stroke-width="2"/></g>'''
    b += _tag(150, 40, "+1 DAY OVERTIME", "#2e7d4f", "#fff", 9.5)
    return svg(w, h, b)


def robots(w=238, h=62):
    b = '''<rect width="238" height="62" fill="#2b6c8f"/>
    <g transform="translate(14 6)"><rect x="6" y="10" width="40" height="30" rx="7" fill="#e9eef2"/><rect x="25" y="2" width="2" height="8" fill="#e9eef2"/><circle cx="26" cy="2" r="3" fill="#ffd36b"/>
    <circle cx="18" cy="24" r="5" fill="#d6283c"/><circle cx="34" cy="24" r="5" fill="#d6283c"/><rect x="16" y="33" width="20" height="3" fill="#2b6c8f"/><rect x="0" y="42" width="52" height="8" rx="2" fill="#1b3e52"/></g>
    <g transform="translate(84 14)"><rect x="0" y="0" width="40" height="34" fill="#fff"/><path d="M6 8 h28 M6 14 h28 M6 20 h20" stroke="#99a" stroke-width="2"/>
    <path d="M4 26 L36 6" stroke="#d6283c" stroke-width="3"/></g>
    <text x="134" y="28" font-size="11" font-weight="900" fill="#fff">TREATY?</text>'''
    b += _tag(134, 36, "RULES BY 2028", "#ffd36b", "#111", 10)
    return svg(w, h, b)


def bepi(w=238, h=62):
    b = '''<rect width="238" height="62" fill="#1a1236"/>
    <g fill="#fff" opacity=".7"><circle cx="10" cy="10" r="1"/><circle cx="60" cy="50" r="1"/><circle cx="120" cy="8" r="1"/><circle cx="200" cy="54" r="1"/><circle cx="226" cy="14" r="1"/></g>
    <circle cx="48" cy="34" r="24" fill="#9b948c"/><circle cx="40" cy="26" r="5" fill="#7c766f"/><circle cx="56" cy="42" r="6" fill="#7c766f"/><circle cx="58" cy="24" r="3" fill="#7c766f"/>
    <ellipse cx="48" cy="34" rx="40" ry="11" fill="none" stroke="#f2c94c" stroke-width="1.4" stroke-dasharray="3 2" transform="rotate(-18 48 34)"/>
    <g transform="translate(96 16) rotate(-18)"><rect x="-4" y="-4" width="8" height="8" fill="#e6e6e6"/><rect x="-20" y="-2.5" width="15" height="5" fill="#3d6fd6"/><rect x="5" y="-2.5" width="15" height="5" fill="#3d6fd6"/></g>
    <text x="124" y="24" font-size="10" font-weight="800" fill="#cfc3ff">ESA · JAXA</text>'''
    b += _tag(124, 32, "BURN 18:24 UTC", "#f2c94c", "#111", 10)
    return svg(w, h, b)


def quake(w=238, h=62):
    b = '''<rect width="238" height="62" fill="#0f7c86"/>
    <path d="M0 30 L40 30 L46 22 L52 40 L58 10 L64 50 L70 16 L76 44 L82 26 L88 34 L94 30 L238 30" stroke="#fff" stroke-width="2" fill="none" stroke-linejoin="round"/>
    <text x="110" y="24" font-size="22" font-weight="900" fill="#ffd36b" font-family="Head">M6.8</text>'''
    b += _tag(110, 34, "132 KM DEEP", "#fff", "#0f7c86", 10)
    b += _tag(188, 34, "09:42 UTC", "#111", "#fff", 9.5)
    return svg(w, h, b)


def france(w=238, h=62):
    b = '''<rect width="238" height="62" fill="#1f4e8c"/>
    <rect x="200" y="6" width="2" height="34" fill="#fff"/><rect x="202" y="6" width="9" height="14" fill="#1f3f9e"/><rect x="211" y="6" width="9" height="14" fill="#fff"/><rect x="220" y="6" width="9" height="14" fill="#e0302f"/>'''
    for i, x in enumerate((14, 40, 66, 92, 118, 144, 170)):
        b += f'<circle cx="{x}" cy="{38 + (i % 2) * 3}" r="6" fill="#0d2347"/><rect x="{x-6}" y="{44 + (i % 2) * 3}" width="12" height="20" rx="4" fill="#0d2347"/>'
    b += '<rect x="30" y="8" width="34" height="16" fill="#ffd36b"/><rect x="46" y="24" width="2" height="10" fill="#ffd36b"/><rect x="110" y="10" width="34" height="16" fill="#fff"/><rect x="126" y="26" width="2" height="8" fill="#fff"/>'
    b += '<text x="47" y="20" font-size="8" font-weight="900" fill="#111" text-anchor="middle">SALAIRES</text><text x="127" y="22" font-size="8" font-weight="900" fill="#1f4e8c" text-anchor="middle">SERVICES</text>'
    b += _tag(150, 30, "6TH WEEKEND", "#ffd36b", "#111", 9.5)
    return svg(w, h, b)


def gaza(w=238, h=62):
    b = '''<rect width="238" height="62" fill="#c9b48a"/><rect y="48" width="238" height="14" fill="#a8916a"/>
    <g fill="#bba27a"><rect x="150" y="18" width="22" height="30"/><rect x="176" y="10" width="18" height="38"/><rect x="198" y="24" width="30" height="24"/></g>
    <g transform="translate(20 22)"><rect x="0" y="4" width="50" height="22" fill="#eee"/><path d="M50 8 h14 l10 10 v8 h-24z" fill="#ddd"/><rect x="6" y="9" width="12" height="9" fill="#c9a25a"/><rect x="22" y="9" width="12" height="9" fill="#c9a25a"/>
    <circle cx="12" cy="28" r="5" fill="#222"/><circle cx="60" cy="28" r="5" fill="#222"/></g>
    <path d="M100 4 l3 10 l10 -5 l-6 9 l10 3 l-10 3 l5 9 l-10 -5 l-3 9 l-3 -9 l-9 5 l5 -9 l-10 -3 l10 -3 l-6 -9 l10 5z" fill="#ffd36b" stroke="#b3122e" stroke-width="1"/>'''
    b += _tag(122, 6, "3 KILLED", "#b3122e", "#fff", 9.5)
    return svg(w, h, b)


def eubudget(w=238, h=62):
    b = '''<rect width="238" height="62" fill="#003399"/>
    <circle cx="36" cy="31" r="24" fill="none" stroke="#ffcc00" stroke-width="0"/>'''
    import math
    for i in range(12):
        a = i * math.pi / 6
        b += f'<circle cx="{36 + 20*math.cos(a):.1f}" cy="{31 + 20*math.sin(a):.1f}" r="2.6" fill="#ffcc00"/>'
    b += '''<text x="36" y="40" font-size="24" font-weight="900" fill="#ffcc00" text-anchor="middle" font-family="Head">€</text>
    <g transform="translate(76 12)"><circle cx="6" cy="30" r="6" fill="none" stroke="#fff" stroke-width="2.5"/><circle cx="20" cy="30" r="6" fill="none" stroke="#fff" stroke-width="2.5"/>
    <path d="M9 25 L30 4 M17 25 L-2 4" stroke="#fff" stroke-width="2.5"/></g>
    <text x="114" y="30" font-size="21" font-weight="900" fill="#fff" font-family="Head">−€204bn</text>'''
    b += _tag(114, 38, "+ BIG TECH TAX", "#ffcc00", "#003399", 9.5)
    return svg(w, h, b)


def scoreboard(w=92, h=40):
    b = '''<rect width="92" height="40" rx="4" fill="#111"/><rect x="3" y="3" width="86" height="34" rx="3" fill="#1d2a1d"/>
    <text x="24" y="15" font-size="8" font-weight="800" fill="#9fdc9f" text-anchor="middle">ENG</text><text x="68" y="15" font-size="8" font-weight="800" fill="#9fdc9f" text-anchor="middle">NZL</text>
    <text x="24" y="33" font-size="17" font-weight="900" fill="#ffd36b" text-anchor="middle" font-family="Head">37</text>
    <text x="46" y="31" font-size="12" font-weight="900" fill="#ffd36b" text-anchor="middle">–</text>
    <text x="68" y="33" font-size="17" font-weight="900" fill="#ffd36b" text-anchor="middle" font-family="Head">12</text>'''
    return svg(w, h, b)


def daydial(size=64):
    """Ring showing day 325 of 365."""
    import math
    r = size / 2 - 5
    c = size / 2
    frac = 325 / 365
    a = 2 * math.pi * frac - math.pi / 2
    x, y = c + r * math.cos(a), c + r * math.sin(a)
    b = (f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="#2b3a5c" stroke-width="6"/>'
         f'<path d="M{c} {c-r} A{r} {r} 0 1 1 {x:.2f} {y:.2f}" fill="none" stroke="#f2c94c" stroke-width="6"/>'
         f'<text x="{c}" y="{c-2}" font-size="22" font-weight="900" fill="#fff" text-anchor="middle" font-family="Head">21</text>'
         f'<text x="{c}" y="{c+11}" font-size="9" font-weight="800" fill="#f2c94c" text-anchor="middle" letter-spacing="1">NOV</text>')
    return svg(size, size, b)
