# Ask Gemini about a specific moment in a video using timestamps
import time
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from pydantic_ai import Agent, VideoUrl
from pydantic_ai.providers.google import GoogleProvider

DATA = Path(__file__).parent.parent / "data"
VIDEO = DATA / "rDXubdQdJYs.mp4"
PROMPT = "What is happening at 01:30 in this video? Describe the scene and any text on screen."
MODEL = "google-gla:gemini-2.5-flash"

provider = GoogleProvider()
video_file = provider.client.files.upload(file=str(VIDEO))

while video_file.state.name == "PROCESSING":
    time.sleep(5)
    video_file = provider.client.files.get(name=video_file.name)

agent = Agent(MODEL)
result = agent.run_sync([PROMPT, VideoUrl(url=video_file.uri, media_type=video_file.mime_type)])
print(result.output)
