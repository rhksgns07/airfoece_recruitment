import os
import requests

token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

print("--- Telegram Connection Test ---")
print(f"TELEGRAM_BOT_TOKEN: {'Set (starts with ' + token[:5] + '...)' if token else 'NOT SET'}")
print(f"TELEGRAM_CHAT_ID: {'Set (' + chat_id + ')' if chat_id else 'NOT SET'}")

if not token or not chat_id:
    print("Error: Secrets are not properly set in GitHub.")
else:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        res = requests.post(url, json={"chat_id": chat_id, "text": "✅ 공군 모집 알림 봇 테스트 메세지입니다!"})
        print(f"HTTP Status: {res.status_code}")
        print(f"Response Body: {res.text}")
        if res.status_code == 200:
            print("Success! Check your Telegram.")
        else:
            print("Failed. Check the error message above.")
    except Exception as e:
        print(f"Exception occurred: {e}")
