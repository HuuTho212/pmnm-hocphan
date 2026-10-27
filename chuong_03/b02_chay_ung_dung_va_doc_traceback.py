from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    return "<h1>Xin chào, Flask!</h1>"

@app.route("/chia-nhom")
def chia_nhom():
    so_bai = 12
    so_nhom = 0
    return f"Mỗi nhóm làm {so_bai / so_nhom} bài"