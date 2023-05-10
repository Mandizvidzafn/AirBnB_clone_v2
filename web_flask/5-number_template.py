#!/usr/bin/python3
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def home():
    """Returns Hello HBNB!"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Should return HBNB when the route is called"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    """Replace _ with a space and returns the text"""
    text = text.replace("_", " ")
    return f"C {text}"


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text="is_cool"):
    """Should return text if provided else returns is cool when the route is called"""
    text = text.replace("_", " ")
    return text


@app.route("/number/<int:n>", strict_slashes=False)
def n(n):
    """Should return n is a number when the route is called"""
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def n_template(n):
    """Should render the html template when the route is called"""
    return render_template("5-number.html")


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
