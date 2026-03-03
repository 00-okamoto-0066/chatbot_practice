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
    

    

