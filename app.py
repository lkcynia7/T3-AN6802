from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["POST","GET"])
def index():
    return(render_template("index.html"))

@app.route("/main", methods=["POST","GET"])
def main():
    user_name = request.form.get("q")
    return(render_template("main.html"))

@app.route("/foodexp", methods=["POST","GET"])
def foodexp():
    return(render_template("foodexp.html"))

@app.route("/foodexp_pred", methods=["POST","GET"])
def foodexp_pred():
    q = float(request.form.get("q"))
    return(render_template("foodexp_pred.html", r=(q*0.4815)+147.4))

@app.route("/ethical_test", methods=["POST","GET"])
def ethical_test():
    return(render_template("ethical_test.html"))

@app.route("/test_result", methods=["POST","GET"])
def test_result():
    answer = request.form.get("answer")
    if answer == "false":
        return(render_template("pass.html"))
    elif answer == "true":
        return(render_template("fail.html"))

if __name__ == "__main__":
    app.run()
