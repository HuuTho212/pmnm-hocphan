"""Bài 8 – Thông tin request: /info nhận cả GET và POST.

Chạy:  flask --app b08_thong_tin_request run --debug --port 8000
Thử:   /info?x=1&y=2      curl http://127.0.0.1:8000/info?x=1&y=2
       curl -X POST http://127.0.0.1:8000/info
"""
from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/info", methods=["GET", "POST"])
def info():
    rows = [
        ("Phương thức", request.method),
        ("Đường dẫn", request.path),
        ("Đường dẫn kèm query", request.full_path),
        ("URL đầy đủ", request.url),
        ("Địa chỉ IP", request.remote_addr),
        ("User-Agent", request.headers.get("User-Agent", "(không có)")),
        ("Tham số query", request.args.to_dict(flat=False)),
    ]
    body = "".join(
        f"<tr><th>{escape(name)}</th><td>{escape(value)}</td></tr>" for name, value in rows
    )
    return f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><title>Thông tin request</title></head>
<body>
<h1>Thông tin request</h1>
<table border="1" cellpadding="6">{body}</table>
</body></html>"""