# The risky way: ask Gemini "who got more screen time?" -- confident answer, no evidence
import time
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from pydantic_ai import Agent, VideoUrl
from pydantic_ai.providers.google import GoogleProvider

DATA = Path(__file__).parent.parent / "data"
VIDEO = DATA / "rDXubdQdJYs.mp4"
MODEL = "google-gla:gemini-2.5-flash"

provider = GoogleProvider()
video_file = provider.client.files.upload(file=str(VIDEO))

while video_file.state.name == "PROCESSING":
    time.sleep(5)
    video_file = provider.client.files.get(name=video_file.name)

agent = Agent(MODEL)
result = agent.run_sync([
    "Who got more screen time in this debate video? "
    "Give me a breakdown of approximately how much time each person was on screen.",
    VideoUrl(url=video_file.uri, media_type=video_file.mime_type),
])

print(result.output)
