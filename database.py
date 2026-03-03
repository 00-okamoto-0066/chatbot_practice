import sqlite3

DB_FILE = "chat_history.db"

#データベースの準備
def setup_database():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    # historyテーブルがなければ作成する
    cur.execute(""" 
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY,
        role TEXT,
        content TEXT
    )
    """)

    con.commit()
    con.close()



# 会話をデータベースに保存をする
def save_message(role,content):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    # 会話内容をhistoryテーブルに追加する
    cur.execute(""" 
    INSERT INTO history(role,content)
    VALUES(?,?)
    """,(role,content)
    )

    con.commit()
    con.close()
    
    

# 過去の履歴を読み込む
def load_history():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    # historyテーブルから全件取得する
    cur.execute(""" 
    SELECT role,content FROM history ORDER BY id 
    """
    )
    
    conversation_history_list = cur.fetchall()
    
    
    conversation_history = []
    # Claudeに渡せる形にデータを変換
    for rows in conversation_history_list:
        # 履歴に過去のやりとりを追加 
        conversation_history.append({
            "role":rows[0],
            "content":rows[1]
        })

    con.close()
    
    
    return conversation_history

