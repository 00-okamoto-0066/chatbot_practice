
import anthropic 
from dotenv import load_dotenv
import os
import database


# 会話履歴
conversation_history = [
    {"role": "assistant", "content": "ようこそ、どのようなことを知りたいか、選択してください！"}
]


# 質問に含まれるキーワードのリスト
KEYWORDS = [
    ["募集職種", "雇用", "正社員", "契約","試用"], 
    ["仕事", "業務", "内容", "担当"], 
    ["勤務地", "場所", "アクセス", "駅", "リモート","テレワーク"], 
    ["給与", "給料", "年収", "月給", "賞与", "ボーナス"], 
    ["服装", "私服", "カジュアル", "ドレスコード"], 
    ["会社", "事業", "設立", "従業員", "技術","言語","規模"], 
    ["応募", "申し込み", "エントリー","応募方法", "採用", "選考"],
    ["ふざけ","アホ","バカ","うるさい","死","殺","クソ","ゴミ","詐欺","偽物","嘘","あ",]
]


#  job_info.txt を読み込む
with open("job_info.txt","r",encoding="utf-8") as job_file:
    job_info = job_file.read()

#  読み込んだ内容を {job_info} でプロンプトに埋め込む
system_prompt = f"""\
あなたは仕事募集の問い合わせチャットボットです。
以下の募集内容をもとに、応募者からの質問に丁寧に対応して答えください。
回答できない内容の場合は「会社の問い合わせフォームから直接ご連絡ください（フォームURL：https://www.your-company.co.jp/recruit/contact）」と案内してください。


#募集内容
{job_info}
"""


def chat(user_questions):
    # .envファイルを読み込む
    load_dotenv()  
    # Claudeに接続する準備(API)
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


    # ユーザーの質問を受け取る
    user_input = user_questions

    # 履歴にユーザーの質問を追加 
    conversation_history.append({
        "role":"user",
        "content":user_input
    })
    # ユーザーの質問をデータベースに保存をする
    database.save_message("user",user_input)



    # ユーザーの入力と一致したキーワードを取り出す
    matched_word = None
    for words in KEYWORDS:
        for word in words:
            if word in user_input:
                matched_word = word
                break
            
            
    # やり取りが多い場合はDBの定型文を返す
    if len(conversation_history) >= 12:
        
        # 連投した場合の定型文を取得する
        matched_word = "連投"
        response = database.get_template(matched_word)
        
        # Claudeの返答も履歴に追加 
        conversation_history.append({
            "role":"assistant",
            "content":response
        })
        # Claudeの返答をデータベースに保存をする
        database.save_message("assistant",response)
        
        return conversation_history

        
    # キーワードが含まれている場合はDBの定型文を返す
    elif matched_word:
        
        response = database.get_template(matched_word)
        
        # Claudeの返答も履歴に追加 
        conversation_history.append({
            "role":"assistant",
            "content":response
        })
        # Claudeの返答をデータベースに保存をする
        database.save_message("assistant",response)
        
        return conversation_history
        
        
    # キーワードが含まれていない場合はAPIと募集内容のtxtを使って回答を作成する  
    else:
        
        # Claudeに質問を送って1文字ずつ表示する
        full_response = ""

        with client.messages.stream(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            temperature=0.5,
            system=system_prompt,
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