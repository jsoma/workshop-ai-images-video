# Classify a folder of images with structured output → DataFrame/CSV.
from pathlib import Path
import mimetypes

import pandas as pd
from pydantic import BaseModel, Field
from pydantic_ai import Agent, BinaryContent
from dotenv import load_dotenv

DATA = Path(__file__).parent.parent / "data"
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

MODEL = "openai:gpt-4o-mini"


class ImageClassification(BaseModel):
    category: str = Field(description="e.g. 'sedan', 'SUV', 'truck', 'van', 'motorcycle', 'bicycle', 'other'")
    color: str = Field(description="Dominant color of the main subject")
    description: str = Field(description="One-sentence description")
    confidence: float = Field(ge=0.0, le=1.0)


# --- Step 1: Discover images ---
folder = DATA / "cars"
images = sorted(p for p in folder.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"})
print(f"Found {len(images)} images")

# --- Step 2: Classify each image ---
agent = Agent(MODEL, output_type=ImageClassification)
rows = []
for img_path in images:
    mime, _ = mimetypes.guess_type(str(img_path))
    result = agent.run_sync([
        "Classify this image. What type of vehicle or object is shown?",
        BinaryContent(data=img_path.read_bytes(), media_type=mime or "image/jpeg"),
    ])
    rows.append({
        "filename": img_path.name,
        "category": result.output.category,
        "color": result.output.color,
        "description": result.output.description,
        "confidence": result.output.confidence,
    })
print(f"Classified {len(rows)} images")

# --- Step 3: Output ---
df = pd.DataFrame(rows)
df.to_csv(folder.parent / "car_classifications.csv", index=False)

df
