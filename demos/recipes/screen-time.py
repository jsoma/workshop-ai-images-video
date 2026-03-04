# Classify pre-extracted debate frames → per-subject screen time summary.
# Audit trail: every frame gets a row, not a vibe answer.
from pathlib import Path
import pandas as pd
from pydantic import BaseModel, Field
from pydantic_ai import Agent, BinaryContent
from dotenv import load_dotenv
import ffmpeg
from typing import Literal

DATA = Path(__file__).parent.parent / "data"
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

MODEL, SECONDS_PER_FRAME = "openai:gpt-5-nano", 2.0

class FrameClassification(BaseModel):
    primary_subject: Literal[
        "Donald Trump", "Joe Biden", "neither/other/both"
    ] = Field(description="Who is primarily on screen, Donald Trump, Joe Biden, or neither/other?")
    scene_type: str = Field(description="'close-up', 'wide shot', 'split screen', 'graphic', 'audience', 'other'")
    confidence: float = Field(ge=0.0, le=1.0)

# --- cell ---
# ## Step 0: Extract frames from video
video_path = DATA / "debate.mp4"
frames_dir = DATA / "debate"
frames_dir.mkdir(exist_ok=True)
(
    ffmpeg.input(video_path)
    .filter("fps", fps=1/SECONDS_PER_FRAME)
    .output(str(frames_dir / "frame-%03d.jpg"))
    .overwrite_output()
    .run(quiet=True)
)

# --- cell ---
# ## Step 1: Discover frames
# Now we just have to collect the frames we just generated
frames_dir = DATA / "debate"
frames = sorted(p for p in frames_dir.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"})
print(f"Found {len(frames)} frames")

# --- cell ---
# ## Step 2: Classify each frame
# While we could do this in a fancy way, we're going to be simple: just ask the LLM who is on screen.
agent = Agent(MODEL, output_type=FrameClassification)
rows = []
for i, fpath in enumerate(frames):
    r = agent.run_sync([
        "This is a frame from a political debate. Identify who is on screen: Donald Trump or Joe Biden",
        BinaryContent(data=fpath.read_bytes(), media_type="image/jpeg"),
    ])
    rows.append({
        "frame": i,
        "timestamp_sec": i * SECONDS_PER_FRAME,
        "primary_subject": r.output.primary_subject,
        "scene_type": r.output.scene_type,
        "confidence": r.output.confidence,
    })
print(f"Classified {len(rows)} frames")

# --- cell ---
# ## Step 3: Build summary
# Count frames per subject → screen time
df = pd.DataFrame(rows)
summary = df.groupby("primary_subject").agg(
    frames=("frame", "count"),
    avg_confidence=("confidence", "mean"),
)
summary["seconds"] = summary["frames"] * SECONDS_PER_FRAME
summary["pct"] = (summary["seconds"] / summary["seconds"].sum() * 100).round(1)
print(summary.sort_values("seconds", ascending=False))

df
