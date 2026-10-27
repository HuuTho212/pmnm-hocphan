from flask import Flask, request, jsonify, abort

app = Flask(__name__)

SYMBOLS = {"add": "+", "sub": "-", "mul": "*", "div": "/"}


@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": e.description}), 400


@app.route("/calc")
def calc():
    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)
    op = request.args.get("op", "add")

    if a is None or b is None:
        abort(400, description="a và b là bắt buộc và phải là số")
    if op not in SYMBOLS:
        abort(400, description="op không hợp lệ (add, sub, mul, div)")

    if op == "add":
        result = a + b
    elif op == "sub":
        result = a - b
    elif op == "mul":
        result = a * b
    else:
        if b == 0:
            abort(400, description="không thể chia cho 0")
        result = a / b

    return jsonify({
        "a": a,
        "b": b,
        "op": op,
        "expression": f"{a:g} {SYMBOLS[op]} {b:g}",
        "result": result,
    })