# Full annotated video with boxes, traces, and counting line
import cv2
import supervision as sv
import ipywidgets as widgets
from IPython.display import display
from pathlib import Path
from ultralytics import YOLO

DATA = Path(__file__).parent.parent / "data"
VIDEO = DATA / "rDXubdQdJYs.mp4"
OUTPUT = Path(__file__).parent / "outputs"
OUTPUT.mkdir(exist_ok=True)

model = YOLO("yolo26n")
tracker = sv.ByteTrack()
cap = cv2.VideoCapture(str(VIDEO))
fps, w, h = cap.get(cv2.CAP_PROP_FPS), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

line_zone = sv.LineZone(start=sv.Point(0, h // 2), end=sv.Point(w, h // 2))
box_ann, label_ann = sv.BoxAnnotator(thickness=2), sv.LabelAnnotator(text_scale=0.5)
trace_ann, line_ann = sv.TraceAnnotator(thickness=2, trace_length=30), sv.LineZoneAnnotator(thickness=2)
writer = cv2.VideoWriter(str(OUTPUT / "annotated.mp4"), cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
image_widget = widgets.Image(format='jpeg')
display(image_widget)

frame_count = 0
while cap.isOpened() and frame_count < 300:
    ret, frame = cap.read()
    if not ret:
        break
    dets = sv.Detections.from_ultralytics(model(frame, verbose=False)[0])
    dets = tracker.update_with_detections(dets)
    line_zone.trigger(dets)
    labels = [f"#{tid} {model.names[int(cid)]}" for tid, cid in zip(dets.tracker_id, dets.class_id)] if dets.tracker_id is not None else []
    out = line_ann.annotate(trace_ann.annotate(label_ann.annotate(box_ann.annotate(frame.copy(), dets), dets, labels=labels), dets), line_zone)
    writer.write(out)
    _, buf = cv2.imencode('.jpg', out)
    image_widget.value = buf.tobytes()
    frame_count += 1

cap.release()
writer.release()
print(f"Annotated {frame_count} frames -> {OUTPUT / 'annotated.mp4'}")
