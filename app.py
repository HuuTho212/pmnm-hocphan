from flask import Flask
from werkzeug.routing import BaseConverter
app = Flask(__name__)
@app.route("/")
@app.route("/home")
@app.route("/index")

def hello():
    return "Hello, World!"


@app.route("/chia_nhom")
def chia_nhom():
    so_bai=12
    so_nhom=0
    return f"Mỗi nhóm làm {so_bai/so_nhom} bài"

@app.route("/hello")
@app.route("/hello/<name>")
def hello_name(name="bạn"):
    return f"Xin chào, {name} !"

@app.route("/user/<username>")
def user_profile(username):
    return f"Chào {username}"


@app.route("/post/<int:post_id>")
def post_detail(post_id):
    return f"bài viết số{post_id}"

@app.route("/square/<float(signed=True):x>")
def square(x):
    return f"bình phương của {x} là {x*x}"

class ListConverter(BaseConverter):
    def __init__(self, url_map):
        super(ListConverter, self).__init__(url_map)
        self.regex = r'-?\d+(?:,-?\d+)*'

    def to_python(self, value):
        # Biến chuỗi URL thành list[int] trước khi truyền vào view function
        return [int(x) for x in value.split(',')]

    def to_url(self, value):
        return ','.join(str(x) for x in value)

app.url_map.converters['list'] = ListConverter
@app.route("/sum/<list:numbers>")
def sum(numbers):
    total = 0
    for i in numbers:
        total += i
    return f"sum = {total}"

if __name__ == '__main__':
    app.run(debug=False, port=8000)