---
install:
  - ffmpeg-python
data_files:
  - "rDXubdQdJYs.mp4"
  - "debate/*.jpg"
---
# Video

What can you do with a video? It's images + audio + time. Decompose it, then use the tools you already have.

## Download

```script
video/download.py
```

## Extract frames

Decompose into one image per second. Now you have images — use the image tools.

```script
video/frames.py
```

## Extract audio

Extract the audio track. Now you have audio — use the audio tools.

```script
video/audio.py
```

This is the pipeline behind real investigations. Documented examined hundreds of TikTok videos in French and Wolof: download, extract audio, transcribe with Whisper. Público processed 7,616 TikTok health videos the same way, then used GPT-4o to extract verifiable claims from the transcripts. Video → audio → text → structured data.

## The wrong way

Ask Gemini a question about the video. Get a confident answer with no evidence.

```script
video/vibe-answer.py
```

You can't fact-check this. You can't show your editor the work. You can't catch errors. It's a vibe.

## The right way

Classify each frame with an LLM. Produce an auditable CSV — every row links to a frame you can check.

```script
video/decompose-classify.py
```

**Compare the two.** Same question, same video. One gives you a number. The other gives you a spreadsheet with an audit trail. Even if the vibe answer is right, you can't verify it. That's the point.
