import json
import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Opening SHL catalog...")

# Load catalog data
with open("shl_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

texts = []
metadata = []

print(f"Processing {len(catalog)} assessments...")

# Convert each assessment into searchable text
for item in catalog:

    text = f"""
    Assessment Name: {item.get('name', '')}

    Description:
    {item.get('description', '')}

    Test Type:
    {item.get('test_type', '')}

    URL:
    {item.get('url', '')}
    """

    texts.append(text)

    metadata.append({
        "name": item.get("name", ""),
        "url": item.get("url", ""),
        "description": item.get("description", ""),
        "test_type": item.get("test_type", "")
    })

print("Generating embeddings...")

# Create embeddings
embeddings = model.encode(
    texts,
    show_progress_bar=True
)

# Convert to numpy array
embeddings = np.array(embeddings)

print("Saving vector store...")

# Save embeddings
np.savez(
    "vector_store.npz",
    embeddings=embeddings
)

# Save metadata
with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print("\n===================================")
print("Vector store successfully created")
print("Saved files:")
print("1. vector_store.npz")
print("2. metadata.json")
print("===================================")