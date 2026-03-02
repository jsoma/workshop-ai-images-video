# Build a CLIP + ChromaDB image search index
import chromadb
from pathlib import Path
from PIL import Image
from sentence_transformers import SentenceTransformer

DATA = Path(__file__).parent.parent / "data"
FOLDER = DATA / "cars"
DB_PATH = Path(__file__).parent / "outputs" / "chroma_db"
COLLECTION = "images"

model = SentenceTransformer("clip-ViT-B-32")

image_paths = sorted(p for p in FOLDER.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"} and p.is_file())
images = [Image.open(p).convert("RGB") for p in image_paths]
embeddings = model.encode(images, show_progress_bar=True, batch_size=32)

DB_PATH.mkdir(parents=True, exist_ok=True)
client = chromadb.PersistentClient(path=str(DB_PATH))
collection = client.get_or_create_collection(name=COLLECTION, metadata={"hnsw:space": "cosine"})
collection.add(
    ids=[p.name for p in image_paths],
    embeddings=[e.tolist() for e in embeddings],
    metadatas=[{"path": str(p.resolve()), "file": p.name} for p in image_paths],
)

print(f"Indexed {len(image_paths)} images into '{COLLECTION}' at {DB_PATH}")
