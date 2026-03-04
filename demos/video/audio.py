# Extract audio track from a video file using ffmpeg-python
import ffmpeg
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"
VIDEO = DATA / "rDXubdQdJYs.mp4"
OUTPUT = Path(__file__).parent / "outputs"
OUTPUT.mkdir(parents=True, exist_ok=True)

(
    ffmpeg
    .input(str(VIDEO))
    .output(str(OUTPUT / "rDXubdQdJYs.mp3"), acodec="libmp3lame", vn=None)
    .overwrite_output()
    .run(quiet=True)
)

print(f"Audio saved to {OUTPUT / 'rDXubdQdJYs.mp3'}")
