# Basic Whisper transcription
from pathlib import Path
import whisper

DATA = Path(__file__).parent.parent / "data"
AUDIO = DATA / "rDXubdQdJYs.mp3"
MODEL = "turbo"

model = whisper.load_model(MODEL)
result = model.transcribe(str(AUDIO))

print(result["text"].strip())
# --- cell ---
# You can also get timestamps for each segment of the transcription. This is useful for aligning the text with the audio.
for seg in result["segments"]:
    start = f"{int(seg['start']//60):02d}:{seg['start']%60:05.2f}"
    end = f"{int(seg['end']//60):02d}:{seg['end']%60:05.2f}"
    print(f"[{start} - {end}] {seg['text'].strip()}")
