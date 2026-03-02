# The RIGHT way: classify each frame with Pydantic AI, produce an auditable CSV
import csv
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")
from pydantic import BaseModel
from pydantic_ai import Agent, BinaryContent

DATA = Path(__file__).parent.parent / "data"
FRAMES_DIR = DATA / "debate"
OUTPUT = Path(__file__).parent / "outputs" / "frame_classifications.csv"

class FrameClassification(BaseModel):
    subject: str
    confidence: float
    speaking: bool
    description: str

agent = Agent(
    "openai:gpt-4o-mini",
    output_type=FrameClassification,
    system_prompt="Classify frames from a political debate. Identify who is on screen, confidence 0-1, whether they are speaking.",
)

frames = sorted(f for f in FRAMES_DIR.iterdir() if f.suffix.lower() in {".jpg", ".jpeg", ".png"})
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["frame", "subject", "confidence", "speaking", "description"])
    for i, path in enumerate(frames, 1):
        c = agent.run_sync([f"Frame {i}", BinaryContent(data=path.read_bytes(), media_type="image/jpeg")]).output
        w.writerow([i, c.subject, f"{c.confidence:.2f}", c.speaking, c.description])
        print(f"{path.name}: {c.subject} ({c.confidence:.2f})")
print(f"\nSaved to {OUTPUT}")
