#!/usr/bin/env python3
"""Collect source-linked news, create Hindi UPSC/RPSC summaries and publish to Supabase.

Only items dated the previous India calendar day are considered. Uses standard library only.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")
TIMEOUT = 25
USER_AGENT = "ShriShyamLibrary-CurrentAffairsBot/1.0 (+https://github.com/brruuuhhhh-praxis/Library-)"
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

# Reliable, public feeds. Rajasthan's west/east PIB regional feeds are included
# alongside the official Rajasthan DIPR site scraper below.
FEEDS = [
    {"url": "https://www.pib.gov.in/RssMain.aspx?ModId=6&Lang=2&Regid=3", "name": "PIB / भारत सरकार", "category": "national"},
    {"url": "https://news.un.org/feed/subscribe/en/news/all/rss.xml", "name": "UN News", "category": "international"},
    {"url": "https://feeds.bbci.co.uk/news/world/rss.xml", "name": "BBC News World", "category": "international"},
    {"url": "https://www.pib.gov.in/RssMain.aspx?ModId=6&Lang=2&Regid=17", "name": "PIB पश्चिमी राजस्थान क्षेत्र", "category": "rajasthan"},
    {"url": "https://www.pib.gov.in/RssMain.aspx?ModId=6&Lang=2&Regid=18", "name": "PIB पूर्वी राजस्थान क्षेत्र", "category": "rajasthan"},
]


def log(message: str) -> None:
    print(message, flush=True)


def http_get(url: str, headers: dict[str, str] | None = None, timeout: int = TIMEOUT) -> bytes:
    request_headers = {"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/atom+xml, application/xml, text/html, */*"}
    if headers:
        request_headers.update(headers)
    req = urllib.request.Request(url, headers=request_headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def child_text(node: ET.Element, names: set[str]) -> str:
    for child in node.iter():
        if local_name(child.tag) in names and child is not node:
            value = " ".join(part.strip() for part in child.itertext() if part and part.strip())
            if value:
                return value
    return ""


def strip_html(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", value)
    value = re.sub(r"(?s)<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def parse_datetime(value: str) -> dt.datetime | None:
    value = html.unescape((value or "").strip())
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=IST)
        return parsed.astimezone(IST)
    except (TypeError, ValueError, OverflowError):
        pass
    try:
        normalized = value.replace("Z", "+00:00")
        parsed = dt.datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=IST)
        return parsed.astimezone(IST)
    except (TypeError, ValueError, OverflowError):
        return None


def canonical_url(value: str) -> str:
    value = html.unescape((value or "").strip())
    if value.startswith("//"):
        value = "https:" + value
    if not value.startswith(("http://", "https://")):
        return ""
    return value


def parse_feed(payload: bytes, feed: dict, target_date: dt.date) -> list[dict]:
    try:
        root = ET.fromstring(payload)
    except ET.ParseError as exc:
        log(f"WARN feed XML parse error {feed['name']}: {exc}")
        return []
    result = []
    nodes = [node for node in root.iter() if local_name(node.tag) in {"item", "entry"}]
    for node in nodes:
        title = strip_html(child_text(node, {"title"}))
        description = strip_html(child_text(node, {"description", "summary", "encoded", "content"}))
        date_text = child_text(node, {"pubdate", "published", "updated", "date"})
        published = parse_datetime(date_text)
        link = ""
        for child in list(node):
            if local_name(child.tag) == "link":
                candidate = child.attrib.get("href") or (child.text or "")
                candidate = canonical_url(candidate)
                if candidate:
                    link = candidate
                    if child.attrib.get("rel", "alternate") == "alternate":
                        break
        if not link:
            guid = child_text(node, {"guid", "id"})
            link = canonical_url(guid)
        if not title or not link or not published or published.date() != target_date:
            continue
        if len(description) > 1400:
            description = description[:1400].rsplit(" ", 1)[0]
        result.append({
            "source_id": "", "category": feed["category"], "source_name": feed["name"],
            "source_url": link, "source_title": title, "source_description": description,
            "event_date": target_date.isoformat(), "published_at": published.isoformat(),
        })
    return result


class DIPRLinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self._href = None
        self._text: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            self._href = dict(attrs).get("href")
            self._text = []

    def handle_data(self, data):
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._href is not None:
            href = self._href
            title = re.sub(r"\s+", " ", " ".join(self._text)).strip()
            if "/press-release-detail/" in (href or "") and title:
                self.links.append((href, title))
            self._href = None
            self._text = []


class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta: dict[str, str] = {}
        self.title_parts: list[str] = []
        self.in_title = False
        self.text_parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag.lower() == "meta":
            key = (attrs.get("property") or attrs.get("name") or "").lower()
            value = attrs.get("content", "")
            if key and value:
                self.meta[key] = value
        if tag.lower() == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)
        if data and data.strip():
            self.text_parts.append(data.strip())


def parse_loose_date(text: str) -> dt.date | None:
    # Prefer explicit structured metadata formats.
    for pattern in (r"\b(20\d{2}-\d{2}-\d{2})\b", r"\b(\d{1,2}[/-]\d{1,2}[/-]20\d{2})\b"):
        match = re.search(pattern, text or "")
        if match:
            value = match.group(1)
            for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y"):
                try:
                    return dt.datetime.strptime(value, fmt).date()
                except ValueError:
                    continue
    return None


def fetch_dipr(target_date: dt.date) -> list[dict]:
    """Best-effort extraction from Rajasthan government's DIPR listing/details."""
    urls = ["https://dipr.rajasthan.gov.in/home", "https://dipr.rajasthan.gov.in/"]
    listing = b""
    for page_url in urls:
        try:
            listing = http_get(page_url)
            if listing:
                break
        except Exception as exc:
            log(f"WARN DIPR listing unavailable ({page_url}): {exc}")
    if not listing:
        return []
    parser = DIPRLinkParser()
    try:
        parser.feed(listing.decode("utf-8", errors="replace"))
    except Exception as exc:
        log(f"WARN DIPR listing parse error: {exc}")
        return []
    base = "https://dipr.rajasthan.gov.in"
    unique: dict[str, str] = {}
    for href, title in parser.links:
        link = urllib.parse.urljoin(base, href)
        if link.startswith(base + "/press-release-detail/"):
            unique.setdefault(link, title)
    results = []
    # The detail page is used to confirm the date, not merely the listing order.
    for link, listing_title in list(unique.items())[:30]:
        try:
            page = http_get(link)
            meta = MetaParser()
            meta.feed(page.decode("utf-8", errors="replace"))
            published = None
            for key in ("article:published_time", "datepublished", "date", "pubdate", "article:modified_time"):
                if meta.meta.get(key):
                    parsed = parse_datetime(meta.meta[key])
                    if parsed:
                        published = parsed.date()
                        break
                    published = parse_loose_date(meta.meta[key])
                    if published:
                        break
            full_text = " ".join(meta.text_parts)
            if published is None:
                # Conservative fallback: only accept the target date if explicitly present.
                published = parse_loose_date(full_text)
            if published != target_date:
                continue
            title = strip_html(" ".join(meta.title_parts))
            if not title or title.lower() in {"dipr rajasthan", "home"}:
                title = listing_title
            description = strip_html(full_text)
            description = description.replace(title, "", 1).strip()
            results.append({
                "source_id": "", "category": "rajasthan", "source_name": "राजस्थान सूचना एवं जनसम्पर्क विभाग",
                "source_url": link, "source_title": title[:300], "source_description": description[:1400],
                "event_date": target_date.isoformat(), "published_at": published.isoformat(),
            })
        except Exception as exc:
            log(f"WARN DIPR item skipped ({link}): {exc}")
    return results


