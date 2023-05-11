#!/usr/bin/python3
""" start flask web app """
from ..models import storage
from ..models.state import State
from ..models.city import City
from ..models.amenity import Amenity
from ..models.place import Place

from flask import Flask, render_template
app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """ should remove the current SQLAlchemy session """
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ renders the page """
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    city_state = []

    for state in states:
        city_state.append([state, sorted(state.cities, key=lambda k: k.name)])

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    return render_template('100-hbnb.html', states=city_state, amenities=amenities, places=places)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
