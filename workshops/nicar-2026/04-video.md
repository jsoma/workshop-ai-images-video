---
install:
  - ffmpeg-python
  - yt-dlp
data_files:
  - "rDXubdQdJYs.mp4"
  - "debate/*.jpg"
---
# Video

You've got image tools and audio tools. Video is both — frames and a soundtrack — so you already have everything you need! Yes, you could send it to Gemini or another LLM (which we do at the end), but you can also just decompose it and reuse what you've learned.

## Download

[yt-dlp](https://github.com/yt-dlp/yt-dlp) is the best tool for downloading video content on the internet. It's gotten less effect at YouTube in the past 6 months or so, but it's still great for older videos and non-YT sites. Always try it out first!

```script
video/download.py
```

## Extract frames

Since you know how to analyze images, why not just separate out the frames in a video? Below we extract one frame every two seconds. Now you have images: use the image tools!

```script
video/frames.py
```

## Extract audio

Same thing for the audio. Now you have audio: use the audio tools!

```script
video/audio.py
```

## The slightly risky way

Ask Gemini a question about the video. Get a confident answer... that regrettably has little to no evidence.

```script
video/vibe-answer.py
```

While it's *convenient*, using Gemini is slightly more difficult to fact-check. It's harder to show your editor the work. Errors are a little more hidden. It's a vibe, for better or worse. (Gemini's raw API docs: [video](https://ai.google.dev/gemini-api/docs/video-understanding), [audio](https://ai.google.dev/gemini-api/docs/audio).)

## The boring (auditable) way

Instead of getting Gemini to go whole-hog on the video analysis, we use our other skills: split into frames, classify each frame with an LLM. Produce an auditable CSV, where every row links to a frame you can check.

```script
video/decompose-classify.py
```

Even if the vibe answer was right, sometimes verification is more important than speed.

## What's this for?

These are the pipelines behind real investigations.

- [Documented examined hundreds of TikTok videos](https://pulitzercenter.org/misinformation-tiktok-how-documented-examined-hundreds-videos-different-languages): download, extract audio, transcribe with Whisper.
- [Público processed 7,616 TikTok health videos](https://www.publico.pt/interactivos/tiktok-desinformacao-saude-pernas-compridas) the same way, then used GPT-4o to extract verifiable claims from the transcripts.
- DW used a [custom detection model](https://universe.roboflow.com/menegat/brasileirao-pitch-ads) to [count betting ads in Brazilian football](https://www.dw.com/en/betting-ads-swamp-brazilian-football-as-addiction-spikes/a-72941493) broadcasts


**Up next:** Putting it all together — full pipelines and checking your work.
