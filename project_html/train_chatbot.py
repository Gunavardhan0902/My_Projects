import json
import random
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

nltk.download("punkt")
nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()

# Load intents
with open("intents.json") as file:
    data = json.load(file)

corpus = []
tags = []
responses = {}

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        corpus.append(pattern)
        tags.append(intent["tag"])
    responses[intent["tag"]] = intent["responses"]

# Vectorization
vectorizer = CountVectorizer(tokenizer=nltk.word_tokenize)
X = vectorizer.fit_transform(corpus)
y = tags

# Train classifier
model = MultinomialNB()
model.fit(X, y)

# Save model and vectorizer
with open("chatbot_model.pkl", "wb") as f:
    pickle.dump((model, vectorizer, responses), f)

print("✅ Chatbot model trained and saved.")
