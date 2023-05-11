#!/usr/bin/python3
""" start flask web app """
from ..models import storage
from ..models.state import State
from flask import Flask, render_template
app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """ should remove the current SQLAlchemy session """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """ renders html page with a list of states """
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    return render_template('7-states_list.html', states=states)



@app.route('/cities_by_states', strict_slashes=False)
def cities_list():
    """ renders html page with a list of cities by state """
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    cities_states = []
    for state in states:
        cities_states.append([state, sorted(state.cities, key=lambda k: k.name)])
    return render_template('8-cities_by_states.html',
                           states=cities_states,
                           h1="States")


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
