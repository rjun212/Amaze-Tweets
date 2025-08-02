import subprocess
import requests
import os

# Secrets from GitHub environment
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# Updated list of Twitter accounts
authors = [
    "MLiebreich", "NatBullard", "JesseJenkins", "AukeHoekstra", "JigarShahDC",
    "JessePaltan", "AndrewDessler", "NickVanOsdol", "SamButlerSloss",
    "janrosenow", "TomSteyer", "AkshatRathi", "BloombergNEF", "BloombergNRG"
]

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
        print(f"✅ Found tweet: {tweet}")
        send_telegram(f"🧠 @{author}:
{tweet}")

# Always confirm the run
send_telegram("✅ Bot ran successfully. All tweets forwarded.")
