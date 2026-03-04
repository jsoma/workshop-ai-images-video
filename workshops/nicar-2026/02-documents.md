---
install:
  - natural-pdf[ai]
data_files:
  - "city.png"
  - "flock-scan.png"
  - "letter.png"
  - "letter.pdf"
  - "natural-pdf.png"
---
# Documents

You just extracted structured data from photos. PDFs are the same problem — images with text trapped in them. A scan, a posted notice, a 500-page FOIA dump.

## OCR with an LLM

OCR stands for **Optical Character Recognition**, which just means "get the text out of an image." Send a photo (of a document or otherwise) to an LLM. Get structured text back.

Let's try with a PNG of a letter.

```show
data/flock-scan.png
```

It's not an ideal scan - off angles, a little fuzzy, weird lines going through it. How will it do?

```script
documents/llm-ocr.py
```

Wonderful!

## OCR a PDF

But as a journalist, you almost never need to recognize text in images - it's almost always in PDFs. The workflow that goes from PDF->LLM->OCR is a little more difficult than it should be, so I made a library called [Natural PDF](https://github.com/jsoma/natural-pdf) to help you do that.

```show
data/letter.png
```

While you [can use an LLM for OCR with Natural PDF](https://jsoma.github.io/natural-pdf-workshop/natural-pdf/02-ocr-and-ai-magic-ANSWERS.html) you don't need to! Using one fo the built-in OCR engines usually works pretty well.

```script{log=error}
documents/pdf-ocr.py
```

## Extract structured data from PDFs

[Natural PDF](https://github.com/jsoma/natural-pdf) can also help you extract **structured data** from PDFs. In this example, we pull specific fields from a document page. Visual citations show exactly where on the page each answer came from — you can see what the model looked at.

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

```script{log=error}
documents/classify-pages.py
```

**Up next:** Audio. Same idea — turn it into text, then do text things.
