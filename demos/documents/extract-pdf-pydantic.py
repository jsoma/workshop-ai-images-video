# Extract structured data from a PDF using a Pydantic schema
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

import os
from openai import OpenAI
from pydantic import BaseModel, Field
from natural_pdf import PDF

class ReportInfo(BaseModel):
    inspection_number: str = Field(description="The main report identifier")
    inspection_date: str = Field(description="Date of the inspection")
    inspection_service: str = Field(description="Name of inspection service")
    site: str = Field(description="Name of company inspected")
    city: str
    state: str = Field(description="Full name of state")
    violation_count: int

# --- cell ---
# It isn't too interesting, but notice how we get the *full state name* now!
URL = "https://github.com/jsoma/natural-pdf/raw/refs/heads/main/pdfs/01-practice.pdf"

client = OpenAI(
    api_key=os.environ["GOOGLE_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

pdf = PDF(URL)
page = pdf.pages[0]
result = page.extract(
    schema=ReportInfo,
    client=client,
    model="gemini-2.5-flash"
)

print(result.to_dict())
