#!/usr/bin/env python3
"""Expand Shri Shyam Library's daily Current Affairs pipeline.

Run from the repository root. Only automation/publish_current_affairs.py is changed.
A backup is saved under .git/ca-pipeline-backups/ before writing.
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

ROOT = Path.cwd()
PIPELINE = ROOT / "automation" / "publish_current_affairs.py"

OLD_FEEDS = '''# Reliable, public feeds. Rajasthan's west/east PIB regional feeds are included
# alongside the official Rajasthan DIPR site scraper below.
FEEDS = [
    {"url": "https://www.pib.gov.in/RssMain.aspx?ModId=6&Lang=2&Regid=3", "name": "PIB / भारत सरकार", "category": "national"},
    {"url": "https://news.un.org/feed/subscribe/en/news/all/rss.xml", "name": "UN News", "category": "international"},
    {"url": "https://feeds.bbci.co.uk/news/world/rss.xml", "name": "BBC News World", "category": "international"},
    {"url": "https://www.pib.gov.in/RssMain.aspx?ModId=6&Lang=2&Regid=17", "name": "PIB पश्चिमी राजस्थान क्षेत्र", "category": "rajasthan"},
    {"url": "https://www.pib.gov.in/RssMain.aspx?ModId=6&Lang=2&Regid=18", "name": "PIB पूर्वी राजस्थान क्षेत्र", "category": "rajasthan"},
]'''

NEW_FEEDS = '''# RSS discovery sources. Every story is date-filtered, deduplicated and AI-screened.
# Official sources are listed first; publisher feeds add breadth but are not treated as
# proof by themselves. The published entry always keeps the original article URL.
FEEDS = [
    # National: official policy, central-bank and reputable national reporting.
    {"url": "https://www.pib.gov.in/RssMain.aspx?ModId=6&Lang=2&Regid=3", "name": "PIB / भारत सरकार", "category": "national"},
    {"url": "https://www.rbi.org.in/pressreleases_rss.xml", "name": "भारतीय रिज़र्व बैंक (RBI)", "category": "national"},
    {"url": "https://www.thehindu.com/news/national/feeder/default.rss", "name": "The Hindu / National", "category": "national"},
    {"url": "https://indianexpress.com/section/india/feed/", "name": "The Indian Express / India", "category": "national"},
    {"url": "https://indianexpress.com/section/explained/feed/", "name": "The Indian Express / Explained", "category": "national"},
    {"url": "https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml", "name": "Hindustan Times / India", "category": "national"},
    {"url": "https://www.business-standard.com/rss/latest.rss", "name": "Business Standard", "category": "national"},

    # International: multilateral and established global-news desks.
    {"url": "https://news.un.org/feed/subscribe/en/news/all/rss.xml", "name": "UN News", "category": "international"},
    {"url": "https://feeds.bbci.co.uk/news/world/rss.xml", "name": "BBC News World", "category": "international"},
    {"url": "https://www.thehindu.com/news/international/feeder/default.rss", "name": "The Hindu / International", "category": "international"},
    {"url": "https://indianexpress.com/section/world/feed/", "name": "The Indian Express / World", "category": "international"},
    {"url": "https://www.aljazeera.com/xml/rss/all.xml", "name": "Al Jazeera", "category": "international"},

    # Rajasthan: government releases plus state/city reporting.
    {"url": "https://www.pib.gov.in/RssMain.aspx?ModId=6&Lang=2&Regid=17", "name": "PIB पश्चिमी राजस्थान क्षेत्र", "category": "rajasthan"},
    {"url": "https://www.pib.gov.in/RssMain.aspx?ModId=6&Lang=2&Regid=18", "name": "PIB पूर्वी राजस्थान क्षेत्र", "category": "rajasthan"},
    {"url": "https://api.livehindustan.com/feeds/rss/rajasthan/rssfeed.xml", "name": "हिन्दुस्तान / राजस्थान", "category": "rajasthan"},
    {"url": "https://api.livehindustan.com/feeds/rss/rajasthan/jaipur/rssfeed.xml", "name": "हिन्दुस्तान / जयपुर", "category": "rajasthan"},
    {"url": "https://api.livehindustan.com/feeds/rss/rajasthan/jodhpur/rssfeed.xml", "name": "हिन्दुस्तान / जोधपुर", "category": "rajasthan"},
    {"url": "https://www.hindustantimes.com/feeds/rss/cities/jaipur-news/rssfeed.xml", "name": "Hindustan Times / Jaipur", "category": "rajasthan"},
]'''

OLD_PROMPT = "- कुल अधिकतम 30 खबरें चुनो। लक्ष्य: national अधिकतम 15, rajasthan अधिकतम 10 और international अधिकतम 5। ये अधिकतम/लक्ष्य हैं, अनिवार्य कोटा नहीं। किसी श्रेणी में योग्य खबरें कम हों तो कम ही दो; संख्या पूरी करने के लिए खबर मत गढ़ना।"
NEW_PROMPT = "- दैनिक प्रकाशन लक्ष्य 30 खबरें है: national 15, rajasthan 10 और international 5। स्रोतों में पर्याप्त, अलग और सत्यापन-योग्य खबरें उपलब्ध हों तो हर श्रेणी का पूरा quota भरो। कुल/श्रेणी सीमा से अधिक खबरें न चुनो। किसी श्रेणी में योग्य खबरें कम हों तो कमी रहने दो—खबर, आँकड़ा या MCQ कभी मत गढ़ो; log में quota shortfall दर्ज होगा।"

OLD_LOG = '''    log("AI-filtered stories: " + ", ".join(
        f"{cat}={category_counts[cat]}" for cat in ("national", "rajasthan", "international")
    ))
    return verified'''
NEW_LOG = '''    targets = {"national": 15, "rajasthan": 10, "international": 5}
    log("AI-filtered stories: " + ", ".join(
        f"{cat}={category_counts[cat]}/{targets[cat]}" for cat in ("national", "rajasthan", "international")
    ))
    for category, target in targets.items():
        if category_counts[category] < target:
            log(f"WARN quota shortfall {category}: {category_counts[category]}/{target}; no unsupported stories were added.")
    return verified'''


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise ValueError(f"Expected exactly one {label} block; found {count}. No file was changed.")
    return text.replace(old, new, 1)


def main() -> int:
    if not PIPELINE.is_file():
        print("ERROR: Run this command from the Shri Shyam Library repository root.", file=sys.stderr)
        return 2

    original = PIPELINE.read_text(encoding="utf-8")
    try:
        updated = replace_once(original, OLD_FEEDS, NEW_FEEDS, "FEEDS")
        updated = replace_once(updated, OLD_PROMPT, NEW_PROMPT, "quota prompt")
        updated = replace_once(updated, OLD_LOG, NEW_LOG, "quota log")
        compile(updated, str(PIPELINE), "exec")
    except (ValueError, SyntaxError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = ROOT / ".git" / "ca-pipeline-backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / f"publish_current_affairs.py.before-15-10-5-{stamp}"
    backup.write_text(original, encoding="utf-8")
    PIPELINE.write_text(updated, encoding="utf-8")

    print("SUCCESS: daily Current Affairs pipeline updated.")
    print("Targets: National 15 | Rajasthan 10 | International 5 | Total 30")
    print("Expanded RSS sources; strict source/date/duplicate/MCQ validation is preserved.")
    print("Safety: if a category has fewer qualified stories, the pipeline publishes fewer rather than inventing news.")
    print(f"Backup: {backup.relative_to(ROOT)}")
    print("Python syntax check: PASS")
    print("Next: run `git diff --check` and inspect `git diff -- automation/publish_current_affairs.py`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
