# Send audio to Gemini for transcription and analysis
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from google import genai

DATA = Path(__file__).parent.parent / "data"
AUDIO = DATA / "rDXubdQdJYs.mp3"
MODEL = "gemini-2.5-flash"
PROMPT = "Transcribe this audio. Then list key topics, names, and numbers mentioned."

client = genai.Client()
audio_file = client.files.upload(file=str(AUDIO))
response = client.models.generate_content(model=MODEL, contents=[PROMPT, audio_file])
print(response.text)
client.files.delete(name=audio_file.name)
