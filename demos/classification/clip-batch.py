# Batch zero-shot classification of a folder to CSV
from pathlib import Path
import pandas as pd
from transformers import pipeline

DATA = Path(__file__).parent.parent / "data"
MODEL_NAME = "openai/clip-vit-base-patch32"

CATEGORIES = [
    "a photo of a sedan",
    "a photo of an SUV",
    "a photo of a truck",
    "a photo of a van",
    "a photo of a motorcycle",
    "a photo of a bus",
]

classifier = pipeline("zero-shot-image-classification", model=MODEL_NAME)

rows = []
for path in sorted((DATA / "cars").glob("*.jpg")):
    results = classifier(str(path), candidate_labels=CATEGORIES)
    row = {"filename": path.name, "best_match": results[0]["label"], "confidence": results[0]["score"]}
    for r in results:
        row[r["label"]] = r["score"]
    rows.append(row)

df = pd.DataFrame(rows)
output = Path(__file__).parent / "outputs" / "classification_results.csv"
output.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output, index=False)
df
