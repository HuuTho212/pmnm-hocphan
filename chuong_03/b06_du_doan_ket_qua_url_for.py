from flask import Flask, url_for
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def index():
    return "Trang chủ"

@app.route("/about")
def about():
    return "Giới thiệu"

@app.route("/post/<int:post_id>")
def post_detail(post_id):
    return f"Bài viết số {post_id}"

@app.route("/user/<username>")
def user_profile(username):
    return f"Trang cá nhân của {escape(username)}"

@app.route("/search")
def search():
    return "Tìm kiếm"

@app.route("/menu")
def menu():
    links = [
        ("Trang chủ", url_for("index")),
        ("Giới thiệu", url_for("about")),
        ("Bài viết số 7", url_for("post_detail", post_id=7)),
        ("Trang của An", url_for("user_profile", username="an")),
        ("Tìm kiếm flask", url_for("search", q="flask")),
    ]
    items = "".join(f'<li><a href="{href}">{label}</a></li>' for label, href in links)
    return f"<h1>Menu</h1><ul>{items}</ul>"