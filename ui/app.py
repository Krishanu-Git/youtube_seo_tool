import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from api.youtube_api import get_single_video_metadata, get_video_comments
from core.tag_generator import generate_seo_tags_from_text, translate_tags
from utils.helpers import extract_video_id, analyze_comment_sentiment
import openai

OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", None)

openai.api_key = OPENAI_API_KEY

def generate_ai_title(original_title):
    prompt = f"Rewrite the following YouTube title to be more clickworthy and SEO-friendly: '{original_title}'. Keep it under 70 characters."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"AI Error: {str(e)}"

st.title("🎯 YouTube Video SEO Tag Analyzer")
video_url = st.text_input("Enter a YouTube video URL")

if st.button("Analyze Video"):
    video_id = extract_video_id(video_url)
    if not video_id:
        st.error("❌ Invalid YouTube video link")
    else:
        with st.spinner("Fetching video metadata..."):
            metadata = get_single_video_metadata(video_id)
            if not metadata:
                st.error("❌ Could not retrieve video data.")
            else:
                st.success("✅ Video Loaded!")
                thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
                st.image(thumbnail_url, caption="Video Thumbnail", use_container_width=True)
                st.subheader("Channel Title:")
                st.write(metadata['channelTitle'])
                st.subheader("Video Title:")
                st.write(metadata['title'])
                st.subheader("Video Description:")
                st.write(metadata['description'])

                texts = [metadata['title'] + " " + metadata['description']]
                tags = generate_seo_tags_from_text(texts)

                st.subheader("🔖 SEO-Optimized Tags Suggestion")
                st.code(", ".join(tags), language="text")

                if metadata.get("tags"):
                    st.subheader("📌 Existing Tags (from YouTube)")
                    st.code(", ".join(metadata['tags']), language="text")
                
                # Tag Translation
                st.subheader("🌐 Tag Translations")
                translated = translate_tags(metadata['tags'])
                for lang, tags in translated.items():
                    st.write(f"{lang.upper()}: {', '.join(tags)}")

                # AI Title Suggestion
                st.subheader("🔮 AI-Generated SEO Title")
                ai_title = generate_ai_title(metadata["title"])
                st.success(ai_title)

                # Sentiment Analysis
                st.subheader("🗣️ Comment Sentiment")
                comments = get_video_comments(video_id)
                if comments:
                    sentiment = analyze_comment_sentiment(comments)
                    st.write(f"Average Sentiment Score: `{sentiment:.2f}` (−1: Negative, +1: Positive)")
                else:
                    st.warning("No comments found or error fetching comments.")
