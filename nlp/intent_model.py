import json
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from config import INTENTS_PATH


@st.cache_resource
def load_model():

    with open(INTENTS_PATH) as file:
        intents = json.load(file)

    vectorizer = TfidfVectorizer()
    clf = LogisticRegression(max_iter=1000)

    tags = []
    patterns = []

    for intent in intents:
        for pattern in intent["patterns"]:
            patterns.append(pattern.lower())
            tags.append(intent["tag"])

    x = vectorizer.fit_transform(patterns)
    clf.fit(x, tags)

    return vectorizer, clf


vectorizer, clf = load_model()


def predict_intent(text):
    return clf.predict(vectorizer.transform([text.lower()]))[0]
