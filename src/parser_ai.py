import os, json
from dotenv import load_dotenv
from openai import OpenAI
from jsonschema import validate

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

RISK_FACTOR_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["company_name", "cik", "filing_date", "risk_title", "risk_text", "category"],
        "properties": {
            "company_name": {"type": "string"},
            "cik": {"type": "string"},
            "filing_date": {"type": "string"},
            "risk_title": {"type": "string"},
            "risk_text": {"type": "string"},
            "category": {"type": "string", "enum": ["market", "operational", "legal", "financial", "cyber"]}
        }
    }
}

def structure_html(html, prompt):
    # Use LLM to extract structured data. Only run to generate selectors or for new layouts.
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Return valid JSON only. No commentary. Return a JSON object with an items array."},
            {"role": "user", "content": f"{prompt}\n\nThe API response mode requires a JSON object, so wrap the requested array as {{\"items\": [...]}}. If no risk factors are found, return {{\"items\": []}}.\n\nHTML:\n{html[:12000]}"}
        ],
        response_format={"type": "json_object"}
    )
    payload = json.loads(res.choices[0].message.content)
    if isinstance(payload, dict) and isinstance(payload.get("items"), list):
        return payload["items"]
    raise ValueError("OpenAI response must be a JSON object with an items array")

def validate_schema(data):
    try:
        validate(instance=data, schema=RISK_FACTOR_SCHEMA)
        return True
    except Exception as e:
        print(f"Schema validation failed: {e}")
        return False
