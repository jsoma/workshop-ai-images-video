# search

Semantic image search with CLIP + ChromaDB. Embed images into vectors, then search by text or by example image. Runs locally, no API keys.

## Files

| File | What it does |
|------|-------------|
| `index.py` | Embed a folder of images and store in a persistent ChromaDB index |
| `query.py` | Search the index by text query or by example image |
