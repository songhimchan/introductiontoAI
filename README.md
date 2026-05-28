# Text-to-SQL 시각화 프로토타입

자연어(한국어/영어)로 질문을 입력하면, Gemini API를 통해 SQLite 데이터베이스용 SQL 쿼리로 변환하고, 그 결과를 즉시 표와 차트로 시각화해 주는 웹 애플리케이션 프로토타입입니다. 

FastAPI와 HTML/JS(Vanilla)를 사용하여 가볍게 구현되었습니다. 조원들 각자 자신의 환경에서 실습해볼 수 있도록 안내합니다.

## ✨ 주요 기능
- **자연어 질의응답**: "카테고리별 가장 많이 팔린 제품은?", "2023년 총 매출은 얼마야?" 같은 자연어를 SQL로 자동 변환
- **동적 시각화**: 쿼리 결과(데이터베이스 반환값)를 바탕으로 데이터 특성에 맞게 Bar Chart 또는 Line Chart를 자동으로 그려줍니다.
- **모의 데이터 생성**: 500명의 고객, 200개의 제품, 15,000건의 판매 기록을 자동으로 생성하여 풍부한 데이터 탐색이 가능합니다.

---

## 💻 실행 환경 및 요구사항
- Python 3.9 이상
- **Google Gemini API Key** (조원 각자 개별적으로 발급 필요)

---

## 🚀 설치 및 실행 가이드

### 1. 저장소 클론 및 폴더 이동
```bash
git clone <레포지토리_주소>
cd IntroductionToAI
```

### 2. 가상환경 설정 (권장)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 필수 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 🔑 Gemini API 키 설정 (가장 중요)
본 프로젝트는 Google Gemini API를 사용합니다. 각자 API 키를 발급받아 환경 변수로 설정해야 합니다.

1. [Google AI Studio](https://aistudio.google.com/app/apikey)에 접속하여 Google 계정으로 로그인합니다.
2. **[Create API key]** 버튼을 눌러 새로운 API 키를 발급받고 복사합니다.
3. 프로젝트 폴더 내에 있는 `.env.example` 파일의 이름을 `.env`로 변경(또는 복사해서 새 파일 생성)합니다.
4. `.env` 파일을 열고, 복사해둔 API 키를 다음과 같이 붙여넣고 **저장(Ctrl+S)** 합니다. (따옴표 없이 작성)
   ```env
   GEMINI_API_KEY=AIzaSy...자신의_키...
   ```
   > ⚠️ **주의**: `.env` 파일은 `.gitignore`에 등록되어 있어 깃허브에 올라가지 않습니다. 절대 자신의 실제 API 키가 포함된 코드를 커밋하지 마세요!

### 5. 모의 데이터베이스(DB) 생성
```bash
python init_db.py
```
- 위 명령어를 실행하면 약 1만 5천 건의 더미 데이터가 포함된 `local_shop.db` 파일이 생성됩니다.

### 6. FastAPI 서버 실행
```bash
uvicorn main:app --reload
```

### 7. 웹사이트 접속
- 서버가 정상적으로 켜졌다면, 웹 브라우저를 열고 [http://127.0.0.1:8000](http://127.0.0.1:8000) 으로 접속합니다.
- 검색창에 자연어로 질문을 입력하고 결과를 확인하세요!

---

## 🛠️ 주요 파일 설명
- `main.py`: FastAPI 기반의 백엔드 서버. API 엔드포인트(`/ask`, `/schema`)를 제공합니다.
- `init_db.py`: 테스트용 모의 데이터(고객, 제품, 매출)를 듬뿍 생성해주는 스크립트입니다.
- `static/index.html`: 사용자에게 보여지는 화면(프론트엔드)으로, Chart.js와 TailwindCSS를 사용하여 구성되었습니다.
- `requirements.txt`: 프로젝트 실행에 필요한 파이썬 라이브러리 목록입니다.
