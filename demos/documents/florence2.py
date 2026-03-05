# Local OCR with annotated bounding boxes (Florence-2 + supervision, no API key)
from pathlib import Path
import torch
from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import supervision as sv

DATA = Path(__file__).parent.parent / "data"
IMAGE = DATA / "city.jpg"
MODEL_ID = "microsoft/Florence-2-base"
TASK = "<OCR_WITH_REGION>"

device = "cuda" if torch.cuda.is_available() else "cpu"
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, trust_remote_code=True).to(device)
processor = AutoProcessor.from_pretrained(MODEL_ID, trust_remote_code=True)

image = Image.open(IMAGE).convert("RGB")
inputs = processor(text=TASK, images=image, return_tensors="pt").to(device)
ids = model.generate(**inputs, max_new_tokens=1024, num_beams=3)
parsed = processor.post_process_generation(
    processor.batch_decode(ids, skip_special_tokens=False)[0],
    task=TASK, image_size=image.size,
)

detections = sv.Detections.from_lmm(sv.LMM.FLORENCE_2, parsed, resolution_wh=image.size)
annotated = sv.BoxAnnotator(color_lookup=sv.ColorLookup.INDEX).annotate(image.copy(), detections)
annotated = sv.LabelAnnotator(color_lookup=sv.ColorLookup.INDEX).annotate(annotated, detections)
sv.plot_image(annotated)

for label in parsed[TASK]["labels"]:
    print(label)
