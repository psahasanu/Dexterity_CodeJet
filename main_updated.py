import os
import tempfile
from typing import Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from python_updated import (
    read_txtfile,
    read_pdffile,
    read_frmurl,
    fetch_offer_from_email,
)
from cheak_external_api import (
    check_1_company_exists,
    check_2_recruiter_real,
    check_3_salary_viability,
    check_4_email_verification,
    check_5_scam_database,
)

app = FastAPI(title="DEXTERITY API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OfferRequest(BaseModel):
    offer_text: str

class URLRequest(BaseModel):
    url: str

class EmailRequest(BaseModel):
    email_address: str
    app_password: str

CHECKS = [
    ("Company Exists", check_1_company_exists),
    ("Recruiter Is Real", check_2_recruiter_real),
    ("Salary & Opening Viability", check_3_salary_viability),
    ("Email Verification", check_4_email_verification),
    ("Scam Database", check_5_scam_database),
]

def run_checks(offer_text: str):
    if not offer_text or not offer_text.strip():
        raise HTTPException(status_code=400, detail="No offer text was provided.")

    results = []
    total_score = 0

    for name, fn in CHECKS:
        try:
            result = fn(offer_text)
            result = dict(result)
            result["name"] = name
            total_score += result.get("points", 0) or 0
        except Exception as exc:
            result = {
                "name": name,
                "passed": None,
                "points": 0,
                "reason": f"Check could not be completed: {exc}",
            }
        results.append(result)

    return {
        "score": total_score,
        "checks": results,
    }

def _read_upload(upload: UploadFile) -> str:
    suffix = os.path.splitext(upload.filename or "")[1].lower()
    if suffix not in {".txt", ".pdf"}:
        raise HTTPException(status_code=400, detail="Only .txt and .pdf files are supported.")

    data = upload.file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(data)
        path = tmp.name

    try:
        return read_txtfile(path) if suffix == ".txt" else read_pdffile(path)
    finally:
        try:
            os.remove(path)
        except OSError:
            pass

@app.get("/health")
def health():
    return {
        "status": "ok",
        "company_api_configured": bool(os.getenv("OPENCORPORATES_API_TOKEN")),
    }

@app.post("/read-txt")
async def read_txt_endpoint(file: UploadFile = File(...)):
    text = _read_upload(file)
    if text.startswith("Error:"):
        raise HTTPException(status_code=400, detail=text)
    return {"text": text}

@app.post("/read-pdf")
async def read_pdf_endpoint(file: UploadFile = File(...)):
    text = _read_upload(file)
    if text.startswith("Error:"):
        raise HTTPException(status_code=400, detail=text)
    return {"text": text}

@app.get("/read-url")
def read_url_endpoint(url: str):
    text = read_frmurl(url)
    if text.startswith("Error"):
        raise HTTPException(status_code=400, detail=text)
    return {"text": text}

@app.post("/read-email")
def read_email_endpoint(request: EmailRequest):
    text = fetch_offer_from_email(request.email_address, request.app_password)
    if text.startswith("Error"):
        raise HTTPException(status_code=400, detail=text)
    return {"text": text}

@app.post("/run-check-1")
def run_check_1(request: OfferRequest):
    return check_1_company_exists(request.offer_text)

@app.post("/run-all-checks")
def run_all_checks(request: OfferRequest):
    return run_checks(request.offer_text)

@app.post("/verify-file")
async def verify_file(file: UploadFile = File(...)):
    text = _read_upload(file)
    return run_checks(text)

@app.post("/verify-url")
def verify_url(request: URLRequest):
    text = read_frmurl(request.url)
    if text.startswith("Error"):
        raise HTTPException(status_code=400, detail=text)
    return run_checks(text)

@app.post("/verify-email")
def verify_email(request: EmailRequest):
    text = fetch_offer_from_email(request.email_address, request.app_password)
    if text.startswith("Error"):
        raise HTTPException(status_code=400, detail=text)
    return run_checks(text)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
