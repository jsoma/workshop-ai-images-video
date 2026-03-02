# Send a YouTube URL directly to Gemini for analysis (no download needed)
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from pydantic_ai import Agent, VideoUrl

URL = "https://www.youtube.com/watch?v=rDXubdQdJYs"
PROMPT = "What topics are discussed in this video?"
MODEL = "google-gla:gemini-2.5-flash"

agent = Agent(MODEL)
result = agent.run_sync([
    PROMPT,
    VideoUrl(url=URL),
])

print(result.output)
