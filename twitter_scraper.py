import subprocess
import requests
import os
from datetime import datetime

# Secrets from GitHub environment
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# Final verified and updated list of Twitter accounts
authors = [
    "MLiebreich", "NatBullard", "JesseJenkins", "AukeHoekstra", "JigarShahDC",
    "JessePeltan", "AndrewDessler", "nickvanosdol", "SamButl3r", "janrosenow",
    "TomSteyer", "AkshatRathi", "BloombergNEF", "BloombergNRG"
]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

summary = f"🗓️ *Clean Energy Tweet Digest* – {datetime.now().strftime('%b %d')}"
tweet_count = 0

for author in authors:
    cmd = f"snscrape --max-results 5 twitter-user:{author}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    tweets = result.stdout.splitlines()

    if tweets:
        summary += f"\n\n*{author}*"
        for tweet in tweets:
            tweet_count += 1
            summary += f"\n- {tweet[:200]}..."

if tweet_count == 0:
    summary += "\n\n_No tweets found today._"

send_telegram(summary)
