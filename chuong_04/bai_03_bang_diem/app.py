from flask import Flask, render_template

app = Flask(__name__)

STUDENTS = [
    {"ma": "SV001", "ten": "Nguyễn Văn An", "diem": 8.5},
    {"ma": "SV002", "ten": "Trần Thị Bình", "diem": 7.0},
    {"ma": "SV003", "ten": "Lê Minh Châu", "diem": 5.5},
    {"ma": "SV004", "ten": "Phạm Quốc Dũng", "diem": 4.0},
    {"ma": "SV005", "ten": "Hoàng Thu Hà", "diem": 9.0},
]


@app.route("/")
def index():
    return render_template("bang_diem.html", students=STUDENTS)


@app.route("/rong")
def rong():
    return render_template("bang_diem.html", students=[])
