#!/usr/bin/python3
""" This script handles all default RESTFul API actions """

from flask import abort, jsonify, request
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    all_users = storage.all(User).values()
    user_list = []
    for user in all_users:
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route(
        '/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_get_id(user_id):
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    return jsonify(user_obj.to_dict())


@app_views.route(
        '/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def user_id_delete(user_id):
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    storage.delete(user_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_post():
    try:
        if not request.get_json():
            abort(400, "Not a JSON")
    except Exception as e:
        abort(400, "Not a JSON")
    user_obj_dict = request.get_json()
    if 'email' not in user_obj_dict:
        abort(400, "Missing email")
    if 'password' not in user_obj_dict:
        abort(400, "Missing password")
    user_instance = User(**user_obj_dict)
    user_instance.save()

    return jsonify(user_instance.to_dict()), 201


@app_views.route(
        '/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_put_id(user_id):
    user_obj = storage.get(User, user_id)

    if not user_obj:
        abort(404)
    try:
        if not request.get_json():
            abort(400, "Not a JSON")
    except Exception:
        abort(400, "Not a JSON")

    new_data = request.get_json()
    for key, value in new_data.items():
        if key not in ('id, email, created_at, updated_at'):
            setattr(user_obj, key, value)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
