# Process a folder of images into structured data -> DataFrame -> CSV
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

import pandas as pd
from pydantic import BaseModel, Field
from pydantic_ai import Agent, BinaryContent
from typing import Literal

MODEL = "openai:gpt-4o-mini"
DATA = Path(__file__).parent.parent / "data"

class Vehicle(BaseModel):
    make: str = Field(description="Vehicle manufacturer")
    model: str = Field(description="Vehicle model name")
    color: str = Field(description="Primary color")
    year_estimate: int = Field(description="Estimated model year")
    vehicle_type: Literal["sedan", "SUV", "truck", "van", "motorcycle", "other"] = Field(description="Type of vehicle")
    confidence: float = Field(description="Confidence in identification, 0.0 to 1.0")

agent = Agent(MODEL, output_type=Vehicle)
rows = []
image_paths = sorted((DATA / "cars").glob("*.jpg"))
for image_path in image_paths:
    result = agent.run_sync([
        "Analyze the vehicle in this image. Fill in all fields.",
        BinaryContent(data=image_path.read_bytes(), media_type="image/jpeg"),
    ])
    rows.append({"filename": image_path.name, **result.output.model_dump()})

df = pd.DataFrame(rows)
output = Path(__file__).parent / "outputs" / "cars_analysis.csv"
output.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output, index=False)
df
