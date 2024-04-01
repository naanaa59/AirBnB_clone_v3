#!/usr/bin/python3
"""
This script create an new view for the link between
Place objects and Amenity objects
"""

from models.amenity import Amenity
from models.place import Place
from models import storage
from flask import abort, jsonify, request
from api.v1.views import app_views
from os import environ
storage_t = environ.get('HBNB_TYPE_STORAGE')


@app_views.route("/places/<place_id>/amenities", methods=[
    'GET'], strict_slashes=False)
def amenities_get(place_id):
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    if storage_t == "db":
        amenities = place.amenities
    else:
        amenities = storage.get(Amenity, amenity_ids)
    all_amenities = [
            amenity.to_dict() for amenity in place_obj.amenity_ids]
    return jsonify(all_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=[
    'DELETE'], strict_slashes=False)
def amenity_id_delete(amenity_id):
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    if storage_t == "db":
        if amenity_obj not in place_obj.amenities:
            abort(404)
        place_obj.amenities.remove(amenity_obj)
    else:
        if amenity_id not in place_obj.amenity_ids:
            abort(404)
        place_obj.amenities.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=[
    'POST'], strict_slashes=False)
def amenity_post(amenity_id):
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
        if storage_t == "db":
            if amenity_obj not in place_obj.amenities:
                place_obj.amenities.append(amenity_obj)
            else:
                return jsonify(amenity_obj.to_dict()), 200
        else:
            if amenity_id not in place_obj.amenity_ids:
                place_obj.amenity_ids.append(amenity_id)
            else:
                return jsonify(amenity_obj.to_dict()), 200
        return jsonify(amenity_obj.to_dict()), 201
