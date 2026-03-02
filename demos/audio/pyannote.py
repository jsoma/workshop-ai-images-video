# Standalone pyannote speaker diarization (who spoke when, no transcription)
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

import os
from collections import defaultdict
from pyannote.audio import Pipeline

DATA = Path(__file__).parent.parent / "data"
AUDIO = DATA / "rDXubdQdJYs.mp3"
HF_TOKEN = os.environ["HF_TOKEN"]

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-community-1", token=HF_TOKEN)
diarization = pipeline(str(AUDIO))

for turn, _, speaker in diarization.itertracks(yield_label=True):
    start = f"{int(turn.start//60):02d}:{turn.start%60:05.2f}"
    end = f"{int(turn.end//60):02d}:{turn.end%60:05.2f}"
    print(f"[{start} - {end}] {speaker}")

# Speaker time summary
speaker_time = defaultdict(float)
for turn, _, speaker in diarization.itertracks(yield_label=True):
    speaker_time[speaker] += turn.end - turn.start
total = sum(speaker_time.values())
print(f"\n{'Speaker':<12} {'Time':>8} {'%':>6}")
for spk in sorted(speaker_time):
    t = speaker_time[spk]
    print(f"  {spk:<10} {t/60:>6.1f}m {t/total*100:>5.1f}%")
