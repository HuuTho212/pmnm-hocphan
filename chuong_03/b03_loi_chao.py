from flask import Flask
from markupsafe import escape
app = Flask(__name__)

@app.route("/hello/", defaults={"name":"bạn"})
@app.route("/hello/<name>")
def hello(name):
    return f"Xin chào, {escape(name)}!"
