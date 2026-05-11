import json
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

print("Loading catalog...")

with open("shl_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

texts = []

for item in catalog:

    text = f"""
    {item.get('name', '')}
    {item.get('description', '')}
    {item.get('test_type', '')}
    """

    texts.append(text)

print("Creating TF-IDF vectors...")

vectorizer = TfidfVectorizer()

vectors = vectorizer.fit_transform(texts)

joblib.dump(vectorizer, "vectorizer.pkl")
joblib.dump(vectors, "vectors.pkl")

with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, indent=2)

print("Vector store created successfully")