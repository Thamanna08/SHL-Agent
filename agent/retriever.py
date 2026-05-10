import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading embedding model...")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Loading vector store...")

# Load embeddings
data = np.load("vector_store.npz")
embeddings = data["embeddings"]

print("Loading metadata...")

# Load metadata
with open("metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

print(f"Loaded {len(metadata)} assessments")


def search_assessments(query, top_k=5):

    try:
        # Convert query into embedding
        query_embedding = model.encode([query])

        # Calculate cosine similarity
        similarities = cosine_similarity(
            query_embedding,
            embeddings
        )[0]

        # Get top matches
        top_indices = similarities.argsort()[-top_k:][::-1]

        results = []

        for idx in top_indices:

            item = metadata[idx]

            results.append({
                "name": item["name"],
                "url": item["url"],
                "test_type": item["test_type"],
                "description": item["description"]
            })

        return results

    except Exception as e:

        print("Retriever Error:", e)

        return []


# Optional local test
if __name__ == "__main__":

    query = "Hiring Java developer with communication skills"

    results = search_assessments(query)

    print("\nTop Recommendations:\n")

    for i, item in enumerate(results, start=1):

        print(f"{i}. {item['name']}")
        print(f"Type: {item['test_type']}")
        print(f"URL: {item['url']}")
        print("-" * 50)