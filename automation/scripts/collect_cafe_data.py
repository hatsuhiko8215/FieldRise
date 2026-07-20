import requests
import json
import os
import re
from datetime import datetime

# Configuration
ARTIST_URL = "https://www.tiktok.com/@runa_girl8215"
# Example track list based on initial research
TRACKS = {
    "cafe (Original)": "https://www.tiktok.com/music/cafe-7415813060487104513",
    "cafe (night)": "https://www.tiktok.com/music/cafe-night-7415813060487104513", # Placeholder IDs
}

def get_tiktok_stats(url):
    """
    Scrapes basic profile stats. 
    Note: In production (GitHub Actions), we use simple regex to avoid heavy browser usage.
    """
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        if response.status_code == 200:
            # Simple regex to find follower/like counts in HTML
            followers = re.search(r'"followerCount":(\d+)', response.text)
            likes = re.search(r'"heartCount":(\d+)', response.text)
            return {
                "followers": int(followers.group(1)) if followers else 0,
                "likes": int(likes.group(1)) if likes else 0
            }
    except Exception as e:
        print(f"Error fetching profile: {e}")
    return {"followers": 0, "likes": 0}

def get_track_usage(track_url):
    """
    Scrapes track usage count from TikTok music page.
    """
    try:
        response = requests.get(track_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        if response.status_code == 200:
            # Look for video count (e.g., "59.4K videos" or "59400")
            # In Japanese: "59.4K 動画"
            match = re.search(r'(\d+(\.\d+)?K?)\s*(動画|videos)', response.text)
            if match:
                val_str = match.group(1)
                if 'K' in val_str:
                    return int(float(val_str.replace('K', '')) * 1000)
                return int(val_str)
    except Exception as e:
        print(f"Error fetching track: {e}")
    return 0

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # 1. Profile Stats
    profile_stats = get_tiktok_stats(ARTIST_URL)
    
    # 2. Track Stats
    track_stats = {}
    for name, url in TRACKS.items():
        usage = get_track_usage(url)
        track_stats[name] = usage
        
    # 3. Output Data
    result = {
        "date": date_str,
        "profile": profile_stats,
        "tracks": track_stats
    }
    
    # Save to data directory
    os.makedirs("data", exist_ok=True)
    with open(f"data/raw_stats_{date_str}.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"Data collected for {date_str}")

if __name__ == "__main__":
    main()
