---
install:
  - whisperx
  - nemo_toolkit[asr]
env_keys:
  - HF_TOKEN
data_files:
  - "rDXubdQdJYs.mp3"
---
# Audio

What can you do with audio? Turn it into text, then do text things. Split it by speaker.

## Transcribe

Once upon a time OpenAI released an *open model* named Whisper. It's actually great! There are newer models out there - like [Parakeet](https://parakeettdt.com/), which is super quick - but Whisper is very easy to use so everyone runs it.


```show
data/rDXubdQdJYs.mp3
```

There are different versions of the model - like tiny, base, large - but **turbo** is the best combination of speed and accuracy. Below we're using **WhisperX** which is a feature-packed tool built on top of Whisper.

```script
audio/whisperx.py
```

## Transcribe

Here's Parakeet! If you're on a mac, use [parakeet-mlx](https://github.com/senstella/parakeet-mlx). I'm specifically using the *most complicated possible version of Parakeet* because it's the best.

```script
audio/parakeet.py
```

## Transcribe and diarize (local)

Along with transcribing, WhisperX transcribes the audio *and identifies who said what*. Free, runs locally (on your own computer), your audio never leaves your machine.

**Setup:** Diarization requires a free Hugging Face token (`HF_TOKEN`) and accepting the model licenses at [pyannote/segmentation-3.0](https://huggingface.co/pyannote/segmentation-3.0) and [pyannote/speaker-diarization-community-1](https://huggingface.co/pyannote/speaker-diarization-community-1).

```script
audio/whisperx-diarize.py
```

"Speaker 1 said X at 0:42, Speaker 2 said Y at 1:15." Now you have a searchable, speaker-labeled transcript.

If you'd prefer to not write code (lol), try [MacWhisper](https://goodsnooze.gumroad.com/l/macwhisper), [Handy](https://handy.computer/), [VoiceInk](https://tryvoiceink.com/), [Buzz](https://buzzcaptions.com/).

## Structured transcription (cloud)

Sometimes your computer is slow, or you don't care about privacy or cost, and you just want something to get *done*. Here's the same audio, but Gemini returns structured data — each utterance as a typed object with speaker, timestamps, and text. Same Pydantic AI pattern as the image notebooks.

```script
audio/gemini-diarize.py
```

Cloud tradeoff: faster, structured output built-in, but your audio goes to Google. Most newsrooms will use both local and cloud depending on the sensitivity of the material.
