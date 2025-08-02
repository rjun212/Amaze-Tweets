import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# Telegram config
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# Authors or terms to search for, unrestricted by site
search_queries = [
    ("Michael Liebreich", "Michael Liebreich"),
    ("Jesse Jenkins", "Jesse Jenkins"),
    ("Auke Hoekstra", "Auke Hoekstra"),
    ("Akshat Rathi", "Akshat Rathi"),
    ("Nick van Osdol", "Nick van Osdol"),
    ("Andrew Dessler", "Andrew Dessler"),
    ("Tom Steyer", "Tom Steyer"),
    ("Jan Rosenow", "Jan Rosenow"),
    ("Jigar Shah", "Jigar Shah"),
    ("BloombergNEF", "BloombergNEF"),
    ("Carbon Brief", "Carbon Brief"),
    ("Sam Butler-Sloss", "Sam Butler-Sloss"),
    ("JKempEnergy", "JKempEnergy"),
    ("IRENA", "IRENA"),
    ("Ember Climate", "Ember Climate")
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def bing_search(query):
    url = f"https://www.bing.com/search?q={requests.utils.quote(query)}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    results = []
    for item in soup.select(".b_algo h2 a")[:3]:
        title = item.get_text(strip=True)
        link = item["href"]
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
digest = f"🌐 *Web Mentions Digest – {datetime.now().strftime('%b %d')}*\n"

total_found = 0
for query, label in search_queries:
    matches = bing_search(query)
    if matches:
        digest += f"\n🔍 *{label}*"
        for title, link in matches:
            digest += f"\n- [{title}]({link})"
        total_found += len(matches)

if total_found == 0:
    digest += "\n\n_No new mentions found today._"

send_telegram(digest)
