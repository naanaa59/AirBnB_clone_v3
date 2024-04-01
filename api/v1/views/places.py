#!/usr/bin/python3
""" This script handles all default RESTFul API actions """

from models.city import City
from models.place import Place
from models.user import User
from flask import abort, jsonify, request, make_response
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_get(city_id):
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    places = city_obj.places
    list_places = []
    for place in places:
        list_places.append(place.to_dict())

    return jsonify(list_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_get_id(place_id):

    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)

    return jsonify(place_obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_id_delete(place_id):
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    storage.delete(place_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    try:
        if not request.get_json():
            abort(400, "Not a JSON")
    except Exception as e:
        abort(400, "Not a JSON")

    place_req = request.get_json()
    if 'user_id' not in place_req:
        abort(400, "Missing user_id")

    for key, value in place_req.items():
        if key == "user_id":
            user_id = value

    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    if 'name' not in place_req:
        abort(400, "Missing name")
    place_inst = Place(city_id=city_id, **place_req)
    place_inst.save()

    return jsonify(place_inst.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_put(place_id):

    place_obj = storage.get(Place, place_id)

    if not city_obj:
        abort(404)

    try:
        if not request.get_json():
            abort(400, "Not a JSON")
    except Exception as e:
        abort(400, "Not a JSON")

    data = request.get_json()
    ignored_keys = ["id", "created_at", "updated_at", "user_id", "city_id"]
    for key, value in data.items():
        if key in ignored_keys:
            pass
        setattr(place_obj, key, value)
        storage.save()

    return jsonify(city_obj.to_dict()), 200
