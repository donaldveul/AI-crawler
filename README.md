# AI-Ready Data Packs Crawler

Turn unstructured public data into LLM-ready JSON. 15% cheaper than AWS Data Exchange and legacy data brokers.

## The problem
Companies building AI agents hit a "data ceiling" on structured data. 90% of enterprise data is unstructured: SEC filings, PDFs, court docs, research papers, support tickets. Data teams spend 80% of their time on prep, not insights.

## The solution
This crawler targets high-value public sources, uses GPT-4o-mini to extract clean JSON, and serves it as an API. No dashboard bloat. Just AI-ready data.

## Business model
**Competitors**: AWS Data Exchange, Bloomberg, Refinitiv charge $5k-$20k/mo for licensed datasets  
**You**: $4,250-$17,000/mo — 15% cheaper for the same source data, pre-structured for RAG

**Example use cases**:
- Biotech: Clinical trial PDFs → structured drug interactions
- Legal tech: Court filings → entity + outcome JSON  
- Finance: 10-K risk factors → normalized sentiment + topics

## Repo structure
```
.
├── src/
│   ├── crawler.py          # Polite crawler with robots.txt + rate limits
│   ├── parser_ai.py        # LLM extraction → validated JSON schema
│   └── api.py              # FastAPI: /v1/demo, /v1/feed, /v1/schema, /pricing
├── data/
│   └── sample_output.json  # Example: SEC risk factors structured
├── config.yaml             # Define sources, schema, pricing
├── requirements.txt        
└── .gitignore
```

## Quick start
1. `pip install -r requirements.txt`
2. Set `OPENAI_API_KEY` in `.env`
3. Edit `config.yaml` with your data source + JSON schema
4. `python src/crawler.py` to test crawl + parse
5. `uvicorn src.api:app --reload` to serve data

## API endpoints
- `GET /v1/demo` returns deterministic NVIDIA risk-factor demo JSON for landing pages and demos. No API key required.
- `GET /v1/feed` returns the sample structured feed from `data/sample_output.json`. Requires an `x-api-key` header.
- `GET /v1/schema` returns the RiskFactor schema metadata.
- `GET /pricing` returns pricing and SLA details from `config.yaml`.
- `GET /health` returns service health.

## Legal
Only crawl public domain or permissively licensed data. Respect robots.txt and ToS. This repo does not include legal advice. Consult counsel before selling data derived from third-party sources.
