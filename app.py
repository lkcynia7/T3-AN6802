from flask import Flask, request, render_template
import requests
import sqlite3
import datetime
import google.generativeai as genai
import os
import wikipedia
import time

api = os.getenv("makersuite")
model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key=api)

TELEGRAM_API = os.getenv("lkcynia_bot")
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

@app.route('/telegram', methods=['GET','POST'])
def telegram():
    #grab id
    time.sleep(5) #ensure telegram is activated
    response = requests.get(BASE_URL + 'getUpdates')
    data = response.json()
    text = data['result'][-1]['message']['text']
    chat_id = data['result'][-1]['message']['chat']['id']
    print("Text:", text)
    print("Chat ID:", chat_id)
    send_url = BASE_URL + f'sendMessage?chat_id={chat_id}&text={"Welcome to prediction, please enter the salary"}'
    requests.get(send_url)
    time.sleep(6)
    response = requests.get(BASE_URL + 'getUpdates')
    data = response.json()
    text = data['result'][-1]['message']['text']
    if text.isnumeric():
        msg = str(float(text) * 0.2 + 100)
        send_url = BASE_URL + f'sendMessage?chat_id={chat_id}&text={msg}'
        requests.get(send_url)
    else:
        msg = "salary must be a number"
        send_url = BASE_URL + f'sendMessage?chat_id={chat_id}&text={msg}'
        requests.get(send_url)
        send_url = BASE_URL + f'sendMessage?chat_id={chat_id}&text={"Welcome to prediction, please enter the salary"}'
        requests.get(send_url)
        time.sleep(3)
    return(render_template("telegram.html"))


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
