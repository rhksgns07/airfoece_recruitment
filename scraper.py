import requests
from bs4 import BeautifulSoup
import os
import sys
import urllib.parse
import html

# 설정
URL = "https://www.mma.go.kr/board/boardList.do?gesipan_id=95&mc=usr0000152"
BASE_URL = "https://www.mma.go.kr"
LAST_POST_FILE = "last_post.txt"

# 공백 제거 처리
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

def send_telegram_message(message):
    print("Attempting to send Telegram message...")
    if not TELEGRAM_BOT_TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN is missing! Please check GitHub Secrets.")
    if not TELEGRAM_CHAT_ID:
        print("ERROR: TELEGRAM_CHAT_ID is missing! Please check GitHub Secrets.")
        
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    
    # 봇 토큰 형식 체크 (숫자:알파벳 형태여야 함)
    if ":" not in TELEGRAM_BOT_TOKEN:
        print("CRITICAL ERROR: TELEGRAM_BOT_TOKEN is invalid. It must include the numeric prefix and a colon (e.g., 123456:ABCDEF).")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        response = requests.post(url, json=payload)
        print(f"Telegram API Response Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Telegram API Error Detail: {response.text}")
        response.raise_for_status()
        print("Telegram message sent successfully.")
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def scrape():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        table = soup.find("table", class_="board_list")
        if not table:
            print("Could not find the board table.")
            return
        
        rows = table.find("tbody").find_all("tr")
        if not rows:
            print("No posts found.")
            return
        
        latest_post = None
        
        for row in rows:
            # '공지' 아이콘이 있는지 확인 (공지는 건너뜜)
            notice_icon = row.find("span", class_="icon_notice")
            if notice_icon:
                continue
            
            # 공지가 아닌 첫 번째 행이 최신 공고
            title_tag = row.find("td", class_="t_left").find("a")
            if title_tag:
                title = title_tag.text.strip()
                link = BASE_URL + title_tag["href"]
                
                # ID 추출
                parsed_url = urllib.parse.urlparse(link)
                params = urllib.parse.parse_qs(parsed_url.query)
                post_id = params.get("ntt_id", [title])[0]
                
                latest_post = {
                    "id": post_id,
                    "title": title,
                    "link": link
                }
                break
        
        if not latest_post:
            print("Could not find any non-notice posts.")
            return

        print(f"Latest Post ID: {latest_post['id']}")
        print(f"Title: {latest_post['title']}")
        
        # 이전 ID와 비교
        last_id = ""
        if os.path.exists(LAST_POST_FILE):
            with open(LAST_POST_FILE, "r", encoding="utf-8") as f:
                last_id = f.read().strip()
        
        if latest_post['id'] != last_id:
            print("New post detected!")
            safe_title = html.escape(latest_post['title'])
            message = f"<b>[공군 모집 새 공고]</b>\n\n{safe_title}\n\n<a href='{latest_post['link']}'>👉 게시글 바로가기</a>"
            send_telegram_message(message)
            
            with open(LAST_POST_FILE, "w", encoding="utf-8") as f:
                f.write(latest_post['id'])
        else:
            print("No new posts.")
            
    except Exception as e:
        print(f"An error occurred during scraping: {e}")

if __name__ == "__main__":
    scrape()
