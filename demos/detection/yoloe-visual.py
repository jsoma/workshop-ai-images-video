# YOLOE visual prompting — find objects that look like a reference crop
from pathlib import Path
from PIL import Image
from ultralytics import YOLO, YOLOE

DATA = Path(__file__).parent.parent / "data"
SOURCE_IMAGE = DATA / "city.png"
SEARCH_IMAGE = DATA / "city.png"

# Auto-crop a reference object from the source image using YOLO
detector = YOLO("yolo26n")
detections = detector(str(SOURCE_IMAGE), verbose=False)
box = detections[0].boxes[0]
x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
ref_crop = Image.open(SOURCE_IMAGE).crop((x1, y1, x2, y2)).convert("RGB")

# Use YOLOE visual prompting to find similar objects
model = YOLOE("yoloe-v8l-seg.pt")
results = model.predict(
    str(SEARCH_IMAGE),
    visual_prompts={"bboxes": None, "images": [ref_crop]},
    verbose=False,
)

for box in results[0].boxes:
    conf = float(box.conf)
    x1, y1, x2, y2 = box.xyxy[0].tolist()
    print(f"match: conf={conf:.3f} at ({x1:.0f},{y1:.0f},{x2:.0f},{y2:.0f})")
