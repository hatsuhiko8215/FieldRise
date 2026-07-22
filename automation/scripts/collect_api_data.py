import os
import json
import requests
import sys
from typing import Dict, Any, Optional
from datetime import datetime

sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

# API Credentials (to be set in GitHub Secrets)
TIKTOK_API_KEY = os.environ.get("TIKTOK_API_KEY")
INSTAGRAM_API_KEY = os.environ.get("INSTAGRAM_API_KEY")
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

def get_tiktok_user_info(unique_id: str) -> Dict[str, Any]:
    """
    Fetch user information from TikTok using the Manus API.
    """
    client = ApiClient()
    query_params = {
        'uniqueId': unique_id
    }
    try:
        response = client.call_api('Tiktok/get_user_info', query=query_params)
        return response
    except Exception as e:
        print(f"Error calling TikTok API (get_user_info): {str(e)}")
        return {}

def get_tiktok_user_popular_posts(
    sec_uid: str,
    count: int = 35,
    cursor: str = "0"
) -> Dict[str, Any]:
    """
    Fetch popular posts from a TikTok user using the Manus API.
    """
    client = ApiClient()
    query_params = {
        'secUid': sec_uid,
        'count': str(count),
        'cursor': cursor
    }
    try:
        response = client.call_api('Tiktok/get_user_popular_posts', query=query_params)
        return response
    except Exception as e:
        print(f"Error calling TikTok API (get_user_popular_posts): {str(e)}")
        return {}

def collect_youtube_data():
    """Fetches YouTube analytics for Cafe series."""
    if not YOUTUBE_API_KEY:
        return None
    # TODO: Implement YouTube Data API v3 calls
    print("YouTube API key found. Ready to implement collection.")
    return {"views": 0, "subscribers": 0}

def collect_instagram_data():
    """
    Fetches Instagram Graph API data.
    """
    if not INSTAGRAM_API_KEY:
        return None
    # TODO: Implement Instagram Graph API calls
    print("Instagram API key found. Ready to implement collection.")
    return {"followers": 0, "reach": 0}

def collect_tiktok_api_data():
    """
    Fetches TikTok Research API or Display API data.
    """
    if not TIKTOK_API_KEY:
        print("TikTok API key not found. Skipping TikTok data collection.")
        return None

    tiktok_data = {}
    # Example: Get user info for 'fieldrise_official'
    tiktok_username = "fieldrise_official" # This should be replaced with the actual TikTok username
    user_info = get_tiktok_user_info(tiktok_username)

    if user_info and user_info.get('userInfo', {}).get('user', {}).get('secUid'):
        sec_uid = user_info['userInfo']['user']['secUid']
        tiktok_data['user_info'] = {
            'uniqueId': user_info['userInfo']['user']['uniqueId'],
            'nickname': user_info['userInfo']['user']['nickname'],
            'followerCount': user_info['userInfo']['stats']['followerCount'],
            'heartCount': user_info['userInfo']['stats']['heartCount'],
            'videoCount': user_info['userInfo']['stats']['videoCount']
        }
        print(f"TikTok user info collected for {tiktok_username}.")

        # Get popular posts
        popular_posts = get_tiktok_user_popular_posts(sec_uid, count=10)
        if popular_posts and popular_posts.get('data', {}).get('itemList'):
            tiktok_data['popular_posts'] = []
            for post in popular_posts['data']['itemList']:
                tiktok_data['popular_posts'].append({
                    'id': post.get('id'),
                    'desc': post.get('desc'),
                    'playCount': post.get('stats', {}).get('playCount'),
                    'diggCount': post.get('stats', {}).get('diggCount'),
                    'commentCount': post.get('stats', {}).get('commentCount')
                })
            print(f"TikTok popular posts collected for {tiktok_username}.")
    else:
        print(f"Could not retrieve TikTok user info or secUid for {tiktok_username}.")

    return tiktok_data

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
        print("No API keys configured or no data collected. Skipping collection.")

if __name__ == "__main__":
    main()
