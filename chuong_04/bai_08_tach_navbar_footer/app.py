from flask import Flask, render_template

app = Flask(__name__)

OWNER = {"ho_ten": "Trần Đình Hữu Thọ", "email": "trandinhhuutho@gmail.com"}

PROJECTS = [
    {"ten": "MiniBlog", "mo_ta": "Blog nhỏ viết bằng Flask, Jinja2 và Bootstrap 5."},
    {"ten": "LibraryMS", "mo_ta": "Hệ thống quản lý thư viện dùng Flask."},
    {"ten": "Bảng điểm", "mo_ta": "Trang hiển thị điểm sinh viên bằng template."},
]

EDUCATION = [
    {"nam": "2022 – nay", "noi": "Trường Đại học Khoa học, Đại học Huế", "nganh": "Công nghệ thông tin"},
    {"nam": "2019 – 2022", "noi": "THPT Hai Bà Trưng", "nganh": "Khối A"},
]


@app.context_processor
def inject_owner():
    return {"owner": OWNER}


@app.route("/")
def about():
    return render_template("about.html")


@app.route("/hoc-van")
def hoc_van():
    return render_template("hoc_van.html", education=EDUCATION)


@app.route("/du-an")
def du_an():
    return render_template("du_an.html", projects=PROJECTS)


@app.route("/lien-he")
def lien_he():
    return render_template("lien_he.html")
