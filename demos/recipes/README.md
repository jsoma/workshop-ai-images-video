# recipes

End-to-end story pipelines combining multiple tools. Each recipe takes raw media in and produces a journalistic artifact (CSV, clips, index) out.

## Files

| File | What it does |
|------|-------------|
| `screen-time.py` | Classify debate frames, produce per-subject screen time summary |
| `speaker-time.py` | Transcribe + diarize audio, produce per-speaker time breakdown |
| `keyword-clips.py` | Find keyword mentions in audio, extract short video clips |
| `ad-counting.py` | Sample broadcast frames, classify ad vs content, time breakdown |
| `batch-classify.py` | Classify a folder of images with structured output to CSV |
| `photo-search.py` | Embed photos with CLIP, store in ChromaDB, text search |
| `redact-faces.py` | Detect and blur faces before cloud upload (YOLO + OpenCV) |
| `cost.py` | Estimate API cost for a batch of images (no API key needed) |
