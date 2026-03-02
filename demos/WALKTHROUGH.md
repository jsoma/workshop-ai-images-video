# Workshop Walkthrough

A path through the demos for "Analyzing Images & Video with AI." Each bullet is a runnable script. Run them in order — each one builds on the idea before it.

## The big idea

You already know what to do with text: summarize it, answer questions about it, extract data from it. Images, audio, and video are just ways of **getting to text and structured data.**

---

## Core path (90 minutes)

Everything below is the core path. The rest of the file is the full index.

**Images** — from prose to structured data to spreadsheet

1. `vision-llm/structured.py` — Send an image to an LLM, get structured data back (not prose — fields you can sort, filter, verify). This is the pattern for everything else.
2. `vision-llm/batch.py` — Same thing, whole folder. Out comes a CSV. Open it, spot-check a few rows against the source images.
3. `vision-llm/providers.py` — Same task, swap the provider string. OpenAI, Google, Anthropic, Ollama — one line change.

**Documents** — PDFs are images too (natural-pdf)

4. `documents/llm-ocr.py` — Text trapped in an image (signs, documents, handwriting). Send it to an LLM, get structured text back.
5. `documents/classify-pages.py` — Got 500 pages from a FOIA? Classify every page visually as diagram, text, invoice, blank. Uses CLIP, no API key. Filter to just the pages you want.
6. `documents/extract.py` — Extract structured data from a page with an LLM. Visual citations show exactly where on the page each answer came from.
7. `documents/extract-pydantic.py` — Same extraction, but with a Pydantic schema for precise field control. Same pattern as the image demos.

**Audio** — turn it into text, then do text things

8. `audio/whisperx-diarize.py` — Transcribe audio AND identify who said what. Free, runs locally.
9. `audio/gemini.py` — Same audio, sent to Gemini instead. Cloud, can also summarize and reason about the content. Different tradeoffs: local/free/private vs. cloud/fast/flexible.

**Video** — decompose, then use the tools you already have

10. `video/download.py` — Download a video from a URL with yt-dlp.
11. `video/frames.py` — Decompose into one image per second. Now you have images — use the image tools.
12. `video/audio.py` — Extract the audio track. Now you have audio — use the audio tools.

This is the pipeline behind real investigations. Documented examined hundreds of TikTok videos in French and Wolof: download → extract audio → transcribe with Whisper. Público did the same with 7,616 TikTok health videos, then used GPT-4o to extract verifiable claims from the transcripts. Video → audio → text → structured data.

**Video** — the audit trail moment

13. `video/vibe-answer.py` — Ask Gemini "who got more screen time?" Confident answer, no evidence.
14. `video/decompose-classify.py` — Classify each frame → CSV. Every row links to a frame you can check.

Compare scripts 13 and 14. One gives you a number. The other gives you a spreadsheet with an audit trail. Even if the vibe answer is right, you can't verify it. **That's the point.**

**Recipe** — the full pipeline

15. `recipes/screen-time.py` — Frames → classify → per-subject screen time with percentages. The deliverable you'd bring to an editor.
16. `recipes/cost.py` — Before you run a big batch: how much will it cost? Images x tokens x price = receipt.

---

## All demos

Everything below is the full index — use it as reference, for self-guided exploration after the workshop, or if you finish the core path early.

## Images

What can you do with an image? Describe it, answer questions about it, extract items from it.

- `vision-llm/basic.py` — Send an image to an LLM, get a description back. The simplest possible version.
- `vision-llm/structured.py` — Same thing, but get structured data (a Pydantic object) instead of prose. This is the key upgrade: you get fields you can filter, sort, and verify.
- `vision-llm/batch.py` — Do it to a whole folder of images. Out comes a CSV.
- `detection/yolo11.py` — Find and locate objects in an image (bounding boxes, counts). Runs locally, no API key.
- `classification/clip.py` — Classify an image into your own categories, no training. Also local.

**Where you are now:** You can take a pile of images and turn it into a spreadsheet. Every row is auditable — you can check the image that produced it.

---

## Documents

PDFs are images too. Extract text, classify pages, pull structured data — with visual citations showing where each answer came from.

