from flask import Flask, request, jsonify

app = Flask(__name__)
app.json.ensure_ascii = False

counter = 0 

@app.route("/counter", methods=["GET", "POST", "DELETE"])
def counter_view():
    global counter

    if request.method == "GET":
        return jsonify({"counter": counter})

    if request.method == "POST":
        step = request.args.get("step", 1, type=int)
        counter += step
        return jsonify({"counter": counter, "message": f"Đã tăng {step}"})
    
    counter = 0
    return "", 204