import json
import os
import random
import pickle
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report, accuracy_score
from collections import Counter

DATA_PATH = os.path.join("ml", "dataset.json")
MODEL_PATH = os.path.join("ml", "model.pkl")
VECTORIZER_PATH = os.path.join("ml", "vectorizer.pkl")

RANDOM_SEED = 42

def load_dataset():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts, labels = [], []

    for intent in data["intents"]:
        tag = intent["tag"]
        for pattern in intent["patterns"]:
            texts.append(pattern.lower().strip())
            labels.append(tag)

    return texts, labels

def train():
    print("\nFalconAI ML Training Started...\n")

    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    texts, labels = load_dataset()

    counts = Counter(labels)
    texts  = [t for t, l in zip(texts, labels) if counts[l] >= 4]
    labels = [l for l in labels if counts[l] >= 4]

    print(f"Dataset size: {len(texts)} samples")
    print(f"Intents: {len(set(labels))}\n")

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels,
        test_size=0.2,
        random_state=RANDOM_SEED,
        stratify=labels
    )

    vectorizer = TfidfVectorizer(
        max_features=8000,
        ngram_range=(1, 3),
        stop_words="english",
        lowercase=True,
        sublinear_tf=True
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec  = vectorizer.transform(X_test)

    print("Vectorization complete")

    base_model = LinearSVC(max_iter=3000, C=0.8)

    model = CalibratedClassifierCV(base_model, cv=3)
    model.fit(X_train_vec, y_train)
    
    test_cases = [
        ("stock market today", "business_news"),
        ("what happened in kosovo", "watch_balkan_news"),
        ("goodbye", "goodbye"),
        ("tech news today", "tech_news"),
        ("I am sad", "music_sad"),
    ]
    
    print("\n[TEST CASES]")
    for phrase, expected in test_cases:
        vec = vectorizer.transform([phrase])
        pred = model.predict(vec)[0]
        proba = max(model.predict_proba(vec)[0])
        status = "✅" if pred == expected else "❌"
        print(f"{status} '{phrase}' -> {pred} (expected: {expected}, conf: {round(proba*100,1)}%)")
        
    print("Model training complete")
        
    predictions = model.predict(X_test_vec)
    acc = accuracy_score(y_test, predictions)

    print(f"\nAccuracy: {round(acc * 100, 2)}%\n")
    print("Classification Report:\n")
    print(classification_report(y_test, predictions, zero_division=0))

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

    print("Model saved successfully!")
    print("model.pkl + vectorizer.pkl created")

if __name__ == "__main__":
    train()