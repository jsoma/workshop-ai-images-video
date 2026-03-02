# Audio

What can you do with audio? Turn it into text, then do text things. Split it by speaker.

## Transcribe and diarize (local)

WhisperX transcribes the audio and identifies who said what. Free, runs locally, your audio never leaves your machine.

**Setup:** Diarization requires a free Hugging Face token (`HF_TOKEN`) and accepting the model licenses at [pyannote/segmentation-3.0](https://huggingface.co/pyannote/segmentation-3.0) and [pyannote/speaker-diarization-community-1](https://huggingface.co/pyannote/speaker-diarization-community-1).

```script
audio/whisperx-diarize.py
```

"Speaker 1 said X at 0:42, Speaker 2 said Y at 1:15." Now you have a searchable, speaker-labeled transcript.

## Structured transcription (cloud)

Same audio, but Gemini returns structured data — each utterance as a typed object with speaker, timestamps, and text. Same Pydantic AI pattern as the image notebooks.

```script
audio/gemini-diarize.py
```

Cloud tradeoff: faster, structured output built-in, but your audio goes to Google. Most newsrooms will use both local and cloud depending on the sensitivity of the material.
