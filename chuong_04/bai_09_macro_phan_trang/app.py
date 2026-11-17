import math

from flask import Flask, abort, render_template, request

app = Flask(__name__)

ITEMS = [f"Mục {i}" for i in range(1, 96)]        
USERS = [f"Người dùng {i}" for i in range(1, 34)]
PER_PAGE = 10


def paginate(items, per_page=PER_PAGE):
    raw = request.args.get("page", "1")
    if not raw.isdigit():
        abort(404)
    page = int(raw)
    total_pages = max(1, math.ceil(len(items) / per_page))
    if page < 1 or page > total_pages:
        abort(404)
    start = (page - 1) * per_page
    return items[start:start + per_page], page, total_pages


@app.route("/items")
def items():
    rows, page, total_pages = paginate(ITEMS)
    return render_template("danh_sach.html", title="Danh sách mục", rows=rows,
                           page=page, total_pages=total_pages, endpoint="items")


@app.route("/users")
def users():
    rows, page, total_pages = paginate(USERS)
    return render_template("danh_sach.html", title="Danh sách người dùng", rows=rows,
                           page=page, total_pages=total_pages, endpoint="users")
