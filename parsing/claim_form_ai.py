import json
from json import JSONDecodeError

from config.openai_config import get_client

SCHEMA = {
    "policyholder_title": "string",
    "policyholder_name": "string",
    "policyholder_surname": "string",
    "policyholder_id": "string",
    "contact_number": "string",
    "email": "string",
    "patient_name": "string",
    "patient_surname": "string",
    "patient_id": "string",
    "patient_dob": "string",
    "relationship": "string",
    "policy_number": "string",
    "medical_aid": "string",
    "option": "string",
    "admission_date": "string",
    "discharge_date": "string",
    "provider_name": "string",
    "provider_contact": "string",
    "bank": "string",
    "account_number": "string",
    "branch_code": "string",
    "account_holder": "string",
}

PROMPT_TEMPLATE = (
    "You are an OCR post-processor. Extract the above fields from this "
    "GapCover claim form text and return valid JSON only."
)


def ai_extract(text: str) -> dict:
    client = get_client()
    prompt = (
        f"{PROMPT_TEMPLATE}\n\n"
        f"JSON schema:\n{json.dumps(SCHEMA, indent=2)}\n\n"
        f"Claim form text:\n{text}"
    )
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.0,
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
        )
        return json.loads(resp.choices[0].message.content)
    except JSONDecodeError:
        return {}

