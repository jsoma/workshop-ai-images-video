# Classify pre-extracted debate frames → per-subject screen time summary.
# Audit trail: every frame gets a row, not a vibe answer.
from pathlib import Path
import mimetypes, re
import pandas as pd
from pydantic import BaseModel, Field
from pydantic_ai import Agent, BinaryContent
from dotenv import load_dotenv

DATA = Path(__file__).parent.parent / "data"
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

MODEL, SECONDS_PER_FRAME = "openai:gpt-4o-mini", 1.0

class FrameClassification(BaseModel):
    primary_subject: str = Field(description="Who is primarily on screen (name or description)")
    scene_type: str = Field(description="'close-up', 'wide shot', 'split screen', 'graphic', 'audience', 'other'")
    confidence: float = Field(ge=0.0, le=1.0)

# --- Step 1: Discover frames ---
frames_dir = DATA / "debate"
frames = sorted(p for p in frames_dir.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"})
print(f"Found {len(frames)} frames")

# --- Step 2: Classify each frame ---
agent = Agent(MODEL, output_type=FrameClassification)
rows = []
for fpath in frames:
    num = int(m.group(1)) if (m := re.search(r"(\d+)", fpath.stem)) else 0
    mime, _ = mimetypes.guess_type(str(fpath))
    r = agent.run_sync([
        "This is a frame from a political debate. Identify who is on screen.",
        BinaryContent(data=fpath.read_bytes(), media_type=mime or "image/jpeg"),
    ])
    rows.append({"filename": fpath.name, "frame_number": num, "timestamp_sec": num * SECONDS_PER_FRAME,
                 "primary_subject": r.output.primary_subject, "scene_type": r.output.scene_type,
                 "confidence": r.output.confidence})
print(f"Classified {len(rows)} frames")

# --- Step 3: Build summary ---
df = pd.DataFrame(rows).sort_values("frame_number").reset_index(drop=True)
summary = (
    df.groupby("primary_subject")
    .agg(frames=("primary_subject", "count"),
         total_seconds=("timestamp_sec", lambda x: len(x) * SECONDS_PER_FRAME),
         avg_confidence=("confidence", "mean"))
    .sort_values("total_seconds", ascending=False)
)
summary["pct_of_total"] = (summary["total_seconds"] / summary["total_seconds"].sum() * 100).round(1)
print(summary)

df
