from flask import Flask, render_template

app = Flask(__name__)


@app.template_filter("vnd")
def format_vnd(value):
    return "" if value is None else f"{value:,.0f}".replace(",", ".") + " ₫"


PRODUCTS = [
    {"ten": "Bàn phím cơ", "gia": 1500000, "con_hang": True},
    {"ten": "Chuột không dây", "gia": 350000, "con_hang": True},
    {"ten": "Màn hình 24 inch", "gia": 3290000, "con_hang": False},
    {"ten": "Tai nghe chụp tai", "gia": 890000, "con_hang": True},
    {"ten": "Webcam Full HD", "gia": 640000, "con_hang": False},
    {"ten": "Ổ cứng SSD 512GB", "gia": 1250000, "con_hang": True},
    {"ten": "Bộ chia USB-C", "gia": 420000, "con_hang": True},
    {"ten": "Đế tản nhiệt laptop", "gia": 280000, "con_hang": False},
]


@app.route("/")
def index():
    return render_template("san_pham.html", products=PRODUCTS)
