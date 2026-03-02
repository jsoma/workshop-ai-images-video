# Extract frames from a video at 1 fps using ffmpeg-python
import ffmpeg
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"
VIDEO = DATA / "rDXubdQdJYs.mp4"
OUTPUT = Path(__file__).parent / "outputs" / "frames"
OUTPUT.mkdir(parents=True, exist_ok=True)

(
    ffmpeg
    .input(str(VIDEO))
    .filter("fps", fps=1)
    .output(str(OUTPUT / "frame_%04d.jpg"), **{"qscale:v": 2})
    .overwrite_output()
    .run(quiet=True)
)

frames = sorted(OUTPUT.glob("frame_*.jpg"))
print(f"Extracted {len(frames)} frames to {OUTPUT}")
