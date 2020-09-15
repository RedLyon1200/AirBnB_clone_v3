#!7usr/bin/python3
"""
-*- Coding UTF-8 -*-
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity

opt_route = {'strict_slashes': False}


@app_views.route('/places/<place_id>/amenities', methods=['GET'], **opt_route)
def get_amenities_by_place(place_id):
    """ Retrieves the list of all Amenities objects of a place """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]

    return jsonify(amenities), 200


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE'], **opt_route)
def delete_amenity_to_place(place_id, amenity_id):
    """ Deletes a Amenity object to a Place. """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    for amenity in place.amenities:
        amenity_ = amenity.to_dict()
        if amenity_.get('id') == amenity_id:
            storage.delete(amenity)

    storage.save()

    return make_response(jsonify({}), 200)
