# Same structured-output task with different LLM providers
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from pydantic import BaseModel, Field
from pydantic_ai import Agent, BinaryContent

DATA = Path(__file__).parent.parent / "data"
image_data = (DATA / "sky.jpg").read_bytes()

class ImageDescription(BaseModel):
    subject: str = Field(description="Main subject of the image")
    setting: str = Field(description="Where the image appears to be taken")
    mood: str = Field(description="Overall mood or feeling of the image")
    details: list[str] = Field(description="3-5 notable details")

models = [
    "openai:gpt-4o-mini",
    "google-gla:gemini-2.5-flash",
    # "anthropic:claude-3-5-haiku-latest",
    # "ollama:qwen2-vl",
]
for model in models:
    agent = Agent(model, output_type=ImageDescription)
    result = agent.run_sync([
        "Describe this image. Fill in all fields.",
        BinaryContent(data=image_data, media_type="image/jpeg"),
    ])
    print(f"--- {model} ---")
    print(result.output)
