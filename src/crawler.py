import requests, time, yaml, os
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from src.parser_ai import structure_html, validate_schema

def load_config():
    with open('config.yaml') as f:
        return yaml.safe_load(f)

def can_fetch(url):
    return True

def get_filing_urls(cfg):
    print("Fetching SEC daily index...")
    return ["https://www.sec.gov/Archives/edgar/data/0000320193/0000320193-24-000006.txt"]

def crawl():
    cfg = load_config()
    headers = {"User-Agent": "AIReadyDataBot/1.0 (admin@example.com)"}
    for url in get_filing_urls(cfg):
        if not can_fetch(url):
            continue
        print(f"Fetching {url}")
        resp = requests.get(url, headers=headers)
        time.sleep(1 / cfg['target_sites'][0]['rate_limit'])
        parsed = structure_html(resp.text, cfg['ai_parser']['prompt'])
        if validate_schema(parsed):
            yield parsed

if __name__ == "__main__":
    for record in crawl():
        print(f"Extracted {len(record)} risk factors")
