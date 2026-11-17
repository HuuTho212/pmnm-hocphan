"""Bài 4: kiểm tra dự đoán kết quả filter bằng render_template_string."""
from flask import Flask, render_template_string

app = Flask(__name__)

CONTEXT = dict(
    name="nguyễn an",
    bio="Sinh viên năm ba ngành Công nghệ thông tin",
    skills=["Python", "Flask", "Git"],
    score=7,
)

BIEU_THUC = {
    "a": '{{ name|upper }}',
    "b": '{{ name|title }}',
    "c": '{{ bio|truncate(20) }}',
    "d": '{{ nickname|default("chưa có") }}',
    "e": '{{ skills|join(", ") }}',
    "f": '{{ skills|length }}',
    "g": '{{ 3.14159|round(2) }}',
    "h": '{{ "%05d"|format(42) }}',
    "i": '{{ "<b>Chào</b>" }}',
    "j": '{{ "<b>Chào</b>"|striptags }}',
    "k": '{{ score is odd }}',
    "l": '{{ skills|sort|join(" < ") }}',
}

if __name__ == "__main__":
    with app.test_request_context():
        for key, expr in BIEU_THUC.items():
            kq = render_template_string(expr, **CONTEXT)
            print(f"{key}  {expr:<42} -> {kq!r}")
