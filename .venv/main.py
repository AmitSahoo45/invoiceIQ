import tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from invoice import extract_fields
from pathlib import Path

app = FastAPI(title="InvoiceIQ API")

@app.get("/")
async def root():
    return {"message": "Welcome to the InvoiceIQ API"}

@app.post("/extract")
async def extract_invoice(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".pdf", ".png", ".jpg", ".jpeg"}:
        raise HTTPException(400, "Only .pdf, .png, .jpg, .jpeg allowed")

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        result = extract_fields(tmp_path)
    except Exception as e:
        raise HTTPException(500, f"Extraction failed: {e}")

    return JSONResponse(result)