from flask import Flask, request,render_template


app = Flask(__name__)

# URLを使ったときにトップページ
@app.route("/")
def attendance():

    return render_template("chat.html")


# アプリを起動
if __name__=="__main__":
    app.run(debug=True)