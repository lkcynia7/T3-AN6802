from flask import Flask, request, render_template, redirect
import requests
import sqlite3
import datetime
import google.generativeai as genai
import os
import wikipedia
import time
import threading

api = os.getenv("makersuite")
model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key=api)

TELEGRAM_API = os.getenv("lkcynia_bot")
# TELEGRAM_API = ""
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_API}/"

app = Flask(__name__)
flag = 1

@app.route("/", methods=["POST","GET"])
def index():
    return render_template("index.html")

@app.route("/main", methods=["POST","GET"])
def main():
    global flag
    if flag == 1:
        t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_name = request.form.get("q")
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("insert into user (name, timestamp) values (?, ?)", (user_name, t))
        conn.commit()
        c.close()
        conn.close
        flag = 0
    return render_template("main.html")

@app.route("/foodexp", methods=["POST","GET"])
def foodexp():
    return render_template("foodexp.html")

@app.route("/foodexp1", methods=["POST","GET"])
def foodexp1():
    return render_template("foodexp1.html")

@app.route("/foodexp2", methods=["POST","GET"])
def foodexp2():
    return render_template("foodexp2.html")

@app.route("/foodexp_pred", methods=["POST","GET"])
def foodexp_pred():
    q = float(request.form.get("q"))
    return render_template("foodexp_pred.html", r=(q*0.4815)+147.4)

@app.route("/ethical_test", methods=["POST","GET"])
def ethical_test():
    return render_template("ethical_test.html")

@app.route("/test_result", methods=["POST","GET"])
def test_result():
    answer = request.form.get("answer")
    if answer == "false":
        return(render_template("pass.html"))
    elif answer == "true":
        return render_template("fail.html")

@app.route("/FAQ", methods=["POST","GET"])
def FAQ():
    return render_template("FAQ.html")

@app.route("/FAQ1", methods=["POST","GET"])
def FAQ1():
    r = model.generate_content("Factors for Profit")
    return render_template("FAQ1.html", r=r)
    
@app.route("/FAQinput", methods=["POST","GET"])
def FAQinput():
    q = request.form.get("q")
    r = wikipedia.summary(q)
    return render_template("FAQinput.html", r=r)

@app.route("/telegram", methods=["POST", "GET"])
def telegram():
    def start_bot():
        updates_url = BASE_URL + "getUpdates"
        print("Waiting for user to send the first message...")

        chat_id = None
        last_update_id = None

        # 等待用户发送第一条消息以获取 chat_id
        while not chat_id:
            try:
                r = requests.get(updates_url).json()
                if "result" in r and len(r["result"]) > 0:
                    last_msg = r["result"][-1]["message"]
                    chat_id = last_msg["chat"]["id"]
                    last_update_id = r["result"][-1]["update_id"]
                    print("Chat ID acquired:", chat_id)
            except Exception as e:
                print("Error getting updates:", e)
            time.sleep(2)

        prompt = "Please enter the inflation rate in % (type exit to break)"
        err_msg = "Please enter a valid number (type exit to break)"

        # 第一次发送提示语
        requests.get(BASE_URL + f"sendMessage?chat_id={chat_id}&text={prompt}")

        flag = ""

        while True:
            time.sleep(2)
            try:
                r = requests.get(updates_url).json()
                if "result" not in r or len(r["result"]) == 0:
                    continue

                new_messages = [msg for msg in r["result"] if msg["update_id"] > last_update_id]
                if not new_messages:
                    continue

                last_msg = new_messages[-1]["message"]
                user_input = last_msg["text"]
                last_update_id = new_messages[-1]["update_id"]

                print("User input:", user_input)

                if user_input.lower() == "exit":
                    break
                elif user_input.replace(".", "", 1).isdigit():
                    # 输入有效数字，计算利率
                    reply = f"The predicted interest rate is {float(user_input) + 1.5}"
                    # 回复用户预测利率并重新提示
                    requests.get(BASE_URL + f"sendMessage?chat_id={chat_id}&text={reply}")
                    requests.get(BASE_URL + f"sendMessage?chat_id={chat_id}&text={prompt}")
                else:
                    # 输入无效数字，提示重新输入
                    requests.get(BASE_URL + f"sendMessage?chat_id={chat_id}&text={err_msg}")
            
            except Exception as e:
                print("Error during processing:", e)

    # 启动线程运行 bot（非阻塞）
    threading.Thread(target=start_bot).start()
    return redirect("https://t.me/lkcynia_bot")

@app.route("/userLog", methods=["POST","GET"])
def userLog():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("select * from user")
    r = ""
    for row in c:
        r = r + str(row) + "\n"
    print(r)
    c.close()
    conn.close
    return render_template("userLog.html", r=r)

@app.route("/deleteLog", methods=["POST","GET"])
def deleteLog():
    # where name = 'xia xai'
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("""
    delete from user
    """)
    conn.commit()
    c.close()
    conn.close
    return render_template("deleteLog.html")

if __name__ == "__main__":

    app.run()
