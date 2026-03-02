# audio

Transcription, speaker diarization, and word error rate measurement. Whisper and WhisperX run locally; Gemini requires an API key. Diarization (pyannote) requires a HuggingFace token with model access.

## Files

| File | What it does |
|------|-------------|
| `whisper.py` | Basic Whisper transcription with timestamps |
| `whisperx.py` | WhisperX word-level aligned transcription |
| `whisperx-diarize.py` | Full WhisperX pipeline: transcribe, align, diarize (who said what) |
| `pyannote.py` | Standalone pyannote speaker diarization (who spoke when) |
| `gemini.py` | Send audio to Gemini for transcription and analysis |
| `wer.py` | Word Error Rate comparison across Whisper model sizes |

## Comparison

| Tool | Timestamps | Diarization | Runs | Notes |
|------|-----------|-------------|------|-------|
| Whisper | Segment-level | No | Local | Simplest, fewest dependencies |
| WhisperX | Word-level | Yes (via pyannote) | Local | Default workshop tool |
| pyannote | Segment-level | Yes | Local | Speaker-only, no transcription |
| Gemini | No | No | Cloud (API) | Can also summarize and reason about audio |
