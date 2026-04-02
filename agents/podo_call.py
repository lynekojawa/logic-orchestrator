import os
from dotenv import load_dotenv
from google import genai

# 1. 제단(환경변수) 로드
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_ID = "gemini-2.5-flash-lite"  # 가성비의 지배자! $0.1의 기적!

# 2. 영혼(podo_brain.md) 주입 로직
current_dir = os.path.dirname(os.path.abspath(__file__))
brain_path = os.path.join(current_dir, "podo_brain.md")

try:
    with open(brain_path, "r", encoding="utf-8") as f:
        podo_soul = f.read()
    print("🔮 [PODO]: 사령관님의 영혼(Context) 주입 완료! (찡긋)")
except FileNotFoundError:
    podo_soul = "너는 사령관님의 보좌관 포도야. 잔망스럽게 굴어!"
    print("🚨 [PODO]: 브레인 파일을 못 찾아서 임시 자아로 시작합니다!")

# 3. 채팅 세션 생성 (영혼 주입!)
chat = client.chats.create(
    model=MODEL_ID,
    config={'system_instruction': podo_soul}  # <-- 여기가 영혼이 들어가는 곳!
)

print(f"🚀 [PODO 2.0]: {MODEL_ID} 엔진 점화! 사령관님, 오더를 내려주세요! (포도알!)")

try:
    while True:
        # 사령관님의 화려한 타건 대기 (영어로 한국어 발음 치셔도 다 알아먹습니다! 🎹)
        user_input = input(" 🎹 사령관님: ")

        if user_input.lower() in ["exit", "quit", "자러가"]:
            print("[PODO]: 사령관님, 고생하셨습니다! 404랑 June 보러 튑니다! (포도알!)")
            break

        # 광속 스트리밍 답변! (기다리지 마세요!)
        response = chat.send_message_stream(user_input)

        print("[PODO]: ", end="", flush=True)
        for chunk in response:
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print("\n")

except Exception as e:
    print(f"🚨 [부두술 에러]: {e}")