---
install:
  - torchvision
  - ffmpeg-python
  - whisperx
  - "yt-dlp[default]"
env_keys:
  - HF_TOKEN
data_files:
  - "debate/*.jpg"
  - "debate.mp4"
  - "rDXubdQdJYs.mp3"
---
# The full pipeline

## Let's snag some content from a meeting

Transcription isn't perfect, and summaries aren't either. But if you plug one into the other... it's definitely tempting. Let's try it with a city council meeting.

```show
https://www.youtube.com/watch?v=buEGUxrz8ho
```

It's 2.5 hours long, which is *far too long* for us to sit through ourselves (right?). Instead, we'll see if we can get to do all the work.

```script{log=error}
recipes/meeting-minutes.py
```

We could have done this other ways: pass the entire thing to Gemini, use local models for the summarization/extraction, all kinds of options. But it's a good starting point!

> I also tried [to do the same thing with Google Opal](https://developers.google.com/opal), and it just *hallucinated every single aspect of the meeting*. I don't even think [the end result](https://opal.google/edit/1k6P7domgII6AZ6edCprG34Bn9v0dh25e) was working from a transcript, despite the fact that Google owns YouTube. Weird!

Trust but verify!

## Cost

Before you run a big batch: how much will it cost? Images × tokens × price = receipt. I would *not* trust the below, but it'll give you a general idea of what processing 500 images might look like, and the variation across different models.

```script
recipes/cost.py
```
