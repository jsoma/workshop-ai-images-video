# Full WhisperX pipeline: transcribe, align, diarize (who said what)
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")
import os
import warnings
import logging
warnings.filterwarnings("ignore")
logging.getLogger("whisperx").setLevel(logging.ERROR)
logging.getLogger("pyannote").setLevel(logging.ERROR)
from collections import defaultdict
import torch, whisperx
from whisperx.diarize import DiarizationPipeline

DATA = Path(__file__).parent.parent / "data"
AUDIO = DATA / "rDXubdQdJYs.mp3"
MODEL, LANGUAGE = "large-v3", "en"
HF_TOKEN = os.environ["HF_TOKEN"]
device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if device == "cuda" else "int8"

# Step 1: Transcribe
model = whisperx.load_model(MODEL, device, compute_type=compute_type)
audio = whisperx.load_audio(str(AUDIO))
result = model.transcribe(audio, batch_size=16)
# Step 2: Align
model_a, metadata = whisperx.load_align_model(language_code=LANGUAGE, device=device)
result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
# Step 3: Diarize
diarize_model = DiarizationPipeline(token=HF_TOKEN, device=device)
result = whisperx.assign_word_speakers(diarize_model(audio), result)

# Print speaker-labeled segments
current_speaker = None
for seg in result["segments"]:
    speaker = seg.get("speaker", "UNKNOWN")
    if speaker != current_speaker:
        print(f"\n--- {speaker} ---")
        current_speaker = speaker
    start = f"{int(seg['start']//60):02d}:{seg['start']%60:05.2f}"
    end = f"{int(seg['end']//60):02d}:{seg['end']%60:05.2f}"
    print(f"  [{start} - {end}] {seg['text'].strip()}")

# Speaker time summary
speaker_time = defaultdict(float)
for seg in result["segments"]:
    speaker_time[seg.get("speaker", "UNKNOWN")] += seg["end"] - seg["start"]
total = sum(speaker_time.values())
print(f"\n{'Speaker':<12} {'Time':>8} {'%':>6}")
for spk in sorted(speaker_time):
    t = speaker_time[spk]
    print(f"  {spk:<10} {t/60:>6.1f}m {t/total*100:>5.1f}%")

# --- cell ---
import pandas as pd
df = pd.DataFrame(result["segments"])
df