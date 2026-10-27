from flask import Flask, request, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return f'<a href="{url_for("index")}">Trang chủ</a> | <a href="{url_for("contact")}">Liên hệ</a>'


@app.route("/about")
def about():
    return "Giới thiệu"


@app.route("/post/<int:post_id>")
def post(post_id):
    return f"Bài viết số {post_id}"


@app.route("/grade/<int:score>")
def grade(score):
    if score >= 8:
        return "Giỏi"
    if score >= 5:
        return "Đạt"
    return "Chưa đạt"


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return "Đã gửi liên hệ"
    return '<form method="post"><button>Gửi liên hệ</button></form>'