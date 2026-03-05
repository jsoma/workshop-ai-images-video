# Transcribe + diarize with Parakeet and pyannote
from pathlib import Path
import warnings  # hidden
warnings.filterwarnings("ignore")  # hidden
from pyannote.audio import Pipeline
from dotenv import load_dotenv

DATA = Path(__file__).parent.parent / "data"
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

AUDIO = DATA / "rDXubdQdJYs.mp3"

try:
    from parakeet_mlx import from_pretrained
    print("Using parakeet-mlx...")
    model = from_pretrained("mlx-community/parakeet-tdt-0.6b-v3")
    result = model.transcribe(str(AUDIO), chunk_duration=600, overlap_duration=15)
except ImportError:
    import onnx_asr
    import ffmpeg
    print("Using onnx-asr...")
    WAV = AUDIO.with_suffix(".wav")
    if not WAV.exists():
        ffmpeg.input(str(AUDIO)).output(str(WAV), ar=16000, ac=1).run(quiet=True)
    model = onnx_asr.load_model("nemo-parakeet-tdt-0.6b-v3")
    result = model.recognize(str(WAV))

sentences = [{"start": s.start, "end": s.end, "text": s.text} for s in result.sentences]
print(f"Transcribed {len(sentences)} sentences")

# --- cell ---
# ### Diarize with pyannote
# Parakeet gives us *what* was said. Pyannote tells us *who* said it.
import torchaudio
import os

HF_TOKEN = os.environ["HF_TOKEN"]
waveform, sample_rate = torchaudio.load(str(AUDIO))
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-community-1",
    token=HF_TOKEN
)
diarization = pipeline({"waveform": waveform, "sample_rate": sample_rate})

# --- cell ---
# ### Combine: match speakers to sentences
# For each sentence, find which speaker was talking at its midpoint.
for s in sentences:
    mid = (s["start"] + s["end"]) / 2
    speaker = "UNKNOWN"
    for turn, label in diarization.speaker_diarization:
        if turn.start <= mid <= turn.end:
            speaker = label
            break
    s["speaker"] = speaker
sentences[:5]

# --- cell ---
# ### Display results
import pandas as pd
df = pd.DataFrame(sentences[:15])
df
