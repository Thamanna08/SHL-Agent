import json
import joblib
from sklearn.metrics.pairwise import cosine_similarity

print("Loading vectorizer...")

# Load TF-IDF vectorizer
vectorizer = joblib.load("vectorizer.pkl")

print("Loading vectors...")

# Load saved vectors
vectors = joblib.load("vectors.pkl")

print("Loading metadata...")

# Load assessment metadata
with open("metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)


def search_assessments(query, top_k=5):

    try:

        # Convert query into TF-IDF vector
        query_vector = vectorizer.transform([query])

        # Calculate similarity
        similarities = cosine_similarity(
            query_vector,
            vectors
        )[0]

        # Get top matching indices
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

    except Exception as e:

        print("Retriever Error:", e)

        return []


#