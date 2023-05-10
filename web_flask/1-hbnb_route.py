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


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
