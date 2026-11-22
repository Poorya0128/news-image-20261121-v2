"""Compact story-specific drawings for the 160x56 cards, plus simplified flags.

All lettering inside the drawings is 8.5 px or larger.
"""
import math

W, H = 160, 56


def svg(body, w=W, h=H):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="Small">{body}</svg>')


def tag(x, y, text, bg="#111", fg="#fff", fs=9, anchor="start"):
    w = len(text) * fs * 0.7 + 8
    if anchor == "end":
        x = x - w
    return (f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{fs + 5}" rx="2" fill="{bg}"/>'
            f'<text x="{x + w / 2:.0f}" y="{y + fs + 1}" font-size="{fs}" font-weight="800" fill="{fg}" '
            f'text-anchor="middle" letter-spacing=".3">{text}</text>')


def kryvyi():
    b = '<rect width="160" height="56" fill="#151a2c"/>'
    b += '<g fill="#2b3150"><rect x="4" y="28" width="14" height="28"/><rect x="20" y="20" width="12" height="36"/><rect x="34" y="32" width="16" height="24"/></g>'
    b += '<g fill="#ffd36b" opacity=".8"><rect x="7" y="33" width="2.5" height="2.5"/><rect x="24" y="26" width="2.5" height="2.5"/><rect x="38" y="38" width="2.5" height="2.5"/></g>'
    b += '<path d="M24 20 C22 13 28 11 26 4 C32 9 31 14 34 16 C35 12 38 10 37 6 C42 11 41 16 38 20Z" fill="#ff7a1a"/>'
    b += '<g stroke="#5a6288" stroke-width="2" fill="none"><path d="M64 56 L70 20 L76 56 M66 42 L74 42 M67 31 L73 31"/><circle cx="70" cy="20" r="4"/></g>'
    b += '<g stroke="#ff9a4a" stroke-width="1.6"><path d="M150 2 L104 22"/><path d="M156 10 L112 30"/></g>'
    b += tag(88, 36, "148 DRONES", "#ffd36b", "#111", 9)
    return svg(b)


def cop31():
    b = '<rect width="160" height="56" fill="#e6dcc3"/><rect y="42" width="160" height="14" fill="#b9a983"/>'
    b += '<g transform="translate(8 8)"><rect width="1.6" height="22" fill="#555"/><rect x="1.6" width="18" height="12" fill="#e30a17"/><circle cx="9" cy="6" r="3.3" fill="#fff"/><circle cx="10.1" cy="6" r="2.6" fill="#e30a17"/></g>'
    b += '<g transform="translate(34 8)"><rect width="1.6" height="22" fill="#555"/><rect x="1.6" width="18" height="12" fill="#012169"/><path d="M1.6 0 L10 5 M10 0 L1.6 5" stroke="#fff" stroke-width="1.2"/><circle cx="15" cy="8.5" r="1.4" fill="#fff"/></g>'
    b += '<rect x="4" y="30" width="56" height="12" fill="#6b5b3a"/><text x="32" y="39" font-size="8.5" font-weight="800" fill="#fff" text-anchor="middle">ANTALYA</text>'
    b += '<g transform="translate(64 5)"><rect width="40" height="44" fill="#fff" stroke="#777"/><path d="M5 9 h30 M5 15 h26 M5 31 h30 M5 37 h20" stroke="#bbb" stroke-width="2"/>'
    b += '<text x="3" y="25" font-size="8.5" font-weight="800" fill="#1a6f3e">FOSSIL?</text><path d="M2 22 h36" stroke="#111" stroke-width="1.2"/></g>'
    b += tag(157, 8, "NO DEAL", "#111", "#fff", 8.5, "end")
    return svg(b)


