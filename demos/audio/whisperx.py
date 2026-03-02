# WhisperX segment-level aligned transcription
from pathlib import Path
import warnings  # hidden
import logging  # hidden
warnings.filterwarnings("ignore")  # hidden
logging.getLogger("whisperx").setLevel(logging.ERROR)  # hidden
logging.getLogger("pyannote").setLevel(logging.ERROR)  # hidden
import torch
import whisperx

DATA = Path(__file__).parent.parent / "data"
AUDIO = DATA / "rDXubdQdJYs.mp3"
MODEL = "large-v3"
LANGUAGE = "en"

device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if device == "cuda" else "int8"

model = whisperx.load_model(MODEL, device, compute_type=compute_type)
audio = whisperx.load_audio(str(AUDIO))
result = model.transcribe(audio, batch_size=16)

model_a, metadata = whisperx.load_align_model(language_code=LANGUAGE, device=device)
result = whisperx.align(
    result["segments"], model_a, metadata, audio, device,
    return_char_alignments=False,
)

# Print out the entire transcript
print(" ".join(seg["text"].strip() for seg in result["segments"]))

# --- cell ---
# You can also view the segments with timestamps and aligned text
import pandas as pd

df = pd.DataFrame(result["segments"])
df