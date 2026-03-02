# Send one image to an LLM, get structured Pydantic data back
from pathlib import Path
from typing import Literal
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from pydantic import BaseModel, Field
from pydantic_ai import Agent, BinaryContent
from typing import Literal

MODEL = "openai:gpt-4o-mini"
DATA = Path(__file__).parent.parent / "data"

image_data = (DATA / "car.jpg").read_bytes()

class Vehicle(BaseModel):
    make: str = Field(description="Vehicle manufacturer (e.g., Toyota, Ford)")
    model: str = Field(description="Vehicle model name (e.g., Camry, F-150)")
    color: str = Field(description="Primary color of the vehicle")
    year_estimate: int = Field(description="Estimated model year (best guess)")
    vehicle_type: Literal[
        "sedan", "SUV", "truck", "van", "motorcycle", "other"
    ] = Field(description="Type of vehicle")
    confidence: float = Field(description="Your confidence in this identification, 0.0 to 1.0")

agent = Agent(MODEL, output_type=Vehicle)
result = agent.run_sync([
    "Analyze the vehicle in this image. Fill in all fields accurately.",
    BinaryContent(data=image_data, media_type="image/jpeg"),
])
result.output
