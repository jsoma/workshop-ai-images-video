# Send one image to an LLM, get a text description back
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from pydantic_ai import Agent, BinaryContent

MODEL = "openai:gpt-4o-mini"
DATA = Path(__file__).parent.parent / "data"

agent = Agent(MODEL, output_type=str)
result = agent.run_sync([
    "Describe what you see in this image in 2-3 sentences.",
    BinaryContent(data=(DATA / "sky.jpg").read_bytes(), media_type="image/jpeg"),
])
print(result.output)
