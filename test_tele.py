import os
import requests

token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()

print("--- Telegram Connection Test ---")
print(f"TELEGRAM_BOT_TOKEN set: {bool(token)}")
if token and ":" not in token:
    print("WARNING: TELEGRAM_BOT_TOKEN does not contain a colon (:). It might be incomplete.")

print(f"TELEGRAM_CHAT_ID set: {bool(chat_id)}")

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
            if res.status_code == 401:
                print("Hint: 401 Unauthorized means your BOT TOKEN is wrong.")
            elif res.status_code == 400:
                print("Hint: 400 Bad Request usually means your CHAT ID is wrong or you haven't started the bot.")
    except Exception as e:
        print(f"Exception occurred: {e}")
