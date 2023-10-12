from flask import Flask,render_template,redirect,url_for,request
from main import sync

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/send",methods=["POST"])
def syncronise():
    form = request.form
    code = sync(form["sp_url"],form["url"])
    if code == 200:
        return render_template("congrats.html")
    redirect(url_for("/"))
if __name__ == "__main__":
    app.run(debug=True)
