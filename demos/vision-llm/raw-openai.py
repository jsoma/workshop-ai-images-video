# Same task using raw OpenAI client (base64, JSON schema) — contrast to Pydantic AI
import base64
import json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from openai import OpenAI

MODEL = "gpt-4o-mini"
DATA = Path(__file__).parent.parent / "data"

client = OpenAI()
base64_image = base64.b64encode((DATA / "car.jpg").read_bytes()).decode("utf-8")

response = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": [
        {"type": "text", "text": "Analyze the vehicle in this image."},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
    ]}],
    response_format={"type": "json_schema", "json_schema": {
        "name": "vehicle_description",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "make": {"type": "string"}, "model": {"type": "string"},
                "color": {"type": "string"}, "year_estimate": {"type": "integer"},
                "confidence": {"type": "number"},
            },
            "required": ["make", "model", "color", "year_estimate", "confidence"],
            "additionalProperties": False,
        },
    }},
)
print(json.loads(response.choices[0].message.content))
