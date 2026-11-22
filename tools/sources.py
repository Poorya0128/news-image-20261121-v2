#!/usr/bin/env python3
"""Writes SOURCES.md with the same story numbers as the page (imports build.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B  # noqa: E402  (also rebuilds poster/index.html)

LINKS = {
    "baltic": ["https://www.afp.com/en/russian-cargo-ship-catches-fire-after-ukrainian-strike-baltic", "https://www.straitstimes.com/world/europe/russia-says-cargo-vessel-struck-by-drones-finland-says-it-is-on-fire-in-its-waters", "https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-november-21-2026/", "https://adaderana.lk/news/252094"],
    "hormuz": ["https://www.straitstimes.com/world/europe/tanker-hit-by-unknown-projectile-near-omans-khasab-ukmto-says", "https://www.jpost.com/middle-east/article-915628", "https://apnews.com/article/mideast-iran-gaza-israel-november-21-2026-29159a6f3365ff447c0ccbd1d7260f75"],
    "sinaloa": ["https://www.pbs.org/newshour/world/mexico-detains-top-cartel-boss-el-chapo-isidro-setting-off-a-burst-of-violence-in-sinaloa", "https://globalnews.ca/news/12161000/mexico-cartel-leader-captured/"],
    "kryvyi": ["https://ca.news.yahoo.com/ballistic-missile-attack-zelenskyys-hometown-105551537.html", "https://kyivindependent.com/russian-attacks-kill-at-least-2-injure-83-across-ukraine-as-strikes-devastate-kryvyi-rih/", "https://united24media.com/war-in-ukraine/russia-bombards-ukraine-overnight-killing-7-year-old-boy-and-paramedic-injuring-dozens-24584"],
    "cop": ["https://www.yahoo.com/news/science/articles/fight-over-fossil-fuels-leaves-073500434.html", "https://www.theguardian.com/environment/2026/nov/21/climate-talks-stall-countries-mull-showdown-saudi-arabia-over-fossil-fuels"],
    "bepi": ["https://apnews.com/article/mercury-bepicolombo-space-planet-esa-0c80bbf2039ed4f6ee4a34426b3594a0", "https://earthsky.org/space/bepicolombo-mission-mercury/"],
    "quake": ["https://earthquake.usgs.gov/earthquakes/eventpage/us6000ucij/executive", "https://www.ibtimes.com.au/magnitude-6-8-banda-sea-earthquake-felt-darwin-1879081"],
    "france": ["https://www.lemonde.fr/en/france/article/2026/11/21/french-protesters-rally-for-sixth-weekend-over-living-costs-public-services-inequality_6786265_7.html", "https://www.bloomberg.com/news/articles/2026-11-21/french-protests-draw-fewer-people-after-government-concessions", "https://www.euronews.com/2026/11/21/thousands-take-to-streets-in-portugal-france-and-spain-over-rising-living-costs"],
    "gaza": ["https://uk.news.yahoo.com/israeli-strike-kills-three-vehicle-135323513.html", "https://www.aol.com/articles/israeli-strike-kills-three-vehicle-135323000.html"],
    "eu": ["https://www.yahoo.com/news/politics/articles/eu-mulls-tax-big-tech-060606649.html", "https://www.yahoo.com/news/politics/articles/germany-still-not-satisfied-costa-170339274.html"],
    "heli": ["https://www.aerotime.aero/articles/russian-helicopter-finnish-airspace-sparta-ii-drone-strike", "https://www.dw.com/en/russian-helicopter-suspected-of-violating-finnish-airspace/a-80010133"],
    "blacksea": ["https://news.sky.com/story/ukraine-live-updates-satellite-images-show-new-russia-deployments-as-biden-and-putin-summit-mooted-12541713"],
    "kyiv": ["https://www.itv.com/news/2026-11-21/zelenskyy-says-putins-a-killer-as-trump-defends-calling-him-a-friend"],
    "pope": ["https://www.vaticannews.va/en/pope/news/2026-11/pope-leo-meets-participants-in-the-international-space-forum.html"],
    "mq9": ["https://www.tasnimnews.ir/en/news/2026/11/21/3753905/irgc-downs-58th-us-mq-9-drone-over-strait-of-hormuz", "https://www.aljazeera.com/news/2026/11/21/irans-irgc-downs-us-drone-over-hormuz-as-efforts-to-end-war-remain-stalled"],
    "aoun": ["https://www.arabnews.com/middle-east/lebanons-president-aoun-demands-end-to-israeli-occupation-iranian-interference-3013406"],
    "unifil": ["https://www.aa.com.tr/en/middle-east/unifil-begins-handing-over-positions-in-southern-lebanon-to-lebanese-army/4133076"],
    "israel": ["https://www.timesofisrael.com/liveblog_entry/in-first-statement-since-netanyahu-meeting-bennett-backs-unity-government-under-eisenkot-rules-out-defection-under-any-circumstances/"],
    "dar": ["https://www.dailyindependent.com.pk/2026/11/21/dar-hopeful-of-early-us-iran-deal-says-middle-east-conflict-threatens-global-stability/"],
    "houthi": ["https://understandingwar.org/research/middle-east/iran-update-november-21-2026/"],
    "fbi": ["https://www.yahoo.com/news/politics/articles/trump-downplays-fbi-data-breach-220234871.html", "https://www.axios.com/2026/11/21/trump-russia-fbi-hack"],
    "iran": ["https://www.cbsnews.com/live-updates/iran-war-trump-tehran-denies-chemical-weapons/"],
    "halifax": ["https://abcnews.com/International/wireStory/taiwan-warns-canada-faces-china-risks-carney-cautioned-138346706"],
    "peru": ["https://earthquake.usgs.gov/earthquakes/eventpage/us6000ucfm/technical", "https://abcnews.com/International/wireStory/magnitude-67-earthquake-shakes-perus-andes-damage-casualties-138334341"],
    "bd": ["https://www.khaleejtimes.com/world/asia/bangladesh-deploys-extra-paramilitary-troops-political-unrest"],
    "kr": ["https://www.koreaherald.com/article/10944666"],
    "tw": ["https://www.taiwannews.com.tw/en/news/6479444"],
    "nk": ["https://www.channelnewsasia.com/east-asia/north-korea-kim-jong-un-donald-trump-snub-6571201"],
    "in": ["https://www.theweek.in/wire-updates/business/2026/11/21/google-announces-usd-5-mn-funding-for-iit-kharagpur-for-advanced-ai-research.html", "https://timesofindia.indiatimes.com/india/google-commits-5-million-to-iit-kharagpur-for-ai-research-talent-development/articleshow/136053247.cms"],
    "eg": ["https://dailynewsegypt.com/2026/11/21/al-sisi-calls-for-global-financial-system-reform-greater-african-role-in-shaping-world-order/", "https://dailynewsegypt.com/2026/11/21/egypt-signs-cooperation-pacts-with-sudan-dr-congo-at-aswan-forum/"],
    "sudan": ["https://www.radiotamazuj.org/en/news/article/sennar-imposes-night-curfew-as-blue-nile-fighting-intensifies", "https://www.aa.com.tr/en/africa/sudanese-relief-group-accuses-rsf-of-killing-civilians-including-3-children-in-west-kordofan/4133027"],
    "ng": ["https://www.premiumtimesng.com/regional/ssouth-west/927036-tinubu-campaigns-in-ibadan-says-nigeria-on-path-to-prosperity.html", "https://leadership.ng/bayelsa-boat-tragedy-tinubu-orders-low-key-ibadan-rally/"],
    "eng": ["https://www.skysports.com/rugby-union/news/13614346/nations-championship-england-37-12-new-zealand-most-complete-performance-under-steve-borthwick-sees-hosts-stay-in-title-hunt"],
    "epl": ["https://global.espn.com/football/story/_/id/50532558/premier-league-live-updates-man-city-chelsea-arsenal"],
    "cric": ["https://www.afp.com/en/india-take-118-run-lead-over-new-zealand-reach-486-4-stumps-day-3"],
    "t20": ["https://www.espn.co.uk/cricket/series/24273/game/1528706/australia-vs-england-1st-t20i-24273"],
    "cfb": ["https://www.nbcsports.com/college-football/news/nebraska-ends-31-game-losing-streak-against-ap-top-25-opponents-with-31-28-win-over-no-16-buckeyes"],
    "ufc": ["https://www.ufc.com/news/ufc-qatar-results-prochazka-vs-stirling", "https://www.espn.com/mma/fightcenter"],
    "geneva": ["https://abcnews.com/US/wireStory/nations-talks-ai-killer-robots-agree-talks-firm-138339624", "https://www.theguardian.com/technology/2026/nov/21/international-talks-control-ai-autonomous-weapons-collapse"],
    "front": ["https://en.lb.ua/news/2026/11/21/50906_116_clashes_reported_front_line.html", "https://www.kyivpost.com/post/90823"],
    "btc": ["https://www.globalbankingandfinance.com/bitcoin-rises-over-2-60-000/", "https://finance.yahoo.com/markets/crypto/articles/bitcoin-crashes-below-56-000-061626263.html"],
    "riemann": ["https://www.theguardian.com/technology/2026/nov/21/anthropic-riemann-hypothesis-solved-claude-ai", "https://www.scientificamerican.com/article/the-ai-riemann-hypothesis-proof-is-almost-certainly-true-independent-mathematicians-attest/"],
    "brazil": ["https://www.riotimesonline.com/lula-calls-brazil-fiscal-bill-an-adjustment/"],
    "flu": ["https://theprint.in/india/bird-flu-outbreak-alert-central-team-visits-cuddalore/3105023/"],
    "mama": ["https://www.koreaherald.com/article/10944819", "https://www.asiaone.com/entertainment/bts-reign-supreme-2026-mamas-cortis-steal-spotlight-song-year-win"],
    "oyo": ["https://www.kenyans.co.ke/news/129580-ruto-jets-out-congo-meeting-amid-tensions-between-kenya-and-drc"],
    "somalia": ["https://garoweonline.com/index.php/en/news/somalia/turkish-military-chief-visits-somalia-amid-deepening-defence-ties"],
}

title = {x["k"]: x["h"] for x in B.LEADS + B.CARDS}
title.update({b[0]: f"{b[3]}: {b[4]}" for b in B.BRIEFS})
flags = {b[0]: b[5] for b in B.BRIEFS}

LINKS["robots"] = LINKS.get("geneva", ["https://abcnews.com/US/wireStory/nations-talks-ai-killer-robots-agree-talks-firm-138339624"])
LINKS["ams"] = ["https://www.gov.uk/government/news/pm-meeting-with-prime-minister-jetten-of-the-netherlands-21-november-2026"]
LINKS["lisbon"] = ["https://www.euronews.com/2026/11/21/thousands-take-to-streets-in-portugal-france-and-spain-over-rising-living-costs"]
LINKS["icj"] = ["https://www.timesofisrael.com/liveblog_entry/france-calls-for-un-security-council-action-after-myanmar-rejects-icj-genocide-ruling/"]
LINKS["ire"] = ["https://sports.yahoo.com/articles/south-africa-stumbles-nations-championship-190124713.html"]
LINKS["pope"] = ["https://www.vaticannews.va/en/pope/news/2026-11/pope-leo-meets-participants-in-the-international-space-forum.html"]
LINKS["epl"] = ["https://global.espn.com/football/story/_/id/50532558/premier-league-live-updates-man-city-chelsea-arsenal"]
LINKS["baltic"] = LINKS.get("baltic", [])
LINKS = {k: v for k, v in LINKS.items() if k in B.N}
assert set(LINKS) == set(B.N), set(B.N) ^ set(LINKS)
rows = []
for k, n in sorted(B.N.items(), key=lambda kv: kv[1]):
    links = " · ".join(f"[{u.split('/')[2].replace('www.', '')}]({u})" for u in LINKS[k])
    st = {x["k"]: x["st"][0] for x in B.LEADS + B.CARDS}
    tag = {"claim": " **(CLAIM)**", "report": " **(REPORTED: event on 20 Nov, first made public 21 Nov)**"}.get(flags.get(k, ""), "")
    if k in st:
        tag = " ✓ CONFIRMED"
    rows.append(f"| {n} | {title[k]}{tag} | {links} |")

md = f"""# Sources: {B.TOTAL} stories from Saturday 21 November 2026

Generated from `tools/build.py` by `tools/sources.py`. Stories 1-3 are the lead drawings, 4-{B.DRAWN} the drawn cards,
and the rest the "Also on Saturday 21 November" strip.

| # | Story | Sources |
|---|-------|---------|
""" + "\n".join(rows) + """

**Date rule.** Every story happened, or was first reported, on Saturday 21 November 2026.
Events from Friday 20 November (for example Russian missiles landing in Poland and the UK–EU summit deal) were left out.

**Wording rule.** One side's account is attributed in the text ("Finland says", "Iran says", "Relief group accuses").
CONFIRMED = two or more independent outlets, or an official source.
"""
open(os.path.join(B.ROOT, "SOURCES.md"), "w", encoding="utf-8").write(md)
print("SOURCES.md rows:", len(rows))
