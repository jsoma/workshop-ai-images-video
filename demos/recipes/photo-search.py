# Embed a folder of photos with CLIP → store in ChromaDB → text search.
# Type "red car" and it finds them. No manual tagging.
from pathlib import Path

import chromadb
from PIL import Image
from sentence_transformers import SentenceTransformer

DATA = Path(__file__).parent.parent / "data"

FOLDER = DATA / "cars"
QUERY = "red car"

# --- Step 1: Load CLIP model ---
model = SentenceTransformer("clip-ViT-B-32")

# --- Step 2: Embed images and store in ChromaDB ---
images = sorted(p for p in FOLDER.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"})
client = chromadb.Client()
collection = client.get_or_create_collection("photos", metadata={"hnsw:space": "cosine"})

ids, embeddings, metadatas = [], [], []
for img_path in images:
    emb = model.encode([Image.open(img_path).convert("RGB")])[0]
    ids.append(img_path.name)
    embeddings.append(emb.tolist())
    metadatas.append({"filename": img_path.name, "path": str(img_path)})

collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)
print(f"Indexed {len(ids)} images")

# --- Step 3: Search by text query ---
query_emb = model.encode([QUERY]).tolist()
results = collection.query(query_embeddings=query_emb, n_results=5)

print(f"\nTop results for '{QUERY}':")
for rank, (id, dist) in enumerate(zip(results["ids"][0], results["distances"][0]), 1):
    print(f"  {rank}. [{1 - dist:.4f}] {id}")
