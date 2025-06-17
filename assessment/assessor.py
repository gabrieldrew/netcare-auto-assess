import json
from config.openai_config import get_client

PROMPT = """You are an expert claims assessor for a Gap Cover product.

### Policy rules (excerpts)
{rules}

### Claim information
{claim}

### Instructions
1. Determine whether the claim is covered.
2. If covered, specify benefit numbers and payable amount (consider limits).
3. If not covered, quote the rule that excludes it.

Return JSON with:
{{
  "covered": bool,
  "benefits": [string],
  "payable_amount_ZAR": string | null,
  "explanation": string
}}
""".strip()

def assess_claim(claim_struct, rules):
    client = get_client()
    prompt = PROMPT.format(
        rules="\n---\n".join(rules[:5]),
        claim=json.dumps(claim_struct, indent=2)
    )
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.0,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(resp.choices[0].message.content)