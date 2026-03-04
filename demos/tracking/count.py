# LineZone counting -- count objects crossing a horizontal line
import cv2
import supervision as sv
from pathlib import Path
from ultralytics import YOLO

DATA = Path(__file__).parent.parent / "data"
VIDEO = DATA / "rDXubdQdJYs.mp4"
MAX_FRAMES = 300

model = YOLO("yolo26n")
tracker = sv.ByteTrack()

cap = cv2.VideoCapture(str(VIDEO))
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

y_pos = h // 2
line_zone = sv.LineZone(start=sv.Point(0, y_pos), end=sv.Point(w, y_pos))

frame_count = 0
while cap.isOpened() and frame_count < MAX_FRAMES:
    ret, frame = cap.read()
    if not ret:
        break
    detections = sv.Detections.from_ultralytics(model(frame, verbose=False)[0])
    detections = tracker.update_with_detections(detections)
    line_zone.trigger(detections)
    frame_count += 1

cap.release()

print(f"Frames processed: {frame_count}")
print(f"Objects crossing IN:  {line_zone.in_count}")
print(f"Objects crossing OUT: {line_zone.out_count}")
print(f"Total crossings:      {line_zone.in_count + line_zone.out_count}")
