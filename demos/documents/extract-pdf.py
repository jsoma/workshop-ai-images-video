# Extract structured data from a PDF page with an LLM, with visual citations
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

import os
from openai import OpenAI
from natural_pdf import PDF

URL = "https://github.com/jsoma/natural-pdf/raw/refs/heads/main/pdfs/01-practice.pdf"

client = OpenAI(
    api_key=os.environ["GOOGLE_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

pdf = PDF(URL)
page = pdf.pages[0]

fields = ["site", "date", "violation count", "inspection service", "summary", "city", "state"]
results = page.extract(
    fields,
    client=client,
    model="gemini-2.5-flash",
    citations=True)
print(results.to_dict())

# --- cell ---
# Here we go with some **visual citations,** highlights on the PDF show where each answer came from.
from IPython.display import display

display(results.show())