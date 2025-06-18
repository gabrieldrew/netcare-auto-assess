import json
import re

from config.openai_config import get_client

PROMPT = """You are an expert claims assessor for a Gap Cover product.

### Policy rules (complete)
{rules}

### Claim information
{claim}

### Instructions
1. Determine whether the claim is covered under any of the 12 GapCare benefits.
2. If covered, specify the actual benefit names (not numbers) that apply.
3. If not covered, quote the specific rule that excludes it.
4. Consider all waiting periods, limits, and conditions.

IMPORTANT: Return ONLY valid JSON with no additional text or formatting. Do not use markdown code blocks.

Use these exact benefit names when applicable:
- "In-Hospital Specialist cover"
- "In-Hospital Co-payments and deductibles" 
- "Co-payments for voluntary use of a non-network hospital"
- "Specialists (out of Hospital)"
- "Additional day to day"
- "Maternity"
- "Oncology"
- "Emergency Departments"
- "Trauma Counselling"
- "Premium Waiver"
- "Charges Above Sub Limits"
- "Waiting Periods"

Required JSON format:
{{
  "covered": true/false,
  "benefits": ["benefit name 1", "benefit name 2"],
  "payable_amount_ZAR": "amount or null",
  "explanation": "detailed explanation"
}}
""".strip()


def extract_json_from_response(response_text: str) -> dict:
    """
    Extract JSON from LLM response, handling various formatting issues.
    """
    # Remove markdown code blocks if present
    cleaned = re.sub(r"```(?:json)?\s*", "", response_text)
    cleaned = re.sub(r"```\s*$", "", cleaned)

    # Try to find JSON object in the response
    json_pattern = r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}"
    matches = re.findall(json_pattern, cleaned, re.DOTALL)

    if matches:
        # Try each potential JSON match
        for match in matches:
            try:
                return json.loads(match.strip())
            except json.JSONDecodeError:
                continue

    # If no valid JSON found, try parsing the whole response
    try:
        return json.loads(cleaned.strip())
    except json.JSONDecodeError:
        # Last resort: try to find and parse just the content between braces
        brace_start = cleaned.find("{")
        brace_end = cleaned.rfind("}")
        if brace_start != -1 and brace_end != -1 and brace_end > brace_start:
            try:
                json_part = cleaned[brace_start : brace_end + 1]
                return json.loads(json_part)
            except json.JSONDecodeError:
                pass

    # If all else fails, return a default error response
    return {
        "covered": False,
        "benefits": [],
        "payable_amount_ZAR": None,
        "explanation": f"Error: Could not parse LLM response as JSON. Raw response: {response_text[:500]}...",
    }


def assess_claim(claim_struct, rules):
    """
    Assess a claim against policy rules using OpenAI.
    Returns a structured assessment result.
    """
    client = get_client()
    prompt = PROMPT.format(
        rules="\n---\n".join(rules),  # Use all rules, not just first 5
        claim=json.dumps(claim_struct, indent=2)
    )

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}],
        )

        response_content = resp.choices[0].message.content
        return extract_json_from_response(response_content)

    except Exception as e:
        # Handle any API or other errors
        return {
            "covered": False,
            "benefits": [],
            "payable_amount_ZAR": None,
            "explanation": f"Error during assessment: {str(e)}",
        }
