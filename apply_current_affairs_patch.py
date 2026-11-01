#!/usr/bin/env python3
"""Safely improve the existing Shri Shyam Library current-affairs publisher.

Run from anywhere inside the repository. Only these files are changed:
  automation/publish_current_affairs.py
  .github/workflows/current-affairs.yml
Local App.jsx/Admin UI work is deliberately left untouched.
"""
from __future__ import annotations
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
PIPELINE = ROOT / "automation" / "publish_current_affairs.py"
WORKFLOW = ROOT / ".github" / "workflows" / "current-affairs.yml"

NEW_FUNCTION = r"""def generate_stories(candidates: list[dict], api_key: str) -> list[dict]:
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


"""


def main() -> int:
    if not PIPELINE.is_file() or not WORKFLOW.is_file():
        print("ERROR: Run this from inside ~/shri-shyam-library (repo root).", file=sys.stderr)
        return 2

    pipeline_original = PIPELINE.read_text(encoding="utf-8")
    workflow_original = WORKFLOW.read_text(encoding="utf-8")

    start = pipeline_original.find("def generate_stories(candidates: list[dict], api_key: str) -> list[dict]:")
    end = pipeline_original.find("def rest_request(", start)
    if start < 0 or end < 0:
        print("ERROR: Could not locate the expected generate_stories() function; no files changed.", file=sys.stderr)
        return 3

    pipeline = pipeline_original[:start] + NEW_FUNCTION + pipeline_original[end:]

    old_cap = "    candidates = deduped[:60]"
    new_cap = '''    # Stratified input cap: a long national/international feed must not crowd Rajasthan out.
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
    ))'''
    if pipeline.count(old_cap) != 1:
        print("ERROR: Could not find the expected candidate cap; no files changed.", file=sys.stderr)
        return 4
    pipeline = pipeline.replace(old_cap, new_cap)

    # Preserve the current Asia/Kolkata schedule; only give the run more room for up to 30 briefs.
    if "timeout-minutes: 10" not in workflow_original:
        print("ERROR: Workflow timeout marker differs from expected; no files changed.", file=sys.stderr)
        return 5
    workflow = workflow_original.replace("timeout-minutes: 10", "timeout-minutes: 20", 1)

    # Validate before touching files.
    try:
        compile(pipeline, str(PIPELINE), "exec")
    except SyntaxError as exc:
        print(f"ERROR: Generated pipeline has a syntax error; no files changed: {exc}", file=sys.stderr)
        return 6
    # Guard against accidental loss of the higher completion budget during future edits.
    if '"maxOutputTokens": 22000' not in pipeline:
        print("ERROR: Output-token limit validation failed; no files changed.", file=sys.stderr)
        return 7

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = ROOT / ".git" / "ca-patch-backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    pipeline_backup = backup_dir / f"publish_current_affairs.py.backup-quality-{stamp}"
    workflow_backup = backup_dir / f"current-affairs.yml.backup-quality-{stamp}"
    pipeline_backup.write_text(pipeline_original, encoding="utf-8")
    workflow_backup.write_text(workflow_original, encoding="utf-8")
    PIPELINE.write_text(pipeline, encoding="utf-8")
    WORKFLOW.write_text(workflow, encoding="utf-8")

    print("SUCCESS: Current-affairs pipeline patched and Python syntax validated.")
    print("Changed: automation/publish_current_affairs.py")
    print("Changed: .github/workflows/current-affairs.yml (timeout 10 -> 20 min)")
    print("Preserved: src/App.jsx, src/CurrentAffairsAdmin.jsx and all other UI files.")
    print(f"Backups saved outside version control: {backup_dir}")
    print("Next: review with git diff --check && git diff -- automation/publish_current_affairs.py .github/workflows/current-affairs.yml")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
