# Search the CLIP+ChromaDB index by text or image
import chromadb
from pathlib import Path
from PIL import Image
from sentence_transformers import SentenceTransformer

DB_PATH = Path(__file__).parent / "outputs" / "chroma_db"
QUERY = "red car"
TOP = 5

model = SentenceTransformer("clip-ViT-B-32")
client = chromadb.PersistentClient(path=str(DB_PATH))
collection = client.get_collection("images")

query_embedding = model.encode([QUERY]).tolist()
results = collection.query(query_embeddings=query_embedding, n_results=TOP)

for rank, (id, dist) in enumerate(zip(results["ids"][0], results["distances"][0]), 1):
    print(f"  {rank}. {id}  (similarity: {1 - dist:.4f})")
