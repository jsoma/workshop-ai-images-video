# Download a video from a URL using yt-dlp
import subprocess
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"
URL = "https://www.youtube.com/watch?v=rDXubdQdJYs"

DATA.mkdir(parents=True, exist_ok=True)
subprocess.run([
    "yt-dlp",
    "-o", str(DATA / "%(title)s [%(id)s].%(ext)s"),
    "-f", "best",
    "--no-overwrites",
    URL,
])
