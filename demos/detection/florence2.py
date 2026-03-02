# Florence-2 detection + captioning — one model, many vision tasks
from pathlib import Path
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM

DATA = Path(__file__).parent.parent / "data"
MODEL_ID = "microsoft/Florence-2-base"

device = "cuda" if torch.cuda.is_available() else "cpu"
processor = AutoProcessor.from_pretrained(MODEL_ID, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID, trust_remote_code=True, torch_dtype=torch.float32
).to(device)

image = Image.open(DATA / "city.png").convert("RGB")

for task in ["OD", "DENSE_REGION_CAPTION"]:
    prompt = f"<{task}>"
    inputs = processor(text=prompt, images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        generated_ids = model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            num_beams=3,
        )
    text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]
    parsed = processor.post_process_generation(text, task=prompt, image_size=(image.width, image.height))
    print(f"--- {task} ---")
    print(parsed)
