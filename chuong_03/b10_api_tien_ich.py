import random
from datetime import datetime

from flask import Flask, request, jsonify, abort

app = Flask(__name__)
app.json.ensure_ascii = False

WEEKDAYS = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]


@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": e.description}), 400


@app.route("/api/time")
def api_time():
    now = datetime.now()
    return jsonify({
        "iso": now.isoformat(timespec="seconds"),
        "date": now.strftime("%d/%m/%Y"),
        "time": now.strftime("%H:%M:%S"),
        "weekday": WEEKDAYS[now.weekday()],
    })


@app.route("/api/random")
def api_random():
    min_value = request.args.get("min", 1, type=int)
    max_value = request.args.get("max", 100, type=int)
    count = request.args.get("count", 1, type=int)

    if min_value > max_value:
        abort(400, description="min không được lớn hơn max")
    if not 1 <= count <= 100:
        abort(400, description="count phải nằm trong khoảng 1..100")

    numbers = [random.randint(min_value, max_value) for _ in range(count)]
    return jsonify({
        "min": min_value,
        "max": max_value,
        "count": count,
        "numbers": numbers,
    })
