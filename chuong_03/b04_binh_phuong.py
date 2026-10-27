from flask import Flask
app = Flask(__name__)

@app.route("/square/<int(signed=True):n>")
def square(n):
    return str(n * n)