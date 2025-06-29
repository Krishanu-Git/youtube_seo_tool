from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from googletrans import Translator
import re

def clean_text(texts):
    return [" ".join(re.sub(r'[^a-zA-Z0-9 ]', '', t.lower()).split()) for t in texts]

def generate_seo_tags_from_text(texts, num_tags=10):
    texts = clean_text(texts)
    tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
    X = tfidf.fit_transform(texts)

    lda = LatentDirichletAllocation(n_components=1, random_state=42)
    lda.fit(X)

    keywords = []
    terms = tfidf.get_feature_names_out()
    for idx in lda.components_[0].argsort()[::-1][:num_tags]:
        keywords.append(terms[idx])

    return keywords

def translate_tags(tags, target_langs=["hi", "bn"]):
    translator = Translator()
    translations = {}
    for lang in target_langs:
        translations[lang] = [translator.translate(tag, dest=lang).text for tag in tags]
    return translations