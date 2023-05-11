#!/usr/bin/python3
""" Starts a flask application """
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ return  Hello hbnb  when / is called """
    return 'Hello HBNB!'

if __name__ == "__main__":
    """ run the app """
    app.run(host='0.0.0.0', port=5000)
