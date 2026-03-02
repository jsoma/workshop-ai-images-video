# WhisperX word-level aligned transcription
from pathlib import Path
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

for seg in result["segments"]:
    for w in seg.get("words", []):
        start = w.get("start", 0)
        end = w.get("end", 0)
        print(f"[{start:7.2f} - {end:7.2f}] {w.get('word', '')}  ({w.get('score', 0):.2f})")
