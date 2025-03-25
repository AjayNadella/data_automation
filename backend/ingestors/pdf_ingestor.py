# ingestors/pdf_ingestor.py

import fitz  # PyMuPDF

def extract_text_from_pdf(filepath):
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text
