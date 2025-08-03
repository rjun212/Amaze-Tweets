
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

RELEVANT_KEYWORDS = ["renewable", "energy", "electricity", "batteries", "power"]
TRUSTED_DOMAINS = [
    "bloomberg.com", "iea.org", "irena.org", "carbonbrief.org",
    "canarymedia.com", "cleantechnica.com", "etenergyworld.com", "substack.com"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def is_relevant(title, link):
    title_match = any(kw in title.lower() for kw in RELEVANT_KEYWORDS)
    link_match = any(kw in link.lower() for kw in RELEVANT_KEYWORDS)
    domain_match = any(domain in link for domain in TRUSTED_DOMAINS)
    return (title_match or link_match) and domain_match

def bing_search(query):
    url = f"https://www.bing.com/search?q={requests.utils.quote(query)}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    results = []
    for item in soup.select(".b_algo h2 a")[:6]:
        title = item.get_text(strip=True)
        link = item["href"]
        if is_relevant(title, link):
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

digest = f"🗞️ *Filtered Report Titles – {datetime.now().strftime('%b %d')}*"
total_found = 0

for author in authors:
    query = f'"{author}" renewable OR grid OR energy OR power OR electricity OR climate'
    matches = bing_search(query)
    if matches:
        digest += f"\n\n🔍 *{author}*"
        for title, link in matches:
            digest += f"\n- [{title}]({link})"
        total_found += len(matches)

if total_found == 0:
    digest += "\n\n_No relevant report titles found today._"

send_telegram(digest)
