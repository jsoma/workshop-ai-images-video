# Parakeet transcription via NeMo (NVIDIA Parakeet TDT with timestamps)
from pathlib import Path
import nemo.collections.asr as nemo_asr

DATA = Path(__file__).parent.parent / "data"
AUDIO = DATA / "rDXubdQdJYs.mp3"
MODEL = "nvidia/parakeet-tdt-0.6b-v2"

model = nemo_asr.models.ASRModel.from_pretrained(model_name=MODEL)
output = model.transcribe([str(AUDIO)], timestamps=True, channel_selector=0)

for stamp in output[0].timestamp["segment"]:
    start = f"{int(stamp['start']//60):02d}:{stamp['start']%60:05.2f}"
    end = f"{int(stamp['end']//60):02d}:{stamp['end']%60:05.2f}"
    print(f"[{start} - {end}] {stamp['segment']}")
