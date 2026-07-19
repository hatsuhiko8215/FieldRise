# CTO Review Request: Cafe Brand Strategy & Database Design

## Context
President has initiated Project-001 Ver.2 "Cafe Brand Cultivation System". The goal is to make the "Cafe series" by Runa-Girl8215 a globally recognized BGM brand. The President explicitly stated: "The market for the Cafe series is the WORLD."

## Brand Manager (COO/桃花) Proposal
As the Brand Manager, I propose the following analysis logic and data structure:

### 1. Key Metrics to Track
- **Track Level**: Total usage (videos), Daily/7d/30d growth, Viral potential (Breakout status).
- **Account Level**: Followers, Total Likes, Engagement rate.
- **Brand Level**: Total brand usage (sum of all Cafe tracks), Sentiment/Category of videos using the tracks.

### 2. Database Structure (GitHub-based CSV/JSON)
We need a persistent record to track long-term trends. I suggest:
- `data/tiktok_account_stats.csv`: Daily snapshots of @runa_girl8215.
- `data/cafe_series_usage.csv`: Daily usage counts for each track in the series.
- `data/video_trends.json`: Metadata of top videos using the tracks to identify popular genres.

### 3. Analysis Logic
- **Growth Rate**: (Today - Yesterday) / Yesterday.
- **Momentum**: Acceleration of growth rate.
- **Strategy Recommendation**: If a specific track (e.g., "Midnight Espresso") is growing in "Cooking" videos, suggest creating more tracks with similar vibes or targeting that niche.

## CTO Questions
1. Does this database structure support the "5-10 year global brand growth" vision? How should we handle multi-region data?
2. What advanced KPIs should we use to measure "Brand Love" beyond just usage counts?
3. How can we leverage GitHub Automation to make these insights "経営判断できる (Decision-ready)" for the President?

Please review and provide your CTO perspective.
