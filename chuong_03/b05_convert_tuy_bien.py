from flask import Flask
from werkzeug.routing import BaseConverter

class ListConverter(BaseConverter):
    """Danh sách số nguyên (có thể âm) cách nhau bởi dấu phẩy."""
    regex = r"-?\d+(?:,-?\d+)*"

    def to_python(self, value):
        return [int(item) for item in value.split(",")]

    def to_url(self, value):
        return ",".join(str(int(item)) for item in value)

app = Flask(__name__)
app.json.ensure_ascii = False
app.url_map.converters["list"] = ListConverter

@app.route("/sum/<list:numbers>")
def sum_numbers(numbers):
    return {"numbers": numbers, "sum": sum(numbers)}