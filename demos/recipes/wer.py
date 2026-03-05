# Word error rate: how wrong is the cheap model vs the good one?
from pathlib import Path
import re
import warnings  # hidden
import logging  # hidden
warnings.filterwarnings("ignore")  # hidden
logging.getLogger("whisperx").setLevel(logging.ERROR)  # hidden
import os
os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"
import torch
import whisperx

DATA = Path(__file__).parent.parent / "data"
AUDIO = DATA / "rDXubdQdJYs.mp3"
MODELS = ["tiny", "turbo"]

device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if device == "cuda" else "int8"

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return re.sub(r"\s+", " ", text).strip()

def word_error_rate(reference, hypothesis):
    ref, hyp = normalize(reference).split(), normalize(hypothesis).split()
    n, m = len(ref), len(hyp)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1): d[i][0] = i
    for j in range(m + 1): d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i][j] = d[i-1][j-1] if ref[i-1] == hyp[j-1] else 1 + min(d[i-1][j], d[i][j-1], d[i-1][j-1])
    return d[n][m] / n if n else 0.0

# --- cell ---
# ## Transcribe with both models
transcripts = {}
for name in MODELS:
    print(f"Loading {name}...")
    model = whisperx.load_model(name, device, compute_type=compute_type)
    audio = whisperx.load_audio(str(AUDIO))
    result = model.transcribe(audio, batch_size=16)
    transcripts[name] = " ".join(seg["text"].strip() for seg in result["segments"])
    del model

# --- cell ---
# ## Compare
# Using `turbo` as the reference (it's the better model), how many words does `tiny` get wrong?
score = word_error_rate(transcripts["turbo"], transcripts["tiny"])
print(f"Word Error Rate (tiny vs turbo): {score*100:.1f}%")
print(f"  turbo: {len(transcripts['turbo'].split())} words")
print(f"  tiny:  {len(transcripts['tiny'].split())} words")

# --- cell ---
# Show the first 500 characters of each so you can eyeball the differences.
print("=== turbo ===")
print(transcripts["turbo"][:500])
print("\n=== tiny ===")
print(transcripts["tiny"][:500])
