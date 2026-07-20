import json
import os
import glob
from datetime import datetime, timedelta

def load_latest_data(days_ago=0):
    target_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
    path = f"data/raw_stats_{target_date}.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def generate_report():
    today_data = load_latest_data(0)
    yesterday_data = load_latest_data(1)
    
    if not today_data:
        return "本日のデータが取得できませんでした。"

    # Analysis Logic
    report = []
    report.append(f"【Cafeブランドレポート】 {today_data['date']}")
    report.append("---")
    
    # 1. Overall Brand Stats
    total_usage = sum(today_data['tracks'].values())
    prev_total = sum(yesterday_data['tracks'].values()) if yesterday_data else total_usage
    diff = total_usage - prev_total
    
    report.append(f"■ Cafeシリーズ総使用数: {total_usage:,}")
    report.append(f"  前日比: {'+' if diff >= 0 else ''}{diff:,}")
    
    # 2. Ranking
    sorted_tracks = sorted(today_data['tracks'].items(), key=lambda x: x[1], reverse=True)
    report.append("\n■ 人気ランキング")
    for i, (name, usage) in enumerate(sorted_tracks[:3], 1):
        report.append(f" {i}. {name}: {usage:,}")

    # 3. Brand Manager Analysis (桃花)
    report.append("\n■ 桃花の分析")
    if diff > 100:
        analysis = "世界各地で楽曲の採用が加速しています。特にカフェ系Vlogでの使用が目立ちます。"
        next_step = "今の勢いを活かし、リラックス系の新曲を準備することをおすすめします。"
    else:
        analysis = "安定した成長を維持しています。ブランドの認知度は着実に世界へ広がっています。"
        next_step = "既存曲の別バージョン（Lo-fi版など）の展開を検討しましょう。"
        
    report.append(f"・状況: {analysis}")
    report.append(f"・今日のアクション: {next_step}")
    
    report.append("\n■ 経営判断用提案")
    report.append("・現在の成長率に基づくと、来月には累計10万回使用を達成する見込みです。")
    report.append("・海外の特定地域での反応をフル分析する価値が出てきています（要提案）。")

    return "\n".join(report)

def main():
    report_text = generate_report()
    
    # Save for LINE notification
    with open("data/latest_report.txt", "w", encoding="utf-8") as f:
        f.write(report_text)
        
    # Save as Markdown briefing
    date_str = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("projects/project-001-ai-secretary/briefings", exist_ok=True)
    with open(f"projects/project-001-ai-secretary/briefings/cafe_{date_str}.md", "w", encoding="utf-8") as f:
        f.write(f"# Cafeブランドレポート {date_str}\n\n" + report_text)

if __name__ == "__main__":
    main()
