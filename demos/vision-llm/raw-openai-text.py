# Same task using raw OpenAI client, plain text response — no structured output
import base64
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from openai import OpenAI

MODEL = "gpt-4o-mini"
DATA = Path(__file__).parent.parent / "data"

client = OpenAI()
base64_image = base64.b64encode((DATA / "car.jpg").read_bytes()).decode("utf-8")

prompt = """List the following about this vehicle:
- make
- model
- type
- color
- estimated year
"""

response = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
    ]}],
)
print(response.choices[0].message.content)
