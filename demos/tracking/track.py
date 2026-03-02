# YOLO + ByteTrack object tracking -- print unique tracker IDs and class counts
import cv2
import supervision as sv
from pathlib import Path
from ultralytics import YOLO

DATA = Path(__file__).parent.parent / "data"
VIDEO = DATA / "rDXubdQdJYs.mp4"
MAX_FRAMES = 100

model = YOLO("yolo11n.pt")
tracker = sv.ByteTrack()
cap = cv2.VideoCapture(str(VIDEO))

all_class_tracker = {}
frame_count = 0

while cap.isOpened() and frame_count < MAX_FRAMES:
    ret, frame = cap.read()
    if not ret:
        break
    detections = sv.Detections.from_ultralytics(model(frame, verbose=False)[0])
    detections = tracker.update_with_detections(detections)
    if detections.tracker_id is not None:
        for tid, cid in zip(detections.tracker_id, detections.class_id):
            cls_name = model.names[int(cid)]
            all_class_tracker.setdefault(cls_name, set()).add(tid)
    frame_count += 1

cap.release()

total = sum(len(tids) for tids in all_class_tracker.values())
print(f"Frames processed: {frame_count}")
print(f"Unique objects: {total}")
for cls, tids in sorted(all_class_tracker.items(), key=lambda x: -len(x[1])):
    print(f"  {cls}: {len(tids)}")
