# detection

Object detection: find and locate things in images. Each detected object gets a bounding box, class label, and confidence score. All models run locally, no API keys needed.

## Files

| File | What it does |
|------|-------------|
| `yolo11.py` | YOLO11 fixed-vocab detection (80 COCO classes, fastest) |
| `yoloe-text.py` | YOLOE open-vocab detection by text prompt |
| `yoloe-visual.py` | YOLOE visual prompting (find objects similar to a reference crop) |
| `gdino.py` | Grounding DINO open-vocab detection (most accurate text-prompted) |
| `florence2.py` | Florence-2 detection + captioning (one model, many tasks) |
| `rfdetr.py` | RF-DETR detection (highest COCO accuracy, requires `uv pip install rfdetr`) |

## Comparison

| Model | Vocab | Speed | Notes |
|-------|-------|-------|-------|
| YOLO11 | Fixed (80 COCO classes) | Fastest | Cars, people, common objects |
| YOLOE | Open (text or image prompt) | Fast | Describe what to find in plain text |
| Grounding DINO | Open (text prompt) | Slow | Most accurate open-vocab detector |
| Florence-2 | Open (text + caption + OCR) | Medium | Multi-task: detection, captioning, OCR |
| RF-DETR | Fixed (COCO) | Fast | Highest accuracy on COCO benchmark |
