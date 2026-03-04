# Send an image to an LLM and get structured text extraction back
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from natural_pdf import PDF

DATA = Path(__file__).parent.parent / "data"

pdf = PDF(DATA / "letter.pdf")
pdf.apply_ocr('easyocr')

print(pdf.extract_text())