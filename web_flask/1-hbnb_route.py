#!/usr/bin/python3
""" Starts a flask application """
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ returns  Hello hbnb  when / is called """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """  returns hbnb  when /hbnb is called """
    return 'HBNB'

if __name__ == "__main__":
    """ runs app """
    app.run(host='0.0.0.0', port=5000)