def post_json(url: str, body: dict, headers: dict[str, str] | None = None, timeout: int = 180) -> dict:
    payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
    request_headers = {"Content-Type": "application/json", "Accept": "application/json", "User-Agent": USER_AGENT}
    if headers:
        request_headers.update(headers)
    req = urllib.request.Request(url, data=payload, headers=request_headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read().decode("utf-8", errors="replace")
        return json.loads(raw) if raw.strip() else {}


def generate_stories(candidates: list[dict], api_key: str) -> list[dict]:
    # Generate source-grounded exam briefs, then apply deterministic validation and caps.
    if not candidates:
        return []

    for index, item in enumerate(candidates, start=1):
        item["source_id"] = f"S{index:03d}"

    # Keep the model's input compact enough for a daily, repeatable run.
    compact = [{
        "source_id": item["source_id"],
        "category": item["category"],
        "source_name": item["source_name"],
        "source_title": item["source_title"][:300],
        "source_description": item["source_description"][:1000],
        "event_date": item["event_date"],
        "source_url": item["source_url"],
    } for item in candidates]

    prompt = f'''तुम "श्री श्याम लाइब्रेरी" के UPSC, RPSC और RSSB करंट-अफेयर्स संपादक हो। केवल नीचे दिए गए मूल स्रोतों के आधार पर परीक्षा-उपयोगी, स्पष्ट हिंदी सामग्री बनाओ।

संपादकीय कसौटी:
- कुल अधिकतम 30 खबरें चुनो। लक्ष्य: national अधिकतम 15, rajasthan अधिकतम 10 और international अधिकतम 5। ये अधिकतम/लक्ष्य हैं, अनिवार्य कोटा नहीं। किसी श्रेणी में योग्य खबरें कम हों तो कम ही दो; संख्या पूरी करने के लिए खबर मत गढ़ना।
- राष्ट्रीय: संविधान/राजव्यवस्था, कानून/न्यायपालिका, अर्थव्यवस्था/बैंकिंग/मुद्रास्फीति/रोजगार, सरकारी नीति/योजना, बजट/रिपोर्ट/आँकड़े, पर्यावरण/आपदा, विज्ञान/तकनीक/अंतरिक्ष, रक्षा/सुरक्षा, स्वास्थ्य/शिक्षा/प्रशासन जैसे परीक्षा-संबंधी बदलाव।
- राजस्थान: राज्य की नीति/योजना, बजट/अर्थव्यवस्था, पानी/सिंचाई/कृषि, प्रशासन, शिक्षा/स्वास्थ्य, पर्यावरण/वन्यजीव, महत्वपूर्ण परियोजना, राजस्थान-विशिष्ट आँकड़े/रिपोर्ट और परीक्षोपयोगी विरासत/भूगोल। खबर का राजस्थान से स्पष्ट संबंध होना चाहिए।
- अंतरराष्ट्रीय: भारत के संबंध, कूटनीति/समझौते, युद्ध/सुरक्षा, वैश्विक अर्थव्यवस्था, जलवायु/पर्यावरण, विज्ञान/तकनीक, महत्वपूर्ण अंतरराष्ट्रीय संगठन/रिपोर्ट।
- केवल सामान्य भाषण, किसी नेता की उपस्थिति/दौरा, औपचारिक मुलाकात, नियमित समारोह, सेलिब्रिटी, मनोरंजन, रोज़मर्रा का खेल, स्थानीय अपराध/दुर्घटना या बिना परीक्षा-संदर्भ वाली हल्की खबरें छोड़ दो। केवल किसी मंत्री के कार्यक्रम में शामिल होने के बजाय नई नीति, निर्णय, आँकड़ा, परियोजना या उसके वास्तविक परिणाम को प्राथमिकता दो।
- हर खबर स्रोत से समर्थित और अलग विषय की हो। समान घटना/योजना की duplicate खबरों में सबसे स्पष्ट प्राथमिक स्रोत वाली एक ही चुनो। स्रोत में पर्याप्त तथ्य न हों तो खबर छोड़ दो।

हर चुनी हुई खबर:
- source_id को ज्यों-का-त्यों रखो; केवल दिए गए source_id इस्तेमाल करो। category को मूल स्रोत वाली category ही रखो।
- headline संक्षिप्त और तथ्य-केंद्रित हिंदी में हो; headline/one_liner में URL, वेबसाइट लिंक या markdown link बिल्कुल न डालो। स्रोत URL केवल source metadata के लिए है।
- one_liner हिंदी में 35–70 शब्द और लगभग 2–4 वाक्य का हो। उसमें क्या निर्णय/घटना हुई, कहाँ/किससे संबंधित है, और स्रोत में उपलब्ध मुख्य संख्या/तारीख/लक्ष्य/प्रभाव/विशेषता बताओ। उपलब्ध न हो तो अनुमान लगाकर न भरो। केवल स्रोत में प्रमाणित UPSC/RPSC महत्व बताओ; बेवजह “यह परीक्षा के लिए महत्वपूर्ण है” जैसी filler पंक्ति न लिखो।
- MCQ केवल स्रोत में मौजूद तथ्यों पर बनाओ। एक या दो प्रश्न; हर प्रश्न में चार अलग options, answer_index 0–3 और संक्षिप्त तथ्य-आधारित explanation हो। यदि एक भी सत्यापन-योग्य प्रश्न नहीं बनता, तो वह खबर लौटाओ ही मत।
- तारीख, रकम, आँकड़े, व्यक्ति/पद, योजना की पात्रता, परियोजना की दूरी/लागत/मार्ग या निष्कर्ष कभी मत गढ़ो। किसी तथ्य की पुष्टि स्रोत में नहीं है तो उसे छोड़ दो।
- priority 1 (सबसे अधिक महत्वपूर्ण) से 100 (कम महत्वपूर्ण) तक integer हो।
- केवल valid JSON लौटाओ, markdown fence नहीं। Format: {{"items":[{{"source_id":"S001","category":"national","headline":"...","one_liner":"...","priority":1,"quiz_questions":[{{"question":"...","options":["...","...","...","..."],"answer_index":0,"explanation":"..."}}]}}]}}

स्रोत खबरें:
{json.dumps(compact, ensure_ascii=False)}'''

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{urllib.parse.quote(GEMINI_MODEL, safe='')}:generateContent?key={urllib.parse.quote(api_key, safe='')}"
    response = post_json(url, {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0.1, "maxOutputTokens": 22000},
    })
    try:
        raw_text = response["candidates"][0]["content"]["parts"][0]["text"]
        data = json.loads(raw_text)
        items = data.get("items", [])
        if not isinstance(items, list):
            raise ValueError("Gemini response 'items' is not a list")
    except (KeyError, IndexError, TypeError, json.JSONDecodeError, ValueError) as exc:
        raise RuntimeError(f"AI response was not valid JSON: {exc}; response keys={list(response.keys())}") from exc

    allowed = {item["source_id"]: item for item in candidates}
    category_caps = {"national": 15, "rajasthan": 10, "international": 5}
    category_counts = {key: 0 for key in category_caps}
    seen_source_ids: set[str] = set()
    verified: list[dict] = []

    def clean_text(value: object) -> str:
        value = str(value or "")
        value = re.sub(r"https?://\S+|www\.\S+", "", value, flags=re.IGNORECASE)
        value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
        value = re.sub(r"\s+", " ", value).strip()
        return value

    for story in items:
        if not isinstance(story, dict):
            continue
        source_id = story.get("source_id")
        if not isinstance(source_id, str) or source_id not in allowed or source_id in seen_source_ids:
            continue
        original = allowed[source_id]
        category = original["category"]
        if category not in category_caps or category_counts[category] >= category_caps[category]:
            continue

        headline = clean_text(story.get("headline"))
        one_liner = clean_text(story.get("one_liner"))
        word_count = len(one_liner.split())
        if not (12 <= len(headline) <= 180 and 25 <= word_count <= 90):
            log(f"WARN summary length/relevance check failed for {source_id}; ignored")
            continue

        questions = []
        supplied = story.get("quiz_questions", [])
        if isinstance(supplied, list):
            seen_q = set()
            for question in supplied[:2]:
                if not isinstance(question, dict):
                    continue
                qtext = clean_text(question.get("question"))
                options = question.get("options")
                answer_index = question.get("answer_index")
                explanation = clean_text(question.get("explanation"))
                if (len(qtext) >= 8 and isinstance(options, list) and len(options) == 4
                        and all(isinstance(opt, str) and opt.strip() for opt in options)
                        and len({str(opt).strip().casefold() for opt in options}) == 4
                        and isinstance(answer_index, int) and not isinstance(answer_index, bool)
                        and 0 <= answer_index <= 3 and explanation):
                    qkey = qtext.casefold()
                    if qkey in seen_q:
                        continue
                    seen_q.add(qkey)
                    questions.append({
                        "question": qtext[:260],
                        "options": [clean_text(opt)[:220] for opt in options],
                        "answer_index": answer_index,
                        "explanation": explanation[:600],
                    })
        # A story without at least one source-supported practice question is not published.
        if not questions:
            log(f"WARN no valid source-grounded MCQ for {source_id}; story ignored")
            continue

        try:
            priority = max(1, min(100, int(story.get("priority", 50))))
        except (ValueError, TypeError):
            priority = 50

        verified.append({
            "edition_date": "", "event_date": original["event_date"], "category": category,
            "headline": headline, "one_liner": one_liner,
            "source_name": original["source_name"], "source_url": original["source_url"],
            "quiz_questions": questions, "priority": priority, "status": "published",
        })
        seen_source_ids.add(source_id)
        category_counts[category] += 1

    verified.sort(key=lambda item: item["priority"])
    log("AI-filtered stories: " + ", ".join(
        f"{cat}={category_counts[cat]}" for cat in ("national", "rajasthan", "international")
    ))
    return verified


