import requests
from bs4 import BeautifulSoup
import os
import sys

# 설정
URL = "https://www.mma.go.kr/board/boardList.do?gesipan_id=95&mc=usr0000152"
BASE_URL = "https://www.mma.go.kr"
LAST_POST_FILE = "last_post.txt"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram tokens are not set. Skipping notification.")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload)
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
        
        # 게시판 테이블 찾기
        table = soup.find("table", class_="board_list")
        if not table:
            print("Could not find the board table.")
            return
        
        # 첫 번째 행 찾기 (공지 제외하고 싶다면 추가 로직 필요)
        # 여기서는 단순히 첫 번째 데이터 행을 가져옵니다.
        rows = table.find("tbody").find_all("tr")
        if not rows:
            print("No posts found.")
            return
        
        # 가장 최근 게시물 (보통 첫 번째 행)
        latest_row = rows[0]
        
        # 제목 및 링크 추출
        title_tag = latest_row.find("td", class_="t_left").find("a")
        if not title_tag:
            print("Could not find title tag.")
            return
            
        title = title_tag.text.strip()
        link = BASE_URL + title_tag["href"]
        
        # 게시글 고유 ID 추출 (ntt_id 파라미터 등)
        # 예: /board/boardView.do?gesipan_id=95&gs_id=&ntt_id=123456...
        import urllib.parse
        parsed_url = urllib.parse.urlparse(link)
        params = urllib.parse.parse_qs(parsed_url.query)
        post_id = params.get("ntt_id", [title])[0] # ntt_id가 없으면 제목을 ID로 사용
        
        print(f"Latest Post ID: {post_id}")
        print(f"Title: {title}")
        
        # 이전에 저장된 ID와 비교
        last_id = ""
        if os.path.exists(LAST_POST_FILE):
            with open(LAST_POST_FILE, "r", encoding="utf-8") as f:
                last_id = f.read().strip()
        
        if post_id != last_id:
            print("New post detected!")
            message = f"<b>[공군 모집 새 공고]</b>\n\n{title}\n\n<a href='{link}'>바로가기</a>"
            send_telegram_message(message)
            
            # 새로운 ID 저장
            with open(LAST_POST_FILE, "w", encoding="utf-8") as f:
                f.write(post_id)
        else:
            print("No new posts.")
            
    except Exception as e:
        print(f"An error occurred during scraping: {e}")

if __name__ == "__main__":
    scrape()
