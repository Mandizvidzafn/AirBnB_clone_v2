#!/usr/bin/python3
from flask import Flask

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


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
