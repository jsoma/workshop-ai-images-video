# Track objects across video frames with YOLO + ByteTrack
from pathlib import Path
import cv2
import supervision as sv
import ipywidgets as widgets
from IPython.display import display
from ultralytics import YOLO

DATA = Path(__file__).parent.parent / "data"
VIDEO = DATA / "istockphoto-534232220-640_adpp_is.mp4"
MAX_FRAMES = 100

model = YOLO("yolo26n")
tracker = sv.ByteTrack()
smoother = sv.DetectionsSmoother()
box_ann = sv.BoxAnnotator()
label_ann = sv.LabelAnnotator()
trace_ann = sv.TraceAnnotator()

image_widget = widgets.Image(format='jpeg')
display(image_widget)

cap = cv2.VideoCapture(str(VIDEO))
frame_count = 0
while cap.isOpened() and frame_count < MAX_FRAMES:
    ret, frame = cap.read()
    if not ret:
        break
    detections = sv.Detections.from_ultralytics(model(frame, verbose=False)[0])
    detections = tracker.update_with_detections(detections)
    detections = smoother.update_with_detections(detections)
    labels = [f"#{tid} {model.names[int(c)]}" for tid, c in zip(detections.tracker_id, detections.class_id)] if detections.tracker_id is not None else []
    annotated = box_ann.annotate(frame.copy(), detections)
    annotated = trace_ann.annotate(annotated, detections)
    annotated = label_ann.annotate(annotated, detections, labels=labels)
    _, buf = cv2.imencode('.jpg', annotated)
    image_widget.value = buf.tobytes()
    frame_count += 1
cap.release()

print(f"Tracked {frame_count} frames")