def eubudget():
    b = '<rect width="160" height="56" fill="#003399"/>'
    for i in range(12):
        a = i * math.pi / 6
        b += f'<circle cx="{18 + 11 * math.cos(a):.1f}" cy="{22 + 11 * math.sin(a):.1f}" r="1.7" fill="#ffcc00"/>'
    b += '<rect x="38" y="8" width="116" height="13" fill="#8fa6e6"/><text x="42" y="18" font-size="8.5" font-weight="800" fill="#001a66">COMMISSION</text>'
    b += '<rect x="38" y="26" width="84" height="13" fill="#ffcc00"/><text x="42" y="36" font-size="8.5" font-weight="800" fill="#001a66">COSTA</text>'
    b += '<rect x="122" y="26" width="32" height="13" fill="none" stroke="#ffcc00" stroke-dasharray="3 2"/>'
    b += '<text x="138" y="52" font-size="11" font-weight="800" fill="#fff" text-anchor="middle">−€204bn</text>'
    b += '<text x="6" y="51" font-size="8.5" font-weight="700" fill="#cfd8ff">2028–34</text>'
    return svg(b)


def bitcoin():
    pts = [(34, 12), (48, 16), (60, 28), (70, 40), (78, 46), (88, 36), (100, 28), (112, 22), (124, 18)]
    b = '<rect width="160" height="56" fill="#14181f"/><circle cx="16" cy="28" r="11" fill="#f7931a"/>'
    b += '<text x="16" y="33" font-size="13" font-weight="800" fill="#fff" text-anchor="middle">B</text>'
    b += '<path d="M14 15 V19 M18 15 V19 M14 37 V41 M18 37 V41" stroke="#fff" stroke-width="1.4"/>'
    b += '<path d="M' + " L".join(f"{x} {y}" for x, y in pts) + '" stroke="#f7931a" stroke-width="2.2" fill="none" stroke-linejoin="round"/>'
    b += '<circle cx="78" cy="46" r="2.6" fill="#fff"/><circle cx="124" cy="18" r="2.6" fill="#fff"/>'
    b += tag(84, 40, "$55.3K", "#fff", "#111", 8.5)
    b += tag(156, 4, "$60,192", "#f7931a", "#111", 9, "end")
    return svg(b)


def bepi():
    b = '<rect width="160" height="56" fill="#1a1236"/>'
    b += '<g fill="#fff" opacity=".7"><circle cx="8" cy="8" r="1"/><circle cx="70" cy="50" r="1"/><circle cx="150" cy="48" r="1"/></g>'
    b += '<circle cx="36" cy="30" r="20" fill="#9b948c"/><circle cx="29" cy="23" r="4" fill="#7c766f"/><circle cx="43" cy="37" r="5" fill="#7c766f"/>'
    b += '<ellipse cx="36" cy="30" rx="32" ry="9" fill="none" stroke="#f2c94c" stroke-width="1.3" stroke-dasharray="3 2" transform="rotate(-16 36 30)"/>'
    b += '<g transform="translate(78 14) rotate(-16)"><rect x="-4" y="-4" width="8" height="8" fill="#e6e6e6"/><rect x="-18" y="-2.5" width="13" height="5" fill="#3d6fd6"/><rect x="5" y="-2.5" width="13" height="5" fill="#3d6fd6"/></g>'
    b += tag(100, 30, "18:24 UTC", "#f2c94c", "#111", 9)
    return svg(b)


def riemann():
    b = '<rect width="160" height="56" fill="#f1edff"/><rect x="18" y="0" width="32" height="56" fill="#e0d8ff"/>'
    b += '<path d="M4 28 H70 M18 0 V56" stroke="#888"/><path d="M34 0 V56" stroke="#5b3a8c" stroke-width="2" stroke-dasharray="4 2"/>'
    b += '<g fill="#5b3a8c"><circle cx="34" cy="9" r="2.4"/><circle cx="34" cy="17" r="2.4"/><circle cx="34" cy="39" r="2.4"/><circle cx="34" cy="47" r="2.4"/></g>'
    b += '<text x="78" y="20" font-size="13" font-weight="800" fill="#2a1a4a">ζ(s) = 0</text>'
    b += '<text x="78" y="33" font-size="9" font-weight="700" fill="#5b3a8c">Re(s) = ½</text>'
    b += tag(78, 38, "LEAN-CHECKED", "#2a1a4a", "#fff", 8.5)
    return svg(b)


