import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

authors = [
    "Michael Liebreich", "Jesse Jenkins", "Auke Hoekstra", "Akshat Rathi",
    "Nick van Osdol", "Andrew Dessler", "Tom Steyer", "Jan Rosenow",
    "Jigar Shah", "BloombergNEF", "Carbon Brief", "Sam Butler-Sloss",
    "JKempEnergy", "IRENA", "Ember Climate"
]

TOPIC_FILTER = "renewable OR grid OR energy OR power OR electricity OR climate"
RELEVANT_KEYWORDS = ["renewable", "grid", "energy", "power", "electricity", "climate"]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def bing_search(query):
    url = f"https://www.bing.com/search?q={requests.utils.quote(query)}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    results = []
    for item in soup.select(".b_algo")[:5]:
        link_tag = item.select_one("h2 a")
        snippet_tag = item.select_one(".b_caption p")
        if link_tag and any(kw in link_tag.get_text(strip=True).lower() for kw in RELEVANT_KEYWORDS):
            title = link_tag.get_text(strip=True)
            link = link_tag["href"]
            snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
            results.append((title, link, snippet))
    return results

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    requests.post(url, data=payload)

digest = f"🌐 *Filtered Web Mentions Digest – {datetime.now().strftime('%b %d')}*\n"
total_found = 0

for author in authors:
    query = f'"{author}" {TOPIC_FILTER}'
    matches = bing_search(query)
    if matches:
        digest += f"\n🔍 *{author}*"
        for title, link, snippet in matches:
            digest += f"\n- [{title}]({link})"
            if snippet:
                digest += f"\n  _{snippet}_"
        total_found += len(matches)

if total_found == 0:
    digest += "\n\n_No relevant mentions found today._"

send_telegram(digest)