- `documents/llm-ocr.py` — Send a photo of a sign/document to an LLM, get structured text back (cloud).
- `documents/florence2.py` — Local OCR with bounding boxes showing where text appears in images.
- `documents/doc-to-md.py` — Convert scanned documents to markdown (local, PDFs/images/Office docs).
- `documents/classify-pages.py` — Classify pages of a PDF visually with CLIP (diagram, text, invoice, etc.). Filter and save subsets.
- `documents/extract.py` — Extract structured data from a PDF page with an LLM. Visual citations show where each answer came from.
- `documents/extract-pydantic.py` — Same extraction using a Pydantic schema for precise field control.

**Where you are now:** You can triage a FOIA dump of hundreds of pages — classify them, extract the data from the ones that matter, and show exactly where on the page each answer came from.

---

## Audio

What can you do with audio? Turn it into text, then do text things. Split it by speaker.

- `audio/whisper.py` — Transcribe audio to text with timestamps. Now it's text — you can search it, summarize it, extract from it.
- `audio/whisperx-diarize.py` — Transcribe AND identify who said what. "Speaker 1 said X at 0:42, Speaker 2 said Y at 1:15."
- `audio/wer.py` — How accurate is the transcription? Compare model sizes, see where they fail. This is verification.

**Where you are now:** You can turn audio into a searchable, speaker-labeled transcript, and you know how to check if it's accurate.

---

## Video

What can you do with a video? It's images + audio + time. Decompose it, then use the tools you already have.

### The wrong way

- `video/vibe-answer.py` — Ask Gemini "who got more screen time?" It gives a confident answer with no evidence. You can't fact-check it, you can't show your editor the work, you can't catch errors.

### The right way

- `video/frames.py` — Decompose the video into frames (one image per second).
- `video/audio.py` — Extract the audio track.
- `video/decompose-classify.py` — Classify each frame with an LLM → auditable CSV. Every row is a frame you can check.

Now you have images (frames) and audio (transcript) — the same tools from above apply.

### The audit trail moment

Compare `vibe-answer.py` and `decompose-classify.py`. Same question, same video. One gives you a number. The other gives you a spreadsheet where every row links to a frame. Even if the vibe answer is correct, you can't verify it. That's the point.

---

## Combining everything

Full pipelines that chain the pieces together.

- `recipes/screen-time.py` — Video → frames → classify each frame → per-subject screen time summary with percentages.
- `recipes/speaker-time.py` — Audio → transcribe → diarize → per-speaker time breakdown.
- `recipes/keyword-clips.py` — Find keyword mentions in audio, extract short video clips around each one.
- `recipes/cost.py` — Estimate what a batch job costs before you run it.

---

## Search

When you have hundreds or thousands of images and need to find specific ones.

- `search/index.py` — Embed a folder of images into a searchable index.
- `search/query.py` — Search by typing what you're looking for ("person holding a sign") or by giving an example image.

---

## Tracking

Count things moving through a video over time.

- `tracking/track.py` — Detect and track objects across frames (each object gets a unique ID).
- `tracking/count.py` — Count objects crossing a line (e.g., cars through an intersection).
- `tracking/annotated.py` — Write an annotated video with boxes, trails, and counts overlaid.

---

## Bonus / deeper dives

Things you can explore after the workshop or if you finish early.

- `vision-llm/providers.py` — Same structured task, swap between OpenAI / Google / Anthropic with one line.
- `vision-llm/raw-openai.py` — What the raw SDK looks like without Pydantic AI (base64, JSON schema). Appreciate the abstraction.
- `detection/yoloe-text.py` — Open-vocabulary detection: describe what to find in plain English.
- `detection/gdino.py` — Grounding DINO: most accurate open-vocab detector.
- `detection/florence2.py` — One model that does detection + captioning + OCR.
- `classification/clip-batch.py` — Classify every image in a folder to CSV.
- `audio/whisperx.py` — Word-level alignment (without diarization).
- `audio/gemini.py` — Send audio to Gemini for cloud transcription/analysis.
- `video/scenes.py` — Scene detection: find where cuts happen in a video.
- `video/gemini-upload.py` / `video/gemini-youtube.py` — Send video directly to Gemini.
- `recipes/ad-counting.py` — Sample broadcast frames, classify ad vs. content.
- `recipes/batch-classify.py` — Classify a folder of images with structured output.
- `recipes/photo-search.py` — Embed photos, store in ChromaDB, text search.
- `recipes/redact-faces.py` — Detect and blur faces before uploading to the cloud.
