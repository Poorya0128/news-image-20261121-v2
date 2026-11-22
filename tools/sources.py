#!/usr/bin/env python3
"""Writes SOURCES.md with the same story numbers as the page (imports build.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B  # noqa: E402  (also rebuilds poster/index.html)

LINKS = {
    "baltic": ["https://www.afp.com/en/russian-cargo-ship-catches-fire-after-ukrainian-strike-baltic", "https://www.straitstimes.com/world/europe/russia-says-cargo-vessel-struck-by-drones-finland-says-it-is-on-fire-in-its-waters", "https://understandingwar.org/research/russia-ukraine/russian-offensive-campaign-assessment-november-21-2026/"],
    "hormuz": ["https://apnews.com/article/mideast-iran-gaza-israel-november-21-2026-29159a6f3365ff447c0ccbd1d7260f75", "https://www.aljazeera.com/news/2026/11/21/tankers-hit-in-strait-of-hormuz-as-iran-tightens-grip-on-shipping"],
    "sinaloa": ["https://www.pbs.org/newshour/world/mexico-detains-top-cartel-boss-el-chapo-isidro-setting-off-a-burst-of-violence-in-sinaloa", "https://globalnews.ca/news/12161000/mexico-cartel-leader-captured/"],
    "kryvyi": ["https://ca.news.yahoo.com/ballistic-missile-attack-zelenskyys-hometown-105551537.html", "https://united24media.com/war-in-ukraine/russia-bombards-ukraine-overnight-killing-7-year-old-boy-and-paramedic-injuring-dozens-24584"],
    "cop": ["https://www.yahoo.com/news/science/articles/fight-over-fossil-fuels-leaves-073500434.html", "https://www.theguardian.com/environment/2026/nov/21/climate-talks-stall-countries-mull-showdown-saudi-arabia-over-fossil-fuels"],
    "robots": ["https://abcnews.com/US/wireStory/nations-talks-ai-killer-robots-agree-talks-firm-138339624", "https://www.theguardian.com/technology/2026/nov/21/international-talks-control-ai-autonomous-weapons-collapse"],
    "bepi": ["https://apnews.com/article/mercury-bepicolombo-space-planet-esa-0c80bbf2039ed4f6ee4a34426b3594a0", "https://earthsky.org/space/bepicolombo-mission-mercury/"],
    "quake": ["https://earthquake.usgs.gov/earthquakes/eventpage/us6000ucij/executive", "https://www.ibtimes.com.au/magnitude-6-8-banda-sea-earthquake-felt-darwin-1879081"],
    "france": ["https://www.lemonde.fr/en/france/article/2026/11/21/french-protesters-rally-for-sixth-weekend-over-living-costs-public-services-inequality_6786265_7.html", "https://www.bloomberg.com/news/articles/2026-11-21/french-protests-draw-fewer-people-after-government-concessions"],
    "gaza": ["https://uk.news.yahoo.com/israeli-strike-kills-three-vehicle-135323513.html"],
    "eu": ["https://www.yahoo.com/news/politics/articles/eu-mulls-tax-big-tech-060606649.html", "https://www.yahoo.com/news/politics/articles/germany-still-not-satisfied-costa-170339274.html"],
    "heli": ["https://www.dw.com/en/russian-helicopter-suspected-of-violating-finnish-airspace/a-80010133"],
    "blacksea": ["https://news.sky.com/story/ukraine-live-updates-satellite-images-show-new-russia-deployments-as-biden-and-putin-summit-mooted-12541713"],
    "kyiv": ["https://www.itv.com/news/2026-11-21/zelenskyy-says-putins-a-killer-as-trump-defends-calling-him-a-friend"],
    "lisbon": ["https://www.euronews.com/2026/11/21/thousands-take-to-streets-in-portugal-france-and-spain-over-rising-living-costs"],
    "ams": ["https://www.gov.uk/government/news/pm-meeting-with-prime-minister-jetten-of-the-netherlands-21-november-2026"],
    "tories": ["https://www.independent.co.uk/news/business/andy-burnham-tories-european-union-brussels-government-b3089311.html"],
    "pope": ["https://www.vaticannews.va/en/pope/news/2026-11/pope-leo-meets-participants-in-the-international-space-forum.html"],
    "icj": ["https://www.timesofisrael.com/liveblog_entry/france-calls-for-un-security-council-action-after-myanmar-rejects-icj-genocide-ruling/"],
    "mq9": ["https://www.tasnimnews.ir/en/news/2026/11/21/3753905/irgc-downs-58th-us-mq-9-drone-over-strait-of-hormuz", "https://www.aljazeera.com/news/2026/11/21/irans-irgc-downs-us-drone-over-hormuz-as-efforts-to-end-war-remain-stalled"],
    "aoun": ["https://www.arabnews.com/middle-east/lebanons-president-aoun-demands-end-to-israeli-occupation-iranian-interference-3013406"],
    "unifil": ["https://www.aa.com.tr/en/middle-east/unifil-begins-handing-over-positions-in-southern-lebanon-to-lebanese-army/4133076"],
    "israel": ["https://www.timesofisrael.com/liveblog_entry/in-first-statement-since-netanyahu-meeting-bennett-backs-unity-government-under-eisenkot-rules-out-defection-under-any-circumstances/"],
    "dar": ["https://www.dailyindependent.com.pk/2026/11/21/dar-hopeful-of-early-us-iran-deal-says-middle-east-conflict-threatens-global-stability/"],
    "houthi": ["https://understandingwar.org/research/middle-east/iran-update-november-21-2026/"],
    "fbi": ["https://www.yahoo.com/news/politics/articles/trump-downplays-fbi-data-breach-220234871.html", "https://www.axios.com/2026/11/21/trump-russia-fbi-hack"],
    "iran": ["https://www.cbsnews.com/live-updates/iran-war-trump-tehran-denies-chemical-weapons/"],
    "taiwan_ca": ["https://abcnews.com/International/wireStory/taiwan-warns-canada-faces-china-risks-carney-cautioned-138346706"],
    "ca_us": ["https://ca.news.yahoo.com/no-change-top-canadian-officials-153807614.html"],
    "bd": ["https://www.khaleejtimes.com/world/asia/bangladesh-deploys-extra-paramilitary-troops-political-unrest"],
    "kr": ["https://www.koreaherald.com/article/10944666"],
    "tw": ["https://www.taiwannews.com.tw/en/news/6479444"],
    "nk": ["https://www.channelnewsasia.com/east-asia/north-korea-kim-jong-un-donald-trump-snub-6571201"],
    "au": ["https://www.abc.net.au/news/2026-11-21/homebirth-rallies-midwife-insurance-freebirth/107412380"],
    "in": ["https://www.thehindu.com/news/national/pm-modi-iit-kharagpur-bengal-updates-november-21-2026/article71727603.ece"],
    "eg": ["https://dailynewsegypt.com/2026/11/21/al-sisi-calls-for-global-financial-system-reform-greater-african-role-in-shaping-world-order/"],
    "sennar": ["https://www.radiotamazuj.org/en/news/article/sennar-imposes-night-curfew-as-blue-nile-fighting-intensifies"],
    "rsf": ["https://www.usmuslims.com/sudanese-relief-group-accuses-rsf-of-killing-civilians-including-3-children-in-383026h.htm"],
    "ng": ["https://www.premiumtimesng.com/regional/ssouth-west/927036-tinubu-campaigns-in-ibadan-says-nigeria-on-path-to-prosperity.html", "https://leadership.ng/bayelsa-boat-tragedy-tinubu-orders-low-key-ibadan-rally/"],
    "za": ["https://uk.news.yahoo.com/ex-african-deputy-president-un-080146042.html"],
    "eng": ["https://www.skysports.com/rugby-union/news/13614346/nations-championship-england-37-12-new-zealand-most-complete-performance-under-steve-borthwick-sees-hosts-stay-in-title-hunt"],
    "ire": ["https://sports.yahoo.com/articles/south-africa-stumbles-nations-championship-190124713.html"],
    "sco": ["https://ca.sports.yahoo.com/news/australia-breaks-win-over-wales-224803005.html"],
    "wal": ["https://www.skysports.com/rugby-union/news/13615075/nations-championship-wales-fall-short-in-29-26-defeat-to-australia-after-epic-new-zealand-victory"],
    "epl": ["https://global.espn.com/football/story/_/id/50532558/premier-league-live-updates-man-city-chelsea-arsenal"],
    "new": ["https://global.espn.com/football/story/_/id/50532558/premier-league-live-updates-man-city-chelsea-arsenal"],
    "cric": ["https://www.afp.com/en/india-take-118-run-lead-over-new-zealand-reach-486-4-stumps-day-3"],
    "t20": ["https://uk.sports.yahoo.com/news/australia-chase-188-defeat-england-120953861.html"],
    "cfb": ["https://www.nbcsports.com/college-football/news/nebraska-ends-31-game-losing-streak-against-ap-top-25-opponents-with-31-28-win-over-no-16-buckeyes"],
    "ufc": ["https://www.fightbookmma.com/ufc-doha-2026-results/"],
}

title = {x["k"]: x["h"] for x in B.LEADS + B.CARDS}
title.update({b[0]: f"{b[2]}: {b[3]}" for b in B.BRIEFS})
title.update({s[0]: f"{s[2]}: {s[3]}" for s in B.SPORT})
flags = {b[0]: b[5] for b in B.BRIEFS}

assert set(LINKS) == set(B.N), set(B.N) ^ set(LINKS)
rows = []
for k, n in sorted(B.N.items(), key=lambda kv: kv[1]):
    links = " · ".join(f"[{u.split('/')[2].replace('www.', '')}]({u})" for u in LINKS[k])
    tag = " **(claim)**" if flags.get(k) == "claim" else (" ◆ official" if flags.get(k) == "official" else "")
    rows.append(f"| {n} | {title[k]}{tag} | {links} |")

md = f"""# Sources: {B.TOTAL} stories, all from Saturday 21 November 2026 (UTC)

Numbers match the badges and map pins on the page. This file is generated from `tools/build.py` by `tools/sources.py`.

| # | Story | Sources |
|---|-------|---------|
""" + "\n".join(rows) + """

**Date check: left out on purpose.**
- Happened on Friday 20 November: Russian missiles landing in Poland, the Peru M6.7 quake, the Brazil supercell storm, the UK–EU summit deal, and Ruto's Busia speech.
- Ended after 00:00 UTC on Sunday 22 November: the Las Vegas GP (started 04:00 UTC) and the Copa Sudamericana final (kicked off 22:30 UTC).

**Key UTC times:** Geneva talks ended just before 05:00 Geneva time (~04:00 UTC, Guardian); the Banda Sea quake struck at 09:42 UTC (USGS); the Russian helicopter was reported at 12:34 Finnish time (10:34 UTC); BepiColombo's 37-minute orbit burn began at 18:24 UTC (ESA via EarthSky).
"""
open(os.path.join(B.ROOT, "SOURCES.md"), "w", encoding="utf-8").write(md)
print("SOURCES.md rows:", len(rows))
