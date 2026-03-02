# Ask Gemini about a specific time range in audio
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from pydantic_ai import Agent, BinaryContent

DATA = Path(__file__).parent.parent / "data"
AUDIO = DATA / "rDXubdQdJYs.mp3"
MODEL = "google-gla:gemini-2.5-flash"
PROMPT = "What is being discussed between 00:30 and 01:30? Summarize the key points."

agent = Agent(MODEL)
result = agent.run_sync([
    PROMPT,
    BinaryContent(data=AUDIO.read_bytes(), media_type="audio/mpeg"),
])
print(result.output)
