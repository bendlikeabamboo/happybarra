from flask import Flask, render_template, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/installment_dates")
def installment_dates():
    return render_template("index.html")


@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"


@app.route("/trying_out_jinja")
def trying_out_jinja():
    return render_template("index.j2")
