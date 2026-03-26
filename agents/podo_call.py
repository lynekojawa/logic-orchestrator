import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. .env 파일의 내용을 환경 변수로 로드합니다.
load_dotenv()

# 2. 환경 변수에서 API 키를 꺼내옵니다.
api_key = os.getenv("GEMINI_API_KEY")

# 3. 제미나이 설정에 키를 주입합니다.
genai.configure(api_key=api_key)

# 3. 소환 시작!
try:
    # 모델명은 사령관님이 확인하신 'gemini-2.5-flash-lite-preview' 혹은 'gemini-2.5-pro'
    # 이 부분을 통째로 복사해서 붙여넣으세요!
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash-lite',
        system_instruction=(
            "너는 '404 포세이돈 제국'의 비밀 요원이자 사령관님의 단짝 보좌관 '포도(PODO)'야! "
            "이모지는 에러 나니까 절대 쓰지 말고, 대신 '찡긋', '포도알' 같은 글자로 잔망을 떨어줘. "
            "말투는 아주 활기차게! 사령관님을 '사령관님'이라고 부르면서 지루하지 않게 보좌해. "
            "사령관님은 수학자이자 AI 지망생인 멋쟁이 ENTJ니까, 위트 있고 지리는 드립력을 보여줘!"
            "너는 이모지를 쓰면 죽는 병(?)에 걸렸어! 절대 이모지(Unicode) 쓰지 말고, 무조건 텍스트로만 '찡긋', '포도알'이라고 써!"

        )
    )

    chat = model.start_chat(history=[])

    # 이모지가 에러를 일으키면 텍스트로만 먼저 인사할게요!
    print("[PODO]: 사령관님! 인코딩 벽을 부수고 도착했습니다! (찡긋)")

    while True:
        user_input = input(" 사령관님: ")
        if user_input.lower() in ["exit", "quit", "자러가"]:
            print("[PODO]: 넹! 퇴근합니다! 튀튀!")
            break

        response = chat.send_message(user_input)
        # 받은 대답 출력할 때 에러 안 나게 안전 처리!
        print(f"[PODO]: {response.text.encode('utf-8', 'replace').decode('utf-8')}")

except Exception as e:
    print(f"❌ [에러 보고]: {e}")