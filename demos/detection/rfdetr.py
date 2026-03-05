# RF-DETR detection — highest accuracy COCO detector
# Requires extra install: uv pip install rfdetr
from pathlib import Path
from rfdetr import RFDETRBase
import supervision as sv

DATA = Path(__file__).parent.parent / "data"
COCO_CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
    "truck", "boat", "traffic light", "fire hydrant", "stop sign",
    "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
    "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag",
    "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
    "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
    "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana",
    "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza",
    "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table",
    "toilet", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone",
    "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock",
    "vase", "scissors", "teddy bear", "hair drier", "toothbrush",
]

model = RFDETRBase()
detections = model.predict(str(DATA / "city.jpg"), threshold=0.5)

for i in range(len(detections)):
    cls_name = COCO_CLASSES[int(detections.class_id[i])]
    conf = float(detections.confidence[i])
    print(f"{cls_name}: {conf:.3f}")
