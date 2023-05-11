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


@app.route('/c/<text>', strict_slashes=False)
def c_is_fun(text):
    """ replaces _ in text with space when route is called """
    return "C " + text.replace('_', ' ')


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_is_cool(text='is_cool'):
    """ replaces _ in text with space when route is called """
    return "Python " + text.replace('_', ' ')

if __name__ == "__main__":
    """ runs app """
    app.run(host='0.0.0.0', port=5000)
