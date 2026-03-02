# Zero-shot image classification with custom categories (no training needed)
from pathlib import Path
from transformers import pipeline

DATA = Path(__file__).parent.parent / "data"
MODEL_NAME = "openai/clip-vit-base-patch32"

CATEGORIES = [
    "a photo of a building",
    "a photo of a vehicle",
    "a photo of a person",
    "a photo of nature or landscape",
    "a photo of text or a document",
]

classifier = pipeline("zero-shot-image-classification", model=MODEL_NAME)
results = classifier(str(DATA / "city.png"), candidate_labels=CATEGORIES)

for r in results:
    print(f"  {r['score']:.3f}  {r['label']}")
