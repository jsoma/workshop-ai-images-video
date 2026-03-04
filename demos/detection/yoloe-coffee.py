# YOLOE open-vocab detection — find anything you can describe
from pathlib import Path
from ultralytics import YOLOE

DATA = Path(__file__).parent.parent / "data"
CLASSES = ["coffee cup", "peanut butter toast", "spiral notebook", "blue pencil", "ballpoint pen", "dog"]

model = YOLOE("yoloe-26l-seg.pt")
model.set_classes(CLASSES)

results = model(str(DATA / "coffee.jpg"), conf=0.1, verbose=False)

for box in results[0].boxes:
    cls_name = results[0].names[int(box.cls)]
    conf = float(box.conf)
    print(f"{cls_name}: {conf:.3f}")

# --- cell ---
# Instead of just seeing what's there - and getting confidence scores - let's see where they're at!
import cv2
from PIL import Image as PILImage
annotated = results[0].plot(masks=False)
PILImage.fromarray(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
