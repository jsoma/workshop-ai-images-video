# Detect objects in a single video frame with YOLO
from pathlib import Path
from PIL import Image
import cv2
import supervision as sv
from ultralytics import YOLO

DATA = Path(__file__).parent.parent / "data"
VIDEO = DATA / "istockphoto-534232220-640_adpp_is.mp4"

model = YOLO("yolo26n")
cap = cv2.VideoCapture(str(VIDEO))
cap.set(cv2.CAP_PROP_POS_FRAMES, 50)
ret, frame = cap.read()
cap.release()

detections = sv.Detections.from_ultralytics(model(frame, verbose=False)[0])
labels = [f"{model.names[int(c)]} {conf:.2f}" for c, conf in zip(detections.class_id, detections.confidence)]
annotated = sv.BoxAnnotator().annotate(frame.copy(), detections)
annotated = sv.LabelAnnotator().annotate(annotated, detections, labels=labels)

print(f"Found {len(detections)} objects")
Image.fromarray(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
