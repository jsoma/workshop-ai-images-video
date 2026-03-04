# Send audio to Gemini for transcription and analysis
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from pydantic_ai import Agent, BinaryContent

DATA = Path(__file__).parent.parent / "data"
AUDIO = DATA / "rDXubdQdJYs.mp3"
MODEL = "google-gla:gemini-2.5-flash"
PROMPT = "Transcribe this audio. Then list key topics, names, and numbers mentioned."

agent = Agent(MODEL)
result = agent.run_sync([
    PROMPT,
    BinaryContent(data=AUDIO.read_bytes(), media_type="audio/mpeg"),
])
print(result.output)
