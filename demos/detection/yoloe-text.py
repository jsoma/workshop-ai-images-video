# YOLOE open-vocab detection by text prompt — detect anything you describe
from pathlib import Path
from ultralytics import YOLOE

DATA = Path(__file__).parent.parent / "data"
CLASSES = ["car", "truck", "bus", "person", "traffic light", "building"]

model = YOLOE("yoloe-v8l-seg.pt")
model.set_classes(CLASSES)

results = model(str(DATA / "city.png"), conf=0.1, verbose=False)

for box in results[0].boxes:
    cls_name = results[0].names[int(box.cls)]
    conf = float(box.conf)
    print(f"{cls_name}: {conf:.3f}")
