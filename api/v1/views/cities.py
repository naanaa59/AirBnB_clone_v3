#!/usr/bin/python3
""" This script handles all default RESTFul API actions """

from models.city import City
from models.state import State
from flask import abort, jsonify, request, make_response
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def citites_get(state_id):
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    cities = state_obj.cities
    list_cities = []
    for city in cities:
        list_cities.append(city.to_dict())

    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def citites_get_id(city_id):

    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)

    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def city_id_delete(city_id):
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def city_post(state_id):
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    try:
        if not request.get_json():
            abort(400, "Not a JSON")
    except Exception as e:
        abort(400, "Not a JSON")

    city_req = request.get_json()
    if 'name' not in city_req:
        abort(400, "Missing name")

    city_inst = City(state_id=state_id, **city_req)
    city_inst.save()

    return jsonify(city_inst.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_put(city_id):

    city_obj = storage.get(City, city_id)

    if not city_obj:
        abort(404)

    try:
        if not request.get_json():
            abort(400, "Not a JSON")
    except Exception as e:
        abort(400, "Not a JSON")

    data = request.get_json()
    ignored_keys = ["id", "created_at", "updated_at", "state_id"]
    for key, value in data.items():
        if key in ignored_keys:
            pass
        setattr(city_obj, key, value)
        storage.save()

    return jsonify(city_obj.to_dict()), 201