def banda():
    b = '<rect width="160" height="56" fill="#0f7c86"/>'
    b += '<path d="M0 30 L12 30 L16 22 L20 40 L24 12 L28 48 L32 18 L36 36 L40 30 L50 30" stroke="#fff" stroke-width="1.6" fill="none"/>'
    b += '<path d="M64 26 L84 21 L100 20 L106 24 L90 29 L72 32Z" fill="#cfe8d0"/>'
    b += '<path d="M96 56 L104 47 L124 46 L144 50 L160 48 L160 56Z" fill="#cfe8d0"/>'
    b += '<circle cx="124" cy="18" r="3.5" fill="#ffd36b"/><circle cx="124" cy="18" r="9" fill="none" stroke="#ffd36b" stroke-width="1.3"/>'
    b += '<text x="54" y="13" font-size="13" font-weight="800" fill="#ffd36b">M6.8</text>'
    b += '<text x="66" y="42" font-size="8.5" font-weight="700" fill="#e6fff7">TIMOR</text><text x="112" y="44" font-size="8.5" font-weight="700" fill="#e6fff7">DARWIN</text>'
    return svg(b)


def gaza():
    b = '<rect width="160" height="56" fill="#c9b48a"/><rect y="44" width="160" height="12" fill="#a8916a"/>'
    b += '<g fill="#bba27a"><rect x="118" y="16" width="16" height="28"/><rect x="136" y="8" width="20" height="36"/></g>'
    b += '<g transform="translate(8 22)"><rect y="4" width="40" height="16" rx="2" fill="#ece8e0"/><path d="M40 8 h10 l7 7 v5 h-17z" fill="#d6d1c7"/><circle cx="10" cy="22" r="4.5" fill="#222"/><circle cx="48" cy="22" r="4.5" fill="#222"/></g>'
    b += '<path d="M62 4 l3 8 l8 -4 l-4 8 l8 3 l-8 3 l4 7 l-8 -4 l-3 8 l-3 -8 l-7 4 l3 -7 l-8 -3 l8 -3 l-4 -8 l8 4z" fill="#ffd36b" stroke="#7a4a00"/>'
    b += tag(80, 6, "3 KILLED", "#111", "#fff", 9)
    return svg(b)


def france():
    b = '<rect width="160" height="56" fill="#1f4e8c"/>'
    b += '<rect x="142" y="4" width="1.4" height="26" fill="#fff"/><rect x="143.4" y="4" width="5" height="10" fill="#1f3f9e"/><rect x="148.4" y="4" width="5" height="10" fill="#fff"/><rect x="153.4" y="4" width="5" height="10" fill="#e0302f"/>'
    for i, x in enumerate((10, 28, 46, 64, 82, 100, 118)):
        b += f'<circle cx="{x}" cy="{36 + (i % 2) * 3}" r="5" fill="#0d2347"/><rect x="{x - 5}" y="{41 + (i % 2) * 3}" width="10" height="16" rx="3" fill="#0d2347"/>'
    b += '<rect x="14" y="6" width="50" height="14" fill="#ffd36b"/><rect x="38" y="20" width="2" height="10" fill="#ffd36b"/>'
    b += '<text x="39" y="16.5" font-size="8.5" font-weight="800" fill="#111" text-anchor="middle">SALAIRES</text>'
    b += tag(68, 6, "6TH WEEKEND", "#fff", "#1f4e8c", 8.5)
    return svg(b)


