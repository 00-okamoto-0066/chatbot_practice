import anthropic
import time  
from dotenv import load_dotenv
import os
import database


# .envファイルを読み込む
load_dotenv()  
# Claudeに接続する準備(API)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
# データベースを作成
database.setup_database()


print("Claudeチャットボット（終了するには '終了' と入力）")
print("-" * 40)


# 過去の会話履歴を取得
conversation_history = database.load_history()

# ずっとチャットを続けるループ
while True:

    # キーボードから入力を受け取る
    user_input = input("あなた：")

     #「quit」と入力されたら終了
    if user_input == "終了":
        print("終了します")
        break


    # 履歴にユーザーの質問を追加 
    conversation_history.append({
        "role":"user",
        "content":user_input
    })
    # ユーザーの質問をデータベースに保存をする
    database.save_message("user",user_input)


    # Claudeに質問を送って1文字ずつ表示する
    print("Claude: ", end="")
    full_response = ""

    with client.messages.stream(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        temperature=0.5,
        system="あなたはClaudeが詳しいAIエンジニアです。",
        # 会話履歴の直近10件だけ渡す
        messages=conversation_history[-10:]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)  # できた文字をすぐ表示
            full_response += text
            time.sleep(0.05)  # 1文字ごとに0.1秒待つ（数字を変えると速さが変わる）


    # Claudeの返答も履歴に追加 
    conversation_history.append({
        "role":"assistant",
        "content":full_response
    })
    # Claudeの返答をデータベースに保存をする
    database.save_message("assistant",full_response)


    print()
    print("-" * 40)