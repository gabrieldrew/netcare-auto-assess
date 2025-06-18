import json

from config.openai_config import get_client

PROMPT_TEMPLATE = (
    "You are a medical billing assistant. Extract all ICD10 diagnosis codes "
    "and rand amounts from the text below. Return valid JSON only in the "
    "following format:\n"
    "{\n  \"icd10\": [\"A00\", \"B99\"],\n  \"amounts\": [\"1234.56\"]\n}"
)


def parse_statement(text: str) -> dict:
    """Extract ICD10 codes and amounts from statement text using OpenAI."""
    client = get_client()
    prompt = f"{PROMPT_TEMPLATE}\n\n{text}"
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.0,
            response_format={"type": "json_object"},
            messages=[{"role": "user", "content": prompt}],
        )
        data = json.loads(resp.choices[0].message.content)
    except Exception:
        data = {}

    return {
        "icd10": data.get("icd10", []),
        "amounts": data.get("amounts", []),
        "raw_excerpt": text[:2000],
    }

