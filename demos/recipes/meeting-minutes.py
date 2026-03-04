# Download a public meeting, transcribe it, summarize with Gemini.
from pathlib import Path
import warnings  # hidden
import logging  # hidden
warnings.filterwarnings("ignore")  # hidden
logging.getLogger("whisperx").setLevel(logging.ERROR)  # hidden
import yt_dlp
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from dotenv import load_dotenv

DATA = Path(__file__).parent.parent / "data"
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

URL = "https://www.youtube.com/watch?v=buEGUxrz8ho"
VIDEO_ID = "buEGUxrz8ho"
MODEL = "google-gla:gemini-2.5-flash"

# --- cell ---
# We'll start by downloading the audio.
audio_path = DATA / f"{VIDEO_ID}.mp3"
if not audio_path.exists():
    ydl_opts = {
        "outtmpl": str(DATA / "%(id)s.%(ext)s"),
        "format": "bestaudio/best",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])
print(f"Audio ready: {audio_path.name}")

# --- cell ---
# Now we'll transcribe. I know we talked about Whisper this and Whisper that, but there's a new model from NVIDIA called Parakeet, and the [Parakeet MLX](https://github.com/senstella/parakeet-mlx) implementation is super super fast on macOS. I transcribed this entire 2.5 hour meeting in about a minute. In the code below it first tries Parakeet, but if you don't have it (or are on Colab or Windows) it falls back to WhisperX.
try:
    from parakeet_mlx import from_pretrained
    print("Loading parakeet-mlx...")
    parakeet = from_pretrained("mlx-community/parakeet-tdt-0.6b-v3")
    print("Transcribing (chunked for long audio)...")
    result = parakeet.transcribe(str(audio_path), chunk_duration=600, overlap_duration=15)
    segments = [{"start": s.start, "text": s.text} for s in result.sentences]
    print(f"Transcribed {len(segments)} segments (parakeet-mlx)")
except ImportError:
    import torch
    import whisperx
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    print("Loading whisperx turbo...")
    model = whisperx.load_model("turbo", device, compute_type=compute_type)
    audio = whisperx.load_audio(str(audio_path))
    print("Transcribing...")
    result = model.transcribe(audio, batch_size=16)
    segments = [{"start": s["start"], "text": s["text"].strip()} for s in result["segments"]]
    print(f"Transcribed {len(segments)} segments (whisperx)")

# --- cell ---
# **What do we want to know from the meeting?** Maybe agenda items, votes, public comments, and some vague general details.
class AgendaItem(BaseModel):
    summary: str = Field(description="One-sentence summary of what was discussed")
    timestamp: str = Field(description="Approximate timestamp, MM:SS")

class Vote(BaseModel):
    item: str = Field(description="What was voted on")
    result: str = Field(description="Passed/failed/tabled and vote count if stated")
    timestamp: str = Field(description="MM:SS")

class PublicComment(BaseModel):
    speaker: str = Field(description="Name of commenter, if stated")
    topic: str = Field(description="What they spoke about")
    stance: str = Field(description="For/against/neutral")
    timestamp: str = Field(description="MM:SS")

class MeetingMinutes(BaseModel):
    title: str = Field(description="Short title for the meeting")
    overall_summary: str = Field(description="2-3 sentence summary of the meeting")
    agenda_items: list[AgendaItem] = Field(description="Major agenda items discussed")
    votes: list[Vote] = Field(description="Votes taken and their outcomes")
    public_comments: list[PublicComment] = Field(description="Public comments from residents")
    notable_quotes: list[str] = Field(description="Direct quotes that stood out, with speaker name")

# --- cell ---
# Now we can send the transcript to Gemini for all the details.
transcript_with_timestamps = "\n".join(
    f"[{int(seg['start']//60):02d}:{int(seg['start']%60):02d}] {seg['text']}"
    for seg in segments
)

print("Sending transcript to Gemini for summarization...")
agent = Agent(MODEL, output_type=MeetingMinutes)
summary = agent.run_sync(
    f"Summarize this city council meeting transcript. Extract agenda items, "
    f"votes and outcomes, public comments, and notable quotes. "
    f"Use timestamps from the transcript.\n\n"
    f"{transcript_with_timestamps}"
)

# --- cell ---
# And here's our structured meeting minutes.
minutes = summary.output
print(f"# {minutes.title}\n")
print(f"{minutes.overall_summary}\n")

print("## Agenda Items")
for item in minutes.agenda_items:
    print(f"  [{item.timestamp}] {item.summary}")

print("\n## Votes")
for v in minutes.votes:
    print(f"  [{v.timestamp}] {v.item} — {v.result}")

print("\n## Public Comments")
for pc in minutes.public_comments:
    print(f"  [{pc.timestamp}] {pc.speaker}: {pc.topic} ({pc.stance})")

print("\n## Notable Quotes")
for q in minutes.notable_quotes:
    print(f"  \"{q}\"")
