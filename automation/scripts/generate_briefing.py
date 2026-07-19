#!/usr/bin/env python3
"""FieldRise AI秘書 - 日報（デイリーブリーフィング）生成スクリプト

収集済みの天気・AIニュースデータから、社長向けの日報Markdownを生成する。
GitHub Actionsから毎日実行される。
"""
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

JST = timezone(timedelta(hours=9))
WEEKDAYS_JA = ["月", "火", "水", "木", "金", "土", "日"]

BASE = Path(__file__).resolve().parents[2] / "projects" / "project-001-ai-secretary"


def load_json(path: Path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return None


def weather_section(data) -> str:
    if not data:
        return "本日の天気データは取得できませんでした。\n"
    lines = [
        f"**地点**: {data['location']}（データ提供: Open-Meteo）",
        "",
        "| 日付 | 天気 | 最高/最低気温 | 降水量 | 降水確率 | 最大風速 |",
        "|---|---|---|---|---|---|",
    ]
    for d in data["forecast"][:5]:
        dt = datetime.strptime(d["date"], "%Y-%m-%d")
        wd = WEEKDAYS_JA[dt.weekday()]
        lines.append(
            f"| {d['date']}（{wd}） | {d['weather']} "
            f"| {d['temp_max_c']}°C / {d['temp_min_c']}°C "
            f"| {d['precipitation_mm']}mm | {d['precipitation_probability_pct']}% "
            f"| {d['wind_max_kmh']}km/h |"
        )
    # 農業向けアラート（簡易ルール）
    alerts = []
    today = data["forecast"][0]
    if today["temp_max_c"] >= 35:
        alerts.append("猛暑日予想（35°C以上）。高温障害・水管理に注意してください。")
    if today["precipitation_probability_pct"] >= 70:
        alerts.append("降水確率70%以上。屋外作業の予定調整をおすすめします。")
    if today["wind_max_kmh"] >= 40:
        alerts.append("強風予想（40km/h以上）。resource・設備の固定を確認してください。")
    for d in data["forecast"][:3]:
        if d["precipitation_mm"] >= 30:
            alerts.append(f"{d['date']}に大雨予想（{d['precipitation_mm']}mm）。排水対策をご検討ください。")
            break
    if alerts:
        lines.append("")
        lines.append("**【農業アラート】**")
        for a in alerts:
            lines.append(f"- {a}")
    return "\n".join(lines) + "\n"


def news_section(data) -> str:
    if not data or not data.get("items"):
        return "本日のAIニュースは取得できませんでした。\n"
    lines = []
    # 日本語ソース優先で表示
    ja = [i for i in data["items"] if i.get("lang") == "ja"][:6]
    en = [i for i in data["items"] if i.get("lang") == "en"][:6]
    if ja:
        lines.append("**国内AIニュース**")
        lines.append("")
        for i in ja:
            lines.append(f"- [{i['title']}]({i['url']}) — {i['source']}")
        lines.append("")
    if en:
        lines.append("**海外AIニュース**")
        lines.append("")
        for i in en:
            lines.append(f"- [{i['title']}]({i['url']}) — {i['source']}")
    return "\n".join(lines) + "\n"


def main() -> None:
    now = datetime.now(JST)
    date_str = now.strftime("%Y-%m-%d")
    wd = WEEKDAYS_JA[now.weekday()]

    weather = load_json(BASE / "data" / "weather" / "latest.json")
    news = load_json(BASE / "data" / "ai-news" / "latest.json")

    md = f"""# FieldRise デイリーブリーフィング {date_str}（{wd}）

**作成**: FieldRise 秘書の桃花（自動生成） | **生成時刻**: {now.strftime('%H:%M')} JST

---

## 1. 天気情報（まんのう町）

{weather_section(weather)}

---

## 2. AIニュース

{news_section(news)}

---

## 3. 運用メモ

本ブリーフィングはGitHub Actionsにより毎朝自動生成されています。
掲載領域の追加（YouTube・SNS分析、売上、農業データ等）は段階的に拡張予定です。
問題や改善要望はCOO（Manus）までお知らせください。
"""

    out_dir = BASE / "briefings"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{date_str}.md"
    out_file.write_text(md, encoding="utf-8")
    (out_dir / "latest.md").write_text(md, encoding="utf-8")
    print(f"briefing saved: {out_file}")


if __name__ == "__main__":
    main()
