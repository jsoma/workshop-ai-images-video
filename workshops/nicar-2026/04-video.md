---
install:
  - ffmpeg-python
  - yt-dlp
data_files:
  - "rDXubdQdJYs.mp4"
  - "debate/*.jpg"
---
# Video

You've got image tools and audio tools. Video is both — frames and a soundtrack — so you already have everything you need! Yes, you could send it to Gemini or another LLM (which we do at the end), but you can also just split it up and reuse what you've learned. Just because public meetings come as videos doesn't mean [you can't just treat them as audio](https://ryanserpi.co/projects/assembly/), and the same way you count or detect objects in images [you can do the same thing in videos](https://www.dw.com/en/betting-ads-swamp-brazilian-football-as-addiction-spikes/a-72941493).

## Download

[yt-dlp](https://github.com/yt-dlp/yt-dlp) is the best tool for downloading video content on the internet. It's gotten less effect at YouTube in the past 6 months or so, but it's still great for older videos and non-YT sites. Always try it out first!

If you'd prefer something that has a "normal" non-programming-y interface, [Stacher](https://stacher.io/) is great.

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

## Answering quetsions the slightly risky way

Just like you can ask AI about images, you can also ask about videos! ...at least, for some of the models. Gemini is probably the best: ask a question about the video, get a confident answer. It... may or may not be accurate.

```script
video/vibe-answer.py
```

> Gemini's raw API docs: [video](https://ai.google.dev/gemini-api/docs/video-understanding), [audio](https://ai.google.dev/gemini-api/docs/audio).

While it's *convenient*, using Gemini is slightly more difficult to fact-check. It's harder to show your editor the work, errors are hidden behind a wall of "just trust me!" It's a vibe, for better or worse. 


## The boring (auditable) way

Instead of getting Gemini to go whole-hog on the video analysis, we use our other skills: split into frames, classify each frame with an LLM. This allows you to produce an auditable CSV, where every row links to a frame you can check.

```script
video/decompose-classify.py
```

```show{cols=5 rows=3}
data/debate/*.jpg
```

Even if the vibe answer was right, sometimes verification is more important than ease of use.

## What's this for?

These are the pipelines behind real investigations!

- [Documented examined hundreds of TikTok videos](https://pulitzercenter.org/misinformation-tiktok-how-documented-examined-hundreds-videos-different-languages): download, extract audio, transcribe with Whisper.
- [Público processed 7,616 TikTok health videos](https://www.publico.pt/interactivos/tiktok-desinformacao-saude-pernas-compridas) the same way, then used GPT-4o to extract verifiable claims from the transcripts.
- DW used a [custom detection model](https://universe.roboflow.com/menegat/brasileirao-pitch-ads) to [count betting ads in Brazilian football](https://www.dw.com/en/betting-ads-swamp-brazilian-football-as-addiction-spikes/a-72941493) broadcasts


**Up next:** Putting it all together — full pipelines and checking your work.