def robots():
    b = '<rect width="160" height="56" fill="#2b6c8f"/>'
    b += '<g transform="translate(8 6)"><rect x="4" y="8" width="36" height="28" rx="6" fill="#e9eef2"/><rect x="21" y="1" width="2" height="7" fill="#e9eef2"/><circle cx="22" cy="1" r="2.6" fill="#ffd36b"/>'
    b += '<circle cx="15" cy="20" r="4.5" fill="#d6283c"/><circle cx="29" cy="20" r="4.5" fill="#d6283c"/><rect x="13" y="28" width="18" height="2.5" fill="#2b6c8f"/></g>'
    b += '<g transform="translate(52 10)"><rect width="26" height="36" fill="#fff"/><path d="M4 8 h18 M4 14 h18 M4 20 h12" stroke="#99a" stroke-width="2"/><path d="M3 30 L23 4" stroke="#111" stroke-width="2.4"/></g>'
    b += tag(84, 10, "NO TREATY", "#fff", "#2b6c8f", 9)
    b += tag(84, 30, "UNTIL 2028", "#ffd36b", "#111", 8.5)
    return svg(b)


def peru():
    b = '<rect width="160" height="56" fill="#cfe3ec"/>'
    b += '<path d="M0 56 L22 22 L36 38 L58 10 L80 40 L98 20 L122 46 L140 28 L160 44 L160 56Z" fill="#8a7a5a"/>'
    b += '<path d="M54 16 L58 10 L62 16Z M94 25 L98 20 L102 25Z" fill="#fff"/>'
    b += '<circle cx="70" cy="44" r="3.5" fill="#c0152f"/><circle cx="70" cy="44" r="9" fill="none" stroke="#c0152f" stroke-width="1.3"/>'
    b += tag(4, 4, "M6.7 · 108 KM DEEP", "#111", "#fff", 8.5)
    b += tag(4, 20, "00:09 UTC", "#fff", "#111", 8.5)
    return svg(b)


def mama():
    b = '<rect width="160" height="56" fill="#1b0f2e"/>'
    b += '<path d="M10 0 L30 56 M150 0 L130 56" stroke="#f2c94c" stroke-width="18" opacity=".12"/>'
    b += '<rect y="44" width="160" height="12" fill="#3a2460"/>'
    b += '<g transform="translate(40 8)"><path d="M0 0 H22 V8 C22 18 14 22 11 22 C8 22 0 18 0 8Z" fill="#f2c94c"/><rect x="8" y="22" width="6" height="8" fill="#f2c94c"/><rect x="3" y="30" width="16" height="4" fill="#f2c94c"/></g>'
    b += tag(74, 8, "BTS · 5 AWARDS", "#f2c94c", "#111", 9)
    b += tag(74, 26, "OSAKA", "#fff", "#1b0f2e", 9)
    return svg(b)


