# Grounding DINO open-vocab detection — most accurate text-prompted detector
from pathlib import Path
from PIL import Image
from transformers import pipeline

DATA = Path(__file__).parent.parent / "data"
MODEL_ID = "IDEA-Research/grounding-dino-base"
LABELS = ["car", "building", "tree", "person", "traffic light"]

detector = pipeline("zero-shot-object-detection", model=MODEL_ID)
image = Image.open(DATA / "city.png").convert("RGB")

results = detector(image, candidate_labels=LABELS, threshold=0.3)

for r in results:
    box = r["box"]
    print(f"{r['label']}: {r['score']:.3f}  ({box['xmin']},{box['ymin']},{box['xmax']},{box['ymax']})")
