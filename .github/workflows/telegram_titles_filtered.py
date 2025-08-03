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

KEYWORDS = ["renewable", "energy", "electricity", "batteries", "power"]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def bing_search(query):
    url = f"https://www.bing.com/search?q={requests.utils.quote(query)}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    results = []
    for item in soup.select(".b_algo h2 a")[:5]:
        title = item.get_text(strip=True)
        link = item["href"]
        if any(keyword in title.lower() for keyword in KEYWORDS):
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
    query = f'"{author}" {TOPIC_FILTER}'
    matches = bing_search(query)
    if matches:
        digest += f"\n\n🔍 *{author}*"
        for title, link in matches:
            digest += f"\n- [{title}]({link})"
        total_found += len(matches)

if total_found == 0:
    digest += "\n\n_No relevant titles found today._"

send_telegram(digest)
