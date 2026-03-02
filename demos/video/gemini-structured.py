# Get a structured scene-by-scene breakdown of a video
import time
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from pydantic import BaseModel, Field
from pydantic_ai import Agent, VideoUrl
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

DATA = Path(__file__).parent.parent / "data"
VIDEO = DATA / "rDXubdQdJYs.mp4"

class Scene(BaseModel):
    start: str = Field(description="Start timestamp MM:SS")
    end: str = Field(description="End timestamp MM:SS")
    description: str = Field(description="What happens in this scene")
    people_visible: list[str] = Field(description="People visible")
    text_on_screen: str = Field(description="Any chyrons, captions, or on-screen text", default="")

provider = GoogleProvider()
video_file = provider.client.files.upload(file=str(VIDEO))

while video_file.state.name == "PROCESSING":
    time.sleep(5)
    video_file = provider.client.files.get(name=video_file.name)

agent = Agent(GoogleModel("gemini-2.5-flash", provider=provider), output_type=list[Scene])
result = agent.run_sync([
    "Break this video into scenes. For each scene identify timestamps, "
    "what happens, who is visible, and any text on screen.",
    VideoUrl(url=video_file.uri, media_type=video_file.mime_type),
])
for s in result.output:
    print(f"[{s.start} - {s.end}] {s.description}")
    if s.people_visible:
        print(f"  People: {', '.join(s.people_visible)}")
    if s.text_on_screen:
        print(f"  Text: {s.text_on_screen}")
provider.client.files.delete(name=video_file.name)
