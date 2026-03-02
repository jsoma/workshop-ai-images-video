# Detect and blur faces in an image before cloud upload (YOLO + OpenCV).
from pathlib import Path

import cv2
from ultralytics import YOLO

DATA = Path(__file__).parent.parent / "data"

IMAGE = DATA / "city.png"
BLUR_STRENGTH = 99
CONFIDENCE = 0.25

# --- Detect faces ---
model = YOLO("yolo11n-face.pt")
img = cv2.imread(str(IMAGE))
results = model(img, conf=CONFIDENCE, verbose=False)

# --- Blur each face ---
face_count = 0
for result in results:
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        pad_w, pad_h = int((x2 - x1) * 0.1), int((y2 - y1) * 0.1)
        x1, y1 = max(0, x1 - pad_w), max(0, y1 - pad_h)
        x2, y2 = min(img.shape[1], x2 + pad_w), min(img.shape[0], y2 + pad_h)
        roi = img[y1:y2, x1:x2]
        img[y1:y2, x1:x2] = cv2.GaussianBlur(roi, (BLUR_STRENGTH, BLUR_STRENGTH), 30)
        face_count += 1

# --- Save ---
out_path = IMAGE.parent / f"{IMAGE.stem}_redacted{IMAGE.suffix}"
cv2.imwrite(str(out_path), img)
print(f"Blurred {face_count} face(s) → {out_path.name}")
