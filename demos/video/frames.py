# Extract frames from a video at 1 frame every 2 seconds using ffmpeg-python
import ffmpeg
from pathlib import Path

DATA = Path(__file__).parent.parent / "data"
VIDEO = DATA / "rDXubdQdJYs.mp4"
OUTPUT = Path(__file__).parent / "outputs" / "frames"
OUTPUT.mkdir(parents=True, exist_ok=True)

(
    ffmpeg
    .input(str(VIDEO))
    .filter("fps", fps=0.5)
    .output(str(OUTPUT / "frame_%04d.jpg"), **{"qscale:v": 2})
    .overwrite_output()
    .run(quiet=True)
)

frames = sorted(OUTPUT.glob("frame_*.jpg"))
print(f"Extracted {len(frames)} frames to {OUTPUT}")

# --- cell ---
# Preview: a sample of what we just extracted.
import matplotlib.pyplot as plt
from PIL import Image

sample = frames[:10]
fig, axes = plt.subplots(2, 5, figsize=(15, 6))
for ax, path in zip(axes.flat, sample):
    ax.imshow(Image.open(path))
    ax.set_title(path.stem, fontsize=8)
    ax.axis("off")
plt.tight_layout()
