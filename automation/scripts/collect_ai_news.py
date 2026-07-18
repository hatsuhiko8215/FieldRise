#!/usr/bin/env python3
"""FieldRise AI秘書 - AIニュース収集スクリプト

主要なAI関連RSSフィード（無料・キー不要）から最新ニュースを取得し、
JSONとして保存する。GitHub Actionsから毎日実行される。
標準ライブラリのみで動作（外部依存なし）。
"""
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from pathlib import Path

JST = timezone(timedelta(hours=9))

# AI関連RSSフィード（すべて公開・無料）
FEEDS = [
    {"name": "ITmedia AI+", "url": "https://rss.itmedia.co.jp/rss/2.0/aiplus.xml", "lang": "ja"},
    {"name": "ASCII.jp AI", "url": "https://ascii.jp/rss.xml", "lang": "ja"},
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "lang": "en"},
    {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/", "lang": "en"},
]

MAX_ITEMS_PER_FEED = 8
UA = "Mozilla/5.0 (FieldRise-AI-Secretary/1.0)"


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()


def parse_feed(name: str, url: str, lang: str) -> list:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as res:
        data = res.read()
    root = ET.fromstring(data)

    items = []
    # RSS 2.0
    for item in root.iter("item"):
        title = strip_html(item.findtext("title", ""))
        link = (item.findtext("link") or "").strip()
        pub = item.findtext("pubDate") or item.findtext(
            "{http://purl.org/dc/elements/1.1/}date") or ""
        desc = strip_html(item.findtext("description", ""))[:200]
        try:
            dt = parsedate_to_datetime(pub).astimezone(JST).isoformat() if pub else ""
        except Exception:
            dt = pub
        items.append({"source": name, "lang": lang, "title": title,
                      "url": link, "published": dt, "summary": desc})
        if len(items) >= MAX_ITEMS_PER_FEED:
            break
    # Atom
    if not items:
        ns = "{http://www.w3.org/2005/Atom}"
        for entry in root.iter(f"{ns}entry"):
            title = strip_html(entry.findtext(f"{ns}title", ""))
            link_el = entry.find(f"{ns}link")
            link = link_el.get("href") if link_el is not None else ""
            pub = entry.findtext(f"{ns}updated", "")
            items.append({"source": name, "lang": lang, "title": title,
                          "url": link, "published": pub, "summary": ""})
            if len(items) >= MAX_ITEMS_PER_FEED:
                break
    return items


def main() -> None:
    now = datetime.now(JST)
    all_items, errors = [], []
    for feed in FEEDS:
        try:
            items = parse_feed(feed["name"], feed["url"], feed["lang"])
            all_items.extend(items)
            print(f"OK: {feed['name']} ({len(items)} items)")
        except Exception as e:
            errors.append({"source": feed["name"], "error": str(e)})
            print(f"NG: {feed['name']} - {e}")

    output = {
        "collected_at": now.isoformat(),
        "total_items": len(all_items),
        "errors": errors,
        "items": all_items,
    }

    out_dir = Path(__file__).resolve().parents[2] / "projects" / "project-001-ai-secretary" / "data" / "ai-news"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{now.strftime('%Y-%m-%d')}.json"
    out_file.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out_dir / "latest.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"ai-news saved: {out_file}")


if __name__ == "__main__":
    main()
