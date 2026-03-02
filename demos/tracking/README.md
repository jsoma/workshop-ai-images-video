# tracking

Multi-object tracking and line-crossing counts using YOLO11 + ByteTrack + supervision. All local, no API keys.

## Files

| File | What it does |
|------|-------------|
| `track.py` | YOLO + ByteTrack object tracking: unique tracker IDs and class counts |
| `count.py` | LineZone counting: count objects crossing a horizontal line |
| `annotated.py` | Write annotated video with boxes, traces, and counting line |
