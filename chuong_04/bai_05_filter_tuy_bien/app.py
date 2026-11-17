from datetime import date

from flask import Flask, render_template

app = Flask(__name__)


@app.template_filter("vnd")
def format_vnd(value):
    """1500000 -> '1.500.000 ₫'"""
    if value is None:
        return ""
    return f"{value:,.0f}".replace(",", ".") + " ₫"


@app.template_filter("ngay")
def format_date(value, fmt="%d/%m/%Y"):
    """Định dạng ngày; None -> chuỗi rỗng."""
    if value is None:
        return ""
    return value.strftime(fmt)


PRODUCTS = [
    {"ten": "Bàn phím cơ", "gia": 1500000, "nhap": date(2026, 9, 5)},
    {"ten": "Chuột không dây", "gia": 350000, "nhap": date(2026, 8, 20)},
    {"ten": "Màn hình 24 inch", "gia": 3290000, "nhap": None},
    {"ten": "Tai nghe", "gia": 890000, "nhap": date(2026, 10, 1)},
]


@app.route("/")
def index():
    return render_template("san_pham.html", products=PRODUCTS)
