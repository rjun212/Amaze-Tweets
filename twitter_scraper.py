import subprocess
import re
import requests
from datetime import datetime
import os

# Secrets from GitHub environment
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

authors = [
    "MLiebreich", "NatBullard", "JesseJenkins", "AukeHoekstra", "JigarShahDC",
    "JessePaltan", "AndrewDessler", "NickVanOsdol", "SamButlerSloss",
    "janrosenow", "TomSteyer", "AkshatRathi"
]
keywords = ["renewable", "solar", "wind", "grid", "power", "energy", "hydrogen", "battery", "electricity", "India"]

def contains_keywords(text):
    return any(re.search(rf"\b{kw}\b", text, re.IGNORECASE) for kw in keywords)

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    requests.post(url, data=payload)

for author in authors:
    print(f"\n🔍 Scanning tweets by @{author}...")
    cmd = f"snscrape --max-results 10 twitter-user:{author}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    tweets = result.stdout.splitlines()

    for tweet in tweets:
        if contains_keywords(tweet):
            print(f"✅ Match: {tweet}")
            send_telegram(f"🧠 @{author}:\n{tweet}")
