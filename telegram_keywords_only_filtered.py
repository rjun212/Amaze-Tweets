
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

SEARCH_TERMS = [
    "renewable energy", "electricity", "batteries", "power",
    "battery storage", "energy storage"
]

TRUSTED_DOMAINS = [
    "bloomberg.com", "iea.org", "irena.org", "carbonbrief.org",
    "canarymedia.com", "cleantechnica.com", "etenergyworld.com", "substack.com"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def is_trusted(link):
    return any(domain in link for domain in TRUSTED_DOMAINS)

def bing_search(query):
    url = f"https://www.bing.com/search?q={requests.utils.quote(query)}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    results = []
    for item in soup.select(".b_algo h2 a")[:6]:
        title = item.get_text(strip=True)
        link = item["href"]
        if is_trusted(link):
            results.append((title, link))
    return results

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    requests.post(url, data=payload)

# Build digest
digest = f"🗞️ *Clean Energy Report Scan – {datetime.now().strftime('%b %d')}*"
total_found = 0

for query in SEARCH_TERMS:
    matches = bing_search(query)
    if matches:
        digest += f"\n\n🔍 *{query.title()}*"
        for title, link in matches:
            digest += f"\n- [{title}]({link})"
        total_found += len(matches)

if total_found == 0:
    digest += "\n\n_No relevant report titles found today._"

send_telegram(digest)
