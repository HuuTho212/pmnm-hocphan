from flask import Flask, url_for
app = Flask(__name__)

@app.get("/login")
def login_form():
    return f"""<h1>Đăng nhập</h1>
<form method="post" action="{url_for('login_submit')}">
  <input name="username" placeholder="Tên đăng nhập">
  <button>Đăng nhập</button>
</form>"""


@app.post("/login")
def login_submit():
    return "Đã nhận yêu cầu đăng nhập (POST)"