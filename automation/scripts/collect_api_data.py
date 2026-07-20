import os
import json
import requests
from datetime import datetime

# API Credentials (to be set in GitHub Secrets)
TIKTOK_API_KEY = os.environ.get("TIKTOK_API_KEY")
INSTAGRAM_API_KEY = os.environ.get("INSTAGRAM_API_KEY")
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

def collect_youtube_data():
    """Fetches YouTube analytics for Cafe series."""
    if not YOUTUBE_API_KEY:
        return None
    # TODO: Implement YouTube Data API v3 calls
    print("YouTube API key found. Ready to implement collection.")
    return {"views": 0, "subscribers": 0}

def collect_instagram_data():
    """Fetches Instagram Graph API data."""
    if not INSTAGRAM_API_KEY:
        return None
    # TODO: Implement Instagram Graph API calls
    print("Instagram API key found. Ready to implement collection.")
    return {"followers": 0, "reach": 0}

def collect_tiktok_api_data():
    """Fetches TikTok Research API or Display API data."""
    if not TIKTOK_API_KEY:
        return None
    # TODO: Implement TikTok API calls
    print("TikTok API key found. Ready to implement collection.")
    return {"video_count": 0, "likes": 0}

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"Checking API availability for {date_str}...")
    
    data = {
        "date": date_str,
        "youtube": collect_youtube_data(),
        "instagram": collect_instagram_data(),
        "tiktok": collect_tiktok_api_data()
    }
    
    # Save results if any API was successful
    if any(v is not None for v in data.values() if v != date_str):
        os.makedirs("data", exist_ok=True)
        with open(f"data/api_stats_{date_str}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("API data collection completed.")
    else:
        print("No API keys configured. Skipping collection.")

if __name__ == "__main__":
    main()
