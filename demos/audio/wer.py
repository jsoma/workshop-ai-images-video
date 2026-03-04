# Word Error Rate comparison across Whisper model sizes
from pathlib import Path
import re
import whisper

DATA = Path(__file__).parent.parent / "data"
AUDIO = DATA / "rDXubdQdJYs.mp3"
MODELS = ["tiny", "turbo"]
REFERENCE = """relative to what we're going to do with more 
border patrol and more asylum officers. President Trump? 
I really don't know what he said at the end of that sentence. 
I don't think he knows what he said either.  The only person 
on this stage is a convicted felon is the man I'm looking at 
right now. But when he talks about a convicted felon, his son 
is a convicted felon. What are you talking about? You have 
the morals of an alley cat. My son was not a loser, was not 
a sucker.""".strip()

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return re.sub(r"\s+", " ", text).strip()

def compute_wer(reference, hypothesis):
    ref = normalize(reference).split()
    hyp = normalize(hypothesis).split()
    n, m = len(ref), len(hyp)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1): d[i][0] = i
    for j in range(m + 1): d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i][j] = d[i-1][j-1] if ref[i-1] == hyp[j-1] else 1 + min(d[i-1][j], d[i][j-1], d[i-1][j-1])
    return d[n][m] / n if n else 0.0

print(f"{'Model':<12} {'WER':>8}")
print("-" * 22)
for name in MODELS:
    model = whisper.load_model(name)
    result = model.transcribe(str(AUDIO))
    wer = compute_wer(REFERENCE, result["text"])
    print(f"  {name:<10} {wer*100:>6.1f}%")
