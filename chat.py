
import anthropic
import time  
from dotenv import load_dotenv
import os
import database

# 会話履歴
conversation_history = []

def chat(user_questions):
    # .envファイルを読み込む
    load_dotenv()  
    # Claudeに接続する準備(API)
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    # データベースを作成
    database.setup_database()


    # ユーザーの質問を受け取る
    user_input = user_questions

    # 履歴にユーザーの質問を追加 
    conversation_history.append({
        "role":"user",
        "content":user_input
    })
    # ユーザーの質問をデータベースに保存をする
    database.save_message("user",user_input)


    # Claudeに質問を送って1文字ずつ表示する
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
            full_response += text


    # Claudeの返答も履歴に追加 
    conversation_history.append({
        "role":"assistant",
        "content":full_response
    })
    # Claudeの返答をデータベースに保存をする
    database.save_message("assistant",full_response)

    return conversation_history



if __name__=="__main__":
    chat()