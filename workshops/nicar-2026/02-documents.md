---
install:
  - natural-pdf[ai]
data_files:
  - "city.png"
---
# Documents

PDFs are images too. Text trapped in a scan, a photo of a posted notice, a 500-page FOIA dump — these are all "images with text in them."

## OCR with an LLM

Send a photo (of a document or otherwise) to an LLM. Get structured text back.

```show
data/flock-scan.png
```

```script
documents/llm-ocr.py
```

## Extract structured data from PDFs

The workflow that goes from PDF->LLM->structured data is a little more difficult than it should be, so I made a library called [Natural PDF](https://github.com/jsoma/natural-pdf) to help you do that.

In this example, we pull specific fields from a document page. Visual citations show exactly where on the page each answer came from — you can see what the model looked at.

```show
data/natural-pdf.png
```

```script
documents/extract-pdf.py
```

## Extract with a Pydantic schema

Same extraction, but with a Pydantic schema for precise field control. Same pattern as the image demos — define your fields, the model fills them in.

```script
documents/extract-pdf-pydantic.py
```

## Classify pages visually

If you're trying to put content in rough categories, there are models that can do it for free! While they aren't perfect about nuance, if you're trying to split up invoices and photographs and love letters they can do a pretty good job. *And they run on your own computer*

Got hundreds of pages from a FOIA? Classify every page as diagram, text, invoice, blank — no API key needed. Then filter to just the ones you want.

```script
documents/classify-pages.py
```
