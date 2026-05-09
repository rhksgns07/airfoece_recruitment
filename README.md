# 공군 모집 알림 봇 (Air Force Recruitment Bot)

병무청 사이트의 공군 모집계획 게시판을 감시하고, 새로운 공고가 올라오면 텔레그램으로 알림을 보내는 GitHub Action입니다.

## 🛠 설정 방법

### 1. 텔레그램 봇 생성 및 ID 확인
1.  텔레그램에서 [@BotFather](https://t.me/botfather)에게 `/newbot`을 입력하여 봇을 만듭니다.
2.  받은 **API Token**을 따로 적어둡니다.
3.  [@userinfobot](https://t.me/userinfobot)에게 아무 메세지나 보내 본인의 **Chat ID**를 확인합니다.

### 2. GitHub 저장소 설정
1.  이 코드를 본인의 GitHub 저장소(Repository)에 올립니다.
2.  저장소의 **Settings** -> **Secrets and variables** -> **Actions**로 이동합니다.
3.  **New repository secret**을 클릭하여 다음 두 가지를 추가합니다:
    *   `TELEGRAM_BOT_TOKEN`: 위에서 받은 API Token
    *   `TELEGRAM_CHAT_ID`: 위에서 확인한 Chat ID

### 3. 작동 방식
*   GitHub Actions가 6시간마다 자동으로 실행됩니다.
*   `last_post.txt` 파일을 통해 마지막 알림을 보낸 게시글을 기억합니다.
*   새로운 게시글이 발견되면 텔레그램으로 알림을 보내고 `last_post.txt`를 업데이트하여 저장소에 다시 저장합니다.

## 📝 참고 사항
*   동작을 테스트해보려면 저장소의 **Actions** 탭에서 `Check Air Force Recruitment` 워크플로우를 선택하고 **Run workflow**를 클릭하여 수동으로 실행해 볼 수 있습니다.
