# Find every mention of a keyword in audio → extract short video clips with ffmpeg.
from pathlib import Path
import subprocess

import whisper
import pandas as pd

DATA = Path(__file__).parent.parent / "data"

VIDEO = DATA / "rDXubdQdJYs.mp4"
KEYWORD = "president"
PADDING = 3  # seconds before/after

# --- Step 1: Transcribe with word-level timestamps ---
model = whisper.load_model("base")
result = model.transcribe(str(VIDEO), word_timestamps=True, verbose=False)

words = []
for seg in result["segments"]:
    for w in seg.get("words", []):
        words.append({"word": w["word"].strip(), "start": round(w["start"], 3), "end": round(w["end"], 3)})
print(f"Transcribed {len(words)} words")

# --- Step 2: Search for keyword ---
matches = []
kw = KEYWORD.lower()
for w in words:
    if kw in w["word"].lower().strip(".,!?;:'\""):
        matches.append(w)
print(f"Found {len(matches)} mentions of '{KEYWORD}'")

# --- Step 3: Extract clips with ffmpeg ---
clips_dir = Path(__file__).parent / "outputs" / "clips"
clips_dir.mkdir(parents=True, exist_ok=True)

clip_rows = []
for i, m in enumerate(matches):
    clip_start = max(0, m["start"] - PADDING)
    duration = (m["end"] + PADDING) - clip_start
    clip_name = f"clip_{i+1:03d}.mp4"
    clip_path = clips_dir / clip_name
    subprocess.run([
        "ffmpeg", "-y",
        "-ss", str(clip_start), "-i", str(VIDEO), "-t", str(duration),
        "-c:v", "libx264", "-c:a", "aac", "-loglevel", "error",
        str(clip_path),
    ], check=True)
    clip_rows.append({"clip": clip_name, "keyword": KEYWORD, "start": m["start"], "end": m["end"]})

print(f"Extracted {len(clip_rows)} clips to {clips_dir}")

df = pd.DataFrame(clip_rows)
df
