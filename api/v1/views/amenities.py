#!/usr/bin/python3
""" This script handles all default RESTFul API actions """

from models.amenity import Amenity
from flask import abort, jsonify, request
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    all_amenities = storage.all(Amenity).values()
    amenity_list = []
    for amenity in all_amenities:
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route(
        '/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def amenity_get_id(amenity_id):
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    return jsonify(amenity_obj.to_dict())


@app_views.route(
        '/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def amenity_id_delete(amenity_id):
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    storage.delete(amenity_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenity_post():
    try:
        if not request.get_json:
            abort(400, "Not a JSON")
    except Exception as e:
        abort(400, "Not a JSON")
    amenity_obj_dict = request.get_json()
    if 'name' not in amenity_obj_dict:
        abort(400, "Missing name")
    amenity_instance = Amenity(**amenity_obj_dict)
    amenity_instance.save()

    return jsonify(amenity_instance.to_dict), 201


@app_views.route(
        '/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def amenity_put_id(amenity_id):
    amenity_obj = storage.get(Amenity, amenity_id)

    if not amenity_obj:
        abort(404)
    try:
        if not request.get_json():
            abort(400, "Not a JSON")
    except Exception as e:
        abort(400, "Not a JSON")

    new_data = request.get_json()
    for key, value in new_data.items():
        if key == "id" or key == "created_at" or key == "updated_at":
            pass
        setattr(amenity_obj, key, value)
        storage.save()

    return jsonify(amenity_obj.to_dict()), 200
