#!/usr/bin/python3
""" This script handles all default RESTFul API actions """

from models.state import State
from flask import abort, jsonify, request, make_response
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    all_states = storage.all(State).values()
    state_list = []
    for state in all_states:
        state_list.append(state.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id_get(state_id):
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)

    return jsonify(state_obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def state_id_delete(state_id):
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    storage.delete(state_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():

    if request.get_json() is None:
        abort(400, "Not a JSON")

    state_obj_dict = request.get_json()
    if 'name' not in state_obj_dict:
        abort(400, "Missing name")

    state_inst = State(**state_obj_dict)
    state_inst.save()

    return jsonify(state_inst.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_put(state_id):

    state_obj = storage.get(State, state_id)

    if not state_obj:
        abort(404)

    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key == "id" or key == "created_at" or key == "updated_at":
            pass
        setattr(state_obj, key, value)
        storage.save()

    return jsonify(state_obj.to_dict()), 201
