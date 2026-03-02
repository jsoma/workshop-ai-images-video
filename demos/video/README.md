# video

Download, decompose, and analyze video. The core pattern is decompose into frames/scenes/audio, analyze each piece, reassemble into structured data.

## Files

| File | What it does |
|------|-------------|
| `download.py` | Download video from a URL with yt-dlp |
| `frames.py` | Extract frames at 1 fps with ffmpeg-python |
| `scenes.py` | Detect scene boundaries, extract mid-scene frames (PySceneDetect) |
| `audio.py` | Extract audio track from video with ffmpeg-python |
| `gemini-upload.py` | Upload a video file to Gemini and ask a question |
| `gemini-youtube.py` | Send a YouTube URL directly to Gemini (no download) |
| `vibe-answer.py` | Ask Gemini a question about a video (no evidence, black box) |
| `decompose-classify.py` | Classify each frame with Pydantic AI, produce an auditable CSV |

`vibe-answer.py` and `decompose-classify.py` are a pair: same question, opposite methodology. The vibe answer gives a confident response with no evidence. The decompose-classify approach produces a CSV you can audit row by row.
