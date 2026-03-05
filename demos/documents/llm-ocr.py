# Send an image to an LLM and get structured text extraction back
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from pydantic import BaseModel, Field
from pydantic_ai import Agent, BinaryContent

DATA = Path(__file__).parent.parent / "data"
MODEL = "openai:gpt-5-nano"
IMAGE = DATA / "flock-scan.jpg"

agent = Agent(MODEL)
image_data = IMAGE.read_bytes()

result = agent.run_sync([
    "Extract all visible text from this image. Preserve layout and reading order.",
    BinaryContent(data=image_data, media_type="image/jpeg"),
])

print(result.output)
