# Send one image to an LLM, get structured Pydantic data back
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from pydantic import BaseModel, Field
from pydantic_ai import Agent, BinaryContent

MODEL = "openai:gpt-4o-mini"
DATA = Path(__file__).parent.parent / "data"

class Vehicle(BaseModel):
    make: str = Field(description="Vehicle manufacturer (e.g., Toyota, Ford)")
    model: str = Field(description="Vehicle model name (e.g., Camry, F-150)")
    color: str = Field(description="Primary color of the vehicle")
    year_estimate: int = Field(description="Estimated model year (best guess)")
    vehicle_type: str = Field(description="Type: sedan, SUV, truck, van, motorcycle, etc.")
    confidence: float = Field(description="Your confidence in this identification, 0.0 to 1.0")

agent = Agent(MODEL, output_type=Vehicle)
result = agent.run_sync([
    "Analyze the vehicle in this image. Fill in all fields accurately.",
    BinaryContent(data=(DATA / "car.jpg").read_bytes(), media_type="image/jpeg"),
])
result.output
