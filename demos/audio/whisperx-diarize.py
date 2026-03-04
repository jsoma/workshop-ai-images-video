# Full WhisperX pipeline: transcribe, align, diarize (who said what)
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")
import os
import warnings  # hidden
import logging  # hidden
warnings.filterwarnings("ignore")  # hidden
logging.getLogger("whisperx").setLevel(logging.ERROR)  # hidden
logging.getLogger("pyannote").setLevel(logging.ERROR)  # hidden
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

# Step 3: Diarize (split speakers)
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

# --- cell ---
# It isn't perfect, as you can tell!
# We probably want them split up beautifully though, right?
import pandas as pd
df = pd.DataFrame(result["segments"])
df