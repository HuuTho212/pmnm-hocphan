from flask import Flask, render_template, request, url_for, flash, session, redirect
app = Flask(__name__)

def parse_number(text):
    try:
        value = float(text.strip().replace(",","."))
    except ValueError:
        return None
    return value

def validate_score(text):
    value = parse_number(text)
    if value is None:
        return None, "Vui lòng nhập một số."
    if not 0 <= value <= 10:
        return None, "Điểm phải từ 0 đến 10."
    return value, None

@app.route("/")
def index():
    return render_template("base.html")

@app.route("/bmi", methods=["GET", "POST"])
def bmi():
    errors ={}
    result = None
    height_str =""
    weight_str =""
    if request.method == "POST":
        height_str = request.form.get("height")
        weight_str = request.form.get("weight")
        height = parse_number(height_str)
        weight = parse_number(weight_str)
        if height is None:
            errors["height"] = "Vui lòng nhập một số."
        elif not 50 <= height <=250:
            msg = "Giá trị phải từ 50 đến 250."
            if height <= 2.5:
                msg+= " (nhập mét thay vì cm)"
            errors["height"] = msg
        if weight is None:
            errors["weight"] = "Vui lòng nhập một số."
        elif not 10 <= weight <= 300:
            msg="Giá trị phải từ 10 đến 300."
            errors["weight"] = msg
        if not errors:
            h = height/100
            bmi = weight / h**2
            if bmi < 18.5:
                response, color = "Thiếu cân","warning"
            elif bmi < 23:
                response, color = "Bình thường", "success"
            elif bmi < 25:
                response,color = "Thừa cân", "warning"
            else:
                response, color = "Béo phì", "danger"

            result ={
                "bmi": round(bmi,1),
                "response": response,
                "color": color,
                "min_weight": round(18.5 * h **2, 1),
                "max_weight": round(22.9 * h **2, 1)
            }

    return render_template("bmi.html", errors = errors, result = result, height = height_str, weight = weight_str)

def validate_score(text):
    value = parse_number(text)
    if value is None:
        return None, "Vui lòng nhập một số."
    if not 0 <= value <= 10:
        return None, "Điểm phải từ 0 đến 10."
    return value, None


@app.route("/score", methods=["GET", "POST"])
def score():
    errors = {}
    result = None
    diem_cc_str = ""
    diem_gk_str = ""
    diem_ck_str = ""

    if request.method == "POST":
        diem_cc_str = request.form.get("cc", "").strip()
        diem_gk_str = request.form.get("gk", "").strip()
        diem_ck_str = request.form.get("ck", "").strip()

        diem_cc, err = validate_score(diem_cc_str)
        if err:
            errors["cc"] = err

        diem_gk, err = validate_score(diem_gk_str)
        if err:
            errors["gk"] = err

        diem_ck, err = validate_score(diem_ck_str)
        if err:
            errors["ck"] = err

        if not errors:
            diem = round(diem_cc * 0.1 + diem_gk * 0.3 + diem_ck * 0.6, 1)
            note = ""
            if diem_ck < 1:
                rank = "F"
                note = "Điểm thi dưới 1"
            elif diem >= 8.5:
                rank = "A"
            elif diem >= 7.0:
                rank = "B"
            elif diem >= 5.5:
                rank = "C"
            elif diem >= 4.0:
                rank = "D"
            else:
                rank = "F"

            result = {"diem": diem, "rank": rank, "note": note}

    return render_template("score.html", errors=errors, result=result,
                           diem_cc=diem_cc_str, diem_gk=diem_gk_str,
                           diem_ck=diem_ck_str)


@app.route("/calculate", methods=["GET", "POST"])
def calculate():
    return render_template("calculate.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

    return render_template("login.html")

@app.route("/logout", methods = ["GET", "POST"])
def logout():
    session.pop("username", None)
    flash("Bạn đã đăng xuất", "success")
    return redirect(url_for("index"))
                    
@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


if __name__ == '__main__':
    app.run(debug=True)