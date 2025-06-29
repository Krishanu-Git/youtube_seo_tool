import requests
from googleapiclient.discovery import build
import html
import streamlit as st

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"

API_KEY = st.secrets.get("YOUTUBE_API_KEY", None)

def search_videos(query, max_results=5):
    params = {
        'part': 'snippet',
        'q': query,
        'key': API_KEY,
        'maxResults': max_results,
        'type': 'video'
    }
    response = requests.get(YOUTUBE_SEARCH_URL, params=params)
    return [item['id']['videoId'] for item in response.json().get('items', [])]

def get_video_metadata(video_ids):
    params = {
        'part': 'snippet',
        'id': ','.join(video_ids),
        'key': API_KEY
    }
    response = requests.get(YOUTUBE_VIDEO_URL, params=params)
    results = []
    for item in response.json().get('items', []):
        snippet = item['snippet']
        results.append({
            'title': snippet['title'],
            'description': snippet['description'],
            'tags': snippet.get('tags', []),
            'channelTitle': snippet['channelTitle']
        })
    return results

def get_single_video_metadata(video_id):
    result = get_video_metadata([video_id])
    return result[0] if result else None

def get_video_comments(video_id, max_comments=50):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    comments = []
    try:
        results = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=min(max_comments, 100),
            textFormat="plainText"
        ).execute()

        for item in results["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(html.unescape(comment))
    except Exception as e:
        print("Error fetching comments:", e)
    return comments