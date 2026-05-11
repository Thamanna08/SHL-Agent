import json
import joblib
from sklearn.metrics.pairwise import cosine_similarity

print("Loading vectorizer...")

vectorizer = joblib.load("vectorizer.pkl")

print("Loading vectors...")

vectors = joblib.load("vectors.pkl")

print("Loading metadata...")

with open("metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)


def search_assessments(query, top_k=5):

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(
        query_vector,
        vectors
    )[0]

    top_indices = similarities.argsort()[-top_k:][::-1]

    results = []

    for idx in top_indices:

        item = metadata[idx]

        results.append({
            "name": item["name"],
            "url": item["url"],
            "description": item["description"],
            "test_type": item["test_type"]
        })

    return results