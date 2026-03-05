# The auditable way: classify each frame with Pydantic AI, produce an auditable CSV
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")
import pandas as pd
from pydantic import BaseModel
from pydantic_ai import Agent, BinaryContent

DATA = Path(__file__).parent.parent / "data"
MODEL = "google-gla:gemini-2.5-flash"
# MODEL = "openai:gpt-5-nano"
FRAMES_DIR = DATA / "debate"
OUTPUT = Path(__file__).parent / "outputs" / "frame_classifications.csv"

class FrameClassification(BaseModel):
    subject: str
    confidence: float
    speaking: bool
    description: str

agent = Agent(
    MODEL,
    output_type=FrameClassification,
    system_prompt="Classify frames from a political debate. Identify who is on screen, confidence 0-1, whether they are speaking.",
)

frames = sorted(FRAMES_DIR.glob("*.jpg"))
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

rows = []
for i, path in enumerate(frames):
    r = agent.run_sync([
        f"Frame {i}",
        BinaryContent(data=path.read_bytes(), media_type="image/jpeg"),
    ])
    rows.append({"frame": i, **r.output.model_dump()})
    print(f"{path.name}: {r.output.subject} ({r.output.confidence:.2f})")

# --- cell ---
# Every frame is now a row. You can sort, filter, and fact-check any one of them.
df = pd.DataFrame(rows)
df.to_csv(OUTPUT, index=False)
print(f"Saved {len(df)} frames to {OUTPUT}")

df
