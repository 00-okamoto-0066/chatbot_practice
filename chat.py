import anthropic
import time  
from dotenv import load_dotenv
import os


# .envファイルを読み込む
load_dotenv()  
# Claudeに接続する準備
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

print("Claudeチャットボット（終了するには 'quit' と入力）")
print("-" * 40)



conversation_history = [] 

# ずっとチャットを続けるループ
while True:

    # キーボードから入力を受け取る
    user_input = input("あなた：")

     #「quit」と入力されたら終了
    if user_input == "quit":
        print("終了します")
        break


    # 履歴にユーザーの発言を追加 ← 追加
    conversation_history.append({
        "role":"user",
        "content":user_input
    })


    # Claudeに質問を送って1文字ずつ表示する
    print("Claude: ", end="")
    full_response = ""

    with client.messages.stream(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system="あなたは日本語の先生です。",
        messages=conversation_history
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)  # できた文字をすぐ表示
            full_response += text
            time.sleep(0.05)  # 1文字ごとに0.1秒待つ（数字を変えると速さが変わる）


    # Claudeの返答も履歴に追加 
    conversation_history.append({
        "role":"user",
        "content":full_response
    })

    print()
    print("-" * 40)