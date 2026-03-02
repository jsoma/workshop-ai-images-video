# Send an image to an LLM and get the text back
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from pydantic_ai import Agent, BinaryContent

DATA = Path(__file__).parent.parent / "data"
MODEL = "openai:gpt-5-nano"
IMAGE = DATA / "flock-scan.png"

agent = Agent(MODEL)

result = agent.run_sync([
    "Extract all visible text from this image. Preserve layout and reading order.",
    BinaryContent(data=IMAGE.read_bytes(), media_type="image/png"),
])

print(result.output)
