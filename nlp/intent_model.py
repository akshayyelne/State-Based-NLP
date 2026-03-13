import json
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from config import INTENTS_PATH

# ======================================

# LOAD & TRAIN INTENT MODEL (CACHED)

# ======================================

@st.cache_resource
def load_model():
"""
Loads intents from JSON, trains the TF-IDF + Logistic Regression model,
and caches it for reuse across Streamlit sessions.
"""

```
with open(INTENTS_PATH, "r") as file:
    intents = json.load(file)

patterns = []
tags = []

for intent in intents:
    for pattern in intent["patterns"]:
        patterns.append(pattern.lower())
        tags.append(intent["tag"])

vectorizer = TfidfVectorizer()
clf = LogisticRegression(max_iter=1000)

x = vectorizer.fit_transform(patterns)
clf.fit(x, tags)

return vectorizer, clf
```

# ======================================

# INTENT PREDICTION

# ======================================

def predict_intent(text):
"""
Predicts the intent tag for user input.
"""

```
vectorizer, clf = load_model()
prediction = clf.predict(vectorizer.transform([text.lower()]))

return prediction[0]
```
