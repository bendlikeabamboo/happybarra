from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/installment_dates")
def installment_dates():
    return "<p>Hello, World!</p>"