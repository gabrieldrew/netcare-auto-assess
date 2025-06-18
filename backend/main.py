import base64
import io
import json
import logging

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from assessment.assessor import assess_claim
from ocr import extract_text
from parsing.claim_form_ai import ai_extract
from parsing.statement_parser import parse_statement
from retrieval.vector_search import load_policy_index, retrieve_rules
from utils.pdf_generator import generate_assessment_pdf

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = FastAPI(title="GapCare Assessment API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

policy_index = None


@app.on_event("startup")
def startup():
    global policy_index
    policy_index = load_policy_index()


@app.post("/assess")
async def assess_claim_endpoint(
    medical: UploadFile = File(...),
    provider: UploadFile = File(...),
    claim: UploadFile = File(...),
):
    try:
        medical_text = extract_text(io.BytesIO(await medical.read()))
        provider_text = extract_text(io.BytesIO(await provider.read()))
        claim_text = extract_text(io.BytesIO(await claim.read()))

        medical_data = parse_statement(medical_text)
        provider_data = parse_statement(provider_text)
        form_data = ai_extract(claim_text)

        claim_data = {
            "medical_aid_statement": medical_data,
            "provider_statement": provider_data,
            **form_data,
        }

        rules = retrieve_rules(policy_index, claim_data)
        result = assess_claim(claim_data, rules)

        pdf_buffer = generate_assessment_pdf(claim_data, result, form_data)
        pdf_b64 = base64.b64encode(pdf_buffer.getvalue()).decode()

        logging.info(
            json.dumps(
                {"claimData": claim_data, "formData": form_data, "result": result},
                indent=2,
                ensure_ascii=False,
            )
        )

        return {
            "claimData": claim_data,
            "formData": form_data,
            "result": result,
            "pdf": pdf_b64,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
