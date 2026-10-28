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
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

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


def post_json(url: str, body: dict, headers: dict[str, str] | None = None, timeout: int = 60) -> dict:
    payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
    request_headers = {"Content-Type": "application/json", "Accept": "application/json", "User-Agent": USER_AGENT}
    if headers:
        request_headers.update(headers)
    req = urllib.request.Request(url, data=payload, headers=request_headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read().decode("utf-8", errors="replace")
        return json.loads(raw) if raw.strip() else {}


def generate_stories(candidates: list[dict], api_key: str) -> list[dict]:
    if not candidates:
        return []
    for index, item in enumerate(candidates, start=1):
        item["source_id"] = f"S{index:03d}"
    compact = [{k: item[k] for k in ("source_id", "category", "source_name", "source_url", "source_title", "source_description", "event_date")} for item in candidates]
    prompt = f'''तुम श्री श्याम लाइब्रेरी के UPSC/RPSC करंट अफेयर्स संपादक हो। नीचे केवल मूल स्रोतों से मिली खबरें हैं। इन्हीं के आधार पर हिंदी सामग्री बनाओ।
नियम:
- केवल परीक्षा उपयोगी, महत्वपूर्ण और स्रोत से समर्थित तथ्य चुनो; अधिकतम 18 खबरें। गैर-प्रासंगिक/डुप्लिकेट आइटम छोड़ दो।
- तथ्य, संख्या, तारीख, पद, योजना या निष्कर्ष मत गढ़ो। विवरण कम हो तो संक्षिप्त लिखो।
- प्रत्येक कहानी का source_id ठीक वही रखना; कोई नया/अज्ञात source_id नहीं। category को दिए हुए category से न बदलना।
- headline स्पष्ट हिंदी में हो, one_liner 2-4 तथ्यात्मक वाक्यों में 40-100 शब्द तक हो और UPSC/RPSC संदर्भ बताए, पर अटकल न लगाए।
- प्रति कहानी 2 MCQ बनाओ; हर MCQ में चार options, answer_index 0-3 और एक तथ्य-आधारित explanation हो। अगर स्रोत से दो सत्यापन योग्य प्रश्न नहीं बनते तो 1 प्रश्न देना, लेकिन तथ्य न बनाना।
- priority 1 (सबसे महत्वपूर्ण) से 100 (कम महत्वपूर्ण) के बीच integer हो।
- सिर्फ valid JSON लौटाना, markdown fences नहीं। Format: {{"items":[{{"source_id":"S001","category":"national","headline":"...","one_liner":"...","priority":1,"quiz_questions":[{{"question":"...","options":["...","...","...","..."],"answer_index":0,"explanation":"..."}}]}}]}}
स्रोत खबरें:
{json.dumps(compact, ensure_ascii=False)}'''
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{urllib.parse.quote(GEMINI_MODEL, safe='')}:generateContent?key={urllib.parse.quote(api_key, safe='')}"
    response = post_json(url, {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0.2, "maxOutputTokens": 12000},
    })
    try:
        text = response["candidates"][0]["content"]["parts"][0]["text"]
        data = json.loads(text)
        items = data.get("items", [])
        if not isinstance(items, list):
            raise ValueError("Gemini response 'items' is not a list")
    except (KeyError, IndexError, TypeError, json.JSONDecodeError, ValueError) as exc:
        raise RuntimeError(f"AI response was not valid JSON: {exc}; response keys={list(response.keys())}") from exc
    allowed = {item["source_id"]: item for item in candidates}
    verified = []
    for story in items:
        if not isinstance(story, dict) or story.get("source_id") not in allowed:
            continue
        original = allowed[story["source_id"]]
        headline = str(story.get("headline", "")).strip()
        one_liner = str(story.get("one_liner", "")).strip()
        category = original["category"]
        if not (5 <= len(headline) <= 220 and 10 <= len(one_liner) <= 700):
            log(f"WARN invalid summary ignored for {original['source_id']}")
            continue
        questions = []
        supplied = story.get("quiz_questions", [])
        if isinstance(supplied, list):
            for question in supplied[:2]:
                if not isinstance(question, dict):
                    continue
                qtext = str(question.get("question", "")).strip()
                options = question.get("options")
                answer_index = question.get("answer_index")
                explanation = str(question.get("explanation", "")).strip()
                if (len(qtext) >= 8 and isinstance(options, list) and len(options) == 4
                        and all(isinstance(opt, str) and opt.strip() for opt in options)
                        and isinstance(answer_index, int) and 0 <= answer_index <= 3):
                    questions.append({"question": qtext, "options": [opt.strip()[:220] for opt in options],
                                      "answer_index": answer_index, "explanation": explanation[:600]})
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
    candidates = deduped[:60]
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

