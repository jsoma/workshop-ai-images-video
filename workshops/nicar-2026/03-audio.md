---
install:
  - ffmpeg-python
  - "onnx-asr[cpu,hub]"
  - "torchaudio<2.9"
  - torchvision
  - whisperx

env_keys:
  - HF_TOKEN
data_files:
  - "rDXubdQdJYs.mp3"
---
# Audio

Images and documents gave you structured data. Audio is another way to get text — and once it's text, you already know what to do with it. This is how you can do story research like [Misinformation on TikTok: How 'Documented' Examined Hundreds of Videos in Different Languages](https://pulitzercenter.org/misinformation-tiktok-how-documented-examined-hundreds-videos-different-languages).

## Transcription with Whisper

Once upon a time OpenAI released an open model [named Whisper](https://github.com/openai/whisper/). It's great! Very very popular.

There are newer models out there — [parakeet-mlx](https://github.com/senstella/parakeet-mlx) is blazing fast on Macs — but Whisper is very easy to use so everyone (and I mean *everyone*) uses it.

When you use Whisper, you have to make some decisions:

* **Which packaging of Whisper:** Whisper is free to distribute, so a zillion tools are built on top of it. Below we're using **WhisperX** which is a feature-packed tool built on top of Whisper.
* **Which version of the model:** Like tiny, base, large... bigger is better, but slower! **Turbo** is the best combination of speed and accuracy. 

Let's practice on this Trump/Biden debate clip.

```show
https://www.youtube.com/watch?v=rDXubdQdJYs
```

I saved it as an mp3 to make life a little easier.

```show
data/rDXubdQdJYs.mp3
```

```script{log=error}
audio/transcribe-whisperx.py
```

## A faster option: Parakeet

NVIDIA's [Parakeet](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3) is a newer speech model that's significantly faster than Whisper — especially on Macs via [parakeet-mlx](https://github.com/senstella/parakeet-mlx). It also gives you cleaner sentence-level output without needing a separate alignment step.

Here we combine Parakeet for transcription with **pyannote** for speaker diarization — "who said what?"

**Setup:** Diarization requires a free Hugging Face token (`HF_TOKEN`) and accepting the model licenses at [pyannote/segmentation-3.0](https://huggingface.co/pyannote/segmentation-3.0) and [pyannote/speaker-diarization-community-1](https://huggingface.co/pyannote/speaker-diarization-community-1). It's kind of a pain to jump through the hoops but if you're vaguely technical it's definitely worth it.

> In the example below, we try to use Parakeet MLX (it's fast on my mac!) but if that fails we go for [onnx-asr](https://istupakov.github.io/onnx-asr/usage/), a flexible, portable tool that allows you to use different ASR (automatic speech recognition) models.

```script{log=error}
audio/transcribe-parakeet.py
```

## Transcription and speaker identification (WhisperX)

WhisperX can do the same thing — transcribe **and** separate speakers. It's slower than Parakeet but widely used and runs everywhere.

```script{log=error}
audio/whisperx-diarize.py
```

"Speaker 1 said X at 0:42, Speaker 2 said Y at 1:15." Now you have a searchable, speaker-labeled transcript!

If you'd prefer to not write code (lol), try [MacWhisper](https://goodsnooze.gumroad.com/l/macwhisper), [Handy](https://handy.computer/), [VoiceInk](https://tryvoiceink.com/), [Buzz](https://buzzcaptions.com/).

## Using the cloud

Sometimes your computer is slow, or you don't care about privacy or cost, and you just want something to get *done*. Here's the same audio, but using Gemini (Google's LLM). We make it send back structured data — each utterance gets a speaker, timestamps, text, *and* some sentiment to mix it up a bit. Same Pydantic AI pattern as the image notebooks!

```script
audio/gemini-diarize.py
```

Cloud tradeoff: faster, structured output built-in, but your audio goes to Google. Most newsrooms will use both local and cloud depending on the sensitivity of the material.

This is how real investigations work:

- [Documented examined hundreds of TikTok videos](https://pulitzercenter.org/misinformation-tiktok-how-documented-examined-hundreds-videos-different-languages) by extracting audio and transcribing with Whisper. 
- [Público did the same with 7,616 health TikToks](https://www.publico.pt/interactivos/tiktok-desinformacao-saude-pernas-compridas), then used an LLM to pull verifiable claims from the transcripts.
- [Hearst built Assembly](https://ryanserpi.co/projects/assembly/) to transcribe 13,000+ hours of government meetings with Whisper and surface keywords via alerts.
- [Chalkbeat uses LocalLens](https://www.niemanlab.org/2025/03/local-newsrooms-are-using-ai-to-listen-in-on-public-meetings/) to monitor 80 school districts across 30 states the same way.

**Up next:** Video is just images + audio + time. Decompose it, then use the tools you already have.
