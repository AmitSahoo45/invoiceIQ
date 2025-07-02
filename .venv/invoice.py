import sys, json
import fitz
from PIL import Image
from transformers import pipeline

def pdf_to_images(pdf_path: str, dpi: int = 300):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    mode = "RGBA" if pix.alpha else "RGB"
    img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)
    return [img]

def extract_fields(path: str):
    nlp = pipeline(
        "document-question-answering",
        model="impira/layoutlm-document-qa",
        tokenizer="impira/layoutlm-document-qa"
    )

    if path.lower().endswith(".pdf"):
        images = pdf_to_images(path)
        image = images[0]
    else:
        image = Image.open(path)

    fields = {
        "invoice_number": "What is the invoice number?",
        "invoice_date":   "What is the invoice date?",
        "vendor_name":    "Who is the vendor?",
        "total_amount":   "What is the total amount?"
    }

    results = {}
    for key, question in fields.items():
        out = nlp(image, question)
        results[key] = {"answer": out["answer"], "confidence": out["score"]}
    return results

data = extract_fields("invoice/invoice1.pdf")
print(json.dumps(data, indent=2))
