# YOLO26 fixed-vocab detection (80 COCO classes, fastest detector)
from pathlib import Path
from ultralytics import YOLO

DATA = Path(__file__).parent.parent / "data"

model = YOLO("yolo26n")
results = model(str(DATA / "city.png"), conf=0.25, verbose=False)

for box in results[0].boxes:
    cls_name = results[0].names[int(box.cls)]
    conf = float(box.conf)
    print(f"{cls_name}: {conf:.3f}")
