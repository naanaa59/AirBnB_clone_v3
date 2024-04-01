#!/usr/bin/python3
""" This script create an new view for Review object """

from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def reviews_get(place_id):
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    reviews = place_obj.reviews
    reviews_list = []
    for review in reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def review_id(review_id):
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)

    return jsonify(review_obj.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def reviews_id_delete(review_id):
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)

    storage.delete(review_obj)
    storage.save()

    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def review_post(place_id):
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)

    try:
        if not request.get_json():
            abort(400, "Not a JSON")
    except Exception as e:
        abort(400, "Not a JSON")

    data = request.get_json()
    if "user_id" not in data:
        abort(400, "Missing user_id")

    for key, value in data.items():
        if key == "user_id":
            user_id = value

    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)

    if "text" not in data:
        abort(400, "Missing text")

    review_obj = Review(place_id=place_id, **data)
    review_obj.save()

    return jsonify(review_obj.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def review_put(review_id):

    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)
    try:
        if not request.get_json():
            abort(400, "Not a JSON")
    except Exception as e:
        abort(400, "Not a JSON")

    data = request.get_json()

    ignored_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]

    for key, value in data.items():
        if key not in ignored_keys:
            setattr(review_obj, key, value)
    storage.save()
    return jsonify(review_obj.to_dict()), 200
