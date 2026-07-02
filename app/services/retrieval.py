
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[1]
CATALOG_PATH = BASE_DIR / "data" / "catalog.json"

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = []
for item in catalog:
    text = f"""
    {item.get('name', '')}
    {item.get('description', '')}
    {' '.join(item.get('job_levels', []))}
    {' '.join(item.get('keys', []))}
    """
    texts.append(text)

embeddings = model.encode(texts, convert_to_numpy=True)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings).astype("float32"))

def retrieve(query: str, top_k: int = 5):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(np.array(query_embedding).astype("float32"), top_k)

    results = []
    for idx in indices[0]:
        item = catalog[idx]
        results.append(item)

    return results
