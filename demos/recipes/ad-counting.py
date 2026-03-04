# Sample frames from broadcast video → classify ad vs content → time breakdown.
from pathlib import Path
import cv2, pandas as pd
from pydantic import BaseModel, Field
from pydantic_ai import Agent, BinaryContent
from dotenv import load_dotenv

DATA = Path(__file__).parent.parent / "data"
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

VIDEO, MODEL, INTERVAL = DATA / "rDXubdQdJYs.mp4", "openai:gpt-5-nano", 3

class FrameType(BaseModel):
    classification: str = Field(description="'advertisement','sponsored_content','logo_bug','editorial_content','transition','other'")
    brand_or_sponsor: str = Field(default="")
    description: str
    confidence: float = Field(ge=0.0, le=1.0)

# --- Step 1: Extract frames ---
cap = cv2.VideoCapture(str(VIDEO))
fps = cap.get(cv2.CAP_PROP_FPS)
frame_interval = int(fps * INTERVAL)
frame_data, idx = [], 0
while True:
    cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
    ret, frame = cap.read()
    if not ret:
        break
    _, buf = cv2.imencode(".jpg", frame)
    frame_data.append((idx / fps, buf.tobytes()))
    idx += frame_interval
cap.release()
print(f"Extracted {len(frame_data)} frames")

# --- Step 2: Classify each frame ---
agent = Agent(MODEL, output_type=FrameType)
rows = []
for ts, img_bytes in frame_data:
    r = agent.run_sync([
        "Is this TV broadcast frame an advertisement, sponsored content, logo/bug, or editorial content?",
        BinaryContent(data=img_bytes, media_type="image/jpeg"),
    ])
    rows.append({"timestamp_sec": round(ts, 1), "classification": r.output.classification,
                 "brand_or_sponsor": r.output.brand_or_sponsor, "description": r.output.description,
                 "confidence": r.output.confidence})
print(f"Classified {len(rows)} frames")

# --- Step 3: Summarize ---
df = pd.DataFrame(rows)
df["is_ad"] = df["classification"].str.lower().isin({"advertisement", "sponsored_content", "logo_bug"})
ad_sec, total_sec = df["is_ad"].sum() * INTERVAL, len(df) * INTERVAL
print(f"Ad time: {ad_sec/60:.1f} min / {total_sec/60:.1f} min ({ad_sec/total_sec*100:.1f}%)")

df
