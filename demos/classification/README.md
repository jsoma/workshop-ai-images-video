# classification

Zero-shot image classification with CLIP. Define your own categories (no training needed), score each image against every label, highest score wins. Runs locally, no API keys.

## Files

| File | What it does |
|------|-------------|
| `clip.py` | Classify a single image into custom categories |
| `clip-batch.py` | Classify every image in a folder to CSV |

Uses `openai/clip-vit-base-patch32` via the Hugging Face `transformers` pipeline.
