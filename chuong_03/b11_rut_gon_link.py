from flask import Flask, abort, redirect, url_for

app = Flask(__name__)

LINKS = {
    "flask": "https://flask.palletsprojects.com",
    "python": "https://www.python.org",
    "github": "https://github.com",
    "osi": "https://opensource.org",
}


@app.route("/go/<code>")
def go(code):
    url = LINKS.get(code.lower())  # không phân biệt hoa thường
    if url is None:
        abort(404)
    return redirect(url, code=302)


@app.errorhandler(404)
def not_found(e):
    html = (
        "<h1>404 - Không tìm thấy</h1>"
        "<p>Mã liên kết không tồn tại.</p>"
        f'<p><a href="{url_for("links")}">Xem danh sách các liên kết</a></p>'
    )
    return html, 404


@app.route("/links")
def links():
    items = ""
    for code, url in LINKS.items():
        items += f'<li><a href="{url_for("go", code=code)}">/go/{code}</a> &rarr; {url}</li>'
    return f"<h1>Danh sách liên kết</h1><ul>{items}</ul>"