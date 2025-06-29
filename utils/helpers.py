import re
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

def extract_video_id(url):
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    return match.group(1) if match else None

def analyze_comment_sentiment(comments):
    nltk.download("vader_lexicon")

    sia = SentimentIntensityAnalyzer()
    sentiment_scores = [sia.polarity_scores(comment)["compound"] for comment in comments]
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
    return avg_sentiment