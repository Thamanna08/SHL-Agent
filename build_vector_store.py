import json
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

print("Loading SHL catalog...")

# Load assessment catalog
with open("shl_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

texts = []

print(f"Found {len(catalog)} assessments")

# Prepare text data
for item in catalog:

    text = f"""
    Assessment Name:
    {item.get('name', '')}

    Description:
    {item.get('description', '')}

    Test Type:
    {item.get('test_type', '')}
    """

    texts.append(text)

print("Creating TF-IDF vectors...")

# Create vectorizer
vectorizer = TfidfVectorizer()

# Generate vectors
vectors = vectorizer.fit_transform(texts)

print("Saving files...")

# Save vectorizer
joblib.dump(
    vectorizer,
    "vectorizer.pkl"
)

# Save vectors
joblib.dump(
    vectors,
    "vectors.pkl"
)

# Save metadata
with open("metadata.json", "w", encoding="utf-8") as f:

    json.dump(
        catalog,
        f,
        indent=2,
        ensure_ascii=False
    )

print("\n===================================")
print("Vector store created successfully")
print("Saved files:")
print("1. vectorizer.pkl")
print("2. vectors.pkl")
print("3. metadata.json")
print("===================================")