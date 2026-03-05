# Local document-to-markdown with Docling (PDFs, images, Office docs)
from pathlib import Path
from docling.document_converter import DocumentConverter

DATA = Path(__file__).parent.parent / "data"
IMAGE = DATA / "flock-scan.jpg"

converter = DocumentConverter()
result = converter.convert(str(IMAGE))
print(result.document.export_to_markdown())
