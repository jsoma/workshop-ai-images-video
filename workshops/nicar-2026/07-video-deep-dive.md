---
install:
  - scenedetect
  - opencv-python-headless
data_files:
  - "rDXubdQdJYs.mp4"
---
# Bonus: Video Deep Dive

The main video notebook showed you how to split video into frames and audio. This one goes deeper: automatic scene detection, and using Gemini to understand video directly — with timestamps, structured data, and zero decomposition.

## Scene detection with PySceneDetect

[PySceneDetect](https://www.scenedetect.com/) finds cuts in video automatically by flagging big visual changes. It's ancient technology, but super quick and (mostly) effective. Great for splitting long videos into meaningful chunks.

```script
video/scenes.py
```

Each scene gets a start time, end time, and a representative frame saved to disk. Now you can analyze scenes individually instead of processing the whole video.

## Send a video file to Gemini

Gemini can watch video. Upload a file, ask a question, get an answer. It's slower, it's more expensive, but it's *very easy to do*.

```script
video/gemini-upload.py
```

## Or just give it a YouTube URL

If the video is already on YouTube, it's even easier: Gemini accepts YouTube URLs directly.

```script
video/gemini-youtube.py
```

## Ask about a specific moment

"What's happening at 1:30?" Gemini can jump to timestamps. Useful when you already know *where* to look but need the AI to describe *what* it sees.

```script
video/gemini-timestamp.py
```

## Structured scene-by-scene breakdown

If you join Gemini with Pydantic, you can ask for exactly what you want: timestamps, descriptions, people visible, text on screen. It's the same structured output pattern from the image notebooks, just applied to video.

```script
video/gemini-structured.py
```
