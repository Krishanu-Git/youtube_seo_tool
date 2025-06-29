import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from api.youtube_api import get_single_video_metadata
from core.tag_generator import generate_seo_tags_from_text
from utils.helpers import extract_video_id

def detailed_seo_score(metadata, suggested_tags, search_term):
    title = metadata['title'].lower()
    desc = metadata['description'].lower()
    tags = [t.lower() for t in metadata.get('tags', [])]
    keywords = search_term.lower().split()

    score = 0
    report = []

    # Title Length
    if 50 <= len(title) <= 70:
        score += 10
    else:
        report.append("✏️ Title should be 50–70 characters. (+0/10)")

    # Description Length
    if len(desc) >= 150:
        score += 15
    else:
        report.append("📝 Description should be at least 150 characters. (+0/15)")

    # Keyword in Title
    if any(k in title for k in keywords):
        score += 15
    else:
        report.append("🔑 Use keywords in your title. (+0/15)")

    # Keyword in Tags
    if any(k in ' '.join(tags) for k in keywords):
        score += 10
    else:
        report.append("🏷️ Include keywords in your tags. (+0/10)")

    # Tag Count
    if len(tags) >= 10:
        score += 10
    else:
        report.append("🔖 Add at least 10 tags. (+0/10)")

    # Matching Suggested Tags
    match_count = len(set(suggested_tags).intersection(tags))
    if match_count >= 3:
        score += 10
    else:
        report.append("🧩 Use more suggested tags from SEO engine. (+0/10)")

    # Keyword in Description
    if any(k in desc for k in keywords):
        score += 10
    else:
        report.append("🗣️ Mention keywords in your description. (+0/10)")

    # Tag Uniqueness (avoid overused tags like “funny”)
    generic_tags = {"funny", "cool", "nice", "fun", "new", "youtube", "video"}
    unique_tags = [t for t in tags if t not in generic_tags]
    if len(unique_tags) >= len(tags) * 0.7:
        score += 10
    else:
        report.append("📌 Use more specific/unique tags. (+0/10)")

    return score, report

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
                
                # st.subheader("📊 Advanced SEO Performance Score")
                # seo_score, issues = detailed_seo_score(metadata, tags, video_url)
                # st.write(f"🔎 Final SEO Score: **{seo_score} / 100**")
                # if issues:
                #     st.warning("💡 Suggestions to Improve SEO:")
                #     for msg in issues:
                #         st.markdown(f"- {msg}")
                # else:
                #     st.success("✅ Excellent SEO optimization! 🔥")
