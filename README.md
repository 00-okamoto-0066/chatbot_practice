# 仕事募集 問い合わせチャットボット

## 概要
Claude の API を使った採用情報の問い合わせチャットボットです。
トップページの吹き出しをクリックするとチャットパネルが開き、
募集内容について質問することができます。

## 使用技術
- Python
- Flask
- Anthropic
- SQLite

## 機能一覧
- 吹き出しをクリックすると画面右半分にチャットパネルが開き、✕ボタンで閉じることができる
- クイック選択ボタンまたは入力欄から質問ができる
- 質問の内容や回数に応じて柔軟な回答ができる

## フォルダ構成
```
chatbot_practice/
├── app.py              # Flask アプリのエントリーポイント
├── chat.py             # チャットの回答処理
├── database.py         # データベース接続・操作処理
├── setup_database.py   # データベースの初期設定
├── job_info.txt        # プロンプトで活用する資料
├── requirements.txt    # 使用ライブラリ一覧
├── README.md           # プロジェクトの説明書
├── .gitignore          # Git管理から除外するファイル
├── templates/
│   └── chat.html       # チャット画面
└── static/
    ├── style.css       # チャット画面のデザイン・レイアウト
    └── chat.js         # チャットの開閉・送信処理
```

## 環境構築

### 1. リポジトリをクローンする
```
git clone リポジトリのURL
```

### 2. ライブラリをインストールする
```
pip install -r requirements.txt
```

### 3. 環境変数を設定する
.env ファイルを作成して以下を記入してください。
```
ANTHROPIC_API_KEY=your_api_key
```

### 4. データベースをセットアップする
```
python setup_database.py
```

### 5. アプリを起動する
```
python app.py
```

### 6. ブラウザで開く
```
http://127.0.0.1:5000
```

## 注意事項
- `.env` ファイルは `.gitignore` に追加して GitHub に上げないようにしてください。