# ------------------------------------------------------------------ simplified flags, 18x12
def flag(code):
    f = {
        "FI": '<rect width="18" height="12" fill="#fff"/><rect x="5" width="3" height="12" fill="#003580"/><rect y="4.5" width="18" height="3" fill="#003580"/>',
        "RU": '<rect width="18" height="4" fill="#fff"/><rect y="4" width="18" height="4" fill="#0039a6"/><rect y="8" width="18" height="4" fill="#d52b1e"/>',
        "UA": '<rect width="18" height="6" fill="#0057b7"/><rect y="6" width="18" height="6" fill="#ffd700"/>',
        "GB": '<rect width="18" height="12" fill="#012169"/><path d="M0 0 L18 12 M18 0 L0 12" stroke="#fff" stroke-width="2.4"/><path d="M0 0 L18 12 M18 0 L0 12" stroke="#c8102e" stroke-width=".9"/><rect x="7" width="4" height="12" fill="#fff"/><rect y="4" width="18" height="4" fill="#fff"/><rect x="7.8" width="2.4" height="12" fill="#c8102e"/><rect y="4.8" width="18" height="2.4" fill="#c8102e"/>',
        "ENG": '<rect width="18" height="12" fill="#fff"/><rect x="7.5" width="3" height="12" fill="#ce1124"/><rect y="4.5" width="18" height="3" fill="#ce1124"/>',
        "UN": '<rect width="18" height="12" fill="#4b92db"/><circle cx="9" cy="6" r="3.6" fill="none" stroke="#fff" stroke-width="1.2"/>',
        "PT": '<rect width="7" height="12" fill="#046a38"/><rect x="7" width="11" height="12" fill="#da291c"/><circle cx="7" cy="6" r="2.4" fill="#ffe900"/>',
        "NL": '<rect width="18" height="4" fill="#ae1c28"/><rect y="4" width="18" height="4" fill="#fff"/><rect y="8" width="18" height="4" fill="#21468b"/>',
        "VA": '<rect width="9" height="12" fill="#ffe000"/><rect x="9" width="9" height="12" fill="#fff"/><circle cx="13.5" cy="6" r="1.8" fill="#c9a227"/>',
        "FR": '<rect width="6" height="12" fill="#002395"/><rect x="6" width="6" height="12" fill="#fff"/><rect x="12" width="6" height="12" fill="#ed2939"/>',
        "IE": '<rect width="6" height="12" fill="#169b62"/><rect x="6" width="6" height="12" fill="#fff"/><rect x="12" width="6" height="12" fill="#ff883e"/>',
        "LB": '<rect width="18" height="12" fill="#ed1c24"/><rect y="3" width="18" height="6" fill="#fff"/><path d="M9 3.6 L11.4 8.4 H6.6Z" fill="#00a651"/>',
        "IL": '<rect width="18" height="12" fill="#fff"/><rect y="1.5" width="18" height="1.6" fill="#0038b8"/><rect y="8.9" width="18" height="1.6" fill="#0038b8"/><path d="M9 3.6 L11 7.2 H7Z M9 8.4 L11 4.8 H7Z" fill="none" stroke="#0038b8" stroke-width=".7"/>',
        "YE": '<rect width="18" height="4" fill="#ce1126"/><rect y="4" width="18" height="4" fill="#fff"/><rect y="8" width="18" height="4" fill="#000"/>',
        "QA": '<rect width="18" height="12" fill="#8a1538"/><rect width="6" height="12" fill="#fff"/><path d="M6 0 L8 1 L6 2 L8 3 L6 4 L8 5 L6 6 L8 7 L6 8 L8 9 L6 10 L8 11 L6 12Z" fill="#fff"/>',
        "US": '<rect width="18" height="12" fill="#fff"/>' + "".join(f'<rect y="{i * 1.85:.2f}" width="18" height=".92" fill="#b22234"/>' for i in range(7)) + '<rect width="8" height="6.5" fill="#3c3b6e"/>',
        "CA": '<rect width="4.5" height="12" fill="#d52b1e"/><rect x="4.5" width="9" height="12" fill="#fff"/><rect x="13.5" width="4.5" height="12" fill="#d52b1e"/><path d="M9 2.5 L10.6 5.5 L12 5 L11 8.5 H7 L6 5 L7.4 5.5Z" fill="#d52b1e"/>',
        "BR": '<rect width="18" height="12" fill="#009c3b"/><path d="M9 1.5 L16.5 6 L9 10.5 L1.5 6Z" fill="#ffdf00"/><circle cx="9" cy="6" r="2.6" fill="#002776"/>',
        "PE": '<rect width="6" height="12" fill="#d91023"/><rect x="6" width="6" height="12" fill="#fff"/><rect x="12" width="6" height="12" fill="#d91023"/>',
        "PK": '<rect width="18" height="12" fill="#01411c"/><rect width="4.5" height="12" fill="#fff"/><circle cx="11" cy="6" r="3" fill="#fff"/><circle cx="12" cy="5.3" r="2.6" fill="#01411c"/>',
        "IN": '<rect width="18" height="4" fill="#ff9933"/><rect y="4" width="18" height="4" fill="#fff"/><rect y="8" width="18" height="4" fill="#138808"/><circle cx="9" cy="6" r="1.5" fill="none" stroke="#000080" stroke-width=".6"/>',
        "BD": '<rect width="18" height="12" fill="#006a4e"/><circle cx="8" cy="6" r="3.6" fill="#f42a41"/>',
        "KR": '<rect width="18" height="12" fill="#fff" stroke="#ccc" stroke-width=".4"/><circle cx="9" cy="6" r="3" fill="#cd2e3a"/><path d="M6 6 A3 3 0 0 0 12 6 A1.5 1.5 0 0 0 9 6 A1.5 1.5 0 0 1 6 6Z" fill="#0047a0"/>',
        "KP": '<rect width="18" height="12" fill="#024fa2"/><rect y="2" width="18" height="8" fill="#fff"/><rect y="2.8" width="18" height="6.4" fill="#ed1c27"/><circle cx="6.5" cy="6" r="2.4" fill="#fff"/>',
        "TW": '<rect width="18" height="12" fill="#fe0000"/><rect width="9" height="6" fill="#000095"/><circle cx="4.5" cy="3" r="1.6" fill="#fff"/>',
        "JP": '<rect width="18" height="12" fill="#fff" stroke="#ccc" stroke-width=".4"/><circle cx="9" cy="6" r="3.4" fill="#bc002d"/>',
        "NZ": '<rect width="18" height="12" fill="#012169"/><rect width="8" height="6" fill="#012169" stroke="#fff" stroke-width=".6"/><path d="M0 0 L8 6 M8 0 L0 6" stroke="#fff" stroke-width=".8"/><g fill="#c8102e"><circle cx="13" cy="3" r=".9"/><circle cx="15" cy="6" r=".9"/><circle cx="12" cy="7" r=".9"/><circle cx="13" cy="10" r=".9"/></g>',
        "AU": '<rect width="18" height="12" fill="#012169"/><rect width="8" height="6" fill="#012169" stroke="#fff" stroke-width=".6"/><path d="M0 0 L8 6 M8 0 L0 6" stroke="#fff" stroke-width=".8"/><g fill="#fff"><circle cx="4" cy="9" r="1.2"/><circle cx="13" cy="3" r=".8"/><circle cx="15.5" cy="6" r=".8"/><circle cx="12" cy="7" r=".8"/><circle cx="13" cy="10" r=".8"/></g>',
        "EG": '<rect width="18" height="4" fill="#ce1126"/><rect y="4" width="18" height="4" fill="#fff"/><rect y="8" width="18" height="4" fill="#000"/><circle cx="9" cy="6" r="1.2" fill="#c09300"/>',
        "SD": '<rect width="18" height="4" fill="#d21034"/><rect y="4" width="18" height="4" fill="#fff"/><rect y="8" width="18" height="4" fill="#000"/><path d="M0 0 L6 6 L0 12Z" fill="#007229"/>',
        "CG": '<rect width="18" height="12" fill="#fbde4a"/><path d="M0 0 H12 L0 12Z" fill="#009543"/><path d="M18 0 V12 H6Z" fill="#dc241f"/>',
        "SO": '<rect width="18" height="12" fill="#4189dd"/><path d="M9 3 L9.9 5.6 H12.6 L10.4 7.2 L11.2 9.8 L9 8.2 L6.8 9.8 L7.6 7.2 L5.4 5.6 H8.1Z" fill="#fff"/>',
        "NG": '<rect width="6" height="12" fill="#008751"/><rect x="6" width="6" height="12" fill="#fff"/><rect x="12" width="6" height="12" fill="#008751"/>',
    }[code]
    return f'<svg class="flag" width="18" height="12" viewBox="0 0 18 12">{f}</svg>'