def rest_request(url: str, key: str, method: str = "GET", payload: list | None = None, prefer: str | None = None) -> tuple[int, str]:
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
    }
    if prefer:
        headers["Prefer"] = prefer
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.status, response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace")


def main() -> int:
    supabase_url = os.getenv("SUPABASE_URL", "").strip().rstrip("/")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    missing = [name for name, value in (("SUPABASE_URL", supabase_url), ("SUPABASE_SERVICE_ROLE_KEY", supabase_key), ("GEMINI_API_KEY", gemini_key)) if not value]
    if missing:
        log("ERROR Required GitHub Actions secrets missing: " + ", ".join(missing))
        return 2

    now = dt.datetime.now(IST)
    edition_date = now.date()
    target_date = edition_date - dt.timedelta(days=1)
    log(f"Edition: {edition_date.isoformat()} | news date: {target_date.isoformat()} (Asia/Kolkata)")

    candidates: list[dict] = []
    for feed in FEEDS:
        try:
            parsed = parse_feed(http_get(feed["url"]), feed, target_date)
            candidates.extend(parsed)
            log(f"Feed {feed['name']}: {len(parsed)} item(s) for {target_date}")
        except Exception as exc:
            log(f"WARN feed failed {feed['name']}: {exc}")
    dipr_items = fetch_dipr(target_date)
    candidates.extend(dipr_items)
    log(f"Rajasthan DIPR: {len(dipr_items)} item(s) for {target_date}")

    # Deduplicate by canonical source URL before asking the model.
    deduped = []
    seen_urls = set()
    for item in candidates:
        if item["source_url"] not in seen_urls:
            seen_urls.add(item["source_url"])
            deduped.append(item)
    # Stratified input cap: a long national/international feed must not crowd Rajasthan out.
    category_limits = {"national": 45, "rajasthan": 45, "international": 30}
    category_seen = {key: 0 for key in category_limits}
    candidates = []
    for item in deduped:
        category = item.get("category")
        if category in category_limits and category_seen[category] < category_limits[category]:
            candidates.append(item)
            category_seen[category] += 1
    log("Source candidates after category balancing: " + ", ".join(
        f"{cat}={category_seen[cat]}" for cat in ("national", "rajasthan", "international")
    ))
    if not candidates:
        log("No source items dated yesterday were found. Nothing has been auto-published; this avoids inventing current affairs.")
        return 0

    # Skip links already published to today's edition.
    query = urllib.parse.urlencode({"edition_date": f"eq.{edition_date.isoformat()}", "select": "source_url"})
    existing_url = f"{supabase_url}/rest/v1/current_affairs?{query}"
    status, body = rest_request(existing_url, supabase_key)
    if status < 200 or status >= 300:
        log(f"ERROR Supabase duplicate check failed: HTTP {status} {body[:500]}")
        return 3
    try:
        existing = {row.get("source_url") for row in json.loads(body) if isinstance(row, dict)}
    except (json.JSONDecodeError, TypeError):
        log("ERROR Supabase duplicate check returned invalid JSON")
        return 3
    candidates = [item for item in candidates if item["source_url"] not in existing]
    if not candidates:
        log("All source links for today's edition already exist. Nothing new to publish.")
        return 0

    log(f"Sending {len(candidates)} source candidates to Gemini ({GEMINI_MODEL})...")
    try:
        stories = generate_stories(candidates, gemini_key)
    except Exception as exc:
        log(f"ERROR AI generation failed: {exc}")
        return 4
    if not stories:
        log("AI returned no valid, source-linked stories. Nothing has been published.")
        return 0

    published_at = now.isoformat()
    for story in stories:
        story["edition_date"] = edition_date.isoformat()
        story["published_at"] = published_at
    # PostgREST upsert is protected by the existing unique constraint.
    endpoint = f"{supabase_url}/rest/v1/current_affairs?on_conflict=edition_date%2Ccategory%2Cheadline%2Csource_url"
    status, body = rest_request(endpoint, supabase_key, method="POST", payload=stories,
                                prefer="resolution=merge-duplicates,return=representation")
    if status < 200 or status >= 300:
        log(f"ERROR Supabase publish failed: HTTP {status} {body[:1000]}")
        return 5
    try:
        saved = json.loads(body) if body.strip() else []
        count = len(saved) if isinstance(saved, list) else len(stories)
    except json.JSONDecodeError:
        count = len(stories)
    log(f"SUCCESS: {count} story/stories published for edition {edition_date.isoformat()}.")
    log("Categories: " + ", ".join(f"{cat}={sum(1 for item in stories if item['category'] == cat)}" for cat in ("national", "international", "rajasthan")))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)

