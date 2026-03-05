# Download a video from YouTube with yt-dlp
from pathlib import Path
import yt_dlp

DATA = Path(__file__).parent.parent / "data"
URL = "https://www.youtube.com/watch?v=rDXubdQdJYs"

DATA.mkdir(parents=True, exist_ok=True)
VIDEO_ID = URL.split("v=")[1]

existing = list(DATA.glob(f"{VIDEO_ID}.*"))
if existing:
    print(f"Already downloaded: {existing[0].name}")
else:
    ydl_opts = {
        "outtmpl": str(DATA / "%(id)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL])
    print(f"Downloaded: {VIDEO_ID}")
