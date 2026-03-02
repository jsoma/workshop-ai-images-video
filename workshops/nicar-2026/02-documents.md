---
install:
  - natural-pdf[ai]
data_files:
  - "city.png"
---
# Documents

PDFs are images too. Text trapped in a scan, a photo of a posted notice, a 500-page FOIA dump — these are all "images with text in them."

## OCR with an LLM

Send a photo of a document to an LLM. Get structured text back.

```script
documents/llm-ocr.py
```

## Classify pages visually

Got hundreds of pages from a FOIA? Classify every page as diagram, text, invoice, blank — using CLIP, no API key needed. Then filter to just the ones you want.

```script
documents/classify-pages.py
```

## Extract structured data

Pull specific fields from a document page. Visual citations show exactly where on the page each answer came from — you can see what the model looked at.

```script
documents/extract.py
```

## Extract with a Pydantic schema

Same extraction, but with a Pydantic schema for precise field control. Same pattern as the image demos — define your fields, the model fills them in.

```script
documents/extract-pydantic.py
```
