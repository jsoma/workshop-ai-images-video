# Transcribe + diarize audio → per-speaker time breakdown.
# WhisperX + pyannote: "who spoke and for how long?"
from pathlib import Path
import os

import pandas as pd
import os
os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"
import torch
import whisperx
from whisperx.diarize import DiarizationPipeline
from dotenv import load_dotenv

DATA = Path(__file__).parent.parent / "data"
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

AUDIO = DATA / "rDXubdQdJYs.mp3"
HF_TOKEN = os.environ["HF_TOKEN"]

device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if device == "cuda" else "int8"

# --- Step 1: Transcribe ---
model = whisperx.load_model("large-v3", device, compute_type=compute_type)
audio = whisperx.load_audio(str(AUDIO))
result = model.transcribe(audio, batch_size=16)
print(f"Transcribed {len(result['segments'])} segments")

# --- Step 2: Align word-level timestamps ---
lang = result.get("language", "en")
model_a, metadata = whisperx.load_align_model(language_code=lang, device=device)
result = whisperx.align(
    result["segments"], model_a, metadata, audio, device,
    return_char_alignments=False,
)

# --- Step 3: Diarize (who spoke?) ---
diarize_model = DiarizationPipeline(token=HF_TOKEN, device=device)
diarize_segments = diarize_model(audio)
result = whisperx.assign_word_speakers(diarize_segments, result)
print(f"Diarized {len(result['segments'])} segments")

# --- Step 4: Build speaker time summary ---
rows = []
for seg in result["segments"]:
    rows.append({
        "speaker": seg.get("speaker", "UNKNOWN"),
        "start": round(seg["start"], 2),
        "end": round(seg["end"], 2),
        "duration": round(seg["end"] - seg["start"], 2),
        "text": seg.get("text", "").strip(),
    })

df = pd.DataFrame(rows)
summary = (
    df.groupby("speaker")["duration"]
    .agg(["sum", "count"])
    .rename(columns={"sum": "total_seconds", "count": "num_segments"})
    .sort_values("total_seconds", ascending=False)
)
summary["total_minutes"] = (summary["total_seconds"] / 60).round(1)
summary["pct_of_total"] = (summary["total_seconds"] / summary["total_seconds"].sum() * 100).round(1)
print(summary)

df
