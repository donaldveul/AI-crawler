from fastapi import FastAPI, Header, HTTPException
import json, yaml

app = FastAPI(
    title="AI-Ready Data Packs API",
    description="15% cheaper than AWS Data Exchange. Structured SEC risk factors for RAG.",
    version="1.0.0"
)

DEMO_DATA = {
    "ticker": "NVDA",
    "company": "NVIDIA Corporation",
    "filing_date": "2024-02-15",
    "risk_factors": [
        {
            "category": "Market Risk",
            "description": "Exposure to cyclical demand in AI and data center markets. Semiconductor industry volatility may impact revenue growth.",
            "severity": "high",
            "relevance_score": 0.95,
        },
        {
            "category": "Regulatory Risk",
            "description": "Compliance with U.S. export controls on advanced semiconductors to China and other restricted countries.",
            "severity": "high",
            "relevance_score": 0.92,
        },
        {
            "category": "Supply Chain Risk",
            "description": "Dependency on Taiwan Semiconductor Manufacturing Company (TSMC) for chip production. Geopolitical tensions may disrupt supply.",
            "severity": "medium",
            "relevance_score": 0.88,
        },
        {
            "category": "Competition Risk",
            "description": "Intense competition from AMD, Intel, and emerging AI chip manufacturers. Price pressure may affect margins.",
            "severity": "medium",
            "relevance_score": 0.85,
        },
        {
            "category": "Technology Risk",
            "description": "Rapid technological change requires continuous R&D investment. Failure to innovate could result in market share loss.",
            "severity": "medium",
            "relevance_score": 0.83,
        },
        {
            "category": "Intellectual Property Risk",
            "description": "Patent disputes and licensing challenges in the semiconductor industry. Potential litigation costs and licensing fees.",
            "severity": "low",
            "relevance_score": 0.72,
        },
    ],
    "extraction_confidence": 0.94,
    "source": "SEC 10-K Filing 2024",
}

def load_config():
    with open('config.yaml') as f:
        return yaml.safe_load(f)

@app.get("/v1/demo")
def get_demo():
    return DEMO_DATA

@app.get("/v1/feed")
def get_feed(x_api_key: str = Header(None)):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")
    with open("data/sample_output.json") as f:
        return json.load(f)

@app.get("/v1/schema")
def get_schema():
    return {
        "schema_name": "RiskFactor",
        "fields": ["company_name", "cik", "filing_date", "risk_title", "risk_text", "category"],
        "format": "JSON array"
    }

@app.get("/pricing")
def pricing():
    cfg = load_config()
    m = cfg['monetization']
    return {
        "plan": "AI-Ready SEC Risk Factors",
        "price_monthly_usd": m['your_price_monthly'],
        "competitor_price_usd": m['competitor_price_monthly'],
        "discount": m['discount'],
        "value_prop": m['value_prop'],
        "sla": cfg['api']['sla']
    }

@app.get("/health")
def health():
    return {"status": "ok"}
