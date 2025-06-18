import json

from config.openai_config import get_client

PROMPT_TEMPLATE = """
    You are an expert parser of South-African medical-scheme statements.
    Return the data as a single **valid JSON object** – no comments, no Markdown.

    ### Guidance
    • Capture any statement-level metadata you can recognise
    (e.g. scheme_name, membership_number, patient_name, provider_practice_number,
    statement_date_range, claim_number, etc.).  
    If a datum is missing, simply omit the key.

    • Capture the **tabular service lines** in an array called "service_lines".
    For each row include *whatever* columns you reliably identify, such as:
        tariff_code, description, service_date, icd10, quantity,
        charged_amount_zar, scheme_rate_zar, scheme_paid_zar,
        member_liability_zar, pm_b_indicator, etc.

    • Preserve row order with a "row_index" starting at 1.

    • Create a "totals" object if the statement shows overall totals
    (e.g. total_charged_zar, total_scheme_paid_zar, total_gap_zar).

    • All rand amounts → numbers with two decimals (no "R", no commas).

    • Feel free to include **any extra keys** that add value – do *not* invent data.
"""


def parse_statement(text: str) -> dict:
    """Extract metadata and service lines from statement text using OpenAI."""
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
    except Exception as err:
        # log err if you like
        data = {}

    return {
        **data,
        "raw_excerpt": text[:1000],
    }
