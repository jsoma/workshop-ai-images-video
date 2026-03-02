# Send an image to an LLM and get structured text extraction back
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

import mimetypes
from pydantic import BaseModel, Field
from pydantic_ai import Agent, BinaryContent

DATA = Path(__file__).parent.parent / "data"
MODEL = "openai:gpt-5-nano"
IMAGE = DATA / "city.png"

class ExtractedText(BaseModel):
    text: str = Field(description="All visible text, preserving layout")
    text_type: str = Field(description="sign, document, screenshot, handwritten, label, other")
    language: str = Field(description="Primary language of the text")
    confidence: str = Field(description="high, medium, or low")

agent = Agent(MODEL, output_type=ExtractedText)
mime_type, _ = mimetypes.guess_type(str(IMAGE))
image_data = IMAGE.read_bytes()

result = agent.run_sync([
    "Extract all visible text from this image. Preserve layout and reading order.",
    BinaryContent(data=image_data, media_type=mime_type or "image/jpeg"),
])

output = result.output
print(output.text)
print(f"\nType: {output.text_type}  Language: {output.language}  Confidence: {output.confidence}")
