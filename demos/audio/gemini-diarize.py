# Structured transcription with speaker labels via Gemini (cloud alternative to WhisperX)
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from pydantic import BaseModel, Field
from pydantic_ai import Agent, BinaryContent

DATA = Path(__file__).parent.parent / "data"
AUDIO = DATA / "rDXubdQdJYs.mp3"
MODEL = "google-gla:gemini-2.5-flash"

class Utterance(BaseModel):
    speaker: str = Field(description="Speaker label (e.g., Speaker 1, Speaker 2)")
    start: str = Field(description="Start timestamp MM:SS")
    end: str = Field(description="End timestamp MM:SS")
    text: str = Field(description="What was said")

agent = Agent(MODEL, output_type=list[Utterance])
result = agent.run_sync([
    "Transcribe this audio with speaker labels and timestamps for each utterance.",
    BinaryContent(data=AUDIO.read_bytes(), media_type="audio/mpeg"),
])
for u in result.output:
    print(f"[{u.start} - {u.end}] {u.speaker}: {u.text}")
