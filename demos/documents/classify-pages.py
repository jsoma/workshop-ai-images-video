# Classify pages of a PDF visually (diagram, text, invoice, etc.) using CLIP
from natural_pdf import PDF

URL = "https://github.com/jsoma/ire25-natural-pdf/raw/refs/heads/main/cia-doc.pdf"

pdf = PDF(URL)
pdf.classify_pages(['diagram', 'text', 'invoice', 'blank'], using='vision')

for page in pdf.pages:
    print(f"Page {page.number}: {page.category} ({page.category_confidence:.2f})")

diagrams = pdf.pages.filter(lambda p: p.category == 'diagram')
print(f"\nFound {len(diagrams)} diagram pages")
diagrams.show(show_category=True)
