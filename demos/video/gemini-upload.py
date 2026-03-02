# Upload a video file to Gemini and ask a question about it
import time
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from google import genai

DATA = Path(__file__).parent.parent / "data"
VIDEO = DATA / "rDXubdQdJYs.mp4"
PROMPT = "Describe what happens in this video."
MODEL = "gemini-2.5-flash"

client = genai.Client()

video_file = client.files.upload(file=str(VIDEO), config={"display_name": VIDEO.name})

while video_file.state.name == "PROCESSING":
    time.sleep(5)
    video_file = client.files.get(name=video_file.name)

response = client.models.generate_content(
    model=MODEL,
    contents=[PROMPT, video_file],
)

print(response.text)
