# Demos

Runnable code snippets for "Analyzing Images & Video with AI" (NICAR 2026). One concept per file, 15-60 lines each.

## Setup

```bash
cd demos/
uv sync
```

Copy `.env.example` to `.env` (or export directly) with any API keys you need:

```
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
ANTHROPIC_API_KEY=sk-ant-...
HF_TOKEN=hf_...
```

## Folders

| Folder | What |
|--------|------|
| `vision-llm/` | Send images to LLMs, get structured data back |
| `detection/` | Object detection: YOLO11, YOLOE, Grounding DINO, Florence-2, RF-DETR |
| `classification/` | Zero-shot image classification with CLIP |
| `documents/` | Text extraction, page classification, structured data from PDFs (natural-pdf) |
| `audio/` | Transcription, diarization, word error rate |
| `video/` | Download, decompose, and analyze video |
| `tracking/` | Multi-object tracking and line-crossing counts |
| `search/` | Semantic image search with CLIP + ChromaDB |
| `recipes/` | End-to-end story recipes combining multiple tools |

## Data

`data/` is a symlink to the parent directory containing sample images, video, and audio files.
