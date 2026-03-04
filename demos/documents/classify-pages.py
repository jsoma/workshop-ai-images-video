# Classify pages of a PDF visually (diagram, text, invoice, etc.) using CLIP
from natural_pdf import PDF
from IPython.display import display

pdf = PDF("https://github.com/jsoma/ire25-natural-pdf/raw/refs/heads/main/cia-doc.pdf")

display(pdf.show(columns=5))

# --- cell ---
# You can classify with either vision or text. In this case we'll see whether they're diagrams, text-heavy, invoices, or blank pages.
pdf.classify_pages(['diagram', 'text', 'invoice', 'blank'], using='vision')

for page in pdf.pages:
    print(f"Page {page.number}: {page.category} ({page.category_confidence:.2f})")

# --- cell ---
# **Amazing!** You can then filter and show pages by category (this also works with entire PDFs!)
diagrams = pdf.pages.filter(lambda p: p.category == 'diagram')
print(f"\nFound {len(diagrams)} diagram pages")
diagrams.show(show_category=True)
