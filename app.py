from flask import Flask, request, render_template
import sqlite3
import datetime
import google.generativeai as genai
import os
import wikipedia

api = os.get("makersuite")
model = genai.GenerativeModel("gemini-1.5-flash")
genai.configure(api_key=api)

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
