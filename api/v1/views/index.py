#!/usr/bin/python3
""" This script creates a route /status on the object app_views """

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """ status app """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """ stats app """
    stats = {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State)
            "users": storage.count(User)
            }
    return jsonify(stats)
