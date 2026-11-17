from datetime import date

from flask import Flask, render_template, request
from jinja2 import UndefinedError

app = Flask(__name__)

MENU = [("index", "Trang chủ"), ("about", "Giới thiệu"), ("contact", "Liên hệ")]


@app.context_processor
def inject_globals():
    def is_active(endpoint):
        return "active" if request.endpoint == endpoint else ""

    return {
        "menu": MENU,
        "site_name": "Menu Demo",
        "current_year": date.today().year,
        "is_active": is_active,
    }


@app.route("/")
def index():
    return render_template("page.html", title="Trang chủ")


@app.route("/about")
def about():
    return render_template("page.html", title="Giới thiệu")


@app.route("/contact")
def contact():
    return render_template("page.html", title="Liên hệ")


@app.route("/thu-macro/<cach>")
def thu_macro(cach):
    if cach not in ("khong-context", "with-context"):
        return "Dùng /thu-macro/khong-context hoặc /thu-macro/with-context", 404
    try:
        return render_template(f"thu_macro_{cach.replace('-', '_')}.html")
    except UndefinedError as e:
        return f"UndefinedError: {e}", 500
