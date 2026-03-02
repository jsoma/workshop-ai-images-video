# documents

Extract text, classify pages, and pull structured data from PDFs and images. Three approaches: LLM-based (cloud), Florence-2 (local), and natural-pdf (local classification, cloud extraction).

## Files

| File | What it does |
|------|-------------|
| `llm-ocr.py` | Send a photo of a sign/document to an LLM for structured text extraction (API) |
| `florence2.py` | Florence-2 OCR with bounding boxes (local, scene text in photos) |
| `doc-to-md.py` | Docling document-to-markdown (local, PDFs/images/Office docs) |
| `classify-pages.py` | Classify pages of a PDF visually with CLIP (diagram, text, invoice, etc.) |
| `extract.py` | Extract structured data from a PDF page with an LLM, with visual citations |
| `extract-pydantic.py` | Same extraction using a Pydantic schema for precise field control |

## Comparison

| Tool | Runs | Best for |
|------|------|----------|
| LLM OCR | Cloud (API key) | Quick reads from a few photos, handwriting |
| Florence-2 | Local | Finding where text appears in images (bounding boxes) |
| Docling | Local | Documents to markdown (scans, PDFs, forms) |
| natural-pdf | Local + Cloud | Classify pages visually (local), extract structured data (cloud), visual citations |
